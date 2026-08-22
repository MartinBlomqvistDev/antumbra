"""Check the register of cited secrecy grounds against the deliveries.

Step 29 of the pipeline, and the only step that produces nothing. It validates
`data/sekretessgrunder.jsonl`, which is not machine generated: every row is one
authority's own sentence about what it masked and on what legal basis, copied
by hand out of the covering e-mail. The register exists because P9's criteria
are written in terms of the provision invoked, and that fact lived only as free
text inside the protocol log's notes.

**A hand-curated file needs a declared population, or it cannot carry a null.**
The criteria include one negative claim, that no authority masked class B under
30 kap. 23 §. A negative claim over an undefined set is worthless: it can always
be true of the rows that happen to be there. The population is therefore defined
here, mechanically, from `data/maskning.jsonl`: every county and class with at
least one masked document must have a row. Where the authority stated no ground
at all, the row still exists and says so, so that silence is recorded rather
than missing.

**A provision must be readable in the quote it comes from.** `citat` is verbatim
and `bestammelser` is a normalised reading of it, in the project's own spelling
rather than the authority's shorthand. Normalisation is allowed; invention is
not, so a provision whose paragraph is not quoted anywhere in the row is
reported. That failure was real: one row carried 21 kap. 1 § from a paragraph
that had not been stored.

**One row carries no message id.** Kalmar's covering e-mail of 14 August cannot
be located through the mailbox API, although the delivery is in the protocol log
and its files are on disk. Its row is flagged kalla_ej_atkomlig, which permits a
missing id and a missing quote without requiring either; the quote itself was
read out of the mailbox by hand and is present.

**This step never edits the register.** It reports what is missing and what does
not hold together, and returns non-zero, so the gap is visible in a run and in
CI rather than in someone's memory. The precedent is
`data/dgsante_annex_labels.jsonl`, the hand-read ground truth for the annex
classifier, which is likewise written by hand and likewise guarded by tests.

Usage:
    python pipeline/29_check_grounds.py
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GROUNDS = ROOT / "data" / "sekretessgrunder.jsonl"
MASKING = ROOT / "data" / "maskning.jsonl"

REQUIRED = {
    "myndighet",
    "klass",
    "meddelande_id",
    "citat",
    "bestammelser",
    "citat_fullstandigt",
    "erbjudet_beslut",
    "kalla_ej_atkomlig",
}

# The delivery folders are named after the county in a transliterated form.
# Written out rather than derived, so that a new folder fails loudly instead of
# quietly falling outside the population.
FOLDER = {
    "blekinge": "Blekinge",
    "dalarna": "Dalarna",
    "gotland": "Gotland",
    "gavleborg": "Gävleborg",
    "halland": "Halland",
    "jamtland": "Jämtland",
    "jonkoping": "Jönköping",
    "kalmar": "Kalmar",
    "kronoberg": "Kronoberg",
    "norrbotten": "Norrbotten",
    "skane": "Skåne",
    "stockholm": "Stockholm",
    "sodermanland": "Södermanland",
    "uppsala": "Uppsala",
    "varmland": "Värmland",
    "vasterbotten": "Västerbotten",
    "vasternorrland": "Västernorrland",
    "vastmanland": "Västmanland",
    "vastra_gotaland": "Västra Götaland",
    "orebro": "Örebro",
    "ostergotland": "Östergötland",
}


def masked_deliveries() -> set[tuple[str, str]]:
    """Every county and class where at least one document is masked."""
    found: set[tuple[str, str]] = set()
    for line in MASKING.read_text("utf-8").splitlines():
        row = json.loads(line)
        if not row["masked"]:
            continue
        folder = row["path"].split("/")[0]
        county, _, klass = folder.rpartition("_")
        if klass in {"A", "B"} and county in FOLDER:
            found.add((FOLDER[county], klass))
    return found


def chapter_is_quoted(provision: str, quote: str) -> bool:
    """Whether the paragraph behind a normalised provision appears in the quote.

    The authorities write the same rule several ways, "30 kap. 23 §" and
    "OSL 30:23" and "30 kap 23§", so the check looks for the two numbers next to
    each other rather than for the project's own spelling.
    """
    numbers = re.findall(r"\d+", provision)
    if len(numbers) < 2:
        # A provision named in words rather than by chapter, such as the point
        # in the annex to the ordinance. Its number must appear, and so must the
        # stem of the word it is named after, since a bare number proves little.
        stem = provision.split()[0].casefold()[:5]
        if not numbers:
            # A provision named only in words, such as the data protection
            # regulation. The word itself is all there is to look for.
            return stem in quote.casefold()
        return numbers[0] in quote and stem in quote.casefold()
    chapter, paragraph = numbers[0], numbers[1]
    # The chapter marker is written kap, kap., kapitel or a bare colon, and the
    # paragraph can sit inside a list, as in "18 kapitel 1 och 3 §§". So the
    # chapter is located first and the paragraph is looked for in the short
    # window that follows it.
    marker = re.search(rf"\b{chapter}\s*(kap\.?|kapitel|:)", quote, re.IGNORECASE)
    if not marker:
        return False
    window = quote[marker.end() : marker.end() + 40]
    return re.search(rf"\b{paragraph}\b", window) is not None


def main() -> int:
    """Report every hole in the register, and fail if there is one."""
    for path in (GROUNDS, MASKING):
        if not path.exists():
            print(f"missing {path.name}")
            return 1
    rows = [json.loads(line) for line in GROUNDS.read_text("utf-8").splitlines()]
    covered = {(r["myndighet"], r["klass"]) for r in rows}
    population = masked_deliveries()

    problems: list[str] = []
    for row in rows:
        missing_fields = REQUIRED - set(row)
        if missing_fields:
            name = f"{row.get('myndighet')} {row.get('klass')}"
            problems.append(f"{name}: saknar fält {sorted(missing_fields)}")
            continue
        if not row["citat"].strip() and not row["kalla_ej_atkomlig"]:
            problems.append(f"{row['myndighet']} {row['klass']}: tomt citat")
        for provision in row["bestammelser"]:
            if not chapter_is_quoted(provision, row["citat"]):
                problems.append(
                    f"{row['myndighet']} {row['klass']}: {provision} står i "
                    "bestammelser men syns inte i citatet"
                )

    print(f"{len(rows)} rader i registret, {len(population)} maskade leveranser")
    print(f"täckning: {len(covered & population)} av {len(population)}")

    uncovered = sorted(population - covered)
    if uncovered:
        print(f"\nmaskade leveranser utan grundrad ({len(uncovered)}):")
        for county, klass in uncovered:
            print(f"  {county} {klass}")
    extra = sorted(covered - population)
    if extra:
        print(f"\nrader utan maskad leverans ({len(extra)}): {extra}")

    if problems:
        print(f"\ninre motsägelser ({len(problems)}):")
        for problem in problems:
            print(f"  {problem}")

    unreachable = [
        f"{r['myndighet']} {r['klass']}" for r in rows if r["kalla_ej_atkomlig"]
    ]
    if unreachable:
        print(
            f"\nleveranser vars följebrev inte gått att hämta "
            f"({len(unreachable)}): {unreachable}"
        )

    incomplete = [
        f"{r['myndighet']} {r['klass']}" for r in rows if not r["citat_fullstandigt"]
    ]
    if incomplete:
        print(f"\ncitat som är avhuggna i källan ({len(incomplete)}): {incomplete}")

    ok = not uncovered and not problems
    print(f"\n{'registret är slutet' if ok else 'registret är inte slutet'}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
