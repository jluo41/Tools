"""`audit --today`: s00 has one name, every Block has it, and an old index's number is never reused (JL 261012)."""
import contextlib
import io
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
            b = block(Path(tmp), "s00-overview", "s02-fees")
            self.assertEqual(debts(b), [])

    def test_a_block_without_s00_owes_one(self):
        with tempfile.TemporaryDirectory() as tmp:
            b = block(Path(tmp), "s02-fees")
            self.assertTrue(any("has no s00-overview" in m for m in debts(b)))

    def test_s00_has_one_name_and_an_old_index_is_renumbered(self):
        with tempfile.TemporaryDirectory() as tmp:
            b = block(Path(tmp), "s00-overview", "s00-structure", "s01-background-index")
            found = debts(b)
            self.assertTrue(any("s00-structure/ is a background index" in m for m in found))
            self.assertTrue(any("s01-background-index/ is a background index" in m for m in found))

    def test_the_old_index_number_is_never_reused(self):
        with tempfile.TemporaryDirectory() as tmp:
            b = block(Path(tmp), "s00-overview", "s01-charge-timeline",
                      "s00-overview/history/pre-s00-2026-10-12/topic/s01-background-index")
            self.assertTrue(any("s01-charge-timeline/ reuses s01" in m for m in debts(b)))


    def test_the_old_name_is_flagged_and_renamed_whole(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            b = block(root, "s00-background-and-index", "s02-fees")
            old = b / "studio" / "s00-background-and-index"
            (old / "s00-background-and-index.md").write_text("see s00-background-and-index.excalidraw\n")
            (old / "build_s00_background_and_index.py").write_text("print(1)\n")
            (b / "studio" / "s02-fees" / "s02-fees.md").write_text("[index](../s00-background-and-index/s00-background-and-index.md)\n")
            self.assertTrue(any("is s00's old name" in m for m in debts(b)))
            renames = ladder.s00_renames(b)
            self.assertEqual([(o.name, n.name) for o, n in renames], [("s00-background-and-index", "s00-overview")])
            with contextlib.redirect_stdout(io.StringIO()):
                ladder.rename_s00(*renames[0], b, root, apply=True)
            new = b / "studio" / "s00-overview"
            self.assertEqual(sorted(p.name for p in new.iterdir()), ["build_s00_overview.py", "s00-overview.md"])
            self.assertEqual((new / "s00-overview.md").read_text(), "see s00-overview.excalidraw\n")
            self.assertIn("../s00-overview/s00-overview.md", (b / "studio" / "s02-fees" / "s02-fees.md").read_text())
            self.assertEqual(debts(b), [])


if __name__ == "__main__":
    unittest.main()
