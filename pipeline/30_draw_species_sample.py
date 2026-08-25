"""Draw the hand-read sample that the species rule must be checked against.

Step 30 of the pipeline. Step 20 registers which animals each delivered document
concerns by counting terms, and says of itself that the result "must be checked
against hand-read documents before any figure derived from it is published,
exactly as the DG SANTE annex classification was checked against forty hand-read
annexes". This step draws that sample and, once the answers are filled in,
compares them. It never invents an answer.

**The draw is stratified on the rule's own outcome, three per class.** The
classes are nöt, gris, fjäderfä and none, with 190, 16, 41 and 46 documents. A
simple random sample of twelve would hold roughly eight cattle documents and
might hold no pig document at all, and the fragile classes are exactly the small
ones: gris rests on sixteen documents, and "none" is where the rule declined to
choose. Three per class puts every failure mode in front of a reader. Accuracy
is therefore reported per class and never pooled into one number, because the
sample is not proportional to the population.

**The sheet is blind, and that is the point.** The rows carry the path and
whether the text came from OCR, and nothing else. Neither the counts, nor which
species the rule found present, nor its verdict, nor even the stratum a document
was drawn from reaches the reader, since the stratum is the verdict. A check
that shows the answer first is not a check.

**Answers are never overwritten.** Once `data/djurslag_facit.jsonl` exists the
step leaves it alone and reports progress instead. The draw is reproducible from
the seed, so re-running cannot quietly produce a different sample after someone
has seen the first one.

Usage:
    python pipeline/30_draw_species_sample.py
"""

from __future__ import annotations

import json
import random
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SPECIES = ROOT / "data" / "djurslag.jsonl"
OUT = ROOT / "data" / "djurslag_facit.jsonl"
DELIVERIES = ROOT / "data" / "leveranser"

SEED = 20260825
PER_CLASS = 3
CLASSES = ("nöt", "gris", "fjäderfä", None)
# What a reader may write. "flera" is for a holding that genuinely keeps more
# than one species, "oklart" for a document that does not say.
ANSWERS = {"nöt", "gris", "fjäderfä", "flera", "oklart"}


def load() -> list[dict]:
    """One record per delivered document, as step 20 left it."""
    return [
        json.loads(line) for line in SPECIES.read_text("utf-8").splitlines() if line
    ]


def draw(rows: list[dict]) -> list[dict]:
    """Three documents per outcome class, by a fixed seed."""
    rng = random.Random(SEED)
    picked: list[dict] = []
    for klass in CLASSES:
        pool = sorted(r["path"] for r in rows if r["dominant"] == klass)
        chosen = rng.sample(pool, min(PER_CLASS, len(pool)))
        for path in sorted(chosen):
            source = next(r["source"] for r in rows if r["path"] == path)
            picked.append(
                {"path": path, "källa": source, "handlast": None, "anteckning": ""}
            )
    # Sorted by path so the sheet does not group the classes together, which
    # would let a reader infer the verdict from the order.
    return sorted(picked, key=lambda record: record["path"])


def report(rows: list[dict], answers: list[dict]) -> int:
    """Progress, and the comparison once every answer is in."""
    verdict = {r["path"]: r["dominant"] for r in rows}
    filled = [a for a in answers if a["handlast"]]
    print(f"{len(filled)} av {len(answers)} handlästa")

    bad = [a["handlast"] for a in filled if a["handlast"] not in ANSWERS]
    if bad:
        print(f"svar utanför {sorted(ANSWERS)}: {sorted(set(bad))}")
        return 1
    if len(filled) < len(answers):
        print("\nkvar att läsa:")
        for answer in answers:
            if not answer["handlast"]:
                print(f"  {answer['path']}")
        return 1

    print("\nregelns utfall mot handläsningen, per klass:")
    per_class: dict[str, list[bool]] = {}
    for answer in answers:
        rule = verdict[answer["path"]] or "ingen"
        per_class.setdefault(rule, []).append(rule == answer["handlast"])
    for klass, hits in sorted(per_class.items()):
        print(f"  {klass:10} {sum(hits)} av {len(hits)}")
    disagreements = [
        (a["path"], verdict[a["path"]] or "ingen", a["handlast"])
        for a in answers
        if (verdict[a["path"]] or "ingen") != a["handlast"]
    ]
    if disagreements:
        print(f"\navvikelser ({len(disagreements)}):")
        for path, rule, read in disagreements:
            print(f"  {path}\n    regeln: {rule}, handläst: {read}")
    return 0


def main() -> int:
    """Draw the sample once, then report on it every run after that."""
    if not SPECIES.exists():
        print(f"missing {SPECIES.name}; run step 20 first")
        return 1
    rows = load()
    print(
        "population per klass: "
        + ", ".join(
            f"{klass or 'ingen'} {n}"
            for klass, n in sorted(
                Counter(r["dominant"] or "ingen" for r in rows).items()
            )
        )
    )

    if OUT.exists():
        answers = [
            json.loads(line) for line in OUT.read_text("utf-8").splitlines() if line
        ]
        return report(rows, answers)

    picked = draw(rows)
    with OUT.open("w", encoding="utf-8", newline="\n") as out:
        for record in picked:
            out.write(json.dumps(record, ensure_ascii=False) + "\n")
    print(f"\n{len(picked)} dokument dragna med frö {SEED} -> {OUT.name}\n")
    for record in picked:
        print(f"  {DELIVERIES / record['path']}")
        print(f"    källa: {record['källa']}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
