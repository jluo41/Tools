#!/usr/bin/env python3
"""Focused regression tests for QD8 board activity timing."""

import datetime as dt
import sqlite3
import sys
import tempfile
import time
import unittest
from pathlib import Path
from unittest import mock

HERE = Path(__file__).resolve().parent.parent  # the engine dir
sys.path.insert(0, str(HERE))

import serve as board_serve  # noqa: E402


class ActivityTimingTest(unittest.TestCase):
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
        self.base = time.time()

    def tearDown(self):
        self.temp.cleanup()

    def send(self, op, at, **extra):
        payload = {
            "op": op,
            "path": "/work/diagram/01-board/board.html",
            "span": "activity-test-span",
            "page": "QD8",
            "group": "QD · Working",
            "title": "Activity timing",
            "actor": "JL",
            "active": True,
            "changed": False,
            **extra,
        }
        with mock.patch.object(board_serve.time, "time", return_value=at):
            result, error = self.handler.activity(payload)
        self.assertIsNone(error)
        return result

    def test_span_accumulates_once_and_records_stop_reason(self):
        self.send("start", self.base)
        self.send("pulse", self.base + 30, changed=True)
        self.send("stop", self.base + 50, reason="idle")

        # The DASHBOARD stopped reporting time on 260726 (JL: "I don't care
        # about the time"), so these assertions read the stored span instead of
        # the stats payload. The recorder is still exact; it is simply no
        # longer what the page shows.
        db = sqlite3.connect(self.root / ".haipipe-board" / "activity.sqlite3")
        row = db.execute("""
            SELECT active_seconds, stop_reason
            FROM activity_spans WHERE span_id='activity-test-span'
        """).fetchone()
        tick_seconds = db.execute("""
            SELECT SUM(seconds) FROM activity_ticks
            WHERE span_id='activity-test-span'
        """).fetchone()[0]
        db.close()
        self.assertAlmostEqual(row[0], 50)
        self.assertEqual(row[1], "idle")
        self.assertAlmostEqual(tick_seconds, 50)

        self.send("pulse", self.base + 80)
        db = sqlite3.connect(self.root / ".haipipe-board" / "activity.sqlite3")
        replayed = db.execute(
            "SELECT active_seconds FROM activity_spans "
            "WHERE span_id='activity-test-span'").fetchone()[0]
        db.close()
        self.assertAlmostEqual(replayed, 50)   # a stopped span never resumes

    def test_cross_midnight_seconds_land_on_both_days(self):
        start = dt.datetime(2026, 7, 26, 23, 59, 50).timestamp()
        end = dt.datetime(2026, 7, 27, 0, 0, 20).timestamp()
        self.send("start", start)
        self.send("stop", end, reason="pagehide")

        db = sqlite3.connect(self.root / ".haipipe-board" / "activity.sqlite3")
        parts = db.execute("""
            SELECT day, seconds FROM activity_ticks
            WHERE span_id='activity-test-span' ORDER BY day
        """).fetchall()
        db.close()

        self.assertEqual([day for day, _ in parts], ["2026-07-26", "2026-07-27"])
        self.assertAlmostEqual(parts[0][1], 10)
        self.assertAlmostEqual(parts[1][1], 20)
        self.assertAlmostEqual(sum(seconds for _, seconds in parts), 30)

    def test_capped_gap_is_allocated_nearest_the_heartbeat(self):
        start = dt.datetime(2026, 7, 26, 23, 0, 0).timestamp()
        end = dt.datetime(2026, 7, 27, 0, 0, 15).timestamp()
        parts = board_serve.Handler.activity_day_parts(start, end, 45)

        self.assertEqual([day for day, _ in parts], ["2026-07-26", "2026-07-27"])
        self.assertAlmostEqual(parts[0][1], 30)
        self.assertAlmostEqual(parts[1][1], 15)

    def test_late_idle_request_uses_the_exact_activity_deadline(self):
        self.send("start", self.base)
        for seconds in range(30, 271, 30):
            self.send("pulse", self.base + seconds)
        self.send(
            "stop",
            self.base + 329,
            reason="idle",
            active_until=self.base + 300,
        )

        db = sqlite3.connect(self.root / ".haipipe-board" / "activity.sqlite3")
        ended_at, stop_reason = db.execute("""
            SELECT ended_at, stop_reason FROM activity_spans
            WHERE span_id='activity-test-span'
        """).fetchone()
        db.close()
        self.assertAlmostEqual(ended_at, self.base + 300)
        self.assertEqual(stop_reason, "idle")

    def test_page_change_cannot_reassign_the_span(self):
        self.send("start", self.base)
        self.send(
            "stop",
            self.base + 10,
            page="QA1",
            group="QA · Defining",
            title="Destination page",
            reason="page-change",
        )

        db = sqlite3.connect(self.root / ".haipipe-board" / "activity.sqlite3")
        page, group_name = db.execute("""
            SELECT page, group_name FROM activity_spans
            WHERE span_id='activity-test-span'
        """).fetchone()
        db.close()
        self.assertEqual(page, "QD8")
        self.assertEqual(group_name, "QD · Working")

    def test_legacy_stage_ids_are_accepted(self):
        for index, page in enumerate(("S0", "SM1", "SA1"), start=1):
            span = f"legacy-stage-span-{index}"
            self.send("start", self.base + index, span=span, page=page)
            self.send(
                "stop",
                self.base + index + 1,
                span=span,
                page=page,
                reason="pagehide",
            )

        db = sqlite3.connect(self.root / ".haipipe-board" / "activity.sqlite3")
        pages = [
            row[0]
            for row in db.execute(
                "SELECT page FROM activity_spans ORDER BY span_id"
            ).fetchall()
        ]
        db.close()
        self.assertEqual(pages, ["S0", "SM1", "SA1"])


if __name__ == "__main__":
    unittest.main()
