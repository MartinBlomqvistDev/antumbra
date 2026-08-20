"""Guards for invariants that would otherwise break silently.

Three things can drift without anyone noticing: the generated schema module
against its source document, the figures quoted in the documentation against
the data they describe, and the rule that no personal data enters the
repository. Each is asserted here so it fails in CI rather than in public.
"""

import json
import re
import subprocess
from collections import Counter
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
def action_plans() -> list[dict]:
    """One record per recommendation answered in an action plan."""
    path = ROOT / "data" / "dgsante_action_plans.jsonl"
    return [json.loads(line) for line in path.read_text("utf-8").splitlines() if line]


@pytest.fixture(scope="module")
def warehouse() -> dict:
    """The manifest describing the dimensional model."""
    path = ROOT / "data" / "dgsante_warehouse_manifest.json"
    return json.loads(path.read_text("utf-8"))


@pytest.fixture(scope="module")
def dashboard() -> str:
    """The generated dashboard page."""
    return (ROOT / "docs" / "dashboard.html").read_text("utf-8")


@pytest.fixture(scope="module")
def graph() -> list[dict]:
    """One record per citation edge, with the paragraph it points at."""
    path = ROOT / "data" / "dgsante_graph.jsonl"
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
def grounds() -> list[dict]:
    """One record per authority statement about what was masked and why."""
    path = ROOT / "data" / "sekretessgrunder.jsonl"
    return [json.loads(line) for line in path.read_text("utf-8").splitlines() if line]


@pytest.fixture(scope="module")
def masking() -> list[dict]:
    """One record per delivered document judged by step 18."""
    path = ROOT / "data" / "maskning.jsonl"
    return [json.loads(line) for line in path.read_text("utf-8").splitlines() if line]


@pytest.fixture(scope="module")
def hidden_text() -> list[dict]:
    """One record per delivered document with a text layer."""
    path = ROOT / "data" / "dold_text.jsonl"
    return [json.loads(line) for line in path.read_text("utf-8").splitlines() if line]


@pytest.fixture(scope="module")
def conditions() -> list[dict]:
    """One record per condition segmented out of a permit decision."""
    path = ROOT / "data" / "villkor_baseline.jsonl"
    return [json.loads(line) for line in path.read_text("utf-8").splitlines() if line]


@pytest.fixture(scope="module")
def permits() -> list[dict]:
    """One record per downloaded permit decision."""
    path = ROOT / "data" / "tillstand_manifest.jsonl"
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


class TestThePipelineStaysOrdered:
    """The numbered steps are how docs and ADRs refer to the work."""

    def test_step_numbers_are_unique(self):
        steps = (ROOT / "pipeline").glob("[0-9][0-9]_*.py")
        numbers = [path.name[:2] for path in steps]
        duplicates = sorted({n for n in numbers if numbers.count(n) > 1})
        assert not duplicates, (
            f"two pipeline scripts share a step number: {duplicates}. The number "
            "is how docs and ADRs cite a step, so a collision makes every such "
            "reference ambiguous."
        )


