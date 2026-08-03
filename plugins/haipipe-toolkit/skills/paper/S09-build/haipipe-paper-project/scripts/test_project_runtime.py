#!/usr/bin/env python3
"""Disposable safety and determinism tests for project_runtime."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import project_runtime as runtime


SOURCE = """# S Main 1 · Introduction
state: ✅ GATED 2026-07-30
owner: Test

## Content
### §1 Introduction
#### P1. One paragraph
(one beat)

Evidence stays attached \\citep{key-a,key-b} [Q-Test-1].

> Citation: apparatus-only \\citep{TOADD} [Q-Apparatus-Only].

<!-- \\citep{COMMENTED} [Q-Comment-Only] -->

```text
\\citep{FENCED} [Q-Fence-Only]
```
"""


MANIFEST = """schema: haipipe.paper.projection/v1
master: Paper.tex
target_roots: [sections]
dependency_roots: []
candidate_root: 3-dist/tex
units:
  main-1:
    source:
      page: 0-lifecycle/4-main/S-Main-1-introduction.md
      select: content
    gate: S-Main-1
    entry: sections/01_introduction.tex
    outputs:
      - path: sections/01_introduction.tex
        role: prose
unreachable: []
"""


class RuntimeTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory(prefix="haipipe-project-test-")
        self.paper = Path(self.temp.name) / "Paper-Test"
        (self.paper / "0-lifecycle/4-main").mkdir(parents=True)
        (self.paper / "2-src").mkdir()
        (self.paper / "sections").mkdir()
        (self.paper / "0-lifecycle/4-main/S-Main-1-introduction.md").write_text(
            SOURCE, encoding="utf-8"
        )
        (self.paper / "sections/01_introduction.tex").write_text(
            "OLD SUBMISSION\n", encoding="utf-8"
        )
        (self.paper / "Paper.tex").write_text(
            "\\documentclass{article}\n"
            "\\usepackage{natbib}\n"
            "\\begin{document}\n"
            "\\input{sections/01_introduction}\n"
            "% \\input{displays/commented-out-and-missing}\n"
            "\\bibliographystyle{plain}\n"
            "\\bibliography{Paper}\n"
            "\\end{document}\n",
            encoding="utf-8",
        )
        (self.paper / "Paper.bib").write_text(
            "@article{key-a,title={A},author={Author, A},journal={J},year={2025}}\n"
            "@article{key-b,title={B},author={Author, B},journal={J},year={2026}}\n",
            encoding="utf-8",
        )
        (self.paper / "2-src/projection.yaml").write_text(MANIFEST, encoding="utf-8")

    def tearDown(self) -> None:
        self.temp.cleanup()

    def context(self) -> runtime.Context:
        return runtime.load_context(str(self.paper), None)

    def test_generate_is_isolated_deterministic_and_checkable(self) -> None:
        ctx = self.context()
        self.assertEqual(runtime.validate_context(ctx)["G0"], "pass")
        before = (self.paper / "sections/01_introduction.tex").read_bytes()

        first = runtime.generate(ctx, ["main-1"])
        second = runtime.generate(ctx, ["main-1"])
        self.assertEqual(first["candidate_id"], second["candidate_id"])
        self.assertFalse(first["reused"])
        self.assertTrue(second["reused"])
        generate_receipt = json.loads((self.paper / first["receipt"]).read_text(encoding="utf-8"))
        self.assertIn("main-1", generate_receipt["source_hashes"])
        self.assertEqual(
            (self.paper / "sections/01_introduction.tex").read_bytes(),
            before,
            "generate must never write the submission tree",
        )

        candidate = self.paper / first["candidate"]
        checked = runtime.check_candidate(
            ctx, candidate, compile_requested=False, write_check_receipt=False
        )
        self.assertEqual(checked["gates"]["G3"], "pass")
        tex = (candidate / "sections/01_introduction.tex").read_text(encoding="utf-8")
        self.assertIn("\\citep{key-a,key-b}", tex)
        self.assertIn("[Q-Test-1]", tex)
        self.assertNotIn("TOADD", tex)
        self.assertNotIn("[Q-Apparatus-Only]", tex)
        recorded_check = runtime.check_candidate(
            ctx, candidate, compile_requested=False, write_check_receipt=True
        )
        check_receipt = json.loads(
            (self.paper / recorded_check["receipt"]).read_text(encoding="utf-8")
        )
        self.assertIn("manifest_sha256", check_receipt)
        self.assertIn("main-1", check_receipt["source_hashes"])

        (self.paper / "Paper.bib").write_text(
            (self.paper / "Paper.bib").read_text(encoding="utf-8") + "% dependency change\n",
            encoding="utf-8",
        )
        changed_dependency = runtime.generate(ctx, ["main-1"])
        self.assertNotEqual(first["candidate_id"], changed_dependency["candidate_id"])

    def test_g3_is_independent_of_renderer_output(self) -> None:
        original_renderer = runtime.markdown_to_tex

        def dropping_renderer(markdown: str, source_rel: str, selector: str) -> str:
            return original_renderer(markdown, source_rel, selector).replace(
                "\\citep{key-a,key-b} [Q-Test-1]", "renderer silently dropped bindings"
            )

        with mock.patch.object(runtime, "markdown_to_tex", side_effect=dropping_renderer):
            ctx = self.context()
            generated = runtime.generate(ctx, ["main-1"])
            candidate = self.paper / generated["candidate"]
            with self.assertRaisesRegex(runtime.ProjectionError, "G3 evidence"):
                runtime.check_candidate(
                    ctx, candidate, compile_requested=False, write_check_receipt=False
                )

    def test_malicious_candidate_root_is_rejected(self) -> None:
        bad = MANIFEST.replace("candidate_root: 3-dist/tex", "candidate_root: .")
        (self.paper / "2-src/projection.yaml").write_text(bad, encoding="utf-8")
        with self.assertRaisesRegex(runtime.ProjectionError, "candidate_root"):
            self.context()

    def test_output_escape_is_rejected(self) -> None:
        bad = MANIFEST.replace(
            "path: sections/01_introduction.tex", "path: ../../outside.tex"
        )
        (self.paper / "2-src/projection.yaml").write_text(bad, encoding="utf-8")
        ctx = self.context()
        with self.assertRaisesRegex(runtime.ProjectionError, "unsafe"):
            runtime.validate_context(ctx)

    def test_gate_id_must_resolve_to_one_s_page(self) -> None:
        bad = MANIFEST.replace("gate: S-Main-1", "gate: WRONG-GATE")
        (self.paper / "2-src/projection.yaml").write_text(bad, encoding="utf-8")
        ctx = self.context()
        with self.assertRaisesRegex(runtime.ProjectionError, "gate must be a valid S-page id"):
            runtime.generate(ctx, ["main-1"])

    def test_promotion_requires_token_and_rolls_through_backup(self) -> None:
        ctx = self.context()
        generated = runtime.generate(ctx, ["main-1"])
        candidate = self.paper / generated["candidate"]
        with self.assertRaisesRegex(runtime.ProjectionError, "literal approval token"):
            runtime.promote(ctx, candidate, "", "Reviewer", "accept exact candidate")

        result = runtime.promote(
            ctx, candidate, "PROMOTE", "Reviewer", "accept exact candidate"
        )
        self.assertEqual(result["gates"]["G5"], "pass")
        self.assertIn("GENERATED from", (self.paper / "sections/01_introduction.tex").read_text())
        self.assertTrue((self.paper / result["backup_root"] / "sections/01_introduction.tex").is_file())

    def test_blocked_compile_writes_a_check_receipt(self) -> None:
        master = self.paper / "Paper.tex"
        master.write_text(
            master.read_text(encoding="utf-8").replace(
                "\\begin{document}\n",
                "\\begin{document}\n\\input{displays/active-and-missing}\n",
            ),
            encoding="utf-8",
        )
        ctx = self.context()
        generated = runtime.generate(ctx, ["main-1"])
        candidate = self.paper / generated["candidate"]
        before = set((self.paper / "2-src/projection-receipts").glob("*-check-*.json"))
        with self.assertRaisesRegex(runtime.ProjectionError, "G4 blocked"):
            runtime.check_candidate(
                ctx, candidate, compile_requested=True, write_check_receipt=True
            )
        after = set((self.paper / "2-src/projection-receipts").glob("*-check-*.json"))
        self.assertEqual(len(after - before), 1)
        receipt = json.loads(next(iter(after - before)).read_text(encoding="utf-8"))
        self.assertEqual(receipt["status"], "blocked")
        self.assertEqual(receipt["gates"]["G4"], "blocked")

    def test_workspace_runtime_has_no_recursive_delete(self) -> None:
        source = Path(runtime.__file__).read_text(encoding="utf-8")
        self.assertNotIn("rmtree(", source)


if __name__ == "__main__":
    unittest.main()
