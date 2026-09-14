"""The ⚙️ Runs presenter separates Page feedback from Task outputs."""
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from live.folderstat import folder_status
from live.runs import (_audit_page_run_order, _page_run_label,
                       _track_change_html, _word_track_changes, RunsTabMixin,
                       local_runs, render, run_inventory)


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

    def test_track_changes_keep_surviving_words_plain(self):
        rendered = _word_track_changes(
            "The Page owns the editable document.",
            "The Page Folder owns its editable document.",
        )
        self.assertEqual(
            rendered,
            "The Page<ins> Folder</ins> owns<del> the</del>"
            "<ins> its</ins> editable document.",
        )
        self.assertNotIn("<del>The Page", rendered)
        self.assertNotIn("<ins>The Page", rendered)

    def test_track_change_card_shows_type_reason_and_bounded_preference(self):
        section = """### Saved result

#### C1.P1

Saved prose.

#### Track changes

##### F06 · Concept clarification · capability completeness

###### Before

Studio Chat keeps the conversations and discussion summaries that shaped the Page.

###### After

Studio is where people brainstorm for the Page. Studio Chat keeps the conversation, while Studio Draw turns ideas into visual sketches.

###### Why

The former sentence omitted Draw.

###### Inferred preference

Define the parent before its child capabilities. <script>alert(1)</script>

###### Preference status

Provisional · Page-local.
"""
        body = _track_change_html(section)
        self.assertIn("class=track-card", body)
        self.assertIn("<h4>Feedback 6</h4>", body)
        self.assertNotIn("<h4>F06</h4>", body)
        self.assertIn("Concept clarification · capability completeness", body)
        self.assertIn(
            "<ins>Studio is where people brainstorm for the Page. </ins>", body)
        self.assertIn("Studio Chat keeps the", body)
        self.assertIn("<del> conversations and discussion summaries", body)
        self.assertIn("<ins> conversation, while Studio Draw", body)
        self.assertIn("<b>Why</b>", body)
        self.assertIn("<b>Inferred preference</b>", body)
        self.assertIn("Provisional · Page-local.", body)
        self.assertNotIn("<script>", body)
        self.assertIn("&lt;script&gt;", body)

    def test_track_changes_skip_missing_or_unchanged_text(self):
        unchanged = """### Saved result

#### Track changes

##### F01 · Status only

###### Before

The Page remains open.

###### After

The Page remains open.
"""
        missing_after = """### Saved result

#### Track changes

##### F02 · Navigation only

###### Before

Open the Current Run.
"""
        self.assertEqual(_track_change_html(unchanged), "")
        self.assertEqual(_track_change_html(missing_after), "")

    def test_unresolved_supporting_run_is_a_held_supporting_row(self):
        self.assertEqual(local_runs(self.page), [])
        body = render(self.page, "/examples/paper/board/MAIN/S-Test.html", "MAIN/S-Test.md")
        self.assertIn("No Run P yet.", body)
        self.assertIn("<h2>Run P</h2>", body)
        self.assertIn("<h2>Run E</h2>", body)
        self.assertIn("b03.j01.t01.r01", body)
        self.assertIn("Held", body)
        self.assertIn("not available yet", body)
        self.assertIn("Supporting Runs", body)
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
        self.assertIn("<h2>Run P</h2>", body)
        self.assertIn("<h2>Run E</h2>", body)
        self.assertIn("<h2>Supporting Runs</h2>", body)
        self.assertIn("<h2>Run E</h2>", body)
        self.assertIn("<th>Type / Where</th>", body)
        self.assertIn("<th>What happened</th>", body)
        self.assertIn("P j01.t01.r01", body)
        self.assertIn("results/b01.j01.t01.r01", body)
        self.assertNotIn("runtime.yaml", body)
        self.assertNotIn("Run path", body)
        self.assertNotIn("Result path", body)
        self.assertIn("class=repo-path", body)
        self.assertNotIn("href=", body)
        self.assertNotIn(">Ticket<", body)
        self.assertNotIn(">Receipt<", body)
        self.assertIn("b03.j01.t01.r01</code></td>", body)
        self.assertNotIn("global Run Index", body)

    def test_standalone_local_run_keeps_r_identity_and_summarizes_result(self):
        (self.page.parent / "page.toml").write_text(
            'schema = "haipipe-page/v1"\n', encoding="utf-8")
        ticket = self.page.parent / "runs" / "r01_page-setup.md"
        ticket.parent.mkdir()
        ticket.write_text(
            "---\nfamily: page\noperation: page-setup\n"
            "target: S-Test.md\n---\n", encoding="utf-8")
        result = self.page.parent / "results" / ticket.stem
        result.mkdir(parents=True)
        (result / "runtime.yaml").write_text(
            "run: r01_page-setup\nfamily: page\noperation: page-setup\n"
            "mode: resume-and-build\ntarget: S-Test.md\nstatus: complete\n",
            encoding="utf-8")
        (result / "report.md").write_text(
            "# Result\n\n- Coverage: 3 sections; 8 reader-move Bullets.\n"
            "- Mechanical gate: **PASS**.\n", encoding="utf-8")

        row = local_runs(self.page)[0]
        body = render(self.page, "", "")

        self.assertEqual(row["run_id"], "r01_page-setup")
        self.assertEqual(row["origin"], "Local")
        self.assertEqual(
            row["outcome"],
            "Resumed and rebuilt Page — 3 sections; 8 reader-move Bullets · Mechanical gate PASS",
        )
        self.assertNotIn("r01_page-setup", body)
        self.assertIn("No Run E yet.", body)
        self.assertNotIn("no item binding recorded", body)

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
        self.assertNotIn("b03.j02.t01.r01", body)
        self.assertNotIn("j02_replication_measurement/results/t01_measure_result", body)
        self.assertNotIn("runtime.yaml", body)
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

    def test_design_ticket_without_runtime_is_not_a_paper_run(self):
        stem = "rd01_generate_sms"
        ticket = self.page.parent / "runs" / (stem + ".yaml")
        ticket.parent.mkdir()
        ticket.write_text("schema: haipipe.design-ticket/v2\n", encoding="utf-8")
        rows = local_runs(self.page)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["run_id"], stem)
        self.assertIsNone(rows[0]["runtime"])

    def test_design_yaml_ticket_keeps_design_identity(self):
        stem = "rd01_generate_sms"
        ticket = self.page.parent / "runs" / (stem + ".yaml")
        ticket.parent.mkdir()
        ticket.write_text("schema: haipipe.design-ticket/v2\n", encoding="utf-8")
        runtime = self.page.parent / "results" / stem / "runtime.yaml"
        runtime.parent.mkdir(parents=True)
        runtime.write_text(
            "family: design\nstatus: complete\nrun: " + stem + "\n",
            encoding="utf-8")
        (runtime.parent / "result.yaml").write_text("verdict: pass\n", encoding="utf-8")
        rows = local_runs(self.page)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["run_id"], stem)
        self.assertFalse(rows[0]["run_id"].startswith("P "))
        self.assertEqual(rows[0]["ticket"], ticket)
        self.assertEqual(rows[0]["runtime"], runtime)

    def test_retired_design_identity_is_flagged_unsupported(self):
        stem = "r01_design_generate_sms"
        ticket = self.page.parent / "runs" / (stem + ".yaml")
        ticket.parent.mkdir()
        ticket.write_text("schema: haipipe.design-ticket/v1\n", encoding="utf-8")
        row = local_runs(self.page)[0]
        self.assertEqual(row["run_id"], stem)
        self.assertIn("retired Design Run identity is unsupported", row["audit"])

    def writing_pair(self, status="planned"):
        stem = "r02_page-writing_c01-p02"
        ticket = self.page.parent / "runs" / (stem + ".md")
        ticket.parent.mkdir(exist_ok=True)
        ticket.write_text(
            "---\nrun: " + stem + "\nfamily: page\noperation: paragraph-writing\n"
            "target: C1.P2\n---\n## Prompt\nExplain the empty field.\n"
            "<script>alert('unsafe')</script>\n", encoding="utf-8")
        result = self.page.parent / "results" / stem
        result.mkdir(parents=True)
        (result / "runtime.yaml").write_text(
            "status: " + status + "\noperation: paragraph-writing\n"
            "target: C1.P2\n", encoding="utf-8")
        return ticket, result

    def test_markdown_writing_target_and_prompt_are_visible_before_result(self):
        ticket, result = self.writing_pair()
        rows = local_runs(self.page)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["status"], "Ready")
        self.assertEqual(rows[0]["target"], "C1.P2")
        self.assertEqual(rows[0]["kind"], "Paragraph writing")
        self.assertEqual(rows[0]["lane"], "task")
        body = render(self.page, "", "")
        self.assertIn("Writing instructions / Prompt", body)
        self.assertIn("Explain the empty field.", body)
        self.assertIn("&lt;script&gt;", body)
        self.assertNotIn("<script>alert", body)
        self.assertIn("Not available yet.", body)
        # An orphan remains discoverable, but cannot claim to be ready.
        (result / "runtime.yaml").unlink()
        self.assertEqual(local_runs(self.page)[0]["target"], "C1.P2")
        self.assertEqual(local_runs(self.page)[0]["status"], "Held")
        self.assertIn("Missing runtime.yaml", render(self.page, "", ""))

    def test_complete_writing_requires_both_outputs_and_previews_the_paragraph(self):
        _ticket, result = self.writing_pair("complete")
        self.assertEqual(local_runs(self.page)[0]["status"], "Held")
        (result / "paragraph.md").write_text("An empty field is not zero.\n", encoding="utf-8")
        self.assertEqual(local_runs(self.page)[0]["status"], "Held")
        (result / "trace.md").write_text("C1.P2.B1 → sentence 1; pass.\n", encoding="utf-8")
        self.assertEqual(local_runs(self.page)[0]["status"], "Done")
        body = render(self.page, "", "")
        self.assertIn("An empty field is not zero.", body)
        self.assertIn("C1.P2.B1", body)
        self.assertIn("<h2>Run P</h2>", body)
        self.assertIn("<th>Version / Step</th>", body)
        self.assertIn('aria-expanded="false"', body)
        self.assertNotIn("href=", body)

    def test_writing_preview_does_not_follow_external_symlink(self):
        _ticket, result = self.writing_pair("complete")
        external = self.page.parent / "private.md"
        external.write_text("NEVER_PREVIEW_THIS", encoding="utf-8")
        (result / "paragraph.md").symlink_to(external)
        (result / "trace.md").write_text("pass", encoding="utf-8")
        self.assertEqual(local_runs(self.page)[0]["status"], "Held")
        self.assertNotIn("NEVER_PREVIEW_THIS", render(self.page, "", ""))

    def test_interactive_history_does_not_follow_external_version_file_symlink(self):
        stem = "rp00_mermaid-structure"
        ticket = self.page.parent / "runs" / (stem + ".md")
        ticket.parent.mkdir(exist_ok=True)
        ticket.write_text(
            "---\nfamily: page\noperation: interactive-writing\n"
            "interaction: human-feedback\ntarget: C1.P1\n---\n",
            encoding="utf-8",
        )
        result = self.page.parent / "results" / stem
        result.mkdir(parents=True)
        (result / "runtime.yaml").write_text(
            "status: waiting-for-feedback\noperation: interactive-writing\n"
            "version: v001\nstep: s001\n",
            encoding="utf-8",
        )
        (result / "working.md").write_text("Current: v001/s001\n", encoding="utf-8")
        outside = self.page.parent / "private-history-SECRET-NAME.md"
        outside.write_text(
            "## Step s001\n### Human feedback\nNEVER_PREVIEW_HISTORY\n"
            "### Saved result\nNEVER_PREVIEW_RESULT\n", encoding="utf-8"
        )
        (result / "v001.md").symlink_to(outside)

        body = render(self.page, "", "")
        self.assertNotIn("SECRET-NAME", body)
        self.assertNotIn("NEVER_PREVIEW_HISTORY", body)

    def test_run_discovery_ignores_ticket_and_runtime_symlink_escapes(self):
        outside_ticket = self.page.parent / "private-ticket.md"
        outside_ticket.write_text(
            "---\nfamily: page\noperation: interactive-writing\n---\nSECRET_TICKET",
            encoding="utf-8",
        )
        runs = self.page.parent / "runs"
        runs.mkdir()
        (runs / "rp09_page-writing_escape.md").symlink_to(outside_ticket)
        outside_runtime = self.page.parent / "private-runtime.yaml"
        outside_runtime.write_text("status: complete\ntarget: SECRET_RUNTIME\n", encoding="utf-8")
        result = self.page.parent / "results" / "r10-local"
        result.mkdir(parents=True)
        (result / "runtime.yaml").symlink_to(outside_runtime)
        (runs / "r10-local.sh").write_text("#!/bin/sh\n", encoding="utf-8")

        rows = local_runs(self.page)
        self.assertEqual([row["run_id"] for row in rows], ["P r10-local"])
        self.assertIsNone(rows[0]["runtime"])
        body = render(self.page, "", "")
        self.assertNotIn("SECRET_TICKET", body)
        self.assertNotIn("SECRET_RUNTIME", body)

    def test_interactive_page_run_projects_version_step_and_feedback_history(self):
        stem = "rp00_mermaid-structure"
        ticket = self.page.parent / "runs" / (stem + ".md")
        ticket.parent.mkdir(exist_ok=True)
        ticket.write_text(
            "---\nfamily: page\noperation: interactive-writing\n"
            "interaction: human-feedback\ntarget: C1.P1\n---\n"
            "- Goal: Make the opening clear in the person's terms.\n",
            encoding="utf-8",
        )
        result = self.page.parent / "results" / stem
        result.mkdir(parents=True)
        (result / "runtime.yaml").write_text(
            "status: waiting-for-feedback\noperation: interactive-writing\n"
            "interaction: human-feedback\ntarget: C1.P1\nversion: v001\nstep: s002\n",
            encoding="utf-8",
        )
        (result / "working.md").write_text(
            "Current: v001/s002\nState: waiting-for-feedback\n",
            encoding="utf-8",
        )
        version_text = (
            "# Version v001\n\n## Step s001\n\n"
            "### Human feedback\nEarlier feedback.\n\n"
            "### Saved result\nEarlier result.\n\n"
            "## Step s002\n\n"
            "### Human feedback\nPlease make this less abstract.\n\n"
            "### Saved result\nThe Page keeps the writing history.\n"
        )
        (result / "v001.md").write_text(version_text, encoding="utf-8")

        rows = local_runs(self.page)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["lane"], "page")
        self.assertEqual(rows[0]["status"], "Waiting")
        self.assertEqual(rows[0]["version"], "v001")
        self.assertEqual(rows[0]["step"], "s002")
        body = render(self.page, "", "")
        self.assertIn("Make the opening clear", body)
        self.assertIn("v001/s002", body)
        self.assertIn("Latest feedback", body)
        self.assertIn("Current saved result", body)
        self.assertIn("Please make this less abstract.", body)
        self.assertIn("The Page keeps the writing history.", body)
        self.assertIn("Earlier steps · 1", body)
        self.assertIn("<summary>Technical details</summary>", body)
        self.assertIn('class="runs-table', body)
        self.assertIn("@media(max-width:700px)", body)
        self.assertIn("table.runs-table>thead", body)
        self.assertNotIn(".runs-table thead{display:none}", body)
        self.assertIn(".step-history pre{white-space:pre-wrap", body)
        self.assertNotIn("Page Run brief", body)
        self.assertNotIn("family: page", body)

        (result / "v001.md").write_text(
            version_text.replace("### Saved result\nThe Page keeps the writing history.",
                                 "### Saved result\n"),
            encoding="utf-8",
        )
        self.assertEqual(local_runs(self.page)[0]["status"], "Held")
        self.assertIn("Step s002 · Saved result", render(self.page, "", ""))
        (result / "v001.md").write_text(version_text, encoding="utf-8")

        (result / "runtime.yaml").write_text(
            "status: waiting-for-feedback\noperation: interactive-writing\n"
            "version: v001\nstep: s003\n", encoding="utf-8"
        )
        self.assertEqual(local_runs(self.page)[0]["status"], "Held")
        body = render(self.page, "", "")
        self.assertIn("History integrity finding", body)
        self.assertIn("Step s003", body)

    def test_exact_run_query_expands_the_readable_history(self):
        stem = "rp01_p01"
        ticket = self.page.parent / "runs" / (stem + ".md")
        ticket.parent.mkdir(exist_ok=True)
        ticket.write_text(
            "---\nrun: " + stem + "\nfamily: page\noperation: interactive-writing\n"
            "interaction: human-feedback\ntarget: P01\n---\n",
            encoding="utf-8",
        )
        result = self.page.parent / "results" / stem
        result.mkdir(parents=True)
        (result / "runtime.yaml").write_text(
            "run: " + stem + "\nstatus: waiting-for-feedback\n"
            "operation: interactive-writing\nversion: v001\nstep: s001\n",
            encoding="utf-8",
        )
        (result / "working.md").write_text(
            "Current: v001/s001\nState: waiting-for-feedback\n",
            encoding="utf-8",
        )
        (result / "v001.md").write_text(
            "## Step s001\n### Human feedback\nMake it direct.\n"
            "### Saved result\nThe Page owns its source.\n",
            encoding="utf-8",
        )

        collapsed = render(self.page, "", "")
        expanded = render(self.page, "", "", stem)

        self.assertIn('data-run="rp01_p01"', expanded)
        self.assertIn(
            'data-run="rp01_p01" tabindex="0" aria-expanded="false"',
            collapsed,
        )
        self.assertIn(
            'data-run="rp01_p01" tabindex="0" aria-expanded="true"',
            expanded,
        )
        self.assertRegex(
            expanded,
            r'<tr class="detail" data-key="p-\d+"><td colspan=5>',
        )

    def test_page_and_task_runs_keep_separate_local_identity_sequences(self):
        page_stem = "rp00_mermaid-structure"
        task_stem = "r01_execution_export"
        runs = self.page.parent / "runs"
        runs.mkdir(exist_ok=True)
        (runs / f"{page_stem}.md").write_text(
            "---\nrun: " + page_stem + "\nfamily: page\n"
            "operation: interactive-writing\ninteraction: human-feedback\n---\n",
            encoding="utf-8",
        )
        page_result = self.page.parent / "results" / page_stem
        page_result.mkdir(parents=True)
        (page_result / "runtime.yaml").write_text(
            "run: " + page_stem + "\nstatus: waiting-for-feedback\n"
            "operation: interactive-writing\nversion: v001\nstep: s001\n",
            encoding="utf-8",
        )
        (page_result / "working.md").write_text("Current: v001/s001\n", encoding="utf-8")
        (page_result / "v001.md").write_text(
            "## Step s001\n\n### Human feedback\nFeedback.\n\n"
            "### Saved result\nResult.\n",
            encoding="utf-8",
        )
        (runs / f"{task_stem}.sh").write_text("#!/bin/sh\n", encoding="utf-8")

        rows = local_runs(self.page)
        by_id = {row["run_id"]: row for row in rows}
        self.assertEqual(by_id[page_stem]["lane"], "page")
        self.assertEqual(by_id[f"P {task_stem}"]["lane"], "task")
        # The fixture also contributes one unresolved Supporting Run.
        body = render(self.page, "", "")
        self.assertIn("<h2>Run P</h2>", body)
        self.assertIn("<h2>Supporting Runs</h2>", body)

    def test_mermaid_structure_must_close_before_numbered_paragraph_runs(self):
        runs = self.page.parent / "runs"
        runs.mkdir(exist_ok=True)
        (self.page.parent / "outline" / "S-Test-logic.mmd").write_text(
            'flowchart TD\nP01["P01 · Opening"]\nP02["P02 · Meaning"]\n'
            'P01 -->|"establishes the question"| P02\n',
            encoding="utf-8",
        )

        def writing_run(stem, target, status="waiting-for-feedback", closed=False):
            (runs / f"{stem}.md").write_text(
                "---\nrun: " + stem + "\nfamily: page\n"
                "operation: interactive-writing\ninteraction: human-feedback\n"
                "target: " + target + "\n---\n- Goal: Review " + target + ".\n",
                encoding="utf-8",
            )
            result = self.page.parent / "results" / stem
            result.mkdir(parents=True)
            (result / "runtime.yaml").write_text(
                "run: " + stem + "\nstatus: " + status + "\n"
                "operation: interactive-writing\nversion: v001\nstep: s001\n",
                encoding="utf-8",
            )
            (result / "working.md").write_text("Current: v001/s001\n", encoding="utf-8")
            closure = ("\n## Version closure\n\n### Human close\nApproved.\n"
                       if closed else "")
            (result / "v001.md").write_text(
                "## Step s001\n\n### Human feedback\nReview.\n\n"
                "### Saved result\nCandidate.\n" + closure,
                encoding="utf-8",
            )
            return result

        structure = writing_run("rp00_mermaid-structure", "Mermaid Structure + P01..PN")
        writing_run("rp01_p01-p03", "P01-P03")

        by_id = {row["run_id"]: row for row in local_runs(self.page)}
        self.assertEqual(by_id["rp00_mermaid-structure"]["status"], "Waiting")
        self.assertEqual(by_id["rp01_p01-p03"]["status"], "Held")
        self.assertTrue(any("requires a closed rp00_mermaid-structure" in finding
                            for finding in by_id["rp01_p01-p03"]["audit"]))
        body = render(self.page, "", "")
        self.assertIn("rp00 · Mermaid Structure", body)
        self.assertIn("rp01 · P01-P03", body)
        self.assertIn("Argument flow", body)
        self.assertIn("establishes the question", body)
        self.assertIn("class=logic-steps", body)
        self.assertIn("Whole-page argument flow and paragraph order (P01–P06)", body)
        self.assertIn('aria-label="Page Mermaid Structure"', body)

        (structure / "runtime.yaml").write_text(
            "run: rp00_mermaid-structure\nstatus: complete\noperation: interactive-writing\n"
            "version: v001\nstep: s001\n",
            encoding="utf-8",
        )
        (structure / "v001.md").write_text(
            "## Step s001\n\n### Human feedback\nReview.\n\n"
            "### Saved result\nCandidate.\n\n## Version closure\n\n"
            "### Human close\nApproved.\n",
            encoding="utf-8",
        )
        by_id = {row["run_id"]: row for row in local_runs(self.page)}
        self.assertEqual(by_id["rp00_mermaid-structure"]["status"], "Done")
        self.assertEqual(by_id["rp01_p01-p03"]["status"], "Waiting")

    def test_noncanonical_structure_identity_is_rejected(self):
        rows = [
            {"lane": "page", "run_id": "rp01_mermaid-structure", "status": "Done"},
            {"lane": "page", "run_id": "rp02_p01", "status": "Waiting"},
        ]

        _audit_page_run_order(rows)

        self.assertEqual(rows[0]["status"], "Held")
        self.assertTrue(any("invalid Page Run identity" in finding
                            for finding in rows[0]["audit"]))
        self.assertEqual(_page_run_label(rows[0]["run_id"]),
                         "rp01_mermaid-structure")
        self.assertEqual(_page_run_label("rp01_p1"), "rp01_p1")
        self.assertEqual(rows[1]["status"], "Held")
        self.assertTrue(any("requires a closed rp00_mermaid-structure" in finding
                            for finding in rows[1]["audit"]))

    def test_interactive_page_run_completes_only_with_version_closure(self):
        stem = "rp00_mermaid-structure"
        ticket = self.page.parent / "runs" / (stem + ".md")
        ticket.parent.mkdir(exist_ok=True)
        ticket.write_text(
            "---\nfamily: page\noperation: interactive-writing\ntarget: C3.P1\n---\n",
            encoding="utf-8",
        )
        result = self.page.parent / "results" / stem
        result.mkdir(parents=True)
        (result / "runtime.yaml").write_text(
            "status: complete\noperation: interactive-writing\n"
            "version: v001\nstep: s001\n",
            encoding="utf-8",
        )
        (result / "working.md").write_text("Current: v001/s001\n", encoding="utf-8")
        version = result / "v001.md"
        version.write_text(
            "# Version v001\n\n## Step s001\n\n"
            "### Human feedback\nClose this version.\n\n"
            "### Saved result\nFinal summary.\n",
            encoding="utf-8",
        )
        self.assertEqual(local_runs(self.page)[0]["status"], "Held")
        version.write_text(
            version.read_text(encoding="utf-8")
            + "\n## Version closure\n\n### Human close\nApproved by the person.\n",
            encoding="utf-8",
        )
        self.assertEqual(local_runs(self.page)[0]["status"], "Done")

    def test_discovery_support_is_a_supporting_run_and_exposes_result_only(self):
        result_card = self.page.parent / "discoveries" / "result-card.md"
        result_card.parent.mkdir()
        result_card.write_text("Result output.\n", encoding="utf-8")
        registry = {
            "b03j01t01r01": {
                "status": "complete", "label": "Done", "family": "Discovery",
                "target": "Find prior evidence", "ticket": "private/run.sh",
                "runtime": "private/runtime.yaml", "result": "discoveries/result-card.md",
            }
        }
        with patch("live.runs.run_registry", return_value=registry):
            rows = run_inventory(self.page)
            body = render(self.page, "", "")

        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["lane"], "task")
        self.assertEqual(rows[0]["kind"], "Discovery")
        self.assertEqual(rows[0]["origin"], "Linked")
        self.assertIn("<h2>Supporting Runs</h2>", body)
        self.assertIn("Discovery", body)
        self.assertIn("discoveries/result-card.md", body)
        self.assertNotIn("private/run.sh", body)
        self.assertNotIn("private/runtime.yaml", body)

    def test_complete_task_registry_entry_without_result_is_held(self):
        registry = {
            "b03j01t01r01": {
                "status": "complete", "family": "Discovery",
                "result": "discoveries/missing-result.md",
            }
        }
        with patch("live.runs.run_registry", return_value=registry):
            row = run_inventory(self.page)[0]
            body = render(self.page, "", "")
        self.assertEqual(row["status"], "Held")
        self.assertEqual(row["result"], "")
        self.assertIn("not available yet", body)

    def test_orphan_interactive_result_is_visible_and_held(self):
        result = self.page.parent / "results" / "rp08_page-writing_orphan"
        result.mkdir(parents=True)
        (result / "runtime.yaml").write_text(
            "family: page\noperation: interactive-writing\n"
            "status: waiting-for-feedback\nversion: v001\nstep: s001\n",
            encoding="utf-8",
        )
        (result / "working.md").write_text("Current: v001/s001\n", encoding="utf-8")
        (result / "v001.md").write_text(
            "## Step s001\n\n### Human feedback\nFeedback.\n\n"
            "### Saved result\nResult.\n",
            encoding="utf-8",
        )
        row = local_runs(self.page)[0]
        self.assertEqual(row["run_id"], "rp08_page-writing_orphan")
        self.assertEqual(row["status"], "Held")
        self.assertTrue(row["orphan"])
        self.assertIn("Result exists without its authored Run record", render(self.page, "", ""))

    def test_interactive_runtime_identity_mismatch_is_held(self):
        stem = "rp09_page-writing_identity"
        ticket = self.page.parent / "runs" / (stem + ".md")
        ticket.parent.mkdir(exist_ok=True)
        ticket.write_text(
            "---\nfamily: page\noperation: interactive-writing\n---\n",
            encoding="utf-8",
        )
        result = self.page.parent / "results" / stem
        result.mkdir(parents=True)
        (result / "runtime.yaml").write_text(
            "run: r99_wrong\nstatus: waiting-for-feedback\n"
            "operation: interactive-writing\nversion: v001\nstep: s001\n",
            encoding="utf-8",
        )
        (result / "working.md").write_text("Current: v001/s001\n", encoding="utf-8")
        (result / "v001.md").write_text(
            "## Step s001\n\n### Human feedback\nFeedback.\n\n"
            "### Saved result\nResult.\n",
            encoding="utf-8",
        )
        row = local_runs(self.page)[0]
        self.assertEqual(row["status"], "Held")
        self.assertIn("identity does not match", render(self.page, "", ""))

    def test_newer_same_status_runs_sort_first_and_scripts_stay_offstage(self):
        runs = self.page.parent / "runs"
        runs.mkdir()
        for stem in ("r01-local", "r02-local"):
            (runs / (stem + ".sh")).write_text("#!/bin/sh\n", encoding="utf-8")
        scripts = self.page.parent / "scripts"
        scripts.mkdir()
        (scripts / "helper.py").write_text("SECRET_IMPLEMENTATION = True\n", encoding="utf-8")

        rows = local_runs(self.page)
        self.assertEqual([row["run_id"] for row in rows], ["P r02-local", "P r01-local"])
        body = render(self.page, "", "")
        self.assertNotIn("Scripts ▸", body)
        self.assertNotIn("scripts/helper.py", body)
        self.assertNotIn("SECRET_IMPLEMENTATION", body)

    def test_runs_plugin_post_route_escapes_page_parameters(self):
        class Surface(RunsTabMixin):
            def target(_self, payload):
                return self.page, None
        result, error = Surface().plug_runs({"path": "/a b", "file": "S&Test.md"})
        self.assertIsNone(error)
        self.assertIn("path=/a%20b", result["url"])
        self.assertIn("file=S%26Test.md", result["url"])


if __name__ == "__main__":
    unittest.main()
