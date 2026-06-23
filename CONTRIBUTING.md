# Contributing

## Contribution model

MCOS/C-MORE accepts public feedback and proposed changes through reviewed GitHub workflows.

This does not grant commercial use rights.

## Before contributing

Run:

```bash
python -m unittest discover -s tests
python -m mcos.cli selfdebug
bash scripts/run_all_checks.sh
```

## Rules

- Keep v0.1 local-first.
- Do not activate external APIs.
- Do not activate paid APIs.
- Do not add credentials.
- Do not add private data.
- Use synthetic examples.
- Keep human review gates explicit.

## Pull requests

A pull request should explain:

- what changed;
- why it helps the Math Knowledge Graph goal;
- what tests were run;
- whether any future adapter boundary is affected.

## Commercial use

Commercial use requires a separate written agreement.
