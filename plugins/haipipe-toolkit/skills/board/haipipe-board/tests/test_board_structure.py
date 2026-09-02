import unittest

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


if __name__ == "__main__":
    unittest.main()
