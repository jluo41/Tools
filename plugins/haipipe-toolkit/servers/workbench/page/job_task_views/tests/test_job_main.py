"""A work Job's Main: a Job with nothing found draws no Findings band (b17 trace 261126/1225)."""
import tempfile
import unittest
from pathlib import Path

from host_paths import bootstrap

bootstrap()

from live import project_findings  # noqa: E402


class JobMainTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name).resolve()
        self.block = self.root / "P" / "work" / "b01_x"
        self.job = self.block / "j01_a"
        self.job.mkdir(parents=True)
        (self.block / "board.md").write_text("# b01 · X\n")
        (self.job / "j01_a.md").write_text("# j01 · A\ngoal: a\n\n## Tasks\n")

    def tearDown(self):
        self.tmp.cleanup()

    def test_a_job_with_nothing_found_draws_no_findings(self):
        self.assertEqual(project_findings.work_findings(self.job, self.root), "")

    def test_a_block_with_nothing_found_keeps_its_line(self):
        self.assertIn("No findings here.", project_findings.work_findings(self.block, self.root))


if __name__ == "__main__":
    unittest.main()
