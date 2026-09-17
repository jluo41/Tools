"""The Design presenter and its actions, exercised on contract-valid v2 folders."""

import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from live import design_actions as acts
from live.design import (
    design_contract_status,
    design_snapshot,
    is_current_design_page,
    modern_file,
    perform_action,
    render_design,
)
from tests.fixture_design_v2 import (
    ItemSpec, audit, build_design_folder, build_insight_board, demo_specs, sms_criteria,
)


def legacy_fixture(root: Path) -> tuple[Path, Path]:
    board = root / "Current-DesignBoard"
    folder = board / "2-Design" / "Design-01-patient-confirm-sms"
    folder.mkdir(parents=True)
    (board / "board.md").write_text("# Current DesignBoard\n", encoding="utf-8")
    page = folder / "Design-01-patient-confirm-sms.md"
    page.write_text("# Patient confirmation SMS\n\nfolder-kind: design\n", encoding="utf-8")
    return board, page


def v2_fixture(root: Path, stem: str = "Design-01-patient-confirm-sms",
               specs: list | None = None) -> tuple[Path, Path, dict]:
    """A DesignBoard reading a sibling InsightBoard, laid out like the demo."""
    build_insight_board(root / "DesignPlugin-Demo-260916-InsightBoard")
    board = root / "DesignPlugin-Demo-260916-DesignBoard"
    board.mkdir(parents=True, exist_ok=True)
    (board / "board.md").write_text(
        "# Demo DesignBoard\nboard-kind: design-board\nreads: DesignPlugin-Demo-260916-InsightBoard\n",
        encoding="utf-8")
    brief = board / "0-BR-brief" / "BR00-brief" / "BR00-brief.md"
    brief.parent.mkdir(parents=True, exist_ok=True)
    brief.write_text(
        "# Design Brief\nfolder-kind: brief\n\n### 8 · What to design\n\n"
        "| line | audience | job | venue | designs | folder |\n|---|---|---|---|---|---|\n"
        "| R1 | full SMSR2 population, unconditioned | prescription review | sms | 2 | `Design-01-patient-confirm-sms` |\n"
        "| R2 | patients with a refill due within 7 days | refill review | ui-card | 1 | `Design-02-refill-reminder-ui` |\n",
        encoding="utf-8")
    spec = demo_specs()[stem]
    folder = board / "2-Design" / stem
    runs = build_design_folder(folder, stem, spec["title"], spec["opening"], specs or spec["specs"])
    return board, folder / f"{stem}.md", runs


class DesignContractTest(unittest.TestCase):
    def test_current_design_page_is_the_only_accepted_identity(self):
        with TemporaryDirectory() as td:
            _board, page = legacy_fixture(Path(td))
            self.assertTrue(is_current_design_page(page))
            self.assertEqual(design_contract_status(page), (True, ""))

    def test_legacy_design_shapes_are_not_reinterpreted(self):
        with TemporaryDirectory() as td:
            _board, page = legacy_fixture(Path(td))
            (page.parent / "design" / "DU01-old").mkdir(parents=True)
            self.assertFalse(is_current_design_page(page))
            self.assertIn("legacy design/DU*", design_contract_status(page)[1])
        with TemporaryDirectory() as td:
            _board, page = legacy_fixture(Path(td))
            (page.parent / "runs").mkdir()
            (page.parent / "runs" / "r01_design_generate_sms.yaml").write_text(
                "schema: haipipe.design-ticket/v1\n", encoding="utf-8")
            self.assertFalse(is_current_design_page(page))
            self.assertIn("legacy rNN_design_*", design_contract_status(page)[1])


