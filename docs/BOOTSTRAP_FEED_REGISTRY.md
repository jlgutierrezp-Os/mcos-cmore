# Bootstrap Feed Registry

The bootstrap feed registry defines how MCOS/C-MORE is fed immediately after installation.

## Active modes

- manual JSON;
- JSONL batch;
- source package JSON;
- zero-distillation review.

## Future modes not active

- Lean adapter;
- Coq adapter;
- MCP adapter;
- external API;
- paid API.

## Command

```bash
python -m mcos.cli feed-registry
python -m mcos.cli init-feed-registry --data-dir data
python -m mcos.cli bootstrap-readiness
```

## Principle

MCOS/C-MORE starts agnostic but not empty. It can ingest synthetic public seeds and inspect private/proprietary models only through local review and zero-distillation before any publication decision.
