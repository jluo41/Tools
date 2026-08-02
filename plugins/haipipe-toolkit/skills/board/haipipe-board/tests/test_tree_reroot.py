import unittest

from src.page_board import tree_reroot


class TreeRerootTest(unittest.TestCase):
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
