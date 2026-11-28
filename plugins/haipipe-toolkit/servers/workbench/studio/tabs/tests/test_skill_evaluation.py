"""skill_evaluation: one skill measured from its own files, each criterion with its mark and what was found."""
import tempfile
import unittest
from pathlib import Path

from live import skill_evaluation

GOOD = '---\nname: skill-x\ndescription: "Does x. Trigger: x, /skill-x."\nmetadata:\n  version: "0.2.0"\n---\n\n# X\n\nRead `ref/a.md`. Run `scripts/run.py`.\n'


class SkillEvaluation(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name).resolve()
        self.skill = self.root / "skills" / "skill-x"
        for sub in ("ref", "scripts", "tests"):
            (self.skill / sub).mkdir(parents=True)
        (self.skill / "SKILL.md").write_text(GOOD)
        (self.skill / "ref" / "a.md").write_text("# A\n\nThe rule.\n")
        (self.skill / "scripts" / "run.py").write_text("")
        (self.skill / "tests" / "test_run.py").write_text("import run\n")
        (self.skill / "CHANGELOG.md").write_text("# Changelog\n\n## [0.2.0] — today\n")

    def tearDown(self):
        self.tmp.cleanup()

    def marks(self):
        return {name: mark for mark, name, _, _ in skill_evaluation.evaluate(self.skill)}

    def test_a_sound_skill_holds_and_a_fresh_agent_stays_a_persons_call(self):
        marks = self.marks()
        self.assertEqual({m for n, m in marks.items() if n not in ("Rules can be checked", "A fresh agent can use it")}, {"✅"})
        self.assertEqual(marks["Rules can be checked"], "—")                    # no CONSTITUTION.md: does not apply
        self.assertEqual(marks["A fresh agent can use it"], "🙋")                # never counted as passed

    def test_each_weakness_lands_on_its_own_criterion(self):
        (self.skill / "SKILL.md").write_text(GOOD.replace("name: skill-x", "name: other").replace('"0.2.0"', '"0.3.0"')
                                             + "\n(JL 261112: \"a note\")\n" + "x\n" * 720)
        (self.skill / "scripts" / "lone.py").write_text("")
        (self.skill / "CONSTITUTION.md").write_text("# Rules\n\n## A01 · One\n\n**Rule:** x\n")
        marks = self.marks()
        for name in ("Found by its name", "Read in one sitting", "No file too long", "States the rule only",
                     "Nothing unreachable", "Rules can be checked", "Version is recorded"):
            self.assertEqual(marks[name], "❗", name)
        self.assertEqual(marks["Scripts are tested"], "🔶")                      # one of two scripts has no test
        rows = {name: lines for _, name, _, lines in skill_evaluation.evaluate(self.skill)}
        self.assertIn("lone.py", rows["Scripts are tested"])
        self.assertTrue(any("A01 · One" in x for x in rows["Rules can be checked"]))

    def test_the_page_opens_what_does_not_hold_and_shows_no_tally(self):
        (self.skill / "scripts" / "run.py").write_text("x = 1\n" * 720)
        page = skill_evaluation.document(self.skill, self.root)
        self.assertIn("<details open><summary><i>❗</i><b>No file too long</b>", page)
        self.assertNotRegex(page, r"\d+ of \d+")
        self.assertEqual(skill_evaluation.document(self.root / "skills", self.root), "")       # no SKILL.md: no page
        self.assertEqual(skill_evaluation.document(self.root.parent, self.root), "")          # outside the SPACE


if __name__ == "__main__":
    unittest.main()
