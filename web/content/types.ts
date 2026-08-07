/**
 * The shape both languages must fill. The rule of the house: never edit one
 * language without the other, and never put copy in components.
 */
export type PageCopy = {
  title: string;
  lead: string;
};

export type Copy = {
  locale: "sv" | "en";
  site: {
    name: string;
    tagline: string;
    description: string;
    navLabel: string;
  };
  nav: { href: string; label: string }[];
  languageSwitch: { href: string; label: string };
  themeToggle: string;
  footer: { privacy: string; source: string };
  home: {
    title: string;
    kicker: string;
    lead: string;
    numberLabels: {
      audits: string;
      recommendations: string;
      citationsResolved: string;
    };
  };
  jamforelse: PageCopy & {
    table: {
      caption: string;
      country: string;
      audits: string;
      recommendations: string;
      shareBasis: string;
      shareAnswered: string;
    };
    notShown: { title: string; body: string };
    charts: {
      tableView: string;
      of: string;
      byYear: { title: string; note: string };
      basis: { title: string };
      answered: { title: string };
      chain: { title: string; note: string };
      yearHeader: string;
      shareHeader: string;
    };
  };
  chain: {
    sourceDocument: string;
    checksum: string;
    recommendationLabel: string;
    recommendationsCount: string;
    legalBasis: string;
    citesHeading: string;
    unresolved: string;
    responseHeading: string;
    backToTable: string;
  };
  uppslag: PageCopy & {
    banner: string;
    examplesHeading: string;
    similarity: string;
    noAnswers: string;
    search: {
      label: string;
      button: string;
      searching: string;
      error: string;
      note: string;
    };
  };
  metod: PageCopy & {
    ai: { heading: string; body: string };
    adr: { heading: string; note: string };
    log: {
      heading: string;
      note: string;
      countLabel: string;
      filterLabel: string;
      all: string;
      headers: {
        date: string;
        time: string;
        channel: string;
        authority: string;
        request: string;
        event: string;
        note: string;
      };
    };
  };
  handlingar?: PageCopy & {
    overview: {
      heading: string;
      sent: string;
      files: string;
      deliveringAuthorities: string;
      feeNotices: string;
      feeStopped: string;
      paid: string;
      paidValue: string;
    };
    wordings: {
      heading: string;
      note: string;
      items: { label: string; text: string }[];
    };
    feeStopped: { heading: string; note: string };
    deliveries: {
      heading: string;
      note: string;
      filesWord: string;
      headers: { file: string; bytes: string; sha256: string };
    };
  };
  data?: PageCopy;
  building: string;
};
