"""An Idea Block in paper/ (Paper-Idea 261124: Idea-CGM-Pred drew as a 📄 Paper Board with Support blocks and Writing):
its type, its one Ideas view of the Idea Jobs, an Idea Job's face as its view, and no Job in it read as a version.
Placeholders only, in a temp folder."""
from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "_host"))
from host_paths import bootstrap  # noqa: E402
bootstrap()

from live import board_read, focus_identity, focus_themes, idea_block  # noqa: E402


def write(p: Path, text: str) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")


class IdeaBlock(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        paper = self.root / "Proj-X" / "paper"
        write(self.root / "Proj-X" / "project.yaml", "name: x\n")
        self.block = paper / "Idea-X"
        write(self.block / "board.md", "# Idea-X\n\nboard-kind: ideation-block\n")
        write(paper / "Paper-A" / "board.md", "# Paper-A\n")
        write(self.block / "j01_a" / "j01_a.md", "# j01_a\n\nstate: selected\nwent to: ../../Paper-A/ ((Venue, j11_v))\n\n"
              "## Question\n\nCan A be read off B?\n\n## Claim\n\nIt can.\n")
        write(self.block / "j02_b" / "j02_b.md", "# j02_b\n\nstate: eliminated\n\n## Question\n\nCan C?\n")
        write(self.block / "j03_c" / "j03_c.md", "# j03_c\n\nstate: open\n")
        write(self.block / "j03_c" / "ideation.yaml", "question: Can D?\n")

    def tearDown(self):
        self.tmp.cleanup()

    def test_rows_carry_question_mark_and_where_it_went(self):
        rows = idea_block.idea_jobs(self.block)
        self.assertEqual([r["question"] for r in rows], ["Can A be read off B?", "Can C?", "Can D?"])
        self.assertEqual(rows[0]["went"].name, "Paper-A")
        self.assertEqual(rows[0]["where"], "Venue, j11_v")
        html = idea_block.ideas_html(self.block, self.root)
        self.assertIn("✅", html)
        self.assertIn("idea-out", html)                  # an eliminated idea is faded, no state word
        self.assertNotIn("selected", html.replace("idea-", ""))

    def test_the_block_is_an_idea_block_not_a_paper_board(self):
        self.assertEqual(focus_identity.page_type("paper", "Block", self.block, self.root, {}), "💡 Idea Block")
        self.assertEqual(focus_identity.page_type("paper", "Job", self.block / "j01_a", self.root, {}), "💡 Idea Job")
        self.assertEqual(list(focus_themes.paper_board_report(self.block, self.root)), ["ideas"])
        self.assertFalse(board_read.is_version(self.block / "j01_a"))
        self.assertTrue(board_read.is_version(self.root / "Proj-X" / "paper" / "Paper-A" / "j11_writing_v1124_x"))

    def test_an_idea_job_shows_its_face(self):
        views = focus_themes.paper_job_views(self.block / "j01_a", self.root, "report")
        self.assertEqual(list(views), ["idea"])
        body = views["idea"][1]()
        self.assertIn("Can A be read off B?", body)
        self.assertNotIn("went to", body)

    def test_an_assessment_task_shows_its_face_and_its_verdicts(self):
        from live import paper_tasks
        task = self.block / "j03_c" / "t01_prior_work"
        write(task / "t01_prior_work.md", "# What does the closest work establish?\n\ntask-type: ideation\n\n"
              "## Where it stands\n\nNothing stronger than inconclusive. Receipt: "
              "[`../workflow/novelty/i03.yaml`](../workflow/novelty/i03.yaml).\n")
        write(self.block / "j03_c" / "workflow" / "novelty" / "i03.yaml",
              "kind: idea-novelty-check\nclaims:\n- claim_id: c01\n  verdict: inconclusive\n  confidence: low\n")
        self.assertEqual(focus_identity.page_type("paper", "Task", task, self.root, {}), "💡 Assessment Task")
        views = paper_tasks.views(task, self.root, "report", {"mindmap": ("MindMap", None)})
        self.assertEqual(list(views), ["assessment"])
        body = views["assessment"][1]()
        self.assertIn("Nothing stronger than inconclusive", body)
        self.assertIn("<td>c01</td><td>inconclusive</td><td>low</td>", body)
        self.assertIn("<a href=", body.split("Receipt:")[1][:20])       # a code span as link text stays a link


if __name__ == "__main__":
    unittest.main()
