"""A Studio type's elements.md: its Elements view, and what a right-click says about each element."""
import tempfile
import unittest
from pathlib import Path

from host_paths import bootstrap

bootstrap()

from live import studio_types  # noqa: E402

ELEMENTS = """# Elements

page: examples/Project-Ladder/work/b01_example_work
query: section=jobs&group=j11

### Job type row
mark: job-types
from: `job-type:` on each Job face
what: Filters the Jobs by kind.
why: A Block mixes kinds of Jobs.

### Main
mark: jsub-to=main
what: The Job itself.
"""


class StudioTypeElementsTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name).resolve()
        self.topic = self.root / studio_types.HOME / "s71-studio-type-x"
        self.topic.mkdir(parents=True)
        (self.topic / "s71-studio-type-x.md").write_text("s71 · Studio Type: X\n=====\nemoji: 👀\nband: s1N\nname: X\n")
        (self.topic / "elements.md").write_text(ELEMENTS)
        (self.root / "examples/Project-Ladder/work/b01_example_work").mkdir(parents=True)

    def tearDown(self):
        self.tmp.cleanup()

    def test_defaults_reach_every_element(self):
        els = studio_types.elements_of(self.topic)
        self.assertEqual([e["name"] for e in els], ["Job type row", "Main"])
        self.assertEqual(els[1]["query"], "section=jobs&group=j11")

    def test_the_elements_view_shows_each_element_marked_on_the_live_page(self):
        view = studio_types.element_view(self.topic, self.root)
        self.assertEqual([name for name, _, _ in view], ["Job type row", "Main"])
        self.assertIn("section=jobs", view[0][1])
        self.assertTrue(view[0][1].endswith("&mark=job-types"))
        self.assertTrue(view[1][1].endswith("&mark=jsub-to=main"))

    def test_a_right_click_finds_a_row_by_its_mark(self):
        about = studio_types.element_about(self.root)
        self.assertEqual([a["css"] for a in about], [".job-types", '[data-jsub-to="main"]'])
        self.assertEqual((about[0]["what"], about[0]["why"], about[0]["type"]),
                         ("Filters the Jobs by kind.", "A Block mixes kinds of Jobs.", "X"))

    def test_a_tab_is_found_inside_its_own_view_in_the_type_and_its_instances(self):
        (self.topic / "elements.md").write_text(
            'instances: article[id^="s1"]\n\n## Page\nwhat: The pages.\n\n### Job\nwhat: A Job.\nmust:\n- its rows\n- its Main\n'
            'check: the page opens\n\n## Draw\nwhat: The drawing.\n\n### Job\nwhat: A Job, drawn.\n')
        (self.topic / "studio-views.json").write_text('{"views": [{"name": "Page", "items": []}, {"name": "Draw", "items": []}]}')
        els = studio_types.elements_of(self.topic)
        self.assertEqual([(e["view"], e["tab"]) for e in els], [("Page", None), ("Page", "Job"), ("Draw", None), ("Draw", "Job")])
        self.assertEqual((els[1]["must"], els[1]["check"]), (["its rows", "its Main"], "the page opens"))
        about = {a["css"]: a["what"] for a in studio_types.element_about(self.root)}
        scope = ':is(article[id="s71-studio-type-x"],article[id^="s1"])'
        self.assertEqual(about[f"{scope} [data-studio-view]"], "The drawing.")       # both buttons share the selector, told apart by text
        self.assertEqual(about[f'{scope} [data-studio-name="Page"] .pb-item'], "A Job.")
        self.assertEqual(about[f'{scope} [data-studio-name="Draw"] .pb-item'], "A Job, drawn.")


class BaseTypeTest(unittest.TestCase):
    """A type with a `base:` line starts from the base's parts; its own tabs come before the base's."""

    def test_own_tabs_first_then_the_base(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp).resolve()
            (root / "plugins/haipipe-toolkit").mkdir(parents=True)
            base = root / "base/learning"
            base.mkdir(parents=True)
            (base / "elements.md").write_text("## Page\nwhat: The page.\n\n### Try explaining\nwhat: Explain it.\n\n"
                                              "## Draw\nwhat: The drawing.\n\n### 〈topic title〉\nwhat: One canvas.\n")
            kind = root / "block/s78-studio-type-method"
            kind.mkdir(parents=True)
            (kind / "elements.md").write_text("base: base/learning\ninstances: article[id=\"s21-x\"]\n\n"
                                              "## Page\n\n### Where you start\nwhat: The start.\n")
            els = studio_types.elements_of(kind)
            self.assertEqual([(e["view"], e["tab"]) for e in els],
                             [("Page", None), ("Page", "Where you start"), ("Page", "Try explaining"),
                              ("Draw", None), ("Draw", "〈topic title〉")])
            self.assertEqual(els[0]["what"], "The page.")                         # the type wrote Page again, empty: the base fills it
            self.assertTrue(all(e["instances"] == 'article[id="s21-x"]' for e in els))
