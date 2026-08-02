"""Unit tests for the paragraph parser.

These run without the corpus, so CI checks the rules themselves. Each case
below is a layout that broke an earlier version.
"""

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def load_module():
    """Import the numbered pipeline step, whose name is not an identifier."""
    path = ROOT / "pipeline" / "08_parse_paragraphs.py"
    spec = importlib.util.spec_from_file_location("parse_paragraphs", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


parser = load_module()


class TestSplittingParagraphs:
    def test_the_table_of_contents_does_not_start_the_sequence(self):
        """Contents lines look like paragraphs and used to consume 1 and 2.

        With them counted, the real first paragraph no longer continued the
        sequence and most reports were truncated to a couple of paragraphs.
        """
        text = (
            "TABLE OF CONTENTS\n"
            "1. INTRODUCTION ....................................... 1\n"
            "2. OBJECTIVES ......................................... 1\n"
            "5. FINDINGS AND CONCLUSIONS\n"
            "    1. The competent authority has been designated in line with\n"
            "       the requirements of the Regulation and coordinates work.\n"
            "    2. The audit team examined a number of approval files and\n"
            "       noted that only part of the procedure had been applied.\n"
        )
        found = parser.split_paragraphs(text)
        assert [n for _, n, _ in found] == [1, 2]
        assert "competent authority" in found[0][2]

    def test_a_lost_paragraph_does_not_discard_the_rest(self):
        """Extraction drops the odd paragraph at a page break.

        Requiring an unbroken run made one loss throw away everything after
        it, which left the median report with twelve paragraphs.
        """
        text = (
            "    1. The competent authority has been designated in line with\n"
            "       the requirements of the Regulation and coordinates work.\n"
            "    3. Customs coordinate the single window project planning the\n"
            "       introduction of a shared electronic interface this year.\n"
            "    4. The audit team examined a number of approval files and\n"
            "       noted that only part of the procedure had been applied.\n"
        )
        assert [n for _, n, _ in parser.split_paragraphs(text)] == [1, 3, 4]

    def test_numbering_does_not_jump_to_an_unrelated_sequence(self):
        text = (
            "    1. The competent authority has been designated in line with\n"
            "       the requirements of the Regulation and coordinates work.\n"
            "    47. Regulation cited in a table far from the running text and\n"
            "        carrying enough words to look like a paragraph of prose.\n"
        )
        assert [n for _, n, _ in parser.split_paragraphs(text)] == [1]


class TestAPageBreakDoesNotHideAnything:
    """The form feed that opens each page must not mask a paragraph."""

    def test_a_paragraph_at_the_top_of_a_page_is_read(self):
        text = (
            "    1. The competent authority has been designated in line with\n"
            "       the requirements of the Regulation and coordinates work.\n"
            "\f    2. The audit team examined a number of approval files and\n"
            "       noted that only part of the procedure had been applied.\n"
        )
        assert [n for _, n, _ in parser.split_paragraphs(text)] == [1, 2]

    def test_a_section_heading_at_the_top_of_a_page_is_read(self):
        assert parser.SECTION.search("\f5 FINDINGS AND CONCLUSIONS\n")


class TestLabellingParagraphs:
    def test_a_conclusions_heading_labels_what_follows(self):
        assert parser.kind_of("FINDINGS AND CONCLUSIONS", "Conclusions on listing") == (
            "conclusion"
        )

    def test_a_findings_heading_labels_what_follows(self):
        assert parser.kind_of("FINDINGS AND CONCLUSIONS", "Findings") == "finding"

    def test_section_five_alone_says_nothing(self):
        """Section 5 holds both, so its name cannot decide the kind.

        Reading it as findings by default disagreed with the citations in the
        reports themselves.
        """
        assert parser.kind_of("FINDINGS AND CONCLUSIONS", "") == "unlabelled"

    def test_the_overall_conclusion_section_speaks_for_itself(self):
        assert parser.kind_of("OVERALL CONCLUSION", "") == "conclusion"

    def test_a_sub_section_ends_the_reach_of_a_heading(self):
        text = (
            "5. FINDINGS AND CONCLUSIONS\n"
            "    Conclusions on registration\n"
            "5.2 OFFICIAL CONTROLS\n"
            "    1. The audit team examined a number of approval files here.\n"
        )
        marks = parser.headings(text)
        position = text.index("1. The audit team")
        _, label = parser.context_at(marks, position)
        assert label == ""
