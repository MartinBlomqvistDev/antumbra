"""Export the Swedish openness layer for the website.

The figures are the ones each authority already received in its P12 packet, and
they come from the same functions that wrote the packets, in step 36. The site
renders this file and computes nothing of its own: a second computation path
would be a second chance to disagree with the record.

Three things are added here that a letter does not carry.

The first is an interval. Risk 10 in ``docs/BEGARANMALL.md`` has the
countermeasure "intervall redovisas alltid; indexet rangordnar inte myndigheter
vars intervall överlappar", and the sent tables carry an order without one. The
published order is the order the authorities were given, so their letters stay
true, and the interval is added beside it with the overlap written out.

The second is each authority's reply, verbatim, from ``data/p12_svar.jsonl``,
or the note that no reply has come in. P12: "Svaren publiceras oavkortade."

The third is the checksum of the letter the authority was actually sent, from
``data/p12_avsant_manifest.jsonl``. Step 36 has been corrected twice since the
packets went out, so the letters it writes today are not the letters that were
sent; the sent ones are archived and both corrections are in the log.

Writes ``web/public/data/sverige.json``, beside the DG SANTE export.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import math
import sys
from collections import defaultdict
from datetime import date
from pathlib import Path
from statistics import median
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

MASKING = ROOT / "data" / "maskning.jsonl"
CONTRAST = ROOT / "data" / "kontrast.jsonl"
REPLIES = ROOT / "data" / "p12_svar.jsonl"
SENT = ROOT / "data" / "p12_avsant_manifest.jsonl"
ANNEXES = ROOT / "data" / "bilagor.jsonl"
LOG = ROOT / "data" / "protokoll_logg.jsonl"
CORRESPONDENCE = ROOT / "data" / "korrespondens.jsonl"
OUTGOING = ROOT / "data" / "korrespondens_utgaende.jsonl"
PAIRS = ROOT / "data" / "dubbelforekomst.jsonl"
OUT = ROOT / "web" / "public" / "data" / "sverige.json"

# Facts about the dispatch rather than choices made here: the packets went out
# on 2 October 2026 and the letters name 23 October as the last day to reply.
# Tillämpningsnot 8 puts the earliest publication the day after.
P12_SENT = "2026-10-02"
P12_DEADLINE = "2026-10-23"
PUBLICATION_FLOOR = "2026-10-24"
# The floor is the rule, the chosen day is the decision; see docs/PUBLICERING.md.
PUBLICATION_DAY = "2026-10-26"

CLASSES = ("A", "B")


def load_step36() -> Any:
    """Import step 36, whose name starts with a digit, the way steps 33 and 38 do."""
    path = ROOT / "pipeline" / "36_build_p12_packets.py"
    spec = importlib.util.spec_from_file_location("p12_packets", path)
    if spec is None or spec.loader is None:  # pragma: no cover - import guard
        raise SystemExit(f"kan inte importera {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules["p12_packets"] = module
    spec.loader.exec_module(module)
    return module


def read(path: Path) -> list[dict]:
    """Every row of a JSONL file."""
    return [
        json.loads(line)
        for line in path.read_text("utf-8").splitlines()
        if line.strip()
    ]


def wilson(successes: int, total: int) -> tuple[float, float]:
    """A 95 per cent Wilson score interval for a share.

    Wilson rather than the normal approximation because the shares sit at nought
    and one, where the normal interval runs outside the unit interval and has no
    width at all at the endpoints. Five documents giving five maskings is the
    common case here, and the interval has to say that such a county cannot be
    separated from one at 80 per cent.

    The interval treats one authority's documents as independent draws, which
    they are not: they are consecutive cases, often from the same officer. It is
    therefore a floor on the uncertainty rather than a statement about the
    authority's practice, and the site says so where it prints it.
    """
    if total == 0:
        return (0.0, 1.0)
    z = 1.959963984540054
    share = successes / total
    denominator = 1 + z**2 / total
    centre = share + z**2 / (2 * total)
    spread = z * math.sqrt(share * (1 - share) / total + z**2 / (4 * total**2))
    return ((centre - spread) / denominator, (centre + spread) / denominator)


def overlaps(first: tuple[float, float], second: tuple[float, float]) -> bool:
    """Whether two intervals share a value, so the measure does not separate them."""
    return first[0] <= second[1] and second[0] <= first[1]


def ranking_rows(step36: Any, masking: list[dict], klass: str) -> list[dict]:
    """The sent order for one class, with each authority's interval beside it."""
    rows: list[dict] = []
    place = 0
    previous: float | None = None
    for index, (slug, documents, share) in enumerate(
        step36.ranking(masking, klass), start=1
    ):
        if previous is None or share != previous:
            place = index
            previous = share
        masked = round(share * documents)
        low, high = wilson(masked, documents)
        rows.append(
            {
                "plats": place,
                "slug": slug,
                "namn": step36.NAME.get(slug, slug),
                "dokument": documents,
                "maskade": masked,
                "andel": share,
                "andel_text": step36.percent(share),
                "intervall": [low, high],
                "intervall_text": f"{step36.percent(low)} till {step36.percent(high)}",
            }
        )
    return rows


