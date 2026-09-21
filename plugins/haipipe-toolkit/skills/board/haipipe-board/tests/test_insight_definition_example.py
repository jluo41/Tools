"""Validate relationships in the published resume example, beyond YAML syntax."""
import re
import unittest
from pathlib import Path
import yaml


class DefinitionExampleTest(unittest.TestCase):
    def test_managed_inventory_and_frontier_resolve_in_frozen_definition(self):
        skills = Path(__file__).resolve().parents[3]
        text = (skills / "insight/haipipe-insight-workflow/ref/run-workflow.md").read_text()
        records = [yaml.safe_load(block) for block in re.findall(r"```yaml\n(.*?)\n```", text, re.S)]
        definition = next(r for r in records if r.get("schema") == "haipipe.insight-definition/v1")
        runtime = next(r for r in records if r.get("schema") == "haipipe.workflow-runtime/v1")
        specs = {r["id"]: r for r in definition["run_specs"]}
        runs = {r["run_id"]: r for r in runtime["runs"]}
        self.assertEqual(len(runs), len(runtime["runs"]))
        for row in runtime["runs"]:
            if row["participation"] == "reused":
                self.assertNotIn("run_spec_id", row)
                self.assertEqual("complete", row["status"])
                continue
            spec = specs[row["run_spec_id"]]
            for key in ("owner", "run_type", "target", "inputs", "depends_on"):
                self.assertEqual(spec[key], row[key], key)
            for dependency in row["depends_on"]:
                source = runs[dependency]
                self.assertEqual("reused", source["participation"])
                self.assertIn({"path": source["result"], "hash": source["result_hash"]}, row["inputs"])
        for entry in runtime["frontier"]:
            self.assertEqual(specs[entry["run_spec_id"]]["target"], entry["target"])
