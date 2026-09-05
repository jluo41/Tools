#!/usr/bin/env python3
"""Resolved Section outlines enforce the current venue-template guard."""

import tempfile
import unittest
from pathlib import Path

from src.plan_shape import check, type_outline


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


if __name__ == "__main__":
    unittest.main()
