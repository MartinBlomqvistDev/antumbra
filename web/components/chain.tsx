import type { Copy } from "@/content/types";
import type { AuditReport, Recommendation } from "@/lib/underlag";

/**
 * The chain, rendered once and reused wherever a number needs its source:
 * recommendation, then the verbatim paragraphs it states as its basis,
 * then the member state's response, then the document and its checksum.
 * Built on native details/summary so the whole chain works without
 * JavaScript and prints as opened.
 */
export function ChainAudit({
  audit,
  labels,
}: {
  audit: AuditReport;
  labels: Copy["chain"];
}) {
  return (
    <section className="space-y-4">
      <div>
        <h2 className="font-display text-2xl font-semibold tracking-tight">
          {audit.ref}
          {audit.year !== null ? (
            <span className="ml-2 font-normal text-ink-secondary">
              {audit.year}
            </span>
          ) : null}
        </h2>
        {audit.title ? (
          <p className="mt-1 text-sm text-ink-secondary">{audit.title}</p>
        ) : null}
        <p className="mt-1 text-xs text-ink-secondary">
          {labels.sourceDocument}:{" "}
          <span className="break-all">{audit.report_path}</span>
          {audit.sha256 ? (
            <>
              {" · "}
              {labels.checksum}{" "}
              <code className="break-all">{audit.sha256}</code>
            </>
          ) : null}
        </p>
      </div>
      <ol className="space-y-3">
        {audit.recommendations.map((recommendation) => (
          <li key={`${audit.report_path}-${recommendation.number}`}>
            <ChainRecommendation
              recommendation={recommendation}
              labels={labels}
            />
          </li>
        ))}
      </ol>
    </section>
  );
}

function ChainRecommendation({
  recommendation,
  labels,
}: {
  recommendation: Recommendation;
  labels: Copy["chain"];
}) {
  const preview =
    recommendation.text.length > 160
      ? `${recommendation.text.slice(0, 160)}…`
      : recommendation.text;
  return (
    <details className="rounded-lg border border-border-soft bg-surface-raised">
      <summary className="cursor-pointer p-4 text-sm">
        <span className="font-semibold">
          {labels.recommendationLabel} {recommendation.number}.
        </span>{" "}
        {preview}
      </summary>
      <div className="space-y-4 border-t border-border-soft p-4 text-sm">
        <p>{recommendation.text}</p>
        {recommendation.legal_basis ? (
          <p className="text-ink-secondary">
            {labels.legalBasis}: {recommendation.legal_basis}
          </p>
        ) : null}
        {recommendation.citations.length > 0 ? (
          <div className="space-y-3">
            <h3 className="font-semibold">{labels.citesHeading}</h3>
            {recommendation.citations.map((citation, index) => (
              <blockquote
                key={index}
                className="border-l-2 border-accent pl-3"
              >
                {citation.text !== null ? (
                  <p>{citation.text}</p>
                ) : (
                  <p className="italic text-ink-secondary">
                    {labels.unresolved}
                  </p>
                )}
                <footer className="mt-1 text-xs text-ink-secondary">
                  {citation.cites}
                  {citation.number !== null ? ` §${citation.number}` : null}
                  {citation.section ? ` · ${citation.section}` : null}
                </footer>
              </blockquote>
            ))}
          </div>
        ) : null}
        {recommendation.responses.length > 0 ? (
          <div className="space-y-3">
            <h3 className="font-semibold">{labels.responseHeading}</h3>
            {recommendation.responses.map((response, index) => (
              <blockquote
                key={index}
                className="border-l-2 border-accent-warm pl-3"
              >
                <p>{response.response}</p>
              </blockquote>
            ))}
          </div>
        ) : null}
      </div>
    </details>
  );
}
