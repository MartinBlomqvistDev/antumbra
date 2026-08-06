"""Export the web layer's data from the tested model.

Step 15 of the pipeline; run 10, 12 and dbt build first. The site never
queries BigQuery: this step reads the dbt-tested marts once, recomputes the
same numbers locally from the Parquet warehouse, and refuses to write
anything if the two disagree. What reaches the site has therefore passed the
dbt tests in the cloud and a second, independent computation on this machine.

Outputs, all committed, all deterministic (no timestamps, stable ordering):

    web/public/data/country_year.json      the mart_country_year rows
    web/public/data/headline.json          corpus-wide totals
    web/public/data/underlag/<slug>.json   per country: audits, their
                                           recommendations, the cited
                                           paragraphs verbatim, the member
                                           state responses, and the source
                                           document's sha256
    web/public/data/manifest.json          sha256, bytes and rows per file

Credentials as in step 12, read from the environment and never the repo:

    ANTUMBRA_GCP_PROJECT             the project id
    GOOGLE_APPLICATION_CREDENTIALS   path to the service account key file

Running without them prints the plan and exits without touching anything.

Usage:
    python pipeline/15_export_web_data.py [--dry-run]
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import unicodedata
from collections import defaultdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
WAREHOUSE = DATA / "warehouse"
OUT_DIR = ROOT / "web" / "public" / "data"
MARTS_DATASET = "dgsante_marts"
SHARE_DECIMALS = 4

COUNT_COLUMNS = (
    "recommendations",
    "audits",
    "stating_their_basis",
    "answered",
    "confirmed",
)


def slugify(country: str) -> str:
    """A stable ascii slug for a country name, used as a file name.

    Args:
        country: The country name as the dimension spells it.

    Returns:
        Lowercase ascii with single hyphens, e.g. "bosnia-and-herzegovina".
    """
    ascii_name = (
        unicodedata.normalize("NFKD", country).encode("ascii", "ignore").decode()
    )
    pieces = "".join(ch if ch.isalnum() else " " for ch in ascii_name.lower()).split()
    return "-".join(pieces)


def read_jsonl(path: Path) -> list[dict]:
    """Read one JSONL file into a list of rows."""
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line
    ]


def load_table(name: str) -> list[dict]:
    """Read one warehouse table written by step 10."""
    import pyarrow.parquet as pq

    return pq.read_table(WAREHOUSE / f"{name}.parquet").to_pylist()


def staged_audits(dim_audit: list[dict], dim_country: list[dict]) -> list[dict]:
    """Join the audit dimension with its country, as stg_audits does."""
    countries = {c["country_key"]: c for c in dim_country}
    rows = []
    for audit in dim_audit:
        country = countries.get(audit["country_key"], {})
        rows.append(
            {
                **audit,
                "country": country.get("country"),
                "in_eu27": country.get("in_eu27"),
            }
        )
    return rows


def local_country_year(
    fact_recommendation: list[dict], audits: list[dict]
) -> list[dict]:
    """Recompute mart_country_year from the local warehouse.

    Mirrors the dbt model exactly: recommendations inner-joined to audits,
    grouped by country, EU-27 flag and audit year, with the counts the mart
    publishes. Shares are left out here; they are derived from the counts.

    Args:
        fact_recommendation: The recommendation fact rows.
        audits: The staged audit rows from staged_audits().

    Returns:
        One row per (country, in_eu27, audit_year), sorted.
    """
    audits_by_key = {a["audit_key"]: a for a in audits}
    groups: dict[tuple, dict[str, Any]] = {}
    for rec in fact_recommendation:
        audit = audits_by_key.get(rec["audit_key"])
        if audit is None:
            continue
        key = (audit["country"], audit["in_eu27"], audit["year"])
        group = groups.setdefault(
            key,
            {
                "country": audit["country"],
                "in_eu27": audit["in_eu27"],
                "audit_year": audit["year"],
                "recommendations": 0,
                "_audit_keys": set(),
                "stating_their_basis": 0,
                "answered": 0,
                "confirmed": 0,
            },
        )
        group["recommendations"] += 1
        group["_audit_keys"].add(rec["audit_key"])
        group["stating_their_basis"] += 1 if rec["states_its_basis"] else 0
        group["answered"] += 1 if rec["is_answered"] else 0
        group["confirmed"] += 1 if rec["answer_confirmed_by_text"] else 0
    rows = []
    for group in groups.values():
        group["audits"] = len(group.pop("_audit_keys"))
        rows.append(group)
    return sorted(rows, key=lambda r: (r["country"] or "", r["audit_year"] or 0))


def reconcile(cloud: list[dict], local: list[dict]) -> None:
    """Stop the export if the marts and the local recomputation disagree.

    Args:
        cloud: mart_country_year rows from BigQuery.
        local: The rows from local_country_year().

    Raises:
        ValueError: On the first group or count that differs.
    """

    def index(rows: list[dict]) -> dict[tuple, dict]:
        return {(r["country"], r["audit_year"]): r for r in rows}

    cloud_by_key, local_by_key = index(cloud), index(local)
    if cloud_by_key.keys() != local_by_key.keys():
        odd = cloud_by_key.keys() ^ local_by_key.keys()
        raise ValueError(f"cloud and local group keys differ: {sorted(odd)[:5]}")
    for key, cloud_row in cloud_by_key.items():
        local_row = local_by_key[key]
        for column in COUNT_COLUMNS:
            if cloud_row[column] != local_row[column]:
                raise ValueError(
                    f"{key} {column}: mart says {cloud_row[column]}, "
                    f"local warehouse says {local_row[column]}"
                )


def with_shares(rows: list[dict]) -> list[dict]:
    """Derive the published shares from the verified counts."""
    published = []
    for row in rows:
        total = row["recommendations"]
        published.append(
            {
                "country": row["country"],
                "slug": slugify(row["country"]),
                "in_eu27": row["in_eu27"],
                "audit_year": row["audit_year"],
                **{column: row[column] for column in COUNT_COLUMNS},
                "share_stating_their_basis": round(
                    row["stating_their_basis"] / total, SHARE_DECIMALS
                ),
                "share_answered": round(row["answered"] / total, SHARE_DECIMALS),
            }
        )
    return published


def build_underlag(
    fact_recommendation: list[dict],
    fact_citation: list[dict],
    fact_commitment: list[dict],
    dim_paragraph: list[dict],
    audits: list[dict],
    sha_by_path: dict[str, str],
) -> dict[str, dict]:
    """Assemble the per-country underlag, the chain behind every number.

    Args:
        fact_recommendation: Recommendation facts.
        fact_citation: Citation edges.
        fact_commitment: Member state responses.
        dim_paragraph: The paragraph dimension, texts included.
        audits: Staged audit rows.
        sha_by_path: Document sha256 by repository path.

    Returns:
        One country object per slug, audits sorted by reference.
    """
    paragraphs = {p["paragraph_key"]: p for p in dim_paragraph}
    audits_by_key = {a["audit_key"]: a for a in audits}

    citations_by_rec: dict[int, list[dict]] = defaultdict(list)
    for edge in fact_citation:
        paragraph = paragraphs.get(edge["paragraph_key"])
        citations_by_rec[edge["recommendation_key"]].append(
            {
                "cites": edge["cites"],
                "number": edge["paragraph_number"],
                "resolved": edge["resolved"],
                "kind": paragraph["kind"] if paragraph else None,
                "section": paragraph["section"] if paragraph else None,
                "text": paragraph["text"] if paragraph else None,
            }
        )

    responses_by_rec: dict[int, list[dict]] = defaultdict(list)
    for row in fact_commitment:
        if row["recommendation_key"] is None:
            continue
        responses_by_rec[row["recommendation_key"]].append(
            {
                "response": row["response"],
                "plan_path": row["plan_path"],
                "confirmed_by_text": row["confirmed_by_text"],
            }
        )

    reports: dict[tuple[str, str], dict] = {}
    for rec in fact_recommendation:
        audit = audits_by_key.get(rec["audit_key"])
        if audit is None or audit["country"] is None:
            continue
        report_key = (audit["country"], rec["report_path"])
        report = reports.setdefault(
            report_key,
            {
                "ref": audit["ref"],
                "year": audit["year"],
                "title": audit["title"],
                "report_path": rec["report_path"],
                "sha256": sha_by_path.get(rec["report_path"]),
                "recommendations": [],
            },
        )
        report["recommendations"].append(
            {
                "number": rec["number"],
                "text": rec["text"],
                "legal_basis": rec["legal_basis"],
                "states_its_basis": rec["states_its_basis"],
                "is_answered": rec["is_answered"],
                "answer_confirmed_by_text": rec["answer_confirmed_by_text"],
                "citations": sorted(
                    citations_by_rec.get(rec["recommendation_key"], []),
                    key=lambda c: (c["number"] is None, c["number"]),
                ),
                "responses": responses_by_rec.get(rec["recommendation_key"], []),
            }
        )

    countries: dict[str, dict] = {}
    for (country, _), report in sorted(reports.items()):
        slug = slugify(country)
        entry = countries.setdefault(
            slug,
            {
                "country": country,
                "in_eu27": next(
                    a["in_eu27"] for a in audits if a["country"] == country
                ),
                "audits": [],
            },
        )
        report["recommendations"].sort(key=lambda r: r["number"])
        entry["audits"].append(report)
    return countries


def reconcile_underlag(countries: dict[str, dict], mart_rows: list[dict]) -> None:
    """Assert the underlag carries exactly the rows the mart counted.

    Args:
        countries: The per-country objects from build_underlag().
        mart_rows: The verified mart_country_year rows.

    Raises:
        ValueError: If any (country, year) recommendation count differs.
    """
    counted: dict[tuple, int] = defaultdict(int)
    for entry in countries.values():
        for audit in entry["audits"]:
            counted[(entry["country"], audit["year"])] += len(audit["recommendations"])
    for row in mart_rows:
        key = (row["country"], row["audit_year"])
        if counted.get(key, 0) != row["recommendations"]:
            raise ValueError(
                f"underlag holds {counted.get(key, 0)} recommendations for "
                f"{key}, the mart says {row['recommendations']}"
            )


def fetch_marts(project: str) -> tuple[list[dict], dict]:
    """Read the tested marts from BigQuery, once.

    Args:
        project: The GCP project id.

    Returns:
        The mart_country_year rows and the mart_chain totals.
    """
    from google.cloud import bigquery

    client = bigquery.Client(project=project, location="EU")
    country_year = [
        dict(row)
        for row in client.query(
            f"select country, in_eu27, audit_year, recommendations, audits,"
            f" stating_their_basis, answered, confirmed"
            f" from `{project}.{MARTS_DATASET}.mart_country_year`"
            f" order by country, audit_year"
        ).result()
    ]
    chain = dict(
        next(
            iter(
                client.query(
                    f"select count(*) as recommendations,"
                    f" sum(case when chain_closes then 1 else 0 end)"
                    f" as chain_closes,"
                    f" sum(citations) as citations,"
                    f" sum(citations_resolved) as citations_resolved"
                    f" from `{project}.{MARTS_DATASET}.mart_chain`"
                ).result()
            )
        )
    )
    return country_year, chain


def local_chain_totals(
    fact_recommendation: list[dict],
    fact_citation: list[dict],
    fact_commitment: list[dict],
) -> dict:
    """Recompute the mart_chain totals from the local warehouse."""
    resolved_by_rec: dict[int, int] = defaultdict(int)
    for edge in fact_citation:
        if edge["resolved"]:
            resolved_by_rec[edge["recommendation_key"]] += 1
    answered_recs = {
        row["recommendation_key"]
        for row in fact_commitment
        if row["recommendation_key"] is not None
    }
    chain_closes = sum(
        1
        for rec in fact_recommendation
        if rec["states_its_basis"]
        and resolved_by_rec.get(rec["recommendation_key"], 0) > 0
        and rec["recommendation_key"] in answered_recs
    )
    return {
        "recommendations": len(fact_recommendation),
        "chain_closes": chain_closes,
        "citations": len(fact_citation),
        "citations_resolved": sum(1 for e in fact_citation if e["resolved"]),
    }


def write_json(path: Path, payload: object, *, compact: bool) -> dict:
    """Write one JSON file and describe it for the manifest.

    Args:
        path: Where to write.
        payload: What to write.
        compact: Without indentation, for the larger underlag files.

    Returns:
        The file's manifest entry.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(
        payload,
        ensure_ascii=False,
        indent=None if compact else 2,
        separators=(",", ":") if compact else None,
    )
    data = (text + "\n").encode("utf-8")
    path.write_bytes(data)
    rows = len(payload) if isinstance(payload, list) else 1
    return {
        "path": path.relative_to(ROOT).as_posix(),
        "bytes": len(data),
        "rows": rows,
        "sha256": hashlib.sha256(data).hexdigest(),
    }


