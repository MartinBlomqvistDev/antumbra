import type { Copy } from "./types";

export const sv: Copy = {
  locale: "sv",
  site: {
    name: "Antumbra",
    tagline: "Från siffra till källa på två klick.",
    description:
      "Att göra tillsynen mätbar: EU:s revisioner av medlemsstaternas " +
      "kontrollsystem, där varje tal kan klickas ned till den exakta " +
      "meningen i källdokumentet.",
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
    table: {
      caption:
        "Rekommendationer i DG SANTE:s revisioner per land, hela " +
        "perioden. Klicka på ett land för underlaget ned till stycket.",
      country: "Land",
      audits: "Revisioner",
      recommendations: "Rekommendationer",
      shareBasis: "Anger sin grund",
      shareAnswered: "Besvarade",
    },
    notShown: {
      title: "Vad sidan inte visar",
      body:
        "Sidan omfattar EU-länderna, vars rapporter är hämtade i " +
        "fulltext; övriga länders revisioner finns i registret men är " +
        "inte styckeindexerade här. Andelar visas alltid tillsammans med " +
        "sina antal: en andel över fyra rekommendationer är inte samma " +
        "sak som en andel över fyrahundra.",
    },
    charts: {
      tableView: "Tabellvy",
      of: "av",
      byYear: {
        title: "Rekommendationer per år",
        note:
          "Samtliga rekommendationer i EU-ländernas revisionsrapporter, " +
          "efter revisionens år.",
      },
      basis: { title: "Anger sin grund, per land" },
      answered: { title: "Besvarade av medlemsstaten, per land" },
      chain: {
        title: "Kedjan sluts, per land",
        note:
          "Kedjan sluts när rekommendationen anger sin grund, grunden " +
          "upplöses till ett ordagrant stycke och en åtgärdsplan besvarar " +
          "den. Allt annat räknas som en delvis kedja, aldrig uppåt.",
      },
      yearHeader: "År",
      shareHeader: "Andel",
    },
  },
  chain: {
    sourceDocument: "Källdokument",
    checksum: "sha256",
    recommendationLabel: "Rekommendation",
    recommendationsCount: "rekommendationer",
    legalBasis: "Rättslig grund",
    citesHeading: "Rekommendationen anger som grund",
    unresolved:
      "Citeringen kunde inte upplösas till ett numrerat stycke i " +
      "rapporten.",
    responseHeading: "Medlemsstatens svar",
    backToTable: "Till jämförelsen",
  },
  uppslag: {
    title: "Uppslag",
    lead:
      "Sök i 81 292 stycken ur DG SANTE:s revisionsrapporter. Svaren är " +
      "alltid ordagranna citat med land, referens och styckenummer.",
    banner:
      "Sökningen hittar var ett ämne behandlas, aldrig vad som " +
      "konstaterats. Läs alltid citatet.",
    examplesHeading: "Exempelfrågor",
    similarity: "likhet",
    noAnswers:
      "Inget stycke över likhetströskeln. Ett tomt svar är ett tomt " +
      "svar, aldrig en gissning.",
    search: {
      label: "Sök i korpusen",
      button: "Sök",
      searching: "Söker",
      error: "Söket kunde inte nås. Exempelfrågorna nedan fungerar ändå.",
      note:
        "Livesöket öppnar tillsammans med sajten. Exempelsvaren nedan är " +
        "förberäknade genom samma kod som livesöket kör.",
    },
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
