from __future__ import annotations

import argparse
import json
import re
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from uuid import uuid4

UUID_RE = re.compile(r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$")
OBJECT_TYPES = {"Definition", "Axiom", "Theorem", "Lemma", "Corollary", "Conjecture", "Proof", "Counterexample", "Type", "Group", "Ring", "Field", "Function", "Relation", "Transformation", "Dataset", "SimulationResult", "Space", "Category", "Functor", "Morphism"}
RELATION_TYPES = {"defines", "implies", "depends_on", "proves", "refutes", "equivalent_to", "generalizes", "specializes", "transforms_into", "approximates", "derived_from"}
OBJECT_STATUS = {"open", "verified", "failed", "partial", "refuted"}
RESPONSE_STATUS = {"success", "partial", "failed"}

class ValidationError(ValueError):
    pass

def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")

def new_id() -> str:
    return str(uuid4())

def require_string(value: Any, name: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValidationError(f"{name} must be a non-empty string")

def require_uuid(value: Any, name: str) -> None:
    require_string(value, name)
    if not UUID_RE.match(value):
        raise ValidationError(f"{name} must be canonical lowercase UUID")

def require_alpha(value: Any) -> None:
    if not isinstance(value, (int, float)) or isinstance(value, bool) or value < 0 or value > 1:
        raise ValidationError("alpha_confidence must be a number in [0, 1]")

def closed(obj: dict[str, Any], required: list[str], optional: set[str] | None = None) -> None:
    optional = optional or set()
    missing = [k for k in required if k not in obj]
    extra = [k for k in obj if k not in set(required) | optional]
    if missing:
        raise ValidationError(f"missing required fields: {missing}")
    if extra:
        raise ValidationError(f"unexpected fields: {extra}")

@dataclass
class MathObject:
    name: str
    object_type: str = "Definition"
    formal_system: str = "math"
    alpha_confidence: float = 0.4
    dependencies: list[str] = field(default_factory=list)
    status: str = "open"
    id: str = field(default_factory=new_id)
    created_at: str = field(default_factory=utc_now)
    updated_at: str = field(default_factory=utc_now)
    metadata: dict[str, Any] = field(default_factory=dict)
    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

@dataclass
class MathRelation:
    source: str
    target: str
    relation_type: str
    alpha_confidence: float = 0.4
    id: str = field(default_factory=new_id)
    created_at: str = field(default_factory=utc_now)
    metadata: dict[str, Any] = field(default_factory=dict)
    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

def validate_math_object(obj: dict[str, Any]) -> bool:
    closed(obj, ["id", "name", "object_type", "formal_system", "alpha_confidence", "dependencies", "status"], {"created_at", "updated_at", "metadata"})
    require_uuid(obj["id"], "id")
    require_string(obj["name"], "name")
    require_string(obj["formal_system"], "formal_system")
    require_alpha(obj["alpha_confidence"])
    if obj["object_type"] not in OBJECT_TYPES:
        raise ValidationError("object_type not allowed")
    if obj["status"] not in OBJECT_STATUS:
        raise ValidationError("status not allowed")
    if not isinstance(obj["dependencies"], list) or any(not isinstance(x, str) or not x.strip() for x in obj["dependencies"]):
        raise ValidationError("dependencies must be list of non-empty strings")
    return True

def validate_math_relation(obj: dict[str, Any]) -> bool:
    closed(obj, ["id", "source", "target", "relation_type", "alpha_confidence"], {"created_at", "metadata"})
    require_uuid(obj["id"], "id")
    require_string(obj["source"], "source")
    require_string(obj["target"], "target")
    require_alpha(obj["alpha_confidence"])
    if obj["relation_type"] not in RELATION_TYPES:
        raise ValidationError("relation_type not allowed")
    return True

def validate_adapter_response(obj: dict[str, Any]) -> bool:
    closed(obj, ["request_id", "status", "result"], {"message", "equivalence_report", "created_at"})
    require_uuid(obj["request_id"], "request_id")
    if obj["status"] not in RESPONSE_STATUS:
        raise ValidationError("status not allowed")
    if "message" in obj:
        require_string(obj["message"], "message")
    if not isinstance(obj["result"], dict) or not obj["result"]:
        raise ValidationError("result must be non-empty object")
    return True

class JsonlStore:
    def __init__(self, data_dir: str | Path = "data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.nodes_path = self.data_dir / "nodes.jsonl"
        self.edges_path = self.data_dir / "edges.jsonl"
    def add_node(self, obj: dict[str, Any]) -> dict[str, Any]:
        validate_math_object(obj); self._append(self.nodes_path, obj); return obj
    def add_edge(self, obj: dict[str, Any]) -> dict[str, Any]:
        validate_math_relation(obj); self._append(self.edges_path, obj); return obj
    def nodes(self) -> list[dict[str, Any]]:
        return self._read(self.nodes_path)
    def edges(self) -> list[dict[str, Any]]:
        return self._read(self.edges_path)
    def export(self) -> dict[str, Any]:
        return {"nodes": self.nodes(), "edges": self.edges()}
    @staticmethod
    def _append(path: Path, obj: dict[str, Any]) -> None:
        with path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(obj, ensure_ascii=False) + "\n")
    @staticmethod
    def _read(path: Path) -> list[dict[str, Any]]:
        if not path.exists():
            return []
        return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]

def load_json(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))

