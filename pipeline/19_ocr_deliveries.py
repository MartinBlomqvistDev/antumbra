"""Read the scanned Swedish deliveries with OCR.

Step 19 of the pipeline. Some authorities answer by scanning paper, so those
documents carry no text layer and nothing downstream can read them: not the
animal species behind a comparison within species, not the fields a redaction
covers. This step renders those pages and runs Tesseract in Swedish over them.

Two outputs, and the split matters. The recognised text goes to ocr/leveranser/
outside git, because it is the authorities' own documents and names natural
persons. What the repository keeps is an index of counts: pages, words and mean
confidence per document, enough to judge whether the reading can be trusted
without republishing a word of it.

Resumable: a document whose text file already exists is skipped, so the step
can be run again after every delivery.

Needs Tesseract with the Swedish language pack, the same installation step 06
uses, and pymupdf from `pip install -e ".[ocr]"`.

Usage:
    python pipeline/19_ocr_deliveries.py
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DELIVERIES = ROOT / "data" / "leveranser"
MASKING = ROOT / "data" / "maskning.jsonl"
OCR_DIR = ROOT / "ocr" / "leveranser"
INDEX = ROOT / "data" / "leveranser_ocr_index.jsonl"

TESSERACT = Path(r"C:\Program Files\Tesseract-OCR\tesseract.exe")
TESSDATA = Path(os.path.expandvars(r"%LOCALAPPDATA%\antumbra\tessdata"))
LANGUAGE = "swe"
RENDER_DPI = 300
TIMEOUT = 300


def scanned_documents() -> list[str]:
    """Paths of the delivered documents that step 18 had to judge as images."""
    if not MASKING.exists():
        return []
    rows = [json.loads(line) for line in MASKING.read_text("utf-8").splitlines()]
    return sorted(row["path"] for row in rows if row["method"] == "image")


def read_page(image: Path, workdir: Path) -> tuple[str, float]:
    """Recognised text and mean word confidence for one page image."""
    base = workdir / "out"
    subprocess.run(
        [
            str(TESSERACT),
            "--tessdata-dir",
            str(TESSDATA),
            "-l",
            LANGUAGE,
            str(image),
            str(base),
            "tsv",
        ],
        capture_output=True,
        timeout=TIMEOUT,
        check=True,
    )
    rows = base.with_suffix(".tsv").read_text(encoding="utf-8", errors="replace")
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


def read_document(source: Path) -> tuple[str, int, float]:
    """Recognised text, page count and mean confidence for one document."""
    import pymupdf

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
    """Read every scanned delivery that has not been read already."""
    targets = scanned_documents()
    if not targets:
        print("nothing to read; run pipeline/18_analyse_masking.py first")
        return 0

    OCR_DIR.mkdir(parents=True, exist_ok=True)
    if not TESSERACT.exists():
        print(f"Tesseract not found at {TESSERACT}")
        return 1

    done = set()
    if INDEX.exists():
        done = {
            json.loads(line)["path"] for line in INDEX.read_text("utf-8").splitlines()
        }

    added = 0
    with INDEX.open("a", encoding="utf-8", newline="\n") as index:
        for relative in targets:
            if relative in done:
                continue
            source = DELIVERIES / relative
            target = OCR_DIR / (relative.replace("/", "__") + ".txt")
            try:
                text, pages, confidence = read_document(source)
            except Exception as exc:
                print(f"FAILED {relative}: {str(exc)[:120]}", flush=True)
                continue
            target.write_text(text, encoding="utf-8", newline="\n")
            record = {
                "path": relative,
                "pages": pages,
                "words": len(text.split()),
                "confidence": confidence,
            }
            index.write(json.dumps(record, ensure_ascii=False) + "\n")
            index.flush()  # a run cut short must not lose the resume record
            added += 1
            print(
                f"{relative}: {pages} pages, {record['words']} words, "
                f"confidence {confidence}",
                flush=True,
            )

    print(f"\n{added} documents read, {len(done)} already done")
    return 0


if __name__ == "__main__":
    sys.exit(main())
