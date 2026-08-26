"""Draw the hand-read sample that the species rule must be checked against.

Step 30 of the pipeline. Step 20 registers which animals each delivered document
concerns by counting terms, and says of itself that the result "must be checked
against hand-read documents before any figure derived from it is published,
exactly as the DG SANTE annex classification was checked against forty hand-read
annexes". This step draws that sample and, once the answers are filled in,
compares them. It never invents an answer.

**The draw is stratified on the rule's own outcome, three per class.** The
classes are nöt, gris, fjäderfä and none, with 190, 16, 42 and 46 documents. A
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

**The comparison runs against two fields, because they answer two questions.**
`dominant` is the rule's single verdict, and `present` is the set of species it
found at all. A reader who answers "flera" disagrees with every `dominant`,
including the honest `ingen`, so a comparison against `dominant` alone counts the
rule's refusal to name one species as an error. `present` is what says whether
the rule saw one species or several, and it is the field that tests the counting.

**The cattle stratum was extended after the first twelve, and the reason is
declared.** Three documents cannot carry a class of 190, and cattle was the only
class where nothing disagreed, so the population's largest cell rested on the
thinnest evidence. Six more cattle documents are drawn with a second seed,
excluding those already read. Extending an under-powered stratum is legitimate;
dropping a document that gave an inconvenient answer would not be, and none is
dropped.

**The sample was drawn from 293 documents, one short of the population.** A
delivery that arrived on 17 August was missing from step 20 when the draw was
made and only appeared when the step was re-run on 26 August. It was therefore
not eligible. The sample is not redrawn with it: changing a sample after its
answers are known does more damage than the known limit that one document of 294
could not be drawn.

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
# The extension of the cattle stratum, drawn separately so the first sample is
# untouched and both draws stay reproducible from their own seed.
EXTRA_SEED = 20260826
EXTRA = {"nöt": 6}
CLASSES = ("nöt", "gris", "fjäderfä", None)
# What a reader may write. "flera" is for a holding that genuinely keeps more
# than one species, "oklart" for a document that does not say.
ANSWERS = {"nöt", "gris", "fjäderfä", "flera", "oklart"}
# A holding can keep an animal the project does not measure. Step 20 has no
# pattern for horses, sheep, goats or rabbits and could not see one if it tried,
# so a document read as "flera" because of such an animal is not a counting
# failure: within the three species the project compares, it holds one. The
# reader's own words are kept in the row's anteckning, and the paths are listed
# here so the distinction is declared rather than inferred from free text.
#
# Four of the seven mixed holdings turned out to be of this kind, which is why
# the first reading of this sample judged the rule wrongly: a bare answer of
# "flera" does not say which animals, and the sheet did not ask. It does now.
OUT_OF_SCOPE = {
    # fjäderfä plus häst
    "gavleborg_A/Normal kontroll, risk - kontrollrapport(8916-2025-2).pdf",
    # gris plus kanin, häst och får
    "uppsala_A/7826-2025 Kopia på klagomål.pdf",
    # fjäderfä, inklusive gås, plus häst
    "vasterbotten_A/11096-2025, Kontrollrapport.pdf",
    # nöt plus får
    "vasternorrland_B/Föreläggande enligt 8 kap 9 § djurskyddslagen(10488-2023-9).pdf",
}


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


def extend(rows: list[dict], answers: list[dict]) -> list[dict]:
    """The extra documents an under-powered stratum needs, drawn once.

    Only ever adds. The rows already in the file are what someone has read, and
    a sample that can shrink after its answers are known is not a sample.
    """
    have = {a["path"] for a in answers}
    rng = random.Random(EXTRA_SEED)
    added: list[dict] = []
    for klass, count in EXTRA.items():
        drawn = sum(1 for r in rows if r["dominant"] == klass and r["path"] in have)
        missing = count + PER_CLASS - drawn
        if missing <= 0:
            continue
        pool = sorted(
            r["path"] for r in rows if r["dominant"] == klass and r["path"] not in have
        )
        for path in sorted(rng.sample(pool, min(missing, len(pool)))):
            source = next(r["source"] for r in rows if r["path"] == path)
            added.append(
                {"path": path, "källa": source, "handlast": None, "anteckning": ""}
            )
    return added


def report(rows: list[dict], answers: list[dict]) -> int:
    """Progress, and the comparison once every answer is in."""
    verdict = {r["path"]: r["dominant"] for r in rows}
    filled = [a for a in answers if a["handlast"]]
    print(f"{len(filled)} av {len(answers)} handlästa")

    bad = [a["handlast"] for a in filled if a["handlast"] not in ANSWERS]
    if bad:
        print(f"svar utanför {sorted(ANSWERS)}: {sorted(set(bad))}")
        return 1
    # An answer of "flera" that does not say which animals cannot be told apart
    # from a mixture with a species the project never counts, and the first
    # reading of this sample was misjudged for exactly that reason.
    unnamed = [
        a["path"]
        for a in filled
        if a["handlast"] == "flera" and not a["anteckning"].strip()
    ]
    if unnamed:
        print(f"\nflera-svar utan djuren utskrivna ({len(unnamed)}):")
        for path in unnamed:
            print(f"  {path}")
        return 1
    if len(filled) < len(answers):
        print("\nkvar att läsa:")
        for answer in answers:
            if not answer["handlast"]:
                print(f"  {answer['path']}")
        return 1

    present = {r["path"]: r["present"] for r in rows}

    print("\nett: regelns dominant mot handläsningen, per klass:")
    per_class: dict[str, list[bool]] = {}
    for answer in answers:
        rule = verdict[answer["path"]] or "ingen"
        per_class.setdefault(rule, []).append(rule == answer["handlast"])
    for klass, hits in sorted(per_class.items()):
        print(f"  {klass:10} {sum(hits)} av {len(hits)}")

    print("\ntvå: en art eller flera, inom projektets tre djurslag?")
    several = [
        a for a in answers if a["handlast"] == "flera" and a["path"] not in OUT_OF_SCOPE
    ]
    named = [a for a in answers if a["handlast"] in {"nöt", "gris", "fjäderfä"}]
    outside = [a for a in answers if a["path"] in OUT_OF_SCOPE]
    # A holding of cattle and sheep holds one of the three species compared, so
    # it belongs with the single-species documents for this question.
    single = named + outside
    if outside:
        print(
            f"  ({len(outside)} dokument blandar med djurslag projektet inte "
            "mäter och räknas därför som en art)"
        )
    caught = [a for a in several if len(present[a["path"]]) > 1]
    clean = [a for a in single if len(present[a["path"]]) == 1]
    print(f"  flera arter, sedda som flera: {len(caught)} av {len(several)}")
    print(f"  en art, sedd som en:          {len(clean)} av {len(single)}")

    print("\ntre: namngav regeln någonsin fel art?")
    # Only the documents where the reader named one of the three species, since
    # a "flera" answer gives nothing to compare a single name against.
    wrong = [
        a
        for a in named
        if verdict[a["path"]] is not None and verdict[a["path"]] != a["handlast"]
    ]
    print(f"  fel art: {len(wrong)} av {len(named)}")

    missed = [a for a in several if len(present[a["path"]]) == 1]
    if missed:
        print(f"\nmissat andra djurslag ({len(missed)}):")
        for answer in missed:
            print(f"  {answer['path']}\n    regeln såg bara {present[answer['path']]}")
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
        added = extend(rows, answers)
        if added:
            with OUT.open("a", encoding="utf-8", newline="\n") as out:
                for record in added:
                    out.write(json.dumps(record, ensure_ascii=False) + "\n")
            print(f"\n{len(added)} dokument tillagda med frö {EXTRA_SEED}:\n")
            for record in added:
                print(f"  {DELIVERIES / record['path']}")
                print(f"    källa: {record['källa']}")
            answers += added
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
