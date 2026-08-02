# Antumbra: villkorsschema

Datastruktur för ett villkor i korpusen om 237 miljötillståndsbeslut för stora
gris- och fjäderfäanläggningar, 2013 till 2026. Designad 2026-08-01 mot fyra
beslut i fulltext: Lidfarm 2017 (MPD Västra Götaland), Motala 2021 2021
(MPD Östergötland), Stora Markie 2022 (MPD Skåne), SweHatch 2026 (MPD Skåne,
dnr 26665-2025, beslutsdatum 2026-06-04).

All kod är på engelska: klasser, fält, enum-medlemmar och enum-värden.
Svenska förvaltningstermer utan ren engelsk motsvarighet behålls som lånord
(`dnr`, `mpd`, `orgnr`) och förklaras i docstrings. Prosa och citat är på
svenska. Citat ur besluten återges med återställda svenska tecken;
källtexterna har trasig teckenkodning efter `pdftotext -layout`.
Sidhänvisningar avser beslutens egen paginering.

---

## 1. Pydantic v2-modellerna

```python
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
```

---

## 2. Motivering per designval

### 2.1 Vad är ett villkor som enhet

Raden är det numrerade villkoret. Kvantifierade krav ligger som nästlad
lista i `requirements` och exploderas till egen vy.

Belägg för att båda nivåerna behövs. Stora Markie villkor 11 sätter fyra
gränser och ett kontrollkrav i en punkt: "50 dB(A) dagtid helgfri
måndag-fredag, kl. 06.00 – 18.00", "45 dB(A) dagtid, lör-, sön- och helgdag",
"45 dB(A) kväll", "40 dB(A) natt", samt "De angivna värdena ska kontrolleras
genom mätning vid bullerkällorna" (s. 3). Motala 2021 villkor 11 sätter
motsvarande gränser i tabellform (s. 2).

Konsekvens om raden är villkoret: antalet rader per beslut går att verifiera
mot dokumentet självt. Stora Markie skriver i klartext "Länsstyrelsen
tillstyrker ansökan och föreslår 13 villkor" (s. 18), och Motivering av
villkor har exakt tretton rubriker. Måttet "villkor per beslut" blir
delegationens eget tal.

Konsekvens om raden är det enskilda kravet: segmenteringen blir en tolkning.
Stora Markie villkor 10 kan läsas som fyra eller sju krav beroende på var
man klipper meningarna om invallning, påkörningsskydd, nederbörd och
absorptionsmedel. Inget i dokumentet validerar valet, och delegationer med
ordrikare mall får systematiskt fler rader. Jämförelsen mellan delegationer,
projektets huvudmått, skulle mäta mallens ordrikedom.

Valet var inte jämnt; villkoret som rad vinner på verifierbarhet.

### 2.2 Villkorstypologin

Rubriker som faktiskt förekommer:

| Beslut | Rubriker över villkoren |
| --- | --- |
| Lidfarm 2017 | Inga villkor alls; förlängningsbeslut |
| Motala 2021 2021 | Allmänt; Gödselhantering m.m.; Utsläpp till luft; Kemikalie- och avfallsfrågor; Buller; Övrigt |
| Stora Markie 2022 | Allmänt; Omhändertagande av dagvatten; Lagring och hantering av gödsel; Utsläpp av ammoniak och luktande ämnen; Kemiska produkter och avfall; Buller; Kontroll av verksamheten; Avveckling |
| SweHatch 2026 | Inga rubriker; villkor 1 till 13 löper numrerade utan mellanrubriker (s. 1 till 4) |

Återkommer i alla beslut som har villkor: allmänt-villkoret, gödsel,
kemikalier och avfall, buller. Varierar: dagvatten och kontroll har egna
rubriker bara i Stora Markie; SweHatch har inga rubriker alls fast
motiveringsdelen rubricerar samma ämnen ("Villkor 7 – dagvatten",
"Villkor 12 – kontrollprogram", s. 34 och 36).

