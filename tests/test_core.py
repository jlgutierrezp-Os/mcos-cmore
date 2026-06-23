import tempfile
import unittest

from mcos.core import (
    JsonlStore,
    MathObject,
    MathRelation,
    ValidationError,
    compare_math_objects,
    review_packet,
    validate_adapter_response,
    validate_math_object,
    validate_math_relation,
)


class CoreTests(unittest.TestCase):
    def test_valid_object(self):
        self.assertTrue(validate_math_object(MathObject("Group").to_dict()))

    def test_invalid_alpha(self):
        with self.assertRaises(ValidationError):
            validate_math_object(MathObject("Bad", alpha_confidence=2).to_dict())

    def test_valid_relation(self):
        self.assertTrue(validate_math_relation(MathRelation("Group", "Monoid", "specializes").to_dict()))

    def test_store(self):
        with tempfile.TemporaryDirectory() as d:
            store = JsonlStore(d)
            store.add_node(MathObject("Group").to_dict())
            self.assertEqual(len(store.nodes()), 1)

    def test_compare_review(self):
        response = compare_math_objects(MathObject("Group").to_dict(), MathObject("Group").to_dict())
        packet = review_packet(response)
        self.assertIn(response["status"], {"success", "partial"})
        self.assertIn(packet["required_decision"], {"accept", "revise"})

    def test_valid_empty_report_differences(self):
        self.assertTrue(validate_adapter_response({
            "request_id": "550e8400-e29b-41d4-a716-446655440000",
            "status": "success",
            "result": {"ok": True},
            "equivalence_report": {
                "checked": True,
                "comparison_scope": "minimal_equivalence",
                "differences": []
            }
        }))

    def test_invalid_report_missing_fields(self):
        with self.assertRaises(ValidationError):
            validate_adapter_response({
                "request_id": "550e8400-e29b-41d4-a716-446655440000",
                "status": "success",
                "result": {"ok": True},
                "equivalence_report": {"checked": True}
            })

    def test_invalid_report_severity(self):
        with self.assertRaises(ValidationError):
            validate_adapter_response({
                "request_id": "550e8400-e29b-41d4-a716-446655440000",
                "status": "partial",
                "result": {"ok": False},
                "equivalence_report": {
                    "checked": True,
                    "comparison_scope": "minimal_equivalence",
                    "differences": [{
                        "description": "Bad item",
                        "path": "/x",
                        "severity": "minor"
                    }]
                }
            })


if __name__ == "__main__":
    unittest.main()
