"""type_follow.py: a topic started from a type has the type's buttons and tabs, and is held against them (A10)."""
import json
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))
import type_follow  # noqa: E402

ELEMENTS = """## Page
what: the pages

### Rows
what: its rows
check: open it

### Notes
what: notes
when: the topic keeps notes

### 〈quick page〉
what: one more page

## Draw
what: the drawing
when: the topic has a drawing
"""


class TypeFollow(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name).resolve()
        self.kind = self.root / "block" / "s71-studio-type-x"
        self.topic = self.root / "block" / "s11-x"
        for folder in (self.kind, self.topic):
            folder.mkdir(parents=True)
        (self.kind / "elements.md").write_text(ELEMENTS)

    def tearDown(self):
        self.tmp.cleanup()

    def views(self, *views):
        (self.topic / "studio-views.json").write_text(json.dumps({
            "check_type": "block/s71-studio-type-x",
            "views": [{"name": n, "items": [{"name": i, "path": "block/s11-x/a.md"} for i in items]} for n, items in views]}))
        return type_follow.problems(self.topic, self.root)

    def test_a_topic_with_the_types_parts_follows(self):
        self.assertEqual(self.views(("Page", ["Rows"])), ([], []))                       # Notes and Draw have a when:
        self.assertEqual(self.views(("Page", ["Rows", "Notes", "try 1", "try 2"]), ("Draw", ["Draw"])), ([], []))

    def test_missing_extra_and_out_of_order_are_named(self):
        bad, _ = self.views(("Draw", ["Draw"]), ("Page", ["Notes"]), ("Extra", ["x"]))
        self.assertIn("Page: no left tab Rows", bad)
        self.assertIn("top button Extra is not in the type", bad)
        self.assertIn("its top buttons are out of the type's order", bad)
        self.assertEqual(self.views(("Draw", ["Draw"]))[0], ["no top button Page"])

    def test_a_topic_that_names_no_type_is_not_judged(self):
        (self.topic / "studio-views.json").write_text(json.dumps({"views": []}))
        self.assertIsNone(type_follow.problems(self.topic, self.root))

    def test_new_starts_from_the_types_own_views_and_reads_as_not_filled(self):
        (self.kind / "studio-views.json").write_text(json.dumps({"check_type": "block/s71-studio-type-x", "views": [
            {"name": "Page", "items": [{"name": "Rows", "path": "block/s71-studio-type-x/delivery/requirements/page--rows.html"}]},
            {"name": "Check", "items": [{"name": "Page", "path": "block/s71-studio-type-x/delivery/check.html"}]}]}))
        (self.topic / "studio-views.json").write_text(type_follow.new(self.kind, self.topic, self.root))
        data = json.loads((self.topic / "studio-views.json").read_text())
        self.assertEqual([v["name"] for v in data["views"]], ["Page"])                   # the type's Check is not copied
        self.assertEqual(type_follow.problems(self.topic, self.root), ([], ["Page › Rows still shows the requirement"]))


if __name__ == "__main__":
    unittest.main()
