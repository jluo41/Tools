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
        self.assertIn("items in a round: in Labeling → Rounds once shown to you", body)
        self.assertIn('/demo/board/SL/S-Label-1-demo.html?pane=chat', body)
        self.assertNotIn("board.md?pane=chat", body)
        self.assertIn("Open Studio Chat", body)
        self.assertNotIn('id=studio-chat', body)
        self.assertIn('<meta name="viewport"', body)
        self.assertIn('aria-label="Labeling Spaces"', body)
        self.assertIn('role=tabpanel', body)
        # a Workflow map returned 260918 as a view inside the Run Space (like the Paper plugin), never its own Space
        self.assertNotIn("Workflow Space", body)
        for retired in ("Human Space", "Data &amp; Label", "Guideline Space",
                        "Run Spec × Space", "DICES", "Q_overall", "safety_gold"):
            self.assertNotIn(retired, body)
        order = [body.index('data-space=%s>' % sid) for sid in
                 ("data", "labeling", "quality", "run", "delivery")]
        self.assertEqual(order, sorted(order))
        for view in ("Contract", "Schema", "Embedding", "Discussion", "Label", "Rounds", "Guideline", "Test",
                     "Evaluation", "Audit", "Runs", "Phases", "Handoff", "Final labels"):
            self.assertIn(">%s</button>" % view, body)
        self.assertIn("Current discussion", body)
        self.assertIn("One discussion may use several examples", body)
        self.assertIn("rlNN_discussion-calibration", body)
        self.assertNotIn('<iframe', body)

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


class LabelingWriteDoorTest(unittest.TestCase):
    """POST /_board/labeling/act: the engine decides; the door refuses early and plainly."""

    def setUp(self):
        base = LabelingSurfaceTest("test_missing_lane_reports_contract_without_creating_it")
        base.setUp()
        self.base = base

    def tearDown(self):
        self.base.tearDown()

    def handler(self, origin="", host="127.0.0.1:5601"):
        from live.labeling import LabelingMixin

        class Fake(LabelingMixin):
            pass

        fake = Fake()
        fake.headers = {"Origin": origin, "Host": host} if origin else {"Host": host}
        board = self.base.board

        def target(p):
            return (board / p["file"], board) if p.get("file") else (None, "no file")

        fake.target = target
        return fake

    def payload(self, **extra):
        body = {"path": "/demo/board.md", "file": self.base.file_q,
                "page": "/demo/board/SL/S-Label-1-demo.html",
                "action": "release_round", "human_id": "JL", "attest": True, "session_id": "s"}
        body.update(extra)
        return body

    def test_cross_origin_write_is_refused(self):
        code, res = self.handler(origin="http://evil.example").labeling_act(self.payload())
        self.assertEqual(code, 403)
        self.assertFalse(res["ok"])

    def test_write_without_attestation_is_refused(self):
        code, res = self.handler().labeling_act(self.payload(attest=False))
        self.assertEqual(code, 400)
        self.assertIn("attestation", res["err"])

    def test_meaning_confirmation_requires_board_origin(self):
        code, res = self.handler().labeling_act(self.payload(action="confirm_meaning"))
        self.assertEqual(code, 403)
        self.assertIn("Board origin", res["err"])

    def test_page_without_canonical_job_is_refused(self):
        self.base.make_contract()
        code, res = self.handler().labeling_act(self.payload())
        self.assertEqual(code, 409)
        self.assertIn("no canonical labeling job", res["err"])

    def test_embedding_build_accepts_only_catalog_models_and_checks_the_job(self):
        self.base.make_contract()
        self.base.put("gates/p0-contract/receipt.json", "{}")
        code, res = self.handler().labeling_act(self.payload(action="build_embedding", model="org/anything"))
        self.assertEqual(code, 409)
        self.assertIn("not in the embedding catalog", res["err"])
        code, res = self.handler().labeling_act(self.payload(action="build_embedding", model="BAAI/bge-m3"))
        self.assertEqual(code, 409)  # this fixture names no human, so it is HOLD and no process starts
        self.assertIn("read-only", res["err"])
        code, res = self.handler().labeling_act(self.payload(action="embedding_status"))
        self.assertEqual(code, 200)
        states = {m["id"]: m["state"] for m in res["result"]["models"]}
        self.assertEqual(states["Qwen/Qwen3-Embedding-0.6B"], "none")
        code, res = self.handler().labeling_act(self.payload(action="embedding_item", version="nope", item_id="1"))
        self.assertEqual(code, 409)
        self.assertIn("no embedding named", res["err"])
        code, res = self.handler().labeling_act(self.payload(action="group_examples", version="nope", group_index=0))
        self.assertEqual(code, 409)
        self.assertIn("no embedding named", res["err"])
        code, res = self.handler().labeling_act(self.payload(action="embedding_item_text", version="nope", item_id="1"))
        self.assertEqual(code, 409)
        self.assertIn("no embedding named", res["err"])

    def test_unknown_page_url_is_refused(self):
        code, res = self.handler().labeling_act(self.payload(page="/demo/board/SL/other.html"))
        self.assertEqual(code, 400)

    def test_render_reads_each_jobs_own_config(self):
        self.base.make_contract(
            "schema_version: subjective-label/v2\nconstruct:\n  name: politeness\n"
            "  question: How polite is the reply?\nlabels:\n  values: [high, low, none]\n"
            "  meanings:\n    high: very polite\nauthority:\n  human_id: JL\n"
            "  mode: single_human_semantic_authority\n  creates_human_gold: true\n")
        self.base.put("corpus/manifest.json", '{"n_items": 12, "n_sealed": 2, "n_eligible": 10}')
        body = render(self.base.page, "/demo/board.md", self.base.file_q,
                      "/demo/board/SL/S-Label-1-demo.html", self.base.board)
        self.assertIn("How polite is the reply?", body)
        self.assertIn("very polite", body)
        self.assertIn(">10<", body)
        for other in ("DICES", "Q_overall", "safety_gold", "unsafe"):
            self.assertNotIn(other, body)


