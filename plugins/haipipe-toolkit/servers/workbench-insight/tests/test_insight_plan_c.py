"""The insight theme on plan C (b11 s11 · s12 · s13, 261007): the Board, a Job and a Task drawn from a
placeholder plan-C Project (plan_c_fixture.py), plus today's layout (a Block in tasks/ claimed by
`workbench: insight`). Every Space's subviews and run types as the design draws them, its second row of
buttons, and every ↗ in a page opening a file that exists."""
from __future__ import annotations

import json
import re
import sys
import tempfile
import unittest
from pathlib import Path
from urllib.parse import parse_qs, unquote, urlparse

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "_host"))
sys.path.insert(0, str(HERE))
from host_paths import bootstrap  # noqa: E402
bootstrap()

from live import frame  # noqa: E402
from live.insight_theme import THEME, spaces  # noqa: E402
import plan_c_fixture as F  # noqa: E402

# (Space, subspaces, run types), as b11's s11 · s12 · s13 SCREENS draw them and the run cards
# (haipipe-insight-workflow/ref/run-cards.md) name them; a "?" design run is left out
BOARD = {"Description": (["Map", "Prototype", "Dataset", "Partitions"], ["Add a data version", "Add a Job"]),
         "Idea Studio": ([], ["Draw the question map", "Add a topic"]),
         "Audience Report": (["Full", "part-a", "part-b", "Cross"], ["Update the coverage", "Propose questions"]),
         "Work Details": (["All", "p1", "p2"], ["Add a Job", "Close a Job"]),
         "Runs": (["All", "soft", "from below"], ["Add a Job", "Update the coverage", "Check consistency"]),
         "Delivery": (["Handoff"], ["Write the counsel", "Draft the handoff"])}
JOB = {"Description": (["Prototype", "Dataset"], ["Open the release ↗"]),
       "Idea Studio": ([], ["Draw the question map", "Add a topic"]),  # the Block's Studio (b03 s02-D09)
       "Audience Report": (["Full", "part-a", "part-b", "Cross"], ["Write the Data report", "Write the Information report",
                                                               "Write the Knowledge report", "Write the Wisdom report",
                                                               "Check a report"]),
       "Work Details": (["All", "hard", "soft"], ["Run the Job", "Run a partition", "Check alignment"]),
       "Runs": (["All", "hard", "soft", "launch", "power", "compare", "propose", "close"],
                ["Run the Job", "Measure the power", "Run a partition", "Compare with the Job before",
                 "Propose questions", "Close the Job"]),
       "Delivery": ([], [])}
TASK = {"Description": (["Question", "Records"], []),
        "Idea Studio": ([], ["Draw the question map", "Add a topic"]),  # the Block's Studio (b03 s02-D09)
        "Audience Report": (["Table", "Reading"], ["Write the Knowledge report", "Check a report"]),
        "Work Details": (["Partitions"], ["Run a partition", "Check alignment"]),
        "Runs": (["All", "hard", "soft"], ["Run a partition", "Check alignment"]),
        "Delivery": ([], [])}
OLD_CLASSES = ("hl-row", "class=lead", "class=pill", "class=pane", "class=shell", "gateset")


class PlanCTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.board = F.make(self.root) / F.BOARD
        self.job = self.board / "j03_prototype-p2_data-demov2"
        self.task = self.job / "t03_K01_question-c"

    def tearDown(self):
        self.tmp.cleanup()

    def frame_of(self, folder, sub=""):
        data = json.loads(frame.frame_json(THEME, self.root, folder, sub))
        return {s["name"]: s for s in data["spaces"]}

    def test_every_level_is_the_insight_theme(self):
        for folder in (self.board, self.job, self.task):
            self.assertEqual(frame.theme_of(folder, self.root), "insight")

    def test_each_level_serves_the_designed_subviews_and_run_types(self):
        for folder, want in ((self.board, BOARD), (self.job, JOB), (self.task, TASK)):
            got = self.frame_of(folder)
            for space, (subs, runs) in want.items():
                with self.subTest(level=folder.name, space=space):
                    self.assertEqual(got[space]["subspaces"], subs)
                    self.assertEqual(got[space]["run_doing"], runs)          # each button's words
                    for name in got[space]["run_types"]:                         # named by the Run it makes
                        self.assertRegex(name, r"^(run-|rNN_)|↗$")

    def test_the_second_rows(self):
        board = frame.render(THEME, self.root, self.board, "Audience Report", "part-a/Consistency")
        self.assertIn("Reading:", board)
        self.assertIn('class="tab on" href', board)
        self.assertIn("Consistency", board)
        job = frame.render(THEME, self.root, self.job, "Audience Report", "part-a/vs previous")
        self.assertIn("Period:", job)
        self.assertIn("1 new question · 1 new finding · 2 held · 1 changed · 0 dropped · 1 not comparable", job)

    def test_the_map_crosses_the_two_clocks(self):
        page = frame.render(THEME, self.root, self.board, "Description", "Map")
        self.assertIn("j03_prototype-p2_data-demov2", page)
        self.assertIn("Add a Job", page)                 # an empty cell (p1 × v3)

    def test_the_job_menu_shows_the_folder_name(self):
        """JL 261012: "I just want to show the job folder name": each Job ▾ option is the folder as it is on disk."""
        page = frame.render(THEME, self.root, self.job, "Description", "Dataset")
        options = re.findall(r'<option value="[^"]*" title="(j\d+_[^"]+)"[^>]*>([^<]+)</option>', page)
        self.assertEqual([n for n, _ in options], [j[0] for j in F.JOBS])
        self.assertEqual([label for _, label in options], [j[0] for j in F.JOBS])

    def test_the_job_tab_reads_its_pair_and_its_tree(self):
        desc = frame.render(THEME, self.root, self.job, "Description", "Dataset")
        self.assertIn("AP2 × F2", frame.render(THEME, self.root, self.job, "Description", "Prototype"))
        for space in ("Audience Report", "Work Details", "Runs"):      # no band beside the tab (s12, 261007)
            self.assertNotIn("AP2 × F2", spaces("Job", self.job, self.root, "")[space].html, space)
        self.assertIn("refused", frame.render(THEME, self.root, self.board / "j02_prototype-p1_data-demov2", "Description", "Dataset"))
        tree = frame.render(THEME, self.root, self.job, "Work Details", "")
        self.assertIn("t03_K01_question-c", tree)
        self.assertIn("r04_cross", tree)

    def test_the_still_open_points_are_not_decided(self):
        job = frame.render(THEME, self.root, self.job, "Description", "Prototype")
        self.assertIn("not set (still open)", job)        # what "held" means
        handoff = spaces("Block", self.board, self.root, "Handoff")["Delivery"].html   # the Space itself
        self.assertNotIn("stale", handoff)

    def test_every_pop_out_opens_a_file_that_exists(self):
        seen = 0
        for folder, want in ((self.board, BOARD), (self.job, JOB), (self.task, TASK)):
            for space, (subs, _) in want.items():
                for sub in [""] + subs:
                    page = frame.render(THEME, self.root, folder, space, sub)
                    for href in re.findall(r'data-pop="[^"]*" href="([^"]+)"', page):
                        q = parse_qs(urlparse(href.replace("&amp;", "&")).query)
                        if "path" not in q or not href.startswith("/_board/page"):
                            continue
                        seen += 1
                        with self.subTest(level=folder.name, space=space, sub=sub, href=href):
                            self.assertTrue((self.root / unquote(q["path"][0]).lstrip("/")).is_file())
        self.assertGreater(seen, 40)

    def test_base_classes_only(self):
        for folder, want in ((self.board, BOARD), (self.job, JOB), (self.task, TASK)):
            for space in want:
                page = frame.render(THEME, self.root, folder, space, "")
                for old in OLD_CLASSES:
                    self.assertNotIn(old, page)


