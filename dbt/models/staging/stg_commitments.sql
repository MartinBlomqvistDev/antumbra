-- One row per answer in a member state's action plan. Rows whose number has no
-- match in the parsed report keep a null recommendation key rather than being
-- dropped, for the same reason the unresolved citations are kept.

select
    m.recommendation_key,
    m.audit_key,
    m.plan_path,
    m.recommendation_number,
    m.response,
    m.text_similarity,
    m.confirmed_by_text
from {{ source('raw', 'fact_commitment') }} as m
