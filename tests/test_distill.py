import json
import tempfile
import unittest
from pathlib import Path

from mcos.distill import distill_file, zero_distill_model


class DistillTests(unittest.TestCase):
    def test_zero_distill_model(self):
        result = zero_distill_model({
            "objects": [{"name": "Private Concept", "object_type": "Definition", "alpha_confidence": 0.9}],
            "relations": [{"source": "A", "target": "B", "relation_type": "depends_on", "alpha_confidence": 0.9}],
        })
        self.assertFalse(result["public_release_allowed"])
        self.assertTrue(result["human_review_required"])
        self.assertEqual(result["objects"][0]["name"], "DISTILLED_OBJECT")
        self.assertLessEqual(result["objects"][0]["alpha_confidence"], 0.2)

    def test_distill_file(self):
        with tempfile.TemporaryDirectory() as d:
            source = Path(d) / "model.json"
            target = Path(d) / "out" / "zero.json"
            source.write_text(json.dumps({"objects": [], "relations": []}), encoding="utf-8")
            summary = distill_file(source, target)
            self.assertEqual(summary["status"], "written")
            self.assertTrue(target.exists())


if __name__ == "__main__":
    unittest.main()
