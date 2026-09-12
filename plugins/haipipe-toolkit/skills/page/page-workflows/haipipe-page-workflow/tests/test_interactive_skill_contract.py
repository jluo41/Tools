"""Static routing guards; behavioral acceptance is a fresh-agent field test.

These tests deliberately do not claim a new writer, scheduler or UI exists.
"""

import re
import unittest
from pathlib import Path


SKILLS = Path(__file__).resolve().parents[4]
WORKFLOW = SKILLS / "page/page-workflows/haipipe-page-workflow"


class InteractiveSkillContractTest(unittest.TestCase):
    def test_relative_instruction_links_resolve(self):
        files = [
            WORKFLOW / "SKILL.md",
            WORKFLOW / "ref/interactive-writing-run.md",
            WORKFLOW / "ref/workflow-table.md",
            SKILLS / "page/page-workflows/haipipe-page-content/SKILL.md",
            SKILLS / "page/page-workflows/haipipe-page-content/ref/paragraph-run.md",
            SKILLS / "writing/haipipe-writing/SKILL.md",
            SKILLS / "run/haipipe-run/SKILL.md",
        ]
        for source in files:
            for reference in re.findall(r"`((?:\.\./)+[^`\s<>*]+\.md)`", source.read_text()):
                with self.subTest(source=source.name, reference=reference):
                    self.assertTrue((source.parent / reference).is_file(), reference)

    def test_entry_points_route_to_one_interactive_contract(self):
        for relative in (
            "page/haipipe-page/SKILL.md",
            "page/page-workflows/haipipe-page-content/SKILL.md",
            "page/page-workflows/haipipe-page-outline/SKILL.md",
            "writing/haipipe-writing/SKILL.md",
            "run/haipipe-run/SKILL.md",
        ):
            with self.subTest(skill=relative):
                self.assertIn("interactive-writing-run.md", (SKILLS / relative).read_text())

    def test_content_default_is_adoption_not_paragraph_allocation(self):
        text = (SKILLS / "page/page-workflows/haipipe-page-content/SKILL.md").read_text()
        self.assertIn("## Adopt · no second draft", text)
        self.assertIn("## Optional delegated single-paragraph path", text)
        self.assertNotIn("normally commissions six writing Runs", text)
        self.assertNotIn("Every current writing dispatch records", text)

    def test_template_preserves_input_output_and_seal(self):
        template = (WORKFLOW / "ref/writing-step-template.md").read_text()
        for required in (
            "s001-input.md", "s001-result.md", "Original request",
            "Selected quote", "Source Version/Step", "Agent interpretation",
            "Planning snapshot", "Protected/out-of-scope", "Sealed records",
        ):
            with self.subTest(field=required):
                self.assertIn(required, template)

    def test_handoff_and_runtime_boundary_are_explicit(self):
        packet = (SKILLS / "page/haipipe-page/ref/user-check-packet.md").read_text()
        self.assertIn("both direct clickable links at the very end", packet)
        self.assertIn("lens=div", packet)
        self.assertIn("lens=workspace&seg=items", packet)
        contract = (WORKFLOW / "ref/interactive-writing-run.md").read_text()
        self.assertIn("not a newly implemented CLI", contract)
        self.assertIn("waiting-for-feedback", contract)
        self.assertIn("Closed records", (SKILLS / "run/haipipe-run/SKILL.md").read_text())


if __name__ == "__main__":
    unittest.main()
