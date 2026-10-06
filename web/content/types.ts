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
    swedenHeading?: string;
    euHeading?: string;
    swedenLabels?: {
      sent: string;
      files: string;
      paid: string;
      paidValue: string;
    };
    numberLabels: {
      audits: string;
      recommendations: string;
      citationsResolved: string;
    };
    chain: {
      heading: string;
      intro: string;
      steps: {
        figure: string;
        rows: string;
        paragraph: string;
        document: string;
      };
      figureLead: string;
      toCountry: string;
    };
  };
  sverige?: PageCopy & {
    design: { heading: string; body: string };
    processNote: string;
    resultat: {
      heading: string;
      note: string;
      classLabel: string;
      documents: string;
      masked: string;
      authorities: string;
      classes: { A: string; B: string };
      contrast: string;
      contrastException: string;
      contrastNoException: string;
    };
    lanJamforelse: {
      heading: string;
      note: string;
      classHeading: { A: string; B: string };
      caption: string;
      intervalNote: string;
      separated: string;
      headers: {
        place: string;
        authority: string;
        documents: string;
        share: string;
        interval: string;
      };
    };
    notShown: { heading: string; items: string[] };
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
    toHandlingar: string;
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
    avvikelser: {
      heading: string;
      note: string;
      items: { title: string; body: string }[];
    };
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
    tavla: {
      heading: string;
      note: string;
      classWord: string;
      documents: string;
      masked: string;
      area: string;
      interval: string;
      place: string;
      placeOf: string;
      noFigures: string;
      reply: {
        heading: string;
        none: string;
        kinds: { autosvar: string; besked: string; substantiellt: string };
        from: string;
        subject: string;
        attachments: string;
        omitted: string;
        message: string;
      };
      packet: { heading: string; note: string; sent: string };
    };
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
