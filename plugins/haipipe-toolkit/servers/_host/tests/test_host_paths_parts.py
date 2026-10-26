"""host_paths.skill_dir finds a skill wherever it lives: a skill folder, or a part of its door (<door>/_parts/<part>/)."""
import unittest

from host_paths import SKILLS, part_dir, skill_dir, skill_file


class PartsTest(unittest.TestCase):
    def test_a_part_is_found_by_its_old_skill_name_and_by_its_own(self):
        tex = SKILLS / "1_base/display/haipipe-display/_parts/tex"
        if not tex.is_dir():
            self.skipTest("no display parts in this checkout")
        self.assertEqual(skill_dir("haipipe-display-tex"), tex)
        self.assertEqual(part_dir("tex"), tex)
        self.assertEqual(skill_file("haipipe-display-tex").name, "PART.md")

    def test_a_skill_folder_still_wins_and_a_missing_name_stays_a_path(self):
        self.assertEqual(skill_dir("haipipe-draft").name, "haipipe-draft")
        self.assertEqual(skill_file("haipipe-draft").name, "SKILL.md")
        self.assertIsNone(part_dir("no-such-skill-anywhere"))
        self.assertEqual(skill_dir("no-such-skill-anywhere"), SKILLS / "no-such-skill-anywhere")


if __name__ == "__main__":
    unittest.main()
