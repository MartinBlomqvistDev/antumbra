"""Read the decisions whose text layer is not a reading of the page, by OCR.

Step 39 of the pipeline, and the second route kontroll 3 said it lacked.

Kontroll 3 reads every born-digital decision back with pdfplumber and every
scanned one against step 25's recognised text. One decision fell outside both:
`361be3bd133c` gives pdfplumber 40 characters out of 34 pages while pymupdf
gives 73 459, so its 31 conditions rest on a single library agreeing with
itself. The diagnosis is worse than the gap. **The pages declare no fonts at
all**, `get_fonts` returns an empty list, and pypdf and pdfminer read the same
few bullet characters pdfplumber does. What pymupdf recovers has broken
geometry: a word box 81 points tall, and words split as `Tillstån` and
`dsplikt`. The text is there, but nothing in the file says where on the page it
belongs, so the reading order cannot be trusted from the text layer alone.

**A second shape of the same defect reads the page without its letters.**
`13df613f9802` carries no å, ä or ö at all, not one in 981 letters, where the
median decision is at 5,4 per cent and the next lowest at 4,3. Swedish
administrative prose without them does not exist, so that text layer is not a
reading of the page either. It passes step 24's character count and a second
library reads the same crippled characters, so nothing before this step could
see it.

**The independent route is the printed page.** The pages are rendered and read
with Tesseract on the same terms step 25 uses for the scans, and each stored
condition is measured against that reading with kontroll 3's own decomposition.
Recognition of a rendered page shares nothing with the text layer, so the two
readings agreeing is evidence about the document rather than about a library.

**The floor is lower than kontroll 3's, and that is the point.** Kontroll 3
compares two readings of the same character stream and asks for 0,99. This
compares a character stream with a reading of an image, where hyphenation,
spacing and single letters differ without either side being wrong. The
pre-registered condition is a median coverage of at least 0,90 per condition
and no single condition below 0,50, read with å, ä and ö folded to a, a and o
on both sides so that a decision which lost its letters is judged on its words.
The straight and case-folded figures are printed beside it.

The recognised text stays outside version control, in `ocr/tillstand_kontroll/`,
for the same reason step 25's does: it carries company and place names
throughout.

Usage:
    python pipeline/39_verify_broken_text_layer.py
    python pipeline/39_verify_broken_text_layer.py --screen   # only the screen
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import re
import statistics
import sys
from pathlib import Path
from types import ModuleType

import pymupdf

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "pdf" / "jordbruksverket"
REGISTER = ROOT / "data" / "villkor.jsonl"
OCR_DIR = ROOT / "ocr" / "tillstand_kontroll"

# A page that shows text while declaring no font is the defect this step exists
# for. Forty characters is the same floor kontroll 3 uses to call a reading
# empty, and it keeps a blank page or a bare page number out of the screen.
MIN_CHARS = 40

# Swedish administrative prose is about five per cent å, ä and ö. A decision at
# a fiftieth of that has a text layer that dropped the letters rather than a
# vocabulary that avoids them; the corpus median is 0,054 and the lowest but one
# is 0,043, so any line drawn between them separates the same single decision.
DIACRITIC_FLOOR = 0.02
DIACRITICS = str.maketrans({"å": "a", "ä": "a", "ö": "o", "Å": "A", "Ä": "A", "Ö": "O"})

# Pre-registered, written to the protocol log before the run.
MEDIAN_FLOOR = 0.90
CONDITION_FLOOR = 0.50


def load(step: str, name: str) -> ModuleType:
    """A pipeline step as a module, since a name starting with a digit cannot."""
    spec = importlib.util.spec_from_file_location(name, ROOT / "pipeline" / step)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def screen_diacritics(records: list[dict]) -> list[str]:
    """Every decision whose stored conditions have all but lost å, ä and ö."""
    letters: dict[str, list[int]] = {}
    for record in records:
        text = record["text"]
        counts = letters.setdefault(record["id"], [0, 0])
        counts[0] += sum(text.count(c) for c in "åäöÅÄÖ")
        counts[1] += len(re.findall(r"[^\W\d_]", text, re.UNICODE))
    flagged = []
    for ident, (marks, total) in sorted(letters.items()):
        if total and marks / total < DIACRITIC_FLOOR:
            print(f"  {ident}  {marks} av {total} bokstäver är å, ä eller ö")
            flagged.append(ident)
    print(f"{len(flagged)} beslut av {len(letters)} träffas av sikten")
    return flagged


def screen() -> list[str]:
    """Every decision with at least one page that has text but declares no font."""
    flagged = []
    for path in sorted(SOURCE.glob("*.pdf")):
        with pymupdf.open(path) as document:
            pages = sum(
                1
                for page in document
                if not page.get_fonts() and len(page.get_text().strip()) > MIN_CHARS
            )
            total = len(document)
        if pages:
            flagged.append((path.stem, pages, total))
    for ident, pages, total in flagged:
        print(f"  {ident}  {pages} av {total} sidor utan typsnitt")
    total_files = len(list(SOURCE.glob("*.pdf")))
    print(f"{len(flagged)} beslut av {total_files} träffas av sikten")
    return [ident for ident, _, _ in flagged]


def recognise(ident: str) -> tuple[str, float]:
    """The decision as Tesseract reads the rendered pages, cached on disk."""
    OCR_DIR.mkdir(parents=True, exist_ok=True)
    target = OCR_DIR / f"{ident}.txt"
    if target.exists():
        return target.read_text("utf-8"), -1.0
    step25 = load("25_ocr_permits.py", "ocr_permits")
    text, _pages, confidence = step25.read_document(SOURCE / f"{ident}.pdf")
    target.write_text(text, "utf-8", newline="\n")
    return text, confidence


def measure(ident: str, records: list[dict], recognised: str) -> list[dict]:
    """Each stored condition against the recognised text, kontroll 3's way."""
    step34 = load("34_verify_conditions.py", "verify_conditions")
    raw = step34.collapse(recognised)
    folded = raw.casefold()
    out = []
    for record in records:
        stored = step34.collapse(record["text"])
        plain = sum(len(p) for p in step34.fragments(stored, raw))
        cased = sum(len(p) for p in step34.fragments(stored.casefold(), folded))
        flat = sum(
            len(p)
            for p in step34.fragments(
                stored.casefold().translate(DIACRITICS), folded.translate(DIACRITICS)
            )
        )
        out.append(
            {
                "id": ident,
                "position": record["position"],
                "villkorsnummer": record["villkorsnummer"],
                "tecken": len(stored),
                "täckning": plain / len(stored) if stored else 0.0,
                "täckning_gemener": cased / len(stored) if stored else 0.0,
                "täckning_vikt": flat / len(stored) if stored else 0.0,
            }
        )
    return out


