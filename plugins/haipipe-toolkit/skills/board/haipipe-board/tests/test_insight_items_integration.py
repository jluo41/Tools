"""Insight instance identities and item tables through the real Board engine."""
import importlib.util
from pathlib import Path
import sys
import tempfile
import unittest

from src import item_table as it
from src.insight_instances import contract, render_items
from src.page_question import render_outline
from live.runs import local_runs, render as render_runs

SCRIPTS = Path(__file__).resolve().parents[3] / "task/page-types/haipipe-page-insight/scripts"
sys.path.insert(0, str(SCRIPTS))
from test_insight_items import fixture, write


class InsightIntegrationTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.a, self.exec_a = fixture(self.root)
        self.b, _ = fixture(self.root, "patient-b")
        self.page = self.a / "I01-topic.md"
        self.page.write_text("# Topic\npage-type: insight\ninsight-layout: items-v1\n")
        it.run_registry.cache_clear()

    def tearDown(self):
        it.run_registry.cache_clear()
        self.temp.cleanup()

    def test_two_patients_have_separately_registered_results(self):
        registry = it.run_registry(str(self.root))
        a = "study/patient-a#r01_description@v001"
        b = "study/patient-b#r01_description@v001"
        self.assertEqual("complete", registry[a]["status"])
        self.assertEqual("complete", registry[b]["status"])
        self.assertNotEqual(registry[a]["result"], registry[b]["result"])
        self.assertEqual(a, it.compact_global_run(a))
        self.assertEqual(a, it.readable_global_run(a))
        self.assertEqual((True, 1), it._valid_supporting(f"Insight · reuse · {a}"))
        self.assertTrue(it._registered_supports(f"Insight · reuse · {a}", registry))

    def test_unversioned_instance_reference_is_rejected(self):
        self.assertEqual("", it.compact_global_run("study/patient-a#r01_description"))
        self.assertEqual((False, 1), it._valid_supporting("Insight · reuse · r01_description"))

    def test_bad_source_hash_prevents_ready_registry_result(self):
        (self.a / "outline/evidence/materials/snapshot-01.yaml").write_text("changed: true\n")
        registry = it.run_registry(str(self.root))
        self.assertEqual("rerun", registry["study/patient-a#r01_description@v001"]["status"])
        self.assertEqual("complete", registry["study/patient-b#r01_description@v001"]["status"])

    def test_real_outline_renders_item_table_without_inventing_run_for_open_item(self):
        html = render_outline(self.page, "insight")
        self.assertIn("Insight item table", html)
        self.assertIn("r02_temporal", html)
        self.assertIn("planned", html)
        self.assertIn("study/patient-a#r01_description@v001", html)
        self.assertNotIn("patient-b", html)

    def test_table_escapes_data_text(self):
        path = self.a / "workflow/insight.yaml"
        manifest = contract().read_yaml(path)
        manifest["items"][1]["question"] = "<script>alert(1)</script>"
        write(path, manifest)
        html = render_items(self.page)
        self.assertNotIn("<script>", html)
        self.assertIn("&lt;script&gt;", html)

    def test_runs_panel_projects_versions_but_not_unallocated_items(self):
        write(self.exec_a.parent / "v002/runtime.yaml", {
            "schema": "haipipe.insight-runtime/v1", "execution": "study/patient-a#r01_description@v002",
            "family": "insight", "operation": "item", "status": "planned", "checkpoints": {},
            "attempts": [{"attempt": 1, "status": "planned"}]})
        rows = local_runs(self.page)
        self.assertEqual(2, len(rows))
        by_id = {row["global_id"]: row for row in rows}
        self.assertEqual("Done", by_id["study/patient-a#r01_description@v001"]["status"])
        self.assertEqual("Ready", by_id["study/patient-a#r01_description@v002"]["status"])
        self.assertNotIn("r02_temporal", str(rows))
        html = render_runs(self.page, "", "")
        self.assertIn("@v001", html)
        self.assertIn("@v002", html)


if __name__ == "__main__":
    unittest.main()
