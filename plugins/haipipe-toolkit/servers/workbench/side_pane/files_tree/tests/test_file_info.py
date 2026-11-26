"""Files › the hover card: what a file or folder is, its path, its traces (side_pane/files_tree/file_info.py)."""
import tempfile
import unittest
from pathlib import Path

from host_paths import bootstrap

bootstrap()

from live import file_info, focus_scope  # noqa: E402


class FileInfoTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = root = Path(self.tmp.name).resolve()
        self.block = root / "blueprints" / "P" / "work" / "b01_x"
        (self.block / "s03-ladder").mkdir(parents=True)
        (self.block / "s03-ladder" / "s03-ladder.md").write_text("# s03 · How does work climb the ladder?\n")
        (root / "tools").mkdir()
        (root / "tools" / "page.py").write_text('"""A trace in the Files pane: its files. More words."""\nx = 1\n')
        (root / "tools" / "notes.md").write_text("---\ntitle: Notes kept\n---\n# Other\n")
        day = self.block / "trace" / "261125"
        day.mkdir(parents=True)
        (day / "1051_view.md").write_text("---\ntitle: trace view\naim: A.\nplan:\n  - do: edit\n    path: tools/page.py\n"
                                          "    what: marks\nchanged:\n  - tools/page.py\n---\n")

    def tearDown(self):
        self.tmp.cleanup()

    def test_a_file_says_its_first_sentence_and_the_traces_that_touched_it(self):
        self.assertEqual(file_info.what(self.root / "tools" / "page.py"), "A trace in the Files pane: its files.")
        self.assertEqual(file_info.what(self.root / "tools" / "notes.md"), "Notes kept")
        card = file_info.card(self.root / "tools" / "page.py", self.root)
        self.assertIn("tools/page.py", card)
        self.assertIn("10:51 trace view", card)
        self.assertIn('aria-label="Editing"', card)
        self.assertIn('data-fi="copy" data-path="tools/page.py"', card)   # Copy path
        self.assertIn("Open ↗", card)

    def test_the_card_opens_on_a_right_click_never_on_hover(self):
        self.assertIn("'contextmenu'", file_info.CARD)
        self.assertNotIn("mouseover", file_info.CARD)
        self.assertIn("if(e.shiftKey)return", file_info.CARD)                 # shift keeps the browser's own menu
        self.assertIn("document.execCommand('copy')", file_info.CARD)      # Copy path works over plain http too

    def test_a_folder_says_its_face_title(self):
        card = file_info.card(self.block / "s03-ladder", self.root)
        self.assertIn("How does work climb the ladder?", card)

    def test_outside_the_space_there_is_no_card(self):
        self.assertEqual(file_info.card(self.root.parent, self.root), "")

    def test_folder_rows_carry_no_grey_title(self):
        page = focus_scope.assets(self.block / "s03-ladder", self.root)
        self.assertNotIn("sc-what", page)
        self.assertNotIn("__scopeWhat", page)


if __name__ == "__main__":
    unittest.main()
