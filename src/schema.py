"""Data contracts for the permit-condition dataset.

Grain: one row in fact_condition is one numbered condition in one
decision. Quantified requirements are nested as a list on the condition
and exploded into a separate view at analysis time. All models are
frozen; mutation raises.

Verified against four full-text decisions; see VILLKORSSCHEMA.md.

Swedish loanwords kept deliberately:
    dnr: diarienummer, the registrar's case number. Unique per county
        administrative board, not nationally.
    mpd: miljoprovningsdelegation, the environmental permit delegation
        within a county administrative board that issues these permits.
    orgnr: organisationsnummer, the Swedish company registration number.
"""

from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field, model_validator


# ----------------------------------------------------------------------
# Controlled vocabularies
# ----------------------------------------------------------------------

class DecisionType(StrEnum):
    """Document type per the Jordbruksverket listing and the decision's own heading."""

    PERMIT = "permit"                        # tillstand
    AMENDMENT = "amendment"                  # andringstillstand
    EXTENSION = "extension"                  # forlangning av igangsattningstid
    COURT_RULING = "court_ruling"            # dom, MMD/MOD
    FINAL_CONDITIONS = "final_conditions"    # slutliga villkor
    COMMENCEMENT = "commencement"            # igangsattningsbeslut
    REVOCATION = "revocation"                # upphavande
    UNKNOWN = "unknown"


class ConditionType(StrEnum):
    """Controlled condition typology, derived from headings observed in the corpus sample.

    The vocabulary is additive: new members may be appended, existing
    members never change meaning. An unseen heading is classed OTHER and
    flagged for manual review; the verbatim heading is kept on the row.
    """

    GENERAL = "general"                      # the general condition (allmant)
    MANURE = "manure"                        # storage, handling, contracts, analysis
    WATER = "water"                          # stormwater, wash and rinse water
    AIR = "air"                              # ammonia, odour, dust, flue gases
    CHEMICALS_WASTE = "chemicals_waste"      # chemical products, waste, ash
    NOISE = "noise"
    MONITORING = "monitoring"                # monitoring programme, measurement
    DECOMMISSIONING = "decommissioning"      # avveckling
    OTHER = "other"


class ValidityStatus(StrEnum):
    """Condition status as of the latest corpus pass."""

    IN_FORCE = "in_force"
    SUPERSEDED = "superseded"
    REVOKED = "revoked"        # set aside by ruling or revocation decision
    LAPSED = "lapsed"          # permit never taken into use
    UNKNOWN = "unknown"


class DateSource(StrEnum):
    """How a validity date was determined. Drives reliability filtering."""

    EXPLICIT = "explicit"                        # date stated in the decision text
    PROXY_DECISION_DATE = "proxy_decision_date"
    DERIVED_LINK = "derived_link"                # via DecisionLink to a later decision
    MANUAL = "manual"
    UNKNOWN = "unknown"


class ExtractionMethod(StrEnum):
    PDFTOTEXT = "pdftotext"
    OCR = "ocr"
    MANUAL = "manual"


class ClassificationMethod(StrEnum):
    """How a derived field (type, requirement, link) was produced."""

    RULE = "rule"
    LLM = "llm"
    MANUAL = "manual"


class MatchMethod(StrEnum):
    """Rule that tied a decision to a facility, in priority order."""

    FACILITY_NUMBER = "facility_number"
    PROPERTY_MUNICIPALITY = "property_municipality"
    ORGNR_MUNICIPALITY = "orgnr_municipality"
    MANUAL = "manual"


class Operator(StrEnum):
    AT_MOST = "<="
    AT_LEAST = ">="
    EXACT = "=="
    BELOW = "<"
    ABOVE = ">"


class Species(StrEnum):
    """Livestock species a decision covers.

    PIG and POULTRY are the only species in the published permit corpus,
    which follows the IED activity code 1.10-i. CATTLE is present because
    cattle holdings above 400 animal units are permit-liable under national
    code 1.11; those decisions exist but are not published centrally, and
    are a planned later strand.
    """

    PIG = "pig"
    POULTRY = "poultry"
    CATTLE = "cattle"
    MIXED = "mixed"
    UNKNOWN = "unknown"


# ----------------------------------------------------------------------
# Provenance
# ----------------------------------------------------------------------

