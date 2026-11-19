"""Tabs and paragraphs as cards (JL 261116): a content tab carries marks after its name and its cards on the right; a
paragraph with an id carries marks at its end; paragraph_ids.py gives the ids once."""
import importlib.util
import tempfile
import unittest
from pathlib import Path

from live import item_cards as IC
from live.paragraph_cards import mark_paragraphs
from live.tab_cards import slug
from live.ui_parts import _side_tabs

IDS = Path(__file__).resolve().parents[2] / "workbench-work" / "paragraph_ids.py"


def ids_module():
    spec = importlib.util.spec_from_file_location("paragraph_ids", IDS)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class TabParagraphCardsTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.page = self.root / "b01_study"
        self.page.mkdir()
        (self.page / "board.md").write_text("# b01\n")

    def tearDown(self):
        self.tmp.cleanup()

    def test_a_content_tab_carries_marks_and_its_cards_open_on_the_right(self):
        html = _side_tabs("fVx", [("Main estimates", "")], ["<p>table</p>"], cards=(self.page, self.root, "findings.values"))
        self.assertIn('<div class=pb-trow><button', html)
        self.assertIn('data-addr="findings.values.Main-estimates"', html)
        self.assertLess(html.index('data-im-slot="findings.values.Main-estimates"'), html.index("<p>table</p>"))
        self.assertNotIn("pb-trow", _side_tabs("x", [("Files", "")], ["<p>f</p>"]))        # structure tabs: none
        self.assertEqual(slug("The <b>sub</b>group (n=3)"), "The-subgroup-n-3")

    def test_a_paragraph_with_an_id_carries_marks_and_one_without_none(self):
        html = '<p>The census covers 67 tables. &lt;!-- id: p3 --&gt;</p><p>No id.</p><ul><li>An item &lt;!-- id: p4 --&gt;</li></ul>'
        out = mark_paragraphs(html, self.page, self.root, "findings")
        self.assertIn('data-addr="findings.p3"', out)
        self.assertIn('data-addr="findings.p4"', out)
        self.assertNotIn("id: p3", out)                                      # the id stays invisible
        self.assertIn('data-words="The census covers 67 tables."', out)
        self.assertEqual(mark_paragraphs("<p>No id.</p>", self.page, self.root, "findings"), "<p>No id.</p>")

    def test_paragraph_ids_are_given_once_and_never_renumbered(self):
        (self.page / "still-open.md").write_text("# Still open\n\n- One open thing.\n- **Header**\n- Two <!-- id: p07 -->\n"
                                                 "- Parent\n  - child\n")
        (self.page / "board.md").write_text("# b01\n\n## Findings\n\nA first paragraph\nover two lines.\n\n"
                                            "embed: still-open.md\n\n## Jobs\n\nNot an own section.\n")
        ids = ids_module()
        self.assertTrue(ids.run(self.page, apply=False))
        ids.run(self.page, apply=True)
        face = (self.page / "board.md").read_text()
        self.assertIn("over two lines. <!-- id: p08 -->", face)
        self.assertNotIn("own section. <!--", face)                         # outside an own section: untouched
        still = (self.page / "still-open.md").read_text()
        self.assertIn("- One open thing. <!-- id: p09 -->", still)
        self.assertIn("- **Header**\n", still)                               # a header item: none
        self.assertIn("- Parent\n", still)                                   # an item with sub-items: none
        self.assertEqual(ids.run(self.page, apply=True), [])                 # a second run adds nothing
        self.assertEqual(IC.cards(self.page), {})


if __name__ == "__main__":
    unittest.main()
