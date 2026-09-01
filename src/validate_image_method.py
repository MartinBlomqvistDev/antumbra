"""Check the image method against the text method, on the documents that have both.

The masking measure in step 18 uses two methods. Born-digital documents are
judged from the text layer, scanned ones from the rendered page, and the second
was trusted because it was compared against the first on every born-digital
document. That comparison was run once, by hand, on 14 August 2026, and no
script was kept. When the text method was corrected on 1 September 2026 the
comparison had to be run again, and the published table's clean row could not be
reproduced: it reports one false positive where the detector produces thirty.
Whether the table was miscounted or computed some other way cannot be settled,
because nothing in the repository could re-run it.

This module exists so that cannot happen twice. It renders every born-digital
document, runs the image detector over it, and prints the cross-tabulation
against the text method's verdict. It changes no data file and decides nothing;
it reports, and the numbers it reports belong in docs/VERIFIERAT.md next to the
figures they qualify.

Reading the output: the rows are the text method's verdict, which is the facit,
and the columns are whether the image detector found a bar. A born-digital
document the text method calls clean and the image method calls masked is a
false positive of the image method, and the count of those is the number the
scanned half of the corpus rests on.

Usage:
    python src/validate_image_method.py
"""

from __future__ import annotations

import importlib.util
import json
import sys
from collections import Counter
from pathlib import Path
from types import ModuleType

ROOT = Path(__file__).resolve().parent.parent
MASKING = ROOT / "data" / "maskning.jsonl"
DELIVERIES = ROOT / "data" / "leveranser"
STEP = ROOT / "pipeline" / "18_analyse_masking.py"

KINDS = ("text_removed", "box_over_text", "marker_only", "none")


def load_step() -> ModuleType:
    """Step 18 as a module, since its file name cannot be imported directly."""
    spec = importlib.util.spec_from_file_location("step18", STEP)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> int:
    """Run the image detector over the born-digital documents and report."""
    if not MASKING.exists():
        print(f"missing {MASKING.name}; run step 18 first")
        return 1
    step = load_step()
    records = [
        json.loads(line) for line in MASKING.read_text("utf-8").splitlines() if line
    ]
    born = [r for r in records if r["method"] == "text"]
    print(f"{len(born)} digitalt födda dokument, facit ur textlagret\n")

    table: Counter[tuple[str, bool]] = Counter()
    for position, record in enumerate(born, 1):
        bars, _, _ = step.scan_bars(DELIVERIES / record["path"])
        if bars < 0:
            print('pymupdf saknas: pip install -e ".[ocr]"')
            return 1
        table[(record["kind"], bool(bars))] += 1
        if position % 50 == 0:
            print(f"{position}/{len(born)}", flush=True)

    print(f"\n{'facit ur textlagret':22} {'balk hittad':>12} {'ingen balk':>12}")
    for kind in KINDS:
        found, clean = table[(kind, True)], table[(kind, False)]
        if found or clean:
            print(f"{kind:22} {found:>12} {clean:>12}")
    false_positives = table[("none", True)]
    clean_total = table[("none", True)] + table[("none", False)]
    if clean_total:
        share = false_positives / clean_total
        print(
            f"\nfalsklarm: {false_positives} av {clean_total} omaskade dokument "
            f"ger balk, {share:.0%}"
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
