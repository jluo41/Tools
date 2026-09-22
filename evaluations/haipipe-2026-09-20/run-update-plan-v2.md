# haipipe-run: revised update plan and consumer map

Date: 2026-09-20. Status: implemented; see the [implementation and validation report](run-implementation.md).

This plan follows the current Run inventory and replaces the implementation ordering in [the earlier findings and fix plan](run-findings-and-fix-plan.md). That report remains the evidence record for F01–F11. The proposal below is preserved as the planning record; its statements about future implementation and unrun checks describe the planning turn. The linked implementation report records the subsequent changes and observed results.

## 1. Intended purpose

`haipipe-run` should help an agent answer five practical questions:

1. Does this work qualify as an independently closable Run?
2. Which owner, Run profile, and native identity apply?
3. Should we reuse a Result, resume an existing Run, or allocate a new Run?
4. What must be recorded, and who can declare the work complete?
5. How do we count and present the work once across its consumers?

Recommended opening definition:

> A Run is one durable, addressable commission for a bounded target and close rule. Its authored Ticket and generated Result/receipt describe the same work. A Run may contain several Steps and execution attempts. Its owner defines allocation, execution, acceptance, and any permitted Version history.

Recommended Workflow definition:

> A Workflow is a list of Runs. Its definition describes planned work as Run Specs; its runtime lists the actual Run Instances. Dependencies and routes connect those entries and may permit branching, waiting, and parallel execution.

Keep the existing Type → Spec → Instance distinction. A Type supplies reusable defaults, a Spec commissions a bounded target, and an Instance is allocated work with a native address and receipt. Proposed work and controller activity can exist without an allocated Run. A simple Run does not require a new aggregate Workflow Runtime directory.

## 2. Who will use it?

The immediate reader is an agent operating a HAIPIPE skill. People can also invoke `haipipe-run` directly to design or audit Runs. Domain workers, workflows, and presenters need different portions of the contract.

Paths in the tables are relative to the repository root.

| Consumer | When it uses haipipe-run | What it needs | What that consumer continues to own |
|---|---|---|---|
| User-facing assistant invoking `haipipe-run` directly | “Is this a Run?”, “list our Runs”, “resume this work”, or “audit these Results” | Classification, owner resolution, history, counting, and missing-record diagnosis | Scope of the user's request; execution still goes through the selected domain owner |
| `haipipe-workflow` | Creating or auditing executable Run Specs | Type/Spec/Instance distinction, independent closure, cardinality, and actual-versus-planned inventory | Workflow composition, Spec routes, dependencies, frontier, and completion policy |
| `haipipe-task` and `haipipe-folder` | Allocating, scaffolding, executing, or locating a Task Run | Native identity, Ticket/Result resolver, receipt lifecycle, retry rules | Folder/Job layout, concrete runner, config, execution environment, and Task-specific output checks |
| `haipipe-discovery` and its Inquiry workflow | Admitting a source and deciding whether to reuse or analyze it | One commissioned Subject per Run, duplicate handling, pairing, and truthful outcomes | Subject admission, source access, facts, citations, Bib provenance, and analysis acceptance |
| Page workflow, Outline, Evidence, and Content agents | Planning bounded work; selecting RP/RE/RD or explicitly delegated paragraph work | Profile selection, allocation boundary, Step/Version rules, supporting identity, and scoped closure | Page plan, evidence semantics, writing acceptance, delivery checks, and whole-Page CHECK |
| Paper and Ideation agents | Commissioning judgment or missing evidence and coordinating Section work | Judgment versus writing profiles, native references, and distinction between planning templates and instances | Idea selection, Story decisions, Section release, and Paper-specific gates |
| `haipipe-insight-workflow` and `haipipe-page-insight` | Composing InsightBoard work or binding a base recipe to frozen research data | Reuse of native supporting Runs; RI binding, execution-version references, and count rules | Insight dependencies, DIKW interpretation, independent review, and publication |
| Design workflow and `haipipe-design-unit` | Commissioning, generating, or verifying a Design Item | Caller-owned identity/receipt, independent commission and review, frozen inputs | Design config, generation criteria, reviewer independence, and native result schema |
| Subjective Labeling workflows | Planning, allocating, resuming, and auditing the 25 operation kinds | Shared identity, pairing, attempts, terminal receipts, and counting | Operation catalogue, human authority, protected data handling, domain gates, and promotion |
| `table-workflow` | Showing a catalogue, specification table, runtime inventory, or human queue | Resolvable type/profile references, planned-versus-actual grain, and deduplication | Table shape, Workspace/Cell projections, and presentation |
| `table-task` and `haipipe-workbench-page` | Reading status and showing Run/Result records | Native resolvers, missing-record findings, display-state mapping, and one identity per Run | Read-only views; they do not allocate, execute, accept, or repair records on display |
| Project/Board maintainers and skill authors | Adding a dialect or changing shared Run behavior | Extension requirements and the consumer map | Project structure and their own domain contract; no new horizontal Folder owner is needed |

