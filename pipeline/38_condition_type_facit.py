"""Draw a blind sample of conditions, and score a hand-read facit against it.

Step 38 of the pipeline, and the measurement the schema's own decision log
rests on without anyone having made it. The row "Rubrik" in VILLKORSSCHEMA
section 3 rejects deriving the condition type from the heading, with the reason
that it "klassar fel och kraschar på rubriklösa beslut", and the evidence is a
single example: Motala 2021 condition 12 sits under Övrigt and is in substance a
decommissioning condition. There are now 2 359 conditions to measure it on.

**The blindness is mechanical, and intention has no part in it.** With no flag,
the step prints the identifier, the position and the condition text, with the
heading withheld, in an order shuffled across decisions with a fixed seed. The
reader assigns a type to each. Only with `--score`, and only after the answers
exist, is the heading joined back on. A reader who has seen the heading first
is not reading the text, and a facit produced that way measures nothing.

**The sample is deliberately not proportional.** Four strata of thirty, crossing
the source, text layer against OCR, with whether the condition carries a
heading. A facit should be precise where the instrument is weakest, and the
weights are reported when the figures are.

**A derived field carries its own method.** Section 2.8 requires it: a perfectly
extracted text can be wrongly classed and the reverse. These judgements are
MANUAL, with no RULE among them, and the file records that.

Usage:
    python pipeline/38_condition_type_facit.py            # emit the blind sample
    python pipeline/38_condition_type_facit.py --score    # join and score
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import random
import sys
from collections import Counter
from pathlib import Path
from types import ModuleType

ROOT = Path(__file__).resolve().parent.parent
REGISTER = ROOT / "data" / "villkor.jsonl"
SAMPLE = ROOT / "data" / "villkor_facit_urval.jsonl"
ANSWERS = ROOT / "data" / "villkor_facit.jsonl"

SEED = 20260909
PER_STRATUM = 30

# The nine the schema fixes, the six the corpus adds, plus the two answers a
# reader must be able to give without inventing a type.
CANNOT_TELL = "kan inte avgöra"
DELEGATION = "delegation"


def load_step35() -> ModuleType:
    """Step 35 as a module, since a name starting with a digit cannot be imported."""
    path = ROOT / "pipeline" / "35_condition_types.py"
    spec = importlib.util.spec_from_file_location("condition_types", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def register() -> list[dict]:
    """Every condition, with its heading, which the blind sample must not show."""
    return [
        json.loads(line) for line in REGISTER.read_text("utf-8").splitlines() if line
    ]


def strata(records: list[dict]) -> dict[tuple[str, bool], list[dict]]:
    """The four cells the sample is drawn from."""
    cells: dict[tuple[str, bool], list[dict]] = {}
    for record in records:
        key = (record["källa"], bool(record["rubrik"]))
        cells.setdefault(key, []).append(record)
    return cells


def draw(records: list[dict]) -> list[dict]:
    """Thirty per cell, shuffled across decisions so the order carries nothing."""
    rng = random.Random(SEED)
    picked: list[dict] = []
    for key in sorted(strata(records)):
        pool = sorted(strata(records)[key], key=lambda r: (r["id"], r["position"]))
        picked.extend(rng.sample(pool, min(PER_STRATUM, len(pool))))
    rng.shuffle(picked)
    return picked


def emit(records: list[dict]) -> int:
    """Write the blind sample: identity and text, and nothing that gives it away."""
    picked = draw(records)
    with SAMPLE.open("w", encoding="utf-8", newline="\n") as out:
        for order, record in enumerate(picked, 1):
            out.write(
                json.dumps(
                    {
                        "ordning": order,
                        "id": record["id"],
                        "position": record["position"],
                        "villkorsnummer": record["villkorsnummer"],
                        "tecken": record["tecken"],
                        "text": record["text"],
                    },
                    ensure_ascii=False,
                )
                + "\n"
            )
    cells = Counter((r["källa"], bool(r["rubrik"])) for r in picked)
    print(f"{len(picked)} villkor i blint urval -> {SAMPLE.name}")
    for key in sorted(cells):
        label = f"{key[0]}, {'med rubrik' if key[1] else 'utan rubrik'}"
        print(f"  {label:<22}{cells[key]}")
    print(f"  frö {SEED}, ordningen slumpad över beslut")
    print("  rubriken står inte i filen; den fogas till av --score")
    return 0


def score(records: list[dict]) -> int:
    """Join the answers to the headings and report what the heading is worth."""
    if not ANSWERS.exists():
        print(f"{ANSWERS.name} saknas; läs urvalet och skriv svaren först")
        return 1
    step35 = load_step35()
    answers = {
        (row["id"], row["position"]): row
        for row in (
            json.loads(line) for line in ANSWERS.read_text("utf-8").splitlines() if line
        )
    }
    by_key = {(r["id"], r["position"]): r for r in records}

    missing = [k for k in answers if k not in by_key]
    if missing:
        print(f"{len(missing)} svar pekar på villkor som inte finns: {missing[:5]}")
        return 1

    told = [a for a in answers.values() if a["typ"] != CANNOT_TELL]
    print(f"{len(answers)} handlästa villkor, {len(told)} med satt typ")
    share = len(told) / len(answers)
    print(f"  andel klassificerbara ur texten ensam: {share:.1%}")

    with_heading = [
        (a, by_key[(a["id"], a["position"])])
        for a in answers.values()
        if by_key[(a["id"], a["position"])]["rubrik"]
    ]
    agree = 0
    disagreements: list[tuple[str, str, str, str]] = []
    for answer, record in with_heading:
        from_heading = step35.HEADING_TYPE.get(record["rubrik"])
        if answer["typ"] == CANNOT_TELL:
            continue
        if from_heading == answer["typ"]:
            agree += 1
        else:
            disagreements.append(
                (record["rubrik"], from_heading or "?", answer["typ"], answer["id"])
            )
    judged = agree + len(disagreements)
    print(f"\nrubrikens typ mot sakens typ, {judged} villkor med rubrik")
    if judged:
        print(f"  överens: {agree} ({agree / judged:.1%})")
        print(f"  oense:   {len(disagreements)} ({len(disagreements) / judged:.1%})")
    worst = Counter(d[0] for d in disagreements)
    if worst:
        print("\n  rubriker som stämmer sämst")
        for heading, count in worst.most_common(8):
            total = sum(1 for _, r in with_heading if r["rubrik"] == heading)
            print(f"    {count} av {total}  {heading}")
    print("\n  varje oenighet, rubrikens typ mot sakens")
    for heading, from_heading, mine, ident in disagreements:
        print(f"    {from_heading:<16} -> {mine:<16} {ident}  {heading}")

    without = [
        a for a in answers.values() if not by_key[(a["id"], a["position"])]["rubrik"]
    ]
    told_without = [a for a in without if a["typ"] != CANNOT_TELL]
    print(f"\nde rubriklösa, {len(without)} villkor")
    if without:
        print(
            f"  typ satt ur texten: {len(told_without)} "
            f"({len(told_without) / len(without):.1%})"
        )
        for typ, count in Counter(a["typ"] for a in without).most_common():
            print(f"    {count:>3}  {typ}")
    return 0


def main() -> int:
    """Emit the blind sample, or score the answers against the headings."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--score",
        action="store_true",
        help="join the hand-read answers to the headings and report",
    )
    args = parser.parse_args()
    if not REGISTER.exists():
        print("run pipeline/33_condition_register.py first")
        return 1
    records = register()
    return score(records) if args.score else emit(records)


if __name__ == "__main__":
    sys.exit(main())
