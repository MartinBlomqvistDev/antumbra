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
};

export type Sweden = {
  byggd: string;
  p12: {
    avsant: string;
    svar_senast: string;
    publicering_tidigast: string;
    myndigheter: number;
    svarat_substantiellt: number;
  };
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
