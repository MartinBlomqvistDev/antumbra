"""Prepare the day 40 letters: P10's last reminder and P11's denominator question.

Step 37 of the pipeline. Two letters go out on day 40, Monday 28 September 2026.
P10's reminder goes to the requests that have received neither documents nor a
decision, and P11's question goes to all 21 county boards. Neither has a
template in the protocol, unlike P2, P3, P5 and P8, so the wording lives here,
committed and reviewable, rather than in the protocol, where a template added
now would be a rule written after the fact.

**Neither letter says that anything is being measured.** That is decision 8 in
the protocol's own decision log, dated 2 August 2026, before the first request
went out: informing the authorities was considered and rejected, because a
pre-announced measurement measures an announced review. Section 5 says the same
of an unrequested statement of purpose, and section 9 already asserts publicly
that all correspondence followed a pre-registered protocol. The authority learns
everything at P12, three weeks before publication, with its reply published
unabridged. A machine check below refuses to write a letter that would break
this, because the rule was broken twice in one afternoon while these drafts were
written.

**P10 does not ask for an appealable decision.** Decision 5 in the same log:
such a decision is requested only after a masked delivery, uniformly, because
asking in advance risks a more cautious first delivery, and the first delivery
is what the masking measure rests on. The eighteen authorities that delivered
were asked afterwards under P8. Asking the three that have not delivered would
put the request before their first delivery and treat them differently.

**The quoted request is read out of the protocol, not copied.** A copy drifts.
The letter quotes the code block under section 2 or section 3 of
docs/BEGARANMALL.md as it stands.

**The recipient set is read against notes 3 and 7, not against a filter.** A
request that is fee-stopped with a decision requested under note 2 reaches its
final status through note 3 point 2, not through note 7's silence, however
literally it lacks both documents and a decision. Kalmar B is that shape and has
answered eight times; a filter would have sent it the wrong letter.

Writes data/dag40/, which is gitignored. Nothing is sent, and the sending date
is set by the protocol, not by this step.

Usage:
    python pipeline/37_build_day40_letters.py
"""

from __future__ import annotations

import re
import sys
import textwrap
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from open_items import THEIRS, by_request, load  # noqa: E402

OUT = ROOT / "data" / "dag40"
PROTOCOL = ROOT / "docs" / "BEGARANMALL.md"

# Day 40 in the protocol, Monday. The letters are dated, not sent, here.
DAY_40 = date(2026, 9, 28)

DELIVERED = frozenset(
    {"leverans", "rättad leverans", "delvis avslag och kompletterande leverans"}
)
DECIDED = frozenset(
    {
        "avslagsbeslut mottaget",
        "delvis avslagsbeslut mottaget",
        "avgiftsbeslut mottaget",
        "avgiftsbeslut vägrat",
    }
)
# Tillämpningsnot 3 point 2: copies declined and a decision on the fee asked
# for. Such a request reaches its final status at day 40 through the note, and
# P10's reminder is not for it.
FEE_STOPPED = frozenset({"avstående"})

CLASS_SECTION = {"A": "## 2. Begäran A", "B": "## 3. Begäran B"}

# What a letter may never contain. Decision 8 in the protocol's decision log is
# a rule about content, so it is checked as one. Every word here was either in a
# draft written on 7 September 2026 or is the obvious next way to say it.
FORBIDDEN_WORDS = (
    "mäta",
    "mätning",
    "mäts",
    "jämför",
    "jämförelse",
    "samtliga länsstyrelser",
    "alla länsstyrelser",
    "kartläggning",
    "studie",
    "undersökning",
    "granskning",
    "redovisas",
    "publiceras",
    "projekt",
)
# Personal data, screened as everywhere else. The address in the signature is
# the sender's own and is allowed; nothing else that looks like contact details
# may appear.
FORBIDDEN_PATTERNS = {
    "personnummer": re.compile(r"\b(?:19|20)\d{6}[-+]\d{4}\b"),
    "telefonnummer": re.compile(r"\b0\d{1,3}[-\s]\d{2,3}\s?\d{2}\s?\d{2}\b"),
}

COUNTIES = [
    "Blekinge",
    "Dalarna",
    "Gotland",
    "Gävleborg",
    "Halland",
    "Jämtland",
    "Jönköping",
    "Kalmar",
    "Kronoberg",
    "Norrbotten",
    "Skåne",
    "Stockholm",
    "Södermanland",
    "Uppsala",
    "Värmland",
    "Västerbotten",
    "Västernorrland",
    "Västmanland",
    "Västra Götaland",
    "Örebro",
    "Östergötland",
]

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

