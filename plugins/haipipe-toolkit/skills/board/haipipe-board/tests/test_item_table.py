#!/usr/bin/env python3
"""Tests for the typed Evidence Item ledger and derived Page cycle."""
import os
import sys
import tempfile
import time
import unittest
from pathlib import Path

ENGINE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ENGINE))

from src import item_table as it

PLAN = """# QT2 · outline v1
approved: {tick}

## C1 · One
### C1.P1 · move
- B1 · the adjusted treatment estimate
  Note: report the focal estimate
  Evidence: E01-VALUE-adjusted-effect · estimate, interval, unit, population, and model label
  Accept: recomputes from the accepted model Result
- B2 · the guideline and figure
  Note: support and show the comparison
  Evidence: E02-CITE-guideline-anchor · verified guideline claim and locator
  Accept: source identity and locator resolve
  Evidence: E03-DISPLAY-effect-forest · forest plot ready to place
  Accept: preview, caption claim, and frozen intake exist
- B3 · no item here
  Note: nothing owed
"""

ITEMS = """# QT2 · evidence items
page: QT2
kind: evidence-items · authored
plan: v1

### E01-VALUE-adjusted-effect · C1.P1.B1 · adjusted treatment effect
- **Target**: C1.P1.B1
- **Need**: the focal estimate
- **Expected**: VALUE · estimate, interval, unit, population, and model label
- **Acceptance**: recomputes from the accepted model Result
- **Supporting Runs**: Execution · reuse · b01j01t01r01
- **PageX Bindings**: source/page/results/r01/result.yaml · authority b01j01t01r01
- **Local Input**: Supporting Results + PageX bindings
- **Local Run**: Page · Evidence Item · new-run · b02j01t01{arrow}
- **Decide**: {decide}

### E02-CITE-guideline-anchor · C1.P1.B2 · guideline anchor
- **Target**: C1.P1.B2
- **Need**: a verified source claim
- **Expected**: CITE · verified guideline claim and locator
- **Acceptance**: source identity and locator resolve
- **Supporting Runs**: Discovery · rerun · b01j02t01r03
- **PageX Bindings**: []
- **Local Input**: Supporting Results only
- **Local Run**: Page · Evidence Item · new-run · b02j01t01
- **Decide**: ☑ defer · awaiting source access

### E03-DISPLAY-effect-forest · C1.P1.B2 · effect forest
- **Target**: C1.P1.B2
- **Need**: a ready forest plot
- **Expected**: DISPLAY · forest plot ready to place
- **Acceptance**: preview, caption claim, and frozen intake exist
- **Supporting Runs**: []
- **PageX Bindings**: []
- **Local Input**: item contract only
- **Local Run**: Page · Evidence Item · new-run · b02j01t01
- **Decide**: ☑ drop · no longer needed
"""


def _register_runtime(root, global_id):
    """Create the minimum formal Ticket + planned runtime receipt for a test."""
    match = it._GLOBAL_RUN_RE.fullmatch(global_id)
    assert match
    block, job, task, run = match.groups()
    root = Path(root)
    (root / "pyproject.toml").write_text("[project]\nname = 'fixture'\n")
    (root / "code").mkdir(exist_ok=True)
    stem = f"b{block}_fixture/j{job}_fixture"
    ticket = (f"tasks/{stem}/runs/t{task}_fixture/r{run}_fixture.md")
    ticket_path = root / ticket
    ticket_path.parent.mkdir(parents=True, exist_ok=True)
    ticket_path.write_text(f"# {global_id}\n")
    # Tickets live under tasks/, while runtime receipts live under the formal
    # results/ mirror.  Keep both paths explicit so the registry checks both.
    runtime = (root / "examples" / "Fixture" / "tasks" / f"b{block}_fixture"
               / f"j{job}_fixture" / "results" / f"t{task}_fixture"
               / f"r{run}_fixture" / "runtime.yaml")
    runtime.parent.mkdir(parents=True, exist_ok=True)
    runtime.write_text(
        f"global_id: {global_id}\nfamily: Test\ntarget: fixture\n"
        f"status: planned\nticket: {ticket}\n"
    )