class OverallReportTest(unittest.TestCase):
    """JL 261012: "before the Full, we should have a Overall Report ... we can click and read it". A release that asks
    an Executive question (X) puts an Overall Report button before Full at the Job and the Board: its X pages as one
    document, each (K01 · t03) a link to that Task's page; no cut's table lists X."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        base = F.make(self.root)
        self.board, rel = base / F.BOARD, base / F.PROTO / "j02_p2"
        self.job = self.board / "j03_prototype-p2_data-demov2"
        F._write(rel / "t07_X01_what-we-ran" / "question.md", F._front(
            {"id": "X01", "level": "executive", "name": "What We Ran", "question": "what did we run?"}, "# What We Ran\n"))
        rows = F.yaml.safe_load((rel / "release.yaml").read_text())
        rows["questions"]["X01"] = {"task": "t07_X01_what-we-ran", "change": "new"}
        (rel / "release.yaml").write_text(F.yaml.safe_dump(rows, sort_keys=False))
        F._write(self.job / "t07_X01_what-we-ran" / "t07_X01_what-we-ran.md", F._front(
            {"question": "X01", "answer-status": "written", "answer": "<the plain answer>", "how-sure": "<how sure>",
             "figures": [{"name": "funnel", "title": "<the outcome>", "kind": "bars",
                          "table": "t03_K01_question-c/runs/r01_full/result/rates.csv"},
                         {"name": "not-drawn", "title": "<another outcome>", "kind": "dots",
                          "table": "t01_D01_question-a/runs/r01_full/result/rates.csv"}]},
            "# X01 · What We Ran\n\n**The ask**: <the ask>\n\n## Answer\n\n1. <a point> (K01 · t03).\n\n"
            "## What it rests on\n\n- <a limit> (D01 · t01).\n"))
        F._write(self.board / "delivery" / self.job.name / "overall-report.pdf", "%PDF placeholder")
        F._write(self.board / "delivery" / self.job.name / "figures" / "X01-funnel.png", "<png placeholder>")

    def tearDown(self):
        self.tmp.cleanup()

    def test_the_overall_report_comes_before_full(self):
        for folder, runs in ((self.job, ["Write the overall report", "Check a report"]), (self.board, ["Open the latest Job ↗"])):
            got = {s["name"]: s for s in json.loads(frame.frame_json(THEME, self.root, folder, ""))["spaces"]}["Audience Report"]
            with self.subTest(level=folder.name):
                self.assertEqual(got["subspaces"], ["Overall Report", "Full", "part-a", "part-b", "Cross"])
                self.assertEqual(got["run_doing"], runs)

    def test_it_reads_as_one_document_with_its_cites_as_links(self):
        for folder in (self.job, self.board):
            page = spaces("Job" if folder == self.job else "Block", folder, self.root, "")["Audience Report"].html
            with self.subTest(level=folder.name):
                self.assertIn("<article class=report-doc>", page)
                self.assertIn("1. What We Ran", page)
                self.assertIn("&lt;the plain answer&gt;", page)
                self.assertIn("t03_K01_question-c", page)                      # (K01 · t03) opens that Task's page
                self.assertIn(">K01 · t03</a>)", page)
                self.assertIn("overall-report.pdf", page)
                self.assertNotIn("Reading:", page)
                self.assertNotIn("Period:", page)

    def test_each_answer_shows_its_figure_and_the_top_shows_them_all(self):
        """JL 261013: "figures to show it to quickly get the outcome": the outcome above each picture, under its
        answer and in the At a glance grid; a figure not drawn yet says so and names its source."""
        page = spaces("Job", self.job, self.root, "")["Audience Report"].html
        png = f"/Project-InsightDemo/{F.BOARD}/delivery/{self.job.name}/figures/X01-funnel.png"
        self.assertIn("<nav class=rep-glance>", page)
        self.assertIn(f'<b>&lt;the outcome&gt;</b><img src="{png}"', page)              # the glance card
        self.assertIn("<figure class=rep-fig><figcaption>&lt;the outcome&gt;</figcaption>", page)
        self.assertIn(">K01 · t03</a>)", page)                                        # its source, a link
        self.assertIn("Figure not drawn yet: ref/overall_report.py draws it from (D01 · t01)", page)

    def test_no_cut_lists_the_executive_questions(self):
        for folder, level in ((self.job, "Job"), (self.board, "Block")):
            page = spaces(level, folder, self.root, "Full")["Audience Report"].html
            with self.subTest(level=folder.name):
                self.assertIn("question-K01", page)
                self.assertNotIn("question-X01", page)
                self.assertNotIn("Executive", page)


class TodaysLayoutTest(unittest.TestCase):
    """A Block in tasks/ that says `workbench: insight` (as b52 does) opens in the insight theme."""

    def test_a_tasks_block_with_workbench_insight_is_claimed(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            block = root / "Project-Demo" / "tasks" / "b52_demo_dikw"
            block.mkdir(parents=True)
            (block / "board.md").write_text("# b52 · demo\n\nboard-kind: task-block\nworkbench: insight\n", encoding="utf-8")
            self.assertEqual(frame.theme_of(block, root), "insight")


if __name__ == "__main__":
    unittest.main()
