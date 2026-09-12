"""Outline Bullet groups and writes stay Markdown-authoritative."""
import sys
import tempfile
import unittest
from pathlib import Path

ENGINE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ENGINE))

from live.outline import _edit_plan_bullet, parse_outline, plan_card, render
from src.plan_shape import iter_plan_bullets, plan_addresses, presentation_point


PAGE = """# S-page

## Opening
What should this page establish?

## Content
### 1 · Introduction
The page content.
"""

PLAN = """# S-page · outline v1.1
outline-version: v1.1
approved: ✅ JL 260908
shape-accepted: ✅
status: CONTENT · approved

## C1 · Introduction
### C1.P1 · Establish the point · S1 to S1
- B1 · S1 · State the point
  Note: keep the rationale with the Bullet.
  Evidence: none · page-owned statement
"""


class OutlineBulletEditingTest(unittest.TestCase):
    def _page(self, root):
        page = Path(root) / "Board" / "S-page"
        page.mkdir(parents=True)
        source = page / "S-page.md"
        source.write_text(PAGE, encoding="utf-8")
        outline = page / "outline"
        outline.mkdir()
        (outline / "S-page-outline-v1.1.md").write_text(PLAN, encoding="utf-8")
        (outline / "S-page-log.md").write_text("# log\n", encoding="utf-8")
        return source

    def test_paragraph_summary_contains_only_its_bullets_and_editor(self):
        with tempfile.TemporaryDirectory() as directory:
            page = self._page(directory)
            card = plan_card(
                page, root=directory, path_q="/Board/board.md",
                file_q="S-page/S-page.md",
            )
            start = card.index('data-paragraph="C1.P1"')
            end = card.index("</details>", card.index('data-paragraph-reading', start))
            inside = card[start:end]
            self.assertIn("C1.P1.B1", inside)
            self.assertIn('data-bullet-edit="edit-bullet-C1-P1-B1"', inside)
            self.assertIn("Save Bullet", inside)
            self.assertIn("Read paragraph", inside)
            self.assertNotIn("+ Bullet", card)
            self.assertNotIn('data-bullet-add=', card)
            self.assertNotIn('value="append-bullet"', card)
            self.assertNotIn("Planned move", card)

    def test_first_write_copies_approved_shape_then_reuses_working_version(self):
        with tempfile.TemporaryDirectory() as directory:
            page = self._page(directory)
            approved = page.parent / "outline" / "S-page-outline-v1.1.md"
            approved_bytes = approved.read_bytes()
            result, err = _edit_plan_bullet(
                page, "edit-bullet", "C9.P9", "B1", "would not be written"
            )
            self.assertIsNone(result)
            self.assertIsNotNone(err)
            self.assertFalse((approved.parent / "S-page-outline-v1.2.md").exists())

            result, err = _edit_plan_bullet(
                page, "edit-bullet", "C1.P1", "B1", "S1 · State the revised point"
            )
            self.assertIsNone(err)
            self.assertEqual(result["version"], "v1.2")
            self.assertTrue(result["created_working_shape"])
            working = approved.parent / "S-page-outline-v1.2.md"
            self.assertEqual(approved.read_bytes(), approved_bytes)
            self.assertTrue(working.exists())
            working_text = working.read_text(encoding="utf-8")
            self.assertIn("outline-version: v1.2", working_text)
            self.assertIn("approved: ⬜", working_text)
            self.assertIn("working-copy-of: v1.1", working_text)
            self.assertIn("S1 · State the revised point", working_text)
            self.assertIn("Note: keep the rationale", working_text)

            result, err = _edit_plan_bullet(
                page, "append-bullet", "C1.P1", "", "A new point",
                "the added point has a bounded job", "none · page-owned point",
            )
            self.assertIsNone(err)
            self.assertEqual(result["version"], "v1.2")
            self.assertFalse(result["created_working_shape"])
            working_text = working.read_text(encoding="utf-8")
            self.assertIn("- B2 · S2 · A new point", working_text)
            self.assertIn("Note: the added point has a bounded job", working_text)
            self.assertIn("Evidence: none · page-owned point", working_text)
            self.assertFalse((approved.parent / "S-page-outline-v1.3.md").exists())
            self.assertEqual(approved.read_bytes(), approved_bytes)

    def test_working_shape_renders_after_write(self):
        with tempfile.TemporaryDirectory() as directory:
            page = self._page(directory)
            _edit_plan_bullet(
                page, "append-bullet", "C1.P1", "", "Another point",
                "the point's local rationale", "none · page-owned point",
            )
            plan = page.parent / "outline" / "S-page-outline-v1.2.md"
            rendered = render("S-page", parse_outline(plan.read_text()), page,
                              root=directory, path_q="/Board/board.md",
                              file_q="S-page/S-page.md")
            self.assertIn("✍️ plan v1.2", rendered)
            self.assertIn("approved: ⬜", rendered)
            self.assertIn("Another point", rendered)

    def test_logic_map_renders_at_top_of_bullet_workspace(self):
        logic = """%% Derived from S-page-outline-v1.1.md.
flowchart TD
    P1[\"P1 · First move<br/>Clinical problem\"]
    P2[\"P2 · Second move<br/>Study question\"]
    P1 -->|\"What follows?\"| P2
    classDef default fill:transparent,stroke-width:0px;
        """
        with tempfile.TemporaryDirectory() as directory:
            page = self._page(directory)
            (page.parent / "outline" / "S-page-logic.mmd").write_text(
                logic, encoding="utf-8"
            )
            plan = page.parent / "outline" / "S-page-outline-v1.1.md"
            rendered = render(
                "S-page", parse_outline(plan.read_text(encoding="utf-8")), page,
                root=directory, path_q="/Board/board.md", file_q="S-page/S-page.md",
            )

        self.assertEqual(rendered.count('class="card logic-card"'), 1)
        self.assertLess(rendered.index('class="card logic-card"'),
                        rendered.index('class="card plan-card"'))
        self.assertIn('class="logic-svg"', rendered)
        self.assertIn("Clinical problem", rendered)
        self.assertIn("What follows?", rendered)
        self.assertIn("Mermaid source", rendered)
        self.assertIn("flowchart TD", rendered)

    def test_point_form_renders_role_statement_annotations_and_transition(self):
        point_plan = PLAN.replace(
            "- B1 · S1 · State the point\n  Note: keep the rationale with the Bullet.",
            "- B1 · [Phenomenon] Physician behavior varies within settings.\n"
            "  Note: settings = clinical decision contexts\n"
            "  Note: focus = comparable situations\n"
            "  Transition: illustration: general pattern → specific example",
        )
        with tempfile.TemporaryDirectory() as directory:
            page = self._page(directory)
            (page.parent / "outline" / "S-page-outline-v1.1.md").write_text(
                point_plan, encoding="utf-8"
            )
            card = plan_card(page, root=directory, path_q="/Board/board.md",
                             file_q="S-page/S-page.md")
        self.assertIn("[1 · Phenomenon]", card)
        self.assertIn("Physician behavior varies within settings.", card)
        self.assertIn("<li>settings = clinical decision contexts</li>", card)
        self.assertIn("<li>focus = comparable situations</li>", card)
        self.assertIn("→ <span>[illustration: general pattern → specific example]</span>", card)
        self.assertNotIn("Core statement:", card)
        self.assertNotIn("Note:", card)

    def test_point_parser_keeps_transition_out_of_annotation_list(self):
        point = presentation_point(
            "[1 · Example] For example, prescribing choices differ.",
            ["- transition opening: For example", "Transition: contrast: general → specific"],
            1,
        )
        self.assertEqual(point["role"], "Example")
        self.assertEqual(point["number"], 1)
        self.assertEqual(point["annotations"], ["transition opening: For example"])
        self.assertEqual(point["transition"], "contrast: general → specific")

    def test_live_point_form_keeps_lowercase_dash_annotation_separate(self):
        # The live compatibility join uses a private sentinel for indented
        # phrase-only annotations.  Exercise the whole card path so a lower-
        # case dash cannot silently merge into the Point statement again.
        point_plan = PLAN.replace(
            "- B1 · S1 · State the point\n  Note: keep the rationale with the Bullet.",
            "- B1 · [Phenomenon] Physician behavior varies within settings.\n"
            "  Annotation: compare physicians facing comparable situations\n"
            "  - use comparable clinical cases\n",
        )
        with tempfile.TemporaryDirectory() as directory:
            page = self._page(directory)
            (page.parent / "outline" / "S-page-outline-v1.1.md").write_text(
                point_plan, encoding="utf-8"
            )
            card = plan_card(page, root=directory, path_q="/Board/board.md",
                             file_q="S-page/S-page.md")
        self.assertIn("<li>compare physicians facing comparable situations</li>", card)
        self.assertIn("<li>use comparable clinical cases</li>", card)
        self.assertNotIn("<li>use comparable clinical cases Evidence:", card)
        self.assertNotIn("situations - use comparable", card)

    def test_plan_bullet_iterator_preserves_explicit_identity_with_indented_dash(self):
        blocks = iter_plan_bullets(
            "## C1 · Intro\n"
            "### C1.P1 · Move\n"
            "- B4 · [Example] For example, choices differ.\n"
            "  - comparable cases only\n"
            "  Evidence: none · rhetorical point\n"
        )
        self.assertEqual(blocks[0]["address"], "C1.P1.B4")
        self.assertEqual(blocks[0]["point"]["annotations"], ["comparable cases only"])
        self.assertEqual(plan_addresses(
            "## C1 · Intro\n### C1.P1 · Move\n"
            "- B4 · [Example] For example, choices differ.\n"
        ), {"C1.P1.B4"})


