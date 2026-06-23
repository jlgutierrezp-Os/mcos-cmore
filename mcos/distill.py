from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from mcos.core import RELATION_TYPES, OBJECT_TYPES, utc_now


class DistillError(ValueError):
    pass


SAFE_OBJECT_TYPE = "Definition"
SAFE_RELATION_TYPE = "depends_on"
MAX_DISTILL_ITEMS = 1000


def load_private_model(path: str | Path) -> dict[str, Any]:
    p = Path(path)
    if not p.exists():
        raise DistillError(f"model file not found: {p}")
    payload = json.loads(p.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise DistillError("model payload must be an object")
    return payload


def _safe_reduced_alpha(value: Any) -> float:
    try:
        numeric = float(value)
    except (TypeError, ValueError):
        numeric = 0.2
    if numeric < 0:
        numeric = 0.0
    if numeric > 1:
        numeric = 1.0
    return min(numeric, 0.2)


def _safe_object_type(value: Any) -> str:
    if isinstance(value, str) and value in OBJECT_TYPES:
        return value
    return SAFE_OBJECT_TYPE


def _safe_relation_type(value: Any) -> str:
    if isinstance(value, str) and value in RELATION_TYPES:
        return value
    return SAFE_RELATION_TYPE


def _safe_list(value: Any, field_name: str) -> list[Any]:
    if value is None:
        return []
    if not isinstance(value, list):
        raise DistillError(f"{field_name} must be an array")
    if len(value) > MAX_DISTILL_ITEMS:
        raise DistillError(f"{field_name} exceeds maximum allowed items")
    return value


def zero_distill_model(payload: dict[str, Any], mode: str = "skeleton") -> dict[str, Any]:
    if not isinstance(payload, dict):
        raise DistillError("payload must be an object")
    if mode not in {"skeleton", "structure"}:
        raise DistillError("mode must be skeleton or structure")

    objects = _safe_list(payload.get("objects", []), "objects")
    relations = _safe_list(payload.get("relations", []), "relations")

    skipped = {"objects": 0, "relations": 0}
    distilled_objects = []
    for item in objects:
        if not isinstance(item, dict):
            skipped["objects"] += 1
            continue
        distilled_objects.append({
            "name": "DISTILLED_OBJECT",
            "object_type": _safe_object_type(item.get("object_type", SAFE_OBJECT_TYPE)),
            "formal_system": "unknown",
            "alpha_confidence": _safe_reduced_alpha(item.get("alpha_confidence", 0.2)),
            "status": "open",
            "publication_state": "private_review_required",
        })

    distilled_relations = []
    for item in relations:
        if not isinstance(item, dict):
            skipped["relations"] += 1
            continue
        distilled_relations.append({
            "source": "DISTILLED_SOURCE",
            "target": "DISTILLED_TARGET",
            "relation_type": _safe_relation_type(item.get("relation_type", SAFE_RELATION_TYPE)),
            "alpha_confidence": _safe_reduced_alpha(item.get("alpha_confidence", 0.2)),
            "publication_state": "private_review_required",
        })

    return {
        "distillation_status": "created",
        "mode": mode,
        "release_state": "private_review_required",
        "public_release_allowed": False,
        "human_review_required": True,
        "created_at": utc_now(),
        "review_summary": {
            "source_objects_count": len(objects),
            "source_relations_count": len(relations),
            "distilled_objects_count": len(distilled_objects),
            "distilled_relations_count": len(distilled_relations),
            "skipped_items": skipped,
            "private_names_preserved": False,
            "private_metadata_preserved": False,
            "source_identifiers_preserved": False,
        },
        "objects": distilled_objects,
        "relations": distilled_relations,
    }


def distill_file(input_path: str | Path, output_path: str | Path, mode: str = "skeleton") -> dict[str, Any]:
    payload = load_private_model(input_path)
    distilled = zero_distill_model(payload, mode=mode)
    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(distilled, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return {
        "status": "written",
        "output_file": str(out),
        "public_release_allowed": False,
        "human_review_required": True,
        "review_summary": distilled["review_summary"],
    }
