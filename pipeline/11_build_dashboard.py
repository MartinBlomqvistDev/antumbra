"""Render the DG SANTE layer as a self-contained dashboard.

Step 11 of the pipeline; run 10_build_warehouse.py first. Reads the star
schema and writes one HTML file that needs no server, no account and no
network: the charts are inline SVG and the styles and scripts are inline too.

The page is also the specification for the Power BI version. Same measures,
same order, same wording, so building the .pbix is a matter of reproducing
something that already exists rather than deciding what to show.

Every chart carries a table view, because a value a reader can only reach by
hovering is a value some readers cannot reach at all. The limitations section
is part of the page, not a footnote: what the measurement cannot show decides
how its results may be read.

Writes docs/dashboard.html.

Usage:
    python pipeline/11_build_dashboard.py
"""

from __future__ import annotations

import html
import sys
from pathlib import Path

import pyarrow.parquet as pq

ROOT = Path(__file__).resolve().parent.parent
WAREHOUSE = ROOT / "data" / "warehouse"
OUT = ROOT / "docs" / "dashboard.html"

# The two categorical slots this page uses, validated in both modes with
# scripts/validate_palette.js: worst adjacent CVD deltaE 24.7 light and 26.8
# dark against a target of 8, contrast above 3:1 on both surfaces.
SERIES = ("--series-1", "--series-2")

FIRST_LINKED_YEAR = 2014


def load(name: str) -> list[dict]:
    """Read one warehouse table."""
    return pq.read_table(WAREHOUSE / f"{name}.parquet").to_pylist()


def group_countries(
    recommendations: list[dict], audits: list[dict], countries: list[dict]
) -> list[dict]:
    """Aggregate the recommendation fact to one row per EU-27 country."""
    country_of = {row["country_key"]: row["country"] for row in countries}
    in_eu27 = {row["country_key"] for row in countries if row["in_eu27"]}
    audit_country = {row["audit_key"]: row["country_key"] for row in audits}

    rows: dict[str, dict] = {}
    for record in recommendations:
        key = audit_country.get(record["audit_key"])
        if key not in in_eu27:
            continue
        name = country_of[key]
        row = rows.setdefault(
            name,
            {"country": name, "recommendations": 0, "states_basis": 0, "answered": 0},
        )
        row["recommendations"] += 1
        row["states_basis"] += bool(record["states_its_basis"])
        row["answered"] += bool(record["is_answered"])
    return sorted(rows.values(), key=lambda r: -r["recommendations"])


def group_years(
    recommendations: list[dict], audits: list[dict], countries: list[dict]
) -> list[dict]:
    """Aggregate the recommendation fact to one row per year, EU-27 only."""
    in_eu27 = {row["country_key"] for row in countries if row["in_eu27"]}
    audit = {row["audit_key"]: row for row in audits}

    rows: dict[int, dict] = {}
    for record in recommendations:
        parent = audit.get(record["audit_key"])
        if parent is None or parent["country_key"] not in in_eu27:
            continue
        year = parent["year"]
        if year is None or year < FIRST_LINKED_YEAR:
            continue
        row = rows.setdefault(
            year, {"year": year, "recommendations": 0, "states_basis": 0, "answered": 0}
        )
        row["recommendations"] += 1
        row["states_basis"] += bool(record["states_its_basis"])
        row["answered"] += bool(record["is_answered"])
    # The newest audits have no action plan yet, which would read as a
    # collapse rather than as a lag; they are left out of the trend and said
    # so in the note beneath it.
    return [row for row in sorted(rows.values(), key=lambda r: r["year"])][:-2]


def escape(value: object) -> str:
    """Escape a value for HTML."""
    return html.escape(str(value), quote=True)


# Swedish groups thousands with a thin space rather than a comma.
THIN_SPACE = chr(0x2009)


def thousands(value: int) -> str:
    """Group thousands the way Swedish prose does."""
    return f"{value:,}".replace(",", THIN_SPACE)


