"""Test the pre-registered hypothesis about unannounced controls.

Step 28 of the pipeline, and the question the project was built around. Section
10 of docs/BEGARANMALL.md, timestamped before any request was sent, states it:
unannounced controls find deficiencies more often than announced ones, and the
share of unannounced controls explains part of the spread between counties in
the share of controls finding deficiencies.

**Only half the pre-registered test can be run, and that is stated first.**
Section 10 asks for two things: the association between the two shares across
counties, and the difference in deficiency rate between unannounced and
announced controls *within* the same county, species and control type. The
second needs the announced flag crossed with the deficiency flag. The authority
delivered the announced dimension as 336 separate reports, every one of them
covering "Alla kontrolltypgrupper", so no crossing exists. Only the association
across counties can be computed. The within-county contrast is not weakened
here, it is absent, and no substitute is offered for it.

**The denominator is the sum of announced and unannounced, never the row
count.** The row level extract holds more controls than the two reports add up
to, by five to six per cent for cattle and by 27 per cent for broilers in 2025.
A control whose announced field is empty falls out of both, which is risk 2 in
the pre-registration confirmed in the data. Dividing by the row count would
silently treat those controls as announced.

**The deficiency share is computed twice.** Over routine controls, which is
what the authority's own published figure concerns and what step 22 measures,
and over every control type, which is the population the announced reports
actually cover. Neither is the pre-registered pairing, because that required the
crossing; both are reported so the choice cannot carry the result.

**The association is tested by permutation.** Spearman's rank correlation over
counties, with the counties' deficiency shares reshuffled against their
announced shares, a fixed seed and the observed value placed against that
distribution. Baseline before conclusion, as everywhere else here.

Writes data/oanmald_hypotes.jsonl, one row per county, species and year.

Usage:
    python pipeline/28_unannounced_hypothesis.py
"""

from __future__ import annotations

import json
import random
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ANNOUNCED = ROOT / "data" / "foranmalda.jsonl"
DEFICIENCY = ROOT / "data" / "bristandel.jsonl"
OUT = ROOT / "data" / "oanmald_hypotes.jsonl"

PERMUTATIONS = 2000
SEED = 20260821
# A county contributes to a correlation only when both of its shares rest on
# enough controls to mean anything. The same floor step 22 uses.
MIN_CONTROLS = 20

# The two deliveries name the same things differently, so the join is written
# out rather than guessed by string surgery.
SPECIES = {
    "Nötkreatur": "nötkreatur",
    "Gris": "gris",
    "Värphöns fler än 350 st": ">350 värphöns",
    "Slaktkyckling": "slaktkyckling",
}
COUNTY = {
    "Blekinge": "Blekinge län",
    "Dalarna": "Dalarnas län",
    "Gotland": "Gotlands län",
    "Gävleborg": "Gävleborgs län",
    "Halland": "Hallands län",
    "Jämtland": "Jämtlands län",
    "Jönköping": "Jönköpings län",
    "Kalmar": "Kalmar län",
    "Kronoberg": "Kronobergs län",
    "Norrbotten": "Norrbottens län",
    "Skåne": "Skåne län",
    "Stockholm": "Stockholms län",
    "Södermanland": "Södermanlands län",
    "Uppsala": "Uppsala län",
    "Värmland": "Värmlands län",
    "Västerbotten": "Västerbottens län",
    "Västernorrland": "Västernorrlands län",
    "Västmanland": "Västmanlands län",
    "Västra Götaland": "Västra Götalands län",
    "Örebro": "Örebro län",
    "Östergötland": "Östergötlands län",
}


def ranks(values: list[float]) -> list[float]:
    """Ranks with ties averaged, which is what Spearman needs."""
    order = sorted(range(len(values)), key=lambda i: values[i])
    out = [0.0] * len(values)
    position = 0
    while position < len(order):
        stop = position
        while (
            stop + 1 < len(order) and values[order[stop + 1]] == values[order[position]]
        ):
            stop += 1
        shared = (position + stop) / 2 + 1
        for index in order[position : stop + 1]:
            out[index] = shared
        position = stop + 1
    return out


