"""The retrieval layer may quote the corpus and may do nothing else.

The unit tests run everywhere: they use a synthetic corpus and a
deterministic embedder, so CI never downloads a model. The final test runs
against the real corpus and skips itself where the corpus is absent.
"""

import importlib.util
import json
from dataclasses import replace
from pathlib import Path

import numpy as np
import pytest

from retrieval import (
    Candidate,
    Paragraph,
    ThresholdSelector,
    ask,
    assemble,
    load_corpus,
    load_embeddings,
)

ROOT = Path(__file__).resolve().parent.parent


class HashEmbedder:
    """Deterministic vectors without any model: same text, same vector."""

    dimension = 16

    def encode(self, texts: list[str]) -> np.ndarray:
        vectors = []
        for text in texts:
            seed = int.from_bytes(text.encode("utf-8")[:8].ljust(8, b"\0"), "big")
            state = np.random.default_rng(seed % (2**32))
            vector = state.standard_normal(self.dimension).astype(np.float32)
            vectors.append(vector / np.linalg.norm(vector))
        return np.stack(vectors)


def corpus() -> list[Paragraph]:
    return [
        Paragraph("2001-1001", "Sweden", 12, "Residues of antibiotics were found."),
        Paragraph("2003-2002", "Denmark", 7, "The laboratory lacked accreditation."),
        Paragraph("2005-3003", "Poland", 44, "Border checks were satisfactory."),
    ]


def matrix(paragraphs: list[Paragraph]) -> np.ndarray:
    return HashEmbedder().encode([p.text for p in paragraphs])


class TestAnswersAreVerbatim:
    def test_asking_with_its_own_text_returns_the_paragraph_verbatim(self):
        paragraphs = corpus()
        answers = ask(
            question=paragraphs[0].text,
            embedder=HashEmbedder(),
            selector=ThresholdSelector(0.99),
            matrix=matrix(paragraphs),
            paragraphs=paragraphs,
        )
        assert [a.text for a in answers] == [paragraphs[0].text]
        assert answers[0].ref == "2001-1001"
        assert answers[0].country == "Sweden"
        assert answers[0].number == 12

    def test_a_paraphrasing_selector_is_refused(self):
        """The guarantee of ADR-0015: rewritten text cannot leave the module."""
        paragraphs = corpus()

        class Paraphraser:
            def select(self, question: str, candidates: list) -> list:
                """Return a tampered quotation."""
                tampered = replace(
                    candidates[0].paragraph,
                    text="Antibiotic residues were detected.",
                )
                return [Candidate(tampered, candidates[0].score)]

        with pytest.raises(ValueError, match="not verbatim"):
            ask(
                question="antibiotics",
                embedder=HashEmbedder(),
                selector=Paraphraser(),
                matrix=matrix(paragraphs),
                paragraphs=paragraphs,
            )

    def test_assemble_carries_the_source_reference_untouched(self):
        paragraphs = corpus()
        answers = assemble([Candidate(paragraphs[1], 0.9)], set(paragraphs))
        assert answers[0].text == paragraphs[1].text
        assert (answers[0].ref, answers[0].number) == ("2003-2002", 7)

    def test_a_correct_quotation_under_a_false_citation_is_refused(self):
        """Attributing one country's words to another is the worse failure.

        Found by probing the first implementation, which validated the text
        alone and let the citation through untouched.
        """
        paragraphs = corpus()
        misattributed = replace(paragraphs[0], country="Denmark", ref="9999-9999")
        with pytest.raises(ValueError, match="not verbatim"):
            assemble([Candidate(misattributed, 0.9)], set(paragraphs))


class TestStaleEmbeddingsAreRefused:
    def test_a_matrix_of_the_wrong_height_stops_the_answer(self):
        """A stale embedding file would quote real text under wrong sources."""
        paragraphs = corpus()
        with pytest.raises(ValueError, match="out of step"):
            ask(
                question="antibiotics",
                embedder=HashEmbedder(),
                selector=ThresholdSelector(0.0),
                matrix=matrix(paragraphs)[:2],
                paragraphs=paragraphs,
            )


class TestNothingMeansNothing:
    def test_below_threshold_returns_the_empty_answer(self):
        """An empty corpus match must be an empty answer, with nothing invented."""
        paragraphs = corpus()
        answers = ask(
            question="volcanic eruptions on Mars",
            embedder=HashEmbedder(),
            selector=ThresholdSelector(0.99),
            matrix=matrix(paragraphs),
            paragraphs=paragraphs,
        )
        assert answers == []


class TestAgainstTheRealCorpus:
    corpus_file = ROOT / "data" / "dgsante_paragraphs.jsonl"
    shard_dir = ROOT / "data" / "embeddings"

    ready = (
        corpus_file.exists()
        and shard_dir.exists()
        and any(shard_dir.glob("shard_*.npy"))
        and importlib.util.find_spec("sentence_transformers") is not None
    )

    @pytest.mark.skipif(
        not ready,
        reason="real corpus, embeddings or the embedding model not on this machine",
    )
    def test_real_answers_exist_verbatim_in_the_corpus_file(self):
        """End to end against the real data, embedding the query with the model."""
        from retrieval import SentenceTransformerEmbedder

        manifest = json.loads(
            (ROOT / "data" / "dgsante_embeddings_manifest.json").read_text("utf-8")
        )
        paragraphs = load_corpus()
        answers = ask(
            question="deficiencies in animal welfare during transport",
            embedder=SentenceTransformerEmbedder(manifest["model"]),
            selector=ThresholdSelector(0.3),
            matrix=load_embeddings(),
            paragraphs=paragraphs,
        )
        assert answers, "a corpus of 81,292 paragraphs should match this"
        raw = self.corpus_file.read_text(encoding="utf-8")
        for answer in answers:
            assert json.dumps(answer.text, ensure_ascii=False)[1:-1] in raw
