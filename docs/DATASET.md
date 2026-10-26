---
license: cc-by-4.0
language:
  - sv
pretty_name: "Swedish animal welfare supervision measured through parallel freedom-of-information requests, 2026"
tags:
  - animal-welfare
  - official-controls
  - freedom-of-information
  - public-administration
  - transparency
  - sweden
size_categories:
  - 1K<n<10K
---

# Swedish animal welfare supervision, measured 2026

Twenty-four files holding what 43 freedom-of-information requests to Sweden's
21 county administrative boards and the Board of Agriculture produced, the
measurement built from them, and the complete record of how every request was
handled. The requests went out on 3 August 2026, worded identically, and were
handled under a protocol written before the first answer arrived, so a
difference in outcome is a difference between authorities and not between
questions.

The dataset is the Swedish layer of [Antumbra]. The European comparison layer,
parsed from the Commission's audits of member state control systems, is a
separate dataset with its own card in `docs/HF_DATASET.md`.

## What it measures

Two document classes were requested from every county with the same sentence:
the most recent inspection reports (class A) and the most recent enforcement
decisions (class B). Both classes carry the same kind of information under the
same secrecy provision, so the share of documents that arrive redacted is
comparable across the 21 counties.

- **Class A: 170 documents from 17 counties, 109 redacted, 64,1 per cent.**
- **Class B: 140 documents from 18 counties, 32 redacted, 22,9 per cent.**
- Every figure is reproducible from the files below, and the gaps are declared
  rather than estimated: see Limitations.

## Files

| File | Rows | Grain |
| --- | --- | --- |
| `protokoll_logg.jsonl` | 612 | one row per event: date, clock time read from the system, channel, authority, request and note |
| `korrespondens.jsonl` | 198 | the authorities' own messages verbatim, 262 messages in all, each row saying in `utelamnat` what it leaves out |
| `p12_avsant_manifest.jsonl` | 22 | the packets sent to each authority before publication, with sha256 per letter |
| `leveranser_manifest.jsonl` | 692 | one row per received file: path, byte size, sha256 and when it was recorded |
| `maskning.jsonl` | 343 | one row per measured document: pages, characters, bars, boxes, covered area and which method measured it |
| `kontrast.jsonl` | 67 | the redaction share per authority, class and dominant animal |
| `djurslag.jsonl` | 343 | the animals named in each document, and which one dominates |
| `dold_text.jsonl` | 298 | text present but not visible, measured per document |
| `sekretessgrunder.jsonl` | 27 | the provisions an authority invoked, quoted verbatim, with the role of the signer and never the name |
| `namnare.jsonl` | 21 | each county's own count of inspections and enforcement decisions, quoted from its answer |
| `beslut.jsonl` | 7 | the appealable decisions: reference, service, provisions quoted, appeal route and case number |
| `avgiftsskrivelser.jsonl` | 21 | the fee question per county: how many written exchanges it took and how it ended |
| `utlamningsgrad.jsonl` | 42 | the ceiling, the denominator and the file count per county and class |
| `dubbelforekomst.jsonl` | 18 | cases appearing both as a report in class A and as an annex in class B |
| `bristandel.jsonl` | 305 | the share of inspections finding a deficiency, from the Board of Agriculture's register |
| `foranmalda.jsonl` | 336 | announced against unannounced inspections per county and year |
| `oanmald_hypotes.jsonl` | 259 | the pre-registered hypothesis on unannounced inspections, with its outcome |
| `atagande.jsonl` | 16 | every open commitment the project made to itself, with the date it closed |
| `villkor.jsonl` | 2 359 | one row per permit condition, verbatim, under the heading the decision itself wrote |
| `villkor_baseline.jsonl` | 2 359 | the same conditions as hashes, for the test of whether permit conditions are standard text |
| `villkor_facit.jsonl` | 120 | a hand-read sample of condition types, answered blind to the heading |
| `tillstand_manifest.jsonl` | 236 | the permit decisions harvested, with sha256 per file |
| `tillstand_typ.jsonl` | 236 | the type of each permit decision, taken from the publisher's own link text |
| `tillstand_ocr_index.jsonl` | 72 | OCR confidence per scanned permit decision |

## Provenance and method

Every figure is produced by a numbered pipeline step in the [Antumbra]
repository, and every step is open source and deterministic. The protocol, the
exact wording of the requests and every application note are in
`docs/BEGARANMALL.md`; what was measured, how and against which pre-registered
condition is in `docs/VERIFIERAT.md`; the decisions that shaped the instruments
are the numbered records in `docs/adr/`.

**The received documents are never redistributed.** They contain private
individuals' names, and what the dataset publishes is the manifest with sha256
per file so that anyone holding the same documents can verify they are the same
ones. Officials' names are not reproduced anywhere: where a decision names the
signer, the role is written instead.

**Clock times are read from the system in the same action that writes them**,
never from memory, and the log is append-only: a correction is a new row.

## Limitations

- **Two measures were pre-registered and could not be computed**, and they are
  published as gaps with the reason rather than estimated: the share of annexes
  withheld, because the material cannot tell a withheld annex from one that
  never existed, and the release rate, because the ceiling counts inspections
  while the delivery arrives as files.
- **Two counties' denominators do not exist.** Skåne does not register animal
  welfare inspections by species, and Norrbotten declined on the service
  obligation in the Administrative Procedure Act. Both answers are quoted in
  `namnare.jsonl` and neither is estimated.
- **The conditions layer reaches 180 of 236 permit decisions.** The rest carry
  no conditions section that can be located, and most of them are amendment
  decisions that change named conditions in an earlier permit.
- **47 of the 2 359 conditions sit outside the register's own back-reading
  check**, because the two decisions they come from have only one readable text
  layer between them. Both are named in `docs/VERIFIERAT.md`.
- **Three counties declined copies** once a fee remained after the protocol's
  narrowing. They carry a response time and a fee figure but no documents in the
  redaction measure, and the loss is never counted as a release or a refusal.
- **The collection is closed.** It covers what the authorities delivered up to
  day 40, 28 September 2026, and later deliveries are logged but do not reopen
  the response-time measure.

## License and attribution

The aggregates are published under CC BY 4.0. The pipeline that produces them is
AGPL-3.0. The received authority documents are not part of the dataset and are
not redistributed at all.

## Citation

See `CITATION.cff` in the Antumbra repository.

[Antumbra]: https://github.com/MartinBlomqvistDev/antumbra
