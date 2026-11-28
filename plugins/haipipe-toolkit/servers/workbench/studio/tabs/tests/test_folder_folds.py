"""A folder item of studio-views.json: one fold per file, read live, nothing outside the SPACE."""
import json
import tempfile
import unittest
from pathlib import Path

from host_paths import bootstrap

bootstrap()

from live import folder_folds, studio_views  # noqa: E402


class FolderFoldsTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name).resolve() / "space"
        self.ref = self.root / "skill" / "ref"
        self.ref.mkdir(parents=True)
        (self.ref / "b-topic.md").write_text("# b\n")
        (self.ref / "a-topic.md").write_text("# a\n")
        (self.ref / ".hidden.md").write_text("x")
        (self.ref / "picture.png").write_bytes(b"x")
        (self.ref / "__pycache__").mkdir()
        self.topic = self.root / "block" / "s51-skills-x"
        self.topic.mkdir(parents=True)

    def tearDown(self):
        self.tmp.cleanup()

    def views(self, items):
        (self.topic / "studio-views.json").write_text(json.dumps({"views": [{"name": "skill-x", "items": items}]}))
        return studio_views.read_views(self.topic, self.root)

    def test_one_fold_per_file_in_name_order(self):
        item = folder_folds.folder_item(self.ref, self.root)
        self.assertEqual([name for name, _ in item.files], ["a-topic.md", "b-topic.md"])
        page = folder_folds.folds("Skills: X", item)
        self.assertEqual(page.count('<details class="st-fold">'), 2)
        self.assertEqual(page.count("data-fold-src="), 2)            # fetched when the fold opens, never copied
        self.assertNotIn("data-studio-src", page)                     # so the page's loader leaves a closed fold alone
        self.assertNotIn(" src=", page)
        self.assertNotIn(" open", page.split("</style>")[1])           # every fold starts closed

    def test_views_file_names_a_folder(self):
        _, parts = self.views([{"name": "ref", "folder": "skill/ref"}])
        label, held, _ = parts["skill-x"][0]
        self.assertEqual(label, "ref")
        self.assertIsInstance(held, folder_folds.Folder)
        self.assertEqual(len(held.files), 2)

    def test_skipped_files_are_left_out(self):
        _, parts = self.views([{"name": "other", "folder": "skill/ref", "skip": ["a-topic.md"]}])
        self.assertEqual([name for name, _ in parts["skill-x"][0][1].files], ["b-topic.md"])
        self.assertIsNone(self.views([{"name": "other", "folder": "skill/ref", "skip": ["a-topic.md", "b-topic.md"]}]))

    def test_empty_or_missing_folder_is_no_tab(self):
        (self.root / "skill" / "empty").mkdir()
        self.assertIsNone(self.views([{"name": "empty", "folder": "skill/empty"},
                                      {"name": "gone", "folder": "skill/gone"}]))

    def test_folder_outside_the_space_is_refused(self):
        outside = self.root.parent / "outside"
        outside.mkdir()
        (outside / "secret.md").write_text("x")
        self.assertEqual(folder_folds.files_of(outside, self.root), [])
        self.assertIsNone(self.views([{"name": "out", "folder": "../outside"},
                                      {"name": "abs", "folder": str(outside)}]))


if __name__ == "__main__":
    unittest.main()
