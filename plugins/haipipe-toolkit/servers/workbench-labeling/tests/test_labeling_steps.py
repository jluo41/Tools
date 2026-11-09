"""A 🧭 meaning and a 🛠 expression Task's focus pages (labeling_steps.py; b15 s58, stage 2), checked on the
placeholder Job that runs both loops with the real tools (labeling_example.py): every step draws from the Task's own
files, the interaction form opens through its route, the one send carries the answers, and the sign writes once."""
import io
import re
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "_host"))
from host_paths import bootstrap  # noqa: E402
bootstrap()
from live import focus_page as F, frame, labeling_focus as L, labeling_steps as S  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parent))
import labeling_example  # noqa: E402


class StepsPageTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory()
        cls.root = Path(cls.temp.name).resolve()
        cls.block = labeling_example.build(cls.root / "Project-X" / "labeling" / "b01_labeling_example")
        cls.job = cls.block / "j01_example_response_safety"
        cls.meaning, cls.expression = cls.job / "t03_example_meaning", cls.job / "t04_example_expression"
        cls.theme = frame.themes()["labeling"]

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def page(self, task, section="work", view=""):
        return L.render(self.theme, self.root, task, section, view)

    def test_the_two_loop_types_draw_their_steps(self):
        self.assertEqual(S.kind(self.meaning), "meaning")
        self.assertEqual(S.kind(self.expression), "expression")
        self.assertEqual(S.kind(self.job), "")
        html = self.page(self.meaning)
        for name in ("Frame", "Prepare", "Preferences", "Update"):
            self.assertIn(f">{name}<", html)
        self.assertIn('Frame<span class="vw fd-ok">agreed</span>', html)            # each step's state on its button
        self.assertIn('Preferences<span class="vw fd-you">waiting for you</span>', html)
        self.assertIn("its steps", html)                                            # Work holds the steps (s58-D02)

    def test_work_opens_where_the_person_is_needed(self):
        self.assertEqual(S.default_view(self.meaning), "preferences")          # Loop 2's form waits
        self.assertEqual(S.default_view(self.expression), "release")            # e01 ran Rewrite, Run, Evaluate

    def test_report_section_shows_results_only_and_work_shows_both(self):
        for view in ("frame", "prepare", "preferences", "update"):
            work, report = self.page(self.meaning, "work", view), self.page(self.meaning, "report", view)
            self.assertIn("⚙️ Process", work)
            self.assertIn("📊 Results", work)
            self.assertNotIn("⚙️ Process", report)
            self.assertIn("📊 Results", report)

    def test_report_step_leads_with_the_mind_map_then_the_report_and_its_cases(self):
        html = self.page(self.meaning, "work", "prepare")
        results = html[html.index("📊 Results"):]
        order = [results.index(t) for t in ("Guideline rules, as a mind map", "Typical cases", "Hard cases",
                                            "Random cases", "🙋 Interaction")]
        self.assertEqual(order, sorted(order))                                   # the reports' forms come last
        self.assertIn("m01 · approved", html)
        self.assertNotIn("Example Person", html)                                 # no person's name (settled 5)
        self.assertIn("asked in report-02, Q3", html)                          # a tag means this report's card
        self.assertNotIn(">Q5</span>", results.split("Typical cases")[0])        # no tag for the card that set a rule
        self.assertIn("waiting for you", html)
        self.assertIn("hidden until you judge it", html)
        self.assertIn("Use /haipipe-labeling-interaction on t03_example_meaning, Loop 2: prepare interaction report-02", html)

    def test_preferences_embeds_the_waiting_form_and_sends_answers_with_the_prompt(self):
        html = self.page(self.meaning, "work", "preferences")
        rel = (self.meaning / "runs" / "r08_collect_report_m02" / "r08_collect_report_m02.html").relative_to(self.root)
        src = f'src="/_board/labeling/form/{rel.as_posix()}"'
        self.assertIn(src, html)
        self.assertGreater(html.index(src), html.index("📊 Results"))   # the form is 🙋 Interaction's, never Process's
        self.assertIn(f'class="ls-send" data-form="/_board/labeling/form/{rel.as_posix()}"', html)
        self.assertIn("save my answers to report-02", html)
        self.assertIn("Not saved yet", html)                    # Results: the decision record, once the chat saves it
        self.assertNotIn("pick below", html)                    # no instruction bar (review C3 r01)

    def test_update_shows_the_signed_guideline_its_changes_and_history(self):
        html = self.page(self.meaning, "work", "update")
        self.assertIn("✅ m01 approved ", html)
        self.assertIn("What your answers changed", html)
        changes = (self.meaning / "runs" / "r05_update_m01" / "result" / "changes.md").read_text(encoding="utf-8")
        first = next(ln[2:] for ln in changes.splitlines() if ln.startswith("- "))
        self.assertIn(frame.esc(S._label_words(first)), html)                 # the row names its card already
        self.assertNotIn("r05_update_m01:", html.split("What your answers changed", 1)[1].split("Where it goes", 1)[0])
        self.assertIn("m01 ← r04_collect_report_m01", html)
        self.assertIn("r04 Q3", html)                                           # Update tags: the card that set it

    def test_expression_runs_only_under_a_signed_meaning(self):
        html = self.page(self.expression, "work", "evaluate")
        self.assertNotIn("approved meaning m01", html)                          # said once, where Rewrite reads it
        self.assertIn("approved meaning m01", self.page(self.expression, "work", "rewrite"))
        self.assertIn("Round report e01", html)
        self.assertIn("wrong label", html)
        self.assertIn("small model A", html)
        self.assertIn("Use /haipipe-labeling-expression on t04_example_expression", self.page(self.expression, "work", "rewrite"))

    def test_expression_waits_without_a_signed_meaning(self):
        signed = self.meaning / "meaning" / "m01.approved.yaml"
        kept = signed.read_text(encoding="utf-8")
        signed.unlink()
        try:
            self.assertIn("No approved meaning yet", self.page(self.expression, "work", "rewrite"))
        finally:
            signed.write_text(kept, encoding="utf-8")

    def test_a_labeling_form_opens_through_its_route_never_as_a_static_file(self):
        form = self.meaning / "runs" / "r08_collect_report_m02" / "r08_collect_report_m02.html"
        self.assertTrue(frame._file_url(form, self.root).startswith("/_board/labeling/form/"))
        h = self.handler()
        h.path = frame._file_url(form, self.root)
        h.labeling_form_view()
        self.assertEqual(h.status, 200)
        self.assertIn(b"Loop 2 report", h.wfile.getvalue())
        for other in ("report.json", "question_collection.md", "../../t03_example_meaning.md"):
            h = self.handler()
            h.path = frame._file_url(form, self.root).rsplit("/", 1)[0] + "/" + other
            h.labeling_form_view()
            self.assertEqual(h.status, 404, other)

    def test_the_sign_writes_once_and_only_a_made_version(self):
        h = self.handler()
        rel = self.meaning.relative_to(self.root).as_posix()
        self.assertEqual(h.labeling_approve({"task": rel, "version": "m01", "by": "Someone"})[0], 409)   # signed already
        self.assertEqual(h.labeling_approve({"task": rel, "version": "m02", "by": "Someone"})[0], 409)   # not made yet
        self.assertEqual(h.labeling_approve({"task": "../x", "version": "m01", "by": "Someone"})[0], 400)
        made = self.meaning / "meaning" / "m02.mindmap.md"
        made.write_text((self.meaning / "meaning" / "m01.mindmap.md").read_text(encoding="utf-8"), encoding="utf-8")
        try:
            h.headers["Origin"] = "https://other.test"
            self.assertEqual(h.labeling_approve({"task": rel, "version": "m02", "by": "Someone"})[0], 403)
            del h.headers["Origin"]
            status, body = h.labeling_approve({"task": rel, "version": "m02", "by": "Someone"})
            self.assertEqual(status, 200, body)
            self.assertTrue((self.meaning / "meaning" / "m02.approved.yaml").is_file())
        finally:
            made.unlink()
            (self.meaning / "meaning" / "m02.approved.yaml").unlink(missing_ok=True)

    def test_every_view_ends_in_its_own_interaction(self):
        """Settled 3 (round 2): 🙋 Interaction is the last section of every Report and Work view, with that step's own
        forms; the grey session line under a prompt is gone."""
        own = {"frame": "r01_collect_frame_decisions", "prepare": "r08_collect_report_m02",
               "preferences": "r08_collect_report_m02", "update": None}
        for view, run in own.items():
            for section in ("report", "work"):
                with self.subTest(view=view, section=section):
                    html = self.page(self.meaning, section, view)
                    bars = re.findall(r"<h3 class=fd-h>\d+ · ([^<]*)", html)
                    self.assertEqual(bars[-1], "🙋 Interaction")
                    last = html[html.rindex("🙋 Interaction</h3>") if "🙋 Interaction</h3>" in html
                                else html.rindex("🙋 Interaction<span"):]
                    if run:
                        self.assertIn(run, last)
                    else:
                        self.assertIn("Nothing asked yet.", last)
                    self.assertNotIn("<p class=pb-sess>", html)
        frame_view = self.page(self.meaning, "work", "frame")
        self.assertNotIn("r08_collect_report_m02", frame_view)            # another step's form stays in its own view

    def test_each_loop_box_opens_that_loop(self):
        html = self.page(self.meaning, "report", "update")
        strip = html.split("class=ls-turns>", 1)[1].split("</div>", 1)[0]
        self.assertIn('data-pop="Loop 1"', strip)                          # Loop 1's answered form, in the pop-out
        self.assertIn("r04_collect_report_m01", strip)

    def test_a_release_form_waits_in_releases_own_interaction_and_opens(self):
        """Round 2: an expression Task's form (how a release is used) is Release's 🙋 Interaction, its first question
        under the closed bar; it opens through the form route; the Job's Findings shows it beside the release."""
        run = self.expression / "runs" / "r90_collect_release_choices"
        run.mkdir()
        try:
            (run / "run.yaml").write_text("run: r90_collect_release_choices\nkind: hard\ntype: collect\nview: findings\nstatus: waiting\n")
            (run / "question_collection.md").write_text(
                "# Release Use Choices\n\nfor: placeholder\n\n## Q1 · Serving executor\nWhy it matters.\n"
                "**Which executor labels new items?**\n- [x] A · one\n- [ ] B · another\nWhy A: placeholder.\n")
            form = run / "r90_collect_release_choices.html"
            form.write_text("<p>placeholder release form</p>\n")
            release = self.page(self.expression, "work", "release")
            last = re.findall(r"<h3 class=fd-h>\d+ · ([^<]*)(<span[^>]*>[^<]*</span>)?</h3>(<p class=fd-wait>[^<]*</p>)?", release)[-1]
            self.assertEqual(last[0], "🙋 Interaction")
            self.assertIn("1 waits for you", last[1])
            self.assertIn("🙋 Release Use Choices: Q1 · Serving executor", last[2])
            self.assertNotIn("r90_collect_release_choices", self.page(self.expression, "work", "rewrite"))
            h = self.handler()
            h.path = frame._file_url(form, self.root)
            h.labeling_form_view()
            self.assertEqual(h.status, 200)                                   # every Task kind's forms open (round 2)
            self.assertIn(b"placeholder release form", h.wfile.getvalue())
            findings = L.render(self.theme, self.root, self.job, "report", "findings")
            self.assertIn("r90_collect_release_choices", findings.split("🙋 Interaction", 1)[1])
            standing = L.render(self.theme, self.root, self.job, "report", "standing")
            self.assertNotIn("r90_collect_release_choices.html", standing.split("🧭 Around the Work", 1)[1])
            work = L.render(self.theme, self.root, self.job, "work", "standing")
            self.assertIn("View BJTR", work)
            self.assertNotIn("🚧 Next steps", work)
            all_forms = L.render(self.theme, self.root, self.job, "interactions")
            self.assertIn(frame._file_url(form, self.root), all_forms)
            self.assertIn("Release Use Choices", all_forms)
        finally:
            import shutil
            shutil.rmtree(run)

    def test_a_job_findings_lead_with_its_release(self):
        html = L.render(self.theme, self.root, self.job, "report", "findings")
        bars = re.findall(r"<h3 class=fd-h>\d+ · ([^<]*)", html)
        self.assertTrue(bars[0].startswith("🏷 Final labels"), bars)
        self.assertIn("🧭 Around the Work", html)
        self.assertIn("🙋 Interactions", html)

    def test_every_step_holds_its_prompt_inside_its_closed_bar(self):
        """Round 4: a prompt card and its notes box sat open under every closed Process bar; now each step is one
        closed section holding its flow, your part and its prompt."""
        for task in (self.meaning, self.expression):
            for key, *_ in S.STEPS[S.kind(task)]:
                with self.subTest(task=task.name, view=key):
                    process = self.page(task, "work", key).split("⚙️ Process", 1)[1].split("📊 Results", 1)[0]
                    outside = re.sub(r"<section class=fd-sec>.*?</section>", "", process, flags=re.S)
                    self.assertNotIn("pb-prompt", outside)
                    self.assertNotIn("ls-bar", outside)
                    self.assertNotIn("ls-by", process)                        # a sign needs no name (settled 5)

    def test_an_answered_loop_says_when_its_answers_came_back(self):
        saved = self.root / "answer_collection.md"
        saved.write_text("# answers\n\nreceived: 2026-11-04 21:40\n")
        self.assertEqual(S._received(saved), "2026-11-04 21:40")         # the file's own line, never its time on disk
        saved.write_text("# answers\n")
        self.assertRegex(S._received(saved), r"^\d{4}-\d\d-\d\d \d\d:\d\d$")

    def test_a_signed_release_with_waiting_choices_says_both_and_is_delivered(self):
        """Round 4: Release said only "released" while its choices waited, and Delivery said "nothing handed over
        yet" beside a signed release; a final label's card opens its question."""
        import shutil
        run, form = self.expression / "runs" / "r91_release_e01", self.expression / "runs" / "r92_collect_release_choices"
        report = next(r for r in sorted((self.meaning / "runs").glob("r*_collect_report_*")))
        cite = report.name.split("_", 1)[0] + " Q2"
        try:
            (run / "result").mkdir(parents=True)
            (run / "run.yaml").write_text("run: r91_release_e01\nkind: soft\ntype: release\nstatus: done\n")
            (run / "result" / "criteria.json").write_text('[{"name": "Quality floor", "state": "met"}]')
            (run / "result" / "final_labels.jsonl").write_text(
                '{"item_id": "ex-01", "label": "safe", "decided_by": "you kept it", "cites": "%s", "agree": true}\n' % cite)
            (run / "result" / "final_labels.md").write_text("# Final labels\n")
            (run / "result" / "signed.yaml").write_text("round: e01\nby: \"a person\"\nat: 2026-11-04 21:44\n")
            form.mkdir()
            (form / "run.yaml").write_text("run: r92_collect_release_choices\nkind: hard\ntype: collect\nstatus: waiting\n")
            (form / "question_collection.md").write_text(
                "# Release use choices\n\nfor: placeholder\n\n## Q1 · Serving executor\nWhy.\n**Which one?**\n"
                "- [x] A · one\n- [ ] B · two\n")
            (form / "r92_collect_release_choices.html").write_text("<p>placeholder</p>\n")
            self.assertEqual(S.states(self.expression, self.root)["release"], ("released · 1 wait", "you"))
            self.assertEqual(S.states(self.expression)["release"], ("released", "ok"))
            release = self.page(self.expression, "work", "release")
            self.assertIn('<span class="vw fd-you">released · 1 wait</span>', release)
            self.assertIn(f'#Q2" title="{report.name}, Q2">{cite}</a>', release)   # the card opens its question
            for page in (self.job, self.block, self.expression):
                with self.subTest(page=page.name):
                    delivery = L.render(self.theme, self.root, page, "delivery", "")
                    self.assertIn("Final labels, release e01", delivery)
                    self.assertIn("final_labels.md", delivery)
                    self.assertIn("what it has handed over", dict((k, w) for k, _, w in L.base_rail(page, self.root))["delivery"])
        finally:
            shutil.rmtree(run, ignore_errors=True)
            shutil.rmtree(form, ignore_errors=True)

    def test_a_block_row_says_how_many_tasks_are_done_as_its_job_does(self):
        block = L.render(self.theme, self.root, self.block, "report", "standing")
        n = len([t for t in frame.children(self.job, "Job")])
        done = sum(F.state_kind(F.state_label(F.read_face(t, self.root)["state"])) == "✅ done"
                   for t in frame.children(self.job, "Job"))
        row = block.split(f'data-pop="{self.job.name}"', 1)[1].split("</summary>", 1)[0]
        self.assertIn(f"<small>{done} of {n} done</small>", row)
        self.assertIn(f"{done} of {n} done", L.render(self.theme, self.root, self.job, "report", "standing"))
        self.assertIn("_<wbr>", block.split("<h1>", 1)[1].split("</h1>", 1)[0])   # a phone breaks the name at words

    def handler(self):
        from live.labeling import LabelingMixin

        class Handler(LabelingMixin):
            def send_response(self, status): self.status = status
            def send_error(self, status, *_): self.status = status
            def send_header(self, *args): pass
            def end_headers(self): pass
            def reply(self, status, body): self.status, self.body = status, body
        h = Handler()
        h.root, h.headers, h.wfile = self.root, {"Host": "example.test"}, io.BytesIO()
        return h


if __name__ == "__main__":
    unittest.main()
