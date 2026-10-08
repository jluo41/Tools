"""The paper ladder's scaffold (haipipe-paper/scripts/paper_ladder.py, b16 Q05): each level is made, the next
version copies only written files, a comments batch becomes a report, and rollback restores the Board exactly."""
from __future__ import annotations

import contextlib
import importlib.util
import io
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).parents[1]


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


L = load("paper_ladder", ROOT / "haipipe-paper" / "scripts" / "paper_ladder.py")
R = load("review_items", ROOT / "haipipe-paper-comments" / "scripts" / "review_items.py")


def quiet(fn, *args):
    with contextlib.redirect_stdout(io.StringIO()):
        return fn(*args)


def snapshot(folder: Path) -> dict:
    return {p.relative_to(folder).as_posix(): p.read_bytes() for p in folder.rglob("*")
            if p.is_file() and not p.name.startswith(".paper-version")
            and not any(x.startswith(".paper-version") for x in p.relative_to(folder).parts)}


class PaperLadderTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.board = Path(self.tmp.name) / "Paper-Demo"
        quiet(L.main, ["board", str(self.board), "--title", "Demo paper"])

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def test_board_is_its_face_only(self) -> None:
        face = (self.board / "board.md").read_text()
        for field in ("board-kind: paper-board", "dialect: paper", "spine:", "close:", "## Questions"):
            self.assertIn(field, face)
        self.assertEqual([p.name for p in self.board.iterdir()], ["board.md"])   # no folder ahead of its content

    def test_version_task_and_run(self) -> None:
        quiet(L.main, ["version", str(self.board), "--desk", "desk", "--date", "0101"])
        v = self.board / "j01_v0101_desk"
        self.assertEqual([p.name for p in v.iterdir()], ["j01_v0101_desk.md"])
        face = (v / "j01_v0101_desk.md").read_text()
        for field in ("goal:", "close:", "## Tasks"):
            self.assertIn(field, face)
        self.assertIn("## Narrative", face)
        self.assertIn("haipipe:compile-order:start", face)
        for stem in ("t00_abstract", "t01_introduction", "t21_methods-detail", "t31_cover-letter"):
            quiet(L.main, ["task", str(v), stem])
            sec = (v / stem / f"{stem}.md").read_text()
            self.assertIn("page-type: section", sec)
            self.assertIn(f"story-row: j01_v0101_desk ## Narrative / {stem}", sec)
            self.assertIn("task-kind: page", sec)
        self.assertIn("section_kind: letter", (v / "t31_cover-letter" / "t31_cover-letter.md").read_text())
        tasks = (v / "j01_v0101_desk.md").read_text().split("## Tasks", 1)[1].split("## ", 1)[0]
        self.assertIn("1. t00_abstract · Abstract", tasks)
        self.assertIn("4. t31_cover-letter · Cover-letter".replace("Cover-letter", "Cover letter"), tasks)
        pages = (self.board / "board.md").read_text()
        self.assertIn("### J01 · j01_v0101_desk", pages)
        self.assertIn("t21_methods-detail.md", pages)
        quiet(L.main, ["run", str(self.board), "add", "j02"])           # Open a version makes the base run-add-<jNN>
        run = self.board / "runs" / "run-add-j02"                      # the shared writer's folder (haipipe-run)
        self.assertTrue((run / "run-add-j02.md").is_file())
        card = (run / "run.yaml").read_text()
        self.assertIn("kind: soft", card)
        self.assertIn("skill: haipipe-paper\n", card)                # from the Open a version run card
        self.assertIn("agent: haipipe-page-writing-agent", card)
        quiet(L.main, ["run", str(v), "release-section", "t01"])        # a card that a person signs
        self.assertIn("release of one Section (G3)", (v / "runs" / "run-release-section-t01" / "run.yaml").read_text())
        with self.assertRaises(SystemExit):              # the same Run twice: a new round is a pass
            quiet(L.main, ["run", str(self.board), "add", "j02"])
        with self.assertRaises(SystemExit):              # a Section's Runs are the Page workflow's
            quiet(L.main, ["run", str(v / "t01_introduction"), "revise", "x"])
        with self.assertRaises(SystemExit):              # a Task is tNN_<lowercase-kebab>
            quiet(L.main, ["task", str(v), "S-Desk-Main-1-Intro"])

    def test_next_comments_and_rollback(self) -> None:
        quiet(L.main, ["version", str(self.board), "--desk", "desk", "--date", "0101"])
        v = self.board / "j01_v0101_desk"
        quiet(L.main, ["task", str(v), "t01_introduction"])
        (v / "t01_introduction" / "draft").mkdir()
        (v / "t01_introduction" / "draft" / "t01_introduction-draft-v0.1.md").write_text("words\n")
        (v / "t01_introduction" / "runs").mkdir()
        (v / "t01_introduction" / "runs" / "run-structure-plan.md").write_text("a receipt\n")
        batch = v / "RD01-editor-0916"
        batch.mkdir()
        (batch / "RD01-editor-0916.md").write_text("# RD01-editor-0916 · Editor decision\n\n## Opening\n\n"
                                                   "The editor asks for a major revision.\n")
        before = snapshot(self.board)
        quiet(L.main, ["next", str(self.board), "--from", "j01_v0101_desk", "--date", "0202"])
        n = self.board / "j02_v0202_desk"
        self.assertTrue((n / "t01_introduction" / "draft" / "t01_introduction-draft-v0.1.md").is_file())
        self.assertFalse((n / "t01_introduction" / "runs").exists())   # receipts are not copied
        self.assertIn("from: j01_v0101_desk", (n / "j02_v0202_desk.md").read_text())
        quiet(R.main, [str(self.board), "add", "j01_v0101_desk/RD01-editor-0916", "--to", "j02_v0202_desk"])
        rep = n / "reports" / "q01_editor-0916" / "q01_editor-0916.md"
        self.assertTrue(rep.is_file())
        self.assertIn("page-type: comments", rep.read_text())
        self.assertIn("group: comments", (n / "j02_v0202_desk.md").read_text())
        self.assertIn("responds-to: reports/q01_editor-0916/q01_editor-0916.md", (n / "j02_v0202_desk.md").read_text())
        self.assertNotIn("\nanswers:", (n / "j02_v0202_desk.md").read_text())      # answers: is for Question ids
        self.assertIn("answers: Q01", rep.read_text())                               # the report names its Question
        self.assertIn("answer-status: open", rep.read_text())
        quiet(R.main, [str(self.board), "rollback"])     # the add, then the next: the Board as it was
        quiet(L.main, ["rollback", str(self.board)])
        self.assertEqual(snapshot(self.board), before)

    def test_route_and_reply_a_review_item(self) -> None:
        quiet(L.main, ["version", str(self.board), "--desk", "desk", "--date", "0101"])
        rep = self.board / "j01_v0101_desk" / "reports" / "q01_editor-0916"
        rep.mkdir(parents=True)
        face = rep / "q01_editor-0916.md"
        face.write_text("# q01_editor-0916 · Editor decision\n\npage-type: comments\n\n## Review Items\n\n"
                        "| item | cites | lands on | work | reply | state |\n|---|---|---|---|---|---|\n"
                        "| Review-causal-claim | R1.1 · E1.2 |  |  |  | open |\n| Review-sample | R2.1 |  |  |  | open |\n")
        before = snapshot(self.board)
        quiet(R.main, [str(self.board), "route", "j01_v0101_desk/reports/q01_editor-0916", "Review-causal-claim",
                       "--to", "t04_results ¶2 · C2"])
        text = face.read_text()
        self.assertIn("| Review-causal-claim | R1.1 · E1.2 | t04_results ¶2 · C2 | run-revise-causal-claim |  | routed |",
                      text)
        self.assertIn("| Review-sample | R2.1 |  |  |  | open |", text)          # the other row is untouched
        quiet(R.main, [str(self.board), "reply", "j01_v0101_desk/reports/q01_editor-0916", "Review-causal-claim",
                       "--reply", "P3"])
        self.assertIn("| run-revise-causal-claim | P3 | answered |", face.read_text())
        with self.assertRaises(SystemExit):              # an item that is not there
            quiet(R.main, [str(self.board), "reply", "j01_v0101_desk/reports/q01_editor-0916", "Review-x",
                           "--reply", "P1"])
        quiet(R.main, [str(self.board), "rollback"])
        quiet(R.main, [str(self.board), "rollback"])
        self.assertEqual(snapshot(self.board), before)


if __name__ == "__main__":
    unittest.main()
