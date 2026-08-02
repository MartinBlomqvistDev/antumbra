"""Guards for invariants that would otherwise break silently.

Three things can drift without anyone noticing: the generated schema module
against its source document, the figures quoted in the documentation against
the data they describe, and the rule that no personal data enters the
repository. Each is asserted here so it fails in CI rather than in public.
"""

import json
import re
import subprocess
from pathlib import Path
from typing import ClassVar

import pytest

ROOT = Path(__file__).resolve().parent.parent
EU27 = {
    "Austria",
    "Belgium",
    "Bulgaria",
    "Croatia",
    "Cyprus",
    "Czechia",
    "Czech Republic",
    "Denmark",
    "Estonia",
    "Finland",
    "France",
    "Germany",
    "Greece",
    "Hungary",
    "Ireland",
    "Italy",
    "Latvia",
    "Lithuania",
    "Luxembourg",
    "Malta",
    "Netherlands",
    "Poland",
    "Portugal",
    "Romania",
    "Slovakia",
    "Slovenia",
    "Spain",
    "Sweden",
}


def tracked_files() -> list[Path]:
    """List files under version control, or every file when git is absent."""
    result = subprocess.run(
        ["git", "ls-files"], cwd=ROOT, capture_output=True, text=True, check=False
    )
    if result.returncode != 0:
        return [p for p in ROOT.rglob("*") if p.is_file()]
    return [ROOT / line for line in result.stdout.split()]


@pytest.fixture(scope="module")
def index() -> list[dict]:
    """The DG SANTE audit index."""
    return json.loads((ROOT / "data" / "dgsante_index.json").read_text("utf-8"))


@pytest.fixture(scope="module")
def details() -> list[dict]:
    """One record per harvested audit detail page."""
    path = ROOT / "data" / "dgsante_details.jsonl"
    return [json.loads(line) for line in path.read_text("utf-8").splitlines() if line]


class TestSchemaIsInSyncWithItsDocument:
    """src/schema.py is generated from the code block in the design document."""

    def test_generated_module_matches_document(self):
        doc = (ROOT / "docs" / "VILLKORSSCHEMA.md").read_text("utf-8")
        blocks = re.findall(r"```(?:python)?\n(.*?)```", doc, re.S)
        expected = "\n\n".join(blocks).strip()
        actual = (ROOT / "src" / "schema.py").read_text("utf-8").strip()
        assert actual == expected, (
            "src/schema.py has drifted from docs/VILLKORSSCHEMA.md. "
            "Edit the document and regenerate the module."
        )


class TestNoPersonalDataIsCommitted:
    """The project measures authorities, never named individuals."""

    EMAIL = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-z]{2,}")
    ALLOWED_EMAILS: ClassVar[set[str]] = {
        "cm.blomqvist@gmail.com",
        "kammarrattenisundsvall@dom.se",
    }

    def test_no_third_party_email_addresses(self):
        offenders = []
        for path in tracked_files():
            if path.suffix not in {".md", ".py", ".toml", ".cff", ".yml", ".yaml"}:
                continue
            for found in self.EMAIL.findall(path.read_text("utf-8", errors="ignore")):
                if found not in self.ALLOWED_EMAILS:
                    offenders.append(f"{path.name}: {found}")
        assert not offenders, f"third-party e-mail addresses committed: {offenders}"

    def test_no_source_pdfs_are_tracked(self):
        pdfs = [p.name for p in tracked_files() if p.suffix.lower() == ".pdf"]
        assert not pdfs, (
            f"source PDFs are tracked: {pdfs}. Their file names carry the names "
            "of natural persons and belong outside version control."
        )


class TestDocumentationMatchesData:
    """Figures quoted in docs/DGSANTE.md must hold against the data files."""

    def test_index_and_details_cover_the_same_audits(self, index, details):
        assert len(index) == len(details) == 4690
        assert {r["detail_id"] for r in index} == {r["detail_id"] for r in details}

    def test_harvest_recorded_no_errors(self, details):
        assert [r for r in details if r.get("error")] == []

    def test_eu27_and_sweden_counts(self, index):
        assert sum(1 for r in index if r["country"] in EU27) == 3020
        assert sum(1 for r in index if r["country"] == "Sweden") == 98

    def test_english_coverage(self, details):
        with_english = sum(
            1 for r in details if any(x["language"] == "English" for x in r["reports"])
        )
        assert with_english == 4563

    def test_action_plan_coverage(self, details):
        with_plan = [
            r
            for r in details
            if any("action" in (a["title"] or "").lower() for a in r["annexes"])
        ]
        assert len(with_plan) == 1747
        assert sum(1 for r in with_plan if r["country"] in EU27) == 1084

    def test_two_reference_formats(self, index):
        assert sum(1 for r in index if r["ref"].startswith("CT-")) == 122
        assert sum(1 for r in index if re.fullmatch(r"\d{4}-\d{4}", r["ref"])) == 4568
