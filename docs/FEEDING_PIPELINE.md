# MCOS/C-MORE Feeding Pipeline

## Purpose

This document answers how MCOS/C-MORE is fed after installation.

## Active v0.1 feed flow

```text
JSON / JSONL / source package
↓
mcos.ingest.load_records()
↓
mcos.ingest.validate_feed_records()
↓
validate_math_object() / validate_math_relation()
↓
JsonlStore.add_node() / JsonlStore.add_edge()
↓
data/nodes.jsonl + data/edges.jsonl
```

## Commands

Dry-run:

```bash
python -m mcos.cli ingest examples/feed_source_package.json --dry-run
```

Write locally:

```bash
python -m mcos.cli ingest examples/feed_source_package.json
```

Export graph:

```bash
python -m mcos.cli graph-export
```

## Governance

No external or paid API is active. Human review is required before promotion of private or proprietary material.