Två fynd styr designen. Först: rubriken kan saknas helt, alltså är `heading`
nullable och typen sätts per villkor av en klassificerare. Sedan: rubrik och
innehåll skiljer sig åt. Motala 2021:s villkor 12 står under "Övrigt" men är
i sak samma avvecklingsvillkor som Stora Markies villkor 13 under
"Avveckling"; båda kräver anmälan, omhändertagande av kemikalier och
utredning av föroreningar. Klassning på rubrik ensam hade räknat noll
avvecklingsvillkor i Östergötland.

Ny okänd rubrik hanteras i tre steg: rubriken bevaras ordagrant i `heading`,
typen sätts till OTHER, raden flaggas via låg `type_confidence` för manuell
granskning. Vokabulären utökas additivt; en befintlig typ byter aldrig
betydelse, så ingen omextraktion krävs. Aska och stoft placeras enligt
underlaget: Motala 2021 lägger aska under "Kemikalie- och avfallsfrågor"
(villkor 9, s. 2), alltså CHEMICALS_WASTE; stoft i rökgaser är utsläpp till
luft, alltså AIR.

### 2.3 Kvantifierade krav

`QuantifiedRequirement` bär subject, operator, value, unit och qualifier.
Beläggen för att kvalificeraren måste vara strukturbärande: nattgränsen
40 dB(A) är identisk i Motala 2021, Stora Markie och SweHatch, men
dagfönstret börjar kl. 06.00 i Stora Markie och kl. 07.00 i SweHatch,
uttryckligen motiverat: "begränsningsvärdet dagtid ska gälla från klockan
07.00 eftersom det är vad som gäller enligt nuvarande tillstånd"
(SweHatch s. 36). Utan kvalificerare ser två olika krav identiska ut.

Tidsfrister är samma modell: Stora Markie kräver kontrollprogram "senast sex
(6) månader efter att tillståndet har tagits i anspråk" (villkor 12) och
SweHatch "senast tre månader" (villkor 12). Det blir
`subject="monitoring programme in place after taking into use"`,
`operator="<="`, `value=6` respektive `3`, `unit="months"`. Samma
delegation, fyra års mellanrum, halverad frist: exakt den variation
projektet ska mäta.

Villkor utan värde är normalfallet och kräver ingenting: `requirements` är
tom lista och villkorsraden står på egna ben. Motala 2021 villkor 2,
"Hantering av gödselmedel ska ske på sådant sätt att läckage och spill samt
olägenheter för närboende förebyggs och begränsas", är fullt jämförbart via
`text` och `condition_type`; baseline-mätningen av textlikhet körs på `text`
oavsett kravlista. Varje krav bär dessutom `quote`, meningen det utvanns ur,
så att en granskare aldrig behöver gå till PDF:en.

### 2.4 Rubriken Delegationer: separat tabell

Egen tabell, `DelegatedMatter`. Tre skäl.

Grainet är ett annat: punkterna är onumrerade och är avståenden, inga krav.
Stora Markie listar sex punkter, bland annat "åtgärder för att minimera
lukt" (s. 3 till 4); Motala 2021 en enda, "de ytterligare villkor som kan
föranledas av aska från bränslepannan" (s. 3); SweHatch två, lukt och
kontroll (s. 4). I samma tabell som villkoren hade de förorenat varje
villkorsräkning.

Måttet är eget: antal delegationspunkter per beslut är projektets mått på
hur mycket prövningen lämnar ifrån sig, och det ska kunna ställas mot antal
villkor per ämne. Därför bär punkten `subject_type` ur samma typologi;
SweHatch delegerar lukt samtidigt som Stora Markie villkorsreglerar
luftrening, och den kontrasten ska gå att ta fram med en join.

Rubriken driftar dessutom: Östergötland skriver "Delegation" i singular,
Skåne "Delegationer". Parsern matchar båda; fältet i schemat är tabellnamnet.

