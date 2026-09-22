#!/usr/bin/env python3
"""The 🧭 plan card makes one Section-review packet from source records."""
import tempfile
import sys
import unittest
from pathlib import Path

ENGINE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ENGINE))

from live.outline import parse_outline, plan_card, render


PLAN = """# SM00 · outline v1
approved: ⬜

## C1 · Problem and positioning
### C1.P1 · The decision
- B1 · frame the physician decision problem
  Note: name the clinical choice before the trait signal
  Evidence: E01-VALUE-review-cohort-counts · scored physicians and reviews
  Accept: counts recompute from the frozen local Result
"""

ITEMS = """# SM00 · evidence items
page: SM00
kind: evidence-items · authored
plan: v1

### E01-VALUE-review-cohort-counts · C1.P1.B1 · review cohort counts
- **Target**: C1.P1.B1
- **Need**: the cohort counts named in the abstract
- **Expected**: VALUE · scored physicians and reviews
- **Acceptance**: counts recompute from the frozen local Result
- **Supporting Runs**: Execution · new-block · MISQ-evidence-bridge
- **Local Input**: Supporting Results only
- **Local Run**: Page · Evidence Item · new-block · MISQ-evidence-bridge → _pending/SM00/E01/result.md
- **Decide**: ☐ make / defer / drop
"""


