"""studio_move.py rewrites a link only when its path leads to a topic that moves, and never inside a Result, a pass
or an archive (Ladder-b17's review, 261031: the old name-based rewrite broke held topics and other Blocks' links)."""
import importlib.util
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("studio_move", HERE.parent / "scripts" / "studio_move.py")
SM = importlib.util.module_from_spec(spec)
spec.loader.exec_module(SM)


def put(p: Path, text: str) -> Path:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")
    return p


class StudioMove(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        root = Path(self.tmp.name) / "work"
        self.a, self.b = root / "b01_a", root / "b02_b"
        put(self.a / "studio" / "s01-alpha" / "s01-alpha.md", "# s01\n")
        put(self.a / "studio" / "s02-beta" / "s02-beta.md", "# held, an s02-beta sits beside the Jobs already\n")
        put(self.a / "s02-beta" / "s02-beta.md", "# the other s02-beta\n")
        put(self.b / "studio" / "s03-gamma" / "s03-gamma.md", "# another Block's topic, not moving\n")
        self.face = put(self.a / "board.md", "\n".join([
            "[alpha](studio/s01-alpha/s01-alpha.md)",
            "[beta](studio/s02-beta/s02-beta.md)",
            "[gamma](../b02_b/studio/s03-gamma/s03-gamma.md)",
            "a template: `studio/sNN-<topic>/`",
        ]) + "\n")
        self.kept = [put(self.a / "j01_x" / "t01_y" / "runs" / "r01_z" / "result" / "RUN-REPORT.md",
                         "see studio/s01-alpha\n"),
                     put(self.a / "runs" / "run-draw-s01" / "passes" / "p01-1001" / "pass.md", "drew studio/s01-alpha\n"),
                     put(self.a / "_old" / "HISTORY.md", "was in studio/s01-alpha\n")]

    def tearDown(self):
        self.tmp.cleanup()

    def test_only_links_to_a_moving_topic_change_and_results_stay(self):
        before = [k.read_text() for k in self.kept]
        self.assertEqual(SM.main([str(self.a), "--apply"]), 0)
        face = self.face.read_text()
        self.assertIn("[alpha](s01-alpha/s01-alpha.md)", face)                      # moved: the link follows
        self.assertIn("[beta](studio/s02-beta/s02-beta.md)", face)                  # held: still its own s02-beta
        self.assertIn("[gamma](../b02_b/studio/s03-gamma/s03-gamma.md)", face)      # another Block: not moving
        self.assertIn("`studio/sNN-<topic>/`", face)                                # a template stays
        self.assertTrue((self.a / "s01-alpha" / "s01-alpha.md").is_file())
        self.assertTrue((self.a / "studio" / "s02-beta").is_dir())
        self.assertEqual([k.read_text() for k in self.kept], before)               # Result, pass, archive untouched

    def test_a_link_written_from_the_space_root_is_read_from_there(self):
        page = put(self.a / "j01_x" / "j01_x.md", "[alpha](work/b01_a/studio/s01-alpha/s01-alpha.md)\n")
        SM.main([str(self.a), "--apply"])
        self.assertIn("(work/b01_a/s01-alpha/s01-alpha.md)", page.read_text())


if __name__ == "__main__":
    unittest.main()
