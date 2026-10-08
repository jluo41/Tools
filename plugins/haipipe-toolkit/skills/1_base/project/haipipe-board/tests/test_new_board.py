"""haipipe-board: the new-Block scaffold, in a synthetic Project."""
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))
import new_board  # noqa: E402


class NewBoardTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.tasks = Path(self.tmp.name) / "Project-Example" / "tasks"
        self.tasks.mkdir(parents=True)

    def tearDown(self):
        self.tmp.cleanup()

    def test_the_first_block_is_b01_with_its_face_and_no_empty_folders(self):
        md = new_board.new_board(self.tasks, "first_topic", "First topic")
        self.assertEqual(md.relative_to(self.tasks).as_posix(), "b01_first_topic/board.md")
        text = md.read_text()
        self.assertTrue(text.startswith("# b01 · First topic\n"))
        self.assertIn("board-kind: task-block", text)
        self.assertIn("spine: <", text)
        self.assertIn("## Topic", text)
        self.assertEqual([p.name for p in md.parent.iterdir()], ["board.md"])

    def test_the_next_block_takes_the_next_free_number(self):
        (self.tasks / "b07_older").mkdir()
        md = new_board.new_board(self.tasks, "next", "Next")
        self.assertEqual(md.parent.name, "b08_next")

    def test_a_taken_number_or_a_bad_slug_is_refused(self):
        (self.tasks / "b03_there").mkdir()
        with self.assertRaises(ValueError):
            new_board.new_board(self.tasks, "again", "Again", nn=3)
        with self.assertRaises(ValueError):
            new_board.new_board(self.tasks, "Bad-Slug", "Bad")

    def test_the_kind_follows_the_theme_folder_and_a_claim_is_a_field(self):
        cowork = self.tasks.parent / "cowork"
        cowork.mkdir()
        md = new_board.new_board(cowork, "notes", "Notes", workbench="insight", questions=True)
        text = md.read_text()
        self.assertIn("board-kind: cowork-block", text)
        self.assertIn("workbench: insight", text)
        self.assertIn("## Questions\n\n```yaml\nquestions: []\n```", text)

    def test_an_unknown_theme_folder_needs_a_kind(self):
        other = self.tasks.parent / "elsewhere"
        other.mkdir()
        with self.assertRaises(ValueError):
            new_board.new_board(other, "x", "X")
        self.assertIn("board-kind: custom-board",
                      new_board.new_board(other, "x", "X", kind="custom-board").read_text())

    def test_the_cli_dry_run_writes_nothing(self):
        out = subprocess.run([sys.executable, str(SCRIPTS / "new_board.py"), str(self.tasks), "--slug", "dry",
                              "--title", "Dry", "--dry-run"], capture_output=True, text=True)
        self.assertEqual(out.returncode, 0, out.stderr)
        self.assertIn("would write", out.stdout)
        self.assertFalse(any(self.tasks.iterdir()))

    def test_the_report_check_reads_the_new_face(self):
        sys.path.insert(0, str(SCRIPTS.parents[1] / "haipipe-report" / "scripts"))
        import check_report
        md = new_board.new_board(self.tasks, "q", "Q", questions=True)
        self.assertEqual(check_report.rows(md.parent), ([], []))


if __name__ == "__main__":
    unittest.main()
