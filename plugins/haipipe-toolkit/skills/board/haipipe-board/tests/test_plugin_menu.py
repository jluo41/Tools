import unittest
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1] / "assets" / "js" / "10-drawer"


class PluginMenuTest(unittest.TestCase):
    def test_picker_has_one_category_menu(self):
        registry = (ROOT / "05-plugins.js").read_text(encoding="utf-8")
        picker = (ROOT / "50-structure.js").read_text(encoding="utf-8")
        pageflow = (ROOT / "65-plugin-pageflow.js").read_text(encoding="utf-8")
        slides = (ROOT / "70-plugin-slides.js").read_text(encoding="utf-8")
        draw = (ROOT / "80-plugin-draw.js").read_text(encoding="utf-8")
        delivery = (ROOT / "82-plugin-delivery.js").read_text(encoding="utf-8")

        self.assertIn("var MENUS = ['plugin'];", registry)
        self.assertIn("pick.innerHTML = group('\\u{1F50C} Plugin', 'plugin');", picker)
        self.assertNotIn("group('\\u{1FA9C} Workflow'", picker)
        self.assertIn("id: 'studio'", picker)
        self.assertNotIn("id: 'chat', label:", picker)
        self.assertNotIn("window.boardPlugins.register({", pageflow)
        self.assertNotIn("window.boardPlugins.register({", slides)
        self.assertNotIn("window.boardPlugins.register({", draw)
        self.assertIn("id: 'delivery'", delivery)

    def test_page_pane_hides_its_duplicate_picker(self):
        shell = (ROOT.parents[2] / "live" / "shell.py").read_text(encoding="utf-8")
        self.assertIn("body.pane-page #chatfabmore", shell)
        self.assertIn("window.__boardShowTab = showTab;", shell)

    def test_outline_run_link_opens_outline_evidence_workspace(self):
        outline = (ROOT / "07-plugin-outline.js").read_text(encoding="utf-8")
        self.assertIn("a[data-outline-focus]", outline)
        self.assertIn("localStorage.setItem('board-outline-lens', 'workspace')", outline)
        self.assertIn("localStorage.setItem('board-outline-evidence-focus', focus)", outline)
        self.assertIn("parent.__boardShowTab('outline')", outline)
        self.assertIn("event.metaKey || event.ctrlKey || event.shiftKey", outline)
        self.assertFalse((ROOT / "84-plugin-evidence.js").exists())

    def test_picker_uses_explicit_reader_order(self):
        registry = (ROOT / "05-plugins.js").read_text(encoding="utf-8")
        sources = {
            "outline": ROOT / "07-plugin-outline.js",
            "studio": ROOT / "50-structure.js",
            "runs": ROOT / "85-plugin-runs.js",
            "delivery": ROOT / "82-plugin-delivery.js",
            "folder": ROOT / "06-plugin-folder.js",
            "labeling": ROOT / "60-plugin-labeling.js",
        }
        expected = {
            "outline": 10,
            "studio": 20,
            "runs": 30,
            "delivery": 40,
            "folder": 50,
            "labeling": 70,
        }

        self.assertIn("function ordered(entries)", registry)
        self.assertIn("return ordered(reg.filter", registry)
        self.assertIn("all: function () { return ordered(reg); }", registry)
        for plugin_id, path in sources.items():
            source = path.read_text(encoding="utf-8")
            match = re.search(
                rf"id:\s*'{plugin_id}'.*?order:\s*(\d+)", source, re.DOTALL
            )
            self.assertIsNotNone(match, plugin_id)
            self.assertEqual(int(match.group(1)), expected[plugin_id])
        for source in ROOT.glob("*.js"):
            self.assertNotIn("id: 'evidence'", source.read_text(encoding="utf-8"))
        skill = (ROOT / "83-plugin-skillmap.js").read_text(encoding="utf-8")
        self.assertNotIn("window.boardPlugins.register({", skill)


if __name__ == "__main__":
    unittest.main()
