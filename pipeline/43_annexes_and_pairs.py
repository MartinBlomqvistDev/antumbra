"""The two measures that are about annexes and about the same case twice.

Both were pre-registered in ``docs/BEGARANMALL.md`` and neither had been
computed. The rules are written here before the step is run.

**The annex measures.** Section 5: "Bilagor mäts som en egen klass ... **andel
bilagor helt undanhållna** och **andel bilagor levererade i bearbetat skick**.
De redovisas skilt från textmåttet, per begäran A och B, och slås aldrig ihop
med ytmåttet. Ett beslut som saknar bilaga trots att beslutstexten hänvisar till
en flaggas ``utan_bilaga``."

Three readings are needed and each is stated with what it cannot see.

1. *A delivered annex* is a file whose own name says it is one: bilaga, foto or
   bild. An annex delivered under a neutral name is invisible to this reading,
   so the count is a floor and never a ceiling.
2. *A document that refers to an annex* is one whose text names a bilaga in a
   sentence of its own. The reading is on the text layer; a scanned page without
   OCR cannot be read this way and is counted apart rather than as a nought.

   **Refined after a hand-read of 22 matches on 6 October 2026, and the
   refinement is declared rather than quiet.** The first rule counted every
   mention, and the hand-read showed two kinds that are not the same thing. A
   *substantive* reference points at content from the case: "Foton som togs
   finns i bilaga", "Bilagor, foton från kontrollen", "Bilaga tillhörande
   kontrollrapport", the checklist with the answers. A *formal* reference points
   at the paperwork every decision carries: the appeal instruction, the list of
   legislation, the note on simplified service. Only the first is an annex in
   the sense section 5 measures, and both are counted so the split is visible.
3. *Withheld* cannot be read at all, and that is the result. The difference
   between a document that refers to an annex and a county that delivered none
   looked like a measure of withholding until the sentences behind the matches
   were counted on 7 October 2026. The commonest one by far is template text in
   the national inspection report, "Vid kontrollen användes nationella
   checklistor. Foton som togs finns i bilaga", which stands there whether or
   not a photograph was taken. The material therefore cannot separate an annex
   that was held back from one that never existed, and nothing links an annex
   file to the document it belongs to. The pre-registered annex measures are
   reported as a gap with that reason, in the same way as P11's release rate,
   and the counts below are published so the reading can be checked.

**The pairs.** P1: "par där samma kontrolltillfälle förekommer i både A och B
redovisas separat", which section 13 calls the contrast's strongest comparison.
The county file names carry the case number the authority itself assigned, in
the form (12392-2025-11), where the first two parts are the case and the third
is the document inside it. A pair is the same case number present in both the
county's class A folder and its class B folder. A county that names its files
without a case number cannot be read this way, and that is reported as its own
number rather than as nought pairs.

Writes ``data/bilagor.jsonl`` and ``data/dubbelforekomst.jsonl``.
"""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DELIVERIES = ROOT / "data" / "leveranser"
MASKING = ROOT / "data" / "maskning.jsonl"
ANNEX_OUT = ROOT / "data" / "bilagor.jsonl"
PAIR_OUT = ROOT / "data" / "dubbelforekomst.jsonl"

# Reading 1: the file's own name.
ANNEX_IN_NAME = re.compile(
    r"bilaga|bilagor|foto|fotobilaga|bild(?!ning)", re.IGNORECASE
)

# Reading 2: the document's own sentence. "Bilaga 1", "se bifogad", "bifogas"
# and "enligt bilagan" are the forms the delivered documents use. A heading that
# is only the word itself is included, since a heading is the document's own
# reference as much as a sentence is.
ANNEX_IN_TEXT = re.compile(
    r"\bbilag(?:a|an|or|orna)\b|\bbifogad(?:e|a)?\b|\bbifogas\b|\bfotobilag",
    re.IGNORECASE,
)

