import { readFileSync, readdirSync } from "node:fs";
import { join } from "node:path";

/**
 * The published record: the protocol event log and the delivery manifest,
 * read at build time from the repository's data directory. The site adds
 * rendering, never interpretation; the rows appear as they were logged.
 */
export type LogRow = {
  datum: string;
  klockslag: string;
  kanal: string;
  myndighet: string;
  begaran: string;
  handelse: string;
  notering: string;
};

export type ManifestRow = {
  path: string;
  bytes: number;
  sha256: string;
  recorded: string;
};

const dataDir = join(process.cwd(), "..", "data");

/** Every event in the protocol log, in logged order. */
export function readLog(): LogRow[] {
  return readFileSync(join(dataDir, "protokoll_logg.jsonl"), "utf-8")
    .split("\n")
    .filter(Boolean)
    .map((line) => JSON.parse(line) as LogRow);
}

/** Every delivered file with its checksum. */
export function readDeliveryManifest(): ManifestRow[] {
  return readFileSync(join(dataDir, "leveranser_manifest.jsonl"), "utf-8")
    .split("\n")
    .filter(Boolean)
    .map((line) => JSON.parse(line) as ManifestRow);
}

/** The decision records under docs/adr, id and title from the heading. */
export function readAdrIndex(): { id: string; title: string }[] {
  const adrDir = join(process.cwd(), "..", "docs", "adr");
  // Only the numbered records; the directory also holds its own README.
  return readdirSync(adrDir)
    .filter((name) => /^\d{4}-.*\.md$/.test(name))
    .sort()
    .map((name) => {
      const firstLine = readFileSync(join(adrDir, name), "utf-8")
        .split("\n", 1)[0]
        .replace(/^#\s*/, "");
      return { id: name.replace(/\.md$/, ""), title: firstLine };
    });
}