### Evidence for these consumers

Direct references are present in:

- [Task Workflow](../../plugins/haipipe-toolkit/skills/task/haipipe-workflow/SKILL.md), [Folder](../../plugins/haipipe-toolkit/skills/board/haipipe-folder/SKILL.md), and [Task hierarchy](../../plugins/haipipe-toolkit/skills/task/haipipe-task/ref/hierarchy.md).
- [Discovery](../../plugins/haipipe-toolkit/skills/discovery/haipipe-discovery/SKILL.md), [Page Workflow](../../plugins/haipipe-toolkit/skills/page/page-workflows/haipipe-page-workflow/SKILL.md), [Page Evidence](../../plugins/haipipe-toolkit/skills/page/page-workflows/haipipe-page-evidence/SKILL.md), and [Page Content](../../plugins/haipipe-toolkit/skills/page/page-workflows/haipipe-page-content/SKILL.md).
- [Paper](../../plugins/haipipe-toolkit/skills/paper/haipipe-paper/SKILL.md), [Ideation](../../plugins/haipipe-toolkit/skills/ideation/haipipe-ideation/SKILL.md), [Insight Workflow](../../plugins/haipipe-toolkit/skills/insight/haipipe-insight-workflow/SKILL.md), and [Task-side Insight](../../plugins/haipipe-toolkit/skills/task/page-types/haipipe-page-insight/SKILL.md).
- [Design worker](../../plugins/haipipe-toolkit/skills/design/haipipe-design-unit/SKILL.md), [Labeling](../../plugins/subjective-label/skills/subjective-label/SKILL.md), [Workflow tables](../../plugins/haipipe-toolkit/skills/0_utils/table-workflow/SKILL.md), [Task tables](../../plugins/haipipe-toolkit/skills/0_utils/table-task/SKILL.md), and [Run presenter](../../plugins/haipipe-toolkit/skills/page/haipipe-workbench-page/ref/run-space.md).

This is a traced consumer map, not a claim that every consumer implementation has been fully audited.

### Code that consumes the resulting records

These programs parse or write domain records. Updating `SKILL.md` does not automatically change their behavior.

| Implementation | Dependency relevant to this update |
|---|---|
| `servers/workbench-page/runs.py` | Reads native Tickets/receipts; recognizes writing operations and RP identities; maps status; locates Results. Keep waiting distinct from completion and diagnose missing receipts. |
| `skills/page/page-workflows/haipipe-page-content/cli/promote_paragraph.py` | Consumes the delegated paragraph profile. Preserve its distinction from interactive RP writing. |
| `skills/task/page-types/haipipe-page-insight/scripts/insight_items.py` | Resolves and validates RI execution identities, dataset bindings, versions, and review records. |
| `servers/workbench-design/design_actions.py` and `servers/workbench-design/design.py` | Allocate/write Design records and route UI actions. The current public action router rejects retired Adopt actions; historical helpers/records still exist. Preserve that distinction. |
| `skills/design/haipipe-design-unit/scripts/check_unit.py` | Enforces native Design Ticket and Result shapes; a generic receipt example cannot replace these schemas. |
| `plugins/subjective-label/engine/run_catalog.py` | Defines 25 operation names and computes planned instances. Its planned count is not proof of allocation. |