# The log's event names are the project's own vocabulary and do not belong in a
# letter to the authority whose message they describe. These are the same events
# in the words a letter uses.
IN_PLAIN = {
    "avgiftsbesked": "fick jag besked om en avgift",
    "avgiftsbesked och förtydligande": (
        "fick jag besked om en avgift och ett förtydligande"
    ),
    "avgiftsbesked och erbjudande om maskad elektronisk leverans": (
        "fick jag besked om en avgift"
    ),
    "förtydligandefråga": "fick jag en fråga om begärans omfattning",
    "förtydligandefråga och avgiftsbesked": (
        "fick jag en fråga om begärans omfattning och besked om en avgift"
    ),
    "förtydligandefråga upprepad": "fick jag en förnyad fråga om begärans omfattning",
    "besked om uttagets omfattning och förtydligandefråga": (
        "fick jag en fråga om begärans omfattning"
    ),
    "arbetsbesked": "fick jag besked om att ärendet handläggs",
    "mottagningsbesked": "fick jag ett mottagningsbesked",
    "diarieföringsbesked": "fick jag besked om att begäran diarieförts",
    "manuellt svar": "fick jag ett svar",
    "besked": "fick jag ett besked",
}

# My own moves, in the same plain words. The narrowing carries P5's fixed
# wording, so the letter states the request that actually stands rather than
# re-asserting the wider one it started as.
MINE_PLAIN = {
    "avsmalningssvar": (
        "begränsade jag begäran till {narrowing}, och det är den begränsade "
        "begäran som står"
    ),
    "svar på förtydligandefråga": "svarade jag på frågan",
    "svar på förtydligande": "svarade jag på frågan",
    "förtydligande": "lämnade jag ett förtydligande",
    "påminnelse": "påminde jag om begäran",
}

# P5's fixed narrowing, per request class, in the protocol's own words.
NARROWING = {
    "A": (
        "de fem senast genomförda kontrollerna, räknat efter kontrolldatum, "
        "under samma period"
    ),
    "B": (
        "de fem senast meddelade besluten, räknat efter beslutsdatum, under "
        "samma period"
    ),
}

# P11's question, quoted from the protocol so that it cannot drift.
P11_QUESTION = (
    "Hur många djurskyddskontroller av anläggningar med nötkreatur, grisar "
    "respektive fjäderfä genomförde ni under perioden 1 januari 2024 till 31 "
    "december 2025, och hur många beslut om föreläggande i djurskyddsärenden "
    "som gäller hållning av nötkreatur, grisar eller fjäderfä meddelade ni "
    "under perioden 1 januari 2022 till 31 december 2025?"
)


def swedish(iso: str) -> str:
    """A date as a letter writes it, not as a file names it."""
    year, month, day = (int(part) for part in iso.split("-"))
    return f"{day} {MONTHS[month - 1]} {year}"


def quoted_request(klass: str, myndighet: str) -> str:
    """The original request, read out of the protocol with the placeholder filled.

    A copy would drift from the protocol, and an unfilled placeholder would go
    out in a letter. Both are avoided by reading the block and substituting the
    one thing the template leaves open.
    """
    text = PROTOCOL.read_text("utf-8")
    start = text.index(CLASS_SECTION[klass])
    block = text.index("```", start) + 3
    end = text.index("```", block)
    request = text[block:end].strip("\n")
    return request.replace("Till Länsstyrelsen i [län]", f"Till {myndighet}")


def p10_recipients(rows: list[dict]) -> list[tuple[str, str, list[dict]]]:
    """The requests P10's reminder is for, and their events."""
    out = []
    for (myndighet, klass), events in sorted(by_request(rows).items()):
        if klass not in CLASS_SECTION:
            continue
        names = {e["handelse"] for e in events}
        if names & DELIVERED or names & DECIDED or names & FEE_STOPPED:
            continue
        out.append((myndighet, klass, events))
    return out


def last_exchange(events: list[dict]) -> tuple[dict | None, dict | None]:
    """Their last message and my last one, which is where the silence began."""
    ordered = sorted(events, key=lambda e: (e["datum"], e["klockslag"]))
    mine = [
        e for e in ordered if e["kanal"] == "e-post" and e["handelse"] not in THEIRS
    ]
    theirs = [
        e for e in ordered if e["handelse"] in THEIRS and e["handelse"] != "autosvar"
    ]
    return (theirs[-1] if theirs else None, mine[-1] if mine else None)


