import json
import tempfile
import unittest
from pathlib import Path

from mcos.distill import DistillError, distill_file, zero_distill_model


class DistillTests(unittest.TestCase):
    def test_zero_distill_model(self):
        result = zero_distill_model({
            "model_id": "SHOULD_NOT_APPEAR",
            "objects": [{"name": "Private Concept", "object_type": "Definition", "alpha_confidence": 0.9, "metadata": {"secret": "x"}}],
            "relations": [{"source": "A", "target": "B", "relation_type": "depends_on", "alpha_confidence": 0.9}],
        })
        as_text = json.dumps(result)
        self.assertFalse(result["public_release_allowed"])
        self.assertTrue(result["human_review_required"])
        self.assertEqual(result["objects"][0]["name"], "DISTILLED_OBJECT")
        self.assertEqual(result["relations"][0]["source"], "DISTILLED_SOURCE")
        self.assertLessEqual(result["objects"][0]["alpha_confidence"], 0.2)
        self.assertNotIn("Private Concept", as_text)
        self.assertNotIn("SHOULD_NOT_APPEAR", as_text)
        self.assertNotIn("secret", as_text)
        self.assertFalse(result["review_summary"]["private_names_preserved"])

    def test_alpha_values_are_safely_reduced(self):
        result = zero_distill_model({
            "objects": [
                {"alpha_confidence": "not-a-number"},
                {"alpha_confidence": 99},
                {"alpha_confidence": -5},
                {},
            ],
            "relations": [
                {"alpha_confidence": "bad"},
                {"alpha_confidence": 0.99},
            ],
        })
        for item in result["objects"] + result["relations"]:
            self.assertGreaterEqual(item["alpha_confidence"], 0.0)
            self.assertLessEqual(item["alpha_confidence"], 0.2)

    def test_invalid_collection_shape_rejected(self):
        with self.assertRaises(DistillError):
            zero_distill_model({"objects": {}, "relations": []})
        with self.assertRaises(DistillError):
            zero_distill_model({"objects": [], "relations": {}})

    def test_unknown_types_are_normalized(self):
        result = zero_distill_model({
            "objects": [{"object_type": "PrivateObjectType"}],
            "relations": [{"relation_type": "private_relation"}],
        })
        self.assertEqual(result["objects"][0]["object_type"], "Definition")
        self.assertEqual(result["relations"][0]["relation_type"], "depends_on")

    def test_distill_file(self):
        with tempfile.TemporaryDirectory() as d:
            source = Path(d) / "model.json"
            target = Path(d) / "out" / "zero.json"
            source.write_text(json.dumps({"objects": [], "relations": []}), encoding="utf-8")
            summary = distill_file(source, target)
            self.assertEqual(summary["status"], "written")
            self.assertTrue(summary["human_review_required"])
            self.assertTrue(target.exists())


if __name__ == "__main__":
    unittest.main()
