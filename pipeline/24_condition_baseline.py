"""Test whether permit conditions are standard text before building anything.

Step 24 of the pipeline, and the gate the conditions layer has to pass. STATUS
puts it before extraction for a reason: if the conditions in the permit
decisions are boilerplate reused across installations, then a register of them
describes a template, and that is the result. If they differ, the register
measures something, and the work of building it is justified. Deciding this
first costs two days; discovering it after the extractor is built costs weeks.

**The page footer is dropped, because a condition that runs across a page
break swallows it.** Every county board prints the same block of address,
switchboard and registry lines at the foot of the page, and the text layer puts
it in the middle of whatever condition spans the break. It sat inside 54 of the
2 347 conditions on 4 September 2026, one per affected decision, adding about
150 characters each. It was found by screening every condition for personal
data before the text could be stored: the only e-mail addresses, telephone
numbers and personnummer-shaped strings in the whole corpus were the boards'
own, and all of them arrived this way.

**The conditions section is bounded, not searched for everywhere.** A first
version segmented on any line opening with a number and a full stop, anywhere
in the document, and 12 decisions of 144, 8 per cent, then produced an unbroken
1..N series of condition numbers. Numbered lists live all over these decisions,
in the account of the case and in the closing information, so that measure was
taken over a mixture of conditions and other text. This version finds the
conditions heading, reads until the next section heading, and segments only
inside that window: 108 of 123, 88 per cent, then produce an unbroken series.
The heading list and the stop list are heuristics over the layouts actually
present in the corpus, and VILLKORSSCHEMA section 2.2 already records that
headings vary and can be absent.

**Two of the openers are fallbacks, added on 4 September 2026.** Reading the
seven permits that carried no conditions showed that five of them open the
section without a heading line: four introduce it with a sentence, "För
tillståndet gäller följande villkor: 1. ...", and one has a text layer that runs
the heading into the next word. Both fallbacks are tried only when no heading
line exists anywhere in the document, so a decision that segmented before keeps
the code path it had. The condition set before the change was written down and
compared afterwards: seven decisions entered and none lost a condition.

**What this step is not.** It does not classify conditions by type, parse
quantified requirements or resolve the decision's identity. It reaches only the
decisions whose conditions section can be located, which is the limit that
decides coverage. That limit is counted and printed with the result rather than
hidden behind it.

**The measure.** Two condition texts count as the same when they are identical
after case folding and whitespace collapsing, and nothing else is normalised.
Numbers are deliberately kept: 40 dB(A) and 45 dB(A) are different conditions,
and a similarity threshold that hides that difference would answer a question
nobody asked. ADR-0013 chose containment over similarity for a directional
question; this question is symmetric, so exact match after normalisation is the
conservative instrument, and it can only understate reuse.

**Verification is check 1 from VILLKORSSCHEMA section 5**, the numbers forming
the series 1..N. Every decision carries the outcome as series_ok, and the
reuse figures are reported over the clean subset as well as over everything, so
that a segmentation failure cannot carry the headline.

**The check does not apply to amendment decisions, and the row says so.** An
amendment that changes conditions 1, 3 and 8 in an earlier permit is correctly
extracted as 1, 3 and 8, so a gap is the right answer and not a fault. Reading
seven amendments by hand on 4 September 2026 showed three shapes: a full set
numbered from 1, a consecutive run appended after the base permit's last number,
and a scattered set of the conditions being changed. Only the first is testable
by the series. The field `serie_prövas` carries that judgement per decision, the
type comes from step 31, and every decision keeps its raw `series_ok` so that
nothing downstream changes meaning. Where the type is unknown the check is
applied, since that is the stricter reading.

**Born-digital and OCR text are never pooled into the headline.** Step 25 reads
the scans, and every row records which source it came from. OCR breaks words
across line ends and loses characters, so two identical conditions seldom
survive as identical strings once one has been read by OCR. A pooled reuse share
would therefore fall for an instrument reason and not a factual one. The
born-digital figure is printed first and labelled as the headline, the OCR set
is reported beside it, and the pooled figure is printed last carrying nothing.

**Reuse staying inside one permit division is tested against chance.** Two
divisions hold half the corpus, so a shared text landing inside one division is
common by chance and the raw count means nothing on its own. The clusters are
re-drawn from the same decisions with their sizes kept, which holds the division
sizes fixed and destroys only the association, and the observed count is placed
against that distribution. Baseline before conclusion, as everywhere else here.

Writes data/villkor_baseline.jsonl, one row per extracted condition, carrying a
hash of the normalised text and never the text itself, since the corpus is
outside version control for good reasons.

Usage:
    python pipeline/24_condition_baseline.py
"""

