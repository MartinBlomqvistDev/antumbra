"""Unit tests for the recommendation parser.

These run without the corpus on disk, so CI checks the parsing rules
themselves. The sentence forms below are quoted from real reports; each one
broke an earlier version of the parser.
"""

import importlib.util
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent


def load_module():
    """Import the numbered pipeline step, whose name is not an identifier."""
    path = ROOT / "pipeline" / "07_parse_recommendations.py"
    spec = importlib.util.spec_from_file_location("parse_recommendations", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


parser = load_module()


class TestReadingParagraphNumbers:
    @pytest.mark.parametrize(
        ("blob", "expected"),
        [
            ("31", [31]),
            ("17 and 18", [17, 18]),
            ("6, 42", [6, 42]),
            ("9, 34, 35, 37, and 38", [9, 34, 35, 37, 38]),
            ("29-31, 50 and 71", [29, 30, 31, 50, 71]),
            ("61" + chr(0x2013) + "62", [61, 62]),
        ],
    )
    def test_lists_and_ranges(self, blob, expected):
        assert parser.numbers(blob) == expected

    def test_a_range_too_long_to_be_real_is_read_as_two_numbers(self):
        assert parser.numbers("5-900") == [5, 900]


class TestFindingTheReferences:
    @pytest.mark.parametrize(
        ("sentence", "conclusions", "findings"),
        [
            (
                "Recommendation based on conclusion: 31. "
                "Associated findings: 22 and 23.",
                [31],
                [22, 23],
            ),
            (
                "The recommendation is based on conclusions No 19 and 46. "
                "Associated findings No 6 and 42.",
                [19, 46],
                [6, 42],
            ),
            (
                "Recommendation based on conclusion Nos. 35 and 50 "
                "Associated finding Nos. 29 and 47",
                [35, 50],
                [29, 47],
            ),
            (
                "Based on conclusion 52, and associated findings 36 and 37.",
                [52],
                [36, 37],
            ),
        ],
    )
    def test_real_sentence_forms(self, sentence, conclusions, findings):
        assert parser.numbers(parser.CONCLUSIONS.search(sentence).group(1)) == (
            conclusions
        )
        assert parser.numbers(parser.FINDINGS.search(sentence).group(1)) == findings

    def test_a_legal_citation_does_not_become_an_edge(self):
        """Article and regulation numbers must not be read as paragraphs.

        An earlier character-class pattern ran past the full stop and turned
        "2017/625" into edges numbered 201, 7 and 625.
        """
        sentence = (
            "Recommendation based on conclusion No 33. Associated findings Nos 16-19. "
            "To review the guidance under Article 5(1) of Regulation (EU) 2017/625."
        )
        assert parser.numbers(parser.CONCLUSIONS.search(sentence).group(1)) == [33]
        assert parser.numbers(parser.FINDINGS.search(sentence).group(1)) == [
            16,
            17,
            18,
            19,
        ]


class TestSplittingTheSection:
    def test_numbering_that_counts_up_is_split(self):
        section = (
            "The CA should:\n"
            "1. Ensure that official controls are planned as required by law.\n"
            "   Recommendation based on conclusion 5.\n"
            "2. Ensure that inspectors receive documented training in good time.\n"
        )
        items = parser.split_items(section)
        assert [n for n, _ in items] == [1, 2]
        assert "planned" in items[0][1]

    def test_a_number_alone_on_its_line_still_opens_an_item(self):
        section = (
            "No.     Recommendation\n"
            "    1.\n"
            "        Ensure that inspections of consignments follow the documented\n"
            "        procedure in line with Article 12(1).\n"
        )
        assert [n for n, _ in parser.split_items(section)] == [1]

    def test_parenthesised_numbering_from_the_older_reports(self):
        section = (
            "9.1. To the competent authorities of Italy\n"
            "  (1) Action should be taken to address the shortage of "
            "veterinary staff in the regions.\n"
            "  (2) Action should be taken to ensure the respect of EU "
            "legislation on milk processing.\n"
        )
        assert [n for n, _ in parser.split_items(section)] == [1, 2]

    def test_a_stray_number_in_sequence_does_not_split_a_recommendation(self):
        section = (
            "1. Ensure that official controls are carried out on a risk basis and "
            "that the results are recorded in the national database.\n"
            "2\n"
            "3. Ensure that laboratories are accredited as set out in Article 37.\n"
        )
        items = parser.split_items(section)
        assert [n for n, _ in items] == [1]


class TestTheTwoColumnTable:
    """The layout that the action plans exposed as systematically misparsed.

    The left column holds only the numbers. Over a page break the numbers of
    the next page are emitted in a run of their own, away from the text they
    belong to, and reading the section line by line found one recommendation
    where the report has five.
    """

    TABLE = (
        "N°.     Recommendation\n"
        "    1.  To register operators being final users of oils in bags of up\n"
        "\n"
        "        10\n"
        "\n"
        "N°.     Recommendation\n"
        "    2.\n"
        "    3.  to 50 kg, as required by Article 23 of Regulation 1069/2009.\n"
        "\n"
        "        To approve the plant manufacturing oils as required by Article\n"
        "        24 of Regulation 1069/2009.\n"
        "\n"
        "        To ensure that commercial documents accompany the oils sold to\n"
        "        operators being final users, as required by Article 21.\n"
    )

    def test_the_numbers_are_paired_with_their_own_text(self):
        rows = parser.split_table(self.TABLE)
        assert [n for n, _ in rows] == [1, 2, 3]
        assert "To approve the plant" in rows[1][1]

    def test_a_recommendation_broken_over_a_page_is_joined_back(self):
        rows = parser.split_table(self.TABLE)
        assert "To register operators" in rows[0][1]
        assert "Article 23 of Regulation 1069/2009" in rows[0][1]

    def test_the_repeated_header_does_not_reach_the_text(self):
        for _, text in parser.split_table(self.TABLE):
            assert "Recommendation" not in text
            assert "N°" not in text

    def test_columns_that_do_not_line_up_are_left_alone(self):
        """Pairing on a mismatch would invent recommendations."""
        body = (
            "    1.  To register operators being final users of oils in bags.\n"
            "    2.\n"
            "    3.\n"
        )
        assert parser.pair_columns(body, 8) == []

    def test_prose_without_a_table_header_is_not_treated_as_one(self):
        section = (
            "The CA should:\n"
            "1. Ensure that official controls are planned as required by law.\n"
        )
        assert parser.split_table(section) == []


class TestHierarchicalNumbering:
    """The older reports number recommendations inside the section hierarchy.

    A parser that only knew flat numbering read none of the 337 reports
    written this way, and their sections were recorded as holding no items.
    """

    SECTION = (
        "7.1. To the Competent Authorities of Croatia:\n"
        "7.1.1. To define the role of the Veterinary Stations and of the\n"
        "       authorised veterinary inspectors within the export plants.\n"
        "7.1.2. To take action to rectify structural and hygienic deficiencies\n"
        "       seen in some of the plants that the mission visited.\n"
        "7.1.3. To ensure that the approval procedure is applied consistently\n"
        "       across all of the establishments concerned.\n"
    )

    def test_the_leaves_are_the_recommendations(self):
        items = parser.split_hierarchical(self.SECTION)
        assert [n for n, _, _ in items] == [1, 2, 3]
        assert [label for _, label, _ in items] == ["7.1.1", "7.1.2", "7.1.3"]

    def test_the_heading_above_them_is_not_counted(self):
        for _, label, text in parser.split_hierarchical(self.SECTION):
            assert label != "7.1"
            assert "To the Competent Authorities" not in text

    def test_the_documents_own_label_is_kept(self):
        items = parser.split_hierarchical(self.SECTION)
        assert items[1][1] == "7.1.2"
        assert "rectify structural" in items[1][2]

    def test_a_single_entry_is_not_a_list(self):
        section = "8.1. To the competent authorities of Spain, action is needed.\n"
        assert parser.split_hierarchical(section) == []


class TestAPageBreakDoesNotHideAnything:
    """A form feed sits at the head of the first line of every page.

    Anchoring on spaces and tabs alone made every heading, item and table
    that opened a page invisible. It cost about a third of the citation
    graph, and nothing in the output showed it.
    """

    def test_a_heading_at_the_top_of_a_page_is_found(self):
        text = "some closing text\n\f8 RECOMMENDATIONS\n\nThe CA should act.\n"
        assert parser.HEADING.search(text)

    def test_an_item_at_the_top_of_a_page_opens_a_recommendation(self):
        section = (
            "1. Ensure that official controls are carried out on a risk basis\n"
            "   and that results are recorded in the national database.\n"
            "\f2. Ensure that laboratories are accredited as set out in the\n"
            "   Regulation on official controls.\n"
        )
        assert [n for n, _ in parser.split_items(section)] == [1, 2]

    def test_a_table_header_at_the_top_of_a_page_is_recognised(self):
        assert parser.TABLE_HEADER.search("\fN°.     Recommendation\n")

    def test_a_page_number_after_a_page_break_is_stripped(self):
        assert parser.PAGE_NUMBER.search("\f   21   \n")


class TestAnHonestZero:
    def test_a_report_stating_no_recommendation_is_recognised(self):
        assert parser.NO_RECOMMENDATION.search(
            "The report does not make any recommendation."
        )

    def test_ordinary_text_is_not_mistaken_for_a_zero(self):
        assert not parser.NO_RECOMMENDATION.search(
            "The report makes four recommendations to the competent authority."
        )


class TestMetadataIsStrippedFromTheText:
    """The fields carry the metadata; the wording must not repeat it."""

    def test_a_trailing_metadata_block_is_removed(self):
        flattened = (
            "To ensure that identity checks are performed at the minimum "
            "frequencies laid down in EU legislation. Legal basis: Articles 6 "
            "and 8 and Annexes I and II to Regulation (EU) 2019/1793 "
            "Recommendation based on conclusion:40 Associated findings: 34"
        )
        assert parser.strip_metadata(flattened) == (
            "To ensure that identity checks are performed at the minimum "
            "frequencies laid down in EU legislation."
        )

    def test_an_interior_reference_phrase_is_removed_without_eating_wording(self):
        flattened = (
            "First recommendation wording. The recommendation is based on "
            "conclusions 12 and 14. Second recommendation wording follows here."
        )
        assert parser.strip_metadata(flattened) == (
            "First recommendation wording. Second recommendation wording follows here."
        )

    def test_a_legal_basis_far_from_the_end_is_left_alone(self):
        flattened = (
            "The legal basis: framework applies. " + "Wording continues. " * 40
        ).strip()
        assert "legal basis" in parser.strip_metadata(flattened).lower()

    def test_the_legal_basis_field_stops_before_the_reference_lines(self):
        body = (
            "To ensure something.\n"
            "Legal basis: Articles 6 and 8 and Annexes I and II to Regulation "
            "(EU) 2019/1793\n"
            "Recommendation based on conclusion: 40\n"
            "Associated findings: 34\n"
        )
        match = parser.LEGAL_BASIS.search(body)
        captured = " ".join(match.group(1).split())
        assert captured.endswith("2019/1793")
        assert "based on" not in captured.lower()

    def test_a_metadata_only_block_keeps_its_text(self):
        flattened = "Recommendation based on conclusion: 40"
        assert parser.strip_metadata(flattened) == flattened

    def test_wording_that_mentions_a_legal_basis_is_not_eaten(self):
        flattened = (
            "Establish a legal basis for official controls of feed at the "
            "primary production stage."
        )
        assert parser.strip_metadata(flattened) == flattened

    def test_a_stub_after_stripping_keeps_the_original_text(self):
        flattened = (
            "Establish a Legal basis: Article 45(6) of Regulation (EC) No 882/2004."
        )
        assert parser.strip_metadata(flattened) == flattened
