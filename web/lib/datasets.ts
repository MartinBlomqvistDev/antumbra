import { readFileSync, statSync } from "node:fs";
import { join } from "node:path";

/**
 * The published files, measured at build time. The page states what the
 * repository actually carries, so a row count on the page cannot drift from
 * the file it describes.
 */
export type DatasetFile = {
  path: string;
  rows: number;
  bytes: number;
};

const repoRoot = join(process.cwd(), "..");

/** One file's size and row count, or null when it is not in this checkout. */
export function readDataset(path: string): DatasetFile | null {
  try {
    const full = join(repoRoot, path);
    const text = readFileSync(full, "utf-8");
    const rows = path.endsWith(".jsonl")
      ? text.split("\n").filter(Boolean).length
      : 1;
    return { path, rows, bytes: statSync(full).size };
  } catch {
    return null;
  }
}
