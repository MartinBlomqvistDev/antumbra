import type { Copy } from "./types";

export const en: Copy = {
  locale: "en",
  site: {
    name: "Antumbra",
    tagline: "From figure to source in two clicks.",
    description:
      "Making supervision measurable: the EU's audits of member state " +
      "control systems, where every figure can be clicked down to the " +
      "exact sentence in the source document.",
    navLabel: "Main navigation",
  },
  nav: [
    { href: "/en/", label: "Home" },
    { href: "/en/jamforelse/", label: "Comparison" },
    { href: "/en/uppslag/", label: "Reference" },
    { href: "/en/metod/", label: "Method" },
  ],
  languageSwitch: { href: "/", label: "Svenska" },
  footer: {
    privacy: "No cookies, no tracking. Search queries are not logged.",
    source: "Source data: DG SANTE's published audit reports.",
  },
  home: {
    title: "Antumbra",
    lead:
      "Every figure on this site can be clicked down to the exact " +
      "sentence in the source document: aggregates to rows, rows to " +
      "verbatim paragraphs, paragraphs to documents with checksums.",
    numberLabels: {
      audits: "audits 1998–2026",
      recommendations: "recommendations",
      citationsResolved: "of citations resolved to their paragraph",
    },
  },
  jamforelse: {
    title: "Comparison",
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
        "The table covers the EU countries, whose reports are fetched in " +
        "full text; other countries' audits exist in the register but " +
        "are not paragraph-indexed here. Shares are always shown next to " +
        "their counts: a share over four recommendations is not the same " +
        "fact as a share over four hundred.",
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
  },
  metod: {
    title: "Method",
    lead:
      "The protocol, the event log, the decisions and their reasons. " +
      "Everything needed to repeat the measurement.",
  },
  building: "This page is under construction.",
};
