from __future__ import annotations

import hashlib
import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import yaml


CLI_DIR = Path(__file__).resolve().parents[1] / "cli"
SPEC = importlib.util.spec_from_file_location(
    "promote_paragraph", CLI_DIR / "promote_paragraph.py"
)
assert SPEC and SPEC.loader
promote_paragraph = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = promote_paragraph
SPEC.loader.exec_module(promote_paragraph)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


class PromoteParagraphTest(unittest.TestCase):
    def make_result(
        self,
        root: Path,
        page: Path,
        target: str,
        paragraph: str,
        *,
        status: str = "complete",
        result_ref: str = ".",
        trace_extra: str = "Style verdict: pass",
    ) -> Path:
        results_root = root / "results"
        results_root.mkdir(exist_ok=True)
        run_number = len(list(results_root.iterdir())) + 1
        result_dir = results_root / (
            f"r{run_number:02d}_page-writing_{target.lower().replace('.', '-')}"
        )
        result_dir.mkdir(parents=True)
        (result_dir / "paragraph.md").write_text(paragraph + "\n", encoding="utf-8")
        (result_dir / "trace.md").write_text(
            f"# Trace\n\nTarget: {target}\n\n{trace_extra}\n", encoding="utf-8"
        )
        runtime = {
            "run": result_dir.name,
            "family": "page",
            "operation": "paragraph-writing",
            "target": target,
            "ticket": "runs/r01.md",
            "result": result_ref,
            "inputs": [
                {
                    "role": "page-source",
                    "path": page.name,
                    "sha256": sha256(page.read_bytes()),
                }
            ],
            "worker": "haipipe-page-content",
            "status": status,
        }
        (result_dir / "runtime.yaml").write_text(
            yaml.safe_dump(runtime, sort_keys=False), encoding="utf-8"
        )
        return result_dir

    def test_replaces_only_target_and_records_idempotent_receipt(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            page = root / "page.md"
            page.write_text(
                "## Content\n"
                "\n"
                "### 1 · First\n"
                "\n"
                "Old first paragraph.\n"
                "\n"
                "<!-- keep this annotation -->\n"
                "\n"
                "Old second paragraph.\n"
                "\n"
                "### 2 · Second\n"
                "\n"
                "Other division stays.\n",
                encoding="utf-8",
            )
            result = self.make_result(root, page, "C1.P1", "New first paragraph.")

            outcome = promote_paragraph.promote(page, result)

            self.assertEqual(outcome["status"], "promoted")
            page_text = page.read_text(encoding="utf-8")
            self.assertIn("New first paragraph.", page_text)
            self.assertIn("Old second paragraph.", page_text)
            self.assertIn("<!-- keep this annotation -->", page_text)
            self.assertIn("Other division stays.", page_text)
            runtime = yaml.safe_load(
                (result / "runtime.yaml").read_text(encoding="utf-8")
            )
            self.assertEqual(runtime["promotion"]["status"], "promoted")
            self.assertEqual(
                runtime["promotion"]["page_after_sha256"], sha256(page.read_bytes())
            )

            repeated = promote_paragraph.promote(page, result)
            self.assertEqual(repeated["status"], "already-promoted")
            self.assertEqual(page.read_text(encoding="utf-8"), page_text)

    def test_inserts_next_unheaded_paragraph_with_separators(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            page = root / "page.md"
            page.write_text(
                "## Content\n\n### 1 · Only\n\nExisting paragraph.\n\n"
                "### 2 · Next\n\nNext division.\n",
                encoding="utf-8",
            )
            result = self.make_result(root, page, "C1.P2", "Inserted paragraph.")

            promote_paragraph.promote(page, result)

            self.assertIn(
                "Existing paragraph.\n\nInserted paragraph.\n\n### 2 · Next",
                page.read_text(encoding="utf-8"),
            )

    def test_replaces_explicit_paragraph_heading_body(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            page = root / "page.md"
            page.write_text(
                "## Content\n\n### 1 · Explicit\n\n#### 1.1\n\nFirst.\n\n"
                "#### 1.2\n\nSecond old.\n",
                encoding="utf-8",
            )
            result = self.make_result(root, page, "C1.P2", "Second new.")

            promote_paragraph.promote(page, result)

            text = page.read_text(encoding="utf-8")
            self.assertIn("#### 1.1\n\nFirst.", text)
            self.assertIn("#### 1.2\n\nSecond new.", text)

    def test_explicit_heading_with_two_prose_blocks_is_refused(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            page = root / "page.md"
            page.write_text(
                "## Content\n\n### 1 · Explicit\n\n#### 1.1\n\nFirst block.\n\n"
                "Second block.\n",
                encoding="utf-8",
            )
            result = self.make_result(root, page, "C1.P1", "Replacement.")

            with self.assertRaisesRegex(
                promote_paragraph.PromotionError, "more than one prose block"
            ):
                promote_paragraph.promote(page, result)
            self.assertIn(
                "First block.\n\nSecond block.", page.read_text(encoding="utf-8")
            )

    def test_stale_page_is_refused_without_writing(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            page = root / "page.md"
            page.write_text("## Content\n\n### 1\n\nOriginal.\n", encoding="utf-8")
            result = self.make_result(root, page, "C1.P1", "Replacement.")
            page.write_text(
                "## Content\n\n### 1\n\nConcurrent edit.\n", encoding="utf-8"
            )

            with self.assertRaisesRegex(
                promote_paragraph.PromotionError, "stale promotion"
            ):
                promote_paragraph.promote(page, result)
            self.assertIn("Concurrent edit.", page.read_text(encoding="utf-8"))

    def test_page_change_after_preparation_is_refused_before_page_write(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            page = root / "page.md"
            page.write_text("## Content\n\n### 1\n\nOriginal.\n", encoding="utf-8")
            result = self.make_result(root, page, "C1.P1", "Replacement.")
            original_atomic_write = promote_paragraph._atomic_write

            def mutate_after_runtime(path: Path, text: str) -> None:
                original_atomic_write(path, text)
                if path.resolve() == (result / "runtime.yaml").resolve():
                    page.write_text(
                        "## Content\n\n### 1\n\nConcurrent edit.\n", encoding="utf-8"
                    )

            with mock.patch.object(
                promote_paragraph, "_atomic_write", side_effect=mutate_after_runtime
            ):
                with self.assertRaisesRegex(
                    promote_paragraph.PromotionError, "changed during promotion"
                ):
                    promote_paragraph.promote(page, result)
            self.assertIn("Concurrent edit.", page.read_text(encoding="utf-8"))

    def test_fenced_heading_is_not_a_paragraph_address(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            page = root / "page.md"
            page.write_text(
                "## Content\n\n### 1\n\n```md\n#### not a paragraph\n```\n"
                "\nReal paragraph.\n",
                encoding="utf-8",
            )
            result = self.make_result(root, page, "C1.P1", "Real paragraph replaced.")

            promote_paragraph.promote(page, result)

            text = page.read_text(encoding="utf-8")
            self.assertIn("#### not a paragraph", text)
            self.assertIn("Real paragraph replaced.", text)

    def test_structural_or_blocked_result_is_refused(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            page = root / "page.md"
            page.write_text(
                "## Content\n\n### 1\n\nOld paragraph.\n> citation lane\n",
                encoding="utf-8",
            )
            result = self.make_result(root, page, "C1.P1", "Replacement.")

            with self.assertRaises(promote_paragraph.PromotionError):
                promote_paragraph.promote(page, result)
            self.assertIn("Old paragraph.", page.read_text(encoding="utf-8"))

            blocked = self.make_result(
                root,
                page,
                "C1.P1",
                "Replacement.",
                trace_extra="status: blocked",
            )
            with self.assertRaisesRegex(
                promote_paragraph.PromotionError, "upstream block"
            ):
                promote_paragraph.promote(page, blocked)


if __name__ == "__main__":
    unittest.main()
