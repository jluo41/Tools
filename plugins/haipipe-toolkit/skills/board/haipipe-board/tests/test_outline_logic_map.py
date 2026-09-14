"""A Page's Mermaid Structure leads the Draft Space."""
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from live.outline import _logic_map, _logic_svg, parse_outline, render


PAGE = """# S-test
page-type: section

## Content
### 1 · Introduction
Current prose.
"""

PLAN = """# S-test · outline v1.2
approved: ⬜

## C1 · Introduction
### C1.P1 · Phenomenon · S1 to S1
- B1 · [Phenomenon] Physician behavior varies.
  Evidence: none · planning fixture
"""

MAP = """%% Derived from S-test-outline-v1.2.md (unapproved working Shape).
%% Argument flow, not causal effects.
flowchart TD
    subgraph C1["C1 · Prescribing behavior"]
        direction TD
        P1["P1 · Prescribing behavior<br/>Variation and consequences"]
        P2["P2 · Agreeableness<br/>Clinical relevance"]
    end
    P1 -->|"Why might physicians differ?"| P2
    classDef default fill:transparent,stroke-width:0px;
"""


class OutlineLogicMapTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.page = Path(self.tmp.name) / "S-test.md"
        self.page.write_text(PAGE, encoding="utf-8")
        outline = self.page.parent / "outline"
        outline.mkdir()
        (outline / "S-test-outline-v1.2.md").write_text(PLAN, encoding="utf-8")
        self.logic = outline / "S-test-logic.mmd"

    def test_map_is_visible_before_plan_when_matching_mermaid_exists(self):
        self.logic.write_text(MAP, encoding="utf-8")
        body = render("S-test", parse_outline(PAGE), self.page)

        self.assertIn("Mermaid Structure", body)
        self.assertIn('aria-label="Mermaid"', body)
        self.assertEqual(body.count('class="logic-node"'), 2)
        self.assertEqual(body.count('class="logic-group"'), 1)
        self.assertIn("C1 · Prescribing behavior", body)
        self.assertIn("Why might physicians differ?", body)
        self.assertIn('<details class="card logic-card" aria-label="Mermaid">', body)
        self.assertIn('<summary class="logic-heading">', body)
        self.assertNotIn('<details class="card logic-card" aria-label="Mermaid" open>', body)
        self.assertLess(body.index("Mermaid Structure"), body.index("Physician behavior varies"))
        self.assertIn('class="card plan-card minimal-plan"', body)
        self.assertIn("S-test-logic.mmd", body)
        self.assertNotIn("flowchart TD", body)
        self.assertNotIn('aria-label="Diagram zoom controls"', body)
        self.assertNotIn("data-logic-zoom", body)
        self.assertNotIn("data-logic-fit", body)
        self.assertIn('class="logic-canvas"', body)
        self.assertNotIn("setupLogicZoom", body)

    def test_no_file_means_no_extra_workspace_panel(self):
        self.assertEqual(_logic_map(self.page), "")
        body = render("S-test", parse_outline(PAGE), self.page)
        self.assertNotIn("Mermaid Structure", body)

    def test_active_first_page_run_keeps_mermaid_collapsible(self):
        self.logic.write_text(MAP, encoding="utf-8")
        runtime = (self.page.parent / "results" /
                   "rp00_mermaid-structure" / "runtime.yaml")
        runtime.parent.mkdir(parents=True)
        for status in ("ready", "running", "waiting-for-feedback", "blocked"):
            with self.subTest(status=status):
                runtime.write_text("status: %s\n" % status, encoding="utf-8")
                body = render("S-test", parse_outline(PAGE), self.page)
                self.assertIn('<details class="card logic-card" aria-label="Mermaid">', body)
                self.assertNotIn('<details class="card logic-card" aria-label="Mermaid" open>', body)
                self.assertNotIn("rp00 open · review now", body)

    def test_completed_first_page_run_keeps_mermaid_collapsible(self):
        self.logic.write_text(MAP, encoding="utf-8")
        runtime = (self.page.parent / "results" /
                   "rp00_mermaid-structure" / "runtime.yaml")
        runtime.parent.mkdir(parents=True)
        runtime.write_text("status: complete\n", encoding="utf-8")

        body = render("S-test", parse_outline(PAGE), self.page)

        self.assertIn('<details class="card logic-card" aria-label="Mermaid">', body)
        self.assertNotIn('<details class="card logic-card" aria-label="Mermaid" open>', body)

    def test_noncanonical_structure_runtime_does_not_open_review_map(self):
        self.logic.write_text(MAP, encoding="utf-8")
        runtime = (self.page.parent / "results" /
                   "rp01_mermaid-structure" / "runtime.yaml")
        runtime.parent.mkdir(parents=True)
        runtime.write_text("status: waiting-for-feedback\n", encoding="utf-8")

        body = render("S-test", parse_outline(PAGE), self.page)

        self.assertIn('<details class="card logic-card" aria-label="Mermaid">', body)
        self.assertNotIn('<details class="card logic-card" aria-label="Mermaid" open>', body)
        self.assertNotIn("rp00 open · review now", body)

    def test_matching_png_does_not_replace_rendered_mermaid(self):
        self.logic.write_text(MAP, encoding="utf-8")
        self.logic.with_suffix(".png").write_bytes(b"\x89PNG\r\nfixture")

        body = _logic_map(self.page)

        self.assertIn('class="logic-viewport"', body)
        self.assertIn('class="logic-svg"', body)
        self.assertNotIn('class="logic-png"', body)
        self.assertNotIn("Download PNG", body)

    def test_svg_is_inside_bounded_viewport(self):
        self.logic.write_text(MAP, encoding="utf-8")
        body = _logic_map(self.page)
        self.assertIn('class="logic-viewport"', body)
        self.assertIn('<div class="logic-canvas"><svg class="logic-svg"', body)

    def test_malformed_mermaid_does_not_copy_raw_source_into_reader_space(self):
        self.logic.write_text("flowchart TD\nP1 --> P2\n", encoding="utf-8")
        body = _logic_map(self.page)
        self.assertIn("Mermaid preview unavailable", body)
        self.assertIn("S-test-logic.mmd", body)
        self.assertNotIn("P1 --&gt; P2", body)
        self.assertNotIn("flowchart TD", body)

    def test_svg_escapes_authored_labels(self):
        svg = _logic_svg('flowchart TD\nP1["<script>alert(1)</script>"]')
        self.assertNotIn("<script>", svg)
        self.assertIn("&lt;script&gt;", svg)


if __name__ == "__main__":
    unittest.main()
