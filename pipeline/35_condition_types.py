"""Place every heading in the corpus against the schema's condition typology.

Step 35 of the pipeline, and the first slice of VILLKORSSCHEMA section 2.2.
The schema fixes nine condition types from four decisions. The register now
holds 148 distinct headings out of 180 decisions, so the first question is
whether nine is enough, and it is asked before any classifier is written.

**Every heading is placed by hand.** The map below is data, not a rule: each
heading is written out and given a type, so that a reader can disagree with one
placement without having to reverse-engineer a pattern. A word-matching rule
would have been shorter and would have hidden exactly the judgements that need
to be visible, such as whether a buffer strip along a ditch is a manure
condition or a water condition.

**The vocabulary is short, and the map says where.** Nine types cover the four
decisions the schema was designed from. The corpus adds recurring subjects that
none of the nine names: animal housing, combustion and energy, transport,
fallen stock, nature protection and contaminated soil. They are proposed here
as additions rather than folded into OTHER, because OTHER is where a subject
goes to stop being counted. VILLKORSSCHEMA says the vocabulary is additive and
that an existing type never changes meaning, so an addition costs no
re-extraction.

**Delegation is not a condition type.** Section 2.4 of the schema gives the
delegated matters a table of their own, since a delegation is the authority
keeping a question open rather than a requirement on the operator. The heading
is placed as DELEGATION here so that those rows can be routed, and they are
reported apart from the types.

**OCR read three headings wrong and they are placed anyway.** `Ålbhnänt`,
`Allnänt` and `Alhnänt` are all the word Allmänt, and `Sk yddszoner` is as
plain. The register stores what the text layer says, because rewriting the
source silently is a worse fault than a misspelling; the correction belongs
here, in the map, where it is declared.

Two placements left the map on 10 October 2026, `Allmant` and `Lagring av
godsel`. Both came from `13df613f9802`, whose text layer was a recognition
pasted over a scan, and ADR-0026 sends that decision to the project's own OCR
instead. The headings are spelled correctly in the register from then on, and a
placement with no heading left in the register is drift this step stops on.

Nothing here writes to data/. The step reports, and the map is the artefact.

Usage:
    python pipeline/35_condition_types.py
"""

from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REGISTER = ROOT / "data" / "villkor.jsonl"

# The nine types VILLKORSSCHEMA section 2.2 fixes, in the schema's own order.
SCHEMA_TYPES = (
    "general",
    "manure",
    "water",
    "air",
    "chemicals_waste",
    "noise",
    "monitoring",
    "decommissioning",
    "other",
)
# What the corpus adds. Each is a subject that recurs and that none of the nine
# names, so putting it in OTHER would be a decision to stop counting it.
PROPOSED_TYPES = ("housing", "energy", "transport", "carcasses", "nature", "soil")
# Not a condition type at all; see the docstring.
ROUTED = ("delegation",)

