#!/usr/bin/env python3
"""Regression tests for Activity counts from Page outline log records."""

import datetime as dt
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent  # the engine dir
sys.path.insert(0, str(HERE))

sys.path.insert(0, str(HERE / "cli"))          # the CLI moved into cli/ (260801)

import serve as board_serve  # noqa: E402
from live import activity  # noqa: E402


def stamp(days_ago):
    """A Page log date in YYMMDD form."""
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
        # `log_boards()` shares one 2-second walk across every request, and the
        # cache lives on the MIXIN. Each test builds a fresh temp root, so it
        # must be cleared where it is actually read or the second test in a run
        # counts the first test's deleted directory and sees nothing.
        activity.ActivityMixin._boards_cache = (0.0, None)

    def tearDown(self):
        self.temp.cleanup()

    def page(self, name, log_lines):
        stem = Path(name).stem
        home = self.board / stem
        (home / "outline").mkdir(parents=True)
        (home / name).write_text(
            "# A page\n\nstate: 🟡 PARTIAL\n\n## Opening\nA current Page.\n",
            encoding="utf-8",
        )
        (home / "outline" / f"{stem}-log.md").write_text(
            f"# {stem} · log\npage: {stem}\n"
            "kind: log · authored · append-only, newest first\n\n"
            + "".join(f"### {line}\n" for line in log_lines),
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

    def test_page_prose_is_not_counted(self):
        self.page("QD8-test.md", [f"{stamp(0)} · the one real update"])
        page = self.board / "QD8-test" / "QD8-test.md"
        page.write_text(
            page.read_text(encoding="utf-8")
            + f"\n{stamp(0)} · dated prose, not a log record\n",
            encoding="utf-8",
        )
        self.assertEqual(self.stats()["totals"]["updates"], 1)

    def test_flat_page_log_remains_a_compatibility_fallback(self):
        (self.board / "QD8-test.md").write_text(
            "# A historical page\n\n"
            f"## Log\n- {stamp(0)} · historical update\n",
            encoding="utf-8",
        )
        self.assertEqual(self.stats()["totals"]["updates"], 1)

    def test_the_route_takes_no_op_but_stats(self):
        """The read-only endpoint accepts only the stats operation."""
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
