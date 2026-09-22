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
    ItemSpec, audit, bind_insight_handoff, build_design_folder, build_insight_board, demo_specs, sms_criteria,
)


def legacy_fixture(root: Path) -> tuple[Path, Path]:
    board = root / "Current-DesignBoard"
    folder = board / "2-Design" / "Design-01-all-patients-prescription-review-sms"
    folder.mkdir(parents=True)
    (board / "board.md").write_text("# Current DesignBoard\n", encoding="utf-8")
    page = folder / "Design-01-all-patients-prescription-review-sms.md"
    page.write_text("# Prescription review SMS for all patients\n\nfolder-kind: design\n", encoding="utf-8")
    return board, page


def v2_fixture(root: Path, stem: str = "Design-01-all-patients-prescription-review-sms",
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
        "| R1 | all patients | prescription review | sms | 2 | `Design-01-all-patients-prescription-review-sms` |\n"
        "| R2 | patients with a refill due within 7 days | refill review | ui-card | 1 | `Design-02-patients-refill-due-refill-review-ui-card` |\n",
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
            self.assertEqual(item01["state"], "ready")
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
            self.assertEqual((item02["state"], item02["waiting"]), ("generate failed", "you · queue a revise"))
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
                          "built on evidence", "ready for Delivery",
                          "Page level", "Queue revise · agent", "New Design Item",
                          # the explanation reads as blocks, the insight as a flow (JL 260918)
                          "<th>Why this design</th>", "<th>From insight to design</th>", "<th>The bet</th>",
                          "<th>Rules</th>", "<table class=explain>",
                          "<span class=rung>Wisdom</span>", "<b>full-W01</b>", "✅ signed",
                          # named criteria (length, optout) still mark their rules: audit M5
                          "5 of 5 pass",
                          "<span class=rung>This design</span>",
                          # each item folds into one fixed-height row; the selected one opens (JL 260918)
                          "<details class=itemfold open><summary><b>ITEM01", "<span class=peek>Hi, it&#x27;s Dr.",
                          "<details class=itemfold><summary><b>ITEM02", "data-fold=open", "class=itembody", ".itembody .pair .pic{position:sticky",
                          "expected</span>salience stays the best arm",
                          "wrong if</span>a concurrently fielded"):
                self.assertIn(label, rendered)
            # the strip of Runs and the all-items bar are gone (JL 260921)
            for gone in ("<table class=kv><tr><th>goal</th>", "supported by FW01",
                         "<th>Runs</th>", "class=steps", "Commission ✓", "For all items at once"):
                self.assertNotIn(gone, rendered)
            for jargon in ("pinned in Ticket", "candidate text", "check_unit", "handoffs signed", "roster"):
                self.assertNotIn(jargon, rendered)
            # the design on the left, its explanation on the right; an SMS reads as a phone bubble
            # with the link where the sending system puts it (JL 260918)
            for label in ('<div class="pair text"><div class=pic><div class=phone>', "<div class=bubble>",
                          ": <span class=link>link</span> Reply STOP to opt-out</div>", "<div class=facts>"):
                self.assertIn(label, rendered)
            # a step that needs a click says "you", never the reader's name (JL 260921)
            for noise in ("current Design Folder", "handoffs signed", "waiting on JL", "register "):
                self.assertNotIn(noise, rendered.split("<div class=tabs", 1)[0])
            for retired in ("Flow nodes", "Spaces: 4", "Anchor", "Trial", "Candidates:", "Signal Space"):
                self.assertNotIn(retired, rendered)

    def test_ready_card_pins_the_exact_verified_candidate(self):
        with TemporaryDirectory() as td:
            board, page, runs = v2_fixture(Path(td))
            snapshot = design_snapshot(page, board)
            ready = snapshot["items"][0]["ready"]
            self.assertEqual(ready["run"], runs["ITEM01"]["generate"])
            self.assertEqual(ready["verification"], runs["ITEM01"]["verify"])
            self.assertEqual(len(ready["sha256"]), 64)
            rendered = render_design(snapshot, "delivery").split('data-space="delivery">', 1)[1]
            # Delivery Space lists only designs whose independent Verify passed.
            self.assertIn("<tr><th>item</th><th>design</th></tr>", rendered)
            for text in ("ITEM01", "Send the tested winner, verbatim", "Hi, it&#x27;s Dr. {NAME}&#x27;s office.",
                         ):
                self.assertIn(text, rendered)
            for status in ("adopted", "sha256", "waiting on", "data-action=adopt"):
                self.assertNotIn(status, rendered.split("</section>", 1)[0])

    def test_generated_item_waits_on_the_independent_verifier(self):
        with TemporaryDirectory() as td:
            board, page, _runs = v2_fixture(Path(td), "Design-02-patients-refill-due-refill-review-ui-card")
            snapshot = design_snapshot(page, board)
            item = snapshot["items"][0]
            self.assertEqual((item["state"], item["waiting"]), ("generated", "you · queue the review"))
            self.assertIsNone(item["ready"])
            self.assertIn("Queue Verify · independent agent", render_design(snapshot))

    def test_empty_current_folder_is_truthful(self):
        with TemporaryDirectory() as td:
            board, page = legacy_fixture(Path(td))
            rendered = render_design(design_snapshot(page, board))
            self.assertIn("No Design Item register yet", rendered)
            self.assertIn("No Design Run records", rendered)
            self.assertIn("No design is ready yet", rendered)
            self.assertNotIn("nothing waiting", rendered)
            self.assertIn("Page level", rendered)


