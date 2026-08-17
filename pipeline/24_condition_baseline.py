"""Test whether permit conditions are standard text before building anything.

Step 24 of the pipeline, and the gate the conditions layer has to pass. STATUS
puts it before extraction for a reason: if the conditions in the permit
decisions are boilerplate reused across installations, then a register of them
describes a template, and that is the result. If they differ, the register
measures something, and the work of building it is justified. Deciding this
first costs two days; discovering it after the extractor is built costs weeks.

**The conditions section is bounded, not searched for everywhere.** A first
version segmented on any line opening with a number and a full stop, anywhere
in the document, and 12 decisions of 144, 8 per cent, then produced an unbroken
1..N series of condition numbers. Numbered lists live all over these decisions,
in the account of the case and in the closing information, so that measure was
taken over a mixture of conditions and other text. This version finds the
conditions heading, reads until the next section heading, and segments only
inside that window: 106 of 120, 88 per cent, then produce an unbroken series.
The heading list and the stop list are heuristics over the layouts actually
present in the corpus, and VILLKORSSCHEMA section 2.2 already records that
headings vary and can be absent.

**What this step is not.** It does not classify conditions by type, parse
quantified requirements or resolve the decision's identity. It reads only the
decisions that carry a usable text layer, and among those only the ones whose
conditions section can be located. Both limits are counted and printed with the
result rather than hidden behind it.

**The measure.** Two condition texts count as the same when they are identical
after case folding and whitespace collapsing, and nothing else is normalised.
Numbers are deliberately kept: 40 dB(A) and 45 dB(A) are different conditions,
and a similarity threshold that hides that difference would answer a question
nobody asked. ADR-0013 chose containment over similarity for a directional
question; this question is symmetric, so exact match after normalisation is the
conservative instrument, and it can only understate reuse.

**Verification is check 1 from VILLKORSSCHEMA section 5**, the numbers forming
the series 1..N. Every decision carries the outcome as series_ok, and the
reuse figures are reported twice, over every decision and over the clean subset
alone, so that a segmentation failure cannot carry the headline.

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
SOURCE = ROOT / "pdf" / "jordbruksverket"
MANIFEST = ROOT / "data" / "tillstand_manifest.jsonl"
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
# A condition opens with its number. The text can follow on the same line or on
# the next one, which is how the decisions that amend a single condition are set.
CONDITION_START = re.compile(r"^(\d{1,2})[.)]\s*(.*)$")


def normalise(text: str) -> str:
    """Case folded with whitespace collapsed, and nothing else changed."""
    return re.sub(r"\s+", " ", text).strip().casefold()


def section(lines: list[str]) -> list[str]:
    """The lines of the conditions section, or empty if no heading is found."""
    for index, line in enumerate(lines):
        if not SECTION_START.match(line.strip()):
            continue
        out: list[str] = []
        for candidate in lines[index + 1 :]:
            stripped = candidate.strip()
            if out and SECTION_STOP.match(stripped):
                break
            out.append(stripped)
        return out
    return []


def conditions(lines: list[str]) -> list[tuple[int, str]]:
    """Number and text of every condition in the bounded section."""
    found: list[tuple[int, str]] = []
    number: int | None = None
    current: list[str] = []
    for line in lines:
        match = CONDITION_START.match(line)
        if match:
            if number is not None and current:
                found.append((number, " ".join(current)))
            number = int(match.group(1))
            current = [match.group(2)] if match.group(2) else []
        elif number is not None:
            if not line:
                if current:
                    found.append((number, " ".join(current)))
                number, current = None, []
            else:
                current.append(line)
    if number is not None and current:
        found.append((number, " ".join(current)))
    return [
        (n, normalise(t))
        for n, t in found
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
        with pymupdf.open(path) as document:
            pages = len(document)
            text = "\n".join(page.get_text() for page in document)
        if len(text) < MIN_CHARS_PER_PAGE * pages:
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
        ok = series_ok([n for n, _ in found])
        if ok:
            clean.add(path.stem)
        for number, body in found:
            records.append(
                {
                    "id": path.stem,
                    "prövningsgrupp": groups[path.stem],
                    "villkorsnummer": number,
                    "tecken": len(body),
                    "series_ok": ok,
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

    print("\nalla segmenterade beslut")
    print(reuse(records, groups))
    print("\nbara beslut med obruten serie")
    print(reuse([r for r in records if r["id"] in clean], groups))
    return 0


if __name__ == "__main__":
    sys.exit(main())
