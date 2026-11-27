"""A work Job's Findings by type: a fold per kind its Runs name under finds:, a tab per file (b17 trace 261127/0045);
a finding's raw files and steps under it, one finding full width (trace 261127/1215)."""
import os
import tempfile
import unittest
from pathlib import Path

from host_paths import bootstrap

bootstrap()

from live import project_findings, run_finds  # noqa: E402


class FindingsByTypeTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name).resolve()
        self.block = self.root / "P" / "work" / "b01_x"
        self.job = self.block / "j11_a"
        self.job.mkdir(parents=True)
        (self.block / "board.md").write_text("# b01 · X\n")
        (self.job / "j11_a.md").write_text("# j11 · A\n\n## Tasks\n\n1. t01_one · One\n2. t02_two · Two\n3. t03_three · Three\n")
        for name in ("t01_one", "t02_two", "t03_three"):
            (self.job / name).mkdir()
            (self.job / name / f"{name}.md").write_text(f"# Task {name[1:3]} name\nstate: OPEN\n")

    def tearDown(self):
        self.tmp.cleanup()

    def run_with(self, task, run, day, files, extra=""):
        r = self.job / task / "runs" / run
        (r / "passes" / f"p01-{day}").mkdir(parents=True)
        lines = ["finds:"]
        for rel, kind, text in files:
            (r / rel).parent.mkdir(parents=True, exist_ok=True)
            (r / rel).write_text(text)
            lines += [f"- file: {rel}", f"  kind: {kind}"]
        lines += [extra] if extra else []
        (r / "run.yaml").write_text(f"run: {run}\n" + "\n".join(lines) + "\n")

    def test_three_kinds_give_three_folds_a_tab_per_file(self):
        self.run_with("t01_one", "run-build-01-name", "1120", [("result/r.csv", "value", "a,b\n1,2\n")])
        self.run_with("t02_two", "run-draw-01-name", "1121", [("result/f.svg", "display", "<svg/>")])
        self.run_with("t03_three", "run-build-01-name", "1122", [("result/a.txt", "report", "text one"),
                                                                ("result/b.html", "report", "<p>page</p>")])
        secs = run_finds.sections(self.job, self.root)
        self.assertEqual([s[0] for s in secs], ["🔢 Values", "🖼️ Displays", "📄 Reports"])
        self.assertIn("<td>1</td>", secs[0][2])
        self.assertIn("<img", secs[1][2])
        self.assertIn("Task 03 name · a.txt", secs[2][2])
        self.assertIn("Task 03 name · b.html", secs[2][2])
        self.assertIn("class=open-dot", secs[2][2])

    def test_the_newest_run_wins(self):
        self.run_with("t01_one", "run-build-01-name", "1110", [("result/old.csv", "value", "a\nold\n")])
        self.run_with("t01_one", "run-build-02-name", "1125", [("result/new.csv", "value", "a\nnew\n")])
        html = run_finds.sections(self.job, self.root)[0][2]
        self.assertIn("<td>new</td>", html)
        self.assertNotIn("<td>old</td>", html)

    def test_one_finding_full_width_and_several_get_left_tabs(self):
        self.run_with("t01_one", "run-build-01-name", "1120", [("result/r.csv", "value", "a\n1\n")])
        self.run_with("t03_three", "run-build-01-name", "1122", [("result/a.txt", "report", "one"),
                                                                ("result/b.txt", "report", "two")])
        values, reports = run_finds.sections(self.job, self.root)
        self.assertNotIn("pb-tabset", values[2])
        self.assertIn("pb-tabset", reports[2])

    def raw(self, text="a\n1\n"):
        f = self.job / "t02_two" / "runs" / "run-check-01-name" / "result" / "raw.csv"
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text(text)
        return f

    def valued(self, how=""):
        self.run_with("t01_one", "run-build-01-name", "1120", [("result/r.csv", "value", "a\n1\n")],
                      "  from: [../../../t02_two/runs/run-check-01-name/result/raw.csv]" + how)
        return self.job / "t01_one" / "runs" / "run-build-01-name" / "result" / "r.csv"

    def test_from_links_the_raw_file_current(self):
        raw = self.raw()
        made = self.valued("\n  how: [read raw.csv, keep column a]")
        os.utime(raw, (1000, 1000))
        html = run_finds.sections(self.job, self.root)[0][2]
        self.assertIn("✅", html)
        self.assertIn("raw.csv", html)
        self.assertIn("t02_two/runs/run-check-01-name/result/raw.csv", html)
        self.assertIn("How this table is made", html)
        self.assertIn("<li>keep column a</li>", html)
        self.assertTrue(made.is_file())

    def test_from_marks_a_newer_or_gone_raw_file(self):
        raw = self.raw()
        made = self.valued()
        os.utime(made, (1000, 1000))
        html = run_finds.sections(self.job, self.root)[0][2]
        self.assertIn("❗", html)
        self.assertIn("changed after r.csv was made", html)
        self.assertNotIn("How this", html)
        raw.unlink()
        self.assertIn("is gone", run_finds.sections(self.job, self.root)[0][2])

    def test_no_finds_no_fold_and_no_round_folds(self):
        self.assertEqual(run_finds.sections(self.job, self.root), [])
        self.assertEqual(project_findings.work_findings(self.job, self.root), "")


if __name__ == "__main__":
    unittest.main()
