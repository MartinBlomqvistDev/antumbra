import { readFileSync } from "node:fs";
import { join } from "node:path";

/**
 * The Swedish openness layer, exported by pipeline/41_export_sweden_web_data.py
 * out of the same functions that wrote the P12 packets. The site renders these
 * figures and computes none of its own, so a number on a page is the number the
 * authority was sent.
 */
export type ClassFigures = {
  dokument: number;
  maskade: number;
  andel: number;
  andel_text: string;
  yta: number;
  yta_text: string;
  intervall: [number, number];
  intervall_text: string;
};

export type RankingRow = {
  plats: number;
  slug: string;
  namn: string;
  dokument: number;
  maskade: number;
  andel: number;
  andel_text: string;
  intervall: [number, number];
  intervall_text: string;
};

export type Reply = {
  myndighet: string;
  datum: string;
  klockslag: string;
  typ: "autosvar" | "besked" | "substantiellt";
  meddelande: string;
  avsandare: string;
  roll: string | null;
  amnesrad: string;
  text: string;
  bilagor: string | null;
  utelamnat: string | null;
  kalla: string;
};

/**
 * One of my own letters, from the outgoing register. The recipient is a kind
 * and never an address: writing to a named case officer does not make their
 * address mine to publish. My own signature stays, because the measurement
 * rests on who asked.
 */
export type Sent = {
  datum: string;
  klockslag: string;
  myndighet: string;
  begaran: string;
  mottagare: "funktionsbrevlåda" | "namngiven tjänsteman";
  handelse: string;
  amnesrad: string;
  /** Null on the two rows where no sent copy exists anywhere. */
  meddelande: string | null;
  text: string | null;
  utelamnat: string | null;
  storlek: number | null;
  /** A packet: its text stays in the repository, at this path. */
  kodarkiv?: string;
  /** Day figures are masked here and stand in the outgoing register. */
  dagtal_maskade?: boolean;
  kalla: string;
};

export type Letter = {
  datum: string;
  klockslag: string;
  myndighet: string;
  avsandare: string;
  roll: string | null;
  amnesrad: string;
  meddelande: string;
  text: string;
  bilagor: string | null;
  utelamnat: string | null;
  kalla: string;
  /** A standing autoreply is carried once, with its repeats listed here. */
  forekomster?: {
    datum: string;
    klockslag: string;
    meddelande: string;
    amnesrad: string;
    storlek: number;
  }[];
};

export type Authority = {
  myndighet: string;
  slug: string;
  namn: string;
  klasser: Partial<Record<"A" | "B", ClassFigures>>;
  plats: Partial<Record<"A" | "B", number>>;
  kontrast: {
    djurslag: string;
    begaran: string;
    dokument: number;
    maskade: number;
    andel_maskade: number;
    andel_yta: number;
  }[];
  paket: {
    slug: string;
    path: string;
    bytes: number;
    sha256: string;
    avsant: string;
  } | null;
  svar: Reply[];
  svar_saknas: boolean;
  /** Why the authority carries no redaction figures, or null when it does. */
  utan_matning: "avgiftsstoppad" | "statistik" | null;
  /** P0b: the authority handled both requests as one case. */
  sammanslagen: boolean;
  /** Everything the authority itself wrote in the cases, verbatim. */
  brev: Letter[];
  /** Everything I wrote to the authority in the same cases, verbatim. */
  utgaende: Sent[];
};

export type RegisterCell = {
  slug: string;
  namn: string;
  djurslag: string;
  ar: number;
  /** The announced split, over all control types. */
  aviserade: number | null;
  oaviserade: number | null;
  andel_oanmalda: number | null;
  /** The deficiency share, over routine controls and in keeper rows. */
  rutin_rader: number | null;
  rutin_brist: number | null;
  rutin_andel: number | null;
};

export type RegisterAssociation = {
  djurslag: string;
  ar: number;
  kategori: "rutin" | "alla";
  lan: number;
  rho: number;
  p: number;
};

