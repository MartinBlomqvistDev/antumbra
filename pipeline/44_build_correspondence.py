"""Build the correspondence register from saved raw replies.

The register was built by hand, message by message, in the session. That made
every session re-read the rules, re-fetch messages whose answers had scrolled
away, and re-compare texts against their carrier. This step moves all of it
except the fetch itself into code.

The raw API answer for each message is saved under `data/korrespondens_raw/`,
which is outside git because it carries officials' names and personal
addresses. What is committed is a manifest with the message id, the header
time, the size and a sha256 per file, the same pattern as ADR-0004 uses for
the source documents. The step is deterministic: run it again and it writes
the same rows.

Run as: python pipeline/44_build_correspondence.py [--check]
"""

import argparse
import hashlib
import json
import re
from datetime import UTC, datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "korrespondens_raw"
MANIFEST = ROOT / "data" / "korrespondens_manifest.jsonl"
SIGNATURES = ROOT / "data" / "korrespondens_signaturer.jsonl"

# The header time is UTC and the register is Swedish local time. August to
# October 2026 is CEST throughout, so the offset is a constant two hours; a
# message outside that window would need the rule rewritten, and the step says
# so instead of guessing.
SWEDISH_OFFSET = timedelta(hours=2)
CEST = (datetime(2026, 3, 29, tzinfo=UTC), datetime(2026, 10, 25, tzinfo=UTC))

# A link target the mail client renders after the link text, and an address in
# angle brackets. Both are dropped; the text that carried them stays.
LINK_TARGET = re.compile(r"<(?:https?://|mailto:)[^>]*>")
# The same thing in the other syntax: the system notices from the counties'
# shared no_reply address render a link as [text](url). The link text is the
# authority's own word and stays; only the target goes.
MARKDOWN_LINK = re.compile(r"\[([^\]]+)\]\((?:https?://|mailto:)[^)]*\)")
# The quoted history starts at the first of these, and everything after it is
# the copy of my own letter or the authority's earlier one, published elsewhere.
HISTORY = (
    # Outlook opens every quoted letter with this header, whoever sent it. The
    # first version matched only my own name and the counties', and a letter
    # forwarded inside Jordbruksverket therefore kept its history, address and
    # all. Anything after the header is a copy of a letter published elsewhere.
    re.compile(r"^Från: ", re.MULTILINE),
    re.compile(r"^On \w{3}, \w{3} \d{1,2}, \d{4}", re.MULTILINE),
)
# The file list the Filskick service writes into the body, and its link. The
# service writes the header in Swedish or in English depending on the
# message, and Jordbruksverket's delivery of 336 files came in English.
FILE_LIST = re.compile(
    r"^(?:Dessa filer är bifogade i meddelandet:|"
    r"The following files are attached to this message:)",
    re.MULTILINE,
)
# A greeting ends the letter's own words. What follows is the signature, and
# where that signature names a person ADR-0018 keeps the name out, so the cut
# is made after the greeting whenever the next line looks like a name. The
# same pattern guards the register in tests/, and the words an authority's own
# name starts with are excluded there and here.
GREETING = re.compile(
    r"^(Med vänlig hälsning|Med vänliga hälsningar|Vänliga hälsningar|"
    r"Vänlig hälsning|Vänligen|Hälsningar|Mvh)[,!]?$",
    re.MULTILINE,
)
NAME_LINE = re.compile(r"^[A-ZÅÄÖ][a-zåäöé]+ [A-ZÅÄÖ][a-zåäöé]+$")
# A signature whose first line is a single capitalised word is either a first
# name, a title or the unit itself, and nothing in the word says which: this
# mailbox holds both Djurskyddshandläggare and signers who write only their
# first name. The step does not guess. The judgement is read per message out
# of data/korrespondens_signaturer.jsonl, which carries the judgement and
# never the word, and a message without one stops the step.
ONE_WORD = re.compile(r"^[A-ZÅÄÖ][a-zåäöé]+$")
A_NAME = "namn"
NOT_A_PERSON = "befattning eller enhet"
NEWLINE = chr(10)
# An inline image the mail client renders as a placeholder on its own line:
# the authority's logo, not its words.
IMAGE_LINE = re.compile(r"^\[(?:cid:)?[^\]]*\]$", re.MULTILINE)
NOT_A_NAME = (
    "Länsstyrelsen",
    "Kammarrätten",
    "Jordbruksverket",
    "Enheten",
    "Enhet",
    "Avdelningen",
    "Avdelning",
    "Diarium",
    "Diariet",
    "Central",
    "Säker",
    "Arkivet",
    "Arkivfunktionen",
    "Registrator",
    "Registraturen",
    "Webbplats",
    "Besöksadress",
    "Postadress",
    "Telefon",
    "Växel",
    "Djurvälfärdsenheten",
)


