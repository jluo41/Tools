#!/usr/bin/env python3
"""Guard the canonical Task Folder / Page Folder vocabulary."""

import unittest
from pathlib import Path


SKILL = Path(__file__).resolve().parents[1]
TOOLKIT_SKILLS = SKILL.parents[1]


class TaskFolderVocabularyTest(unittest.TestCase):
    def read(self, path: Path) -> str:
        return path.read_text(encoding="utf-8")

    def test_three_core_contracts_name_one_physical_folder(self):
        paths = (
            SKILL / "SKILL.md",
            TOOLKIT_SKILLS / "board" / "haipipe-folder" / "SKILL.md",
            TOOLKIT_SKILLS / "board" / "haipipe-page" / "SKILL.md",
        )
        for path in paths:
            with self.subTest(path=path):
                self.assertIn("Task Folder = Page Folder", self.read(path))

    def test_current_authoring_never_calls_a_job_task_folder(self):
        paths = (
            SKILL / "SKILL.md",
            SKILL / "fn" / "audit.md",
            SKILL / "ref" / "hierarchy.md",
        )
        forbidden = ("alias `task-folder`", "task-folder = JOB")
        for path in paths:
            text = self.read(path)
            for phrase in forbidden:
                with self.subTest(path=path, phrase=phrase):
                    self.assertNotIn(phrase, text)

    def test_lifecycle_targets_task_folder_and_limits_job_compatibility(self):
        workflow = self.read(SKILL / "ref" / "task-lifecycle.workflow.js")
        self.assertIn("const taskFolder = parsed.task_folder ?? parsed.job", workflow)
        self.assertIn("flat implicit-Task compatibility only", workflow)
        self.assertIn("return {\n  task_folder: taskFolder,", workflow)
        self.assertNotIn("const folder =", workflow)

    def test_current_templates_bind_task_folder_to_tnn_not_job(self):
        sources = (
            SKILL / "fn" / "stage-plan.md",
            SKILL / "ref" / "invocation-modes.md",
            SKILL / "ref" / "workflow-template.yaml",
        )
        for path in sources:
            text = self.read(path)
            with self.subTest(path=path):
                self.assertIn("tNN_<task>", text)
                self.assertNotIn("<PATH_TO_JOB>", text)


if __name__ == "__main__":
    unittest.main()
