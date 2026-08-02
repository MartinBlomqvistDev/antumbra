"""Tests for the permit-condition data contracts.

These assert the design decisions documented in docs/VILLKORSSCHEMA.md, so a
change that quietly breaks one of them fails here rather than in the analysis.
"""

from datetime import date, datetime
from decimal import Decimal

import pytest
from pydantic import ValidationError

from schema import (
    ClassificationMethod,
    Condition,
    ConditionType,
    DateSource,
    Decision,
    DecisionType,
    Extraction,
    ExtractionMethod,
    Operator,
    QuantifiedRequirement,
    Species,
)

EXTRACTION = Extraction(
    method=ExtractionMethod.PDFTOTEXT,
    source_file="Trelleborg_Stora_Markie_2022-09-08.pdf",
    source_size_kb=331,
    page_from=3,
    page_to=3,
    char_quality=0.99,
    extracted_at=datetime(2026, 8, 2, 10, 0),
    pipeline_version="0.1.0",
)


def noise_limit(value: str, qualifier: str) -> QuantifiedRequirement:
    """Build one equivalent-noise limit as it appears in the source decisions."""
    return QuantifiedRequirement(
        subject="ekvivalent ljudniva vid bostader",
        operator=Operator.AT_MOST,
        value=Decimal(value),
        unit="dB(A)",
        qualifier=qualifier,
        quote=f"{value} dB(A) {qualifier}",
        classification_method=ClassificationMethod.RULE,
        classification_confidence=1.0,
    )


def condition(**overrides) -> Condition:
    """Stora Markie condition 11: four noise limits in one numbered condition."""
    fields = {
        "condition_id": "skane:551-7167-2022:11",
        "decision_id": "skane:551-7167-2022",
        "number": "11",
        "position": 11,
        "heading": "Buller",
        "text": "Buller fran verksamheten far inte ge upphov till hogre ...",
        "condition_type": ConditionType.NOISE,
        "type_method": ClassificationMethod.RULE,
        "type_confidence": 1.0,
        "requirements": [
            noise_limit("50", "dagtid helgfri man-fre 06-18"),
            noise_limit("45", "dagtid lor-, son- och helgdag 06-18"),
            noise_limit("45", "kvall 18-22"),
            noise_limit("40", "natt 22-06"),
        ],
        "valid_from": date(2022, 9, 8),
        "valid_from_source": DateSource.PROXY_DECISION_DATE,
        "extraction": EXTRACTION,
    }
    return Condition(**{**fields, **overrides})


class TestGrain:
    """The row is the numbered condition; requirements nest inside it."""

    def test_one_condition_holds_several_quantified_requirements(self):
        assert len(condition().requirements) == 4

    def test_a_condition_may_carry_no_requirements(self):
        assert condition(requirements=[]).requirements == []


class TestValidity:
    """Validity intervals drive the point-in-time join against inspection dates."""

    def test_reversed_interval_is_rejected(self):
        with pytest.raises(ValidationError, match="valid_to"):
            condition(valid_to=date(2020, 1, 1))

    def test_equal_dates_are_accepted(self):
        assert condition(valid_to=date(2022, 9, 8)).valid_to == date(2022, 9, 8)

    def test_every_date_carries_its_own_source(self):
        assert condition().valid_from_source is DateSource.PROXY_DECISION_DATE


class TestProvenance:
    """Every derived field must be filterable on reliability."""

    def test_confidence_is_bounded(self):
        for bad in (-0.1, 1.4):
            with pytest.raises(ValidationError):
                condition(type_confidence=bad)

    def test_extraction_method_is_recorded(self):
        assert condition().extraction.method is ExtractionMethod.PDFTOTEXT


class TestImmutability:
    """Rows are frozen so an analysis cannot silently rewrite the corpus."""

    def test_condition_is_frozen(self):
        with pytest.raises(ValidationError):
            condition().number = "12"


class TestNumericPrecision:
    """Legal thresholds are exact; floating point would not be."""

    def test_values_are_decimal(self):
        assert isinstance(condition().requirements[0].value, Decimal)

    def test_decimal_comparison_is_exact(self):
        assert noise_limit("40", "natt").value == Decimal("40")


class TestSpecies:
    """Cattle is in scope even though the published corpus is pig and poultry."""

    def test_cattle_is_available(self):
        assert Species.CATTLE.value == "cattle"

    def test_a_cattle_decision_under_code_1_11_validates(self):
        decision = Decision(
            decision_id="ostergotland:test",
            dnr="551-0000-2026",
            facility_number=None,
            mpd="ostergotland",
            decision_date=date(2026, 1, 1),
            decision_type=DecisionType.PERMIT,
            facility_id="facility-1",
            species=Species.CATTLE,
            activity_code="1.11",
            condition_count=0,
            extraction=EXTRACTION,
        )
        assert decision.activity_code == "1.11"
