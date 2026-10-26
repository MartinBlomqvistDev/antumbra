"""Build one row of the outgoing correspondence register from a sent message.

The rules are in docs/KORRESPONDENS.md under the outgoing section, and they are
here in code rather than in a judgement per letter. The step takes the payload
of one message from the mailbox, cuts what the rules say to cut, and writes the
row to ``data/korrespondens_utgaende.jsonl``.

What it cuts: the quoted history under my own text, the link targets, and a
line that was nothing but a link. What it never writes: the recipient's
address. A letter to a named official is recorded as having gone to a named
official and nothing more, because writing to someone does not make their
address mine to publish.

What it keeps: my own signature, my name and the e-mail address I wrote from.
The measurement rests on who asked, and masking that would hide the one thing
all twenty-two authorities could see.

What it removes even though it is mine: the identity block an appeal to an
administrative court of appeal has to carry, which is a personal identity
number, a home address and a daytime telephone number. Those were written for
one court, not for a public register, and a line that makes sense in a filing
does not become publishable because the person who wrote it is the one
publishing. The cut is declared in the row like every other.
"""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "korrespondens_utgaende.jsonl"

# Where an Outlook or Gmail quote begins. The authorities' clients write the
# first, mine writes the second, and both start the block that is already in
# the registers.
# Where a quote begins. Every client writes the marker differently, and
# Gmail breaks "On ... wrote:" across two lines, which an expression
# anchored to one line silently misses: four of the first eight rows kept
# their marker and the first quoted line until the reconciliation caught
# it. A line starting with ">" is the last resort, since every client
# prefixes the quoted block that way. A second miss, found by CI on the
# first commit of the outgoing register: Gmail wraps the marker so that
# the sender's address lands on its own line before "wrote:", which an
# expression allowing only a newline between them lets through, address
# and all.
QUOTE = re.compile(
    r"^(?:Från: |From: |Den [^\n]{0,60} skrev[^\n]*:$"
    r"|On\b[^\n]{0,80}(?:\n[^\n]{0,80})?wrote:"
    r"|-{3,} ?Vidarebefordrat|>)",
    re.M,
)
# A markdown-style link target the client appended after the text it labels.
TARGET = re.compile(r"<(?:https?|mailto):[^>\s]+>")
# A line that was nothing but a link once its target is gone.
BARE = re.compile(r"^\s*(?:https?://\S+|\[cid:[^\]]+\])\s*$", re.M)
# The identity block of an appeal: the labelled lines a filing to a court has
# to carry. Four appeals went, each one carrying these three lines, and the
# register is published.
IDENTITY = re.compile(
    r"^(?:Personnummer|Adress|Telefon(?: dagtid)?|Postadress)\s*:.*$",
    re.M | re.I,
)
# A personal identity number anywhere else in the text, whatever label stands
# in front of it. The labelled lines above are the known shape; this is for the
# one that is written some other way.
PERSONNUMMER = re.compile(
    r"\b(?:19|20)?\d{2}(?:0[1-9]|1[0-2])(?:0[1-9]|[12]\d|3[01])[-+]\d{4}\b"
)


def swedish_time(utc: str) -> tuple[str, str]:
    """The message header's UTC turned into Swedish time, as date and clock.

    August to October 2026 is summer time throughout, so the offset is two
    hours for every message in this collection. The register says so rather
    than carrying a library that would be right for dates it never sees.
    """
    stamp = datetime.fromisoformat(utc.replace("Z", "+00:00")) + timedelta(hours=2)
    return stamp.strftime("%Y-%m-%d"), stamp.strftime("%H:%M:%S")


def cut(body: str) -> tuple[str, list[str]]:
    """The text as it was written, with the four cuts the rules require."""
    omitted = []
    quote = QUOTE.search(body)
    if quote:
        body = body[: quote.start()]
        omitted.append("den citerade historiken under mitt meddelande")
    if TARGET.search(body):
        body = TARGET.sub("", body)
        omitted.append("länkmålen bakom texten")
    if BARE.search(body):
        body = BARE.sub("", body)
        omitted.append("en rad som inte var annat än en länk")
    if IDENTITY.search(body):
        body = IDENTITY.sub("[utelämnat]", body)
        omitted.append(
            "mina egna identitetsuppgifter ur överklagandets partsuppgifter, "
            "alltså personnummer, bostadsadress och telefonnummer"
        )
    if PERSONNUMMER.search(body):
        body = PERSONNUMMER.sub("[utelämnat]", body)
        omitted.append("ett personnummer i löptexten")
    return body.strip(), omitted


def main() -> int:
    """Read a payload, write the row, and say what it left out."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("payload", type=Path, help="meddelandets nyttolast som JSON")
    parser.add_argument("--myndighet", required=True, help="mottagande myndighet")
    parser.add_argument("--begaran", required=True, help="A, B, C eller A+B")
    parser.add_argument(
        "--mottagare",
        required=True,
        choices=("funktionsbrevlåda", "namngiven tjänsteman"),
        help="mottagarens art, aldrig adressen",
    )
    parser.add_argument("--handelse", required=True, help="loggens händelsetyp")
    parser.add_argument(
        "--anmarkning", default="", help="det som bara en läsare kan anmärka"
    )
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    payload = json.loads(args.payload.read_text("utf-8"))
    date, clock = swedish_time(payload["date"])
    text, omitted = cut(payload["plaintextBody"])
    if args.anmarkning:
        omitted.append(args.anmarkning)

    row = {
        "datum": date,
        "klockslag": clock,
        "myndighet": args.myndighet,
        "begaran": args.begaran,
        "mottagare": args.mottagare,
        "handelse": args.handelse,
        "amnesrad": payload["subject"],
        "meddelande": payload["id"],
        "text": text,
        "utelamnat": "; ".join(omitted) or None,
        "storlek": payload["sizeEstimate"],
        "kalla": (
            "Gmail, meddelandets plaintext-del. Inget råsvar är arkiverat: "
            "raden är byggd ur nyttolasten vid hämtningen, och meddelande-id "
            "är det som gör den kontrollerbar mot brevlådan."
        ),
    }

    print(json.dumps(row, ensure_ascii=False, indent=1))
    if args.dry_run:
        return 0

    existing = set()
    if OUT.exists():
        existing = {
            json.loads(line)["meddelande"]
            for line in OUT.read_text("utf-8").splitlines()
            if line.strip()
        }
    if row["meddelande"] in existing:
        print("raden finns redan, ingenting skrivet")
        return 0
    with OUT.open("a", encoding="utf-8", newline="\n") as handle:
        handle.write(json.dumps(row, ensure_ascii=False) + "\n")
    print(f"skrivet till {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
