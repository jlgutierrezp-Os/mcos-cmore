# MCOS / C-MORE

> Source-available non-commercial. Public review, local testing, educational/research use, feedback, and contributions are welcome. Commercial use requires a separate written license agreement.

MCOS / C-MORE is a local-first bootstrap for a Mathematical Cognitive Operating System focused first on a Math Knowledge Graph.

## Current status

PR #1 has been squash-merged into `main` after Batch 6B runtime proof.

The integration branch was:

```text
integration/mcos-transfer-v0-1-r
```

The active public bootstrap is now on:

```text
main
```

## Current scope

Active in `main`:

- MathObject;
- MathRelation;
- local validation;
- JSONL node/edge store;
- graph export;
- minimal equivalence comparison;
- human review packet generation;
- local ingestion;
- zero-distillation review workflow;
- bootstrap feed registry;
- Foundation Layer seed: ZFC + Category Theory + HoTT;
- selfdebug;
- tests.

Not active:

- Lean adapter;
- Coq adapter;
- MCP server;
- external APIs;
- paid APIs;
- automatic promotion to core.

## Install

```bash
git clone https://github.com/jlgutierrezp-Os/mcos-cmore.git
cd mcos-cmore
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e .
python -m mcos.cli selfdebug
python -m unittest discover -s tests
bash scripts/run_all_checks.sh
```

## Feed the graph

Dry-run:

```bash
python -m mcos.cli ingest examples/feed_source_package.json --dry-run
```

Write locally:

```bash
python -m mcos.cli ingest examples/feed_source_package.json
```

Export:

```bash
python -m mcos.cli graph-export
```

## Foundation Layer

Dry-run the initial foundation seed:

```bash
python -m mcos.cli ingest examples/foundation_layer_seed.json --dry-run
```

Current foundation triad:

```text
ZFC + Category Theory + HoTT
```

## Private/proprietary model workflow

Private or proprietary models are not public by default. They should pass through local zero-distillation before any publication decision.

```bash
python -m mcos.cli distill-zero examples/private_model_synthetic_input.private.json distill/review_queue/zero_candidate.json --mode skeleton
```

## Bootstrap registry

```bash
python -m mcos.cli feed-registry
python -m mcos.cli init-feed-registry --data-dir data
python -m mcos.cli bootstrap-readiness
```

## Review gate

All future promotion from staged material into core requires explicit human review.
