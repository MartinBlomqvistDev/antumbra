"""Label every permit decision with the type the publisher gives it.

Step 31 of the pipeline, and the missing precondition for check 2 in
docs/VILLKORSSCHEMA.md. That check requires the corpus to decompose into
decision types, and it states the expected split as "cirka 160/38/15/14" for
permits, amendments, extensions and court judgments. The number came from
reading the listing, and nothing in the repository held it: the manifest from
step 23 carries an identifier, a permit division, a size and a hash, and no type
at all. A check cannot run against a figure nobody stored.

**The label is the publisher's own word. Reading the document gives another.** Every
decision on the Board of Agriculture's page sits behind a link whose text names
the decision type: "Tillstånd", "Ändringstillstånd", "Förlängning", "Dom MMD".
Taking the type from there follows ADR-0007, which classifies on the document's
own words rather than on an inference, and it gives the conditions layer an
independent label to test a text classifier against later. This step makes no
claim about what is inside the documents.

**The link text is safe to store, and the file name is not.** Step 23 records
why the published file names never enter the repository: they follow
Kommun_Bolag_Djurslag_Typ_Datum and at least three name natural persons. The
link text carries the type, the format and the file size, and nothing else, so
the label is kept verbatim while the file name stays outside git.

**The fourteen labels are mapped one by one, and keyword matching is wrong.**
The page uses fourteen distinct wordings for seven kinds of decision, including
one that is split by a soft hyphen and one that merges a permit with a
revocation. Each is written out below with the type it maps to. A wording that
is not in the table is typed as "annat" and withheld from the file, because an
unknown wording is the one place a party's name could enter through this route;
it is printed to the console so that a reader can see it before it is mapped.
The table only ever grows, in the sense VILLKORSSCHEMA section 2.2 requires.

**A difference against the harvest is reported as a finding.** The page is
live and the corpus grows. This step joins on the same identifier step 23 used,
the first twelve hex digits of the sha256 of the URL, and prints what is on the
page but not in the manifest and the other way round. Neither is repaired here.

Writes data/tillstand_typ.jsonl, one row per decision on the page.

Usage:
    python pipeline/31_permit_decision_types.py
"""

from __future__ import annotations

import hashlib
import json
import re
import ssl
import sys
import unicodedata
import urllib.parse
import urllib.request
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "data" / "tillstand_manifest.jsonl"
OUT = ROOT / "data" / "tillstand_typ.jsonl"

SITE = "https://jordbruksverket.se"
INDEX = (
    f"{SITE}/kontroller-och-tillsyn/miljo/"
    "stora-anlaggningar-for-uppfodning-av-fjaderfa-och-gris/"
    "tillstand-och-domar-for-stora-gris--och-fjaderfaanlaggningar"
)
UA = "Mozilla/5.0 (research; contact cm.blomqvist@gmail.com)"
TIMEOUT = 120

# Every wording the page used on 2026-09-04, with the type it stands for. The
# left column is the link text after the format and size have been trimmed off
# and the soft hyphens removed; it names a decision type and never a party.
LABELS: dict[str, str] = {
    "Tillstånd": "tillstånd",
    "Tillstånd samt återkallelse av del av tidigare tillstånd": "tillstånd",
    "Ändringstillstånd": "ändring",
    "Ändrings-tillstånd": "ändring",
    "Ändring av tillstånd": "ändring",
    "Ändring tillstånd": "ändring",
    "Ändringsbeslut": "ändring",
    "Förlängning": "förlängning",
    "Dom MMD": "dom",
    "Dom MÖD": "dom",
    "Beslut, igångsättning": "igångsättning",
    "Villkor": "villkor",
    "Slutliga villkor": "villkor",
    "Upphävande del av tillstånd": "upphävande",
}

# What VILLKORSSCHEMA section 5 says the corpus should look like, so that the
# comparison is against the written figure rather than a memory of it.
DOCUMENTED = {"tillstånd": 160, "ändring": 38, "förlängning": 15, "dom": 14}


def context() -> ssl.SSLContext | None:
    """An SSL context that works where the system trust store is incomplete."""
    try:
        import certifi
    except ImportError:
        return None
    return ssl.create_default_context(cafile=certifi.where())


