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
# The mail client also renders a target without its scheme, as <www.…>, which
# the courts' signatures use. It is the same thing and goes the same way.
LINK_TARGET = re.compile(r"<(?:https?://|mailto:|www\.)[^>]*>")
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
    # A P12 reply that pastes the packet back without any header of its own.
    # Added 22 October 2026, when Norrbotten answered and Outlook put my whole
    # letter under the reply as plain text. The anchor is the letter's own first
    # line, written by step 40 and identical in all 22 packets, so it matches my
    # text and nothing an authority wrote.
    re.compile(r"^Till (Länsstyrelsen i |Jordbruksverket)", re.MULTILINE),
)
# The courts' Säker e-post notice carries a one-time link with a token that
# opens the message as the addressee. It is a personal access link, not a
# published address, so it is taken out and the omission is declared. The link
# expires 30 days after the message, and the register says so rather than
# leaving a credential standing in a published file.
SECURE_LINK = re.compile(r"^https://securemail\.domstol\.se/\S+$", re.MULTILINE)
# A line that was nothing but a link: a label and its target, or a target and a
# label and another target, and no other words. Stripping the targets alone
# would leave a dangling label such as "Central e-post" standing as if the
# authority had written it as a sentence. The register's hand-written rows cut
# those lines from the start, and from 8 October 2026 the step does the same, so
# the same standing autoreply is not carried in two shapes.
ONLY_LINK = re.compile(
    r"^[^<>]{0,70}<(?:https?://|mailto:)[^>]*>"
    r"(?:[^<>]{0,70}<(?:https?://|mailto:)[^>]*>)*$"
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
# A greeting with the signer on the same line, as in "Mvh <name>/Länsstyrelsen".
# The greeting is then not a line of its own, so the signature rule below never
# sees it, and the name would stay in the text. The line is cut whole, greeting
# included, and the omission is declared. The word Vänligen is deliberately not
# in the list: it opens a request in the authorities' own letters ("Vänligen
# återkoppla om det fungerar"), and cutting that would cut their words.
INLINE_SIGN = re.compile(
    r"^(?:Mvh|Med vänlig hälsning|Med vänliga hälsningar|Vänlig hälsning|"
    r"Vänliga hälsningar|Hälsningar)[ 	]+(\S.*)$",
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
# A rule of underscores or dashes between the greeting and the signer, which
# Västerbotten writes. It is not a line of words, so it is skipped before the
# signer's line is looked at, and it goes with the signature.
# The hyphen is written last in the class on purpose: next to another
# character it would open a range from the equals sign to an en dash, which
# once matched every letter,
# which cut four signatures that name nobody.
SEPARATOR = re.compile("^[_=" + chr(8211) + chr(8212) + r"\s" + chr(45) + "]+$")
A_NAME = "namn"
NOT_A_PERSON = "befattning eller enhet"
NEWLINE = chr(10)
# An inline image the mail client renders as a placeholder on its own line:
# the authority's logo, not its words.
IMAGE_LINE = re.compile(r"^\[(?:cid:)?[^\]]*\]$", re.MULTILINE)
NOT_A_NAME = (
    "Alla",
    "Arkivet",
    "Arkivfunktionen",
    "Avdelning",
    "Avdelningen",
    "Avgift",
    "Begär",
    "Beslut",
    "Besöksadress",
    "Bifogar",
    "Central",
    "Dessa",
    "Det",
    "Diariet",
    "Diarium",
    "Din",
    "Djurvälfärdsenheten",
    "Du",
    "Enhet",
    "Enheten",
    "Exempel",
    "Extra",
    "För",
    "Föreläggande",
    "Har",
    "Hej",
    "Här",
    "Information",
    "Jag",
    "Jordbruksverket",
    "Kammarrätten",
    "Länsstyrelsen",
    "Med",
    "Mer",
    "Normal",
    "När",
    "Observera",
    "Om",
    "Postadress",
    "Registrator",
    "Registraturen",
    "Sammanlagt",
    "Sidan",
    "Sveriges",
    "Säker",
    "Så",
    "Tack",
    "Telefon",
    "Vi",
    "Vill",
    "Vänliga",
    "Växel",
    "Webbplats",
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
    for found in INLINE_SIGN.finditer(text):
        # "Med vänliga hälsningar Länsstyrelsen i Jönköpings län" is the
        # authority signing itself, not a person, and it stays.
        rest = found.group(1).strip()
        if not rest.startswith(NOT_A_NAME):
            return text[: found.start()].rstrip(), True
    for found in GREETING.finditer(text):
        lines = text[found.end() :].lstrip(NEWLINE).split(NEWLINE)
        while lines and (not lines[0].strip() or SEPARATOR.match(lines[0])):
            lines.pop(0)
        first = lines[0].strip() if lines else ""
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
    # A signature with no greeting above it at all: the letter ends and the
    # signer's name stands on its own line. The invariant in tests/ fails any
    # row that carries a line of two capitalised words, so such a line can
    # never be published, and the step cuts from it rather than leaving the
    # omission to be noticed by hand.
    for line in text.split(NEWLINE):
        stripped = line.strip()
        if NAME_LINE.match(stripped) and not stripped.startswith(NOT_A_NAME):
            return text[: text.index(line)].rstrip(), True
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
    kept = [line for line in text.splitlines() if not ONLY_LINK.match(line.strip())]
    if len(kept) != len(text.splitlines()):
        taken.append("raderna som bara var länkar till myndighetens kontaktuppgifter")
    text = NEWLINE.join(kept)
    body, under = strip_history(text)
    taken.extend(under)
    body, had_signature = strip_signature(body, judgement, message)
    if had_signature:
        taken.append(
            "signaturblocket med tjänstemannens namn och det som följer det "
            "enligt ADR-0018"
        )
    if SECURE_LINK.search(body):
        taken.append(
            "engångslänken till domstolens tjänst Säker e-post, som är en "
            "personlig åtkomstlänk och inte en publicerad adress"
        )
        body = SECURE_LINK.sub("", body)
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
