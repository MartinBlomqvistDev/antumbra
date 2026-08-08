"""Parse the numbered paragraphs that the recommendations cite.

Step 08 of the pipeline; run 07_parse_recommendations.py first. Step 07 read
the edges of the citation graph, but they pointed at paragraph numbers with
nothing at the other end. This step reads the nodes: the numbered paragraphs
of the report, which run in one sequence through the whole document.

Findings and conclusions are not separated by section alone. Within section 5
the report groups them under sub-headings, and a heading that begins with
"Conclusion" turns the paragraphs beneath it into conclusions. Where the
document gives no such signal the paragraph is recorded as unlabelled rather
than assigned a kind it never claimed.

Writes data/dgsante_paragraphs.jsonl, one row per numbered paragraph, which
is large and stays out of the repository, and data/dgsante_graph.jsonl, one
row per citation edge with the cited paragraph beside it. The second file is
the closed chain and is small enough to review.

Usage:
    python pipeline/08_parse_paragraphs.py
"""

from __future__ import annotations

import bisect
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "data" / "dgsante_manifest.jsonl"
RECOMMENDATIONS = ROOT / "data" / "dgsante_recommendations.jsonl"
OUT = ROOT / "data" / "dgsante_paragraphs.jsonl"
OUT_GRAPH = ROOT / "data" / "dgsante_graph.jsonl"

# How much of a cited paragraph is carried into the committed graph. The full
# paragraph corpus is 66 MB and stays out of the repository; the graph holds
# the paragraphs the reports actually cite, which is the reviewable payload.
GRAPH_TEXT_CHARS = 700

# A numbered paragraph. Indentation varies with the layout, so it is not
# pinned; what is required is a capital opening, which keeps table cells,
# figures and legal article numbers out. The form feed is in the class
# because a page break puts one at the head of the line, and without it every
# heading and paragraph that opens a page is invisible to the parser.
PARAGRAPH = re.compile(r"^[ \t\f]{0,24}(\d{1,3})\.[ \t]+(?=[A-Z(\"'])", re.M)

# A top-level section heading, used to say which section a paragraph sits in.
SECTION = re.compile(
    r"^[ \t\f]{0,12}(\d{1,2})[.\s]{1,4}([A-Z][A-Z \-&/,']{4,60})[ \t]*$", re.M
)

# Section 5 is titled "FINDINGS AND CONCLUSIONS" and holds both, so the
# section name cannot say which a paragraph is. The reports separate them with
# their own headings: "Findings", "Conclusions on registration and listing".
# Only those two words are recognised. An earlier version accepted any
# indented capitalised line as a heading and collected legal citations
# instead, then labelled every paragraph in section 5 a finding by default,
# which the reports' own citations contradicted.
LABEL_HEADING = re.compile(
    r"^[ \t\f]{0,24}((?:overall[ \t]+)?(?:findings?|conclusions?)\b[^\n]{0,60})[ \t]*$",
    re.M | re.I,
)

# A numbered sub-section such as "5.1 COMPETENT AUTHORITIES". It carries no
# label itself, but it ends the reach of the previous findings or conclusions
# heading. Without it a "Conclusions on ..." heading kept labelling paragraphs
# in the sub-sections that followed, and the reports' own citations showed it.
SUBSECTION = re.compile(
    r"^[ \t\f]{0,16}\d{1,2}\.\d{1,2}\.?[ \t]+([A-Za-z][^\n]{3,70})[ \t]*$", re.M
)

CONCLUSION_WORD = re.compile(r"^\s*(?:overall\s+)?conclusions?\b", re.I)
FINDING_WORD = re.compile(r"^\s*findings?\b", re.I)

MIN_PARAGRAPH_LETTERS = 40

# Table of contents lines look exactly like numbered paragraphs once the dot
# leaders are ignored: "1. INTRODUCTION ......... 1". Left in, they consume the
# opening numbers of the sequence, and the real first paragraph then never
# matches, which truncated most reports to a handful of paragraphs.
DOT_LEADERS = re.compile(r"\.{4,}")

