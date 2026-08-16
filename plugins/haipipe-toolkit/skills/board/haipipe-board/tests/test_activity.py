#!/usr/bin/env python3
"""Regression tests for the Activity readout: updates counted from `## Log`.

These replaced six timer tests on 260816. Those tests protected a browser
focus-timer that wrote SQLite spans nobody read back, and they asserted things
the panel never printed: how seconds split across midnight, which heartbeat a
capped gap was allocated to, whether a late idle request honoured its deadline.
JL had already ruled on 260726 that the unit is UPDATES rather than time, so the
one behaviour on this route that a reader can actually see — counting dated
`## Log` lines — was the one behaviour with no test at all.
"""

import datetime as dt
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent  # the engine dir
sys.path.insert(0, str(HERE))

sys.path.insert(0, str(HERE / "cli"))          # the CLI moved into cli/ (260801)

import serve as board_serve  # noqa: E402


def stamp(days_ago):
    """A `## Log` date written the way a page writes it: YYMMDD."""
    return (dt.date.today() - dt.timedelta(days=days_ago)).strftime("%y%m%d")


class ActivityCountsTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.board = self.root / "work" / "diagram" / "01-board"
        self.board.mkdir(parents=True)
        (self.board / "board.md").write_text(
            "# Activity fixture\n\n## Pages\n### QD · Working\nQD8-test.md\n",
            encoding="utf-8",
        )
        self.handler = object.__new__(board_serve.Handler)
        self.handler.root = self.root
        self.handler._log_cache = {}
        board_serve.Handler._boards_cache = (0.0, None)

    def tearDown(self):
        self.temp.cleanup()

    def page(self, name, log_lines):
        (self.board / name).write_text(
            "# A page\n\nstate: 🟡 PARTIAL\n\n## Log\n" +
            "".join(f"- {line}\n" for line in log_lines),
            encoding="utf-8",
        )

    def stats(self):
        result, error = self.handler.activity(
            {"op": "stats", "path": "/work/diagram/01-board/board.html"})
        self.assertIsNone(error)
        return result

    def test_one_dated_log_line_is_one_update(self):
        self.page("QD8-test.md", [f"{stamp(0)} · did a thing",
                                  f"{stamp(0)} · did another thing",
                                  f"{stamp(1)} · did a thing yesterday"])
        s = self.stats()
        self.assertEqual(s["unit"], "updates")
        self.assertEqual(s["totals"]["updates"], 3)
        self.assertEqual(s["totals"]["today"], 2)

    def test_an_undated_line_is_not_an_update(self):
        self.page("QD8-test.md", [f"{stamp(0)} · dated, so counted",
                                  "no date here, so not counted"])
        self.assertEqual(self.stats()["totals"]["updates"], 1)

    def test_only_the_log_section_is_read(self):
        """A dated line outside `## Log` is prose, and prose is not a change."""
        (self.board / "QD8-test.md").write_text(
            f"# A page\n\n## States\n- {stamp(0)} · status prose, not a change\n"
            f"\n## Log\n- {stamp(0)} · the one real update\n",
            encoding="utf-8",
        )
        self.assertEqual(self.stats()["totals"]["updates"], 1)

    def test_the_route_takes_no_op_but_stats(self):
        """The timer's start/pulse/stop went with the SQLite store (260816)."""
        self.page("QD8-test.md", [f"{stamp(0)} · a thing"])
        for op in ("start", "pulse", "stop"):
            result, error = self.handler.activity(
                {"op": op, "path": "/work/diagram/01-board/board.html"})
            self.assertIsNone(result)
            self.assertIn(op, error)

    def test_no_state_is_written_anywhere(self):
        """The readout reads markdown and keeps nothing of its own."""
        self.page("QD8-test.md", [f"{stamp(0)} · a thing"])
        self.stats()
        self.assertFalse((self.root / ".haipipe-board").exists())


if __name__ == "__main__":
    unittest.main()
