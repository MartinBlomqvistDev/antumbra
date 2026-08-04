"""Record every document delivered by an authority in a sha256 manifest.

Step 13 of the pipeline. The documents themselves live in data/leveranser/
outside git, one directory per authority and request class, and can contain
personal data. What the repository keeps is this manifest: enough to prove
later that a cited document is the one received, without redistributing it.

Resumable: files already in the manifest are skipped, so the step can be run
after every new delivery. A file whose hash changes under an existing name is
an error, never a silent update.

Usage:
    python pipeline/13_hash_deliveries.py
"""

from __future__ import annotations

import hashlib
import json
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DELIVERIES = ROOT / "data" / "leveranser"
MANIFEST = ROOT / "data" / "leveranser_manifest.jsonl"


def sha256(path: Path) -> str:
    """The file's content hash."""
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def known() -> dict[str, str]:
    """Relative path to hash for every file already recorded."""
    if not MANIFEST.exists():
        return {}
    rows = (json.loads(line) for line in MANIFEST.read_text("utf-8").splitlines())
    return {row["path"]: row["sha256"] for row in rows}


def main() -> int:
    """Hash new deliveries and append them to the manifest."""
    if not DELIVERIES.is_dir():
        print("no deliveries yet: data/leveranser/ does not exist")
        return 0

    recorded = known()
    added = 0
    with MANIFEST.open("a", encoding="utf-8") as out:
        for path in sorted(DELIVERIES.rglob("*")):
            if not path.is_file():
                continue
            relative = path.relative_to(DELIVERIES).as_posix()
            digest = sha256(path)
            if relative in recorded:
                if recorded[relative] != digest:
                    print(f"HASH CHANGED under existing name: {relative}")
                    return 1
                continue
            row = {
                "path": relative,
                "bytes": path.stat().st_size,
                "sha256": digest,
                "recorded": date.today().isoformat(),
            }
            out.write(json.dumps(row, ensure_ascii=False) + "\n")
            added += 1
            print(f"{digest[:12]}  {relative}")
    print(f"{added} new files recorded, {len(recorded)} already known")
    return 0


if __name__ == "__main__":
    sys.exit(main())
