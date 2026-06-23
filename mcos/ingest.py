from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from mcos.core import JsonlStore, validate_math_object, validate_math_relation, utc_now


class IngestError(ValueError):
    pass


def load_records(path: str | Path) -> list[dict[str, Any]]:
    p = Path(path)
    if not p.exists():
        raise IngestError(f"feed file not found: {p}")
    text = p.read_text(encoding="utf-8").strip()
    if not text:
        raise IngestError("feed file is empty")
    if p.suffix.lower() == ".jsonl":
        return [json.loads(line) for line in text.splitlines() if line.strip()]
    payload = json.loads(text)
    if isinstance(payload, list):
        return payload
    if isinstance(payload, dict):
        if "objects" in payload or "relations" in payload:
            objects = payload.get("objects", [])
            relations = payload.get("relations", [])
            if not isinstance(objects, list) or not isinstance(relations, list):
                raise IngestError("objects and relations must be arrays")
            return objects + relations
        return [payload]
    raise IngestError("unsupported feed payload type")


def classify_record(record: dict[str, Any]) -> str:
    if not isinstance(record, dict):
        raise IngestError("each feed record must be an object")
    if {"source", "target", "relation_type"}.issubset(record.keys()):
        return "relation"
    if {"name", "object_type", "formal_system"}.issubset(record.keys()):
        return "object"
    raise IngestError("record is neither MathObject nor MathRelation")


def validate_feed_records(records: list[dict[str, Any]]) -> dict[str, Any]:
    report = {"status": "passed", "records_total": len(records), "objects_valid": 0, "relations_valid": 0, "errors": [], "created_at": utc_now()}
    for idx, record in enumerate(records):
        try:
            kind = classify_record(record)
            if kind == "object":
                validate_math_object(record)
                report["objects_valid"] += 1
            elif kind == "relation":
                validate_math_relation(record)
                report["relations_valid"] += 1
        except Exception as exc:
            report["errors"].append({"index": idx, "error": repr(exc)})
    if report["errors"]:
        report["status"] = "failed"
    return report


def ingest_file(path: str | Path, data_dir: str | Path = "data", dry_run: bool = False) -> dict[str, Any]:
    records = load_records(path)
    validation = validate_feed_records(records)
    summary = {"status": validation["status"], "feed_file": str(path), "data_dir": str(data_dir), "dry_run": dry_run, "records_total": validation["records_total"], "objects_valid": validation["objects_valid"], "relations_valid": validation["relations_valid"], "objects_written": 0, "relations_written": 0, "errors": validation["errors"], "created_at": utc_now()}
    if summary["status"] != "passed" or dry_run:
        return summary
    store = JsonlStore(data_dir)
    for record in records:
        kind = classify_record(record)
        if kind == "object":
            store.add_node(record)
            summary["objects_written"] += 1
        elif kind == "relation":
            store.add_edge(record)
            summary["relations_written"] += 1
    return summary
