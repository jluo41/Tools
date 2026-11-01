"""A 🧭 meaning and a 🛠 expression Task's focus pages (labeling_steps.py; b15 s58, stage 2), checked on the
placeholder Job that runs both loops with the real tools (labeling_example.py): every step draws from the Task's own
files, the interaction form opens through its route, the one send carries the answers, and the sign writes once."""
import io
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "_host"))
from host_paths import bootstrap  # noqa: E402
bootstrap()
from live import frame, labeling_focus as L, labeling_steps as S  # noqa: E402

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
        for name in ("Frame", "Report", "Preferences", "Update"):
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
        order = [results.index(t) for t in ("Guideline rules, as a mind map", "Interaction report", "Typical cases",
                                            "Hard cases", "Random cases")]
        self.assertEqual(order, sorted(order))
        self.assertIn("approved by Example Person", html)
        self.assertIn("asked in report-02, Q3", html)                          # a tag means this report's card
        self.assertNotIn(">Q5</span>", results.split("Interaction report")[0])  # no tag for the card that set a rule
        self.assertIn("waiting for you", html)
        self.assertIn("hidden until you judge it", html)
        self.assertIn("Use /haipipe-labeling-interaction on t03_example_meaning, Loop 2: prepare interaction report-02", html)

    def test_preferences_embeds_the_waiting_form_and_sends_answers_with_the_prompt(self):
        html = self.page(self.meaning, "work", "preferences")
        rel = (self.meaning / "runs" / "r08_collect_report_m02" / "r08_collect_report_m02.html").relative_to(self.root)
        self.assertIn(f'src="/_board/labeling/form/{rel.as_posix()}"', html)
        self.assertIn("class=\"ls-send\"", html)
        self.assertIn("save my answers to report-02", html)
        self.assertIn("Not saved yet", html)                    # Results: the decision record, once the chat saves it
        self.assertNotIn("pick below", html)                    # no instruction bar (review C3 r01)

    def test_update_shows_the_signed_guideline_its_changes_and_history(self):
        html = self.page(self.meaning, "work", "update")
        self.assertIn("✅ m01 approved by Example Person", html)
        self.assertIn("What your answers changed", html)
        changes = (self.meaning / "runs" / "r05_update_m01" / "result" / "changes.md").read_text(encoding="utf-8")
        first = next(ln[2:] for ln in changes.splitlines() if ln.startswith("- "))
        self.assertIn(frame.esc(first), html)
        self.assertIn("m01 ← r04_collect_report_m01", html)
        self.assertIn("r04 Q3", html)                                           # Update tags: the card that set it

    def test_expression_runs_only_under_a_signed_meaning(self):
        html = self.page(self.expression, "work", "evaluate")
        self.assertIn("approved meaning m01", html)
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
