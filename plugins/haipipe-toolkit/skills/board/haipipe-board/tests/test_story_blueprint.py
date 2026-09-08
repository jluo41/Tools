"""Story plans resolve their semantic owner and enforce the paper blueprint."""
import tempfile
import unittest
from pathlib import Path

from src.plan_shape import check, type_outline


SKILLS_ROOT = Path(__file__).resolve().parents[3]
BLUEPRINT = (
    "Identity", "Pitch", "Research Questions", "Stakes",
    "Evidence Basis and Boundaries", "Discovery Roadmap",
    "Task Roadmap", "Section Narrative",
)


class StoryBlueprintTest(unittest.TestCase):
    def findings(self, divisions):
        with tempfile.TemporaryDirectory() as temporary:
            page = Path(temporary) / "StoryA-misq-phytrait-discretion.md"
            page.write_text("# Proposed paper\npage-type: story\n", encoding="utf-8")
            plan = "\n".join(
                f"## C{i} · {title}" for i, title in enumerate(divisions, 1)
            )
            return check(page, plan, SKILLS_ROOT)

    def test_runtime_resolves_story_owner_without_registry(self):
        resolved = type_outline("story", SKILLS_ROOT)
        self.assertEqual("fixed", resolved["mode"])
        self.assertEqual(
            SKILLS_ROOT / "paper/workflow-phases/haipipe-paper-story/SKILL.md",
            Path(resolved["type_path"]),
        )

    def test_prospective_blueprint_is_accepted(self):
        self.assertEqual([], self.findings(BLUEPRINT))

    def test_old_control_layout_is_rejected(self):
        control = BLUEPRINT[:4] + (
            "Source Pages", "Evidence and Work Control", "Boundaries",
            "Section and Compile Handoff",
        )
        self.assertTrue(self.findings(control))

    def test_missing_research_roadmap_is_rejected(self):
        self.assertTrue(self.findings(BLUEPRINT[:6] + BLUEPRINT[7:]))

    def test_empty_story_plan_is_rejected(self):
        self.assertTrue(self.findings(()))

    def test_roadmap_order_cannot_be_swapped(self):
        swapped = BLUEPRINT[:5] + (BLUEPRINT[6], BLUEPRINT[5], BLUEPRINT[7])
        self.assertTrue(self.findings(swapped))


if __name__ == "__main__":
    unittest.main()
