"""Read the register back against the documents, and run the two canaries.

Step 34 of the pipeline, and check 3 of docs/VILLKORSSCHEMA.md section 5. Checks
1 and 2 ask whether the segmentation is internally consistent: the numbers form
an unbroken series, and the counts match the corpus. Neither can see a condition
whose text is wrong, because a corrupted string still numbers correctly and
still counts. This step reads the text back.

**The born-digital half is read by a second extractor.** The register was
segmented from pymupdf's text layer. Here every born-digital decision is read
again with pdfplumber, and each stored condition is looked for in that output.
Two libraries agreeing on a string is evidence about the document; one library
agreeing with itself is evidence about nothing. The OCR half has no second path,
since the recognised text is the only text there is, so it is measured against
the same file the segmenter read and reported as the weaker check it is: it can
still catch a fault in the joining and in the footer removal, and it cannot
replicate the reading.

**A condition is matched as fragments, where one string would miss.** A page footer
removed from the middle of a condition leaves the stored text as two pieces of
the document with a hole between them, so a plain substring test would fail on
exactly the decisions where the footer rule did its job. The stored text is
therefore consumed greedily: the longest prefix still present in the raw stream
is taken, the search continues after it, and the number of pieces is reported.
One piece is the ordinary case; more than one means either a removed footer or a
place where the two extractors disagree about a character.

**Containment cannot see a truncation**, because a condition cut short is still
present in the document. The canary for that is the last character: a condition
that stops mid-sentence ends on a letter. The share is counted and reported, and
the two canaries VILLKORSSCHEMA asks for run beside it: conditions per decision
for the OCR half against the born-digital half, and the noise values against the
set the schema opened with four documents. This is the first full run, which is
where that set is fixed.

Nothing here writes to data/. The step reports and exits non-zero when the
pre-registered acceptance condition fails.

Usage:
    python pipeline/34_verify_conditions.py
"""

from __future__ import annotations

import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

import pdfplumber

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "pdf" / "jordbruksverket"
OCR_DIR = ROOT / "ocr" / "tillstand"
REGISTER = ROOT / "data" / "villkor.jsonl"

# The pre-registered acceptance condition, written to the protocol log before
# this file was run: 99 per cent of the characters of the born-digital half must
# be found again by the second extractor, every condition below 95 per cent is
# read by hand, and more than a tenth of the conditions ending mid-sentence
# means the register cannot be quoted verbatim.
COVERAGE_FLOOR = 0.99
CONDITION_FLOOR = 0.95
TRUNCATION_CEILING = 0.10

# When the second path returns less than this share of the characters the
# register holds for a decision, it did not read the decision, and scoring the
# decision as nothing found would measure the library rather than the register.
# The pre-registration said such a document would be set aside; the number was
# chosen after the run and nothing turns on its value. The one document it
# separates holds 9 813 characters of conditions and gives pdfplumber 40, a
# ratio of 0.004, so any threshold from a hundredth to nine tenths draws the
# same line.
UNREADABLE_SHARE = 0.10

WHITESPACE = re.compile(r"\s+")
SENTENCE_END = (".", ":", ";", "!", "?", ")", "”", "%")
# Equivalent and momentary sound levels, as the decisions write them.
NOISE = re.compile(r"(\d{2,3})\s*dB\s*\(?A\)?", re.IGNORECASE)


def collapse(text: str) -> str:
    """One space between words, so two extractors can be compared at all."""
    return WHITESPACE.sub(" ", text).strip()


def raw_text(record_id: str, origin: str) -> str:
    """The document as an independent path reads it, collapsed to one line."""
    if origin == "ocr":
        path = OCR_DIR / f"{record_id}.txt"
        return collapse(path.read_text("utf-8")) if path.exists() else ""
    path = SOURCE / f"{record_id}.pdf"
    if not path.exists():
        return ""
    with pdfplumber.open(path) as document:
        pages = [page.extract_text() or "" for page in document.pages]
    return collapse("\n".join(pages))


