"""Runs panels: run types come from the Run cards; runs sort into their Space."""
from __future__ import annotations

from pathlib import Path
import sys
import tempfile
import unittest

SERVER_DIR = Path(__file__).resolve().parents[1]
PAGE_ROOT = SERVER_DIR.parents[1] / "skills" / "page" / "haipipe-page"
sys.path.insert(0, str(PAGE_ROOT))
sys.path.insert(0, str(SERVER_DIR.parent / "workbench-page"))

from runs_panel import page_bar_html, panel_html, row_space, run_types  # noqa: E402


class RunsPanelTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.page = Path(self.tmp.name) / "Sample" / "Sample.md"
        (self.page.parent / "runs" / "draft-manual-run").mkdir(parents=True)
        self.page.write_text("# Sample\n", encoding="utf-8")
        ticket = self.page.parent / "runs" / "draft-manual-run" / "rp-para-02_P02.md"
        ticket.write_text("---\nrun: rp-para-02_P02\n---\n", encoding="utf-8")
        self.rows = [
            {"global_id": "rp-para-02_P02", "ticket": str(ticket), "target": "C1.P2",
             "status": "Waiting", "result": "results/rp-para-02_P02", "goal": "Revise P2"},
            {"global_id": "rd01_latex", "ticket": "", "target": "latex", "status": "Done",
             "result": "results/rd01_latex"},
        ]

    def tearDown(self):
        self.tmp.cleanup()

    def test_run_cards_give_every_space_its_buttons_and_prompts(self):
        types = run_types()
        labels = {(t["space"], t["label"]) for t in types}
        for wanted in [("Draft", "Paragraph revise"), ("Draft", "Evidence embed"),
                       ("Draft", "Auto write"), ("Evidence", "Citation"),
                       ("Delivery", "LaTeX"), ("Page", "Check")]:
            self.assertIn(wanted, labels)
        self.assertTrue(all(t["prompt"] for t in types))

    def test_runs_sort_into_their_space_and_type(self):
        self.assertEqual(row_space(self.rows[0]), "draft")
        self.assertEqual(row_space(self.rows[1]), "delivery")
        html = panel_html(self.page, "draft", self.rows, run_types(), plan_name="draft/Sample-draft-v1.1.md")
        self.assertIn('data-run="rp-para-02_P02"', html)
        self.assertIn('data-targets="C1.P2"', html)
        self.assertIn("1 run · 1 waiting for you", html)
        self.assertIn("revise Sample C1.P2", html)
        self.assertNotIn("rd01_latex", html)

    def test_page_bar_counts_waiting_runs_and_offers_page_runs(self):
        bar = page_bar_html(self.page, run_types(), self.rows, plan_name="draft/x.md", readiness="ready")
        self.assertIn("Runs · 1 waiting", bar)
        self.assertIn("Check run", bar)
        self.assertIn("pagebar-focus", bar)


if __name__ == "__main__":
    unittest.main()