def print_json(obj: Any) -> None:
    print(json.dumps(obj, indent=2, ensure_ascii=False))

def compare_math_objects(left: dict[str, Any], right: dict[str, Any]) -> dict[str, Any]:
    differences = []
    for field_name in ["name", "object_type", "formal_system", "dependencies", "status"]:
        if left.get(field_name) != right.get(field_name):
            differences.append({"description": f"Field differs: {field_name}", "path": f"/{field_name}", "severity": "error"})
    response = {"request_id": new_id(), "status": "success" if not differences else "partial", "result": {"equivalent": not differences, "difference_count": len(differences)}, "equivalence_report": {"checked": True, "comparison_scope": "minimal_math_object_equivalence", "differences": differences}, "created_at": utc_now()}
    validate_adapter_response(response)
    return response

def review_packet(response: dict[str, Any]) -> dict[str, Any]:
    validate_adapter_response(response)
    return {"review_id": new_id(), "request_id": response["request_id"], "summary": response.get("message", "Review required."), "status": response["status"], "severity": "warning" if response["status"] == "success" else "error", "recommendation": "Human review required before promotion.", "required_decision": "accept" if response["status"] == "success" else "revise", "artifact": response["result"], "created_at": utc_now()}

def selfdebug() -> dict[str, Any]:
    checks = []
    def ok(name: str, fn):
        try:
            fn(); checks.append({"name": name, "passed": True})
        except Exception as exc:
            checks.append({"name": name, "passed": False, "error": repr(exc)})
    ok("valid_math_object", lambda: validate_math_object(MathObject("Group").to_dict()))
    try:
        validate_math_object(MathObject("Bad", alpha_confidence=2).to_dict())
        checks.append({"name": "invalid_alpha_rejected", "passed": False})
    except ValidationError:
        checks.append({"name": "invalid_alpha_rejected", "passed": True})
    ok("valid_math_relation", lambda: validate_math_relation(MathRelation("Group", "Monoid", "specializes").to_dict()))
    ok("compare_and_review", lambda: review_packet(compare_math_objects(MathObject("Group").to_dict(), MathObject("Group").to_dict())))
    return {"status": "passed" if all(c["passed"] for c in checks) else "failed", "checks": checks, "created_at": utc_now()}

def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(prog="mcos")
    sub = parser.add_subparsers(required=True)
    p = sub.add_parser("selfdebug"); p.set_defaults(func=lambda args: print_json(selfdebug()))
    p = sub.add_parser("object-new"); p.add_argument("name"); p.set_defaults(func=lambda args: print_json(MathObject(args.name).to_dict()))
    p = sub.add_parser("validate"); p.add_argument("kind", choices=["object", "relation", "response"]); p.add_argument("file")
    def validate_cmd(args):
        obj = load_json(args.file)
        {"object": validate_math_object, "relation": validate_math_relation, "response": validate_adapter_response}[args.kind](obj)
        print("VALID")
    p.set_defaults(func=validate_cmd)
    p = sub.add_parser("graph-add"); p.add_argument("file"); p.set_defaults(func=lambda args: print_json(JsonlStore().add_node(load_json(args.file))))
    p = sub.add_parser("graph-edge"); p.add_argument("file"); p.set_defaults(func=lambda args: print_json(JsonlStore().add_edge(load_json(args.file))))
    p = sub.add_parser("graph-export"); p.set_defaults(func=lambda args: print_json(JsonlStore().export()))
    p = sub.add_parser("compare"); p.add_argument("left"); p.add_argument("right"); p.set_defaults(func=lambda args: print_json(compare_math_objects(load_json(args.left), load_json(args.right))))
    args = parser.parse_args(argv); args.func(args)

if __name__ == "__main__":
    main()
