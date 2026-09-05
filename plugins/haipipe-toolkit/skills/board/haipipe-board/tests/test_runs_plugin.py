"""The ⚙️ Runs presenter shows local Ticket → Result pairs only."""
import tempfile
import unittest
from pathlib import Path

from live.folderstat import folder_status
from live.runs import local_runs, render


class RunsPluginTest(unittest.TestCase):

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.page = Path(self.tmp.name) / "S-Test.md"
        self.page.write_text("# Test\n", encoding="utf-8")
        outline = self.page.parent / "outline"
        outline.mkdir()
        (outline / "S-Test-evidence-items.md").write_text(
            """### E01-VALUE-effect · C1.P1.B1 · Effect estimate
- **Target**: C1.P1.B1
- **Need**: One aggregate estimate.
- **Expected**: VALUE estimate with interval.
- **Acceptance**: Aggregate output passes review.
- **Supporting Runs**: Execution · rerun · b03.j01.t01.r01
- **Local Input**: Frozen aggregate envelope.
- **Local Run**: Page · Evidence Item · registered · b01.j01.t01.r01 → results/b01.j01.t01.r01/
- **Decide**: ☑ make
""",
            encoding="utf-8",
        )

    def tearDown(self):
        self.tmp.cleanup()

    def test_unallocated_plan_and_supporting_runs_do_not_become_local_rows(self):
        self.assertEqual(local_runs(self.page), [])
        body = render(self.page, "/examples/paper/board/MAIN/S-Test.html", "MAIN/S-Test.md")
        self.assertIn("No local Run allocated.", body)
        self.assertIn("Evidence lineage", body)
        self.assertNotIn("b03.j01.t01.r01</code></td>", body)
        self.assertNotIn("newrun", body)

    def test_projects_one_real_local_ticket_and_its_paired_result(self):
        ticket = self.page.parent / "runs" / "b01.j01.t01.r01.sh"
        ticket.parent.mkdir()
        ticket.write_text("#!/bin/sh\n", encoding="utf-8")
        result = self.page.parent / "results" / "b01.j01.t01.r01"
        result.mkdir(parents=True)
        (result / "runtime.yaml").write_text(
            "global_id: b01j01t01r01\nstatus: complete\ntarget: effect receipt\n"
            "ticket: b01.j01.t01.r01.sh\nresult: results/b01.j01.t01.r01\n",
            encoding="utf-8",
        )
        (result / "value.yaml").write_text("estimate: 1.2\n", encoding="utf-8")

        rows = local_runs(self.page)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["run_id"], "P j01.t01.r01")
        self.assertEqual(rows[0]["global_id"], "b01.j01.t01.r01")
        self.assertEqual(rows[0]["compact_id"], "b01j01t01r01")
        self.assertEqual(rows[0]["status"], "Done")
        self.assertEqual(rows[0]["refs"], ["E01-VALUE-effect"])
        body = render(self.page, "/examples/paper/board/MAIN/S-Test.html", "MAIN/S-Test.md")
        self.assertIn("1 local runs", body)
        self.assertIn("P j01.t01.r01", body)
        self.assertIn("runtime.yaml", body)
        self.assertIn("Run path", body)
        self.assertIn("Result path", body)
        self.assertIn("class=repo-path", body)
        self.assertNotIn("href=", body)
        self.assertNotIn(">Ticket<", body)
        self.assertNotIn(">Receipt<", body)
        self.assertNotIn("b03.j01.t01.r01</code></td>", body)
        self.assertNotIn("global Run Index", body)

    def test_task_page_resolves_job_backed_result_and_full_address(self):
        block = Path(self.tmp.name) / "b03_result_interpretation"
        (block / "board.md").parent.mkdir(parents=True)
        (block / "board.md").write_text(
            "# Task Block\nboard-kind: task-block\n", encoding="utf-8"
        )
        task = block / "j02_replication_measurement" / "t01_measure_result"
        task.mkdir(parents=True)
        page = task / "t01_measure_result.md"
        page.write_text("# Measure result\nfolder-kind: task\ntask: .\n", encoding="utf-8")
        ticket = task / "runs" / "r01_execution_measure-result.sh"
        ticket.parent.mkdir()
        ticket.write_text("#!/bin/sh\n", encoding="utf-8")
        runtime = (task.parent / "results" / task.name / ticket.stem
                   / "runtime.yaml")
        runtime.parent.mkdir(parents=True)
        runtime.write_text(
            "status: complete\ntarget: replicated measure\n",
            encoding="utf-8",
        )
        (runtime.parent / "result.txt").write_text("ok\n", encoding="utf-8")

        rows = local_runs(page)

        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["run_id"], "b03.j02.t01.r01")
        self.assertEqual(rows[0]["global_id"], "b03.j02.t01.r01")
        self.assertEqual(rows[0]["compact_id"], "b03j02t01r01")
        self.assertEqual(rows[0]["runtime"], runtime)
        self.assertEqual(rows[0]["result"],
                         "results/t01_measure_result/r01_execution_measure-result")
        self.assertEqual(rows[0]["status"], "Done")
        body = render(page, "", "")
        self.assertIn("b03.j02.t01.r01", body)
        self.assertIn("j02_replication_measurement/results/t01_measure_result", body)
        self.assertNotIn("P r01_execution_measure-result", body)

    def test_folder_distinguishes_evidence_bindings_from_local_execution(self):
        bindings = (self.page.parent / "outline" / "evidence" /
                    "supporting-runs" / "S-Test-run-bindings.md")
        bindings.parent.mkdir(parents=True)
        bindings.write_text("# derived pointers\n", encoding="utf-8")
        ticket = self.page.parent / "runs" / "r01-local.sh"
        ticket.parent.mkdir()
        ticket.write_text("#!/bin/sh\n", encoding="utf-8")
        receipt = self.page.parent / "results" / "r01-local" / "runtime.yaml"
        receipt.parent.mkdir(parents=True)
        receipt.write_text("status: planned\n", encoding="utf-8")

        _title, _mtime, rows, _stubs = folder_status(self.page)
        by_label = {row["label"]: row for row in rows}
        self.assertIn("outline", by_label)
        self.assertIn("outline/evidence/supporting-runs", by_label)
        self.assertIn("runs", by_label)
        self.assertIn("results", by_label)
        self.assertIn(
            "S-Test-run-bindings.md",
            [rel for rel, _path in
             by_label["outline/evidence/supporting-runs"]["list"]],
        )
        self.assertNotIn(
            "evidence/supporting-runs/S-Test-run-bindings.md",
            [rel for rel, _path in by_label["outline"]["list"]],
        )
        self.assertFalse(by_label["outline"]["derived"])
        self.assertTrue(by_label["outline/evidence/supporting-runs"]["derived"])
        self.assertFalse(by_label["runs"]["derived"])
        self.assertFalse(by_label["results"]["derived"])

    def test_folder_shows_skill_as_an_explicit_outline_lane(self):
        skill = self.page.parent / "outline" / "skill"
        skill.mkdir(parents=True)
        (skill / "S-Test.md").write_text("- haipipe-page-outline\n",
                                          encoding="utf-8")

        _title, _mtime, rows, _stubs = folder_status(self.page)
        by_label = {row["label"]: row for row in rows}
        self.assertIn("outline/skill", by_label)
        self.assertEqual(by_label["outline/skill"]["files"], 1)
        self.assertNotIn(
            "skill/S-Test.md",
            [rel for rel, _path in by_label["outline"]["list"]],
        )


if __name__ == "__main__":
    unittest.main()
