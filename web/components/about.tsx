import Image from "next/image";
import { PageIntro } from "@/components/shell";
import type { Copy } from "@/content/types";

/**
 * Who made the measurement, in whichever language the page is served in.
 *
 * The site carried the figures, the protocol and the authorities' own words,
 * and said nothing about the person who sent the requests, which sits badly
 * with decision 3 in the project's own log: the requests were made under a
 * name on purpose, and all twenty-two authorities have had that name since the
 * third of August. The portrait is the same file the consultancy site serves,
 * for the same reason the name is here: a measurement of openness is read
 * differently when the reader can see who made it. The markup is shared
 * because the two language versions differ only in their words, and a second
 * copy of it would be a second place for the layout to drift.
 */
export function About({ copy }: { copy: NonNullable<Copy["om"]> }) {
  return (
    <div className="space-y-10">
      <PageIntro title={copy.title} lead={copy.lead} />
      <section className="max-w-2xl gap-6 sm:grid sm:grid-cols-[11rem_1fr]">
        <Image
          src="/martin-blomqvist.jpg"
          alt={copy.photoAlt}
          width={768}
          height={768}
          className="mb-6 w-40 border border-border-soft sm:mb-0 sm:w-full"
        />
        <div className="space-y-4">
          {copy.body.map((paragraph) => (
            <p key={paragraph.slice(0, 40)} className="text-ink-secondary">
              {paragraph}
            </p>
          ))}
        </div>
      </section>
      <section className="max-w-2xl space-y-3">
        <h2 className="text-2xl font-semibold tracking-tight">
          {copy.linksHeading}
        </h2>
        <dl className="divide-y divide-border-soft border-y border-border-soft">
          {copy.links.map((link) => (
            <div key={link.href} className="space-y-1 py-3">
              <dt>
                <a href={link.href} rel="me noopener" className="record">
                  {link.label}
                </a>
              </dt>
              <dd className="text-sm text-ink-secondary">{link.note}</dd>
            </div>
          ))}
        </dl>
      </section>
      <section className="max-w-2xl space-y-2">
        <h2 className="text-2xl font-semibold tracking-tight">
          {copy.contactHeading}
        </h2>
        <p>
          <a href={`mailto:${copy.contact}`} className="record">
            {copy.contact}
          </a>
        </p>
      </section>
    </div>
  );
}
