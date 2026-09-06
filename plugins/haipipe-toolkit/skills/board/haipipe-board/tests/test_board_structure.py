import tempfile
import unittest
from pathlib import Path

from live.structure import Q_STUB, structure_op
from src.page_board import render
from src.parse import parse_board


class BoardStructureTest(unittest.TestCase):
    def board_source(self, structure=True):
        middle = (
            "## Board Structure\n"
            "**Board-Folder**\n"
            "Markdown is the source.\n\n"
            "**Board-Webpage**\n"
            "#### Board-Webpage-Index\n"
            "The Index is the top view.\n\n"
        ) if structure else ""
        return (
            "# Test Board\n"
            "spine: test the Board Index\n"
            "close: the structure is visible\n"
            "## Topic\n"
            "A test Board.\n"
            "## Pipeline\n"
            "One page follows another.\n"
            f"{middle}"
            "## Pages\n"
        )

    def test_structure_stays_in_board_source(self):
        meta = parse_board(self.board_source())
        html = render(meta, [])
        self.assertIn("Board-Webpage-Index", meta["structure"])
        self.assertNotIn("Board-Structure — Board-Folder and Board-Webpage", html)
        self.assertNotIn("Board-Webpage-Index", html)

    def test_structure_is_optional_for_existing_boards(self):
        meta = parse_board(self.board_source(structure=False))
        html = render(meta, [])
        self.assertEqual(meta["structure"], "")
        self.assertNotIn("Board-Structure — Board-Folder and Board-Webpage", html)

    def test_pages_only_index_hides_orientation_panels(self):
        meta = parse_board(self.board_source() + "index-view: pages\n")
        html = render(meta, [])
        self.assertEqual(meta["index_view"], "pages")
        self.assertIn("ALL PAGES", html)
        self.assertNotIn("<b>🦴 Spine</b>", html)
        self.assertNotIn("When, then where", html)

    def test_new_page_stub_uses_only_the_current_page_face(self):
        self.assertIn("## Opening", Q_STUB)
        self.assertIn("## Content", Q_STUB)
        self.assertIn("## Aims", Q_STUB)
        self.assertIn("**Now:**", Q_STUB)
        for heading in ("Outline", "States", "Files", "Discussion", "Log"):
            self.assertNotRegex(Q_STUB, rf"(?m)^## {heading}\s*$")

    def test_archive_moves_the_whole_page_folder_and_writes_outline_log(self):
        with tempfile.TemporaryDirectory() as tmp:
            board = Path(tmp)
            (board / "board.md").write_text(
                self.board_source(structure=False)
                + "### QA · Questions\nQA1-old.md\n",
                encoding="utf-8",
            )
            home = board / "QA1-old"
            home.mkdir()
            (home / "QA1-old.md").write_text(
                Q_STUB.format(title="Old Page"), encoding="utf-8"
            )
            (home / "studio").mkdir()
            (home / "studio" / "note.md").write_text("kept\n", encoding="utf-8")

            result, error = structure_op(
                board, {"op": "archive_question", "q": "QA1-old/QA1-old.md"}
            )

            self.assertIsNone(error)
            archived = board / result["to"]
            self.assertTrue(archived.is_file())
            self.assertTrue((archived.parent / "studio" / "note.md").is_file())
            log = archived.parent / "outline" / "QA1-old-log.md"
            self.assertIn("Archived from the Board index", log.read_text(encoding="utf-8"))
            self.assertNotIn("QA1-old.md", (board / "board.md").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
