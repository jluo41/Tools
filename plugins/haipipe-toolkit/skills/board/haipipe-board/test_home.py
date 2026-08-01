#!/usr/bin/env python3
"""Read-only discovery and rendering checks for the SPACE Board Home."""
import tempfile
import unittest
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from live.home import HomeMixin, discover_boards, render_home


class SpaceHomeTest(unittest.TestCase):
    def test_public_route_is_boards_not_the_private_api_namespace(self):
        request = HomeMixin()
        request.path = "/boards/"
        self.assertTrue(request.is_home_request())
        request.path = "/_board/home"
        self.assertFalse(request.is_home_request())

    def test_discovers_real_boards_and_ignores_generated_or_archived_ones(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            board = root / "project" / "diagram" / "01-topic"
            (board / "QA-design").mkdir(parents=True)
            (board / "board").mkdir()
            (board / "board.md").write_text("# A <Board>\nspine: Find & settle it\n")
            (board / "QA-design" / "QA1-question.md").write_text("# Q\nstate: ✅ SETTLED\n")
            (board / "board" / "index.html").write_text("ok")
            archived = root / "_archive" / "old"; archived.mkdir(parents=True)
            (archived / "board.md").write_text("# Do not show\n")
            cards = discover_boards(root)
            self.assertEqual(len(cards), 1)
            self.assertEqual(cards[0]["title"], "A <Board>")
            self.assertEqual(cards[0]["settled"], 1)
            self.assertTrue(cards[0]["ready"])
            page = render_home(root)
            self.assertIn("A &lt;Board&gt;", page)
            self.assertIn("Open board", page)
            self.assertIn("/project/diagram/01-topic/board/index.html", page)
            self.assertEqual(cards[0]["kind"], "Task Board")

    def test_groups_task_paper_and_skill_boards_with_skill_precedence(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)

            def add_board(relative, title):
                board = root / relative
                (board / "QA-group").mkdir(parents=True)
                (board / "board.md").write_text(f"# {title}\nspine: Test type\n")
                (board / "QA-group" / "QA1-question.md").write_text("# Q\nstate: 🟡 PARTIAL\n")

            add_board("project/diagram/01-task", "Task")
            add_board("papers/Paper-A/0-lifecycle", "Paper")
            add_board("Tools/plugins/example/skills/diagrams/01-paper-skill", "Paper Skill")
            cards = {card["title"]: card for card in discover_boards(root)}
            self.assertEqual(cards["Task"]["kind"], "Task Board")
            self.assertEqual(cards["Paper"]["kind"], "Paper Board")
            self.assertEqual(cards["Paper Skill"]["kind"], "Skill Board")
            page = render_home(root)
            self.assertIn("📋 Task Boards", page)
            self.assertIn("📄 Paper Boards", page)
            self.assertIn("🧩 Skill Boards", page)
