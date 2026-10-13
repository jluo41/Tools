"""/wb update <block> (cli/wb_update.py, b10 s10): today's rules found, a dry run that writes nothing, and an
--apply that moves only data files out of studio/ and leaves a pass with the proposals to tick."""
import contextlib
import io
import sys
import tempfile
import unittest
from pathlib import Path

CLI = Path(__file__).resolve().parents[1] / "cli"
sys.path.insert(0, str(CLI))
import wb_update as U  # noqa: E402


def write(p: Path, text: str) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")


def old_block(space: Path) -> Path:
    """A Block made before studio topics and Questions: two Jobs, one profile Task each, loose studio files."""
    write(space / "env.sh", "")
    b = space / "work" / "b07_demo"
    write(b / "board.md", "board-kind: task-block\n\n# b07\n\n## Rules\n")
    write(b / "studio" / "drops.tsv", "drop\tfiles\n")
    write(b / "studio" / "old.excalidraw", "{}")
    for job, fam, row in (("j01_a", "one", "**A reading every 5 minutes.**"), ("j02_b", "two", "**none**")):
        write(b / job / f"{job}.md", "goal: read the drop\n")
        task = b / job / f"t01_profile_{job[-1]}"
        write(task / f"{task.name}.md", f"family: {fam}\n\n### What is one row?\n\n{row}\n")
    return b


def files(folder: Path) -> set:
    return {p.relative_to(folder).as_posix() for p in folder.rglob("*") if p.is_file()}


class WbUpdateTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.space = Path(self.tmp.name).resolve()
        self.block = old_block(self.space)

    def tearDown(self):
        self.tmp.cleanup()

    def run_update(self, *flags):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = U.main(["work/b07_demo", "--root", str(self.space), "--no-open", *flags])
        return code, out.getvalue()

    def test_today_rules_see_what_the_shape_audit_passes(self):
        found = [m for _, m in U.ladder.today_findings(self.block)]
        self.assertIn("today: studio/ has no sNN-<topic>/ topic", found)
        self.assertIn("today: board.md has no ## Questions register", found)
        self.assertTrue(any("drops.tsv is not a topic: moves to the Block" in m for m in found))
        self.assertTrue(any("old.excalidraw is not a topic: gather it" in m for m in found))
        moves = [(a.name, b.relative_to(self.block).as_posix()) for a, b, _ in U.ladder.today_moves(self.block)]
        self.assertEqual(moves, [("drops.tsv", "drops.tsv")])          # the drawing waits for a topic

    def test_dry_run_writes_nothing(self):
        before = files(self.space)
        code, out = self.run_update()
        self.assertEqual(code, 0)
        self.assertEqual(files(self.space), before)
        self.assertIn("dry run: nothing written", out)
        self.assertIn("s01-profile-tasks", out)
        self.assertIn("Q01 Profile  What is one row?", out)

    def test_apply_moves_data_files_and_leaves_a_pass_to_tick(self):
        code, out = self.run_update("--apply")
        self.assertEqual(code, 0)
        self.assertTrue((self.block / "drops.tsv").is_file())
        self.assertTrue((self.block / "studio" / "old.excalidraw").is_file())
        run = self.block / "runs" / "run-update-b07"
        card = (run / "run.yaml").read_text()
        self.assertIn("status: waiting", card)
        ticks = (run / "passes").glob("p01-*/proposals.md")
        text = next(ticks).read_text()
        self.assertIn("- [ ] s01-profile-tasks", text)
        self.assertIn("- [ ] Q01 · Profile · What is one row?", text)
        self.assertIn("## Group order (studio/_groups.txt", text)          # the bar's order, proposed too
        self.assertNotIn(str(self.space), text)                        # no absolute path in the pass
        self.assertFalse((self.block / "studio" / "s01-profile-tasks").exists())   # nothing made before a tick
        self.assertNotIn("## Questions", (self.block / "board.md").read_text())


class OnePortTest(unittest.TestCase):
    """wb.space_port: one SPACE, one port (JL 261012); a taken port stops, never drifts."""

    def test_a_space_keeps_its_port_or_stops(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            real = U.wb._port_free
            try:
                U.wb._port_free = lambda port: port >= 5610
                self.assertEqual(U.wb.space_port(root), 5610)                  # none set: first free, written down
                self.assertIn("PORT=5610", (root / ".server_config" / "settings.env").read_text())
                self.assertEqual(U.wb.space_port(root), 5610)                  # and kept
                U.wb._port_free = lambda port: False
                with self.assertRaises(SystemExit):                            # taken: stop, never drift
                    U.wb.space_port(root)
            finally:
                U.wb._port_free = real


if __name__ == "__main__":
    unittest.main()
