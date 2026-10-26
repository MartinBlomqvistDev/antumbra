"""Find text that a document hides without blacking it out.

Step 26 of the pipeline, and the half of the pre-registered masking measure that
step 18 cannot see. Risk 6 in docs/BEGARANMALL.md says it plainly: masking that
is not black leaves no trace in an area measure, so maskningsgrad is registered
as covered area **plus** covered fields. Step 18 counts rectangles whose fill is
solid dark. A white rectangle drawn over a name is invisible to it, and the
delivered documents do contain white rectangles drawn over text.

**The instrument compares the text layer against the rendered page.** A
character is hidden when its glyph box, rendered at 150 dpi in grey, holds no
pixel darker than LIGHT: the character is in the file, and the reader of the
page cannot see it. Nothing is assumed about what covers it, so a white
rectangle, a light image and a covering annotation are all caught by the same
test, and no reasoning about drawing order is needed.

**The corpus carries its own negative control.** The standard kontrollrapport
template draws a white panel behind the body text, and 39 of the first 60
documents put dark characters inside it, 27 of them exactly 2 701 characters in
counties that share nothing else. Every one of those characters renders visibly,
so the panel is correctly read as lying behind the text rather than over it. A
colour-based measure flagged all 39, and only this comparison exposes that as
wrong.

**A hidden character is not yet a redaction.** The first documents found this
way hide four characters each, and those characters are the page number in the
header, covered by the authority's own white header box. A redaction covers a
span, so runs of hidden characters are counted and the longest run per document
is what the finding rests on. The run length distribution is printed with the
result so the threshold can be judged rather than trusted.

**The hidden text itself is never written anywhere.** It is exactly the material
the authority meant to withhold, and recovering it into a file in this
repository would be both a personal data leak and a misuse of the measurement.
Only counts leave this step.

Writes data/dold_text.jsonl, one row per document with a text layer.

Usage:
    python pipeline/26_hidden_text.py
"""

from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

import numpy as np
import pymupdf

ROOT = Path(__file__).resolve().parent.parent
DELIVERIES = ROOT / "data" / "leveranser"
MASKING = ROOT / "data" / "maskning.jsonl"
OUT = ROOT / "data" / "dold_text.jsonl"

RENDER_DPI = 150
SCALE = RENDER_DPI / 72.0
# A pixel lighter than this counts as background. Anti-aliasing keeps a visible
# glyph well below it even at small sizes, and the threshold is deliberately
# generous so that a faint but readable character is never called hidden.
LIGHT = 200
# Ink darker than this is text meant to be read. Light grey furniture and white
# text on a coloured band are excluded, as in step 18.
DARK_INK = 0x404040
# Page furniture sits in the top and bottom margins, in points. Header boxes
# covering a page number are the known false positive, and this keeps them out
# of the body figure without hiding them: both counts are written.
MARGIN = 60.0
# A redaction covers a span. Shorter runs are counted but do not on their own
# make a document masked by a light cover.
MIN_RUN = 10


def hidden_runs(path: Path) -> tuple[int, int, list[int], list[int]]:
    """Dark characters, hidden ones, and the runs they form.

    Returns the total dark characters, the hidden count, every run length in
    reading order, and the run lengths that lie clear of the page margins.
    """
    total = hidden = 0
    runs: list[int] = []
    body_runs: list[int] = []
    with pymupdf.open(path) as document:
        for page in document:
            height = float(page.rect.height)
            pixmap = page.get_pixmap(dpi=RENDER_DPI, colorspace=pymupdf.csGRAY)
            image = np.frombuffer(pixmap.samples, dtype=np.uint8).reshape(
                pixmap.height, pixmap.width
            )
            run = 0
            in_body = True
            for block in page.get_text("rawdict")["blocks"]:
                for line in block.get("lines", []):
                    for span in line.get("spans", []):
                        if span.get("color", 0) > DARK_INK:
                            continue
                        for char in span.get("chars", []):
                            if not char["c"].strip():
                                continue
                            x0, y0, x1, y1 = char["bbox"]
                            left = max(int(x0 * SCALE), 0)
                            top = max(int(y0 * SCALE), 0)
                            right = min(max(left + 1, int(x1 * SCALE)), pixmap.width)
                            bottom = min(max(top + 1, int(y1 * SCALE)), pixmap.height)
                            if right <= left or bottom <= top:
                                continue
                            total += 1
                            if image[top:bottom, left:right].min() > LIGHT:
                                hidden += 1
                                if not run:
                                    in_body = MARGIN < y0 < height - MARGIN
                                run += 1
                            elif run:
                                runs.append(run)
                                if in_body:
                                    body_runs.append(run)
                                run = 0
            if run:
                runs.append(run)
                if in_body:
                    body_runs.append(run)
    return total, hidden, runs, body_runs


def main() -> int:
    """Measure every delivered document that carries a text layer."""
    if not MASKING.exists():
        print("run pipeline/18_analyse_masking.py first")
        return 1
    rows = [json.loads(line) for line in MASKING.read_text("utf-8").splitlines()]
    targets = [r for r in rows if r["method"] == "text"]
    print(
        f"{len(targets)} dokument med textlager av {len(rows)} levererade", flush=True
    )

    records = []
    missing = 0
    for position, row in enumerate(targets, 1):
        path = DELIVERIES / row["path"]
        if not path.exists():
            missing += 1
            continue
        total, hidden, runs, body_runs = hidden_runs(path)
        # The delivery folder is myndighet_klass, except for the few documents
        # that are neither A nor B: fee decisions and one fee guideline, which
        # were delivered in the same correspondence and are kept as övrigt.
        folder = row["path"].split("/")[0]
        suffix = folder.rsplit("_", 1)[-1]
        records.append(
            {
                "path": row["path"],
                "mapp": folder,
                "klass": suffix if suffix in {"A", "B"} else "övrigt",
                "tecken": total,
                "dolda": hidden,
                "längsta_körning": max(runs, default=0),
                "längsta_i_brödtext": max(body_runs, default=0),
                "körningar": len(runs),
                "dold_av_ljus_täckning": max(body_runs, default=0) >= MIN_RUN,
            }
        )
        if position % 50 == 0:
            print(f"{position}/{len(targets)}", flush=True)

    with OUT.open("w", encoding="utf-8", newline="\n") as out:
        for record in records:
            out.write(json.dumps(record, ensure_ascii=False) + "\n")

    with_hidden = [r for r in records if r["dolda"]]
    flagged = [r for r in records if r["dold_av_ljus_täckning"]]
    print(
        f"\n{len(records)} dokument mätta, {missing} saknades på disk -> {OUT.name}\n"
        f"dokument med minst ett dolt tecken: {len(with_hidden)}\n"
        f"dokument med en dold körning på minst {MIN_RUN} tecken i brödtext: "
        f"{len(flagged)}"
    )
    per_class = Counter(r["klass"] for r in records)
    hidden_class = Counter(r["klass"] for r in with_hidden)
    print(
        "per klass: "
        + ", ".join(
            f"{k} {hidden_class[k]} av {per_class[k]}" for k in sorted(per_class)
        )
    )
    lengths = Counter(r["längsta_körning"] for r in with_hidden)
    if lengths:
        print("\nlängsta dolda körning per dokument, antal dokument:")
        for length in sorted(lengths):
            print(f"  {length:4} tecken: {lengths[length]}")
    for record in sorted(flagged, key=lambda r: -r["längsta_i_brödtext"])[:10]:
        print(
            f"  {record['längsta_i_brödtext']:5} tecken dolda i brödtext  "
            f"{record['path'][:60]}"
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
