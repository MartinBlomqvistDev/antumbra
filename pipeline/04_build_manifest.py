"""Build a provenance manifest for the downloaded DG SANTE corpus.

Step 04 of the pipeline; run 03_download_reports.py first. Hashes every
downloaded file and joins it back to the harvested detail records, so each
file on disk carries its source URL, audit reference and sha256 checksum.

The manifest is committed while the documents themselves are not: anyone
can re-download a file from the Commission and compare hashes, which makes
the corpus verifiable without redistributing it.

Writes data/dgsante_manifest.jsonl, one line per file, sorted by path.

Usage:
    python pipeline/04_build_manifest.py
"""

from __future__ import annotations

import hashlib
import json
import sys
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DETAILS = ROOT / "data" / "dgsante_details.jsonl"
REPORT_DIR = ROOT / "pdf" / "dgsante" / "reports"
ANNEX_DIR = ROOT / "pdf" / "dgsante" / "annexes"
OUT = ROOT / "data" / "dgsante_manifest.jsonl"

REPORT_URL = "https://ec.europa.eu/food/audits-analysis/audit-report/download/"
ANNEX_URL = "https://ec.europa.eu/food/audits-analysis/audit-report/annex/download/"


def stem_index(details: list[dict]) -> dict[tuple[str, str], dict]:
    """Map (kind, file stem) to source metadata from the detail records.

    Args:
        details: Records from data/dgsante_details.jsonl.

    Returns:
        Source metadata keyed the same way step 03 names files on disk.
    """
    index: dict[tuple[str, str], dict] = {}
    for rec in details:
        ref = rec["ref"]
        for report in rec["reports"]:
            index[("report", f"{ref}_{report['id']}_en")] = {
                "ref": ref,
                "country": rec["country"],
                "file_id": report["id"],
                "language": report["language"],
                "url": f"{REPORT_URL}{report['id']}",
            }
        for annex in rec["annexes"]:
            index[("annex", f"{ref}_{annex['id']}")] = {
                "ref": ref,
                "country": rec["country"],
                "file_id": annex["id"],
                "title": annex["title"],
                "url": f"{ANNEX_URL}{annex['id']}",
            }
    return index


def manifest_row(path: Path, kind: str, meta: dict) -> dict:
    """Hash one file and combine it with its source metadata.

    Args:
        path: Downloaded file on disk.
        kind: "report" or "annex".
        meta: Source metadata from stem_index.

    Returns:
        One manifest record; fetched is the file's mtime as a UTC date.
    """
    stat = path.stat()
    return {
        "path": path.relative_to(ROOT).as_posix(),
        "kind": kind,
        **meta,
        "bytes": stat.st_size,
        "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "fetched": datetime.fromtimestamp(stat.st_mtime, tz=UTC).date().isoformat(),
    }


def main() -> int:
    """Hash every downloaded file and write the manifest."""
    details = [
        json.loads(line)
        for line in DETAILS.read_text(encoding="utf-8").splitlines()
        if line
    ]
    index = stem_index(details)
    rows: list[dict] = []
    for kind, directory in (("report", REPORT_DIR), ("annex", ANNEX_DIR)):
        for path in sorted(directory.iterdir()):
            if not path.is_file() or path.suffix == ".part":
                continue
            meta = index.get((kind, path.stem))
            if meta is None:
                raise SystemExit(f"file has no source in the details: {path}")
            rows.append(manifest_row(path, kind, meta))
    rows.sort(key=lambda r: r["path"])
    with open(OUT, "w", encoding="utf-8", newline="\n") as fh:
        for row in rows:
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")
    print(f"{len(rows)} rows -> {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
