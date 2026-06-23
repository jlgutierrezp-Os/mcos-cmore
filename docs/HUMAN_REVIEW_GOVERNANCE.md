# Human Review Governance

## Rule

No staged material is promoted to core without explicit human review.

## Decisions

Allowed decisions:

- accept;
- reject;
- revise;
- defer;
- promote_to_core.

## Review packet

Each promotion candidate should include:

```json
{
  "artifact": "path or id",
  "status": "success | partial | failed",
  "severity": "warning | error | critical",
  "recommendation": "string",
  "required_decision": "accept | reject | revise | defer | promote_to_core",
  "human_comment": "string"
}
```

## Branch policy

The integration branch may collect staged changes.

Merge to `main` requires human approval.
