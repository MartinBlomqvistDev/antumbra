# Antumbra

[![CI](https://github.com/MartinBlomqvistDev/antumbra/actions/workflows/ci.yml/badge.svg)](https://github.com/MartinBlomqvistDev/antumbra/actions/workflows/ci.yml)
[![License: AGPL v3](https://img.shields.io/badge/license-AGPL--3.0-blue.svg)](LICENSE)
[![Python 3.12+](https://img.shields.io/badge/python-3.12%2B-blue.svg)](pyproject.toml)

*Making supervision measurable.*

The antumbra is the outer zone of a half-shadow: the place you stand when
something blocks the light source, far enough back to see a ring around the
edge of what is in the way. That is the project's method. The direct view is
obstructed, so the measurement happens around the edge.

## The question

The Swedish state imposes detailed conditions on large livestock
installations and publishes those conditions freely. The outcome of its own
inspections it discloses in redacted form, to varying degrees depending on
which county administrative board and which case officer answers.

The responsible agency reports, at the same time, a spread of **51
percentage points** between the county with the lowest and the county with
the highest share of inspections finding deficiencies, and writes in its
own report that the difference cannot be read out of the statistics.

Nobody has measured the gap, and nobody has tested an explanation for it.

## Three layers

**The conditions layer.** 235 environmental permit decisions for large pig
and poultry installations, 2013 to 2026, published by the Swedish Board of
Agriculture, harvested as 236 files under 237 links. 2,264 individual
conditions have been read out of the 173 files whose conditions section can be
located. The whole population, not a sample.

**The openness layer.** Three identically worded freedom-of-information
requests, sent the same morning to all 21 county administrative boards and
handled under a protocol written in advance: the same narrowing when a fee
is raised, the same request for an appealable decision, the same deadlines.
A concerns free-standing inspection reports, where appellate case law has
accepted redaction. B concerns injunction decisions with annexes, where the
secrecy provision does not apply to decisions. The contrast between A and B
is the measurement. C is a register question to the Board of Agriculture
about the split between announced and unannounced inspections, which has
never been published. Every event is logged with a verified timestamp in
`data/protokoll_logg.jsonl`, and every received file is recorded with its
sha256 in an append-only manifest; the documents themselves contain
personal data and are never committed.

**The comparison layer.** 4,690 audit reports from the European
Commission's directorate for health and food audits, 1998 to 2026, 165
countries. The same auditor, the same legal basis, the same report template
for every member state, so comparable by construction. Parsed into 11,999
recommendations with a citation graph resolved to the verbatim paragraph in
95.7 percent of edges, a dimensional model tested in dbt on BigQuery, and
an 81,292-paragraph corpus with a retrieval layer that can answer only in
verbatim quotations. Sweden has 98 reports, 8 of them on animal welfare.

## From figure to source

Every number the project publishes carries its chain: aggregate to rows,
rows to verbatim paragraphs, paragraphs to documents with checksums. The
website under `web/` renders that chain as the interface, the retrieval
service in `src/webapi.py` enforces it over HTTP, and the export step
refuses to write anything the cloud model and a local recomputation do not
agree on.

## Method

- **The subject is the state, not the animals and not the keeper.** The
  project contains no evaluative sentence about animal husbandry.
- **Never characterise, always quote.** The authority's own words, verbatim.
- **Baseline first.** The trivial explanation runs before the interesting
  one.
- **Pre-registration.** Hypotheses and the analysis plan are timestamped in
  the repository before data collection.
- **Null results are published on top.** If the hypothesis fails, that is
  the result.
- **Compare conditions only within Sweden**, where the system is one.
  Compare control regimes between countries through DG SANTE, which is
  built to be compared.
- **No personal data is published.** Aggregated by county and legal person.
- **AI assistance is declared, dated, in ADR-0014.** A language model is an
  instrument here, never a cited source; every published figure traces to a
  source document.

## What the measurement cannot show

Stated here rather than in a footnote, because it governs how the results
may be read.

**The conditions layer is not national.** Five of twelve permit divisions
carry 208 of the 237 decisions. Three have zero. Conclusions about
conditions hold for the pig and poultry belt, not the country.

**72 of the 236 permit files carried no text layer** and were read with OCR
in Swedish. OCR text segments worse than a text layer, so the two sources are
reported apart and never pooled into a headline; the difference is measured
against the documents that have a text layer, not assumed.

**Validity dates are partly proxies.** A permit is replaced only when the
new one is taken into use, and that date sits with the supervisory
authority, not in the decisions. Decision dates are used as proxies, the
error always points the same way, and every row carries its own date
source.

**The register extract counts animal keepers, not controls.** The row level
extract behind the recomputed deficiency spread carries one row per animal
keeper at a control, so a control with two keepers appears twice. The authority
stated this on 24 August 2026, and the file carries four columns and no
identifier, so the duplicates cannot be located and the rows cannot be collapsed.
Every figure taken from it is a figure over keeper rows, and the share over rows
equals the share over controls only where duplicated keepers carry the same
deficiency flag.

**The deficiency flag is not split by species.** Documents are assigned to an
animal by counting terms, and that assignment was checked against eighteen
hand-read documents on 25 August 2026 without a single wrong animal. The
deficiency field, however, sits on the control and not on the animal, and one of
the eighteen records its faults in the horse facilities of a holding that also
keeps birds. A deficiency share computed per species can therefore carry a fault
found in an animal outside the three the project measures.

**The law on redaction is unsettled.** The appellate courts have ruled in
different directions and the Supreme Administrative Court has not decided
the question. Differences between authorities are therefore not in
themselves evidence of misapplied law.

**Observational data cannot separate all explanations.** Risk-based
selection, species mix, inspection-type mix and registration practice can
each produce the same pattern as the tested hypothesis. They are reported
as unresolved confounding.

**Installations below the threshold are not in the conditions layer.** The
IED boundary sits at 40,000 poultry, 2,000 fattening pigs or 750 sows, and
smaller installations have no published permits to compare against.

## Reproduce

Requires Python 3.12. The DG SANTE harvest uses only the standard library;
`pydantic` carries the data contracts.

```bash
pip install -e ".[dev]"
python pipeline/01_harvest_index.py        # one search per year, 1998 to 2027
python pipeline/02_harvest_details.py      # one detail page per audit
python pipeline/03_download_reports.py     # EU-27, English reports and annexes
python pipeline/04_build_manifest.py       # sha256 and source link per file
python pipeline/05_classify_annexes.py     # annexes classed on their own words
python pipeline/06_ocr_annexes.py          # OCR where scanned
python pipeline/07_parse_recommendations.py  # recommendations and citation edges
python pipeline/08_parse_paragraphs.py     # the cited paragraphs, graph nodes
python pipeline/09_link_action_plans.py    # member state commitments linked back
python pipeline/10_build_warehouse.py      # the star schema in Parquet
python pipeline/11_build_dashboard.py      # docs/dashboard.html
python pipeline/12_load_bigquery.py --dry-run  # shows what would be loaded
python pipeline/13_hash_deliveries.py      # sha256 over received Swedish documents
python pipeline/14_embed_paragraphs.py     # local embeddings for retrieval
python pipeline/15_export_web_data.py      # the site's data, verified twice
python pipeline/16_bake_examples.py        # example answers via the live code path
python pipeline/17_package_hf_dataset.py   # the corpus packaged for Hugging Face
python pipeline/18_analyse_masking.py      # redaction kind per received document
python pipeline/19_ocr_deliveries.py       # Swedish OCR over the scanned deliveries
python pipeline/20_extract_species.py      # which animals each document concerns
python pipeline/21_contrast_within_species.py  # class A against B, within species
python pipeline/22_deficiency_gap.py       # the spread between counties, recomputed
python pipeline/23_download_permits.py     # the permit decisions, named by hash
python pipeline/24_condition_baseline.py   # are the conditions standard text?
python pipeline/25_ocr_permits.py          # Swedish OCR over the scanned permits
python pipeline/26_hidden_text.py          # text covered by something that is not black
python pipeline/27_parse_announced.py      # announced or not, per county and year
python pipeline/28_unannounced_hypothesis.py  # the pre-registered hypothesis
python pipeline/29_check_grounds.py        # is the register of cited grounds closed?
python pipeline/30_draw_species_sample.py  # the blind sample the species rule is checked against
python pipeline/31_permit_decision_types.py   # what the publisher calls each permit decision
```

Two reports are not pipeline steps, because they derive nothing and write
nothing. The first reads the protocol log and prints what each of the 43
requests is waiting for, which side owes the next move, and when it falls due.
The second re-runs the check that the redaction measure's image method rests
on, by pointing it at the born-digital documents where the text method already
holds an answer:

```bash
python src/open_items.py
python src/validate_image_method.py
```

The steps write to `data/`. The slow ones are resumable and skip what is
already fetched. Step 03 downloads 2.2 GB to `pdf/`, which is never
committed. Step 06 needs the Tesseract binary plus `pip install -e
".[ocr]"`, step 10 needs `".[warehouse]"`, steps 14 to 16 need
`".[retrieval]"`, and the HTTP service needs `".[api]"`. The website is a
static Next.js export:

```bash
cd web && npm ci && npm run build
```

Quality gates, the same three CI runs on every push:

```bash
ruff check . && ruff format --check .
pytest
```

The 152 tests carry guarantees beyond ordinary unit testing: the generated
schema module must match its design document, the figures in the
documentation must hold against the data files, no personal data may exist
in the repository, the retrieval layer must refuse paraphrases, false
citations and stale embeddings, and the web export must refuse to write
numbers the cloud marts and a local recomputation disagree on.

## Structure

```
docs/VERIFIERAT.md     verified facts with date and source
docs/BEGARANMALL.md    the three request templates, legal grounds, protocol
docs/VILLKORSSCHEMA.md data contract with rationale and checks
docs/DGSANTE.md        the comparison corpus, structure and volume
docs/WEBB.md           the website plan, in decision form
docs/adr/              dated decisions on scope and method
docs/POWERBI.md        build notes for the .pbix over the same model
dbt/                   staging and marts on top of the star schema
data/                  derived datasets and the public event log
src/                   data contracts, retrieval, the HTTP service
pipeline/              numbered steps, run in order
web/                   the site: Swedish first, an English mirror
tests/                 unit tests and repository invariants
CONTRIBUTING.md        code standard and what is never committed
```

Swedish project prose lives in `docs/`; code, comments and this file are in
English.

## Status

As of 7 August 2026: the Swedish collection is running under the protocol
(day 4: 43 requests sent, 14 of 21 county boards have delivered, 195 files
verified, no fee paid), the comparison layer and the website are built, and
no analytical result has been published. The repository stays private until
the collection protocol closes.

## License and citation

Code is AGPL-3.0 (see `LICENSE`). Derived datasets in `data/` are CC BY
4.0. Received authority documents are not redistributed at all. To cite the
project, see `CITATION.cff`.