def fragments(stored: str, raw: str) -> list[str]:
    """The stored text cut into the longest pieces the raw stream still holds.

    The pieces are taken greedily and in order, so a piece never overlaps the
    one before it and the sequence is a decomposition of the stored text rather
    than a bag of matches. A word that neither extractor spells the same way is
    dropped one word at a time until the rest of the text can be searched for
    again, which is what keeps a single disagreement from ending the match.
    """
    found: list[str] = []
    remaining = stored
    cursor = 0
    while remaining:
        low, high = 0, len(remaining)
        while low < high:
            middle = (low + high + 1) // 2
            if raw.find(remaining[:middle], cursor) != -1:
                low = middle
            else:
                high = middle - 1
        piece = remaining[:low].rstrip() if low else ""
        # Only whole words count, or a match could end inside one.
        if piece and low < len(remaining) and remaining[low] != " ":
            piece = piece.rpartition(" ")[0]
        if not piece:
            # Not even the first word survives here. Drop it and go on, so the
            # measure counts the characters lost instead of stopping at them.
            remaining = remaining.partition(" ")[2]
            continue
        cursor = raw.find(piece, cursor) + len(piece)
        found.append(piece)
        remaining = remaining[len(piece) :].lstrip()
    return found


def coverage(
    records: list[dict],
) -> tuple[dict[str, tuple[int, int]], list[dict], list[str]]:
    """Characters found and characters stored, per source, and the weak rows.

    A document the second extractor cannot read at all is not evidence about
    the register, so it is named and set aside rather than scored as nothing
    found. That separation was written into the pre-registration before the
    run, because pdfplumber returning an empty page is a property of the
    library rather than of the text stored.
    """
    totals: dict[str, list[int]] = defaultdict(lambda: [0, 0])
    weak: list[dict] = []
    unreadable: list[str] = []
    by_document: dict[str, list[dict]] = defaultdict(list)
    for record in records:
        by_document[record["id"]].append(record)
    for index, (record_id, rows) in enumerate(sorted(by_document.items()), 1):
        origin = rows[0]["källa"]
        raw = raw_text(record_id, origin)
        held_here = sum(len(collapse(row["text"])) for row in rows)
        if len(raw) < UNREADABLE_SHARE * held_here:
            unreadable.append(record_id)
            continue
        for row in rows:
            stored = collapse(row["text"])
            pieces = fragments(stored, raw)
            held = sum(len(piece) for piece in pieces)
            totals[origin][0] += held
            totals[origin][1] += len(stored)
            share = held / len(stored) if stored else 0.0
            if share < CONDITION_FLOOR:
                weak.append(
                    {
                        "id": record_id,
                        "villkor": row["villkorsnummer"],
                        "källa": origin,
                        "andel": share,
                        "delar": len(pieces),
                        "text": row["text"],
                    }
                )
        if index % 20 == 0:
            print(f"  {index} av {len(by_document)} beslut omlästa", file=sys.stderr)
    return {k: (v[0], v[1]) for k, v in totals.items()}, weak, unreadable


def truncation(records: list[dict]) -> tuple[int, int]:
    """How many conditions stop on a character no sentence ends on."""
    cut = sum(1 for r in records if not r["text"].rstrip().endswith(SENTENCE_END))
    return cut, len(records)


