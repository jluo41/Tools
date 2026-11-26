"""A work Job's Findings: a fold per Task group, a left tab per Task with a round, its newest round on the right."""
import re
import tempfile
import unittest
from pathlib import Path

from host_paths import bootstrap

bootstrap()

from live import round_findings  # noqa: E402


class RoundFindingsTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name).resolve()
        self.job = self.root / "P" / "work" / "b01_x" / "j11_a"
        self.job.mkdir(parents=True)
        (self.job / "j11_a.md").write_text("# j11 · A\nbands: t0N Task Group 1 · t1N Task Group 2\n\n## Tasks\n\n"
                                            "1. t01_one · One\n2. t02_two · Two\n3. t11_three · Three\n")
        for name, passes in (("t01_one", [("p01-1120", "first", "Old."), ("p02-1125", "second", "Date is text.")]),
                             ("t02_two", []), ("t11_three", [("p01-1118", "report", "One line per check.")])):
            t = self.job / name
            t.mkdir()
            (t / f"{name}.md").write_text(f"# {name}\nstate: OPEN\n")
            for p, head, summary in passes:
                d = t / "runs" / "run-check-x" / "passes" / p
                d.mkdir(parents=True)
                (d / "pass.md").write_text(f"# {head}\n\n## Summary\n\n{summary}\n\n## Changed\n\n- `a/b.py`\n")
            if passes:
                (t / "runs" / "run-check-x" / "run.yaml").write_text("status: waiting\n")

    def tearDown(self):
        self.tmp.cleanup()

    def test_a_fold_per_group_a_tab_per_task_with_a_round(self):
        secs = round_findings.sections(self.job, self.root)
        self.assertEqual([s[0] for s in secs], ["📌 Task Group 1", "📌 Task Group 2"])
        first = secs[0][2]
        self.assertEqual(len(re.findall(r'data-pbtab=', first)), 1)          # t02 has no round, no tab
        self.assertIn("Date is text.", first)                                  # the newest round's Summary
        self.assertNotIn("Old.", first)
        self.assertIn("a/b.py", first)                                         # what it changed
        self.assertIn("pass.md", first.replace("%2F", "/"))                    # the round to open


if __name__ == "__main__":
    unittest.main()
