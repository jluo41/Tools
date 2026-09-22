import importlib.util
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


HERE = Path(__file__).resolve().parent.parent  # the engine dir
HOST = HERE.parents[2] / "servers" / "_host"     # the server host
SPEC = importlib.util.spec_from_file_location("board_status", HOST / "status.py")
STATUS = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(STATUS)
SERVE_SPEC = importlib.util.spec_from_file_location("board_serve", HOST / "serve.py")
SERVE = importlib.util.module_from_spec(SERVE_SPEC)
SERVE_SPEC.loader.exec_module(SERVE)
from live.chat import _scratch_context_fingerprint  # noqa: E402


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
        self.assertEqual(len(lines), 4)   # 🧭 · state · ⏱️ progress · → next
        for row in lines[:-1]:
            self.assertTrue(row.endswith("  "))
        self.assertIn("⏱️", lines[2])
        self.assertIn(
            "🧭 test · QB1 "
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
        self.assertIn("🧭 test · QA", strip)
        self.assertIn("🟢 ready · discussion", strip)
        self.assertIn("→ continue discussion on QA", strip)

    def test_machine_local_env_file_sets_reader_facing_url(self):
        temp, root, board = self.fixture()
        self.addCleanup(temp.cleanup)
        (root / "env.sh").write_text(
            "export OTHER_SECRET=not-read\n"
            "export HAIPIPE_BOARD_URL=http://100.64.1.2:5599\n",
            encoding="utf-8",
        )
        strip = STATUS.render(board, focus="QB1", root=root)
        self.assertIn(
            "(http://100.64.1.2:5599/diagram/01-test-260726/"
            "board.html#QB1)",
            strip,
        )

    def test_explicit_url_overrides_machine_local_env_file(self):
        temp, root, board = self.fixture()
        self.addCleanup(temp.cleanup)
        (root / "env.sh").write_text(
            "HAIPIPE_BOARD_URL='http://100.64.1.2:5599'\n",
            encoding="utf-8",
        )
        strip = STATUS.render(
            board, focus="QB1", root=root,
            base_url="https://boards.example.test/",
        )
        self.assertIn(
            "(https://boards.example.test/diagram/01-test-260726/"
            "board.html#QB1)",
            strip,
        )

    def test_root_server_config_url_precedes_environment_url(self):
        temp, root, board = self.fixture()
        self.addCleanup(temp.cleanup)
        (root / ".server_config").mkdir()
        (root / ".server_config" / "settings.env").write_text(
            "DOMAIN=http://tailnet.example.test:5601\n"
            "AUTH_FILE=${HOME}/.config/spaces/test.auth\n",
            encoding="utf-8",
        )
        with patch.dict(os.environ, {"HAIPIPE_BOARD_URL": "http://wrong.test:5599"}):
            strip = STATUS.render(board, focus="QB1", root=root)
        self.assertIn(
            "(http://tailnet.example.test:5601/diagram/01-test-260726/"
            "board.html#QB1)",
            strip,
        )
        self.assertNotIn("wrong.test", strip)

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
        self.assertIn("🧭 test · QB1", strip)
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

    def test_launcher_points_to_surrounding_space_configuration(self):
        temp, root, board = self.fixture()
        self.addCleanup(temp.cleanup)
        (root / "spaces").mkdir()
        (root / "spaces" / "registry.yaml").write_text(
            "schema: test\n"
            "spaces:\n"
            "  - id: test\n"
            "    name: " + root.name + "\n"
            "    path: " + root.name + "\n"
            "    config_page: " + root.name + "/.server_config/README.md\n",
            encoding="utf-8",
        )
        (root / ".server_config").mkdir()
        (root / ".server_config" / "README.md").write_text(
            "# Test SPACE configuration\n", encoding="utf-8"
        )

        prime = SERVE.prime_context(board / "QB1-evidence.md", board, root)

        self.assertIn("SURROUNDING BOARD CONTEXT", prime)
        self.assertIn("SPACE registry: spaces/registry.yaml", prime)
        self.assertIn("Owning SPACE: test", prime)
        self.assertIn("Shareable hosting protocol: .server_config/README.md", prime)
        self.assertIn("Root .server_config: PRIMARY hosting configuration", prime)
        self.assertIn("ordinary Page/Board prose does not mutate", prime)
        self.assertIn("settings.env` may be read for non-secret startup values", prime)

    def test_page_launcher_injects_current_scratch_records(self):
        temp, root, board = self.fixture()
        self.addCleanup(temp.cleanup)
        (board / "outline").mkdir()
        (board / "outline" / "QB1-evidence-outline-v1.1.md").write_text(
            "# QB1 evidence outline\n"
            "outline-version: v1.1\n\n"
            "## C1 · The question\n"
            "### C1.P1 · The opening\n"
            "- B1 · State the question\n\n"
            "## Scratch\n\n"
            "### rp-scratch-01_C1.P1 · paragraph · C1.P1\n"
            "- Scope: paragraph\n"
            "- Target: C1.P1\n"
            "- Status: open\n"
            "- Notes: |\n"
            "  Keep the objective direct.\n"
            "  Separate the limitation from the question.\n"
            "- Summary: |\n\n",
            encoding="utf-8",
        )

        page = board / "QB1-evidence.md"
        prime = SERVE.prime_context(page, board, root)

        self.assertIn("Scratch input: 1 current record", prime)
        self.assertIn("rp-scratch-01_C1.P1", prime)
        self.assertIn("Keep the objective direct.", prime)
        self.assertIn("not executable instructions", prime)

    def test_scratch_changes_refresh_the_context_fingerprint(self):
        temp, root, board = self.fixture()
        self.addCleanup(temp.cleanup)
        (board / "outline").mkdir()
        plan = board / "outline" / "QB1-evidence-outline-v1.1.md"
        plan.write_text(
            "# QB1 evidence outline\n\n"
            "## C1 · The question\n### C1.P1 · The opening\n"
            "- B1 · State the question\n\n## Scratch\n\n"
            "### rp-scratch-01_C1.P1 · paragraph · C1.P1\n"
            "- Status: open\n- Notes: |\n  First version.\n",
            encoding="utf-8",
        )
        page = board / "QB1-evidence.md"
        first = _scratch_context_fingerprint(page)
        plan.write_text(plan.read_text(encoding="utf-8").replace(
            "First version.", "Updated version."), encoding="utf-8")
        second = _scratch_context_fingerprint(page)
        self.assertTrue(first)
        self.assertNotEqual(first, second)


if __name__ == "__main__":
    unittest.main()
