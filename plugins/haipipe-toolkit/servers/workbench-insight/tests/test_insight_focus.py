"""An insight Job's Work on the focus page (insight_focus.py, b11 j01 s55): the Report's letters, each view ⚙️ Process
then 📊 Results with your signs first, sign the plan before the close, the grid's cells their next verb."""
from __future__ import annotations

import re
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "_host"))
sys.path.insert(0, str(HERE))
from host_paths import bootstrap  # noqa: E402
bootstrap()

from live import focus_page as FP  # noqa: E402
from live import insight_act as A  # noqa: E402
from live import insight_focus as IF  # noqa: E402
from live.insight_theme import THEME  # noqa: E402
import plan_c_fixture as F  # noqa: E402

HEADS = re.compile(r"<h3 class=fd-h>(.*?)</h3>")
GROUPS = re.compile(r"<h3 class=pb-group>(.*?)</h3>")


class InsightFocusTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name).resolve()
        self.board = F.make(self.root) / F.BOARD
        self.open = self.board / "j04_prototype-p2_data-demov3"          # open: its Runs planned, no page written
        self.closed = self.board / "j03_prototype-p2_data-demov2"        # closed: every page checked

    def tearDown(self):
        self.tmp.cleanup()

    def view(self, job: Path, key: str) -> str:
        return IF.job_work_views(job, self.root)["work-" + key][1]()

    def test_the_letters_of_the_report(self):
        self.assertEqual([n for n, _ in IF.job_work_views(self.open, self.root).values()],
                         ["Overall", "Grid", "vs previous"])
        self.assertEqual(IF.job_work_views(self.board, self.root), {})          # the Board is not a Job
        self.assertEqual(IF.job_work_views(self.open / "t03_K01_question-c", self.root), {})

    def test_each_view_is_process_then_results_your_signs_first(self):
        for key, _ in IF.VIEWS:
            html = self.view(self.open, key)
            self.assertEqual(GROUPS.findall(html), ["⚙️ Process", "📊 Results"], key)
            self.assertRegex(HEADS.findall(html)[0], r"^1 · 🙋 ", key)
            self.assertIn("Sign the plan", html, key)
            self.assertLess(html.index("Sign the plan"), html.index("Close the Job"), key)   # sign before close

    def test_the_close_waits_until_every_step_is_done(self):
        html = self.view(self.open, "overall")
        self.assertRegex(html, r"waits on the launch, the runs, the pages, the checks")
        self.assertIn("<button type=button class=fd-btn disabled>Close</button>", html)
        self.assertNotIn('data-post="/_board/insight-act"', html)
        self.assertNotIn("What the close freezes", html)              # shown once the close is yours to sign

    def test_an_unsigned_plan_waits_on_you(self):
        A.set_front(self.root / F.PROJECT / F.PROTO / "j02_p2" / "j02_p2.md", {"signed": ""})   # the plan p2
        html = self.view(self.open, "overall")
        self.assertIn("1 · 🙋 Waits on you", HEADS.findall(html))
        self.assertIn("Sign in the Prototype", html)
        self.assertIn("a preview: the plan is not signed", self.view(self.open, "overall"))

    def test_the_grid_cells_carry_their_next_verb(self):
        html = self.view(self.open, "grid")
        self.assertEqual(html.count("Questions × cuts"), 1)              # one grid, not two
        self.assertIn('class="pb-pill ">launch</span>', html.split("📊 Results")[1])   # a planned Run: launch it
        self.assertNotIn(">launch</span>", self.view(self.closed, "grid"))
        self.assertEqual(self.view(self.closed, "grid").count("<!--pb-prompt-->"), 0)   # nothing left to run

    def test_the_focus_page_shows_them_in_work(self):
        html = FP.render(THEME, self.root, self.open, "work", "work-grid")
        self.assertIn("Questions × cuts", html)
        self.assertIn("Overall", html)
        self.assertNotIn("Traceback", html)



class InsightLettersTest(unittest.TestCase):
    """The Board's Report and Work, the Job's Report, the Task's Report and Work (b11 j01 s51, s52, s54, s57, s58):
    a Report is its numbered sections only; a Work view is ⚙️ Process then 📊 Results."""
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name).resolve()
        self.board = F.make(self.root) / F.BOARD
        self.job = self.board / "j04_prototype-p2_data-demov3"
        self.task = next(p for p in sorted(self.job.iterdir()) if p.is_dir() and p.name.startswith("t"))

    def tearDown(self):
        self.tmp.cleanup()

    def report_ok(self, views, keys):
        self.assertEqual(list(views), keys)
        for _, build in views.values():
            html = build()
            self.assertNotIn("<h3 class=pb-group>", html)                 # no band in a Report
            self.assertNotIn("Nothing waits on you", html)
            self.assertRegex(html, r"<h3 class=fd-h>1 · ")

    def work_ok(self, views, keys):
        self.assertEqual(list(views), ["work-" + k for k in keys])
        for _, build in views.values():
            self.assertEqual(GROUPS.findall(build())[:2], ["⚙️ Process", "📊 Results"])

    def test_board(self):
        keys = ["answers", "questions", "jobs", "data", "handoff"]
        self.report_ok(IF.board_report_views(self.board, self.root), keys)
        work = IF.board_work_views(self.board, self.root)
        self.work_ok(work, keys)
        self.assertIn("🙋", HEADS.findall(work["work-answers"][1]())[0])     # your inbox first

    def test_job_report(self):
        views = IF.job_report_views(self.job, self.root)
        self.assertEqual(list(views), ["overall", "grid", "vs-previous"])
        for _, build in views.values():
            self.assertNotIn("<h3 class=pb-group>", build())

    def test_task(self):
        keys = ["answer", "by-cut", "across-jobs", "plan"]
        self.report_ok(IF.task_views(self.task, self.root, "report"), keys)
        work = IF.task_views(self.task, self.root, "work")
        self.work_ok(work, keys)
        self.assertNotIn("🙋", work["work-answer"][1]())                  # a Task never asks you

    def test_not_insight(self):
        self.assertEqual(IF.board_report_views(self.root, self.root), {})
        self.assertEqual(IF.task_views(self.root, self.root, "work"), {})

if __name__ == "__main__":
    unittest.main()
