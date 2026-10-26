"""Classify the numbered annexes from the older DG SANTE era.

Step 05 of the pipeline; run 03_download_reports.py first. The annexes
labelled only "1", "2", "3" carry no title that says what they are, so they
must not be counted as action plans on the strength of their position. This
step opens each one, extracts what text it has and assigns a class from the
document's own wording.

Every record carries how the class was derived and the quoted evidence for
it, so a reader can check the call instead of trusting it. Files with no
extractable text are classed as needing OCR rather than guessed at.

**The quoted evidence carries no e-mail addresses.** The annexes are letters,
and a letter's head holds the writer's address. Three of the 1 974 hold a named
official's own work address. ADR-0018 keeps officials' names in the source
document, and a file this project commits is not the source document, so the
stored excerpt replaces every address with a marker. The evidence exists to show
the phrase the class was read from, and that phrase never needs an address
beside it. 29 of the 1 974 excerpts change.

**Telephone numbers are left as they stand, and that was measured rather than
assumed.** A screen wide enough to catch how 27 countries write their numbers
changed 220 excerpts and ate what it was not aimed at, among them the mission
reference `602/287 03-18` and dates written as two digit groups. The numbers in
these letter heads are switchboards and fax lines printed on the authority's own
letterhead, so the screen would have cost evidence without removing anyone's
personal detail. The excerpt is otherwise verbatim, and both calls are measured
in `docs/VERIFIERAT.md`.

Writes data/dgsante_annex_classes.jsonl, one line per numbered annex.

Usage:
    python pipeline/05_classify_annexes.py
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from html import unescape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "data" / "dgsante_manifest.jsonl"
OUT = ROOT / "data" / "dgsante_annex_classes.jsonl"
OCR_DIR = ROOT / "ocr" / "dgsante"

IMAGE_FORMATS = {".gif", ".jpg", ".jpeg", ".tif", ".tiff"}
# The e-mail address a letter's head carries, replaced in the stored excerpt.
# The shape is exact, so it takes addresses and nothing else.
ADDRESS = re.compile(r"[\w.\-]+@[\w.-]+\.[a-z]{2,}", re.IGNORECASE)
MIN_CHARS = 40

# A document is classed on how it introduces itself, leaving aside words that
# happen
# to appear somewhere inside it. Only this many leading characters are matched:
# "action plan" in the body of a member state's comments is the discussion of a
# plan where a plan is wanted, and matching the whole text would silently turn
# one into the
# other. That is exactly the miscount docs/DGSANTE.md warns against.
HEAD_CHARS = 800

# Every official language's word for a draft report, used by the structural
# fallback below together with the mission reference.
DRAFT_WORDS = (
    "draft",
    "projet",
    "proyecto",
    "progetto",
    "projecto",
    "projeto",
    "projekt",
    "entwurf",
    "ontwerp",
    "concept",
    "udkast",
    "luonnos",
    "utkast",
    "raporttiluonnos",
    "predlog",
    "navrh",
    "návrh",
)

# Order matters: the first pattern that matches wins, so the most specific
# comes first. Each rule carries its own window: action_plan gets a narrow
# title zone because a letter that says it is "preparing an action plan" is
# correspondence about a plan where the plan is wanted, and a wide window turns
# one into
# the other. Two such false positives were found by held-out sampling.
TITLE_CHARS = 200

# Rules are tried in this order, which is not the order they are written in
# below. The
# two response classes go first so that a document titled "actions taken in
# response to draft report" is read as a response rather than as comments:
# the word "comments" is broad enough to swallow them otherwise.
PRECEDENCE = (
    "actions_taken_response",
    "action_plan",
    "comments_on_draft_report",
    "legal_text",
    "correspondence",
    "data_table",
)

RULES: tuple[tuple[str, tuple[str, ...], int], ...] = (
    (
        "comments_on_draft_report",
        (
            "on the draft report",
            "on draft report",
            "to the draft report",
            "to the mission report",
            "comments on the report",
            "comments on main findings",
            "comments on the main findings",
            "concept-rapport",
            "projektu raportu",
            "projecto de relat",
            "proyecto de informe",
            "observaciones al documento",
            "stellungnahme",
            "bemrerkninger",
            "bemaerkninger",
            "bemærkninger",
            "reacties op",
            "huomautukset",
            "observations on the text of draft report",
            "comments of the competent authority",
            "competent authority comments",
            "correction requested",
            "errori di traduzione",
            "osservazioni",
            "observaciones al proyecto",
            "al proyecto de informe",
            "commentaires sur le projet",
            "projet de rapport",
            "bemerkungen zum entwurf",
            "entwurf des berichts",
            "opmerkingen bij het ontwerp",
            "draft report",
            "mission report",
            "raportu",
        ),
        HEAD_CHARS,
    ),
    (
        # Kept apart from action_plan on the documents' own terms: these list
        # steps already taken, and several say in as many words that the plan
        # itself will follow later. Merging the two would overstate how often
        # the recommendation-to-commitment chain actually closes.
        "actions_taken_response",
        (
            "actions to the recommendations",
            "actions already taken",
            "action taken in response",
            "actions taken in response",
            "competent authority response",
        ),
        TITLE_CHARS,
    ),
    (
        "action_plan",
        (
            "action plan",
            "plan of action",
        ),
        TITLE_CHARS,
    ),
    (
        "legal_text",
        (
            "regulation (ec)",
            "council directive",
            "official journal",
            "ministerial decree",
            "maa- ja metsätalousministeriön",
            "förordning",
            "verordnung",
            "decreto",
        ),
        TITLE_CHARS,
    ),
    (
        "correspondence",
        (
            "dear sir",
            "dear mr",
            "dear ms",
            "yours sincerely",
            "yours faithfully",
            "please find attached",
            "please find enclosed",
            "with reference to your letter",
            "telefax",
            "fax no",
            "number of pages",
            "food and veterinary office",
            "your ref",
            "our ref",
            "votre r",
            "unser zeichen",
        ),
        HEAD_CHARS,
    ),
    (
        "data_table",
        (
            "list of establishments",
            "number of samples",
            "results of analyses",
        ),
        HEAD_CHARS,
    ),
)


def pdf_text(path: Path) -> str:
    """Extract text from a PDF, preferring pdftotext and falling back to pypdf.

    Args:
        path: PDF on disk.

    Returns:
        Extracted text, empty when the PDF carries no text layer.
    """
    try:
        done = subprocess.run(
            ["pdftotext", "-layout", "-q", str(path), "-"],
            capture_output=True,
            text=True,
            errors="replace",
            timeout=120,
            check=False,
        )
        if done.stdout.strip():
            return done.stdout
    except (OSError, subprocess.SubprocessError):
        pass
    try:
        from pypdf import PdfReader

        reader = PdfReader(str(path))
        return "\n".join((page.extract_text() or "") for page in reader.pages)
    except Exception:
        return ""


def html_text(path: Path) -> str:
    """Extract visible text from an HTML annex, dropping style and script."""
    raw = path.read_text(encoding="utf-8", errors="replace")
    raw = re.sub(r"<(style|script)[^>]*>.*?</\1>", " ", raw, flags=re.S | re.I)
    return re.sub(r"\s+", " ", unescape(re.sub(r"<[^>]+>", " ", raw)))


def extract(path: Path) -> str:
    """Extract whatever text a downloaded annex carries.

    A scanned annex has no text of its own. When step 06 has read one, its
    output is used here instead, so that re-running this step reclassifies
    what OCR made readable.
    """
    suffix = path.suffix.lower()
    if suffix == ".pdf":
        text = pdf_text(path)
        if text.strip():
            return text
    elif suffix in {".html", ".htm"}:
        return html_text(path)
    sidecar = OCR_DIR / (path.stem + ".txt")
    if sidecar.exists():
        return sidecar.read_text(encoding="utf-8", errors="replace")
    return ""


def classify(text: str, suffix: str) -> tuple[str, str, str]:
    """Assign a class from how the document introduces itself.

    Args:
        text: Extracted text, possibly empty.
        suffix: Lowercase file extension, used to explain empty text.

    Returns:
        The class, the derivation method and the quoted evidence. Anything
        that cannot be read or does not name itself is left unclassified
        rather than guessed at.
    """
    if len(text.strip()) < MIN_CHARS:
        if suffix in IMAGE_FORMATS:
            return "needs_ocr", "image_without_text_layer", ""
        if suffix == ".doc":
            return "needs_conversion", "legacy_word_binary", ""
        return "needs_ocr", "pdf_without_text_layer", ""
    # Collapse whitespace before measuring: pdftotext -layout pads with runs
    # of spaces, which would otherwise push a document's own title out of the
    # title zone and hide it from the narrow rules.
    head = re.sub(r"\s+", " ", text).strip()[:HEAD_CHARS]
    lowered = head.lower()
    for name, patterns, window in sorted(RULES, key=lambda r: PRECEDENCE.index(r[0])):
        for pattern in patterns:
            position = lowered.find(pattern, 0, window)
            if position != -1:
                start = max(0, position - 60)
                quote = re.sub(r"\s+", " ", head[start : position + 120]).strip()
                return name, f"head_phrase:{pattern}", quote

    # Language-independent fallback. The member states comment in every
    # official language, so a phrase list will never cover them all; what
    # every such document does carry is the mission reference next to its own
    # language's word for "draft". Structure generalises where vocabulary
    # does not.
    reference = re.search(r"dg\s*\(?sanco\)?\s*/?\s*\d{3,4}\s*/\s*\d{4}", lowered)
    if reference:
        for word in DRAFT_WORDS:
            if word in lowered:
                quote = re.sub(r"\s+", " ", head[: reference.end() + 80]).strip()
                return (
                    "comments_on_draft_report",
                    f"reference_and_draft_word:{word}",
                    quote,
                )
    return "unclassified_text", "no_pattern_matched_in_head", ""


def main() -> int:
    """Classify every numbered annex and write one record each."""
    rows = [
        json.loads(line)
        for line in MANIFEST.read_text(encoding="utf-8").splitlines()
        if line
    ]
    numbered = [
        r for r in rows if r["kind"] == "annex" and r.get("title", "").strip().isdigit()
    ]
    records = []
    for i, row in enumerate(numbered, start=1):
        path = ROOT / row["path"]
        suffix = path.suffix.lower()
        text = extract(path)
        name, method, evidence = classify(text, suffix)
        records.append(
            {
                "path": row["path"],
                "ref": row["ref"],
                "country": row["country"],
                "annex_number": int(row["title"].strip()),
                "format": suffix.lstrip("."),
                "chars": len(text.strip()),
                "class": name,
                "method": method,
                "evidence": ADDRESS.sub("[e-postadress]", evidence)[:300],
            }
        )
        if i % 250 == 0:
            print(f"{i}/{len(numbered)} classified", flush=True)

    with open(OUT, "w", encoding="utf-8", newline="\n") as fh:
        for record in records:
            fh.write(json.dumps(record, ensure_ascii=False) + "\n")

    counts: dict[str, int] = {}
    for record in records:
        counts[record["class"]] = counts.get(record["class"], 0) + 1
    print(f"{len(records)} rows -> {OUT.relative_to(ROOT)}")
    for name, count in sorted(counts.items(), key=lambda kv: -kv[1]):
        print(f"  {name}: {count}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
