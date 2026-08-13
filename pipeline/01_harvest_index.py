"""Harvest the DG SANTE audit report index, one search per year.

The search at ec.europa.eu/food/audits-analysis/audit-report is a
server-rendered Symfony form, not a SPA. One POST per year returns a
result table with reference, country, audit period, subject and a link
to the detail page.

Writes data/dgsante_index.json.

Usage:
    python pipeline/01_harvest_index.py [--from 1998] [--to 2027]
"""

from __future__ import annotations

import argparse
import http.cookiejar
import json
import re
import sys
import urllib.parse
import urllib.request
from pathlib import Path

URL = "https://ec.europa.eu/food/audits-analysis/audit-report"
UA = "Mozilla/5.0 (research; contact cm.blomqvist@gmail.com)"
OUT = Path(__file__).resolve().parent.parent / "data" / "dgsante_index.json"


def strip_tags(s: str) -> str:
    """Remove tags and collapse whitespace."""
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", s)).strip()


def harvest_year(opener: urllib.request.OpenerDirector, year: int) -> list[dict]:
    """Post the search form for one year and parse the result rows.

    A fresh CSRF token is fetched per request; the token is bound to the
    session cookie the opener carries.
    """
    page = opener.open(URL, timeout=60).read().decode("utf-8", "replace")
    token_pattern = r'name="report_search\[_token\]"[^>]*value="([^"]+)"'
    token = re.search(token_pattern, page).group(1)
    data = urllib.parse.urlencode(
        {
            "report_search[_token]": token,
            "report_search[basic][year]": str(year),
            "report_search[basic][report_number]": "",
            "report_search[basic][searchBasic]": "",
        }
    ).encode()
    request = urllib.request.Request(URL, data=data)
    html = opener.open(request, timeout=120).read().decode("utf-8", "replace")

    rows: list[dict] = []
    for tr in re.findall(r"<tr[^>]*>(.*?)</tr>", html, re.S):
        cells = [strip_tags(c) for c in re.findall(r"<td[^>]*>(.*?)</td>", tr, re.S)]
        detail = re.findall(r"audit-report/details/(\d+)", tr)
        if len(cells) >= 4 and detail:
            rows.append(
                {
                    "ref": cells[0],
                    "country": cells[1],
                    "period": cells[2],
                    "subject": cells[3],
                    "detail_id": detail[0],
                    "year": year,
                }
            )
    return rows


def main() -> int:
    """Parse arguments, harvest every year in range and write the index."""
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--from", dest="start", type=int, default=1998)
    ap.add_argument("--to", dest="end", type=int, default=2027)
    args = ap.parse_args()

    opener = urllib.request.build_opener(
        urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar())
    )
    opener.addheaders = [("User-Agent", UA)]

    all_rows: list[dict] = []
    failed: list[int] = []
    for year in range(args.start, args.end + 1):
        try:
            rows = harvest_year(opener, year)
            all_rows.extend(rows)
            print(f"{year} {len(rows)}", flush=True)
        except Exception as exc:
            failed.append(year)
            print(f"{year} FAILED {exc}", flush=True)

    # The index is rewritten whole, so a partial harvest would silently shrink
    # it, and a caller comparing the index against the corpus would read the
    # gap as "nothing new published". Write nothing unless every year answered.
    if failed:
        print(f"NOT WRITTEN, {len(failed)} years failed: {failed}")
        return 1

    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(all_rows, ensure_ascii=False), encoding="utf-8")
    print(f"TOTAL {len(all_rows)} -> {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
