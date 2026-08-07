import { readDeliveryManifest, readLog } from "@/lib/log";

/**
 * The Swedish collection in numbers, derived mechanically from the event
 * log and the delivery manifest. Nothing here is typed in by hand: the
 * page shows what the record supports, and only that.
 */
export type SwedenStats = {
  sent: number;
  files: number;
  deliveringAuthorities: number;
  feeNotices: number;
  feeStopped: string[];
};

export function swedenStats(): SwedenStats {
  const log = readLog();
  const distinct = (rows: typeof log) =>
    new Set(rows.map((row) => row.myndighet)).size;
  return {
    sent: log.filter((row) => row.handelse === "avsändning").length,
    files: readDeliveryManifest().length,
    deliveringAuthorities: distinct(
      log.filter((row) => row.handelse === "leverans"),
    ),
    feeNotices: distinct(
      log.filter((row) => (row.handelse ?? "").includes("avgiftsbesked")),
    ),
    feeStopped: [
      ...new Set(
        log
          .filter((row) => (row.notering ?? "").includes("avgiftsstoppad"))
          .map((row) => `${row.myndighet} · ${row.begaran}`),
      ),
    ].sort(),
  };
}
