import unittest
from pathlib import Path

from src.folder_contract import discover, read_contract, resolve
from src.plan_shape import type_outline


class ApplicationFolderArchitectureTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.skills = Path(__file__).resolve().parents[3]
        cls.application = cls.skills / "application"

    def test_application_has_six_insight_phase_owned_folder_contracts(self):
        contracts = [
            c for c in discover(self.skills)
            if c.workflow in {
                "haipipe-insight-workflow",
                "haipipe-design-workflow",
            }
        ]
        self.assertEqual(len(contracts), 6)
        self.assertEqual(
            {(c.phase, c.folder_kind, c.primary_face) for c in contracts},
            {
                ("I0", "meta", "page"),
                ("I1", "question", "page"),
                ("I2", "data", "task"),
                ("I3", "information", "page"),
                ("I4", "knowledge", "page"),
                ("I5", "wisdom", "page"),
            },
        )

    def test_phase_contracts_own_the_page_ruling_map(self):
        contracts = {
            c.phase: c for c in discover(self.skills)
            if c.workflow in {
                "haipipe-insight-workflow", "haipipe-design-workflow"
            }
        }
        self.assertEqual(
            {phase: contract.page_ruling for phase, contract in contracts.items()},
            {
                "I0": "none", "I1": "none", "I2": "none",
                "I3": "none", "I4": "none", "I5": "domain-gate",
            },
        )

    def test_application_page_type_skill_set_is_absent(self):
        page_types = self.application / "page-types"
        self.assertFalse(page_types.exists())
        old = (
            "haipipe-page-for-meta",
            "haipipe-page-for-question",
            "haipipe-page-for-data",
            "haipipe-page-for-information",
            "haipipe-page-for-knowledge",
            "haipipe-page-for-wisdom",
            "haipipe-page-for-brief",
            "haipipe-page-for-design",
            "haipipe-page-for-principle",
        )
        for path in self.application.rglob("*.md"):
            if "_old" in path.parts or path.name == "CHANGELOG.md":
                continue
            text = path.read_text(encoding="utf-8", errors="replace")
            for name in old:
                self.assertNotIn(name, text, str(path))
            self.assertNotIn("application/page-types", text, str(path))

    def test_application_workflow_is_cross_board_only(self):
        workflow = (
            self.application / "haipipe-application-workflow" / "SKILL.md"
        ).read_text(encoding="utf-8")
        for crossing in ("X0", "X1", "X2", "X3"):
            self.assertIn(crossing, workflow)
        for mapping in ("P0 =", "P1 =", "P2 =", "P3 =", "P4 ="):
            self.assertNotIn(mapping, workflow)
        self.assertIn("haipipe-insight-workflow", workflow)
        self.assertIn("haipipe-design-workflow", workflow)

    def test_new_application_scaffold_writes_folder_kind(self):
        enter = (
            self.application / "haipipe-application" / "fn" / "enter.md"
        ).read_text(encoding="utf-8")
        for kind in ("meta", "question", "brief"):
            self.assertIn("folder-kind: " + kind, enter)
        self.assertNotIn("page-type: principle", enter)

    def test_retired_design_phase_and_plugin_skills_are_absent(self):
        self.assertFalse(
            (self.application / "haipipe-application" / "fn" / "principle.md").exists()
        )
        retired = (
            "haipipe-design-card", "haipipe-design-verdict",
            "haipipe-design-division", "haipipe-design-pagedown",
            "haipipe-design-realization",
        )
        for name in retired:
            self.assertFalse(
                (self.application / "workflow-phases" / name).exists(), name
            )
        self.assertFalse((self.application / "haipipe-plugin-design").exists())

    def test_runs_is_optional_presenter_beneath_task_face(self):
        self.assertFalse(
            (self.skills / "board" / "page-plugins"
             / "haipipe-plugin-execution").exists()
        )
        runs = (
            self.skills / "board" / "page-plugins"
            / "haipipe-plugin-runs" / "SKILL.md"
        ).read_text(encoding="utf-8")
        self.assertIn("Runs, not Execution", runs)
        self.assertIn("Task Page", runs)
        self.assertIn("optional", runs)
        self.assertIn("JOB-BACKED TASK", runs)
        self.assertIn("FOLDER-LOCAL", runs)
        self.assertIn("<folder>/results/<run>/", runs)
        self.assertIn("<job>/results/<task>/<run>/", runs)

        discovery = (
            self.skills / "discovery" / "haipipe-discovery" / "SKILL.md"
        ).read_text(encoding="utf-8")
        self.assertIn("LOAD `haipipe-plugin-runs`", discovery)
        self.assertIn("`scripts/` stays optional", " ".join(discovery.split()))

        task = (
            self.skills / "task" / "haipipe-task" / "SKILL.md"
        ).read_text(encoding="utf-8")
        task_page = (
            self.skills / "task" / "haipipe-task" / "ref" / "task-page.md"
        ).read_text(encoding="utf-8")
        self.assertIn("Run/Result pairing", task)
        self.assertIn("<task>/results/<run>/", task)
        self.assertIn("Run overview belongs to `haipipe-plugin-runs`", task_page)
        self.assertIn("Never copy or symlink", " ".join(runs.split()))

    def test_insight_data_separates_relationship_from_evidence_authority(self):
        data = (
            self.application / "workflow-phases"
            / "haipipe-insight-data" / "SKILL.md"
        ).read_text(encoding="utf-8")
        self.assertIn("relationship and live status through the Folder's Run/Result", data)
        self.assertIn("accepted Run/Result", data)
        self.assertNotIn("PageX", data)
        self.assertNotIn("Probe", data)
        self.assertIn("every D value is bound by path", data)
        self.assertNotIn("accepted QA/run artifact", data)

        workflow = (
            self.application / "haipipe-insight-workflow" / "SKILL.md"
        ).read_text(encoding="utf-8")
        self.assertIn("accepted source Result backed by a named run", workflow)

    def test_insight_gi5_exports_then_gi6_settles(self):
        workflow = (
            self.application / "haipipe-insight-workflow" / "SKILL.md"
        ).read_text(encoding="utf-8")
        wisdom = (
            self.application / "workflow-phases"
            / "haipipe-insight-wisdom" / "SKILL.md"
        ).read_text(encoding="utf-8")
        self.assertIn("GI5 is the outward-export boundary", workflow)
        self.assertIn("I1-owned GI6 register\n  settlement", workflow)
        self.assertIn("GI5 passes only", wisdom)
        self.assertIn("GI6 is the following I1 register-settlement act", wisdom)

    def test_design_has_no_legacy_reader_references(self):
        self.assertFalse(
            (self.application / "haipipe-design-workflow" / "references"
             / "legacy-workflow.md").exists()
        )
        self.assertFalse(
            (self.application / "haipipe-design" / "references"
             / "legacy-board.md").exists()
        )
        self.assertFalse(
            (self.application / "haipipe-design" / "references"
             / "migration.md").exists()
        )

    def test_design_clean_break_forbids_compatibility_labels(self):
        design = (
            self.application / "haipipe-design" / "SKILL.md"
        ).read_text(encoding="utf-8")
        workflow = (
            self.application / "haipipe-design-workflow" / "SKILL.md"
        ).read_text(encoding="utf-8")
        required = "Unsupported Design bytes are not readable history"
        self.assertIn(required, " ".join(design.split()))
        self.assertIn(required, " ".join(workflow.split()))
        for text in (design, workflow):
            self.assertNotIn("read-only migration history", text.lower())
            self.assertNotIn("readable migration history", text.lower())

    def test_design_family_version_requires_human_major_release(self):
        names = (
            "haipipe-design",
            "haipipe-design-workflow",
            "haipipe-design-unit",
            "haipipe-design-brief",
        )
        approval_law = "Only explicit user approval may authorize `1.0.0`"
        for name in names:
            text = (self.application / name / "SKILL.md").read_text(
                encoding="utf-8"
            )
            self.assertIn('version: "0.4.0"', text, name)
            self.assertIn(approval_law, " ".join(text.split()), name)

    def test_design_address_and_render_lane_are_canonical(self):
        design = (
            self.application / "haipipe-design" / "SKILL.md"
        ).read_text(encoding="utf-8")
        render_fn = (
            self.application / "haipipe-application" / "fn" / "render.md"
        ).read_text(encoding="utf-8")
        self.assertIn("Design-<NN>-<audience>-<job>-<venue>", design)
        self.assertIn("delivery/render/", design)
        self.assertIn("<page>/delivery/render/", render_fn)
        self.assertNotIn("<page>/render/", render_fn)

    def test_render_has_folder_native_writer_and_optional_adapter(self):
        render = (
            self.skills / "board" / "page-plugins"
            / "haipipe-plugin-delivery" / "ref" / "render.md"
        ).read_text(encoding="utf-8")
        self.assertIn("haipipe-application/fn/render.md", render)
        self.assertIn("optional served adapter", render)
        self.assertIn("zero or more promoted-P versions PLUS every directly bound W handoff", render)
        self.assertNotIn("ghost until", render)

    def test_result_never_becomes_the_adoption_authority(self):
        design = (
            self.application / "haipipe-design" / "SKILL.md"
        ).read_text(encoding="utf-8")
        unit = (
            self.application / "haipipe-design-unit" / "SKILL.md"
        ).read_text(encoding="utf-8")
        self.assertIn("person adopts exact version", design)
        self.assertIn("caller", unit)
        self.assertIn("adopts results", unit)

    def test_brainstorm_entries_carry_reach_and_origin(self):
        modes = (
            self.application / "haipipe-design-unit"
            / "references" / "modes.md"
        ).read_text(encoding="utf-8")
        self.assertIn("per-member provenance", modes)
        self.assertIn("authorized insight", modes)
        self.assertIn("labeled intuition", modes)

    def test_runtime_board_names_are_subject_first_suffixes(self):
        application = (
            self.application / "haipipe-application" / "SKILL.md"
        ).read_text(encoding="utf-8")
        insight = (
            self.application / "haipipe-insight" / "SKILL.md"
        ).read_text(encoding="utf-8")
        self.assertIn("<DataSubject>-InsightBoard/", application)
        self.assertIn("<DesignTopic>-DesignBoard/", application)
        self.assertIn("<DataSubject>-InsightBoard/", insight)
        self.assertIn("optional A<NN>_ ordering prefix", insight)
        for stale in (
            "InsightBoard-<Cohort>", "A01_InsightBoard-SMSR2Full",
            "B01_DesignBoard-RefillFraming", "<Kind>-<Subject>",
        ):
            self.assertNotIn(stale, application)

    def test_design_stops_at_exact_adoption(self):
        workflow = (
            self.application / "haipipe-design-workflow" / "SKILL.md"
        ).read_text(encoding="utf-8")
        self.assertIn("Stop Design work once", " ".join(workflow.split()))
        self.assertIn("Only Commission → Generate → Verify → Adopt is routable", workflow)

    def test_probe_lane_is_legacy_read_only(self):
        workflow = (
            self.skills / "board" / "page-workflows"
            / "haipipe-page-workflow" / "SKILL.md"
        ).read_text(encoding="utf-8")
        phase = (
            self.skills / "board" / "haipipe-board" / "src" / "page_phase.py"
        ).read_text(encoding="utf-8")
        self.assertIn("never creates a new `probe/` lane", workflow)
        self.assertIn('evidence_lane_dirs(pd, "probe")', phase)

    def test_designer_agent_uses_current_thread_grammar(self):
        agent = (
            self.application / "haipipe-design" / "agents"
            / "haipipe-designer-agent.md"
        ).read_text(encoding="utf-8")
        self.assertIn("YAML Ticket", agent)
        self.assertIn("haipipe-design-unit/SKILL.md", agent)
        self.assertIn("Do not edit a card", agent)

    def test_design_unit_worker_does_not_own_a_folder_phase(self):
        worker = self.application / "haipipe-design-unit" / "SKILL.md"
        self.assertIsNone(read_contract(worker))
        self.assertIsNone(resolve(self.skills, folder_kind="design-unit"))
        current = type_outline("design", self.skills)
        self.assertEqual(Path(current["type_path"]),
                         self.application / "haipipe-design" / "SKILL.md")

    def test_venue_packs_are_profiles_not_private_lifecycles(self):
        venue = self.application / "venue"
        for readme in sorted(venue.glob("venue-*/README.md")):
            text = readme.read_text(encoding="utf-8")
            self.assertIn("design_profile:", text, str(readme))
            self.assertIn("terminal: adopted", text, str(readme))
            self.assertNotIn("stages:", text, str(readme))
            self.assertNotIn("claims_settlement:", text, str(readme))
            self.assertNotIn("adopted_A", text, str(readme))

    def test_named_domain_gates_do_not_hide_page_local_ticks(self):
        insight = (
            self.application / "haipipe-insight-workflow" / "SKILL.md"
        ).read_text(encoding="utf-8")
        design = (
            self.application / "haipipe-design-workflow" / "SKILL.md"
        ).read_text(encoding="utf-8")
        self.assertIn("cross-phase authority gates", insight)
        self.assertIn("nested Page-Face controls", " ".join(insight.split()))
        self.assertIn("adoption receipt satisfies", design)
        self.assertIn("must not solicit duplicate candidate acceptance", design)

    def test_native_design_and_page_workflows_are_orthogonal(self):
        design = (
            self.application / "haipipe-design" / "SKILL.md"
        ).read_text(encoding="utf-8")
        workflow = (
            self.application / "haipipe-design-workflow" / "SKILL.md"
        ).read_text(encoding="utf-8")
        self.assertIn("one Folder, two workflows", design)
        self.assertIn("rp-struct-01", design)   # the Page workflow's current Structure Run id (haipipe-page-outline)
        self.assertIn("rdNN_", design)
        self.assertNotIn("rNN_design_", design.split("## Clean-break contract")[0])
        self.assertIn("Page Runs cannot satisfy Commission release", workflow)
        self.assertIn("candidate content or behavior", workflow)
        self.assertIn("Page structure or explanatory prose", workflow)

    def test_application_preferences_use_phase_native_architecture(self):
        preferences = (
            self.application / "haipipe-application" / "PREFERENCES.md"
        ).read_text(encoding="utf-8")
        self.assertIn("matching I1-I5\n  Folder", preferences)
        self.assertIn("Commission → Generate → Verify → Adopt", preferences)
        self.assertIn("haipipe-design-unit", preferences)
        self.assertIn("It does not migrate Insight", preferences)
        self.assertIn("two orthogonal workflows", preferences)
        self.assertNotIn("Artifact Pages consume", preferences)
        self.assertNotIn("Brief→Insights→Design→Artifacts", preferences)

    def test_design_verb_closes_both_frontiers_without_shipping(self):
        design = (
            self.application / "haipipe-application" / "fn" / "design.md"
        ).read_text(encoding="utf-8")
        self.assertIn("haipipe-design-workflow", design)
        self.assertIn("Design frontier, Page frontier", design)
        self.assertIn("domain-gate", design)
        self.assertIn("Do not ship or measure", design)

    def test_page_run_is_folder_first_and_probe_is_retired(self):
        workflow = (
            self.skills / "board" / "page-workflows"
            / "haipipe-page-workflow" / "SKILL.md"
        ).read_text(encoding="utf-8")
        self.assertIn("authoritative `workflow/phase.yaml`", workflow)
        self.assertIn("Legacy outbound-card history is read-only", workflow)
        self.assertNotIn("remains canonical at\n`evidence/probe", workflow)
        self.assertNotIn("Resolve\n   the Page Type from the filename", workflow)

    def test_brainstorm_contract_has_no_fake_forecast(self):
        modes = (
            self.application / "haipipe-design-unit"
            / "references" / "modes.md"
        ).read_text(encoding="utf-8")
        self.assertIn("not experiment design", modes)
        self.assertIn("forecast and failure must be null", modes)

    def test_x2_application_workflow_owns_its_candidate_packet(self):
        workflow = (
            self.application / "haipipe-application-workflow" / "SKILL.md"
        ).read_text(encoding="utf-8")
        self.assertIn("schema: haipipe.application-candidate/v2", workflow)
        self.assertIn("packet_version: <N>", workflow)
        self.assertIn("generation_results", workflow)
        self.assertIn("verification_results", workflow)
        self.assertIn("adoption:", workflow)
        self.assertIn("terminal CHECK receipt", workflow)
        self.assertIn("not fabricated as Supporting Runs", workflow)

    def test_application_receipts_use_canonical_outline_logs(self):
        workflow = (
            self.application / "haipipe-application-workflow" / "SKILL.md"
        ).read_text(encoding="utf-8")
        self.assertIn("Design adoption/crossing index", workflow)   # the DS folder kind is retired (260918)
        self.assertIn("immutable human adoption receipt", workflow)
        for path in self.application.rglob("*.md"):
            if "_old" in path.parts or path.name == "CHANGELOG.md":
                continue
            text = path.read_text(encoding="utf-8", errors="replace")
            for stale in ("## Log", "Page Log", "DS Log", "BR00 Log", "Folder Log"):
                self.assertNotIn(stale, text, str(path))

        design_plugin = (
            self.application / "haipipe-design-workflow" / "SKILL.md"
        ).read_text(encoding="utf-8")
        self.assertIn("under `outline/`", design_plugin)
        self.assertIn("immutable adoption receipt", design_plugin)

    def test_shared_page_template_does_not_scaffold_retired_process_sections(self):
        template = (
            self.skills / "board" / "haipipe-board"
            / "ref" / "page-template.md"
        ).read_text(encoding="utf-8")
        self.assertIn("outline/<stem>-log.md", template)
        for heading in ("## States", "## Files", "## Discussion", "## Log"):
            self.assertNotRegex(template, rf"(?m)^{heading}$")

        creator = (
            self.skills / "board" / "agents"
            / "haipipe-page-creator-agent.md"
        ).read_text(encoding="utf-8")
        self.assertIn("outline/<stem>-log.md", creator)
        self.assertNotIn("`## States` rows", creator)
        self.assertNotIn("page's `## Log`", creator)

        task_template = (
            self.skills / "task" / "haipipe-task"
            / "ref" / "task-page-template.md"
        ).read_text(encoding="utf-8")
        self.assertIn("outline/<stem>-files.md", task_template)
        self.assertIn("outline/<stem>-log.md", task_template)
        for heading in ("## States", "## Files", "## Discussion", "## Log"):
            self.assertNotRegex(task_template, rf"(?m)^{heading}$")

    def test_task_insight_page_is_task_only(self):
        insight = (
            self.skills / "task" / "page-types"
            / "haipipe-page-insight" / "SKILL.md"
        ).read_text(encoding="utf-8")
        self.assertIn("insight-layout: items-v2", insight)
        self.assertIn("Historical\n`items-v1` records", insight)
        self.assertIn("one item owns", insight)
        self.assertIn("one `riNN` Insight Run binding", insight)
        self.assertNotIn("One Page covers one answerable insight question", insight)
        self.assertIn("scope: task", insight)
        self.assertIn("RF<n> Reusable Finding", insight)
        self.assertIn("RF is not a\nDesign Handoff", insight)
        self.assertIn("I1 QW", insight)
        self.assertIn("human-signed I5 Wisdom", insight)
        self.assertIn("parent: haipipe-page", insight)
        self.assertNotIn("haipipe-page-for-task", insight)
        for stale in (
            "scope: application", "Application Need", "Application Wisdom",
            "both scopes", "one of two scopes",
        ):
            self.assertNotIn(stale, insight)

        manifest = (
            self.skills / "task" / "page-types"
            / "haipipe-page-insight" / "agents" / "openai.yaml"
        ).read_text(encoding="utf-8")
        self.assertIn('display_name: "Task Insight Page"', manifest)
        self.assertIn("DIKW findings", manifest)
        self.assertNotIn("Application-local", manifest)
        self.assertNotIn("Design Handoff", manifest)

        entry = (
            self.skills / "task" / "haipipe-task" / "fn" / "insight.md"
        ).read_text(encoding="utf-8")
        self.assertIn("`I<NN>-<slug>/` Folder", entry)
        self.assertNotIn("folded Q or S Page", entry)

    def test_task_page_contract_is_owned_by_task_door(self):
        retired = (
            self.skills / "task" / "page-types" / "haipipe-page-for-task"
        )
        self.assertFalse(retired.exists())

        task_skill = (
            self.skills / "task" / "haipipe-task" / "SKILL.md"
        ).read_text(encoding="utf-8")
        task_contract = (
            self.skills / "task" / "haipipe-task" / "ref" / "task-page.md"
        ).read_text(encoding="utf-8")
        task_template = (
            self.skills / "task" / "haipipe-task" / "ref"
            / "task-page-template.md"
        ).read_text(encoding="utf-8")

        self.assertNotIn("legacy_page_type:", task_skill)
        self.assertIn("folder_kind: task", task_skill)
        self.assertIn("folder_owner: canonical", task_skill)
        self.assertIn("primary_face: task", task_skill)
        self.assertIn("page_ruling: local", task_skill)
        self.assertIn("Board rendering belongs to `haipipe-board`", task_skill)
        self.assertIn("Task Folder = Page Folder", task_skill)
        self.assertNotIn("haipipe-page-for-task", task_skill)
        self.assertIn("Supporting Runs", task_contract)
        self.assertIn("<!-- realizes: C<n>.P<m>.B<k> -->", task_contract)
        self.assertIn("<task>.md#reading-current", task_contract)
        self.assertIn("there is no separate Page\n`accepted:` field", task_contract)
        self.assertIn("folder-kind: task", task_template)
        self.assertNotIn("page-type: task", task_template)
        self.assertNotIn("## Diagram", task_template)
        self.assertEqual(6, task_template.count("**Division map —"))
        self.assertIn('<a id="reading-current"></a>', task_template)
        self.assertIn("| R01 |", task_template)

        item_table = (
            self.skills / "board" / "page-plugins" / "haipipe-plugin-outline"
            / "ref" / "item-table.md"
        ).read_text(encoding="utf-8")
        self.assertIn("exactly one owner-native", item_table)
        self.assertIn("Supporting or Task-local: parent `bNNjNNtNN`", item_table)
        self.assertIn("new-run → registered → reuse", item_table)
        self.assertIn("A failed attempt\nends as `rerun`", item_table)
        self.assertNotIn("exactly one Paper-local", item_table)

    def test_application_and_task_insight_routes_do_not_share_a_page_type(self):
        application = (
            self.application / "haipipe-application" / "SKILL.md"
        ).read_text(encoding="utf-8")
        self.assertIn("These routes do not share a Page Type", application)
        self.assertIn("separate I2 Data, I3 Information", application)
        self.assertNotIn("The two scopes share one contract", application)

        task_readme = (
            self.skills / "task" / "README.md"
        ).read_text(encoding="utf-8")
        self.assertIn(
            "I1 registration → signed I5 bridge → Design Commission → Generate → Verify → Adopt",
            task_readme,
        )
        self.assertNotIn("Application selects K/W", task_readme)
        self.assertNotIn("Brief → Intervention → Artifact", task_readme)

        manifest = (
            self.application / "haipipe-application"
            / "agents" / "openai.yaml"
        ).read_text(encoding="utf-8")
        self.assertIn("Design Commission/Generate/Verify/Adopt", manifest)
        self.assertIn("Design Page frontiers separately", manifest)
        self.assertNotIn("Artifact frontier", manifest)

    def test_task_rf_requires_an_application_owned_signed_bridge(self):
        application = (
            self.application / "haipipe-application" / "SKILL.md"
        ).read_text(encoding="utf-8")
        chain = (
            self.application / "haipipe-application" / "fn" / "chain.md"
        ).read_text(encoding="utf-8")
        insight_workflow = (
            self.application / "haipipe-insight-workflow" / "SKILL.md"
        ).read_text(encoding="utf-8")
        insight_door = (
            self.application / "haipipe-insight" / "SKILL.md"
        ).read_text(encoding="utf-8")
        wisdom = (
            self.application / "workflow-phases"
            / "haipipe-insight-wisdom" / "SKILL.md"
        ).read_text(encoding="utf-8")
        design_workflow = (
            self.application / "haipipe-design-workflow" / "SKILL.md"
        ).read_text(encoding="utf-8")

        self.assertIn("pre-climbed external parent", application)
        self.assertIn("Application I1 QW", application)
        self.assertIn("Application I5 W", application)
        self.assertIn("signed Application W", application)
        self.assertNotIn("no local chain page needed", application)
        self.assertIn("Task RF never binds directly to Design", chain)
        self.assertIn("Pre-climbed external parent", insight_workflow)
        self.assertIn("I1 QW → I5 contextual W", insight_workflow)
        self.assertIn("unrelated open items do not block", insight_workflow)
        self.assertIn("RF itself never satisfies X1", insight_workflow)
        self.assertIn("RF never reaches Design directly", insight_door)
        self.assertNotIn("local P2", insight_door)
        self.assertIn("Task Insight instance/item@execution-version/RF<n>", wisdom)
        self.assertIn("exact external K/W/RF row ids", wisdom)
        self.assertIn("signed: ✅ <initials> <YYMMDD>", wisdom)
        self.assertIn("signed contextual W handoff", design_workflow)

    def test_endpoint_target_uses_canonical_task_folder_surfaces(self):
        endpoint = (
            self.skills / "task" / "3_end"
            / "haipipe-task-for-endpoint" / "SKILL.md"
        ).read_text(encoding="utf-8")
        for surface in (
            "t01_<task_name>.md", "workflow/inbox/application/",
            "folder-kind: task", "scripts/config/r01_base.yaml",
        ):
            self.assertIn(surface, endpoint)
        self.assertNotIn("evidence/pagex/", endpoint)
        self.assertIn("flat endpoint jobs remain readable", endpoint)
        self.assertNotIn("├── 1_{task_name}.py", endpoint)

    def test_application_chain_names_phase_owned_folder_contracts(self):
        chain = (
            self.application / "haipipe-application" / "fn" / "chain.md"
        ).read_text(encoding="utf-8")
        self.assertIn("phase-owned Folder contracts", chain)
        self.assertNotIn("page-type contracts", chain)

    def test_presenters_route_pagex_and_render_to_their_real_owners(self):
        outline = (
            self.skills / "board" / "page-plugins"
            / "haipipe-plugin-outline" / "SKILL.md"
        ).read_text(encoding="utf-8")
        delivery = (
            self.skills / "board" / "page-plugins"
            / "haipipe-plugin-delivery" / "SKILL.md"
        ).read_text(encoding="utf-8")
        live_delivery = (
            self.skills / "board" / "haipipe-board" / "live" / "delivery.py"
        ).read_text(encoding="utf-8")
        self.assertIn("A Page-owned Evidence attempt is an `RE`", outline)
        self.assertIn("ref/evidence/pagex.md", outline)
        self.assertNotIn("haipipe-plugin-evidence/ref/pagex.md", outline)
        self.assertIn("Folder-native `haipipe-application/fn/render.md`", delivery)
        self.assertNotIn("ghost until the lane's route ships", delivery)
        self.assertIn('base / "delivery" / "render"', live_delivery)
        self.assertNotIn("route pending", live_delivery)

    def test_generic_page_plugins_keep_five_categories_and_allow_domain_extensions(self):
        root = self.skills / "board" / "page-plugins"
        found = {
            path.parent.name
            for path in root.glob("*/SKILL.md")
        }
        self.assertEqual(
            found - {"haipipe-plugin-design"},
            {
                "haipipe-plugin-outline",
                "haipipe-plugin-studio",
                "haipipe-plugin-runs",
                "haipipe-plugin-delivery",
                "haipipe-plugin-folder",
            },
        )
        self.assertIn("haipipe-plugin-design", found)
        self.assertTrue((root / "haipipe-plugin-design" / "SKILL.md").is_file())
        self.assertTrue((root / "haipipe-plugin-studio" / "ref" / "chat.md").is_file())
        self.assertTrue((root / "haipipe-plugin-studio" / "ref" / "draw.md").is_file())
        self.assertTrue((root / "haipipe-plugin-outline" / "ref" / "skill-record.md").is_file())
        for lane in ("latex", "word", "slide", "render"):
            self.assertTrue((root / "haipipe-plugin-delivery" / "ref" / f"{lane}.md").is_file())

    def test_design_worker_and_meeting_ownership_are_outside_page_plugins(self):
        self.assertTrue((self.application / "haipipe-design-unit" / "SKILL.md").is_file())
        self.assertFalse((self.application / "haipipe-plugin-design").exists())
        meeting = self.skills / "project" / "haipipe-project-meeting" / "SKILL.md"
        self.assertTrue(meeting.is_file())
        self.assertIn("<project>/meetings/", meeting.read_text(encoding="utf-8"))

        serve = (
            self.skills / "board" / "haipipe-board" / "cli" / "serve.py"
        ).read_text(encoding="utf-8")
        self.assertNotIn("from live.meeting import", serve)
        self.assertIn('"/_board/meeting-entry"', serve)
        self.assertIn("Page-local meetings are retired", serve)

    def test_content_has_no_phase_redirect_skills_or_agents(self):
        workflows = self.skills / "board" / "page-workflows"
        self.assertFalse((workflows / "haipipe-page-draft").exists())
        self.assertFalse((workflows / "haipipe-page-revise").exists())
        self.assertFalse((workflows / "agents" / "haipipe-page-draft-agent.md").exists())
        self.assertFalse((workflows / "agents" / "haipipe-page-revise-agent.md").exists())

    def test_verify_and_adopt_keep_render_version_bound(self):
        workflow = (
            self.application / "haipipe-design-workflow" / "SKILL.md"
        ).read_text(encoding="utf-8")
        self.assertIn("delivery/render/", workflow)
        self.assertIn("render manifest/version", workflow)
        self.assertIn("Review pass cannot adopt", workflow)

    def test_page_serving_job_is_not_paper_specific(self):
        specialist = (
            self.skills / "task" / "10_page"
            / "haipipe-task-for-page" / "SKILL.md"
        ).read_text(encoding="utf-8")
        self.assertIn("b<NN>_page_service", specialist)
        self.assertIn("whether their owning Folder belongs to Paper", specialist)
        self.assertNotIn("one block per paper's service jobs", specialist)


if __name__ == "__main__":
    unittest.main()
