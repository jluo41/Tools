"""A Section's optional Mermaid argument map leads the Bullet Workspace."""
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

        self.assertIn("Section logic", body)
        self.assertIn('aria-label="Section argument map"', body)
        self.assertEqual(body.count('class="logic-node"'), 2)
        self.assertEqual(body.count('class="logic-group"'), 1)
        self.assertIn("C1 · Prescribing behavior", body)
        self.assertIn("Why might physicians differ?", body)
        self.assertIn('<details class="card logic-card">', body)
        self.assertIn('<summary class="logic-summary">', body)
        self.assertNotIn('<details class="card logic-card" open>', body)
        self.assertLess(body.index("Section logic"), body.index("plan v1.2"))
        self.assertIn("S-test-logic.mmd", body)
        self.assertIn("flowchart TD", body)

    def test_no_file_means_no_extra_workspace_panel(self):
        self.assertEqual(_logic_map(self.page), "")
        body = render("S-test", parse_outline(PAGE), self.page)
        self.assertNotIn("Section logic", body)

    def test_matching_png_is_preferred_and_downloadable(self):
        self.logic.write_text(MAP, encoding="utf-8")
        self.logic.with_suffix(".png").write_bytes(b"\x89PNG\r\nfixture")

        body = _logic_map(self.page)

        self.assertIn('class="logic-png"', body)
        self.assertIn("data:image/png;base64,", body)
        self.assertIn('download="S-test-logic.png"', body)
        self.assertIn("Download PNG", body)
        self.assertNotIn('class="logic-svg"', body)

    def test_malformed_mermaid_falls_back_to_escaped_source(self):
        self.logic.write_text("flowchart TD\nP1 --> P2\n", encoding="utf-8")
        body = _logic_map(self.page)
        self.assertIn("Mermaid source needs review", body)
        self.assertIn("no Mermaid node declarations", body)
        self.assertIn("P1 --&gt; P2", body)

    def test_svg_escapes_authored_labels(self):
        svg = _logic_svg('flowchart TD\nP1["<script>alert(1)</script>"]')
        self.assertNotIn("<script>", svg)
        self.assertIn("&lt;script&gt;", svg)


if __name__ == "__main__":
    unittest.main()