from __future__ import annotations

import hashlib
import json
import random
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

import pymupdf

ROOT = Path(__file__).resolve().parent.parent
# Written by step 31. Optional: without it every decision is tested, which is
# the stricter reading and the behaviour this step had before 4 September 2026.
TYPES = ROOT / "data" / "tillstand_typ.jsonl"
# The one type whose numbering is inherited from another decision, so that a
# gap carries no information about this extraction.
SERIES_NOT_TESTED = frozenset({"ändring"})
SOURCE = ROOT / "pdf" / "jordbruksverket"
MANIFEST = ROOT / "data" / "tillstand_manifest.jsonl"
OCR_DIR = ROOT / "ocr" / "tillstand"
OCR_INDEX = ROOT / "data" / "tillstand_ocr_index.jsonl"
OUT = ROOT / "data" / "villkor_baseline.jsonl"

MIN_CHARS_PER_PAGE = 200
MIN_CONDITION_CHARS = 40
MAX_CONDITION_CHARS = 4000

# The permutation that tells a real concentration from a size effect. Fixed so
# the figure in docs/VERIFIERAT.md can be reproduced exactly.
PERMUTATIONS = 2000
SEED = 20260817

# The heading that opens the conditions section, in the forms the corpus uses.
SECTION_START = re.compile(
    r"^(villkor|följande villkor|villkor för (tillståndet|verksamheten))\b[\s:.]*$",
    re.IGNORECASE,
)
# The headings that end it. A stop word only takes effect once at least one
# line has been read, so a decision that repeats the word Villkor immediately
# under its own heading is not cut off at once.
SECTION_STOP = re.compile(
    r"^(redogörelse|motivering|skäl(en)?\b"
    r"|miljöprövningsdelegationens (skäl|bedömning)"
    r"|upplysning|hur man överklagar|överklagande|kungörelse"
    r"|beskrivning av ärendet|bakgrund|ärendets handläggning"
    r"|sökandens|yttrande|delgivning|avgift|bilaga|sändlista|kopia"
    r"|detta beslut|information)",
    re.IGNORECASE,
)
# Two fallbacks for a section that never gets a heading line of its own. They
# are tried only when SECTION_START matches nothing in the document, so a
# decision that segments today cannot lose a condition to them.
#
# The first is a heading that the text layer glued to the sentence after it, as
# in "Villkor för verksamhetenMiljöprövningsdelegationen fastställer med stöd
# av". The second is a section introduced by a sentence rather than a heading,
# "För tillståndet gäller följande villkor: 1. ...", which is how the four
# OCR-read permits in the hand reading of 4 September 2026 open theirs. The verb
# is required so that the motivation's own "Bolaget har föreslagit följande
# villkor" cannot open a section.
# No word boundary after the heading: the case this rule exists for is a text
# layer that runs the heading straight into the next word.
SECTION_PREFIX = re.compile(
    r"^villkor för (?:tillståndet|verksamheten)[\s:.]*(.*)$", re.IGNORECASE
)
SECTION_INTRO = re.compile(
    r"(?:gäller|meddelas|föreskrivs)\s+följande villkor\s*[:.]?\s*(.*)$",
    re.IGNORECASE,
)

