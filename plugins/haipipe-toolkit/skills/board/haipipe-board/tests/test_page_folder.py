"""The folded-page boundary (JL 260815): every subfolder of a page folder is a
plugin, and discovery never enters one.

The rule this file pins down: `PAGENAME.match("SKILL.md")` is true, so without
the boundary a `skill/` plugin holding a unit snapshot surfaces as a ghost
page. Child pages must keep nesting, because a lifecycle tree is pages inside
pages.
"""
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from src.common import page_files, q_files  # noqa: E402


def touch(root, rel):
    p = root / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text("# x\n", encoding="utf-8")
    return p


class PageFolderBoundary(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.d = Path(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()

    def names(self):
        return sorted(p.name for p in page_files(self.d))

    def test_flat_and_folded_pages_are_both_found(self):
        touch(self.d, "QA-design/QA1-concepts.md")
        touch(self.d, "QB-delivery/QB4-overall/QB4-overall.md")
        self.assertEqual(self.names(), ["QA1-concepts.md", "QB4-overall.md"])

    def test_plugin_content_is_never_a_page(self):
        touch(self.d, "QC/Skill-3-haipipe-page/Skill-3-haipipe-page.md")
        # the hazard this rule exists for: a snapshot whose name matches PAGENAME
        touch(self.d, "QC/Skill-3-haipipe-page/skill/haipipe-page/SKILL.md")
        # ordinary plugin material that happens to look page-shaped
        touch(self.d, "QC/Skill-3-haipipe-page/slide/source/QA4-deck.md")
        self.assertEqual(self.names(), ["Skill-3-haipipe-page.md"])

    def test_child_pages_keep_nesting(self):
        touch(self.d, "1-work/S-Paper-1a/S-Paper-1a.md")
        touch(self.d, "1-work/S-Paper-1a/S-Paper-1b/S-Paper-1b.md")
        touch(self.d, "1-work/S-Paper-1a/draw/S-Paper-1x.md")  # plugin, not a child
        self.assertEqual(self.names(), ["S-Paper-1a.md", "S-Paper-1b.md"])

    def test_stray_file_beside_the_pages_own_md_is_not_a_page(self):
        touch(self.d, "QB/QB4-overall/QB4-overall.md")
        touch(self.d, "QB/QB4-overall/QB4-notes.md")
        self.assertEqual(self.names(), ["QB4-overall.md"])

    def test_q_files_shares_the_boundary(self):
        touch(self.d, "QB/QB4-overall/QB4-overall.md")
        touch(self.d, "QB/QB4-overall/slide/Q-stray.md")
        self.assertEqual([p.name for p in q_files(self.d)], ["QB4-overall.md"])


if __name__ == "__main__":
    unittest.main()
