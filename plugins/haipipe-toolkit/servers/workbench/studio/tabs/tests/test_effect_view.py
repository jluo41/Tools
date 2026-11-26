"""A UI preview topic: Page holds the live pages the server renders, Effect the quick html in delivery/ui/."""
import re
import tempfile
import unittest
from pathlib import Path

from host_paths import bootstrap

bootstrap()

from live import studio_tabs  # noqa: E402


def topic(root: Path, buttons: str) -> Path:
    t = root / "b01_example" / "s07-view"
    (t / "delivery" / "ui").mkdir(parents=True)
    (root / "b01_example" / "board.md").write_text("# Example\n")
    (t / "s07-view.md").write_text("s07 · View\n=========\n\n**Delivery type:** ui\n")
    (t / "delivery" / "ui" / "effects.html").write_text("<p>effects</p>")
    (t / "delivery" / "ui" / "old.html").write_text("<p>old</p>")
    (t / "s07-view.html").write_text(f"<nav>{buttons}</nav>")
    return t


LIVE = '<button data-src="/_board/workbench?path=b01_example&amp;layout=focus">Topic rows</button>'
QUICK = ('<button data-src="delivery/ui/effects.html">Effects</button>'
         '<button class="old" data-src="delivery/ui/old.html">Earlier</button>')


class EffectViewTest(unittest.TestCase):
    def render(self, buttons):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            t = topic(root, buttons)
            return studio_tabs.render([(t, [], {})], root)

    def views(self, html):
        return re.findall(r'data-studio-view="\d+"[^>]*>([^<]+)</button>', html)

    def test_live_and_quick_views_split_into_page_and_effect(self):
        html = self.render(LIVE + QUICK)
        self.assertEqual(self.views(html)[:2], ["Page", "Effect"])
        page, effect = re.findall(r'<div data-studio-content="(\d+)"[^>]*>(.*?)</div>(?=<div data-studio-content|</article>)', html, re.S)[:2]
        self.assertIn("/_board/workbench?path=b01_example", page[1])
        self.assertNotIn("effects.html", page[1])
        self.assertIn("effects.html", effect[1])
        self.assertIn("old.html", effect[1])

    def test_one_quick_view_still_has_its_left_tab(self):
        html = self.render(LIVE + '<button data-src="delivery/ui/effects.html">Task states</button>')
        effect = re.split(r'<div data-studio-content="1"', html)[1]
        self.assertIn("data-pbtab", effect)
        self.assertIn("Task states", effect)

    def test_a_page_of_files_only_keeps_one_page(self):
        html = self.render(QUICK)
        self.assertNotIn("Effect", self.views(html))
        self.assertIn("Page", self.views(html))


if __name__ == "__main__":
    unittest.main()


class TabResetTest(unittest.TestCase):
    def test_picked_tab_reopens_at_its_own_address(self):
        # a view or left tab picked marks its frames fresh, and load() sets their src again
        s = studio_tabs.SCRIPT
        self.assertIn(".studio-topic-content [data-pbtab]", s)
        self.assertIn("f.dataset.fresh='1'", s)
        self.assertIn("f.dataset.fresh)){", s)