# The page footer, which a condition running across a page break otherwise
# swallows. Every county board prints the same block: postal and visiting
# address, switchboard, fax, bank giro, registry address and web address. On
# 4 September 2026 it sat inside 54 of 2 347 conditions, one per decision, and
# added about 150 characters to each. Dropping the line is safe because the
# markers are page furniture: a condition that mentions an address states it in
# prose, not in a column of labels.
PAGE_FOOTER = re.compile(
    r"postadress|bes[öo]ksadress|bankgiro|plusgiro|telefax|v[äa]xel"
    r"|\borg\.? ?nr\b|organisationsnummer|www\.|@|\bvx\b|hemsida|webbadress"
    # Added 5 September 2026, after step 33 refused to write the register.
    # These are the naked continuation lines of the same block, plus the
    # page number, which sits in the same place and breaks a condition the
    # same way. Each was counted and sampled against the corpus first: 24
    # telephone lines, 26 postcode lines, 3 fax lines and 418 page numbers,
    # and a sample of 22 of the last held nothing but page furniture.
    r"|\b0\d{1,3}[-\s]\d{2,3}\s?\d{2}\s?\d{2}\b"
    r"|\b\d{3} ?\d{2} [A-ZÅÄÖ][A-ZÅÄÖa-zåäö]{2,}"
    r"|\(fax\)|telefon/fax"
    r"|\bsid(a|an)?\.? ?\d|\b\d{1,2} ?\( ?\d{1,2} ?\)",
    re.IGNORECASE,
)

# A condition opens with its number. The text can follow on the same line or on
# the next one, which is how the decisions that amend a single condition are set.
CONDITION_START = re.compile(r"^(\d{1,2})[.)]\s*(.*)$")

# A section heading between two conditions, recognised by shape rather than by a
# word list, so that a county's own wording is caught as well as the ones
# VILLKORSSCHEMA section 2.2 lists. It is a short line that does not open a
# condition, does not end like a sentence, and is followed by a line that does
# open one. Before 5 September 2026 such a line was read as the tail of the
# condition above it, which put the next section's heading inside 471 of 2 347
# condition texts and lost the heading the schema asks for.
HEADING_MAX_CHARS = 60
HEADING_ENDINGS = (".", ":", ",", ";")

# What such a line has to look like before it is recorded as a heading. The
# structural rule above removes the line either way, since it is not part of the
# condition; this decides whether it is also a name for what follows. The
# exclusions are the page furniture the corpus actually carries, found by
# reading the 231 candidates the structural rule produced on 5 September 2026:
# page numbers as "2(16)", case numbers as "551-4691-17", facility numbers as
# "1382-90-004", dates, and running headers naming the authority.
NOT_A_HEADING = re.compile(
    r"\d+\s*\(\s*\d+\s*\)"  # page number, "3 (17)"
    r"|^\s*(sid|sida|s\.)\s*\d"  # "sid 2"
    r"|\bdnr\b"
    r"|\d{4}-\d{2}-\d{2}"  # a date
    r"|\blänsstyrelsen\b"
    r"|\|",
    re.IGNORECASE,
)
# A heading is words. An identifier is digits with separators, and the two are
# told apart by which of them the line is mostly made of.
HEADING_MIN_LETTERS = 3


def normalise(text: str) -> str:
    """Case folded with whitespace collapsed, and nothing else changed."""
    return re.sub(r"\s+", " ", text).strip().casefold()


def document_text(path: Path) -> tuple[str, str]:
    """The text of one decision and where it came from.

    A born-digital text layer is preferred. A scan has none, and then step 25's
    OCR output is used if it exists. Which of the two a decision was read from
    is carried through to every row, because OCR text segments worse and a
    figure that pooled the two silently would hide that.
    """
    with pymupdf.open(path) as document:
        pages = len(document)
        text = "\n".join(page.get_text() for page in document)
    if len(text) >= MIN_CHARS_PER_PAGE * pages:
        return text, "text"
    recognised = OCR_DIR / f"{path.stem}.txt"
    if recognised.exists():
        return recognised.read_text("utf-8"), "ocr"
    return "", ""


def read_on(lines: list[str], start: int, first: str = "") -> list[str]:
    """The section from a given line, stopping at the next section heading.

    `first` is what remained of the opening line after the heading or the
    introducing sentence, which is where the first condition sits when the
    section opens mid-line.
    """
    out: list[str] = [first] if first else []
    for candidate in lines[start:]:
        stripped = candidate.strip()
        if out and SECTION_STOP.match(stripped):
            break
        if PAGE_FOOTER.search(stripped):
            continue
        out.append(stripped)
    return out


