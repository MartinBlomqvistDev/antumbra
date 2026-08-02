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


def tracked_under_pdf() -> list[Path]:
    """Tracked files under pdf/, which must always be empty."""
    return [p for p in tracked_files() if p.as_posix().find("/pdf/") != -1]


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


@pytest.fixture(scope="module")
def manifest() -> list[dict]:
    """One record per downloaded corpus file."""
    path = ROOT / "data" / "dgsante_manifest.jsonl"
    return [json.loads(line) for line in path.read_text("utf-8").splitlines() if line]


@pytest.fixture(scope="module")
def annex_classes() -> list[dict]:
    """One record per numbered annex from the older era."""
    path = ROOT / "data" / "dgsante_annex_classes.jsonl"
    return [json.loads(line) for line in path.read_text("utf-8").splitlines() if line]


@pytest.fixture(scope="module")
def recommendations() -> list[dict]:
    """One record per recommendation parsed out of a report."""
    path = ROOT / "data" / "dgsante_recommendations.jsonl"
    return [json.loads(line) for line in path.read_text("utf-8").splitlines() if line]


@pytest.fixture(scope="module")
def report_parse() -> list[dict]:
    """One record per report with the outcome of parsing it."""
    path = ROOT / "data" / "dgsante_report_parse.jsonl"
    return [json.loads(line) for line in path.read_text("utf-8").splitlines() if line]


@pytest.fixture(scope="module")
def ocr_index() -> list[dict]:
    """One record per annex put through OCR."""
    path = ROOT / "data" / "dgsante_ocr_index.jsonl"
    return [json.loads(line) for line in path.read_text("utf-8").splitlines() if line]


@pytest.fixture(scope="module")
def annex_labels() -> list[dict]:
    """Hand-read classes for the held-out samples."""
    path = ROOT / "data" / "dgsante_annex_labels.jsonl"
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


class TestAnnexClassificationHoldsAgainstHandReading:
    """The numbered annexes are classified, and the call is checkable.

    The claim these guard is the one the project would be attacked on: that
    the numbered annexes are overwhelmingly member state comments and only
    rarely action plans. A classifier that quietly drifted into counting
    mentions of a plan as a plan would invert that finding.
    """

    RESPONSES: ClassVar[set[str]] = {"action_plan", "actions_taken_response"}
    AGREEMENT_FLOOR = 0.80

    def test_every_numbered_annex_is_accounted_for(self, manifest, annex_classes):
        numbered = {
            m["path"]
            for m in manifest
            if m["kind"] == "annex" and str(m.get("title", "")).strip().isdigit()
        }
        assert {r["path"] for r in annex_classes} == numbered
        assert len(annex_classes) == 1974

    def test_a_classified_annex_always_quotes_its_evidence(self, annex_classes):
        undecided = {"unclassified_text", "needs_ocr", "needs_conversion"}
        classified = [r for r in annex_classes if r["class"] not in undecided]
        assert classified
        assert all(r["evidence"].strip() for r in classified)
        assert all(r["method"] for r in annex_classes)

    def test_agreement_with_hand_read_labels(self, annex_classes, annex_labels):
        predicted = {r["path"]: r["class"] for r in annex_classes}
        assert {r["path"] for r in annex_labels} <= set(predicted)
        agreed = sum(1 for r in annex_labels if predicted[r["path"]] == r["label"])
        assert agreed / len(annex_labels) >= self.AGREEMENT_FLOOR

    def test_no_document_is_called_a_plan_that_is_not_one(
        self, annex_classes, annex_labels
    ):
        predicted = {r["path"]: r["class"] for r in annex_classes}
        wrong = [
            r["path"]
            for r in annex_labels
            if predicted[r["path"]] in self.RESPONSES
            and r["label"] not in self.RESPONSES
        ]
        assert not wrong, f"classified as a plan or response but is not: {wrong}"

    def test_action_plans_stay_a_small_minority(self, annex_classes):
        plans = sum(1 for r in annex_classes if r["class"] in self.RESPONSES)
        assert plans / len(annex_classes) < 0.10


