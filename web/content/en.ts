import type { Copy } from "./types";

export const en: Copy = {
  locale: "en",
  site: {
    name: "Antumbra",
    tagline: "From figure to source in two clicks.",
    description:
      "Measuring how official controls are audited: the EU's audits of " +
      "member state control systems, with every figure clickable down to " +
      "the exact sentence in the source document.",
    navLabel: "Main navigation",
  },
  nav: [
    { href: "/en/", label: "Home" },
    { href: "/en/jamforelse/", label: "Comparison" },
    { href: "/en/uppslag/", label: "Look up" },
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
  },
  uppslag: {
    title: "Look up",
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
