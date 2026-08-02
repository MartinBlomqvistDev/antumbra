"""Build the dimensional model over the DG SANTE layer.

Step 10 of the pipeline; run 07 to 09 first. The parsed layer is a set of
JSONL files shaped by how the documents read. This step reshapes it into a
star: conformed dimensions for country, audit and paragraph, and one fact
table each for recommendations, citations and commitments.

The model is written as Parquet under data/warehouse/, which is a build
artefact and stays out of the repository. What is committed is
data/dgsante_warehouse_manifest.json: the tables, their columns, their row
counts and their keys, so the shape of the model can be reviewed and tested
without the binaries.

An unresolved citation keeps a null paragraph key rather than being dropped.
The count of what could not be joined is part of the result.

Usage:
    python pipeline/10_build_warehouse.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pyarrow as pa
import pyarrow.parquet as pq

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
OUT_DIR = DATA / "warehouse"
OUT_MANIFEST = DATA / "dgsante_warehouse_manifest.json"

EU27 = {
    "Austria",
    "Belgium",
    "Bulgaria",
    "Croatia",
    "Cyprus",
    "Czechia",
    "Czech Republic",
    "Denmark",
    "Estonia",
    "Finland",
    "France",
    "Germany",
    "Greece",
    "Hungary",
    "Ireland",
    "Italy",
    "Latvia",
    "Lithuania",
    "Luxembourg",
    "Malta",
    "Netherlands",
    "Poland",
    "Portugal",
    "Romania",
    "Slovakia",
    "Slovenia",
    "Spain",
    "Sweden",
}


def read_jsonl(name: str) -> list[dict]:
    """Read one derived dataset."""
    path = DATA / name
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line
    ]


def audit_year(ref: str) -> int | None:
    """Year from an audit reference, in either of the two formats."""
    if ref.startswith("CT-"):
        parts = ref.split("-")
        return int(parts[1]) if len(parts) > 1 and parts[1].isdigit() else None
    return int(ref[:4]) if ref[:4].isdigit() else None


def build_dimensions(details: list[dict], paragraphs: list[dict]) -> dict[str, list]:
    """Build the conformed dimensions.

    Args:
        details: Harvested detail records, one per audit.
        paragraphs: Numbered paragraphs, one per row.

    Returns:
        The country, audit and paragraph dimensions as lists of rows.
    """
    countries = sorted({row["country"] for row in details if row.get("country")})
    dim_country = [
        {"country_key": index, "country": name, "in_eu27": name in EU27}
        for index, name in enumerate(countries, start=1)
    ]
    country_key = {row["country"]: row["country_key"] for row in dim_country}

    dim_audit = []
    audit_key = {}
    for index, row in enumerate(sorted(details, key=lambda r: r["ref"]), start=1):
        audit_key[row["ref"]] = index
        dim_audit.append(
            {
                "audit_key": index,
                "ref": row["ref"],
                "country_key": country_key.get(row.get("country")),
                "year": audit_year(row["ref"]),
                "audit_period": row.get("audit_period") or None,
                "published_date": row.get("published_date") or None,
                "title": (row.get("title") or "")[:500] or None,
                "reference_format": "CT" if row["ref"].startswith("CT-") else "numeric",
            }
        )

    dim_paragraph = []
    paragraph_key = {}
    for index, row in enumerate(paragraphs, start=1):
        key = (row["path"], row["number"])
        # A reissued report can repeat a number; the first reading wins and
        # the duplicate is not given a key of its own.
        if key in paragraph_key:
            continue
        paragraph_key[key] = index
        dim_paragraph.append(
            {
                "paragraph_key": index,
                "audit_key": audit_key.get(row["ref"]),
                "report_path": row["path"],
                "number": row["number"],
                "kind": row["kind"],
                "section": row["section"] or None,
                "label_heading": row["label_heading"] or None,
                "text": row["text"],
            }
        )

    return {
        "dim_country": dim_country,
        "dim_audit": dim_audit,
        "dim_paragraph": dim_paragraph,
        "_audit_key": audit_key,
        "_paragraph_key": paragraph_key,
    }


def build_facts(
    recommendations: list[dict],
    graph: list[dict],
    plans: list[dict],
    audit_key: dict[str, int],
    paragraph_key: dict[tuple[str, int], int],
) -> dict[str, list]:
    """Build the fact tables at their stated grains.

    Args:
        recommendations: One row per recommendation.
        graph: One row per citation edge.
        plans: One row per answered recommendation.
        audit_key: Audit surrogate keys by reference.
        paragraph_key: Paragraph surrogate keys by report path and number.

    Returns:
        The recommendation, citation and commitment facts.
    """
    answered = {(row["ref"], row["recommendation"]) for row in plans}
    confirmed = {
        (row["ref"], row["recommendation"])
        for row in plans
        if row["link_confirmed_by_text"]
    }

    fact_recommendation = []
    recommendation_key = {}
    # An audit can have two English reports, so the file path is what makes a
    # recommendation unique. The reference is kept as a second way in for the
    # plans, which name the audit rather than the file.
    by_reference: dict[tuple[str, int], int] = {}
    for index, row in enumerate(recommendations, start=1):
        key = (row["path"], row["number"])
        recommendation_key[key] = index
        natural = (row["ref"], row["number"])
        by_reference.setdefault(natural, index)
        fact_recommendation.append(
            {
                "recommendation_key": index,
                "audit_key": audit_key.get(row["ref"]),
                "report_path": row["path"],
                "number": row["number"],
                "text": row["text"],
                "legal_basis": row["legal_basis"],
                "parse_method": row["parse_method"],
                "conclusions_cited": len(row["based_on_conclusions"]),
                "findings_cited": len(row["associated_findings"]),
                "states_its_basis": bool(row["based_on_conclusions"]),
                "is_answered": natural in answered,
                "answer_confirmed_by_text": natural in confirmed,
            }
        )

    fact_citation = []
    for row in graph:
        source = recommendation_key.get((row["path"], row["recommendation"]))
        if source is None:
            continue
        target = paragraph_key.get((row["path"], row["paragraph"]))
        fact_citation.append(
            {
                "recommendation_key": source,
                "paragraph_key": target,
                "audit_key": audit_key.get(row["ref"]),
                "cites": row["cites"],
                "paragraph_number": row["paragraph"],
                "resolved": target is not None,
                # Whether the paragraph's own heading agrees with what the
                # citation calls it. Null where nothing resolved or no
                # heading said.
                "heading_agrees": (
                    None
                    if target is None or row["paragraph_kind"] == "unlabelled"
                    else row["paragraph_kind"] == row["cites"]
                ),
            }
        )

    fact_commitment = []
    for row in plans:
        source = by_reference.get((row["ref"], row["recommendation"]))
        fact_commitment.append(
            {
                "recommendation_key": source,
                "audit_key": audit_key.get(row["ref"]),
                "plan_path": row["plan_path"],
                "recommendation_number": row["recommendation"],
                "response": row["response"],
                "text_similarity": row["text_similarity"],
                "confirmed_by_text": row["link_confirmed_by_text"],
            }
        )

    return {
        "fact_recommendation": fact_recommendation,
        "fact_citation": fact_citation,
        "fact_commitment": fact_commitment,
    }


def write_table(name: str, rows: list[dict]) -> dict:
    """Write one table to Parquet and describe it.

    Args:
        name: Table name.
        rows: Its rows.

    Returns:
        The table's entry for the manifest.
    """
    table = pa.Table.from_pylist(rows)
    pq.write_table(table, OUT_DIR / f"{name}.parquet", compression="zstd")
    return {
        "table": name,
        "rows": table.num_rows,
        "columns": [
            {"name": field.name, "type": str(field.type)} for field in table.schema
        ],
    }


def main() -> int:
    """Build the star schema and write its manifest."""
    details = read_jsonl("dgsante_details.jsonl")
    paragraphs = read_jsonl("dgsante_paragraphs.jsonl")
    recommendations = read_jsonl("dgsante_recommendations.jsonl")
    graph = read_jsonl("dgsante_graph.jsonl")
    plans = read_jsonl("dgsante_action_plans.jsonl")

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    dims = build_dimensions(details, paragraphs)
    facts = build_facts(
        recommendations,
        graph,
        plans,
        dims.pop("_audit_key"),
        dims.pop("_paragraph_key"),
    )

    manifest = {"tables": []}
    for name, rows in {**dims, **facts}.items():
        entry = write_table(name, rows)
        manifest["tables"].append(entry)
        print(f"{name}: {entry['rows']} rows")

    citations = facts["fact_citation"]
    manifest["measures"] = {
        "recommendations": len(facts["fact_recommendation"]),
        "recommendations_stating_their_basis": sum(
            1 for r in facts["fact_recommendation"] if r["states_its_basis"]
        ),
        "recommendations_answered": sum(
            1 for r in facts["fact_recommendation"] if r["is_answered"]
        ),
        "citations": len(citations),
        "citations_resolved": sum(1 for r in citations if r["resolved"]),
        "commitments": len(facts["fact_commitment"]),
    }
    OUT_MANIFEST.write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(f"manifest -> {OUT_MANIFEST.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