class DesignItemsTest(unittest.TestCase):
    def test_fixture_is_contract_valid(self):
        with TemporaryDirectory() as td:
            _board, page, _runs = v2_fixture(Path(td))
            self.assertEqual(audit(page.parent), [])

    def test_items_carry_bet_evidence_and_derived_state(self):
        with TemporaryDirectory() as td:
            board, page, runs = v2_fixture(Path(td))
            snapshot = design_snapshot(page, board)
            by_id = {item["id"]: item for item in snapshot["items"]}
            self.assertEqual(list(by_id), ["ITEM01", "ITEM02"])
            item01 = by_id["ITEM01"]
            self.assertEqual((item01["type"], item01["stance"], item01["basis"]), ("sms", "follow", "evidence-informed"))
            self.assertIn("best arm on click", item01["expected"])
            self.assertIn("outside overlapping intervals", item01["falsified"])
            self.assertEqual(len(item01["acceptance"]), 5)
            self.assertEqual(item01["state"], "adopted")
            self.assertEqual(item01["waiting"], "")
            self.assertEqual([r["id"] for r in item01["runs"]],
                             [runs["ITEM01"][k] for k in ("commission", "generate", "verify", "adopt")])
            evidence = item01["evidence_rows"]
            self.assertEqual(len(evidence), 1)
            self.assertEqual(evidence[0]["role"], "handoff")
            self.assertTrue(evidence[0]["exists"])
            self.assertTrue(evidence[0]["pinned"])
            self.assertEqual(evidence[0]["signed"], "signed ✅ JL 260828")
            item02 = by_id["ITEM02"]
            self.assertEqual((item02["state"], item02["waiting"]), ("generate failed", "agent · revise"))
            self.assertEqual(item02["mode"], "challenge")
            self.assertEqual(snapshot["insight"]["status"], "bound")
            self.assertEqual(snapshot["unassigned"], [])
            self.assertEqual(snapshot["audit"], [])

    def test_runs_carry_actor_mode_time_and_checks(self):
        with TemporaryDirectory() as td:
            board, page, runs = v2_fixture(Path(td))
            by_run = {r["id"]: r for r in design_snapshot(page, board)["runs"]}
            commission = by_run[runs["ITEM01"]["commission"]]
            self.assertEqual((commission["actor"], commission["mode"]), ("JL", "human"))
            self.assertEqual(commission["outcome"], "release")
            self.assertEqual(commission["route"], "generate")
            generate = by_run[runs["ITEM01"]["generate"]]
            self.assertEqual(generate["mode"], "agent")
            self.assertEqual(generate["actor"], "designer-context-01")
            self.assertEqual(generate["verdict"], "pass")
            self.assertEqual(generate["checks_passed"], len(generate["checks"]))
            self.assertIn("Reply STOP to opt-out", generate["artifacts"][0]["text"])
            self.assertEqual(generate["finished"], "2026-09-16 13:04")
            self.assertEqual(generate["intent"]["stance"], "follow")
            failed = by_run[runs["ITEM02"]["generate"]]
            self.assertEqual(failed["status"], "failed")
            self.assertIn("configured maximum is 120", failed["failure"])

    def test_design_card_shows_design_why_evidence_prediction(self):
        with TemporaryDirectory() as td:
            board, page, _runs = v2_fixture(Path(td))
            rendered = render_design(design_snapshot(page, board), "design", "ITEM01")
            for label in ("Hi, it&#x27;s Dr. {NAME}&#x27;s office.", "follows the evidence",
                          "built on evidence", "supported by FW01-send-salience ✅", "<th>insight</th>",
                          "expected: salience stays the best arm",
                          "falsified if: a concurrently fielded", "byte-identical to the fielded salience template",
                          "Page level", "Queue revise · agent", "New Design Item", "<th>goal</th>"):
                self.assertIn(label, rendered)
            for jargon in ("pinned in Ticket", "candidate text", "check_unit", "handoffs signed", "roster"):
                self.assertNotIn(jargon, rendered)
            for noise in ("current Design Folder", "handoffs signed", "waiting on JL · adopt</div>", "register "):
                self.assertNotIn(noise, rendered.split("<div class=tabs", 1)[0])
            for retired in ("Flow nodes", "Spaces: 4", "Anchor", "Trial", "Candidates:", "Signal Space"):
                self.assertNotIn(retired, rendered)

    def test_adopted_card_pins_the_exact_candidate(self):
        with TemporaryDirectory() as td:
            board, page, runs = v2_fixture(Path(td))
            snapshot = design_snapshot(page, board)
            adopted = snapshot["items"][0]["adopted"]
            self.assertEqual(adopted["candidate"], runs["ITEM01"]["generate"])
            self.assertEqual(adopted["verification"], runs["ITEM01"]["verify"])
            self.assertEqual(len(adopted["sha256"]), 64)
            self.assertIn("warrant P01", adopted["words"])
            rendered = render_design(snapshot, "delivery")
            self.assertIn("✅ adopted · JL", rendered)
            self.assertIn("ITEM02 · Attribution removed · not adopted", rendered)

    def test_generated_item_waits_on_the_independent_verifier(self):
        with TemporaryDirectory() as td:
            board, page, _runs = v2_fixture(Path(td), "Design-02-refill-reminder-ui")
            snapshot = design_snapshot(page, board)
            item = snapshot["items"][0]
            self.assertEqual((item["state"], item["waiting"]), ("generated", "agent · verify"))
            self.assertIsNone(item["adopted"])
            self.assertIn("Queue Verify · independent agent", render_design(snapshot))

    def test_empty_current_folder_is_truthful(self):
        with TemporaryDirectory() as td:
            board, page = legacy_fixture(Path(td))
            rendered = render_design(design_snapshot(page, board))
            self.assertIn("No Design Item register yet", rendered)
            self.assertIn("No Design Run records", rendered)
            self.assertIn("Nothing adopted", rendered)
            self.assertNotIn("nothing waiting", rendered)
            self.assertIn("Page level", rendered)


