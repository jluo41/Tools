"""studio_types.type_home: a topic names its type; the SPACE's blueprint is read first, then the kept copy."""
import tempfile
import unittest
from pathlib import Path

from live import studio_types


class TypeHome(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name).resolve() / "space"
        self.kept = Path(self.tmp.name).resolve() / "kept"
        self.old, studio_types.KEPT = studio_types.KEPT, self.kept
        for folder in (self.root / "P/blueprint/b17_x/s75-studio-type-skills", self.kept / "skills", self.kept / "report"):
            folder.mkdir(parents=True)
            (folder / "elements.md").write_text("## A\nwhat: a\n")

    def tearDown(self):
        studio_types.KEPT = self.old
        self.tmp.cleanup()

    def test_a_name_reads_the_blueprint_of_this_space_then_the_kept_copy(self):
        self.assertEqual(studio_types.type_home("skills", self.root), self.root / "P/blueprint/b17_x/s75-studio-type-skills")
        self.assertEqual(studio_types.type_home("report", self.root), self.kept / "report")
        self.assertIsNone(studio_types.type_home("nothing", self.root))
        self.assertEqual(studio_types.type_name("s75-studio-type-skills"), "skills")

    def test_a_path_still_reads_and_never_leaves_the_space(self):
        self.assertEqual(studio_types.type_home("P/blueprint/b17_x/s75-studio-type-skills", self.root),
                         self.root / "P/blueprint/b17_x/s75-studio-type-skills")
        self.assertIsNone(studio_types.type_home("../kept/skills", self.root))
        self.assertIsNone(studio_types.type_home("/etc", self.root))
        self.assertIsNone(studio_types.type_home("Skills!", self.root))


if __name__ == "__main__":
    unittest.main()


class NamedBy(unittest.TestCase):
    def test_a_types_instances_are_the_topics_of_its_block_that_name_it(self):
        import json
        with tempfile.TemporaryDirectory() as tmp:
            block = Path(tmp).resolve() / "P/blueprint/b17_x"
            kind = block / "s75-studio-type-skills"
            for name, named in (("s51-skills-a", "skills"), ("s60-skill-b", "P/blueprint/b17_x/s75-studio-type-skills"),
                                ("s11-other", "block-structure"), ("s12-none", None), (kind.name, "skills")):
                (block / name).mkdir(parents=True)
                (block / name / "studio-views.json").write_text(json.dumps({"check_type": named, "views": []}))
            self.assertEqual(studio_types.named_by(kind), ["s51-skills-a", "s60-skill-b"])     # by name or by path; not itself
