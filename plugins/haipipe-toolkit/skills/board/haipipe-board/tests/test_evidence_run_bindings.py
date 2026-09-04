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
    _evidence_cards, _md_lite, _related_run_cards, _run_binding_cards, render,
)


ITEMS = """# S-Test · evidence items
page: S-Test

### E01-CITE-opening · C1.P1.B1 · opening citation
- **Expected**: CITE · verified source
- **Acceptance**: source identity resolves
- **Supporting Runs**: Discovery · new-run · b01j01t01; Discovery · rerun · b01j01t02r01
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
        self.assertIn('<code>/S-Test/runs/b02.j01.t01.r01.sh</code>', rendered)
        self.assertNotIn('href="/S-Test/runs/b02.j01.t01.r01.sh"', rendered)
        self.assertIn('<code>b02.j01.t01.r01</code><small>run</small>', rendered)
        self.assertIn('<b>Availability</b><span>Run exists · Result missing</span>', rendered)
        self.assertIn('<b>Next action</b><span>Run</span>', rendered)
        self.assertIn('<span>no result</span>', rendered)

    def test_run_binding_links_render_but_unsafe_markdown_urls_do_not(self):
        html = _md_lite(
            "- [b03.j01.t01.r01](/examples/Project/runs/r01.ps1) · [Result](/examples/Project/results/r01/runtime.yaml)\n"
            "- [bad](javascript:alert(1))\n"
        )
        self.assertIn('href="/examples/Project/runs/r01.ps1"', html)
        self.assertIn('href="/examples/Project/results/r01/runtime.yaml"', html)
        self.assertNotIn('href="javascript:', html)

    def test_legacy_receipt_link_is_rendered_as_runtime(self):
        binding = """## E01-VALUE-result · C1.P1.B1 · result
- **Supporting Runs**:
  - [b03.j01.t01.r01](/task/runs/r01.ps1) · rerun · Rerun · [Run](/task/runs/r01.ps1) · [Receipt](/task/results/r01/runtime.yaml)
