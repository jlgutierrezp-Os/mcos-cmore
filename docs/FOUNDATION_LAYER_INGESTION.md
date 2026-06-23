# Foundation Layer Ingestion

## Foundation triad

```text
ZFC + Category Theory + HoTT
```

## Purpose

The Foundation Layer gives MCOS/C-MORE a minimal non-empty mathematical starting position.

It prevents absolute zero initialization while avoiding premature commitment to one final foundation.

## Roles

- ZFC: classical set-theoretic reference foundation.
- Category Theory: structural and relational foundation.
- HoTT: type, path, identity and equivalence foundation.

## Status

```json
{
  "activation_state": "local_seed_only",
  "proof_assistants_active": false,
  "external_apis_active": false,
  "paid_apis_active": false,
  "human_review_required": true
}
```

## Ingest command

```bash
python -m mcos.cli ingest examples/foundation_layer_seed.json --dry-run
```

## Policy

The foundation seed is synthetic and public. Private foundation models must pass through zero-distillation and human review before any publication decision.
