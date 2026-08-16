import unittest
import tempfile
from pathlib import Path

from src.page_board import group_canvas, tree_reroot


class TreeRerootTest(unittest.TestCase):
    def test_group_page_emits_only_the_owner_address_no_canvas_on_stage(self):
        """JL 260815, "I don't want the draw in here": a group page's body stays
        prose and the composed drawing opens in the Draw split, so the build
        emits the OWNER ADDRESS alone. This asserts the ruling, not just the
        path: the two edit-mode links it replaced must not come back."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "pyproject.toml").write_text("[project]\nname='fixture'\n")
            board = root / "board-source"
            scene = board / "QA-first" / "draw" / "group.excalidraw"
            scene.parent.mkdir(parents=True)
            scene.write_text("{}")
            html = group_canvas(
                {"dir": str(board), "excalidraw": "/_excalidraw"},
                "QA · First", [{"file": "QA-first/QA1.md"}],
            )
            self.assertIn("board-source/QA-first/draw/group.excalidraw", html)
            self.assertIn('class="group-draw-owner"', html)
            self.assertIn("hidden", html)
            self.assertIn('data-label="QA · First"', html)
            self.assertNotIn("mode=group-source", html)
            self.assertNotIn("mode=arrange", html)
            self.assertNotIn("<iframe", html)

    def test_board_source_links_and_media_move_together(self):
        html = (
            '<a href="_fixture/readme.md">source</a>'
            '<img src="_fixture/figure.png">'
            '<object data="_fixture/preview.pdf"></object>'
        )
        moved = tree_reroot(html, "../../")
        self.assertIn('href="../../_fixture/readme.md"', moved)
        self.assertIn('src="../../_fixture/figure.png"', moved)
        self.assertIn('data="../../_fixture/preview.pdf"', moved)

    def test_generated_and_external_urls_are_not_moved(self):
        html = (
            '<a href="../QS/page.html">page</a>'
            '<link href="../_assets/board.css?v=abc">'
            '<img src="data:image/png;base64,AA">'
            '<iframe src="https://example.test/frame"></iframe>'
            '<iframe src="/_excalidraw/frame"></iframe>'
        )
        self.assertEqual(tree_reroot(html, "../../"), html)

    def test_documented_board_output_is_source_root_relative(self):
        html = (
            '<a href="board/index.html">site</a>'
            '<link href="board/_assets/board.css?v=abc">'
        )
        moved = tree_reroot(html, "../")
        self.assertIn('href="../board/index.html"', moved)
        self.assertIn('href="../board/_assets/board.css?v=abc"', moved)


if __name__ == "__main__":
    unittest.main()