def main() -> int:
    """Verify cloud against local, then export the site's data."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="print the plan and exit without contacting BigQuery",
    )
    args = parser.parse_args()

    project = os.environ.get("ANTUMBRA_GCP_PROJECT")
    credentials = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    if args.dry_run or not project or not credentials:
        print(
            "would verify mart_country_year and mart_chain against the local\n"
            f"warehouse and write JSON under {OUT_DIR.relative_to(ROOT)}/;\n"
            "set ANTUMBRA_GCP_PROJECT and GOOGLE_APPLICATION_CREDENTIALS to run"
        )
        return 0

    dim_country = load_table("dim_country")
    dim_audit = load_table("dim_audit")
    dim_paragraph = load_table("dim_paragraph")
    fact_recommendation = load_table("fact_recommendation")
    fact_citation = load_table("fact_citation")
    fact_commitment = load_table("fact_commitment")
    audits = staged_audits(dim_audit, dim_country)
    sha_by_path = {
        row["path"]: row["sha256"]
        for row in read_jsonl(DATA / "dgsante_manifest.jsonl")
    }

    cloud_rows, cloud_chain = fetch_marts(project)
    local_rows = local_country_year(fact_recommendation, audits)
    reconcile(cloud_rows, local_rows)
    local_chain = local_chain_totals(
        fact_recommendation, fact_citation, fact_commitment
    )
    for column, local_value in local_chain.items():
        if int(cloud_chain[column]) != local_value:
            raise ValueError(
                f"mart_chain {column}: mart says {cloud_chain[column]}, "
                f"local warehouse says {local_value}"
            )
    print(
        f"verified {len(cloud_rows)} country-year groups and "
        f"{local_chain['recommendations']} chain rows against BigQuery"
    )

    countries = build_underlag(
        fact_recommendation,
        fact_citation,
        fact_commitment,
        dim_paragraph,
        audits,
        sha_by_path,
    )
    published = with_shares(local_rows)
    reconcile_underlag(countries, published)

    years = [a["year"] for a in dim_audit if a["year"] is not None]
    headline = {
        "audits": len(dim_audit),
        "countries": len(dim_country),
        "paragraphs": len(dim_paragraph),
        "years": {"min": min(years), "max": max(years)},
        **local_chain,
        "share_citations_resolved": round(
            local_chain["citations_resolved"] / local_chain["citations"],
            SHARE_DECIMALS,
        ),
        "commitments": len(fact_commitment),
    }

    manifest_entries = [
        write_json(OUT_DIR / "country_year.json", published, compact=False),
        write_json(OUT_DIR / "headline.json", headline, compact=False),
    ]
    for slug in sorted(countries):
        manifest_entries.append(
            write_json(
                OUT_DIR / "underlag" / f"{slug}.json",
                countries[slug],
                compact=True,
            )
        )
    write_json(
        OUT_DIR / "manifest.json",
        {"files": manifest_entries},
        compact=False,
    )
    total_bytes = sum(entry["bytes"] for entry in manifest_entries)
    print(
        f"wrote {len(manifest_entries) + 1} files, "
        f"{total_bytes / 1_048_576:.1f} MiB -> {OUT_DIR.relative_to(ROOT)}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
