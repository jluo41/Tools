"""Static routing guards; behavioral acceptance is a fresh-agent field test.

These tests deliberately do not claim a new writer, scheduler or UI exists.
"""

import re
import unittest
from pathlib import Path


SKILLS = Path(__file__).resolve().parents[4]
WORKFLOW = SKILLS / "page/page-workflows/haipipe-page-workflow"


class InteractiveSkillContractTest(unittest.TestCase):
    def test_workflow_is_run_spec_graph_not_phase_authority(self):
        workflow = (WORKFLOW / "SKILL.md").read_text()
        table = (WORKFLOW / "ref/workflow-table.md").read_text()
        cards = (WORKFLOW / "ref/phase-cards.md").read_text()
        for text in (workflow, table, cards):
            with self.subTest(source=text[:40]):
                self.assertIn("Run Spec", text)
                self.assertIn("Gate", text)
                self.assertIn("Route", text)
        self.assertIn("Step is an internal action inside\none Run", workflow)
        self.assertIn("NEW_VERSION", workflow)
        self.assertIn("NEW_RUN", workflow)
        self.assertIn("not Phase authority", table)
        self.assertIn("does not define Phase authority", cards)

    def test_relative_instruction_links_resolve(self):
        files = [
            WORKFLOW / "SKILL.md",
            WORKFLOW / "ref/structure-run.md",
            WORKFLOW / "ref/interactive-writing-run.md",
            WORKFLOW / "ref/workflow-table.md",
            SKILLS / "page/page-workflows/haipipe-page-content/SKILL.md",
            SKILLS / "page/page-workflows/haipipe-page-content/ref/paragraph-run.md",
            SKILLS / "writing/haipipe-writing/SKILL.md",
            SKILLS / "run/haipipe-run/SKILL.md",
            SKILLS / "page/haipipe-page/fn/runs.md",
        ]
        for source in files:
            for reference in re.findall(r"`((?:\.\./)+[^`\s<>*]+\.md)`", source.read_text()):
                with self.subTest(source=source.name, reference=reference):
                    self.assertTrue((source.parent / reference).is_file(), reference)

    def test_entry_points_route_to_one_interactive_contract(self):
        for relative in (
            "page/haipipe-page/SKILL.md",
            "page/page-workflows/haipipe-page-content/SKILL.md",
            "page/page-workflows/haipipe-page-outline/SKILL.md",
            "writing/haipipe-writing/SKILL.md",
            "run/haipipe-run/SKILL.md",
        ):
            with self.subTest(skill=relative):
                self.assertIn("interactive-writing-run.md", (SKILLS / relative).read_text())

    def test_content_default_is_adoption_not_paragraph_allocation(self):
        text = (SKILLS / "page/page-workflows/haipipe-page-content/SKILL.md").read_text()
        self.assertIn("## Adopt · no second draft", text)
        self.assertIn("## Optional delegated single-paragraph path", text)
        self.assertNotIn("normally commissions six writing Runs", text)
        self.assertNotIn("Every current writing dispatch records", text)

    def test_template_preserves_one_version_journal_with_feedback_result_and_seal(self):
        template = (WORKFLOW / "ref/writing-step-template.md").read_text()
        for required in (
            "v001.md", "## Step s001", "### Human feedback", "### Saved result",
            "Original request",
            "Selected quote", "Source Version/Step", "Agent interpretation",
            "Planning snapshot", "Protected/out-of-scope", "Sealed scope",
            "## Version closure",
        ):
            with self.subTest(field=required):
                self.assertIn(required, template)
        self.assertNotIn("s001-input.md", template)
        self.assertNotIn("s001-result.md", template)

    def test_step_response_format_is_fixed_at_execution_layer(self):
        contract = (WORKFLOW / "ref/interactive-writing-run.md").read_text()
        template = (WORKFLOW / "ref/writing-step-template.md").read_text()
        for text in (contract, template):
            self.assertIn("S1", text)
            self.assertIn("Current Run", text)
            self.assertIn("Evidence Space", text)
        self.assertIn("heading `<Run> · <Version/Step>`", contract)
        self.assertIn("Nothing follows the three links", template)
        self.assertIn("remain chat-only coordinates", template)

    def test_entering_an_open_run_returns_a_pre_step_review_packet(self):
        packet = (SKILLS / "page/haipipe-page/ref/user-check-packet.md").read_text()
        contract = (WORKFLOW / "ref/interactive-writing-run.md").read_text()
        for text in (packet, contract):
            self.assertIn("pre-Step", text)
            flat = " ".join(text.split())
            self.assertIn("latest", flat)
            self.assertIn("candidate", flat)
            self.assertIn("Current Run", text)
            self.assertIn("### PNN · Cn.Pm", text)
            self.assertIn("Mermaid Structure description", text)
            self.assertIn("own blockquote", text)
        self.assertIn("does not append a new", packet)
        self.assertIn("Do not append a Step", contract)
        self.assertIn("Never return only a status summary or links", packet)

    def test_step_records_track_changes_and_bounded_preference_inference(self):
        contract = (WORKFLOW / "ref/interactive-writing-run.md").read_text()
        template = (WORKFLOW / "ref/writing-step-template.md").read_text()
        presenter = (SKILLS / "page/page-plugins/haipipe-plugin-runs/SKILL.md").read_text()
        for required in (
            "#### Track changes", "###### Before", "###### After",
            "###### Why", "###### Analysis status",
        ):
            with self.subTest(field=required):
                self.assertIn(required, template)
        self.assertIn("word/punctuation-level red-delete/green-add", contract)
        self.assertIn("A single local preference is not automatically global law", contract)
        self.assertNotIn("#### Feedback classification", template)
        self.assertIn("do not duplicate it in a separate\nclassification table", template)
        self.assertIn(
            "acceptance, status, navigation, or presenter-only Step",
            " ".join(template.split()),
        )
        self.assertNotIn("###### Inferred preference", template)
        self.assertNotIn("###### Preference status", template)
        self.assertIn("surviving context stays plain", presenter)
        self.assertIn("never write visual markup back", presenter)
        self.assertIn("Render a card only when both fields exist and differ", presenter)
        self.assertIn("keep\nall earlier Steps collapsed", presenter)

    def test_steps_are_record_first_and_analysis_is_post_run(self):
        contract = (WORKFLOW / "ref/interactive-writing-run.md").read_text()
        template = (WORKFLOW / "ref/writing-step-template.md").read_text()
        analysis = (WORKFLOW / "ref/post-run-analysis.md").read_text()
        for text in (contract, template):
            with self.subTest(source=text[:40]):
                self.assertIn("record-first", text)
                self.assertIn("Analysis status", text)
        self.assertIn("post-run-analysis.md", contract)
        self.assertIn("launch one independent", contract)
        self.assertIn("Do not prepare it after every Step", analysis)
        self.assertIn("must never edit", analysis)
        self.assertIn("native rNN identity", analysis)

    def test_heavy_inter_run_work_requires_scoped_approval(self):
        policy = (WORKFLOW / "ref/interactive-execution-policy.md").read_text()
        page = (SKILLS / "page/haipipe-page/SKILL.md").read_text()
        workflow = (WORKFLOW / "SKILL.md").read_text()
        self.assertIn("explicit approval", policy)
        self.assertIn("between", policy)
        self.assertIn("explicit scoped approval", page)
        self.assertIn("interactive-execution-policy.md", page)
        self.assertIn("explicit approval", workflow)
        self.assertIn("interactive-execution-policy.md", workflow)
        self.assertIn("awaiting-approval", policy)
        self.assertIn("next Page Run may start immediately", policy)

    def test_fast_foreground_step_has_a_hard_small_scope(self):
        policy = (WORKFLOW / "ref/interactive-execution-policy.md").read_text()
        contract = (WORKFLOW / "ref/interactive-writing-run.md").read_text()
        workflow = (WORKFLOW / "SKILL.md").read_text()
        page = (SKILLS / "page/haipipe-page/SKILL.md").read_text()
        for text in (policy, contract, workflow, page):
            with self.subTest(source=text[:40]):
                self.assertIn("under two minutes", text)
                self.assertIn("sub-agent", text)
                self.assertIn("one bounded", text)
        self.assertIn("wording-only Step never edits the Page source", workflow)
        self.assertIn("wording-only Step does not touch the", policy)
        self.assertIn("If a required record is missing", contract)

    def test_handoff_and_runtime_boundary_are_explicit(self):
        packet = (SKILLS / "page/haipipe-page/ref/user-check-packet.md").read_text()
        self.assertIn("all three direct clickable links at the very end", packet)
        self.assertIn("lens=div", packet)
        self.assertIn("lens=evidence&focus=run-", packet)
        self.assertIn("[Current Run]", packet)
        self.assertIn("&run=<exact-run-id>", packet)
        self.assertIn("own Markdown blockquote", packet)
        self.assertIn("Prefix every sentence with a stable bold\n   review label", packet)
        self.assertIn("Sentence labels are\n   chat review coordinates only", packet)
        contract = (WORKFLOW / "ref/interactive-writing-run.md").read_text()
        self.assertIn("not a newly implemented CLI", contract)
        self.assertIn("waiting-for-feedback", contract)
        self.assertIn("Closed records", (SKILLS / "run/haipipe-run/SKILL.md").read_text())

    def test_step_run_close_and_page_release_have_distinct_write_boundaries(self):
        page = (SKILLS / "page/haipipe-page/SKILL.md").read_text()
        workflow = (WORKFLOW / "SKILL.md").read_text()
        contract = (WORKFLOW / "ref/interactive-writing-run.md").read_text()
        content = (SKILLS / "page/page-workflows/haipipe-page-content/SKILL.md").read_text()
        template = (WORKFLOW / "ref/writing-step-template.md").read_text()
        flat_contract = " ".join(contract.split())

        for text in (page, workflow):
            with self.subTest(source=text[:40]):
                self.assertIn("Writing Step", text)
                self.assertIn("Page Run close", text)
                self.assertIn("Page release", text)

        self.assertIn("Save the completed Step", contract)
        self.assertIn("Do not write adopted Page Content", contract)
        self.assertIn("required structure/Bullet RP Runs", flat_contract)
        self.assertIn("## Page release barrier", content)
        self.assertIn("generate the declared web/LaTeX/Word outputs once", content)
        self.assertIn("Evidence closure", template)
        self.assertIn("Delivery: deferred until all Page Runs", template)

    def test_page_run_identity_is_separate_from_task_run_identity(self):
        contract = (WORKFLOW / "ref/interactive-writing-run.md").read_text()
        run_contract = (SKILLS / "run/haipipe-run/SKILL.md").read_text()
        presenter = (SKILLS / "page/page-plugins/haipipe-plugin-runs/SKILL.md").read_text()
        for text in (contract, run_contract, presenter):
            with self.subTest(source=text[:40]):
                self.assertIn("rp-struct-01", text)
                self.assertRegex(text, r"rp-sec-(?:NN|\d{2})")
                self.assertRegex(text, r"rp-para-\d{2}_P\d{2}")
        for text in (contract, presenter):
            with self.subTest(scratch_source=text[:40]):
                self.assertRegex(text, r"rp-scratch-(?:NN|\d{2})")
        self.assertIn("r01", run_contract + presenter)
        self.assertIn("Delegated Paragraph Writing remains a Task Run", presenter)
        self.assertIn("The four RP kinds are sibling Page Runs", contract)

    def test_runs_function_proposes_only_human_interaction(self):
        runs_fn = (SKILLS / "page/haipipe-page/fn/runs.md").read_text()
        page = (SKILLS / "page/haipipe-page/SKILL.md").read_text()
        workflow = (WORKFLOW / "SKILL.md").read_text()
        run_contract = (SKILLS / "run/haipipe-run/SKILL.md").read_text()

        self.assertIn("fn/runs.md", page)
        self.assertIn("../../haipipe-page/fn/runs.md", workflow)
        self.assertIn("A proposal is not an allocated Run", runs_fn)
        self.assertIn("Do not mint\nany RP identity before selection", runs_fn)
        self.assertIn("Resume an existing matching\n   open Page Run", runs_fn)
        self.assertIn("code/search/data/build produces output", runs_fn)
        self.assertIn("normal Task Run", runs_fn)
        self.assertIn("A Page-owned `fn/Runs` candidate is also planning", run_contract)

    def test_page_has_explicit_structure_section_and_paragraph_run_ids(self):
        runs_fn = (SKILLS / "page/haipipe-page/fn/runs.md").read_text()
        contract = (WORKFLOW / "ref/interactive-writing-run.md").read_text()
        workflow = (WORKFLOW / "SKILL.md").read_text()
        run_contract = (SKILLS / "run/haipipe-run/SKILL.md").read_text()

        for text in (runs_fn, contract, workflow, run_contract):
            with self.subTest(source=text[:40]):
                self.assertIn("rp-struct-01", text)
                self.assertIn("P01..PN", text)
                self.assertIn("1 <= K <= N", text)
                self.assertIn("sibling", text)

        self.assertIn("Ten paragraphs may therefore produce 10, 8, or 6", runs_fn)
        self.assertIn("rp-sec-01", runs_fn)
        self.assertIn("rp-para-01_P03", runs_fn)
        self.assertIn("rp-para-02_P04-P05", runs_fn)
        self.assertIn("Section candidates become legal only after", runs_fn)
        self.assertIn(
            "but allocate only the selected next candidate",
            " ".join(workflow.split()),
        )
        self.assertIn("Candidate positions are planning labels", runs_fn)
        self.assertIn("next free identity whose kind matches", contract)

    def test_structure_run_fuses_shape_survey_and_allows_multiple_contributors(self):
        structure = (WORKFLOW / "ref/structure-run.md").read_text()
        outline = (SKILLS / "page/page-workflows/haipipe-page-outline/SKILL.md").read_text()
        runs_fn = (SKILLS / "page/haipipe-page/fn/runs.md").read_text()
        for text in (structure, outline, runs_fn):
            with self.subTest(source=text[:40]):
                self.assertIn("rp-struct-01", text)
                self.assertIn("SHAPE", text)
                self.assertIn("SURVEY", text)
                self.assertIn("participants", text)
                self.assertIn("contributors", text)
        self.assertIn("no separate", structure)
        self.assertIn("same paired Structure Result", runs_fn)

    def test_draft_paragraph_header_does_not_reserve_bullet_gutter(self):
        outline = (SKILLS / "page/haipipe-page/live/outline.py").read_text()
        self.assertIn(
            "details.paragraph-group>summary .addr{{min-width:0;margin-right:0}}",
            outline,
        )

    def test_evidence_labels_use_generic_display_namespace(self):
        families = (SKILLS / "page/haipipe-page/ref/page-run-families.md").read_text()
        page = (SKILLS / "page/haipipe-page/SKILL.md").read_text()
        evidence = (SKILLS / "page/page-workflows/haipipe-page-evidence/SKILL.md").read_text()
        displays = (SKILLS / "page/page-plugins/haipipe-plugin-outline/ref/evidence/displays.md").read_text()
        citations = (SKILLS / "page/page-plugins/haipipe-plugin-outline/ref/evidence/citations.md").read_text()

        for text in (families, page, evidence):
            with self.subTest(source=text[:40]):
                self.assertRegex(text, r"\$V_[A-Za-z0-9_-]+\$")
                self.assertRegex(text, r"\\figure\{D_[A-Za-z0-9_-]+\}")
                self.assertRegex(text, r"\\table\{D_[A-Za-z0-9_-]+\}")
                self.assertRegex(text, r"\\cite\{C_[A-Za-z0-9_-]+\}")
        self.assertIn("`DISPLAY` is the umbrella type", families)
        self.assertIn("display_kind", displays)
        self.assertIn(r"\figure{D_<slug>}", displays)
        self.assertIn(r"\cite{C_<slug>}", citations)
        self.assertIn("it does not create a new Run", families)


if __name__ == "__main__":
    unittest.main()
