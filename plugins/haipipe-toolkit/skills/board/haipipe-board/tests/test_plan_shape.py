#!/usr/bin/env python3
"""Resolved Section outlines enforce the current venue-template guard."""

import tempfile
import unittest
from pathlib import Path

from src.plan_shape import check, check_coverage, type_outline
from cli.check import Report, check_section_sentences


HERE = Path(__file__).resolve().parent.parent
SKILLS_ROOT = HERE.parents[1]
PLAN = "## C1 · Results\n\n### P1 · Finding\n- B1 · Report result\n  Note: bounded result\n"


class ResolvedSectionShapeTest(unittest.TestCase):
    def findings(self, structure_source: str):
        with tempfile.TemporaryDirectory() as temporary:
            page = Path(temporary) / "Q-section.md"
            page.write_text(
                "# Fixture\n"
                "page-type: section\n"
                "section-kind: results\n"
                f"structure-source: {structure_source}\n",
                encoding="utf-8",
            )
            return check(page, PLAN, SKILLS_ROOT)

    def test_marked_misq_results_template_is_current(self):
        self.assertEqual(
            [],
            self.findings(
                "venue/playbook-utd-is/MISQ/MISQ-results/template.md"
            ),
        )

    def test_unmarked_stage_era_template_is_rejected(self):
        findings = self.findings(
            "venue/playbook-utd-is/MISQ/MISQ-introduction/template.md"
        )
        self.assertTrue(any("lacks required marker" in row for row in findings))

    def test_explicit_generic_fallback_is_current(self):
        self.assertEqual(
            [],
            self.findings(
                "workflow-phases/haipipe-paper-section/ref/generic-template.md"
            ),
        )

    def test_phase_owned_folder_kind_resolves_its_page_face(self):
        with tempfile.TemporaryDirectory() as temporary:
            page = Path(temporary) / "K01-claim.md"
            page.write_text(
                "# Fixture\nfolder-kind: knowledge\n",
                encoding="utf-8",
            )
            complete = "\n".join(
                f"## C{i} · {title}" for i, title in enumerate(
                    ("Claim", "Information Cited", "Strength", "Rivals", "Boundary"), 1
                )
            )
            self.assertEqual([], check(page, complete, SKILLS_ROOT))

    def test_legacy_application_page_type_resolves_the_same_phase(self):
        with tempfile.TemporaryDirectory() as temporary:
            page = Path(temporary) / "K01-claim.md"
            page.write_text(
                "# Fixture\npage-type: knowledge\n",
                encoding="utf-8",
            )
            broken = "## C1 · Claim\n## C2 · Strength\n"
            findings = check(page, broken, SKILLS_ROOT)
            self.assertTrue(any("5 declared divisions" in item for item in findings))

    def test_task_folder_kind_resolves_to_canonical_task_owner(self):
        declaration = type_outline("task", SKILLS_ROOT)
        self.assertEqual("grammar", declaration["mode"])
        self.assertTrue(
            declaration["type_path"].endswith("task/haipipe-task/SKILL.md")
        )
        with tempfile.TemporaryDirectory() as temporary:
            page = Path(temporary) / "t01_model.md"
            page.write_text("# Fixture\nfolder-kind: task\n", encoding="utf-8")
            broken = "## C1 · Files listed\n## C2 · Result found\n"
            findings = check(page, broken, SKILLS_ROOT)
            self.assertTrue(any("outside the closed set" in item for item in findings))

    def test_legacy_task_page_type_uses_the_same_canonical_owner(self):
        with tempfile.TemporaryDirectory() as temporary:
            page = Path(temporary) / "t01_model.md"
            page.write_text("# Fixture\npage-type: task\n", encoding="utf-8")
            broken = "## C1 · Result found\n## C2 · Method chosen\n"
            findings = check(page, broken, SKILLS_ROOT)
            self.assertTrue(any("must be last" in item for item in findings))

    def test_matching_task_current_and_legacy_keys_share_one_owner(self):
        with tempfile.TemporaryDirectory() as temporary:
            page = Path(temporary) / "t01_model.md"
            page.write_text(
                "# Fixture\nfolder-kind: task\npage-type: task\n",
                encoding="utf-8",
            )
            broken = "## C1 · Result found\n## C2 · Method chosen\n"
            findings = check(page, broken, SKILLS_ROOT)
            self.assertFalse(any("different Page Face owners" in item for item in findings))
            self.assertTrue(any("must be last" in item for item in findings))

    def test_conflicting_current_and_legacy_keys_are_rejected(self):
        with tempfile.TemporaryDirectory() as temporary:
            page = Path(temporary) / "t01_model.md"
            page.write_text(
                "# Fixture\nfolder-kind: task\npage-type: knowledge\n",
                encoding="utf-8",
            )
            findings = check(page, "## C1 · Result found\n", SKILLS_ROOT)
            self.assertTrue(any("different Page Face owners" in item for item in findings))

    def test_decimal_plan_requires_one_evidence_decision_per_bullet(self):
        with tempfile.TemporaryDirectory() as temporary:
            page = Path(temporary) / "Q-section.md"
            page.write_text("# Fixture\n", encoding="utf-8")
            plan = (
                "# Q · outline v0.1\noutline-version: v0.1\n\n"
                "## C1 · One\n### C1.P1 · Move\n"
                "- B1 · Make a transition now\n  Note: no source needed\n"
            )
            self.assertIn(
                "C1.P1.B1 has no explicit Evidence declaration",
                check_coverage(page, plan),
            )

    def test_explicit_none_closes_a_source_free_bullet(self):
        with tempfile.TemporaryDirectory() as temporary:
            page = Path(temporary) / "Q-section.md"
            page.write_text("# Fixture\n", encoding="utf-8")
            plan = (
                "# Q · outline v0.1\noutline-version: v0.1\n\n"
                "## C1 · One\n### C1.P1 · Move\n"
                "- B1 · Make a transition now\n  Note: no source needed\n"
                "  Evidence: none · transition only; no citation, value, or display\n"
            )
            self.assertEqual([], check_coverage(page, plan))

    def test_sibling_item_reference_does_not_close_a_bullet(self):
        with tempfile.TemporaryDirectory() as temporary:
            page = Path(temporary) / "Q-section.md"
            page.write_text("# Fixture\n", encoding="utf-8")
            outline = page.parent / "outline"
            outline.mkdir()
            (outline / "Q-section-evidence-items.md").write_text(
                "### E01-CITE-source · C1.P1.B1 · source\n",
                encoding="utf-8",
            )
            plan = (
                "# Q · outline v0.1\noutline-version: v0.1\n\n"
                "## C1 · One\n### C1.P1 · Move\n"
                "- B1 · State the supported external claim\n"
                "  Evidence: E01-CITE-source · verified source\n"
                "  Accept: source resolves\n"
                "- B2 · Explain a second external claim\n"
                "  Note: use E01's source without creating another item\n"
            )
            self.assertIn(
                "C1.P1.B2 has no explicit Evidence declaration",
                check_coverage(page, plan),
            )

    def test_none_cannot_mix_with_a_typed_item(self):
        with tempfile.TemporaryDirectory() as temporary:
            page = Path(temporary) / "Q-section.md"
            page.write_text("# Fixture\n", encoding="utf-8")
            outline = page.parent / "outline"
            outline.mkdir()
            (outline / "Q-section-evidence-items.md").write_text(
                "### E01-CITE-source · C1.P1.B1 · source\n",
                encoding="utf-8",
            )
            plan = (
                "# Q · outline v0.1\noutline-version: v0.1\n\n"
                "## C1 · One\n### C1.P1 · Move\n"
                "- B1 · State an external claim\n  Note: claim\n"
                "  Evidence: none · transition only\n"
                "  Evidence: E01-CITE-source · verified source\n"
                "  Accept: source resolves\n"
            )
            self.assertIn(
                "C1.P1.B1 mixes Evidence none with typed Evidence Items",
                check_coverage(page, plan),
            )

    def test_content_citation_cannot_realize_an_explicit_none_bullet(self):
        with tempfile.TemporaryDirectory() as temporary:
            folder = Path(temporary)
            page = folder / "Q-section.md"
            page.write_text("# Fixture\npage-type: section\n", encoding="utf-8")
            outline = folder / "outline"
            outline.mkdir()
            (outline / "Q-section-outline-v1.0.md").write_text(
                "# Q · outline v1.0\noutline-version: v1.0\napproved: ✅ JL\n\n"
                "## C1 · One\n### C1.P1 · Move\n"
                "- B1 · Make a transition now\n  Note: transition\n"
                "  Evidence: none · transition only\n",
                encoding="utf-8",
            )
            content = (
                "# Fixture\npage-type: section\n\n## Content\n"
                "This transition cites prior work \\citep{source}. "
                "<!-- realizes: C1.P1.B1 -->\n"
            )
            report = Report()
            check_section_sentences(content, page, page.name, report)
            self.assertTrue(any(
                code == "citation-without-bullet-evidence"
                for _level, code, _where, _message in report.rows
            ))

    def test_content_value_requires_value_item_on_the_same_bullet(self):
        with tempfile.TemporaryDirectory() as temporary:
            folder = Path(temporary)
            page = folder / "Q-section.md"
            page.write_text("# Fixture\npage-type: section\n", encoding="utf-8")
            outline = folder / "outline"
            outline.mkdir()
            (outline / "Q-section-outline-v1.0.md").write_text(
                "# Q · outline v1.0\noutline-version: v1.0\napproved: ✅ JL\n\n"
                "## C1 · One\n### C1.P1 · Move\n"
                "- B1 · State an external source\n  Note: citation only\n"
                "  Evidence: E01-CITE-source · source claim\n"
                "  Accept: source resolves\n",
                encoding="utf-8",
            )
            content = (
                "# Fixture\npage-type: section\n\n## Content\n"
                "The estimate was 9.34 MME. <!-- realizes: C1.P1.B1 -->\n"
                "> Value: E99\n"
            )
            report = Report()
            check_section_sentences(content, page, page.name, report)
            self.assertTrue(any(
                code == "value-without-bullet-evidence"
                for _level, code, _where, _message in report.rows
            ))


if __name__ == "__main__":
    unittest.main()
