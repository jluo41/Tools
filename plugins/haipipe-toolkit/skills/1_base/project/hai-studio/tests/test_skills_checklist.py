"""skills_checklist.py: a Skills topic held against its type, one line per part, in the topic's own face (A06, A08)."""
import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))
import skills_views  # noqa: E402

spec = importlib.util.spec_from_file_location("skills_checklist", SCRIPTS / "skills_checklist.py")
skills_checklist = importlib.util.module_from_spec(spec)
spec.loader.exec_module(skills_checklist)

FACE = "s51 · Skills: X\n===============\nview: overview\n\n**Stage:** shaping\n\n\nDecided\n-------\n\n- s51-D01 · kept\n"


class SkillsChecklist(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.space = Path(self.tmp.name).resolve()
        self.old, skills_views.SPACE = skills_views.SPACE, self.space
        full = self.space / "skills" / "full"
        for sub, name in (("ref", "a.md"), ("tests", "test_run.py")):
            (full / sub).mkdir(parents=True)
            (full / sub / name).write_text("x")
        for name in ("SKILL.md", "CHANGELOG.md"):
            (full / name).write_text("x")
        self.topic = self.space / "block" / "s51-skills-x"
        self.topic.mkdir(parents=True)
        self.face = self.topic / "s51-skills-x.md"
        self.face.write_text(FACE)
        skills_views.main(["block/s51-skills-x", "--skills", "skills/full"])

    def tearDown(self):
        skills_views.SPACE = self.old
        self.tmp.cleanup()

    def marks(self):
        return {line.split(" ", 2)[2].split(" · ")[0].split(":")[0]: line[2] for line in skills_checklist.lines_of(self.topic)}

    def test_has_and_does_not_apply(self):
        self.assertEqual(self.marks(), {"〈skill〉": "✅", "SKILL.md": "✅", "CONSTITUTION.md": "—", "ref/": "✅",
                                        "scripts/": "—", "〈folder〉/": "✅", "〈file〉": "✅"})
        self.assertIn("- ✅ 〈folder〉/ · tests/", skills_checklist.lines_of(self.topic))

    def test_the_managed_check_button_is_no_skill(self):
        import json
        views = self.topic / "studio-views.json"
        data = json.loads(views.read_text())
        data["check_type"] = "block/s76-type"
        data["views"].append({"name": "Check", "items": [{"name": "full", "path": "block/s51-skills-x/delivery/check.html"}]})
        views.write_text(json.dumps(data))
        self.assertEqual(self.marks()["〈skill〉"], "✅")

    def name_type(self, elements):
        import json
        kind = self.space / "block" / "s76-type"
        kind.mkdir(exist_ok=True)
        (kind / "elements.md").write_text(elements)
        views = self.topic / "studio-views.json"
        data = json.loads(views.read_text())
        data["check_type"] = "block/s76-type"
        views.write_text(json.dumps(data))

    def test_the_parts_come_from_the_type_the_topic_names(self):
        self.name_type("## 〈skill〉\nwhat: a skill\n\n### SKILL.md\nwhat: it\n\n### 〈notes〉\nwhat: new\n")
        lines = skills_checklist.lines_of(self.topic)
        self.assertEqual([ln.split(" ")[2].rstrip(":") for ln in lines], ["〈skill〉", "SKILL.md", "〈notes〉"])
        self.assertTrue(lines[2].startswith("- ❗ 〈notes〉: the type lists it"))

    def test_a_type_with_a_draw_button_gets_a_draw_line(self):
        self.name_type("## 〈skill〉\nwhat: a skill\n\n### SKILL.md\nwhat: it\ncheck: open it\n\n## Draw\nwhat: the drawing\n")
        self.assertIn("- — Draw: the topic has no drawing", skills_checklist.lines_of(self.topic))
        (self.topic / "s51-skills-x.excalidraw").write_text("{}")
        self.assertIn("- ❗ Draw: the topic has a drawing but shows no Draw button", skills_checklist.lines_of(self.topic))
        skills_views.main(["block/s51-skills-x"])
        self.assertIn("- ✅ Draw · the topic's drawing", skills_checklist.lines_of(self.topic))
        self.assertEqual(self.marks()["〈skill〉"], "✅")                  # the Draw button is no skill

    def test_a_part_the_skill_gained_reads_as_lacking(self):
        (self.space / "skills" / "full" / "scripts").mkdir()
        (self.space / "skills" / "full" / "scripts" / "run.py").write_text("x")
        self.assertEqual(self.marks()["scripts/"], "❗")
        self.assertIn("- ❗ scripts/: full has scripts/ but shows no tab", skills_checklist.lines_of(self.topic))
        self.assertEqual(skills_checklist.main(["block/s51-skills-x", "--check"]), 1)

    def test_the_block_is_written_before_decided_and_refreshed_in_place(self):
        self.assertEqual(skills_checklist.main(["block/s51-skills-x", "--check"]), 1)          # no block yet: stale
        self.assertEqual(skills_checklist.main(["block/s51-skills-x"]), 0)
        text = self.face.read_text()
        self.assertLess(text.index("Checklist\n---------"), text.index("Decided\n-------"))
        self.assertIn("- s51-D01 · kept", text)
        self.assertEqual(skills_checklist.main(["block/s51-skills-x", "--check"]), 0)
        self.face.write_text(text.replace("\n\n\nDecided", "\n\n- a line written by hand\n\n\nDecided"))
        (self.space / "skills" / "full" / "CONSTITUTION.md").write_text("x")
        skills_views.main(["block/s51-skills-x"])
        self.assertEqual(skills_checklist.main(["block/s51-skills-x"]), 0)
        text = self.face.read_text()
        self.assertEqual(text.count("- ✅ SKILL.md"), 1)                 # replaced in place, never doubled
        self.assertIn("- a line written by hand", text)
        self.assertIn("- ✅ CONSTITUTION.md · full", text)
        self.assertNotIn("- — CONSTITUTION.md", text)
        self.assertNotIn("<!--", text)                                    # no marker line: the page would show it
        self.assertEqual(skills_checklist.main(["block/s51-skills-x"]), 0)
        self.assertEqual(self.face.read_text(), text)                     # writing twice changes nothing

    def test_an_earlier_marker_block_is_cleaned(self):
        skills_checklist.main(["block/s51-skills-x"])
        text = self.face.read_text().replace("- ✅ 〈skill〉", "<!-- type-check:start s76-studio-type-skills -->\n- ✅ 〈skill〉")
        self.face.write_text(text.replace("\n\n\nDecided", "\n<!-- type-check:end -->\n\n\nDecided"))
        self.assertEqual(skills_checklist.main(["block/s51-skills-x"]), 0)
        self.assertNotIn("type-check", self.face.read_text())

if __name__ == "__main__":
    unittest.main()
