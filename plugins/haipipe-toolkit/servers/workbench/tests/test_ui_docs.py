"""A theme Block's Docs view: one place per view and section (JL 261115)."""
import tempfile
import unittest
from pathlib import Path

from host_paths import bootstrap

bootstrap()
from live import ui_docs  # noqa: E402

TABLE = ("| Category | Block Type | Use Cases | 💡 Idea | 📖 Story |\n| --- | --- | --- | --- | --- |\n"
         "| 📄 Paper | 📄 Paper Board | Manuscript | 🔀 Directions<br>🎓 Theory | — |\n")


def section(n, title, body):
    return f"<section><h3>{n} · {title}</h3>{body}</section>"


class UiDocsTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.block = self.root / "b16"
        (self.block / "ui").mkdir(parents=True)
        (self.block / "ui" / "block-views.md").write_text(TABLE, encoding="utf-8")

    def tearDown(self):
        self.tmp.cleanup()

    def test_each_view_lists_its_sections_and_skips_a_dash(self):
        views, rows = ui_docs.table(self.block / "ui" / "block-views.md")
        self.assertEqual(rows[0][0], "📄 Paper Board")
        self.assertEqual(rows[0][1], {"💡 Idea": ["🔀 Directions", "🎓 Theory"]})

    def test_a_written_doc_shows_and_a_missing_one_names_its_file(self):
        doc = self.block / "ui" / "docs" / "block" / "idea" / "theory.md"
        doc.parent.mkdir(parents=True)
        doc.write_text("# Theory\n\nThe theory each direction stands on.\n", encoding="utf-8")
        html = ui_docs.view(self.block, self.root, section)
        self.assertIn("The theory each direction stands on.", html)
        self.assertIn("ui/docs/block/idea/directions.md", html)
        self.assertEqual(ui_docs.slug("🗺️ Data + Paper Plan"), "data-paper-plan")


if __name__ == "__main__":
    unittest.main()