def _page(root, *, tick="⬜", decide="☐ make", arrow="", result=True,
          folded=False, registered=False):
    page_dir = Path(root) / "QT2"
    (page_dir / "outline").mkdir(parents=True)
    (page_dir / "QT2.md").write_text("# QT2\n\naccepted: ⬜\n")
    plan = PLAN.format(tick=tick)
    if folded:
        plan = plan.replace(
            "  Accept: recomputes from the accepted model Result\n",
            "  Accept: recomputes from the accepted model Result\n"
            "  Answered: E01-VALUE-adjusted-effect · 1.25 · results/local/value.yaml\n",
        )
    (page_dir / "outline" / "QT2-outline-v1.md").write_text(plan)
    if result:
        (page_dir / "results" / "local").mkdir(parents=True)
        (page_dir / "results" / "local" / "value.yaml").write_text("value: 1.25\n")
    items = ITEMS.format(decide=decide, arrow=arrow)
    if registered:
        _register_runtime(root, "b01j01t01r01")
        _register_runtime(root, "b02j01t01r01")
        items = items.replace(
            "Execution · reuse · b01j01t01r01",
            "Execution · registered · b01j01t01r01",
        ).replace(
            f"Page · Evidence Item · new-run · b02j01t01{arrow}",
            f"Page · Evidence Item · registered · b02j01t01r01{arrow}",
            1,
        )
        it.run_registry.cache_clear()
    (page_dir / "outline" / "QT2-evidence-items.md").write_text(items)
    return page_dir / "QT2.md"


