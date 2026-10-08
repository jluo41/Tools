"""The design ladder's scaffold (ref/design-ladder.md) makes each level, names every Run run-<type>-<target>, never
overwrites, and writes what the design workbench's reader (servers/workbench-design/design_reader.py) reads."""
from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "scripts"))
sys.path.insert(0, str(HERE))
import design_ladder as D  # noqa: E402
from ladder_kit import ready  # noqa: E402

READER = HERE.parents[4] / "servers" / "workbench-design" / "design_reader.py"


def reader():
    spec = importlib.util.spec_from_file_location("design_reader_under_test", READER)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


class DesignLadderTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.block = Path(self.tmp.name) / "Project" / "designs" / "b01_demo_app"
        ready(self.block, n=3)
        self.job = self.block / "j01_g01_m04"
        D.main(["job", str(self.job), "--goal", "G01", "--method", "M04 m2", "--inputs", "i2", "--n", "3"])
        D.main(["task", str(self.job), "t00"])
        D.main(["task", str(self.job), "d01", "reason-first"])
        D.main(["task", str(self.job), "t99"])

    def tearDown(self):
        self.tmp.cleanup()

    def test_each_level_has_its_face_and_folders(self):
        for p in ("board.md", "design-goal.md", "inputs", "observed", "studio", "reports", "delivery", "runs/README.md"):
            self.assertTrue((self.block / p).exists(), p)
        for p in ("j01_g01_m04.md", "inputs", "delivery", "t00_reason-ideas/t00_reason-ideas.md",
                  "t01_d01_reason-first/t01_d01_reason-first.md", "t01_d01_reason-first/elements.yaml",
                  "t99_review-whole/t99_review-whole.md"):
            self.assertTrue((self.job / p).exists(), p)
        self.assertIn("method: M04 m2", (self.job / "j01_g01_m04.md").read_text())

    def test_every_run_is_run_type_target_and_hard_ones_keep_a_result(self):
        t00, d01, t99 = self.job / "t00_reason-ideas", self.job / "t01_d01_reason-first", self.job / "t99_review-whole"
        made = {D.run(self.block, "setup-rules", "", []), D.run(self.block, "add-goal", "g01", []),
                D.run(self.job, "setup-goal", "", []), D.run(self.job, "open-designs", "", []),
                D.run(t00, "reason", "", []), D.run(d01, "generate", "", []), D.run(d01, "verify", "", [])}
        rev = D.run(d01, "revise", "", [])
        (rev / "passes" / "p01-1007").mkdir(parents=True)
        (rev / "passes" / "p01-1007" / "design.md").write_text("<draft 2>\n")
        made |= {rev, D.run(d01, "verify", "", []), D.run(t99, "rank", "", [])}
        self.assertEqual({p.name for p in made},
                         {"run-setup-rules", "run-add-goal-g01", "run-setup-goal-j01", "run-open-designs-j01",
                          "run-reason-t00", "run-generate-d01", "run-verify-d01-v1", "run-revise-d01",
                          "run-verify-d01-v2", "run-rank-t99"})
        for p in made:
            hard = p.name.split("-")[1] in D.HARD
            self.assertIn(f"kind: {'hard' if hard else 'soft'}", (p / "run.yaml").read_text())
            self.assertTrue((p / ("result" if hard else "passes")).is_dir(), p.name)

    def test_nothing_is_overwritten(self):
        self.assertEqual(D.main(["job", str(self.job), "--goal", "G01", "--method", "M04 m2", "--inputs", "i2"]), [])
        with self.assertRaises(SystemExit):                     # verify needs a draft to read
            D.main(["run", str(self.job / "t01_d01_reason-first"), "verify"])
        self.assertEqual(D.main(["task", str(self.job), "d01", "reason-first"]), [])

    def test_bad_names_are_refused(self):
        for argv in (["job", str(self.block / "j02_reminder_by-insight"), "--goal", "G01", "--method", "M04 m2",
                      "--inputs", "i2"],
                     ["job", str(self.block / "j02_g01_m04"), "--goal", "G01", "--method", "by insight", "--inputs", "i2"],
                     ["task", str(self.job), "d02"],
                     ["job", str(self.block / "j02_g01_m04"), "--goal", "G01", "--method", "M04 m9", "--inputs", "i2"],
                     ["job", str(self.block / "j02_g02_m04"), "--goal", "G02", "--method", "M04 m2", "--inputs", "i2"],
                     ["job", str(self.block / "j02_g01_m04"), "--goal", "G01", "--method", "M04 m2", "--inputs", "i7"],
                     ["job", str(self.block / "j02_g01_m04"), "--goal", "G01", "--method", "M04 m2", "--inputs", "i2",
                      "--n", "9"],
                     ["job", str(self.block / "j02_g01_m01"), "--goal", "G01", "--method", "M04 m2", "--inputs", "i2"],
                     ["run", str(self.job / "t00_reason-ideas"), "generate"],
                     ["run", str(self.block), "reason"]):
            with self.assertRaises(SystemExit):
                D.main(argv)

    def test_a_job_name_carries_readable_slugs(self):
        """jNN_<goal>-<goal-slug>_<method>-<method-slug> (JL 261008: ids alone are not human readable)."""
        job = self.block / "j02_g01-a-goal_m04-actionable-insights"
        D.main(["job", str(job), "--goal", "G01", "--method", "M04 m2", "--inputs", "i2", "--n", "3"])
        self.assertTrue((job / f"{job.name}.md").is_file())
        self.assertEqual(D.level_of(job), "Job")
        with self.assertRaises(SystemExit):                              # the ids must still match the pins
            D.main(["job", str(self.block / "j03_g02-a-goal_m04-x"), "--goal", "G01", "--method", "M04 m2", "--inputs", "i2"])

    def test_a_block_is_named_by_its_kind(self):
        """A design Block is a special board, Design-<name>[-<YYMMDD>] (JL 261008); bNN_<app> stays readable."""
        root = Path(self.tmp.name) / "Project" / "designs"
        D.main(["block", str(root / "Design-Demo-Round2-261008"), "--title", "<application>"])
        self.assertTrue((root / "Design-Demo-Round2-261008" / "board.md").is_file())
        self.assertEqual(D.level_of(root / "Design-Demo-Round2-261008"), "Block")
        for bad in ("Insight-Demo", "demo_app", "design-demo"):
            with self.assertRaises(SystemExit):
                D.main(["block", str(root / bad)])

    def test_the_workbench_reads_what_the_scaffold_makes(self):
        R = reader()
        D.run(self.job / "t00_reason-ideas", "reason", "", [])
        D.run(self.job / "t01_d01_reason-first", "generate", "", [])
        self.assertTrue(R.is_ladder(self.block))
        j = R.job(self.job)
        self.assertEqual((j["method"], j["version"], j["inputs"]), ("M04", "m2", "i2"))
        self.assertEqual([d["id"] for d in j["designs"]], ["d01"])
        self.assertEqual(j["reason"]["run"], "run-reason-t00")
        self.assertEqual(j["reason"]["kind"], "hard")          # read from run.yaml, not from the name
        self.assertEqual(j["designs"][0]["drafts"][0]["run"], "run-generate-d01")


if __name__ == "__main__":
    unittest.main()
