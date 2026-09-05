"""The 🏷 Labeling tab reads receipts honestly and reveals no item text."""
import json
import shutil
import tempfile
import unittest
from pathlib import Path

from live.autodraw import autodraw
from live.chat import chat_guard
from live.labeling import (
    P0_FILES, inspect, is_labeling_run_page, is_labeling_surface_page,
    labeling_chat_hold, labeling_hold_for_scene, render, studio_chat_page_url,
)
from live.term import TermMixin, labeling_tui_hold
from src import assets


class LabelingSurfaceTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.board = Path(self.tmp.name)
        self.page_dir = self.board / "S-Label-1-demo"
        self.page_dir.mkdir()
        self.page = self.page_dir / "S-Label-1-demo.md"
        self.page.write_text("# Demo\npage-type: labeling\n", encoding="utf-8")
        self.job = self.page_dir / "labeling"
        (self.board / "board.md").write_text(
            "# Demo Board\n\n## Pages\n\n### SL · Labeling\n"
            "S-Label-1-demo.md\n",
            encoding="utf-8",
        )
        self.file_q = "S-Label-1-demo/S-Label-1-demo.md"
        generated = self.board / "board" / "SL" / "S-Label-1-demo.html"
        generated.parent.mkdir(parents=True)
        generated.write_text(
            '<section class="slide" data-file="%s"></section>\n' % self.file_q,
            encoding="utf-8",
        )

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

    def test_contract_api_keeps_explicit_unconfirmed_meaning_at_p0(self):
        self.make_contract(
            "authority:\n  human_id: JL\n  mode: single_human_semantic_authority\n"
            "  creates_human_gold: true\n  meaning_confirmed: false\n"
        )
        state = inspect(self.page)
        self.assertEqual(state["phase_i"], 0)
        self.assertFalse(state["authority_hold"])
        self.assertFalse(state["meaning_receipt_valid"])
        self.assertIn("P0 Contract", state["next_action"])
        self.assertIn("human meaning confirmation", state["first_failed"])
        self.assertNotIn("G0 Contract", state["first_failed"])

    def test_bare_meaning_boolean_without_receipt_stays_at_p0(self):
        self.make_contract(
            "authority:\n  human_id: JL\n  mode: single_human_semantic_authority\n"
            "  creates_human_gold: true\n  meaning_confirmed: true\n"
        )
        state = inspect(self.page)
        self.assertEqual(state["phase_i"], 0)
        self.assertFalse(state["meaning_receipt_valid"])
        self.assertIn("P0 Contract", state["first_failed"])

    def test_confirmed_meaning_receipt_advances_to_first_round(self):
        self.make_contract(
            "authority:\n  human_id: JL\n  mode: single_human_semantic_authority\n"
            "  creates_human_gold: true\n  meaning_confirmed: true\n"
            "  meaning_receipt:\n"
            "    schema: subjective-label-meaning-confirmation/v1\n"
            "    status: confirmed\n"
            "    human_id: JL\n"
            "    confirmed_at: '2026-09-01'\n"
        )
        state = inspect(self.page)
        self.assertEqual(state["phase_i"], 1)
        self.assertTrue(state["meaning_receipt_valid"])
        self.assertIn("G1 Round close", state["first_failed"])
        self.assertIn("P1 Round", state["next_action"])

    def test_surface_never_renders_protected_or_item_text(self):
        self.make_contract()
        secret = "PRIVATE-ITEM-TEXT-MUST-NOT-RENDER"
        self.put("corpus/items.jsonl", json.dumps({"item_id": "sealed-7", "text": secret}))
        self.put("test/sealed/manifest.enc-or-protected", secret)
        body = render(
            self.page, "/demo/board.md", self.file_q,
            "/demo/board/SL/S-Label-1-demo.html",
            self.board,
        )
        self.assertNotIn(secret, body)
        self.assertNotIn("sealed-7", body)
        self.assertIn("Protected item text", body)
        self.assertIn('/demo/board/SL/S-Label-1-demo.html?pane=chat', body)
        self.assertNotIn("board.md?pane=chat", body)
        self.assertIn('title="Studio Page Chat"', body)
        self.assertIn('id=splitter', body)
        self.assertIn('Resize Labeling workspaces and Studio Chat', body)
        self.assertIn('labeling-workspace:/demo/board.md|S-Label-1-demo/S-Label-1-demo.md', body)
        self.assertIn('labeling-split:/demo/board.md|S-Label-1-demo/S-Label-1-demo.md', body)
        self.assertNotIn("Prefill safe status ask", body)
        for workspace in ("Workflow", "Data", "Guideline", "Human", "Quality"):
            self.assertIn(workspace, body)
        self.assertIn('aria-label="Labeling workspaces"', body)
        self.assertIn('data-workspace=workflow', body)
        self.assertIn('data-workspace=data', body)
        self.assertIn('data-workspace=guideline', body)
        self.assertIn('data-workspace=human', body)
        self.assertIn('data-workspace=quality', body)
        self.assertLess(body.index('id=spaces'), body.index('id=studio-chat'))
        self.assertEqual(body.count('title="Studio Page Chat"'), 1)

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

    def test_canonical_status_rehashes_the_real_job_before_reporting_frontier(self):
        repo = Path(__file__).resolve().parents[7]
        source = (repo / "examples-nlp/Project-Subjective-Label/diagram/01-label-runs-260807"
                  / "pages/S-Label-1-acibench-authority/labeling")
        shutil.copytree(source, self.job)
        state = inspect(self.page)
        self.assertIsNotNone(state["canonical_status"])
        self.assertFalse(state["canonical_status"]["meaning_receipt_valid"])
        self.assertFalse([row for row in state["gate_rows"] if row[0] == "G0"][0][4])

        items = self.job / "corpus" / "items.jsonl"
        items.write_bytes(items.read_bytes() + b'{"tampered":true}\n')
        tampered = inspect(self.page)
        self.assertIn("corpus items checksum mismatch", tampered["canonical_integrity_errors"])
        self.assertEqual(tampered["phase_i"], 0)
        self.assertIn("G0 Contract integrity", tampered["first_failed"])

    def test_old_field_test_layout_is_read_only_bridge_not_new_canonical_shape(self):
        old = self.job / "field-tests" / "FT_01" / "run"
        old.mkdir(parents=True)
        (old / "config.yaml").write_text("simulation_only: true\n", encoding="utf-8")
        state = inspect(self.page)
        self.assertEqual(state["root"], old)
        self.assertIn("migrate", state["location_note"])

    def test_labeling_hold_forces_server_side_read_only_chat(self):
        self.make_contract(
            "simulation_only: true\nauthority:\n  human_id: PROXY\n"
            "  mode: simulation_proxy_only\n  creates_human_gold: false\n"
        )
        self.put("rounds/round_01/checkpoint.json", json.dumps({"state": "closed"}))
        held, reason = labeling_chat_hold(self.page)
        self.assertTrue(held)
        self.assertIn("HOLD", reason)
        # A forged writable client request cannot turn the artifact-derived guard off.
        read_only, mode, guarded_reason = chat_guard(
            self.page, {"quality_check": False, "scope": "bypass"})
        self.assertTrue(read_only)
        self.assertEqual(mode, "scoped")
        self.assertEqual(guarded_reason, reason)
        body = render(
            self.page, "/demo/board.md", self.file_q,
            "/demo/board/SL/S-Label-1-demo.html",
            self.board,
        )
        self.assertIn("labeling_hold=1", body)
        self.assertIn("HOLD", body)

    def test_labeling_hold_blocks_tui_and_draw_server_side(self):
        self.make_contract(
            "simulation_only: true\nauthority:\n  human_id: PROXY\n"
            "  mode: simulation_proxy_only\n  creates_human_gold: false\n"
        )
        self.put("rounds/round_01/checkpoint.json", json.dumps({"state": "closed"}))
        reason = labeling_tui_hold(self.page)
        self.assertIn("HOLD", reason)
        for result in (
            TermMixin.term_type(object(), self.page, {"text": "run anything"}),
            TermMixin.local_cmd(object(), self.page, {}),
            TermMixin.terminal(object(), self.page, {}, self.board),
        ):
            self.assertIsNone(result[0])
            self.assertIn("TUI is read-only", result[1])

        scene = "S-Label-1-demo/draw/S-Label-1.excalidraw"
        held, draw_reason = labeling_hold_for_scene(self.board, scene)
        self.assertTrue(held)
        self.assertEqual(draw_reason, reason)
        draw_result = autodraw(self.board, {"scene": scene, "prompt": "draw it"})
        self.assertFalse(draw_result["ok"])
        self.assertIn("Draw generation is read-only", draw_result["err"])
        self.assertFalse((self.board / scene).exists())

    def test_studio_chat_requires_the_matching_generated_page(self):
        good = studio_chat_page_url(
            "/demo/board.md", self.file_q,
            "/demo/board/SL/S-Label-1-demo.html",
            self.board,
        )
        self.assertEqual(good, "/demo/board/SL/S-Label-1-demo.html")
        self.assertEqual(studio_chat_page_url(
            "/demo/board.md", self.file_q, "", self.board), "")
        self.assertEqual(studio_chat_page_url(
            "/demo/board.md", self.file_q,
            "/demo/board/SL/S-Label-2-demo.html",
            self.board,
        ), "")
        self.assertEqual(studio_chat_page_url(
            "/demo/board.md", self.file_q,
            "/other/board/SL/S-Label-1-demo.html",
            self.board,
        ), "")
        self.assertEqual(studio_chat_page_url(
            "/demo/board.md", self.file_q,
            "/demo/board/WRONG/S-Label-1-demo.html",
            self.board,
        ), "")

    def test_non_hold_labeling_page_does_not_receive_hold_reason(self):
        self.make_contract("authority:\n  human_id: JL\n  mode: real-human\n  creates_human_gold: true\n")
        held, reason = labeling_chat_hold(self.page)
        self.assertFalse(held)
        self.assertEqual(reason, "")

    def test_every_real_page_has_the_surface_but_only_run_pages_have_the_type(self):
        dash = self.page_dir / "S-Label-Dash.md"
        dash.write_text("# Dash\npage-type: labeling\n", encoding="utf-8")
        ordinary = self.page_dir / "SM00-abstract.md"
        ordinary.write_text("# Abstract\npage-type: section\n", encoding="utf-8")
        self.assertFalse(is_labeling_run_page(dash))
        self.assertTrue(is_labeling_run_page(self.page))
        self.assertFalse(is_labeling_run_page(ordinary))
        self.assertFalse(is_labeling_surface_page(dash))
        self.assertTrue(is_labeling_surface_page(self.page))
        self.assertTrue(is_labeling_surface_page(ordinary))
        self.assertEqual(labeling_chat_hold(dash), (False, ""))
        self.assertEqual(labeling_chat_hold(ordinary), (False, ""))

    def test_flat_board_source_resolves_folded_page_task_lane(self):
        board = Path(self.tmp.name) / "board"
        (board / "SL-labeling-runs").mkdir(parents=True)
        (board / "board.md").write_text("# Board\n", encoding="utf-8")
        flat = board / "SL-labeling-runs" / "S-Label-1-demo.md"
        flat.write_text("# Demo\npage-type: labeling\n", encoding="utf-8")
        folded = board / "pages" / flat.stem
        folded.mkdir(parents=True)
        (folded / flat.name).write_text("# Folded Demo\npage-type: labeling\n", encoding="utf-8")
        old = folded / "labeling" / "field-tests" / "FT_01" / "run"
        for rel in P0_FILES:
            target = old / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(
                ("simulation_only: true\n" if rel == "config.yaml" else "{}\n"),
                encoding="utf-8",
            )
        state = inspect(flat)
        self.assertEqual(state["root"], old)
        self.assertIn("page-folder bridge", state["location_note"])
        self.assertIn("legacy nested field-test", state["location_note"])
        read_only, mode, reason = chat_guard(
            flat, {"quality_check": False, "scope": "bypass"})
        self.assertTrue(read_only)
        self.assertEqual(mode, "scoped")
        self.assertIn("HOLD", reason)