class LabelingEmbeddingViewTest(unittest.TestCase):
    """Data Space · Embedding: the recipe from item text to vector, the map, the groups."""

    def setUp(self):
        base = LabelingSurfaceTest("test_missing_lane_reports_contract_without_creating_it")
        base.setUp()
        base.make_contract()
        self.base = base

    def tearDown(self):
        self.base.tearDown()

    def body(self):
        return render(self.base.page, "/demo/board.md", self.base.file_q,
                      "/demo/board/SL/S-Label-1-demo.html", self.base.board)

    def test_without_an_embedding_the_view_says_how_to_build_one(self):
        body = self.body()
        self.assertIn("No embedding yet.", body)
        self.assertNotIn("embedding_build.py build --job-root", body)  # the page runs builds by the button only
        self.assertIn("Nothing runs until you press", body)
        self.assertIn('<option value="BAAI/bge-m3"', body)
        self.assertIn("<div class=runbox data-emb-formbox><h3>Run a new embedding", body)
        for control in ("data-emb-input=reply", "data-emb-input=context", "data-emb-field=instruction",
                        "data-emb-field=groups", "data-emb-map=pca", "data-emb-field=seed", "data-emb-run"):
            self.assertIn(control, body)

    def test_contract_cards_each_take_the_full_row(self):
        body = self.body()
        self.assertNotIn("class=grid", body)

    def test_built_embedding_shows_recipe_example_map_and_groups(self):
        manifest = {
            "schema": "subjective-label-embedding/v1", "run": "rl02_embedding-build_tiny",
            "version": "tiny", "created_at": "2026-09-16T12:00:00-04:00",
            "model": {"id": "org/tiny", "device": "cpu", "dim": 4},
            "preprocessing": {"text_field": "text", "context_field": "context_prev", "normalize": "l2"},
            "encoder": {"steps": [{"module": "Transformer", "max_tokens": 256},
                                  {"module": "Pooling", "mode": "mean"}, {"module": "Normalize"}],
                        "max_tokens": 256, "items_cut": 1, "longest_tokens": 300},
            "example": {"input": "made-up sentence", "word_pieces": ["[CLS]", "made", "[SEP]"],
                        "vector_first": [0.1, -0.2], "dim": 4, "length": 1.0},
            "population": {"eligible_embedded": 2, "sealed_excluded": 1},
            "map": {"method": "tsne", "seed": 0}, "files": [{"path": "vectors.npy", "sha256": "x"}],
        }
        self.base.put("cache/embeddings/tiny/manifest.json", json.dumps(manifest))
        self.base.put("cache/embeddings/tiny/map.jsonl",
                      '{"item_id": "a1", "x": 0.1, "y": 0.2, "group": 0}\n'
                      '{"item_id": "a2", "x": 0.9, "y": 0.8, "group": 1}\n')
        self.base.put("cache/embeddings/tiny/map3d.jsonl",
                      '{"item_id": "a1", "x": 0.1, "y": 0.2, "z": -0.5}\n'
                      '{"item_id": "a2", "x": -0.9, "y": 0.8, "z": 0.4}\n')
        self.base.put("cache/embeddings/tiny/groups.json", json.dumps({
            "k": 2, "silhouette_by_k": {"2": 0.1},
            "groups": [{"group": 0, "size": 1, "keywords": ["weapons"]},
                       {"group": 1, "size": 1, "keywords": ["money"]}]}))
        body = self.body()
        for text in ("From item to vector", "The model reads at most 256", "1 of 2 items are longer",
                     "Average all word-piece vectors", "Worked example", "made-up sentence",
                     "rl02_embedding-build_tiny", ">G2</span>", "weapons", "Your labels",
                     "Embedding model", 'data-emb-show="tiny"', '<option value="Qwen/Qwen3-Embedding-0.6B" data-instruct="1" selected',
                     "data-map-dim=3d", "data-spin", "canvas class=map3d", '"points3d": [["a1", 0.1, 0.2, -0.5, 0]',
                     'data-item="a1"', 'data-group-pick="1"', "class=embdata",
                     "Click a dot to see its group", 'data-map-show=round', 'data-zoom=in',
                     'data-ex-group="1"', "Show typical items", "exposure/group_examples.jsonl",
                     "--started-by &lt;your name&gt;", "from the terminal; no person&#x27;s request is recorded"):
            self.assertIn(text, body)
        self.assertEqual(body.count('<circle class="pt'), 2)
        self.assertNotIn("No embedding yet.", body)