- **Local Run**: not allocated
- **Local Result**: not allocated
"""

        html = _run_binding_cards(binding)

        self.assertIn('<b>Runtime</b><code>/task/results/r01/runtime.yaml</code>', html)
        self.assertNotIn('<b>Result</b><code>/task/results/r01/runtime.yaml</code>', html)

    def test_runtime_receipt_is_not_mislabeled_as_result(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            ticket = root / "task" / "runs" / "r01.ps1"
            runtime = root / "task" / "results" / "r01" / "runtime.yaml"
            ticket.parent.mkdir(parents=True)
            runtime.parent.mkdir(parents=True)
            ticket.write_text("# run\n", encoding="utf-8")
            runtime.write_text("status: incomplete\n", encoding="utf-8")
            registry = {"b03j01t01r01": {
                "ticket": str(ticket.relative_to(root)),
                "runtime": str(runtime.relative_to(root)),
                "result": "",
                "label": "Rerun",
            }}

            binding = evidence_status._run_ref(
                "Execution", "rerun", "b03j01t01r01", registry, root
            )
            rendered = _run_binding_cards(
                "## E01-VALUE-result · C1.P1.B1 · result\n"
                "- **Supporting Runs**:\n  - " + binding + "\n"
                "- **Local Run**: not allocated\n- **Local Result**: not allocated\n"
            )

        self.assertIn("Result not found", binding)
        self.assertIn("[Runtime](/task/results/r01/runtime.yaml)", binding)
        self.assertNotIn("[Result](/task/results/r01/runtime.yaml)", binding)
        self.assertIn('<b>Runtime</b><code>/task/results/r01/runtime.yaml</code>', rendered)

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
  - [b03.j02.t01.r04](/examples/Project/task/runs/r04.ps1) · run · Run only · [Run](/examples/Project/task/runs/r04.ps1) · Result not found
- **Local Run**: planned local Evidence Task · Run not allocated
- **Local Result**: not allocated
"""
        html = _run_binding_cards(binding)
        self.assertIn('id="run-E02-VALUE-linked-design-counts"', html)
        self.assertIn('<code class=runmap-eid>E02</code>', html)
        self.assertIn('linked design counts', html)
        self.assertIn('class=runmap-type>VALUE</span>', html)
        self.assertNotIn('href="/examples/Project/task/runs/r01.ps1"', html)
        self.assertIn('<code>b03.j01.t01.r01</code><small>rerun</small>', html)
        self.assertIn('<code>b03.j02.t01.r04</code><small>run</small>', html)
        self.assertIn('popovertarget="run-detail-E02-VALUE-linked-design-counts-support-1"', html)
        self.assertIn('data-run-address="b01.j01.t04"', html)
        self.assertIn('<b>Availability</b><span>Planned</span>', html)
        self.assertIn('<b>Next action</b><span>Allocate and run</span>', html)
        self.assertIn('Run &amp; Result paths', html)
        self.assertIn('<b>Run</b><code>/examples/Project/task/runs/r01.ps1</code>', html)
        self.assertIn('<b>Result</b><code>/examples/Project/task/results/r01/runtime.yaml</code>', html)
        self.assertNotIn('href="/examples/Project/task/results/r01/runtime.yaml"', html)
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

    def test_allocated_paper_local_run_is_clickable_and_keeps_result_in_details(self):
        binding = """## E01-VALUE-result · C1.P1.B1 · result
- **Supporting Runs**:
  - —
- **Local Run**: [P j01.t01.r01](/Page/runs/r01.ps1) · Ready · [Run](/Page/runs/r01.ps1) · [Result](/Page/results/r01/result.md)
- **Local Result**: P j01.t01.r01
"""
        html = _run_binding_cards(binding)
        self.assertIn('data-run-address="P j01.t01.r01"', html)
        self.assertIn('data-run-kind="local"', html)
        self.assertNotIn('href="/Page/runs/r01.ps1"', html)
        self.assertIn('<code>P j01.t01.r01</code><small>reuse</small>', html)
        self.assertIn('<b>Availability</b><span>Run + Result</span>', html)
        self.assertIn('<b>Next action</b><span>Reuse Result</span>', html)
        self.assertIn('<b>Result</b><code>/Page/results/r01/result.md</code>', html)
        self.assertNotIn('href="/Page/results/r01/result.md"', html)

    def test_allocated_local_ticket_stays_visible_before_result_exists(self):
        binding = """## E01-VALUE-result · C1.P1.B1 · result
- **Supporting Runs**:
  - —
- **Local Run**: [b02.j01.t01.r01](/Page/runs/r01.ps1) · Run only · [Run](/Page/runs/r01.ps1) · Result not found
- **Local Result**: not allocated
"""
        html = _run_binding_cards(binding)
        self.assertIn('<b>Run</b><code>/Page/runs/r01.ps1</code>', html)
        self.assertNotIn('href="/Page/runs/r01.ps1"', html)
        self.assertIn('<code>b02.j01.t01.r01</code><small>run</small>', html)
        self.assertIn('<span>no result</span>', html)
        self.assertNotIn('<b>Local</b><span>not allocated</span>', html)

    def test_proposed_paper_local_run_opens_planned_detail(self):
        snapshot = """plan: v1 · cycle: SURVEY · items 1 · decided 1/1 · VALUE 1

### E01-VALUE-result · C1.P1.B1 · result
- **Status**: specified
- **Type**: VALUE
- **Expected**: VALUE · estimate
- **Acceptance**: matches specification
- **Has**: local Result not ready
"""
        binding = """## E01-VALUE-result · C1.P1.B1 · result
- **Supporting Runs**:
  - —
- **Local Run**: P j01.t01.r01 · new · Run not allocated
- **Local Result**: not allocated
"""

        html = _evidence_cards(snapshot, binding)

        self.assertIn('data-run-address="P j01.t01.r01"', html)
        self.assertIn('<code>P j01.t01.r01</code><small>plan</small>', html)
        self.assertIn('<b>Plan</b><span>Produce the page-local VALUE Result for “result”: estimate.</span>', html)
        self.assertIn('<b>Availability</b><span>Planned</span>', html)
        self.assertIn('<b>Next action</b><span>Allocate and run</span>', html)
        self.assertNotIn('class=run-state', html)
        self.assertIn('<span class=missing>not allocated</span>', html)

    def test_unsurveyed_local_route_is_plain_missing_text(self):
        snapshot = """plan: v1 · cycle: SHAPE · items 1 · decided 0/1 · VALUE 1

### E06-VALUE-boundary · C1.P1.B1 · boundary
- **Status**: specified
- **Type**: VALUE
- **Expected**: VALUE · comparison
- **Acceptance**: comparable models
- **Has**: local Result not ready
"""
        binding = """## E06-VALUE-boundary · C1.P1.B1 · boundary
- **Supporting Runs**:
  - —
- **Local Run**: `not declared` · local Run path not found
- **Local Result**: not allocated
"""

        html = _evidence_cards(snapshot, binding)

        self.assertIn('<b>Local run</b><span>not allocated</span>', html)
        self.assertNotIn('data-run-address="not declared"', html)

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
        self.assertIn('data-run-kind="local"', html)
        self.assertIn("P j01.t01.r01", html)
        self.assertIn('<code>b01.j01.t04</code><small>plan</small>', html)
        self.assertIn('Design a Supporting Run for “primary association”', html)
        self.assertIn('popovertarget="run-detail-E01-VALUE-result-fallback-1"', html)
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
        self.assertNotIn('href="/examples/Project/tasks/T1/runs/r01.ps1"', html)
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
                """# Evidence
### E01-CITE-source · C1.P1.B1 · source
- **Type**: CITE
### E02-VALUE-effect · C1.P1.B2 · effect
- **Type**: VALUE
### E03-VALUE-bound · C1.P1.B3 · bound
- **Type**: VALUE
""", encoding="utf-8"
            )

            html = render(page, "/examples/Board/board/QA/S-Test.html", "QA/S-Test/S-Test.md")

        self.assertIn('data-seg=items', html)
        self.assertIn('🧾 Evidences · 3', html)
        self.assertIn('data-seg=runs', html)
        self.assertIn('⚙️ Runs · 0', html)
        self.assertIn('📚 Citations · 1', html)
        self.assertIn('🧮 Values · 2', html)
        self.assertIn('🖼 Displays · 0', html)
        self.assertNotIn('data-seg=pagex', html)
        self.assertNotIn('🔗 PageX', html)
        self.assertNotIn('data-seg=runlinks', html)
        self.assertNotIn('data-seg=bybullet', html)
        self.assertIn("requestedSeg === 'runlinks'", html)
        self.assertIn("new URLSearchParams(location.search)", html)
        self.assertIn("board-outline-evidence-focus", html)
        self.assertIn("board-outline-evidence-run", html)
        self.assertIn("function runKey(value, local)", html)
        self.assertIn("target.classList.add('run-focus')", html)
        self.assertIn("panel.showPopover()", html)
        self.assertNotIn('data-seg=probe', html)
        self.assertNotIn('🚪 Cards', html)

    def test_related_run_cards_are_grouped_by_evidence_and_report_unique_count(self):
        snapshot = """plan: v6 · cycle: SURVEY · items 2 · decided 2/2 · VALUE 2

### E01-VALUE-counts · C1.P1.B1 · linked design counts
- **Status**: planned
- **Type**: VALUE
- **Label**: Counts
- **Expected**: VALUE · linked cohort counts
- **Acceptance**: counts reconcile
- **Supporting Runs**: Execution · rerun · b03j01t01r01
- **Local Input**: frozen linked data
- **Local Run**: Page · Evidence Item · new-run · pj01t01r01

### E02-VALUE-effect · C1.P1.B2 · LBP effect
- **Status**: planned
- **Type**: VALUE
- **Label**: LBPEffect
- **Expected**: VALUE · estimate and interval
- **Acceptance**: model matches
- **Supporting Runs**: Execution · rerun · b03j01t01r01
- **Local Input**: frozen model input
- **Local Run**: Page · Evidence Item · new-run · pj01t02r01
"""
        bindings = """## E01-VALUE-counts · C1.P1.B1 · linked design counts
- **Supporting Runs**:
  - [b03.j01.t01.r01](/task/runs/r01_data.ps1) · rerun · Rerun · [Run](/task/runs/r01_data.ps1) · Result not found
- **Local Run**: P j01.t01.r01 · new · Run not allocated
- **Local Result**: not allocated

## E02-VALUE-effect · C1.P1.B2 · LBP effect
- **Supporting Runs**:
  - [b03.j01.t01.r01](/task/runs/r01_data.ps1) · rerun · Rerun · [Run](/task/runs/r01_data.ps1) · Result not found
- **Local Run**: P j01.t02.r01 · new · Run not allocated
- **Local Result**: not allocated
"""

        html, count = _related_run_cards(snapshot, bindings)

        self.assertEqual(count, 4)
        self.assertEqual(html.count('class=related-run-card'), 4)
        self.assertEqual(html.count('<code>b03.j01.t01.r01</code>'), 2)
        self.assertIn('4 Run mappings', html)
        self.assertIn('3 unique Runs', html)
        self.assertIn('2 Evidences', html)
        self.assertIn('class=related-evidence-group', html)
        self.assertIn('data; supports “linked design counts”.', html)
        self.assertIn('data; supports “LBP effect”.', html)
        self.assertIn('data-evidence-target="run-E01-VALUE-counts"', html)
        self.assertIn('data-evidence-target="run-E02-VALUE-effect"', html)
        self.assertIn('E1V.Counts', html)
        self.assertIn('E2V.LBPEffect', html)
        self.assertIn('<b>Run</b><code class=repo-path>/task/runs/r01_data.ps1</code>', html)
        self.assertNotIn('href="/task/runs/r01_data.ps1"', html)

    def test_render_counts_all_evidence_related_runs_in_internal_lens(self):
        with tempfile.TemporaryDirectory() as temp:
            page = Path(temp) / "S-Test" / "S-Test.md"
            support = page.parent / "outline" / "evidence" / "supporting-runs"
            support.mkdir(parents=True)
            page.write_text("# Test\n", encoding="utf-8")
            (page.parent / "outline" / "S-Test-evidence.md").write_text(
                """### E01-VALUE-effect · C1.P1.B1 · effect
- **Type**: VALUE
- **Label**: Effect
- **Expected**: VALUE · estimate
- **Supporting Runs**: Execution · rerun · b03j01t01r01
- **Local Run**: Page · Evidence Item · new-run · pj01t01r01
""", encoding="utf-8")
            (support / "S-Test-run-bindings.md").write_text(
                """## E01-VALUE-effect · C1.P1.B1 · effect
- **Supporting Runs**:
  - [b03.j01.t01.r01](/task/runs/r01.ps1) · rerun · Rerun · [Run](/task/runs/r01.ps1) · Result not found
- **Local Run**: P j01.t01.r01 · new · Run not allocated
- **Local Result**: not allocated
""", encoding="utf-8")

            html = render(page, "/examples/Board/board/QA/S-Test.html", "QA/S-Test/S-Test.md")

        self.assertIn('⚙️ Runs · 2', html)
        self.assertIn('<div id=runs style="display:none">', html)
        self.assertIn("runs: document.getElementById('runs')", html)
        self.assertIn("data-evidence-target", html)


if __name__ == "__main__":
    unittest.main()
