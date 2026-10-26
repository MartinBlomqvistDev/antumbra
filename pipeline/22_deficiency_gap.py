"""Measure the spread between counties in the share of controls finding faults.

Step 22 of the pipeline. The project starts from one sentence in the Board of
Agriculture's own report for 2024: "Under 2024 rapporterade en länsstyrelse
brister vid 33 procent av rutinkontrollerna, medan en annan rapporterade
brister vid 84 procent av rutinkontrollerna", followed by the statement that
the difference cannot be read out of the statistics. The register extract
delivered under request C is finer than that report, so the spread can be
recomputed from the rows instead of quoted from the text.

Three restrictions, all forced by the data rather than chosen.

**A row is one animal keeper at one control.** A control it is not. The authority
stated this itself on 24 August 2026, after being asked why its two deliveries
disagree: "i de fall det är fler än en djurhållare på kontrollplatsen så blir
varje djurhållare en egen rad (dvs. en kontroll där det finns två djurhållare
blir två rader i Excelfilen)". The extract carries four columns, county, control
type, checklist and the deficiency flag, and no identifier of any kind, so the
duplicates cannot be located and the rows cannot be collapsed onto controls.
Every count below is therefore a count of keeper rows, which is what the output
field is named. A share over them equals the share over controls only where
duplicated keepers carry the same deficiency flag, and how often they do cannot
be measured from this file.

**The deficiency flag belongs to the control. The animal does not carry it.** The output
is grouped by species, and one of the eighteen documents hand-read for step 30
records deficiencies in the horse facilities of a holding that also keeps 60
birds. A share computed for a species can therefore carry a fault found in an
animal the project does not measure. The extract has one deficiency field per
control and no way to attach it to an animal, so this is reported and not
repaired.

**Routine controls only.** Five of the control types name the outcome in the
type itself, for instance "Klagomål, offentlig kontroll med brister", and in
those rows the deficiency flag agrees with the type name 96 to 100 per cent of
the time. A share computed across all types would partly count the
classification rather than the finding. The report's own figure concerns
routine controls, and so does this one. The categorisation into routine,
complaint and follow-up is the authority's own, quoted from its covering
e-mail of 14 August 2026.

**The 2024 cattle sheet was defective and has been replaced.** The delivery of
14 August held 1 577 rows for 2024 against 2 916 for 2025, lacked Norrbotten and
Uppsala entirely, and gave nine counties a handful of rows where the year should
carry hundreds. The authority was asked whether the extract was complete and
delivered a corrected file on 17 August: 2 451 rows and all 21 counties, with
Jönköping, Kronoberg and Västerbotten each gaining more than 130 rows. Only that
one sheet changed; the other seven are byte-identical in content. Both years are
now usable, and the printed summary still covers them separately so that no
national figure can pool a year silently.

Writes data/bristandel.jsonl, keeper rows and shares per county, year, species
and control category.

Usage:
    python pipeline/22_deficiency_gap.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
# The corrected delivery, received after the authority was asked whether its
# 2024 cattle extract was complete. Named explicitly rather than picked by
# glob: which file a figure came from is provenance, and a newest-file rule
# would change the source without changing the code.
DELIVERY = (
    ROOT
    / "data"
    / "leveranser"
    / "jordbruksverket_C"
    / "Kontrollstatistik per län 2024 2025 nöt, gris, höns, slaktkyckling_v2.xlsx"
)
OUT = ROOT / "data" / "bristandel.jsonl"

MIN_ROWS = 20

# The authority's own grouping, quoted from its e-mail of 2026-08-14. Types in
# the file that appear in none of the three lists are reported, and bucketing
# them is wrong
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
# measures the classification rather than the inspection.
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
        .agg(rader=("fault", "size"), med_brist=("fault", "sum"))
        .reset_index()
    )
    grouped["andel_brist"] = (grouped["med_brist"] / grouped["rader"]).round(3)
    with OUT.open("w", encoding="utf-8", newline="\n") as out:
        for record in grouped.to_dict("records"):
            record["med_brist"] = int(record["med_brist"])
            out.write(json.dumps(record, ensure_ascii=False) + "\n")
    print(f"{len(grouped)} cells written to {OUT.name}\n")

    for year in sorted(rows["year"].unique()):
        routine = rows[(rows["year"] == year) & (rows["category"] == "rutin")]
        per_county = routine.groupby("LÄN")["fault"].agg(["size", "mean"]).reset_index()
        usable = per_county[per_county["size"] >= MIN_ROWS].sort_values("mean")
        if usable.empty:
            print(f"{year}: no county reaches {MIN_ROWS} routine rows\n")
            continue
        low, high = usable.iloc[0], usable.iloc[-1]
        print(
            f"{year}, rutinkontroller, län med minst {MIN_ROWS} rader: "
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
