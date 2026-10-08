import unittest
from pathlib import Path
import re


SERVERS = next(p for p in Path(__file__).resolve().parents if p.name == "skills").parent / "servers"
WORKBENCHES = SERVERS.parents[1]


def drawer_parts():
    """Every 10-drawer/*.js part across the server folders of every workbench (a level folder of
    the base workbench, such as workbench/task-page, is one folder deeper)."""
    return sorted(p for servers in WORKBENCHES.glob("*/servers")
                  for pattern in ("*/assets/js/10-drawer/*.js", "*/*/assets/js/10-drawer/*.js")
                  for p in servers.glob(pattern))


def part(name):
    """One drawer part by file name, wherever its workbench lives."""
    found = [p for p in drawer_parts() if p.name == name]
    assert len(found) == 1, (name, found)
    return found[0]


class _Root:
    """`ROOT / name` and `ROOT.glob("*.js")` over the split drawer parts."""
    def __truediv__(self, name):
        found = [p for p in drawer_parts() if p.name == name]
        return found[0] if found else SERVERS / "_host" / "assets" / "js" / "10-drawer" / name

    def glob(self, pattern):
        return drawer_parts()


ROOT = _Root()


class WorkbenchMenuTest(unittest.TestCase):
    def test_picker_has_one_category_menu(self):
        registry = (ROOT / "05-workbenches.js").read_text(encoding="utf-8")
        picker = (ROOT / "50-structure.js").read_text(encoding="utf-8")
        pageflow = (ROOT / "65-workbench-pageflow.js").read_text(encoding="utf-8")
        slides = (ROOT / "70-workbench-slides.js").read_text(encoding="utf-8")
        draw = (ROOT / "80-workbench-draw.js").read_text(encoding="utf-8")
        delivery = (ROOT / "82-workbench-delivery.js").read_text(encoding="utf-8")
        design = (ROOT / "30-workbench-design.js").read_text(encoding="utf-8")

        self.assertIn("var MENUS = ['workbench'];", registry)
        self.assertIn("pick.innerHTML = group('\\u{1F50C} Workbench', 'workbench');", picker)
        self.assertNotIn("group('\\u{1FA9C} Workflow'", picker)
        self.assertIn("id: 'studio'", picker)
        self.assertNotIn("id: 'chat', label:", picker)
        self.assertNotIn("window.boardWorkbenches.register({", pageflow)
        self.assertNotIn("window.boardWorkbenches.register({", slides)
        self.assertNotIn("window.boardWorkbenches.register({", draw)
        self.assertIn("id: 'delivery'", delivery)
        self.assertIn("id: 'design'", design)
        self.assertIn("data-folder-kind", design)
        self.assertIn("Design Items across Goal, Design, Insight, Run, and Delivery Space", design)

    def test_outline_deep_links_route_runs_and_feedback_through_one_url(self):
        # The three-pane shell (servers/haipipe-board/shell.py) retired with the static site
        # (JL 261004); only the drawer's own half of the deep link is checked here.
        outline = (ROOT / "07-workbench-outline.js").read_text(encoding="utf-8")
        self.assertIn("a[data-outline-focus]", outline)
        self.assertIn("var lens = link.getAttribute('data-outline-lens')", outline)
        self.assertIn("var seg = link.getAttribute('data-outline-seg') || ''", outline)
        self.assertIn("var direct = url + '&lens=' + encodeURIComponent(lens)", outline)
        self.assertIn("if (seg) direct += '&seg='", outline)
        self.assertIn("if (focus) direct += '&focus='", outline)
        self.assertIn("if (run) direct += '&run='", outline)
        self.assertIn("event.stopImmediatePropagation()", outline)
        self.assertIn("parent.__boardShowTab('outline', direct)", outline)
        self.assertNotIn("localStorage.setItem('board-outline-evidence-focus'", outline)
        self.assertIn("event.metaKey || event.ctrlKey || event.shiftKey", outline)
        self.assertFalse((ROOT / "84-workbench-evidence.js").exists())

    def test_picker_uses_explicit_reader_order(self):
        registry = (ROOT / "05-workbenches.js").read_text(encoding="utf-8")
        sources = {
            "outline": ROOT / "07-workbench-outline.js",
            "studio": ROOT / "50-structure.js",
            "design": ROOT / "30-workbench-design.js",
            "delivery": ROOT / "82-workbench-delivery.js",
            "folder": ROOT / "06-workbench-folder.js",
            "labeling": ROOT / "60-workbench-labeling.js",
        }
        expected = {
            "outline": 10,
            "studio": 20,
            "design": 30,
            "runs": 30,
            "delivery": 40,
            "folder": 50,
            "labeling": 70,
        }

        self.assertIn("function ordered(entries)", registry)
        self.assertIn("return ordered(reg.filter", registry)
        self.assertIn("all: function () { return ordered(reg); }", registry)
        for workbench_id, path in sources.items():
            source = path.read_text(encoding="utf-8")
            match = re.search(
                rf"id:\s*'{workbench_id}'.*?order:\s*(\d+)", source, re.DOTALL
            )
            self.assertIsNotNone(match, workbench_id)
            self.assertEqual(int(match.group(1)), expected[workbench_id])
        runs = (ROOT / "85-workbench-runs.js").read_text(encoding="utf-8")
        self.assertNotIn("window.boardWorkbenches.register({", runs)
        for source in ROOT.glob("*.js"):
            self.assertNotIn("id: 'evidence'", source.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
