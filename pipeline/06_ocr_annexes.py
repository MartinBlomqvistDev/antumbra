"""Run OCR over the annexes that carry no text layer.

Step 06 of the pipeline; run 05_classify_annexes.py first. Roughly half of
the numbered annexes from the older era are scanned pages, mostly faxes from
1998 to 2006, and carry no extractable text. This step rasterises what needs
it, runs Tesseract in the language of the member state plus English, and
writes one text file per annex.

Quality varies with the scan, from clean typed pages to degraded fax
transmissions, so every record carries Tesseract's mean word confidence.
Read that before trusting a given file: this step produces evidence of
varying quality, far from uniform text.

The text itself lands under ocr/, which is gitignored; the committed index
records what was produced and how well.

Writes ocr/dgsante/<stem>.txt and data/dgsante_ocr_index.jsonl.

Usage:
    python pipeline/06_ocr_annexes.py
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import threading
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CLASSES = ROOT / "data" / "dgsante_annex_classes.jsonl"
OCR_DIR = ROOT / "ocr" / "dgsante"
INDEX = ROOT / "data" / "dgsante_ocr_index.jsonl"

TESSERACT = Path(r"C:\Program Files\Tesseract-OCR\tesseract.exe")
TESSDATA = Path(os.path.expandvars(r"%LOCALAPPDATA%\antumbra\tessdata"))
RENDER_DPI = 300
WORKERS = 8
TIMEOUT = 300

# The member state's language plus English: these documents are routinely
# bilingual, and the mission reference and headings are in English even when
# the body is not.
LANGUAGE = {
    "Austria": "deu",
    "Belgium": "nld+fra",
    "Bulgaria": "bul",
    "Croatia": "hrv",
    "Cyprus": "ell",
    "Czech Republic": "ces",
    "Czechia": "ces",
    "Denmark": "dan",
    "Estonia": "est",
    "Finland": "fin+swe",
    "France": "fra",
    "Germany": "deu",
    "Greece": "ell",
    "Hungary": "hun",
    "Ireland": "eng",
    "Italy": "ita",
    "Latvia": "lav",
    "Lithuania": "lit",
    "Luxembourg": "fra+deu",
    "Malta": "eng",
    "Netherlands": "nld",
    "Poland": "pol",
    "Portugal": "por",
    "Romania": "ron",
    "Slovakia": "slk",
    "Slovenia": "slv",
    "Spain": "spa",
    "Sweden": "swe",
}

_lock = threading.Lock()
_done = 0
_failed = 0


def languages(country: str) -> str:
    """Tesseract language string for a member state, always including English."""
    primary = LANGUAGE.get(country, "eng")
    parts = [p for p in primary.split("+") if p]
    if "eng" not in parts:
        parts.append("eng")
    return "+".join(parts)


def run_tesseract(image: Path, langs: str, workdir: Path) -> tuple[str, float]:
    """OCR one image and read back its text and mean word confidence.

    Args:
        image: Image file to read.
        langs: Tesseract language string.
        workdir: Directory for Tesseract's output files.

    Returns:
        The recognised text and the mean confidence over recognised words,
        which is 0.0 when nothing was recognised.
    """
    base = workdir / "out"
    subprocess.run(
        [
            str(TESSERACT),
            "--tessdata-dir",
            str(TESSDATA),
            "-l",
            langs,
            str(image),
            str(base),
            "tsv",
        ],
        capture_output=True,
        timeout=TIMEOUT,
        check=True,
    )
    rows = (base.with_suffix(".tsv")).read_text(encoding="utf-8", errors="replace")
    words: list[str] = []
    confidences: list[float] = []
    for line in rows.splitlines()[1:]:
        fields = line.split("\t")
        if len(fields) < 12 or not fields[11].strip():
            continue
        try:
            confidence = float(fields[10])
        except ValueError:
            continue
        if confidence < 0:
            continue
        words.append(fields[11])
        confidences.append(confidence)
    mean = sum(confidences) / len(confidences) if confidences else 0.0
    return " ".join(words), round(mean, 1)


def pdf_pages(path: Path, workdir: Path) -> list[Path]:
    """Rasterise a scanned PDF to one PNG per page."""
    import pymupdf

    pages: list[Path] = []
    with pymupdf.open(str(path)) as document:
        for number, page in enumerate(document):
            pixmap = page.get_pixmap(dpi=RENDER_DPI)
            target = workdir / f"page{number:03d}.png"
            pixmap.save(str(target))
            pages.append(target)
    return pages


def is_ole_document(path: Path) -> bool:
    """Whether a file is a legacy Office document whatever its name says.

    At least one annex is served with a .pdf name while its bytes are an OLE
    compound file. Trusting the extension would send it to a PDF reader that
    cannot open it.
    """
    with path.open("rb") as fh:
        return fh.read(8) == b"\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1"


def salvage_image(path: Path, workdir: Path) -> Path:
    """Re-encode an image so a truncated one can still be read.

    One GIF in the corpus is truncated, and byte-identical to what the
    Commission serves, so the damage is at the source. Pillow can still
    decode the part that arrived; re-encoding it as PNG hands OCR the
    readable portion instead of discarding the page.
    """
    from PIL import Image, ImageFile

    ImageFile.LOAD_TRUNCATED_IMAGES = True
    target = workdir / "salvaged.png"
    with Image.open(path) as image:
        image.load()
        image.convert("L").save(target)
    return target


def work(row: dict) -> dict | None:
    """OCR one annex; failures are recorded and never raised."""
    global _done, _failed
    source = ROOT / row["path"]
    target = OCR_DIR / (source.stem + ".txt")
    langs = languages(row["country"])
    record: dict | None = None
    try:
        if is_ole_document(source):
            raise RuntimeError("legacy Office document behind a .pdf name")
        with tempfile.TemporaryDirectory() as raw:
            workdir = Path(raw)
            images = (
                pdf_pages(source, workdir)
                if source.suffix.lower() == ".pdf"
                else [source]
            )
            texts: list[str] = []
            confidences: list[float] = []
            for index, image in enumerate(images):
                page_dir = workdir / f"p{index}"
                page_dir.mkdir(exist_ok=True)
                try:
                    text, confidence = run_tesseract(image, langs, page_dir)
                except subprocess.CalledProcessError:
                    text, confidence = run_tesseract(
                        salvage_image(image, page_dir), langs, page_dir
                    )
                if text:
                    texts.append(text)
                    confidences.append(confidence)
            joined = "\n\n".join(texts)
            target.write_text(joined, encoding="utf-8")
            mean = round(sum(confidences) / len(confidences), 1) if confidences else 0.0
            if not joined.split():
                # An empty result is a failure to report, far from a quiet
                # success:
                # one annex in the corpus is truncated at source and decodes
                # to a blank page.
                raise RuntimeError("no text recognised; page blank or unreadable")
            record = {
                "path": row["path"],
                "text_path": target.relative_to(ROOT).as_posix(),
                "country": row["country"],
                "languages": langs,
                "pages": len(images),
                "chars": len(joined),
                "words": len(joined.split()),
                "mean_confidence": mean,
                "error": None,
            }
    except Exception as exc:
        record = {
            "path": row["path"],
            "text_path": None,
            "country": row["country"],
            "languages": langs,
            "pages": 0,
            "chars": 0,
            "words": 0,
            "mean_confidence": 0.0,
            "error": str(exc)[:200],
        }
    with _lock:
        _done += 1
        if record and record["error"]:
            _failed += 1
        if _done % 100 == 0:
            print(f"{_done} done, {_failed} failed", flush=True)
    return record


def main() -> int:
    """OCR every annex that has no text layer."""
    if not TESSERACT.exists():
        print(f"Tesseract not found at {TESSERACT}", flush=True)
        return 1
    rows = [
        json.loads(line)
        for line in CLASSES.read_text(encoding="utf-8").splitlines()
        if line
    ]
    todo = [r for r in rows if r["class"] == "needs_ocr"]
    OCR_DIR.mkdir(parents=True, exist_ok=True)

    existing: dict[str, dict] = {}
    if INDEX.exists():
        for line in INDEX.read_text(encoding="utf-8").splitlines():
            if not line:
                continue
            record = json.loads(line)
            # A record with no words is not a finished file: it predates the
            # rule that an empty result must be reported as a failure.
            if not record.get("error") and record.get("words"):
                existing[record["path"]] = record
    pending = [r for r in todo if r["path"] not in existing]
    print(
        f"needing OCR {len(todo)}, already done {len(existing)}, to run {len(pending)}",
        flush=True,
    )

    with ThreadPoolExecutor(WORKERS) as pool:
        produced = [r for r in pool.map(work, pending) if r]

    records = list(existing.values()) + produced
    records.sort(key=lambda r: r["path"])
    with open(INDEX, "w", encoding="utf-8", newline="\n") as fh:
        for record in records:
            fh.write(json.dumps(record, ensure_ascii=False) + "\n")

    good = [r for r in records if not r["error"] and r["mean_confidence"] >= 70]
    print(f"FINISHED, {_done} run, {_failed} failed", flush=True)
    print(f"{len(records)} rows -> {INDEX.relative_to(ROOT)}")
    print(f"mean confidence at or above 70: {len(good)} of {len(records)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