def verified_spec() -> ItemSpec:
    return ItemSpec(id="ITEM01", title="Send the tested winner, verbatim", kind="sms",
                    goal="Field the salience template exactly as round 1 sent it",
                    audience="full SMSR2 population", job="prescription review",
                    content="Hi, it's Dr. {NAME}'s office. New prescription details require your review: Reply STOP to opt-out",
                    criteria=sms_criteria(), acceptance=["≤ 160 characters", "ends with 'Reply STOP to opt-out'"],
                    stage="verified")


class DesignActionsTest(unittest.TestCase):
    def payload(self, page: Path, **kw) -> dict:
        return {"path": "/board.md", "file": f"2-Design/{page.parent.name}/{page.name}", **kw}

    def test_add_item_release_and_queue_generate(self):
        with TemporaryDirectory() as td:
            board, page, _runs = v2_fixture(Path(td))
            out, err = perform_action(page, self.payload(
                page, action="add-item", title="Reminder before refill", type="sms",
                audience="patients due a refill", job="refill", goal="Nudge without alarm",
                stance="generate", basis="brief-only",
                acceptance="≤ 160 characters\nends with 'Reply STOP to opt-out'\nno {NAME} placeholder\nwarm tone"))
            self.assertIsNone(err, err)
            self.assertEqual(out["item"], "ITEM03")
            item = {i["id"]: i for i in design_snapshot(page, board)["items"]}["ITEM03"]
            self.assertEqual((item["state"], item["waiting"]), ("not commissioned", "JL · commission"))
            out, err = perform_action(page, self.payload(page, action="commission-release", item="ITEM03",
                                                         actor="JL", words="Release ITEM03 for a first draft"))
            self.assertIsNone(err, err)
            self.assertTrue(out["run"].startswith("rd07_commission_"))
            snapshot = design_snapshot(page, board)
            item = {i["id"]: i for i in snapshot["items"]}["ITEM03"]
            self.assertEqual((item["state"], item["waiting"]), ("commissioned", "agent · generate"))
            self.assertEqual(snapshot["audit"], [])
            config = acts._load(page.parent / "scripts" / "config" / f"{out['run']}.yaml")
            kinds = [c["kind"] for c in config["criteria"]]
            self.assertEqual(kinds, ["max_chars", "contains", "excludes", "semantic"])
            self.assertEqual(config["criteria"][2]["value"], "{NAME}")
            out, err = perform_action(page, self.payload(page, action="queue-generate", item="ITEM03"))
            self.assertIsNone(err, err)
            snapshot = design_snapshot(page, board)
            item = {i["id"]: i for i in snapshot["items"]}["ITEM03"]
            self.assertEqual((item["state"], item["waiting"]), ("generate queued", "agent · generate"))
            self.assertEqual(snapshot["audit"], [])
            self.assertIn("planned · queued for agent", render_design(snapshot, "run", "ITEM03"))

    def test_revise_queues_generate_with_base_and_feedback(self):
        with TemporaryDirectory() as td:
            board, page, runs = v2_fixture(Path(td))
            out, err = perform_action(page, self.payload(page, action="queue-revise", item="ITEM02",
                                                         feedback="shorten below 120 and keep the opt-out"))
            self.assertIsNone(err, err)
            ticket = acts._load(page.parent / "runs" / f"{out['run']}.yaml")
            roles = {i["role"]: i for i in ticket["inputs"]}
            self.assertIn("base", roles)
            self.assertIn("feedback", roles)
            self.assertEqual(roles["base"]["run_id"], runs["ITEM02"]["generate"])
            config = acts._load(page.parent / "scripts" / "config" / f"{out['run']}.yaml")
            # ITEM02 is a challenge bet: the checker binds stance to mode, so its
            # revision stays `challenge` over the frozen base + feedback.
            self.assertEqual(config["mode"], "challenge")
            self.assertEqual(design_snapshot(page, board)["audit"], [])

    def test_verify_and_adopt_are_refused_before_their_inputs_exist(self):
        with TemporaryDirectory() as td:
            board, page, _runs = v2_fixture(Path(td), "Design-02-refill-reminder-ui")
            _out, err = perform_action(page, self.payload(page, action="adopt", item="ITEM01", actor="JL"))
            self.assertIn("no complete Verify Result", err)
            out, err = perform_action(page, self.payload(page, action="queue-verify", item="ITEM01"))
            self.assertIsNone(err, err)
            item = design_snapshot(page, board)["items"][0]
            self.assertEqual((item["state"], item["waiting"]), ("verify queued", "agent · verify"))
            _out, err = perform_action(page, self.payload(page, action="queue-verify", item="ITEM01"))
            self.assertIsNone(err)  # a second planned verify is legal; it is the agent's queue

    def test_adopt_writes_preview_decision_and_closes_the_item(self):
        with TemporaryDirectory() as td:
            board, page, _runs = v2_fixture(Path(td), specs=[verified_spec()])
            item = design_snapshot(page, board)["items"][0]
            self.assertEqual((item["state"], item["waiting"]), ("verified", "JL · adopt"))
            _out, err = perform_action(page, self.payload(page, action="adopt", item="ITEM01", actor="",
                                                          words="x"))
            self.assertIn("named", err)
            out, err = perform_action(page, self.payload(page, action="adopt", item="ITEM01", actor="JL",
                                                         words="Adopt v1, verbatim salience"))
            self.assertIsNone(err, err)
            snapshot = design_snapshot(page, board)
            item = snapshot["items"][0]
            self.assertEqual(item["state"], "adopted")
            self.assertEqual(item["adopted"]["words"], "Adopt v1, verbatim salience")
            self.assertTrue((page.parent / "delivery" / "render" / out["preview"]).is_file())
            self.assertEqual(snapshot["audit"], [])
            rendered = render_design(snapshot, "design")
            for gone in ("data-action=adopt", "data-action=decline", "Release commission"):
                self.assertNotIn(gone, rendered)
            self.assertIn("data-action=add-item", rendered)  # the register stays open

    def test_queue_verify_on_an_evidence_informed_item_carries_the_evidence(self):
        with TemporaryDirectory() as td:
            spec = demo_specs()["Design-01-patient-confirm-sms"]["specs"][0]
            spec.stage = "generated"
            board, page, _runs = v2_fixture(Path(td), specs=[spec])
            out, err = perform_action(page, self.payload(page, action="queue-verify", item="ITEM01"))
            self.assertIsNone(err, err)
            ticket = acts._load(page.parent / "runs" / f"{out['run']}.yaml")
            self.assertEqual([i["role"] for i in ticket["inputs"]], ["handoff"])
            self.assertEqual(design_snapshot(page, board)["audit"], [])

    def test_complete_run_gates_the_worker_result_before_writing_the_receipt(self):
        with TemporaryDirectory() as td:
            board, page, _runs = v2_fixture(Path(td), "Design-02-refill-reminder-ui")
            out, err = perform_action(page, self.payload(page, action="queue-verify", item="ITEM01"))
            self.assertIsNone(err, err)
            run = out["run"]
            folder = page.parent
            with self.assertRaises(acts.ActionError):
                acts.complete_run(folder, run)          # the worker wrote nothing yet
            # A dishonest worker Result (verdict pass, but no checks) must close as failed.
            (folder / "results" / run / "result.yaml").write_text(
                "schema: haipipe.design-result/v2\nrun: %s\noperation: verify\nverdict: pass\n" % run,
                encoding="utf-8")
            closed = acts.complete_run(folder, run)
            self.assertEqual(closed["status"], "failed")
            self.assertTrue(closed["problems"])
            item = design_snapshot(page, board)["items"][0]
            self.assertEqual(item["state"], "verify invalid")   # the review failed the gate
            self.assertEqual(item["waiting"], "agent · verify")  # redo the review, not the candidate

    def test_revise_decision_queues_a_revise_generate(self):
        with TemporaryDirectory() as td:
            board, page, _runs = v2_fixture(Path(td), specs=[verified_spec()])
            out, err = perform_action(page, self.payload(page, action="revise", item="ITEM01", actor="JL",
                                                         words="drop the apostrophe form"))
            self.assertIsNone(err, err)
            self.assertIn("revise", out)
            item = design_snapshot(page, board)["items"][0]
            self.assertEqual((item["state"], item["waiting"]), ("generate queued", "agent · generate"))
            self.assertEqual(design_snapshot(page, board)["audit"], [])


