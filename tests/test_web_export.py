"""Unit tests for the web export.

The export's one job is double-entry: nothing reaches the site without the
cloud marts and the local warehouse agreeing. The tests guard the refusals
and the arithmetic with synthetic rows; no BigQuery, no Parquet.
"""

import importlib.util
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent


def load_module():
    """Import the numbered pipeline step, whose name is not an identifier."""
    path = ROOT / "pipeline" / "15_export_web_data.py"
    spec = importlib.util.spec_from_file_location("export_web_data", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


export = load_module()


def audits():
    return [
        {
            "audit_key": 1,
            "ref": "2019-1111",
            "year": 2019,
            "title": "Animal welfare",
            "country": "Sweden",
            "in_eu27": True,
        },
        {
            "audit_key": 2,
            "ref": "2019-2222",
            "year": 2019,
            "title": "Feed controls",
            "country": "Sweden",
            "in_eu27": True,
        },
    ]


def recommendations():
    return [
        {
            "recommendation_key": 1,
            "audit_key": 1,
            "report_path": "pdf/a.pdf",
            "number": 1,
            "text": "Ensure inspections are unannounced.",
            "legal_basis": "Article 9",
            "states_its_basis": True,
            "is_answered": True,
            "answer_confirmed_by_text": False,
        },
        {
            "recommendation_key": 2,
            "audit_key": 2,
            "report_path": "pdf/b.pdf",
            "number": 1,
            "text": "Accredit the laboratory.",
            "legal_basis": None,
            "states_its_basis": False,
            "is_answered": False,
            "answer_confirmed_by_text": False,
        },
    ]


class TestSlugs:
    def test_spaces_become_single_hyphens(self):
        assert export.slugify("Czech Republic") == "czech-republic"

    def test_accents_and_apostrophes_reduce_to_ascii(self):
        assert export.slugify("Côte d'Ivoire") == "cote-d-ivoire"


class TestLocalRecomputation:
    def test_counts_group_by_country_and_year(self):
        rows = export.local_country_year(recommendations(), audits())
        assert rows == [
            {
                "country": "Sweden",
                "in_eu27": True,
                "audit_year": 2019,
                "recommendations": 2,
                "audits": 2,
                "stating_their_basis": 1,
                "answered": 1,
                "confirmed": 0,
            }
        ]

    def test_shares_derive_from_the_verified_counts(self):
        counts = export.local_country_year(recommendations(), audits())
        rows = export.with_shares(counts)
        assert rows[0]["share_stating_their_basis"] == 0.5
        assert rows[0]["slug"] == "sweden"


class TestDoubleEntry:
    def test_agreeing_sides_pass(self):
        local = export.local_country_year(recommendations(), audits())
        export.reconcile([dict(row) for row in local], local)

    def test_a_differing_count_stops_the_export(self):
        local = export.local_country_year(recommendations(), audits())
        cloud = [dict(local[0], answered=2)]
        with pytest.raises(ValueError, match="answered"):
            export.reconcile(cloud, local)

    def test_a_missing_group_stops_the_export(self):
        local = export.local_country_year(recommendations(), audits())
        with pytest.raises(ValueError, match="group keys differ"):
            export.reconcile([], local)


class TestUnderlag:
    def build(self):
        return export.build_underlag(
            recommendations(),
            [
                {
                    "recommendation_key": 1,
                    "paragraph_key": 10,
                    "paragraph_number": 47,
                    "cites": "conclusion",
                    "resolved": True,
                }
            ],
            [
                {
                    "recommendation_key": 1,
                    "response": "Inspections are now unannounced.",
                    "plan_path": "pdf/plan.pdf",
                    "confirmed_by_text": True,
                }
            ],
            [
                {
                    "paragraph_key": 10,
                    "kind": "conclusion",
                    "section": "6",
                    "text": "Inspections were announced in advance.",
                }
            ],
            audits(),
            {"pdf/a.pdf": "abc123"},
        )

    def test_the_chain_is_carried_verbatim_with_its_hash(self):
        sweden = self.build()["sweden"]
        first = sweden["audits"][0]
        assert first["sha256"] == "abc123"
        citation = first["recommendations"][0]["citations"][0]
        assert citation["text"] == "Inspections were announced in advance."
        assert first["recommendations"][0]["responses"][0]["confirmed_by_text"]

    def test_underlag_must_carry_exactly_the_marts_rows(self):
        countries = self.build()
        mart = export.with_shares(
            export.local_country_year(recommendations(), audits())
        )
        export.reconcile_underlag(countries, mart)
        mart[0]["recommendations"] = 3
        with pytest.raises(ValueError, match="the mart says 3"):
            export.reconcile_underlag(countries, mart)


class TestChainTotals:
    def test_chain_closes_needs_all_three_links(self):
        totals = export.local_chain_totals(
            recommendations(),
            [
                {
                    "recommendation_key": 1,
                    "paragraph_key": 10,
                    "paragraph_number": 47,
                    "cites": "conclusion",
                    "resolved": True,
                }
            ],
            [
                {
                    "recommendation_key": 1,
                    "response": "Done.",
                    "plan_path": "pdf/plan.pdf",
                    "confirmed_by_text": False,
                }
            ],
        )
        assert totals == {
            "recommendations": 2,
            "chain_closes": 1,
            "citations": 1,
            "citations_resolved": 1,
        }