# Every heading in the register, placed by hand. The comment on a line is the
# reason where the placement is a judgement rather than a reading.
HEADING_TYPE: dict[str, str] = {
    # --- the general condition -------------------------------------------
    "Allmänt": "general",
    "Allmänt villkor": "general",
    "Allmänna villkoret": "general",
    "Ålbhnänt": "general",  # OCR of Allmänt
    "Allnänt": "general",  # OCR of Allmänt
    "Alhnänt": "general",  # OCR of Allmänt
    # --- manure: storage, handling, spreading, disposal, nutrient balance --
    "Lagring och spridning av gödsel": "manure",
    "Gödselspridning": "manure",
    "Spridning av organiska gödselmedel": "manure",
    "Lagring och hantering av gödsel": "manure",
    "Spridning av gödsel": "manure",
    "Gödselhantering": "manure",
    "Lagring av stallgödsel och tvättvatten": "manure",
    "Spridning av stallgödsel": "manure",
    "Hantering av stallgödsel": "manure",
    "Lagring av gödsel och spolvatten": "manure",
    "Hantering och lagring av gödsel och tvättvatten": "manure",
    "Lagring av gödsel": "manure",
    "Spridning av stallgödsel och tvättvatten": "manure",
    "Gödsellagring": "manure",
    "Lagring av organiska gödselmedel samt avlopp från foderkök": "manure",
    "Lagring och hantering av fjäderfägödsel och fodermedel": "manure",
    "Lagringsutrymmen och avlopp från foderkök": "manure",
    "Markkartering och andra beräkningar": "manure",
    "Hantering, lagring och spridning av gödsel med mera": "manure",
    "Lagring av organiska gödselmedel och förorenat vatten": "manure",
    "Spridning/leverans av stallgödsel": "manure",
    "Hantering av gödselmedel och foder samt markkartering": "manure",
    "Hantering och lagring av gödsel": "manure",
    "Hantering, lagring och spridning av gödsel": "manure",
    "Lagring och hantering av gödsel och fodermedel": "manure",
    "Lagring och hantering av gödsel och spolvatten": "manure",
    "Gödselhantering och lagring": "manure",
    "Lagring och hantering av stallgödsel och slam": "manure",
    "Avyttring av organiska gödselmedel": "manure",
    "Spridning av organiska gödselmedel och förorenat vatten": "manure",
    "Spridning av stallgödsel/rötrest": "manure",
    "Stallbalans": "manure",  # the nutrient balance of the house, not the house
    "Växtnäring": "manure",
    "Lagring och hantering av stallgödsel": "manure",
    "Lagring och annan hantering av organiska gödselmedel": "manure",
    "Spridning av gödselmedel": "manure",
    "Lagring och spridning av organiska gödselmedel": "manure",
    "Markkartering och växtnäringsbalans": "manure",
    "Avyttring av stallgödsel": "manure",
    "stallgödsel": "manure",  # heading split across two lines
    "Växtnäringsbalans": "manure",
    "Lagring av organiska gödselmedel": "manure",
    "Provtagning och beräkningar": "manure",  # sampling of the manure produced
    # --- water: stormwater, wash and rinse water, buffer strips ------------
    # The buffer strip is placed here rather than under manure: it is a
    # condition on the ground next to the water, and it is imposed to protect
    # the water. Reading it as a manure condition is defensible, and this is
    # the placement a reader is most likely to want to argue with.
    "Skyddszoner": "water",
    "Sk yddszoner": "water",  # OCR of Skyddszoner
    "Skyddszoner vid spridning av växtskydds- och gödselmedel": "water",
    "Skyddszoner och våtmark": "water",
    "Skyddszoner för växtskyddsmedel, gödselspridning": "water",
    "Skyddszoner för växtskyddsmedel och gödselspridning": "water",
    "Tvätt- och spolvatten": "water",
    "Utsläpp till vatten": "water",
    "Skydd för yt- och grundvatten": "water",
    "Skydd för yt- och grundvatten och skyddade områden": "water",
    "Skydds för yt- och grundvatten": "water",  # OCR of Skydd
    "Omhändertagande av dagvatten": "water",
    "Spridning av tvättvatten": "water",
    "Vattenanvändning och vattenhantering": "water",
    "Spol- och tvättvatten": "water",
    "Spolvatten": "water",
    "Avlopp från foderkök mm": "water",
    "Avlopp från foderkök och lagringsutrymmen": "water",
    "Skyddsåtgärder för att minska utsläpp till vatten": "water",
    "Skydd för dricksvatten": "water",
    "Vattenhantering": "water",
    "Utsläpp till mark och vatten": "water",
    "Spol- och tvättvatten från unghönsstallar": "water",
    "Spol- och tvättvatten från stallar": "water",
    "Dagvatten": "water",
    # --- air: ammonia, odour, dust, flue gases -----------------------------
    "Utsläpp till luft": "air",
    "Rökgaser och aska": "air",
    "Ammoniak och lukt": "air",
    "Rökgasrening och aska": "air",
    "Rökgaser": "air",
    "Utsläpp av ammoniak": "air",
    "Utsläpp av ammoniak till luft": "air",
    # Section 2.2 settles ash explicitly: Motala 2021 puts it under chemicals
    # and waste, so ash alone goes there. Where the heading names flue gas
    # treatment and ash together the flue gas is the subject, so those stay
    # in air.
    "Aska": "chemicals_waste",
    # --- chemicals and waste ------------------------------------------------
    "Kemikalie- och avfallsfrågor": "chemicals_waste",
    "Kemikalier och avfall": "chemicals_waste",
    "Kemikalier och farligt avfall": "chemicals_waste",
    "Kemiska produkter och avfall": "chemicals_waste",
    "Kemiska produkter": "chemicals_waste",
    "Kemiska produkter och farligt avfall": "chemicals_waste",
    "Avfall och kemikalier": "chemicals_waste",
    "Avfall, kemikalier och lagring av olja": "chemicals_waste",
    "Kemiska produkter, hantering, förvaring": "chemicals_waste",
    "Avfallshantering": "chemicals_waste",
    "Avfall": "chemicals_waste",
    "Förvaring av kemikalier": "chemicals_waste",
    "Kemikaliehantering": "chemicals_waste",
    "Villkor om avfall och kemikaliehantering": "chemicals_waste",
    "och farligt avfall": "chemicals_waste",  # heading split across two lines
    # --- noise ---------------------------------------------------------------
    "Buller": "noise",
    "Ljud": "noise",
    "Villkor om buller": "noise",
    # --- monitoring ----------------------------------------------------------
    "Kontroll av verksamheten": "monitoring",
    "Kontroll": "monitoring",
    "Kontrollprogram": "monitoring",
    "Egenkontroll": "monitoring",
    "Driftstörningar": "monitoring",  # reporting duty on upsets
    # --- decommissioning ------------------------------------------------------
    "Nedläggning av verksamheten": "decommissioning",
    "Återställning": "decommissioning",
    "Avveckling": "decommissioning",
    "Avveckling av verksamheten": "decommissioning",
    "Nedläggning": "decommissioning",
    "Villkor om efterbehandling": "decommissioning",
    # --- animal housing, proposed --------------------------------------------
    "Djurstall": "housing",
    "Stallar": "housing",
    "Stallarna": "housing",
    "Djurstallar": "housing",
    "Stall": "housing",
    "Utfodring och stallar": "housing",
    "Foder och djurstall": "housing",
    # --- combustion and energy, proposed --------------------------------------
    # The biogas plant is placed here: it is an energy facility on the holding,
    # and its conditions read like the boiler's rather than like the manure
    # store's, though the substrate is manure.
    "Fastbränslepanna": "energy",
    "Biogasanläggning": "energy",
    "Biogasanläggningen": "energy",
    "Energihushållning": "energy",
    "Energianvändning": "energy",
    "Fastbränsleanläggning": "energy",
    "Energi": "energy",
    "Energianläggning": "energy",
    "Biobränslepannor": "energy",
    "Utsläpp från energianläggning": "energy",
    "Energieffektivisering": "energy",
    "Fastbränslepannor": "energy",
    "Energihushållningsplan": "energy",
    # --- transport, proposed ---------------------------------------------------
    "Transporter": "transport",
    "Transport": "transport",
    "och transporter": "transport",  # heading split across two lines
    # --- fallen stock, proposed -------------------------------------------------
    "Döda djur": "carcasses",
    # --- nature protection, proposed ---------------------------------------------
    # The en dash is the decision's own; the heading is stored verbatim.
    "Biotopskyddsdispens– Villkor och kompensationsåtgärder": "nature",  # noqa: RUF001
    "Biotopskydd": "nature",
    "Skydd för grod- och kräldjur": "nature",
    "Landskapet": "nature",
    "Åtgärd i vattendrag": "nature",
    # --- contaminated soil and earthworks, proposed --------------------------------
    "Markarbeten i förorenad mark": "soil",
    "Masshantering, husbehovstäkt": "soil",
    # --- routed elsewhere ------------------------------------------------------------
    "Delegation": "delegation",
    "(Delegation)": "delegation",
    # --- the document's own word for a residual, and one unreadable fragment ---------
    "Övrigt": "other",
    "uppkommer": "other",  # a fragment of a heading split across two lines
}