class GoalAndInsightSpaceTest(unittest.TestCase):
    def test_goal_space_reads_the_brief_line_that_names_the_folder(self):
        with TemporaryDirectory() as td:
            board, page, _runs = v2_fixture(Path(td))
            snapshot = design_snapshot(page, board)
            goal = snapshot["goal"]
            self.assertEqual(goal["row"]["id"], "R1")
            self.assertEqual((goal["wanted"], goal["registered"], goal["adopted"]), (2, 2, 1))
            self.assertEqual(goal["sentence"], "2 sms designs for full SMSR2 population, unconditioned, prescription review")
            rendered = render_design(snapshot, "goal")
            for label in ("Goal Space", "Design Space", "Insight Space", "Run Space", "Delivery Space",
                          "2 sms designs for full SMSR2 population", "2 wanted · 2 registered · 1 adopted",
                          "<th>their job</th>", "line R1", "Insight board", "1 of 1 insights signed"):
                self.assertIn(label, rendered)

    def test_goal_space_is_truthful_without_a_brief_line(self):
        with TemporaryDirectory() as td:
            board, page = legacy_fixture(Path(td))
            rendered = render_design(design_snapshot(page, board))
            self.assertIn("No Brief under 0-BR-brief/", rendered)
            self.assertIn("none declared by the owning board", rendered)

    def test_insight_space_says_what_each_insight_says_and_what_is_unused(self):
        with TemporaryDirectory() as td:
            board, page, _runs = v2_fixture(Path(td))
            snapshot = design_snapshot(page, board)
            blocks = snapshot["insight_space"]["items"]
            self.assertEqual([b["item"]["id"] for b in blocks], ["ITEM01", "ITEM02"])
            row = blocks[0]["rows"][0]
            self.assertEqual(row["word"], "signed insight")
            self.assertTrue(row["finding"].startswith("Of thirteen arms fielded on 444,691 invitations"))
            self.assertIn("may field `salience` verbatim", row["consequence"])
            self.assertTrue(row["pinned"])
            self.assertEqual(snapshot["insight_space"]["unused"], [])   # the one handoff is used
            rendered = render_design(snapshot, "insight")
            for label in ("<th>what it says</th>", "signed insight · ", "in the run record",
                          "then: Design may field"):
                self.assertIn(label, rendered)

    def test_insight_space_flags_an_item_built_on_evidence_with_none_named(self):
        with TemporaryDirectory() as td:
            board, page, _runs = v2_fixture(Path(td), "Design-02-refill-reminder-ui")
            acts.add_item(page.parent, page.stem, {
                "title": "Second card", "goal": "Try a shorter card", "type": "ui-card",
                "audience": "patients due a refill", "job": "refill review",
                "stance": "follow", "basis": "evidence-informed",
                "evidence": "handoff · ../../../DesignPlugin-Demo-260916-InsightBoard/1-F-full/FW01-send-salience/FW01-send-salience.md",
                "acceptance": "≤ 200 characters"})
            register = page.parent / "outline" / f"{page.stem}-design-items.md"
            text = register.read_text(encoding="utf-8")
            needle = "evidence:\n- handoff · ../../../DesignPlugin-Demo-260916-InsightBoard/1-F-full/FW01-send-salience/FW01-send-salience.md\n"
            cut = text.rfind(needle)
            text = text[:cut] + text[cut + len(needle):]      # strip only ITEM02's line
            register.write_text(text, encoding="utf-8")
            snapshot = design_snapshot(page, board)
            block = next(b for b in snapshot["insight_space"]["items"] if b["item"]["id"] == "ITEM02")
            self.assertTrue(block["needed"])
            rendered = render_design(snapshot, "insight")
            self.assertIn("built on evidence, but no insight is named yet", rendered)
            self.assertIn("needs an insight", rendered)