/** One county and year from step 54: exploratory, cattle only. */
export type MixCounty = {
  slug: string;
  namn: string;
  ar: number;
  rader: number;
  rutin_rader: number;
  klagomal_rader: number;
  uppfoljning_rader: number;
  okategoriserad_rader: number;
  andel_rutin: number;
  aviserade: number;
  oaviserade: number;
  andel_oanmalda: number;
  rutinkontroller_skattade: number;
  oanmalda_bland_rutin_min: number;
  oanmalda_bland_rutin_max: number;
};

export type MixAssociation = {
  matt: string;
  ar: number;
  lan: number;
  rho: number;
  p: number;
};

export type Sweden = {
  byggd: string;
  /** The register extract behind request C, as the Board of Agriculture released it. */
  register: {
    rapporter: number;
    djurslag: string[];
    ar: number[];
    celler: RegisterCell[];
    samband: RegisterAssociation[];
    mix: {
      lan: MixCounty[];
      samband: MixAssociation[];
      par: { ar: number; skilda: number; par: number }[];
    };
  };
  p12: {
    avsant: string;
    svar_senast: string;
    publicering_tidigast: string;
    myndigheter: number;
    svarat_substantiellt: number;
  };
  /** The courts' own letters in the four appeals; they carry no figures. */
  domstolar: { myndighet: string; brev: Letter[] }[];
  klasser: Record<
    "A" | "B",
    {
      dokument: number;
      maskade: number;
      andel: number;
      andel_text: string;
      myndigheter: number;
    }
  >;
  kontrast: {
    lan: number;
    median_dokumentandel: number | null;
    median_yta: number | null;
    hogre_dokumentandel_i_b: string[];
    hogre_yta_i_b: string[];
  };
  bilagor: {
    mappar: number;
    bilagefiler: number;
    lan_med_bilagefil: number;
    hanvisar_till_innehall: number;
    endast_formell_hanvisning: number;
    slag: Record<string, number>;
    utan_lasbar_text: number;
  };
  par: {
    lan: {
      myndighet: string;
      namn: string;
      par: number;
      dokument_a: number;
      maskade_a: number;
      dokument_b: number;
      maskade_b: number;
    }[];
    lan_med_nummer_i_bada: number;
    utan_arendenummer: number;
    filer: number;
  };
  jamforelse: Record<
    "A" | "B",
    { rader: RankingRow[]; atskilda_par: number; par: number }
  >;
  myndigheter: Authority[];
};

/** The exported Swedish layer, read at build time. */
export function readSweden(): Sweden {
  const path = join(process.cwd(), "public", "data", "sverige.json");
  return JSON.parse(readFileSync(path, "utf-8")) as Sweden;
}

/** The Skåne sentence, with its four figures read from the data. */
export function mixSwing(template: string, sweden: Sweden, locale: string): string {
  const percent = new Intl.NumberFormat(locale, {
    style: "percent",
    maximumFractionDigits: 0,
  });
  const own = sweden.register.mix.lan.filter((row) => row.namn === "Skåne");
  const [first, second] = [...own].sort((a, b) => a.ar - b.ar);
  return template
    .replace("{routineFrom}", String(first.rutin_rader))
    .replace("{routineTo}", String(second.rutin_rader))
    .replace("{shareFrom}", percent.format(first.andel_oanmalda))
    .replace("{shareTo}", percent.format(second.andel_oanmalda));
}

/** The bounds paragraph, with how many county pairs the ranges part each year. */
export function mixBounds(template: string, sweden: Sweden): string {
  const pairs = sweden.register.mix.par;
  const parted = (year: number) =>
    String(pairs.find((row) => row.ar === year)?.skilda ?? 0);
  return template
    .replace("{parted2024}", parted(2024))
    .replace("{parted2025}", parted(2025))
    .replace("{pairs}", String(pairs[0]?.par ?? 0));
}
