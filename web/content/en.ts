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
      "The collection is ongoing. What is shown here is the process in " +
      "real time, drawn from the event log; the results and the " +
      "county-by-county comparison are published once the collection " +
      "has closed.",
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