### 2.5 Tidsdimensionen och SCD Type 2

Varje villkor bär `valid_from`, `valid_to`, `status` och källfält för båda
datumen. Länkningen mellan beslut ligger i egen tabell `DecisionLink`
eftersom den är osäker och delvis manuell.

Vad som faktiskt går att automatisera: mer än väntat. Alla tre beslut i
underlaget som förhåller sig till ett tidigare beslut citerar dess
diarienummer i klartext. Motala 2021: "När detta tillstånd tas i anspråk
upphör Miljöprövningsdelegationens beslut daterat 18 december 2012
(dnr 551-6388-12) att gälla" (s. 3). SweHatch: "upphör det av
Miljöprövningsdelegationen tidigare meddelade tillståndet
(dnr 551-13148-2017) att gälla" (s. 4). Lidfarm: "förlänger
igångsättningstiden enligt tillståndsbeslut meddelat den 4 december 2013
(dnr 551-20056-2011)" (s. 1). Regex på dnr-mönster plus närliggande verb
(upphör, förlänger, ändrar, upphäver) bygger länkkandidaterna maskinellt.

Tre saker går inte att lösa automatiskt.

Ianspråktagandet. Ersättningen är villkorad: det gamla tillståndet upphör
först "när detta tillstånd tas i anspråk", och datumet för det står inte i
något beslut; det anmäls till tillsynsmyndigheten. `valid_to` för det
ersatta villkoret sätts därför till det nya beslutets beslutsdatum med
`valid_to_source=PROXY_DECISION_DATE`, och `conditional_on_taking_into_use`
på länken markerar att datumet är en undre gräns. Ianspråktagandet sker efter
beslutet, så det gamla villkoret redovisas som avslutat tidigare än det
faktiskt var. Felet går alltid åt det hållet, och det ska stå i metoden.

Laga kraft. `valid_from` borde vara laga kraft-datum, men det beror på
överklagandefristen och eventuell dom. Konvention: beslutsdatum som proxy,
källflaggat. De 14 domarna i korpusen justerar de fall de täcker.

Mål utanför korpusen. Motala 2021:s företrädare är från 2012 och publiceras
inte; länken får `to_decision_id=None` och det ersatta villkorets rad finns
aldrig i datasetet. Kedjan är då sann men vänsterstympad, och det redovisas
i metoden i stället för att döljas.

Frågan projektet ska kunna svara på, vilka krav gällde den dag kontrollen
gjordes, besvaras med `valid_from <= kontrolldatum < valid_to` filtrerat på
`valid_from_source` och `valid_to_source`, så att svaret alltid bär sin
egen precision.

### 2.6 Anläggningsidentiteten

Fyndet i underlaget: alla fyra beslutshuvuden bär ett anläggningsnummer vars
fyra första siffror är kommunkoden. Lidfarm "Dossienummer 1470-1195"
(Vara är 1470), Motala 2021 "0583-90-013" (Motala är 0583), Stora Markie
"1287-90-508" (Trelleborg är 1287), SweHatch "Anläggningsnr. 1290-91-006"
(Kristianstad är 1290). Det är länsstyrelsernas platsnummer för miljöfarlig
verksamhet och det följer platsen, inte bolaget.

Matchningsregel, i prioritetsordning enligt `MatchMethod`:

1. FACILITY_NUMBER: exakt match på anläggningsnummer, normaliserat till
   sifferföljd.
2. PROPERTY_MUNICIPALITY: fastighetsbeteckning plus kommun, normaliserad
   ("Boberg 4:1" + Motala).
3. ORGNR_MUNICIPALITY: organisationsnummer plus kommun.
4. MANUAL: manuell koppling via filnamnets bolagsnamn och datum.

Metod och konfidens lagras på anläggningsraden så att svaga matchningar går
att granska samlat.