# How far the numbering may jump and still count as the same sequence. Text
# extraction loses the occasional paragraph at a page or column boundary, and
# demanding an unbroken run made one lost paragraph discard the whole rest of
# the report. The gap is small enough that unrelated numbering cannot slip in.
MAX_GAP = 3


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


def headings(text: str) -> list[tuple[int, str, str]]:
    """List section and sub-headings with the position where each starts.

    Args:
        text: Full report text.

    Returns:
        One (position, kind, title) triple per heading, in document order.
    """
    found = [(m.start(), "section", m.group(2).strip()) for m in SECTION.finditer(text)]
    found += [
        (m.start(), "label", m.group(1).strip()) for m in LABEL_HEADING.finditer(text)
    ]
    found += [
        (m.start(), "reset", m.group(1).strip()) for m in SUBSECTION.finditer(text)
    ]
    found.sort()
    return found


def context_at(marks: list[tuple[int, str, str]], position: int) -> tuple[str, str]:
    """Return the section and the labelling heading in force at a position."""
    section = ""
    label = ""
    for start, kind, title in marks:
        if start > position:
            break
        if kind == "section":
            section, label = title, ""
        elif kind == "reset":
            label = ""
        else:
            label = title
    return section, label


def split_paragraphs(
    text: str, boundaries: list[int] | None = None
) -> list[tuple[int, int, str]]:
    """Split a report into its numbered paragraphs.

    The numbering runs in one sequence through the document, so only numbers
    that continue the sequence are accepted. Without that rule the numbers
    inside tables and legal citations break paragraphs apart.

    Args:
        text: Full report text.
        boundaries: Positions of numbered section headings. A paragraph's
            body also ends at the first of these after it, so the next
            section's heading is not glued onto the paragraph's tail. Only
            the acceptance of paragraphs ignores them, deliberately: the
            cleanup must not change which paragraphs exist.

    Returns:
        One (position, number, body) triple per paragraph.
    """
    marks = []
    for match in PARAGRAPH.finditer(text):
        line_end = text.find("\n", match.end())
        line = text[match.start() : line_end if line_end != -1 else len(text)]
        if DOT_LEADERS.search(line):
            continue
        marks.append((match.start(), match.end(), int(match.group(1))))

    # The document may number more than one sequence, and the body sequence is
    # the long one. Every place a "1." occurs is tried as a starting point and
    # the run that yields the most paragraphs wins, so a stray early sequence
    # cannot cut the report short.
    best: list[tuple[int, int, int]] = []
    for first in [i for i, m in enumerate(marks) if m[2] == 1] or [0]:
        kept: list[tuple[int, int, int]] = []
        last = 0
        for index in range(first, len(marks)):
            start, end, value = marks[index]
            if not last < value <= last + MAX_GAP:
                continue
            stop = marks[index + 1][0] if index + 1 < len(marks) else len(text)
            if sum(c.isalpha() for c in text[end:stop]) < MIN_PARAGRAPH_LETTERS:
                continue
            kept.append((start, end, value))
            last = value
        if len(kept) > len(best):
            best = kept
    kept = best

    cuts = sorted(boundaries or [])
    out: list[tuple[int, int, str]] = []
    for index, (start, end, value) in enumerate(kept):
        stop = kept[index + 1][0] if index + 1 < len(kept) else len(text)
        heading = bisect.bisect_right(cuts, end)
        if heading < len(cuts) and cuts[heading] < stop:
            trimmed = " ".join(text[end : cuts[heading]].split())
            body = trimmed or " ".join(text[end:stop].split())
        else:
            body = " ".join(text[end:stop].split())
        if body:
            out.append((start, value, body))
    return out


