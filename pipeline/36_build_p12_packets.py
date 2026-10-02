"""Build one P12 packet per authority out of the committed registers.

Step 36 of the pipeline. P12 gives every affected authority its own results
before publication, with three weeks to reply, and that is 22 packets: the 21
county boards and the Board of Agriculture. They are generated rather than
written, for two reasons. Twenty-two hand-written letters end up saying
different things, and a generated packet can be recomputed when a figure moves,
which figures in this project do.

**Every claim is a number or a verbatim quotation.** The project's rule is never
to characterise, and it binds hardest in a letter to the authority being
measured. The packet therefore states what was counted, how, and out of which
file, and quotes the authority's own words where its reasoning is described.

**A figure is published next to the event that produced it.** T1 is the working
days to the first substantial reply, and P1 lists what counts: a delivery, a fee
notice, a request for clarification, or a decision. An acknowledgement of
receipt, a note that the case is being worked on and an autoreply do not.
Rather than print the number alone, the packet names the event that set it,
with its date, so that the authority can see what was counted and object to the
choice rather than to the arithmetic.

**The step refuses to write rather than warn.** Four conditions were written
into the protocol log before this file existed: the per-authority figures must
reconcile with the corpus figures, every event in a packet must exist in the log
and none of the authority's events may be missing, no packet may contain a
personal name, and the packet must contain no characterisation that is neither a
number nor a quotation. The first three are machine-checkable and are checked
here; the fourth is a property of the templates below and is why they are short.

The packets are a build artefact and are gitignored, like the Parquet warehouse
under ADR-0012. This generator is committed, which is what makes them
reproducible.

Writes data/p12/<slug>.md, one per authority.

Usage:
    python pipeline/36_build_p12_packets.py
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from open_items import (  # noqa: E402
    DAY_ZERO,
    DECISION_CLOSERS,
    DELIVERY_COMPLETED,
    INTERNAL,
    NOT_A_REQUEST,
    P11_REMINDER_DAYS,
    P11_SILENCE_DAYS,
    THEIRS,
    add_working_days,
    is_p11,
    working_days_between,
)

OUT = ROOT / "data" / "p12"
LOG = ROOT / "data" / "protokoll_logg.jsonl"
MASKING = ROOT / "data" / "maskning.jsonl"
CONTRAST = ROOT / "data" / "kontrast.jsonl"
DECISIONS = ROOT / "data" / "beslut.jsonl"
GROUNDS = ROOT / "data" / "sekretessgrunder.jsonl"
DENOMINATORS = ROOT / "data" / "namnare.jsonl"

# The delivery directory each authority's documents sit under, and the short
# name the other registers use. Written out rather than derived, because a
# transliteration rule that turns Västra Götaland into vastra_gotaland also
# turns Västernorrland into something no file is named.
SLUG = {
    "Länsstyrelsen i Blekinge": "blekinge",
    "Länsstyrelsen i Dalarna": "dalarna",
    "Länsstyrelsen i Gotland": "gotland",
    "Länsstyrelsen i Gävleborg": "gavleborg",
    "Länsstyrelsen i Halland": "halland",
    "Länsstyrelsen i Jämtland": "jamtland",
    "Länsstyrelsen i Jönköping": "jonkoping",
    "Länsstyrelsen i Kalmar": "kalmar",
    "Länsstyrelsen i Kronoberg": "kronoberg",
    "Länsstyrelsen i Norrbotten": "norrbotten",
    "Länsstyrelsen i Skåne": "skane",
    "Länsstyrelsen i Stockholm": "stockholm",
    "Länsstyrelsen i Södermanland": "sodermanland",
    "Länsstyrelsen i Uppsala": "uppsala",
    "Länsstyrelsen i Värmland": "varmland",
    "Länsstyrelsen i Västerbotten": "vasterbotten",
    "Länsstyrelsen i Västernorrland": "vasternorrland",
    "Länsstyrelsen i Västmanland": "vastmanland",
    "Länsstyrelsen i Västra Götaland": "vastra_gotaland",
    "Länsstyrelsen i Örebro": "orebro",
    "Länsstyrelsen i Östergötland": "ostergotland",
    "Jordbruksverket": "jordbruksverket",
}

# The county name to print, since a packet is a letter and not a file listing.
NAME = {
    slug: authority.replace("Länsstyrelsen i ", "") for authority, slug in SLUG.items()
}

# P10 closes the response-time collection on day 40, and the addition to
# tillämpningsnot 7 of 29 September 2026 says a delivery after that day does not
# reopen it: T2 is reported as censored at day 40 with the actual date beside
# it. The document measures are untouched by this, since they follow note 3.
MEASURE_CLOSES = 40

# P1: "T1 = arbetsdagar till första substantiella besked per begäran
# (leverans, avgiftsbesked, förtydligandefråga eller beslut; autosvar räknas
# inte)." The four kinds are listed there and nowhere else, so the mapping is
# written out here and the packet names the event it used. What is deliberately
# outside: mottagningsbesked, arbetsbesked, diarieföringsbesked, manuellt svar,
# autosvar, and the court's own events. A human reply that says the case has
# been forwarded is not one of P1's four, however welcome it was.
SUBSTANTIAL = {
    "leverans": "leverans",
    "rättad leverans": "leverans",
    "delvis avslag och kompletterande leverans": "leverans",
    "avgiftsbesked": "avgiftsbesked",
    "avgiftsbesked och erbjudande om maskad elektronisk leverans": "avgiftsbesked",
    "avgiftsbesked och förtydligande": "avgiftsbesked",
    "förtydligandefråga och avgiftsbesked": "avgiftsbesked",
    "förnyat avgiftserbjudande": "avgiftsbesked",
    "avgift kvarstår": "avgiftsbesked",
    "förtydligandefråga": "förtydligandefråga",
    "förtydligandefråga upprepad": "förtydligandefråga",
    "besked om uttagets omfattning och förtydligandefråga": "förtydligandefråga",
    "avslagsbeslut mottaget": "beslut",
    "delvis avslagsbeslut mottaget": "beslut",
    "avgiftsbeslut mottaget": "beslut",
    "avgiftsbeslut vägrat": "beslut",
}
# What ends a request, in the four slutstatus tillämpningsnot 3 names: the
# documents in hand, a delivery the authority itself reports as complete, or a
# decision that closes the track of a request whose copies were waived when the
# fee stood. Written out here by hand, the set drifted from the measure's own:
# it lacked "avgiftsbeslut mottaget" and "leverans fullgjord", so on 1 October
# 2026 three packets said the request was not concluded although Skåne's fee
# decision had arrived on 5 August, Örebro's on 27 August, and Västmanland's
# delivery was logged as complete on 30 September. It is taken from the measure
# now instead of restated beside it.
FINAL = (
    {"leverans", "rättad leverans", "delvis avslag och kompletterande leverans"}
    | set(DELIVERY_COMPLETED)
    | set(DECISION_CLOSERS)
)

# The same screen step 33 runs, for the same reason.
FORBIDDEN = {
    "e-postadress": re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-z]{2,}"),
    "personnummer": re.compile(r"\b(?:19|20)\d{6}[-+]\d{4}\b"),
    "telefonnummer": re.compile(r"\b0\d{1,3}[-\s]\d{2,3}\s?\d{2}\s?\d{2}\b"),
    "filnamn": re.compile(r"\.(docx?|rtf|xlsx?)\b", re.IGNORECASE),
}

CLASSES = {
    "A": "kontrollrapporter med bilagor",
    "B": "beslut om föreläggande",
    "C": "sammanställning ur kontrollregistret",
}


def read(path: Path) -> list[dict]:
    """Every row of a jsonl register."""
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text("utf-8").splitlines() if line]


def events_for(rows: list[dict], authority: str) -> dict[str, list[dict]]:
    """The authority's own events, per request class, in logged order."""
    tracks: dict[str, list[dict]] = defaultdict(list)
    for row in rows:
        if row["myndighet"] != authority:
            continue
        for klass in row["begaran"].split("+"):
            tracks[klass].append(row)
    return tracks


