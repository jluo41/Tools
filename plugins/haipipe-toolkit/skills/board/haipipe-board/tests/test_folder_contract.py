import sys
import tempfile
import unittest
from pathlib import Path

ENGINE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ENGINE))

from src.folder_contract import (  # noqa: E402
    REQUIRED_SECTIONS,
    current_folder_kind,
    resolve,
    validate_tree,
)


class TestFolderContract(unittest.TestCase):
    @property
    def skills(self):
        return ENGINE.parent.parent

    def test_application_phase_family_is_complete(self):
        contracts, problems = validate_tree(self.skills)
        app = [item for item in contracts if item.workflow.startswith("haipipe-i") or item.workflow.startswith("haipipe-d")]
        self.assertEqual(problems, [])
        self.assertEqual(
            {(item.workflow, item.phase) for item in app},
            {
                ("haipipe-insight-workflow", f"I{n}") for n in range(6)
            }
            | {("haipipe-design-workflow", f"D{n}") for n in range(6)},
        )

    def test_current_and_legacy_keys_resolve_to_same_phase(self):
        current = resolve(self.skills, folder_kind="knowledge")
        legacy = resolve(self.skills, legacy_page_type="knowledge")
        self.assertIsNotNone(current)
        self.assertEqual(current, legacy)
        self.assertEqual(current.name, "haipipe-insight-knowledge")

    def test_gate_proves_it_can_fail_on_missing_task_face(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            skill = root / "x" / "workflow-phases" / "haipipe-x-one"
            skill.mkdir(parents=True)
            headings = "\n".join(
                f"## {heading}\n\nbody"
                for heading in REQUIRED_SECTIONS
                if heading != "Task Face"
            )
            (skill / "SKILL.md").write_text(
                "---\nname: haipipe-x-one\nmetadata:\n"
                "  workflow: haipipe-x-workflow\n  phase: X0\n"
                "  folder_kind: one\n  primary_face: page\n"
                "  page_ruling: none\n---\n\n" + headings,
                encoding="utf-8",
            )
            _contracts, problems = validate_tree(root)
            self.assertTrue(any("Task Face" in item for item in problems), problems)

    def test_in_place_phase_file_owns_the_current_kind(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            (folder / "workflow").mkdir()
            (folder / "workflow" / "phase.yaml").write_text(
                "current:\n  phase: D2\n  folder-kind: design-unit\n"
                "history:\n  - {from: D1, to: D2, gate: GD1}\n",
                encoding="utf-8",
            )
            self.assertEqual(current_folder_kind(folder), "design-unit")

    def test_present_phase_file_cannot_fall_back_when_current_is_malformed(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            (folder / "workflow").mkdir()
            (folder / "workflow" / "phase.yaml").write_text(
                "history:\n  - {from: D1, to: D2, gate: GD1}\n",
                encoding="utf-8",
            )
            with self.assertRaisesRegex(ValueError, "missing top-level current"):
                current_folder_kind(folder)


if __name__ == "__main__":
    unittest.main()