def bar_chart(rows: list[dict], chart_id: str) -> str:
    """Horizontal bars, one per country, single series in one colour.

    A single series wears one hue for every bar: colouring each bar by its own
    length would double-encode what the bar already shows.
    """
    row_height, bar_height, gap = 26, 14, 2
    label_width, value_width = 132, 58
    plot_width = 420
    height = len(rows) * row_height + 34
    highest = max(row["recommendations"] for row in rows)

    parts = [
        f'<svg class="chart" viewBox="0 0 {label_width + plot_width + value_width} '
        f'{height}" role="img" aria-labelledby="{chart_id}-title">',
        f'<title id="{chart_id}-title">Rekommendationer per land i EU-27</title>',
    ]
    for tick in range(0, highest + 1, 250):
        x = label_width + plot_width * tick / highest
        parts.append(
            f'<line class="grid" x1="{x:.1f}" y1="0" x2="{x:.1f}" '
            f'y2="{len(rows) * row_height}"/>'
        )
        parts.append(
            f'<text class="tick" x="{x:.1f}" y="{len(rows) * row_height + 16}" '
            f'text-anchor="middle">{thousands(tick)}</text>'
        )
    for index, row in enumerate(rows):
        y = index * row_height + (row_height - bar_height) / 2
        width = plot_width * row["recommendations"] / highest
        share = row["answered"] / row["recommendations"]
        parts.append(
            f'<g class="mark" tabindex="0" role="listitem" '
            f'data-tip="{escape(row["country"])}: '
            f"{thousands(row['recommendations'])} rekommendationer, "
            f'{share:.0%} besvarade">'
        )
        parts.append(
            f'<text class="label" x="{label_width - 8}" y="{y + 11}" '
            f'text-anchor="end">{escape(row["country"])}</text>'
        )
        parts.append(
            f'<rect class="bar" x="{label_width}" y="{y}" '
            f'width="{max(width, 1):.1f}" height="{bar_height - gap}" rx="4"/>'
        )
        parts.append(
            f'<rect class="bar-square" x="{label_width}" y="{y}" width="4" '
            f'height="{bar_height - gap}"/>'
        )
        parts.append(
            f'<text class="value" x="{label_width + width + 8:.1f}" y="{y + 11}">'
            f"{thousands(row['recommendations'])}</text>"
        )
        parts.append("</g>")
    parts.append("</svg>")
    return "".join(parts)