class LabelingRegistrationTest(unittest.TestCase):
    def test_registry_is_a_right_pane_plugin_and_has_no_retired_commands(self):
        script = (Path(__file__).resolve().parents[1] / "assets" / "js" /
                  "10-drawer" / "60-plugin-labeling.js").read_text(encoding="utf-8")
        self.assertIn("menu: 'plugin'", script)
        self.assertIn("tab: { url: url, write: write }", script)
        self.assertIn("function isSurfacePage(page)", script)
        self.assertNotIn("type === 'labeling'", script)
        self.assertIn("S-Label-Dash", script)
        self.assertIn("pageURL()", script)
        self.assertIn("page: pageURL()", script)
        self.assertIn("Studio Chat always below", script)
        for retired in ("/label-init", "/label-round", "/label-evaluate", "/label-complete"):
            self.assertNotIn(retired, script)

    def test_assembled_browser_asset_contains_only_the_new_labeling_plugin(self):
        built = assets.js()
        self.assertIn("id: 'labeling'", built)
        self.assertIn("menu: 'plugin'", built)
        self.assertIn("S-Label-Dash", built)
        for retired in ("/sl-init", "/sl-round", "/sl-evaluate", "/sl-complete"):
            self.assertNotIn(retired, built)


if __name__ == "__main__":
    unittest.main()
