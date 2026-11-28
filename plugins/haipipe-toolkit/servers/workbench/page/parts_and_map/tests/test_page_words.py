"""Page words on rendered pages (hai-ui CONSTITUTION.md A01-A03): the scanner's rules, and the shared SPACE Home
rendered on a small SPACE shows none of the banned words."""
import importlib.util
import tempfile
import unittest
from pathlib import Path

from host_paths import bootstrap
bootstrap()
from live.space_home import space_home  # noqa: E402

SCAN = Path(__file__).resolve().parents[5] / "skills/1_base/workbench/hai-ui/scripts/page_words.py"
spec = importlib.util.spec_from_file_location("page_words", SCAN)
PW = importlib.util.module_from_spec(spec)
spec.loader.exec_module(PW)


class PageWordsTest(unittest.TestCase):
    def test_the_scanner_finds_each_banned_kind_in_visible_text_only(self):
        page = ('<style>.x{content:"JL 261113"}</style><script>var s="Status: done"</script><!-- 3 of 7 written -->'
                '<p>Status: running</p><p>3 of 7 written</p><p>6 to fix</p><span title="JL 261020">x</span>'
                '<p>Nothing handed over yet.</p><p>Nothing asked yet</p>')
        kinds = sorted({(a, n) for a, n, _ in PW.hits(PW.visible(page))})
        self.assertEqual(kinds, [("A01", "state words"), ("A01", "tally"), ("A02", "provenance tag"),
                                 ("A03", "empty state")])
        self.assertEqual(PW.hits(PW.visible("<style>JL 261113</style><p>Runs</p>")), [])

    def test_space_home_on_a_small_space_shows_no_banned_words(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            proj = root / "Project-X"
            proj.mkdir()
            (proj / "project.md").write_text("# Project X\n\nOne line.\n")
            self.assertEqual(PW.hits(PW.visible(space_home(root, root))), [])


if __name__ == "__main__":
    unittest.main()