class LabelingRoundDrawTest(unittest.TestCase):
    """Labeling → Rounds shows how the round was drawn and which items it picked."""

    def setUp(self):
        base = LabelingSurfaceTest("test_missing_lane_reports_contract_without_creating_it")
        base.setUp()
        base.make_contract(
            "schema_version: subjective-label/v2\nconstruct:\n  name: unsafe_response\n"
            "labels:\n  values: [high, low, none]\nauthority:\n  human_id: JL\n"
            "  mode: single_human_semantic_authority\n  creates_human_gold: true\n"
            "  meaning_confirmed: true\n")
        base.put("rounds/round_01/manifest.yaml",
                 "round_id: round_01\npolicy_version: G_00\ndevelopment_pool_size: 300\n"
                 "draw:\n  method: uniform-random\n  n: 2\n  seed: 42\n")
        base.put("rounds/round_01/card.md",
                 "# round_01 · card\n\nstate: released\nreleased_by: JL\n"
                 "released_at: 2026-09-16T15:21:42-04:00\n")
        base.put("rounds/round_01/human_batch.jsonl",
                 '{"item_id": "157", "order": 0, "selection_probability": 0.0667}\n'
                 '{"item_id": "11", "order": 1, "selection_probability": 0.0667}\n')
        self.base = base

    def tearDown(self):
        self.base.tearDown()

    def view(self, embedding=None):
        from live.labeling import _rounds_view
        summary = {"round_id": "round_01", "state": "judging", "finals": 1, "batch_size": 2,
                   "prepare_run": "rl03_round-prepare_round-01",
                   "calibration_run": "rl04_human-calibration_round-01"}
        return _rounds_view({"root": self.base.job, "cal": {"rounds": [summary]}, "embedding": embedding})

    def test_rounds_view_lists_the_drawn_items_without_their_text(self):
        body = self.view()
        for text in ("The items this round drew · 2", "item 157", "item 11", ">#1<", ">#2<",
                     "uniform-random draw, from the 300 items to label, seed 42",
                     "6.7% (1 in 15)", "JL, 16 Sep 2026, 3:21 pm", "waiting",
                     "Text appears once an item has been shown to you",
                     "<th>Text</th><th>Group</th><th>State</th><th>Feedback</th>", "not opened yet"):
            self.assertIn(text, body)
        self.assertIn("Build an embedding in Data → Embedding", body)
        self.assertNotIn("PRIVATE", body)

    def test_a_built_embedding_tags_each_drawn_item_with_its_group(self):
        embedding = {"builds": [{"manifest": {"version": "tiny", "model": {"id": "org/tiny"}},
                                 "map": [{"item_id": "157", "group": 0}, {"item_id": "11", "group": 1},
                                         {"item_id": "99", "group": 2}]}]}
        body = self.view(embedding)
        self.assertIn(">G1</span>", body)
        self.assertIn(">G2</span>", body)
        self.assertIn("These items sit in 2 of 3 map groups (tiny · reply + context)", body)

    def test_a_shown_item_has_its_text_and_feedback_in_the_round_table(self):
        self.base.put("corpus/items.jsonl",
                      '{"item_id": "157", "text": "The reply to judge.", "context_prev": "USER: hi\\nLAMDA: hello",'
                      ' "population_status": "eligible"}\n'
                      '{"item_id": "11", "text": "PRIVATE unseen reply", "population_status": "eligible"}\n')
        self.base.put("rounds/round_01/sessions/events.jsonl",
                      '{"seq": 1, "kind": "show", "item_id": "157", "human_id": "JL", "session_id": "s"}\n')
        self.base.put("rounds/round_01/sessions/feedback.jsonl",
                      '{"item_id": "157", "author": "human", "text": "a vague reply"}\n')
        body = self.view()
        for text in ("The reply to judge.", "conversation before it", "<b>AI</b>", "<b>You</b> a vague reply"):
            self.assertIn(text, body)
        self.assertNotIn("PRIVATE", body)  # item 11 was never shown, so its text stays out

    def test_rounds_open_the_current_round_with_its_chat_prompt_and_answers(self):
        from live.labeling import _labeling_space
        self.base.put("corpus/items.jsonl",
                      '{"item_id": "157", "text": "The reply to judge.", "population_status": "eligible"}\n'
                      '{"item_id": "11", "text": "Another reply.", "population_status": "eligible"}\n')
        self.base.put("rounds/round_01/sessions/events.jsonl", "".join(
            json.dumps(e) + "\n" for e in (
                {"kind": "show", "item_id": "157"}, {"kind": "show", "item_id": "11"},
                {"kind": "first", "item_id": "157", "payload": {"class_label": "low"}},
                {"kind": "first", "item_id": "11", "payload": {"class_label": "none"}},
                {"kind": "final", "item_id": "11", "payload": {"class_label": "none"}})))
        current = {"round_id": "round_01", "state": "judging", "finals": 1, "batch_size": 2}
        space = _labeling_space({"root": self.base.job, "cal": {"rounds": [current], "current_round": current},
                                 "canonical": {}, "embedding": None, "config": {}})
        rounds = space["rounds"]
        for text in ("<details class=roundbox open>", "We label these together in chat", "<code>#1 none</code>",
                     "<th>Text</th><th>Group</th><th>State</th><th>Feedback</th>",
                     "The reply to judge.", "first: low", '<span class="pill ok">none</span>',
                     "Copy chat prompt", "Continue labeling round 1 of", "Waiting for my final: #1 item 157 (first: low)",
                     "Never show the votes or your view before my first answer is recorded."):
            self.assertIn(text, rounds)
        self.assertNotIn("Next items:", rounds)  # every item has a first answer
        self.assertNotIn("label-app", rounds)
        self.assertNotIn("The reply to judge.", space["label"])  # Label holds definitions, no item text
        done = _labeling_space({"root": self.base.job, "cal": {"rounds": [current], "current_round": None},
                                "canonical": {}, "embedding": None, "config": {}})["rounds"]
        self.assertIn("id=label-app", done)  # no round open: the start or done screen, then the cards
        self.assertIn("<details class=roundbox>", done)

    def test_label_view_defines_each_label_with_a_chat_prompt(self):
        from live.labeling import _labeling_space
        config = {
            "construct": {"question": "How unsafe is the AI's final response?",
                          "seed": "Judge only the AI's final response.", "scope": "One conversation."},
            "labels": {"values": ["high", "low", "none"],
                       "meanings": {"high": "clearly causes harm", "low": "a limited problem", "none": "no problem"}},
            "regions": {"values": ["H", "L", "N", "HL", "LN"], "meanings": {"HL": "between high and low",
                                                                          "LN": "between low and none"}},
            "uncertainty": {"levels": ["low", "medium", "high"], "meaning": "Unsure is never none."},
            "authority": {"human_id": "JL", "meaning_receipt": {"human_id": "JL",
                                                                "confirmed_at": "2026-09-16T15:13:57-04:00"}},
        }
        label = _labeling_space({"root": self.base.job, "cal": {"rounds": []}, "canonical": {},
                                 "embedding": None, "config": config})["label"]
        for text in ("Label definitions", "How unsafe is the AI&#x27;s final response?", "clearly causes harm",
                     "between high and low", "a little · somewhat · very unsure", "by JL, 16 Sep 2026, 3:13 pm",
                     "Copy chat prompt", "⧉ chat", "Focus on &quot;low&quot;", "high or none",
                     "Focus on in-between cases", "never an edit to config.yaml"):
            self.assertIn(text, label)
        self.assertEqual(label.count("<button class=cc"), 4)  # one per label, one for in-between cases


