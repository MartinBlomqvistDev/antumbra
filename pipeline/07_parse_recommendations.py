"""Parse recommendations and their cross-references out of the reports.

Step 07 of the pipeline; run 03_download_reports.py first. Each audit report
ends in a numbered list of recommendations, and from the late 2000s onwards
each recommendation names the conclusion it rests on and the findings behind
that conclusion. Those lines are the citation graph in text form.

The parser is deliberately literal. It reads the recommendations section,
splits it on numbering that actually counts up, and records the cross
references only where the document states them. A report that says it makes
no recommendation is recorded as exactly that, so an honest zero is never
confused with a failure to parse.

Writes data/dgsante_recommendations.jsonl, one row per recommendation, and
data/dgsante_report_parse.jsonl, one row per report with the outcome.

Usage:
    python pipeline/07_parse_recommendations.py
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "data" / "dgsante_manifest.jsonl"
OUT_RECS = ROOT / "data" / "dgsante_recommendations.jsonl"
OUT_REPORTS = ROOT / "data" / "dgsante_report_parse.jsonl"

# The heading that opens the closing section. Its number varies by era: the
# older reports run to 9, the modern ones to 8, so the number is not pinned.
# The table of contents carries the same words followed by dot leaders and a
# page number, so a heading may not contain dots or digits after its own
# number; without that the parser reads the contents page as the section.
HEADING = re.compile(
    r"^[ \t\f]*\d{1,2}[.\s)]*\s*RECOMMENDATIONS?\b[^\n.\d]*$", re.M | re.I
)
HEADING_LOOSE = re.compile(
    r"^[ \t\f]*\d{1,2}[.\s)]*\s*RECOMMENDATIONS?\b.*$", re.M | re.I
)

# An audit that found nothing worth recommending says so in plain words. This
# is a result, not a parse failure, and the two must never be merged.
NO_RECOMMENDATION = re.compile(
    r"does not (?:make|contain) any recommendation"
    r"|no recommendations? (?:are|were|is) made"
    r"|there are no recommendations",
    re.I,
)

# Where the sections after the recommendations begin, used to stop reading.
TAIL = re.compile(
    r"^\s*(?:ANNEX\b|APPENDIX\b|\d{1,2}[.\s)]*\s*ANNEX\b"
    r"|Legal Reference\b|TABLE OF CONTENTS\b"
    r"|The competent authority.{0,3}s response to the recommendations)",
    re.M | re.I,
)

# A recommendation opens with its own number at the start of a line. The
# number is written as "1", "1.", "1)" or "(1)" depending on the era, and in
# the two-column layouts it sits alone on its line with the text beneath it.
# What follows must read like the start of a sentence: page numbers, table
# cells and footnote markers also begin a line with a digit, and without this
# they split a recommendation in two.
ITEM = re.compile(r"^[ \t\f]*\(?(\d{1,2})[).]?[ \t]*(?=\n[ \t\f]*[A-Z(]|[A-Z(])", re.M)

# A recommendation carries at least this many letters. Anything shorter is a
# stray number that happened to fall in sequence. The bar is deliberately low:
# the requirement that a sentence follows the number does most of the work,
# and a higher bar was found to drop genuine one-line recommendations.
MIN_ITEM_LETTERS = 40

# No recommendations section runs longer than this. Where the closing tail is
# not recognised the cap stops the parser from swallowing the whole document.
MAX_SECTION_CHARS = 25_000

# The reference lists are written as "31", "17 and 18", "6, 42" and also as
# ranges: "29-31, 50 and 71". The hyphen has to be inside the captured class
# or the list is silently cut short at the first range, which loses edges of
# the graph with nothing to show that anything went missing.
# The repeated table header, which lands inside an item when the table runs
# over a page. The number sign is written "No.", "N°." or "Nº." depending on
# the report, and matching only the first form left the other two in the text:
# "...to verify the 17 N°. Recommendation 2. 3. effectiveness of...".
NOISE = re.compile(r"\s*\d{0,3}\s*N\S{0,3}\s+Recommendation\s*(?:\d{1,2}\.\s*)*", re.I)

# Many reports lay the recommendations out as a two-column table whose left
# column holds nothing but the numbers. Across a page break the layout engine
# emits the numbers of the next page in a run of their own, separated from the
# text they belong to, and reading the section line by line then finds one
# recommendation where there are five. The action plans, which restate each
# recommendation, showed this on 134 reports.
TABLE_HEADER = re.compile(
    r"^[ \t\f]*N\S{0,3}[ \t]{2,}(Recommendation)[ \t]*$", re.M | re.I
)

# A page number left behind between the rows of such a table.
PAGE_NUMBER = re.compile(r"^[ \t\f]*\d{1,3}[ \t\f]*$", re.M)

MIN_BLOCK_LETTERS = 20

# No report numbers its paragraphs beyond this. A reference above it comes
# from a typo or a doubled digit in the source: one report cites "conclusions
# 35 and 5050". Such a number is dropped rather than admitted to the graph,
# and the row is flagged so the loss is visible instead of silent.
MAX_PARAGRAPH_REFERENCE = 300

# A block holding nothing but the cross-reference line belongs to the
# recommendation above it. Counted on its own it becomes a recommendation
# whose text is "Recommendation based on conclusion 84" and whose actual
# wording has been dropped.
REFERENCE_ONLY = re.compile(
    r"^\W*(?:the\s+)?recommendations?\s+(?:is\s+)?based on|^\W*associated finding",
    re.I,
)

DASHES = "-" + chr(0x2013)  # hyphen-minus and en dash; the reports use both
RANGE = re.compile(rf"(\d{{1,3}})\s*[{DASHES}]\s*(\d{{1,3}})|(\d{{1,3}})")

# The reference list has to be matched as a list, not as a run of characters
# that happen to be digits and separators. A character class would keep
# eating: past the full stop, through the next line of a numbered table, and
# into legal citations such as "2017/625", inventing edges out of article
# numbers. This grammar stops at the first token that is not part of a list.
_NUM = r"\d{1,3}"
_SPAN = rf"{_NUM}(?:\s*[{DASHES}]\s*{_NUM})?"
_SEP = r"\s*(?:,\s*and|,|and|&)\s*"
LIST = rf"{_SPAN}(?:{_SEP}{_SPAN})*"

CONCLUSIONS = re.compile(
    rf"based on conclusions?\s*(?:Nos?\b\.?)?\s*:?\s*({LIST})", re.I
)
FINDINGS = re.compile(rf"associated findings?\s*(?:Nos?\b\.?)?\s*:?\s*({LIST})", re.I)
LEGAL_BASIS = re.compile(r"legal basis\s*:?\s*(.+?)(?:\n\s*\n|$)", re.I | re.S)


def report_text(path: Path) -> str:
    """Extract the text layer of one report."""
    done = subprocess.run(
        ["pdftotext", "-layout", "-q", str(path), "-"],
        capture_output=True,
        text=True,
        errors="replace",
        timeout=180,
        check=False,
    )
    return done.stdout


def recommendations_section(text: str) -> str | None:
    """Return the text after the last recommendations heading.

    The heading also appears in the table of contents, so the last match is
    taken; the table of contents always precedes the section itself.
    """
    matches = list(HEADING.finditer(text)) or list(HEADING_LOOSE.finditer(text))
    if not matches:
        return None
    section = text[matches[-1].end() :]
    tail = TAIL.search(section)
    if tail:
        section = section[: tail.start()]
    return section[:MAX_SECTION_CHARS]


def numbers(blob: str) -> list[int]:
    """Read paragraph numbers, expanding ranges.

    Args:
        blob: A reference list such as "19 and 46", "6, 42" or "29-31, 50".

    Returns:
        Every number named, with ranges written out. A range running
        backwards or absurdly long is treated as two separate numbers,
        since it is more likely two references run together than a range.
    """
    found: list[int] = []
    for match in RANGE.finditer(blob):
        low, high, single = match.groups()
        if single is not None:
            found.append(int(single))
            continue
        start, stop = int(low), int(high)
        if 0 <= stop - start <= 30:
            found.extend(range(start, stop + 1))
        else:
            found.extend((start, stop))
    return found


def in_range(number: int) -> bool:
    """Whether a cited number can be a paragraph of a report."""
    return 1 <= number <= MAX_PARAGRAPH_REFERENCE


def split_table(section: str) -> list[tuple[int, str]]:
    """Read a two-column recommendations table, or return nothing.

    The left column carries the numbers and the right the text. They are read
    apart and then paired in order. A recommendation broken over a page ends
    without a full stop, and its continuation is joined back on; where the
    number count and the text count still disagree the table is left alone
    rather than paired on a guess.

    Args:
        section: Text of the recommendations section.

    Returns:
        One (number, text) pair per row, or an empty list.
    """
    header = TABLE_HEADER.search(section)
    if header is None:
        return []
    body = section[header.end() :]
    body = TABLE_HEADER.sub("", body)
    body = PAGE_NUMBER.sub("", body)

    # Where the text column starts. The header's spacing does not always line
    # up with the body, and the body's indentation is not always uniform, so
    # both are offered and the one that pairs consistently is taken.
    indents = [
        len(line) - len(line.lstrip())
        for line in body.splitlines()
        if len(line.strip()) > 30 and not re.match(r"^\s*\d{1,2}\.", line)
    ]
    candidates = []
    if indents:
        candidates.append(max(set(indents), key=indents.count))
    candidates.append(header.group(0).lower().index("recommendation"))

    for gutter in dict.fromkeys(c for c in candidates if c >= 2):
        paired = pair_columns(body, gutter)
        if paired:
            return paired
    return []


def pair_columns(body: str, gutter: int) -> list[tuple[int, str]]:
    """Pair the numbers of the left column with the texts of the right.

    Args:
        body: The table below its header.
        gutter: Column where the text column starts.

    Returns:
        One (number, text) pair per row, or an empty list when the two
        columns do not line up and pairing would be a guess.
    """
    numbers_seen: list[int] = []
    right_lines: list[str] = []
    for line in body.splitlines():
        for found in re.findall(r"\b(\d{1,2})\s*\.", line[:gutter]):
            value = int(found)
            if not numbers_seen or value == numbers_seen[-1] + 1:
                numbers_seen.append(value)
        right_lines.append(line[gutter:])

    blocks: list[str] = []
    for chunk in re.split(r"\n\s*\n", "\n".join(right_lines)):
        text = " ".join(chunk.split())
        if sum(c.isalpha() for c in text) < MIN_BLOCK_LETTERS:
            continue
        # A recommendation broken over a page ends mid-sentence; its
        # continuation is joined back on rather than counted as a new one.
        # The same goes for a block that is only a cross-reference line.
        if blocks and (
            REFERENCE_ONLY.match(text)
            or not blocks[-1].rstrip().endswith((".", ":", ";"))
        ):
            blocks[-1] = f"{blocks[-1]} {text}"
        else:
            blocks.append(text)

    if not numbers_seen or numbers_seen[0] != 1 or len(numbers_seen) != len(blocks):
        return []
    return list(zip(numbers_seen, blocks, strict=True))


def split_items(section: str) -> list[tuple[int, str]]:
    """Split a section into numbered recommendations.

    Only numbering that counts up from one is accepted. Extraction of a
    two-column layout scatters stray numbers through the text, and requiring
    the sequence to increase keeps those from splitting a recommendation in
    half.

    Args:
        section: Text of the recommendations section.

    Returns:
        One (number, text) pair per recommendation, in document order.
    """
    marks = [(m.start(), m.end(), int(m.group(1))) for m in ITEM.finditer(section)]
    kept: list[tuple[int, int, int]] = []
    expected = 1
    for index, (start, end, value) in enumerate(marks):
        if value != expected:
            continue
        stop = len(section)
        for later_start, _, later_value in marks[index + 1 :]:
            if later_value == expected + 1:
                stop = later_start
                break
        if sum(c.isalpha() for c in section[end:stop]) < MIN_ITEM_LETTERS:
            continue
        kept.append((start, end, value))
        expected += 1
    items: list[tuple[int, str]] = []
    for index, (_, end, value) in enumerate(kept):
        stop = kept[index + 1][0] if index + 1 < len(kept) else len(section)
        body = re.sub(r"[ \t]*\n[ \t]*", "\n", section[end:stop]).strip()
        body = re.sub(r"\n{2,}", "\n", NOISE.sub(" ", body))
        if body:
            items.append((value, body))
    return items


def parse_report(record: dict) -> tuple[dict, list[dict]]:
    """Parse one report into its outcome and its recommendations.

    Args:
        record: A manifest row for an English report.

    Returns:
        The per-report outcome and one row per recommendation found.
    """
    base = {
        "ref": record["ref"],
        "country": record["country"],
        "path": record["path"],
    }
    text = report_text(ROOT / record["path"])
    if len(text.strip()) < 500:
        return {**base, "outcome": "no_text_layer", "recommendations": 0}, []

    section = recommendations_section(text)
    if section is None:
        return {**base, "outcome": "no_section_found", "recommendations": 0}, []
    if NO_RECOMMENDATION.search(section[:2000]):
        return {**base, "outcome": "states_no_recommendation", "recommendations": 0}, []

    # Whether the section states cross references at all, measured on the raw
    # text. Recall on these reports is what matters: they are the ones that
    # carry the citation graph, and a parser that quietly dropped them would
    # look fine on the totals.
    graph = bool(CONCLUSIONS.search(section))

    items = split_table(section)
    method = "two_column_table" if items else "numbered_lines"
    if not items:
        items = split_items(section)
    if not items:
        return (
            {
                **base,
                "outcome": "section_without_items",
                "recommendations": 0,
                "section_states_links": graph,
            },
            [],
        )

    rows = []
    for number, body in items:
        conclusion_match = CONCLUSIONS.search(body)
        finding_match = FINDINGS.search(body)
        legal_match = LEGAL_BASIS.search(body)
        cited_conclusions = (
            numbers(conclusion_match.group(1)) if conclusion_match else []
        )
        cited_findings = numbers(finding_match.group(1)) if finding_match else []
        kept_conclusions = [n for n in cited_conclusions if in_range(n)]
        kept_findings = [n for n in cited_findings if in_range(n)]
        dropped = (len(cited_conclusions) - len(kept_conclusions)) + (
            len(cited_findings) - len(kept_findings)
        )
        rows.append(
            {
                **base,
                "number": number,
                "text": " ".join(body.split()),
                "legal_basis": (
                    " ".join(legal_match.group(1).split())[:400]
                    if legal_match
                    else None
                ),
                "based_on_conclusions": kept_conclusions,
                "associated_findings": kept_findings,
                "references_out_of_range": dropped,
                # Two-column layouts sometimes run several recommendations
                # into one block. Where that happened the links belong to the
                # first of them; the flag says so rather than hiding it.
                "multiple_reference_blocks": len(CONCLUSIONS.findall(body)) > 1,
                "parse_method": method,
            }
        )
    linked = sum(1 for r in rows if r["based_on_conclusions"])
    return (
        {
            **base,
            "outcome": "parsed",
            "recommendations": len(rows),
            "with_conclusion_links": linked,
            "section_states_links": graph,
        },
        rows,
    )


def main() -> int:
    """Parse every English report and write recommendations and outcomes."""
    manifest = [
        json.loads(line)
        for line in MANIFEST.read_text(encoding="utf-8").splitlines()
        if line
    ]
    reports = [r for r in manifest if r["kind"] == "report"]
    outcomes: list[dict] = []
    recommendations: list[dict] = []
    for index, record in enumerate(reports, start=1):
        outcome, rows = parse_report(record)
        outcomes.append(outcome)
        recommendations.extend(rows)
        if index % 500 == 0:
            print(f"{index}/{len(reports)} parsed", flush=True)

    for path, rows in ((OUT_REPORTS, outcomes), (OUT_RECS, recommendations)):
        with open(path, "w", encoding="utf-8", newline="\n") as fh:
            for row in rows:
                fh.write(json.dumps(row, ensure_ascii=False) + "\n")

    counts: dict[str, int] = {}
    for outcome in outcomes:
        counts[outcome["outcome"]] = counts.get(outcome["outcome"], 0) + 1
    linked = sum(1 for r in recommendations if r["based_on_conclusions"])
    print(f"{len(reports)} reports, {len(recommendations)} recommendations")
    for name, count in sorted(counts.items(), key=lambda kv: -kv[1]):
        print(f"  {name}: {count}")
    print(f"recommendations citing a conclusion: {linked}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
