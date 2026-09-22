import sys
import tempfile
import unittest
from pathlib import Path

ENGINE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ENGINE))

from src.folder_contract import (  # noqa: E402
    REQUIRED_SECTIONS,
    current_folder_kind,
    folder_identity_path,
    resolved_folder_kind,
    resolve,
    validate_tree,
)


class TestFolderContract(unittest.TestCase):
    @property
    def skills(self):
        return ENGINE.parent.parent

    def test_insight_folder_owners_resolve_without_legacy_lifecycle_metadata(self):
        contracts, integration_problems = validate_tree(self.skills)
        application_workflows = {
            "haipipe-insight-workflow",
            "haipipe-design-workflow",
        }
        app = [
            item for item in contracts
            if item.workflow in application_workflows
        ]
        app_paths = {item.path.as_posix() for item in app}
        problems = [
            problem for problem in integration_problems
            if any(path in problem for path in app_paths)
        ]
        self.assertEqual(problems, [])
        self.assertEqual(
            {(item.workflow, item.folder_kind) for item in app},
            {("haipipe-insight-workflow", kind) for kind in
             ("meta", "question", "data", "information", "knowledge", "wisdom")},
        )
        self.assertTrue(all("folder-kinds" in item.path.parts for item in app))

    def test_current_and_legacy_keys_resolve_to_same_owner(self):
        current = resolve(self.skills, folder_kind="knowledge")
        legacy = resolve(self.skills, legacy_page_type="knowledge")
        self.assertIsNotNone(current)
        self.assertEqual(current, legacy)
        self.assertEqual(current.name, "haipipe-insight-knowledge")

    def test_gate_proves_it_can_fail_on_missing_task_face(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            skill = root / "x" / "folder-kinds" / "haipipe-x-one"
            skill.mkdir(parents=True)
            headings = "\n".join(
                f"## {heading}\n\nbody"
                for heading in REQUIRED_SECTIONS
                if heading != "Task Face"
            )
            (skill / "SKILL.md").write_text(
                "---\nname: haipipe-x-one\nmetadata:\n"
                "  workflow: haipipe-x-workflow\n"
                "  folder_kind: one\n  primary_face: page\n"
                "  page_ruling: none\n---\n\n" + headings,
                encoding="utf-8",
            )
            _contracts, problems = validate_tree(root)
            self.assertTrue(any("Task Face" in item for item in problems), problems)

    def test_legacy_identity_import_does_not_require_a_phase(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            (folder / "workflow").mkdir()
            (folder / "workflow" / "phase.yaml").write_text(
                "current:\n  folder-kind: data\n"
                "history:\n  - {from: I1, to: I2, gate: GI1}\n",
                encoding="utf-8",
            )
            self.assertEqual(current_folder_kind(folder), "data")

    def test_canonical_identity_supersedes_legacy_without_mutating_it(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            (folder / "workflow").mkdir()
            legacy = folder / "workflow" / "phase.yaml"
            legacy.write_text("current:\n  phase: I2\n  folder-kind: data\n")
            before = legacy.read_bytes()
            canonical = folder / "workflow" / "folder.yaml"
            canonical.write_text("current:\n  folder-kind: knowledge\n")
            self.assertEqual(current_folder_kind(folder), "knowledge")
            self.assertEqual(folder_identity_path(folder), canonical)
            self.assertEqual(legacy.read_bytes(), before)

    def test_invalid_canonical_identity_never_falls_back_to_valid_legacy(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            (folder / "workflow").mkdir()
            (folder / "workflow" / "phase.yaml").write_text(
                "current:\n  phase: I2\n  folder-kind: data\n"
            )
            canonical = folder / "workflow" / "folder.yaml"
            for body in ("current: [\n", "current:\n  folder-kind: ???\n",
                         "current:\n  folder-kind: data\n  folder-kind: wisdom\n",
                         "current:\n  unrelated:\n    folder-kind: wisdom\n"):
                with self.subTest(body=body):
                    canonical.write_text(body)
                    with self.assertRaises(ValueError):
                        current_folder_kind(folder)

    def test_present_legacy_lifecycle_file_cannot_fall_back_when_current_is_malformed(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            (folder / "workflow").mkdir()
            (folder / "workflow" / "phase.yaml").write_text(
                "history:\n  - {from: I1, to: I2, gate: GI1}\n",
                encoding="utf-8",
            )
            with self.assertRaisesRegex(ValueError, "missing top-level current"):
                current_folder_kind(folder)

    def test_yaml_direct_children_accept_valid_indentation_and_quotes(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            (folder / "workflow").mkdir()
            for filename in ("phase.yaml", "folder.yaml"):
                path = folder / "workflow" / filename
                for indent in ("  ", "    "):
                    with self.subTest(filename=filename, indent=len(indent)):
                        path.write_text(f"current:\n{indent}folder-kind: 'data'\n")
                        self.assertEqual("data", current_folder_kind(folder))
                path.unlink()

    def test_duplicate_mapping_and_invalid_yaml_never_select_an_owner(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            (folder / "workflow").mkdir()
            (folder / "workflow/phase.yaml").write_text("current:\n  folder-kind: data\n")
            path = folder / "workflow/folder.yaml"
            for text in ("current:\n  folder-kind: data\ncurrent:\n  folder-kind: wisdom\n",
                         "current:\n  folder-kind: 'wisdom\n",
                         "current:\n  child:\n    folder-kind: wisdom\n",
                         "current:\n  folder-kind: [wisdom]\n"):
                with self.subTest(text=text):
                    path.write_text(text)
                    with self.assertRaises(ValueError):
                        current_folder_kind(folder)

    def test_shared_resolution_reports_conflicts_but_ignores_old_alias(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            (folder / "workflow").mkdir()
            (folder / "workflow/folder.yaml").write_text("current:\n  folder-kind: wisdom\n")
            self.assertEqual("wisdom", resolved_folder_kind(folder, legacy="data"))
            with self.assertRaisesRegex(ValueError, "conflicts"):
                resolved_folder_kind(folder, declared="data")


if __name__ == "__main__":
    unittest.main()
