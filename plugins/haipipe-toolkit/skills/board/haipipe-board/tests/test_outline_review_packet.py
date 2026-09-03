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
- **PageX Bindings**: []
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
            "# SM00 · feedback\n\n### R01 · Keep the clinical decision visible\n"
            "- **Status**: open\n",
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
        return page

    def test_packet_joins_shape_survey_feedback_and_content_map(self):
        with tempfile.TemporaryDirectory() as directory:
            page = self._page(directory)
            body = plan_card(page)
            for wanted in (
                "Review this Section", "Survey", "E01-VALUE-review-cohort-counts",
                "Supporting Runs", "PageX Bindings", "Local Run", "Decide",
                "Shape ↔ Content map",
                "Shape has 1 division; current Content has 2", "routed record",
            ):
                self.assertIn(wanted, body)
            self.assertIn("E1V.ReviewCohort", body)
            self.assertNotIn("📝 E1", body)
            start = body.index('<div id="typed-ev1" popover')
            card = body[start:body.index("</div></div>", start) + len("</div></div>")]
            self.assertIn("E01-VALUE-review-cohort-counts", card)
            for field in (
                "Target", "Expected", "Acceptance", "Supporting Runs",
                "PageX Bindings", "Local Input", "Local Run", "Result", "Decide",
            ):
                self.assertIn(field, card)

    def test_outline_owns_one_internal_evidence_workspace(self):
        with tempfile.TemporaryDirectory() as directory:
            page = self._page(directory)
            rendered = render(
                "SM00", parse_outline(page.read_text(encoding="utf-8")), page,
                path_q="/Board/board.md", file_q="MAIN/SM00-abstract/SM00-abstract.md",
            )
            self.assertIn("Bullet Workspace", rendered)
            self.assertIn("Evidence Workspace", rendered)
            self.assertIn("Plan Context", rendered)
            self.assertIn("Page Records", rendered)
            self.assertIn("/_board/evidence?path=/Board/board.md&amp;file=MAIN/SM00-abstract/SM00-abstract.md&amp;embed=1", rendered)
            self.assertNotIn("Evidence / Survey", rendered)
            self.assertIn("🗣 Feedback", rendered)
            self.assertIn("📏 Requirement", rendered)
            self.assertIn("Keep estimates and intervals together", rendered)


if __name__ == "__main__":
    unittest.main()
