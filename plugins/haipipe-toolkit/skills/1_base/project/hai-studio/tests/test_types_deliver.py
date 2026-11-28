"""types_deliver.py: a blueprint type's elements.md is kept in hai-studio/gallery/<name>/, the same file."""
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import types_deliver  # noqa: E402


class TypesDeliver(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.space = Path(self.tmp.name).resolve()
        self.kept = self.space / "plugins/skill/types"
        self.topic = self.space / "P/blueprint/b17_x/s75-studio-type-skills"
        self.topic.mkdir(parents=True)
        (self.topic / "elements.md").write_text("## A\nwhat: a\n")
        (self.space / "P/blueprint/b17_x/s73-studio-type-report").mkdir()              # no elements.md: not a type yet

    def tearDown(self):
        self.tmp.cleanup()

    def run_it(self, *argv):
        return types_deliver.main(list(argv), self.space, self.kept)

    def test_deliver_then_same_then_stale(self):
        self.assertEqual(self.run_it("--check"), 1)                                     # nothing delivered yet
        self.assertEqual(self.run_it(), 0)
        self.assertEqual((self.kept / "skills/elements.md").read_text(), "## A\nwhat: a\n")
        self.assertIn("types/skills/elements.md", (self.topic / "delivery/render.yaml").read_text())
        self.assertFalse((self.kept / "report").exists())
        self.assertEqual(self.run_it("--check"), 0)
        (self.topic / "elements.md").write_text("## B\nwhat: b\n")
        self.assertEqual(self.run_it("--check"), 1)                                     # the blueprint moved on
        self.assertEqual(self.run_it(), 0)

    def test_a_kept_type_nobody_delivers_and_a_name_two_deliver_are_reported(self):
        self.run_it()
        (self.kept / "orphan").mkdir()
        (self.kept / "orphan/elements.md").write_text("## X\n")
        self.assertEqual(self.run_it("--check"), 1)
        (self.kept / "orphan/elements.md").unlink()
        (self.kept / "orphan").rmdir()
        twin = self.space / "Q/blueprint/b11_y/s71-studio-type-skills"
        twin.mkdir(parents=True)
        (twin / "elements.md").write_text("## C\n")
        self.assertEqual(self.run_it("--check"), 1)


if __name__ == "__main__":
    unittest.main()
