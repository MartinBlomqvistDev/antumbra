-- The closed chain is the project's headline claim, so it may not be claimed
-- without its parts. A row where chain_closes is true but nothing resolved, or
-- nothing was committed, would overstate exactly the thing the layer exists to
-- measure.

select
    recommendation_key,
    states_its_basis,
    citations_resolved,
    commitments
from {{ ref('mart_chain') }}
where chain_closes
  and (not states_its_basis or citations_resolved = 0 or commitments = 0)
