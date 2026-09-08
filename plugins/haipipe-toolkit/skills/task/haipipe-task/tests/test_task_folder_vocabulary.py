#!/usr/bin/env python3
"""Guard the canonical Task Folder / Page Folder vocabulary."""

import unittest
from pathlib import Path


SKILL = Path(__file__).resolve().parents[1]
TOOLKIT_SKILLS = SKILL.parents[2]


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
            SKILL / "fn" / "stage-plan.md",
            SKILL / "ref" / "invocation-modes.md",
            SKILL / "ref" / "workflow-template.yaml",
        )
        forbidden = ("alias `task-folder`", "task-folder = JOB", "task_folder:")
        for path in paths:
            text = self.read(path)
            for phrase in forbidden:
                with self.subTest(path=path, phrase=phrase):
                    self.assertNotIn(phrase, text)

    def test_lifecycle_accepts_legacy_input_but_emits_job(self):
        workflow = self.read(SKILL / "ref" / "task-lifecycle.workflow.js")
        self.assertIn("const job = parsed.job ?? parsed.task_folder", workflow)
        self.assertIn("legacy input only", workflow)
        self.assertIn("return {\n  job,", workflow)
        self.assertNotIn("task_folder: folder", workflow)
        self.assertNotIn("Task folder:", workflow)


if __name__ == "__main__":
    unittest.main()