# The window around a match, and what makes it one kind or the other. The words
# are the ones the delivered documents themselves use, read on 6 October 2026.
WINDOW = 90
SUBSTANTIVE = re.compile(
    r"foto|bild|checklist|kontrollrapport|hullklass|mät|protokoll",
    re.IGNORECASE,
)
FORMAL = re.compile(
    r"överklag|lagstiftningsförteckning|delgivning|namnunderskrift"
    # The legislation list travels under two names, and the second one has no
    # word in common with the first: "Gällande djurskyddslagstiftning samt var
    # den går att hitta finns i bilaga". Counting it as content put 33 documents
    # in the wrong class.
    r"|lagstiftning[^.]{0,60}finns i bilaga"
    r"|var den går att hitta finns i bilaga",
    re.IGNORECASE,
)

# The three kinds of reference that remain once the paperwork is out. The first
# is template text: it stands in the national inspection report whether or not
# any photograph was taken, so it cannot carry a claim that an annex is missing.
TEMPLATE_PHOTO = re.compile(r"[Ff]oton som togs finns i bilaga")
CHECKLIST_ANNEX = re.compile(r"besvarats med [^.]{0,40}finns i bilaga")

# The case number the county's own file name carries: (12392-2025-11).
CASE = re.compile(r"\((\d{3,6})-(\d{4})-(\d{1,3})\)")


def read(path: Path) -> list[dict]:
    """Every row of a JSONL file."""
    return [
        json.loads(line)
        for line in path.read_text("utf-8").splitlines()
        if line.strip()
    ]


def text_of(path: Path) -> str | None:
    """The document's text layer, or None when it has none to read."""
    import pymupdf

    try:
        with pymupdf.open(path) as document:
            text = "\n".join(page.get_text() for page in document)
    except Exception:  # pragma: no cover - a file that will not open
        return None
    return text if text.strip() else None


def classify(text: str) -> tuple[bool, bool, str | None]:
    """Whether the reference is to content or to paperwork, and of which kind."""
    substantive = formal = False
    for found in ANNEX_IN_TEXT.finditer(text):
        window = text[max(0, found.start() - WINDOW) : found.end() + WINDOW]
        if FORMAL.search(window):
            formal = True
        elif SUBSTANTIVE.search(window):
            substantive = True
    kind = None
    if substantive:
        if TEMPLATE_PHOTO.search(text):
            kind = "fotomening ur mallen"
        elif CHECKLIST_ANNEX.search(text):
            kind = "den ifyllda checklistan"
        else:
            kind = "annat"
    return substantive, formal, kind


def annex_rows(folders: list[Path]) -> list[dict]:
    """One row per county and class: annex files, references, and what that means."""
    rows = []
    for folder in folders:
        slug, _, klass = folder.name.rpartition("_")
        files = sorted(
            path for path in folder.iterdir() if path.suffix.lower() == ".pdf"
        )
        annex_files = [path for path in files if ANNEX_IN_NAME.search(path.name)]
        refers = []
        formal_only = []
        unreadable = []
        kinds: Counter[str] = Counter()
        for path in files:
            text = text_of(path)
            if text is None:
                unreadable.append(path.name)
                continue
            substantive, formal, kind = classify(text)
            if substantive:
                refers.append(path.name)
                kinds[kind or "annat"] += 1
            elif formal:
                formal_only.append(path.name)
        rows.append(
            {
                "myndighet": slug,
                "begaran": klass,
                "filer": len(files),
                "bilagefiler": len(annex_files),
                "bilagefilnamn": [path.name for path in annex_files],
                "hanvisar_till_bilaga": len(refers),
                "hanvisningens_slag": dict(kinds),
                "endast_formell_hanvisning": len(formal_only),
                "utan_lasbar_text": len(unreadable),
                # The pre-registered flag, kept because the protocol names it,
                # and reported as what it is: the document refers to an annex
                # and none was delivered. It does not say the annex was
                # withheld, because the commonest reference is template text.
                "utan_bilaga": bool(refers) and not annex_files,
                "lasning": (
                    "bilagefil läses ur filnamnet och är ett golv; hänvisning "
                    "läses ur textlagret och kan inte läsas i en skannad sida "
                    "utan OCR"
                ),
            }
        )
    return rows


