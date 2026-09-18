"""The lightweight Page surface has four Outline workspaces."""
import tempfile
import unittest
from pathlib import Path

from live.evidence import render as render_evidence
from live.outline import parse_outline, render as render_outline
from live.runs import render as render_runs


class OutlineV4WorkspaceTest(unittest.TestCase):

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.folder = Path(self.temp.name) / "S-Test"
        self.folder.mkdir()
        self.page = self.folder / "S-Test.md"
        self.page.write_text(
            "# Test\n\n## 🚪 Opening\n\nShort opening.\n\n## 🧭 Outline\n\n"
            "## Content\n\n### 1 · Claim\n\nText.\n\n## Aims\n",
            encoding="utf-8",
        )
        outline = self.folder / "outline"
        outline.mkdir()
        (outline / "S-Test-outline-v1.0.md").write_text(
            "# Plan\noutline-version: v1.0\napproved: ⬜\n\n"
            "## C1 · Claim\n### C1.P1 · Main move\n"
            "- B1 · State the estimate\n"
            "  Evidence: E01-VALUE-estimate · estimate and interval\n"
            "  Accept: frozen result\n",
            encoding="utf-8",
        )
        (outline / "S-Test-logic.mmd").write_text(
            "flowchart LR\nA[Claim] --> B[Evidence]\n", encoding="utf-8"
        )
        (outline / "S-Test-evidence.md").write_text(
            "### E01-VALUE-estimate · C1.P1.B1 · main estimate\n"
            "- **Type**: VALUE\n- **Expected**: estimate and interval\n",
            encoding="utf-8",
        )

        run = self.folder / "runs" / "pj01t01r01_estimate.sh"
        run.parent.mkdir()
        run.write_text(
            "---\nfamily: Page\noperation: evidence-item\n"
            "target: E01-VALUE-estimate\n"
            "result: results/pj01t01r01_estimate/result.yaml\n---\n#!/bin/sh\n",
            encoding="utf-8",
        )
        result = self.folder / "results" / "pj01t01r01_estimate"
        result.mkdir(parents=True)
        (result / "runtime.yaml").write_text(
            "global_id: p.j01.t01.r01\nfamily: Page\n"
            "operation: evidence-item\nstatus: complete\n"
            "target: E01-VALUE-estimate\n",
            encoding="utf-8",
        )
        (result / "result.yaml").write_text(
            "item: E01-VALUE-estimate\n"
            "type: VALUE\nrun: pj01t01r01\nstatus: complete\n"
            "supporting_results:\n"
            "- run: b01j01t01r01\n  kind: Discovery\n"
            "  result: examples/External/results/r01\n",
            encoding="utf-8",
        )

    def tearDown(self):
        self.temp.cleanup()

    def test_outline_has_only_the_four_requested_workspaces(self):
        body = render_outline(
            "S-Test", parse_outline(self.page.read_text(encoding="utf-8")),
            self.page, self.folder, "/board.md", "S-Test/S-Test.md",
        )
        for name in ("Draft Space", "Evidence Space", "Run Space", "Delivery Space"):
            self.assertEqual(body.count(">" + name + "</button>"), 1)
        self.assertIn("lens-delivery", body)
        self.assertIn("workspace=1", body)
        for removed in ("Context Workspace", "Page Records", "What is left", "Page details"):
            self.assertNotIn(removed, body)
        self.assertIn("logic-viewport", body)
        self.assertIn("paragraph-group", body)

    def test_evidence_is_result_first_and_minimal(self):
        body = render_evidence(self.page, "/board.md", "S-Test/S-Test.md")
        self.assertIn("E01-VALUE-estimate", body)
        self.assertIn("results/pj01t01r01_estimate/result.yaml", body)
        self.assertIn("Evidence Items", body)
        self.assertIn(">Values<", body)
        self.assertIn('data-evidence-type="VALUE"', body)
        self.assertIn("<details class=evidence-card", body)
        self.assertIn("Evidence Label", body)
        self.assertIn("Evidence Item", body)
        self.assertIn("Evidence Run", body)
        self.assertNotIn("<th>Evidence</th>", body)
        self.assertNotIn("<nav", body)

    def test_run_workspace_has_p_e_and_external_support(self):
        body = render_runs(self.page, "/board.md", "S-Test/S-Test.md")
        self.assertIn(">Paper Writing</button>", body)
        self.assertIn(">Evidence</button>", body)
        self.assertIn(">Supporting Runs</button>", body)
        self.assertIn(">Workflow map</button>", body)
        self.assertIn("Workflow by Space specification", body)
        self.assertIn("Spaces", body)
        self.assertIn("OutlinePlan + Mermaid", body)
        self.assertIn("runs/rp-struct-", body)
        self.assertIn('class="run-space-tab on"', body)
        self.assertIn('class="run-pill total">', body)
        self.assertIn("Writing Runs", body)
        self.assertIn("Evidence Items", body)
        self.assertIn("Discoveries", body)
        self.assertIn("<h3>Value</h3>", body)
        self.assertIn("<h3>Display</h3>", body)
        self.assertIn("<h3>Citation</h3>", body)
        self.assertIn("class=run-card", body)
        self.assertEqual(body.count('class="run-space-tab'), 4)
        self.assertEqual(body.count('class="run-space-panel'), 4)
        self.assertNotIn("<th>", body)
        self.assertIn("P j01.t01.r01", body)
        self.assertIn("b01.j01.t01.r01", body)
        self.assertNotIn("<h2>Task Runs</h2>", body)
        self.assertNotIn("<summary>Scripts", body)

        selected = render_runs(self.page, "/board.md", "S-Test/S-Test.md",
                               "P j01.t01.r01")
        self.assertIn('class="run-space-tab on" id="run-space-tab-evidence"', selected)
        self.assertIn(
            '<section class="run-space-panel on" id="run-space-panel-evidence"',
            selected,
        )

        mapped = render_runs(self.page, "/board.md", "S-Test/S-Test.md",
                             selected_space="map")
        self.assertIn('class="run-space-tab on" id="run-space-tab-map"', mapped)
        self.assertIn(
            '<section class="run-space-panel on" id="run-space-panel-map"',
            mapped,
        )


if __name__ == "__main__":
    unittest.main()
