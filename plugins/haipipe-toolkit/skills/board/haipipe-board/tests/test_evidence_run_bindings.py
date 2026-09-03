"""Evidence run bindings are pointers, never copied run artifacts."""
import importlib.util
import tempfile
import unittest
from pathlib import Path


ENGINE = Path(__file__).resolve().parent.parent
SPEC = importlib.util.spec_from_file_location(
    "evidence_status", ENGINE / "cli" / "evidence-status.py",
)
evidence_status = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(evidence_status)

from live.evidence import (  # noqa: E402
    _evidence_cards, _md_lite, _run_binding_cards, render,
)


ITEMS = """# S-Test · evidence items
page: S-Test

### E01-CITE-opening · C1.P1.B1 · opening citation
- **Expected**: CITE · verified source
- **Acceptance**: source identity resolves
- **Supporting Runs**: Discovery · new-run · b01j01t01; Discovery · rerun · b01j01t02r01
- **PageX Bindings**: []
- **Local Input**: selected source
- **Local Run**: — Design Page Evidence Task
- **Decide**: ☑ make
"""


class EvidenceRunBindingsTest(unittest.TestCase):
    def test_records_supporting_and_local_lineage_without_minting_a_run(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "pyproject.toml").write_text("[project]\nname='fixture'\n", encoding="utf-8")
            (root / "code").mkdir()
            page = root / "S-Test" / "S-Test.md"
            (page.parent / "outline").mkdir(parents=True)
            page.write_text("# Test\n", encoding="utf-8")
            (page.parent / "outline" / "S-Test-evidence-items.md").write_text(ITEMS, encoding="utf-8")

            text = evidence_status.build_run_bindings(page)

        self.assertIn("kind: evidence-runs · ⚙️ derived · never hand-edited · pointers only", text)
        self.assertIn("`b01.j01.t01` · newrun · Run not allocated", text)
        self.assertIn("`b01.j01.t02.r01` · rerun · Run/Result paths not found", text)
        self.assertIn("planned local Evidence Task · Run not allocated", text)
        self.assertNotIn("b01.j01.t01.r01", text)
        self.assertIn("supporting Runs/Results stay external", text)

    def test_allocated_local_ticket_without_result_is_linked_end_to_end(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "pyproject.toml").write_text("[project]\nname='fixture'\n", encoding="utf-8")
            (root / "code").mkdir()
            page = root / "S-Test" / "S-Test.md"
            outline = page.parent / "outline"
            outline.mkdir(parents=True)
            page.write_text("# Test\n", encoding="utf-8")
            (outline / "S-Test-evidence-items.md").write_text(
                """### E01-VALUE-result · C1.P1.B1 · result
- **Expected**: VALUE · estimate
- **Acceptance**: matches specification
- **Supporting Runs**: []
- **PageX Bindings**: []
- **Local Input**: frozen inputs
- **Local Run**: Page · Evidence Item · registered · b02.j01.t01.r01
- **Decide**: ☑ make
""",
                encoding="utf-8",
            )
            ticket = page.parent / "runs" / "b02.j01.t01.r01.sh"
            ticket.parent.mkdir()
            ticket.write_text("#!/bin/sh\n", encoding="utf-8")

            binding = evidence_status.build_run_bindings(page)
            rendered = _run_binding_cards(binding)

        self.assertIn("[b02.j01.t01.r01](/S-Test/runs/b02.j01.t01.r01.sh)", binding)
        self.assertIn("Result not found", binding)
        self.assertIn('href="/S-Test/runs/b02.j01.t01.r01.sh"', rendered)
        self.assertIn('<code>b02.j01.t01.r01</code><small>run only</small>', rendered)
        self.assertIn('<span>no result</span>', rendered)

    def test_run_binding_links_render_but_unsafe_markdown_urls_do_not(self):
        html = _md_lite(
            "- [b03.j01.t01.r01](/examples/Project/runs/r01.ps1) · [Result](/examples/Project/results/r01/runtime.yaml)\n"
            "- [bad](javascript:alert(1))\n"
        )
        self.assertIn('href="/examples/Project/runs/r01.ps1"', html)
        self.assertIn('href="/examples/Project/results/r01/runtime.yaml"', html)
        self.assertNotIn('href="javascript:', html)

    def test_run_binding_headings_accept_item_deep_links(self):
        html = _md_lite(
            "## E01-CITE-opening · C1.P1.B1 · opening citation\n",
            heading_prefix="run-",
        )
        self.assertIn('id="run-E01-CITE-opening"', html)

    def test_run_binding_cards_are_compact_clickable_and_hide_repeated_copy(self):
        binding = """# S-Test · evidence run bindings
page: S-Test
kind: evidence-runs · derived

## E02-VALUE-linked-design-counts · C2.P1.B3 · corpus, linkage, sample, and model receipt
- **Supporting Runs**:
  - `b01.j01.t04` · newrun · Run not allocated
  - [b03.j01.t01.r01](/examples/Project/task/runs/r01.ps1) · rerun · Rerun · [Run](/examples/Project/task/runs/r01.ps1) · [Result](/examples/Project/task/results/r01/runtime.yaml)
  - [b03.j02.t01.r04](/examples/Project/task/runs/r04.ps1) · rerun · Run only · [Run](/examples/Project/task/runs/r04.ps1) · Result not found
- **Local Run**: planned local Evidence Task · Run not allocated
- **Local Result**: not allocated
"""
        html = _run_binding_cards(binding)
        self.assertIn('id="run-E02-VALUE-linked-design-counts"', html)
        self.assertIn('<code class=runmap-eid>E02</code>', html)
        self.assertIn('linked design counts', html)
        self.assertIn('class=runmap-type>VALUE</span>', html)
        self.assertIn('href="/examples/Project/task/runs/r01.ps1"', html)
        self.assertIn('<code>b03.j01.t01.r01</code><small>rerun</small>', html)
        self.assertIn('<code>b03.j02.t01.r04</code><small>run only</small>', html)
        self.assertIn('Run &amp; Result paths', html)
        self.assertIn('<b>Run</b><code>/examples/Project/task/runs/r01.ps1</code>', html)
        self.assertIn('<b>Result</b><code>/examples/Project/task/results/r01/runtime.yaml</code>', html)
        self.assertIn('href="/examples/Project/task/results/r01/runtime.yaml"', html)
        self.assertIn('<b>Local</b><span>not allocated</span>', html)
        self.assertNotIn('<h2', html)
        self.assertNotIn('<li>', html)
        self.assertNotIn('Supporting Runs:', html)

    def test_run_binding_cards_reject_unsafe_run_links(self):
        binding = """## E01-CITE-opening · C1.P1.B1 · opening citation
- **Supporting Runs**:
  - [b01.j01.t01.r01](javascript:alert(1)) · ready · [Run](javascript:alert(1))
- **Local Run**: not allocated
- **Local Result**: not allocated
"""
        html = _run_binding_cards(binding)
        self.assertNotIn('href="javascript:', html)

    def test_allocated_local_run_is_clickable_and_keeps_receipt_in_details(self):
        binding = """## E01-VALUE-result · C1.P1.B1 · result
- **Supporting Runs**:
  - —
- **Local Run**: [b02.j01.t01.r01](/Page/runs/r01.ps1) · Ready · [Run](/Page/runs/r01.ps1) · [Result](/Page/results/r01/runtime.yaml)
- **Local Result**: b02.j01.t01.r01
"""
        html = _run_binding_cards(binding)
        self.assertIn('href="/Page/runs/r01.ps1"', html)
        self.assertIn('<code>b02.j01.t01.r01</code><small>ready</small>', html)
        self.assertIn('href="/Page/results/r01/runtime.yaml"', html)

    def test_allocated_local_ticket_stays_visible_before_result_exists(self):
        binding = """## E01-VALUE-result · C1.P1.B1 · result
- **Supporting Runs**:
  - —
- **Local Run**: [b02.j01.t01.r01](/Page/runs/r01.ps1) · Run only · [Run](/Page/runs/r01.ps1) · Result not found
- **Local Result**: not allocated
"""
        html = _run_binding_cards(binding)
        self.assertIn('href="/Page/runs/r01.ps1"', html)
        self.assertIn('<code>b02.j01.t01.r01</code><small>run only</small>', html)
        self.assertIn('<span>no result</span>', html)
        self.assertNotIn('<b>Local</b><span>not allocated</span>', html)

    def test_by_bullet_cards_hide_generated_file_mechanics_and_compact_runs(self):
        snapshot = """# S-Test · evidence status
page: S-Test
kind: evidence · derived
# --- evidence-status:begin (generated) ---
  EVIDENCE STATUS, MEASURED 260902 2251. GENERATED; do not hand-edit.
  regenerate: cli/evidence-status.py S-Test.md
plan: v5 · approved: ✅ · cycle: SURVEY · items 1 · decided 1/1 · VALUE 1 · specified 1

### E01-VALUE-result · C2.P1.B4 · primary association
- **Status**: 📝 specified
- **Type**: VALUE
- **Expected**: VALUE · estimate and uncertainty
- **Acceptance**: matches the primary specification
- **Supporting Runs**: Execution · rerun · b03j01t01r01; Discovery · new-run · b01j01t04
- **Local Input**: smoke receipt must rerun
- **Local Run**: Page · Evidence Item · registered · b02j01t01r01
- **Has**: local Result not ready
# --- evidence-status:end ---
"""
        html = _evidence_cards(snapshot)
        self.assertIn('class=evcard', html)
        self.assertIn('b03.j01.t01.r01', html)
        self.assertIn('b01.j01.t04', html)
        self.assertIn('class="runfam execution">X</b>', html)
        self.assertIn('class="runfam discovery">D</b>', html)
        self.assertIn('class="runfam paper">P</b>', html)
        self.assertIn("j01.t01.r01", html)
        self.assertIn('class=runact>new</span>', html)
        self.assertIn('survey details', html)
        self.assertNotIn('evidence-status:begin', html)
        self.assertNotIn('regenerate:', html)
        self.assertNotIn('EVIDENCE STATUS', html)

    def test_evidence_item_joins_run_items_under_one_canonical_identity(self):
        snapshot = """plan: v5 · approved: ✅ · cycle: SURVEY · items 1 · decided 1/1 · VALUE 1

### E01-VALUE-lbp-main-effect · C2.P1.B4 · LBP association and benchmark
- **Status**: 📝 specified
- **Type**: VALUE
- **Label**: LBPEffect
- **Expected**: VALUE · estimate and interval
- **Acceptance**: matches the primary specification
- **Supporting Runs**: Execution · rerun · b03j01t01r01
- **Local Input**: frozen aggregate inputs
- **Local Run**: — Design Page Evidence Task
- **Has**: local Result not ready
"""
        bindings = """## E01-VALUE-lbp-main-effect · C2.P1.B4 · LBP association and benchmark
- **Supporting Runs**:
  - [b03.j01.t01.r01](/examples/Project/tasks/T1/runs/r01.ps1) · rerun · Rerun · [Run](/examples/Project/tasks/T1/runs/r01.ps1) · [Result](/examples/Project/tasks/T1/results/r01/runtime.yaml)
- **Local Run**: planned local Evidence Task · Run not allocated
- **Local Result**: not allocated
"""

        html = _evidence_cards(snapshot, bindings)

        self.assertEqual(html.count("class=evcard"), 1)
        self.assertIn('id="run-E01-VALUE-lbp-main-effect"', html)
        self.assertIn('title="E01-VALUE-lbp-main-effect">E1V.LBPEffect</code>', html)
        self.assertIn('<b>Supporting runs</b>', html)
        self.assertIn('href="/examples/Project/tasks/T1/runs/r01.ps1"', html)
        self.assertIn('Run &amp; Result paths', html)
        self.assertIn('<b>Run</b><code>/examples/Project/tasks/T1/runs/r01.ps1</code>', html)
        self.assertIn('<b>Result</b><code>/examples/Project/tasks/T1/results/r01/runtime.yaml</code>', html)
        self.assertNotIn('class=runmap-card', html)
        self.assertNotIn('Ticket', html)
        self.assertNotIn('Receipt', html)

    def test_evidence_surface_has_one_items_panel_but_no_retired_probe_segment(self):
        with tempfile.TemporaryDirectory() as temp:
            page = Path(temp) / "S-Test" / "S-Test.md"
            (page.parent / "outline").mkdir(parents=True)
            page.write_text("# Test\n", encoding="utf-8")
            (page.parent / "outline" / "S-Test-evidence.md").write_text(
                "# Evidence\n", encoding="utf-8"
            )

            html = render(page, "/examples/Board/board/QA/S-Test.html", "QA/S-Test/S-Test.md")

        self.assertIn('data-seg=items', html)
        self.assertIn('🧾 Evidence Items', html)
        self.assertNotIn('data-seg=runlinks', html)
        self.assertNotIn('data-seg=bybullet', html)
        self.assertIn("requestedSeg === 'runlinks'", html)
        self.assertIn("new URLSearchParams(location.search)", html)
        self.assertIn("board-outline-evidence-focus", html)
        self.assertIn("target.classList.add('run-focus')", html)
        self.assertNotIn('data-seg=probe', html)
        self.assertNotIn('🚪 Cards', html)


if __name__ == "__main__":
    unittest.main()