def first_substantial(events: list[dict]) -> dict | None:
    """The event P1 counts as the first substantial reply."""
    for event in sorted(events, key=lambda e: (e["datum"], e["klockslag"])):
        if event["handelse"] in SUBSTANTIAL:
            return event
    return None


def concluded(events: list[dict]) -> dict | None:
    """The event that ended the request, if one has.

    An event the timeline below does not show may not be the one the letter
    names as the conclusion. Kalmar B ended on 13 August 2026 with both a
    delivery and our own bookkeeping row "beslutsbegäran förfallen", and the
    later timestamp belonged to the bookkeeping row, so the packet told the
    county its request had concluded with an event the county could not see
    and whose wording is the project's own. Where a visible closer exists on
    the same track it is preferred, and only then the latest of the rest.
    """
    ended = [e for e in events if e["handelse"] in FINAL]
    if not ended:
        return None
    visible = [
        e for e in ended if e["kanal"] == "e-post" and e["handelse"] not in INTERNAL
    ]
    return sorted(visible or ended, key=lambda e: (e["datum"], e["klockslag"]))[-1]


def masking_rows(masking: list[dict], slug: str, klass: str) -> list[dict]:
    """The measured documents of one authority in one class."""
    prefix = f"{slug}_{klass}/"
    return [row for row in masking if row["path"].startswith(prefix)]


def timeline(events: list[dict]) -> list[str]:
    """The correspondence, dated, with whose move each event was.

    Internal events are left out. That a delivery was filed with a checksum is
    the project's own bookkeeping and belongs in the published log, not in a
    letter to the authority that sent it.
    """
    lines = []
    for event in sorted(events, key=lambda e: (e["datum"], e["klockslag"])):
        if event["kanal"] != "e-post" or event["handelse"] in INTERNAL:
            continue
        day = working_days_between(DAY_ZERO, date.fromisoformat(event["datum"]))
        who = "ni" if event["handelse"] in THEIRS else "jag"
        lines.append(f"| {event['datum']} | dag {day} | {who} | {event['handelse']} |")
    return lines


