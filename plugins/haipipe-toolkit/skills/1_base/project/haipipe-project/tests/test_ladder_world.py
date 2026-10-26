"""A world's studio/ is not a Block; a Block's studio/ keeps its mind map loose; files are UTF-8 with LF and a Run
card's paths use forward slashes (a Windows laptop, 261024)."""
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import ladder  # noqa: E402

FACE = "# b01 · Demo\nboard-kind: task-block\n\n## Questions\n\n```yaml\nquestions: []\n```\n"


def world(root: Path) -> Path:
    w = root / "Project" / "work"
    (w / "b01_demo" / "studio" / "s01-flow").mkdir(parents=True)
    (w / "b01_demo" / "board.md").write_text(FACE, encoding="utf-8")
    (w / "studio").mkdir()
    (w / "studio" / "mind-map.mindmap.md").write_text("# work\n", encoding="utf-8")
    return w


class WorldTest(unittest.TestCase):
    def test_a_worlds_studio_is_not_called_a_block(self):
        with tempfile.TemporaryDirectory() as tmp:
            w = world(Path(tmp))
            nodes = ladder.audit_path(w, Path(tmp))
            self.assertEqual([n.path.name for n in nodes], ["b01_demo"])
            msgs = [m for n in ladder.walk(nodes) for _s, m in n.findings]
            self.assertFalse(any("not a Block" in m for m in msgs), msgs)

    def test_a_blocks_mind_map_is_kept_loose_and_never_moved(self):
        with tempfile.TemporaryDirectory() as tmp:
            b = world(Path(tmp)) / "b01_demo"
            for name in ("mind-map.mindmap.md", "mind-map.excalidraw", "mind-map.png", "mind-map.mindmap.html"):
                (b / "studio" / name).write_text("x", encoding="utf-8")
            (b / "studio" / "stray.tsv").write_text("a\tb\n", encoding="utf-8")
            msgs = [m for _s, m in ladder.today_findings(b)]
            self.assertFalse(any("mind-map" in m for m in msgs), msgs)
            self.assertTrue(any("stray.tsv" in m for m in msgs))
            self.assertEqual([src.name for src, _dst, _why in ladder.today_moves(b)], ["stray.tsv"])

    def test_files_are_written_utf8_with_lf(self):
        with tempfile.TemporaryDirectory() as tmp:
            f = Path(tmp) / "board.md"
            ladder.write_utf8(f, "# b01 · Demo 去\n\nj01\n")
            raw = f.read_bytes()
            self.assertNotIn(b"\r\n", raw)
            self.assertEqual(raw.decode("utf-8"), "# b01 · Demo 去\n\nj01\n")

    def test_a_run_cards_scope_uses_forward_slashes(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            run = root / "work" / "b01_demo" / "j01_job" / "t01_task" / "runs" / "r01_fit"
            run.mkdir(parents=True)
            card = ladder.make_card(run, "r01_fit", "hard", "r01_fit.sh", root, moved_from=["a/b"])
            self.assertEqual(card["scope"], "work/b01_demo/j01_job/t01_task")
            self.assertNotIn("\\", card["scope"])


if __name__ == "__main__":
    unittest.main()
