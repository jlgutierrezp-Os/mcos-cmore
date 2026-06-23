import tempfile
import unittest

from mcos.core import (
    JsonlStore,
    MathObject,
    MathRelation,
    ValidationError,
    compare_math_objects,
    review_packet,
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


if __name__ == "__main__":
    unittest.main()
