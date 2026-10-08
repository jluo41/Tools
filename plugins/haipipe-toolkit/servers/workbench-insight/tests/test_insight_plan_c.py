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

# (Space, subspaces, run types), as b11's s11 · s12 · s13 SCREENS draw them; a "?" design run is left out
BOARD = {"Description": (["Map", "Prototype", "Dataset", "Partitions"], ["Add a data version", "Add a Job"]),
         "Idea Studio": ([], ["Draw the question map", "Add a topic"]),
         "Audience Report": (["Full", "part-a", "part-b", "Cross"], ["Update the coverage"]),
         "Work Details": (["All", "p1", "p2"], ["Add a Job", "Close a Job"]),
         "Runs": (["All", "soft", "from below"], ["Add a Job", "Update the coverage", "Check consistency"]),
         "Delivery": (["Handoff"], ["Write the counsel", "Draft the handoff"])}
JOB = {"Description": (["Prototype", "Dataset"], ["Open the release ↗"]),
       "Idea Studio": ([], ["Add a topic"]),
       "Audience Report": (["Full", "part-a", "part-b", "Cross"], ["Write a report", "Check a report"]),
       "Work Details": (["All", "hard", "soft"], ["Run a partition", "Check alignment", "Run the Job"]),
       "Runs": (["All", "hard", "soft", "launch", "power", "compare", "propose", "close"],
                ["Run the Job", "Run a partition", "Compare with j02", "Propose questions", "Close the Job"]),
       "Delivery": ([], [])}
TASK = {"Description": (["Question", "Records"], []),
        "Idea Studio": ([], ["Add a topic"]),
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
        self.job = self.board / "j03_p2_demov2"
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
        self.assertIn("j03_p2_demov2", page)
        self.assertIn("Add a Job", page)                 # an empty cell (p1 × v3)

    def test_the_job_tab_reads_its_pair_and_its_tree(self):
        desc = frame.render(THEME, self.root, self.job, "Description", "Dataset")
        self.assertIn("p2 × demo v2", frame.render(THEME, self.root, self.job, "Description", "Prototype"))
        for space in ("Audience Report", "Work Details", "Runs"):      # no band beside the tab (s12, 261007)
            self.assertNotIn("p2 × demo v2", spaces("Job", self.job, self.root, "")[space].html, space)
        self.assertIn("refused", frame.render(THEME, self.root, self.board / "j02_p1_demov2", "Description", "Dataset"))
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
