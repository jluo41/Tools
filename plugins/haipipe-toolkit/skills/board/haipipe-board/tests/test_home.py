#!/usr/bin/env python3
"""Read-only discovery and rendering checks for the SPACE Board Home."""
import tempfile
import unittest
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent.parent  # the engine dir
sys.path.insert(0, str(HERE))
from live.home import (HomeMixin, board_slug, discover_boards, render_home,
                       resolve_short)


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


class ShortRouteTest(unittest.TestCase):
    """QE2 · `/b/<slug>[/<page-id>]`, the route that replaces the long path.

    JL measured a strip's link at 131 characters on 260802, 78 of them the path
    from the SPACE root down to the board folder. These lock in the two things
    that make the short form safe to print: it resolves to the SAME file the
    long URL names, and an id that resolves to nothing is a miss rather than a
    redirect to the wrong page.
    """

    def fixture(self, tmp):
        root = Path(tmp)
        board = root / "unit" / "diagram" / "01-topic-260722"
        (board / "QA-design").mkdir(parents=True)
        (board / "board" / "QA").mkdir(parents=True)
        (board / "board.md").write_text("# /the-board: a title\nspine: s\n")
        (board / "QA-design" / "QA1-question.md").write_text("# Q\nstate: 🔴 OPEN\n")
        (board / "board" / "index.html").write_text("index")
        (board / "board" / "QA.html").write_text("group")
        (board / "board" / "QA" / "QA1-question.html").write_text("page")
        return root, board

    def test_slug_drops_the_ordinal_and_the_date(self):
        self.assertEqual(board_slug("01-boardform-260722"), "boardform")
        self.assertEqual(board_slug("0-lifecycle"), "lifecycle")
        self.assertEqual(board_slug("plain"), "plain")

    def test_resolves_index_page_and_group(self):
        with tempfile.TemporaryDirectory() as tmp:
            root, _ = self.fixture(tmp)
            base = "/unit/diagram/01-topic-260722/board"
            self.assertEqual(resolve_short(root, "topic"), f"{base}/index.html")
            self.assertEqual(resolve_short(root, "topic", "QA1"),
                             f"{base}/QA/QA1-question.html")
            self.assertEqual(resolve_short(root, "topic", "QA"), f"{base}/QA.html")

    def test_the_full_folder_name_still_resolves(self):
        with tempfile.TemporaryDirectory() as tmp:
            root, _ = self.fixture(tmp)
            self.assertEqual(resolve_short(root, "01-topic-260722"),
                             resolve_short(root, "topic"))

    def test_an_unknown_board_or_page_is_a_miss_not_a_wrong_redirect(self):
        with tempfile.TemporaryDirectory() as tmp:
            root, _ = self.fixture(tmp)
            self.assertIsNone(resolve_short(root, "nosuchboard"))
            self.assertIsNone(resolve_short(root, "topic", "QZ9"))
            self.assertIsNone(resolve_short(root, ""))

    def test_the_route_matcher_accepts_only_its_own_shape(self):
        request = HomeMixin()
        for path, expected in [
            ("/b/topic", ("topic", "")),
            ("/b/topic/QA1", ("topic", "QA1")),
            ("/b/topic/QA1/", ("topic", "QA1")),
        ]:
            request.path = path
            self.assertEqual(request.short_request(), expected, path)
        for path in ("/b", "/b/", "/b/topic/QA1/extra", "/boards", "/bogus/x"):
            request.path = path
            self.assertIsNone(request.short_request(), path)


if __name__ == "__main__":
    unittest.main()
