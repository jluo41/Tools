"""The base frame (servers/workbench/page/block_index_page/frame.py): levels, theme options, fill tags, level patterns,
the Block claim, the band and named question ids. Other parts: test_frame_page_task, _delivery, _studio,
_groups and _routes."""
from __future__ import annotations

import json
import os
import re
import shutil
import tempfile
import unittest
import zipfile
from html import unescape
from urllib.parse import parse_qs, unquote, urlparse
from pathlib import Path

from host_paths import bootstrap
bootstrap()

from live import frame  # noqa: E402
from live import task_draft  # noqa: E402
from live.frame_view import FrameMixin  # noqa: E402
from frame_fixtures import project, tiny_deck  # noqa: E402,F401


class LadderTest(unittest.TestCase):
    def test_a_folder_knows_its_level_its_chain_and_its_theme(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = project(tmp)
            task = root / "Project/tasks/b01_topic/j01_job/t01_task"
            self.assertEqual(frame.level_of(task), "Task")
            self.assertEqual(sorted(frame.chain(task, root)), ["Block", "Job", "Task"])
            self.assertEqual(frame.theme_of(task, root), "work")          # tasks/ reads as the work theme
            self.assertEqual([r["type"] for r in frame.runs_of(task)], ["fit", "build"])
            tools = root / "Tools" / "examples" / "b02_workbench"           # not inside a Project
            tools.mkdir(parents=True)
            (tools / "board.md").write_text("# b02\n")
            self.assertEqual(frame.theme_of(tools, root), "vanilla")



class OptionTest(unittest.TestCase):
    # A theme labels and groups the Job ▾ / Task ▾ options (Theme.option, b12 s32 261008)
    def test_a_theme_labels_and_groups_the_dropdown(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = project(tmp)
            job = root / "Project/tasks/b01_topic/j01_job"
            (job / "t02_other").mkdir()
            task = job / "t01_task"
            theme = frame.Theme(option=lambda f: (f"Task · {f.name[:3]}", "steps") if f.name == "t01_task" else None)
            row = frame._level_row(theme, root, task, "Task", "Description")
            self.assertIn('<optgroup label="steps">', row)
            self.assertIn(">Task · t01</option>", row)
            self.assertIn(">t02_other</option>", row)                  # None: the folder name as on disk (b10 s32-D15)
            plain = frame._level_row(frame.VANILLA, root, task, "Task", "Description")
            self.assertNotIn("optgroup", plain)
            self.assertIn('title="t01_task" selected>t01_task</option>', plain)     # the folder name, as on disk


class FillTagTest(unittest.TestCase):
    # a theme's Run name takes the folder's own tag, as the base's buttons do (b17 s32 261008)
    def test_a_placeholder_for_the_folders_level_is_filled(self):
        self.assertEqual(frame.fill_tag("run-plan-<tNN>", Path("x/t01_fit")), "run-plan-t01")
        self.assertEqual(frame.fill_tag("run-face-<jNN>", Path("x/t01_fit")), "run-face-<jNN>")
        self.assertEqual(frame.fill_tag("run-plan-<tNN>", Path("x/Design-A")), "run-plan-<tNN>")

    def test_a_themes_own_view_is_not_shadowed_by_a_page_view(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = project(tmp)
            task = root / "Project/tasks/b01_topic/j01_job/t01_task"
            out = task_draft.with_page_views({"Audience Report": frame.Space(subspaces=("Draft", "Report"), open="Draft")},
                                        "Task", task, root, "Draft", {"Description": "Face", "Audience Report": "Report",
                                        "Work Details": "Work", "Runs": "All", "Delivery": "Files"})
            self.assertEqual(out["Audience Report"].subspaces, ("Draft", "Report"))
            self.assertNotIn("page-view", out["Audience Report"].html)

    def test_the_work_themes_draft_shows_its_own_list(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = project(tmp)
            task = root / "Project/tasks/b01_topic/j01_job/t01_task"
            (task / "draft").mkdir()
            (task / "draft" / "t01-draft-v1.md").write_text("# plan\n")
            theme = frame.themes()["work"]
            out = frame.spaces_for(theme, "Task", task, root, "Draft")
            self.assertNotIn("page-view", out["Audience Report"].html)
            self.assertIn("t01-draft-v1.md", out["Audience Report"].html)

class LevelPatternTest(unittest.TestCase):
    # A theme names its own Job and Task folders (Theme.level_patterns, b03 261007): a paper's version
    # groups Ba-<desk>-Main and its Sections S-<desk>-<N>-<slug> climb the ladder unrenamed.
    def paper(self, tmp: str) -> Path:
        root = Path(tmp)
        board = root / "Project-X" / "paper" / "Paper-Demo"
        for d in (board / "Ba-Desk-Main" / "S-Desk-Main-1-Intro" / "draft", board / "A1-Story" / "StoryA-x",
                  board / "Ba-Desk-Main" / "notes"):
            d.mkdir(parents=True)
        (board / "board.md").write_text("# Paper\n\ndialect: paper\n")
        (board / "Ba-Desk-Main" / "S-Desk-Main-1-Intro" / "S-Desk-Main-1-Intro.md").write_text("# Intro\n")
        return root

    def test_a_theme_names_its_job_and_task_folders(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self.paper(tmp)
            board = root / "Project-X/paper/Paper-Demo"
            group, section = board / "Ba-Desk-Main", board / "Ba-Desk-Main/S-Desk-Main-1-Intro"
            saved = dict(frame._PATTERNS)
            frame._PATTERNS.clear()
            frame._PATTERNS.update({"paper": {"Job": r"^B[a-z]-", "Task": r"^S-"}, "work": {}})
            try:
                self.assertEqual(frame.level_of(board), "Block")
                self.assertEqual(frame.level_of(group), "Job")
                self.assertEqual(frame.level_of(section), "Task")
                self.assertIsNone(frame.level_of(board / "A1-Story"))           # not declared
                self.assertIsNone(frame.level_of(group / "notes"))              # under a Job, not a Section
                self.assertIsNone(frame.level_of(section / "draft"))            # inside a Task
                self.assertEqual(frame.children(board, "Block"), [group])
                self.assertEqual(frame.children(group, "Job"), [section])
                self.assertEqual(frame.chain(section, root), {"Task": section, "Job": group, "Block": board})
                self.assertEqual(frame.theme_of(section, root), "paper")
                page = frame.render(frame.Theme(name="paper", label="Paper"), root, section)
                self.assertIn("S-Desk-Main-1-Intro", page)
                self.assertNotIn('<select disabled aria-label="Task"', page)  # the Task tab is live
            finally:
                frame._PATTERNS.clear()
                frame._PATTERNS.update(saved)

    def test_a_theme_with_no_patterns_reads_as_before(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = project(tmp)
            block = root / "Project/tasks/b01_topic"
            (block / "Bz-group").mkdir()
            self.assertIsNone(frame.level_of(block / "Bz-group"))               # the work theme declares none
            self.assertEqual([p.name for p in frame.children(block, "Block")], ["j01_job"])


class ClaimTest(unittest.TestCase):
    # Theme.claims (261007): a theme reads a Block by what it holds, though its Theme folder names
    # another (a labeling Block with schema.yaml kept in tasks/); a failing check claims nothing.
    def test_a_theme_claims_a_block_by_what_it_holds(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = project(tmp)
            block = root / "Project/tasks/b01_topic"
            other = root / "Project/tasks/b02_schema"
            other.mkdir()
            (other / "board.md").write_text("# b02\n\nboard-kind: task-block\n")
            (other / "schema.yaml").write_text("question: placeholder\n")
            claiming = frame.Theme(name="labeling", claims=lambda b: (b / "schema.yaml").is_file())
            broken = frame.Theme(name="broken", claims=lambda b: 1 / 0)
            saved = frame.themes
            frame.themes = lambda: {"vanilla": frame.VANILLA, "broken": broken, "labeling": claiming}
            frame._CLAIMS.clear()
            try:
                self.assertEqual(frame.theme_of(other, root), "labeling")
                self.assertEqual(frame.theme_of(block, root), "work")          # no claim: its Theme folder
            finally:
                frame.themes = saved
                frame._CLAIMS.clear()


class BandTest(unittest.TestCase):
    def test_the_page_has_no_band_and_no_old_page_link(self):
        # JL 261007: "why I still have this? please remove that": the level tabs say where you are;
        # the path is the title's tooltip
        with tempfile.TemporaryDirectory() as tmp:
            root = project(tmp)
            page = frame.render(frame.themes()["work"], root, root / "Project/tasks/b01_topic")
            self.assertNotIn("class=band", page)
            self.assertNotIn("the old page", page)
            self.assertIn('<h1 title="Block · Project/tasks/b01_topic · Work theme · b01_topic" data-guide="🧪 Work · Guide · Block b01">', page)
            # the level row is the page index, the page's title under it (b03 s32-D13, JL 261008)
            self.assertLess(page.index('<nav class="row levels">'), page.index("<header class=page-title>"))
            self.assertIn("<span class=lv>Block b01 ·</span> Topic</h1>", page)   # its tag said once


class NamedQuestionIdsTest(unittest.TestCase):
    """A register cut by a word (Q-food-1, hai-report rule 1) reads like Q01 does (b51 261021): its report
    folder q-food-1_<topic>/ is found without a report: line, a Task its face and the register's work: both name is
    listed once, and a Job's Description shows its answers: line."""

    def test_a_named_id_finds_its_report_and_its_work_once(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            block = root / "Project" / "work" / "b51_store"
            task = block / "j01_food" / "t51_page"
            (block / "reports" / "q-food-1_input_output").mkdir(parents=True)
            task.mkdir(parents=True)
            (block / "board.md").write_text(
                "# Store\n\nboard-kind: task-block\n\n## Questions\n\n```yaml\nquestions:\n- id: Q-food-1\n"
                "  group: Food\n  title: input and output\n  question: What goes in and what comes back?\n"
                "  work:\n  - j01_food/t51_page\n```\n")
            (block / "reports" / "q-food-1_input_output" / "q-food-1_input_output.md").write_text(
                "# Food · input and output\n\nanswers: Q-food-1\nanswer-status: open\n\n## Opening\n\nNot yet.\n")
            (block / "j01_food" / "j01_food.md").write_text("# j01 · Food\n\ngoal: g\nclose: c\nanswers: Q-food-1\n")
            (task / "t51_page.md").write_text("# t51 · Page\n\nanswers: Q-food-1\n")
            html, _ = frame.question_rows("Block", block, root)
            self.assertIn("q-food-1_input_output.md", unescape(html).replace("%2F", "/"))
            work = re.search(r"<p class=q-work>(.*?)</p>", html).group(1)
            self.assertEqual(re.sub(r"<[^>]+>", "", work).count("j01_food/t51_page"), 1)
            desc = frame.vanilla("Job", block / "j01_food", root)["Description"].html
            self.assertIn("answers", desc)


if __name__ == "__main__":
    unittest.main()
