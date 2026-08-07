"""Bake the example answers for /uppslag through the live code path.

Step 16 of the pipeline; run 14 first. The example questions on the site
are served statically so that a cold-started API never meets a first-time
visitor. They are produced here by exactly the same functions the service
runs: retrieval.ask() with the model named in the embeddings manifest, the
default threshold, and the verbatim guarantee. If the corpus or the
embeddings change, rerunning this step is what keeps the baked answers and
the live answers identical.

The questions are topic-shaped on purpose: the model matches topic, never
polarity, and the examples model the right way to read the search
(docs/DGSANTE.md).

Usage:
    python pipeline/16_bake_examples.py
"""

from __future__ import annotations

import json
import sys
from dataclasses import asdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from retrieval import (  # noqa: E402
    DEFAULT_THRESHOLD,
    SentenceTransformerEmbedder,
    ThresholdSelector,
    ask,
    load_corpus,
    load_embeddings,
)

MANIFEST = ROOT / "data" / "dgsante_embeddings_manifest.json"
OUT = ROOT / "web" / "public" / "data" / "exempel.json"
TOP = 5

QUESTIONS = [
    "advance notice of farm inspections",
    "training of official veterinarians",
    "laboratory accreditation for residue testing",
    "animal welfare during transport",
    "traceability of bovine animals",
    "follow-up of previous audit recommendations",
]


def main() -> int:
    """Answer every example question and write the results as JSON."""
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    embedder = SentenceTransformerEmbedder(manifest["model"])
    selector = ThresholdSelector(DEFAULT_THRESHOLD)
    matrix = load_embeddings()
    paragraphs = load_corpus()

    baked = []
    for question in QUESTIONS:
        answers = ask(question, embedder, selector, matrix, paragraphs)[:TOP]
        baked.append(
            {
                "question": question,
                "answers": [
                    {**asdict(answer), "score": round(answer.score, 4)}
                    for answer in answers
                ],
            }
        )
        print(f"{question}: {len(answers)} answers")

    OUT.write_text(
        json.dumps(baked, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"-> {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