Felmodus per regel. Anläggningsnumret driftar i format: tvådelat 1470-1195
mot tredelat 1287-90-508, och en dom från MMD bär det sannolikt inte alls;
därför listan `facility_numbers`, inte skalär. Fastigheten är stabilast men
inte entydig: Lidfarm spänner två fastigheter, "på fastigheterna Smedtofta
2:85 och Smedtofta 4:8" (s. 1), så matchning kräver snitt, inte likhet, och
en avstyckning byter beteckning. Organisationsnumret är svagast: det är
avsiktligt att det ska överleva namnbyte, men det överlever inte ägarbyte,
och enskilda firmor, där filnamnet bär personnamn, har
personnummer som inte får lagras. Surrogatnyckeln `facility_id` byggs
därför på kommun plus fastighet, det enda som pekar på marken.

### 2.7 Vad som inte ska in i schemat

Utelämnas helt:

- **Fysiska personers namn och kontaktuppgifter.** Besluten innehåller
  privata mejladresser i själva beslutshuvudet; två av fyra granskade
  beslut har en (Lidfarm s. 1, Motala 2021 s. 1). Adresserna återges inte
  här och extraheras inte. För enskilda firmor sätts `is_natural_person=True` och
  `operator_name` lämnas tomt; anläggningen identifieras via fastigheten.
- **Beslutsfattares och handläggares namn.** De står i varje beslut men
  projektet mäter delegationer, och fysiska personers namn hålls utanför det
  publicerade datasetet. `mpd` räcker som analysenhet.
- **Ombud.** Namn och adress i beslutshuvudet (Stora Markie s. 1,
  SweHatch s. 1) saknar analysvärde och pekar ut personer.
- **Sändlistor och kopiemottagare.** Fulla av personliga mejladresser
  (Lidfarm s. 5).
- **MKB-referat, yttranden, bemötanden, överklagandehänvisningar,
  bilagor.** Stora Markie är 29 sidor varav villkorsdelen är fyra;
  situationsplanerna i bilaga 1 extraherar dessutom som teckensallad.
  Beslutsmeningen, villkoren, Delegationer, igångsättningstid och
  ersättningsförordnandet är det som bär mätningen.

Behålls trots att det liknar personuppgift: juridiska personers namn och
organisationsnummer, eftersom de är verksamhetsutövare i offentliga
tillstånd och krävs för ägarbyteskedjan.