The first five paths are beneath `plugins/haipipe-toolkit/`. Inspect the specific reader/writer before changing a field, status, identity grammar, or resolver it uses.

## 3. Recommended skill structure

Apply progressive disclosure: common decisions remain in the entrypoint; detailed identity and receipt examples move to references that are loaded only when needed.

```text
skills/run/haipipe-run/
├── SKILL.md
├── ref/
│   ├── run-catalog.md
│   ├── identity-and-history.md
│   └── receipts-and-inventory.md
├── agents/openai.yaml
└── CHANGELOG.md
```

These are proposed files, not files created in this planning turn. Retain the repository's existing changelog convention. No new executable utility is justified by this documentation restructuring alone.

| File | Contents |
|---|---|
| `SKILL.md` | Purpose and trigger; minimal Run definition; six qualification tests; Type/Spec/Instance; ownership; short action-routing table; allocation/reuse lifecycle; completion versus promotion; one worked example; links to references |
| `ref/run-catalog.md` | Shared type/profile registration requirements, generic reference templates, domain-owner index, and explicit classification of current profiles, planning vocabulary, and historical forms |
| `ref/identity-and-history.md` | Native resolver rules; owner-qualified identity; retries, Steps, Versions, new commissions, aliases, and legacy-read behavior; links to exact domain grammars |
| `ref/receipts-and-inventory.md` | Required semantic facts and where to resolve them; honest timestamps and outcomes; coherent planned/running/terminal examples; inventory union, orphan diagnosis, deduplication, and display-state mapping |
| `agents/openai.yaml` | A short task-oriented prompt aligned with the entrypoint; preserve unrelated policy/dependency settings |
| `CHANGELOG.md` | The implemented contract changes and compatibility scope |

Suggested discovery description:

> Define, allocate, resume, count, or audit HAIPIPE Runs using their owning domain contracts. Use when deciding Run versus Step, resolving Ticket/Result/receipt identity, choosing reuse versus new work, or composing Workflow Run Specs.

Suggested default prompt:

> Use $haipipe-run to resolve the owner and bounded target, decide whether to reuse, resume, or allocate work, and apply the correct Ticket, Result, closure, and inventory rules.

The description should select this skill for HAIPIPE Run work. Ordinary shell execution or an internal worker call does not require a separate Run consultation. Load the shared contract once for the relevant operation and only the selected owner's profile afterward.

### Keep ownership explicit

| Authority | Owns |
|---|---|
| Shared Run contract | Minimum meaning of a Run; shared identity/history/lifecycle facts; registration and inventory rules |
| Domain owner/profile | Native naming and storage; permitted operations; concrete records; acceptance, retry/reopen details, and promotion authority |
| Workflow | Which bounded work is needed; dependencies, routes, cardinality, and overall completion |
| Worker | Performing the commissioned work and producing its declared outputs within the owner's rules |
| Presenter | Deriving views from those records |

A conflict between shared rules and an owner is reported and reconciled at its source. Reading another file is not permission to fabricate missing facts or silently override an incompatible contract.

## 4. Catalogue design and current coverage

Use one shared index to locate authoritative profiles. Keep detailed domain operation definitions in their current owner files. For example, Labeling continues to own its 25 operations and their gates; the shared index links to that catalogue instead of copying all of its acceptance rules.

For each indexed profile, record: owner, declared type/operation, bounded target, permitted actor, native identity/resolver, Result/receipt contract, close rule, history rule, and authoritative source. Mark incomplete or template-only entries explicitly. These are catalogue requirements; do not impose a new set of YAML fields on existing receipts without reader/writer changes.