class OutlineReviewPacketTest(unittest.TestCase):
    def _page(self, root):
        page_dir = Path(root) / "SM00-abstract"
        outline = page_dir / "outline"
        outline.mkdir(parents=True)
        page = page_dir / "SM00-abstract.md"
        page.write_text(
            "# SM00 · Abstract\n\n## Opening\nWhat must this abstract establish?\n\n"
            "## Content\n### 1 · Different heading on purpose\nA current sentence.\n"
            "### 2 · Extra current section\nAnother current sentence.\n\n"
            "## Aims\n- A1.1 · Review the shape.\n\n## States\n- ⬜ A1.1 · Waiting.\n",
            encoding="utf-8",
        )
        (outline / "SM00-abstract-outline-v1.md").write_text(PLAN, encoding="utf-8")
        (outline / "SM00-abstract-evidence-items.md").write_text(ITEMS, encoding="utf-8")
        (outline / "SM00-abstract-feedback.md").write_text(
            "# SM00 · feedback\npage: SM00-abstract\n"
            "kind: feedback · generated\nstatus: 1 of 1 open · 0 landed · 1 round(s)\n\n"
            "The Round's own words, copied. To argue, open a thread.\n\n"
            "## RD01 · MISQ feedback cycle\n"
            "**🔴 rewrite** · Reviewer · [source.md](source.md)\n\n"
            "**Ask** · Keep the clinical decision visible.\n\n"
            "**Order** · problem → evidence → contribution.\n\n"
            "**Gate** · Use a checked value.\n\n"
            "### S0-PP1 · Reposition the opening\n"
            "- **From**: R01\n"
            "- **Feedback**: Begin with the physician decision problem.\n"
            "- **Work**: Rewrite the opening sentence.\n"
            "- **State**: open\n"
            "- **Landed**: —\n"
            "  ↳ R01 · routes SM00-abstract\n",
            encoding="utf-8",
        )
        (outline / "SM00-abstract-evidence.md").write_text(
            "# SM00 · evidence\n\n### E01 · review cohort counts\n"
            "- **Status**: specified\n",
            encoding="utf-8",
        )
        (outline / "SM00-abstract-requirement.md").write_text(
            "# SM00 · requirement\npage: SM00-abstract\n"
            "kind: requirement · generated venue + authored page writing\n\n"
            "# --- requirement:begin (generated) ---\n"
            "REQUIREMENT, MEASURED 260902 1200. GENERATED; do not hand-edit.\n"
            "# --- requirement:end ---\n\n"
            "# --- writing:begin (authored) ---\n"
            "### W1 · Keep estimates and intervals together\n"
            "- **Rule**: Report each estimate with its 95% confidence interval.\n"
            "- **Applies**: Results sentences.\n"
            "- **Source**: Section reporting contract.\n"
            "# --- writing:end ---\n",
            encoding="utf-8",
        )
        (outline / "SM00-abstract-log.md").write_text(
            "# SM00 · log\n\n### 260903 1200 · Outline grouped\n",
            encoding="utf-8",
        )
        skill = outline / "skill"
        skill.mkdir()
        (skill / "SM00-abstract.md").write_text(
            "# skill map · SM00-abstract\n\n- haipipe-page-structure\n",
            encoding="utf-8",
        )
        (skill / "SM00-abstract-skill.html").write_text(
            "<!doctype html><title>Skills</title>", encoding="utf-8"
        )
        return page

    def test_plan_header_is_compact_and_shows_the_four_outline_cycles(self):
        with tempfile.TemporaryDirectory() as directory:
            page = self._page(directory)
            body = plan_card(page)
            for wanted in (
                "✍️ plan v1", "approved: ⬜", "1 evidence item · Decisions 0/1",
                "1</b> SHAPE", "2</b> SURVEY", "3</b> LAND", "4</b> EMBED",
            ):
                self.assertIn(wanted, body)
            self.assertNotIn("PageX Bindings", body)
            for retired in ("Review this Section", "Shape ↔ Content map",
                            "Shape/content mismatch", "waiting on a person",
                            "routed record", "① <b>Shape</b>"):
                self.assertNotIn(retired, body)
            self.assertIn("Bullet", body)
            self.assertIn("Draft", body)
            # Draft keeps a compact, read-only route/card in the Bullet
            # column; the complete Evidence item still belongs to Evidence
            # Space.
            self.assertIn("E01-VALUE-review-cohort-counts", body)
            self.assertIn("E1V.ReviewCohort", body)
            self.assertIn('class=point-evidence', body)
            self.assertNotIn('class=point-evidence-label', body)
            self.assertNotIn('<div class=point-evidence', body)
            self.assertIn(
                '<span class=point-statement>frame the physician decision problem</span>'
                '<span class=point-evidence',
                body,
            )
            self.assertIn('class="evchip warn typed-ev"', body)
            self.assertIn('data-outline-lens="evidence"', body)
            self.assertIn('<span class=point-label>[Point]</span>', body)
            self.assertNotIn('<b>Target</b>', body)
            self.assertNotIn('<b>Supporting Runs</b>', body)
            for field in ("Target", "Expected", "Acceptance", "Supporting Runs",
                          "Local Input", "Local Run", "Result", "Decide"):
                self.assertNotIn("<b>%s</b>" % field, body)

    def test_source_free_evidence_decision_is_not_a_visible_draft_block(self):
        with tempfile.TemporaryDirectory() as directory:
            page = self._page(directory)
            outline = page.parent / "outline"
            (outline / "SM00-abstract-outline-v1.md").write_text(
                PLAN.replace(
                    "Evidence: E01-VALUE-review-cohort-counts · scored physicians and reviews",
                    "Evidence: none · this waypoint is conceptual and needs no source",
                ),
                encoding="utf-8",
            )
            (outline / "SM00-abstract-evidence-items.md").write_text(
                "# SM00 · evidence items\npage: SM00\nkind: evidence-items · authored\n",
                encoding="utf-8",
            )
            body = plan_card(page)
            self.assertIn('data-evidence-state="none"', body)
            self.assertIn('data-evidence-reason="this waypoint is conceptual and needs no source"', body)
            self.assertNotIn("evidence: none", body)
            self.assertNotIn('class=point-evidence-label', body)

    def test_outline_owns_one_internal_evidence_workspace(self):
        with tempfile.TemporaryDirectory() as directory:
            page = self._page(directory)
            rendered = render(
                "SM00", parse_outline(page.read_text(encoding="utf-8")), page,
                root=directory,
                path_q="/Board/board.md", file_q="MAIN/SM00-abstract/SM00-abstract.md",
            )
            self.assertIn("Draft Space", rendered)
            self.assertIn("Evidence Space", rendered)
            self.assertIn("Run Space", rendered)
            self.assertNotIn("Context Workspace", rendered)
            self.assertNotIn("Plan Context", rendered)
            self.assertNotIn("Page Records", rendered)
            self.assertIn("/_board/evidence?path=/Board/board.md&amp;file=MAIN/SM00-abstract/SM00-abstract.md&amp;embed=1", rendered)
            self.assertIn("/_board/runs?path=/Board/board.md&amp;file=MAIN/SM00-abstract/SM00-abstract.md&amp;embed=1", rendered)
            self.assertIn("requestedFocus=params.get('focus')||''", rendered)
            self.assertIn("requestedRun=params.get('run')||''", rendered)
            self.assertIn("requestedSeg=params.get('seg')||''", rendered)
            self.assertIn("function workspaceSource(frame,name)", rendered)
            # Draft exposes only the compact Evidence route; the dedicated
            # Evidence Space owns the full item readout.
            self.assertIn("E01-VALUE-review-cohort-counts", rendered)
            self.assertIn('class=point-evidence', rendered)
            self.assertIn('class="evchip warn typed-ev"', rendered)
            self.assertIn('<span class=point-label>[Point]</span>', rendered)
            self.assertNotIn('<b>Target</b>', rendered)
            self.assertIn("ev.target.closest('a[data-outline-focus]')", rendered)
            self.assertIn("function focusRecord(id)", rendered)
            self.assertIn("/^C\\d+\\.P\\d+\\.B\\d+$/.test(id)", rendered)
            self.assertIn('id="bullet-C1-P1-B1" class=point-group data-point="C1.P1.B1"', rendered)
            self.assertIn(
                'href="/_board/outline?path=/Board/board.md&amp;file=MAIN/SM00-abstract/'
                'SM00-abstract.md&amp;lens=div&amp;focus=C1.P1.B1" '
                'data-outline-lens="div" data-outline-focus="C1.P1.B1"',
                rendered,
            )
            self.assertIn("history.replaceState(null,'',u.href);", rendered)
            self.assertIn(
                "if(requested==='workspace')requested=(requestedSeg==='runs'||requestedRun)?'run':'evidence';",
                rendered)
            self.assertIn("if(requestedFocus)src+=(src.indexOf('?')<0?'?':'&')+'focus='", rendered)
            self.assertNotIn("(requestedRun?'runs':'items')+'&focus='", rendered)
            self.assertNotIn("board-outline-evidence-focus", rendered)
            self.assertNotIn("board-outline-evidence-run", rendered)
            self.assertNotIn("Evidence / Survey", rendered)
            for offstage in ("🛠 Skills", "🗣 Feedback", "📏 Requirement",
                             "Main ask", "Order, gate &amp; source"):
                self.assertNotIn(offstage, rendered)


if __name__ == "__main__":
    unittest.main()