def line_chart(rows: list[dict], chart_id: str) -> str:
    """Two series over time, with a legend and end labels."""
    width, height = 620, 250
    left, right, top, bottom = 34, 92, 16, 34
    plot_w = width - left - right
    plot_h = height - top - bottom
    years = [row["year"] for row in rows]

    def point(index: int, share: float) -> tuple[float, float]:
        x = left + plot_w * index / max(len(rows) - 1, 1)
        return x, top + plot_h * (1 - share)

    series = [
        ("Anger sin grund", [r["states_basis"] / r["recommendations"] for r in rows]),
        ("Besvarade i plan", [r["answered"] / r["recommendations"] for r in rows]),
    ]
    parts = [
        f'<svg class="chart" viewBox="0 0 {width} {height}" role="img" '
        f'aria-labelledby="{chart_id}-title">',
        f'<title id="{chart_id}-title">Andel rekommendationer som anger sin '
        f"grund och som besvarats, EU-27</title>",
    ]
    for tick in (0, 0.25, 0.5, 0.75, 1.0):
        y = top + plot_h * (1 - tick)
        parts.append(
            f'<line class="grid" x1="{left}" y1="{y:.1f}" '
            f'x2="{left + plot_w}" y2="{y:.1f}"/>'
        )
        parts.append(
            f'<text class="tick" x="{left - 8}" y="{y + 4:.1f}" '
            f'text-anchor="end">{tick:.0%}</text>'
        )
    for index, year in enumerate(years):
        if index % 2 == 0 or index == len(years) - 1:
            x, _ = point(index, 0)
            parts.append(
                f'<text class="tick" x="{x:.1f}" y="{height - 12}" '
                f'text-anchor="middle">{year}</text>'
            )
    for slot, (name, values) in enumerate(series):
        colour = f"var({SERIES[slot]})"
        path = " ".join(
            ("M" if i == 0 else "L") + f"{point(i, v)[0]:.1f} {point(i, v)[1]:.1f}"
            for i, v in enumerate(values)
        )
        parts.append(f'<path class="line" d="{path}" stroke="{colour}"/>')
        for i, value in enumerate(values):
            x, y = point(i, value)
            parts.append(
                f'<g class="mark" tabindex="0" data-tip="{escape(years[i])}, '
                f'{escape(name)}: {value:.0%}">'
                f'<circle class="dot" cx="{x:.1f}" cy="{y:.1f}" r="4" '
                f'fill="{colour}"/></g>'
            )
        end_x, end_y = point(len(values) - 1, values[-1])
        parts.append(
            f'<text class="value" x="{end_x + 10:.1f}" y="{end_y + 4:.1f}">'
            f"{values[-1]:.0%}</text>"
        )
    parts.append("</svg>")
    legend = "".join(
        f'<span class="key"><span class="swatch" '
        f'style="background:var({SERIES[slot]})"></span>{escape(name)}</span>'
        for slot, (name, _) in enumerate(series)
    )
    return f'<div class="legend">{legend}</div>' + "".join(parts)


def table(headers: list[str], rows: list[list[str]], table_id: str) -> str:
    """The table twin of a chart, collapsed by default."""
    head = "".join(f"<th>{escape(h)}</th>" for h in headers)
    body = "".join(
        "<tr>" + "".join(f"<td>{escape(cell)}</td>" for cell in row) + "</tr>"
        for row in rows
    )
    return (
        f'<details class="table-view"><summary>Visa som tabell</summary>'
        f'<table id="{table_id}"><thead><tr>{head}</tr></thead>'
        f"<tbody>{body}</tbody></table></details>"
    )


def tile(label: str, value: str, note: str) -> str:
    """One stat tile."""
    return (
        f'<div class="tile"><p class="tile-label">{escape(label)}</p>'
        f'<p class="tile-value">{escape(value)}</p>'
        f'<p class="tile-note">{escape(note)}</p></div>'
    )


def build() -> str:
    """Assemble the page."""
    countries = load("dim_country")
    audits = load("dim_audit")
    recommendations = load("fact_recommendation")
    citations = load("fact_citation")
    commitments = load("fact_commitment")

    per_country = group_countries(recommendations, audits, countries)
    per_year = group_years(recommendations, audits, countries)

    total = len(recommendations)
    stating = sum(1 for r in recommendations if r["states_its_basis"])
    answered = sum(1 for r in recommendations if r["is_answered"])
    resolved = sum(1 for r in citations if r["resolved"])
    agree = [c for c in citations if c["heading_agrees"] is not None]
    agreeing = sum(1 for c in agree if c["heading_agrees"])

    tiles = "".join(
        [
            tile("Revisioner i korpusen", thousands(len(audits)), "1998 till 2027"),
            tile(
                "Rapporter lästa",
                thousands(len({r["report_path"] for r in recommendations})),
                "av 2 940 engelska EU-27-rapporter",
            ),
            tile(
                "Kanter i citatgrafen",
                thousands(len(citations)),
                f"{resolved / len(citations):.0%} pekar på ett funnet stycke",
            ),
            tile(
                "Åtaganden i åtgärdsplaner",
                thousands(len(commitments)),
                f"{answered / total:.0%} av rekommendationerna besvarade",
            ),
        ]
    )

    country_table = table(
        ["Land", "Rekommendationer", "Anger sin grund", "Besvarade"],
        [
            [
                row["country"],
                thousands(row["recommendations"]),
                f"{row['states_basis'] / row['recommendations']:.0%}",
                f"{row['answered'] / row['recommendations']:.0%}",
            ]
            for row in per_country
        ],
        "country-table",
    )
    year_table = table(
        ["År", "Rekommendationer", "Anger sin grund", "Besvarade"],
        [
            [
                row["year"],
                thousands(row["recommendations"]),
                f"{row['states_basis'] / row['recommendations']:.0%}",
                f"{row['answered'] / row['recommendations']:.0%}",
            ]
            for row in per_year
        ],
        "year-table",
    )

    return PAGE.format(
        hero=thousands(total),
        tiles=tiles,
        country_chart=bar_chart(per_country, "countries"),
        country_table=country_table,
        year_chart=line_chart(per_year, "years"),
        year_table=year_table,
        stating=thousands(stating),
        stating_share=f"{stating / total:.0%}",
        resolved=thousands(resolved),
        resolved_share=f"{resolved / len(citations):.0%}",
        agree_share=f"{agreeing / len(agree):.0%}",
        first_year=per_year[0]["year"],
        last_year=per_year[-1]["year"],
    )


