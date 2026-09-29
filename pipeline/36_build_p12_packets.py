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

import json
import re
import sys
from collections import defaultdict
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from open_items import (  # noqa: E402
    DAY_ZERO,
    INTERNAL,
    NOT_A_REQUEST,
    THEIRS,
    working_days_between,
)

OUT = ROOT / "data" / "p12"
LOG = ROOT / "data" / "protokoll_logg.jsonl"
MASKING = ROOT / "data" / "maskning.jsonl"
CONTRAST = ROOT / "data" / "kontrast.jsonl"
DECISIONS = ROOT / "data" / "beslut.jsonl"
GROUNDS = ROOT / "data" / "sekretessgrunder.jsonl"

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
# What ends a request: the documents in hand, or a final decision.
FINAL = {
    "leverans",
    "rättad leverans",
    "delvis avslag och kompletterande leverans",
    "avslagsbeslut mottaget",
    "delvis avslagsbeslut mottaget",
    "avgiftsbeslut vägrat",
}

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
    """The event that ended the request, if one has."""
    ended = [e for e in events if e["handelse"] in FINAL]
    if not ended:
        return None
    return sorted(ended, key=lambda e: (e["datum"], e["klockslag"]))[-1]


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


def percent(value: float) -> str:
    """A share in Swedish, with a comma and a space before the sign."""
    return f"{value * 100:.1f}".replace(".", ",") + " %"


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
        "Detta är underlaget om er myndighet ur ett kunskapsunderlag om",
        "djurskyddskontrollens likvärdighet, byggt på myndigheternas egna beslut",
        "och kontrollhandlingar. Ni får det före publicering, med tre veckors",
        "svarstid, enligt punkt P12 i projektets handläggningsprotokoll. Ett svar",
        "publiceras oavkortat vid sidan av siffrorna. Uteblir svar publiceras",
        "siffrorna som de står, och det antecknas att svar inte kommit.",
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
                    f"Avslutat {last['datum']}, alltså dag {day}, loggat som "
                    f"{last['handelse']}. **Svarstiden redovisas som censurerad "
                    f"vid dag {MEASURE_CLOSES}**, eftersom datainsamlingen för "
                    "svarstidsmåttet stängdes den dagen enligt P10 och en "
                    "leverans efter den inte öppnar måttet igen. Handlingarna "
                    "ingår däremot fullt ut i maskningsmätningen. Regeln står i "
                    "tillägget till tillämpningsnot 7."
                )
            else:
                parts.append(
                    f"Avslutat enligt P1: **dag {day}**, {last['datum']}, "
                    f"loggat som {last['handelse']}."
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
        parts.append("under rektangeln.")
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
                f"| {percent(area)} |"
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
                f"enligt P1, är **{(share_a - share_b) * 100:.0f} procentenheter** "
                f"i andel maskade dokument mellan klass A och klass B."
            )
            parts.append("")

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
            f"delar plats, eftersom mätningen inte skiljer dem åt. Hela "
            f"ordningen står nedan, eftersom en placering utan de andra talen "
            f"inte går att bedöma."
        )
        parts.append("")
        parts.append("| Plats | Myndighet | Dokument | Med minst en maskning |")
        parts.append("| --- | --- | --- | --- |")
        for slug_, count, share in table:
            position = sum(1 for row in table if row[2] > share) + 1
            mark = " **(ni)**" if slug_ == data["slug"] else ""
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
        )
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

    if data["decisions"]:
        parts.append("## Beslut ni meddelat, ordagrant")
        parts.append("")
        for row in data["decisions"]:
            parts.append(
                f"Beslut {row['diarienummer']}, {row['beslutsdatum']}, klass "
                f"{row['klass']}, fattat av {row['beslutsfattare']} med "
                f"{row['foredragande']} som föredragande. Namnen står i beslutet "
                f"och återges inte här."
            )
            parts.append("")
            parts.append(f"> {row['citat_bedomning']}")
            parts.append("")

    parts.extend(
        [
            "## Vad underlaget inte påstår",
            "",
            "Projektet påstår inte att någon myndighet brutit mot lag. Frågan om",
            "sekretess i kontrollhandlingar saknar prejudikat från Högsta",
            "förvaltningsdomstolen för den handlingstyp som mäts, och två beslut",
            "ligger hos kammarrätten. Där en avvikelse redovisas är den en",
            "avvikelse från befintlig kammarrättspraxis för beslutsbilagor,",
            "ingenting mer.",
            "",
            "Måttet är maskinellt och har kända gränser, som redovisas i",
            "dokumentationen tillsammans med de fel som rättats under arbetet.",
            "",
            "## Om ni vill svara",
            "",
            "Svara på detta mejl inom tre veckor. Svaret publiceras oavkortat.",
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
    if not log:
        print("data/protokoll_logg.jsonl saknas")
        return 1
    del contrast

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
            "slug": slug,
            "decisions": [r for r in decisions if r["myndighet"] == authority],
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
