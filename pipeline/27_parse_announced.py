"""Read the 336 per-county reports on announced and unannounced controls.

Step 27 of the pipeline, and the dimension request C was refused on. The Board
of Agriculture wrote on 12 August 2026 that whether a control was announced
"går dessvärre inte att få ut med rutinbetonade åtgärder per län utan endast per
år för hela landet". After the question was put again it offered to pull the
figures county by county, one report per county, species, year and announced
status, and delivered all 336 on 21 August.

**One file is one number.** Each report carries its own parameters as rows:
checklist, county letter, control type group, the date span, whether the control
was announced, and the count. The county is read from inside the file rather
than from the file name, because one file name spells the county letter in lower
case and a name is a weaker source than the report's own header.

**The grouping is not crossed with anything.** Every report says
"Alla kontrolltypgrupper", so the announced dimension arrives per county,
species and year, and not per control type or against the deficiency flag. That
is the limit of what request C's first dimension can support, and it is checked
here rather than assumed: a report with any other group would be reported.

**The authority's own national totals are the check.** In its e-mails of 14 and
17 August the authority stated the national counts per species and year. If the
336 county reports sum to those figures, the two extracts agree and the harvest
is complete; if they do not, the difference is printed and nothing is quietly
reconciled.

Writes data/foranmalda.jsonl, one row per report.

Usage:
    python pipeline/27_parse_announced.py
"""

from __future__ import annotations

import json
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "data" / "leveranser" / "jordbruksverket_C" / "Begarda hanlingar"
OUT = ROOT / "data" / "foranmalda.jsonl"

# The reports are written by a Windows tool and are not UTF-8.
ENCODING = "cp1252"

COUNTY = {
    "AB": "Stockholm",
    "C": "Uppsala",
    "D": "Södermanland",
    "E": "Östergötland",
    "F": "Jönköping",
    "G": "Kronoberg",
    "H": "Kalmar",
    "I": "Gotland",
    "K": "Blekinge",
    "M": "Skåne",
    "N": "Halland",
    "O": "Västra Götaland",
    "S": "Värmland",
    "T": "Örebro",
    "U": "Västmanland",
    "W": "Dalarna",
    "X": "Gävleborg",
    "Y": "Västernorrland",
    "Z": "Jämtland",
    "AC": "Västerbotten",
    "BD": "Norrbotten",
}

# Quoted from the authority's e-mails of 2026-08-14 and 2026-08-17: the national
# counts per species and year, announced and unannounced.
NATIONAL = {
    ("Nötkreatur", 2025): (1855, 913),
    ("Gris", 2025): (177, 92),
    ("Värphöns fler än 350 st", 2025): (40, 12),
    ("Slaktkyckling", 2025): (10, 9),
    ("Nötkreatur", 2024): (1482, 820),
    ("Gris", 2024): (135, 87),
    ("Värphöns fler än 350 st", 2024): (31, 11),
    ("Slaktkyckling", 2024): (18, 9),
}


def read_report(path: Path) -> dict:
    """The parameters and the single count carried by one report."""
    fields: dict[str, str] = {}
    for line in path.read_text(ENCODING).splitlines():
        parts = [p.strip() for p in line.split(";")]
        if not parts or not parts[0]:
            continue
        values = [p for p in parts[1:] if p]
        fields[parts[0]] = values[-1] if values else ""
    return fields


def main() -> int:
    """Parse every report and check the sums against the authority's own."""
    if not SOURCE.is_dir():
        print(f"missing delivery: {SOURCE.name}")
        return 1
    files = sorted(SOURCE.glob("*.skv"))
    print(f"{len(files)} rapporter i {SOURCE.name}")

    records = []
    groups: set[str] = set()
    problems: list[str] = []
    for path in files:
        fields = read_report(path)
        letter = fields.get("Länsbokstav", "").upper()
        if letter not in COUNTY:
            problems.append(f"{path.name}: okänd länsbokstav {letter!r}")
            continue
        groups.add(fields.get("Kontrolltypgrupp", ""))
        start = fields.get("Kontrolldatum fr.o.m", "")
        stop = fields.get("Kontrolldatum t.o.m", "")
        if start[:4] != stop[:4]:
            problems.append(f"{path.name}: spänner över årsskifte, {start} till {stop}")
            continue
        try:
            count = int(fields.get("Antal gånger checklista använd", "0") or 0)
        except ValueError:
            problems.append(f"{path.name}: antalet går inte att läsa")
            continue
        records.append(
            {
                "fil": path.name,
                "myndighet": COUNTY[letter],
                "lansbokstav": letter,
                "checklista": fields.get("Checklista", ""),
                "år": int(start[:4]),
                "aviserad": fields.get("Aviserad", "").upper() == "JA",
                "kontroller": count,
            }
        )

    with OUT.open("w", encoding="utf-8", newline="\n") as out:
        for record in records:
            out.write(json.dumps(record, ensure_ascii=False) + "\n")
    print(f"{len(records)} rapporter lästa -> {OUT.name}")
    if problems:
        print("\nproblem:")
        for problem in problems:
            print(f"  {problem}")
    print(f"kontrolltypgrupper i materialet: {sorted(groups)}")
    print(
        f"län: {len({r['myndighet'] for r in records})}, "
        f"checklistor: {sorted({r['checklista'] for r in records})}"
    )

    totals: dict[tuple[str, int], list[int]] = defaultdict(lambda: [0, 0])
    for record in records:
        totals[(record["checklista"], record["år"])][
            0 if record["aviserad"] else 1
        ] += record["kontroller"]

    print("\nsumma per checklista och år mot myndighetens egna nationella tal:")
    mismatch = 0
    for key in sorted(totals, key=lambda k: (-k[1], k[0])):
        got = tuple(totals[key])
        expected = NATIONAL.get(key)
        if expected is None:
            print(
                f"  {key[0]} {key[1]}: {got[0]} aviserade, {got[1]} oaviserade "
                f"(inget nationellt tal att jämföra med)"
            )
            continue
        agree = got == expected
        mismatch += 0 if agree else 1
        print(
            f"  {key[0]} {key[1]}: {got[0]} mot {expected[0]} aviserade, "
            f"{got[1]} mot {expected[1]} oaviserade  "
            f"{'stämmer' if agree else 'AVVIKER'}"
        )
    print(f"\n{mismatch} av {len(totals)} celler avviker")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
