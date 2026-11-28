"""skills_views.py: a Skills topic's studio-views.json is the skill's whole top level, in a fixed order (A08)."""
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "skills_views.py"
spec = importlib.util.spec_from_file_location("skills_views", SCRIPT)
skills_views = importlib.util.module_from_spec(spec)
spec.loader.exec_module(skills_views)


class SkillsViews(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.space = Path(self.tmp.name).resolve()
        self.old, skills_views.SPACE = skills_views.SPACE, self.space
        full = self.space / "skills" / "full"
        for sub, name in (("ref", "a.md"), ("scripts", "run.py"), ("tests", "test_run.py"), ("agents", "x.yaml")):
            (full / sub).mkdir(parents=True)
            (full / sub / name).write_text("x")
        (full / "empty").mkdir()
        (full / "__pycache__").mkdir()
        (full / "__pycache__" / "run.pyc").write_text("x")
        for name in ("SKILL.md", "CONSTITUTION.md", "CHANGELOG.md"):
            (full / name).write_text("x")
        bare = self.space / "skills" / "bare"
        bare.mkdir()
        (bare / "SKILL.md").write_text("x")
        self.topic = self.space / "block" / "s51-skills-x"
        self.topic.mkdir(parents=True)

    def tearDown(self):
        skills_views.SPACE = self.old
        self.tmp.cleanup()

    def names(self, skill):
        return [item["name"] for item in skills_views.items_of(skill)]

    def test_left_is_the_whole_top_level_in_order(self):
        self.assertEqual(self.names("skills/full"), ["SKILL.md", "CONSTITUTION.md", "ref/", "scripts/", "agents/",
                                                     "tests/", "CHANGELOG.md"])    # the names on disk, no alias
        items = skills_views.items_of("skills/full")
        self.assertEqual(items[2], {"name": "ref/", "folder": "skills/full/ref"})
        self.assertEqual(items[-1], {"name": "CHANGELOG.md", "path": "skills/full/CHANGELOG.md"})

    def test_a_part_the_skill_lacks_has_no_tab(self):
        self.assertEqual(self.names("skills/bare"), ["SKILL.md"])

    def test_write_then_check_then_stale(self):
        run = lambda *a: skills_views.main(["block/s51-skills-x", *a])  # noqa: E731
        self.assertEqual(run("--skills", "skills/full", "skills/bare"), 0)
        views = json.loads((self.topic / "studio-views.json").read_text())["views"]
        self.assertEqual([v["name"] for v in views], ["full", "bare"])
        self.assertEqual(skills_views.skills_of(self.topic), ["skills/full", "skills/bare"])
        self.assertEqual(run("--check"), 0)
        (self.space / "skills" / "bare" / "ref").mkdir()
        (self.space / "skills" / "bare" / "ref" / "new.md").write_text("x")
        self.assertEqual(run("--check"), 1)                    # the skill gained a folder: the views file is stale
        self.assertEqual(run(), 0)
        self.assertEqual(self.names("skills/bare"), ["SKILL.md", "ref/"])
        self.assertEqual(run("--check"), 0)

    def test_a_topic_with_its_own_drawing_gets_a_last_draw_button(self):
        run = lambda *a: skills_views.main(["block/s51-skills-x", *a])  # noqa: E731
        self.assertEqual(run("--skills", "skills/full"), 0)
        (self.topic / "s51-skills-x.excalidraw").write_text("{}")
        self.assertEqual(run("--check"), 1)                    # a drawing arrived: the views file is stale
        self.assertEqual(run(), 0)
        views = json.loads((self.topic / "studio-views.json").read_text())["views"]
        self.assertEqual([v["name"] for v in views], ["full", "Draw"])
        self.assertEqual(views[-1]["items"][0]["path"], "block/s51-skills-x/s51-skills-x.excalidraw")
        self.assertEqual(skills_views.skills_of(self.topic), ["skills/full"])     # the Draw button is no skill

    def test_a_skill_without_skill_md_is_refused(self):
        self.assertEqual(skills_views.main(["block/s51-skills-x", "--skills", "skills/none"]), 1)


if __name__ == "__main__":
    unittest.main()