def load() -> list[dict]:
    """Every condition in the register."""
    return [
        json.loads(line) for line in REGISTER.read_text("utf-8").splitlines() if line
    ]


def main() -> int:
    """Report how far the schema's nine types reach, and what the corpus adds."""
    if not REGISTER.exists():
        print("run pipeline/33_condition_register.py first")
        return 1
    records = load()
    headings = Counter(r["rubrik"] for r in records if r["rubrik"])

    missing = sorted(set(headings) - set(HEADING_TYPE))
    if missing:
        print(f"{len(missing)} rubriker saknar placering i kartan:")
        for heading in missing:
            print(f"  {headings[heading]:>4}  {heading}")
        print("placera dem för hand innan någon siffra publiceras")
        return 1
    unused = sorted(set(HEADING_TYPE) - set(headings))
    if unused:
        print(f"{len(unused)} placeringar utan motsvarande rubrik i registret:")
        for heading in unused:
            print(f"  {heading}")
        print("kartan har drivit ifrån registret")
        return 1

    per_type = Counter()
    for heading, count in headings.items():
        per_type[HEADING_TYPE[heading]] += count
    with_heading = sum(headings.values())
    without = len(records) - with_heading

    print(f"{len(records)} villkor, {with_heading} med rubrik, {without} utan")
    print(f"{len(headings)} olika rubriker, alla placerade för hand\n")

    print("schemats nio typer")
    for name in SCHEMA_TYPES:
        share = per_type[name] / with_heading
        print(f"  {name:<18}{per_type[name]:>6}{share:>8.1%}")
    covered = sum(per_type[name] for name in SCHEMA_TYPES)
    print(f"  {'summa':<18}{covered:>6}{covered / with_heading:>8.1%}")

    print("\nämnen som korpusen lägger till och som de nio inte namnger")
    for name in PROPOSED_TYPES:
        heads = sum(1 for h in headings if HEADING_TYPE[h] == name)
        print(
            f"  {name:<18}{per_type[name]:>6}{per_type[name] / with_heading:>8.1%}"
            f"   {heads} rubriker"
        )
    added = sum(per_type[name] for name in PROPOSED_TYPES)
    print(f"  {'summa':<18}{added:>6}{added / with_heading:>8.1%}")

    print("\nroutat till egen tabell enligt schemat avsnitt 2.4")
    for name in ROUTED:
        print(f"  {name:<18}{per_type[name]:>6}")

    print(
        f"\nOm bara de nio typerna används faller {added + per_type['other']} "
        f"villkor till övrigt, "
        f"{(added + per_type['other']) / with_heading:.1%} av dem med rubrik."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
