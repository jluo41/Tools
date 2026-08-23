"""`store:` on board.md — the optional key that routes commissioned output.

A board that owns its evidence base declares where work it commissions writes
its results, notebooks and QA digests. A dispatching probe resolves the line
once and hands the executor an absolute path, so the key must not climb.
"""
import re
import unittest
from pathlib import Path

from cli.check import ERROR, Report, check_board


def board_src(store_line=""):
    return (
        "# Test Board\n"
        "spine: test the store key\n"
        "close: the store resolves\n"
        f"{store_line}"
        "## Topic\nA test Board.\n"
        "## Pipeline\nOne page follows another.\n"
        "## Pages\n"
    )


class BoardStoreTest(unittest.TestCase):
    def codes(self, store_line, tmp):
        (tmp / "board.md").write_text(board_src(store_line), encoding="utf-8")
        rep = Report()
        check_board(tmp, rep)
        return [row[1] for row in rep.rows]

    def setUp(self):
        import tempfile
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()

    def test_store_is_optional(self):
        # Most boards commission nothing that produces files. Absent is normal,
        # not a gap, and must not be reported as one.
        self.assertNotIn("board-missing-key", self.codes("", self.tmp))
        self.assertNotIn("board-store-path", self.codes("", self.tmp))

    def test_repo_relative_store_passes(self):
        codes = self.codes("store: _WorkSpace/InsightBoardResult/A01_Board\n", self.tmp)
        self.assertNotIn("board-store-path", codes)

    def test_absolute_store_passes(self):
        codes = self.codes("store: /var/data/board-store\n", self.tmp)
        self.assertNotIn("board-store-path", codes)

    def test_climbing_store_is_an_error(self):
        # A `..` resolves against whoever dispatched, so two callers of the same
        # board would write to two different places.
        self.assertIn("board-store-path",
                      self.codes("store: ../../elsewhere\n", self.tmp))

    def test_tilde_store_is_an_error(self):
        # `~` is the shell's, not git's; it resolves per-user.
        self.assertIn("board-store-path",
                      self.codes("store: ~/board-store\n", self.tmp))

    def test_spine_and_close_stay_required(self):
        # The new optional key must not have loosened the two required ones.
        (self.tmp / "board.md").write_text(
            "# Test Board\nstore: some/where\n## Topic\nT.\n## Pipeline\nP.\n## Pages\n",
            encoding="utf-8")
        rep = Report()
        check_board(self.tmp, rep)
        missing = [r for r in rep.rows if r[1] == "board-missing-key"]
        self.assertEqual(len(missing), 2, "spine and close are both still owed")


class BoardStoreContractTest(unittest.TestCase):
    """The contract files must agree on who sets what, or the mechanism drifts."""

    SKILLS = Path(__file__).resolve().parents[3]

    def test_probe_router_states_the_dispatch_field(self):
        text = (self.SKILLS / "probe/haipipe-probe/SKILL.md").read_text(encoding="utf-8")
        self.assertIn("result_store:", text)
        self.assertIn("RESULT_STORE", text)

    def test_qa_return_carries_the_bank(self):
        text = (self.SKILLS / "task/haipipe-task/fn/qa.md").read_text(encoding="utf-8")
        self.assertRegex(text, r"(?m)^bank:",
                         msg="the qa return must name the bank it addressed")

    def test_run_template_resolves_rather_than_hardcodes(self):
        text = (self.SKILLS / "task/haipipe-task/ref/run-sh-template.sh").read_text(encoding="utf-8")
        self.assertIn("RESULT_STORE", text)
        self.assertIn("OUTPUT_ROOT", text)
        self.assertNotRegex(
            text, r'^RESULTS_DIR="\$TASK_DIR/results',
            msg="output location must be resolved, never hardcoded to the task folder")


if __name__ == "__main__":
    unittest.main()