def p10_letter(myndighet: str, klass: str, events: list[dict]) -> str:
    """The last reminder, with this recipient's own dates in it.

    The request that stands is the narrowed one wherever a fee notice was
    answered under P5, so the letter says so. Quoting only the original would
    re-assert a wider request than the one that is outstanding.
    """
    said: list[str] = []
    previous = ""
    for event in sorted(events, key=lambda e: (e["datum"], e["klockslag"])):
        if event["handelse"] in THEIRS:
            phrase = IN_PLAIN.get(event["handelse"])
        else:
            phrase = MINE_PLAIN.get(event["handelse"])
            if phrase:
                phrase = phrase.format(narrowing=NARROWING[klass])
        if not phrase:
            continue
        day = (
            "Samma dag"
            if event["datum"] == previous
            else f"Den {swedish(event['datum'])}"
        )
        said.append(f"{day} {phrase}.")
        previous = event["datum"]
    said.append("Därefter har jag inte fått handlingarna.")
    body = textwrap.wrap(" ".join(said), width=72)
    return "\n".join(
        [
            f"Till {myndighet}",
            "",
            "Hej!",
            "",
            "Den 3 augusti 2026 begärde jag att få ta del av handlingar hos er,",
            "se den ursprungliga begäran nedan.",
            "",
            *body,
            "",
            "Enligt 2 kap. 16 § tryckfrihetsförordningen ska en begäran om kopia",
            "av allmän handling behandlas skyndsamt. Jag ber om besked om när",
            "handlingarna kan lämnas ut.",
            "",
            "Med vänliga hälsningar,",
            "Martin Blomqvist",
            "cm.blomqvist@gmail.com",
            "",
            "",
            quoted_request(klass, myndighet),
            "",
        ]
    )


def p11_letter(county: str) -> str:
    """The denominator question, identical to all 21 but never saying so."""
    return "\n".join(
        [
            f"Till Länsstyrelsen i {county}",
            "",
            "Hej!",
            "",
            "Jag återkommer i det ärende där jag den 3 augusti 2026 begärde",
            "handlingar hos er. Jag har en avslutande fråga:",
            "",
            *textwrap.wrap(P11_QUESTION, width=72),
            "",
            "Frågan gäller antal och inga handlingar.",
            "",
            "Med vänliga hälsningar,",
            "Martin Blomqvist",
            "cm.blomqvist@gmail.com",
            "",
        ]
    )


def screen(letters: dict[str, str]) -> list[str]:
    """What a letter may not contain, checked before anything is written."""
    offenders = []
    for name, text in letters.items():
        # The quoted request is the protocol's own text and is not screened for
        # words; only the part written here is.
        written = text.split("Med vänliga hälsningar,")[0].lower()
        for word in FORBIDDEN_WORDS:
            if word in written:
                offenders.append(f"{name}: ordet {word!r}")
        for label, pattern in FORBIDDEN_PATTERNS.items():
            if pattern.search(text):
                offenders.append(f"{name}: {label}")
    return offenders


def main() -> int:
    """Write both letters for every recipient, refusing on a failed screen."""
    rows = load()
    letters: dict[str, str] = {}

    recipients = p10_recipients(rows)
    for myndighet, klass, events in recipients:
        slug = myndighet.replace("Länsstyrelsen i ", "").lower()
        slug = slug.replace(" ", "_").replace("ä", "a").replace("ö", "o")
        slug = slug.replace("å", "a")
        letters[f"p10_{slug}_{klass}.txt"] = p10_letter(myndighet, klass, events)
    for county in COUNTIES:
        slug = county.lower().replace(" ", "_")
        slug = slug.replace("ä", "a").replace("ö", "o").replace("å", "a")
        letters[f"p11_{slug}.txt"] = p11_letter(county)

    offenders = screen(letters)
    if offenders:
        print(f"{len(offenders)} brev bryter mot beslutslogg rad 8 eller screeningen:")
        for offender in offenders[:20]:
            print(f"  {offender}")
        print("inget skrivet")
        return 1

    OUT.mkdir(parents=True, exist_ok=True)
    for name, text in letters.items():
        (OUT / name).write_text(text, "utf-8", newline="\n")

    print(
        f"{len(letters)} brev skrivna till {OUT.relative_to(ROOT)}, daterade {DAY_40}"
    )
    print(f"  P10, sista påminnelsen: {len(recipients)} mottagare")
    for myndighet, klass, _ in recipients:
        print(f"    {myndighet} {klass}")
    print(f"  P11, nämnarfrågan: {len(COUNTIES)} länsstyrelser")
    print("  screeningen passerad: inget om mätning, jämförelse eller publicering")
    print("  ingenting skickat; utskicksdagen är dag 40 och avgörs av protokollet")
    return 0


if __name__ == "__main__":
    sys.exit(main())
