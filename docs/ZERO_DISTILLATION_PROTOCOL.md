# Zero Distillation Protocol

## Purpose

Zero-distillation lets MCOS/C-MORE analyze private or proprietary models without publishing them.

It converts a private source into a minimal review candidate that preserves only structural shape.

## Principle

```text
agnostic does not mean ignorant
minimal does not mean empty
private does not mean publishable
```

## Flow

```text
private/proprietary model
↓
local validation
↓
zero-distill
↓
private review candidate
↓
human decision
↓
keep private / revise / publish selected synthetic abstraction
```

## Command

```bash
python -m mcos.cli distill-zero examples/private_model_synthetic_input.private.json distill/review_queue/zero_candidate.json --mode skeleton
```

## Default protections

The default distilled package must not preserve:

- private names;
- proprietary identifiers;
- private metadata;
- publication permission;
- private dependency names.

It may preserve:

- object type;
- relation type;
- structural count;
- reduced alpha confidence;
- private review required flag.

## Publication rule

A zero-distilled candidate is not automatically public.

Publication requires explicit human review and a separate decision.
