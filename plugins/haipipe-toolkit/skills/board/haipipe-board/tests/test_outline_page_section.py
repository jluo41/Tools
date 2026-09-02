"""The Page-level Outline is one projection of the existing outline/ plan."""
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

ENGINE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ENGINE))

from src import body as board_body
from src.page_board import sidebar_rows
from src.page_question import render_question
from src.parse import parse_page


PAGE = """# Outline fixture
state: 🟡 PARTIAL
owner: JL

## Opening
Does the Page render one readable Outline surface without copying its plan?

## Outline

**Reader path**: orient before the drafted content.

```text
Opening -> Outline -> Content
```

## Content
### 1 · Product
The drafted material belongs here.
"""

PLAN = """# Outline fixture · outline v1
outline-version: v1
approved: ⬜
arc: The reader sees the planned move before reading its drafted realization.

## C1 · Product
### C1.P1 · Establish the product · S1 to S1
- B1 · State the page product
  Note: The sentence belongs in Content, not the plan.
  Evidence: E01-VALUE-product · one checked source for the page product
  Accept: the source and its local receipt are named.
"""

ITEMS = """# Outline fixture · evidence items
page: fixture

### E01-VALUE-product · C1.P1.B1 · checked product source
- **Expected**: VALUE · one checked source for the page product
- **Acceptance**: the source and its local receipt are named.
- **Supporting Runs**: Execution · reuse · b01j01t01r01
- **PageX Bindings**: []
- **Local Input**: aggregate result only.
- **Local Run**: Page · Evidence Item · reuse · b02j01t01r01
- **Decide**: ☐ make · ☐ defer · ☐ drop
"""


