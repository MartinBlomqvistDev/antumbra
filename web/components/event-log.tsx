"use client";

import { useState } from "react";
import type { Copy } from "@/content/types";
import type { LogRow } from "@/lib/log";

/**
 * The protocol log as a filterable table. It carries no minimum width: the
 * note column is prose, and a floor of 56rem inside a 56rem column with its
 * own gutters put a horizontal scrollbar under the table and clipped the
 * notes on an ordinary laptop. The short columns hold their line; the note
 * wraps.
 *
 * The full table is what the
 * server renders, so without JavaScript every row is simply visible and
 * only the filter control is inert.
 */
export function EventLog({
  rows,
  labels,
}: {
  rows: LogRow[];
  labels: Copy["metod"]["log"];
}) {
  const [authority, setAuthority] = useState("");
  const authorities = [...new Set(rows.map((row) => row.myndighet))].sort();
  const shown = authority
    ? rows.filter((row) => row.myndighet === authority)
    : rows;
  return (
    <div className="space-y-3">
      <label className="flex items-baseline gap-2 text-sm">
        <span className="text-ink-secondary">{labels.filterLabel}</span>
        <select
          value={authority}
          onChange={(event) => setAuthority(event.target.value)}
          className="-md border border-border-soft bg-surface px-2 py-1 text-sm"
        >
          <option value="">{labels.all}</option>
          {authorities.map((name) => (
            <option key={name} value={name}>
              {name}
            </option>
          ))}
        </select>
      </label>
      <div className="overflow-x-auto">
        <table className="w-full border-collapse text-sm">
          <thead>
            <tr className="border-b-2 border-ink text-left tablehead">
              <th scope="col" className="py-2 pr-3">
                {labels.headers.date}
              </th>
              <th scope="col" className="py-2 pr-3">
                {labels.headers.time}
              </th>
              <th scope="col" className="py-2 pr-3">
                {labels.headers.channel}
              </th>
              <th scope="col" className="py-2 pr-3">
                {labels.headers.authority}
              </th>
              <th scope="col" className="py-2 pr-3">
                {labels.headers.request}
              </th>
              <th scope="col" className="py-2 pr-3">
                {labels.headers.event}
              </th>
              <th scope="col" className="py-2">
                {labels.headers.note}
              </th>
            </tr>
          </thead>
          <tbody>
            {shown.map((row, index) => (
              <tr
                key={index}
                className="border-b border-border-soft align-top"
              >
                <td className="py-2 pr-3 whitespace-nowrap tabular-nums">
                  {row.datum}
                </td>
                <td className="py-2 pr-3 whitespace-nowrap tabular-nums">
                  {row.klockslag}
                </td>
                <td className="py-2 pr-3">{row.kanal}</td>
                <td className="py-2 pr-3">{row.myndighet}</td>
                <td className="py-2 pr-3">{row.begaran}</td>
                <td className="py-2 pr-3">{row.handelse}</td>
                <td className="py-2 text-ink-secondary">{row.notering}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
