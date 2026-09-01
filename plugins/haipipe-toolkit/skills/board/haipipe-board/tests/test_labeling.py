"""The 🏷 Labeling tab reads receipts honestly and reveals no item text."""
import json
import tempfile
import unittest
from pathlib import Path

from live.labeling import P0_FILES, inspect, render


class LabelingSurfaceTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.page_dir = Path(self.tmp.name) / "S-Label-1-demo"
        self.page_dir.mkdir()
        self.page = self.page_dir / "S-Label-1-demo.md"
        self.page.write_text("# Demo\npage-type: labeling\n", encoding="utf-8")
        self.job = self.page_dir / "labeling"

    def tearDown(self):
        self.tmp.cleanup()

    def put(self, rel, text="x\n"):
        target = self.job / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8")
        return target

    def make_contract(self, config="schema_version: subjective-label/v2\n"):
        for rel in P0_FILES:
            self.put(rel, config if rel == "config.yaml" else "{}\n")

    def test_missing_lane_reports_contract_without_creating_it(self):
        state = inspect(self.page)
        self.assertFalse(self.job.exists())
        self.assertEqual(state["phase_i"], 0)
        self.assertIn("P0 Contract", state["next_action"])
        self.assertIn("G0", state["first_failed"])

    def test_simulation_checkpoint_holds_before_freeze(self):
        self.make_contract(
            "simulation_only: true\nauthority:\n  human_id: PROXY\n"
            "  mode: simulation_proxy_only\n  creates_human_gold: false\n"
        )
        checkpoint = {
            "state": "closed-simulation",
            "gates": {name: {"pass": name == "risk"}
                      for name in ("quality", "stability", "coverage", "risk")},
            "human_stop_signoff": False,
        }
        self.put("rounds/round_01/checkpoint.json", json.dumps(checkpoint))
        state = inspect(self.page)
        self.assertEqual(state["phase_i"], 1)
        self.assertTrue(state["authority_hold"])
        self.assertIn("HOLD", state["next_action"])
        self.assertIn("owner:", state["next_action"])
        self.assertIn("preserve: rounds/round_01/checkpoint.json", state["next_action"])
        self.assertIn("G2", state["first_failed"])
        self.assertLess(state["first_failed"].index("quality"),
                        state["first_failed"].index("human STOP"))
        self.assertLess(state["first_failed"].index("human STOP"),
                        state["first_failed"].index("simulation/proxy"))
        self.assertEqual(state["human_id"], "PROXY")

    def test_complete_file_set_without_identified_human_is_hold(self):
        self.make_contract()
        state = inspect(self.page)
        self.assertTrue(state["authority_hold"])
        self.assertIn("owner: one identified real human", state["next_action"])
        self.assertIn("does not name one identified human", state["first_failed"])
        self.assertIn("G0", state["first_failed"])

    def test_real_contract_without_checkpoint_routes_to_first_round(self):
        self.make_contract("authority:\n  human_id: JL\n  mode: real-human\n  creates_human_gold: true\n")
        state = inspect(self.page)
        self.assertIn("G1 Round close", state["first_failed"])
        self.assertIn("P1 Round", state["next_action"])
        self.assertNotIn("Freeze", state["next_action"])

    def test_surface_never_renders_protected_or_item_text(self):
        self.make_contract()
        secret = "PRIVATE-ITEM-TEXT-MUST-NOT-RENDER"
        self.put("corpus/items.jsonl", json.dumps({"item_id": "sealed-7", "text": secret}))
        self.put("test/sealed/manifest.enc-or-protected", secret)
        body = render(self.page, "/demo/board/SL/S-Label-1-demo.html",
                      "SL/S-Label-1-demo/S-Label-1-demo.md")
        self.assertNotIn(secret, body)
        self.assertNotIn("sealed-7", body)
        self.assertIn("Protected item text", body)
        self.assertIn("pane=chat", body)

    def test_artifact_chain_moves_observed_frontier_without_certifying_g6(self):
        self.make_contract("authority:\n  human_id: JL\n  mode: real-human\n  creates_human_gold: true\n")
        self.put("rounds/round_01/checkpoint.json", json.dumps({
            "state": "closed",
            "gates": {name: {"pass": True}
                      for name in ("quality", "stability", "coverage", "risk")},
            "human_stop_signoff": True,
        }))
        self.put("handoff/label-v1.yaml", "status: valid\n")
        self.put("evaluation/registry.yaml")
        self.put("test/final/lock.json", "{}\n")
        self.put("evaluation/summary.md")
        self.put("production/run_01/run_report.md")
        self.put("audit/final_01/receipt.json", "{}\n")
        self.put("corpus/final/D_star.jsonl")
        self.put("corpus/final/manifest.yaml")
        state = inspect(self.page)
        self.assertEqual(state["phase_i"], 5)
        self.assertIn("COMPLETE candidate", state["next_action"])
        self.assertIn("None observed", state["first_failed"])
        g6 = [row for row in state["gate_rows"] if row[0] == "G6"][0]
        self.assertFalse(g6[4], "the read-only surface must not certify G6")

    def test_old_field_test_layout_is_read_only_bridge_not_new_canonical_shape(self):
        old = self.job / "field-tests" / "FT_01" / "run"
        old.mkdir(parents=True)
        (old / "config.yaml").write_text("simulation_only: true\n", encoding="utf-8")
        state = inspect(self.page)
        self.assertEqual(state["root"], old)
        self.assertIn("migrate", state["location_note"])


class LabelingRegistrationTest(unittest.TestCase):
    def test_registry_is_a_right_pane_plugin_and_has_no_retired_commands(self):
        script = (Path(__file__).resolve().parents[1] / "assets" / "js" /
                  "10-drawer" / "60-plugin-labeling.js").read_text(encoding="utf-8")
        self.assertIn("menu: 'plugin'", script)
        self.assertIn("tab: { url: url, write: write }", script)
        self.assertIn("type === 'labeling'", script)
        self.assertIn("S-Label-Dash", script)
        for retired in ("/label-init", "/label-round", "/label-evaluate", "/label-complete"):
            self.assertNotIn(retired, script)


if __name__ == "__main__":
    unittest.main()
