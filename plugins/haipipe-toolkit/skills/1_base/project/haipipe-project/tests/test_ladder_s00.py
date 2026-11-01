"""`audit --today`: s00 is retired (JL 261029: the Report MindMap shows the Block), and an old index's number is never
reused (JL 261012)."""
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import ladder  # noqa: E402

FACE = "# A Block\nboard-kind: cowork-block\n\n## Questions\n\n```yaml\nquestions: []\n```\n"


def block(root: Path, *dirs: str) -> Path:
    b = root / "b21_law_firm"
    (b / "studio").mkdir(parents=True)
    (b / "board.md").write_text(FACE)
    for d in dirs:
        (b / "studio" / d).mkdir(parents=True)
    return b


def debts(b: Path) -> list[str]:
    return [m for sev, m in ladder.today_findings(b) if "s00" in m or "reuses" in m]


class S00Test(unittest.TestCase):
    def test_a_block_without_s00_is_clean(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(debts(block(Path(tmp), "s01-fees")), [])

    def test_any_s00_or_background_index_is_retired(self):
        with tempfile.TemporaryDirectory() as tmp:
            found = debts(block(Path(tmp), "s00-overview", "s00-background-and-index", "s01-background-index"))
            for name in ("s00-overview", "s00-background-and-index", "s01-background-index"):
                self.assertTrue(any(f"{name}/ is a retired s00" in m for m in found), name)

    def test_the_old_index_number_is_never_reused(self):
        with tempfile.TemporaryDirectory() as tmp:
            b = block(Path(tmp), "s00-overview", "s01-charge-timeline",
                      "s00-overview/history/pre-s00-2026-10-12/topic/s01-background-index")
            self.assertTrue(any("s01-charge-timeline/ reuses s01" in m for m in debts(b)))


if __name__ == "__main__":
    unittest.main()
