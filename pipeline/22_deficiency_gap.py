"""Measure the spread between counties in the share of controls finding faults.

Step 22 of the pipeline. The project starts from one sentence in the Board of
Agriculture's own report for 2024: "Under 2024 rapporterade en länsstyrelse
brister vid 33 procent av rutinkontrollerna, medan en annan rapporterade
brister vid 84 procent av rutinkontrollerna", followed by the statement that
the difference cannot be read out of the statistics. The register extract
delivered under request C carries one row per control, so the spread can be
recomputed from the rows instead of quoted from the report.

Two restrictions, both forced by the data rather than chosen.

**Routine controls only.** Five of the control types name the outcome in the
type itself, for instance "Klagomål, offentlig kontroll med brister", and in
those rows the deficiency flag agrees with the type name 96 to 100 per cent of
the time. A share computed across all types would partly count the
classification rather than the finding. The report's own figure concerns
routine controls, and so does this one. The categorisation into routine,
complaint and follow-up is the authority's own, quoted from its covering
e-mail of 14 August 2026.

**2025 only for the headline.** The 2024 cattle sheet holds 1 577 rows against
2 916 for 2025, lacks Norrbotten and Uppsala entirely, and several counties
carry a handful of rows where 2025 has hundreds. A question about whether the
extract is complete is with the authority. Every year is written to the output;
the printed summary covers the years separately so that a broken year cannot
quietly enter a national figure.

Writes data/bristandel.jsonl, counts and shares per county, year, species and
control category.

Usage:
    python pipeline/22_deficiency_gap.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
DELIVERY = (
    ROOT
    / "data"
    / "leveranser"
    / "jordbruksverket_C"
    / "Kontrollstatistik per län 2024 2025 nöt, gris, höns, slaktkyckling.xlsx"
)
OUT = ROOT / "data" / "bristandel.jsonl"

MIN_CONTROLS = 20

# The authority's own grouping, quoted from its e-mail of 2026-08-14. Types in
# the file that appear in none of the three lists are reported, never bucketed
# by guess.
ROUTINE = {
    "Fullständig gv-kontroll",
    "Rutinkontroll, risk",
    "Rutinkontroll, slump",
    "Normal kontroll, riktad",
    "Ansökan tillstånd",
}
COMPLAINT = {
    "Klagomål, offentlig kontroll med brister",
    "Klagomål eller anmälan, offentlig kontroll utan brister",
    "Info från OV slakteri, offentlig kontroll med brister",
    "Info från OV slakteri, offentlig kontroll utan brister",
    "Anmälan från veterinar, offentlig kontroll med brister",
    "Extra offentlig kontroll, befogad anmälan från allmänhet",
}
FOLLOW_UP = {
    "Uppföljning efter rutinkontroll",
    "Uppföljning efter kontroll av klagomål eller anmälan",
    "Uppföljning efter kontroll av info från OV på slakteri",
    "Uppföljning djurförbud",
}

# Types whose name states the outcome, so that a deficiency share over them
# measures the classification and not the inspection.
OUTCOME_IN_NAME = {t for t in COMPLAINT if "brister" in t}


def category(control_type: str) -> str:
    """The authority's category for one control type."""
    if control_type in ROUTINE:
        return "rutin"
    if control_type in COMPLAINT:
        return "klagomål"
    if control_type in FOLLOW_UP:
        return "uppföljning"
    return "okategoriserad"


def load() -> pd.DataFrame:
    """Every control row, with year and species from the sheet name."""
    sheets = pd.read_excel(DELIVERY, sheet_name=None, engine="openpyxl")
    frames = []
    for name, frame in sheets.items():
        frame = frame.dropna(how="all").copy()
        frame["year"] = int(name.strip()[-4:])
        frame["species"] = name.replace("år", "").strip()[:-4].strip().lower()
        frames.append(frame)
    rows = pd.concat(frames, ignore_index=True)
    rows["category"] = rows["KONTROLLTYP"].map(category)
    rows["fault"] = rows["FINNS_BRISTER"].eq("Ja")
    return rows


def main() -> int:
    """Write the per-cell shares and report the spread between counties."""
    if not DELIVERY.exists():
        print(f"missing delivery: {DELIVERY.name}")
        return 1

    rows = load()
    unknown = sorted(set(rows.loc[rows["category"] == "okategoriserad", "KONTROLLTYP"]))
    if unknown:
        print(f"control types outside the authority's three lists: {unknown}\n")

    grouped = (
        rows.groupby(["year", "species", "category", "LÄN"])
        .agg(kontroller=("fault", "size"), med_brist=("fault", "sum"))
        .reset_index()
    )
    grouped["andel_brist"] = (grouped["med_brist"] / grouped["kontroller"]).round(3)
    with OUT.open("w", encoding="utf-8", newline="\n") as out:
        for record in grouped.to_dict("records"):
            record["med_brist"] = int(record["med_brist"])
            out.write(json.dumps(record, ensure_ascii=False) + "\n")
    print(f"{len(grouped)} cells written to {OUT.name}\n")

    for year in sorted(rows["year"].unique()):
        routine = rows[(rows["year"] == year) & (rows["category"] == "rutin")]
        per_county = routine.groupby("LÄN")["fault"].agg(["size", "mean"]).reset_index()
        usable = per_county[per_county["size"] >= MIN_CONTROLS].sort_values("mean")
        if usable.empty:
            print(f"{year}: no county reaches {MIN_CONTROLS} routine controls\n")
            continue
        low, high = usable.iloc[0], usable.iloc[-1]
        print(
            f"{year}, rutinkontroller, län med minst {MIN_CONTROLS} kontroller: "
            f"{len(usable)} av {len(per_county)}"
        )
        print(
            f"  lägst {low['LÄN']} {low['mean']:.0%} av {int(low['size'])}, "
            f"högst {high['LÄN']} {high['mean']:.0%} av {int(high['size'])}, "
            f"spridning {100 * (high['mean'] - low['mean']):.0f} procentenheter"
        )
        print(f"  ovägt medel {usable['mean'].mean():.0%}\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
