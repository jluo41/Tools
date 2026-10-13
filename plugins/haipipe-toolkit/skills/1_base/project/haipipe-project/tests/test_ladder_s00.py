"""`audit --today`: s00 has one name, every Block has it, and an old index's number is never reused (JL 261012)."""
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
    return [m for sev, m in ladder.today_findings(b) if "s00" in m or "reuses" in m or "background index" in m]


class S00Test(unittest.TestCase):
    def test_a_block_with_its_s00_and_fresh_numbers_is_clean(self):
        with tempfile.TemporaryDirectory() as tmp:
            b = block(Path(tmp), "s00-background-and-index", "s02-fees")
            self.assertEqual(debts(b), [])

    def test_a_block_without_s00_owes_one(self):
        with tempfile.TemporaryDirectory() as tmp:
            b = block(Path(tmp), "s02-fees")
            self.assertTrue(any("has no s00-background-and-index" in m for m in debts(b)))

    def test_s00_has_one_name_and_an_old_index_is_renumbered(self):
        with tempfile.TemporaryDirectory() as tmp:
            b = block(Path(tmp), "s00-background-and-index", "s00-structure", "s01-background-index")
            found = debts(b)
            self.assertTrue(any("s00-structure/ is a background index" in m for m in found))
            self.assertTrue(any("s01-background-index/ is a background index" in m for m in found))

    def test_the_old_index_number_is_never_reused(self):
        with tempfile.TemporaryDirectory() as tmp:
            b = block(Path(tmp), "s00-background-and-index", "s01-charge-timeline",
                      "s00-background-and-index/history/pre-s00-2026-10-12/topic/s01-background-index")
            self.assertTrue(any("s01-charge-timeline/ reuses s01" in m for m in debts(b)))


if __name__ == "__main__":
    unittest.main()