def section(lines: list[str]) -> list[str]:
    """The lines of the conditions section, or empty if no opening is found."""
    for index, line in enumerate(lines):
        if SECTION_START.match(line.strip()):
            return read_on(lines, index + 1)
    # Only now the fallbacks, so the safest opener always wins.
    for index, line in enumerate(lines):
        stripped = line.strip()
        prefix = SECTION_PREFIX.match(stripped)
        if prefix:
            return read_on(lines, index + 1, prefix.group(1).strip())
        intro = SECTION_INTRO.search(stripped)
        if intro:
            return read_on(lines, index + 1, intro.group(1).strip())
    return []


def between_conditions(line: str, following: str) -> bool:
    """Whether a line sits between two conditions and belongs to neither."""
    line = line.strip()
    if not line or CONDITION_START.match(line):
        return False
    if len(line) > HEADING_MAX_CHARS or line.endswith(HEADING_ENDINGS):
        return False
    return bool(CONDITION_START.match(following.strip()))


def is_heading(line: str) -> bool:
    """Whether such a line names what the conditions below regulate."""
    line = line.strip()
    if NOT_A_HEADING.search(line):
        return False
    letters = sum(character.isalpha() for character in line)
    digits = sum(character.isdigit() for character in line)
    return letters >= HEADING_MIN_LETTERS and letters > digits


def conditions(lines: list[str]) -> list[tuple[int, str, str | None]]:
    """Number, text and heading of every condition in the bounded section."""
    found: list[tuple[int, str, str | None]] = []
    number: int | None = None
    current: list[str] = []
    heading: str | None = None
    for position, line in enumerate(lines):
        following = lines[position + 1] if position + 1 < len(lines) else ""
        match = CONDITION_START.match(line)
        if match:
            if number is not None and current:
                found.append((number, " ".join(current), heading))
            number = int(match.group(1))
            current = [match.group(2)] if match.group(2) else []
        elif between_conditions(line, following):
            # The line belongs to what comes after it, so the condition above is
            # closed here rather than swallowing it. Only a line that reads as a
            # name is kept as the heading; a page number is dropped and leaves
            # the previous heading standing.
            if number is not None and current:
                found.append((number, " ".join(current), heading))
                number, current = None, []
            if is_heading(line):
                heading = line.strip()
        elif number is not None:
            if not line:
                if current:
                    found.append((number, " ".join(current), heading))
                number, current = None, []
            else:
                current.append(line)
    if number is not None and current:
        found.append((number, " ".join(current), heading))
    # The text is returned as it stands in the decision. Normalising is the
    # reuse measure's business, and a register that quotes a condition needs the
    # wording the authority wrote. Step 33 reads this function for that reason.
    return [
        (n, t, h)
        for n, t, h in found
        if MIN_CONDITION_CHARS <= len(normalise(t)) <= MAX_CONDITION_CHARS
    ]


def series_ok(numbers: list[int]) -> bool:
    """Check 1 of VILLKORSSCHEMA section 5: the numbers form 1..N once each."""
    return sorted(numbers) == list(range(1, max(numbers) + 1))


def group_concentration(
    shared: dict[str, set[str]], groups: dict[str, str], decisions: list[str]
) -> str:
    """Whether reuse staying inside one permit division is more than size.

    Half the corpus sits in two divisions, so a shared text landing inside
    one division is common by chance alone. The clusters are re-drawn
    from the same decisions, keeping every cluster's size, which holds the
    division sizes fixed and destroys only the association.
    """
    observed = sum(1 for ids in shared.values() if len({groups[i] for i in ids}) == 1)
    pool = [groups[i] for i in decisions]
    sizes = [len(ids) for ids in shared.values()]
    rng = random.Random(SEED)
    draws = sorted(
        sum(1 for k in sizes if len(set(rng.sample(pool, k))) == 1)
        for _ in range(PERMUTATIONS)
    )
    at_least = sum(1 for d in draws if d >= observed)
    # No permutation reaching the observed count gives a bound, never a zero.
    p = f"= {at_least / PERMUTATIONS:.4f}" if at_least else f"< {1 / PERMUTATIONS:.4f}"
    return (
        f"  inom en enda prövningsgrupp: {observed} av {len(shared)}\n"
        f"  slumpbaslinje över {PERMUTATIONS} permutationer: väntat "
        f"{sum(draws) / len(draws):.1f}, 95:e percentilen "
        f"{draws[int(0.95 * len(draws))]}, p {p}"
    )


