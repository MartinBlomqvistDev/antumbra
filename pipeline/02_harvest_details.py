"""Harvest DG SANTE audit-report detail pages.

Step 02 of the pipeline; run 01_harvest_index.py first. Reads the index and
fetches one detail page per audit, extracting published date, report
language versions and annexes (competent authority comments and action
plans).

Resumable: detail_ids already present in the output are skipped, so an
interrupted run can simply be restarted.

Writes data/dgsante_details.jsonl, one object per audit.

Usage:
    python pipeline/02_harvest_details.py
"""

from __future__ import annotations

import json
import re
import sys
import threading
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from html import unescape
from pathlib import Path
from typing import TextIO

ROOT = Path(__file__).resolve().parent.parent
INDEX = ROOT / "data" / "dgsante_index.json"
OUT = ROOT / "data" / "dgsante_details.jsonl"

BASE = "https://ec.europa.eu/food/audits-analysis/audit-report/details/"
UA = "Mozilla/5.0 (research; contact cm.blomqvist@gmail.com)"
WORKERS = 4
DELAY = 0.25
TIMEOUT = 60
RETRIES = 3

_lock = threading.Lock()
_done = 0


def strip_tags(s: str) -> str:
    """Remove tags, unescape entities and collapse whitespace."""
    return re.sub(r"\s+", " ", unescape(re.sub(r"<[^>]+>", " ", s))).strip()


def parse(html: str) -> dict:
    """Extract the fields of interest from one detail page.

    Args:
        html: Raw detail page markup.

    Returns:
        Country, audit number, title, audit period, published date, plus
        one entry per report language version and per annex.
    """

    def dd(term: str) -> str | None:
        m = re.search(
            rf"<dt[^>]*>\s*{term}\s*</dt>\s*<dd[^>]*>(.*?)</dd>", html, re.S | re.I
        )
        return strip_tags(m.group(1)) if m else None

    reports = [
        {"id": int(i), "language": strip_tags(t), "size": strip_tags(sz)}
        for i, t, sz in re.findall(
            r'audit-report/download/(\d+)"[^>]*title="([^"]*)"[^>]*>.*?<small>\s*\(([^)]*)\)',
            html,
            re.S,
        )
    ]
    annexes = [
        {
            "id": int(i),
            "title": strip_tags(t),
            "label": strip_tags(lbl),
            "size": strip_tags(sz),
        }
        for i, t, lbl, sz in re.findall(
            r'audit-report/annex/download/(\d+)"[^>]*title="([^"]*)"[^>]*>(.*?)</a>.*?<small>\s*\(([^)]*)\)',
            html,
            re.S,
        )
    ]
    return {
        "country": dd("Country"),
        "audit_number": dd("Audit number"),
        "title": dd("Title"),
        "audit_period": dd("Audit period"),
        "published_date": dd("Published date"),
        "reports": reports,
        "annexes": annexes,
    }


def fetch(detail_id: str) -> str:
    """GET one detail page, retrying with backoff on transient failure."""
    req = urllib.request.Request(BASE + detail_id, headers={"User-Agent": UA})
    last: Exception | None = None
    for attempt in range(RETRIES):
        try:
            with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
                return r.read().decode("utf-8", "replace")
        except Exception as exc:
            last = exc
            time.sleep(2 * (attempt + 1))
    raise RuntimeError(f"{detail_id}: {last}")


def work(row: dict, fh: TextIO) -> None:
    """Fetch, parse and append one audit; failures are recorded, not raised."""
    global _done
    try:
        rec = {**row, **parse(fetch(row["detail_id"])), "error": None}
    except Exception as exc:
        rec = {**row, "error": str(exc)[:200]}
    with _lock:
        fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
        fh.flush()
        _done += 1
        if _done % 250 == 0:
            print(f"{_done} done", flush=True)
    time.sleep(DELAY)


def main() -> int:
    """Read the index, fetch every unharvested detail page and append results."""
    rows = json.loads(INDEX.read_text(encoding="utf-8"))
    seen: set[str] = set()
    if OUT.exists():
        for line in OUT.read_text(encoding="utf-8").splitlines():
            try:
                r = json.loads(line)
            except json.JSONDecodeError:
                continue
            if not r.get("error"):
                seen.add(r["detail_id"])

    todo = [r for r in rows if r["detail_id"] not in seen]
    print(
        f"total {len(rows)}, already done {len(seen)}, to fetch {len(todo)}",
        flush=True,
    )

    with (
        open(OUT, "a", encoding="utf-8", newline="\n") as fh,
        ThreadPoolExecutor(WORKERS) as pool,
    ):
        list(pool.map(lambda r: work(r, fh), todo))

    print(f"FINISHED, {_done} fetched in this run", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
