"""Compare redaction between request classes within the same species.

Step 21 of the pipeline. P1 defines the contrast measure as the difference in
redaction between class A, the inspection reports, and class B, the decisions,
within the same authority, computed within species where the material allows.
Pooling over the country would let the mix of animals stand in for a difference
between document classes: a county that inspects mostly poultry is not
comparable to one that inspects mostly cattle, and class A and class B need not
carry the same mix even inside one county.

This step joins step 18's redaction record with step 20's species record and
writes one row per authority, species and class to data/kontrast.jsonl, with
counts and shares only.

Two components, both from the pre-registration in docs/BEGARANMALL.md: the
share of documents carrying any redaction, and the share of page area covered.
The third component, the share of redacted fields, is not built.

**The threshold is a presentation choice. The protocol sets none.** Every cell is
written to the file whatever its size; the printed summary shows cells with at
least MIN_CELL documents in both classes, because a contrast computed on one
document against one document is noise with a decimal point.

Usage:
    python pipeline/21_contrast_within_species.py
"""

from __future__ import annotations

import json
import statistics
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MASKING = ROOT / "data" / "maskning.jsonl"
SPECIES = ROOT / "data" / "djurslag.jsonl"
OUT = ROOT / "data" / "kontrast.jsonl"

MIN_CELL = 3


def load(path: Path) -> dict[str, dict]:
    """One record per document path."""
    return {
        json.loads(line)["path"]: json.loads(line)
        for line in path.read_text("utf-8").splitlines()
    }


def authority_and_class(relative: str) -> tuple[str, str] | None:
    """The authority and request class a delivery folder stands for."""
    folder = relative.split("/")[0]
    if not folder.endswith(("_A", "_B")):
        return None
    return folder.rsplit("_", 1)[0], folder[-1]


def cells(masking: dict[str, dict], species: dict[str, dict]) -> list[dict]:
    """One row per authority, species and class."""
    grouped: dict[tuple[str, str, str], list[dict]] = defaultdict(list)
    for path, mask in masking.items():
        where = authority_and_class(path)
        kind = species.get(path, {}).get("dominant")
        if where is None or kind is None:
            continue
        authority, klass = where
        grouped[(authority, kind, klass)].append(mask)

    rows = []
    for (authority, kind, klass), docs in sorted(grouped.items()):
        rows.append(
            {
                "myndighet": authority,
                "djurslag": kind,
                "begaran": klass,
                "dokument": len(docs),
                "maskade": sum(1 for d in docs if d["masked"]),
                "andel_maskade": round(
                    sum(1 for d in docs if d["masked"]) / len(docs), 3
                ),
                "andel_yta": round(
                    sum(d["masked_area_share"] for d in docs) / len(docs), 5
                ),
            }
        )
    return rows


def contrasts(rows: list[dict]) -> list[dict]:
    """The A minus B difference for every authority and species with both."""
    index = {(r["myndighet"], r["djurslag"], r["begaran"]): r for r in rows}
    pairs = []
    for (authority, kind, klass), row in index.items():
        if klass != "A":
            continue
        other = index.get((authority, kind, "B"))
        if other is None:
            continue
        pairs.append(
            {
                "myndighet": authority,
                "djurslag": kind,
                "dokument_a": row["dokument"],
                "dokument_b": other["dokument"],
                "kontrast_andel": round(
                    row["andel_maskade"] - other["andel_maskade"], 3
                ),
                "kontrast_yta": round(row["andel_yta"] - other["andel_yta"], 5),
            }
        )
    return sorted(pairs, key=lambda p: (p["djurslag"], p["myndighet"]))


def main() -> int:
    """Write the per-cell record and report the contrasts."""
    if not (MASKING.exists() and SPECIES.exists()):
        print("run steps 18 and 20 first")
        return 1

    rows = cells(load(MASKING), load(SPECIES))
    pairs = contrasts(rows)
    with OUT.open("w", encoding="utf-8", newline="\n") as out:
        for row in rows:
            out.write(json.dumps(row, ensure_ascii=False) + "\n")

    print(f"{len(rows)} cells written to {OUT.name}, {len(pairs)} with both classes\n")
    usable = [p for p in pairs if min(p["dokument_a"], p["dokument_b"]) >= MIN_CELL]
    print(f"{'myndighet':17} {'djurslag':9} {'A':>3} {'B':>3}  andel   yta")
    for pair in usable:
        print(
            f"{pair['myndighet']:17} {pair['djurslag']:9} "
            f"{pair['dokument_a']:3} {pair['dokument_b']:3}  "
            f"{pair['kontrast_andel']:+.0%}  {pair['kontrast_yta']:+.2%}"
        )

    for kind in sorted({p["djurslag"] for p in usable}):
        subset = [p for p in usable if p["djurslag"] == kind]
        print(
            f"\n{kind}: {len(subset)} län, median andel "
            f"{statistics.median(p['kontrast_andel'] for p in subset):+.0%}, "
            f"median yta "
            f"{statistics.median(p['kontrast_yta'] for p in subset):+.2%}, "
            f"negativa {sum(1 for p in subset if p['kontrast_andel'] < 0)}"
        )
    thin = len(pairs) - len(usable)
    if thin:
        print(f"\n{thin} cells with both classes fall under {MIN_CELL} documents")
    return 0


if __name__ == "__main__":
    sys.exit(main())