def verified_spec() -> ItemSpec:
    return ItemSpec(id="ITEM01", title="Send the tested winner, verbatim", kind="sms",
                    goal="Field the salience template exactly as round 1 sent it",
                    audience="all patients", job="prescription review",
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
                acceptance=("≤ 160 characters\nends with 'Reply STOP to opt-out'\nno {NAME} placeholder\n"
                            "semantic: warm tone | observe: read as the intended recipient | "
                            "pass: plain words with no pressure | fail: threat or false urgency | "
                            "not-verifiable: no recipient or context is supplied")))
            self.assertIsNone(err, err)
            self.assertEqual(out["item"], "ITEM03")
            item = {i["id"]: i for i in design_snapshot(page, board)["items"]}["ITEM03"]
            self.assertEqual((item["state"], item["waiting"]), ("not commissioned", "you · commission"))
            out, err = perform_action(page, self.payload(page, action="commission-release", item="ITEM03",
                                                         actor="JL", words="Release ITEM03 for a first draft"))
            self.assertIsNone(err, err)
            self.assertTrue(out["run"].startswith("rd07_commission_"))
            snapshot = design_snapshot(page, board)
            item = {i["id"]: i for i in snapshot["items"]}["ITEM03"]
            self.assertEqual((item["state"], item["waiting"]), ("commissioned", "you · queue the draft"))
            self.assertEqual(snapshot["audit"], [])
            config = acts._load(page.parent / "scripts" / "config" / f"{out['run']}.yaml")
            kinds = [c["kind"] for c in config["criteria"]]
            self.assertEqual(kinds, ["max_chars", "ends_with", "excludes", "semantic"])
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

    def test_verify_is_refused_before_its_inputs_exist(self):
        with TemporaryDirectory() as td:
            board, page, _runs = v2_fixture(Path(td), "Design-02-patients-refill-due-refill-review-ui-card")
            out, err = perform_action(page, self.payload(page, action="queue-verify", item="ITEM01"))
            self.assertIsNone(err, err)
            item = design_snapshot(page, board)["items"][0]
            self.assertEqual((item["state"], item["waiting"]), ("verify queued", "agent · verify"))
            _out, err = perform_action(page, self.payload(page, action="queue-verify", item="ITEM01"))
            self.assertIn('"verify queued"; it waits on agent · verify', err)  # a double click queues nothing
            item = design_snapshot(page, board)["items"][0]
            with self.assertRaises(acts.ActionError):                             # nor does the writer alone
                acts.queue_verify(page.parent, page.stem, item, item["runs"])

    def test_verify_pass_is_ready_for_delivery_without_a_decision_run(self):
        with TemporaryDirectory() as td:
            board, page, _runs = v2_fixture(Path(td), specs=[verified_spec()])
            item = design_snapshot(page, board)["items"][0]
            self.assertEqual((item["state"], item["waiting"]), ("ready", ""))
            self.assertIsNotNone(item["ready"])
            snapshot = design_snapshot(page, board)
            item = snapshot["items"][0]
            self.assertEqual(snapshot["audit"], [])
            rendered = render_design(snapshot, "design")
            for gone in ("data-action=adopt", "data-action=decline", "Adopt", "Decline", "Release commission"):
                self.assertNotIn(gone, rendered)
            self.assertIn("ready for Delivery", rendered)
            self.assertIn("data-action=add-item", rendered)  # the register stays open

    def test_queue_verify_on_an_evidence_informed_item_carries_the_evidence(self):
        with TemporaryDirectory() as td:
            spec = demo_specs()["Design-01-all-patients-prescription-review-sms"]["specs"][0]
            spec.stage = "generated"
            board, page, _runs = v2_fixture(Path(td), specs=[spec])
            out, err = perform_action(page, self.payload(page, action="queue-verify", item="ITEM01"))
            self.assertIsNone(err, err)
            ticket = acts._load(page.parent / "runs" / f"{out['run']}.yaml")
            self.assertEqual([i["role"] for i in ticket["inputs"]], ["handoff"])
            self.assertEqual(design_snapshot(page, board)["audit"], [])

    def test_complete_run_gates_the_worker_result_before_writing_the_receipt(self):
        with TemporaryDirectory() as td:
            board, page, _runs = v2_fixture(Path(td), "Design-02-patients-refill-due-refill-review-ui-card")
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
            self.assertEqual(item["waiting"], "you · queue the review again")  # redo the review, not the candidate

    def test_decision_actions_are_removed_after_verify(self):
        with TemporaryDirectory() as td:
            board, page, _runs = v2_fixture(Path(td), specs=[verified_spec()])
            _out, err = perform_action(page, self.payload(page, action="revise", item="ITEM01",
                                                          actor="JL", words="drop the apostrophe form"))
            self.assertEqual(err, "unknown action 'revise'")