class TestTheCitationGraphIsWhatTheReportsSay:
    """Parsed recommendations must stay tied to the documents they came from.

    The graph is the analytic payload of the DG SANTE layer, so the numbers
    quoted about its size have to hold, and an audit that made no
    recommendation has to stay visible as a zero rather than a gap.
    """

    def test_every_report_has_an_outcome(self, manifest, report_parse):
        reports = {m["path"] for m in manifest if m["kind"] == "report"}
        assert {r["path"] for r in report_parse} == reports
        assert len(report_parse) == 2940

    def test_recommendations_belong_to_parsed_reports(
        self, recommendations, report_parse
    ):
        parsed = {r["ref"] for r in report_parse if r["outcome"] == "parsed"}
        assert {r["ref"] for r in recommendations} <= parsed
        assert len(recommendations) > 8000

    def test_numbering_runs_from_one_without_gaps(self, recommendations):
        """Grouped by file, not by audit: 15 audits have two English reports.

        Where an audit was reissued, both files carry their own numbering
        from one, so grouping by reference would look like a gap.
        """
        by_file: dict[str, list[int]] = {}
        for row in recommendations:
            by_file.setdefault(row["path"], []).append(row["number"])
        for path, found in by_file.items():
            assert found == list(range(1, len(found) + 1)), path

    def test_no_recommendation_is_empty(self, recommendations):
        assert all(len(r["text"]) >= 40 for r in recommendations)

    def test_cross_references_are_paragraph_numbers_not_citations(
        self, recommendations
    ):
        """Article and regulation numbers must never enter the graph.

        A regulation is cited as "2017/625", and a pattern that read digits
        greedily once turned that into edges numbered 201, 7 and 625.
        """
        for row in recommendations:
            for number in row["based_on_conclusions"] + row["associated_findings"]:
                assert 1 <= number <= 300, row["ref"]
            assert len(row["based_on_conclusions"]) <= 10

    def test_an_audit_without_recommendations_stays_visible(self, report_parse):
        stated = [r for r in report_parse if r["outcome"] == "states_no_recommendation"]
        assert stated, "an explicit zero must never be folded into a parse failure"

    def test_recall_on_the_reports_that_carry_the_graph(self, report_parse):
        stating = [r for r in report_parse if r.get("section_states_links")]
        parsed = [r for r in stating if r["outcome"] == "parsed"]
        assert len(parsed) / len(stating) >= 0.85


class TestOcrIndexIsHonestAboutQuality:
    """OCR output is evidence of varying quality, and says so per file."""

    def test_every_ocr_record_belongs_to_a_known_annex(self, annex_classes, ocr_index):
        known = {r["path"] for r in annex_classes}
        assert {r["path"] for r in ocr_index} <= known
        assert len(ocr_index) == 1018

    def test_confidence_is_recorded_and_plausible(self, ocr_index):
        readable = [r for r in ocr_index if not r["error"]]
        assert readable
        assert all(0.0 <= r["mean_confidence"] <= 100.0 for r in readable)
        assert all(r["words"] > 0 for r in readable)

    def test_an_unreadable_file_is_reported_not_hidden(self, ocr_index):
        for record in ocr_index:
            if record["error"]:
                assert record["words"] == 0
            else:
                assert record["text_path"]


class TestManifestCoversTheDownloadedCorpus:
    """The committed manifest must mirror the EU-27 subset of the details.

    The corpus itself lives outside version control, so the manifest is the
    only guard CI has that the download was complete and attributable.
    """

    @staticmethod
    def expected_stems(details) -> tuple[set[str], set[str]]:
        reports: set[str] = set()
        annexes: set[str] = set()
        for rec in details:
            if rec["country"] not in EU27:
                continue
            for report in rec["reports"]:
                if report["language"] == "English":
                    reports.add(f"{rec['ref']}_{report['id']}_en")
            for annex in rec["annexes"]:
                annexes.add(f"{rec['ref']}_{annex['id']}")
        return reports, annexes

    def test_manifest_matches_the_details_exactly(self, details, manifest):
        reports, annexes = self.expected_stems(details)
        got_reports = {Path(m["path"]).stem for m in manifest if m["kind"] == "report"}
        got_annexes = {Path(m["path"]).stem for m in manifest if m["kind"] == "annex"}
        assert got_reports == reports
        assert got_annexes == annexes

    def test_headline_counts_hold(self, manifest):
        assert len(manifest) == 7963
        assert sum(1 for m in manifest if m["kind"] == "report") == 2940
        assert sum(1 for m in manifest if m["kind"] == "annex") == 5023

    def test_manifest_is_the_only_committed_trace_of_the_corpus(self, manifest):
        assert all(m["path"].startswith("pdf/") for m in manifest)
        assert not (ROOT / "pdf").exists() or not tracked_under_pdf()

    def test_every_row_is_hashed_and_nonempty(self, manifest):
        assert all(re.fullmatch(r"[0-9a-f]{64}", m["sha256"]) for m in manifest)
        assert all(m["bytes"] > 0 for m in manifest)
        assert all(m["kind"] in {"report", "annex"} for m in manifest)
