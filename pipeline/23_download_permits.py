"""Fetch the environmental permit decisions that carry the conditions layer.

Step 23 of the pipeline, and the first step of the Swedish conditions layer.
The Board of Agriculture publishes every permit decision for large pig and
poultry installations on one page, grouped by the permit division that issued
it rather than by county. This step downloads them and records their
provenance.

**Names never enter the repository.** The published file names follow the
pattern Kommun_Bolag_Djurslag_Typ_Datum, and at least three of them name
natural persons rather than companies, as recorded in docs/VERIFIERAT.md. The
download URL carries the same name. Two consequences, both deliberate:

  * every file is stored as its own identifier, the first twelve hex digits of
    the sha256 of its URL, so no name reaches the file system either;
  * the committed manifest carries the identifier, the permit division, size,
    content hash and retrieval date, and nothing derived from the name.

The crosswalk from identifier to URL and original file name is written next to
the documents in pdf/jordbruksverket/, which is outside version control. It is
what makes the harvest reproducible locally; it is not publishable.

Resumable: a document already on disk with non-zero size is skipped.

Usage:
    python pipeline/23_download_permits.py
"""

from __future__ import annotations

import hashlib
import json
import re
import ssl
import sys
import time
import urllib.parse
import urllib.request
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / "pdf" / "jordbruksverket"
CROSSWALK = TARGET / "crosswalk.jsonl"
MANIFEST = ROOT / "data" / "tillstand_manifest.jsonl"

SITE = "https://jordbruksverket.se"
INDEX = (
    f"{SITE}/kontroller-och-tillsyn/miljo/"
    "stora-anlaggningar-for-uppfodning-av-fjaderfa-och-gris/"
    "tillstand-och-domar-for-stora-gris--och-fjaderfaanlaggningar"
)
UA = "Mozilla/5.0 (research; contact cm.blomqvist@gmail.com)"
DELAY = 0.5
TIMEOUT = 120
RETRIES = 3

# Verified against the page on 2026-08-01 and recorded in docs/VERIFIERAT.md.
# The corpus grows as decisions are published, so a difference is reported and
# never treated as an error; a silent change in the other direction would be.
BASELINE = {
    "Skåne län och Blekinge län": 68,
    "Västra Götalands län": 56,
    "Kalmar län och Kronobergs län": 30,
    "Östergötlands län och Jönköpings län": 28,
    "Hallands län": 26,
    "Uppsala län, Västmanlands län och Södermanlands län": 13,
    "Örebro län och Värmlands län": 12,
    "Dalarnas län och Gävleborgs län": 2,
    "Norrbottens län": 1,
    "Stockholms län och Gotlands län": 1,
}


def context() -> ssl.SSLContext | None:
    """An SSL context that works where the system trust store is incomplete."""
    try:
        import certifi
    except ImportError:
        return None
    return ssl.create_default_context(cafile=certifi.where())


def fetch(url: str, ssl_context: ssl.SSLContext | None) -> bytes:
    """GET one resource, retrying with backoff on transient failure."""
    request = urllib.request.Request(url, headers={"User-Agent": UA})
    last: Exception | None = None
    for attempt in range(RETRIES):
        try:
            with urllib.request.urlopen(
                request, timeout=TIMEOUT, context=ssl_context
            ) as response:
                return response.read()
        except Exception as exc:
            last = exc
            time.sleep(2 * (attempt + 1))
    raise RuntimeError(f"{url}: {last}")


def parse_index(html: str) -> list[tuple[str, str]]:
    """Permit division and absolute URL for every decision on the page."""
    tokens = re.findall(
        r'<h3[^>]*>(.*?)</h3>|href="(/download/[^"]+\.pdf)"', html, re.S | re.I
    )
    found: list[tuple[str, str]] = []
    division = ""
    for heading, link in tokens:
        if heading:
            text = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", heading)).strip()
            if text:
                division = text
        elif link and division:
            found.append((division, urllib.parse.urljoin(SITE, link)))
    # The page lists at least one decision twice under the same URL, so the
    # same document would otherwise be fetched and recorded twice.
    seen: set[str] = set()
    unique = []
    for division, url in found:
        if url in seen:
            continue
        seen.add(url)
        unique.append((division, url))
    return unique


