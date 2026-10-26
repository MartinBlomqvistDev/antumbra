"""Read the scanned permit decisions with OCR so they can be segmented.

Step 25 of the pipeline. The baseline test in step 24 reaches 120 of the 236
permit files, and the single largest reason is that 72 of them are scans with
no text layer at all. Nothing in the conditions layer can see those decisions:
leaving aside the condition texts, the reuse measure and the permit division
comparison. This step renders their pages and runs Tesseract in Swedish over
them, on the same terms as step 19 does for the Swedish deliveries.

**The recognised text stays outside version control.** It goes to
ocr/tillstand/, named by the same identifier step 23 gives the document, because
the published file names carry the names of natural persons and the text carries
company and place names throughout. What the repository keeps is an index of
counts: pages, words and mean confidence per decision, enough to judge whether
a reading can be trusted without republishing a word of it.

**The line structure is kept, and that is not a detail.** Step 19 does the same
work for the Swedish deliveries and joins every recognised word on a page into
one string, which is enough for the species terms it feeds. Step 24 anchors on
the start of a line: the conditions heading is a line of its own and every
condition opens a line with its number. The first run here copied step 19 and
produced one line per page, whereupon all 72 decisions yielded exactly zero
conditions while their text plainly contained them. Tesseract's TSV carries
block, paragraph and line numbers, so the lines are reassembled from those.

**OCR text is not equal to born-digital text, and the index says so per file.**
A decision read at low confidence will segment worse than one with a text layer,
so any figure computed over the OCR set has to be reported beside its confidence
rather than pooled silently with the rest.

Resumable: a decision whose text file already exists is skipped.

Needs Tesseract with the Swedish language pack, the same installation step 06
uses, and pymupdf from `pip install -e ".[ocr]"`.

Usage:
    python pipeline/25_ocr_permits.py
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import time
from pathlib import Path

import pymupdf

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "pdf" / "jordbruksverket"
OCR_DIR = ROOT / "ocr" / "tillstand"
INDEX = ROOT / "data" / "tillstand_ocr_index.jsonl"

TESSERACT = Path(r"C:\Program Files\Tesseract-OCR\tesseract.exe")
TESSDATA = Path(os.path.expandvars(r"%LOCALAPPDATA%\antumbra\tessdata"))
LANGUAGE = "swe"
RENDER_DPI = 300
TIMEOUT = 300
# Tesseract failed on three decisions in the first run and then read every one
# of their pages without error when retried alone, so the failure is transient
# rather than a property of the file. One lost page discards the whole decision,
# so
# the call is retried rather than left to the next run.
RETRIES = 3

# The same threshold step 24 uses to decide a file has no usable text layer.
# Kept as a literal rather than imported, because a module whose name starts
# with a digit cannot be imported, and the two must be read together.
MIN_CHARS_PER_PAGE = 200


def scanned_documents() -> list[Path]:
    """The permit files that carry no usable text layer."""
    found = []
    for path in sorted(SOURCE.glob("*.pdf")):
        with pymupdf.open(path) as document:
            pages = len(document)
            text = "\n".join(page.get_text() for page in document)
        if len(text) < MIN_CHARS_PER_PAGE * pages:
            found.append(path)
    return found


def read_page(image: Path, workdir: Path) -> tuple[str, float]:
    """Recognised text and mean word confidence for one page image."""
    base = workdir / "out"
    command = [
        str(TESSERACT),
        "--tessdata-dir",
        str(TESSDATA),
        "-l",
        LANGUAGE,
        str(image),
        str(base),
        "tsv",
    ]
    for attempt in range(RETRIES):
        try:
            subprocess.run(command, capture_output=True, timeout=TIMEOUT, check=True)
            break
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
            if attempt == RETRIES - 1:
                raise
            time.sleep(2 * (attempt + 1))
    rows = base.with_suffix(".tsv").read_text(encoding="utf-8", errors="replace")
    lines: dict[tuple[str, str, str], list[str]] = {}
    confidences: list[float] = []
    for row in rows.splitlines()[1:]:
        fields = row.split("\t")
        if len(fields) < 12 or not fields[11].strip():
            continue
        try:
            confidence = float(fields[10])
        except ValueError:
            continue
        if confidence < 0:
            continue
        lines.setdefault((fields[2], fields[3], fields[4]), []).append(fields[11])
        confidences.append(confidence)
    mean = sum(confidences) / len(confidences) if confidences else 0.0
    return "\n".join(" ".join(words) for words in lines.values()), round(mean, 1)


def read_document(source: Path) -> tuple[str, int, float]:
    """Recognised text, page count and mean confidence for one decision.

    Pages are kept apart by a blank line, because step 24 segments on lines and
    a condition must not run into the page that follows it.
    """
    texts: list[str] = []
    confidences: list[float] = []
    with tempfile.TemporaryDirectory() as tmp:
        workdir = Path(tmp)
        with pymupdf.open(str(source)) as document:
            pages = len(document)
            for number, page in enumerate(document):
                image = workdir / f"page{number:03d}.png"
                page.get_pixmap(dpi=RENDER_DPI).save(str(image))
                text, confidence = read_page(image, workdir)
                texts.append(text)
                confidences.append(confidence)
    mean = sum(confidences) / len(confidences) if confidences else 0.0
    return "\n\n".join(texts), pages, round(mean, 1)


def main() -> int:
    """Read every scanned permit decision that has not been read already."""
    if not TESSERACT.exists():
        print(f"Tesseract not found at {TESSERACT}")
        return 1
    targets = scanned_documents()
    if not targets:
        print("no permit file lacks a text layer; run pipeline/23_download_permits.py")
        return 0
    OCR_DIR.mkdir(parents=True, exist_ok=True)

    done = set()
    if INDEX.exists():
        done = {
            json.loads(line)["id"] for line in INDEX.read_text("utf-8").splitlines()
        }

    print(f"{len(targets)} skannade beslut, {len(done)} redan lästa", flush=True)
    added = failed = 0
    with INDEX.open("a", encoding="utf-8", newline="\n") as index:
        for position, source in enumerate(targets, 1):
            if source.stem in done:
                continue
            try:
                text, pages, confidence = read_document(source)
            except Exception as exc:
                failed += 1
                print(f"FAILED {source.stem}: {str(exc)[:120]}", flush=True)
                continue
            (OCR_DIR / f"{source.stem}.txt").write_text(
                text, encoding="utf-8", newline="\n"
            )
            record = {
                "id": source.stem,
                "pages": pages,
                "words": len(text.split()),
                "confidence": confidence,
            }
            index.write(json.dumps(record, ensure_ascii=False) + "\n")
            index.flush()  # a run cut short must not lose the resume record
            added += 1
            print(
                f"{position}/{len(targets)} {source.stem}: {pages} sidor, "
                f"{record['words']} ord, konfidens {confidence}",
                flush=True,
            )

    print(f"\n{added} beslut lästa, {failed} misslyckade, {len(done)} sedan tidigare")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
