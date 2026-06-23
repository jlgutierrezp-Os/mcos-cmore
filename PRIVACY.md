# Privacy Policy

## Scope

This repository is public-visible and should contain only synthetic mathematical examples, public documentation, and reviewed source code.

## Private work

Private or proprietary models must remain local unless a human operator explicitly approves a safe abstraction for publication.

Use the zero-distillation workflow before any publication decision:

```bash
python -m mcos.cli distill-zero examples/private_model_synthetic_input.private.json distill/review_queue/zero_candidate.json --mode skeleton
```

## Public repository rule

Do not publish:

- personal private records;
- private health records;
- credentials;
- tokens;
- unreleased proprietary models;
- private source documents;
- private logs.

## Default state

```json
{
  "public_release_default": false,
  "human_review_required": true,
  "synthetic_examples_only": true
}
```
