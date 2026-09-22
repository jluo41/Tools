"""The Page's Structure leads the Draft Space as plain text you can click into and edit."""
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from live.outline import _structure_map, parse_outline, render, OutlineMixin
from live.outline_structure import save_structure, structure_rows, structure_text


PAGE = """# S-test
page-type: section

## Content
### 1 · Introduction
Current prose.
"""

PLAN = """# S-test · outline v1.2
approved: ⬜

## C1 · Prescribing behavior
### C1.P1 · Variation and consequences · S1 to S2
- B1 · [Phenomenon] Physician behavior varies.
  Draft: Physicians vary.
  Evidence: none · planning fixture
- B2 · [Consequence] It matters.
### C1.P2 · Empty paragraph
## C2 · Agreeableness
### C2.P1 · Clinical relevance
- B1 · [Point] Agreeable physicians prescribe differently.

## Aims
- A1 · not a division
"""

TEXT = """C1 · Prescribing behavior
  C1.P1 · Variation and consequences
  C1.P2 · Empty paragraph
C2 · Agreeableness
  C2.P1 · Clinical relevance"""


class StructureTextTest(unittest.TestCase):
    def test_rows_follow_the_outline_and_stop_at_the_first_other_heading(self):
        rows = structure_rows(PLAN)
        self.assertEqual([r["address"] for r in rows], ["C1", "C2"])
        first = rows[0]["paragraphs"][0]
        self.assertEqual((first["address"], first["index"], first["title"], first["bullets"], first["drafted"]),
                         ("C1.P1", "P01", "Variation and consequences", 2, 1))
        self.assertEqual(rows[1]["paragraphs"][0]["index"], "P03")

    def test_text_is_one_line_per_heading_without_the_span_suffix(self):
        self.assertEqual(structure_text(PLAN), TEXT)
        self.assertEqual(structure_text("# no divisions\n## Aims\n- A1\n"), "")


class StructureCardTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.page = Path(self.tmp.name) / "S-test.md"
        self.page.write_text(PAGE, encoding="utf-8")
        self.outline = self.page.parent / "outline"
        self.outline.mkdir()
        self.plan = self.outline / "S-test-outline-v1.2.md"

    def test_card_is_plain_text_with_a_box_behind_it(self):
        self.plan.write_text(PLAN, encoding="utf-8")
        body = render("S-test", parse_outline(PAGE), self.page, path_q="/Board/board.md", file_q="S-test.md")
        self.assertIn('<details class="card structure-card" open aria-label="Structure">', body)
        self.assertIn('<pre class="structure-text" data-structure-edit tabindex="0">%s</pre>' % TEXT, body)
        self.assertIn('<form class="structure-form" hidden data-path="/Board/board.md" data-file="S-test.md"', body)
        self.assertIn('<textarea name="text" class="structure-box"', body)
        self.assertIn("window.__structureEdit", body)
        self.assertIn("addEventListener('beforeunload'", body)
        self.assertIn("S-test-outline-v1.2.md", body)
        self.assertLess(body.index('class="card structure-card"'), body.index("Physician behavior varies"))
        self.assertIn(">⧉ run-structure<", body)
        for absent in ("Mermaid", "flowchart", "structure-list", "structure-index"):
            self.assertNotIn(absent, body)

    def test_read_only_host_shows_the_text_without_a_box(self):
        self.plan.write_text(PLAN, encoding="utf-8")
        body = render("S-test", parse_outline(PAGE), self.page, read_only=True)
        self.assertIn('<pre class="structure-text">%s</pre>' % TEXT, body)
        self.assertNotIn('<form class="structure-form"', body)
        self.assertNotIn("window.__structureEdit", body)

    def test_no_outline_means_only_the_run_structure_button(self):
        top = _structure_map(self.page)
        self.assertIn(">⧉ run-structure<", top)
        self.assertNotIn("structure-card", top)
        body = render("S-test", parse_outline(PAGE), self.page)
        self.assertNotIn('<details class="card structure-card"', body)

    def test_a_stray_mmd_file_is_ignored(self):
        self.plan.write_text(PLAN, encoding="utf-8")
        (self.outline / "S-test-logic.mmd").write_text("flowchart TD\nA-->B\n", encoding="utf-8")
        body = render("S-test", parse_outline(PAGE), self.page)
        self.assertNotIn("logic.mmd", body)


class SaveStructureTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.page = Path(self.tmp.name) / "S-test.md"
        self.page.write_text(PAGE, encoding="utf-8")
        outline = self.page.parent / "outline"
        outline.mkdir()
        self.plan = outline / "S-test-outline-v1.2.md"
        self.plan.write_text(PLAN, encoding="utf-8")
        self.log = outline / "S-test-log.md"
        self.log.write_text("# log\n", encoding="utf-8")

    def save(self, text, **extra):
        return save_structure(self.page, {"text": text, **extra})

    def test_rename_keeps_every_body_line_and_logs_it(self):
        result, err = self.save(TEXT.replace("Variation and consequences", "Why prescribing varies")
                                    .replace("C2 · Agreeableness", "C2 · Agreeableness matters"))
        self.assertIsNone(err, err)
        self.assertTrue(result["changed"])
        plan = self.plan.read_text(encoding="utf-8")
        self.assertIn("### C1.P1 · Why prescribing varies\n- B1 · [Phenomenon] Physician behavior varies.\n  Draft: Physicians vary.\n", plan)
        self.assertIn("## C2 · Agreeableness matters\n### C2.P1 · Clinical relevance\n", plan)
        self.assertIn("## Aims\n- A1 · not a division\n", plan)
        self.assertEqual(plan.count("- B"), 3)
        self.assertIn("2 renamed", result["summary"])
        self.assertIn("Structure text edited in Draft Space", self.log.read_text(encoding="utf-8"))
        self.assertEqual(result["text"], structure_text(plan))

    def test_unchanged_title_keeps_the_original_heading_line_with_its_span(self):
        result, err = self.save(TEXT)
        self.assertIsNone(err)
        self.assertFalse(result["changed"])
        self.assertIn("### C1.P1 · Variation and consequences · S1 to S2\n", self.plan.read_text(encoding="utf-8"))

    def test_add_reorder_and_drop_an_empty_paragraph(self):
        text = ("C1 · Prescribing behavior\n  C1.P3 · A new paragraph\n  C1.P1 · Variation and consequences\n"
                "C2 · Agreeableness\n  C2.P1 · Clinical relevance\n  C2.P2\n")
        result, err = self.save(text)
        self.assertIsNone(err, err)
        plan = self.plan.read_text(encoding="utf-8")
        self.assertLess(plan.index("### C1.P3 · A new paragraph"), plan.index("### C1.P1 ·"))
        self.assertNotIn("Empty paragraph", plan)
        self.assertIn("### C2.P2\n", plan)
        self.assertIn("Draft: Physicians vary.", plan)
        self.assertEqual(structure_text(plan), text.rstrip("\n"))
        for word in ("2 added", "1 removed"):
            self.assertIn(word, result["summary"])

    def test_dropping_a_paragraph_with_points_is_refused(self):
        _, err = self.save("C1 · Prescribing behavior\n  C1.P2 · Empty paragraph\nC2 · Agreeableness\n  C2.P1 · Clinical relevance")
        self.assertIn("C1.P1 has 2 points", err)
        self.assertEqual(self.plan.read_text(encoding="utf-8"), PLAN)

    def test_bad_lines_are_named_and_nothing_is_written(self):
        for text, fragment in (("hello", "line 1 must start with"),
                               ("  C1.P1 · x", "comes before any C<n>"),
                               ("C1 · a\n  C2.P1 · b", "not inside C1"),
                               ("C1 · a\n  C1.P1 · b\n  C1.P1 · c", "appears twice"),
                               ("", "at least one C<n>")):
            with self.subTest(text=text):
                _, err = self.save(text)
                self.assertIn(fragment, err)
        self.assertEqual(self.plan.read_text(encoding="utf-8"), PLAN)
        self.assertEqual(save_structure(self.page, {"text": TEXT}, read_only=True)[1],
                         "This host is read-only; Structure edits are disabled")

    def test_post_action_structure_reaches_save(self):
        page = self.page

        class Host(OutlineMixin):
            root = page.parent

            def target(self, p):
                return (page.name, str(page.parent))

        body, err = Host().plug_outline({"action": "structure", "text": TEXT.replace("Clinical relevance", "Relevance")})
        self.assertIsNone(err, err)
        self.assertTrue(body["changed"])
        self.assertIn("### C2.P1 · Relevance\n", self.plan.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
