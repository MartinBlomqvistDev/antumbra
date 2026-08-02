"""Download the DG SANTE corpus: EU-27 English reports and all annexes.

Step 03 of the pipeline; run 02_harvest_details.py first. Reads the detail
records and downloads, for every EU-27 audit, the English report versions
plus every annex (action plans, competent authority comments and the
unclassified numbered annexes from the older era). French and German report
versions are translations of the same text and are skipped.

Files land under pdf/, which is gitignored: source documents are never
committed. Resumable: a file already on disk with non-zero size is skipped,
so an interrupted run can simply be restarted. Failures are appended to
pdf/dgsante/errors.jsonl instead of stopping the run.

Usage:
    python pipeline/03_download_reports.py
"""

from __future__ import annotations

import json
import re
import sys
import threading
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DETAILS = ROOT / "data" / "dgsante_details.jsonl"
PDF_DIR = ROOT / "pdf" / "dgsante"
REPORT_DIR = PDF_DIR / "reports"
ANNEX_DIR = PDF_DIR / "annexes"
ERRORS = PDF_DIR / "errors.jsonl"

REPORT_URL = "https://ec.europa.eu/food/audits-analysis/audit-report/download/"
ANNEX_URL = "https://ec.europa.eu/food/audits-analysis/audit-report/annex/download/"
UA = "Mozilla/5.0 (research; contact cm.blomqvist@gmail.com)"
WORKERS = 4
DELAY = 0.25
TIMEOUT = 120
RETRIES = 3

# Same set as tests/test_repository_invariants.py: both spellings of Czechia
# occur in the wild even though the harvested data uses "Czech Republic".
EU27 = {
    "Austria",
    "Belgium",
    "Bulgaria",
    "Croatia",
    "Cyprus",
    "Czechia",
    "Czech Republic",
    "Denmark",
    "Estonia",
    "Finland",
    "France",
    "Germany",
    "Greece",
    "Hungary",
    "Ireland",
    "Italy",
    "Latvia",
    "Lithuania",
    "Luxembourg",
    "Malta",
    "Netherlands",
    "Poland",
    "Portugal",
    "Romania",
    "Slovakia",
    "Slovenia",
    "Spain",
    "Sweden",
}

_lock = threading.Lock()
_done = 0
_failed = 0


def extension(headers: dict[str, str], payload: bytes) -> str:
    """Pick a file extension from Content-Disposition, defaulting to pdf.

    Args:
        headers: Response headers of the download.
        payload: First bytes of the response body.

    Returns:
        A lowercase extension without the dot.
    """
    if payload.startswith(b"%PDF"):
        return "pdf"
    disposition = headers.get("Content-Disposition", "")
    m = re.search(r'filename="?[^"]*\.(\w{1,5})"?', disposition)
    return m.group(1).lower() if m else "pdf"


def fetch(url: str) -> tuple[dict[str, str], bytes]:
    """GET one file, retrying with backoff on transient failure."""
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    last: Exception | None = None
    for attempt in range(RETRIES):
        try:
            with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
                return dict(r.headers), r.read()
        except Exception as exc:
            last = exc
            time.sleep(2 * (attempt + 1))
    raise RuntimeError(str(last))


def work(task: tuple[str, Path, str]) -> None:
    """Download one file to its stem; failures are recorded, not raised.

    Args:
        task: Download URL, target directory and file stem (name without
            extension; the extension is decided by the response).
    """
    global _done, _failed
    url, directory, stem = task
    try:
        headers, payload = fetch(url)
        if not payload:
            raise RuntimeError("empty response body")
        stripped = payload.lstrip()
        if stripped.startswith((b"<!DOCTYPE", b"<html", b"<HTML")):
            raise RuntimeError("HTML error page instead of a document")
        target = directory / f"{stem}.{extension(headers, payload)}"
        part = target.with_suffix(target.suffix + ".part")
        part.write_bytes(payload)
        part.replace(target)
        error = None
    except Exception as exc:
        error = str(exc)[:200]
    with _lock:
        _done += 1
        if error:
            _failed += 1
            with open(ERRORS, "a", encoding="utf-8") as fh:
                fh.write(
                    json.dumps({"url": url, "stem": stem, "error": error}) + "\n"
                )
        if _done % 250 == 0:
            print(f"{_done} done, {_failed} failed", flush=True)
    time.sleep(DELAY)


def build_tasks(details: list[dict]) -> list[tuple[str, Path, str]]:
    """List every file to download for the EU-27 subset.

    Args:
        details: Records from data/dgsante_details.jsonl.

    Returns:
        One (url, directory, stem) triple per English report and per annex.
    """
    tasks: list[tuple[str, Path, str]] = []
    for rec in details:
        if rec["country"] not in EU27:
            continue
        ref = rec["ref"]
        for report in rec["reports"]:
            if report["language"] != "English":
                continue
            tasks.append(
                (f"{REPORT_URL}{report['id']}", REPORT_DIR, f"{ref}_{report['id']}_en")
            )
        for annex in rec["annexes"]:
            tasks.append(
                (f"{ANNEX_URL}{annex['id']}", ANNEX_DIR, f"{ref}_{annex['id']}")
            )
    return tasks


def existing_stems(directory: Path) -> set[str]:
    """Stems of non-empty, fully written files already in a directory."""
    return {
        p.stem
        for p in directory.iterdir()
        if p.is_file() and p.suffix != ".part" and p.stat().st_size > 0
    }


def main() -> int:
    """Download every missing EU-27 English report and annex."""
    details = [
        json.loads(line)
        for line in DETAILS.read_text(encoding="utf-8").splitlines()
        if line
    ]
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    ANNEX_DIR.mkdir(parents=True, exist_ok=True)

    tasks = build_tasks(details)
    done = {
        (directory, stem)
        for directory in (REPORT_DIR, ANNEX_DIR)
        for stem in existing_stems(directory)
    }
    todo = [t for t in tasks if (t[1], t[2]) not in done]
    print(
        f"total {len(tasks)}, already downloaded {len(tasks) - len(todo)}, "
        f"to fetch {len(todo)}",
        flush=True,
    )

    with ThreadPoolExecutor(WORKERS) as pool:
        list(pool.map(work, todo))

    print(f"FINISHED, {_done} fetched in this run, {_failed} failed", flush=True)
    if _failed:
        print(f"see {ERRORS}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
