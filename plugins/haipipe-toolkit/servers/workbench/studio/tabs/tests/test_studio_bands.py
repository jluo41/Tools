"""Studio topics group by the bands the Block's board names (`bands: s0N ... · s3N ...`), else by their tags."""
import re
import json
import tempfile
import unittest
from pathlib import Path

from host_paths import bootstrap

bootstrap()

from live import studio_tabs  # noqa: E402


def block(root: Path, bands: str) -> list:
    b = root / "b01_example"
    b.mkdir()
    (b / "board.md").write_text(f"# Example\n\n{bands}\n")
    rows = []
    for name, tag in (("s01-ladder", "Structure"), ("s31-files-pane", "All pages"), ("s32-trace-section", "All pages")):
        (b / name).mkdir()
        emoji = "emoji: 🧵\n" if name == "s32-trace-section" else ""
        (b / name / f"{name}.md").write_text(f"{name} · Title\n=====\n{emoji}\n**Tags:** `{tag}`\n")
        rows.append((b / name, [], {"tags": [tag]}))
    return rows


def bands(html: str) -> list:
    return re.findall(r'<h2 id="studio-band-\d+">([^<]+)</h2>', html)


class StudioBandsTest(unittest.TestCase):
    def render(self, line):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            return studio_tabs.render(block(root, line), root)

    def test_named_bands_group_the_topics_by_decade(self):
        html = self.render("bands: j1N 🧰 Workbench · s0N 🪜 Work ladder · s3N 📁 Side pane")
        self.assertEqual(bands(html), ["🪜 Work ladder", "📁 Side pane"])
        side = html.split("📁 Side pane", 1)[1]
        self.assertIn("s31-files-pane", side)
        self.assertIn("s32-trace-section", side)

    def test_without_s_bands_the_tags_group_them(self):
        self.assertEqual(sorted(bands(self.render("bands: j1N Workbench"))), ["All pages", "Structure"])

    def test_a_topic_names_its_own_emoji_else_the_palette(self):
        html = self.render("bands: s0N 🪜 Work ladder · s3N 📁 Side pane")
        self.assertIn("🧵 Title", html)
        self.assertIn(".studio-topic-content .pb-list{min-width:0;overflow-x:auto", html)   # left tabs scroll sideways
        self.assertIn(".pb-side{grid-template-columns:max-content minmax(0,1fr)", html)       # as wide as their names
        self.assertIn(".studio-topic-content .pb-list{max-width:170px}", html)                # and never wider than this
        self.assertIn("🎨 Title", html)
        self.assertIn("if(!d.open)return false", html)   # a frame in a closed fold does not load


class StudioTypesTest(unittest.TestCase):
    def fixture(self, root):
        home = root / "examples/Project-Ladder/blueprint/b17_theme_work"
        registry = home / "delivery/page-spec/studio-bands.json"
        registry.parent.mkdir(parents=True)
        registry.write_text(json.dumps({"bands": [
            {"band": "s0N", "emoji": "🧱", "name": "Block Structure"},
            {"band": "s3N", "emoji": "🧩", "name": "UI Plugin"},
            {"band": "s4N", "emoji": "🪜", "name": "Task Procedure"},
            {"band": "s7N", "emoji": "🏷️", "name": "Studio Type"},
            {"band": "s9N", "emoji": "🧭", "name": "Guide"}]}))
        return home

    def test_bands_survive_without_recursive_or_procedure_or_guide_types(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            home = self.fixture(root)
            (home / "board.md").write_text("# Example\nbands: s7N Wrong local name\n")
            rows = []
            for name in ("s41-method", "s71-studio-type-structure", "s99-guide"):
                topic = home / name
                topic.mkdir()
                (topic / f"{name}.md").write_text(f"{name} · Topic\n=====\n")
                rows.append((topic, [], {}))
            html = studio_tabs.render(rows, root)
            self.assertEqual(bands(html), ["🪜 Task Procedure", "🏷️ Studio Type", "🧭 Guide"])
            for name in ("s41-method", "s71-studio-type-structure", "s99-guide"):
                self.assertIn(name, html)
            self.assertNotIn("Wrong local name", html)
            self.assertNotIn("Block Structure</h2>", html)  # empty groups stay absent
            self.assertFalse(any(home.glob("s77*")))

    def test_blueprints_share_bands_but_actual_work_keeps_its_own_groups(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            home = self.fixture(root)
            other = home.parent / "b02_other"
            work = home.parent.parent / "work/b03_actual"
            for owner in (home, other, work):
                owner.mkdir(parents=True, exist_ok=True)
                (owner / "board.md").write_text("# Example\nbands: s0N Local topics\n")
            self.assertEqual(studio_tabs.studio_bands(home, root), studio_tabs.studio_bands(other, root))
            self.assertEqual(studio_tabs.studio_bands(work, root), {"0": "Local topics"})
            self.assertNotIn("7", studio_tabs.studio_bands(work, root))
