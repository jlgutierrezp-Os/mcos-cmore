# Graph Index v0.2

## Purpose

Provide local lookup helpers over the existing JSONL node and edge store.

This layer remains local-first and does not require an external graph database.

## Scope

Implemented module:

```text
mcos/index.py
```

Implemented helpers:

- `load_graph_index(data_dir="data")`
- `get_node(index, id_or_name)`
- `get_node_by_id(index, node_id)`
- `get_node_by_name(index, name)`
- `list_dependencies(index, id_or_name)`
- `list_dependents(index, id_or_name)`
- `find_edges(index, source=None, target=None, relation_type=None)`
- `find_equivalent(index, id_or_name)`
- `summarize_index(index)`

## Data source

The index is rebuilt from:

```text
data/nodes.jsonl
data/edges.jsonl
```

using the existing `JsonlStore`.

## Boundary

```json
{
  "local_only": true,
  "external_database_required": false,
  "external_api_required": false,
  "paid_api_required": false,
  "proof_assistant_required": false,
  "mcp_runtime_required": false
}
```

## Tests

```bash
python -m unittest discover -s tests
```

Current test file:

```text
tests/test_index.py
```
