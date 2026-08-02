"""Unit tests for the action plan linker.

The plans are laid out as two-column tables, so the column split is what the
tests guard: reading a row whole mixes the audit's words with the member
state's answer, which is the one confusion this layer must not make.
"""

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def load_module():
    """Import the numbered pipeline step, whose name is not an identifier."""
    path = ROOT / "pipeline" / "09_link_action_plans.py"
    spec = importlib.util.spec_from_file_location("link_action_plans", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


parser = load_module()


class TestSplittingTheColumns:
    def test_the_two_columns_are_kept_apart(self):
        block = (
            "1   To ensure that officials are appropriately    Training sessions were\n"
            "    trained, as required by Article 6(a).         organised in seven\n"
            "                                                  centres during 2018.\n"
        )
        left, right = parser.split_columns(block, 50)
        assert "To ensure that officials" in left
        assert "Training sessions" not in left
        assert "organised in seven centres" in right

    def test_a_single_column_table_yields_no_restatement(self):
        block = "1   The manual is now applicable to all bodies.\n"
        left, right = parser.split_columns(block, None)
        assert right == ""
        assert "manual is now applicable" in left


class TestFindingTheGutter:
    def test_a_blank_channel_between_columns_is_found(self):
        lines = [
            "To ensure that officials are trained         Training sessions were held",
            "as required by Article 6(a) of the           in seven centres during the",
            "Regulation on official controls.             year under review by staff.",
            "The competent authority agreed to            Further sessions are planned",
        ]
        gutter = parser.find_gutter(lines)
        assert gutter is not None
        assert 40 <= gutter <= 46

    def test_prose_without_columns_has_no_gutter(self):
        lines = [
            "The competent authority has undertaken to review its procedures and",
            "to complete the revision of the manual before the end of the year so",
            "that inspectors have current guidance available to them in the field.",
            "A copy of the revised manual will be forwarded to the Commission.",
        ]
        assert parser.find_gutter(lines) is None


class TestAPageBreakDoesNotHideAnything:
    """The form feed that opens each page must not mask a row or a header."""

    def test_a_table_header_at_the_top_of_a_page_is_found(self):
        assert parser.HEADER.search("\fN°  Recommendation   Action Proposed\n")

    def test_a_row_at_the_top_of_a_page_opens_a_row(self):
        table = (
            "1   To ensure that officials are appropriately trained in sampling.\n"
            "\f2   To ensure that the database is operational and holds movements.\n"
        )
        assert [n for n, _ in parser.split_rows(table)] == [1, 2]


class TestComparingTheTexts:
    def test_the_same_wording_scores_high(self):
        report = (
            "To ensure that all local units enter the required data into TRACES, "
            "including consignments which require confirmation of receipt."
        )
        plan = (
            "To ensure that all local units enter the required data into TRACES, "
            "including consignments which require confirmation of receipt."
        )
        assert parser.similarity(report, plan) > 0.95

    def test_unrelated_wording_scores_low(self):
        assert (
            parser.similarity(
                "To ensure that sampling methodology is based on risk.",
                "BAES Federal Office for Food Safety BFW Federal Forest Office",
            )
            < 0.4
        )

    def test_an_empty_side_never_counts_as_agreement(self):
        assert parser.similarity("", "To ensure that officials are trained") == 0.0


class TestMeasuringHowMuchTheTextsShare:
    """Containment answers the question the symmetric ratio could not."""

    REPORT = (
        "To align the system of supervision of the facilities with the "
        "requirements laid down in Article 4.6 of the Regulation."
    )
    BLED = (
        "To align the system of supervision of the facilities with the "
        "MINISTERIO DE SANIDAD, SERVICIOS requirements laid down in "
        "Article 4.6 of the Regulation."
    )

    def test_words_bled_in_from_the_other_column_do_not_hide_a_match(self):
        assert parser.containment(self.REPORT, self.BLED) > 0.9

    def test_the_symmetric_ratio_is_what_the_bleed_defeated(self):
        """Kept as a test so the reason for the change stays visible."""
        assert parser.similarity(self.REPORT, self.BLED) < parser.containment(
            self.REPORT, self.BLED
        )

    def test_an_unrelated_recommendation_is_not_contained(self):
        other = (
            "Ensure that laboratories involved in official controls are "
            "accredited as set out in Article 37 of the Regulation."
        )
        assert parser.containment(self.REPORT, other) < 0.6

    def test_an_empty_side_contains_nothing(self):
        assert parser.containment("", self.BLED) == 0.0
        assert parser.containment(self.REPORT, "") == 0.0


class TestJudgingTheLanguage:
    def test_an_english_restatement_is_recognised(self):
        assert parser.reads_as_english(
            "To ensure that the competent authority carries out official "
            "controls in line with the requirements of the Regulation."
        )

    def test_a_restatement_in_another_language_is_recognised(self):
        assert (
            parser.reads_as_english(
                "Veiller à ce que la mise en oeuvre des plans fondés sur les "
                "principes HACCP chez les exploitants soit évaluée."
            )
            is False
        )

    def test_too_few_words_to_judge(self):
        assert parser.reads_as_english("Action plan") is None


class TestSplittingRows:
    def test_rows_are_split_on_numbering_that_counts_up(self):
        table = (
            "1   To ensure that officials are appropriately trained in sampling.\n"
            "2   To ensure that the database is operational and holds movements.\n"
        )
        assert [n for n, _ in parser.split_rows(table)] == [1, 2]

    def test_a_stray_number_does_not_open_a_row(self):
        table = (
            "1   To ensure that officials are appropriately trained in sampling.\n"
            "2   17\n"
            "3   To ensure that the database is operational and holds movements.\n"
        )
        assert [n for n, _ in parser.split_rows(table)] == [1]