Villkorstexten själv kan referera ansökan ("i huvudsaklig överensstämmelse
med vad sökanden har angivit i ansökningshandlingarna"); den lagras
ordagrant eftersom den är själva mätobjektet, och den innehåller i
underlaget inga personuppgifter.

### 2.8 Extraktionens osäkerhet

Varje rad bär ett `Extraction`-block: metod, OCR-motor, källfil,
filstorlek, sidspann, teckenkvalitet, granskningsflagga, tidsstämpel och
pipelineversion. Varje härlett fält (villkorstyp, krav, länk) bär dessutom
egen metod och konfidens, eftersom en perfekt extraherad text kan vara fel
klassad och tvärtom.

Filstorleken lagras för att den är korpusens billigaste kvalitetssignal:
digitala original ligger 150 till 650 kB, skannade 5 till 9,5 MB, verifierat
2026-08-01. En analys som vill vara konservativ filtrerar då på
`extraction.method == PDFTOTEXT` eller `char_quality >= 0.98`; en analys
som vill ha hela populationen tar allt och redovisar fördelningen per
metod. Poängen med att osäkerheten står i raden är att det valet görs vid
analys, utan omextraktion.

---

## 3. Beslutslogg

| Vägval | Beslut | Avgörande skäl | Förkastat alternativ och varför |
| --- | --- | --- | --- |
| Grain | Numrerat villkor, krav nästlade | Radantalet verifierbart mot dokumentets egen räkning ("föreslår 13 villkor") | Rad per enskilt krav: segmentering blir tolkning, mäter mallens ordrikedom |
| Rubrik | `heading` ordagrann, nullable; typ separat per villkor | SweHatch 2026 saknar rubriker; Motala 2021:s "Övrigt" döljer ett avvecklingsvillkor | Typ härledd ur rubrik: klassar fel och kraschar på rubriklösa beslut |
| Typologi | Nio värden, additiv StrEnum | Grundad i observerade rubriker; OTHER plus flagga fångar det nya | Fri text: ojämförbar; finkornig taxonomi: ogrundat i underlag om fyra |
| Kvantkrav | subject, operator, value, unit, qualifier, quote | 40 dB(A) natt är lika överallt men dagfönstret skiljer; utan kvalificerare försvinner skillnaden | Värde i villkorstexten enbart: buller och frister blir ojämförbara |
| Delegationer | Egen tabell `DelegatedMatter` med `subject_type` | Annat grain, eget mått; ska joinas mot villkor per ämne | Rader i villkorstabellen: förorenar alla villkorsräkningar |
| SCD | Intervall på villkorsraden, länkar i `DecisionLink` | Länkarna är osäkra och delvis manuella; raden ska vara fryst | Intervall enbart på beslutsnivå: kan inte svara på kravbilden per dag |
| valid_from | Beslutsdatum som flaggad proxy | Laga kraft-datum står inte i besluten | Vänta på laga kraft-data: blockerar hela datasetet |
| Anläggningsnyckel | Surrogat på kommun plus fastighet; anläggningsnr som främsta matchregel | Numret finns i alla fyra huvuden och följer platsen; fastigheten pekar på marken | Orgnr som nyckel: dör vid ägarbyte och blir personnummer för enskilda firmor. Valet mellan anläggningsnr och fastighet som surrogatbas var jämnt; fastighet valdes för att den överlever registeromläggning |
| Nummer som str | `number: str` plus `position: int` | Billig försäkring mot suffixnummer i ändringsbeslut; sortering säkras av position | `int`: sparar inget och kan tvinga omextraktion |
| Personuppgifter | Fysiska personer utanför schemat | Privata mejladresser står i beslutshuvudena; dataminimering enligt GDPR | Lagra allt, maska vid publicering: risken flyttar bara nedströms |
| Proveniens | `Extraction`-block per rad plus metod och konfidens per härlett fält | Halva korpusen kräver OCR; filtrering ska ske vid analys | Kvalitet per fil enbart: döljer att klassning och extraktion felar oberoende |
| Kodspråk | Engelska genomgående; `dnr`, `mpd`, `orgnr` som lånord med förklarande docstring | Datamodellen ska kunna granskas och återanvändas av läsare utan svenska; källtext och prosa förblir svensk | Svenska fältnamn: stänger ute icke-svensktalande granskare; blandspråk utan regel: godtyckligt |

---

## 4. Det som inte går att lösa automatiskt

**Ianspråktagandedatum.** Ersättningsförordnandena är villkorade av när
tillståndet tas i anspråk, och det datumet finns hos tillsynsmyndigheten,
inte i korpusen. Berör varje anläggning med mer än ett tillstånd: i
underlaget två av tre tillstånd (Motala 2021, SweHatch). Skalat betyder det
uppskattningsvis 60 till 100 av 160 tillstånd. Hantering: proxykonvention
plus flagga nu; en riktad begäran till tillsynsmyndigheterna om
ianspråktagandeanmälningar kan skärpa datumen senare och passar projektets
öppenhetslager.

**Länkupplösningen i ändringskedjan.** Cirka 38 ändringstillstånd,
15 förlängningar och 14 domar, alltså cirka 67 beslut, ska var och en knytas
till sitt målbeslut. Dnr-citaten automatiserar kandidaterna, men varje länk
behöver okulär bekräftelse eftersom ett beslut kan citera flera dnr
(Lidfarm citerar både tillståndet och en MMÖD-dom, M 9024-15, i löptext).
Manuell insats: cirka 67 granskningar à någon minut, en dags arbete.

**Mål före 2013.** Företrädare utanför korpusen ger länkar utan målrad;
Motala 2021:s 2012-beslut är beviset. Andelen går inte att veta förrän
extraktionen körts; varje tillstånd daterat 2013 till 2016 som ersätter
något är en trolig kandidat. Hantering: `to_decision_id=None`, redovisas
som vänsterstympning i metodsidan.

**Domarnas verkan.** 14 domar kan ändra enskilda villkor, upphäva helt
eller återförvisa; vilka villkor som träffas kräver läsning av domslutet.
Hantering: manuell kodning av 14 dokument, med `status=REVOKED` och
`valid_to_source=MANUAL` på träffade rader.

**Enskilda firmor.** Filnamn med personnamn kräver manuell bedömning av hur
anläggningen ska betecknas utan att namnet lagras. Ur filnamnslistan syns
minst tre; räkna med ett tiotal av 237.

---

## 5. Tre verifieringskontroller

Mönstret är detsamma som i Maktspråk: tre oberoende vägar till samma tal,
och larm när vägarna skiljer sig.

**1. Nummerserien mot dokumentets egna avtryck.** Extraherade
villkorsnummer per beslut ska vara en sammanhängande serie 1 till N utan
hål och dubbletter. N ska dessutom matcha två oberoende avtryck i samma
dokument där de finns: antalet rubriker "Villkor X – ..." i Motivering av
villkor, och innehållsförteckningens villkorsrader. Stora Markie och
SweHatch har båda avtrycken för 1 till 13. Ett hål i serien är det typiska
symptomet på att OCR tappat en sida eller att en radbrytning slukat ett
nummer, och det syns inte i någon aggregerad statistik.

**2. Prosatal och korpustal mot extraherade tal.** Besluten räknar sig
själva i löptext: "Länsstyrelsen tillstyrker ansökan och föreslår 13 villkor
samt att tillsynsmyndigheten ges möjlighet föreskriva ytterligare villkor i
sex punkter" (Stora Markie s. 18). Sådana fraser regexfångas och diffas mot
`condition_count` och antal delegationspunkter. På korpusnivå: 237 filer ska
ge 237 beslutsrader; typfördelningen ska stämma mot länktexternas cirka
160/38/15/14; och noll villkor är bara tillåtet för förlängningar,
igångsättningsbeslut, upphävanden och domar. Ett tillstånd med noll villkor
är per definition en tyst trasig extraktion; Lidfarm visar att noll är
korrekt för en förlängning.

**3. Stratifierad återläsning plus fördelningskanarier.** Ett slumpurval
stratifierat på delegation, år och extraktionsmetod diffas rad för rad mot
rå pdftotext- respektive OCR-utdata; målet är noll avvikelser i
villkorstext. Ovanpå det två kanarier som fångar tyst drift mellan
körningar. Den första: villkor per beslut för OCR-halvan jämförs mot den
digitala halvan inom samma delegation och period, där en glipa betyder att
OCR tappar villkor systematiskt. Den andra: extraherade bullervärden jämförs
mot den hittills observerade värdemängden. I underlaget är den {40, 45, 50}
dB(A) för ekvivalentnivåer samt 55 dB(A) för momentannivå (Motala 2021
villkor 11, tabellen s. 2; SweHatch villkor 11, "Den momentana ljudnivån
utomhus vid bostäder får inte överstiga 55 dBA nattetid", s. 3). Värden
utanför mängden larmar för granskning men fäller inte raden; fyra dokument
räcker inte för att sluta mängden. Mängden fastställs mot hela korpusen i
första fullkörningen och betraktas som sluten först därefter, varefter en
OCR-läsning av 40 som 49 larmar omedelbart.
