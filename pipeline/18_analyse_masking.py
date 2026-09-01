"""Measure how each delivered document was redacted.

Step 18 of the pipeline. The delivered documents live outside git in
data/leveranser/ and contain personal data; this step reads them and writes
only counts and flags to data/maskning.jsonl, never a character of their text.

Two methods, because the deliveries come in two shapes. Born-digital files are
judged from the text layer: a filled rectangle is a redaction, and whether text
survives under it decides whether the redaction is real. Scanned files have no
text layer, so they are judged from the rendered page instead, by looking for
solid dark rectangles in the image.

What it separates, because the difference is the finding:

    text_removed      a filled box is drawn and no text remains under it
    box_over_text     a filled box is drawn but the text under it is still in
                      the file, so the redaction is cosmetic and reversible
    marker_only       no box, but the file name or the page carries a
                      redaction marker
    bars_on_scan      no text layer, and the rendered page carries solid dark
                      rectangles
    none              nothing indicating redaction was found
    unreadable        the file could not be opened

**Not every filled black rectangle is a redaction, and two kinds are excluded
by name.** A dark band carrying light text is a table header, which the reader
is meant to read: the counties' control report template ends with a list of
applied legislation under a black header row reading "Saknr", "Föreskriftens
namn", "Författningssamling" and "Utgivningsnummer", and until 1 September 2026
that header made every document carrying it count as redacted. It was found
when the kammarrätt's notice of a case number was filed and this step judged a
court letter with nothing hidden in it to be masked. A rule thinner than three
points is the second kind: it cannot cover a line of text, and the same court
letter's three hits were hairlines half a point high that cleared the area floor
on their width alone. Neither exclusion can touch a real redaction here: the
corpus holds no box at all between the hairlines' half point and the shortest
real redaction's 13.8, and no excluded box has dark text under it.

The image method was tested against the text method on all 248 born-digital
documents before it was trusted; the result and its two failure modes are
recorded in docs/VERIFIERAT.md. The floor it cannot see past: a scan of a page
whose text was removed before printing looks exactly like a page that never
carried the text, so `masked` false on a scan means no bar was found, not that
nothing was withheld. The scan side has no equivalent of the header exclusion,
because a rendered black band with white text in it cannot be told from a
redaction without reading the pixels as text.

The image method needs pymupdf, `pip install -e ".[ocr]"`.

Usage:
    python pipeline/18_analyse_masking.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pdfplumber

ROOT = Path(__file__).resolve().parent.parent
DELIVERIES = ROOT / "data" / "leveranser"
OUT = ROOT / "data" / "maskning.jsonl"

MIN_BOX_AREA = 150.0
MAX_BOX_SHARE = 0.5
# A redaction has to be at least as tall as the line it hides. Three points is
# well under the shortest real redaction in the corpus, fifteen points, and well
# over the hairline rules that a wide enough page divider clears the area floor
# with.
MIN_BOX_HEIGHT = 3.0
MARKERS = ("bortredigerad", "maskerad", "maskat", "sekretess", "xxxx")

# Image method. A bar is a solid dark rectangle at least 40 by 6 pixels at
# 100 dpi, about 10 by 1.5 millimetres. Blocks covering more than a quarter of
# the page must be almost perfectly solid, so that a dark photograph is not
# read as a redaction while a blacked-out photo still is. Both thresholds were
# chosen by testing three settings against the text method, not by taste.
DPI = 100
DARK_LEVEL = 60
MIN_BAR_W, MIN_BAR_H = 40, 6
MIN_FILL = 0.9
BIG_SHARE, BIG_FILL = 0.25, 0.98
EDGE = 20

# The two template elements the image method has to be told about, because a
# rendered page carries no text and the text method's exclusions cannot be
# applied to pixels. Both are given in points on the page, converted to the
# rendered grid at use, so that the numbers can be checked against a PDF
# viewer's ruler rather than against a screenshot.
#
# The letterhead: the county's coat of arms is a solid black shield in the top
# left corner of page one. Measured across the corpus it sits at x 61 to 96 and
# y 48 to 54 points; the box below is wider on every side.
ARMS_X, ARMS_Y = 130.0, 80.0
# The legislation table's header band, the same element ADR-0019 excludes from
# the text layer. It runs from x 81 to 513 points and is at most 33 points high,
# and it is recognised as a row of blocks spanning that full width rather than
# by any single block, since white text breaks it into pieces.
BAND_LEFT, BAND_RIGHT = 81.0, 513.0
BAND_MAX_HEIGHT = 36.0
BAND_MIN_SPAN = 400.0
BAND_TOLERANCE = 18.0


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


def is_header_band(chars: list[dict], box: tuple[float, ...]) -> bool:
    """True when a dark box carries light text and hides no dark text.

    White text on a black band is a table header, meant to be read. A redaction
    either has nothing under it or has the original dark text still there, so a
    box holding light characters and no dark ones is page furniture.
    """
    light = dark = 0
    x0, top, x1, bottom = box
    for char in chars:
        if not char.get("text", "").strip():
            continue
        cx = (float(char["x0"]) + float(char["x1"])) / 2
        cy = (float(char["top"]) + float(char["bottom"])) / 2
        if not (x0 <= cx <= x1 and top <= cy <= bottom):
            continue
        if is_solid_dark(char.get("non_stroking_color")):
            dark += 1
        else:
            light += 1
    return bool(light) and not dark


def redaction_boxes(page: pdfplumber.page.Page) -> list[tuple[float, ...]]:
    """The filled rectangles on a page that look like redactions.

    Returns each box as x0, top, x1, bottom in points, so that both the count
    and the covered area can be measured. Table header bands and rules too thin
    to cover a line are excluded, because neither hides anything.
    """
    page_area = float(page.width) * float(page.height)
    chars = page.chars
    boxes = []
    for rect in page.rects:
        if not is_solid_dark(rect.get("non_stroking_color")):
            continue
        width = float(rect["x1"]) - float(rect["x0"])
        height = float(rect["bottom"]) - float(rect["top"])
        area = width * height
        if area < MIN_BOX_AREA or area > page_area * MAX_BOX_SHARE:
            continue
        if height < MIN_BOX_HEIGHT:
            continue
        box = (
            float(rect["x0"]),
            float(rect["top"]),
            float(rect["x1"]),
            float(rect["bottom"]),
        )
        if is_header_band(chars, box):
            continue
        boxes.append(box)
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


def dark_runs(dark: np.ndarray) -> list[tuple[int, int, int]]:
    """Row, start and end of every horizontal dark run wide enough to be a bar."""
    height, width = dark.shape
    padded = np.zeros((height, width + 2), dtype=np.int8)
    padded[:, 1:-1] = dark
    edges = np.diff(padded, axis=1)
    starts = np.argwhere(edges == 1)
    ends = np.argwhere(edges == -1)
    return [
        (int(row), int(x0), int(x1))
        for (row, x0), (_, x1) in zip(starts, ends, strict=True)
        if x1 - x0 >= MIN_BAR_W
    ]


def to_pixels(points: float) -> float:
    """A length in points, in rendered pixels."""
    return points * DPI / 72


def to_column(points: float) -> float:
    """A page coordinate in points, on the cropped grid the bar search runs over."""
    return to_pixels(points) - EDGE


def template_blocks(kept: list[list[int]], first_page: bool) -> set[int]:
    """The blocks that belong to the form rather than to a redaction.

    Two elements, both fixed by the authorities' own template: the coat of arms
    in the letterhead, and the black header band over the list of applied
    legislation. The band is found as a row of blocks reaching across the page,
    because its white column headings cut it into pieces that no single block
    describes. ADR-0020 records the test both rules were adopted on.
    """
    drop: set[int] = set()
    if first_page:
        for index, (_, x1, _, y1) in enumerate(kept):
            if x1 <= to_column(ARMS_X) and y1 <= to_column(ARMS_Y):
                drop.add(index)

    rows: list[list[int]] = []
    for index in sorted(range(len(kept)), key=lambda i: kept[i][2]):
        top = kept[index][2]
        for row in rows:
            if top <= max(kept[i][3] for i in row) + 3:
                row.append(index)
                break
        else:
            rows.append([index])
    for row in rows:
        top = min(kept[i][2] for i in row)
        bottom = max(kept[i][3] for i in row)
        left = min(kept[i][0] for i in row)
        right = max(kept[i][1] for i in row)
        if bottom - top + 1 > to_pixels(BAND_MAX_HEIGHT):
            continue
        if right - left < to_pixels(BAND_MIN_SPAN):
            continue
        near_left = abs(left - to_column(BAND_LEFT)) <= BAND_TOLERANCE
        near_right = abs(right - to_column(BAND_RIGHT)) <= BAND_TOLERANCE
        if near_left and near_right:
            drop.update(row)
    return drop


def image_bars(dark: np.ndarray, first_page: bool = False) -> tuple[int, int]:
    """Solid dark rectangles in a rendered page: how many, and their area."""
    runs = dark_runs(dark)
    if not runs:
        return 0, 0
    page_area = dark.size
    open_blocks: list[list[int]] = []  # x0, x1, y0, y1
    closed: list[list[int]] = []
    for row, x0, x1 in runs:
        for block in open_blocks:
            overlap = min(block[1], x1) - max(block[0], x0)
            if block[3] == row - 1 and overlap > 0.5 * (x1 - x0):
                block[0] = min(block[0], x0)
                block[1] = max(block[1], x1)
                block[3] = row
                break
        else:
            open_blocks.append([x0, x1, row, row])
        closed.extend(b for b in open_blocks if b[3] < row - 1)
        open_blocks = [b for b in open_blocks if b[3] >= row - 1]
    closed.extend(open_blocks)

    kept = []
    for block in closed:
        x0, x1, y0, y1 = block
        width, height = x1 - x0, y1 - y0 + 1
        if height < MIN_BAR_H:
            continue
        area = width * height
        fill = dark[y0 : y1 + 1, x0:x1].mean()
        floor = BIG_FILL if area > page_area * BIG_SHARE else MIN_FILL
        if fill >= floor:
            kept.append(block)

    drop = template_blocks(kept, first_page)
    bars = covered = 0
    for index, (x0, x1, y0, y1) in enumerate(kept):
        if index in drop:
            continue
        bars += 1
        covered += (x1 - x0) * (y1 - y0 + 1)
    return bars, covered


def scan_bars(path: Path) -> tuple[int, int, float]:
    """Bars, pages carrying them and covered share, for a scanned document."""
    try:
        import pymupdf
    except ImportError:  # the step still measures born-digital files without it
        return -1, -1, 0.0

    total = pages = 0
    covered = surface = 0
    with pymupdf.open(path) as doc:
        for number, page in enumerate(doc, 1):
            pixmap = page.get_pixmap(dpi=DPI, colorspace=pymupdf.csGRAY)
            grey = np.frombuffer(pixmap.samples, dtype=np.uint8).reshape(
                pixmap.height, pixmap.width
            )
            inner = grey[EDGE:-EDGE, EDGE:-EDGE] < DARK_LEVEL
            found, area = image_bars(inner, first_page=number == 1)
            total += found
            covered += area
            surface += inner.size
            pages += 1 if found else 0
    share = covered / surface if surface else 0.0
    return total, pages, round(share, 5)


def classify(record: dict) -> tuple[str, bool | None]:
    """The redaction kind and whether the document is masked."""
    if record["error"]:
        return "unreadable", None
    if record["pages_with_text"] == 0:
        if record["bars"] < 0:
            return "unreadable", None
        return ("bars_on_scan", True) if record["bars"] else ("none", False)
    if record["boxes"] and record["chars_under_boxes"]:
        return "box_over_text", True
    if record["boxes"]:
        return "text_removed", True
    if record["marker_in_filename"] or record["marker_in_text"]:
        return "marker_only", True
    return "none", False


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
        "bars": 0,
        "pages_with_bars": 0,
        "masked_area_share": 0.0,
        "marker_in_filename": "bortredigerad" in name,
        "marker_in_text": False,
        "method": "text",
        "kind": "unreadable",
        "masked": None,
        "error": None,
    }
    covered = surface = 0.0
    try:
        with pdfplumber.open(path) as pdf:
            record["pages"] = len(pdf.pages)
            for page in pdf.pages:
                surface += float(page.width) * float(page.height)
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
                    covered += sum((x1 - x0) * (b - t0) for x0, t0, x1, b in boxes)
    except Exception as exc:  # a corrupt file is a finding, not a crash
        record["error"] = str(exc)[:200]

    if not record["error"] and record["pages_with_text"] == 0:
        record["method"] = "image"
        record["bars"], record["pages_with_bars"], share = scan_bars(path)
        record["masked_area_share"] = share
    elif surface:
        record["masked_area_share"] = round(covered / surface, 5)

    record["kind"], record["masked"] = classify(record)
    return record


def main() -> int:
    """Analyse every delivered document and write the redaction record."""
    if not DELIVERIES.is_dir():
        print("no deliveries yet: data/leveranser/ does not exist")
        return 0

    records = [analyse(path) for path in sorted(DELIVERIES.rglob("*.pdf"))]

    with OUT.open("w", encoding="utf-8", newline="\n") as out:
        for record in records:
            out.write(json.dumps(record, ensure_ascii=False) + "\n")

    per_delivery: dict[str, dict[str, int]] = {}
    for record in records:
        folder = record["path"].split("/")[0]
        bucket = per_delivery.setdefault(folder, {})
        bucket[record["kind"]] = bucket.get(record["kind"], 0) + 1

    print(f"{len(records)} documents analysed, written to {OUT.name}\n")
    for folder in sorted(per_delivery):
        parts = ", ".join(f"{k} {v}" for k, v in sorted(per_delivery[folder].items()))
        print(f"{folder:26} {parts}")

    judged = [r for r in records if r["masked"] is not None]
    by_image = sum(1 for r in judged if r["method"] == "image")
    print(
        f"\n{len(judged)} of {len(records)} documents judged, "
        f"{by_image} of them from the rendered image; "
        f"{sum(1 for r in judged if r['masked'])} masked"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