class GoalAndInsightSpaceTest(unittest.TestCase):
    def test_goal_space_reads_the_brief_line_that_names_the_folder(self):
        with TemporaryDirectory() as td:
            board, page, _runs = v2_fixture(Path(td))
            snapshot = design_snapshot(page, board)
            goal = snapshot["goal"]
            self.assertEqual(goal["row"]["id"], "R1")
            self.assertEqual((goal["wanted"], goal["registered"], goal["ready"]), (2, 2, 1))
            self.assertEqual(goal["sentence"], "2 prescription review SMS designs for all patients")
            rendered = render_design(snapshot, "goal")
            for label in ("Goal Space", "Design Space", "Insight Space", "Run Space", "Delivery Space",
                          "2 prescription review SMS designs for all patients", "2 wanted · 2 registered · 1 ready",
                          "<th>their job</th>", "· design tasks", "Insight board", "1 of 1 insights currently eligible"):
                self.assertIn(label, rendered)
            self.assertNotIn("line R1", rendered)  # the Brief's row id is a key, never a name on screen

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
            board, page, _runs = v2_fixture(Path(td), "Design-02-patients-refill-due-refill-review-ui-card")
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
            "# Counsel\nfolder-kind: wisdom\nstate: ✅ SETTLED\nquestion-rung: wisdom\nSERVES QW1\n"
            + ("signed: ✅ JL 260828\n" if signed else "signed: ⬜\n"), encoding="utf-8")
        (insight_board / "board.md").write_text("# Insight Board\nboard-kind: insight-board\n", encoding="utf-8")
        if signed:
            bind_insight_handoff(handoff)
        return root, page

    def test_signed_handoff_raises_no_warning(self):
        with TemporaryDirectory() as td:
            root, page = self.signal_fixture(Path(td), signed=True)
            snapshot = design_snapshot(page, root)
            self.assertEqual(snapshot["insight"]["status"], "bound")
            rendered = render_design(snapshot)
            self.assertNotIn("design stays blocked", rendered)
            self.assertIn("1 of 1 insights currently eligible", rendered)  # Goal Space names the board

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
        self.assertEqual(modern_file("2-Design/Design-02-patients-refill-due-refill-review-ui-card/Design-02-patients-refill-due-refill-review-ui-card.md"),
                         "2-Design/Design-02-patients-refill-due-refill-review-ui-card/Design-02-patients-refill-due-refill-review-ui-card.md")
        self.assertEqual(modern_file(""), "")