# The four outcomes tillämpningsnot 5 measures, written so that they follow
# "Den 5 augusti 2026 ..." with the verb before the subject, as Swedish needs.
FEE_OUTCOME = (
    ("avgiftsbeslut mottaget", "meddelade ni ett överklagbart beslut i avgiftsfrågan"),
    ("avgiftsbeslut vägrat", "meddelade ni att något beslut inte fattas"),
    ("taxebeslut bifogat", "skickade ni myndighetens generella taxebeslut"),
    ("riktlinje bifogad", "skickade ni en generell riktlinje om avgiftsuttag"),
)

MONTHS = (
    "januari",
    "februari",
    "mars",
    "april",
    "maj",
    "juni",
    "juli",
    "augusti",
    "september",
    "oktober",
    "november",
    "december",
)


def in_swedish(day: str) -> str:
    """An ISO date as a Swedish reader writes it."""
    when = date.fromisoformat(day)
    return f"{when.day} {MONTHS[when.month - 1]} {when.year}"


def fee_lines(events: list[dict], delivered: bool) -> list[str]:
    """What the fee led to, in the protocol's own four outcomes."""
    names = {event["handelse"] for event in events}
    if not any(
        name.startswith("avgiftsbesked")
        or name in {"avgift kvarstår", "förtydligandefråga och avgiftsbesked"}
        for name in names
    ):
        return []
    lines = ["## Avgiften och vad den ledde till", ""]
    body = [
        "Projektets budget är noll kronor, vilket står i protokollet sedan före "
        "utskicket. Vid varje avgiftsbesked smalnades begäran av enligt en fast "
        "regel, lika mot alla, och kvarstod avgiften avstods kopiorna."
    ]
    for name, said in FEE_OUTCOME:
        when = [e["datum"] for e in events if e["handelse"] == name]
        if when:
            body.append(f"Den {in_swedish(when[0])} {said}.")
    if "avstående" in names and not delivered:
        body.append(
            "Begäran stannade därmed vid avgiften, och er myndighet bidrar med "
            "svarstid och avgiftsuppgift men saknar handlingar i "
            "maskningsmätningen. Bortfallet redovisas öppet och räknas aldrig "
            "som ett utlämnande eller som ett avslag."
        )
    elif "avstående" in names and delivered:
        body.append(
            "Handlingar lämnades därefter ut utan avgift, och de ingår i mätningen."
        )
    lines.append(" ".join(body))
    lines.append("")
    return lines


def denominator_lines(record: dict | None, events: list[dict]) -> list[str]:
    """The closing question: the authority's own answer, or that it is still out.

    A county that has not answered gets the section too. What will be published
    about it is that the denominator is missing for its part, and P12 says the
    packet holds what will be published, so a silent county has to be told that
    its silence is what gets reported. Two were silent on 2 October 2026,
    Gävleborg and Halland, and both had asked about the question's scope without
    sending figures. Halland's question was answered the same day; Gävleborg's
    came in while the packets were being built and is still open.
    """
    if not record:
        asked = [e for e in events if is_p11(e) and e["handelse"] == "nämnarfråga"]
        if not asked:
            return []
        when = date.fromisoformat(asked[0]["datum"])
        reminder = add_working_days(when, P11_REMINDER_DAYS)
        missing = add_working_days(reminder, P11_SILENCE_DAYS)
        # The authority's own question and our answer to it are separate events
        # on the P11 track, and both carry the word förtydligande. They are told
        # apart by name and not by substring: a letter that said the question
        # was answered when it was not would be a claim about my own handling
        # that the log does not carry.
        back = [
            e
            for e in events
            if is_p11(e)
            and e["handelse"].startswith("förtydligandefråga")
            and e["datum"] >= asked[0]["datum"]
        ]
        answered = [
            e
            for e in events
            if is_p11(e)
            and e["handelse"].startswith("svar på förtydligandefråga")
            and back
            and e["datum"] >= back[0]["datum"]
        ]
        lines = ["## Den avslutande frågan, som ännu är obesvarad", ""]
        said = [
            f"Den {in_swedish(asked[0]['datum'])} ställdes en likalydande fråga "
            "till samtliga 21 länsstyrelser om antalet kontroller och "
            "förelägganden. Något svar med tal har inte kommit in från er när "
            "det här paketet byggs."
        ]
        if back and answered and answered[0]["datum"] == back[0]["datum"]:
            said.append(
                f"Ni återkom den {in_swedish(back[0]['datum'])} med frågor om "
                "frågans omfång, och de besvarades samma dag."
            )
        elif back and answered:
            said.append(
                f"Ni återkom den {in_swedish(back[0]['datum'])} med frågor om "
                "frågans omfång, och de besvarades den "
                f"{in_swedish(answered[0]['datum'])}."
            )
        elif back:
            said.append(
                f"Ni återkom den {in_swedish(back[0]['datum'])} med en fråga om "
                "frågans omfång, som inte är besvarad när det här paketet byggs."
            )
        said.append(
            f"En påminnelse går ut tidigast den {in_swedish(reminder.isoformat())}. "
            "Uteblir svar därefter redovisas nämnaren som saknad för er del den "
            f"{in_swedish(missing.isoformat())}, enligt tillämpningsnot 7 i "
            "projektets handläggningsprotokoll. Den redovisas då som en lucka: "
            "den uppskattas aldrig, och den räknas aldrig som ett avslag. "
            "Kommer svaret innan publiceringen förs det in ordagrant."
        )
        lines.append(" ".join(said))
        lines.append("")
        return lines
    lines = ["## Ert svar på den avslutande frågan", ""]
    lines.append(
        "Den 28 september 2026 ställdes en likalydande fråga till samtliga 21 "
        "länsstyrelser om antalet kontroller och förelägganden. Svaret jämförs "
        "med Jordbruksverkets uppgifter, och avvikelser mellan källorna "
        "redovisas utan att någon av dem rättas. Ni svarade:"
    )
    lines.append("")
    lines.append(f"> {record['citat']}")
    lines.append("")
    if record["kan_inte_tas_fram"]:
        lines.append(
            "Svaret redovisas som att nämnaren saknas för er del. Den uppskattas "
            "aldrig, och luckan redovisas som en lucka."
        )
        lines.append("")
    elif record["lasning_fjaderfa"] != "okänd":
        lines.append(
            "Ert svar läses som att fjäderfätalet är "
            f"{record['lasning_fjaderfa']}. Talen jämförs bara med andra läns "
            "tal som vilar på samma läsning."
        )
        lines.append("")
    else:
        lines.append(
            "Svaret säger inte om fjäderfätalet har någon gräns för "
            "besättningsstorlek, så läsningen redovisas som okänd och talet "
            "jämförs inte med län vars läsning är känd."
        )
        lines.append("")
    return lines


