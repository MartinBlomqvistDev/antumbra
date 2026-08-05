"""Embed every paragraph in the corpus for semantic retrieval.

Step 14 of the pipeline; run 08_parse_paragraphs.py first. Encodes the
81,292 numbered paragraphs with a local sentence-transformers model and
writes normalised float32 vectors in shards under data/embeddings/. The
shards are large and derived, so they stay outside git; the committed record
is the manifest, with the model name, dimension, row counts and a sha256 per
shard, in the same spirit as the provenance manifest (ADR-0004).

Resumable: a shard whose file already exists and matches the expected row
count is skipped, so an interrupted run continues where it stopped.

Usage:
    python pipeline/14_embed_paragraphs.py [--batch-size 64]
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
CORPUS = ROOT / "data" / "dgsante_paragraphs.jsonl"
SHARDS = ROOT / "data" / "embeddings"
MANIFEST = ROOT / "data" / "dgsante_embeddings_manifest.json"

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
SHARD_ROWS = 8192


def load_texts() -> list[str]:
    """Every paragraph text, in corpus order.

    Corpus order is the contract between the shards and the metadata: row i
    of the stacked embedding matrix is line i of the corpus file.
    """
    with CORPUS.open(encoding="utf-8") as handle:
        return [json.loads(line)["text"] for line in handle]


def sha256(path: Path) -> str:
    """The file's content hash."""
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def shard_path(index: int) -> Path:
    """Where shard number `index` lives."""
    return SHARDS / f"shard_{index:04d}.npy"


def main() -> int:
    """Encode the corpus shard by shard, then write the manifest."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--batch-size", type=int, default=64)
    args = parser.parse_args()

    if not CORPUS.exists():
        print("corpus missing; run pipeline/08_parse_paragraphs.py first")
        return 1

    texts = load_texts()
    SHARDS.mkdir(parents=True, exist_ok=True)
    shard_count = (len(texts) + SHARD_ROWS - 1) // SHARD_ROWS

    model = None
    for index in range(shard_count):
        start, stop = index * SHARD_ROWS, min((index + 1) * SHARD_ROWS, len(texts))
        path = shard_path(index)
        if path.exists() and np.load(path, mmap_mode="r").shape[0] == stop - start:
            print(f"shard {index:04d}: already done, skipped")
            continue
        if model is None:
            from sentence_transformers import SentenceTransformer

            model = SentenceTransformer(MODEL_NAME)
        vectors = model.encode(
            texts[start:stop],
            batch_size=args.batch_size,
            normalize_embeddings=True,
            show_progress_bar=False,
        ).astype(np.float32)
        np.save(path, vectors)
        print(f"shard {index:04d}: {stop - start} rows encoded")

    dimension = int(np.load(shard_path(0), mmap_mode="r").shape[1])
    manifest = {
        "model": MODEL_NAME,
        "dimension": dimension,
        "rows": len(texts),
        "normalised": True,
        "shard_rows": SHARD_ROWS,
        "shards": [
            {
                "file": shard_path(i).name,
                "rows": int(np.load(shard_path(i), mmap_mode="r").shape[0]),
                "sha256": sha256(shard_path(i)),
            }
            for i in range(shard_count)
        ],
    }
    MANIFEST.write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(f"{len(texts)} paragraphs embedded in {shard_count} shards -> {MANIFEST}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
