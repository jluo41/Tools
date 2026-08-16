"""The /_board/pageruns summarizer: receipts in, one page's run list out."""

import json
import tempfile
import unittest
from pathlib import Path

from live.pageruns import page_runs


def receipt(step, phase, route, verdict=""):
    return {"step": step, "round": 1, "phase": phase, "route": route,
            "verdict": verdict, "status": "ok", "reason": "r"}


def run_json(run_id, page, receipts, status="open"):
    return {"status": status, "run_id": run_id, "page": page,
            "packet": {"start_phase": receipts[0]["phase"] if receipts else ""},
            "receipts": receipts}


class PageRunsTest(unittest.TestCase):

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.board = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def write(self, rel, payload):
        p = self.board / "_runs" / "page" / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(payload), encoding="utf-8")
        return p

    def test_no_runs_dir_is_an_answer_not_an_error(self):
        self.assertEqual(page_runs(self.board, "QB1-form.md"), [])

    def test_matches_by_the_receipts_own_page_field(self):
        self.write("QPw1/a.json", run_json(
            "run-a", "QPw-group/QPw1-loop/QPw1-loop.md",
            [receipt(1, "DRAFT", "CHECK"),
             receipt(2, "CHECK", "REVISE", "revise")]))
        self.write("QB1/b.json", run_json(
            "run-b", "QB1-form.md", [receipt(1, "CHECK", "CLOSE", "close")]))
        got = page_runs(self.board, "QPw-group/QPw1-loop/QPw1-loop.md")
        self.assertEqual([r["run_id"] for r in got], ["run-a"])
        self.assertEqual(got[0]["last"]["phase"], "CHECK")
        self.assertEqual(got[0]["last"]["route"], "REVISE")
        self.assertEqual(got[0]["steps"], 2)
        self.assertEqual(got[0]["start_phase"], "DRAFT")

    def test_newest_run_first(self):
        import os
        a = self.write("QB1/old.json", run_json(
            "old", "QB1-form.md", [receipt(1, "DRAFT", "CHECK")]))
        self.write("QB1/new.json", run_json(
            "new", "QB1-form.md", [receipt(1, "CHECK", "CLOSE", "close")],
            status="closed"))
        old_time = a.stat().st_mtime - 100
        os.utime(a, (old_time, old_time))
        got = page_runs(self.board, "QB1-form.md")
        self.assertEqual([r["run_id"] for r in got], ["new", "old"])

    def test_broken_json_is_skipped_not_fatal(self):
        p = self.board / "_runs" / "page" / "QB1" / "bad.json"
        p.parent.mkdir(parents=True)
        p.write_text("{not json", encoding="utf-8")
        self.write("QB1/good.json", run_json(
            "good", "QB1-form.md", [receipt(1, "DRAFT", "CHECK")]))
        got = page_runs(self.board, "QB1-form.md")
        self.assertEqual([r["run_id"] for r in got], ["good"])


if __name__ == "__main__":
    unittest.main()
