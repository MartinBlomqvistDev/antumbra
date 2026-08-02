-- One row per recommendation. The flags the pipeline derived are kept as they
-- are; this layer renames and types, it does not reinterpret.

select
    r.recommendation_key,
    r.audit_key,
    r.report_path,
    r.number as recommendation_number,
    r.text as recommendation_text,
    r.legal_basis,
    r.parse_method,
    r.conclusions_cited,
    r.findings_cited,
    r.states_its_basis,
    r.is_answered,
    r.answer_confirmed_by_text
from {{ source('raw', 'fact_recommendation') }} as r
