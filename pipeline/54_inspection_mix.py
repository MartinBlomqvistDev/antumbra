"""Read the unannounced share against the mix of inspection types, for cattle.

Step 54 of the pipeline, run after steps 22 and 28. This reading was not
pre-registered. It was made on 30 October 2026, after publication, when the
spread in the unannounced share turned out to track how many of a county's
inspections fell outside routine. Everything it writes is exploratory, and the
page says so.

**Why the spread cannot be read on its own.** Every one of the 336 reports
covers "Alla kontrolltypgrupper", so the unannounced share is taken over routine
inspections, complaints and follow-ups together. A county doing more follow-ups
can show a higher share without announcing a single routine inspection less. The
mix comes from the row level extract and the notice status from the reports, so
the two are separate fields and the association is not built in by construction.

**The share among routine inspections can only be bounded.** The extract
gives the routine count and the reports give the unannounced count, and nothing
crosses them. Two margins still fix a range. The floor assumes every inspection
outside routine was unannounced; the ceiling assumes none of them was. The range
is often wide, and it is reported as a range.

**The units differ, and one assumption is carried openly.** The mix is counted
in keeper rows and the notice status in checklist uses, the extract running five
to six per cent higher for cattle. The routine share is therefore taken from the
extract and applied to the reports' total, which assumes the duplicated rows are
spread evenly across inspection types. That cannot be checked here.

**The associations are two-sided.** Step 28 tests a pre-registered direction, so
it counts one tail. No direction was stated for these, so both tails count, with
the same seed and the same number of permutations.

Writes data/kontrollmix.jsonl, one row per county and year, and
data/kontrollmix_samband.jsonl, one row per association and year.

Usage:
    python pipeline/54_inspection_mix.py
"""

from __future__ import annotations

import importlib.util
import json
import random
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
DEFICIENCY = ROOT / "data" / "bristandel.jsonl"
HYPOTHESIS = ROOT / "data" / "oanmald_hypotes.jsonl"
MIX = ROOT / "data" / "kontrollmix.jsonl"
ASSOCIATIONS = ROOT / "data" / "kontrollmix_samband.jsonl"

SPECIES = "nötkreatur"
YEARS = (2024, 2025)


def load_step28() -> Any:
    """Import step 28 for its rank correlation and its constants."""
    path = ROOT / "pipeline" / "28_unannounced_hypothesis.py"
    spec = importlib.util.spec_from_file_location("unannounced", path)
    if spec is None or spec.loader is None:  # pragma: no cover - import guard
        raise SystemExit(f"kan inte importera {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules["unannounced"] = module
    spec.loader.exec_module(module)
    return module


def read(path: Path) -> list[dict]:
    """The rows of a JSON Lines file."""
    lines = path.read_text("utf-8").splitlines()
    return [json.loads(line) for line in lines if line]


def two_sided_p(
    step28: Any, left: list[float], right: list[float], observed: float
) -> float:
    """How often chance alone reaches an association this strong, either way."""
    rng = random.Random(step28.SEED)
    shuffled = list(right)
    hits = 0
    for _ in range(step28.PERMUTATIONS):
        rng.shuffle(shuffled)
        if abs(step28.spearman(left, shuffled)) >= abs(observed):
            hits += 1
    return (hits + 1) / (step28.PERMUTATIONS + 1)


def routine_range(
    routine_share: float, unannounced: int, inspections: int
) -> tuple[float, float, float]:
    """The routine count on the reports' scale, and the two bounds on its share."""
    routine = routine_share * inspections
    outside = inspections - routine
    low = max(0.0, unannounced - outside) / routine
    high = min(routine, float(unannounced)) / routine
    return routine, low, high


def county_rows(year: int, rows: list[dict], notices: list[dict]) -> list[dict]:
    """One row per county for a year, the mix beside the notice status."""
    out = []
    for notice in notices:
        if (
            notice["djurslag"] != SPECIES
            or notice["år"] != year
            or notice["kategori"] != "alla"
        ):
            continue
        county = notice["myndighet"]
        counts = {
            row["category"]: row
            for row in rows
            if row["species"] == SPECIES
            and row["year"] == year
            and row["LÄN"] == county
        }
        per_type = {
            name: counts[name]["rader"] if name in counts else 0
            for name in ("rutin", "klagomål", "uppföljning", "okategoriserad")
        }
        total = sum(per_type.values())
        inspections = notice["aviserade"] + notice["oaviserade"]
        share = per_type["rutin"] / total
        routine, low, high = routine_range(share, notice["oaviserade"], inspections)
        out.append(
            {
                "myndighet": county,
                "ar": year,
                "rader": total,
                "rutin_rader": per_type["rutin"],
                "klagomal_rader": per_type["klagomål"],
                "uppfoljning_rader": per_type["uppföljning"],
                "okategoriserad_rader": per_type["okategoriserad"],
                "andel_rutin": round(share, 4),
                "aviserade": notice["aviserade"],
                "oaviserade": notice["oaviserade"],
                "andel_oanmalda": notice["andel_oanmalda"],
                "rutinkontroller_skattade": round(routine, 1),
                "oanmalda_bland_rutin_min": round(low, 4),
                "oanmalda_bland_rutin_max": round(high, 4),
            }
        )
    return out


def associations(
    step28: Any, year: int, counties: list[dict], rows: list[dict]
) -> list[dict]:
    """The four associations for one year, across the counties that carry them."""
    deficiency = {
        row["LÄN"]: row["andel_brist"]
        for row in rows
        if row["species"] == SPECIES
        and row["year"] == year
        and row["category"] == "rutin"
        and row["rader"] >= step28.MIN_ROWS
    }
    unannounced = [row["andel_oanmalda"] for row in counties]
    pairs = {
        "ej_rutin": ([1 - row["andel_rutin"] for row in counties], unannounced),
        "klagomal": (
            [row["klagomal_rader"] / row["rader"] for row in counties],
            unannounced,
        ),
        "uppfoljning": (
            [row["uppfoljning_rader"] / row["rader"] for row in counties],
            unannounced,
        ),
    }
    floor = [row for row in counties if row["myndighet"] in deficiency]
    pairs["brist_uppfoljning"] = (
        [deficiency[row["myndighet"]] for row in floor],
        [row["uppfoljning_rader"] / row["rader"] for row in floor],
    )
    out = []
    for key, (left, right) in pairs.items():
        rho = step28.spearman(left, right)
        out.append(
            {
                "matt": key,
                "ar": year,
                "lan": len(left),
                "rho": round(rho, 4),
                "p": round(two_sided_p(step28, left, right, rho), 4),
                "permutationer": step28.PERMUTATIONS,
            }
        )
    return out


def main() -> int:
    """Write the mix per county and the associations, and print both."""
    step28 = load_step28()
    rows = read(DEFICIENCY)
    notices = read(HYPOTHESIS)
    mix: list[dict] = []
    tested: list[dict] = []
    for year in YEARS:
        counties = county_rows(year, rows, notices)
        mix.extend(counties)
        tested.extend(associations(step28, year, counties, rows))
    for path, written in ((MIX, mix), (ASSOCIATIONS, tested)):
        with path.open("w", encoding="utf-8", newline="\n") as out:
            for row in written:
                out.write(json.dumps(row, ensure_ascii=False) + "\n")
        print(f"{len(written)} rader -> {path.name}")
    for row in tested:
        print(row)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
