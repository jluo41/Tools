#!/usr/bin/env python3
"""Resolved Section outlines enforce the current venue-template guard."""

import tempfile
import unittest
from pathlib import Path

from src.plan_shape import check


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


if __name__ == "__main__":
    unittest.main()
