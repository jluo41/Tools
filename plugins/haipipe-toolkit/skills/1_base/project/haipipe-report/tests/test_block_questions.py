"""haipipe-report: `block_questions.py --drawing` makes the report's drawing a Block sNN (JL 261031, b35 r02: no studio/
folder anywhere), never reports/<id>/studio/."""
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "ref" / "block_questions.py"
BOARD = "# b01 · Topic\nboard-kind: task-block\n\n## Questions\n\n```yaml\nquestions: []\n```\n"


def add_question(block: Path, *extra: str) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, str(SCRIPT), "add-question", str(block), "--id", "Q01", "--slug",
                           "input_forms", "--question", "Which input forms does the food API take?", *extra],
                          capture_output=True, text=True)


class DrawingTopicTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.block = Path(self.tmp.name).resolve() / "b01_topic"
        self.block.mkdir()
        (self.block / "board.md").write_text(BOARD, encoding="utf-8")

    def test_the_drawing_is_a_block_snn_that_feeds_the_report(self):
        done = add_question(self.block, "--drawing", "api_food")
        self.assertEqual(done.returncode, 0, done.stderr)
        topic = self.block / "s01-api-food"
        self.assertIn("**Feeds:** `reports/` q01_input_forms", (topic / "s01-api-food.md").read_text(encoding="utf-8"))
        self.assertTrue((topic / "s01-api-food.excalidraw").is_file())
        page = (self.block / "reports" / "q01_input_forms" / "q01_input_forms.md").read_text(encoding="utf-8")
        self.assertIn("(../../s01-api-food/s01-api-food.excalidraw)", page)
        self.assertEqual(list(self.block.rglob("studio")), [])

    def test_a_full_block_refuses_before_board_md_changes(self):
        for n in range(1, 10):
            (self.block / f"s0{n}-t{n}").mkdir()
            (self.block / f"s0{n}-t{n}" / f"s0{n}-t{n}.md").write_text(f"s0{n} · T{n}\n", encoding="utf-8")
        done = add_question(self.block, "--drawing", "api_food")
        self.assertNotEqual(done.returncode, 0)
        self.assertRegex(done.stderr, r"is full|at most 9")             # new_topic's band or Block limit
        self.assertEqual((self.block / "board.md").read_text(encoding="utf-8"), BOARD)
        self.assertFalse((self.block / "reports").exists())


if __name__ == "__main__":
    unittest.main()
