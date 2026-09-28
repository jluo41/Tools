"""The three Spaces: Evidence tabs read the Evidence Markdown; Delivery tabs read delivery/."""
from __future__ import annotations

from pathlib import Path
import sys
import tempfile
import unittest

SERVER_DIR = Path(__file__).resolve().parents[1]
PAGE_ROOT = SERVER_DIR.parents[1] / "skills" / "page" / "haipipe-page"
sys.path.insert(0, str(PAGE_ROOT))
sys.path.insert(0, str(SERVER_DIR.parent / "workbench-page"))

from space_views import (delivery_space_html, draft_reads_html,  # noqa: E402
                         evidence_items, evidence_space_html, file_url, run_tabs)

PLAN = """# Sample · draft v1.1
draft-version: v1.1
approved: ⬜

## 1 · Structure · Bullet Point Table

### Structure Overview

- C1 · Answer
- C1.P1 · State the answer
  → S1 to S2 · the job

### C1.P1 · State the answer · S1 to S2
- B1 · S1 · [Claim] First claim
- B2 · S2 · [Claim] Second claim

## 2 · Scratch · What to write here

### C1.P1 · State the answer · S1 to S2

## 3 · Draft · Reading and Revise

### C1.P1 · State the answer · S1 to S2
- B1 · S1 · The first sentence.
- B2 · S2 · The second sentence.
"""
ITEMS = """# Sample · evidence items

## Citations

### E01-CITE-first-source · C1.P1.B1 · the first source
- **Target**: C1.P1.B1
- **Label**: FirstSource
- **Verified**: ✅ JL 260906
- **Local Run**: Page · Evidence Item · reuse · pj02t01r01 → results/pj02t01r01_first/result.yaml

#### E09-CITE-retired-source · retired

## Displays

## Values

- `E04-DISPLAY-moved` moved out; keep `pj02t04r01` for its new Page.

### E05-VALUE-headline · C1.P1.B2 · headline value
- **Target**: C1.P1.B2
- **Local Run**: Page · Evidence Item · pj02t05r01
"""


class SpaceViewsTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.page = Path(self.tmp.name) / "Sample" / "Sample.md"
        (self.page.parent / "draft").mkdir(parents=True)
        self.page.write_text("# Sample\n", encoding="utf-8")
        (self.page.parent / "draft" / "Sample-draft-v1.1.md").write_text(PLAN, encoding="utf-8")
        (self.page.parent / "draft" / "Sample-evidence-items.md").write_text(ITEMS, encoding="utf-8")

    def tearDown(self):
        self.tmp.cleanup()

    def test_draft_reads_line_names_the_plan_and_its_sections(self):
        self.assertIn("Reads <code>draft/Sample-draft-v1.1.md</code>", draft_reads_html(self.page))
        self.assertIn("## 3 Draft", draft_reads_html(self.page))

    def test_evidence_items_keep_current_items_by_tab_with_their_state(self):
        items = evidence_items(self.page)
        self.assertEqual([(i["id"], i["tab"], i["state"]) for i in items],
                         [("E01", "citations", "verified"), ("E05", "values", "bound")])
        html = evidence_space_html(self.page, card_url="/_board/evidence?embed=1")
        self.assertIn('data-tab="citations" data-label="Citations">Citations <span class=space-count>1</span>', html)
        self.assertIn('data-item="E01"', html)
        self.assertNotIn("E09", html.split("space-source")[0])
        self.assertIn("All values for this page · 1", html)

    def test_supporting_runs_tab_draws_block_job_task_run_with_the_items_they_feed(self):
        ticket = ("/repo/examples/Project-X/task/b03_CD_visit_pain/j02_D_regression_visit_pain/"
                  "t01_D_reg_VisitLBP_1stPair/runs/agre/r04_D_reg_VisitLBP_1stPair_ols.ps1")
        runs = [{"compact_id": "b03j02t01r04", "run_id": "b03.j02.t01.r04", "ticket": ticket,
                 "kind": "Execution", "status": "Ready", "refs": ["E01-CITE-first-source"]},
                {"compact_id": "b09j01t01r01", "run_id": "b09.j01.t01.r01", "ticket": "",
                 "kind": "Discovery", "status": "Held", "refs": []}]
        html = evidence_space_html(self.page, card_url="/x", supporting=runs)
        self.assertIn('data-tab="supporting" data-label="Supporting Runs" data-views="items source">'
                      'Supporting Runs <span class=space-count>2</span>', html)
        tree = html[html.index("sup-tree"):]
        order = [tree.index(s) for s in ("<b>Execution</b> <code class=sup-path>Project-X/task/</code>",
                                          "<span class=sup-lvl>b03</span>_CD_visit_pain</code>",
                                          "<span class=sup-lvl>j02</span>_D_regression_visit_pain</code>",
                                          "<span class=sup-lvl>t01</span>_D_reg_VisitLBP_1stPair</code>",
                                          "<span class=sup-lvl>r04</span>_D_reg_VisitLBP_1stPair_ols</code>",
                                          "<b>Not found</b>")]
        self.assertEqual(order, sorted(order))
        self.assertIn('data-run="b03j02t01r04"', tree)
        self.assertIn('class=sup-item data-item="E01" data-tab="citations"', tree)
        self.assertIn('title="E01-CITE-first-source · the first source">Ecite01</button>', tree)
        empty = evidence_space_html(self.page, card_url="/x")
        self.assertIn("Supporting Runs <span class=space-count>0</span>", empty)
        self.assertIn("No Supporting Runs declared on this page yet.", empty)

    def test_legacy_run_named_by_an_evidence_ticket_joins_that_item(self):
        """Empirical Strategy 260928: re-display-01 binds pj05t01r01, which drew the display;
        the evidence file names only re-display-01, so pj05t01r01 sat in "Other"."""
        tickets = self.page.parent / "runs" / "evidence-run"
        tickets.mkdir(parents=True)
        (tickets / "re-display-01_design.md").write_text(
            "run: re-display-01_design\nitem: E07-DISPLAY-design-flow\ntarget: C1.P1.B2\n"
            "legacy_run: pj05t01r01\n", encoding="utf-8")
        self.assertEqual(run_tabs(self.page)["pj05t01r01"],
                         {"tab": "displays", "item": "E07", "target": "C1.P1.B2"})

    def test_older_paper_runs_join_the_tab_of_the_item_they_serve(self):
        tabs = run_tabs(self.page)
        self.assertEqual(tabs["pj02t01r01"], {"tab": "citations", "item": "E01", "target": "C1.P1.B1"})
        self.assertEqual(tabs["pj02t04r01"]["tab"], "displays")

    def test_delivery_tabs_preview_the_built_file_and_list_artifacts(self):
        latex = self.page.parent / "delivery" / "latex"
        latex.mkdir(parents=True)
        (latex / "Sample.pdf").write_bytes(b"%PDF-1.4")
        (latex / "Sample.tex").write_text("x", encoding="utf-8")
        html = delivery_space_html(self.page, checks_url="/_board/delivery?workspace=1", path_q="",
                                   file_q="Sample.md", asset_base="")
        self.assertIn('data-src="/delivery/latex/Sample.pdf"', html)
        self.assertIn("<code>delivery/latex/</code><span class=space-hint>2 files", html)
        self.assertIn("No Word build yet", html)
        self.assertEqual(file_url("delivery/web/index.html", path_q="", file_q="x.md", asset_base=""),
                         "/delivery/web/index.html")


if __name__ == "__main__":
    unittest.main()