def reuse(records: list[dict], groups: dict[str, str]) -> str:
    """How much condition text repeats across decisions, as a printable block."""
    by_hash: dict[str, set[str]] = defaultdict(set)
    for record in records:
        by_hash[record["text_hash"]].add(record["id"])
    shared = {h: ids for h, ids in by_hash.items() if len(ids) > 1}
    repeated = sum(1 for r in records if len(by_hash[r["text_hash"]]) > 1)
    inside = sum(1 for ids in shared.values() if len({groups[i] for i in ids}) == 1)

    # Short shared fragments would be a different finding from shared
    # conditions, so the two lengths are reported side by side.
    lengths = {r["text_hash"]: r["tecken"] for r in records}
    shared_len = sorted(lengths[h] for h in shared)
    own_len = sorted(lengths[h] for h in by_hash if h not in shared)

    own = Counter()
    total = Counter()
    for record in records:
        total[record["id"]] += 1
        if len(by_hash[record["text_hash"]]) == 1:
            own[record["id"]] += 1
    shares = sorted(own[i] / total[i] for i in total)
    middle = shares[len(shares) // 2] if shares else 0.0

    return (
        f"  {len(records)} villkor i {len(total)} beslut, "
        f"{len(by_hash)} olika texter\n"
        f"  delad text: {repeated} villkor ({repeated / len(records):.0%}), "
        f"{len(shared)} texter i mer än ett beslut, "
        f"{inside} av dem inom en enda prövningsgrupp\n"
        f"  andel egna villkor per beslut: median {middle:.0%}, "
        f"beslut utan eget villkor {sum(1 for s in shares if s == 0.0)}, "
        f"beslut med bara egna {sum(1 for s in shares if s == 1.0)}\n"
        f"  längd i tecken: delade texter median "
        f"{shared_len[len(shared_len) // 2] if shared_len else 0}, "
        f"egna median {own_len[len(own_len) // 2] if own_len else 0}, "
        f"delade under 80 tecken {sum(1 for x in shared_len if x < 80)}\n"
        + group_concentration(shared, groups, sorted(total))
    )


def main() -> int:
    """Segment the readable decisions and report how much text repeats."""
    if not MANIFEST.exists():
        print("run pipeline/23_download_permits.py first")
        return 1
    groups = {
        json.loads(line)["id"]: json.loads(line)["prövningsgrupp"]
        for line in MANIFEST.read_text("utf-8").splitlines()
    }
    kinds: dict[str, str] = {}
    if TYPES.exists():
        kinds = {
            json.loads(line)["id"]: json.loads(line)["typ"]
            for line in TYPES.read_text("utf-8").splitlines()
            if line
        }

    records: list[dict] = []
    no_text = no_heading = no_conditions = unlisted = 0
    clean: set[str] = set()
    for path in sorted(SOURCE.glob("*.pdf")):
        # A file the manifest does not know has no permit division, and the
        # concentration test cannot place it. Counted and skipped, never
        # silently assigned to an empty division.
        if path.stem not in groups:
            unlisted += 1
            continue
        text, origin = document_text(path)
        if not origin:
            no_text += 1
            continue
        window = section(text.split("\n"))
        if not window:
            no_heading += 1
            continue
        found = conditions(window)
        if not found:
            no_conditions += 1
            continue
        ok = series_ok([n for n, _, _ in found])
        tested = kinds.get(path.stem, "") not in SERIES_NOT_TESTED
        if ok:
            clean.add(path.stem)
        for number, raw, heading in found:
            body = normalise(raw)
            records.append(
                {
                    "id": path.stem,
                    "prövningsgrupp": groups[path.stem],
                    "villkorsnummer": number,
                    "tecken": len(body),
                    "källa": origin,
                    # The section heading over this condition, verbatim and
                    # nullable, which is the field VILLKORSSCHEMA section 2.2
                    # asks for. It is the document's own word for what the
                    # condition regulates.
                    "rubrik": heading,
                    "series_ok": ok,
                    "serie_prövas": tested,
                    "text_hash": hashlib.sha256(body.encode("utf-8")).hexdigest()[:16],
                }
            )

    with OUT.open("w", encoding="utf-8", newline="\n") as out:
        for record in records:
            out.write(json.dumps(record, ensure_ascii=False) + "\n")

    decisions = len({r["id"] for r in records})
    print(
        f"{no_text} filer utan textlager, {no_heading} utan hittad villkorsrubrik, "
        f"{no_conditions} med rubrik men inget numrerat villkor, "
        f"{unlisted} utanför manifestet\n"
        f"{decisions} beslut segmenterade, {len(clean)} med obruten serie 1..N "
        f"({len(clean) / decisions:.0%}) -> {OUT.name}"
    )
    if not records:
        return 0

    per_decision = Counter(r["id"] for r in records)
    counts = sorted(per_decision.values())
    print(
        f"villkor per beslut: median {counts[len(counts) // 2]}, "
        f"lägst {counts[0]}, högst {counts[-1]}"
    )

    by_origin = {
        o: {r["id"] for r in records if r["källa"] == o} for o in ("text", "ocr")
    }
    if by_origin["ocr"]:
        confidence = {}
        if OCR_INDEX.exists():
            confidence = {
                json.loads(line)["id"]: json.loads(line)["confidence"]
                for line in OCR_INDEX.read_text("utf-8").splitlines()
            }
        read = sorted(confidence[i] for i in by_origin["ocr"] if i in confidence)
        print(
            f"källa: {len(by_origin['text'])} beslut ur textlagret, "
            f"{len(by_origin['ocr'])} ur OCR"
            + (f", mediankonfidens {read[len(read) // 2]}" if read else "")
        )
        tested = {r["id"] for r in records if r["serie_prövas"]}
        for origin in ("text", "ocr"):
            ids = by_origin[origin]
            good = len(ids & clean)
            share = good / len(ids) if ids else 0.0
            print(f"  {origin}: obruten serie {good} av {len(ids)}, {share:.0%}")
            # The same figure over the decisions the check can speak about. An
            # amendment changes named conditions in an earlier permit, so a gap
            # in its numbering is the right answer and counting it as a failure
            # makes the segmenter look worse than it is.
            scoped = ids & tested
            if scoped and scoped != ids:
                hit = len(scoped & clean)
                print(
                    f"    varav prövbara: {hit} av {len(scoped)}, "
                    f"{hit / len(scoped):.0%}; "
                    f"{len(ids - tested)} ändringsbeslut ligger utanför kontrollen"
                )

    # The headline is the born-digital set, and the order here says so. OCR
    # text breaks words across line ends and drops characters, so two identical
    # conditions rarely survive as identical strings once one of them has been
    # read by OCR. Pooling the two sources would therefore move the reuse share
    # downwards for an instrument reason rather than a factual one, and the
    # figure that goes into docs/VERIFIERAT.md must not move that way.
    print("\nHUVUDSIFFRA, beslut ur textlagret")
    print(reuse([r for r in records if r["källa"] == "text"], groups))
    print("\nbara beslut ur textlagret med obruten serie")
    print(
        reuse([r for r in records if r["källa"] == "text" and r["id"] in clean], groups)
    )
    if by_origin["ocr"]:
        print("\nbara OCR-lästa beslut, exakt matchning missgynnar dem")
        print(reuse([r for r in records if r["källa"] == "ocr"], groups))
        print("\npoolat, redovisas för fullständighet och bär ingen slutsats")
        print(reuse(records, groups))
    return 0


if __name__ == "__main__":
    sys.exit(main())
