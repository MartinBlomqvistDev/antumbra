import type { Copy } from "./types";

export const sv: Copy = {
  locale: "sv",
  site: {
    name: "Antumbra",
    tagline: "Från siffra till källa på två klick.",
    description:
      "Mätning av hur offentlig kontroll granskas: EU:s revisioner av " +
      "medlemsstaternas kontrollsystem, med varje tal klickbart ned till " +
      "den exakta meningen i källdokumentet.",
    navLabel: "Huvudnavigering",
  },
  nav: [
    { href: "/", label: "Hem" },
    { href: "/jamforelse/", label: "Jämförelse" },
    { href: "/uppslag/", label: "Uppslag" },
    { href: "/metod/", label: "Metod" },
    { href: "/handlingar/", label: "Handlingar" },
    { href: "/data/", label: "Data" },
  ],
  languageSwitch: { href: "/en/", label: "English" },
  footer: {
    privacy: "Inga kakor, ingen spårning. Sökfrågor loggas inte.",
    source: "Källdata: DG SANTE:s publicerade revisionsrapporter.",
  },
  home: {
    title: "Antumbra",
    lead:
      "Varje tal på den här sidan kan klickas ned till den exakta meningen " +
      "i källdokumentet: aggregat till rader, rader till ordagranna " +
      "stycken, stycken till dokument med kontrollsumma.",
    numberLabels: {
      audits: "revisioner 1998–2026",
      recommendations: "rekommendationer",
      citationsResolved: "av citeringarna upplösta till sitt stycke",
    },
  },
  jamforelse: {
    title: "Jämförelse",
    lead:
      "EU:s revisioner av medlemsstaternas kontrollsystem, land för land " +
      "och år för år. Varje diagram har en tabellvy och ett underlag ned " +
      "till stycket.",
  },
  uppslag: {
    title: "Uppslag",
    lead:
      "Sök i 81 292 stycken ur DG SANTE:s revisionsrapporter. Svaren är " +
      "alltid ordagranna citat med land, referens och styckenummer.",
    banner:
      "Sökningen hittar var ett ämne behandlas, aldrig vad som " +
      "konstaterats. Läs alltid citatet.",
  },
  metod: {
    title: "Metod",
    lead:
      "Protokollet, händelseloggen, besluten och deras skäl. Allt som " +
      "krävs för att göra om mätningen.",
  },
  handlingar: {
    title: "Handlingar",
    lead:
      "Vad som begärts ut, vad som lämnats ut, vad som inte lämnats ut " +
      "och varför.",
  },
  data: {
    title: "Data",
    lead:
      "Nedladdningsbara aggregat och schemadokumentation. Granskningsbar " +
      "utifrån betyder att vem som helst kan räkna om.",
  },
  building: "Sidan är under uppbyggnad.",
};
