"""Reconcile the outgoing register against the protocol log, authority by authority.

The log recorded every letter when it went, so it is the list the register has
to match. This step asks one question per authority: which of its logged sends
have a row, and which do not. It is run between authorities rather than at the
end, because a sweep that is only checked once is a sweep whose gaps are found
too late to fix cheaply.

A send in the log is an event the project performed. Every event type is listed
below, as a send or as something else, and a type in neither list stops the
step. The first version listed only the sends and filtered on that list, which
is not the same thing: three types of letter were missing from it, and the step
reported the register complete for authorities whose letters it had never asked
for. The docstring claimed an unknown type would show up. Nothing made it.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LOG = ROOT / "data" / "protokoll_logg.jsonl"
OUT = ROOT / "data" / "korrespondens_utgaende.jsonl"

# Every event in the log that is a letter from the project to an authority.
SENDS = frozenset(
    {
        # Found missing on 26 October 2026, when a letter in the mailbox had no
        # line in the reconciliation to belong to. Both are letters: the first
        # declines the copies once a fee remains, which is P5, and the second is
        # P8's request for an appealable decision.
        "avstående",
        "beslutsbegäran och fråga om uttagets fullständighet",
        "avsändning",
        "avsmalningssvar",
        "svar på förtydligandefråga",
        "svar på förtydligandefråga och accept av elektronisk leverans",
        "svar på förtydligandefråga om nämnaren",
        "överklagande",
        "påminnelse",
        "nämnarfråga",
        "P12-paket avsänt",
        "rättelse av P12-paket",
        "förnyad begäran om avgiftsbeslut",
        "beslutsbegäran",
        "beslutsbegäran upprepad",
        "delgivningskvitto",
        "svar på invändning mot P12-paket",
        "förtydligande",
        "svar på besked om tidigare leverans",
        "förfrågan om beskedets innebörd",
        "förfrågan om länsuppdelning",
        "förfrågan om fjäderfätäckning",
        "förfrågan om elektroniskt utlämnande",
        "yttrande till kammarrätten",
    }
)

# Every other event type in the log: the authority's messages, the courts', and
# the project's own notes to itself. Kept explicitly so that the step can tell
# a type it has classified from a type nobody has looked at yet.
#
# "rättelse" sits here although one of its fifteen rows is a letter. The type
# records a correction, and fourteen of them correct the project's own notes,
# its log or an unsent read-copy. The fifteenth, to Västmanland on 28 September
# 2026, is a letter that went. A type cannot be half a send, so the type is not
# one, and that single letter is named in EXTRA below.
NOT_SENDS = frozenset(
    {
        "arbetsbesked",
        "autosvar",
        "beslut",
        "brevlådan genomgången",
        "förberedelse",
        "autosvar på P12-paket",
        "avgift kvarstår",
        "avgiftsbesked",
        "avgiftsbesked och erbjudande om maskad elektronisk leverans",
        "avgiftsbesked och förtydligande",
        "avgiftsbeslut mottaget",
        "avgiftsbeslut vägrat",
        "avslagsbeslut mottaget",
        "avstående från överklagande",
        "besked",
        "besked om att dimension 1 inte kan tas fram",
        "besked om tidigare leverans",
        "besked om uttagets omfattning",
        "besked om uttagets omfattning och förtydligandefråga",
        "besked om vidarebefordran",
        "beslutsbegäran förfallen",
        "delvis avslag och kompletterande leverans",
        "delvis avslagsbeslut mottaget",
        "diarieföringsbesked",
        "förnyat avgiftserbjudande",
        "förregistrerat prövningsvillkor",
        "förregistrering",
        "förtydligandefråga",
        "förtydligandefråga och avgiftsbesked",
        "förtydligandefråga om nämnaren",
        "förtydligandefråga upprepad",
        "kompletterande leverans",
        "kompletterande leverans arkiverad",
        "leverans",
        "leverans arkiverad",
        "leverans fullgjord",
        "manuellt svar",
        "mottagningsbesked",
        "målregistrering i kammarrätten",
        "personuppgift",
        "protokollavvikelse",
        "publicering",
        "påminnelse om delgivning",
        "rättsfråga verifierad",
        "riktlinje bifogad",
        "rättad leverans",
        "rättelse",
        "sammanslagning enligt P0b",
        "svar om uttagets uppbyggnad",
        "svar på P12-paket",
        "svar på förtydligande",
        "svar på nämnarfrågan",
        "taxebeslut bifogat",
        "tillämpningsnot skriven",
        "underrättelse från kammarrätten",
        "utfall",
        "överlämnande till kammarrätten",
    }
)

# Letters whose log row carries a type that is not a send type. One so far: the
# correction sent to Västmanland. It is keyed on the row that records it, so the
# reconciliation asks for it like any other letter.
EXTRA = frozenset(
    {
        ("Länsstyrelsen i Västmanland", "2026-09-28", "rättelse", "A"),
    }
)


def read(path: Path) -> list[dict]:
    """Every row of a JSONL file, or nothing when the file is not there yet."""
    if not path.exists():
        return []
    return [
        json.loads(line)
        for line in path.read_text("utf-8").splitlines()
        if line.strip()
    ]


def main() -> int:
    """Print what is done and what is missing, per authority."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--myndighet", help="stäm av en myndighet i taget")
    args = parser.parse_args()

    rows = read(LOG)
    unknown = sorted({r["handelse"] for r in rows} - SENDS - NOT_SENDS)
    if unknown:
        print("okand handelsetyp, klassificera den i steg 53:")
        for name in unknown:
            print(f"  {name}")
        return 1

    logged: dict[str, list[dict]] = defaultdict(list)
    for row in rows:
        if row["myndighet"] == "samtliga":
            continue
        key = (row["myndighet"], row["datum"], row["handelse"], row["begaran"])
        if row["handelse"] in SENDS or key in EXTRA:
            logged[row["myndighet"]].append(row)

    done: dict[str, list[dict]] = defaultdict(list)
    for row in read(OUT):
        done[row["myndighet"]].append(row)

    names = [args.myndighet] if args.myndighet else sorted(logged)
    total_logged = total_done = 0
    for name in names:
        sends = logged.get(name, [])
        rows = done.get(name, [])
        total_logged += len(sends)
        total_done += len(rows)
        state = "KLAR" if len(rows) >= len(sends) else f"{len(sends) - len(rows)} kvar"
        print(f"{name}: {len(rows)} av {len(sends)} — {state}")
        if args.myndighet or len(rows) < len(sends):
            # Counted and not set-matched: two narrowings on the same day, one
            # per request class, were both ticked off by a single row when the
            # check compared sets. A gap that the gap-finder hides is worse
            # than no gap-finder. The request class belongs in the key for the
            # same reason: the two requests went out one minute apart on 3
            # August, so a key of date and event alone let the class B row tick
            # off the class A line and report a missing letter as present.
            have = Counter(
                (row["datum"], row["handelse"], row["begaran"]) for row in rows
            )
            for send in sends:
                key = (send["datum"], send["handelse"], send["begaran"])
                known = have[key] > 0
                if known:
                    have[key] -= 1
                mark = "  ok    " if known else "  SAKNAS "
                print(
                    f"{mark}{send['datum']} {send['klockslag']} "
                    f"{send['begaran']} {send['handelse']}"
                )
    print(f"\ntotalt: {total_done} av {total_logged} brev i registret")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
