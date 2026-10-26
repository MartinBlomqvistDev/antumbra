"""Measure the retrieval layer against the evaluation set from step 49.

Baseline before model, which is the project's rule everywhere else and had
never been applied to the retrieval layer itself. BM25 is run first and on its
own, so the lexical figure exists before any embedding is loaded, and the dense
retriever the service deploys is then measured on exactly the same questions
and the same corpus.

BM25 is implemented here rather than taken from a package: the formula is four
lines over a term-document matrix, the corpus is 81 292 paragraphs, and a
dependency for that would be the same kind of infrastructure without a question
that ADR-0015 refused for the vector store.

The conditions and the declared bias were written to the protocol log before
this ran. The bias in one sentence: question and gold come from the same
report, so both methods are flattered, and the instrument is for comparing them
rather than for claiming how the search answers a stranger.

Writes ``data/retrieval_matning.json``.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

import numpy as np
import scipy.sparse as sp
from sklearn.feature_extraction.text import CountVectorizer

ROOT = Path(__file__).resolve().parent.parent
PARAGRAPHS = ROOT / "data" / "dgsante_paragraphs.jsonl"
EVAL = ROOT / "data" / "retrieval_eval.jsonl"
MANIFEST = ROOT / "data" / "dgsante_embeddings_manifest.json"
SHARDS = ROOT / "data" / "embeddings"
OUT = ROOT / "data" / "retrieval_matning.json"

CUTS = (1, 5, 10)
# Reciprocal rank fusion's one constant, at the value the paper uses. It
# damps the top of each list so that a single method cannot carry the
# fusion on rank one alone.
RRF_K = 60
MRR_AT = 10
# The standard parameters, fixed before the run and left untuned afterwards.
K1 = 1.5
B = 0.75


def read(path: Path) -> list[dict]:
    """Every row of a JSONL file."""
    return [
        json.loads(line)
        for line in path.read_text("utf-8").splitlines()
        if line.strip()
    ]


def score(ranked: np.ndarray, gold: set[int]) -> dict:
    """Recall at each cut and the reciprocal rank, for one question.

    Recall counts a question as found when any of its gold paragraphs is inside
    the cut, which is the usual reading when a question has several right
    answers: the reader needs one of them to get to the source.
    """
    hits = {f"recall@{k}": float(bool(gold & set(ranked[:k].tolist()))) for k in CUTS}
    rank = next(
        (i + 1 for i, item in enumerate(ranked[:MRR_AT].tolist()) if item in gold),
        None,
    )
    hits[f"mrr@{MRR_AT}"] = 1.0 / rank if rank else 0.0
    return hits


def summarise(rows: list[dict], name: str, questions: int) -> dict:
    """The mean of every per-question measure."""
    keys = [f"recall@{k}" for k in CUTS] + [f"mrr@{MRR_AT}"]
    out = {"metod": name, "fragor": questions}
    for key in keys:
        out[key] = round(sum(row[key] for row in rows) / len(rows), 4)
    return out


def bm25_ranking(texts: list[str], queries: list[str], top: int) -> np.ndarray:
    """Top-k paragraph indices per query under BM25, scored with sparse maths."""
    # One tokeniser for documents and queries, so a term that cannot be matched
    # in the corpus cannot be counted in the question either.
    vectoriser = CountVectorizer(lowercase=True, token_pattern=r"(?u)\b\w\w+\b")
    counts = vectoriser.fit_transform(texts).tocsc().astype(np.float32)
    lengths = np.asarray(counts.sum(axis=1)).ravel()
    average = float(lengths.mean())
    documents = counts.shape[0]

    # Document frequency per term, then the Robertson idf the formula uses.
    frequency = np.diff(counts.indptr)
    idf = np.log(1.0 + (documents - frequency + 0.5) / (frequency + 0.5)).astype(
        np.float32
    )

    # The term-document weight does not depend on the query, so it is computed
    # once: each stored count becomes its saturated, length-normalised weight.
    weights = counts.copy()
    rows = weights.tocoo().row
    denominator = weights.data + K1 * (1.0 - B + B * lengths[rows] / average)
    weights.data = weights.data * (K1 + 1.0) / denominator
    weights = weights.tocsr()

    query_counts = vectoriser.transform(queries)
    # A repeated query term counts once: BM25's query-side saturation is a
    # refinement the baseline does not need, and leaving it out keeps the
    # baseline the plain formula.
    query_counts.data = np.ones_like(query_counts.data, dtype=np.float32)
    query_weights = query_counts.multiply(sp.csr_matrix(idf)).tocsr()

    ranking = np.empty((len(queries), top), dtype=np.int32)
    for start in range(0, len(queries), 64):
        block = query_weights[start : start + 64]
        scores = np.asarray((block @ weights.T).todense())
        order = np.argpartition(-scores, top - 1, axis=1)[:, :top]
        for i, row in enumerate(order):
            ranking[start + i] = row[np.argsort(-scores[i, row])]
    return ranking


def dense_ranking(queries: list[str], top: int) -> np.ndarray:
    """Top-k paragraph indices per query under the deployed dense retriever."""
    from sentence_transformers import SentenceTransformer

    manifest = json.loads(MANIFEST.read_text("utf-8"))
    matrix = np.concatenate(
        [np.load(SHARDS / shard["file"]) for shard in manifest["shards"]]
    )
    if matrix.shape[0] != manifest["rows"]:
        raise SystemExit(
            f"matrisen har {matrix.shape[0]} rader, manifestet säger {manifest['rows']}"
        )

    model = SentenceTransformer(manifest["model"])
    embedded = model.encode(
        queries, batch_size=64, normalize_embeddings=True, show_progress_bar=False
    ).astype(np.float32)

    ranking = np.empty((len(queries), top), dtype=np.int32)
    for start in range(0, len(queries), 256):
        scores = embedded[start : start + 256] @ matrix.T
        order = np.argpartition(-scores, top - 1, axis=1)[:, :top]
        for i, row in enumerate(order):
            ranking[start + i] = row[np.argsort(-scores[i, row])]
    return ranking


def fuse(first: np.ndarray, second: np.ndarray, top: int) -> np.ndarray:
    """Reciprocal rank fusion of two ranked lists, per question.

    Each list contributes 1/(k + rank) for everything it ranked, and the sums
    decide the order. A paragraph one method ranked third and the other missed
    entirely can therefore still surface, which is the whole reason to fuse.
    """
    fused = np.empty((first.shape[0], top), dtype=np.int32)
    for row in range(first.shape[0]):
        points: dict[int, float] = {}
        for ranking in (first, second):
            for rank, item in enumerate(ranking[row].tolist(), start=1):
                points[item] = points.get(item, 0.0) + 1.0 / (RRF_K + rank)
        order = sorted(points, key=lambda item: -points[item])[:top]
        fused[row] = np.array(order + [-1] * (top - len(order)), dtype=np.int32)
    return fused


def main() -> int:
    """Measure one method or both, and write the figures."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--only",
        choices=("bm25", "dense"),
        help="kör en metod i taget, så baslinjen kan mätas för sig",
    )
    args = parser.parse_args()

    paragraphs = read(PARAGRAPHS)
    index = {(row["ref"], row["number"]): i for i, row in enumerate(paragraphs)}
    texts = [row["text"] for row in paragraphs]

    questions = read(EVAL)
    # Whitespace in the question is collapsed, because a paragraph's own line
    # breaks are a feature of the PDF rather than of the language.
    queries = [re.sub(r"\s+", " ", row["text"]).strip() for row in questions]
    gold = [
        {index[(row["ref"], number)] for number in row["facit"]} for row in questions
    ]

    print(f"{len(queries)} frågor mot {len(texts)} stycken")
    # The fusion needs deeper lists than the cut it is measured at, or a
    # paragraph ranked eleventh by one method can never reach the top ten.
    depth = MRR_AT * 5
    results = []
    rankings = {}
    for name in ("bm25", "dense"):
        if args.only and args.only != name:
            continue
        print(f"kör {name} ...", flush=True)
        rankings[name] = (
            bm25_ranking(texts, queries, depth)
            if name == "bm25"
            else dense_ranking(queries, depth)
        )
    if len(rankings) == 2:
        print("kör hybrid ...", flush=True)
        rankings["hybrid"] = fuse(rankings["bm25"], rankings["dense"], depth)
    for name, ranked in rankings.items():
        per = [score(ranked[i], gold[i]) for i in range(len(queries))]
        summary = summarise(per, name, len(queries))
        results.append(summary)
        print("   ", json.dumps(summary, ensure_ascii=False))

    if args.only:
        print("delkörning, filen skrivs inte om")
        return 0

    OUT.write_text(
        json.dumps(
            {
                "fragor": len(queries),
                "stycken": len(texts),
                "facit_per_fraga": round(sum(len(g) for g in gold) / len(gold), 2),
                "bm25_parametrar": {"k1": K1, "b": B},
                "rrf_k": RRF_K,
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