def canary_counts(records: list[dict]) -> str:
    """Conditions per decision, OCR against born-digital, inside each division."""
    per_decision: dict[str, list] = {}
    for record in records:
        per_decision.setdefault(
            record["id"], [record["källa"], record["prövningsgrupp"], 0]
        )
        per_decision[record["id"]][2] += 1
    by_group: dict[str, dict[str, list[int]]] = defaultdict(lambda: defaultdict(list))
    for origin, group, count in per_decision.values():
        by_group[group][origin].append(count)
    lines = ["  prövningsgrupp                digitalfödd        OCR"]
    for group in sorted(by_group):
        sides = by_group[group]
        cells = []
        for origin in ("text", "ocr"):
            values = sorted(sides.get(origin, []))
            if not values:
                cells.append("          -")
                continue
            median = values[len(values) // 2]
            cells.append(f"  {median:>3} (n={len(values):>3})")
        lines.append(f"  {group[:28]:<28}{cells[0]}{cells[1]}")
    return "\n".join(lines)


def canary_noise(records: list[dict]) -> str:
    """The sound levels the corpus actually carries, against the schema's four."""
    opened = {40, 45, 50, 55}
    values = Counter()
    carriers: dict[int, str] = {}
    for record in records:
        for match in NOISE.finditer(record["text"]):
            value = int(match.group(1))
            values[value] += 1
            carriers.setdefault(
                value, f"{record['id']} villkor {record['villkorsnummer']}"
            )
    outside = sorted(set(values) - opened)
    lines = [
        f"  dB(A)-värden i korpusen: {len(values)} olika, "
        f"{sum(values.values())} förekomster",
        "  " + ", ".join(f"{v} ({values[v]})" for v in sorted(values)),
        f"  utanför schemats öppningsmängd {sorted(opened)}: {outside}",
    ]
    lines.extend(f"    {v} dB(A) först i {carriers[v]}" for v in outside)
    return "\n".join(lines)


def main() -> int:
    """Run check 3 and return non-zero when the acceptance condition fails."""
    if not REGISTER.exists():
        print("run pipeline/33_condition_register.py first")
        return 1
    records = [
        json.loads(line) for line in REGISTER.read_text("utf-8").splitlines() if line
    ]
    print(f"kontroll 3 över {len(records)} villkor\n")

    totals, weak, unreadable = coverage(records)
    print("\nåterläsning mot oberoende textutvinning")
    if unreadable:
        outside = set(unreadable)
        skipped = sum(1 for r in records if r["id"] in outside)
        print(
            f"  utanför måttet: {len(unreadable)} beslut med {skipped} villkor, "
            "där den andra vägen inte läser något alls"
        )
        for record_id in unreadable:
            print(f"    {record_id}")
    for origin in ("text", "ocr"):
        held, stored = totals.get(origin, (0, 0))
        if not stored:
            continue
        label = "digitalfödd, pdfplumber" if origin == "text" else "OCR, samma fil"
        print(f"  {label:<26} {held / stored:.4f} av {stored} tecken")
    print(f"  villkor under {CONDITION_FLOOR:.0%}: {len(weak)}")
    for row in sorted(weak, key=lambda r: r["andel"])[:15]:
        print(
            f"    {row['id']} villkor {row['villkor']} ({row['källa']}) "
            f"{row['andel']:.2f} i {row['delar']} delar"
        )

    cut, total = truncation(records)
    print(
        f"\navhuggning: {cut} av {total} slutar utan skiljetecken ({cut / total:.1%})"
    )

    print("\nkanarie 1, villkor per beslut (median)")
    print(canary_counts(records))
    print("\nkanarie 2, bullervärden")
    print(canary_noise(records))

    digital = totals.get("text", (0, 0))
    share = digital[0] / digital[1] if digital[1] else 0.0
    failures = []
    if share < COVERAGE_FLOOR:
        failures.append(f"täckning {share:.4f} under {COVERAGE_FLOOR}")
    if cut / total > TRUNCATION_CEILING:
        failures.append(f"avhuggning {cut / total:.3f} över {TRUNCATION_CEILING}")
    if failures:
        print("\nvillkoret för kontroll 3 ej uppfyllt: " + "; ".join(failures))
        return 1
    print("\nvillkoret för kontroll 3 uppfyllt")
    return 0


if __name__ == "__main__":
    sys.exit(main())