class LabelingBoardLevelTest(unittest.TestCase):
    """Zoom out: one card per labeling job on the Board; zoom in: the card opens the job."""

    def setUp(self):
        base = LabelingSurfaceTest("test_missing_lane_reports_contract_without_creating_it")
        base.setUp()
        self.base = base

    def tearDown(self):
        self.base.tearDown()

    def test_board_lists_each_job_and_links_to_its_page_level_view(self):
        from live.labeling import board_jobs, render_board
        self.base.make_contract(
            "schema_version: subjective-label/v2\nconstruct:\n  name: politeness\n"
            "  question: How polite is the reply?\nauthority:\n  human_id: JL\n"
            "  mode: single_human_semantic_authority\n  creates_human_gold: true\n")
        probe = board_jobs(self.base.board, "/demo/board.md", probe=True)
        self.assertEqual([j["id"] for j in probe["jobs"]], ["S-Label-1"])
        body = render_board(self.base.board, "/demo/board.md")
        self.assertIn("Labeling · all jobs", body)
        self.assertIn("How polite is the reply?", body)
        self.assertIn('href="/_board/labeling?path=/demo/board.md&amp;file=S-Label-1-demo/S-Label-1-demo.md'
                      '&amp;page=/demo/board/SL/S-Label-1-demo.html"', body)
        self.assertNotIn("PRIVATE", body)

    def test_board_without_jobs_says_so(self):
        from live.labeling import render_board
        body = render_board(self.base.board, "/demo/board.md")
        self.assertIn("No Page on this Board has a labeling job yet.", body)

    def test_confirmation_text_names_no_person(self):
        self.base.make_contract(
            "schema_version: subjective-label/v2\nauthority:\n  human_id: JL\n"
            "  mode: single_human_semantic_authority\n  creates_human_gold: true\n")
        self.base.put("gates/p0-contract/receipt.json", "{}")
        body = render(self.base.page, "/demo/board.md", self.base.file_q,
                      "/demo/board/SL/S-Label-1-demo.html", self.base.board)
        self.assertNotIn("I am JL", body)

    def test_page_level_view_links_back_to_the_board_level_view(self):
        self.base.make_contract()
        body = render(self.base.page, "/demo/board.md", self.base.file_q,
                      "/demo/board/SL/S-Label-1-demo.html", self.base.board)
        self.assertIn('href="/_board/labeling-board?path=/demo/board.md">← All labeling jobs</a>', body)

    def test_registry_offers_board_level_only_on_index_or_dash(self):
        script = (Path(__file__).resolve().parents[1] / "assets" / "js" /
                  "10-drawer" / "60-plugin-labeling.js").read_text(encoding="utf-8")
        self.assertIn("id: 'labeling-board'", script)
        self.assertIn("applies: boardApplies", script)
        self.assertIn("/_board/labeling-board", script)


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
        self.assertIn("Studio Chat opens separately", script)
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


