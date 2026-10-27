import Link from "next/link";
import type { ReactNode } from "react";
import { ThemeToggle } from "@/components/theme-toggle";
import type { Copy } from "@/content/types";

/**
 * Header, main column and footer shared by every page. All text comes from
 * the Copy object; the component holds none of its own.
 *
 * The header is a running head, the kind a report carries at the top of
 * every page: the title on the left, the sections beside it, a single
 * hairline underneath. No banner, no coloured bar, nothing that announces a
 * product.
 */
export function Shell({ copy, children }: { copy: Copy; children: ReactNode }) {
  return (
    <>
      <header className="border-b border-border-soft">
        <div className="mx-auto flex max-w-4xl flex-wrap items-baseline gap-x-6 gap-y-1 px-5 pb-3 pt-5">
          <Link
            href={copy.nav[0].href}
            className="flex items-baseline gap-2 text-lg font-semibold tracking-tight no-underline"
          >
            {/* The mark is the thing being measured: a redaction. It is the
                only ornament on the site, and it appears once. */}
            <span
              aria-hidden
              className="inline-block h-[0.6em] w-[1.5em] bg-redaction"
            />
            {copy.site.name}
          </Link>
          <nav
            aria-label={copy.site.navLabel}
            className="flex flex-wrap gap-x-4 text-[0.9375rem] text-ink-secondary"
          >
            {copy.nav.slice(1).map((item) => (
              <Link
                key={item.href}
                href={item.href}
                className="no-underline hover:text-ink"
              >
                {item.label}
              </Link>
            ))}
          </nav>
          <span className="ml-auto flex items-baseline gap-4 text-[0.9375rem] text-ink-secondary">
            <ThemeToggle label={copy.themeToggle} />
            <a href={copy.languageSwitch.href} className="hover:text-ink">
              {copy.languageSwitch.label}
            </a>
          </span>
        </div>
      </header>
      <main className="mx-auto w-full max-w-4xl flex-1 px-5 py-12">
        {children}
      </main>
      <footer className="mt-16 border-t border-border-soft">
        <div className="mx-auto max-w-4xl space-y-1 px-5 py-8 text-sm text-ink-secondary">
          <p className="text-base text-ink">
            {copy.site.name}{" "}
            <span className="text-sm text-ink-secondary">
              {copy.site.tagline}
            </span>
          </p>
          <p>{copy.footer.privacy}</p>
          <p>{copy.footer.source}</p>
          <p>
            {copy.footer.repo.label}:{" "}
            <a href={copy.site.repo} rel="noopener">
              {copy.footer.repo.text}
            </a>
            {" · "}
            {copy.footer.dataset.label}:{" "}
            <a href={copy.footer.dataset.href} rel="noopener">
              {copy.footer.dataset.text}
            </a>
          </p>
        </div>
      </footer>
    </>
  );
}

/** Title and lead for a page that is routed but not yet built out. */
export function PageIntro({ title, lead }: { title: string; lead: string }) {
  return (
    <div className="max-w-[34rem] space-y-4">
      <h1 className="text-4xl font-semibold tracking-tight">{title}</h1>
      <p className="text-lg text-ink-secondary">{lead}</p>
    </div>
  );
}

/**
 * A figure with its basis underneath, set as a row in a table rather than
 * as a card. Three of these read as a statistical appendix; three cards
 * read as a dashboard, and the material is not a dashboard.
 */
export function FigureTable({
  caption,
  rows,
  href,
}: {
  caption: string;
  rows: { value: string; label: string }[];
  href?: string;
}) {
  return (
    <section className="space-y-3">
      {/* An ordinary section head, the same size as every other one on the
          site. Set small and grey it was still the shape the whole redesign
          exists to remove: little muted type sitting above big type. */}
      <h2 className="text-2xl font-semibold tracking-tight">
        {href ? (
          <Link href={href} className="no-underline hover:text-ink">
            {caption}
          </Link>
        ) : (
          caption
        )}
      </h2>
      <dl className="divide-y divide-border-soft border-y border-border-soft">
        {rows.map((row) => (
          <div
            key={row.label}
            className="grid items-baseline gap-x-6 py-4 sm:grid-cols-[9rem_1fr]"
          >
            <dd className="text-3xl font-semibold tabular-nums tracking-tight sm:text-4xl">
              {row.value}
            </dd>
            <dt className="text-ink-secondary">{row.label}</dt>
          </div>
        ))}
      </dl>
    </section>
  );
}
