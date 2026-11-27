"""A work Job's Main: no empty Findings band (b17 trace 261126/1225); its Overview one fold of top views (261127/0010)."""
import tempfile
import unittest
from pathlib import Path

from host_paths import bootstrap

bootstrap()

from live import focus_page, frame, project_findings  # noqa: E402


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

    def test_a_job_overview_is_one_fold_of_top_views(self):
        page = focus_page.render(frame.Theme(name="work"), self.root, self.job, "report", "overview")
        self.assertIn('data-topview="ovj01_a-0"', page)
        for name in ("Goal", "Requirements", "MindMap"):
            self.assertRegex(page, rf'data-topview="ovj01_a-\d"[^>]*>{name}</button>')
        self.assertNotIn("2 · 📋 Requirements", page)
        self.assertIn("1 · 📋 Brief", page)

    def test_a_block_overview_keeps_its_numbered_folds(self):
        page = focus_page.render(frame.Theme(name="work"), self.root, self.block, "report", "overview")
        self.assertIn("2 · 📋 Requirements", page)
        self.assertNotIn("data-topview=", page)

    def test_a_block_with_nothing_found_keeps_its_line(self):
        self.assertIn("No findings here.", project_findings.work_findings(self.block, self.root))


if __name__ == "__main__":
    unittest.main()
