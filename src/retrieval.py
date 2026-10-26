"""Semantic retrieval over the paragraph corpus, quoting and never rewriting.

The corpus paragraphs are the reports' own numbered citation units, so the
answer to a question is a selection of them, returned verbatim with country,
report reference and paragraph number. The selection step sits behind a
Protocol so a language model can be slotted in later; the shipped
implementation selects by similarity threshold and nothing else. Whatever
selects, the assembler refuses to return any text that is not
character-identical to the source paragraph, so a paraphrase cannot leave
this module (ADR-0015).

Usage:
    python -m src.retrieval "antibiotic residues in poultry" [--top 5]
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Protocol

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
CORPUS = ROOT / "data" / "dgsante_paragraphs.jsonl"
SHARDS = ROOT / "data" / "embeddings"

DEFAULT_CANDIDATES = 20
DEFAULT_THRESHOLD = 0.45


@dataclass(frozen=True)
class Paragraph:
    """One numbered paragraph, exactly as parsed from its report."""

    ref: str
    country: str
    number: int
    text: str


@dataclass(frozen=True)
class Candidate:
    """A paragraph with its similarity to the question."""

    paragraph: Paragraph
    score: float


@dataclass(frozen=True)
class Answer:
    """A verbatim quotation with its source."""

    text: str
    ref: str
    country: str
    number: int
    score: float


class Embedder(Protocol):
    """Turns texts into normalised vectors; injectable so tests stay offline."""

    def encode(self, texts: list[str]) -> np.ndarray:
        """Normalised vectors, one row per text."""
        ...


class Selector(Protocol):
    """Chooses which candidates answer the question.

    A selector may only pick from the candidates it is given. It never
    writes text: the assembler enforces that whatever comes back is
    character-identical to the source paragraph.
    """

    def select(self, question: str, candidates: list[Candidate]) -> list[Candidate]:
        """The candidates worth quoting, in answer order."""
        ...


class ThresholdSelector:
    """Keeps every candidate at or above a similarity threshold."""

    def __init__(self, threshold: float = DEFAULT_THRESHOLD) -> None:
        """Remember the similarity floor."""
        self.threshold = threshold

    def select(self, question: str, candidates: list[Candidate]) -> list[Candidate]:
        """The candidates similar enough to quote, or nothing."""
        return [c for c in candidates if c.score >= self.threshold]


class SentenceTransformerEmbedder:
    """The same local model the corpus was embedded with."""

    def __init__(self, model_name: str) -> None:
        """Load the model named in the embeddings manifest."""
        from sentence_transformers import SentenceTransformer

        self.model = SentenceTransformer(model_name)

    def encode(self, texts: list[str]) -> np.ndarray:
        """Normalised float32 vectors for the given texts."""
        return self.model.encode(texts, normalize_embeddings=True).astype(np.float32)


def load_corpus(path: Path = CORPUS) -> list[Paragraph]:
    """Every paragraph, in the same order as the embedding rows."""
    paragraphs = []
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            row = json.loads(line)
            paragraphs.append(
                Paragraph(
                    ref=row["ref"],
                    country=row["country"],
                    number=row["number"],
                    text=row["text"],
                )
            )
    return paragraphs


def load_embeddings(directory: Path = SHARDS) -> np.ndarray:
    """The stacked embedding matrix from step 14's shards."""
    shards = sorted(directory.glob("shard_*.npy"))
    if not shards:
        raise FileNotFoundError(
            "no embedding shards found; run pipeline/14_embed_paragraphs.py first"
        )
    return np.vstack([np.load(path) for path in shards])


def top_candidates(
    question: str,
    embedder: Embedder,
    matrix: np.ndarray,
    paragraphs: list[Paragraph],
    count: int = DEFAULT_CANDIDATES,
) -> list[Candidate]:
    """The paragraphs most similar to the question, best first.

    Vectors are normalised, so the dot product is the cosine similarity and
    brute force over the whole matrix answers in milliseconds (ADR-0015).
    """
    query = embedder.encode([question])[0]
    scores = matrix @ query
    order = np.argsort(scores)[::-1][:count]
    return [Candidate(paragraphs[i], float(scores[i])) for i in order]


def assemble(selected: list[Candidate], corpus: set[Paragraph]) -> list[Answer]:
    """Turn selected candidates into answers, enforcing verbatim quotation.

    The check is the guarantee the whole module exists for: no selector,
    present or future, can smuggle rewritten text past this point. It
    validates the whole paragraph, its text among the parts, because a correct
    quotation under a fabricated citation would put one member state's words
    in another's mouth. That is a worse failure than a paraphrase, and 801
    paragraphs in the corpus share their text with another paragraph, so
    checking the text alone would not even place a quotation reliably.
    """
    answers = []
    for candidate in selected:
        if candidate.paragraph not in corpus:
            raise ValueError(
                "selected paragraph is not verbatim from the corpus: "
                f"{candidate.paragraph.ref} paragraph {candidate.paragraph.number}"
            )
        answers.append(
            Answer(
                text=candidate.paragraph.text,
                ref=candidate.paragraph.ref,
                country=candidate.paragraph.country,
                number=candidate.paragraph.number,
                score=candidate.score,
            )
        )
    return answers


def ask(
    question: str,
    embedder: Embedder,
    selector: Selector,
    matrix: np.ndarray,
    paragraphs: list[Paragraph],
    candidates: int = DEFAULT_CANDIDATES,
) -> list[Answer]:
    """Answer a question with verbatim quotations, or with nothing.

    Row i of the matrix must be paragraph i of the corpus. A stale embedding
    file, for instance one left behind when step 08 regenerated the corpus,
    would otherwise attach real quotations to the wrong reports without
    anything looking wrong in the output, so the mismatch is refused here.
    """
    if matrix.shape[0] != len(paragraphs):
        raise ValueError(
            f"embeddings and corpus are out of step: {matrix.shape[0]} vectors "
            f"for {len(paragraphs)} paragraphs; rerun "
            "pipeline/14_embed_paragraphs.py"
        )
    found = top_candidates(question, embedder, matrix, paragraphs, candidates)
    selected = selector.select(question, found)
    return assemble(selected, set(paragraphs))


def main() -> int:
    """Ask the corpus a question from the command line."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("question")
    parser.add_argument("--top", type=int, default=5)
    parser.add_argument("--threshold", type=float, default=DEFAULT_THRESHOLD)
    args = parser.parse_args()

    import json as _json

    manifest = _json.loads(
        (ROOT / "data" / "dgsante_embeddings_manifest.json").read_text("utf-8")
    )
    paragraphs = load_corpus()
    matrix = load_embeddings()
    answers = ask(
        question=args.question,
        embedder=SentenceTransformerEmbedder(manifest["model"]),
        selector=ThresholdSelector(args.threshold),
        matrix=matrix,
        paragraphs=paragraphs,
        candidates=args.top,
    )
    if not answers:
        print("Nothing in the corpus answers the question.")
        return 0
    for answer in answers:
        print(
            f"[{answer.country}, {answer.ref}, paragraph {answer.number}, "
            f"similarity {answer.score:.2f}]"
        )
        print(answer.text)
        print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
