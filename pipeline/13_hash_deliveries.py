"""Record every document delivered by an authority in a sha256 manifest.

Step 13 of the pipeline. The documents themselves live in data/leveranser/
outside git, one directory per authority and request class, and can contain
personal data. What the repository keeps is this manifest: enough to prove
later that a cited document is the one received, without redistributing it.

Resumable: files already in the manifest are skipped, so the step can be run
after every new delivery. A file whose hash changes under an existing name is
an error, and a silent update it never is.

Usage:
    python pipeline/13_hash_deliveries.py
"""

from __future__ import annotations

import hashlib
import json
import re
import sys
from datetime import date
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parent.parent
DELIVERIES = ROOT / "data" / "leveranser"
MANIFEST = ROOT / "data" / "leveranser_manifest.jsonl"

# An e-mail address inside a delivered file name. A court names its files
# after the division that sent them, and Kammarrätten i Stockholm delivered
# the judgment in case 6901-26 in a zip whose name ends in the division's own
# functional address. The manifest records names verbatim, so the address went
# into the protocol data and the invariant that keeps addresses out of it
# failed. The name is recorded with the address replaced, and the replacement
# stands in the name so that it is declared rather than quietly dropped.
ADDRESS = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")


def screened(relative: str) -> str:
    """The delivered path with any e-mail address in its name replaced.

    Only the stem is screened. The pattern's domain part is greedy and eats a
    trailing extension too, so screening the whole name turned a .zip into
    nothing at all and the manifest no longer said what kind of file it had
    recorded.
    """
    path = PurePosixPath(relative)
    return str(path.with_name(ADDRESS.sub("[adress]", path.stem) + path.suffix))


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
    with MANIFEST.open("a", encoding="utf-8", newline="\n") as out:
        for path in sorted(DELIVERIES.rglob("*")):
            if not path.is_file():
                continue
            relative = screened(path.relative_to(DELIVERIES).as_posix())
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
