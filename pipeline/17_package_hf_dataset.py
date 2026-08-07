"""Package the DG SANTE corpus for Hugging Face, without publishing it.

Step 17 of the pipeline; run 10 first. Collects the warehouse tables, the
source manifest and the dataset card into data/hf/, which stays outside
git. Publication is a separate, deliberate act gated to the protocol's
day 40 at the earliest, because a public dataset describing the project
would reveal the Swedish measurement to the authorities mid-collection:

    hf upload-large-folder MartinBlomqvist/dgsante --repo-type dataset data/hf

The row counts printed at the end are read from the warehouse manifest and
compared against the packaged files' presence, so a partial warehouse
cannot be packaged quietly.

Usage:
    python pipeline/17_package_hf_dataset.py
"""

from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WAREHOUSE = ROOT / "data" / "warehouse"
OUT = ROOT / "data" / "hf"

TABLES = [
    "dim_country",
    "dim_audit",
    "dim_paragraph",
    "fact_recommendation",
    "fact_citation",
    "fact_commitment",
]


def main() -> int:
    """Assemble the dataset directory and report what it holds."""
    manifest = json.loads(
        (ROOT / "data" / "dgsante_warehouse_manifest.json").read_text("utf-8")
    )
    rows = {entry["table"]: entry["rows"] for entry in manifest["tables"]}
    missing = [name for name in TABLES if not (WAREHOUSE / f"{name}.parquet").exists()]
    if missing:
        print(f"warehouse tables missing: {missing}; run step 10 first")
        return 1

    OUT.mkdir(parents=True, exist_ok=True)
    total = 0
    for name in TABLES:
        source = WAREHOUSE / f"{name}.parquet"
        shutil.copy2(source, OUT / f"{name}.parquet")
        total += source.stat().st_size
        print(f"{name}: {rows[name]} rows, {source.stat().st_size // 1024} KiB")

    source_manifest = ROOT / "data" / "dgsante_manifest.jsonl"
    shutil.copy2(source_manifest, OUT / "manifest.jsonl")
    total += source_manifest.stat().st_size

    card = ROOT / "docs" / "HF_DATASET.md"
    shutil.copy2(card, OUT / "README.md")

    print(f"-> {OUT.relative_to(ROOT)}: {total / 1_048_576:.1f} MiB, plus card")
    print("publication is manual and waits for the protocol; see the docstring")
    return 0


if __name__ == "__main__":
    sys.exit(main())
