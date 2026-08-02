-- One row per audit, with its country resolved and the EU-27 flag carried
-- through. Nothing is filtered here: the marts decide what is in scope, so a
-- reader can always see the whole corpus from staging.

select
    a.audit_key,
    a.ref,
    a.year as audit_year,
    a.reference_format,
    a.audit_period,
    a.published_date,
    a.title,
    c.country_key,
    c.country,
    c.in_eu27
from {{ source('raw', 'dim_audit') }} as a
left join {{ source('raw', 'dim_country') }} as c
    on a.country_key = c.country_key
