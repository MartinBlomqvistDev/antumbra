-- A citation must point at a paragraph of its own report. Paragraph numbers
-- repeat across the corpus, so a join that lost the report would silently
-- attach one audit's finding to another's recommendation and every downstream
-- count would still look plausible. This test returns the rows that broke it.

select
    c.recommendation_key,
    c.paragraph_key,
    c.audit_key as citation_audit,
    p.audit_key as paragraph_audit
from {{ ref('stg_citations') }} as c
inner join {{ source('raw', 'dim_paragraph') }} as p
    on c.paragraph_key = p.paragraph_key
where c.audit_key != p.audit_key
