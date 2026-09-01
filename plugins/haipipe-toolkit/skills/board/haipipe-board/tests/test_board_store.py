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

    def test_land_cycle_states_the_result_store(self):
        # the probe router retired 260901; the result-store resolution law
        # lives with the LAND cycle, which writes the row's result pointer
        text = (self.SKILLS / "board/page-workflows/haipipe-page-evidence/SKILL.md").read_text(encoding="utf-8")
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


class BoardReadsTest(unittest.TestCase):
    """`reads:` — the design board's evidence whitelist (JL 260824)."""

    def setUp(self):
        import tempfile
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name)
        (self.tmp / "A01_X-InsightBoard").mkdir()

    def tearDown(self):
        self._tmp.cleanup()

    def codes(self, line):
        (self.tmp / "B01_Y-DesignBoard").mkdir(exist_ok=True)
        (self.tmp / "B01_Y-DesignBoard/board.md").write_text(
            board_src(line), encoding="utf-8")
        rep = Report()
        check_board(self.tmp / "B01_Y-DesignBoard", rep)
        return [row[1] for row in rep.rows]

    def test_reads_is_optional(self):
        codes = self.codes("")
        self.assertNotIn("board-reads-target", codes)

    def test_sibling_board_name_passes(self):
        codes = self.codes("reads: A01_X-InsightBoard\n")
        self.assertNotIn("board-reads-target", codes)
        self.assertNotIn("board-reads-path", codes)
        self.assertNotIn("legacy-application-board-name", codes)

    def test_dead_entry_is_an_error(self):
        # The grant chain starts at reads:, so a dead entry poisons every
        # citation beneath it.
        self.assertIn("board-reads-target",
                      self.codes("reads: A99_Nowhere-InsightBoard\n"))

    def test_climbing_entry_is_an_error(self):
        self.assertIn("board-reads-path", self.codes("reads: ../../elsewhere\n"))

    def test_multiple_entries_each_checked(self):
        codes = self.codes("reads: A01_X-InsightBoard · A99_Gone\n")
        self.assertIn("board-reads-target", codes)

    def test_kind_first_board_name_is_compatibility_only(self):
        legacy = self.tmp / "B01_DesignBoard-Y"
        legacy.mkdir()
        (legacy / "board.md").write_text(board_src(), encoding="utf-8")
        rep = Report()
        check_board(legacy, rep)
        self.assertIn(
            "legacy-application-board-name",
            [row[1] for row in rep.rows],
        )
