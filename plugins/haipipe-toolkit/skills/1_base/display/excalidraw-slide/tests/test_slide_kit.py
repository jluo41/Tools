"""excalidraw-slide: the slides.py check and the slide palette, on a synthetic slide draft."""
import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))
import slide_kit  # noqa: E402

GOOD = textwrap.dedent('''
    AUDIENCE = "<who it is for>"
    LENGTH = "<minutes>"
    SHOWN = "<when it is shown>"
    GROUPS = [("why", "Why", "<the act>"), ("how", "How", "<the act>")]
    SLIDES = [
        {"n": "01", "slug": "the-pain", "group": "why", "title": "<title>", "headline": "<one sentence>",
         "visual": {"kind": "cover", "lines": ["<line>"]}, "caption": "<caption>", "source": "<source>",
         "next": "<why the next follows>", "notes": "<speaker notes>"},
        {"n": "02", "slug": "the-answer", "group": "how", "title": "<title>", "headline": "<one sentence>",
         "visual": {"kind": "flow", "steps": ["<a>", "<b>"], "hl": 1}, "caption": "<caption>",
         "source": "<source>", "next": "", "notes": "<speaker notes>"},
    ]
    OPEN = ["<an open question>"]
''')


class SlideKitTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.path = Path(self.tmp.name) / "slides.py"

    def tearDown(self):
        self.tmp.cleanup()

    def found(self, text):
        self.path.write_text(text)
        return slide_kit.check(self.path)

    def test_a_good_slides_py_holds(self):
        self.assertEqual(self.found(GOOD), [])

    def test_a_missing_field_and_an_out_of_order_slide(self):
        bad = GOOD.replace('"caption": "<caption>", ', "", 1).replace('"n": "02"', '"n": "03"')
        texts = [t for _, t in self.found(bad)]
        self.assertIn("slide 1: no caption", texts)
        self.assertTrue(any("expected '02'" in t for t in texts))

    def test_group_slug_and_visual_rules(self):
        bad = GOOD.replace('"group": "how"', '"group": "later"').replace('"the-answer"', '"the-pain"') \
                  .replace('{"kind": "flow", ', '{')
        texts = " | ".join(t for _, t in self.found(bad))
        self.assertIn("group 'later' is not in GROUPS", texts)
        self.assertIn("slug 'the-pain' is used twice", texts)
        self.assertIn("visual needs a kind", texts)

    def test_an_empty_next_warns_except_on_the_last_slide(self):
        found = self.found(GOOD.replace('"next": "<why the next follows>"', '"next": ""'))
        self.assertEqual(found, [("warn", "slide 1: next is empty (why the next slide follows)")])

    def test_ask_is_an_optional_list_of_questions(self):
        with_ask = GOOD.replace('"notes": "<speaker notes>"},', '"notes": "<speaker notes>", "ask": ["<a question?>"]},', 1)
        self.assertEqual(self.found(with_ask), [])
        bad = GOOD.replace('"notes": "<speaker notes>"},', '"notes": "<speaker notes>", "ask": "<not a list>"},', 1)
        self.assertTrue(any("ask is a list" in t for _, t in self.found(bad)))

    def test_a_slides_py_that_does_not_import_is_a_finding(self):
        found = self.found("SLIDES = [\n")
        self.assertEqual(found[0][0], "error")
        self.assertIn("does not import", found[0][1])

    def test_the_slide_palette_allows_the_accent_inside_a_slide(self):
        els = [{"type": "rectangle", "strokeColor": slide_kit.ACCENT, "backgroundColor": slide_kit.ACCENT_FILL},
               {"type": "text", "strokeColor": slide_kit.MUTED},
               {"type": "image", "strokeColor": "transparent", "backgroundColor": "#123456"},
               {"type": "text", "strokeColor": "#0c8599"}]
        self.assertEqual(slide_kit.off_palette(els), [els[3]])

    def test_the_studio_writer_keeps_the_same_colours(self):
        studio = SCRIPTS.parents[2] / "project" / "haipipe-studio" / "scripts"
        sys.path.insert(0, str(studio))
        import canvas
        self.assertEqual((canvas.ACCENT, canvas.ACCENT_FILL, canvas.MUTED),
                         (slide_kit.ACCENT, slide_kit.ACCENT_FILL, slide_kit.MUTED))
        self.assertTrue(canvas.is_slide_draft("s61-deck.excalidraw"))

    def test_the_cli(self):
        self.path.write_text(GOOD)
        out = subprocess.run([sys.executable, str(SCRIPTS / "slide_kit.py"), "check", str(self.path)],
                             capture_output=True, text=True)
        self.assertEqual(out.returncode, 0, out.stdout + out.stderr)


if __name__ == "__main__":
    unittest.main()