def identifier(url: str) -> str:
    """A stable name for a document that reveals nothing about its subject."""
    return hashlib.sha256(url.encode("utf-8")).hexdigest()[:12]


def main() -> int:
    """Download every decision that is not already on disk."""
    ssl_context = context()
    TARGET.mkdir(parents=True, exist_ok=True)

    print(f"reading {INDEX}", flush=True)
    documents = parse_index(fetch(INDEX, ssl_context).decode("utf-8", "replace"))
    if not documents:
        print("no decisions found; the page layout has changed")
        return 1

    counts: dict[str, int] = {}
    for division, _ in documents:
        counts[division] = counts.get(division, 0) + 1
    print(f"\n{len(documents)} decisions in {len(counts)} permit divisions")
    for division in sorted(counts, key=lambda d: -counts[d]):
        expected = BASELINE.get(division)
        note = ""
        if expected is None:
            note = "  (division not in the 2026-08-01 baseline)"
        elif expected != counts[division]:
            note = f"  (baseline {expected})"
        print(f"  {counts[division]:4}  {division}{note}")
    missing = sorted(set(BASELINE) - set(counts))
    if missing:
        print(f"  divisions in the baseline but not on the page: {missing}")

    known = set()
    if MANIFEST.exists():
        known = {
            json.loads(line)["id"] for line in MANIFEST.read_text("utf-8").splitlines()
        }

    added = failed = 0
    with (
        MANIFEST.open("a", encoding="utf-8", newline="\n") as manifest,
        CROSSWALK.open("a", encoding="utf-8", newline="\n") as crosswalk,
    ):
        for index, (division, url) in enumerate(documents, 1):
            key = identifier(url)
            path = TARGET / f"{key}.pdf"
            if key in known and path.exists() and path.stat().st_size:
                continue
            try:
                payload = fetch(url, ssl_context)
            except Exception as exc:
                failed += 1
                print(f"FAILED {key}: {str(exc)[:120]}", flush=True)
                continue
            path.write_bytes(payload)
            manifest.write(
                json.dumps(
                    {
                        "id": key,
                        "prövningsgrupp": division,
                        "bytes": len(payload),
                        "sha256": hashlib.sha256(payload).hexdigest(),
                        "retrieved": date.today().isoformat(),
                    },
                    ensure_ascii=False,
                )
                + "\n"
            )
            manifest.flush()
            crosswalk.write(
                json.dumps(
                    {"id": key, "url": url, "filename": Path(url).name},
                    ensure_ascii=False,
                )
                + "\n"
            )
            crosswalk.flush()
            added += 1
            if added % 25 == 0:
                print(f"{index}/{len(documents)} handled", flush=True)
            time.sleep(DELAY)

    # Two different URLs can serve the same bytes, which is a property of the
    # page rather than an error; it is reported so the count of distinct decisions
    # is never confused with the count of links.
    digests: dict[str, list[str]] = {}
    for line in MANIFEST.read_text("utf-8").splitlines():
        row = json.loads(line)
        digests.setdefault(row["sha256"], []).append(row["id"])
    repeated = {h: ids for h, ids in digests.items() if len(ids) > 1}
    if repeated:
        print(f"\nidentical content under more than one link: {len(repeated)}")
        for ids in repeated.values():
            print(f"  {ids}")
        print(f"distinct decisions: {len(digests)}")

    total = sum(p.stat().st_size for p in TARGET.glob("*.pdf"))
    print(
        f"\n{added} downloaded, {len(known)} already known, {failed} failed; "
        f"{total / 1_073_741_824:.2f} GB in {TARGET.relative_to(ROOT)}"
    )
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
