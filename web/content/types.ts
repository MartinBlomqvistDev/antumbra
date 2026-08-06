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
  footer: { privacy: string; source: string };
  home: {
    title: string;
    lead: string;
    numberLabels: {
      audits: string;
      recommendations: string;
      citationsResolved: string;
    };
  };
  jamforelse: PageCopy;
  uppslag: PageCopy & { banner: string };
  metod: PageCopy;
  handlingar?: PageCopy;
  data?: PageCopy;
  building: string;
};