def report(rows: list[dict]) -> bool:
    """Print the outcome and say whether the pre-registered condition held."""
    # The verdict is read on the folded measure, as the pre-registration for
    # 13df613f9802 wrote it. The first version of this step read it on the
    # case-folded column and printed a failure for that decision which the
    # written condition does not describe. For 361be3bd133c the two columns
    # give the same median to the third decimal.
    shares = sorted(r["täckning_vikt"] for r in rows)
    median = statistics.median(shares)
    worst = [r for r in rows if r["täckning_vikt"] < CONDITION_FLOOR]
    plain = statistics.median(sorted(r["täckning"] for r in rows))
    cased = statistics.median(sorted(r["täckning_gemener"] for r in rows))
    print(f"\n{len(rows)} villkor mätta mot den igenkända texten")
    print(f"  median täckning, å ä ö vikta: {median:.3f}  (golv {MEDIAN_FLOOR})")
    print(f"  median täckning, gemener: {cased:.3f}")
    print(f"  median täckning, som kontroll 3 mäter: {plain:.3f}")
    print(f"  lägsta: {shares[0]:.3f}   högsta: {shares[-1]:.3f}")
    print(f"  under {CONDITION_FLOOR}: {len(worst)}")
    for record in sorted(rows, key=lambda r: r["täckning_vikt"])[:8]:
        print(
            f"    villkor {record['villkorsnummer']:>3}  "
            f"vikt {record['täckning_vikt']:.3f}  rak {record['täckning']:.3f}  "
            f"{record['tecken']} tecken"
        )
    held = median >= MEDIAN_FLOOR and not worst
    print(f"\n  förregistrerat villkor: {'håller' if held else 'faller'}")
    return held


def main() -> int:
    """Screen the corpus, then read the flagged decisions off the printed page."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--screen", action="store_true", help="only run the screen and stop"
    )
    args = parser.parse_args()
    if not REGISTER.exists():
        print("run pipeline/33_condition_register.py first")
        return 1
    records = [
        json.loads(line) for line in REGISTER.read_text("utf-8").splitlines() if line
    ]
    print("Sikt 1: sidor med text men utan deklarerat typsnitt")
    flagged = screen()
    print("\nSikt 2: villkorstext som förlorat å, ä och ö")
    for ident in screen_diacritics(records):
        if ident not in flagged:
            flagged.append(ident)
    if args.screen:
        return 0
    held = True
    for ident in flagged:
        mine = [r for r in records if r["id"] == ident]
        if not mine:
            print(f"\n{ident}: inga villkor i registret")
            continue
        print(f"\n{ident}: {len(mine)} villkor, läser om sidorna med Tesseract")
        recognised, confidence = recognise(ident)
        if confidence >= 0:
            print(f"  medelkonfidens {confidence}")
        held &= report(measure(ident, mine, recognised))
    return 0 if held else 1


if __name__ == "__main__":
    sys.exit(main())
