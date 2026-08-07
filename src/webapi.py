"""HTTP access to the quotation apparatus.

A thin shell around the retrieval module: the corpus, the embedding matrix
and the model are loaded once, and every question is answered by
retrieval.ask(), whose guarantees pass through untouched. Answers are
verbatim paragraphs or nothing; a tampering selector raises instead of
serving; stale embeddings are refused. The service adds transport, never
interpretation, which is why the endpoint has no logic of its own.

Questions are not logged: no handler here writes the query anywhere, and
the container runs uvicorn without an access log.

Run locally, with the retrieval and api extras installed:

    uvicorn --app-dir src --factory webapi:production_app --port 8322
"""

from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

import numpy as np
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

from retrieval import (
    DEFAULT_THRESHOLD,
    Embedder,
    Paragraph,
    Selector,
    SentenceTransformerEmbedder,
    ThresholdSelector,
    ask,
    load_corpus,
    load_embeddings,
)

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "data" / "dgsante_embeddings_manifest.json"
MAX_QUESTION_LENGTH = 500
MAX_ANSWERS = 20


def create_app(
    embedder: Embedder,
    selector: Selector,
    matrix: np.ndarray,
    paragraphs: list[Paragraph],
) -> FastAPI:
    """Build the service around an already-loaded corpus.

    Args:
        embedder: Encodes the question; the tests inject a deterministic one.
        selector: Decides which candidates are worth quoting.
        matrix: The embedding matrix, row i belonging to paragraph i.
        paragraphs: The corpus in embedding order.

    Returns:
        The FastAPI application.
    """
    app = FastAPI(title="Antumbra retrieval", docs_url=None, redoc_url=None)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["GET"],
        allow_headers=[],
    )

    @app.get("/health")
    def health() -> dict[str, int]:
        """The corpus size, as a liveness signal."""
        return {"paragraphs": len(paragraphs)}

    @app.get("/ask")
    def ask_endpoint(
        q: str = Query(min_length=1, max_length=MAX_QUESTION_LENGTH),
        top: int = Query(default=5, ge=1, le=MAX_ANSWERS),
    ) -> dict[str, object]:
        """Verbatim quotations for a question, best first, or nothing."""
        answers = ask(q, embedder, selector, matrix, paragraphs)[:top]
        return {"question": q, "answers": [asdict(answer) for answer in answers]}

    return app


def production_app() -> FastAPI:
    """Load the real corpus, matrix and model, then build the service."""
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    return create_app(
        embedder=SentenceTransformerEmbedder(manifest["model"]),
        selector=ThresholdSelector(DEFAULT_THRESHOLD),
        matrix=load_embeddings(),
        paragraphs=load_corpus(),
    )
