# Private Model Workflow

## Purpose

MCOS/C-MORE must support personal or proprietary model analysis without requiring public release.

## States

```text
private_input
local_review
zero_distilled_candidate
human_review_required
approved_for_publication / keep_private / revise
```

## Rules

1. Private models are not committed by default.
2. Files ending in `.private.json` or `.private.jsonl` are ignored by Git.
3. Public examples must be synthetic.
4. Zero-distilled output is still not public by default.
5. Human review decides whether an abstraction can be published.

## Local-only example

```bash
python -m mcos.cli distill-zero examples/private_model_synthetic_input.private.json distill/review_queue/zero_candidate.json --mode skeleton
```

## Publication gate

Before publishing a distilled abstraction, confirm:

- no private names remain;
- no proprietary identifiers remain;
- no private source metadata remains;
- no credentials or secrets are included;
- the human operator approved release.