class BatchAndDraftTest(unittest.TestCase):
    def test_no_control_acts_on_every_item_at_once(self):
        """One decision, one item, one sentence on the record (JL 260921)."""
        with TemporaryDirectory() as td:
            board, page, _runs = v2_fixture(Path(td), "Design-02-patients-refill-due-refill-review-ui-card")
            for n in (2, 3):
                acts.add_item(page.parent, page.stem, {
                    "title": f"Card {n}", "goal": f"Try card {n}", "type": "ui-card",
                    "audience": "patients due a refill", "job": "refill review", "stance": "generate",
                    "basis": "brief-only", "acceptance": "\u2264 200 characters"})
            rendered = render_design(design_snapshot(page, board), "design")
            for gone in ("For all items at once", "Release all", "Queue all", "Adopt all",
                         "release-all", "queue-all", "adopt-all", "batchfold"):
                self.assertNotIn(gone, rendered)
            self.assertNotIn("data-action=adopt", rendered)     # historical labels are readable; no new decision button
            self.assertNotIn("mode <b>", rendered)               # mode is not a reader word

    def test_a_renamed_folder_is_found_by_its_design_number(self):
        from live.design import renamed_folder
        with TemporaryDirectory() as td:
            board, page, _runs = v2_fixture(Path(td))
            self.assertEqual(renamed_folder(board, "Design-01-patient-confirm-sms"), page.parent.name)
            self.assertEqual(renamed_folder(board, page.parent.name), page.parent.name)
            self.assertEqual(renamed_folder(board, "Design-09-nothing-here"), "Design-09-nothing-here")

    def test_decision_forms_are_folded_until_opened(self):
        with TemporaryDirectory() as td:
            board, page, _runs = v2_fixture(Path(td), "Design-02-patients-refill-due-refill-review-ui-card")
            acts.add_item(page.parent, page.stem, {
                "title": "Card 2", "goal": "Try card 2", "type": "ui-card", "audience": "patients due a refill",
                "job": "refill review", "stance": "generate", "basis": "brief-only", "acceptance": "≤ 200 characters"})
            snapshot = design_snapshot(page, board)
            rendered = render_design(snapshot, "design")
            self.assertIn("<details class=decide><summary>Release or hold the commission</summary>", rendered)
            self.assertIn('<div class=act><button class=do data-action=queue-verify>', rendered)   # one agent button stays in view
            self.assertIn("<details class=decide open>", render_design(snapshot, "design", "ITEM02"))

    def test_a_screen_design_is_shown_as_its_rendered_picture(self):
        import base64
        import json
        png = base64.b64decode("iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg==")
        with TemporaryDirectory() as td:
            board, page, _runs = v2_fixture(Path(td), "Design-02-patients-refill-due-refill-review-ui-card")
            item = design_snapshot(page, board)["items"][0]
            render = page.parent / "delivery" / "render"
            render.mkdir(parents=True)
            (render / "screen-ITEM01-v1.png").write_bytes(png)
            manifest = render / "manifest.json"
            manifest.write_text(json.dumps([{"item": "ITEM01", "render": "screen-ITEM01-v1.png",
                                             "candidate": item["latest"]["run"], "version": 1}]), encoding="utf-8")
            snapshot = design_snapshot(page, board)
            card = render_design(snapshot, "design")
            self.assertIn('<img class=shot src="/2-Design/', card)                 # served beside the board
            self.assertIn("<summary>the HTML behind this screen</summary>", card)  # the source is one click away
            self.assertIn("<div class=pair>", card)
            self.assertIn("No design is ready yet", render_design(snapshot, "delivery"))
            # A picture of another draft is never shown for this one.
            manifest.write_text(json.dumps([{"item": "ITEM01", "render": "screen-ITEM01-v1.png",
                                             "candidate": "rd99_generate_item01", "version": 1}]), encoding="utf-8")
            snapshot = design_snapshot(page, board)
            self.assertNotIn("<img class=shot", render_design(snapshot, "design"))
            self.assertIn("No design is ready yet", render_design(snapshot, "delivery"))

    def test_a_declined_item_leaves_the_delivery_overview(self):
        with TemporaryDirectory() as td:
            board, page, _runs = v2_fixture(Path(td))
            snapshot = design_snapshot(page, board)
            snapshot["items"][1]["state"] = "declined"
            delivery = render_design(snapshot, "delivery")
            overview, _, folded = delivery.partition("<details class=retired>")
            self.assertIn("<summary>Declined, kept for the record · 1</summary>", folded)
            self.assertIn(snapshot["items"][1]["title"], folded)
            self.assertNotIn(snapshot["items"][1]["title"], overview.split('data-space="delivery"')[-1])
            self.assertIn(snapshot["items"][0]["title"], overview)
            cards = render_design(snapshot, "design").split('data-space="design"')[-1].split('data-space="insight"')[0]
            live, _, folded_cards = cards.partition("<details class=retired>")
            self.assertIn('id="item-ITEM02"', folded_cards)                 # Design Space folds it the same way
            self.assertNotIn('id="item-ITEM02"', live)
            self.assertIn("<details class=retired open>", render_design(snapshot, "design", "ITEM02"))

    def test_a_rule_judged_on_the_render_is_a_visual_check(self):
        kinds = [c["kind"] for c in acts.compile_criteria([
            "fits 390 x 844 with no scrolling, judged on the render",
            "one primary button labelled 'Continue'",
            "plain words a patient understands"])]
        self.assertEqual(kinds, ["visual", "contains", "semantic"])

    def test_every_all_items_action_is_refused(self):
        """The surfaces went first (JL 260921); the endpoints follow, so nothing writes in bulk."""
        with TemporaryDirectory() as td:
            board, page, _runs = v2_fixture(Path(td), "Design-02-patients-refill-due-refill-review-ui-card")
            for n in (2, 3):
                acts.add_item(page.parent, page.stem, {
                    "title": f"Card {n}", "goal": f"Try card {n}", "type": "ui-card",
                    "audience": "patients due a refill", "job": "refill review", "stance": "generate",
                    "basis": "brief-only", "acceptance": "\u2264 200 characters"})
            base = {"path": "/board.md", "file": f"2-Design/{page.parent.name}/{page.name}",
                    "item": "__all__", "actor": "JL", "words": "x"}
            for action in ("release-all", "queue-all", "adopt-all"):
                out, err = perform_action(page, {**base, "action": action})
                self.assertIsNone(out)
                self.assertEqual(err, f"unknown action {action!r}")
            self.assertEqual(acts.planned_runs(page.parent), [])
            self.assertEqual({i["id"]: i["state"] for i in design_snapshot(page, board)["items"]},
                             {"ITEM01": "generated", "ITEM02": "not commissioned", "ITEM03": "not commissioned"})

    def test_name_worker_repins_the_receipt(self):
        with TemporaryDirectory() as td:
            board, page, _runs = v2_fixture(Path(td), "Design-02-patients-refill-due-refill-review-ui-card")
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
            for label in ("items: 8", "goal: 10 prescription review SMS designs for all patients", "DO NOT vary the message",
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


class AuditFixesTest(unittest.TestCase):
    """The fixes of the 260918 skill review, one behaviour each."""

    def payload(self, page: Path, **kw) -> dict:
        return {"path": "/board.md", "file": f"2-Design/{page.parent.name}/{page.name}", **kw}

    def new_item(self, page: Path, **fields) -> str:
        base = {"title": "Nudge", "goal": "Say what to review", "type": "sms", "audience": "all patients",
                "job": "prescription review", "stance": "generate", "basis": "brief-only",
                "acceptance": "≤ 160 characters\nends with 'Reply STOP to opt-out'"}
        return acts.add_item(page.parent, page.stem, {**base, **fields})["item"]

    def item(self, page: Path, board: Path, item_id: str) -> dict:
        return {i["id"]: i for i in design_snapshot(page, board)["items"]}[item_id]

    def test_a_recorded_target_reads_in_plain_words(self):
        """An old Run's target keeps `candidate` in its bytes; the surface says draft."""
        from live.design import plain_words
        self.assertEqual(plain_words("Send the winner · exact verified candidate"),
                         "Send the winner · exact verified draft")
        self.assertEqual(plain_words("two Candidates from one Ticket"), "two drafts from one run record")
        self.assertEqual(plain_words("the candidate-facing copy"), "the candidate-facing copy")  # only whole words

    def test_rules_compile_by_what_they_say(self):
        got = lambda rule: [(c["kind"], c.get("value")) for c in acts.compile_criteria([rule])]
        self.assertEqual(got("does not use 'urgent'"), [("excludes", "urgent")])                    # H1
        self.assertEqual(got("DO NOT say 'urgent' or 'act now'"), [("excludes", "urgent"), ("excludes", "act now")])
        self.assertEqual(got("keeps 'Hi' and does not say 'urgent'"), [("contains", "Hi"), ("excludes", "urgent")])
        self.assertEqual(got("it's short and it's kind"), [("semantic", None)])                     # no apostrophe quotes
        self.assertEqual(got("doesn't say 'urgent'"), [("excludes", "urgent")])
        self.assertEqual(got("surrendered nothing"), [("semantic", None)])                          # not "render"
        self.assertEqual(got("ends with 'Reply STOP to opt-out' verbatim"), [("ends_with", "Reply STOP to opt-out")])  # N7
        self.assertEqual(got("under 140 characters"), [("max_chars", 139)])
        self.assertEqual([c["id"] for c in acts.compile_criteria(["x", "no 'a' or 'b'"])], ["r01", "r02", "r02b"])

    def test_a_released_bet_stays_frozen(self):
        with TemporaryDirectory() as td:
            board, page, _runs = v2_fixture(Path(td))
            item_id = self.new_item(page)
            perform_action(page, self.payload(page, action="commission-release", item=item_id, actor="JL", words="go"))
            register = page.parent / "outline" / f"{page.stem}-design-items.md"
            register.write_text(register.read_text(encoding="utf-8").replace(
                "goal: Say what to review", "goal: Something else").replace("≤ 160 characters", "≤ 40 characters"),
                encoding="utf-8")                                       # edited after release (H2)
            out, err = perform_action(page, self.payload(page, action="queue-generate", item=item_id))
            self.assertIsNone(err, err)
            config = acts._load(page.parent / "scripts" / "config" / f"{out['run']}.yaml")
            self.assertEqual(config["goal"], "Say what to review")          # M4: the goal sentence, frozen
            self.assertEqual(config["criteria"][0]["value"], 160)
            snapshot = design_snapshot(page, board)
            self.assertEqual(snapshot["audit"], [])
            card = render_design(snapshot, "design", item_id)
            self.assertIn("the register changed after release", card)

    def test_a_changed_insight_is_queued_again_in_the_open(self):
        from tests.fixture_design_v2 import HANDOFF_REL
        with TemporaryDirectory() as td:
            board, page, _runs = v2_fixture(Path(td))
            item_id = self.new_item(page, basis="evidence-informed", evidence=f"evidence · {HANDOFF_REL}")
            perform_action(page, self.payload(page, action="commission-release", item=item_id, actor="JL", words="go"))
            first, err = perform_action(page, self.payload(page, action="queue-generate", item=item_id))
            self.assertIsNone(err, err)
            insight = (page.parent / HANDOFF_REL).resolve()
            insight.write_text(insight.read_text(encoding="utf-8") + "\nedited after the queue\n", encoding="utf-8")
            item = self.item(page, board, item_id)
            self.assertEqual((item["state"], item["waiting"]), ("queued run out of date", "you · queue again"))   # H3
            self.assertIn("data-action=requeue", render_design(design_snapshot(page, board), "design", item_id))
            out, err = perform_action(page, self.payload(page, action="requeue", item=item_id))
            self.assertIsNone(err, err)
            self.assertEqual(out["replaces"], first["run"])
            self.assertEqual(acts._load(page.parent / "results" / first["run"] / "runtime.yaml")["status"], "superseded")
            self.assertEqual(self.item(page, board, item_id)["state"], "generate queued")
            self.assertEqual(design_snapshot(page, board)["audit"], [])     # the records check accepts both

    def test_waiting_names_who_must_click(self):
        with TemporaryDirectory() as td:
            board, page, _runs = v2_fixture(Path(td))
            item_id = self.new_item(page)
            perform_action(page, self.payload(page, action="commission-release", item=item_id, actor="JL", words="go"))
            self.assertEqual(self.item(page, board, item_id)["waiting"], "you · queue the draft")        # H4
            _out, err = perform_action(page, self.payload(page, action="commission-release", item=item_id,
                                                          actor="JL", words="again"))
            self.assertIn('"commissioned"', err)                                                  # M14

    def test_a_hold_can_be_picked_up_again(self):
        with TemporaryDirectory() as td:
            board, page, _runs = v2_fixture(Path(td))
            item_id = self.new_item(page)
            perform_action(page, self.payload(page, action="commission-hold", item=item_id, actor="JL", words="wait"))
            item = self.item(page, board, item_id)
            self.assertEqual(item["state"], "commission held")
            self.assertIn("data-action=commission-release", render_design(design_snapshot(page, board), "design"))  # N3
            out, err = perform_action(page, self.payload(page, action="commission-release", item=item_id,
                                                         actor="JL", words="now go"))
            self.assertIsNone(err, err)
            self.assertEqual(self.item(page, board, item_id)["state"], "commissioned")

    def test_a_failed_draft_is_never_shown_as_passed(self):
        with TemporaryDirectory() as td:
            board, page, _runs = v2_fixture(Path(td))
            snapshot = design_snapshot(page, board)
            failed = next(i for i in snapshot["items"] if i["state"] == "generate failed")
            card = render_design(snapshot, "design", failed["id"]).split(f'id="item-{failed["id"]}"')[1].split("</section>")[0]
            # N4: the card says the draft failed. Since 0.11.3 it says it on the item's own
            # line ("✗ generate failed") instead of in a strip of Run chips (JL 260921).
            self.assertIn("generate failed", card)
            self.assertIn("✗", card)
            self.assertNotIn("pass", card.split("<div class=itembody>")[0])
            self.assertIsNone(failed["latest"])                                                   # N8: no failed draft shown

    def test_rule_marks_belong_to_the_draft_on_the_card(self):
        with TemporaryDirectory() as td:
            board, page, _runs = v2_fixture(Path(td), specs=[verified_spec()])
            item = self.item(page, board, "ITEM01")
            gen = next(r for r in item["runs"] if r["kind"] == "generate")
            ver = next(r for r in item["runs"] if r["kind"] == "verify")
            self.assertTrue(str(ver["targets"][0]["path"]).startswith(f'results/{gen["id"]}/'))
            card = render_design(design_snapshot(page, board), "design", "ITEM01")
            self.assertIn(f'independent review {ver["id"].split("_")[0]}', card)                   # N2
            self.assertIn("ready for Delivery", card)

    def test_a_legacy_ds_folder_is_refused(self):
        with TemporaryDirectory() as td:
            folder = Path(td) / "B-DesignBoard" / "2-DS-design" / "DS01-population-rx-review"
            folder.mkdir(parents=True)
            page = folder / "DS01-population-rx-review.md"
            page.write_text("# Old\nfolder-kind: design\n", encoding="utf-8")
            self.assertEqual(design_contract_status(page),
                             (False, "legacy 2-DS-design/DS* folder is not a current Design Folder"))  # L1
