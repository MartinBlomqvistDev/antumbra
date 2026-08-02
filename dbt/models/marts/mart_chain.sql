-- The chain, one row per recommendation: what it rests on and whether the
-- member state answered it.
--
-- This is the model the project exists to make queryable. It is deliberately
-- built as a left join from the recommendation outwards, so a recommendation
-- that cites nothing and was never answered still appears, with zeros. An
-- inner join here would quietly restrict every downstream count to the part
-- of the corpus where the chain happens to close.

with recommendations as (

    select * from {{ ref('stg_recommendations') }}

),

audits as (

    select * from {{ ref('stg_audits') }}

),

citations as (

    select
        recommendation_key,
        count(*) as citations,
        sum(case when resolved then 1 else 0 end) as citations_resolved,
        sum(case when cited_as = 'conclusion' then 1 else 0 end) as cites_conclusions,
        sum(case when cited_as = 'finding' then 1 else 0 end) as cites_findings
    from {{ ref('stg_citations') }}
    group by recommendation_key

),

commitments as (

    select
        recommendation_key,
        count(*) as commitments,
        max(text_similarity) as best_text_similarity,
        max(case when confirmed_by_text then 1 else 0 end) = 1 as any_confirmed
    from {{ ref('stg_commitments') }}
    where recommendation_key is not null
    group by recommendation_key

)

select
    r.recommendation_key,
    a.country,
    a.in_eu27,
    a.audit_year,
    a.ref as audit_ref,
    r.recommendation_number,
    r.recommendation_text,
    r.legal_basis,
    r.parse_method,
    r.states_its_basis,
    coalesce(c.citations, 0) as citations,
    coalesce(c.citations_resolved, 0) as citations_resolved,
    coalesce(c.cites_conclusions, 0) as cites_conclusions,
    coalesce(c.cites_findings, 0) as cites_findings,
    coalesce(m.commitments, 0) as commitments,
    coalesce(m.any_confirmed, false) as commitment_confirmed_by_text,
    m.best_text_similarity,
    -- The chain closes when the recommendation names its basis, that basis
    -- resolves to a paragraph, and a plan answers it. Anything less is a
    -- partial chain and is counted as such rather than rounded up.
    (
        r.states_its_basis
        and coalesce(c.citations_resolved, 0) > 0
        and coalesce(m.commitments, 0) > 0
    ) as chain_closes
from recommendations as r
inner join audits as a
    on r.audit_key = a.audit_key
left join citations as c
    on r.recommendation_key = c.recommendation_key
left join commitments as m
    on r.recommendation_key = m.recommendation_key