class OutlinePageSectionTest(unittest.TestCase):
    def test_outline_section_renders_current_plan_without_a_second_map(self):
        with TemporaryDirectory() as temp:
            root = Path(temp)
            source = root / "QA" / "QA1.md"
            source.parent.mkdir(parents=True)
            source.write_text(PAGE, encoding="utf-8")
            outline = source.parent / "outline"
            outline.mkdir()
            (outline / "QA1-outline-v1.md").write_text(PLAN, encoding="utf-8")
            (outline / "QA1-evidence-items.md").write_text(ITEMS, encoding="utf-8")

            prior_base = board_body.BASE
            board_body.BASE = root
            try:
                page = parse_page("QA1", PAGE, file="QA/QA1.md")
                html = render_question(page, None, None)
            finally:
                board_body.BASE = prior_base

        self.assertIn("🧭 Outline", html)
        self.assertIn("🚪 Opening", html)
        self.assertNotIn("🧭 Opening", html)
        self.assertIn("▤ Outline table", html)
        self.assertIn('<details class="outline-section" open>', html)
        self.assertIn("1 SHAPE", html)
        self.assertIn("2 SURVEY", html)
        self.assertIn("3 LAND", html)
        self.assertIn("4 EMBED", html)
        self.assertNotIn("OUTLINE cycles", html)
        self.assertNotIn("Item progress", html)
        self.assertNotIn("🗺 Narrative map", html)
        self.assertNotIn("Opening -&gt; Outline -&gt; Content", html)
        self.assertIn("Address</th>", html)
        self.assertIn("Planned move</th>", html)
        self.assertIn("Evidence</th>", html)
        self.assertIn("Supporting Runs</th>", html)
        self.assertIn("Local Run</th>", html)
        self.assertNotIn("Route</th>", html)
        self.assertNotIn("Status</th>", html)
        self.assertIn("State the page product", html)
        self.assertIn('aria-label="E01-VALUE-product · VALUE · checked product source"', html)
        self.assertIn("<b>E1V.CheckedProductSource</b>", html)
        self.assertIn('popovertarget="outline-item-E01-VALUE-product"', html)
        self.assertIn('id="outline-item-E01-VALUE-product" popover', html)
        for field in (
            "Name", "Target", "Expected", "Acceptance", "Supporting Runs",
            "PageX Bindings", "Local Input", "Local Run", "Result",
        ):
            self.assertIn(f"<b>{field}</b>", html)
        self.assertIn('href="../runs.html#run-b01j01t01r01"', html)
        self.assertIn("b01.j01.t01.r01", html)
        self.assertIn("b02.j01.t01.r01", html)
        self.assertIn("specified", html)
        self.assertNotIn("🖼 Diagram", html)

    def test_wall_abbreviates_all_three_evidence_types(self):
        cases = (
            ("CITE", "E02-CITE-guideline", "guideline source", "E2C.GuidelineSource"),
            ("DISPLAY", "E03-DISPLAY-forest", "association forest", "E3D.AssociationForest"),
        )
        for item_type, item_id, name, visible in cases:
            with self.subTest(item_type=item_type), TemporaryDirectory() as temp:
                root = Path(temp)
                source = root / "QA" / "QA1.md"
                source.parent.mkdir(parents=True)
                source.write_text(PAGE, encoding="utf-8")
                outline = source.parent / "outline"
                outline.mkdir()
                plan = PLAN.replace("E01-VALUE-product", item_id)
                items = ITEMS.replace("E01-VALUE-product", item_id)
                items = items.replace("checked product source", name)
                items = items.replace("**Expected**: VALUE ·", f"**Expected**: {item_type} ·")
                (outline / "QA1-outline-v1.md").write_text(plan, encoding="utf-8")
                (outline / "QA1-evidence-items.md").write_text(items, encoding="utf-8")

                prior_base = board_body.BASE
                board_body.BASE = root
                try:
                    page = parse_page("QA1", PAGE, file="QA/QA1.md")
                    html = render_question(page, None, None)
                finally:
                    board_body.BASE = prior_base

            self.assertIn(f"<b>{visible}</b>", html)
            self.assertIn(f'popovertarget="outline-item-{item_id}"', html)

    def test_legacy_diagram_source_does_not_render_a_second_outline(self):
        page = parse_page("QA2", PAGE.replace("## Outline", "## Diagram"))
        html = render_question(page, None, None)

        self.assertNotIn("🧭 Outline", html)
        self.assertNotIn("🗺 Narrative map", html)
        self.assertNotIn("Opening -&gt; Outline -&gt; Content", html)

    def test_plan_without_a_map_still_has_one_page_and_sidebar_outline(self):
        with TemporaryDirectory() as temp:
            root = Path(temp)
            source = root / "QB" / "QB3.md"
            source.parent.mkdir(parents=True)
            source.write_text(PAGE.replace(
                "## Outline\n\n**Reader path**: orient before the drafted content.\n\n"
                "```text\nOpening -> Outline -> Content\n```\n\n", ""),
                encoding="utf-8")
            outline = source.parent / "outline"
            outline.mkdir()
            (outline / "QB3-outline-v1.md").write_text(PLAN, encoding="utf-8")
            (outline / "QB3-evidence-items.md").write_text(ITEMS, encoding="utf-8")

            prior_base = board_body.BASE
            board_body.BASE = root
            try:
                page = parse_page("QB3", source.read_text(encoding="utf-8"),
                                  file="QB/QB3.md")
                html = render_question(page, None, None)
                sidebar = "".join(sidebar_rows([page]))
            finally:
                board_body.BASE = prior_base

        self.assertIn("🧭 Outline", html)
        self.assertIn("▤ Outline table", html)
        self.assertIn('<details class="outline-section" open>', html)
        self.assertIn("🧭 Outline", sidebar)
        self.assertIn("🚪 Opening", sidebar)
        self.assertNotIn("🧭 Opening", sidebar)
        self.assertIn("plan table", sidebar)

    def test_manuscript_section_opening_is_one_reader_paragraph(self):
        manuscript = """# Results fixture
state: 🟡 PARTIAL
owner: JL
page-type: section
section_kind: results

## Opening
What did the analysis show?
The reader sees the accepted result and its bounded meaning.

## Stage Contract
### Venue
Keep implementation notes off the reader surface.

## Content
### 1 · Result
The accepted result belongs here.
"""
        page = parse_page("S-Desk-Main-Results", manuscript)
        html = render_question(page, None, None)
        sidebar = "".join(sidebar_rows([page]))

        self.assertIn("🚪 Opening", html)
        self.assertIn("What did the analysis show?", html)
        self.assertIn("The reader sees the accepted result", html)
        self.assertNotIn("Writing Style", html)
        self.assertNotIn("Stage Contract", html)
        self.assertNotIn("Keep implementation notes off", html)
        self.assertNotIn('<details class="it row qd">', html)
        self.assertIn("one reader paragraph", sidebar)

    def test_narrative_opens_with_section_control_and_folds_plan(self):
        narrative_page = """# Narrative fixture
state: 🟡 PARTIAL
owner: JL
page-type: narrative

## Opening
How should this paper be told?

## Content
### 1 · Per-section outline
#### 1.1 · SM00 Abstract · Story04-v1

```text
QUESTION    What are the question and main result?
EXIT        Reader knows the design and bounded takeaway.
ESTABLISH   cohort; exposure; accepted main claim
REFUSE      causality; unaccepted subgroup claims
MOVES       question → design → result → meaning
GATE        accepted main receipt; otherwise retain placeholders
```

## Aims
### A1 · 📚 Per-section outline
- ⬜ A1.1 · The narrative table is inspectable.
  **Done when:** its row is projected from Content.
  **Now:** pending review.
"""
        with TemporaryDirectory() as temp:
            root = Path(temp)
            source = root / "NA" / "NA1.md"
            source.parent.mkdir(parents=True)
            source.write_text(narrative_page, encoding="utf-8")
            outline = source.parent / "outline"
            outline.mkdir()
            (outline / "NA1-outline-v1.md").write_text(PLAN, encoding="utf-8")
            (outline / "NA1-evidence-items.md").write_text(ITEMS, encoding="utf-8")

            prior_base = board_body.BASE
            board_body.BASE = root
            try:
                page = parse_page("NA1", narrative_page, file="NA/NA1.md")
                html = render_question(page, None, None)
            finally:
                board_body.BASE = prior_base

        self.assertIn("▤ Narrative section table", html)
        self.assertIn("Evidence gate / cut", html)
        self.assertIn("SM00 Abstract", html)
        self.assertIn("Runs boundary", html)
        self.assertIn('<details class="outline-plan-secondary">', html)
        self.assertLess(html.index("▤ Narrative section table"),
                        html.index("▤ Plan and evidence"))
        self.assertNotIn('<details class="outline-plan-secondary" open>', html)
        self.assertNotIn("🖼 Diagram", html)


if __name__ == "__main__":
    unittest.main()