def kind_of(section: str, label: str) -> str:
    """Name what a paragraph is, using only what a heading states.

    Args:
        section: The section heading in force.
        label: The nearest preceding findings or conclusions heading.

    Returns:
        "finding", "conclusion", or "unlabelled" where no heading says.
        Section 5 is deliberately not read as findings: it holds both, and
        guessing there is what the reports' own citations disagreed with.
    """
    if CONCLUSION_WORD.search(label):
        return "conclusion"
    if FINDING_WORD.search(label):
        return "finding"
    if CONCLUSION_WORD.search(section):
        return "conclusion"
    if FINDING_WORD.search(section) and "CONCLUSION" not in section.upper():
        return "finding"
    return "unlabelled"


def parse_report(record: dict) -> list[dict]:
    """Parse one report into its numbered paragraphs."""
    text = report_text(ROOT / record["path"])
    if len(text.strip()) < 500:
        return []
    marks = headings(text)
    # Only the numbered headings bound paragraph bodies. The free-standing
    # findings/conclusions lines stay context labels: they are matched
    # case-insensitively and a wrapped body line can look like one, so using
    # them as hard cuts would truncate real paragraphs.
    numbered = sorted(
        {m.start() for m in SECTION.finditer(text)}
        | {m.start() for m in SUBSECTION.finditer(text)}
    )
    rows = []
    for position, number, body in split_paragraphs(text, numbered):
        section, label = context_at(marks, position)
        rows.append(
            {
                "ref": record["ref"],
                "country": record["country"],
                "path": record["path"],
                "number": number,
                "section": section,
                "label_heading": label,
                "kind": kind_of(section, label),
                "text": body[:4000],
            }
        )
    return rows


def main() -> int:
    """Parse every report and report how many cited numbers resolve."""
    manifest = [
        json.loads(line)
        for line in MANIFEST.read_text(encoding="utf-8").splitlines()
        if line
    ]
    reports = [r for r in manifest if r["kind"] == "report"]

    paragraphs: list[dict] = []
    for index, record in enumerate(reports, start=1):
        paragraphs.extend(parse_report(record))
        if index % 500 == 0:
            print(f"{index}/{len(reports)} parsed", flush=True)

    with open(OUT, "w", encoding="utf-8", newline="\n") as fh:
        for row in paragraphs:
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")

    by_number: dict[tuple[str, int], dict] = {
        (row["path"], row["number"]): row for row in paragraphs
    }

    cited = resolved = 0
    edges: list[dict] = []
    for line in RECOMMENDATIONS.read_text(encoding="utf-8").splitlines():
        if not line:
            continue
        row = json.loads(line)
        for edge, cited_numbers in (
            ("conclusion", row["based_on_conclusions"]),
            ("finding", row["associated_findings"]),
        ):
            for number in cited_numbers:
                cited += 1
                target = by_number.get((row["path"], number))
                resolved += target is not None
                edges.append(
                    {
                        "ref": row["ref"],
                        "country": row["country"],
                        "path": row["path"],
                        "recommendation": row["number"],
                        "cites": edge,
                        "paragraph": number,
                        "resolved": target is not None,
                        # The kind read from the paragraph's own heading, kept
                        # beside the kind the citation implies. Where the two
                        # disagree the disagreement is visible instead of
                        # being resolved in favour of either.
                        "paragraph_kind": target["kind"] if target else None,
                        "label_heading": target["label_heading"] if target else None,
                        "paragraph_text": (
                            target["text"][:GRAPH_TEXT_CHARS] if target else None
                        ),
                    }
                )

    with open(OUT_GRAPH, "w", encoding="utf-8", newline="\n") as fh:
        for row in edges:
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")

    kinds: dict[str, int] = {}
    for row in paragraphs:
        kinds[row["kind"]] = kinds.get(row["kind"], 0) + 1
    covered = {row["path"] for row in paragraphs}
    print(f"{len(paragraphs)} paragraphs from {len(covered)} reports")
    for name, count in sorted(kinds.items(), key=lambda kv: -kv[1]):
        print(f"  {name}: {count}")
    share = resolved / cited if cited else 0.0
    print(f"cited paragraph numbers resolving to a paragraph: {resolved}/{cited}")
    print(f"  that is {share:.0%}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