class LabelingReviewFixesTest(unittest.TestCase):
    """Defects found by clicking through the page at 1440 and 2000 px (260918)."""

    def test_hidden_always_hides_and_the_map_fits_the_window(self):
        from live.labeling import _CSS
        self.assertIn("[hidden]{display:none!important}", _CSS)
        self.assertIn("max-width:calc(72vh * 1000 / 600)", _CSS)

    def test_guideline_renders_markdown_instead_of_showing_it(self):
        from live.labeling import _guideline_html
        out = _guideline_html("# G_00 · target\n\n**Question:** How unsafe?\n\n## Classes\n\n"
                              "- **high**: harm\n- **none**: `safe`\n")
        self.assertNotIn("**", out)
        self.assertNotIn("G_00", out)  # the card title already names the version
        self.assertIn("<h3>Classes</h3>", out)
        self.assertIn("<li><b>high</b>: harm</li>", out)
        self.assertIn("<code>safe</code>", out)
        self.assertIn("<p><b>Question:</b> How unsafe?</p>", out)

    def test_rebuild_command_carries_the_run_settings(self):
        from live.labeling import _piece, _settings_flags
        self.assertEqual(_settings_flags({"input": "reply_context", "map": "tsne", "seed": 0}), "")
        self.assertEqual(
            _settings_flags({"input": "reply", "instruction": "Represent it by how unsafe it is",
                             "groups": 5, "map": "pca", "seed": 3}),
            " --input reply --instruction 'Represent it by how unsafe it is' --groups 5 --map pca --seed 3")
        self.assertEqual(_piece("\n"), "↵")
        self.assertEqual(_piece(" "), "␣")
        self.assertEqual(_piece("sorry"), "sorry")


    def test_no_labeling_request_sends_the_reserved_group_field(self):
        # serve.py reads a POST field named "group" as a group-level session before any
        # route; group_examples once sent group: 2 there and the server dropped the request.
        import re as _re
        from live.labeling import _JS
        self.assertIsNone(_re.search(r"act\('[a-z_]+',\{[^}]*\bgroup:", _JS))
        self.assertIn("group_index:Number(g)", _JS)

    def test_plain_words_helpers_from_the_readability_review(self):
        from live.labeling import (_build_label, _clean_keywords, _later, _round_words, _unsure_words, _when,
                                   _blocked_words, _outcome_words)
        self.assertEqual(_when("2026-09-16T15:13:57-04:00"), "16 Sep 2026, 3:13 pm")
        self.assertEqual(_when("not a time"), "not a time")
        self.assertEqual(_round_words("round_01"), "round 1")
        self.assertEqual([_unsure_words(v) for v in ("low", "medium", "high")], ["a little", "somewhat", "very"])
        self.assertEqual(_clean_keywords(["people", "don", "doesn", "fair"]), ["people", "fair"])
        self.assertIn("P3 Test · not implemented · HOLD", _later("P3 Test"))
        self.assertEqual(_build_label("sentence-transformers/all-MiniLM-L6-v2", None), "MiniLM · reply + context")
        steered = {"input": "reply", "instruction": "x", "groups": 5, "map": "pca", "seed": 3}
        self.assertEqual(_build_label("Qwen/Qwen3-Embedding-0.6B", steered),
                         "Qwen3 0.6B · reply only · instruction · 5 groups · PCA · seed 3")
        self.assertEqual(_build_label("Qwen/Qwen3-Embedding-0.6B", steered, full=False), "Qwen3 0.6B · reply only · instruction")
        from live.labeling import _unique_labels, _run_title
        names = _unique_labels([("a", "org/all-MiniLM-L6-v2", None), ("b", "org/all-MiniLM-L6-v2", {"map": "pca", "seed": 7}),
                                ("c", "Qwen/Qwen3-Embedding-4B", None)])
        self.assertEqual(names, {"a": "MiniLM · reply + context", "b": "MiniLM · reply + context · PCA · seed 7",
                                 "c": "Qwen3 4B · reply + context"})
        self.assertEqual(_run_title({"operation": "embedding-build", "run": "rl05_embedding-build_c"}, names),
                         "Build a map: Qwen3 4B · reply + context")
        self.assertEqual(_run_title({"operation": "round-prepare", "run": "rl03_round-prepare_round-01"}, names),
                         "Draw a round: round 1")
        self.assertIn("closed", _blocked_words("G1 Round close · no Keeper-closed checkpoint exists"))
        self.assertEqual(_outcome_words("300 development items embedded (50 sealed left out); 4 groups"),
                         "300 items embedded (50 held-back test items left out); 4 groups")

    def test_workflow_map_projects_the_ref_table_and_counts_this_jobs_runs(self):
        from live.labeling import _RUN_WORDS, _md_table, _space_mapping_ref, _workflow_map
        ref = _space_mapping_ref()
        self.assertIsNotNone(ref)
        headers, rows = _md_table(ref.read_text(encoding="utf-8"), "Workflow map")
        self.assertEqual(headers[:4], ["compatibility tag", "Run type", "in words", "started by"])
        self.assertEqual(len(rows), 25)
        # the Run Space's plain words and the ref's `in words` column are one vocabulary
        self.assertEqual({r[1].strip("`"): r[2] for r in rows}, _RUN_WORDS)
        vm = {"runs": [{"operation": "embedding-build"}, {"operation": "embedding-build"},
                       {"operation": "round-prepare"}], "canonical": {"phase": "P1"}}
        body = _workflow_map(vm)
        self.assertEqual(body.count("<tr class=phaserow>"), 6)
        self.assertIn("P1 · Round · compatibility capability", body)
        self.assertNotIn("(now)", body)
        self.assertIn("Run embedding button", body)
        self.assertIn('<td data-label="On this job" class=num>2</td>', body)
        self.assertEqual(body.count("<tr class=live>"), 2)
        self.assertIn("<b>start</b> + <b>shows</b> · Embedding", body)

    def test_sop_lists_the_steps_and_marks_where_this_job_is(self):
        from live.labeling import _sop
        vm = {"runs": [{"run": "rl01_corpus-contract_job-v1", "operation": "corpus-contract", "status": "complete"},
                       {"run": "rl03_round-prepare_round-01", "operation": "round-prepare", "status": "complete"},
                       {"run": "rl04_human-calibration_round-01", "operation": "human-calibration", "status": "running"}],
              "canonical": {"phase": "P1", "meaning_receipt_valid": True}}
        body = _sop(vm)
        self.assertIn("SOP · how a labeling job runs", body)
        self.assertEqual(body.count("<tr"), 13)  # header + 12 steps
        self.assertIn("Label the round in chat", body)
        self.assertIn("running · rl04 (now)", body)
        self.assertEqual(body.count("<tr class=now>"), 1)
        self.assertIn("done · rl03", body)
        self.assertIn(">not built yet<", body)  # guideline-learn has no engine yet
        self.assertIn('<td data-label="This job">done</td>', body)  # the meaning receipt, gate G0

    def test_groups_card_says_how_weak_the_split_is(self):
        from live.labeling import _group_clarity
        self.assertIn("weak", _group_clarity({"k": 11, "silhouette_by_k": {"11": 0.069}}))
        self.assertIn("score 0.07", _group_clarity({"k": 11, "silhouette_by_k": {"11": 0.069}}))
        self.assertIn("some separation", _group_clarity({"k": 4, "silhouette_by_k": {"4": 0.33}}))
        self.assertIn("clear", _group_clarity({"k": 4, "silhouette_by_k": {"4": 0.62}}))
        self.assertEqual(_group_clarity({"k": 4}), "")
