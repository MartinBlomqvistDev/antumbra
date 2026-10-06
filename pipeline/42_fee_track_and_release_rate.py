"""Two measures the protocol declared and nobody had computed.

Both rules are written here before the step is run, which is the order the
project keeps for anything that can flatter the result.

**The fee measure.** Tillämpningsnot 5 declares it in the same breath as the
rule it belongs to: "Antal skrivelser i avgiftsfrågan fram till ett överklagbart
beslut i ärendet, samt utfall i fyra klasser: beslut meddelat, beslut vägrat,
generellt styrdokument i stället för beslut, och uteblivet svar. Redovisas för
samtliga 21 länsstyrelser oavsett utfall, inklusive de län där noll skrivelser
behövdes." A letter in the fee matter is one of the project's own events in the
fee track; the outcome is read from the authority's own events, in the order the
note lists them, and a county that never raised a fee gets nought letters and
the outcome that no fee was raised.

**The release rate.** P11 defines it as "levererade handlingar delat med det
lägre av taket och antalet som fanns". The denominator is available: the cap is
20 in class A and 10 in class B, five in each after a fee narrowing under P5,
and the county's own count of controls and injunctions sits in
``data/namnare.jsonl``. The numerator is not. The cap counts controls and
decisions, while the deliveries arrive as files, and one control can be a report
plus photo annexes. Uppsala's class A is the plain case: 27 files for a cap of
20 controls. Nothing in the material converts between the two units, so the rate
is written as a gap with its reason, and what can be computed is reported
instead: whether the cap bound, and how many files came.

Writes ``data/avgiftsskrivelser.jsonl`` and ``data/utlamningsgrad.jsonl``.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

LOG = ROOT / "data" / "protokoll_logg.jsonl"
MASKING = ROOT / "data" / "maskning.jsonl"
DENOMINATORS = ROOT / "data" / "namnare.jsonl"
FEE_OUT = ROOT / "data" / "avgiftsskrivelser.jsonl"
RATE_OUT = ROOT / "data" / "utlamningsgrad.jsonl"

# The project's own letters in the fee matter. P5's narrowing answer is the
# first of them, since it is the reply the fee notice forces; the rest are the
# escalation that tillämpningsnot 2 and tillämpningsnot 5 set out.
OUR_FEE_LETTERS = {
    "avsmalningssvar",
    "avstående",
    "beslutsbegäran",
    "beslutsbegäran upprepad",
    "förnyad begäran om avgiftsbeslut",
}

# The authority's own events, read in the order tillämpningsnot 5 lists the
# outcomes. A decision beats a standing document, and a standing document beats
# silence, because each is a stronger answer than the one after it.
OUTCOMES = (
    ("beslut meddelat", {"avgiftsbeslut mottaget"}),
    ("beslut vägrat", {"avgiftsbeslut vägrat"}),
    ("generellt styrdokument", {"riktlinje bifogad", "taxebeslut bifogat"}),
)

FEE_NOTICE = "avgiftsbesked"
NO_FEE = "ingen avgift aviserad"
NO_ANSWER = "uteblivet svar"
# P5's own prediction, and the commonest outcome: the authority raises a fee,
# the narrowing answer goes out, and the documents then arrive without one. That
# is not a missing answer, and calling it one would charge the authority with a
# silence it never kept. It is only read where no fee remained after the
# narrowing, which the log marks with its own event.
FEE_LAPSED = "avgiften föll efter avsmalningen"
FEE_REMAINED = "avgift kvarstår"

CAPS = {"A": 20, "B": 10}
NARROWED_CAP = 5


def read(path: Path) -> list[dict]:
    """Every row of a JSONL file."""
    return [
        json.loads(line)
        for line in path.read_text("utf-8").splitlines()
        if line.strip()
    ]


def load_step36() -> Any:
    """Import step 36 for the authority list, the way steps 33 and 38 do."""
    path = ROOT / "pipeline" / "36_build_p12_packets.py"
    spec = importlib.util.spec_from_file_location("p12_packets", path)
    if spec is None or spec.loader is None:  # pragma: no cover - import guard
        raise SystemExit(f"kan inte importera {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules["p12_packets"] = module
    spec.loader.exec_module(module)
    return module


def counties(step36: Any) -> list[tuple[str, str]]:
    """The 21 county boards and their delivery folders, in alphabetical order."""
    return sorted(
        (authority, slug)
        for authority, slug in step36.SLUG.items()
        if authority.startswith("Länsstyrelsen i ")
    )


def fee_rows(log: list[dict], step36: Any) -> list[dict]:
    """One row per county: letters written, and how the fee matter ended."""
    events: dict[str, list[dict]] = defaultdict(list)
    for row in log:
        events[row["myndighet"]].append(row)

    rows = []
    for county, _ in counties(step36):
        own = events[county]
        notices = [row for row in own if FEE_NOTICE in row["handelse"]]
        letters = [row for row in own if row["handelse"] in OUR_FEE_LETTERS]
        remained = any(row["handelse"] == FEE_REMAINED for row in own)
        delivered = any(row["handelse"] == "leverans" for row in own)
        outcome = NO_FEE
        if notices:
            outcome = NO_ANSWER
            for name, handles in OUTCOMES:
                if any(row["handelse"] in handles for row in own):
                    outcome = name
                    break
            else:
                if delivered and not remained:
                    outcome = FEE_LAPSED
        rows.append(
            {
                "myndighet": county,
                "avgiftsbesked": len(notices),
                "skrivelser": len(letters),
                "skrivelsetyper": sorted({row["handelse"] for row in letters}),
                "utfall": outcome,
                "avgift_kvarstod": remained,
                "forsta_besked": notices[0]["datum"] if notices else None,
            }
        )
    return rows


def rate_rows(
    log: list[dict], masking: list[dict], denominators: list[dict], step36: Any
) -> list[dict]:
    """One row per county and class: the cap, whether it was narrowed, the gap."""
    narrowed = {
        (row["myndighet"], row["begaran"])
        for row in log
        if row["handelse"] == "avsmalningssvar"
    }
    # The denominator register names the county alone, without the authority
    # prefix the log uses.
    own_counts = {row["myndighet"] for row in denominators}

    rows = []
    for county, slug in counties(step36):
        for klass, cap in CAPS.items():
            files = sum(
                1 for row in masking if row["path"].startswith(f"{slug}_{klass}/")
            )
            rows.append(
                {
                    "myndighet": county,
                    "begaran": klass,
                    "tak": NARROWED_CAP if (county, klass) in narrowed else cap,
                    "avsmalnat": (county, klass) in narrowed,
                    "egen_nammare": county.replace("Länsstyrelsen i ", "")
                    in own_counts,
                    "filer": files,
                    "utlamningsgrad": None,
                    "skal": (
                        "täljaren och nämnaren är i olika enheter: taket räknar "
                        "kontroller och beslut, leveransen kommer som filer, och "
                        "ingenting i materialet växlar mellan dem"
                    ),
                }
            )
    return rows


def main() -> int:
    """Write both registers, or print what they would contain."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true", help="skriv ingenting")
    args = parser.parse_args()

    log = read(LOG)
    step36 = load_step36()
    fees = fee_rows(log, step36)
    rates = rate_rows(log, read(MASKING), read(DENOMINATORS), step36)

    tally: dict[str, int] = defaultdict(int)
    for row in fees:
        tally[row["utfall"]] += 1
    for outcome, number in sorted(tally.items()):
        print(f"{outcome}: {number}")
    print(f"skrivelser totalt: {sum(row['skrivelser'] for row in fees)}")
    print(f"län utan avgiftsbesked: {tally[NO_FEE]}")

    if args.dry_run:
        return 0

    for path, rows in ((FEE_OUT, fees), (RATE_OUT, rates)):
        path.write_bytes(
            (
                "\n".join(json.dumps(row, ensure_ascii=False) for row in rows) + "\n"
            ).encode("utf-8")
        )
        print(f"{len(rows)} rader skrivna till {path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