def separated(rows: list[dict]) -> int:
    """How many pairs in a class the measure actually separates."""
    pairs = 0
    for index, row in enumerate(rows):
        for other in rows[index + 1 :]:
            if not overlaps(
                (row["intervall"][0], row["intervall"][1]),
                (other["intervall"][0], other["intervall"][1]),
            ):
                pairs += 1
    return pairs


def class_figures(
    step36: Any, masking: list[dict], slug: str, klass: str
) -> dict | None:
    """One authority's measured documents in one class."""
    rows = step36.masking_rows(masking, slug, klass)
    if not rows:
        return None
    masked = sum(1 for row in rows if row["masked"])
    area = sum(row["masked_area_share"] for row in rows) / len(rows)
    low, high = wilson(masked, len(rows))
    return {
        "dokument": len(rows),
        "maskade": masked,
        "andel": masked / len(rows),
        "andel_text": step36.percent(masked / len(rows)),
        "yta": area,
        "yta_text": step36.area_percent(area),
        "intervall": [low, high],
        "intervall_text": f"{step36.percent(low)} till {step36.percent(high)}",
    }


def without_measurement(log: list[dict], authority: str) -> str | None:
    """Why an authority carries no redaction figures, read out of the log.

    An authority with no documents in the measurement is the single most
    misreadable row on the page: an empty cell looks like a finding about the
    authority when it is a consequence of the protocol. P5 is explicit that the
    loss is reported openly and never hidden by silencing the denominator, so
    the reason is carried as a key and the page writes it out. The key is read
    from the events, where deciding it here would be wrong: a waiver is P5's
    ``avstående``, and a
    request for figures is an ``avsändning`` of request C.
    """
    own = [row for row in log if row["myndighet"] == authority]
    if any(row["handelse"] == "avsändning" and row["begaran"] == "C" for row in own):
        return "statistik"
    if any(row["handelse"] == "avstående" for row in own):
        return "avgiftsstoppad"
    return None


def merged(log: list[dict], authority: str) -> bool:
    """Whether P0b was flagged for this authority, so one class carries both."""
    return any(
        row["myndighet"] == authority and row["handelse"] == "sammanslagning enligt P0b"
        for row in log
    )


def contrast_summary(authorities: list[dict]) -> dict:
    """The P1 contrast: the difference inside one authority, over counties with both.

    P1 defines the contrast as the difference in redaction between class A and
    class B within the same authority, so it is computed per authority and then
    summarised with a median. A county that delivered in one class only carries
    no contrast and is left out rather than counted as zero.
    """
    shares = []
    areas = []
    share_higher = []
    area_higher = []
    for item in authorities:
        first = item["klasser"].get("A")
        second = item["klasser"].get("B")
        if not first or not second:
            continue
        shares.append((first["andel"] - second["andel"]) * 100)
        areas.append((first["yta"] - second["yta"]) * 100)
        # The two measures do not agree, and the disagreement is reported rather
        # than hidden by the median: two counties mask a larger share of their
        # class B documents than of their class A documents, while no county
        # masks a larger area in class B.
        if second["andel"] > first["andel"]:
            share_higher.append(item["namn"])
        if second["yta"] > first["yta"]:
            area_higher.append(item["namn"])
    return {
        "lan": len(shares),
        "median_dokumentandel": median(shares) if shares else None,
        "median_yta": median(areas) if areas else None,
        "hogre_dokumentandel_i_b": sorted(share_higher),
        "hogre_yta_i_b": sorted(area_higher),
    }


