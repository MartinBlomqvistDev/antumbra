"""Link the action plans to the recommendations they answer.

Step 09 of the pipeline; run 07_parse_recommendations.py first. A member
state answers an audit with an action plan laid out as a table: the
recommendation number, the recommendation as the member state restates it,
and the action it undertakes. Reading that table closes the chain from
finding to conclusion to recommendation to commitment.

The restated recommendation is what makes the link checkable. It is compared
with the recommendation parsed from the report itself, so a link is not
asserted on a shared number alone; where the two texts disagree the record
says so instead of hiding it.

Writes data/dgsante_action_plans.jsonl, one row per answered recommendation.

Usage:
    python pipeline/09_link_action_plans.py
"""

from __future__ import annotations

import difflib
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "data" / "dgsante_manifest.jsonl"
RECOMMENDATIONS = ROOT / "data" / "dgsante_recommendations.jsonl"
OUT = ROOT / "data" / "dgsante_action_plans.jsonl"
OUT_PLANS = ROOT / "data" / "dgsante_plan_parse.jsonl"

# The header of the table, which also marks where the table starts. Its own
# column positions are used to split the table: measuring where the response
# column begins from the header is far more reliable than guessing a gutter
# from the body, where a short answer can leave a whole column blank.
HEADER = re.compile(
    r"^[ \t\f]*N[^\n]{0,4}\s+(?:Recommendation|Competent Authority Response)[^\n]*$",
    re.M | re.I,
)
RESPONSE_COLUMN = re.compile(
    r"\b(?:Action|Response|Competent\s+Authority|Measures|Comments)\b", re.I
)

# A row opens with the recommendation number at the start of a line.
ROW = re.compile(r"^[ \t\f]{0,8}(\d{1,2})[.)]?[ \t]+(?=\S)", re.M)

# Some member states answer in their own language while the report is in
# English. Such a plan cannot be confirmed by comparing wording, and counting
# it as a failed match would blame the parser for a translation. The share of
# very common English words separates the two cases well enough to say which
# is which; it is recorded, not used to alter the comparison.
ENGLISH_MARKERS = frozenset(
    "the of to and in that for is are be with by on as it not this which "
    "shall should ensure carried out official controls".split()
)
MIN_WORDS_TO_JUDGE_LANGUAGE = 8
ENGLISH_SHARE = 0.12

MIN_ROW_LETTERS = 30
GUTTER_MIN_WIDTH = 3
GUTTER_MIN_SHARE = 0.9
MATCH_THRESHOLD = 0.6


def plan_text(path: Path) -> str:
    """Extract the text layer of one action plan."""
    done = subprocess.run(
        ["pdftotext", "-layout", "-q", str(path), "-"],
        capture_output=True,
        text=True,
        errors="replace",
        timeout=180,
        check=False,
    )
    return done.stdout


def find_gutter(lines: list[str]) -> int | None:
    """Find the column where the table splits into two.

    The layout puts the recommendation and the response side by side, so a
    line holds both and reading it whole would mix the audit's words with the
    member state's. A run of positions that is blank on nearly every line is
    the gutter between the columns.

    Args:
        lines: Lines of the table region.

    Returns:
        The column index where the right-hand column starts, or None when
        the table is a single column.
    """
    filled = [line for line in lines if len(line.strip()) > 20]
    if len(filled) < 4:
        return None
    width = max(len(line) for line in filled)
    blank = []
    for column in range(width):
        share = sum(
            1 for line in filled if column >= len(line) or line[column] == " "
        ) / len(filled)
        blank.append(share >= GUTTER_MIN_SHARE)

    best: tuple[int, int] | None = None
    start = None
    for column, is_blank in enumerate([*blank, False]):
        if is_blank and start is None:
            start = column
        elif not is_blank and start is not None:
            run = column - start
            # Ignore the left margin and the ragged right edge.
            if run >= GUTTER_MIN_WIDTH and 12 < start < width - 12:
                if best is None or run > best[1]:
                    best = (column, run)
            start = None
    return best[0] if best else None


def split_columns(block: str, gutter: int | None) -> tuple[str, str]:
    """Split a block of table text into its left and right columns."""
    if gutter is None:
        return " ".join(block.split()), ""
    left, right = [], []
    for line in block.splitlines():
        left.append(line[:gutter])
        right.append(line[gutter:])
    return " ".join(" ".join(left).split()), " ".join(" ".join(right).split())


def split_rows(table: str) -> list[tuple[int, str]]:
    """Split the table into numbered rows, requiring the numbers to count up."""
    marks = [(m.start(), m.end(), int(m.group(1))) for m in ROW.finditer(table)]
    kept: list[tuple[int, int, int]] = []
    expected = 1
    for index, (start, end, value) in enumerate(marks):
        if value != expected:
            continue
        stop = marks[index + 1][0] if index + 1 < len(marks) else len(table)
        if sum(c.isalpha() for c in table[end:stop]) < MIN_ROW_LETTERS:
            continue
        kept.append((start, end, value))
        expected += 1

    rows: list[tuple[int, str]] = []
    for index, (start, _, value) in enumerate(kept):
        stop = kept[index + 1][0] if index + 1 < len(kept) else len(table)
        rows.append((value, table[start:stop]))
    return rows


def reads_as_english(text: str) -> bool | None:
    """Whether a passage reads as English.

    Args:
        text: The recommendation as the member state restated it.

    Returns:
        True or False, or None where there are too few words to judge.
    """
    words = re.findall(r"[a-zA-Z]+", text.lower())
    if len(words) < MIN_WORDS_TO_JUDGE_LANGUAGE:
        return None
    return sum(1 for word in words if word in ENGLISH_MARKERS) / len(words) >= (
        ENGLISH_SHARE
    )


