"""The insight theme on the base frame (insight_theme.py): a register board's Block tab in six Spaces,
drawn with base classes only, read-only. Placeholders only; the fixture mirrors the register board's
shapes (an MT00 meta page, MT01/MT04 register grids, a D page and a signed W page)."""
from __future__ import annotations

import json
import re
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "_host"))
from host_paths import bootstrap  # noqa: E402
bootstrap()

from live import frame  # noqa: E402
from live.insight_theme import THEME, spaces  # noqa: E402

OLD_CLASSES = ("hl-row", "class=lead", "class=pill", "class=pane", "class=shell", "gateset", "<style")


def page(folder: Path, stem: str, body: str) -> None:
    folder.mkdir(parents=True, exist_ok=True)
    (folder / f"{stem}.md").write_text(body, encoding="utf-8")


def board(root: Path) -> Path:
    b = root / "Project-Demo" / "insights" / "Demo-InsightBoard"
    page(b / "0-MT-meta" / "MT00-meta", "MT00-meta",
         "# Meta\n\nstate: ✅ SETTLED\npage-type: meta\nowner: X\n\n## Content\n"
         "extract  demo_input.parquet\n"
         "full          where: []  declared unfiltered      full.yaml   1-full/\n"
         "                     1,000 of 1,000 rows · 100.0000%\n"
         "young         age lt 40                          young.yaml  2-young/\n"
         "                       400 of 1,000 rows ·  40.0000%\n")
    page(b / "0-MT-meta" / "MT01-question-data", "MT01-question-data",
         "# Data questions\n\nstate: ✅ SETTLED · 1 question\npage-type: question\nquestion-level: data\nowner: X\n\n"
         "## Content\n\n```text\nid   question                 Gen-1   full   young\n"
         "QD1  what does the extract   Data/1  ✅ D01-full  🚫 full-only\n     hold?\n```\n")
    page(b / "0-MT-meta" / "MT04-question-wisdom", "MT04-question-wisdom",
         "# Wisdom questions\n\nstate: ✅ SETTLED\npage-type: question\nquestion-level: wisdom\nowner: X\n\n"
         "## Content\n\n```text\nid    question           Gen-1     partition   QW1\n"
         "QW1   what to send?      Wisdom/1  full    ✅ W01-full\n"
         "                                   young   🚫 full-only\n```\n")
    page(b / "1-full" / "D01-full-extract-shape", "D01-full-extract-shape",
         "# Extract shape\n\nstate: ✅ SETTLED · answers QD1\npage-type: data\nowner: X\n\n## Opening\n\n"
         "What is in the extract?\n\n## Log\n\n260901 · Created.\n")
    page(b / "1-full" / "W01-full-what-to-send", "W01-full-what-to-send",
         "# Send the one arm\n\nstate: ✅ SETTLED · answers QW1\npage-type: wisdom\nowner: X\n\n## Opening\n\nSend `a`.\n\n"
         "## Content\n\n```text\nSERVES        QW1 · brief\n\nsigned: ✅ X 260902\n```\n\n## Log\n\n260902 · Signed.\n")
    (b / "2-young").mkdir()
    (b / "j01_demo" / "t01_demo").mkdir(parents=True)          # a Job and a Task: the base's own
    (b / "board.md").write_text("# Demo Insight Board\n\nboard-kind: insight-board\n\n## Topic\n\nOne extract.\n",
                                encoding="utf-8")
    return b


class InsightThemeTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.board = board(self.root)

    def tearDown(self):
        self.tmp.cleanup()

    def json(self, folder, sub=""):
        data = json.loads(frame.frame_json(THEME, self.root, folder, sub))
        return {s["name"]: s for s in data["spaces"]}

    def test_the_frame_picks_the_insight_theme_for_a_board_in_insights(self):
        self.assertEqual(frame.theme_of(self.board, self.root), "insight")
        self.assertIn("insight", frame.themes())

    def test_the_block_spaces_carry_the_old_pages_content(self):
        s = self.json(self.board)
        # b11 s11: the Map first (one row on today's layout: one set of questions, not yet versioned)
        self.assertEqual(s["Description"]["subspaces"], ["Map", "Prototype", "Dataset", "Partitions"])
        self.assertEqual(s["Audience Report"]["subspaces"][:2], ["Full", "Young"])
        self.assertEqual(s["Audience Report"]["run_doing"], ["Report", "Pool or split"])
        self.assertIn("Mechanical check", s["Runs"]["run_doing"])
        self.assertEqual(s["Delivery"]["run_types"], ["run-draft-handoff"])
        self.assertIn("Ask", s["Description"]["run_doing"])

    def test_the_audience_report_is_question_work_report_per_partition(self):
        page = frame.render(THEME, self.root, self.board, "Audience Report", "Full")
        self.assertIn('id="question-QD1"', page)
        self.assertIn('id="question-QW1"', page)
        self.assertIn("Extract shape", page)                    # the answering page, as the Report
        young = frame.render(THEME, self.root, self.board, "Audience Report", "Young")
        self.assertIn("Answered on Full", young)               # a question refused on this cut says why

    def test_every_view_draws_with_base_classes_only(self):
        for sub in ("Prototype", "Dataset", "Partitions", "Full", "Young", ""):
            for name, space in spaces("Block", self.board, self.root, sub).items():
                with self.subTest(space=name, sub=sub):
                    for old in OLD_CLASSES:
                        self.assertNotIn(old, space.html)
        self.assertIn("young", spaces("Block", self.board, self.root, "Partitions")["Description"].html)
        self.assertIn("Send the one arm", spaces("Block", self.board, self.root, "")["Work Details"].html)

    def test_a_job_and_a_task_are_the_bases_own(self):
        job, task = self.board / "j01_demo", self.board / "j01_demo" / "t01_demo"
        self.assertEqual(spaces("Job", job, self.root, ""), {})
        self.assertEqual(spaces("Task", task, self.root, ""), {})
        for folder in (job, task):
            with self.subTest(folder=folder.name):
                page = frame.render(THEME, self.root, folder)
                self.assertIn("Description", page)
                self.assertNotIn("Traceback", page)


class CarriedBoardTest(unittest.TestCase):
    """A register board carried over to plan C (carry_today.py): one Job, a Task per question, pointers
    only; every level then draws as b11 s11 · s12 · s13 design it, read live from today's folders."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        (self.root / "env.sh").write_text("", encoding="utf-8")
        self.board = board(self.root)
        sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
        import carry_today
        before = sorted(p for p in self.board.rglob("*") if p.is_file())
        self.written = carry_today.main([str(self.board)])
        self.after = sorted(p for p in self.board.rglob("*") if p.is_file())
        self.new = [p for p in self.after if p not in before]
        self.job = next(p for p in self.board.iterdir() if p.name.startswith("j01_p1_"))

    def tearDown(self):
        self.tmp.cleanup()

    def test_it_writes_pointers_only(self):
        self.assertEqual(self.written, 0)
        self.assertTrue(self.new)
        for f in self.new:
            self.assertEqual(f.suffix, ".md")
            self.assertIn("carried: today", f.read_text(encoding="utf-8"))
        self.assertEqual(sorted(t.name for t in self.job.iterdir() if t.is_dir()),
                         ["t01_D01_what-does-the-extract-hold", "t02_W01_what-to-send"])

    def test_each_level_draws_as_designed(self):
        board_s = spaces("Block", self.board, self.root, "")
        self.assertEqual(board_s["Description"].subspaces, ("Map", "Prototype", "Dataset", "Partitions"))
        self.assertIn(self.job.name, board_s["Description"].html)              # the Map's one cell
        job_s = spaces("Job", self.job, self.root, "")
        self.assertEqual(job_s["Description"].subspaces, ("Prototype", "Dataset"))
        self.assertIn("Propose questions", [k["doing"] for k in job_s["Runs"].run_types])
        task = self.job / "t01_D01_what-does-the-extract-hold"
        task_s = spaces("Task", task, self.root, "Table")
        self.assertEqual(task_s["Audience Report"].subspaces, ("Table", "Reading"))
        self.assertIn("Extract shape", task_s["Audience Report"].html)          # the answering page, per cut
        self.assertIn("refused", task_s["Audience Report"].html)                # 🚫 on young
        for level, folder in (("Block", self.board), ("Job", self.job), ("Task", task)):
            page = frame.render(THEME, self.root, folder)
            self.assertNotIn("Traceback", page, level)

    def test_the_answers_stay_where_they_are(self):
        moved = [p for p in self.after if p not in self.new and not p.exists()]
        self.assertEqual(moved, [])


if __name__ == "__main__":
    unittest.main()
