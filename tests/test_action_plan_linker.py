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