def build() -> dict:
    """The whole export, ready to be written or inspected."""
    step36 = load_step36()
    masking = read(MASKING)
    contrast = read(CONTRAST)
    replies = read(REPLIES)
    # The packet is the project's own letter, and it is the one every reply on
    # the board is a reply to. Its checksum alone put our side behind a hash
    # while the authorities' side stood in full, which is the asymmetry a
    # reader of an openness measurement notices first. The text is read from
    # the archived file and checked against the manifest's own hash, so the
    # page cannot show a letter other than the one that was sent.
    sent = {}
    for row in read(SENT):
        text = (ROOT / row["path"]).read_bytes()
        digest = hashlib.sha256(text).hexdigest()
        if digest != row["sha256"]:
            raise SystemExit(
                f"{row['path']} hashar till {digest}, manifestet säger {row['sha256']}"
            )
        sent[row["slug"]] = {**row, "text": text.decode("utf-8")}
    log = read(LOG)
    # The P12 letters promise that the whole correspondence log is published,
    # and it was, as a file on the data page. An authority's own board showed
    # only its reply to the packet under the heading "the authority's reply",
    # so a county that wrote nine letters appeared to have written one. The
    # messages go on the board, where a reader looks for them.
    letters: dict[str, list[dict]] = defaultdict(list)
    for row in read(CORRESPONDENCE):
        letters[row["myndighet"]].append(row)
    # And my own letters beside them. The board carried every word the
    # authorities wrote while my side of the same cases stood as templates in
    # the protocol, which is the first asymmetry a critic of an openness
    # measurement names: whoever requests other people's documents and
    # publishes them verbatim has to take the same treatment of their own.
    # docs/KORRESPONDENS.md states the rule; this puts it on the page.
    outgoing: dict[str, list[dict]] = defaultdict(list)
    for row in read(OUTGOING):
        outgoing[row["myndighet"]].append(row)

    comparison = {klass: ranking_rows(step36, masking, klass) for klass in CLASSES}
    places = {
        klass: {row["slug"]: row["plats"] for row in rows}
        for klass, rows in comparison.items()
    }

    by_authority: dict[str, list[dict]] = defaultdict(list)
    for row in replies:
        by_authority[row["myndighet"]].append(row)

    authorities = []
    for authority, slug in step36.SLUG.items():
        own = sorted(
            by_authority.get(authority, []),
            key=lambda row: (row["datum"], row["klockslag"]),
        )
        classes = {
            klass: class_figures(step36, masking, slug, klass) for klass in CLASSES
        }
        authorities.append(
            {
                "myndighet": authority,
                "slug": slug,
                "namn": step36.NAME.get(slug, slug),
                "klasser": {
                    klass: own_figures
                    for klass, own_figures in classes.items()
                    if own_figures
                },
                "plats": {
                    klass: places[klass][slug]
                    for klass in CLASSES
                    if slug in places[klass]
                },
                "kontrast": [row for row in contrast if row["myndighet"] == slug],
                "paket": sent.get(slug),
                "svar": own,
                "svar_saknas": not any(row["typ"] == "substantiellt" for row in own),
                "utan_matning": (
                    None
                    if any(classes.values())
                    else without_measurement(log, authority)
                ),
                "sammanslagen": merged(log, authority),
                "brev": sorted(
                    letters.get(authority, []),
                    key=lambda row: (row["datum"], row["klockslag"]),
                ),
                "utgaende": sorted(
                    outgoing.get(authority, []),
                    key=lambda row: (row["datum"], row["klockslag"]),
                ),
            }
        )

    totals = {}
    for klass in CLASSES:
        rows = [
            row for row in masking if row["path"].split("/")[0].endswith(f"_{klass}")
        ]
        masked = sum(1 for row in rows if row["masked"])
        totals[klass] = {
            "dokument": len(rows),
            "maskade": masked,
            "andel": masked / len(rows),
            "andel_text": step36.percent(masked / len(rows)),
            "myndigheter": len({row["path"].split("/")[0] for row in rows}),
        }

    # The register's scope is requests A, B and C and the four appeals, so the
    # courts' own letters belong to the published material. They have no board,
    # because a board carries an authority's figures and a court has none, and
    # without a section of their own ten messages were readable only as a file.
    courts = [
        {
            "myndighet": name,
            "brev": sorted(rows, key=lambda r: (r["datum"], r["klockslag"])),
        }
        for name, rows in sorted(letters.items())
        if name not in step36.SLUG
    ]

    annexes = read(ANNEXES) if ANNEXES.exists() else []
    pairs = read(PAIRS) if PAIRS.exists() else []
    paired = [row for row in pairs if row["par"]]

    return {
        "byggd": date.today().isoformat(),
        "p12": {
            "avsant": P12_SENT,
            "svar_senast": P12_DEADLINE,
            "publicering_tidigast": PUBLICATION_FLOOR,
            "publicering_vald": PUBLICATION_DAY,
            "myndigheter": len(step36.SLUG),
            "svarat_substantiellt": sum(
                1 for item in authorities if not item["svar_saknas"]
            ),
        },
        "klasser": totals,
        "domstolar": courts,
        "kontrast": contrast_summary(authorities),
        "jamforelse": {
            klass: {
                "rader": rows,
                "atskilda_par": separated(rows),
                "par": len(rows) * (len(rows) - 1) // 2,
            }
            for klass, rows in comparison.items()
        },
        # The annex measures are a gap, so what the site carries is the
        # evidence for the gap rather than a figure per county: the files that
        # came,
        # and what the documents' own references turned out to be.
        "bilagor": {
            "mappar": len(annexes),
            "bilagefiler": sum(row["bilagefiler"] for row in annexes),
            "lan_med_bilagefil": len(
                {row["myndighet"] for row in annexes if row["bilagefiler"]}
            ),
            "hanvisar_till_innehall": sum(
                row["hanvisar_till_bilaga"] for row in annexes
            ),
            "endast_formell_hanvisning": sum(
                row["endast_formell_hanvisning"] for row in annexes
            ),
            "slag": {
                kind: sum(row["hanvisningens_slag"].get(kind, 0) for row in annexes)
                for kind in ("fotomening ur mallen", "den ifyllda checklistan", "annat")
            },
            "utan_lasbar_text": sum(row["utan_lasbar_text"] for row in annexes),
        },
        "par": {
            "lan": [
                {
                    "myndighet": row["myndighet"],
                    "namn": step36.NAME.get(row["myndighet"], row["myndighet"]),
                    "par": row["par"],
                    "dokument_a": row["parade_dokument_a"],
                    "maskade_a": row["parade_maskade_a"],
                    "dokument_b": row["parade_dokument_b"],
                    "maskade_b": row["parade_maskade_b"],
                }
                for row in paired
            ],
            "lan_med_nummer_i_bada": sum(
                1 for row in pairs if row["arenden_i_a"] and row["arenden_i_b"]
            ),
            "utan_arendenummer": sum(row["utan_arendenummer"] for row in pairs),
            "filer": sum(row["filer"] for row in pairs),
        },
        "myndigheter": authorities,
    }


def main() -> int:
    """Write the export, or print what it would contain."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--dry-run", action="store_true", help="räkna fram allt och skriv ingenting"
    )
    args = parser.parse_args()
    export = build()

    if args.dry_run:
        print(json.dumps(export["klasser"], ensure_ascii=False, indent=2))
        for klass, block in export["jamforelse"].items():
            print(
                f"klass {klass}: {len(block['rader'])} myndigheter, "
                f"{block['atskilda_par']} av {block['par']} par åtskilda"
            )
        return 0

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_bytes(
        (json.dumps(export, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    )
    print(
        f"{len(export['myndigheter'])} myndigheter skrivna till {OUT.relative_to(ROOT)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
