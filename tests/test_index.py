import tempfile
import unittest

from mcos.core import JsonlStore, MathObject, MathRelation
from mcos.index import (
    GraphIndexError,
    find_edges,
    find_equivalent,
    get_node,
    get_node_by_id,
    get_node_by_name,
    list_dependencies,
    list_dependents,
    load_graph_index,
    summarize_index,
)


class GraphIndexTests(unittest.TestCase):
    def _object(self, name, node_id, dependencies=None):
        obj = MathObject(name).to_dict()
        obj["id"] = node_id
        obj["dependencies"] = dependencies or []
        return obj

    def _relation(self, source, target, relation_type, relation_id):
        rel = MathRelation(source, target, relation_type).to_dict()
        rel["id"] = relation_id
        return rel

    def _build_index(self, data_dir):
        store = JsonlStore(data_dir)
        group = self._object("Group", "550e8400-e29b-41d4-a716-446655440101", ["Monoid"])
        monoid = self._object("Monoid", "550e8400-e29b-41d4-a716-446655440102")
        structure = self._object("Algebraic Structure", "550e8400-e29b-41d4-a716-446655440103")
        group_like = self._object("GroupLike", "550e8400-e29b-41d4-a716-446655440104")
        store.add_node(group)
        store.add_node(monoid)
        store.add_node(structure)
        store.add_node(group_like)
        store.add_edge(self._relation("Group", "Algebraic Structure", "depends_on", "550e8400-e29b-41d4-a716-446655440201"))
        store.add_edge(self._relation("GroupLike", "Group", "depends_on", "550e8400-e29b-41d4-a716-446655440202"))
        store.add_edge(self._relation("Group", "GroupLike", "equivalent_to", "550e8400-e29b-41d4-a716-446655440203"))
        return load_graph_index(data_dir)

    def test_load_graph_index_summary(self):
        with tempfile.TemporaryDirectory() as d:
            index = self._build_index(d)
            summary = summarize_index(index)
            self.assertEqual(summary["status"], "passed")
            self.assertEqual(summary["nodes_total"], 4)
            self.assertEqual(summary["edges_total"], 3)
            self.assertTrue(summary["local_only"])

    def test_get_node_by_id_and_name(self):
        with tempfile.TemporaryDirectory() as d:
            index = self._build_index(d)
            by_name = get_node_by_name(index, "Group")
            by_id = get_node_by_id(index, by_name["id"])
            self.assertEqual(by_name["name"], "Group")
            self.assertEqual(by_id["name"], "Group")
            self.assertEqual(get_node(index, "Group")["id"], by_name["id"])
            self.assertEqual(get_node(index, by_name["id"])["name"], "Group")

    def test_missing_node_raises(self):
        with tempfile.TemporaryDirectory() as d:
            index = self._build_index(d)
            with self.assertRaises(GraphIndexError):
                get_node(index, "Missing")

    def test_dependency_lookup_combines_node_and_edges(self):
        with tempfile.TemporaryDirectory() as d:
            index = self._build_index(d)
            self.assertEqual(list_dependencies(index, "Group"), ["Monoid", "Algebraic Structure"])

    def test_dependent_lookup_combines_node_and_edges(self):
        with tempfile.TemporaryDirectory() as d:
            index = self._build_index(d)
            self.assertEqual(list_dependents(index, "Group"), ["GroupLike"])
            self.assertEqual(list_dependents(index, "Monoid"), ["Group"])

    def test_find_edges_filters(self):
        with tempfile.TemporaryDirectory() as d:
            index = self._build_index(d)
            self.assertEqual(len(find_edges(index, source="Group")), 2)
            self.assertEqual(len(find_edges(index, source="Group", relation_type="depends_on")), 1)
            self.assertEqual(find_edges(index, target="Group", relation_type="depends_on")[0]["source"], "GroupLike")

    def test_find_equivalent(self):
        with tempfile.TemporaryDirectory() as d:
            index = self._build_index(d)
            self.assertEqual(find_equivalent(index, "Group"), ["GroupLike"])
            self.assertEqual(find_equivalent(index, "GroupLike"), ["Group"])


if __name__ == "__main__":
    unittest.main()