def clean(text: str) -> str:
    """The link text with markup, soft hyphens and the size suffix removed."""
    text = re.sub(r"<[^>]+>", " ", text)
    # The soft hyphen splits one of the labels, and the page uses a
    # non-breaking space before the size; both are written as escapes so
    # that the source shows what it removes.
    text = text.replace("\u00ad", "").replace("\u00a0", " ")
    text = unicodedata.normalize("NFC", text)
    text = re.sub(r"\s+", " ", text).strip()
    text = re.sub(r"\s*pdf,\s*[\d.,]+\s*[kMG]?B\.?$", "", text, flags=re.IGNORECASE)
    return text.strip()


def parse_index(html: str) -> list[tuple[str, str, str]]:
    """Permit division, absolute URL and link text for every decision listed."""
    tokens = re.findall(
        r'<h3[^>]*>(.*?)</h3>|<a[^>]+href="(/download/[^"]+\.pdf)"[^>]*>(.*?)</a>',
        html,
        re.S | re.I,
    )
    found: list[tuple[str, str, str]] = []
    division = ""
    for heading, link, label in tokens:
        if heading:
            text = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", heading)).strip()
            if text:
                division = text
        elif link and division:
            found.append((division, urllib.parse.urljoin(SITE, link), clean(label)))
    # The page lists one decision twice under the same URL, as step 23 records.
    seen: set[str] = set()
    unique = []
    for division, url, label in found:
        if url in seen:
            continue
        seen.add(url)
        unique.append((division, url, label))
    return unique


def identifier(url: str) -> str:
    """The same name step 23 gave the document, so the join is exact."""
    return hashlib.sha256(url.encode("utf-8")).hexdigest()[:12]


def known() -> dict[str, dict]:
    """The harvested corpus, by identifier."""
    if not MANIFEST.exists():
        return {}
    rows = (json.loads(line) for line in MANIFEST.read_text("utf-8").splitlines())
    return {row["id"]: row for row in rows}


def main() -> int:
    """Read the listing, type every decision and report against the harvest."""
    print(f"reading {INDEX}", flush=True)
    html = urllib.request.urlopen(
        urllib.request.Request(INDEX, headers={"User-Agent": UA}),
        timeout=TIMEOUT,
        context=context(),
    ).read()
    listed = parse_index(html.decode("utf-8", "replace"))
    if not listed:
        print("no decisions found; the page layout has changed")
        return 1

    manifest = known()
    unmapped: Counter[str] = Counter()
    records = []
    for division, url, label in listed:
        kind = LABELS.get(label, "annat")
        if kind == "annat":
            unmapped[label] += 1
        records.append(
            {
                "id": identifier(url),
                "prövningsgrupp": division,
                # Only a wording the table already knows is written down. An
                # unknown one is the single way a party's name could reach the
                # repository through this step, so it stays on the console.
                "etikett": label if kind != "annat" else None,
                "typ": kind,
                "i_manifestet": identifier(url) in manifest,
            }
        )
    with OUT.open("w", encoding="utf-8", newline="\n") as out:
        for record in records:
            out.write(json.dumps(record, ensure_ascii=False) + "\n")
    print(f"{len(records)} beslut på sidan -> {OUT.name}\n")

    if unmapped:
        print("etiketter utan mappning, typade som annat:")
        for label, count in unmapped.most_common():
            print(f"  {count:3} {label}")
        print()

    listed_ids = {r["id"] for r in records}
    missing = listed_ids - set(manifest)
    extra = set(manifest) - listed_ids
    print(f"manifestet: {len(manifest)} dokument, sidan: {len(listed_ids)}")
    print(f"  på sidan men inte hämtade: {len(missing)}")
    print(f"  hämtade men inte längre på sidan: {len(extra)}\n")

    counts = Counter(r["typ"] for r in records)
    print(f"{'typ':16} {'antal':>6} {'dokumenterat':>13}")
    for kind, count in counts.most_common():
        expected = DOCUMENTED.get(kind)
        print(f"{kind:16} {count:>6} {expected if expected else '':>13}")
    print()

    for kind, expected in DOCUMENTED.items():
        found = counts.get(kind, 0)
        verdict = "stämmer" if abs(found - expected) <= 3 else "AVVIKER"
        print(f"  {kind:14} {found:>4} mot dokumenterade {expected:>4}  {verdict}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