class Extraction(BaseModel):
    """Provenance for one extracted row.

    Carried by every Condition, DelegatedMatter and Decision so that
    analyses can filter on reliability without returning to the PDFs.

    Attributes:
        method: How the text was extracted from the source file.
        ocr_engine: Engine and version when method is OCR, else None.
        source_file: File name in the Jordbruksverket listing.
        source_size_kb: File size; below ~1000 kB indicates a born-digital
            text layer, above indicates a scan.
        page_from: First page of the source span, decision pagination.
        page_to: Last page of the source span.
        char_quality: Share of characters in the source span that belong
            to Swedish body text (0 to 1). Below 0.95 flags for review.
        reviewed: True once a human has checked the row against the source.
        extracted_at: Timestamp of the extraction run.
        pipeline_version: Git tag of the extraction code.
    """

    model_config = ConfigDict(frozen=True)

    method: ExtractionMethod
    ocr_engine: str | None = None
    source_file: str
    source_size_kb: int = Field(gt=0)
    page_from: int | None = Field(default=None, ge=1)
    page_to: int | None = Field(default=None, ge=1)
    char_quality: float = Field(ge=0.0, le=1.0)
    reviewed: bool = False
    extracted_at: datetime
    pipeline_version: str


# ----------------------------------------------------------------------
# Quantified requirement (sub-grain, nested in Condition)
# ----------------------------------------------------------------------

class QuantifiedRequirement(BaseModel):
    """One measurable requirement inside a condition.

    A condition carries zero or more requirements. Stora Markie
    condition 11 carries four noise limits and one monitoring duty;
    Motala 2021 condition 2 carries none. Cross-decision comparisons
    run on exploded requirements.

    Attributes:
        subject: What the value applies to, as a normalised short
            phrase, e.g. "equivalent sound level at dwellings" or
            "monitoring programme in place after taking into use".
        operator: Direction of the comparison.
        value: The numeric value, Decimal for exactness.
        unit: Normalised verbatim unit: "dB(A)", "months", "m3",
            "%", "ha", "kg".
        qualifier: Scope restriction where one exists, kept verbatim
            from the source, e.g. "natt kl. 22.00-06.00". None
            otherwise.
        quote: The sentence in the condition text the requirement was
            extracted from, verbatim.
        classification_method: How the requirement was identified.
        classification_confidence: Classifier certainty, 0 to 1.
    """

    model_config = ConfigDict(frozen=True)

    subject: str
    operator: Operator
    value: Decimal
    unit: str
    qualifier: str | None = None
    quote: str
    classification_method: ClassificationMethod
    classification_confidence: float = Field(ge=0.0, le=1.0)


# ----------------------------------------------------------------------
# Core tables
# ----------------------------------------------------------------------

class Condition(BaseModel):
    """One numbered condition in one decision. The dataset's grain.

    Attributes:
        condition_id: "{decision_id}:{number}".
        decision_id: FK to Decision.
        number: The condition number verbatim, str because amendment
            decisions may introduce suffixed numbers.
        position: Position in the document, 1-based, for sequence checks.
        heading: The heading the condition sits under, verbatim. None
            when the decision has no condition headings (SweHatch 2026).
        text: The condition text verbatim, including table content.
        condition_type: Controlled type, assigned per condition and not
            per heading; heading and content diverge in the sample.
        type_method: How the type was assigned.
        type_confidence: Classifier certainty.
        requirements: Quantified requirements in the condition, empty
            list when there are none.
        valid_from: Interval start. Convention: decision date as proxy,
            since the legal-force date is not stated in the decisions.
        valid_from_source: How valid_from was determined.
        valid_to: Interval end, None while the condition is held valid.
        valid_to_source: How valid_to was determined.
        status: Validity status as of the latest pass.
        superseded_by_decision_id: FK to the superseding decision when known.
        extraction: Provenance.
    """

    model_config = ConfigDict(frozen=True)

    condition_id: str
    decision_id: str
    number: str
    position: int = Field(ge=1)
    heading: str | None
    text: str = Field(min_length=1)
    condition_type: ConditionType
    type_method: ClassificationMethod
    type_confidence: float = Field(ge=0.0, le=1.0)
    requirements: list[QuantifiedRequirement] = Field(default_factory=list)
    valid_from: date | None
    valid_from_source: DateSource
    valid_to: date | None = None
    valid_to_source: DateSource = DateSource.UNKNOWN
    status: ValidityStatus = ValidityStatus.UNKNOWN
    superseded_by_decision_id: str | None = None
    extraction: Extraction

    @model_validator(mode="after")
    def _check_interval(self) -> "Condition":
        """Rejects rows with an inverted validity interval."""
        if (
            self.valid_from is not None
            and self.valid_to is not None
            and self.valid_to < self.valid_from
        ):
            raise ValueError(
                f"{self.condition_id}: valid_to precedes valid_from"
            )
        return self


