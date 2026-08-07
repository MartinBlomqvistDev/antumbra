"""The HTTP shell must not weaken the retrieval guarantees.

The tests run against a synthetic corpus with a deterministic embedder, so
they need no model and no shards. Where fastapi is not installed, as in CI's
base environment, the whole file skips itself.
"""

import importlib.util

import numpy as np
import pytest

from retrieval import Candidate, Paragraph, ThresholdSelector

if importlib.util.find_spec("fastapi") is None:
    pytest.skip("fastapi is not installed", allow_module_level=True)

from fastapi.testclient import TestClient

from webapi import MAX_QUESTION_LENGTH, create_app


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


def client(selector=None) -> TestClient:
    paragraphs = corpus()
    matrix = HashEmbedder().encode([p.text for p in paragraphs])
    app = create_app(
        embedder=HashEmbedder(),
        selector=selector or ThresholdSelector(0.99),
        matrix=matrix,
        paragraphs=paragraphs,
    )
    return TestClient(app)


class TestAskOverHttp:
    def test_answers_arrive_verbatim_with_their_citation(self):
        response = client().get(
            "/ask", params={"q": "Residues of antibiotics were found."}
        )
        assert response.status_code == 200
        answers = response.json()["answers"]
        assert [a["text"] for a in answers] == [corpus()[0].text]
        assert answers[0]["ref"] == "2001-1001"
        assert answers[0]["country"] == "Sweden"
        assert answers[0]["number"] == 12

    def test_no_match_is_an_empty_list_not_an_invention(self):
        response = client().get("/ask", params={"q": "volcanic eruptions on Mars"})
        assert response.status_code == 200
        assert response.json()["answers"] == []

    def test_an_overlong_question_is_rejected_before_retrieval(self):
        response = client().get("/ask", params={"q": "x" * (MAX_QUESTION_LENGTH + 1)})
        assert response.status_code == 422

    def test_a_tampering_selector_fails_loudly_instead_of_serving(self):
        """The verbatim guarantee must hold through HTTP, not only in-process."""
        from dataclasses import replace

        class Paraphraser:
            def select(self, question: str, candidates: list) -> list:
                tampered = replace(
                    candidates[0].paragraph,
                    text="Antibiotic residues were detected.",
                )
                return [Candidate(tampered, candidates[0].score)]

        with pytest.raises(ValueError, match="not verbatim"):
            client(selector=Paraphraser()).get("/ask", params={"q": "antibiotics"})


class TestHealth:
    def test_health_reports_the_corpus_size(self):
        assert client().get("/health").json() == {"paragraphs": 3}
