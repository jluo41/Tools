"""PREPARE regression checks for untyped standalone Pages, without a Board."""

import importlib.util
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


HERE = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "context_record_base_test", HERE / "cli" / "context-record.py"
)
CONTEXT = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CONTEXT)


class BasePageContextTest(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.folder = Path(self.temporary.name)
        self.page = self.folder / "standalone.md"
        self.write_page()

    def write_page(self, metadata=""):
        self.page.write_text(
            "# Standalone source guide\nstate: 🟡 Draft\nowner: Test\n"
            + metadata
            + "\n## Opening\nA Page owns its editable source and delivery.\n"
            "\n## Content\n### 1 · Source ownership\nThe source stays local.\n"
            "\n## Aims\n### P · Page-level\n- ⬜ P1 · Explain ownership.\n"
            "  **Done when:** the reader identifies the source.\n"
            "  **Now:** draft; no human approval.\n",
            encoding="utf-8",
        )

    def build(self):
        # The API's legacy `board` argument is only a path anchor here.
        # No board.md, registration, or group exists in this fixture.
        before = {
            p.relative_to(self.folder): p.read_bytes()
            for p in self.folder.rglob("*") if p.is_file()
        }
        result = CONTEXT.build(self.page, self.folder)
        after = {
            p.relative_to(self.folder): p.read_bytes()
            for p in self.folder.rglob("*") if p.is_file()
        }
        self.assertEqual(before, after, "build() must only project source records")
        self.assertFalse((self.folder / "board.md").exists())
        return result

    @staticmethod
    def record(result, number):
        return result.split(f"### CTX{number} · ", 1)[1].split("\n### CTX", 1)[0]

    def test_omitted_kind_uses_base_authorities_without_board(self):
        result = self.build()
        identity = self.record(result, 1)
        self.assertIn("**Status**: resolved", identity)
        self.assertIn("**Folder kind**: base Page", identity)
        self.assertIn("**Folder owner**: haipipe-page\n", identity)
        self.assertIn("**Page Face owner**: haipipe-page\n", identity)
        policy = self.record(result, 3)
        self.assertIn("**Status**: resolved", policy)
        for authority in (
            "page/haipipe-page/SKILL.md",
            "page/haipipe-page/ref/page-template.md",
            "haipipe-board/ref/writing-rules.md",
        ):
            self.assertIn(authority, policy)
        self.assertNotIn("absent", policy)
        self.assertNotIn("page-type:", self.page.read_text(encoding="utf-8"))
        self.assertIn("**Next authority**: OUTLINE", result)

    def test_unknown_explicit_kind_does_not_fall_back(self):
        for key in ("folder-kind", "page-type"):
            with self.subTest(key=key):
                self.write_page(f"{key}: nonexistent-validation-kind\n")
                result = self.build()
                identity = self.record(result, 1)
                self.assertIn("**Status**: missing", identity)
                self.assertIn("**Folder owner**: unresolved", identity)
                self.assertNotIn("base Page", identity)
                self.assertIn("**Next authority**: CONTEXT", result)

    def test_malformed_workflow_identity_does_not_fall_back(self):
        workflow = self.folder / "workflow"
        workflow.mkdir()
        for body in ("", "current: [\n", "current:\n  folder-kind: unknown-kind\n"):
            with self.subTest(workflow=body):
                (workflow / "phase.yaml").write_text(body, encoding="utf-8")
                result = self.build()
                identity = self.record(result, 1)
                self.assertIn("**Status**: missing", identity)
                self.assertNotIn("base Page", identity)
                self.assertIn("**Next authority**: CONTEXT", result)

    def test_no_plan_before_shape_is_not_a_missing_authority(self):
        result = self.build()
        readiness = self.record(result, 6)
        self.assertIn("**Status**: not-applicable", readiness)
        self.assertIn("**Plan**: no plan on disk", readiness)
        self.assertIn("**Next authority**: OUTLINE", readiness)
        self.assertFalse((self.folder / "outline").exists())
        self.assertNotIn("approved: ✅", result)
        self.assertNotIn("accepted: ✅", result)

    def test_valid_nested_workflow_identity_resolves(self):
        workflow = self.folder / "workflow"
        workflow.mkdir()
        (workflow / "phase.yaml").write_text(
            "current:\n  phase: D2\n  folder-kind: design-unit\n",
            encoding="utf-8",
        )
        result = self.build()
        self.assertIn("**Status**: resolved", self.record(result, 1))
        self.assertIn("**Folder kind**: design-unit", self.record(result, 1))

    def test_malformed_yaml_cannot_resolve_from_a_top_level_kind(self):
        self.write_page(
            "structure-source: workflow-phases/haipipe-paper-section/"
            "ref/generic-template.md\n"
        )
        workflow = self.folder / "workflow"
        workflow.mkdir()
        (workflow / "phase.yaml").write_text(
            "folder-kind: section\ncurrent: [\n", encoding="utf-8"
        )
        result = self.build()
        self.assertIn("**Status**: missing", self.record(result, 1))
        self.assertIn("**Next authority**: CONTEXT", result)

    def test_cli_generates_context_without_board_or_plan(self):
        original = self.page.read_bytes()
        completed = subprocess.run(
            [sys.executable, "-B", str(HERE / "cli" / "context-record.py"),
             str(self.page)],
            cwd=self.folder,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(0, completed.returncode, completed.stderr)
        record = self.folder / "outline" / "standalone-context.md"
        result = record.read_text(encoding="utf-8")
        self.assertIn("**Folder kind**: base Page", result)
        self.assertIn("**Next authority**: OUTLINE", result)
        self.assertEqual(original, self.page.read_bytes())
        self.assertEqual(
            {"standalone.md", "outline/standalone-context.md"},
            {p.relative_to(self.folder).as_posix()
             for p in self.folder.rglob("*") if p.is_file()},
        )

    def test_explicit_section_still_requires_structure(self):
        for key in ("folder-kind", "page-type"):
            with self.subTest(key=key):
                self.write_page(f"{key}: section\n")
                result = self.build()
                self.assertIn("**Status**: resolved", self.record(result, 1))
                self.assertIn("**Status**: missing", self.record(result, 3))
                self.assertIn("**Next authority**: CONTEXT", result)

    def test_unapproved_plan_is_reported_without_granting_approval(self):
        outline = self.folder / "outline"
        outline.mkdir()
        plan = outline / "standalone-outline-v0.1.md"
        plan.write_text(
            "# standalone · outline v0.1\noutline-version: v0.1\n"
            "approved: ⬜\n\n## C1 · Source ownership\n"
            "### C1.P1 · Identify the source\n- B1 · The Page owns its source.\n"
            "  Evidence: none · ownership definition\n",
            encoding="utf-8",
        )
        result = self.build()
        self.assertIn("v0.1 · approved: ⬜", self.record(result, 6))
        self.assertIn("**Next authority**: OUTLINE", result)
        self.assertNotIn("approved: ✅", result)
        self.assertNotIn("accepted: ✅", result)


if __name__ == "__main__":
    unittest.main()
