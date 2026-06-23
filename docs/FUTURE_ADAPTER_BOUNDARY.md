# Future Adapter Boundary

## Status

All adapters beyond local JSON/JSONL ingestion are future-not-active.

```json
{
  "lean_adapter": "future_not_active",
  "coq_adapter": "future_not_active",
  "rdf_adapter": "future_not_active",
  "neo4j_adapter": "future_not_active",
  "mcp_adapter": "future_not_active",
  "external_api_adapter": "future_not_active",
  "paid_api_adapter": "future_not_active"
}
```

## Required before activation

Before any future adapter can be activated, MCOS/C-MORE requires:

1. explicit human approval;
2. adapter contract;
3. validation tests;
4. local dry-run;
5. no committed credentials;
6. cost control if paid;
7. rollback plan;
8. review packet.

## Lean and Coq role

Lean and Coq are essential for future formal verification, but not required for the v0.1 bootstrap.

v0.1 validates structure.

Future proof assistant adapters may validate formal claims.