class DesignSignalTest(unittest.TestCase):
    def signal_fixture(self, root: Path, signed: bool) -> tuple[Path, Path]:
        design_board = root / "B00_DesignBoard"
        insight_board = root / "A00_InsightBoard"
        page = design_board / "2-Design" / "Design-01-message" / "Design-01-message.md"
        page.parent.mkdir(parents=True)
        page.write_text("# Message\nfolder-kind: design\n", encoding="utf-8")
        (design_board / "board.md").write_text("# Design Board\nreads: A00_InsightBoard\n", encoding="utf-8")
        handoff = insight_board / "1-F-full" / "FW01-counsel" / "FW01-counsel.md"
        handoff.parent.mkdir(parents=True)
        handoff.write_text(
            "# Counsel\npage-type: wisdom\nquestion-rung: wisdom\nSERVES QW1\n"
            + ("signed: ✅ JL 260828\n" if signed else "signed: ⬜\n"), encoding="utf-8")
        (insight_board / "board.md").write_text("# Insight Board\nboard-kind: insight-board\n", encoding="utf-8")
        return root, page

    def test_signed_handoff_raises_no_warning(self):
        with TemporaryDirectory() as td:
            root, page = self.signal_fixture(Path(td), signed=True)
            snapshot = design_snapshot(page, root)
            self.assertEqual(snapshot["insight"]["status"], "bound")
            rendered = render_design(snapshot)
            self.assertNotIn("design stays blocked", rendered)
            self.assertIn("1 of 1 insights signed", rendered)      # Goal Space names the board

    def test_unsigned_handoff_warns_in_the_header(self):
        with TemporaryDirectory() as td:
            root, page = self.signal_fixture(Path(td), signed=False)
            snapshot = design_snapshot(page, root)
            self.assertEqual(snapshot["insight"]["status"], "blocked")
            self.assertIn("design stays blocked", render_design(snapshot))


