from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from mcos.core import utc_now

REGISTRY_PATH = Path(__file__).resolve().parents[1] / "registry" / "bootstrap_feed_registry.json"


def load_bootstrap_feed_registry(path: str | Path | None = None) -> dict[str, Any]:
    p = Path(path) if path is not None else REGISTRY_PATH
    return json.loads(p.read_text(encoding="utf-8"))


def write_initial_feed_registry(data_dir: str | Path = "data") -> dict[str, Any]:
    data_path = Path(data_dir)
    data_path.mkdir(parents=True, exist_ok=True)
    registry = load_bootstrap_feed_registry()
    out = data_path / "bootstrap_feed_registry.json"
    out.write_text(json.dumps(registry, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    index = {
        "status": "initialized",
        "created_at": utc_now(),
        "registry_file": str(out),
        "active_feed_modes": registry.get("active_feed_modes", []),
        "minimum_capabilities_total": len(registry.get("minimum_capabilities", [])),
        "local_first": registry.get("local_first", True),
        "public_release_default": registry.get("public_release_default", False),
        "human_review_required": registry.get("human_review_required", True),
    }
    (data_path / "bootstrap_feed_index.json").write_text(json.dumps(index, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return index


def bootstrap_readiness_report(project_root: str | Path = ".") -> dict[str, Any]:
    root = Path(project_root)
    registry = load_bootstrap_feed_registry()
    required_paths = [
        "README.md",
        "LICENSE",
        "pyproject.toml",
        "mcos/core.py",
        "mcos/ingest.py",
        "mcos/distill.py",
        "mcos/feed_registry.py",
        "examples/feed_source_package.json",
        "registry/bootstrap_feed_registry.json",
        "docs/BOOTSTRAP_FEED_REGISTRY.md",
        "docs/MCOS_BOOTSTRAP_BUILD_SPEC.md",
        "scripts/run_all_checks.sh",
    ]
    missing = [p for p in required_paths if not (root / p).exists()]
    capability_summary = {
        item["id"]: {"name": item["name"], "status": item["status"]}
        for item in registry.get("minimum_capabilities", [])
    }
    return {
        "status": "passed" if not missing else "failed",
        "created_at": utc_now(),
        "registry_id": registry.get("registry_id"),
        "required_paths_total": len(required_paths),
        "missing_required_paths": missing,
        "minimum_capabilities_total": len(capability_summary),
        "minimum_capabilities": capability_summary,
        "local_first": registry.get("local_first", True),
        "public_release_default": registry.get("public_release_default", False),
        "human_review_required": registry.get("human_review_required", True),
    }