PAGE = """<!doctype html>
<html lang="sv"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Antumbra: kommissionens revisioner av medlemsstaternas kontrollsystem</title>
<style>
:root {{
  color-scheme: light;
  --surface-1: #fcfcfb; --plane: #f9f9f7;
  --text-primary: #0b0b0b; --text-secondary: #52514e; --muted: #898781;
  --grid: #e1e0d9; --axis: #c3c2b7; --border: rgba(11,11,11,0.10);
  --series-1: #2a78d6; --series-2: #eb6834;
}}
@media (prefers-color-scheme: dark) {{
  :root:where(:not([data-theme="light"])) {{
    color-scheme: dark;
    --surface-1: #1a1a19; --plane: #0d0d0d;
    --text-primary: #ffffff; --text-secondary: #c3c2b7; --muted: #898781;
    --grid: #2c2c2a; --axis: #383835; --border: rgba(255,255,255,0.10);
    --series-1: #3987e5; --series-2: #d95926;
  }}
}}
:root[data-theme="dark"] {{
  color-scheme: dark;
  --surface-1: #1a1a19; --plane: #0d0d0d;
  --text-primary: #ffffff; --text-secondary: #c3c2b7; --muted: #898781;
  --grid: #2c2c2a; --axis: #383835; --border: rgba(255,255,255,0.10);
  --series-1: #3987e5; --series-2: #d95926;
}}
* {{ box-sizing: border-box; }}
body {{
  margin: 0; padding: 32px 20px 64px;
  background: var(--plane); color: var(--text-primary);
  font: 15px/1.6 system-ui, -apple-system, "Segoe UI", sans-serif;
}}
main {{ max-width: 900px; margin: 0 auto; }}
h1 {{ font-size: 26px; line-height: 1.25; margin: 0 0 6px; }}
h2 {{ font-size: 19px; margin: 44px 0 4px; }}
p.lede {{ color: var(--text-secondary); margin: 0 0 28px; max-width: 62ch; }}
p.note {{ color: var(--text-secondary); font-size: 14px; max-width: 68ch; }}
.card {{
  background: var(--surface-1); border: 1px solid var(--border);
  border-radius: 10px; padding: 20px; margin-top: 14px; overflow-x: auto;
}}
.hero {{ font-size: 56px; font-weight: 600; line-height: 1; margin: 0; }}
.hero-label {{ color: var(--text-secondary); margin: 6px 0 0; }}
.tiles {{ display: grid; gap: 12px; grid-template-columns: repeat(auto-fit,
  minmax(190px, 1fr)); margin-top: 22px; }}
.tile {{ background: var(--surface-1); border: 1px solid var(--border);
  border-radius: 10px; padding: 14px 16px; }}
.tile-label {{ margin: 0; color: var(--text-secondary); font-size: 13px; }}
.tile-value {{ margin: 4px 0 2px; font-size: 26px; font-weight: 600; }}
.tile-note {{ margin: 0; color: var(--muted); font-size: 13px; }}
.chart {{ width: 100%; height: auto; display: block; }}
.grid {{ stroke: var(--grid); stroke-width: 1; }}
.bar {{ fill: var(--series-1); }}
.bar-square {{ fill: var(--series-1); }}
.line {{ fill: none; stroke-width: 2; stroke-linejoin: round;
  stroke-linecap: round; }}
.dot {{ stroke: var(--surface-1); stroke-width: 2; }}
.label {{ fill: var(--text-secondary); font-size: 12px; }}
.value {{ fill: var(--text-primary); font-size: 12px; font-weight: 600; }}
.tick {{ fill: var(--muted); font-size: 11px; font-variant-numeric: tabular-nums; }}
.mark {{ cursor: default; outline: none; }}
.mark:hover .bar, .mark:focus-visible .bar {{ opacity: 0.82; }}
.mark:focus-visible .dot {{ stroke: var(--text-primary); }}
.legend {{ display: flex; gap: 18px; margin-bottom: 8px; font-size: 13px;
  color: var(--text-secondary); }}
.key {{ display: inline-flex; align-items: center; gap: 7px; }}
.swatch {{ width: 12px; height: 12px; border-radius: 3px; display: inline-block; }}
.table-view {{ margin-top: 12px; }}
.table-view summary {{ cursor: pointer; color: var(--text-secondary);
  font-size: 14px; }}
table {{ border-collapse: collapse; margin-top: 10px; font-size: 14px;
  font-variant-numeric: tabular-nums; }}
th, td {{ text-align: left; padding: 5px 16px 5px 0;
  border-bottom: 1px solid var(--border); }}
th {{ color: var(--text-secondary); font-weight: 600; }}
#tip {{
  position: fixed; pointer-events: none; opacity: 0; transition: opacity .1s;
  background: var(--surface-1); color: var(--text-primary);
  border: 1px solid var(--border); border-radius: 7px; padding: 6px 10px;
  font-size: 13px; box-shadow: 0 2px 10px rgba(0,0,0,.14); max-width: 280px;
}}
footer {{ margin-top: 52px; color: var(--muted); font-size: 13px; }}
button.theme {{ background: var(--surface-1); color: var(--text-secondary);
  border: 1px solid var(--border); border-radius: 7px; padding: 5px 11px;
  font: inherit; font-size: 13px; cursor: pointer; float: right; }}
</style></head>
<body>
<main>
<button class="theme" id="theme">Byt ljust och mörkt</button>
<h1>Kommissionens revisioner av medlemsstaternas kontrollsystem</h1>
<p class="lede">Samma revisor, samma rättsliga grund och samma rapportmall för
alla medlemsstater, alltså jämförbara till sin konstruktion. Sidan visar vad
korpusen innehåller och hur långt kedjan från iakttagelse till åtagande går att
följa i data.</p>

<p class="hero">{hero}</p>
<p class="hero-label">rekommendationer utlästa ur revisionsrapporterna</p>
<div class="tiles">{tiles}</div>

<h2>Rekommendationer per land</h2>
<p class="note">EU-27. Volymen följer i stort hur ofta ett land reviderats, inte
hur väl dess kontrollsystem fungerar; antalet rekommendationer är ett mått på
granskningens omfattning, inte ett betyg.</p>
<div class="card">{country_chart}{country_table}</div>

<h2>Hur långt kedjan går att följa, {first_year} till {last_year}</h2>
<p class="note">Två andelar per år. <em>Anger sin grund</em> är de
rekommendationer som skriver ut vilken slutsats de vilar på, vilket är det som
gör citatgrafen möjlig. <em>Besvarade i plan</em> är de som återfinns i
medlemsstatens åtgärdsplan. De två senaste åren utelämnas: deras åtgärdsplaner
är ännu inte publicerade, och en nolla där vore en eftersläpning och inte ett
resultat.</p>
<div class="card">{year_chart}{year_table}</div>

<h2>Citatgrafen</h2>
<p class="note">{stating} rekommendationer, {stating_share} av alla, skriver ut
vilken slutsats de vilar på. Praktiken börjar 2014; före det finns inga
korsreferenser alls. {resolved} av kanterna, {resolved_share}, pekar på ett
stycke som faktiskt gick att hitta i rapporten.</p>
<p class="note">Styckets egen rubrik och rapportens citat är två oberoende
läsningar av samma stycke. De är eniga i {agree_share} av de fall där båda
säger något. Oenigheten redovisas rad för rad i datat i stället för att jämkas
ihop, eftersom avvikelsen mellan två läsningar är det bästa kvalitetsmått
lagret har.</p>

<h2>Vad sidan inte visar</h2>
<p class="note">Redovisas här och inte i en fotnot, eftersom det avgör hur
siffrorna får läsas.</p>
<p class="note"><strong>Korsreferenserna är en delmängd.</strong> Bara knappt en
fjärdedel av rapporterna skriver ut vilken slutsats en rekommendation vilar på.
Att beskriva hela korpusen som en graf vore en överdrift.</p>
<p class="note"><strong>Antalet rekommendationer är inget betyg.</strong> Det
speglar hur mycket som granskats, inte hur väl ett kontrollsystem fungerar. Ett
land med många revisioner får många rekommendationer.</p>
<p class="note"><strong>Parsningen är inte fullständig.</strong> Rapporter vars
numrering inte går att följa lämnas oparsade i stället för att gissas, och
antalet står i projektets dokumentation. Det som inte gick att läsa är räknat,
inte utjämnat.</p>
<p class="note"><strong>Åtgärdsplaner saknas för de nyaste revisionerna</strong>
och för allt före 2011, då praktiken inte fanns.</p>

<footer>
Källa: Europeiska kommissionen, generaldirektoratet för hälsa och
livsmedelssäkerhet, revisionsrapporter 1998 till 2027. Byggd ur den öppna
korpusen med <code>pipeline/11_build_dashboard.py</code>. Källdokumenten
återdistribueras inte; ett proveniensmanifest med sha256 per fil ligger i repot.
</footer>
</main>
<div id="tip" role="status" aria-live="polite"></div>
<script>
const tip = document.getElementById("tip");
for (const mark of document.querySelectorAll(".mark")) {{
  const show = (event) => {{
    tip.textContent = mark.dataset.tip;
    tip.style.opacity = "1";
    const box = mark.getBoundingClientRect();
    const x = event.clientX ?? box.left + box.width / 2;
    const y = event.clientY ?? box.top;
    tip.style.left = Math.min(x + 14, innerWidth - 300) + "px";
    tip.style.top = Math.max(y - 42, 8) + "px";
  }};
  const hide = () => {{ tip.style.opacity = "0"; }};
  mark.addEventListener("mouseenter", show);
  mark.addEventListener("mousemove", show);
  mark.addEventListener("mouseleave", hide);
  mark.addEventListener("focus", show);
  mark.addEventListener("blur", hide);
}}
document.getElementById("theme").addEventListener("click", () => {{
  const dark = matchMedia("(prefers-color-scheme: dark)").matches;
  const current = document.documentElement.dataset.theme
    || (dark ? "dark" : "light");
  document.documentElement.dataset.theme = current === "dark" ? "light" : "dark";
}});
</script>
</body></html>
"""


def main() -> int:
    """Render the dashboard."""
    OUT.write_text(build(), encoding="utf-8", newline="\n")
    print(f"{OUT.relative_to(ROOT)} written, {OUT.stat().st_size // 1024} KiB")
    return 0


if __name__ == "__main__":
    sys.exit(main())