if __name__ == "__main__":
    unittest.main()


PLAN_NUMBERED = """# S-page · outline v0.3
outline-version: v0.3
approved: ⬜

## C1 · Introduction
### C1.P1 · Establish the point · S1 to S3
- B1 · S1 · State the point
  Note: first.
- B2 · S2 · Support the point
  Note: second.
  Evidence: none · page-owned statement
- B3 · S3 · Close the point

### C1.P2 · Second move · S4 to S4
- B1 · S4 · Open the second move
"""


class OutlineBulletEditorEdgesTest(unittest.TestCase):
    """The editor addresses the Bullet the file names and keeps the file's layout."""

    def _page(self, root, plan=PLAN_NUMBERED, name="S-page-outline-v0.3.md"):
        page = Path(root) / "Board" / "S-page"
        page.mkdir(parents=True)
        source = page / "S-page.md"
        source.write_text(PAGE, encoding="utf-8")
        (page / "outline").mkdir()
        (page / "outline" / name).write_text(plan, encoding="utf-8")
        return source

    def test_unapproved_shape_is_edited_in_place_and_ids_follow_the_file(self):
        with tempfile.TemporaryDirectory() as directory:
            page = self._page(directory)
            plan = page.parent / "outline" / "S-page-outline-v0.3.md"
            result, err = _edit_plan_bullet(page, "edit-bullet", "C1.P1", "B2", "Support it better")
            self.assertIsNone(err)
            self.assertEqual(result["version"], "v0.3")
            self.assertFalse(result["created_working_shape"])
            text = plan.read_text(encoding="utf-8")
            # the S-slot survives when the editor omits it; neighbours untouched
            self.assertIn("- B2 · S2 · Support it better\n  Note: second.", text)
            self.assertIn("- B1 · S1 · State the point", text)
            self.assertIn("- B3 · S3 · Close the point", text)
            self.assertIn("- B1 · S4 · Open the second move", text)
            self.assertEqual(sorted(p.name for p in plan.parent.glob("*outline-v*")),
                             ["S-page-outline-v0.3.md"])

    def test_append_lands_after_the_last_bullet_block_without_a_blank_line(self):
        with tempfile.TemporaryDirectory() as directory:
            page = self._page(directory)
            plan = page.parent / "outline" / "S-page-outline-v0.3.md"
            result, err = _edit_plan_bullet(page, "append-bullet", "C1.P1", "", "S9 · Extend the point")
            self.assertIsNone(err)
            self.assertEqual(result["bullet"], "B4")
            text = plan.read_text(encoding="utf-8")
            # numbering continues from the file's own B/S counters, the typed
            # S-slot is replaced by the allocated one, no blank line is minted
            self.assertIn("- B3 · S3 · Close the point\n- B4 · S4 · Extend the point\n\n### C1.P2", text)
            result, err = _edit_plan_bullet(page, "append-bullet", "C1.P2", "", "Another")
            self.assertIsNone(err)
            self.assertIn("- B1 · S4 · Open the second move\n- B2 · S5 · Another\n", plan.read_text(encoding="utf-8"))

    def test_refusals_never_touch_the_plan(self):
        with tempfile.TemporaryDirectory() as directory:
            page = self._page(directory)
            plan = page.parent / "outline" / "S-page-outline-v0.3.md"
            before = plan.read_bytes()
            for action, paragraph, bullet, head in (
                ("edit-bullet", "C1.P1", "B9", "missing bullet"),
                ("edit-bullet", "C1.P1", "B1", "   "),
                ("edit-bullet", "P1", "B1", "bad address"),
                ("delete-bullet", "C1.P1", "B1", "no such action"),
            ):
                result, err = _edit_plan_bullet(page, action, paragraph, bullet, head)
                self.assertIsNone(result, (action, paragraph, bullet))
                self.assertTrue(err)
            self.assertEqual(plan.read_bytes(), before)

    def test_plan_card_ids_follow_explicit_bullet_numbers(self):
        with tempfile.TemporaryDirectory() as directory:
            page = self._page(directory)
            card = plan_card(page, root=directory, path_q="/Board/board.md",
                             file_q="S-page/S-page.md")
            for wanted in ('data-bullet-edit="edit-bullet-C1-P1-B1"',
                           'data-bullet-edit="edit-bullet-C1-P1-B3"',
                           'data-bullet-edit="edit-bullet-C1-P2-B1"'):
                self.assertIn(wanted, card)
            self.assertEqual(card.count('<details class="paragraph-group" open'), 2)
            # the hidden fields carry the route the server resolves
            self.assertIn('<input type="hidden" name="path" value="/Board/board.md">', card)
            self.assertIn('<input type="hidden" name="action" value="edit-bullet">', card)
            self.assertEqual(card.count('<summary>Read paragraph</summary>'), 2)
            self.assertNotIn('value="append-bullet"', card)

    def test_live_tab_carries_the_editor_script_and_the_post_route(self):
        with tempfile.TemporaryDirectory() as directory:
            page = self._page(directory)
            plan = page.parent / "outline" / "S-page-outline-v0.3.md"
            rendered = render("S-page", parse_outline(plan.read_text()), page,
                              root=directory, path_q="/Board/board.md",
                              file_q="S-page/S-page.md")
            self.assertIn("form[data-bullet-write]", rendered)
            self.assertIn("fetch('/_board/outline',{method:'POST'", rendered)
            self.assertIn("location.reload()", rendered)
            self.assertIn("details.paragraph-group>summary", rendered)

    def test_post_route_writes_only_for_explicit_bullet_actions(self):
        from live.outline import OutlineMixin
        with tempfile.TemporaryDirectory() as directory:
            page = self._page(directory)

            class Surface(OutlineMixin):
                def target(_self, payload):
                    return page, page.parent.parent

            result, err = Surface().plug_outline({"path": "/Board/board.md", "file": "S-page/S-page.md"})
            self.assertIsNone(err)
            self.assertEqual(result, {"url": "/_board/outline?path=/Board/board.md&file=S-page/S-page.md"})
            result, err = Surface().plug_outline({
                "path": "/Board/board.md", "file": "S-page/S-page.md",
                "action": "edit-bullet", "paragraph": "C1.P2", "bullet": "B1",
                "head": "Open the second move, revised",
            })
            self.assertIsNone(err)
            self.assertEqual(result["version"], "v0.3")
            self.assertIn("- B1 · S4 · Open the second move, revised",
                          (page.parent / "outline" / "S-page-outline-v0.3.md").read_text(encoding="utf-8"))

    def test_post_route_keeps_structured_append_contract(self):
        from live.outline import OutlineMixin
        with tempfile.TemporaryDirectory() as directory:
            page = self._page(directory)
            plan = page.parent / "outline" / "S-page-outline-v0.3.md"

            class Surface(OutlineMixin):
                def target(_self, payload):
                    return page, page.parent.parent

            before = plan.read_bytes()
            result, err = Surface().plug_outline({
                "path": "/Board/board.md", "file": "S-page/S-page.md",
                "action": "append-bullet", "paragraph": "C1.P1", "head": "Missing details",
                "structured": "1",
            })
            self.assertIsNone(result)
            self.assertIn("Note", err)
            self.assertEqual(plan.read_bytes(), before)

            result, err = Surface().plug_outline({
                "path": "/Board/board.md", "file": "S-page/S-page.md",
                "action": "append-bullet", "paragraph": "C1.P1", "head": "A routed point",
                "note": "A bounded rationale", "evidence": "none · page-owned",
                "structured": "1",
            })
            self.assertIsNone(err)
            self.assertEqual(result["bullet"], "B4")
            text = plan.read_text(encoding="utf-8")
            self.assertIn("- B4 · S4 · A routed point\n  Note: A bounded rationale\n  Evidence: none · page-owned", text)
