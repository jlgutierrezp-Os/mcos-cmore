# Publication Gate

## Purpose

The publication gate decides whether an artifact can move from private or staged work into a public branch.

## Default

```json
{
  "public_release_default": false,
  "human_review_required": true
}
```

## Before publication

Confirm:

- source is synthetic or approved;
- no private identifiers remain;
- no credentials remain;
- no private logs remain;
- commercial terms are not changed;
- external APIs remain inactive unless separately approved;
- paid APIs remain inactive unless separately approved.

## Possible outcomes

- keep_private;
- revise;
- publish_synthetic_abstraction;
- promote_to_core;
- reject.
