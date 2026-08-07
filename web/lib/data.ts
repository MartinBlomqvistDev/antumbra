import { readFileSync } from "node:fs";
import { join } from "node:path";

/** Corpus-wide totals written by pipeline/15_export_web_data.py. */
export type Headline = {
  audits: number;
  countries: number;
  paragraphs: number;
  years: { min: number; max: number };
  recommendations: number;
  chain_closes: number;
  citations: number;
  citations_resolved: number;
  share_citations_resolved: number;
  commitments: number;
};

/** Read the exported headline numbers at build time. */
export function readHeadline(): Headline {
  const path = join(process.cwd(), "public", "data", "headline.json");
  return JSON.parse(readFileSync(path, "utf-8")) as Headline;
}

/** One baked example from pipeline/16_bake_examples.py. */
export type Example = {
  question: string;
  answers: {
    text: string;
    ref: string;
    country: string;
    number: number;
    score: number;
  }[];
};

/** Read the baked example answers at build time. */
export function readExamples(): Example[] {
  const path = join(process.cwd(), "public", "data", "exempel.json");
  return JSON.parse(readFileSync(path, "utf-8")) as Example[];
}
