"""Render the P12 packets as the letters that are actually sent.

Step 40 of the pipeline. Step 36 writes one markdown packet per authority,
which is the repository's record of what each one was told. A letter in this
correspondence has gone as the body of an e-mail every time, from the request
of 3 August 2026 to the day 40 letters of 28 September, and markdown headings,
pipe tables and asterisks are not something a registrator can paste into an
ärendesystem. This step turns each packet into the plain text form those
letters use: the address line the first letter used, "Hej!", the body wrapped
at 72 characters, and the sign-off.

Nothing is written here that is not in the packet. The step reformats, and adds
only the address block and the sender's own e-mail address, so a sentence can
never exist in the letter without existing in the record, and the two cannot
drift apart.

Run step 36 first, on the day the letters go out, so that the reply date they
carry is three weeks from that day.
"""

from __future__ import annotations

import re
import sys
import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from recipients import address  # noqa: E402

PACKETS = ROOT / "data" / "p12"
OUT = PACKETS / "brev"
WIDTH = 72

# Hyphens are not break points here. Länsstyrelsen i Södermanland wrote the
# period as "2024-01-01---2025-12-31", and a line broken inside it would split
# a date range in a quotation that is supposed to be verbatim.
WRAP = textwrap.TextWrapper(width=WIDTH, break_on_hyphens=False)
QUOTE = textwrap.TextWrapper(
    width=WIDTH,
    break_on_hyphens=False,
    initial_indent="  ",
    subsequent_indent="  ",
)

# The same screen step 36 and step 33 run, for the same reason: a letter that
# carries an official's name, a personal identity number, a telephone number or
# an internal file name is not sent, and the step refuses rather than warns.
FORBIDDEN = {
    "e-postadress": re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-z]{2,}"),
    "personnummer": re.compile(r"\b(?:19|20)\d{6}[-+]\d{4}\b"),
    "telefonnummer": re.compile(r"\b0\d{1,3}[-\s]\d{2,3}\s?\d{2}\s?\d{2}\b"),
    "filnamn": re.compile(r"\.(pdf|xlsx|docx|jsonl)\b", re.IGNORECASE),
}
# The sender's own address is the single exception, and it is the line the
# letter is signed with.
SENDER = "cm.blomqvist@gmail.com"

# The sign-off is two lines and stays two lines. Wrapped as prose it comes out
# as "Med vänliga hälsningar, Martin Blomqvist" on one line, which is not how
# any other letter in this correspondence ends.
SIGNOFF = ("Med vänliga hälsningar,", "Martin Blomqvist")

TITLE = re.compile(r"^#\s+Resultat som rör (.+)$")
HEADING = re.compile(r"^#{2,3}\s+(.*)$")
BOLD = re.compile(r"\*\*(.+?)\*\*")
CODE = re.compile(r"`([^`]+)`")
COMMENT = re.compile(r"^<!--.*-->$")
TABLE_RULE = re.compile(r"^\|[\s|:-]+\|$")


def plain(text: str) -> str:
    """One line of markdown as the letter writes it."""
    return CODE.sub(r"\1", BOLD.sub(r"\1", text)).strip()


def columns(rows: list[list[str]]) -> list[str]:
    """A pipe table as aligned columns, which plain text can carry."""
    widths = [max(len(row[i]) for row in rows) for i in range(len(rows[0]))]
    out = []
    for row in rows:
        out.append("  ".join(c.ljust(widths[i]) for i, c in enumerate(row)).rstrip())
    return out


