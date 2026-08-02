-- One row per citation edge. An edge that did not resolve keeps its row and a
-- null paragraph key: the count of what could not be joined is part of the
-- result, and dropping it here would flatter every mart downstream.

select
    c.recommendation_key,
    c.paragraph_key,
    c.audit_key,
    c.cites as cited_as,
    c.paragraph_number,
    c.resolved,
    c.heading_agrees
from {{ source('raw', 'fact_citation') }} as c
