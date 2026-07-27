import importlib.util
import tempfile
import unittest
from pathlib import Path


HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("board_status", HERE / "status.py")
STATUS = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(STATUS)
SERVE_SPEC = importlib.util.spec_from_file_location("board_serve", HERE / "serve.py")
SERVE = importlib.util.module_from_spec(SERVE_SPEC)
SERVE_SPEC.loader.exec_module(SERVE)


class StatusStripTest(unittest.TestCase):
    def fixture(self):
        temp = tempfile.TemporaryDirectory()
        root = Path(temp.name)
        board = root / "diagram" / "01-test-260726"
        board.mkdir(parents=True)
        (board / "board.md").write_text(
            "# Test Board\n"
            "spine: test the strip\n"
            "close: both pages settle\n"
            "## Topic\nTest.\n"
            "## Pages\n"
            "### QA · Define\n"
            "Explain the format.\n"
            "QA1-shape.md\n"
            "### QB · Source\n"
            "Find what the page needs.\n"
            "QB1-evidence.md\n",
            encoding="utf-8",
        )
        page = (
            "# Evidence owner\n"
            "state: 🟡 PARTIAL\n"
            "owner: CC\n"
            "method: bind evidence to this page\n\n"
            "## Question\nWhat evidence is needed?\n\n"
            "## Items to Finish\n- [ ] Find it\n\n"
            "## Where we are\nSearching.\n"
        )
        (board / "QB1-evidence.md").write_text(page, encoding="utf-8")
        (board / "QA1-shape.md").write_text(
            page.replace("# Evidence owner", "# Shape"),
            encoding="utf-8",
        )
        return temp, root, board

    def test_page_derives_queue_and_deep_link(self):
        temp, root, board = self.fixture()
        self.addCleanup(temp.cleanup)
        strip = STATUS.render(
            board, focus="QB1", mode="implementation", status="working",
            next_action="finish the renderer", root=root,
        )
        lines = strip.splitlines()
        self.assertEqual(len(lines), 3)
        self.assertTrue(lines[0].endswith("  "))
        self.assertTrue(lines[1].endswith("  "))
        self.assertIn(
            "🧭 [01-test-260726 · QB/QB1]"
            "(http://127.0.0.1:5599/diagram/01-test-260726/board.html#QB1)",
            strip,
        )
        self.assertIn("🔥 working · implementation", strip)
        self.assertIn("→ finish the renderer", strip)
        self.assertNotIn("queue:", strip)
        self.assertNotIn("file:", strip)

    def test_group_focus_is_its_queue(self):
        temp, root, board = self.fixture()
        self.addCleanup(temp.cleanup)
        strip = STATUS.render(board, focus="group:QA", mode="discussion", root=root)
        self.assertIn("🧭 [01-test-260726 · QA]", strip)
        self.assertIn("⬜ ready · discussion", strip)
        self.assertIn("→ continue discussion on QA", strip)

    def test_unowned_sourcing_is_blocked(self):
        temp, root, board = self.fixture()
        self.addCleanup(temp.cleanup)
        strip = STATUS.render(
            board, focus="board", mode="sourcing", status="working", root=root
        )
        self.assertIn("⛔ blocked · sourcing", strip)
        self.assertIn("→ sourcing must serve one page or page group", strip)

    def test_sourcing_for_page_is_visible(self):
        temp, root, board = self.fixture()
        self.addCleanup(temp.cleanup)
        strip = STATUS.render(
            board, focus="QB1", mode="sourcing", status="working", root=root
        )
        self.assertIn("🧭 [01-test-260726 · QB/QB1]", strip)
        self.assertIn("🔥 working · sourcing", strip)

    def test_page_launcher_injects_same_closing_block_contract(self):
        temp, root, board = self.fixture()
        self.addCleanup(temp.cleanup)
        prime = SERVE.prime_context(board / "QB1-evidence.md", board, root)
        self.assertIn("VISIBLE BOARD ATTACHMENT (mandatory)", prime)
        self.assertIn('--focus "QB1"', prime)
        self.assertIn("End EVERY user-visible reply", prime)
        self.assertIn("three-line Markdown closing block", prime)
        self.assertIn("Do not create or update a shared STATUS.md", prime)

    def test_board_launcher_uses_board_focus(self):
        temp, root, board = self.fixture()
        self.addCleanup(temp.cleanup)
        prime = SERVE.prime_context(board / "board.md", board, root)
        self.assertIn('--focus "board"', prime)
        self.assertIn("board-level work is yours", prime.casefold())


if __name__ == "__main__":
    unittest.main()