def letter(markdown: str) -> str:
    """One packet as the letter that is sent."""
    authority = None
    body: list[str] = []
    paragraph: list[str] = []
    table: list[list[str]] = []
    quote: list[str] = []

    def flush() -> None:
        if paragraph:
            body.extend(WRAP.wrap(" ".join(paragraph)))
            body.append("")
            paragraph.clear()
        if table:
            body.extend(columns(table))
            body.append("")
            table.clear()
        if quote:
            body.extend(QUOTE.wrap(" ".join(quote)))
            body.append("")
            quote.clear()

    for raw in markdown.split("\n"):
        line = raw.rstrip()
        found = TITLE.match(line)
        if found:
            authority = found.group(1)
            continue
        if COMMENT.match(line) or TABLE_RULE.match(line):
            continue
        if not line:
            flush()
            continue
        if line.startswith("|"):
            cells = [plain(cell) for cell in line.strip("|").split("|")]
            if not table:
                flush()
            table.append(cells)
            continue
        if line.startswith(">"):
            if not quote:
                flush()
            quote.append(plain(line.lstrip(">")))
            continue
        if line in SIGNOFF:
            if line == SIGNOFF[0]:
                flush()
            body.append(line)
            continue
        found = HEADING.match(line)
        if found:
            flush()
            body.append(plain(found.group(1)))
            body.append("")
            continue
        if table or quote:
            flush()
        paragraph.append(plain(line))
    flush()

    if authority is None:
        raise SystemExit("paketet saknar rubrikraden med myndighetens namn")
    while body and not body[-1]:
        body.pop()
    return "\n".join([f"Till {address(authority)}", "", "Hej!", "", *body, SENDER, ""])


# Markdown's own marks are not words. Comparing without stripping them made
# every bolded figure look invented, because "**-80,0" is not "-80,0".
MARKUP = str.maketrans("", "", "*`|>#")


def words(text: str) -> set[str]:
    """The text as a bag of words, with markdown's marks taken out."""
    return set(text.translate(MARKUP).split())


def invented(packet: str, text: str) -> set[str]:
    """Words the letter carries that its packet does not.

    The letter is a reformatting, so the only words it may add are the ones
    this step writes itself: the address line, the greeting and the sender's
    address. The address line differs from the packet's own name for the
    authority, because the first letter of 3 August 2026 wrote "Länsstyrelsen
    i Gävleborgs län" where the protocol log says "Länsstyrelsen i Gävleborg",
    so those words are allowed and nothing else is.
    """
    head, _, rest = text.partition("Hej!")
    allowed = set(head.split()) | {"Hej!", SENDER}
    return words(rest) - words(packet) - allowed


def main() -> int:
    """Write one letter per packet, refusing to write when a check fails."""
    packets = sorted(p for p in PACKETS.glob("*.md"))
    if not packets:
        print("inga paket i data/p12; kör steg 36 först")
        return 1
    source = {path.stem: path.read_text("utf-8") for path in packets}
    letters = {slug: letter(text) for slug, text in source.items()}

    added = {
        slug: invented(source[slug], text)
        for slug, text in letters.items()
        if invented(source[slug], text)
    }
    if added:
        for slug, words in list(added.items())[:10]:
            print(f"  {slug}: ord som inte står i paketet: {sorted(words)[:8]}")
        print("inget skrivet")
        return 1

    offenders = []
    for slug, text in letters.items():
        for label, pattern in FORBIDDEN.items():
            for found in pattern.finditer(text):
                if found.group(0) == SENDER:
                    continue
                offenders.append(f"{slug}: {label} ({found.group(0)!r})")
    leftovers = [slug for slug, text in letters.items() if "|" in text or "**" in text]
    if offenders or leftovers:
        for offender in offenders[:20]:
            print(f"  {offender}")
        for slug in leftovers:
            print(f"  {slug}: markdown kvar i brevet")
        print("inget skrivet")
        return 1

    OUT.mkdir(parents=True, exist_ok=True)
    for slug, text in letters.items():
        (OUT / f"{slug}.txt").write_text(text, encoding="utf-8", newline="\n")
    longest = max(letters.values(), key=len)
    print(f"{len(letters)} brev skrivna till {OUT.relative_to(ROOT).as_posix()}")
    print(f"  längsta brevet: {len(longest.split())} ord")
    print("  screeningen passerad: " + ", ".join(FORBIDDEN))
    print("  breven går som brödtext, som svar i den befintliga tråden")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
