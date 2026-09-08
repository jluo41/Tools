#!/usr/bin/env python3
"""Guard the canonical Task Folder / Page Folder vocabulary."""

import unittest
import re
import shutil
import subprocess
import tempfile
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
            SKILL / "ref" / "task-structure.md",
        )
        forbidden = ("alias `task-folder`", "task-folder = JOB")
        for path in paths:
            text = self.read(path)
            for phrase in forbidden:
                with self.subTest(path=path, phrase=phrase):
                    self.assertNotIn(phrase, text)

    def test_lifecycle_accepts_only_task_folder(self):
        workflow = self.read(SKILL / "ref" / "task-lifecycle.workflow.js")
        self.assertIn("const taskFolder = parsed.task_folder", workflow)
        self.assertIn("return {\n  task_folder: taskFolder,", workflow)
        self.assertNotIn("const folder =", workflow)
        self.assertNotIn("parsed.job", workflow)

    def test_current_templates_bind_task_folder_to_tnn_not_job(self):
        sources = (
            SKILL / "fn" / "stage-plan.md",
            SKILL / "fn" / "stage-report.md",
            SKILL / "ref" / "invocation-modes.md",
            SKILL / "ref" / "workflow-template.yaml",
        )
        for path in sources:
            text = self.read(path)
            with self.subTest(path=path):
                self.assertIn("tNN_<task>", text)
                self.assertNotIn("<PATH_TO_JOB>", text)

    def test_skill_contains_no_backward_compatibility_surface(self):
        patterns = {
            "legacy language": re.compile(r"\blegacy\b", re.IGNORECASE),
            "compatibility language": re.compile(r"\bcompatib(?:ility|le)\b", re.IGNORECASE),
            "retired language": re.compile(r"\bretired\b", re.IGNORECASE),
            "old task-folder key": re.compile(r"task-folder:"),
            "old task-group name": re.compile(r"task-group"),
            "old task page key": re.compile(r"page-type:\s*task"),
            "flat Job": re.compile(r"flat\s+(?:legacy\s+)?job", re.IGNORECASE),
            "implicit Task": re.compile(r"implicit[- ]task", re.IGNORECASE),
            "old shared-code lane": re.compile(r"0-libs"),
            "old builder home": re.compile(r"code-dev"),
            "old root config lane": re.compile(r"(?<!scripts/)configs/"),
        }
        suffixes = {".md", ".js", ".py", ".sh", ".yaml", ".json", ".ps1", ".psd1"}
        findings = []
        for path in SKILL.rglob("*"):
            if not path.is_file() or path.suffix not in suffixes:
                continue
            if "tests" in path.parts or "__pycache__" in path.parts:
                continue
            text = self.read(path)
            for label, pattern in patterns.items():
                for match in pattern.finditer(text):
                    line = text.count("\n", 0, match.start()) + 1
                    findings.append(f"{path.relative_to(SKILL)}:{line}: {label}")
        self.assertEqual([], findings, "\n".join(findings))

    def test_tree_checker_accepts_only_canonical_task_folders(self):
        checker = SKILL / "ref" / "check_task_tree.py"
        with tempfile.TemporaryDirectory() as tmp:
            tasks = Path(tmp) / "tasks"
            block = tasks / "b01_physician_candidates"
            job = block / "j01_candidates_by_region"
            task = job / "t01_physicians_collected"
            (job / "src").mkdir(parents=True)
            (task / "scripts" / "config").mkdir(parents=True)
            (task / "runs").mkdir()
            (block / "board.md").write_text(
                "---\nboard-kind: task-block\n---\n# Candidates\n",
                encoding="utf-8",
            )
            (task / f"{task.name}.md").write_text(
                "---\nfolder-kind: task\ntask: .\n---\n# Physicians collected\n",
                encoding="utf-8",
            )
            (task / "scripts" / "config" / "r01_healthgrades_full.yaml").write_text(
                "_meta:\n  purpose: collect physicians\n",
                encoding="utf-8",
            )
            (task / "runs" / "r01_healthgrades_full.sh").write_text(
                "#!/bin/bash\n",
                encoding="utf-8",
            )
            canonical = subprocess.run(
                ["python3", str(checker), str(tasks)],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(0, canonical.returncode, canonical.stdout + canonical.stderr)

            duplicate_config = task / "scripts" / "config" / "r01_healthgrades_full_v2.yaml"
            duplicate_ticket = task / "runs" / "r01_healthgrades_full_v2.sh"
            duplicate_config.write_text("_meta:\n  purpose: duplicate\n", encoding="utf-8")
            duplicate_ticket.write_text("#!/bin/bash\n", encoding="utf-8")
            (task / "README.md").write_text("# duplicate surface\n", encoding="utf-8")
            duplicated = subprocess.run(
                ["python3", str(checker), str(tasks)],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertNotEqual(0, duplicated.returncode)
            self.assertIn("N10", duplicated.stdout)
            self.assertIn("S20", duplicated.stdout)
            duplicate_config.unlink()
            duplicate_ticket.unlink()
            (task / "README.md").unlink()

            invalid_job = block / "j02_rankings_by_source"
            (invalid_job / "src").mkdir(parents=True)
            (invalid_job / "runs").mkdir()
            (invalid_job / "rankings.py").write_text("pass\n", encoding="utf-8")
            rejected = subprocess.run(
                ["python3", str(checker), str(tasks)],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertNotEqual(0, rejected.returncode)
            self.assertIn("S19", rejected.stdout)

    def test_ticket_rejects_job_level_runs_lane(self):
        template = SKILL / "ref" / "run-sh-template.sh"
        with tempfile.TemporaryDirectory() as tmp:
            ticket = (
                Path(tmp)
                / "tasks"
                / "b01_physician_candidates"
                / "j01_candidates_by_region"
                / "runs"
                / "r01_healthgrades_full.sh"
            )
            ticket.parent.mkdir(parents=True)
            shutil.copyfile(template, ticket)
            rejected = subprocess.run(
                ["bash", str(ticket)],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(2, rejected.returncode)
            self.assertIn("Task Folder must be named", rejected.stderr)


if __name__ == "__main__":
    unittest.main()