class ItemTableTest(unittest.TestCase):
    def test_wall_label_is_compact_and_keeps_type(self):
        self.assertEqual(
            it.wall_label("E03-VALUE-primary-association", "VALUE", "Total MME"),
            "E3V.TotalMME",
        )
        self.assertEqual(
            it.wall_label("E02-CITE-guideline", "CITE", "guideline source"),
            "E2C.GuidelineSource",
        )
        self.assertEqual(
            it.wall_label("E08-DISPLAY-table", "DISPLAY", "sequence table"),
            "E8D.SequenceTable",
        )

    def test_global_run_addresses_accept_dotted_input_and_keep_compact_key(self):
        self.assertEqual("b01j02t03r04", it.compact_global_run("b01.j02.t03.r04"))
        self.assertEqual("b01.j02.t03.r04", it.readable_global_run("b01j02t03r04"))
        self.assertEqual("", it.compact_global_run("b01.j02.t03"))

    def test_read_items_parses_typed_identity_graph_and_local_result(self):
        with tempfile.TemporaryDirectory() as directory:
            page = _page(
                directory,
                decide="☑ make · JL 260901",
                arrow=" → results/local/value.yaml",
            )
            rows = it.read_items(page)
            row = rows["E01-VALUE-adjusted-effect"]
            self.assertEqual("VALUE", row["type"])
            self.assertEqual("C1.P1.B1", row["target"])
            self.assertEqual("Execution · reuse · b01j01t01r01", row["supporting_runs"])
            self.assertEqual(
                "source/page/results/r01/result.yaml · authority b01j01t01r01",
                row["pagex_bindings"],
            )
            self.assertEqual(1, row["pagex_count"])
            self.assertTrue(row["pagex_valid"])
            self.assertEqual(
                ("new-run", "b02j01t01", "results/local/value.yaml", "make"),
                (row["action"], row["address"], row["result"], row["decision"]),
            )

    def test_plan_parser_allows_multiple_items_on_one_bullet(self):
        got = [(item, target, kind, folded) for item, target, _head, kind, _expected, _accept, folded
               in it.bullets(PLAN.format(tick="⬜"))]
        self.assertEqual([
            ("E01-VALUE-adjusted-effect", "C1.P1.B1", "VALUE", False),
            ("E02-CITE-guideline-anchor", "C1.P1.B2", "CITE", False),
            ("E03-DISPLAY-effect-forest", "C1.P1.B2", "DISPLAY", False),
        ], got)

    def test_status_and_cycle_specified_planned_ready_folded(self):
        with tempfile.TemporaryDirectory() as directory:
            page = _page(directory, tick="✅ JL", result=False)
            summary = it.summarize(page, page.parent / "outline" / "QT2-outline-v1.md")
            self.assertEqual(1, summary["counts"]["specified"])
            self.assertEqual(1, summary["counts"]["deferred"])
            self.assertEqual(1, summary["counts"]["dropped"])
            self.assertEqual("SURVEY", summary["cycle"])
        with tempfile.TemporaryDirectory() as directory:
            page = _page(
                directory, tick="✅ JL", decide="☑ make · JL 260901",
                result=False, registered=True,
            )
            summary = it.summarize(page, page.parent / "outline" / "QT2-outline-v1.md")
            self.assertEqual(1, summary["counts"]["planned"])
            self.assertEqual("LAND", summary["cycle"])
        with tempfile.TemporaryDirectory() as directory:
            page = _page(
                directory, tick="✅ JL", decide="☑ make · JL 260901",
                arrow=" → results/local/value.yaml", registered=True,
            )
            summary = it.summarize(page, page.parent / "outline" / "QT2-outline-v1.md")
            self.assertEqual(1, summary["counts"]["ready"])
            self.assertEqual("EMBED", summary["cycle"])
        with tempfile.TemporaryDirectory() as directory:
            page = _page(
                directory, tick="✅ JL", decide="☑ make · JL 260901",
                arrow=" → results/local/value.yaml", folded=True, registered=True,
            )
            summary = it.summarize(page, page.parent / "outline" / "QT2-outline-v1.md")
            self.assertEqual(1, summary["counts"]["folded"])
            self.assertEqual("WRITE", summary["cycle"])

    def test_stale_when_local_result_is_newer_than_folded_plan(self):
        with tempfile.TemporaryDirectory() as directory:
            page = _page(
                directory, tick="✅ JL", decide="☑ make · JL 260901",
                arrow=" → results/local/value.yaml", folded=True, registered=True,
            )
            plan = page.parent / "outline" / "QT2-outline-v1.md"
            old = time.time() - 600
            os.utime(plan, (old, old))
            summary = it.summarize(page, plan)
            self.assertEqual(1, summary["counts"]["stale"])

    def test_status_label_in_authored_file_is_ignored(self):
        with tempfile.TemporaryDirectory() as directory:
            page = _page(
                directory, decide="☑ make · JL 260901", result=False,
                registered=True,
            )
            path = it.items_path(page)
            path.write_text(path.read_text().replace(
                "- **Decide**: ☑ make · JL 260901",
                "- **Status**: accepted\n- **Decide**: ☑ make · JL 260901",
            ))
            summary = it.summarize(page, page.parent / "outline" / "QT2-outline-v1.md")
            self.assertEqual(1, summary["counts"]["planned"])
            self.assertEqual(0, summary["counts"]["accepted"])

    def test_reuse_and_rerun_require_full_global_run_ids(self):
        with tempfile.TemporaryDirectory() as directory:
            page = _page(directory, tick="✅ JL", decide="☑ make · JL 260901", result=False)
            path = it.items_path(page)
            path.write_text(path.read_text().replace(
                "Execution · reuse · b01j01t01r01",
                "Execution · reuse · b01j01t01",
            ))
            rows = it.read_items(page)
            self.assertFalse(rows["E01-VALUE-adjusted-effect"]["planned"])
            summary = it.summarize(page, page.parent / "outline" / "QT2-outline-v1.md")
            self.assertEqual(1, summary["counts"]["specified"])
            self.assertEqual("SURVEY", summary["cycle"])

    def test_registered_run_requires_both_ticket_and_planned_receipt(self):
        with tempfile.TemporaryDirectory() as directory:
            page = _page(
                directory, tick="✅ JL", decide="☑ make · JL 260901",
                result=False, registered=True,
            )
            row = it.read_items(page)["E01-VALUE-adjusted-effect"]
            self.assertTrue(row["runs_registered"])
            self.assertTrue(row["planned"])

            ticket = (Path(directory) / "tasks" / "b02_fixture" / "j01_fixture"
                      / "runs" / "t01_fixture" / "r01_fixture.md")
            ticket.unlink()
            it.run_registry.cache_clear()
            row = it.read_items(page)["E01-VALUE-adjusted-effect"]
            self.assertFalse(row["runs_registered"])
            self.assertFalse(row["planned"])

    def test_current_task_ticket_without_a_real_result_is_rerun(self):
        """A pre-existing current-tree Ticket is not promoted to Done by a smoke receipt."""
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "pyproject.toml").write_text("[project]\nname = 'fixture'\n")
            (root / "code").mkdir()
            task = (root / "examples" / "Fixture" / "task" / "b03_live"
                    / "j02_regression" / "t01_lbp")
            ticket = task / "runs" / "agre" / "r01_lbp_af7d_ols.ps1"
            ticket.parent.mkdir(parents=True)
            ticket.write_text("# Ticket\n")
            runtime = (task.parent / "results" / task.name / "run_lbp_af7d_ols"
                       / "runtime.yaml")
            runtime.parent.mkdir(parents=True)
            runtime.write_text(
                "status: complete\n"
                "config: r01_lbp_af7d_ols.do\n"
            )
            # A config snapshot alone is not empirical output.
            (runtime.parent / "config_snapshot.do").write_text("// snapshot\n")
            it.run_registry.cache_clear()
            record = it.run_registry(str(root))["b03j02t01r01"]
            self.assertEqual("rerun", record["status"])
            self.assertEqual("Rerun", record["label"])

    def test_current_task_ticket_without_a_receipt_is_run_only(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "pyproject.toml").write_text("[project]\nname = 'fixture'\n")
            (root / "code").mkdir()
            ticket = (root / "examples" / "Fixture" / "task" / "b03_live"
                      / "j02_regression" / "t01_lbp" / "runs" / "agre"
                      / "r04_lbp_af14d_ols.ps1")
            ticket.parent.mkdir(parents=True)
            ticket.write_text("# Ticket\n")
            it.run_registry.cache_clear()
            record = it.run_registry(str(root))["b03j02t01r04"]
            self.assertEqual("ticket", record["status"])
            self.assertEqual("Run only", record["label"])
            self.assertEqual(
                "examples/Fixture/task/b03_live/j02_regression/t01_lbp",
                record["task_root"],
            )
            self.assertEqual("", record["runtime"])

    def test_discovery_ticket_requires_complete_same_stem_result(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "pyproject.toml").write_text("[project]\nname = 'fixture'\n")
            (root / "code").mkdir()
            task = (root / "examples" / "Fixture" / "discoveries" / "b01_lit"
                    / "j01_question" / "t04_measurement")
            ticket = task / "runs" / "r01_luo2026_measurement.sh"
            ticket.parent.mkdir(parents=True)
            ticket.write_text("#!/bin/sh\n")
            ticket.chmod(0o755)
            result = task / "results" / ticket.stem
            result.mkdir(parents=True)
            (result / "runtime.yaml").write_text("status: complete\n")
            (result / f"{ticket.stem}.md").write_text("# Card\n")
            (result / f"{ticket.stem}.bib").write_text("@article{key,}\n")
            (result / "facts.md").write_text("# Facts\n")
            it.run_registry.cache_clear()
            record = it.run_registry(str(root))["b01j01t04r01"]
            self.assertEqual("Discovery", record["family"])
            self.assertEqual("complete", record["status"])
            self.assertEqual("Done", record["label"])
            self.assertEqual(
                "examples/Fixture/discoveries/b01_lit/j01_question/t04_measurement",
                record["task_root"],
            )

    def test_pagex_binding_requires_exact_path_and_authority(self):
        with tempfile.TemporaryDirectory() as directory:
            page = _page(directory, tick="✅ JL", decide="☑ make · JL 260901", result=False)
            path = it.items_path(page)
            path.write_text(path.read_text().replace(
                "source/page/results/r01/result.yaml · authority b01j01t01r01",
                "source/page/ · authority accepted Page v2",
            ))
            row = it.read_items(page)["E01-VALUE-adjusted-effect"]
            self.assertFalse(row["pagex_valid"])
            self.assertFalse(row["planned"])

    def test_pagex_binding_must_be_named_in_local_input(self):
        with tempfile.TemporaryDirectory() as directory:
            page = _page(directory, tick="✅ JL", decide="☑ make · JL 260901", result=False)
            path = it.items_path(page)
            path.write_text(path.read_text().replace(
                "Supporting Results + PageX bindings",
                "Supporting Results only",
                1,
            ))
            row = it.read_items(page)["E01-VALUE-adjusted-effect"]
            self.assertTrue(row["pagex_valid"])
            self.assertFalse(row["planned"])


if __name__ == "__main__":
    unittest.main()
