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

from runs_panel import panel_html, row_space, run_types  # noqa: E402


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
                       ("Draft", "Auto write"), ("Evidence", "Bind / update citation"),
                       ("Delivery", "Build"), ("Delivery", "Check"), ("Draft", "Context"),
                       ("Draft", "Revise edits")]:
            self.assertIn(wanted, labels)
        self.assertTrue(all(t["prompt"] for t in types))
        views = {t["label"]: t["views"] for t in types}
        self.assertEqual(views["Structure revise"], "table")
        # The studio drawing's order puts Context in the Table view (JL 260929).
        self.assertEqual(views["Context"], "table")
        skills = {t["label"]: t["skills"] for t in types}
        # one skill per button (2026-10-03); haipipe-display loads the evidence skill it needs
        self.assertEqual(skills["Build figure / table"], ["haipipe-display"])
        self.assertEqual(skills["Bind / update value"], ["haipipe-page-evidence"])
        # Each view lists only its own run types (JL 260927).
        self.assertEqual(views["Paragraph revise"], "revise")
        self.assertEqual(views["Scratch"], "scratch")
        self.assertEqual(views["Auto write"], "reading")
        self.assertEqual(views["Bind / update value"], "values")
        self.assertTrue(all(t["views"] for t in run_types() if t["space"] != "Page"))

    def test_runs_sort_into_their_space_and_type(self):
        self.assertEqual(row_space(self.rows[0]), "draft")
        self.assertEqual(row_space(self.rows[1]), "delivery")
        html = panel_html(self.page, "draft", self.rows, run_types(), plan_name="draft/Sample-draft-v1.1.md")
        self.assertIn('data-run="rp-para-02_P02"', html)
        self.assertIn('data-targets="C1.P2"', html)
        self.assertIn('data-name="run-paragraph-02"', html)  # the full name, not rp-para
        self.assertIn("revise Sample C1.P2", html)
        self.assertNotIn("rd01_latex", html)

    def test_delivery_shows_one_fixed_run_per_lane_on_its_format_tab(self):
        # JL 260928: one Run per lane (run-delivery-latex); an older numbered rd01_latex is history
        rows = self.rows + [{"global_id": "run-delivery-latex", "ticket": "", "target": "delivery/latex",
                             "status": "Done", "result": "delivery/latex/"}]
        html = panel_html(self.page, "delivery", rows, run_types(), plan_name="draft/x.md")
        self.assertIn('data-run="run-delivery-latex"', html)
        self.assertIn('data-views="latex"', html)
        self.assertNotIn('data-run="rd01_latex"', html)
        self.assertNotIn("rp-para-02_P02", html)


    def test_evidence_runs_are_named_by_the_item_they_serve(self):
        folder = self.page.parent / "runs" / "evidence-run"
        folder.mkdir()
        ticket = folder / "re-value-02_value-dose.md"
        ticket.write_text("---\nrun: re-value-02_value-dose\nitem: E25-VALUE-dose\n---\n", encoding="utf-8")
        rows = [{"global_id": "re-value-02_value-dose", "ticket": str(ticket), "status": "Done"},
                {"global_id": "pj02t25r01_dose", "ticket": str(folder / "pj02t25r01_dose.sh"), "status": "Done"}]
        html = panel_html(self.page, "evidence", rows, run_types(), plan_name="draft/x.md",
                          run_tabs={"pj02t25r01": {"tab": "values", "item": "E25", "target": "C1.P5.B2"}})
        self.assertIn('data-name="run-Evalue25"', html)    # the older run comes first
        self.assertIn('data-name="run-Evalue25-2"', html)  # a later run for the same item


if __name__ == "__main__":
    unittest.main()