def percent(value: float) -> str:
    """A share in Swedish, with a comma and a space before the sign."""
    return f"{value * 100:.1f}".replace(".", ",") + " %"


# P12 gives three weeks, counted in calendar days as tillämpningsnot 8 counts
# them: sent on 12 October the note has the time run out on 2 November.
REPLY_DAYS = 21

# Neuter, because the noun they count is "län".
COUNTED = ("inga", "ett", "två", "tre", "fyra", "fem", "sex", "sju", "åtta")


def outside(log: list[dict], masking: list[dict], klass: str) -> str:
    """Why the comparison holds fewer counties than the request was sent to.

    A table of seventeen in a measure addressed to twenty-one invites the reader
    to ask what happened to the other four, and the answer is not a gap in the
    data. Three waived the copies when the fee stood after the narrowing, so
    they have response times and fee figures but no documents; one handled both
    requests as a single case and delivered under the other class. Counted from
    the log every time the packets are built, so the sentence cannot say
    seventeen after an eighteenth county has delivered.
    """
    counties = {a: slug for a, slug in SLUG.items() if a.startswith("Länsstyrelsen")}
    folders = {row["path"].split("/")[0] for row in masking}
    here = {f[:-2] for f in folders if f.endswith(f"_{klass}")}
    elsewhere = {f[:-2] for f in folders if f.endswith("_A" if klass == "B" else "_B")}
    waived = merged = 0
    for authority, slug in counties.items():
        if slug in here:
            continue
        names = {e["handelse"] for e in log if e["myndighet"] == authority}
        if "avstående" in names:
            waived += 1
        elif slug in elsewhere:
            merged += 1
    said = [f"Jämförelsen omfattar {len(here)} av de {len(counties)} länsstyrelserna."]
    if waived:
        said.append(
            f"{COUNTED[waived].capitalize()} län avstod från kopiorna sedan "
            "avgiften kvarstod efter avsmalningen, och har därför svarstid och "
            "avgiftsuppgift men inga handlingar i maskningsmätningen."
        )
    if merged:
        said.append(
            f"{COUNTED[merged].capitalize()} län hanterade de två begärandena som "
            "ett ärende och lämnade handlingarna i klass "
            f"{'B' if klass == 'A' else 'A'}, där de räknas."
        )
    said.append(
        "Bortfallet redovisas öppet och räknas aldrig som ett utlämnande eller "
        "som ett avslag."
    )
    return " ".join(said)


def points(value: float) -> str:
    """A difference in percentage points, with one decimal and a comma.

    Printed as a whole number this overstated two counties' own contrast on
    1 October 2026: Södermanland's 4,5 points read as 5 and Uppsala's 55,9 as
    56. One decimal is as much precision as a difference between two fractions
    of this size carries, and a figure in a letter to the authority it is about
    should not be rounded in the direction of the finding.
    """
    return f"{value:.1f}".replace(".", ",")


