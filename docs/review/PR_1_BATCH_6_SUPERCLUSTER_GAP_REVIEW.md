# PR #1 Batch 6 Review — Supercluster Gap Review

## Scope

PR: `#1 Draft review: MCOS/C-MORE transfer integration v0.1-R`

Branch: `integration/mcos-transfer-v0-1-r`

Base: `main`

Purpose: review before marking ready.

## Review result

```json
{
  "decision": "keep_draft",
  "ready_for_review": false,
  "ready_to_merge": false,
  "human_review_required": true,
  "runtime_tests_executed_by_connector": false,
  "static_review_completed": true
}
```

## Evidence summary

The PR is draft, open, unmerged, and staged for documentary and technical review. The branch includes local-first kernel, ingestion, zero-distillation, Foundation Layer, governance, security and documentation.

## Supercluster gaps

### SC-P0-RUNTIME — Runtime proof missing

Status: open.

Risk: the connector reviewed files but did not execute the branch locally.

Required proof before ready:

```bash
python -m unittest discover -s tests
python -m mcos.cli selfdebug
bash scripts/run_all_checks.sh
```

Acceptance:

```json
{
  "unit_tests_passed": true,
  "selfdebug_passed": true,
  "run_all_checks_passed": true
}
```

### SC-P1-SCHEMA — AdapterResponse and equivalence report validation too shallow

Status: open.

Current kernel validates response envelope but does not deeply validate `equivalence_report` fields.

Recommendation:

- add explicit `validate_equivalence_report()`;
- require `checked`, `comparison_scope`, and `differences` when present;
- validate difference severity as warning/error/critical.

### SC-P1-PRIVACY — `.private.json` synthetic example is intentionally synthetic but risky as convention

Status: open.

The committed example is synthetic, but its suffix may normalize committing private-looking files.

Recommendation:

- either rename to `private_model_synthetic_input.example.json`;
- or keep it only with explicit synthetic marker and documentation;
- ensure `.private.json` remains ignored for real files.

### SC-P1-DISTILL — Zero-distillation needs adversarial hardening

Status: open.

`zero_distill_model()` reduces names and alpha values, but it should also reject or sanitize malformed alpha values, unexpected structure, and excessive metadata.

Recommendation:

- add adversarial tests for nonnumeric alpha;
- cap output size;
- add source hash without private content;
- emit review packet.

### SC-P2-GRAPH — JSONL store is sufficient for v0.1 but lacks indexes

Status: accepted as v0.1 limitation.

Recommendation for v0.2:

- `get_node(id)`;
- `get_node_by_name(name)`;
- `list_dependencies(id)`;
- `find_equivalent(id)`.

### SC-P2-FOUNDATION — Foundation Layer is adequate as seed, not complete ontology

Status: accepted as minimal.

Recommendation:

- keep as synthetic seed;
- do not claim proof assistant verification;
- expand later with Object, Identity Morphism, Natural Transformation, Term, Universe, and Univalence dependency structure.

## Classification list

```json
[
  {
    "id": "SC-P0-RUNTIME",
    "severity": "P0",
    "classification": "runtime_proof_gap",
    "issue_required": true,
    "ready_blocker": true
  },
  {
    "id": "SC-P1-SCHEMA",
    "severity": "P1",
    "classification": "validation_depth_gap",
    "issue_required": true,
    "ready_blocker": true
  },
  {
    "id": "SC-P1-PRIVACY",
    "severity": "P1",
    "classification": "privacy_convention_gap",
    "issue_required": true,
    "ready_blocker": false
  },
  {
    "id": "SC-P1-DISTILL",
    "severity": "P1",
    "classification": "distillation_hardening_gap",
    "issue_required": true,
    "ready_blocker": false
  },
  {
    "id": "SC-P2-GRAPH",
    "severity": "P2",
    "classification": "graph_index_future_gap",
    "issue_required": true,
    "ready_blocker": false
  },
  {
    "id": "SC-P2-FOUNDATION",
    "severity": "P2",
    "classification": "foundation_seed_expansion_gap",
    "issue_required": true,
    "ready_blocker": false
  }
]
```

## Recommendation

Keep PR #1 as draft.

Do not mark ready until P0 and P1 ready-blockers are resolved or explicitly deferred by human decision.

Next action:

```text
Create issues from SC gap list, link them to PR #1, then apply fixes in batches until local tests pass.
```
