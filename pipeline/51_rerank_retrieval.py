"""Rerank BM25's candidates with a cross-encoder, and measure the result.

Step 50 found that the deployed dense retriever loses to BM25 on this corpus,
and that fusing the two dilutes the better signal. What is left untested is the
lever that usually matters most: a cross-encoder that reads the question and a
candidate paragraph together, rather than comparing two points embedded apart.

The bar and the candidate depth were written to the protocol log before this
ran, together with the ceiling the depth imposes. BM25 recall@50 is 0.6733, so
reranking its top 50 cannot carry recall@10 above that however good the
reranker is, and the bar sits under the ceiling rather than over it.

The questions are split in two deterministic halves by a hash of the question
id. Nothing here is tuned, since the model is taken off the shelf with no
parameters, but the figures that count are the held-out half's: a later
version that does tune anything then has a half it never saw.

Writes ``data/retrieval_omrankning.json``.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import re
import sys
from pathlib import Path
from typing import Any

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "retrieval_omrankning.json"

MODEL = "cross-encoder/ms-marco-MiniLM-L-6-v2"
DEPTH = 50
CUTS = (1, 5, 10)
MRR_AT = 10


def load_step50() -> Any:
    """Import step 50, whose name starts with a digit, the way step 41 does."""
    path = ROOT / "pipeline" / "50_measure_retrieval.py"
    spec = importlib.util.spec_from_file_location("measure_retrieval", path)
    if spec is None or spec.loader is None:  # pragma: no cover - import guard
        raise SystemExit(f"kan inte importera {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules["measure_retrieval"] = module
    spec.loader.exec_module(module)
    return module


def half(question: str) -> int:
    """Which half a question falls in, from its id alone and nothing else."""
    digest = hashlib.sha256(question.encode("utf-8")).hexdigest()
    return int(digest, 16) % 2


def main() -> int:
    """Rerank, measure both halves, and write the figures."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--limit", type=int, help="kör ett urval frågor, för att pröva kedjan"
    )
    args = parser.parse_args()

    step50 = load_step50()
    paragraphs = step50.read(step50.PARAGRAPHS)
    index = {(row["ref"], row["number"]): i for i, row in enumerate(paragraphs)}
    texts = [row["text"] for row in paragraphs]

    questions = step50.read(step50.EVAL)
    if args.limit:
        questions = questions[: args.limit]
    queries = [re.sub(r"\s+", " ", row["text"]).strip() for row in questions]
    gold = [
        {index[(row["ref"], number)] for number in row["facit"]} for row in questions
    ]
    halves = [half(row["fraga"]) for row in questions]

    print(f"{len(queries)} frågor, djup {DEPTH}, tak recall@10 = BM25 recall@{DEPTH}")
    candidates = step50.bm25_ranking(texts, queries, DEPTH)

    from sentence_transformers import CrossEncoder

    model = CrossEncoder(MODEL)
    reranked = np.empty((len(queries), DEPTH), dtype=np.int32)
    for i in range(len(queries)):
        pairs = [(queries[i], texts[j]) for j in candidates[i].tolist()]
        scores = np.asarray(model.predict(pairs, show_progress_bar=False))
        reranked[i] = candidates[i][np.argsort(-scores)]
        if (i + 1) % 200 == 0:
            print(f"   {i + 1} av {len(queries)}", flush=True)

    results = []
    for name, ranking in (("bm25", candidates), ("omrankad", reranked)):
        for which, label in ((0, "installning"), (1, "undanhallen")):
            rows = [
                step50.score(ranking[i], gold[i])
                for i in range(len(queries))
                if halves[i] == which
            ]
            summary = step50.summarise(rows, f"{name}/{label}", len(rows))
            results.append(summary)
            print("   ", json.dumps(summary, ensure_ascii=False))

    OUT.write_text(
        json.dumps(
            {
                "modell": MODEL,
                "djup": DEPTH,
                "fragor": len(queries),
                "tak_recall": round(
                    sum(
                        1
                        for i in range(len(queries))
                        if gold[i] & set(candidates[i].tolist())
                    )
                    / len(queries),
                    4,
                ),
                "resultat": results,
            },
            ensure_ascii=False,
            indent=1,
        )
        + "\n",
        encoding="utf-8",
    )
    print(f"skrivet till {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