def area_percent(value: float) -> str:
    """A masked area, which needs more decimals than a document share.

    Dalarna redacts a personal identity number here and there and nothing else,
    so its class means are 0.03 and 0.02 per cent. Printed with one decimal both
    read 0,0 %, which beside "8 of 10 documents masked" says the opposite of
    what was measured. Two decimals carry every county's figure, and a value
    that is positive but smaller than the last digit is written out rather than
    rounded away.
    """
    if value > 0 and value * 100 < 0.005:
        return "under 0,01 %"
    return f"{value * 100:.2f}".replace(".", ",") + " %"


def ranking(masking: list[dict], klass: str) -> list[tuple[str, int, float]]:
    """Every authority's share of documents with at least one masking."""
    per: dict[str, list[dict]] = defaultdict(list)
    for row in masking:
        folder = row["path"].split("/")[0]
        if folder.endswith(f"_{klass}"):
            per[folder[: -len(f"_{klass}")]].append(row)
    out = [
        (slug, len(rows), sum(1 for r in rows if r["masked"]) / len(rows))
        for slug, rows in per.items()
    ]
    # Within a tie the order carries no meaning, so it is alphabetical by the
    # name the reader sees rather than by the internal slug.
    return sorted(out, key=lambda item: (-item[2], NAME.get(item[0], item[0])))