class DelegatedMatter(BaseModel):
    """One item under the heading Delegationer in a decision.

    Its own table with its own grain: one matter the delegation leaves
    to the supervisory authority. Never counted as a condition.

    Attributes:
        decision_id: FK to Decision.
        position: Item position, 1-based.
        text: The item verbatim.
        subject_type: Mapping onto the condition typology, so that
            matters ceded and matters regulated can be compared per
            subject.
        classification_method: How subject_type was assigned.
        extraction: Provenance.
    """

    model_config = ConfigDict(frozen=True)

    decision_id: str
    position: int = Field(ge=1)
    text: str = Field(min_length=1)
    subject_type: ConditionType
    classification_method: ClassificationMethod
    extraction: Extraction


class Decision(BaseModel):
    """One decision document in the corpus. One row per PDF.

    Attributes:
        decision_id: "{mpd_slug}:{normalised_dnr}", e.g.
            "skane:551-7167-2022". A dnr is unique per county
            administrative board, not nationally, hence the prefix.
        dnr: Diarienummer verbatim, the registrar's case number. The
            format drifts: Skane wrote "551-7167-2022" in 2022 and
            "26665-2025" in 2026.
        facility_number: Facility or dossier number from the decision
            header, verbatim; None when absent. Format drifts here too.
        mpd: Miljoprovningsdelegation, the environmental permit
            delegation that issued the decision; one of the twelve
            groups in the Jordbruksverket listing, as a slug.
        decision_date: Date of the decision.
        decision_type: Document type.
        facility_id: FK to Facility.
        species: From file name and decision text.
        activity_code: Verbatim, e.g. "1.10 B" or "1.10-i".
        condition_count: Number of numbered conditions in the decision.
            Zero is legitimate for extensions and commencement decisions.
        referenced_dnr: Every dnr the decision text cites, verbatim.
            Raw material for link resolution.
        commencement_period_years: Years allowed before operations must
            have started (igangsattningstid), None when not stated.
        extraction: Document-level provenance.
    """

    model_config = ConfigDict(frozen=True)

    decision_id: str
    dnr: str
    facility_number: str | None
    mpd: str
    decision_date: date
    decision_type: DecisionType
    facility_id: str
    species: Species
    activity_code: str | None
    condition_count: int = Field(ge=0)
    referenced_dnr: list[str] = Field(default_factory=list)
    commencement_period_years: float | None = None
    extraction: Extraction


class DecisionLink(BaseModel):
    """One directed relation between two decisions in an amendment chain.

    A separate table because the target may sit outside the corpus;
    decisions issued before 2013 are not published.

    Attributes:
        from_decision_id: The later decision, FK to Decision.
        to_dnr: The cited dnr verbatim.
        to_decision_id: FK when the target exists in the corpus,
            else None.
        link_type: SUPERSEDES, EXTENDS, AMENDS or REVOKES.
        conditional_on_taking_into_use: True when supersession takes
            effect only once the new permit is taken into use
            ("tas i ansprak"); that date is stated in no decision.
        quote: The sentence carrying the reference, verbatim.
        classification_method: How the link was established.
        reviewed: True after manual verification of the link.
    """

    model_config = ConfigDict(frozen=True)

    from_decision_id: str
    to_dnr: str
    to_decision_id: str | None
    link_type: str = Field(pattern=r"^(supersedes|extends|amends|revokes)$")
    conditional_on_taking_into_use: bool
    quote: str
    classification_method: ClassificationMethod
    reviewed: bool = False


class Facility(BaseModel):
    """One physical facility over time. Conformed dimension.

    Attributes:
        facility_id: Surrogate key, slug of municipality and property
            designation, e.g. "motala-boberg-4-1".
        facility_numbers: Every facility or dossier number observed for
            the site; the format drifts between decisions.
        property_designations: Cadastral property designations
            (fastighetsbeteckningar) tied to the facility. One facility
            can span several properties.
        municipality: Municipality name.
        municipality_code: Four-digit SCB code, derivable from the
            first four digits of the facility number where present.
        operator_name: Current operator's name when the operator is a
            legal person. None when the operator is a natural person;
            the name is then not stored.
        orgnr: Organisationsnummer, the Swedish company registration
            number, when a legal person; else None.
        previous_operator_orgnr: Historical orgnr, for ownership changes.
        is_natural_person: True when the operator is a private individual.
        match_method: The rule that most recently tied a decision here.
        match_confidence: Match certainty, 0 to 1.
    """

    model_config = ConfigDict(frozen=True)

    facility_id: str
    facility_numbers: list[str] = Field(default_factory=list)
    property_designations: list[str] = Field(min_length=1)
    municipality: str
    municipality_code: str = Field(pattern=r"^\d{4}$")
    operator_name: str | None
    orgnr: str | None = Field(default=None, pattern=r"^\d{6}-\d{4}$")
    previous_operator_orgnr: list[str] = Field(default_factory=list)
    is_natural_person: bool
    match_method: MatchMethod
    match_confidence: float = Field(ge=0.0, le=1.0)
