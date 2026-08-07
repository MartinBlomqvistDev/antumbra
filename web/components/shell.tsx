import Link from "next/link";
import type { ReactNode } from "react";
import { ThemeToggle } from "@/components/theme-toggle";
import type { Copy } from "@/content/types";

/**
 * Header, main column and footer shared by every page. All text comes from
 * the Copy object; the component holds none of its own.
 */
export function Shell({ copy, children }: { copy: Copy; children: ReactNode }) {
  return (
    <>
      <div aria-hidden className="h-1 bg-accent" />
      <header className="border-b border-border-soft">
        <div className="mx-auto flex max-w-5xl flex-wrap items-baseline gap-x-6 gap-y-2 px-4 py-4">
          <Link
            href={copy.nav[0].href}
            className="font-display text-lg font-semibold tracking-tight"
          >
            {copy.site.name}
          </Link>
          <nav
            aria-label={copy.site.navLabel}
            className="flex flex-wrap gap-x-4 text-sm"
          >
            {copy.nav.slice(1).map((item) => (
              <Link
                key={item.href}
                href={item.href}
                className="text-ink-secondary hover:text-ink"
              >
                {item.label}
              </Link>
            ))}
          </nav>
          <span className="ml-auto flex items-baseline gap-4">
            <ThemeToggle label={copy.themeToggle} />
            <a
              href={copy.languageSwitch.href}
              className="text-sm text-ink-secondary hover:text-ink"
            >
              {copy.languageSwitch.label}
            </a>
          </span>
        </div>
      </header>
      <main className="mx-auto w-full max-w-5xl flex-1 px-4 py-10">
        {children}
      </main>
      <footer className="border-t border-border-soft">
        <div className="mx-auto max-w-5xl space-y-2 px-4 py-8 text-sm text-ink-secondary">
          <p className="font-display text-base font-semibold text-ink">
            {copy.site.name}
            <span className="ml-3 font-sans text-sm font-normal text-ink-secondary">
              {copy.site.tagline}
            </span>
          </p>
          <p>{copy.footer.privacy}</p>
          <p>{copy.footer.source}</p>
        </div>
      </footer>
    </>
  );
}

/** Title and lead for a page that is routed but not yet built out. */
export function PageIntro({
  title,
  lead,
  building,
}: {
  title: string;
  lead: string;
  building?: string;
}) {
  return (
    <div className="max-w-2xl space-y-4">
      <h1 className="font-display text-4xl font-semibold tracking-tight">
        {title}
      </h1>
      <p className="text-lg text-ink-secondary">{lead}</p>
      {building ? <p className="text-sm text-ink-secondary">{building}</p> : null}
    </div>
  );
}
