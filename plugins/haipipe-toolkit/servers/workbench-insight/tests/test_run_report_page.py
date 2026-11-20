"""A Run's page shows its report first, an agent's reading beside result/, then the generated tables (workbench-insight
T31; haipipe-insight ref/run-report.md). A report written before the result changed is marked, and its headline is not
used as the segment's takeaway. Placeholders only.
"""
from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "_host"))
sys.path.insert(0, str(HERE))
from host_paths import bootstrap  # noqa: E402
bootstrap()

from live import insight_plan_c as P  # noqa: E402
from live import insight_view_task as VT  # noqa: E402
import plan_c_fixture as F  # noqa: E402

HEAD = "Placeholder headline: what the segment result shows."


class RunReportPageTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name).resolve()
        board = F.make(self.root) / F.BOARD
        self.run = next(r for r in sorted(board.glob("j*/t*/runs/r01_full")) if (r / "result" / "report.md").is_file())
        res = self.run / "result"
        (res / "report.md").rename(res / "tables.md")
        (res / "runtime.yaml").write_text(yaml.safe_dump({"status": "ok", "tables_sha256": "placeholder-sha"}))
        fm = {"run": "r01_full", "question": "D01", "segment": "full", "status": "ok", "result-sha256": "placeholder-sha",
              "written-by": "haipipe-insight-agent", "check": "✅ 261120 haipipe-insight-reviewer-agent", "headline": HEAD,
              "sentences": [{"text": "Placeholder sentence with 3 rows.", "file": "rates.csv"}], "caveat": "Placeholder caveat."}
        (self.run / "report.md").write_text("---\n" + yaml.safe_dump(fm, sort_keys=False) + "---\n\n# D01 · full\n")

    def tearDown(self):
        self.tmp.cleanup()

    def test_the_run_page_shows_its_report_then_its_tables(self):
        html = VT.render_run_page(self.run, self.root)
        self.assertIn("Report ✅", html)
        self.assertIn(HEAD, html)
        self.assertIn("Placeholder caveat.", html)
        self.assertIn("<h2>Tables</h2>", html)
        self.assertLess(html.index(HEAD), html.index("<h2>Tables</h2>"))
        self.assertEqual(P.run_card(self.run)["report"], self.run / "result" / "tables.md")
        self.assertEqual(P.report_headline(P.run_card(self.run)), HEAD)

    def test_a_report_written_before_the_result_changed_is_marked_and_not_used(self):
        (self.run / "result" / "runtime.yaml").write_text(yaml.safe_dump({"status": "ok", "tables_sha256": "changed"}))
        html = VT.render_run_page(self.run, self.root)
        self.assertIn("Report ❗", html)
        self.assertIn("write it again", html)
        self.assertEqual(P.report_headline(P.run_card(self.run)), "")


if __name__ == "__main__":
    unittest.main()
