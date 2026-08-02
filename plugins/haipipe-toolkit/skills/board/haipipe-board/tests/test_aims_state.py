import importlib.util
import unittest
from pathlib import Path

from src.common import aim_ids, aim_progress, sec
from src.page_question import render_question
from src.parse import parse_page


CANONICAL = """# Aim fixture
state: 🟡 PARTIAL
owner: CC

## Opening
What does this page intend, and what is true now?

## Content
### C1 · Contract
The contract is explicit.

## Aims
### C1 · Contract
- A1.1 · The contract is readable.
  **Done when:** A cold reader can explain it.
- A1.2 · The contract is traceable.
  **Done when:** Every rule has a source.

### P · Page-level
- P1 · The page is coherent.
  **Done when:** Every section agrees.

## States
### C1 · Contract
- ✅ A1.1 · Met by a cold read.
- 🟡 A1.2 · Active; sources are being linked.

### P · Page-level
- ⏸️ P1 · Held explicitly.
"""


class AimsStateTest(unittest.TestCase):
    def test_progress_is_derived_from_state(self):
        page = parse_page("QT1", CANONICAL)
        aims = sec(page["sec"], "Done when")
        state = sec(page["sec"], "Now")
        self.assertEqual(aim_ids(aims), ["A1.1", "A1.2", "P1"])
        self.assertEqual(
            aim_progress(aims, state),
            dict(mode="aims", total=3, met=1, hold=1, active=1,
                 waiting=0, open=0, closed=2,
                 ids=["A1.1", "A1.2", "P1"]),
        )

    def test_canonical_names_and_counts_render(self):
        html = render_question(parse_page("QT1", CANONICAL), None, None)
        self.assertIn("🎯 Aims", html)
        self.assertIn("📍 States", html)
        self.assertNotIn('>📍 State<', html)
        self.assertIn('<span class="cnt">2/3</span>', html)
        self.assertIn('<span class="shc">1/2</span>', html)

    def test_historical_headings_remain_compatible(self):
        legacy = (CANONICAL.replace("## Aims", "## Items to Finish")
                            .replace("## States", "## Where we are"))
        page = parse_page("QT2", legacy)
        self.assertTrue(sec(page["sec"], "Done when").startswith("### C1"))
        self.assertTrue(sec(page["sec"], "Now").startswith("### C1"))
        html = render_question(page, None, None)
        self.assertIn("🎯 Aims", html)
        self.assertIn("📍 States", html)

    def test_singular_state_heading_remains_a_legacy_alias(self):
        page = parse_page("QT3", CANONICAL.replace("## States", "## State"))
        self.assertTrue(sec(page["sec"], "Now").startswith("### C1"))
        self.assertIn("📍 States", render_question(page, None, None))

    def test_new_page_generators_emit_plural_states(self):
        root = Path(__file__).resolve().parent.parent  # the engine dir
        for rel in ("live/structure.py", "cli/stage.py", "cli/skillpage.py", "cli/meetingpage.py"):
            text = (root / rel).read_text(encoding="utf-8")
            self.assertIn("## States", text, rel)
            self.assertNotIn("## State\n", text, rel)

    def test_public_paper_generator_materializes_stage_specific_aims(self):
        root = Path(__file__).resolve().parent.parent  # the engine dir
        paper = root.parents[1] / "paper/1-lifecycle/haipipe-paper-stage"
        spec = importlib.util.spec_from_file_location(
            "paper_stage_create_page", paper / "create-page.py"
        )
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        display_template = paper / "stages/4-display/template.md"
        divisions = [name for name, _ in module.template_divisions(display_template)]
        self.assertIn("Q-consumer", divisions)
        self.assertEqual(
            module.consumer_q_id(
                "- P<n> · Q-Display<unit>-<n> · <title>",
                "Display",
                "4a",
                "main-effect",
            ),
            "Q-Display4a-1",
        )
        self.assertEqual(
            module.consumer_q_id(
                "- P<n> · Q-Sec<unit><Slug>-<n> · <title>",
                "Section Edit",
                "6",
                "main-results",
            ),
            "Q-Sec6MainResults-1",
        )
        seed_template = paper / "stages/0-seed/template.md"
        seed_aim = module.consumer_aim(
            module.board_template_aims(seed_template), "Q-Seed-1"
        )
        self.assertIn("- P1 · Q-Seed-1 · <question title>", seed_aim)
        self.assertNotIn("<what must be learned, using the consumer wording>", seed_aim)

    def test_active_paper_templates_teach_aims_and_states(self):
        root = Path(__file__).resolve().parent.parent  # the engine dir
        paper = root.parents[1] / "paper/1-lifecycle/haipipe-paper-stage"
        for path in (paper / "stages").glob("*/template.md"):
            text = path.read_text(encoding="utf-8")
            self.assertNotIn("## Items to Finish", text, path.as_posix())
            self.assertNotIn("## Where we are", text, path.as_posix())
            self.assertNotIn("- [ ] 🔎 Q-", text, path.as_posix())

    def test_legacy_checkbox_progress_is_not_reinterpreted(self):
        progress = aim_progress("- [x] verified\n- [ ] open", "")
        self.assertEqual(progress["mode"], "legacy")
        self.assertEqual((progress["closed"], progress["total"]), (1, 2))


if __name__ == "__main__":
    unittest.main()
