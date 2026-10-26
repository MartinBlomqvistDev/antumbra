"""Build the evaluation set for the retrieval layer, out of the citation graph.

The retrieval layer has never been measured. It answers with verbatim
paragraphs and refuses anything else, and those guarantees are tested, but
nothing says how often it finds the paragraph a reader was after. A retrieval
system without a number for its own accuracy cannot be called good, and the
project's own rule is baseline before model.

The corpus supplies the labels for free. A recommendation in a DG SANTE report
names the paragraphs it rests on, and step 09 resolved 7 484 of those
references to numbered paragraphs. Each resolved citation is therefore a pair
of a question and a paragraph known to answer it: the recommendation's own text
asks, and the paragraph it cites is the answer the report itself points at.

The conditions were written to the protocol log before this ran, including the
bias this instrument carries: question and answer come from the same report and
share vocabulary, so the absolute figures are kind to every method. What the
set is good for is the comparison between methods.

Writes ``data/retrieval_eval.jsonl``, one row per question.
"""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GRAPH = ROOT / "data" / "dgsante_graph.jsonl"
RECOMMENDATIONS = ROOT / "data" / "dgsante_recommendations.jsonl"
PARAGRAPHS = ROOT / "data" / "dgsante_paragraphs.jsonl"
OUT = ROOT / "data" / "retrieval_eval.jsonl"


def read(path: Path) -> list[dict]:
    """Every row of a JSONL file."""
    return [
        json.loads(line)
        for line in path.read_text("utf-8").splitlines()
        if line.strip()
    ]


def build() -> list[dict]:
    """One row per recommendation that cites at least one resolved paragraph."""
    # The paragraph ids the corpus actually holds, so a gold that step 09
    # resolved but step 08 never wrote cannot enter the set unnoticed.
    present = {(row["ref"], row["number"]) for row in read(PARAGRAPHS)}

    gold: dict[tuple[str, int], set[int]] = defaultdict(set)
    for edge in read(GRAPH):
        if not edge["resolved"]:
            continue
        if (edge["ref"], edge["paragraph"]) not in present:
            continue
        gold[(edge["ref"], edge["recommendation"])].add(edge["paragraph"])

    texts = {(row["ref"], row["number"]): row["text"] for row in read(RECOMMENDATIONS)}

    rows = []
    for (ref, number), paragraphs in sorted(gold.items()):
        text = texts.get((ref, number))
        if not text:
            continue
        rows.append(
            {
                "fraga": f"{ref}#{number}",
                "ref": ref,
                "rekommendation": number,
                "text": text,
                "facit": sorted(paragraphs),
            }
        )
    return rows


def main() -> int:
    """Build the set and write it, unless asked only to count it."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--dry-run", action="store_true", help="räkna utan att skriva filen"
    )
    args = parser.parse_args()

    rows = build()
    golds = sum(len(row["facit"]) for row in rows)
    print(f"{len(rows)} frågor, {golds} facit, {golds / len(rows):.2f} per fråga")
    if args.dry_run:
        return 0

    with OUT.open("w", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")
    print(f"skrivet till {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
