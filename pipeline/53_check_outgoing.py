"""Reconcile the outgoing register against the protocol log, authority by authority.

The log recorded every letter when it went, so it is the list the register has
to match. This step asks one question per authority: which of its logged sends
have a row, and which do not. It is run between authorities rather than at the
end, because a sweep that is only checked once is a sweep whose gaps are found
too late to fix cheaply.

A send in the log is an event the project performed. The event types are listed
here rather than inferred, so that a new type added later shows up as unknown
instead of being silently left out of the reconciliation.
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

    logged: dict[str, list[dict]] = defaultdict(list)
    for row in read(LOG):
        if row["handelse"] in SENDS and row["myndighet"] != "samtliga":
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
            # than no gap-finder.
            have = Counter((row["datum"], row["handelse"]) for row in rows)
            for send in sends:
                key = (send["datum"], send["handelse"])
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
