"""The new design examples are opt-in Block pages, never independent Task pages."""
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "_host"))
from host_paths import bootstrap
bootstrap()
from live.labeling_block_preview import render_block_preview


class BlockPreviewTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.block = self.root / "b03_itemization"
        (self.block / "delivery/ui").mkdir(parents=True)
        self.face = self.block / "board.md"
        self.face.write_text("# b03 · Itemization\npreview-only: true\nlabeling-block-type: itemization\n")
        (self.block / "delivery/ui/block.html").write_text('<div id="b03_itemization"><h1>Itemization</h1></div>')

    def tearDown(self):
        self.temp.cleanup()

    def test_block_title_and_content_are_preserved(self):
        html = render_block_preview(self.block, self.root)
        self.assertIn("<title>Itemization</title>", html)
        self.assertIn('<h1>Itemization</h1>', html)
        self.assertNotIn('href=', html)

    def test_legacy_block_does_not_opt_in(self):
        self.face.write_text("# Legacy\nboard-kind: labeling-board\n")
        self.assertIsNone(render_block_preview(self.block, self.root))

    def test_job_or_task_is_not_a_preview_owner(self):
        task = self.block / "j01_example/t01_example"
        task.mkdir(parents=True)
        self.assertIsNone(render_block_preview(task, self.root))

    def test_unknown_kind_does_not_opt_in(self):
        self.face.write_text("# Unknown\npreview-only: true\nlabeling-block-type: other\n")
        self.assertIsNone(render_block_preview(self.block, self.root))

    def test_path_cannot_escape_root(self):
        with self.assertRaises(ValueError):
            render_block_preview(self.root.parent, self.root)

    def test_preview_symlink_cannot_escape_block(self):
        outside = self.root / "outside.html"
        outside.write_text("unrelated")
        path = self.block / "delivery/ui/block.html"
        path.unlink()
        path.symlink_to(outside)
        with self.assertRaises(ValueError):
            render_block_preview(self.block, self.root)


if __name__ == "__main__":
    unittest.main()
