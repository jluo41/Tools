"""skill_text_check.py: a skill's text states the rule, names what is on disk, and carries no note or marker (A09)."""
import importlib.util
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "skill_text_check.py"
spec = importlib.util.spec_from_file_location("skill_text_check", SCRIPT)
check = importlib.util.module_from_spec(spec)
spec.loader.exec_module(check)


class SkillTextCheck(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.skill = Path(self.tmp.name) / "skill-x"
        (self.skill / "ref").mkdir(parents=True)
        (self.skill / "scripts").mkdir()
        (self.skill / "ref" / "a.md").write_text("# A\n\nThe rule.\n")
        (self.skill / "scripts" / "run.py").write_text("")
        self.write("# X\n\nRead `ref/a.md`. Run `scripts/run.py`.\n")

    def tearDown(self):
        self.tmp.cleanup()

    def write(self, text):
        (self.skill / "SKILL.md").write_text(text)

    def found(self):
        return check.problems(self.skill)[0]

    def test_one_blocks_type_named_by_number_is_flagged(self):
        self.write("# X\n\nRead `ref/a.md`. Run `scripts/run.py`.\n\n| s5N | s76 Skills |\n")
        self.assertTrue(any("names one Block's Studio Type" in line for line in self.found()))
        self.write("# X\n\nRead `ref/a.md`. Run `scripts/run.py`. Open the Studio Type band.\n")
        self.assertEqual(self.found(), [])

    def test_clean_text_passes(self):
        self.assertEqual(self.found(), [])
        self.assertEqual(check.main([str(self.skill)]), 0)

    def test_a_who_and_when_note_and_a_marker_are_flagged(self):
        self.write('# X\n\n<!-- render b35-s01 x -->\nThe look (JL 261112: "I want the vivid ones").\n`ref/a.md` `scripts/run.py`\n')
        found = "\n".join(self.found())
        self.assertIn("SKILL.md:3: a marker comment line", found)
        self.assertIn("SKILL.md:4: a who-and-when note", found)
        self.assertEqual(check.main([str(self.skill)]), 1)

    def test_a_note_in_a_ref_file_is_flagged_and_a_generated_one_is_skipped(self):
        (self.skill / "ref" / "a.md").write_text("# A\n\nAsked (JL 261030).\n")
        self.assertIn("ref/a.md:3: a who-and-when note", "\n".join(self.found()))
        (self.skill / "ref" / "a.md").write_text("<!-- GENERATED FILE by x -->\n(JL 261030)\n")
        found, skipped = check.problems(self.skill)
        self.assertEqual((found, skipped), ([], ["a.md"]))

    def test_a_named_file_must_exist_and_every_file_must_be_named(self):
        self.write("# X\n\nRead `ref/gone.md`.\n")
        found = "\n".join(self.found())
        self.assertIn("names ref/gone.md, which is not on disk", found)
        self.assertIn("never names ref/a.md", found)
        self.assertIn("never names scripts/run.py", found)


if __name__ == "__main__":
    unittest.main()