def spearman(left: list[float], right: list[float]) -> float:
    """Rank correlation, written out to avoid a dependency for one formula."""
    a, b = ranks(left), ranks(right)
    n = len(a)
    mean_a, mean_b = sum(a) / n, sum(b) / n
    top = sum((x - mean_a) * (y - mean_b) for x, y in zip(a, b, strict=True))
    left_ss = sum((x - mean_a) ** 2 for x in a)
    right_ss = sum((y - mean_b) ** 2 for y in b)
    return top / (left_ss * right_ss) ** 0.5 if left_ss and right_ss else 0.0


def permutation_p(left: list[float], right: list[float], observed: float) -> float:
    """How often chance alone reaches an association this positive."""
    rng = random.Random(SEED)
    shuffled = list(right)
    hits = 0
    for _ in range(PERMUTATIONS):
        rng.shuffle(shuffled)
        if spearman(left, shuffled) >= observed:
            hits += 1
    return hits / PERMUTATIONS


def load_announced() -> dict[tuple[str, str, int], tuple[int, int]]:
    """Announced and unannounced counts per county, species and year."""
    found: dict[tuple[str, str, int], list[int]] = defaultdict(lambda: [0, 0])
    for line in ANNOUNCED.read_text("utf-8").splitlines():
        row = json.loads(line)
        key = (COUNTY[row["myndighet"]], SPECIES[row["checklista"]], row["år"])
        found[key][0 if row["aviserad"] else 1] += row["kontroller"]
    return {k: (v[0], v[1]) for k, v in found.items()}


def load_deficiency() -> dict[tuple[str, str, int, str], tuple[int, int]]:
    """Controls and controls with a deficiency, per cell and category."""
    found: dict[tuple[str, str, int, str], list[int]] = defaultdict(lambda: [0, 0])
    for line in DEFICIENCY.read_text("utf-8").splitlines():
        row = json.loads(line)
        for category in (row["category"], "alla"):
            key = (row["LÄN"], row["species"], row["year"], category)
            found[key][0] += row["kontroller"]
            found[key][1] += row["med_brist"]
    return {k: (v[0], v[1]) for k, v in found.items()}


def main() -> int:
    """Join the two deliveries and test the association across counties."""
    for path in (ANNOUNCED, DEFICIENCY):
        if not path.exists():
            print(f"missing {path.name}")
            return 1
    announced = load_announced()
    deficiency = load_deficiency()

    records = []
    for (county, species, year), (yes, no) in sorted(announced.items()):
        total = yes + no
        for category in ("rutin", "alla"):
            cell = deficiency.get((county, species, year, category))
            if not cell:
                continue
            controls, faults = cell
            records.append(
                {
                    "myndighet": county,
                    "djurslag": species,
                    "år": year,
                    "kategori": category,
                    "aviserade": yes,
                    "oaviserade": no,
                    "andel_oanmalda": round(no / total, 4) if total else None,
                    "kontroller_brist": controls,
                    "med_brist": faults,
                    "andel_brist": round(faults / controls, 4) if controls else None,
                }
            )
    with OUT.open("w", encoding="utf-8", newline="\n") as out:
        for record in records:
            out.write(json.dumps(record, ensure_ascii=False) + "\n")
    print(f"{len(records)} celler -> {OUT.name}\n")

    print(
        f"Spearman över län, celler med minst {MIN_CONTROLS} kontroller i båda måtten"
    )
    print(f"{'djurslag':16} {'år':>5} {'kategori':10} {'län':>4} {'rho':>7} {'p':>8}")
    for species in ("nötkreatur", "gris", ">350 värphöns", "slaktkyckling"):
        for year in (2024, 2025):
            for category in ("rutin", "alla"):
                cells = [
                    r
                    for r in records
                    if r["djurslag"] == species
                    and r["år"] == year
                    and r["kategori"] == category
                    and r["aviserade"] + r["oaviserade"] >= MIN_CONTROLS
                    and r["kontroller_brist"] >= MIN_CONTROLS
                ]
                if len(cells) < 5:
                    continue
                left = [r["andel_oanmalda"] for r in cells]
                right = [r["andel_brist"] for r in cells]
                rho = spearman(left, right)
                p = permutation_p(left, right, rho)
                print(
                    f"{species:16} {year:>5} {category:10} {len(cells):>4} "
                    f"{rho:>7.3f} {p:>8.4f}"
                )
    return 0


if __name__ == "__main__":
    sys.exit(main())
