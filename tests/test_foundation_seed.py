import json
import unittest
from pathlib import Path


FOUNDATION_SEED = Path("examples/foundation_layer_seed.json")


class FoundationSeedTests(unittest.TestCase):
    def setUp(self):
        self.payload = json.loads(FOUNDATION_SEED.read_text(encoding="utf-8"))
        self.objects_by_name = {item["name"]: item for item in self.payload["objects"]}
        self.relations_by_id = {item["id"]: item for item in self.payload["relations"]}

    def test_v0_1_object_ids_remain_stable(self):
        stable_ids = {
            "ZFC": "550e8400-e29b-41d4-a716-446655441000",
            "Category Theory": "550e8400-e29b-41d4-a716-446655441001",
            "HoTT": "550e8400-e29b-41d4-a716-446655441002",
            "Set": "550e8400-e29b-41d4-a716-446655441003",
            "Function": "550e8400-e29b-41d4-a716-446655441004",
            "Category": "550e8400-e29b-41d4-a716-446655441005",
            "Morphism": "550e8400-e29b-41d4-a716-446655441006",
            "Composition": "550e8400-e29b-41d4-a716-446655441007",
            "Type": "550e8400-e29b-41d4-a716-446655441008",
            "Path": "550e8400-e29b-41d4-a716-446655441009",
            "Equivalence": "550e8400-e29b-41d4-a716-446655441010",
        }
        for name, expected_id in stable_ids.items():
            with self.subTest(name=name):
                self.assertEqual(self.objects_by_name[name]["id"], expected_id)

    def test_new_v0_1a_object_ids_are_append_only(self):
        for name in [
            "Relation",
            "Object",
            "Identity Morphism",
            "Functor",
            "Natural Transformation",
            "Term",
            "Universe",
            "Univalence",
        ]:
            with self.subTest(name=name):
                self.assertGreaterEqual(self.objects_by_name[name]["id"], "550e8400-e29b-41d4-a716-446655441011")

    def test_new_foundation_dependencies_are_not_inverted(self):
        forbidden_new_edges = [
            ("Category", "Object", "depends_on"),
            ("Category", "Morphism", "depends_on"),
            ("Category", "Composition", "depends_on"),
            ("Category", "Identity Morphism", "depends_on"),
        ]
        actual_edges = {
            (item["source"], item["target"], item["relation_type"])
            for item in self.payload["relations"]
        }
        for edge in forbidden_new_edges:
            with self.subTest(edge=edge):
                self.assertNotIn(edge, actual_edges)

    def test_relation_ids_are_unique(self):
        ids = [item["id"] for item in self.payload["relations"]]
        self.assertEqual(len(ids), len(set(ids)))

    def test_object_ids_are_unique(self):
        ids = [item["id"] for item in self.payload["objects"]]
        self.assertEqual(len(ids), len(set(ids)))


if __name__ == "__main__":
    unittest.main()