| Area | Catalogue coverage required | Treatment |
|---|---|---|
| Execution | Scrape, build-data, fit, validate, write-file | Preserve the five generic reference templates; concrete commissioning still needs an executable owner/profile |
| Discovery | Paper analysis and source analysis | Link the canonical one-Subject profile |
| Page RP | Structure, Scratch, Section, paragraph/group | Four identity variants of interactive work; preserve their scoped close/history rules |
| Page delegated paragraph | `paragraph-writing` | Keep separate from the interactive RP profile |
| Page RE | Value, display, citation | Three focal-result variants; labels and display subtypes do not multiply Runs |
| Page independent display | Separately commissioned display production | Preserve the existing profile while resolving its owner/closure; rendering inside an RE remains internal work |
| Page RD | Delivery target and source version | Include it explicitly; output format is a target parameter, not an automatic new type per renderer |
| Insight RI | Frozen base-recipe/data/question/target binding | Preserve owner-qualified RI and exact execution-version references |
| Design | Commission, Generate, Verify | Three current types; mark Adopt as historical and Delivery as a read-only projection |
| Paper judgment | Idea, claim, evidence obligation, section narrative | Preserve the four named identities; require Paper to complete any missing close/receipt rules before declaring the profiles fully specified |
| Paper planning vocabulary | The ten `paper.*` coordination templates | Keep distinct from allocated records; map each to a resolved owner/profile or an explicit control action |
| Labeling | The 25 operation kinds | Link the domain catalogue and separate planned cardinality from actual inventory |

The previous seven-domain grouping is a human inventory aid. It is not a new mandatory `family` enum. Likewise, RP identity variants, RE focal types, generic templates, and independent operations should not be summed into a misleading universal Run-Type total.

Move the shared catalogue semantics out of `0_utils/table-workflow/ref/run-catalog.md` into the Run skill, updating direct consumers together. Keep the old reference path as a short forwarding document so existing links still resolve. Workflow tables continue to own catalogue presentation and Workspace/Cell layout. They should not maintain a second semantic list of active types.

Do not choose new normalized type keys just by lowercasing existing strings. For example, `Page.interactive-writing`, `page.interactive-writing.paragraph`, and `Page.paragraph-writing` require profile-aware resolution; the last is a different commissioned-work profile. Preserve native serialized values until their owners and readers support an explicit mapping.

## 5. Decisions the updated skill must make reliably

| Situation | Required decision |
|---|---|
| Planning a possible target | Create/retain a Spec or candidate; no invented runtime identity |
| Exact accepted Result already satisfies the target | Bind its native identity, version, and hash; no new Run |
| Matching open Run exists | Resume through its owner |
| Worker fails with unchanged frozen contract | Preserve failure; append an attempt when the owner permits retry |
| Ordinary feedback within an open interactive RP goal | Add a Step under the same Run |
| Reopening the same RP target | Use the owner's Version rule; do not generalize that exception to all domains |
| Later independently commissioned Section writing session | Follow the explicit Page rule allowing the next `rp-sec-NN`; scope alone does not uniquely identify a commission |
| Material change to frozen data, target, goal, or acceptance | Allocate a new Run through its owner; use supersedes only when the semantic relationship warrants it |
| New Insight dataset binding reuses a base R | Allocate RI; preserve base R and its history; do not create an extra wrapper for the same producer work |
| One Run appears in several Pages, Workspaces, or supporting references | Count the native Run once within the declared inventory scope; show consumers/aliases as references |
| Human click or gate evaluation | Keep it within its owner unless separately commissioned, bounded, independently closable, and durably recorded |
| Page delivery build versus Design Delivery view | Page RD can be commissioned work; the Design projection adds no Run |
| Known Ticket is missing its receipt | Report an incomplete allocation/orphan; do not silently omit it or claim it is a valid completed Run |
| Work is waiting for human feedback | Preserve waiting and null unfinished timestamps; no synthetic completion |

