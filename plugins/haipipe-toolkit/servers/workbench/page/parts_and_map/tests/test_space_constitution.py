"""SPACE Home › 📜 Constitution (page/parts_and_map/space_constitution.py): rows, marks, links, and Home never failing on it."""
import tempfile
import unittest
from pathlib import Path

from host_paths import bootstrap
bootstrap()
from live.space_constitution import constitution_html  # noqa: E402

ART = ('## A01 · Rule one\n\n> "words one" (JL 261118)\n\n**Status:** solved 261118\n**Report:** constitution/A01-one.md\n\n'
       '## A02 · Rule two\n\n> "words two" (JL 261118)\n\n**Status:** solved 261118\n')


class ConstitutionTest(unittest.TestCase):
    def test_rows_marks_and_links_also_through_a_tools_link(self):
        with tempfile.TemporaryDirectory() as tmp:
            tools, space = Path(tmp) / "Tools-SPACE", Path(tmp) / "X-SPACE"
            skill = tools / "plugins" / "kit" / "skills" / "0_utils" / "demo"
            (skill / "constitution").mkdir(parents=True)
            (skill / "CONSTITUTION.md").write_text(ART)
            (skill / "constitution" / "A01-one.md").write_text("# A01\n")
            space.mkdir()
            (space / "Tools").symlink_to(tools)
            for root, prefix in ((tools, "%2Fplugins"), (space, "%2FTools%2Fplugins")):
                h = constitution_html(root)
                self.assertIn("✅</span><a href=\"/_board/page?path=" + prefix, h)
                self.assertIn("A01-one.md", h)
                self.assertIn("🔶</span>", h)                    # A02 says solved but has no report
                self.assertIn("“words two”", h)
            self.assertEqual(constitution_html(Path(tmp) / "empty"), "")

    def test_a_broken_file_never_fails_home(self):
        with tempfile.TemporaryDirectory() as tmp:
            skill = Path(tmp) / "plugins" / "kit" / "skills" / "demo"
            skill.mkdir(parents=True)
            (skill / "CONSTITUTION.md").write_bytes(b"\xff\xfe## A01 \x00")
            self.assertEqual(constitution_html(Path(tmp)), "")


if __name__ == "__main__":
    unittest.main()
