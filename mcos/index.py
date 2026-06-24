from __future__ import annotations

from pathlib import Path
from typing import Any

from mcos.core import JsonlStore, validate_math_object, validate_math_relation


class GraphIndexError(ValueError):
    pass


def _add_unique(items: list[str], value: Any) -> None:
    if isinstance(value, str) and value.strip() and value not in items:
        items.append(value)


def _node_keys(node: dict[str, Any]) -> set[str]:
    keys = set()
    for key in ("id", "name"):
        value = node.get(key)
        if isinstance(value, str) and value.strip():
            keys.add(value)
    return keys


def _resolve_keys(index: dict[str, Any], id_or_name: str | None) -> set[str]:
    if id_or_name is None:
        return set()
    node = get_node(index, id_or_name, required=False)
    if node is None:
        return {id_or_name}
    return _node_keys(node)


def load_graph_index(data_dir: str | Path = "data") -> dict[str, Any]:
    store = JsonlStore(data_dir)
    nodes = store.nodes()
    edges = store.edges()

    nodes_by_id: dict[str, dict[str, Any]] = {}
    nodes_by_name: dict[str, dict[str, Any]] = {}
    duplicate_ids: list[str] = []
    duplicate_names: list[str] = []

    for node in nodes:
        validate_math_object(node)
        node_id = node["id"]
        node_name = node["name"]
        if node_id in nodes_by_id:
            duplicate_ids.append(node_id)
        if node_name in nodes_by_name:
            duplicate_names.append(node_name)
        nodes_by_id[node_id] = node
        nodes_by_name[node_name] = node

    for edge in edges:
        validate_math_relation(edge)

    return {
        "data_dir": str(data_dir),
        "nodes": nodes,
        "edges": edges,
        "nodes_by_id": nodes_by_id,
        "nodes_by_name": nodes_by_name,
        "duplicate_ids": duplicate_ids,
        "duplicate_names": duplicate_names,
        "nodes_total": len(nodes),
        "edges_total": len(edges),
    }


def get_node_by_id(index: dict[str, Any], node_id: str, required: bool = True) -> dict[str, Any] | None:
    node = index["nodes_by_id"].get(node_id)
    if node is None and required:
        raise GraphIndexError(f"node id not found: {node_id}")
    return node


def get_node_by_name(index: dict[str, Any], name: str, required: bool = True) -> dict[str, Any] | None:
    node = index["nodes_by_name"].get(name)
    if node is None and required:
        raise GraphIndexError(f"node name not found: {name}")
    return node


def get_node(index: dict[str, Any], id_or_name: str, required: bool = True) -> dict[str, Any] | None:
    node = index["nodes_by_id"].get(id_or_name) or index["nodes_by_name"].get(id_or_name)
    if node is None and required:
        raise GraphIndexError(f"node not found: {id_or_name}")
    return node


def find_edges(
    index: dict[str, Any],
    source: str | None = None,
    target: str | None = None,
    relation_type: str | None = None,
) -> list[dict[str, Any]]:
    source_keys = _resolve_keys(index, source)
    target_keys = _resolve_keys(index, target)
    results = []
    for edge in index["edges"]:
        if source is not None and edge["source"] not in source_keys:
            continue
        if target is not None and edge["target"] not in target_keys:
            continue
        if relation_type is not None and edge["relation_type"] != relation_type:
            continue
        results.append(edge)
    return results


def list_dependencies(index: dict[str, Any], id_or_name: str) -> list[str]:
    node = get_node(index, id_or_name)
    dependencies: list[str] = []
    for dependency in node.get("dependencies", []):
        _add_unique(dependencies, dependency)
    for edge in find_edges(index, source=id_or_name, relation_type="depends_on"):
        _add_unique(dependencies, edge["target"])
    return dependencies


def list_dependents(index: dict[str, Any], id_or_name: str) -> list[str]:
    node = get_node(index, id_or_name)
    keys = _node_keys(node)
    dependents: list[str] = []
    for candidate in index["nodes"]:
        for dependency in candidate.get("dependencies", []):
            if dependency in keys:
                _add_unique(dependents, candidate["name"])
    for edge in find_edges(index, target=id_or_name, relation_type="depends_on"):
        _add_unique(dependents, edge["source"])
    return dependents


def find_equivalent(index: dict[str, Any], id_or_name: str) -> list[str]:
    keys = _resolve_keys(index, id_or_name)
    if not keys:
        raise GraphIndexError(f"node not found: {id_or_name}")
    equivalents: list[str] = []
    for edge in index["edges"]:
        if edge["relation_type"] != "equivalent_to":
            continue
        if edge["source"] in keys:
            _add_unique(equivalents, edge["target"])
        if edge["target"] in keys:
            _add_unique(equivalents, edge["source"])
    return equivalents


def summarize_index(index: dict[str, Any]) -> dict[str, Any]:
    return {
        "status": "passed" if not index["duplicate_ids"] and not index["duplicate_names"] else "warning",
        "data_dir": index["data_dir"],
        "nodes_total": index["nodes_total"],
        "edges_total": index["edges_total"],
        "duplicate_ids": index["duplicate_ids"],
        "duplicate_names": index["duplicate_names"],
        "local_only": True,
    }