def swedish_time(stamp: str) -> tuple[str, str]:
    """The header's UTC stamp as a Swedish date and clock time."""
    utc = datetime.fromisoformat(stamp.replace("Z", "+00:00"))
    if not CEST[0] <= utc <= CEST[1]:
        raise SystemExit(
            f"{stamp} ligger utanfor CEST-fonstret; regeln maste skrivas om"
        )
    local = utc + SWEDISH_OFFSET
    return local.date().isoformat(), local.time().isoformat()


def load_judgements() -> dict[str, str]:
    """How a one-word signature was judged, per message id."""
    if not SIGNATURES.exists():
        return {}
    judged = {}
    for line in SIGNATURES.read_text("utf-8").splitlines():
        if line:
            row = json.loads(line)
            judged[row["meddelande"]] = row["signaturen"]
    return judged


def strip_signature(
    text: str, judgement: str | None = None, message: str = ""
) -> tuple[str, bool]:
    """The letter without a signature that names a person, and whether one was cut.

    The greeting itself is kept, since it is the authority's own word; what goes
    is everything after it when the next line is a person's name. A one-word
    signature is cut only where the judgement says it is a name.
    """
    for found in GREETING.finditer(text):
        after = text[found.end() :].lstrip(NEWLINE)
        first = after.split(NEWLINE, 1)[0].strip() if after else ""
        if first.startswith(NOT_A_NAME):
            continue
        if NAME_LINE.match(first):
            return text[: found.end()].rstrip(), True
        if ONE_WORD.match(first):
            if judgement is None:
                raise SystemExit(
                    f"{message}: signaturens forsta rad ar ett enda ord och "
                    f"saknar bedomning. Skriv en rad i {SIGNATURES.name} med "
                    f'signaturen satt till "{A_NAME}" eller "{NOT_A_PERSON}"'
                )
            if judgement == A_NAME:
                return text[: found.end()].rstrip(), True
    return text, False


def strip_history(text: str) -> tuple[str, list[str]]:
    """The letter's own text, and what was cut away under it.

    Two different things sit under a letter: the quoted history, and the file
    list the Filskick service writes with its download link. They were reported
    under one label until 8 October 2026, which said quoted history about a
    message that had none.
    """
    cut = len(text)
    taken = []
    for pattern in HISTORY:
        found = pattern.search(text)
        if found and found.start() < cut:
            cut = found.start()
            taken = ["den citerade historiken under meddelandet"]
    found = FILE_LIST.search(text)
    if found and found.start() < cut:
        cut = found.start()
        taken = ["filskicktjänstens förteckning över filerna och dess länk"]
    return text[:cut].rstrip(), taken


def normalise(
    text: str, judgement: str | None = None, message: str = ""
) -> tuple[str, list[str]]:
    """The text as the register carries it, and what was taken out of it."""
    taken = []
    body, under = strip_history(text)
    taken.extend(under)
    body, had_signature = strip_signature(body, judgement, message)
    if had_signature:
        taken.append(
            "signaturblocket med tjänstemannens namn och det som följer det "
            "enligt ADR-0018"
        )
    if LINK_TARGET.search(body) or MARKDOWN_LINK.search(body):
        taken.append("länkmålen bakom texten")
        body = LINK_TARGET.sub("", body)
        body = MARKDOWN_LINK.sub("\\1", body)
    if IMAGE_LINE.search(body):
        taken.append("myndighetens bildsignatur")
        body = IMAGE_LINE.sub("", body)
    body = "\n".join(line.rstrip() for line in body.splitlines())
    # Removing a line leaves the blank lines that framed it; a letter never
    # has three breaks in a row, so they collapse to one blank line.
    body = re.sub(NEWLINE + "{3,}", NEWLINE * 2, body)
    return body.strip(), taken


def digest(path: Path) -> str:
    """The file's sha256, so the manifest can be checked against it."""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    """Write the manifest for every saved raw reply, and report the state."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="report without writing")
    args = parser.parse_args()

    if not RAW.exists():
        print(f"{RAW} finns inte an; inga rasvar sparade")
        return 0

    judged = load_judgements()
    rows = []
    for path in sorted(RAW.glob("*.json")):
        raw = json.loads(path.read_text("utf-8"))
        datum, klockslag = swedish_time(raw["date"])
        body, taken = normalise(
            raw.get("plaintextBody") or "", judged.get(raw["id"]), raw["id"]
        )
        rows.append(
            {
                "meddelande": raw["id"],
                "datum": datum,
                "klockslag": klockslag,
                "storlek": raw["sizeEstimate"],
                "sha256": digest(path),
                "tecken": len(body),
                "utelamnat_mekaniskt": taken,
            }
        )

    if args.check:
        print(f"{len(rows)} rasvar sparade")
        for row in rows:
            print(
                f"  {row['meddelande']} {row['datum']} "
                f"{row['klockslag']} {row['tecken']} tecken"
            )
        return 0

    body = "\n".join(json.dumps(row, ensure_ascii=False) for row in rows)
    MANIFEST.write_bytes((body + "\n").encode("utf-8") if rows else b"")
    print(f"{len(rows)} rader i {MANIFEST.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
