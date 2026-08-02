-- The grain a dashboard filters on: country by year.
--
-- Shares are left as numerator and denominator beside the ratio, so a reader
-- can see how thin a percentage is before trusting it. A share over four
-- recommendations is not the same fact as a share over four hundred, and a
-- chart that shows only the ratio hides that.

with recommendations as (

    select * from {{ ref('stg_recommendations') }}

),

audits as (

    select * from {{ ref('stg_audits') }}

)

select
    a.country,
    a.in_eu27,
    a.audit_year,
    count(*) as recommendations,
    count(distinct a.audit_key) as audits,
    sum(case when r.states_its_basis then 1 else 0 end) as stating_their_basis,
    sum(case when r.is_answered then 1 else 0 end) as answered,
    sum(case when r.answer_confirmed_by_text then 1 else 0 end) as confirmed,
    safe_divide(
        sum(case when r.states_its_basis then 1 else 0 end), count(*)
    ) as share_stating_their_basis,
    safe_divide(
        sum(case when r.is_answered then 1 else 0 end), count(*)
    ) as share_answered
from recommendations as r
inner join audits as a
    on r.audit_key = a.audit_key
group by a.country, a.in_eu27, a.audit_year
