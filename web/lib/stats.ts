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
  feeStopped: { authority: string; request: string }[];
};

export function swedenStats(): SwedenStats {
  const log = readLog();
  // Rows the project wrote about the whole collection carry "samtliga" in the
  // authority field. Counted as an authority it put a twentieth deliverer on
  // the page and two rows reading "samtliga · A+B" under the fee stops.
  const authorities = log.filter((row) => row.myndighet !== "samtliga");
  const distinct = (rows: typeof log) =>
    new Set(rows.map((row) => row.myndighet)).size;
  return {
    // The 43 requests, and only those. Two later requests for court rulings
    // are logged as dispatches as well, under "samtliga" and both classes at
    // once; counting them made the page say 45 requests were sent.
    sent: log.filter(
      (row) =>
        row.handelse === "avsändning" && ["A", "B", "C"].includes(row.begaran),
    ).length,
    files: readDeliveryManifest().length,
    deliveringAuthorities: distinct(
      authorities.filter((row) => row.handelse === "leverans"),
    ),
    feeNotices: distinct(
      authorities.filter((row) => (row.handelse ?? "").includes("avgiftsbesked")),
    ),
    feeStopped: [
      ...new Set(
        authorities
          .filter((row) => (row.notering ?? "").includes("avgiftsstoppad"))
          .map((row) => `${row.myndighet}|${row.begaran}`),
      ),
    ]
      .sort()
      .map((entry) => {
        const [authority, request] = entry.split("|");
        return { authority, request };
      }),
  };
}