class TestOpenItemsKnowsEveryEvent:
    """The open-items report must never guess which side an event came from."""

    def test_every_logged_event_is_mapped_to_a_side(self):
        from open_items import load, unmapped

        holes = unmapped(load())
        assert not holes, (
            f"event types missing from src/open_items.py: {sorted(holes)}. Until "
            "they are placed in OURS, THEIRS or INTERNAL the report cannot say "
            "who owes the next move, and a new event type would silently drop "
            "out of the check."
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


class TestTheGraphClosesOntoRealParagraphs:
    """Every edge must name a paragraph, and say when it cannot find one."""

    def test_every_edge_belongs_to_a_parsed_recommendation(
        self, graph, recommendations
    ):
        known = {(r["path"], r["number"]) for r in recommendations}
        assert {(e["path"], e["recommendation"]) for e in graph} <= known

    def test_edge_counts_match_the_recommendations(self, graph, recommendations):
        expected = sum(
            len(r["based_on_conclusions"]) + len(r["associated_findings"])
            for r in recommendations
        )
        assert len(graph) == expected

    def test_an_unresolved_edge_carries_no_invented_paragraph(self, graph):
        for edge in graph:
            if edge["resolved"]:
                assert edge["paragraph_text"]
            else:
                assert edge["paragraph_text"] is None
                assert edge["paragraph_kind"] is None

    def test_most_cited_paragraphs_resolve(self, graph):
        resolved = sum(1 for e in graph if e["resolved"])
        assert resolved / len(graph) >= 0.85

    def test_the_two_readings_agree_more_often_than_not(self, graph):
        """The paragraph's heading and the citation are separate evidence.

        They disagree on a real minority of edges, which is recorded rather
        than reconciled; this guards the rate against silent decay.
        """
        cited = [e for e in graph if e["resolved"] and e["cites"] == "conclusion"]
        agreeing = sum(1 for e in cited if e["paragraph_kind"] == "conclusion")
        assert agreeing / len(cited) >= 0.55


class TestActionPlansAnswerRealRecommendations:
    """A commitment must be tied to a recommendation that exists."""

    def test_every_response_names_a_plan_and_a_number(self, action_plans):
        assert action_plans
        for row in action_plans:
            assert row["plan_path"].startswith("pdf/dgsante/annexes/")
            assert 1 <= row["recommendation"] <= 40
            assert row["response"] or row["restated_recommendation"]

    def test_responses_mostly_match_a_parsed_recommendation(
        self, action_plans, recommendations
    ):
        known = {(r["ref"], r["number"]) for r in recommendations}
        matched = sum(
            1 for r in action_plans if (r["ref"], r["recommendation"]) in known
        )
        assert matched / len(action_plans) >= 0.4

    def test_the_restated_text_is_kept_so_the_link_can_be_checked(self, action_plans):
        """The plan restates the recommendation; that is the check on the link.

        A link resting on a shared number alone cannot be verified, so the
        restatement has to survive into the output for most rows.
        """
        with_text = sum(1 for r in action_plans if r["restated_recommendation"])
        assert with_text / len(action_plans) >= 0.8

    def test_a_confirmed_link_really_does_have_matching_text(self, action_plans):
        """Confirmation rests on containment, not on a symmetric ratio.

        The plans are two-column tables whose response column bleeds words
        into the restatement. A symmetric ratio punished that heavily even
        where every word of the recommendation was present, so what is
        measured is how much of the report's wording the plan holds.
        """
        for row in action_plans:
            if row["link_confirmed_by_text"]:
                assert row["text_containment"] >= 0.6
                assert row["restated_recommendation"]

    def test_a_plan_in_another_language_is_marked_as_such(self, action_plans):
        """A translated plan cannot be confirmed by comparing wording.

        Counting it as a failed match would blame the parser for a
        translation, so the language is recorded and reported apart.
        """
        judged = [r for r in action_plans if r["restated_reads_as_english"] is not None]
        assert judged
        foreign = [r for r in judged if r["restated_reads_as_english"] is False]
        assert foreign, "no plan was found in another language, which is implausible"
        assert len(foreign) / len(judged) < 0.2


class TestTheWarehouseDescribesWhatWasBuilt:
    """The Parquet tables are a build artefact; the manifest is the record.

    These run without the binaries, so CI checks that the model still has
    the shape the documentation claims and that its row counts still follow
    from the committed datasets.
    """

    EXPECTED: ClassVar[set[str]] = {
        "dim_country",
        "dim_audit",
        "dim_paragraph",
        "fact_recommendation",
        "fact_citation",
        "fact_commitment",
    }

    def test_the_star_has_its_dimensions_and_facts(self, warehouse):
        assert {t["table"] for t in warehouse["tables"]} == self.EXPECTED

    def test_every_table_declares_its_key(self, warehouse):
        for table in warehouse["tables"]:
            names = {column["name"] for column in table["columns"]}
            if table["table"].startswith("dim_"):
                assert f"{table['table'][4:]}_key" in names, table["table"]
            else:
                assert "audit_key" in names, table["table"]

    def test_row_counts_follow_from_the_committed_datasets(
        self, warehouse, recommendations, graph, action_plans, index
    ):
        rows = {t["table"]: t["rows"] for t in warehouse["tables"]}
        assert rows["fact_recommendation"] == len(recommendations)
        assert rows["fact_citation"] == len(graph)
        assert rows["fact_commitment"] == len(action_plans)
        assert rows["dim_audit"] == len(index)

    def test_the_measures_agree_with_the_facts(self, warehouse, recommendations):
        measures = warehouse["measures"]
        assert measures["recommendations"] == len(recommendations)
        stating = sum(1 for r in recommendations if r["based_on_conclusions"])
        assert measures["recommendations_stating_their_basis"] == stating
        assert measures["citations_resolved"] <= measures["citations"]

    def test_a_citation_that_did_not_resolve_is_still_a_row(self, warehouse):
        """Dropping the unresolved would flatter the model.

        The count of what could not be joined is part of the result, so the
        citation fact must hold more rows than it resolved.
        """
        measures = warehouse["measures"]
        assert measures["citations"] > measures["citations_resolved"]


class TestTheDashboardSaysWhatTheDataSays:
    """The published page is generated, so its figures must still hold.

    A dashboard that drifts from its source is worse than none: it is the
    surface a reader trusts without being able to check it.
    """

    def test_the_page_is_present_and_self_contained(self, dashboard):
        assert "<svg" in dashboard
        for forbidden in ("http://", "https://cdn", "<script src", '<link rel="style'):
            assert forbidden not in dashboard, forbidden

    def test_the_headline_figures_come_from_the_warehouse(self, dashboard, warehouse):
        measures = warehouse["measures"]
        for value in (measures["recommendations"], measures["citations"]):
            assert f"{value:,}".replace(",", chr(0x2009)) in dashboard

    def test_every_chart_has_a_table_view(self, dashboard):
        assert dashboard.count("<svg") == dashboard.count("Visa som tabell")

    def test_the_limitations_are_on_the_page(self, dashboard):
        assert "Vad sidan inte visar" in dashboard
        assert "inget betyg" in dashboard

    def test_both_themes_are_declared(self, dashboard):
        assert "prefers-color-scheme: dark" in dashboard
        assert 'data-theme="dark"' in dashboard


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


class TestTheConditionBaselineHoldsItsClaim:
    """The boilerplate null hypothesis fell, and the numbers must stay checkable.

    docs/VERIFIERAT.md states that 36 per cent of conditions share text with
    another decision and that reuse concentrates inside a permit division. If
    the segmenter drifts, those figures move and the claim silently changes,
    which is exactly the failure the retrain of Site Sentinel taught. The
    figures are pinned here, and a change to them has to be a deliberate edit
    of both the data and the document.
    """

    def test_the_corpus_is_the_one_the_document_describes(self, conditions, permits):
        assert len(permits) == 236
        assert len({p["sha256"] for p in permits}) == 235
        assert len(conditions) == 2264
        assert len({r["id"] for r in conditions}) == 173

    def test_the_two_sources_are_kept_apart(self, conditions):
        # The published figure is the born-digital one. OCR text loses
        # characters and breaks words at line ends, so pooling the two moves
        # the reuse share for an instrument reason. Both counts are pinned so
        # that a pooled headline cannot appear unnoticed.
        by_source = Counter(r["källa"] for r in conditions)
        assert by_source == {"text": 1704, "ocr": 560}
        assert len({r["id"] for r in conditions if r["källa"] == "text"}) == 120
        assert len({r["id"] for r in conditions if r["källa"] == "ocr"}) == 53

    def test_no_condition_row_carries_text(self, conditions):
        # The corpus is outside version control because the file names carry
        # private individuals' names; the hash is the only thing that may leave.
        fields = {
            "id",
            "prövningsgrupp",
            "villkorsnummer",
            "tecken",
            "källa",
            "series_ok",
        }
        for record in conditions:
            assert set(record) == fields | {"text_hash"}
            assert len(record["text_hash"]) == 16

    def test_every_condition_belongs_to_a_manifested_decision(
        self, conditions, permits
    ):
        groups = {p["id"]: p["prövningsgrupp"] for p in permits}
        for record in conditions:
            assert record["prövningsgrupp"] == groups[record["id"]]

    def test_the_series_check_still_passes_on_most_decisions(self, conditions):
        per_decision = {}
        source = {}
        for record in conditions:
            per_decision.setdefault(record["id"], []).append(record["villkorsnummer"])
            source[record["id"]] = record["källa"]
        clean = {
            i
            for i, ns in per_decision.items()
            if sorted(ns) == list(range(1, max(ns) + 1))
        }
        # OCR segments worse, and the gap is the reason the sources stay apart.
        assert sum(1 for i in clean if source[i] == "text") == 106
        assert sum(1 for i in clean if source[i] == "ocr") == 21
        for record in conditions:
            assert record["series_ok"] == (record["id"] in clean)

    @staticmethod
    def owners(rows) -> dict[str, set[str]]:
        """Which decisions carry each condition text."""
        found: dict[str, set[str]] = {}
        for record in rows:
            found.setdefault(record["text_hash"], set()).add(record["id"])
        return found

    def test_the_headline_share_of_shared_text(self, conditions):
        rows = [r for r in conditions if r["källa"] == "text"]
        owners = self.owners(rows)
        shared = {h: ids for h, ids in owners.items() if len(ids) > 1}
        repeated = sum(1 for r in rows if len(owners[r["text_hash"]]) > 1)
        assert len(owners) == 1316
        assert len(shared) == 217
        assert repeated == 605
        assert round(repeated / len(rows), 2) == 0.36

    def test_reuse_stays_inside_a_permit_division(self, conditions):
        groups = {r["id"]: r["prövningsgrupp"] for r in conditions}
        inside = {}
        for source in ("text", "ocr"):
            rows = [r for r in conditions if r["källa"] == source]
            shared = [ids for ids in self.owners(rows).values() if len(ids) > 1]
            inside[source] = (
                sum(1 for ids in shared if len({groups[i] for i in ids}) == 1),
                len(shared),
            )
        # The OCR set shares no document with the born-digital one, so its own
        # concentration is a replication and not a restatement.
        assert inside["text"] == (204, 217)
        assert inside["ocr"] == (39, 41)


class TestNoDocumentHidesBodyTextBehindALightCover:
    """The pre-registered field measure resolved to a null, and nulls drift too.

    ADR-0017 replaced "andel maskerade fält" with a covered-content measure and
    published the result: no delivered document hides body text behind anything
    light. A null result is the easiest kind of finding to lose, because an
    instrument that quietly stops detecting produces the same number as an
    instrument that correctly detects nothing. These pin both sides.
    """

    def test_the_corpus_is_the_one_the_document_describes(self, hidden_text):
        assert len(hidden_text) == 249
        by_class = Counter(r["klass"] for r in hidden_text)
        assert by_class == {"A": 125, "B": 120, "övrigt": 4}

    def test_the_measure_still_sees_the_header_boxes(self, hidden_text):
        # The detector must keep finding the known true positives. Were it to
        # return nothing at all, the null below would be vacuous.
        with_hidden = [r for r in hidden_text if r["dolda"]]
        assert len(with_hidden) == 41
        assert sum(r["dolda"] for r in hidden_text) == 232
        assert max(r["längsta_körning"] for r in hidden_text) == 13

    def test_no_body_text_is_hidden(self, hidden_text):
        assert [r["path"] for r in hidden_text if r["dold_av_ljus_täckning"]] == []
        assert max(r["längsta_i_brödtext"] for r in hidden_text) == 0

    def test_hidden_text_is_only_ever_counted_never_stored(self, hidden_text):
        fields = {
            "path",
            "mapp",
            "klass",
            "tecken",
            "dolda",
            "längsta_körning",
            "längsta_i_brödtext",
            "körningar",
            "dold_av_ljus_täckning",
        }
        for record in hidden_text:
            assert set(record) == fields
            assert isinstance(record["dolda"], int)


class TestTheP9CriteriaRestOnQuotedGrounds:
    """P9 turns on which provision each authority invoked, so it is quoted.

    Criterion (c) is a null: no authority masked class B under 30 kap. 23 §.
    A null that lives in someone's memory is a null that drifts, and this one
    decides whether an appeal is required, so it is pinned against the quoted
    grounds rather than against a recollection.
    """

    GROUND_30_23 = "30 kap. 23 § OSL"

    def test_every_ground_is_traceable_to_a_message(self, grounds):
        for record in grounds:
            assert record["meddelande_id"]
            assert record["citat"].strip()
            assert record["klass"] in {"A", "B"}
            assert isinstance(record["citat_fullstandigt"], bool)

    def test_criterion_c_is_empty(self, grounds):
        klass_b = [
            r
            for r in grounds
            if r["klass"] == "B" and self.GROUND_30_23 in r["bestammelser"]
        ]
        assert klass_b == []

    def test_criterion_b_has_a_comparison_set(self, masking):
        # (b) needs at least three other counties releasing class A unmasked.
        clean = set()
        for record in masking:
            folder = record["path"].split("/")[0]
            county, _, klass = folder.rpartition("_")
            if klass == "A" and not record["masked"]:
                clean.add(county)
        assert len(clean) == 5
        assert clean == {"dalarna", "gavleborg", "jamtland", "sodermanland", "uppsala"}

    def test_the_counties_invoking_30_23_in_class_a(self, grounds):
        counties = {
            r["myndighet"]
            for r in grounds
            if r["klass"] == "A" and self.GROUND_30_23 in r["bestammelser"]
        }
        assert counties == {
            "Gotland",
            "Halland",
            "Kronoberg",
            "Södermanland",
            "Värmland",
            "Västernorrland",
        }
