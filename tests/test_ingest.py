import json
import tempfile
import unittest
from pathlib import Path

from mcos.ingest import ingest_file


class IngestTests(unittest.TestCase):
    def test_source_package_dry_run(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "feed.json"
            p.write_text(json.dumps({
                "objects": [{
                    "id": "550e8400-e29b-41d4-a716-446655440020",
                    "name": "Group",
                    "object_type": "Definition",
                    "formal_system": "math",
                    "alpha_confidence": 0.4,
                    "dependencies": ["Set"],
                    "status": "open"
                }],
                "relations": [{
                    "id": "550e8400-e29b-41d4-a716-446655440021",
                    "source": "Group",
                    "target": "Monoid",
                    "relation_type": "specializes",
                    "alpha_confidence": 0.4
                }]
            }), encoding="utf-8")
            result = ingest_file(p, Path(d) / "data", dry_run=True)
            self.assertEqual(result["status"], "passed")
            self.assertEqual(result["records_total"], 2)
            self.assertEqual(result["objects_written"], 0)

    def test_source_package_write(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "feed.jsonl"
            p.write_text(json.dumps({
                "id": "550e8400-e29b-41d4-a716-446655440030",
                "name": "Ring",
                "object_type": "Definition",
                "formal_system": "math",
                "alpha_confidence": 0.4,
                "dependencies": ["Group"],
                "status": "open"
            }) + "\n", encoding="utf-8")
            result = ingest_file(p, Path(d) / "data", dry_run=False)
            self.assertEqual(result["status"], "passed")
            self.assertEqual(result["objects_written"], 1)


if __name__ == "__main__":
    unittest.main()
