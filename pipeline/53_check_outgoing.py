"""Reconcile the outgoing register against the protocol log, authority by authority.

The log recorded every letter when it went, so it is the list the register has
to match. This step asks one question per authority: which of its logged sends
have a row, and which do not. It is run between authorities rather than at the
end, because a sweep that is only checked once is a sweep whose gaps are found
too late to fix cheaply.

A send in the log is an event the project performed, and which events those are
is settled in src/open_items.py rather than again here. This step subtracts
from that set the few of our own events that send no letter, and names the one
letter whose log row carries a type that is not a letter type.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

import open_items  # noqa: E402  the project's own module, after the path

LOG = ROOT / "data" / "protokoll_logg.jsonl"
OUT = ROOT / "data" / "korrespondens_utgaende.jsonl"

# Which events are the project's own is already settled, once, in
# src/open_items.py, and an invariant in the test suite fails if a type in the
# log is in none of its three sets. This step had its own copy of that list.
# The copy was wrong: three kinds of letter were missing from it, so the
# reconciliation reported authorities complete whose letters it had never asked
# for, and the denominator stood at 160 when it was 176. The list is derived
# here instead, and a new event type is classified in the one place.
NOT_A_LETTER = frozenset(
    {
        # Ours, but no letter goes. It is the decision not to appeal a
        # decision, taken under tillämpningsnot 6.
        "avstående från överklagande",
        # Ours, but no letter goes. A request for a decision that lapsed on a
        # condition the earlier letter set itself.
        "beslutsbegäran förfallen",
        # Ours, and one of the fifteen was a letter. The rest correct the
        # project's own notes, its log or an unsent read-copy, so the type is
        # not a letter type and the one letter stands in EXTRA below.
        "rättelse",
    }
)
SENDS = frozenset(open_items.OURS) - NOT_A_LETTER

# Letters whose log row carries a type that is not a letter type. One so far:
# the correction sent to Västmanland. It is keyed on the row that records it,
# so the reconciliation asks for it like any other letter.
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