For Insight, distinguish the logical RI binding from its version-qualified execution reference. The inventory must state whether it is listing Run bindings or historical executions. Multiple versions do not imply newly allocated `riNN` bindings; reused evidence must still pin the exact version/hash.

### Receipt policy

- Specify shared semantic facts and their authoritative locations. Some facts are in the Ticket or profile, others in the runtime or Result. Avoid requiring every dialect to duplicate all facts in one universal YAML shape.
- Keep actor, worker, lifecycle status, terminal outcome, gate decision, and promotion distinct. A recorded `hold` decision can complete a bounded decision Run while its Workflow remains held.
- Use non-null RFC 3339 timestamps for events that actually occurred. Planned scaffolding does not establish `started_at` or `finished_at`; waiting is not termination.
- Replace the current mixed paragraph/interactive example with coherent examples in identified dialects. Preserve native writer ownership and atomic-write rules.
- Show valid allocated Runs and recovery-needed records separately while retaining one row per logical identity. State inventory scope and distinguish existing/reused Runs from newly allocated work.

## 6. Implementation sequence

Re-read target files and their diffs at the start of each batch. The current working tree contains substantial edits by other tasks, particularly Workflow tables, Insight, Page, and Board. Preserve and incorporate those changes.

| Batch | Concrete changes | Dependencies and completion condition |
|---|---|---|
| 1. Establish shared meaning | Rewrite the Run opening/ownership/action routing; clarify Workflow lists and their dependency graph, commission versus attempt, timestamps, and independent closure | Resolve F01/F09/F10. A reader can correctly decide between a Spec, Run, Step, attempt, and permitted Version without reading unrelated domains |
| 2. Refactor the entrypoint and catalogue | Add the three references; relocate detailed shared examples; update Files, description, UI metadata, and changelog; forward the old table-workflow catalogue and update its active examples | Depends on batch 1. One shared catalogue entry point; all profile links resolve; no active Design Adopt; missing RP Scratch/RD/Paper judgment represented honestly |
| 3. Align Task planning and reporting | Update `haipipe-task/ref/workflow-template.yaml`, `fn/stage-plan.md`, and `fn/stage-report.md` against `haipipe-workflow/ref/plan-schema.md`; align shared Workflow/runtime explanations | Depends on batches 1–2. Plans describe Specs; reports join actual native Runs/receipts; management commands and script cells do not become Runs automatically |
| 4. Align Page and Paper contracts | Reconcile `page-run-families.md`, interactive and delegated-writing profiles, Page glossary/workflow, Paper naming, judgment closure, and the Paper template map | Depends on the shared contract and current owner rules. Four RP kinds, RE, RD, delegated paragraphs, and Paper judgments have consistent routing; selection/release gates stay with their owners |
| 5. Close domain and presenter dependencies | Reconcile Design's current three types, Insight identity/version references, and Labeling's operation link; review `table-task`, `table-workflow`, Run presenter, Folder, STRUCTURE, and package README summaries | Depends on batches 2–4. Views agree with the relevant native records. Any required parser/writer change is scoped to its owning implementation |
| 6. Validate and document the result | Review changed references and examples; use the repository's fresh-context skill validation on representative isolated tasks; check affected readers/writers when implementation verification is in scope | Report observed behavior and remaining limitations. Do not call a documentation update a verified runtime migration |

Batch 2's catalogue relocation and consumer-reference changes should be one coherent patch. Do not leave two conflicting catalogues between implementation steps.

Page/Paper selector wording requires care: a current `[from <phase>]` argument may select a controller operation. Document the supported operation or implement a real Run selector with its parser; changing the help text alone cannot create that behavior. Avoid a repository-wide `Phase → Run` replacement.

Legacy record names, schema fields, and public routes remain readable according to their owner contracts. The update should not rename historical Runs or rewrite published Results.

