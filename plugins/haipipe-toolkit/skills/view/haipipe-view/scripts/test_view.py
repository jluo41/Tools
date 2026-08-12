#!/usr/bin/env python3
"""Regression tests for View scaffolding and shared fixture ownership."""

from __future__ import annotations

import base64
import importlib.util
import json
import pathlib
import shutil
import tempfile
import unittest


SCRIPT = pathlib.Path(__file__).with_name("view.py")
SPEC = importlib.util.spec_from_file_location("haipipe_view_impl", SCRIPT)
assert SPEC and SPEC.loader
view = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(view)

PNG_1X1 = base64.b64decode(
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+A8AAQUBAScY42YAAAAASUVORK5CYII="
)


class ViewTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory(prefix="haipipe-view-test-")
        self.root = pathlib.Path(self.temporary.name)
        self.pages = self.root / "pages"
        self.pages.mkdir()
        self.fixture = self.root / "shared-fixture"

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def make_view(self, stem: str, bib_key: str, bib_title: str) -> pathlib.Path:
        self.assertEqual(view.create(self.pages, stem, f"Test {stem}"), 0)
        page = self.pages / f"{stem}.md"
        unit = self.pages / "views" / stem
        probe = unit / "input" / "QA-probes" / "Q1.md"
        probe.write_text("# Answered Probe\n\nA bounded test answer.\n", encoding="utf-8")
        bib = unit / "input" / "sources" / "references.bib"
        bib.write_text(
            f"@article{{{bib_key},\n  author = {{Test, Agent}},\n  title = {{{bib_title}}},\n  year = {{2026}}\n}}\n",
            encoding="utf-8",
        )
        page.write_text(
            f"# Test {stem}\npage-type: view\nview-unit: views/{stem}\n\n"
            "## Content\n\n### 1 · QA inputs\nOne answered Probe.\n\n"
            "### 2 · View body\nA bounded test body.\n\n"
            "### 3 · Displays\nNo rendered Display yet.\n\n"
            "### 4 · Consumers\nNo consumer yet.\n\n"
            "## Aims\n\n## States\n\n## Files\n",
            encoding="utf-8",
        )
        manifest_path = unit / "manifest.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        manifest["inputs"] = {
            "qa_probes": ["input/QA-probes/Q1.md"],
            "sources": ["input/sources/references.bib"],
        }
        manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
        return page

    def render_test_display(self, page: pathlib.Path, slug: str = "bounded-result") -> str:
        self.assertEqual(
            view.add_display(page, "text", slug, "Read one bounded test result.", ["EC1"]),
            0,
        )
        unit = page.parent / "views" / page.stem
        manifest_path = unit / "manifest.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        row = manifest["displays"][-1]
        row["status"] = "rendered"
        folder = row["folder"]
        display = unit / "output" / folder
        (display / "assets" / "artifact.txt").write_text("bounded result\n", encoding="utf-8")
        (display / "float.tex").write_text("Bounded test display.\n", encoding="utf-8")
        (display / "preview.png").write_bytes(PNG_1X1)
        (display / "preview.pdf").write_bytes(b"%PDF-1.4\n% test display preview\n")
        manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
        text = page.read_text(encoding="utf-8").replace(
            "No rendered Display yet.",
            f"![](views/{page.stem}/output/{folder}/preview.png)",
        )
        page.write_text(text, encoding="utf-8")
        return folder

    def test_add_display_creates_native_unit(self) -> None:
        page = self.make_view("QT1-for-view", "qt1", "First")
        self.assertEqual(
            view.add_display(page, "table", "main-table", "Compare bounded rows.", ["EC1"]),
            0,
        )
        display = self.pages / "views" / page.stem / "output" / "QT1-Display1-main-table"
        for name in view.DISPLAY_REQUIRED_FILES:
            self.assertTrue((display / name).is_file(), name)
        for name in view.DISPLAY_REQUIRED_DIRS:
            self.assertTrue((display / name).is_dir(), name)
        manifest = json.loads((self.pages / "views" / page.stem / "manifest.json").read_text())
        self.assertEqual(manifest["displays"][0]["unit_contract"], view.DISPLAY_UNIT_CONTRACT)

    @unittest.skipUnless(shutil.which("xelatex"), "xelatex is required for fixture tests")
    def test_shared_fixture_is_owned_and_source_free(self) -> None:
        page1 = self.make_view("QT1-for-view", "qt1", "First")
        page2 = self.make_view("QT2-for-view", "qt2", "Second")
        folder1 = self.render_test_display(page1)
        folder2 = self.render_test_display(page2)
        self.assertEqual(view.build(page1, False, self.fixture), 0)
        self.assertEqual(view.build(page2, False, self.fixture), 0)
        unit1 = view.view_paths(page1)[1]
        manifest1 = view.read_json(unit1 / "manifest.json")
        failures = view.check_fixture(page1, unit1, manifest1, self.fixture)
        current_digest = view.source_receipt(page1.resolve(), unit1, manifest1)[0]
        built_digest = view.read_json(
            self.fixture / "views" / page1.stem / "build-manifest.json"
        )["source_digest"]
        self.assertFalse(failures, f"{failures}; built={built_digest}; current={current_digest}")
        self.assertTrue((self.fixture / "displays" / folder1 / "manifest.json").is_file())
        self.assertTrue((self.fixture / "displays" / folder2 / "manifest.json").is_file())
        self.assertIn("@article{qt1", (self.fixture / "references.bib").read_text())
        self.assertIn("@article{qt2", (self.fixture / "references.bib").read_text())
        public_files = {path.name for path in (self.fixture / "displays" / folder1).rglob("*")}
        self.assertNotIn("output.md", public_files)
        self.assertNotIn("manifest.yaml", public_files)
        self.assertNotIn("recipe", public_files)

        manifest_path = self.pages / "views" / page1.stem / "manifest.json"
        manifest = json.loads(manifest_path.read_text())
        manifest["displays"] = []
        manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")
        self.assertEqual(view.build(page1, False, self.fixture), 0)
        self.assertFalse((self.fixture / "displays" / folder1).exists())
        self.assertTrue((self.fixture / "displays" / folder2).is_dir())

    @unittest.skipUnless(shutil.which("xelatex"), "xelatex is required for fixture tests")
    def test_conflicting_bib_key_is_refused(self) -> None:
        page1 = self.make_view("QT1-for-view", "shared", "First definition")
        page2 = self.make_view("QT2-for-view", "shared", "Conflicting definition")
        self.assertEqual(view.build(page1, False, self.fixture), 0)
        self.assertEqual(view.build(page2, False, self.fixture), 1)
        bibliography = (self.fixture / "references.bib").read_text()
        self.assertIn("First definition", bibliography)
        self.assertNotIn("Conflicting definition", bibliography)


if __name__ == "__main__":
    unittest.main()
