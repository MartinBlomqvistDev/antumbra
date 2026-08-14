"""Register the animal species each delivered document concerns.

Step 20 of the pipeline. The protocol compares masking within species, because
counties inspect different animals and a county with mostly poultry is not
comparable to one with mostly cattle without adjustment; see docs/BEGARANMALL.md
section 4 and P1. This step reads each delivered document, born-digital text
from the file itself and scanned text from step 19, and counts the terms for
each species.

It writes counts, never text, to data/djurslag.jsonl.

**The counts are evidence, not a verdict.** Swedish inspection reports are
written on a template whose checklist names several species whether or not the
holding keeps them, so a single mention is weak and the majority rule below is
a baseline, not a classifier. It must be checked against hand-read documents
before any figure derived from it is published, exactly as the DG SANTE annex
classification was checked against forty hand-read annexes.

The rule: a species is registered as present when its terms appear at least
MIN_MENTIONS times, and the dominant species is the one with most mentions,
or none when two are within DOMINANCE of each other.

Usage:
    python pipeline/20_extract_species.py
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import pdfplumber

ROOT = Path(__file__).resolve().parent.parent
DELIVERIES = ROOT / "data" / "leveranser"
OCR_DIR = ROOT / "ocr" / "leveranser"
MASKING = ROOT / "data" / "maskning.jsonl"
OUT = ROOT / "data" / "djurslag.jsonl"

MIN_MENTIONS = 2
DOMINANCE = 1.5

# Swedish inflections, matched on word boundaries so that "gris" does not fire
# inside an unrelated word. The terms are the ones the reports actually use.
TERMS = {
    "nöt": r"nötkreatur|nötdjur|\bnöt\b|\bkalv(ar|en|arna)?\b|\bko\b|\bkor\b|"
    r"\bkviga|\btjur|mjölkko|dikor",
    "gris": r"\bgris(ar|en|arna|ning)?\b|\bsugga|\bsuggor|slaktsvin|smågris|"
    r"\bgalt\b|\bsvin\b",
    "fjäderfä": r"fjäderfä|\bhöns\b|värphöns|unghöns|\bkyckling|\bkalkon|"
    r"\bank(or|a)?\b|\bgäss\b|\bgås\b|slaktkyckling",
}
PATTERNS = {name: re.compile(pattern, re.IGNORECASE) for name, pattern in TERMS.items()}


def scanned_paths() -> set[str]:
    """Documents whose text comes from step 19 rather than from the file."""
    if not MASKING.exists():
        return set()
    rows = [json.loads(line) for line in MASKING.read_text("utf-8").splitlines()]
    return {row["path"] for row in rows if row["method"] == "image"}


def document_text(relative: str, scanned: set[str]) -> str | None:
    """The text of one delivered document, from OCR when it was scanned."""
    if relative in scanned:
        target = OCR_DIR / (relative.replace("/", "__") + ".txt")
        return target.read_text("utf-8") if target.exists() else None
    try:
        with pdfplumber.open(DELIVERIES / relative) as pdf:
            return "\n".join(page.extract_text() or "" for page in pdf.pages)
    except Exception:
        return None


def classify(counts: dict[str, int]) -> tuple[list[str], str | None]:
    """Species present, and the dominant one when one clearly leads."""
    present = sorted(name for name, n in counts.items() if n >= MIN_MENTIONS)
    if not present:
        return [], None
    ranked = sorted(present, key=lambda name: counts[name], reverse=True)
    if len(ranked) == 1:
        return present, ranked[0]
    top, second = counts[ranked[0]], counts[ranked[1]]
    return present, ranked[0] if top >= second * DOMINANCE else None


def main() -> int:
    """Count species terms in every delivered document."""
    if not MASKING.exists():
        print("run pipeline/18_analyse_masking.py first")
        return 1

    scanned = scanned_paths()
    rows = [json.loads(line) for line in MASKING.read_text("utf-8").splitlines()]
    records = []
    for row in rows:
        relative = row["path"]
        text = document_text(relative, scanned)
        if text is None:
            records.append(
                {
                    "path": relative,
                    "source": "ocr" if relative in scanned else "text",
                    "counts": {},
                    "present": [],
                    "dominant": None,
                    "readable": False,
                }
            )
            continue
        counts = {name: len(p.findall(text)) for name, p in PATTERNS.items()}
        present, dominant = classify(counts)
        records.append(
            {
                "path": relative,
                "source": "ocr" if relative in scanned else "text",
                "counts": counts,
                "present": present,
                "dominant": dominant,
                "readable": True,
            }
        )

    with OUT.open("w", encoding="utf-8", newline="\n") as out:
        for record in records:
            out.write(json.dumps(record, ensure_ascii=False) + "\n")

    readable = [r for r in records if r["readable"]]
    print(f"{len(records)} documents, {len(readable)} readable -> {OUT.name}\n")
    for name in PATTERNS:
        present = sum(1 for r in readable if name in r["present"])
        dominant = sum(1 for r in readable if r["dominant"] == name)
        print(f"{name:10} nämnd i {present:3}, dominerande i {dominant:3}")
    mixed = sum(1 for r in readable if len(r["present"]) > 1)
    silent = sum(1 for r in readable if not r["present"])
    print(f"\nflera djurslag nämnda: {mixed}, inget djurslag nämnt: {silent}")
    print(
        f"utan utpekat dominerande djurslag: "
        f"{sum(1 for r in readable if r['dominant'] is None)}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
