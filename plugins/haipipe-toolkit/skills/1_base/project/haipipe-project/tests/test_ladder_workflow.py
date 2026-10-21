"""`audit --today` at a work Block: the workflow rules of LLMRec b01 and b02 (261021). The face opts in, a Job says what
it hands on and its emoji, a work Task its goal and close, a Run card its role, and no Run keeps a stand-in receipt;
`update --today --apply` writes the missing roles and nothing else."""
import io
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import ladder  # noqa: E402

STAND_IN = "run: r02_fold00\nstatus: blocked\nrepair:\n  why: its ticket wrote no receipt\n  newest_file_at: '2026-09-01'\n"


def block(root: Path, done: bool) -> Path:
    b = root / "work" / "b01_topic"
    task = b / "j01_tables" / "t01_answers"
    (task / "runs" / "r01_fold00" / "result").mkdir(parents=True)
    (root / "pyproject.toml").write_text("")
    (root / "code").mkdir()
    (b / "board.md").write_text("# b01\n" + ("workbench-layout: workflow\n" if done else ""))
    (b / "j01_tables" / "j01_tables.md").write_text(
        "# j01 · Tables\n" + ("emoji: 🧭\n\n## Deliverables\n\n```yaml\ndeliverables: []\n```\n" if done else ""))
    (task / "t01_answers.md").write_text("# Answers\n" + ("goal: one table\nclose: it is stored\n" if done else ""))
    (task / "runs" / "r01_fold00" / "run.yaml").write_text("run: r01_fold00\nkind: hard\n" + ("role: make\n" if done else ""))
    if not done:
        (task / "runs" / "r02_retry_fold00" / "result").mkdir(parents=True)
        (task / "runs" / "r02_retry_fold00" / "run.yaml").write_text("run: r02_retry_fold00\nkind: hard\nstatus: done\n")
        (task / "runs" / "r02_retry_fold00" / "result" / "runtime.yaml").write_text(STAND_IN)
    return b


def workflow(b: Path) -> list[str]:
    return [m for _, m in ladder.today_findings(b) if "studio" not in m and "Questions" not in m and "reports/" not in m]


class WorkflowTest(unittest.TestCase):
    def test_a_block_on_the_workflow_layout_owes_nothing(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(workflow(block(Path(tmp), done=True)), [])

    def test_each_missing_rule_is_one_counted_line(self):
        with tempfile.TemporaryDirectory() as tmp:
            found = workflow(block(Path(tmp), done=False))
            self.assertEqual(len(found), 7, found)
            joined = "\n".join(found)
            for words in ("no workbench-layout: workflow line", "1 Job face(s) have no ## Deliverables: j01_tables",
                          "1 Job face(s) have no emoji: line", "1 Task face(s) have no goal: line: j01/t01_answers",
                          "1 Task face(s) have no close: line", "2 Task Run card(s) have no role: line",
                          "1 Run(s) ran but keep only a stand-in receipt", "t01/r02_retry_fold00"):
                self.assertIn(words, joined)

    def test_update_writes_only_the_missing_roles(self):
        with tempfile.TemporaryDirectory() as tmp:
            b = block(Path(tmp), done=False)
            with redirect_stdout(io.StringIO()):
                ladder.update(b, Path(tmp), apply=True, today=True)
            card = b / "j01_tables/t01_answers/runs/r02_retry_fold00/run.yaml"
            self.assertEqual(card.read_text(), "run: r02_retry_fold00\nkind: hard\nrole: fix\nstatus: done\n")
            self.assertEqual((b / "j01_tables/j01_tables.md").read_text(), "# j01 · Tables\n")   # words wait for an agent
            self.assertFalse(any("role:" in m for m in workflow(b)))

    def test_update_sets_a_cards_kind_from_its_name_and_folder(self):
        with tempfile.TemporaryDirectory() as tmp:
            b = block(Path(tmp), done=True)
            run = b / "j01_tables/t01_answers/runs/r03_figures_by_rank"
            (run / "result").mkdir(parents=True)
            (run / "r03_figures_by_rank.sh").write_text("#!/bin/bash\n")
            (run / "run.yaml").write_text("run: r03_figures_by_rank\nkind: soft\nrole: figures\n")
            with redirect_stdout(io.StringIO()):
                ladder.update(b, Path(tmp), apply=True)
            self.assertEqual((run / "run.yaml").read_text(), "run: r03_figures_by_rank\nkind: hard\nrole: figures\n")

    def test_a_block_of_another_family_keeps_its_own_workbench(self):
        with tempfile.TemporaryDirectory() as tmp:
            b = block(Path(tmp), done=False)
            (b / "board.md").write_text("# b01\nboard-kind: cowork-block\n")
            self.assertEqual(workflow(b), [])


if __name__ == "__main__":
    unittest.main()
