"""Validate relationships in the published resume example, beyond YAML syntax."""
import re
import unittest
from pathlib import Path
import yaml


class DefinitionExampleTest(unittest.TestCase):
    def test_managed_inventory_and_frontier_resolve_in_frozen_definition(self):
        skills = next(p for p in Path(__file__).resolve().parents if p.name == "skills")
        text = (skills / "2_theme/insight/haipipe-insight-workflow/ref/run-workflow.md").read_text()
        records = [yaml.safe_load(block) for block in re.findall(r"```yaml\n(.*?)\n```", text, re.S)]
        definition = next(r for r in records if r.get("schema") == "haipipe.insight-definition/v1")
        runtime = next(r for r in records if r.get("schema") == "haipipe.workflow-runtime/v1")
        specs = {r["id"]: r for r in definition["run_specs"]}
        runs = {r["run_id"]: r for r in runtime["runs"]}
        self.assertEqual(len(runs), len(runtime["runs"]))
        for row in runtime["runs"]:
            if row["participation"] == "reused":
                # run-workflow.md § runtime: a reused Result may name the Spec it
                # satisfies, but gets no new Ticket allocation or frontier entry.
                if "run_spec_id" in row:
                    spec = specs[row["run_spec_id"]]
                    for key in ("owner", "run_type"):
                        self.assertEqual(spec[key], row[key], key)
                    self.assertNotIn(row["run_spec_id"],
                                     [entry["run_spec_id"] for entry in runtime["frontier"]])
                self.assertEqual("complete", row["status"])
                continue
            spec = specs[row["run_spec_id"]]
            for key in ("owner", "run_type", "target"):
                self.assertEqual(spec[key], row[key], key)
            # a runtime row depends on native Run ids; each resolves to the reused Run
            # whose Spec the frozen definition names, and its result path is that Spec's RESULT_DIR
            for dependency in row["depends_on"]:
                source = runs[dependency]
                self.assertEqual("reused", source["participation"])
                self.assertIn(source["run_spec_id"], spec["depends_on"])
                self.assertEqual(source["result"], specs[source["run_spec_id"]]["env"]["RESULT_DIR"])
        # Inputs are named by path and version, never by content hash (JL 260928).
        for spec in specs.values():
            for ref in spec.get("inputs", []):
                self.assertFalse({"hash", "sha256"} & set(ref), ref)
                self.assertEqual({"path", "version"}, set(ref), ref)
        for entry in runtime["frontier"]:
            self.assertEqual(specs[entry["run_spec_id"]]["target"], entry["target"])
