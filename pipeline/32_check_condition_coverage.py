"""Run check 2 from VILLKORSSCHEMA: does every decision carry the conditions it should.

Step 32 of the pipeline. Section 5 of docs/VILLKORSSCHEMA.md states the rule in
one sentence: "noll villkor är bara tillåtet för förlängningar,
igångsättningsbeslut, upphävanden och domar. Ett tillstånd med noll villkor är
per definition en tyst trasig extraktion." The rule could not be run until step
31 gave every decision its type, because until then a decision with no extracted
conditions could not be told apart from a decision that has none.

**This replaces a coverage figure that was true and useless.** Step 24 reports
that 173 of 236 files, 73 per cent, could be segmented. Read on its own that
number invites the conclusion that a quarter of the corpus is lost. Split by
type it says something else: the extraction reaches 155 of 162 permits, and the
fifteen extensions that carry no conditions at all are counted as failures by
the pooled figure while they are in fact the correct answer, exactly as the
Lidfarm decision in VILLKORSSCHEMA predicts.

**What the step reports, and what it refuses to decide.** It prints the split by
type, names the permits with no conditions so that they can be read by hand, and
counts the amendments, which the document says nothing about. It does not
declare any of them broken. Whether an amendment carries conditions of its own
or only changes a condition in the underlying permit is a question about the
documents, and answering it from the absence of a heading would be a guess.

**Zero is a result for some types and an alarm for others.** The step exits
zero even when permits are missing, because the missing ones are a standing
finding rather than a fault in this run, and the count is pinned in a repository
invariant so that it cannot grow without someone noticing. A step that fails on
a known number teaches its reader to ignore it.

Usage:
    python pipeline/32_check_condition_coverage.py
"""

from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TYPES = ROOT / "data" / "tillstand_typ.jsonl"
BASELINE = ROOT / "data" / "villkor_baseline.jsonl"

# The types VILLKORSSCHEMA section 5 allows to carry no conditions at all.
ZERO_ALLOWED = frozenset({"förlängning", "igångsättning", "upphävande", "dom"})
# The order the report prints, permits first because the rule is about them.
ORDER = (
    "tillstånd",
    "ändring",
    "förlängning",
    "dom",
    "villkor",
    "igångsättning",
    "upphävande",
    "annat",
)


def load(path: Path) -> list[dict]:
    """Every record in a jsonl file."""
    return [json.loads(line) for line in path.read_text("utf-8").splitlines() if line]


def main() -> int:
    """Split the conditions coverage by decision type and report the exceptions."""
    for path in (TYPES, BASELINE):
        if not path.exists():
            print(f"missing {path.name}; run steps 31 and 24 first")
            return 1

    kinds = {row["id"]: row["typ"] for row in load(TYPES)}
    conditions = Counter(row["id"] for row in load(BASELINE))
    orphans = set(conditions) - set(kinds)
    if orphans:
        print(f"{len(orphans)} dokument har villkor men saknar typ; kör steg 31\n")

    covered: Counter[tuple[str, bool]] = Counter()
    for document, kind in kinds.items():
        covered[(kind, conditions.get(document, 0) > 0)] += 1

    print(f"{len(kinds)} beslut, {sum(conditions.values())} extraherade villkor\n")
    header = f"{'typ':16} {'med':>5} {'utan':>6} {'totalt':>7}  {'noll ok':>8}"
    print(header)
    for kind in ORDER:
        yes, no = covered[(kind, True)], covered[(kind, False)]
        if not (yes or no):
            continue
        allowed = "ja" if kind in ZERO_ALLOWED else "nej"
        print(f"{kind:16} {yes:>5} {no:>6} {yes + no:>7}  {allowed:>8}")

    silent = sorted(
        document
        for document, kind in kinds.items()
        if kind == "tillstånd" and conditions.get(document, 0) == 0
    )
    print(f"\ntillstånd utan extraherade villkor: {len(silent)}")
    for document in silent:
        print(f"  {document}")
    print("  var och en är enligt VILLKORSSCHEMA en tyst trasig extraktion")
    print("  tills en handläsning visar något annat")

    unclear = sorted(
        document
        for document, kind in kinds.items()
        if kind not in ZERO_ALLOWED
        and kind != "tillstånd"
        and conditions.get(document, 0) == 0
    )
    print(f"\növriga utan villkor där regeln inte uttalar sig: {len(unclear)}")
    by_kind = Counter(kinds[document] for document in unclear)
    for kind, count in by_kind.most_common():
        print(f"  {kind}: {count}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
