"""The design theme on the base frame: a Block made by design_ladder.py, read at each level."""
from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

HOST = Path(__file__).resolve().parents[2] / "_host"
sys.path.insert(0, str(HOST))
from host_paths import bootstrap  # noqa: E402
bootstrap()

from live import frame  # noqa: E402
from live.design_theme import THEME  # noqa: E402

SKILL = Path(__file__).resolve().parents[3] / "skills/2_theme/design/haipipe-design/scripts/carry_over"
sys.path.insert(0, str(SKILL))
import design_ladder_by_method as design_ladder  # noqa: E402   the old `_by-<method>` scaffold, which this test reads


def demo(tmp: str) -> Path:
    """A design Block: one goal by two methods, three designs under the first, a generate Run and a verify."""
    root = Path(tmp)
    block = root / "Project" / "designs" / "b01_demo_app"
    design_ladder.main(["block", str(block), "--title", "Demo application"])
    job = block / "j01_reminder_by-insight"
    design_ladder.main(["job", str(job), "--n", "3", "--goal", "a reminder for <who>"])
    design_ladder.main(["job", str(block / "j02_reminder_by-goal"), "--n", "3"])
    design_ladder.main(["run", str(job), "generate", "--n", "3"])
    for k, state in enumerate(("passed", "verify", "revise"), start=1):
        t = job / f"t0{k}_d0{k}_option-{k}"
        design_ladder.main(["task", str(t)])
        md = t / f"{t.name}.md"
        md.write_text(md.read_text().replace("state: draft", f"state: {state}")
                      .replace("<the design, word for word>", f"<message {k}>"))
        (t / "elements.yaml").write_text(f"- element: ask\n  words: <ask {k}>\n  from: internal\n  source: W-01\n"
                                         f"  thinking: reasoned\n  because: <why>\n  changed: {str(k != 2).lower()}\n"
                                         "- element: sender\n  words: <sender>\n  from: requirements\n  changed: false\n")
    design_ladder.main(["run", str(job / "t01_d01_option-1"), "verify"])
    return root


def main(page: str) -> str:
    """The open Space's content only (the level row's menus list every sibling)."""
    body = page.split("<div class=space-main>", 1)[1]
    return body.split("</div><aside", 1)[0].split('<div class="runs', 1)[0].split("<section class=runs-panel", 1)[0]


def data(root: Path, folder: Path, space: str = "", sub: str = "") -> dict:
    return {s["name"]: s for s in json.loads(frame.frame_json(THEME, root, folder, sub))["spaces"]}


class DesignThemeTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = demo(self.tmp.name)
        self.block = self.root / "Project/designs/b01_demo_app"
        self.job = self.block / "j01_reminder_by-insight"

    def tearDown(self):
        self.tmp.cleanup()

    def test_the_scaffold_makes_each_level_and_never_overwrites(self):
        self.assertTrue((self.job / "method.md").is_file())
        self.assertTrue((self.job / "runs/r01_generate_3/run.yaml").is_file())
        self.assertTrue((self.job / "t01_d01_option-1/runs/r01_verify_d01/result").is_dir())
        self.assertEqual(design_ladder.main(["job", str(self.job)]), [])          # all there: nothing made
        self.assertEqual(frame.theme_of(self.job, self.root), "design")

    def test_block_groups_its_jobs_by_method_family(self):
        sp = data(self.root, self.block)
        self.assertEqual(sp["Description"]["subspaces"], ["Goal list", "Theory", "Rules"])
        self.assertEqual(sp["Work Details"]["subspaces"], ["All", "Internal", "External", "Goal Only"])
        page = main(frame.render(THEME, self.root, self.block, "Work Details", "Internal"))
        self.assertIn("j01_reminder_by-insight", page)
        self.assertNotIn("j02_reminder_by-goal", page)                         # Goal Only, filtered out
        self.assertIn("Design Board", frame.render(THEME, self.root, self.block))

    def test_job_shows_goal_method_elements_and_designs(self):
        sp = data(self.root, self.job)
        self.assertEqual(sp["Description"]["subspaces"], ["Goal", "Method"])
        self.assertEqual(sp["Audience Report"]["subspaces"], ["Elements", "Evaluation"])
        self.assertIn("run-generate-d<NN>", sp["Work Details"]["run_types"])        # named by its Run (rule 6)
        elements = frame.render(THEME, self.root, self.job, "Audience Report", "Elements")
        self.assertIn("2 of 3", elements)                                       # ask changed in two designs
        method = frame.render(THEME, self.root, self.job, "Description", "Method")
        self.assertIn("① See input", method)
        verify = main(frame.render(THEME, self.root, self.job, "Work Details", "verify"))
        self.assertIn("t02_d02_option-2", verify)
        self.assertNotIn("t01_d01_option-1", verify)
        runs = frame.render(THEME, self.root, self.job, "Runs")
        self.assertIn("r01_generate_3", runs)                                   # vanilla Runs, by type

    def test_task_shows_its_design_and_elements(self):
        task = self.job / "t01_d01_option-1"
        page = frame.render(THEME, self.root, task, "Description", "Design")
        self.assertIn("&lt;message 1&gt;", page)
        self.assertIn("W-01", frame.render(THEME, self.root, task, "Work Details"))
        self.assertEqual(data(self.root, task)["Runs"]["run_types"], ["run-verify-d<NN>-v<k>", "run-revise-d<NN>"])

    def test_an_older_board_shows_its_designs_on_the_frame(self):
        # JL 261008: "the frame has no display for design items": an older board reads Block · method group · Design
        old = self.root / "Project/designs/B00_DesignBoard-old"
        design = old / "2-Design" / "Design-01-all-audience-task-sms"
        (design / "units").mkdir(parents=True)
        (old / "board.md").write_text("# old board\n")
        (design / "Design-01-all-audience-task-sms.md").write_text("# Design 01\n")
        self.assertEqual((frame.level_of(old / "2-Design"), frame.level_of(design)), ("Job", "Task"))
        self.assertIn("2-Design", THEME.spaces("Block", old, self.root, "")["Work Details"].html)
        self.assertIn("Design-01-all-audience-task-sms", THEME.spaces("Job", old / "2-Design", self.root, "")["Work Details"].html)
        task = THEME.spaces("Task", design, self.root, "")
        self.assertIn("/_board/design?", task["Work Details"].html)
        self.assertIn("space=design", task["Work Details"].html)
        self.assertIn("space=delivery", task["Delivery"].html)

    def test_a_folder_off_the_ladder_reads_as_vanilla(self):
        other = self.root / "Project/designs/b09_notes"
        other.mkdir(parents=True)
        (other / "board.md").write_text("# notes\n")
        self.assertEqual(THEME.spaces("Block", other, self.root, ""), {})


if __name__ == "__main__":
    unittest.main()