def masking_by_case(masking: list[dict], slug: str) -> dict[str, dict[str, list[bool]]]:
    """One county's measured documents, grouped by case number and class."""
    out: dict[str, dict[str, list[bool]]] = {}
    for row in masking:
        folder, _, name = row["path"].partition("/")
        if not folder.startswith(f"{slug}_"):
            continue
        klass = folder.rpartition("_")[2]
        found = CASE.search(name)
        if not found:
            continue
        case = f"{found.group(1)}-{found.group(2)}"
        out.setdefault(case, {}).setdefault(klass, []).append(bool(row["masked"]))
    return out


def pair_rows(folders: list[Path], masking: list[dict]) -> list[dict]:
    """One row per county: the cases that appear in both classes, and their masking."""
    cases: dict[str, dict[str, set[str]]] = defaultdict(lambda: defaultdict(set))
    unnumbered: dict[str, int] = defaultdict(int)
    totals: dict[str, int] = defaultdict(int)
    for folder in folders:
        slug, _, klass = folder.name.rpartition("_")
        for path in folder.iterdir():
            if path.suffix.lower() != ".pdf":
                continue
            totals[slug] += 1
            found = CASE.search(path.name)
            if found:
                cases[slug][klass].add(f"{found.group(1)}-{found.group(2)}")
            else:
                unnumbered[slug] += 1

    rows = []
    for slug in sorted(set(totals)):
        both = sorted(cases[slug].get("A", set()) & cases[slug].get("B", set()))
        measured = masking_by_case(masking, slug)
        counted = {
            klass: [
                value
                for case in both
                for value in measured.get(case, {}).get(klass, [])
            ]
            for klass in ("A", "B")
        }
        rows.append(
            {
                "myndighet": slug,
                "filer": totals[slug],
                "utan_arendenummer": unnumbered[slug],
                "arenden_i_a": len(cases[slug].get("A", set())),
                "arenden_i_b": len(cases[slug].get("B", set())),
                "par": len(both),
                # P1 reports the pairs separately, and this is what separately
                # means: the same cases, the same authority, measured in both
                # classes with every other difference held still.
                "parade_dokument_a": len(counted["A"]),
                "parade_maskade_a": sum(counted["A"]),
                "parade_dokument_b": len(counted["B"]),
                "parade_maskade_b": sum(counted["B"]),
                "arendenummer": both,
            }
        )
    return rows


def main() -> int:
    """Write both registers, or print what they would contain."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true", help="skriv ingenting")
    args = parser.parse_args()

    if not DELIVERIES.exists():
        raise SystemExit(f"{DELIVERIES} saknas; leveranserna ligger utanför git")

    folders = sorted(
        path
        for path in DELIVERIES.iterdir()
        if path.is_dir() and path.name.rpartition("_")[2] in {"A", "B"}
    )
    annexes = annex_rows(folders)
    pairs = pair_rows(folders, read(MASKING))

    print(f"mappar: {len(folders)}")
    print(f"bilagefiler: {sum(row['bilagefiler'] for row in annexes)}")
    refers = sum(row["hanvisar_till_bilaga"] for row in annexes)
    print(f"dokument som hänvisar till en bilaga: {refers}")
    print(f"utan läsbar text: {sum(row['utan_lasbar_text'] for row in annexes)}")
    withheld = sum(1 for row in annexes if row["utan_bilaga"])
    print(f"län och klasser med hänvisning men ingen bilagefil: {withheld}")
    counties = sum(1 for row in pairs if row["par"])
    print(f"par: {sum(row['par'] for row in pairs)} i {counties} län")
    for row in pairs:
        if row["par"]:
            print(
                f"  {row['myndighet']}: klass A {row['parade_maskade_a']} av "
                f"{row['parade_dokument_a']} maskade, klass B "
                f"{row['parade_maskade_b']} av {row['parade_dokument_b']}"
            )
    print(f"filer utan ärendenummer: {sum(row['utan_arendenummer'] for row in pairs)}")

    if args.dry_run:
        return 0

    for path, rows in ((ANNEX_OUT, annexes), (PAIR_OUT, pairs)):
        path.write_bytes(
            (
                "\n".join(json.dumps(row, ensure_ascii=False) for row in rows) + "\n"
            ).encode("utf-8")
        )
        print(f"{len(rows)} rader skrivna till {path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
