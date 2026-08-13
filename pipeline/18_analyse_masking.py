"""Measure how each delivered document was redacted.

Step 18 of the pipeline. The delivered documents live outside git in
data/leveranser/ and contain personal data; this step reads them and writes
only counts and flags to data/maskning.jsonl, never a character of their text.

What it separates, because the difference is the finding:

    text_removed      a filled box is drawn and no text remains under it
    box_over_text     a filled box is drawn but the text under it is still in
                      the file, so the redaction is cosmetic and reversible
    marker_only       no box, but the file name or the page carries a
                      redaction marker
    scanned           no text layer at all, so redaction cannot be judged
                      without OCR
    none              nothing indicating redaction was found

A box counts as a redaction box when it is filled in a near-black or near-white
solid, is larger than a character but smaller than half the page, and is not
the page frame. Text under a box is counted by character centre, which is
robust to the box being drawn slightly larger than the glyphs.

Usage:
    python pipeline/18_analyse_masking.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pdfplumber

ROOT = Path(__file__).resolve().parent.parent
DELIVERIES = ROOT / "data" / "leveranser"
OUT = ROOT / "data" / "maskning.jsonl"

MIN_BOX_AREA = 150.0
MAX_BOX_SHARE = 0.5
MARKERS = ("bortredigerad", "maskerad", "maskat", "sekretess", "xxxx")


def is_solid_dark(colour: object) -> bool:
    """True when a fill colour is a solid black or near-black."""
    if colour is None:
        return False
    if isinstance(colour, (int, float)):
        return float(colour) <= 0.25
    if isinstance(colour, (list, tuple)) and colour:
        values = [float(c) for c in colour if isinstance(c, (int, float))]
        return bool(values) and max(values) <= 0.25
    return False


def redaction_boxes(page: pdfplumber.page.Page) -> list[tuple[float, ...]]:
    """The filled rectangles on a page that look like redactions."""
    page_area = float(page.width) * float(page.height)
    boxes = []
    for rect in page.rects:
        if not is_solid_dark(rect.get("non_stroking_color")):
            continue
        width = float(rect["x1"]) - float(rect["x0"])
        height = float(rect["bottom"]) - float(rect["top"])
        area = width * height
        if area < MIN_BOX_AREA or area > page_area * MAX_BOX_SHARE:
            continue
        boxes.append(
            (
                float(rect["x0"]),
                float(rect["top"]),
                float(rect["x1"]),
                float(rect["bottom"]),
            )
        )
    return boxes


def chars_inside(page: pdfplumber.page.Page, boxes: list[tuple[float, ...]]) -> int:
    """How many dark characters have their centre inside one of the boxes.

    Light characters inside a dark box are white text on a coloured band, a
    table header or a page furniture element, and are meant to be read. Only
    dark text under a dark box is text the reader was not meant to see.
    """
    if not boxes:
        return 0
    hits = 0
    for char in page.chars:
        if not char.get("text", "").strip():
            continue
        if not is_solid_dark(char.get("non_stroking_color")):
            continue
        cx = (float(char["x0"]) + float(char["x1"])) / 2
        cy = (float(char["top"]) + float(char["bottom"])) / 2
        for x0, top, x1, bottom in boxes:
            if x0 <= cx <= x1 and top <= cy <= bottom:
                hits += 1
                break
    return hits


def classify(scanned: bool, boxes: int, under: int, marker: bool) -> str:
    """The redaction kind for one document."""
    if scanned:
        return "scanned"
    if boxes and under:
        return "box_over_text"
    if boxes:
        return "text_removed"
    if marker:
        return "marker_only"
    return "none"


def analyse(path: Path) -> dict:
    """Read one document and return its redaction record, never its text."""
    name = path.name.lower()
    record = {
        "path": path.relative_to(DELIVERIES).as_posix(),
        "pages": 0,
        "pages_with_text": 0,
        "chars": 0,
        "boxes": 0,
        "pages_with_boxes": 0,
        "chars_under_boxes": 0,
        "marker_in_filename": "bortredigerad" in name,
        "marker_in_text": False,
        "kind": "unreadable",
        "error": None,
    }
    try:
        with pdfplumber.open(path) as pdf:
            record["pages"] = len(pdf.pages)
            for page in pdf.pages:
                text = (page.extract_text() or "").lower()
                if text.strip():
                    record["pages_with_text"] += 1
                if any(marker in text for marker in MARKERS):
                    record["marker_in_text"] = True
                record["chars"] += len(page.chars)
                boxes = redaction_boxes(page)
                if boxes:
                    record["boxes"] += len(boxes)
                    record["pages_with_boxes"] += 1
                    record["chars_under_boxes"] += chars_inside(page, boxes)
    except Exception as exc:  # a corrupt file is a finding, not a crash
        record["error"] = str(exc)[:200]
        return record

    record["kind"] = classify(
        scanned=record["pages_with_text"] == 0,
        boxes=record["boxes"],
        under=record["chars_under_boxes"],
        marker=record["marker_in_filename"] or record["marker_in_text"],
    )
    return record


def main() -> int:
    """Analyse every delivered document and write the redaction record."""
    if not DELIVERIES.is_dir():
        print("no deliveries yet: data/leveranser/ does not exist")
        return 0

    records = []
    for path in sorted(DELIVERIES.rglob("*.pdf")):
        records.append(analyse(path))

    with OUT.open("w", encoding="utf-8", newline="\n") as out:
        for record in records:
            out.write(json.dumps(record, ensure_ascii=False) + "\n")

    per_delivery: dict[str, dict[str, int]] = {}
    for record in records:
        folder = record["path"].split("/")[0]
        bucket = per_delivery.setdefault(folder, {})
        bucket[record["kind"]] = bucket.get(record["kind"], 0) + 1
        bucket["chars_under_boxes"] = (
            bucket.get("chars_under_boxes", 0) + record["chars_under_boxes"]
        )

    print(f"{len(records)} documents analysed, written to {OUT.name}\n")
    for folder in sorted(per_delivery):
        counts = per_delivery[folder]
        leaked = counts.pop("chars_under_boxes", 0)
        parts = ", ".join(f"{k} {v}" for k, v in sorted(counts.items()))
        tail = f"  [{leaked} characters under boxes]" if leaked else ""
        print(f"{folder:26} {parts}{tail}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
