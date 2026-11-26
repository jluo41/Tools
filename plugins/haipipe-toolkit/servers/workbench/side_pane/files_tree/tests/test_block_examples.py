"""Files › Block Examples: the example Blocks a Block's face names on its `examples:` line, as a numbered part after
Skills (side_pane/files_tree/work_files.py)."""
import tempfile
import unittest
from pathlib import Path

from host_paths import bootstrap

bootstrap()

from live import work_files  # noqa: E402


class BlockExamplesTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = root = Path(self.tmp.name).resolve()
        (root / "env.sh").write_text("")
        self.project = root / "P"
        (self.project / "project.md").parent.mkdir(parents=True)
        (self.project / "project.md").write_text("# P\n")
        self.block = self.project / "work" / "b01_x"
        self.block.mkdir(parents=True)
        for name in ("Insight-A", "InsightDataPrep-A"):
            (self.project / "insight" / name).mkdir(parents=True)
            (self.project / "insight" / name / "board.md").write_text("# A\n")

    def tearDown(self):
        self.tmp.cleanup()

    def face(self, line):
        (self.block / "board.md").write_text(f"---\ntitle: x\n{line}---\n\n# X\n")

    def test_the_examples_line_lists_each_example_from_the_project_folder(self):
        self.face("examples: insight/Insight-A, insight/InsightDataPrep-A, insight/Missing\n")
        base, rows = work_files.examples_tree(self.block, self.root)
        self.assertEqual(base, self.project / "insight")
        self.assertIn("Insight-A", rows)
        self.assertIn("InsightDataPrep-A", rows)
        self.assertNotIn("Missing", rows)                  # a folder not on disk is left out, never drawn

    def test_examples_in_two_theme_folders_each_show_under_their_folder(self):
        (self.project / "cowork" / "b01_example_cowork").mkdir(parents=True)
        self.face("examples: insight/Insight-A, cowork/b01_example_cowork\n")
        base, rows = work_files.examples_tree(self.block, self.root)
        self.assertEqual(base, self.project)
        self.assertRegex(rows, r'<span title="[^"]*/insight">insight</span>')       # the theme folder, opened
        self.assertRegex(rows, r'<span title="[^"]*/cowork">cowork</span>')
        self.assertLess(rows.index(">cowork<"), rows.index("b01_example_cowork"))   # the example inside it

    def test_a_block_without_the_line_draws_no_part(self):
        self.face("")
        self.assertEqual(work_files.examples_tree(self.block, self.root)[1], "")


if __name__ == "__main__":
    unittest.main()
