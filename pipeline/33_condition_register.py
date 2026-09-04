"""Write the conditions themselves, verbatim, with the heading each sits under.

Step 33 of the pipeline, and the first slice of the register that
docs/VILLKORSSCHEMA.md designs. Step 24 answers whether the conditions are
boilerplate and keeps only a hash, because that question needs no text. This
step keeps the text, because the questions after it do: what each permit
division regulates, in what words, and with which requirements.

**The text is the measurement object, so it is stored as written.** Section 2.7
of VILLKORSSCHEMA settles that: names of natural persons, officials, agents and
distribution lists stay out, while the condition text itself "lagras ordagrant
eftersom den är själva mätobjektet". Step 24's rows carry the case folded form,
which is right for comparing two conditions and wrong for quoting one, so this
step takes the raw text from the same segmenter and leaves the folding to the
measure that needs it.

**The step screens before it writes, and refuses rather than warns.** The
guarantee that no personal data enters the repository cannot rest on someone
having checked once. Every condition is searched for e-mail addresses,
personnummer and telephone numbers, and the step exits without writing if it
finds any, naming the rows. When the screen was first run on 4 September 2026 it
found 79 such strings, all of them the county boards' own switchboards and
registry addresses, carried in by a page footer that a condition running across
a page break had swallowed. Step 24 drops those lines now, and the screen is
what keeps them out.

**One segmenter, two outputs.** This step imports step 24 rather than repeating
its rules, so a change to how a condition is found cannot reach one file and
miss the other. The row carries the same `text_hash` as the baseline, which is
what joins them.

Writes data/villkor.jsonl, one row per condition.

Usage:
    python pipeline/33_condition_register.py
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import re
import sys
from pathlib import Path
from types import ModuleType

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "pdf" / "jordbruksverket"
MANIFEST = ROOT / "data" / "tillstand_manifest.jsonl"
TYPES = ROOT / "data" / "tillstand_typ.jsonl"
OUT = ROOT / "data" / "villkor.jsonl"

# What may never reach the repository. The name test is deliberately absent:
# a capitalised pair is a place, an authority or a statute far more often than a
# person, and a check that cries wolf is a check nobody reads. The three below
# are unambiguous, and they are the shapes the corpus actually carried.
FORBIDDEN = {
    "e-postadress": re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-z]{2,}"),
    "personnummer": re.compile(r"\b(?:19|20)\d{6}[-+]\d{4}\b"),
    "telefonnummer": re.compile(r"\b0\d{1,3}[-\s]\d{2,3}\s?\d{2}\s?\d{2}\b"),
}


def load_step24() -> ModuleType:
    """Step 24 as a module, since a name starting with a digit cannot be imported."""
    path = ROOT / "pipeline" / "24_condition_baseline.py"
    spec = importlib.util.spec_from_file_location("condition_baseline", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def read(path: Path, field: str) -> dict[str, str]:
    """One field per decision identifier, from a jsonl file."""
    if not path.exists():
        return {}
    rows = (json.loads(line) for line in path.read_text("utf-8").splitlines() if line)
    return {row["id"]: row[field] for row in rows}


def main() -> int:
    """Segment every decision and write its conditions with their text."""
    if not MANIFEST.exists():
        print("run pipeline/23_download_permits.py first")
        return 1
    step24 = load_step24()
    groups = read(MANIFEST, "prövningsgrupp")
    kinds = read(TYPES, "typ")

    records = []
    for path in sorted(SOURCE.glob("*.pdf")):
        if path.stem not in groups:
            continue
        text, origin = step24.document_text(path)
        if not origin:
            continue
        window = step24.section(text.split("\n"))
        if not window:
            continue
        for position, (number, body, heading) in enumerate(
            step24.conditions(window), 1
        ):
            folded = step24.normalise(body)
            records.append(
                {
                    "id": path.stem,
                    "prövningsgrupp": groups[path.stem],
                    "beslutstyp": kinds.get(path.stem),
                    "villkorsnummer": number,
                    # Where in the section the condition stood. Two conditions
                    # can carry the same number in one decision, so the number
                    # alone does not identify a row.
                    "position": position,
                    "rubrik": heading,
                    "text": body,
                    "tecken": len(folded),
                    "källa": origin,
                    "text_hash": hashlib.sha256(folded.encode("utf-8")).hexdigest()[
                        :16
                    ],
                }
            )

    offenders = []
    for record in records:
        for label, pattern in FORBIDDEN.items():
            if pattern.search(record["text"]):
                offenders.append(
                    f"{record['id']} villkor {record['villkorsnummer']}: {label}"
                )
    if offenders:
        print(f"{len(offenders)} villkor bär uppgifter som inte får committas:")
        for offender in offenders[:20]:
            print(f"  {offender}")
        print("inget skrivet")
        return 1

    with OUT.open("w", encoding="utf-8", newline="\n") as out:
        for record in records:
            out.write(json.dumps(record, ensure_ascii=False) + "\n")

    decisions = len({r["id"] for r in records})
    with_heading = sum(1 for r in records if r["rubrik"])
    print(f"{len(records)} villkor i {decisions} beslut -> {OUT.name}")
    print(f"  med rubrik: {with_heading}")
    print(f"  screeningen passerad: {', '.join(FORBIDDEN)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