def similarity(left: str, right: str) -> float:
    """How alike two passages are, ignoring case and spacing."""
    if not left or not right:
        return 0.0
    return difflib.SequenceMatcher(
        None, " ".join(left.lower().split()), " ".join(right.lower().split())
    ).ratio()


def containment(needle: str, haystack: str) -> float:
    """How much of one passage is found inside another.

    The question this layer asks is whether the plan restates the report's
    recommendation, not whether the two strings are the same length. The
    plans are two-column tables and the response column bleeds words into the
    restatement, which a symmetric ratio punishes heavily even where every
    word of the recommendation is present. Measuring containment asks the
    question that was meant.

    Args:
        needle: The recommendation as the report words it.
        haystack: The recommendation as the plan restates it.

    Returns:
        The share of the needle matched inside the haystack, 0 to 1.
    """
    if not needle or not haystack:
        return 0.0
    left = " ".join(needle.lower().split())
    right = " ".join(haystack.lower().split())
    matcher = difflib.SequenceMatcher(None, left, right)
    matched = sum(block.size for block in matcher.get_matching_blocks())
    return matched / len(left)


def parse_plan(record: dict, expected: dict[int, str]) -> list[dict]:
    """Read one action plan and match its rows to the report's recommendations.

    Args:
        record: A manifest row for an action plan annex.
        expected: The recommendations parsed from the report, by number.

    Returns:
        One row per numbered response found in the plan.
    """
    text = plan_text(ROOT / record["path"])
    if len(text.strip()) < 200:
        return []
    header = HEADER.search(text)
    if header is None:
        return []
    header_line = header.group(0)
    table = text[header.end() :]

    # Where the response column starts, read off the header itself. Some
    # plans have only a number and a response, and then there is no left
    # column to compare against the report.
    gutter = None
    after_recommendation = header_line.lower().find("recommendation")
    if after_recommendation != -1:
        keyword = RESPONSE_COLUMN.search(
            header_line, after_recommendation + len("recommendation")
        )
        if keyword:
            gutter = keyword.start()
    if gutter is None:
        gutter = find_gutter(table.splitlines())

    out = []
    for number, block in split_rows(table):
        restated, response = split_columns(block, gutter)
        restated = re.sub(r"^\d{1,2}[.)]?\s*", "", restated)
        if not response:
            response, restated = restated, ""
        reported = expected.get(number, "")
        score = similarity(restated, reported)
        held = containment(reported, restated)
        out.append(
            {
                "ref": record["ref"],
                "country": record["country"],
                "plan_path": record["path"],
                "plan_title": record.get("title"),
                "recommendation": number,
                "restated_recommendation": restated[:600],
                "response": response[:1200],
                # The report's own recommendation is the check on the link.
                # A shared number is not enough: plans are reissued and
                # renumbered, so the texts have to agree as well.
                "recommendation_in_report": number in expected,
                "text_similarity": round(score, 2),
                "text_containment": round(held, 2),
                "restated_reads_as_english": reads_as_english(restated),
                "link_confirmed_by_text": held >= MATCH_THRESHOLD,
            }
        )
    return out


def main() -> int:
    """Link every action plan to the recommendations of its report."""
    manifest = [
        json.loads(line)
        for line in MANIFEST.read_text(encoding="utf-8").splitlines()
        if line
    ]
    plans = [
        m
        for m in manifest
        if m["kind"] == "annex"
        and "action" in (m.get("title") or "").lower()
        and m["path"].lower().endswith(".pdf")
    ]

    by_report: dict[str, dict[int, str]] = {}
    for line in RECOMMENDATIONS.read_text(encoding="utf-8").splitlines():
        if not line:
            continue
        row = json.loads(line)
        by_report.setdefault(row["ref"], {})[row["number"]] = row["text"]

    rows: list[dict] = []
    outcomes: list[dict] = []
    for index, record in enumerate(plans, start=1):
        expected = by_report.get(record["ref"], {})
        found = parse_plan(record, expected)
        rows.extend(found)
        outcomes.append(
            {
                "ref": record["ref"],
                "country": record["country"],
                "plan_path": record["path"],
                "report_parsed": bool(expected),
                "responses": len(found),
                "outcome": "parsed" if found else "layout_not_recognised",
            }
        )
        if index % 250 == 0:
            print(f"{index}/{len(plans)} plans read", flush=True)

    for path, payload in ((OUT, rows), (OUT_PLANS, outcomes)):
        with open(path, "w", encoding="utf-8", newline="\n") as fh:
            for row in payload:
                fh.write(json.dumps(row, ensure_ascii=False) + "\n")

    answered = {(r["ref"], r["recommendation"]) for r in rows}
    confirmed = {
        (r["ref"], r["recommendation"]) for r in rows if r["link_confirmed_by_text"]
    }
    known = {(ref, number) for ref, items in by_report.items() for number in items}
    foreign = {
        (r["ref"], r["recommendation"])
        for r in rows
        if r["restated_reads_as_english"] is False
    }
    comparable = (answered & known) - foreign
    print(f"{len(rows)} responses from {len({r['plan_path'] for r in rows})} plans")
    print(f"audits with a linked plan: {len({r['ref'] for r in rows})}")
    print(f"recommendations answered: {len(answered & known)} of {len(known)}")
    print(f"  written in another language, so not comparable: {len(foreign & known)}")
    print(
        f"  confirmed by matching text: {len(confirmed & known)} of {len(comparable)}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
