"""md_sections: a view's one Markdown file reads as a left tab per `##` section."""
import json
import tempfile
import unittest
from pathlib import Path

from live import md_sections, studio_views

TEXT = "---\nname: x\n---\n\n# The Title\n\nA lead line.\n\n## One\n\nfirst\n\n```\n## not a heading\n```\n\n## Two `b`\n\nsecond\n"


class MdSections(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name).resolve()
        self.topic = self.root / "block" / "s21-x"
        self.topic.mkdir(parents=True)
        self.file = self.topic / "learning.md"
        self.file.write_text(TEXT)

    def tearDown(self):
        self.tmp.cleanup()

    def views(self, *items):
        (self.topic / "studio-views.json").write_text(json.dumps({"views": [{"name": "Page", "items": [
            {"name": n, "path": f"block/s21-x/{f}"} for n, f in items]}]}))
        return studio_views.read_views(self.topic, self.root)[1]["Page"]

    def test_the_lead_then_each_section_by_its_own_heading(self):
        self.assertEqual(md_sections.sections_of(self.file), ["The Title", "One", "Two b"])
        self.assertIn("first", md_sections.section_text(TEXT, 1))
        self.assertIn("## not a heading", md_sections.section_text(TEXT, 1))        # a fence is no heading
        self.assertNotIn("second", md_sections.section_text(TEXT, 1))

    def test_a_title_with_no_lead_is_no_tab_and_setext_headings_count(self):
        self.file.write_text("Title\n=====\n\nOne\n---\n\nfirst\n\nTwo\n---\n\nsecond\n")
        self.assertEqual(md_sections.sections_of(self.file), ["One", "Two"])

    def test_one_section_and_a_page_face_stay_whole(self):
        self.file.write_text("# T\n\n## Only\n\nx\n")
        self.assertEqual(md_sections.sections_of(self.file), [])
        self.file.write_text("# T\n\n## Opening\n\nx\n\n## More\n\ny\n")
        self.assertEqual(md_sections.sections_of(self.file), [])

    def test_a_view_with_one_markdown_file_gets_a_tab_per_section(self):
        items = self.views(("Page", "learning.md"))
        self.assertEqual([label for label, _, _ in items], ["The Title", "One", "Two b"])
        self.assertTrue(items[2][1].endswith("&section=2"))

    def test_a_view_with_several_items_keeps_each_file_whole(self):
        (self.topic / "other.md").write_text(TEXT)
        self.assertEqual([label for label, _, _ in self.views(("A", "learning.md"), ("B", "other.md"))], ["A", "B"])


if __name__ == "__main__":
    unittest.main()
