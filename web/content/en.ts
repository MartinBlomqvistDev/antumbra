import type { Copy } from "./types";
import { wordingItems } from "./sv";

export const en: Copy = {
  locale: "en",
  site: {
    name: "Antumbra",
    tagline: "From figure to source in two clicks.",
    description:
      "A measurement of Swedish animal welfare supervision, with the " +
      "EU's audits of member state control systems as its baseline. " +
      "Every figure can be clicked down to the exact sentence in the " +
      "source document.",
    navLabel: "Main navigation",
  },
  nav: [
    { href: "/en/", label: "Home" },
    { href: "/en/sverige/", label: "Sweden" },
    { href: "/en/jamforelse/", label: "EU comparison" },
    { href: "/en/uppslag/", label: "Reference" },
    { href: "/en/metod/", label: "Method" },
  ],
  languageSwitch: { href: "/", label: "Svenska" },
  themeToggle: "Switch colour scheme",
  footer: {
    privacy: "No cookies, no tracking. Search queries are not logged.",
    source: "Source data: DG SANTE's published audit reports.",
  },
  home: {
    title: "Antumbra",
    kicker: "A measurement of Swedish animal welfare supervision",
    lead:
      "Three identically worded freedom-of-information requests to all " +
      "21 county administrative boards, handled under a pre-written " +
      "protocol: the differences in the answers are the measurement. " +
      "The baseline is the EU's audits of member state controls, where " +
      "every figure can be clicked down to the exact sentence in the " +
      "source document.",
    swedenHeading: "Sweden, collection in progress",
    euHeading: "The EU comparison, 1998–2026",
    swedenLabels: {
      sent: "requests sent on 3 August 2026",
      files: "files received, verified with sha256",
      paid: "fees paid",
      paidValue: "0 kr",
    },
    numberLabels: {
      audits: "audits",
      recommendations: "recommendations",
      citationsResolved: "of citations resolved to their paragraph",
    },
    chain: {
      heading: "The chain, in one example",
      intro:
        "The same path sits behind every figure on this site: from the " +
        "aggregate, through the rows, to the verbatim paragraph and the " +
        "document's checksum.",
      steps: {
        figure: "The figure",
        rows: "The rows behind it",
        paragraph: "The paragraph, verbatim",
        document: "The source document",
      },
      figureLead: "recommendations to Sweden in the EU's audits",
      toCountry: "The full underlying record for Sweden",
    },
  },
  sverige: {
    title: "Sweden",
    lead:
      "Is animal welfare supervised equivalently across the country, " +
      "and can the supervision be examined from outside? The " +
      "investigation measures this with the county administrative " +
      "boards' own answers.",
    design: {
      heading: "How the measurement is built",
      body:
        "Two requests went to all 21 county administrative boards with " +
        "identical wording: A concerns the most recent inspection " +
        "reports, B the most recent injunction decisions. A third " +
        "request, C, concerns statistics from the Swedish Board of " +
        "Agriculture's animal welfare inspection register. Every answer " +
        "is handled under a protocol written in advance: the same " +
        "narrowing when a fee is raised, the same request for a formal " +
        "decision, the same deadlines. When the questions are identical " +
        "and the handling predetermined, differences in outcome reflect " +
        "the authorities, not the questions.",
    },
    processNote:
      "The collection is closed. All 43 requests reached a final status, " +
      "and every authority concerned received its own figures on 2 October " +
      "2026 with three weeks to reply. The authorities' replies stand " +
      "verbatim beside the figures on the Swedish page Handlingar, and a " +
      "missing reply is written out as a missing reply.",
    resultat: {
      heading: "Redaction in the two document classes",
      note:
        "A document counts as redacted when a filled rectangle covers text " +
        "or when text is missing under the rectangle. The measure is " +
        "machine-made and described in full in the method. It measures " +
        "whether the authority released the information, never what the " +
        "information is.",
      classLabel: "Class",
      documents: "Documents",
      masked: "With at least one redaction",
      authorities: "Authorities",
      classes: {
        A: "A, inspection reports with annexes",
        B: "B, injunction decisions with annexes",
      },
      contrast:
        "The contrast measure under point P1 of the protocol is the " +
        "difference inside the same authority. Across the {counties} " +
        "counties that delivered in both classes the median difference is " +
        "{share} percentage points in the share of redacted documents and " +
        "{area} percentage points in redacted area.",
      contrastException:
        "The two measures pull apart, and that is reported rather than " +
        "evened out by the median: {names} redact a larger share of their " +
        "class B documents than of their class A documents. No county " +
        "redacts a larger area in class B.",
      contrastNoException:
        "No county redacts more in class B than in class A, on either " +
        "measure.",
    },
    lanJamforelse: {
      heading: "The counties in the order the measure gives",
      note:
        "The order is the one every authority received in its own material " +
        "before publication. Authorities with the same share share a place, " +
        "because the measure does not separate them, and the order implies " +
        "no judgement of their handling.",
      classHeading: {
        A: "Class A, inspection reports",
        B: "Class B, injunction decisions",
      },
      caption:
        "The share of documents with at least one redaction, per authority. " +
        "The number of documents differs between authorities, because the " +
        "request had a cap and some authorities raised a fee that led to a " +
        "narrowing.",
      intervalNote:
        "The interval is a 95 per cent Wilson interval. It treats one " +
        "authority's documents as independent draws, which they are not, so " +
        "it is a floor on the uncertainty and no statement about the " +
        "authority's practice.",
      separated:
        "The measure separates {separated} of {pairs} pairs of counties; the " +
        "remaining pairs have overlapping intervals and are held apart by " +
        "nothing.",
      headers: {
        place: "Place",
        authority: "Authority",
        documents: "Documents",
        share: "With at least one redaction",
        interval: "Interval",
      },
    },
    notShown: {
      heading: "What this page does not show",
      items: [
        "The documents themselves. They contain personal data and are never published; the listing with a checksum per file is on the Swedish page Handlingar.",
        "Any claim that an authority has broken the law. The law is unsettled, the Supreme Administrative Court has not decided the question, and four cases are before the administrative courts of appeal.",
        "Three counties that declined the copies once a fee remained after the narrowing. They carry a response time and a fee figure but no documents in the redaction measure, and the loss is never counted as a release or as a refusal.",
        "Pigs as a comparison. Sixteen documents have pigs as their dominant animal, spread across ten counties, so no county has material on both sides.",
        "The limits of the measure. They are in the method, together with the deviations from the pre-registration and the errors corrected during the work.",
      ],
    },
    overview: {
      heading: "The state of play in numbers",
      sent: "requests sent",
      files: "files received, verified with sha256",
      deliveringAuthorities: "authorities have delivered documents",
      feeNotices: "authorities raised a fee",
      feeStopped: "requests fee-stopped",
      paid: "fees paid",
      paidValue: "0 kr",
    },
    wordings: {
      heading: "The exact wording of the requests",
      note:
        "The requests were made in Swedish and are reproduced verbatim " +
        "below. The same text went to all 21 county administrative " +
        "boards on 3 August 2026, one request per e-mail; request C " +
        "went to the Swedish Board of Agriculture the same day.",
      items: wordingItems,
    },
    feeStopped: {
      heading: "Fee-stopped requests",
      note:
        "Requests where a fee remained after the protocol's narrowing. " +
        "Copies are then declined, a written decision on the fee is " +
        "requested, and the outcome is documented. No fee has been " +
        "paid.",
    },
    toHandlingar:
      "Every received file is listed with its checksum on the Swedish " +
      "page Handlingar.",
  },
  jamforelse: {
    title: "The EU comparison",
    lead:
      "The EU's audits of member state control systems, country by " +
      "country and year by year. Every chart has a table view and " +
      "supporting rows down to the paragraph.",
    table: {
      caption:
        "Recommendations in DG SANTE audits per country, full period. " +
        "Click a country for the underlying rows down to the paragraph.",
      country: "Country",
      audits: "Audits",
      recommendations: "Recommendations",
      shareBasis: "State their basis",
      shareAnswered: "Answered",
    },
    notShown: {
      title: "What this page does not show",
      body:
        "The page covers the EU countries, whose reports are fetched in " +
        "full text; other countries' audits exist in the register but " +
        "are not paragraph-indexed here. Shares are always shown next to " +
        "their counts: a share over four recommendations is not the same " +
        "fact as a share over four hundred.",
    },
    charts: {
      tableView: "Table view",
      of: "of",
      byYear: {
        title: "Recommendations per year",
        note:
          "All recommendations in the EU countries' audit reports, by " +
          "audit year.",
      },
      basis: { title: "State their basis, per country" },
      answered: { title: "Answered by the member state, per country" },
      chain: {
        title: "The chain closes, per country",
        note:
          "The chain closes when the recommendation states its basis, " +
          "the basis resolves to a verbatim paragraph, and an action " +
          "plan answers it. Anything less counts as a partial chain, " +
          "never rounded up.",
      },
      yearHeader: "Year",
      shareHeader: "Share",
    },
  },
  chain: {
    sourceDocument: "Source document",
    checksum: "sha256",
    recommendationLabel: "Recommendation",
    recommendationsCount: "recommendations",
    legalBasis: "Legal basis",
    citesHeading: "The recommendation states as its basis",
    unresolved:
      "The citation could not be resolved to a numbered paragraph in " +
      "the report.",
    responseHeading: "Member state response",
    backToTable: "Back to the comparison",
  },
  uppslag: {
    title: "Reference",
    lead:
      "Search 81,292 paragraphs from DG SANTE's audit reports. Answers " +
      "are always verbatim quotations with country, reference and " +
      "paragraph number.",
    banner:
      "The search finds where a topic is discussed, never what was " +
      "concluded. Always read the quotation.",
    examplesHeading: "Example questions",
    similarity: "similarity",
    noAnswers:
      "No paragraph above the similarity threshold. An empty answer is " +
      "an empty answer, never a guess.",
    search: {
      label: "Search the corpus",
      button: "Search",
      searching: "Searching",
      error:
        "The search could not be reached. The example questions below " +
        "still work.",
      note:
        "Live search opens with the site. The example answers below are " +
        "precomputed by the same code the live search runs.",
    },
  },
  metod: {
    title: "Method",
    lead:
      "The protocol, the event log, the decisions and their reasons. " +
      "Everything needed to repeat the measurement.",
    ai: {
      heading: "AI assistance",
      body:
        "Collection, logging and analysis are AI-assisted. Every " +
        "letter, log row and published figure is reviewed by a person " +
        "before it is sent or committed, and the role is documented, " +
        "dated, in ADR-0014. No figure on this site has a language " +
        "model as its source; everything traces to a source document " +
        "with a checksum.",
    },
    avvikelser: {
      heading: "Deviations from the pre-registration",
      note:
        "The measures and the hypothesis were timestamped in the repository " +
        "before any request was sent. Three parts could not be carried out " +
        "as written. They stand here, on top, with what was done instead.",
      items: [
        {
          title: "The field measure could not be computed literally",
          body:
            "Redaction was pre-registered as masked area plus masked " +
            "fields. The documents are running prose and carry no field " +
            "structure, so the field half cannot be computed. It was " +
            "replaced on 17 August 2026 by a measure of covered content, " +
            "decided in ADR-0017, and the outcome was a null result: no " +
            "document hides body text under a light covering, and the 236 " +
            "covered characters are a page header under the authority's own " +
            "white box.",
        },
        {
          title: "The area measure points the wrong way for one technique",
          body:
            "Where the text under the blacking has been removed, the area " +
            "measures how the boxes were drawn and not how much is held " +
            "back. For that technique the character count is the better " +
            "measure. The limit belongs to the pre-registered area figure " +
            "and is to be read beside every area number.",
        },
        {
          title: "Half the unannounced hypothesis cannot be tested",
          body:
            "The pre-registration asks both for the correlation across " +
            "counties and for the difference in deficiency share between " +
            "unannounced and announced inspections within county, species " +
            "and inspection type. The second needs the notice field crossed " +
            "with the deficiency field, and that extract was not released. " +
            "The pre-written null-result text asserts the outcome of that " +
            "very test, so it is struck rather than reproduced. The half " +
            "that could be tested does not separate a weak positive " +
            "correlation from none.",
        },
      ],
    },
    adr: {
      heading: "Decision log (ADR)",
      note:
        "Every method and architecture decision is dated and documented " +
        "with its reasons and rejected alternatives.",
    },
    log: {
      heading: "Event log",
      note:
        "The log is kept as the collection runs. Each row is one event " +
        "with a verified timestamp; nothing is written after the fact. " +
        "Entries are in Swedish, the language of the record.",
      countLabel: "events up to and including",
      filterLabel: "Filter by authority",
      all: "All authorities",
      headers: {
        date: "Date",
        time: "Time",
        channel: "Channel",
        authority: "Authority",
        request: "Request",
        event: "Event",
        note: "Note",
      },
    },
  },
  building: "This page is under construction.",
};