if __name__ == "__main__":
    unittest.main()


class OldLinkTest(unittest.TestCase):
    def test_old_ds_links_map_to_the_full_names(self):
        self.assertEqual(modern_file("2-DS-design/DS01-patient-confirm-sms/DS01-patient-confirm-sms.md"),
                         "2-Design/Design-01-patient-confirm-sms/Design-01-patient-confirm-sms.md")
        self.assertEqual(modern_file("2-Design/Design-02-refill-reminder-ui/Design-02-refill-reminder-ui.md"),
                         "2-Design/Design-02-refill-reminder-ui/Design-02-refill-reminder-ui.md")
        self.assertEqual(modern_file(""), "")


class BatchAndDraftTest(unittest.TestCase):
    def test_batch_bar_shows_only_the_buttons_with_work(self):
        with TemporaryDirectory() as td:
            board, page, _runs = v2_fixture(Path(td))
            rendered = render_design(design_snapshot(page, board), "design")
            self.assertNotIn("Release all", rendered)            # both items already commissioned
            self.assertNotIn("Adopt all verified", rendered)     # nothing verified in the fixture
            self.assertNotIn("Queue all", rendered)              # adopted + generate failed: nothing queueable
            self.assertNotIn("mode <b>", rendered)               # mode is not a reader word

    def test_release_all_queue_all_and_adopt_all(self):
        with TemporaryDirectory() as td:
            board, page, _runs = v2_fixture(Path(td), "DS02-refill-reminder-ui".replace("DS02", "Design-02"))
            for n in (2, 3):
                acts.add_item(page.parent, page.stem, {
                    "title": f"Card {n}", "goal": f"Try card {n}", "type": "ui-card", "audience": "patients due a refill",
                    "job": "refill review", "stance": "generate", "basis": "brief-only", "acceptance": "≤ 200 characters"})
            snapshot = design_snapshot(page, board)
            self.assertIn("Release all · 2", render_design(snapshot, "design"))
            out, err = perform_action(page, {"path": "/board.md", "file": f"2-Design/{page.parent.name}/{page.name}",
                                             "action": "release-all", "item": "__all__", "actor": "JL",
                                             "words": "Release the new cards"})
            self.assertIsNone(err, err)
            self.assertEqual(out["items"], ["ITEM02", "ITEM03"])
            snapshot = design_snapshot(page, board)
            states = {i["id"]: i["state"] for i in snapshot["items"]}
            self.assertEqual(states, {"ITEM01": "generated", "ITEM02": "commissioned", "ITEM03": "commissioned"})
            self.assertIn("Queue all · 3 · agent", render_design(snapshot, "design"))
            out, err = perform_action(page, {"path": "/board.md", "file": f"2-Design/{page.parent.name}/{page.name}",
                                             "action": "queue-all", "item": "__all__"})
            self.assertIsNone(err, err)
            self.assertEqual(len(out["runs"]), 3)                # one verify + two generates
            self.assertEqual(sorted(r.split("_")[1] for r in out["runs"]), ["generate", "generate", "verify"])
            self.assertEqual(len(acts.planned_runs(page.parent)), 3)
            self.assertEqual(snapshot["audit"], [])
            _out, err = perform_action(page, {"path": "/board.md", "file": f"2-Design/{page.parent.name}/{page.name}",
                                              "action": "adopt-all", "item": "__all__", "actor": "JL", "words": "x"})
            self.assertEqual(err, "nothing to adopt; no item is verified")

    def test_name_worker_repins_the_receipt(self):
        with TemporaryDirectory() as td:
            board, page, _runs = v2_fixture(Path(td), "Design-02-refill-reminder-ui")
            snapshot = design_snapshot(page, board)
            run = acts.queue_verify(page.parent, page.stem, snapshot["items"][0], snapshot["items"][0]["runs"])["run"]
            out = acts.name_worker(page.parent, run, "reviewer-context-09")
            self.assertEqual(out["actor"], "reviewer-context-09")
            self.assertEqual(design_snapshot(page, board)["audit"], [])       # ticket and receipt still pair
            self.assertEqual(acts.planned_runs(page.parent), [])               # running, no longer planned
            with self.assertRaises(acts.ActionError):
                acts.name_worker(page.parent, run, "someone-else")
            back = acts.release_worker(page.parent, run)             # the worker died and left nothing
            self.assertEqual(back["lost"], "reviewer-context-09")
            self.assertEqual([r["run"] for r in acts.planned_runs(page.parent)], [run])
            self.assertEqual(design_snapshot(page, board)["audit"], [])
            self.assertEqual(design_snapshot(page, board)["items"][0]["state"], "verify queued")

    def test_counsel_lines_become_rules(self):
        text = ("```text\nid   counsel                                                       from\n"
                "W1   DO send `salience` to the whole population.                   FK01 · K1\n"
                "W2   DO NOT vary the message by age, gender, send day or region.   FK02 · K1\n"
                "W3   DO NOT ship a message this experiment never ran.              FK03 · K1\n```\n")
        rows = acts.counsel_lines(text)
        self.assertEqual([(r["id"], r["do"]) for r in rows], [("W1", True), ("W2", False), ("W3", False)])
        self.assertEqual(rows[1]["text"], "vary the message by age, gender, send day or region")
        self.assertEqual(acts.counsel_rules(text),
                         ["does not vary the message by age, gender, send day or region",
                          "does not ship a message this experiment never ran"])

    def test_draft_request_is_written_once_and_shown_in_goal_space(self):
        with TemporaryDirectory() as td:
            board, page, _runs = v2_fixture(Path(td))
            brief = board / "0-BR-brief" / "BR00-brief" / "BR00-brief.md"
            brief.write_text(brief.read_text(encoding="utf-8").replace("| sms | 2 |", "| sms | 10 |"), encoding="utf-8")
            snapshot = design_snapshot(page, board)
            rendered = render_design(snapshot, "goal")
            self.assertIn("Ask the agent to draft the missing 8", rendered)
            out, err = perform_action(page, {"path": "/board.md", "file": f"2-Design/{page.parent.name}/{page.name}",
                                             "action": "draft-request", "item": "__all__", "actor": "JL"})
            self.assertIsNone(err, err)
            request = Path(out["request"])
            text = request.read_text(encoding="utf-8")
            for label in ("items: 8", "goal: 10 sms designs for full SMSR2 population", "DO NOT vary the message",
                          "finding: Of thirteen arms", "asked-by: JL"):
                self.assertIn(label, text)
            snapshot = design_snapshot(page, board)
            self.assertEqual(snapshot["draft_request"]["items"], 8)
            rendered = render_design(snapshot, "goal")
            self.assertIn("draft request open: 8 item(s) asked by JL", rendered)
            self.assertNotIn("Ask the agent to draft", rendered)
            _out, err = perform_action(page, {"path": "/board.md", "file": f"2-Design/{page.parent.name}/{page.name}",
                                              "action": "draft-request", "item": "__all__", "actor": "JL"})
            self.assertIn("already open", err)

    def test_insight_space_lists_the_rules_the_page_implies(self):
        with TemporaryDirectory() as td:
            board, page, _runs = v2_fixture(Path(td))
            rendered = render_design(design_snapshot(page, board), "insight")
            self.assertIn("rules it implies: DO send", rendered)
            self.assertIn("DO NOT vary the message by age, gender, send day or region", rendered)
