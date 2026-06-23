from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from mcos.core import utc_now


class DistillError(ValueError):
    pass


def load_private_model(path: str | Path) -> dict[str, Any]:
    p = Path(path)
    if not p.exists():
        raise DistillError(f"model file not found: {p}")
    payload = json.loads(p.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise DistillError("model payload must be an object")
    return payload


def zero_distill_model(payload: dict[str, Any], mode: str = "skeleton") -> dict[str, Any]:
    if mode not in {"skeleton", "structure"}:
        raise DistillError("mode must be skeleton or structure")
    objects = payload.get("objects", [])
    relations = payload.get("relations", [])
    if not isinstance(objects, list) or not isinstance(relations, list):
        raise DistillError("objects and relations must be arrays")
    distilled_objects = []
    for item in objects:
        if not isinstance(item, dict):
            continue
        distilled_objects.append({
            "name": "DISTILLED_OBJECT",
            "object_type": item.get("object_type", "Definition"),
            "formal_system": "unknown",
            "alpha_confidence": min(float(item.get("alpha_confidence", 0.2)), 0.2),
            "status": "open",
            "publication_state": "private_review_required",
        })
    distilled_relations = []
    for item in relations:
        if not isinstance(item, dict):
            continue
        distilled_relations.append({
            "source": "DISTILLED_SOURCE",
            "target": "DISTILLED_TARGET",
            "relation_type": item.get("relation_type", "depends_on"),
            "alpha_confidence": min(float(item.get("alpha_confidence", 0.2)), 0.2),
            "publication_state": "private_review_required",
        })
    return {
        "distillation_status": "created",
        "mode": mode,
        "release_state": "private_review_required",
        "public_release_allowed": False,
        "human_review_required": True,
        "created_at": utc_now(),
        "objects": distilled_objects,
        "relations": distilled_relations,
    }


def distill_file(input_path: str | Path, output_path: str | Path, mode: str = "skeleton") -> dict[str, Any]:
    payload = load_private_model(input_path)
    distilled = zero_distill_model(payload, mode=mode)
    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(distilled, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return {"status": "written", "output_file": str(out), "public_release_allowed": False, "human_review_required": True}
