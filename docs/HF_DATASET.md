---
license: cc-by-4.0
language:
  - en
pretty_name: "DG SANTE audits of member state control systems, 1998-2026"
tags:
  - official-controls
  - food-safety
  - animal-welfare
  - public-administration
  - transparency
  - european-union
size_categories:
  - 10K<n<100K
---

# DG SANTE audits of member state control systems, 1998-2026

Audit reports from the European Commission's Directorate-General for
Health and Food Safety (DG SANTE, formerly the Food and Veterinary
Office), parsed into a citation-resolved dimensional model: 4,690 audits
across 165 countries, 11,999 recommendations from the EU-27 full-text
corpus, a recommendation-to-paragraph citation graph resolved to the
verbatim source paragraph in 95.7 percent of edges, and the 81,292
numbered paragraphs the graph points into.

The same auditor, the same legal basis and the same report template apply
to every member state, so the corpus is comparable by construction. The
dataset is the comparison layer of [Antumbra], a project measuring Swedish
animal welfare supervision; it is published separately because the corpus
answers questions far beyond that use.

## Files

| File | Rows | Grain |
| --- | --- | --- |
| `dim_country.parquet` | 165 | one row per audited country |
| `dim_audit.parquet` | 4,690 | one row per audit: reference, country, year, period, title |
| `dim_paragraph.parquet` | 81,292 | one row per numbered paragraph, verbatim text included |
| `fact_recommendation.parquet` | 11,999 | one row per recommendation, verbatim text included |
| `fact_citation.parquet` | 7,821 | one edge per stated basis: recommendation to paragraph |
| `fact_commitment.parquet` | 5,710 | one row per member state response to a recommendation |
| `manifest.jsonl` | one row per source file | source URL, sha256 and byte size of every harvested document |

Surrogate keys join the tables: `country_key`, `audit_key`,
`paragraph_key`, `recommendation_key`. An unresolved citation keeps a null
`paragraph_key` rather than being dropped; the count of what could not be
joined is part of the dataset.

## Provenance and method

Every document was harvested from the Commission's public audit register
(ec.europa.eu/food/audits-analysis) with per-file sha256 recorded in
`manifest.jsonl`. Full text was downloaded for the EU-27 English reports;
for the remaining countries the register metadata is included. Parsing is
deterministic and open source: numbered pipeline steps 01 to 10 in the
Antumbra repository, with 152 tests covering, among other things, that
recommendation parsing matches its design document and that a citation is
parsed literally from the report's own wording, never inferred.

Two figures worth knowing before use: 2,010 of 11,999 recommendations
state their evidential basis explicitly, and the citation graph resolves
95.7 percent of stated citations to a numbered paragraph. Both are
properties of the reports, not of the parser, and both are reported rather
than smoothed over.

## Limitations

- Full text covers the EU-27; other countries appear with register
  metadata only.
- Scanned annexes passed through OCR (step 06) with per-file confidence
  recorded; paragraph text quality varies with the source scan.
- The corpus ends at the harvest date. Audits published later are absent.
- Names of officials and company representatives may appear where the
  Commission published them; the source documents are public Commission
  publications. The dataset contains no Swedish personal data and nothing
  from the Antumbra freedom-of-information collection.

## License and attribution

The underlying documents are European Commission publications, reusable
under Commission Decision 2011/833/EU on the reuse of Commission
documents. The parsed dataset is published under CC BY 4.0. Cite the
European Commission as the source of the report texts, and this dataset
for the parsed structure.

## Citation

See `CITATION.cff` in the Antumbra repository.

[Antumbra]: https://github.com/MartinBlomqvistDev/antumbra