## 7. Specific issues to settle during implementation

1. **Paper judgment closure.** The naming contract defines four IDs and journals, but does not provide a complete shared close rule. Paper must identify the closing actor, outcome, and required receipt. Do not infer idea admission or Section release from closing a discussion.
2. **Independent display versus RE display.** Keep the independent profile only for a separately commissioned, independently closable unit. Trace its concrete owner before advertising an executable capability.
3. **Type keys versus operation/identity variants.** Publish an explicit mapping for current writers. Preserve distinctions such as delegated paragraph-writing versus RP interactive-writing.
4. **Task storage resolution.** Current documents show different `$OUTPUT_ROOT` path orderings. Resolve the native path from the actual Task owner/runner before consolidating examples; no generic path substitution is justified yet.
5. **Labeling plan cardinality.** The 25 operation names agree with `engine/run_catalog.py`, but the Workflow now describes optional P0 work while `ref-run.md` and the planner still describe fixed P0 allocations. Keep its formula out of the shared skill and reconcile the domain sources if that planning path is changed.
6. **Consumer implementation limits.** The presenter has explicit RP/status recognition; a catalogue addition alone does not prove a new profile is displayed correctly. Likewise, retained Design Adopt helper code is not proof of a currently exposed UI action: the public router rejects those actions.

These are bounded owner tasks, not reasons to postpone the already supported shared-contract corrections. Keep unresolved capabilities labeled accurately.

## 8. Proposed validation and acceptance

No implementation checks were run for this planning turn. The following describes later validation; it is not a claim of passing results.

| Scenario | Observable result required |
|---|---|
| One target, several tool calls, one failed attempt and retry | One Run with preserved attempt history |
| One Spec commissions two independent targets | One parameterized Spec and two actual native Run records |
| Existing Result serves two Pages | One producing Run, exact reused references, no duplicate allocation |
| RP feedback, same-goal reopen, separate Section commission | Respectively Step, owner-defined Version, and a new commissioned Section Run |
| Scratch, RE display, and RD delivery | Correct distinct owner profiles; labels/render calls add no duplicate Runs |
| Planned, running, waiting, failed, and complete records | Honest timestamps and outcomes; UI state agrees with native evidence |
| One Design Commission, Generate, and Verify | Three allocated Runs; Delivery projection adds zero |
| New Insight binding plus subsequent publication version | New RI for changed binding; version-qualified provenance without false new binding counts |
| Paper judgment discussion closes | Durable scoped outcome; admission/release still requires its own owner gate |
| Labeling operation versus Round/Test/Scan episode | Count allocated operation records; episodes and per-item judgments add zero |
| Orphan Ticket/Result/runtime | Visible recovery finding with no invented repair facts |
| New Task plan and report | Follow the same Spec/Instance schema and join real receipts |

The root [README skill-development guidance](../../README.md) requires fresh-context validation for skill changes. During implementation, give the independent evaluator only a realistic request, the relevant skill, and minimal fixture artifacts; keep the expected answer with the evaluator's caller. Use an isolated directory, preserve the resulting evidence, and do not expose live project mutation as part of a fixture exercise.

The update is complete when a fresh reader can identify the owner, choose the right allocation/history action, find the authoritative profile, explain closure, and count actual work correctly—and the affected writers/readers agree with any changed serialized contract.

## 9. Expected user experience

A person should be able to say “continue this paragraph,” “analyze these sources,” or “show unfinished Runs.” The assistant selects the domain owner, consults the shared Run rules when needed, and returns understandable targets, status, Results, and the next required action. The person should not need to supply a Run Type key, Cell matrix, or receipt schema to request ordinary work.

The recommended first implementation patch is the shared Run entrypoint, its references, and the catalogue forwarding/alignment changes. Subsequent patches resolve the explicitly listed owner dependencies. This keeps the first result concrete and reviewable while making the limits of a skill-only change visible.