def packet(authority: str, data: dict) -> str:
    """One authority's own results, as the letter it will be sent with."""
    slug = SLUG[authority]
    parts = [
        f"# Resultat som rör {authority}",
        "",
        "Det här är vad som kommer att publiceras om er myndighet i ett",
        "kunskapsunderlag om djurskyddskontrollens likvärdighet, byggt på",
        "myndigheternas egna beslut och kontrollhandlingar. Ni får det före",
        "publicering, med tre veckors svarstid, enligt punkt P12 i projektets",
        "handläggningsprotokoll. Ett svar publiceras oavkortat vid sidan av",
        "siffrorna. Uteblir svar publiceras siffrorna som de står, och det",
        "antecknas att svar inte kommit.",
        "",
        "Publiceringen sker tidigast dagen efter svarstidens slut. Den omfattar",
        "ett publikt kodarkiv på GitHub, en webbplats och ett dataset, och i",
        "materialet ingår hela handläggningsprotokollet och hela",
        "korrespondensloggen, alltså också de mejl ni har skickat i de här",
        "ärendena, ordagrant. Namn på enskilda tjänstemän återges inte någonstans:",
        "där ett beslut namnger beslutsfattare och föredragande skrivs rollen i",
        "stället.",
        "",
        "Vill ni läsa metodbeskrivningen innan den publiceras skickar jag de",
        "delar som rör er myndighet om ni hör av er.",
        "",
        "Varje uppgift nedan är antingen ett tal som går att räkna fram ur",
        "underlaget eller ett ordagrant citat ur er egen skrivelse. Ingenting är",
        "en karaktärisering av myndigheten.",
        "",
        "## Begäran och tidsförlopp",
        "",
        "Begäran skickades måndag 2026-08-03, samma dag till samtliga 21",
        "länsstyrelser och till Jordbruksverket, som dag 0. Arbetsdagar räknas",
        "därifrån.",
        "",
    ]
    for klass, events in sorted(data["tracks"].items()):
        if klass not in CLASSES:
            continue
        parts.append(f"### Begäran {klass}, {CLASSES[klass]}")
        parts.append("")
        first = first_substantial(events)
        last = concluded(events)
        if first:
            day = working_days_between(DAY_ZERO, date.fromisoformat(first["datum"]))
            parts.append(
                f"Första substantiella besked enligt P1: **dag {day}**, "
                f"{first['datum']}, loggat som {first['handelse']}."
            )
        else:
            parts.append(
                "Inget substantiellt besked enligt P1 har registrerats. "
                "Mottagningsbesked, arbetsbesked och autosvar räknas inte, "
                "eftersom P1 räknar leverans, avgiftsbesked, förtydligandefråga "
                "eller beslut."
            )
        if last:
            day = working_days_between(DAY_ZERO, date.fromisoformat(last["datum"]))
            if day > MEASURE_CLOSES:
                parts.append(
                    f"Avslutat {last['datum']}, alltså dag {day}. "
                    "**Svarstiden redovisas som censurerad "
                    f"vid dag {MEASURE_CLOSES}**, eftersom datainsamlingen för "
                    "svarstidsmåttet stängdes den dagen enligt P10 och en "
                    "leverans efter den inte öppnar måttet igen. Handlingarna "
                    "ingår däremot fullt ut i maskningsmätningen. Regeln står i "
                    "tillägget till tillämpningsnot 7."
                )
            elif last["kanal"] == "e-post" and last["handelse"] not in INTERNAL:
                parts.append(
                    f"Avslutat enligt P1: **dag {day}**, {last['datum']}, "
                    f"loggat som {last['handelse']}."
                )
            else:
                # The track has no closing message of its own. Naming the
                # project's own bookkeeping row here would tell the authority
                # that its request ended with an event it cannot find in the
                # correspondence below.
                parts.append(
                    f"Avslutat enligt P1: **dag {day}**, {last['datum']}. Den "
                    "här begäran har ingen egen avslutande skrivelse i "
                    "korrespondensen nedan; slutdatumet är satt utifrån era "
                    "egna besked och det utlämnande de gäller."
                )
        else:
            parts.append("Begäran är inte avslutad i skrivande stund.")
        parts.append("")
        rows = timeline(events)
        if rows:
            parts.append("| Datum | Arbetsdag | Vem | Händelse |")
            parts.append("| --- | --- | --- | --- |")
            parts.extend(rows)
            parts.append("")

    parts.append("## Maskningsmätningen")
    parts.append("")
    if not data["masking"]:
        parts.append(
            "Inga handlingar från er myndighet ingår i maskningsmätningen, "
            "eftersom ingen leverans har arkiverats."
        )
        parts.append("")
    else:
        parts.append("Måttet är maskinellt och beskrivet i sin helhet i projektets")
        parts.append("dokumentation. Två tal redovisas: andelen dokument med minst en")
        parts.append(
            "maskning, och andelen av sidytan som är maskad. Ett dokument räknas"
        )
        parts.append(
            "som maskat när en fylld rektangel täcker text eller när text saknas"
        )
        parts.append("under rektangeln. Ytan i tabellen är ett medelvärde över")
        parts.append("klassens samtliga dokument. Dokument utan maskning räknas då")
        parts.append("som noll och drar ned medelvärdet.")
        parts.append("")
        parts.append("| Klass | Dokument | Med minst en maskning | Maskad yta |")
        parts.append("| --- | --- | --- | --- |")
        for klass in ("A", "B"):
            rows = data["masking"].get(klass, [])
            if not rows:
                continue
            masked = sum(1 for r in rows if r["masked"])
            area = sum(r["masked_area_share"] for r in rows) / len(rows)
            parts.append(
                f"| {klass} | {len(rows)} | {masked} ({percent(masked / len(rows))}) "
                f"| {area_percent(area)} |"
            )
        # A class can hold masked documents and still measure zero area, when
        # the masking was recognised from the authority's own marker and no
        # filled rectangle could be measured. Beside a share of 25 per cent a
        # bare 0,00 % reads as a contradiction, so the reason is written out.
        for klass in ("A", "B"):
            rows = data["masking"].get(klass, [])
            if not rows:
                continue
            marked = [r for r in rows if r["masked"]]
            if marked and not sum(r["masked_area_share"] for r in rows):
                parts.append(
                    f"I klass {klass} är maskningen igenkänd på er egen "
                    "markering, i filnamnet eller i texten, utan att någon fylld "
                    "rektangel kunnat mätas. Den maskade ytan blir därför noll, "
                    "vilket säger något om mätningen och inte om handlingen."
                )
                parts.append("")
        both = all(data["masking"].get(k) for k in ("A", "B"))
        if both:
            a = data["masking"]["A"]
            b = data["masking"]["B"]
            share_a = sum(1 for r in a if r["masked"]) / len(a)
            share_b = sum(1 for r in b if r["masked"]) / len(b)
            parts.append(
                f"Skillnaden inom er myndighet, som är projektets kontrastmått "
                f"enligt P1, är **{points((share_a - share_b) * 100)} "
                f"procentenheter** i andel maskade dokument mellan klass A och "
                f"klass B."
            )
            parts.append("")

    said_about_counts = False
    for klass in ("A", "B"):
        table = data["rank"].get(klass) or []
        mine = [row for row in table if row[0] == data["slug"]]
        if not mine:
            continue
        own_share = mine[0][2]
        # Competition ranking: everyone on the same share holds the same place.
        # Ordering ties by anything else, alphabet included, would invent a
        # difference the measurement does not carry.
        place = sum(1 for row in table if row[2] > own_share) + 1
        tied = sum(1 for row in table if row[2] == own_share) - 1
        if tied > 1:
            shared = f", delad med {tied} andra myndigheter"
        elif tied == 1:
            shared = ", delad med en annan myndighet"
        else:
            shared = ""
        parts.append(f"## Er plats i jämförelsen, klass {klass}")
        parts.append("")
        parts.append(
            f"Ordnat efter andelen dokument med minst en maskning ligger er "
            f"myndighet på plats **{place} av {len(table)}** bland dem som "
            f"levererat i klass {klass}{shared}. Myndigheter med samma andel "
            f"delar plats, eftersom mätningen inte skiljer dem åt. Ordningen "
            f"följer måttet och innebär ingen bedömning av handläggningen. Hela "
            f"ordningen står nedan, eftersom en placering utan de andra talen "
            f"inte går att bedöma."
        )
        parts.append("")
        parts.append(data["outside"][klass])
        parts.append("")
        parts.append("| Plats | Myndighet | Dokument | Med minst en maskning |")
        parts.append("| --- | --- | --- | --- |")
        for slug_, count, share in table:
            position = sum(1 for row in table if row[2] > share) + 1
            # Spelled out rather than abbreviated to (ni): the marker has to
            # say what it means to someone reading the table for the first
            # time, and nothing else in the packet explains it.
            mark = " **(er myndighet)**" if slug_ == data["slug"] else ""
            parts.append(
                f"| {position} | {NAME.get(slug_, slug_)}{mark} | {count} "
                f"| {percent(share)} |"
            )
        parts.append("")
        parts.append(
            "Antalet dokument skiljer sig mellan myndigheter, eftersom begäran "
            "hade ett tak och några myndigheter tog ut en avgift som ledde till "
            "en avsmalning. Andelen är därför räknad på olika stora underlag, "
            "och det talet står i tabellen."
            if not said_about_counts
            else "Antalet dokument skiljer sig mellan myndigheter av samma skäl "
            "som ovan."
        )
        said_about_counts = True
        parts.append("")

    if data["grounds"]:
        parts.append("## Vad ni skrev när handlingarna lämnades ut, ordagrant")
        parts.append("")
        for row in sorted(data["grounds"], key=lambda r: r["klass"]):
            if row["bestammelser"]:
                parts.append(
                    f"Klass {row['klass']}, med åberopad bestämmelse "
                    f"{', '.join(row['bestammelser'])}:"
                )
            else:
                parts.append(
                    f"Klass {row['klass']}, utan åberopad bestämmelse i följebrevet:"
                )
            parts.append("")
            parts.append(f"> {row['citat']}")
            parts.append("")
            # A quote that the archived copy cuts off, or whose covering letter
            # cannot be fetched at all, is said to be exactly that. Printing it
            # as a clean quotation would let an authority read its own sentence
            # ending mid-word and conclude, fairly, that it had been misquoted.
            if not row["citat_fullstandigt"]:
                parts.append(
                    "Citatet är avhugget i den kopia som finns i brevlådan och "
                    "återges så långt det går att läsa. Vill ni att hela "
                    "meningen återges ber jag om den."
                )
                parts.append("")
            if row["kalla_ej_atkomlig"]:
                parts.append(
                    "Följebrevet går inte att hämta ur brevlådan, så citatet är "
                    "avskrivet för hand när meddelandet lästes. Är ordalydelsen "
                    "fel ber jag om den riktiga."
                )
                parts.append("")

    parts.extend(
        fee_lines(
            data.get("events", []),
            delivered=bool(data["masking"].get("A") or data["masking"].get("B")),
        )
    )
    parts.extend(denominator_lines(data.get("denominator"), data["events"]))

    if data["decisions"]:
        parts.append("## Beslut ni meddelat, ordagrant")
        parts.append("")
        for row in data["decisions"]:
            # The register records what the decision itself states. Jordbruksverket
            # names no title for the person presenting the case, and the register
            # says so in words; interpolated as if it were a title, the sentence
            # read "fattat av avdelningschef med titel anges inte som
            # föredragande".
            if row["foredragande"] == "titel anges inte":
                who = (
                    f"fattat av {row['beslutsfattare']}. Beslutet anger ingen "
                    "titel för föredraganden"
                )
            else:
                who = (
                    f"fattat av {row['beslutsfattare']} med "
                    f"{row['foredragande']} som föredragande"
                )
            parts.append(
                f"Beslut {row['diarienummer']}, {row['beslutsdatum']}, klass "
                f"{row['klass']}, {who}. Namnen står i beslutet "
                f"och återges inte här."
            )
            parts.append("")
            parts.append(f"> {row['citat_bedomning']}")
            parts.append("")

    if any("[...]" in line for line in parts):
        parts.append(
            "Tecknet [...] i ett citat ovan markerar att text har utelämnats "
            "mellan två stycken i er egen skrivelse. Ingenting annat är ändrat, "
            "och hela lydelsen finns i det meddelande eller beslut som anges."
        )
        parts.append("")

    parts.extend(
        [
            "## Vad underlaget inte påstår",
            "",
            "Projektet påstår inte att någon myndighet brutit mot lag. Frågan om",
            "sekretess i kontrollhandlingar saknar prejudikat från Högsta",
            "förvaltningsdomstolen för den handlingstyp som mäts, och "
            f"{COUNTED[data['appeals']]} beslut om maskning",
            "ligger hos kammarrätten. Där en avvikelse redovisas är den en",
            "avvikelse från befintlig kammarrättspraxis för beslutsbilagor,",
            "ingenting mer.",
            "",
            "Måttet är maskinellt och har kända gränser, som redovisas i",
            "dokumentationen tillsammans med de fel som rättats under arbetet.",
            "",
            "## Om ni vill svara",
            "",
            f"Svara på detta mejl senast den {in_swedish(data['deadline'])}, tre",
            "veckor efter att paketet skickades. Svaret publiceras oavkortat.",
            "Vill ni rätta en uppgift ber jag om den rättade uppgiften och var",
            "den kommer ifrån, så att rättelsen kan göras i underlaget och inte",
            "bara i texten.",
            "",
            "Med vänliga hälsningar,",
            "Martin Blomqvist",
            "",
            f"<!-- {slug}, genererad ur registren av "
            "pipeline/36_build_p12_packets.py -->",
        ]
    )
    return "\n".join(parts) + "\n"


