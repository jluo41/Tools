"""haipipe-run: the soft-Run writer, and the Run type table naming every button's skill."""
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import yaml

SKILL = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SKILL / "scripts"))
import soft_run  # noqa: E402


class SoftRunTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        (self.root / "env.sh").write_text("")
        self.block = self.root / "Project-Example" / "tasks" / "b01_topic"
        self.block.mkdir(parents=True)

    def tearDown(self):
        self.tmp.cleanup()

    def test_a_new_soft_run_has_its_card_and_ticket(self):
        run = soft_run.new(self.block, "draw", "s01", skill="haipipe-studio", feeds=["reports/q01_x"])
        self.assertEqual(run.name, "run-draw-s01")
        card = yaml.safe_load((run / "run.yaml").read_text())
        self.assertEqual(list(card)[:6], ["run", "kind", "type", "scope", "target", "ticket"])
        self.assertEqual((card["run"], card["kind"], card["type"], card["target"]), ("run-draw-s01", "soft", "draw", "s01"))
        self.assertEqual(card["scope"], "Project-Example/tasks/b01_topic")
        self.assertEqual((card["status"], card["passes"], card["skill"]), ("planned", [], "haipipe-studio"))
        self.assertIsNone(card["agent"])
        self.assertTrue((run / "run-draw-s01.md").is_file())

    def test_a_name_has_no_date_and_a_second_round_is_a_pass(self):
        with self.assertRaises(ValueError):
            soft_run.new(self.block, "section", "1007-intro")
        with self.assertRaises(ValueError):
            soft_run.new(self.block, "section", "intro-261007")
        soft_run.new(self.block, "section", "intro")
        with self.assertRaises(ValueError):
            soft_run.new(self.block, "section", "intro")

    def test_passes_count_up_and_update_the_card(self):
        run = soft_run.new(self.block, "draw", "s02")
        p1 = soft_run.add_pass(run, "First session", ask="<ask>", changed=["studio/s02-x/s02-x.md"], date="1007")
        p2 = soft_run.add_pass(run, "Second session", date="1008")
        self.assertEqual((p1.name, p2.name), ("p01-1007", "p02-1008"))
        self.assertTrue((p1 / "pass.md").read_text().startswith("# First session"))
        card = yaml.safe_load((run / "run.yaml").read_text())
        self.assertEqual(card["passes"], ["p01-1007", "p02-1008"])
        self.assertEqual(card["status"], "done")
        self.assertEqual(card["writes"], ["studio/s02-x/s02-x.md"])

    def test_a_hyphenated_type_and_signs(self):
        run = soft_run.new(self.block, "add-venue", "v01", signs=["agreed", "checked"])
        self.assertEqual(run.name, "run-add-venue-v01")
        card = yaml.safe_load((run / "run.yaml").read_text())
        self.assertEqual((card["type"], card["target"], card["signs"]), ("add-venue", "v01", ["agreed", "checked"]))
        for bad in ("Add-venue", "add--venue", "add-", "-add"):
            with self.assertRaises(ValueError):
                soft_run.new(self.block, bad, "v02")

    def test_no_scope_root_leaves_scope_null(self):
        (self.root / "env.sh").unlink()
        card = yaml.safe_load((soft_run.new(self.block, "face", "b01") / "run.yaml").read_text())
        self.assertIsNone(card["scope"])

    def test_the_cli(self):
        run = lambda *a: subprocess.run([sys.executable, str(SKILL / "scripts" / "soft_run.py"), *a],
                                        capture_output=True, text=True)
        self.assertEqual(run("new", str(self.block), "--type", "report", "--target", "q01").returncode, 0)
        out = run("pass", str(self.block / "runs" / "run-report-q01"), "--title", "T", "--date", "1007")
        self.assertEqual(out.returncode, 0, out.stderr)
        self.assertEqual(run("new", str(self.block), "--type", "report", "--target", "q01").returncode, 2)


class RunTypesBySpaceTest(unittest.TestCase):
    """ref/run-types-by-space.md names a skill for every button it lists, and each skill exists."""

    def test_every_button_names_an_existing_skill(self):
        text = (SKILL / "ref" / "run-types-by-space.md").read_text()
        rows = [r for r in re.findall(r"(?m)^\| *([A-Z][^|]*?) *\| *([^|]+?) *\| *`?(haipipe-[a-z-]+|workbench-<theme>)`? *\|", text)]
        self.assertGreater(len(rows), 10)
        skills = SKILL.parents[2]
        names = {p.parent.name for p in skills.glob("**/SKILL.md")}
        for space, button, skill in rows:
            if skill != "workbench-<theme>":
                self.assertTrue(skill in names, f"{space} · {button}: no skill {skill}")


if __name__ == "__main__":
    unittest.main()