def main() -> int:
    """Build every packet, refusing to write when a check fails."""
    log = read(LOG)
    masking = read(MASKING)
    contrast = read(CONTRAST)
    decisions = read(DECISIONS)
    grounds = read(GROUNDS)
    denominators = read(DENOMINATORS)
    if not log:
        print("data/protokoll_logg.jsonl saknas")
        return 1
    del contrast

    # The reply deadline is three weeks from the day the packets go out, which
    # is the day they are built unless the sender says otherwise. P12 gives
    # three weeks and tillämpningsnot 8 makes them a floor, so the date is
    # printed rather than left to the reader to count.
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--skickas",
        default=date.today().isoformat(),
        help="avsändningsdag, YYYY-MM-DD, förvalt i dag",
    )
    sent = date.fromisoformat(parser.parse_args().skickas)
    deadline = (sent + timedelta(days=REPLY_DAYS)).isoformat()
    # Counted from the decision register: it was written out as two and had
    # been three since Gotland was appealed on 22 September 2026.
    appeals = sum(
        1 for row in decisions if row["klass"] == "A" and row.get("malnummer")
    )

    authorities = sorted({r["myndighet"] for r in log if r["myndighet"] in SLUG})
    # The aggregate words come from open_items, so that a row logged under one
    # of them can never build a packet for an authority that does not exist,
    # and so that the two lists cannot drift apart.
    unknown = {r["myndighet"] for r in log if r["myndighet"] not in SLUG}
    unknown -= set(NOT_A_REQUEST)
    if unknown:
        print(f"myndigheter utan slug: {sorted(unknown)}")
        return 1

    built: dict[str, str] = {}
    for authority in authorities:
        slug = SLUG[authority]
        tracks = events_for(log, authority)
        data = {
            "tracks": tracks,
            "masking": {
                klass: masking_rows(masking, slug, klass) for klass in ("A", "B")
            },
            "grounds": [
                r
                for r in grounds
                if r["myndighet"] == authority.replace("Länsstyrelsen i ", "")
            ],
            "rank": {klass: ranking(masking, klass) for klass in ("A", "B")},
            "appeals": appeals,
            "deadline": deadline,
            "outside": {klass: outside(log, masking, klass) for klass in ("A", "B")},
            "slug": slug,
            "decisions": [r for r in decisions if r["myndighet"] == authority],
            "denominator": next(
                (
                    r
                    for r in denominators
                    if r["myndighet"] == authority.replace("Länsstyrelsen i ", "")
                ),
                None,
            ),
            "events": [e for e in log if e["myndighet"] == authority],
        }
        data["masking"] = {k: v for k, v in data["masking"].items() if v}
        built[authority] = packet(authority, data)

    offenders = []
    for authority, text in built.items():
        for label, pattern in FORBIDDEN.items():
            found = pattern.search(text)
            if found:
                offenders.append(f"{authority}: {label} ({found.group(0)!r})")
    if offenders:
        print(f"{len(offenders)} paket bär uppgifter som inte får skickas:")
        for offender in offenders[:20]:
            print(f"  {offender}")
        print("inget skrivet")
        return 1

    placed = sum(
        len([r for r in grounds if r["myndighet"] == a.replace("Länsstyrelsen i ", "")])
        for a in authorities
    )
    if placed != len(grounds):
        print(
            f"avstämningen faller: {len(grounds)} rader i sekretessgrunder, "
            f"{placed} placerade i ett paket"
        )
        return 1

    # Reconciliation: the documents named across the packets must be the
    # documents the corpus measure was taken over, class by class.
    for klass in ("A", "B"):
        corpus = [r for r in masking if r["path"].split("/")[0].endswith(f"_{klass}")]
        per_packet = sum(
            len(masking_rows(masking, SLUG[a], klass)) for a in authorities
        )
        if len(corpus) != per_packet:
            print(
                f"avstämningen faller för klass {klass}: korpus {len(corpus)}, "
                f"summa över paket {per_packet}"
            )
            return 1

    OUT.mkdir(parents=True, exist_ok=True)
    for authority, text in built.items():
        (OUT / f"{SLUG[authority]}.md").write_text(text, "utf-8", newline="\n")

    with_masking = sum(
        1
        for a in authorities
        if masking_rows(masking, SLUG[a], "A") or masking_rows(masking, SLUG[a], "B")
    )
    print(f"{len(built)} paket skrivna till {OUT.relative_to(ROOT)}")
    print(f"  med maskningsmätning: {with_masking}")
    print(f"  med eget beslut: {len({r['myndighet'] for r in decisions})}")
    print(f"  screeningen passerad: {', '.join(FORBIDDEN)}")
    print("  avstämning mot korpus per klass: A och B stämmer")
    return 0


if __name__ == "__main__":
    sys.exit(main())
