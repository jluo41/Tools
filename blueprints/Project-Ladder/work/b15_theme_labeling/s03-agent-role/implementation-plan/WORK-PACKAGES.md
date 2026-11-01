# Dependency-ordered engineering work packages

Version: 2  
Reconciled on 2026-11-01 to slide deck version 12 (Train and Test, Execution & Audit Agent, round report); version 1 was written against version 8.

All paths below are relative to Tools-SPACE unless explicitly qualified. Proposed filenames are assignments, not evidence that files exist. No model campaign or production labeling Run is authorized by this document alone.

## 1. Ownership and dependency map

Abbreviations: E = plugins/haipipe-toolkit/skills/2_theme/labeling/engine; W = plugins/haipipe-toolkit/servers/workbench-labeling/workbench-task-labeling; H = plugins/haipipe-toolkit/servers/_host; B = blueprints/Project-Ladder/work/b15_theme_labeling.

Roles: A owns engine contracts and Meaning; B owns Workbench presentation and interaction; C owns evaluation/executor components; R is the coordinator and final reviewer. These are engineering work assignments, not the runtime Meaning Loop Agent and Execution & Audit Agent.

| ID | Deliverable | Owner | Dependencies | Milestone |
|---|---|---|---|---|
| T00 | Baseline, ownership and fixture inventory | R | None | M0 |
| T01 | Validated records and version contracts | A | T00 | M1 |
| T02 | Atomic report/draft/submission store | A | T01 | M1 |
| T03 | Stable decision-card renderer | B | T01 | M1 |
| T04 | Workbench response API and permissions | B | T02, T03 | M1 |
| T05 | Real Workbench vertical-slice acceptance | R | T04 | M1 |
| T06 | Corpus itemization and Train/Test custody | C | T01 | M2 |
| T07 | Human sources, Train evidence and audit issues | A | T01, T06 | M2 |
| T08 | Report planner and publication tools | A | T02, T07 | M2 |
| T09 | Semantic integration and issue resolution | A | T08 | M2 |
| T10 | Approved references and diagnostics | A | T09, T06 | M2 |
| T11 | Asynchronous Meaning harness | A | T08–T10 | M2 |
| T12 | Executor adapter and result validation | C | T01, T06 | M3 |
| T13 | Staging evaluation and disclosure boundary | C | T10, T12 | M3 |
| T14 | Meaning-preserving candidate generation | A | T09, T10, T12 | M3 |
| T15 | Step 5 staging loop and round report | C | T13, T14 | M3 |
| T16 | Loop status and feedback visibility | B | T11, T15 | M3 |
| T17 | Release readiness check and frozen handoff | C | T15 | M4 |
| T18 | Resumable production and audit routing | C | T17 | M4 |
| T19 | Production review and acceptance | A | T18 | M4 |
| T20 | Research tickets, skills and slide alignment | R | M2, M3 or M4 evidence as appropriate | M5 |

Critical path for the first usable delivery: T00 → T01 → T02/T03 → T04 → T05. Do not delay the first real form for model optimization. C may investigate T06 during M1 but must not change T01 interfaces unilaterally.

Each package must return: changed source paths, user-visible behavior, tests actually run, failures/limitations, migration effects and the smallest runnable demonstration. A screenshot alone is never sufficient evidence of durable submission.

## 2. M0 and M1: form to durable human feedback

### T00. Inventory the current checkout

Owner R. Read applicable repository and skill instructions, current blueprint and target files. Record existing modifications and file ownership before editing. Verify the existing targeted tests, private lane resolution and browser entry route. Capture only non-secret settings needed for the configured Workbench origin. Do not reset, commit, move or reformat unrelated work.

Outputs: source inventory, fixture selection, file-owner table, baseline result and actual Workbench route. Acceptance: another agent can reproduce the baseline and identify which existing files it may edit. If the server is unavailable, record that limitation; do not report browser acceptance until it is available and checked.

### T01. Define and validate the records

Owner A. Proposed E/meaning_contracts.py and E/test_meaning_contracts.py. Implement bounded validators for sources, cards, reports, drafts, submissions, semantic snapshots, reference releases, issues and round reports. Use existing project dependencies when possible. Define error types and schema versions. Include exact approval scope, actor evidence, immutable option IDs, base versions and synthetic fixture markers.

Inputs: CONTRACTS.md and existing job configuration. Outputs: pure validators, normalization rules and synthetic fixtures consumed by B and C. Functions should include validate_report(), validate_submission(), validate_meaning_snapshot(), validate_reference_release() and validate_round_report(); exact signatures must be settled before T02/T03 start.

Acceptance: reject duplicate decision IDs, missing source references, unsafe identifiers, unknown choices, contradictory statuses, invalid approval scope, Test text where only a custody reference is allowed, confirmation item evidence and a round report without a route or its reason. Preserve original comments exactly. Validation is deterministic and makes no model calls. Check schema upgrades explicitly; never infer compatibility from similarly named fields.

### T02. Implement the authoritative store

Owner A. Proposed E/meaning_store.py and E/test_meaning_store.py. Implement publish_report(), load_report(), save_draft(), submit_feedback(), read_submission(), list_pending_integrations() and commit_integration(). Store new records under J/meaning/. Reuse an existing lock only after checking process/platform behavior and lock scope.

Publish immutable reports. Save mutable per-actor drafts using compare-and-swap revisions. Submit an atomic immutable bundle with an outbox entry. A repeated request ID and exactly equal normalized payload returns the same receipt; a different payload with the same ID is rejected. Indexes are rebuildable. Disk or worker failure must never become a false successful integration.

Acceptance: two tabs cannot overwrite without conflict; duplicate submit yields one receipt; interrupted writes leave either no committed bundle or one valid bundle; pending work survives restart; obsolete report answers cannot be mapped onto new option IDs. After a lost response, advance the draft and supersede the report, then replay the same committed request and recover its original receipt. Changed reuse fails, and another actor cannot retrieve it. Delete derived indexes and rebuild the same lifecycle status while immutable report/submission payloads remain unchanged. Check partial submission, draft conflict, withdrawn reports, permission changes, missing source, malformed input and replay. No content hashes.

### T03. Build the reusable decision-card view

Owner B. Proposed W/decision_report_view.py plus scoped JavaScript/CSS under the existing labeling asset mechanism. Confirm actual asset routing before choosing paths. Use the existing prototype as interaction evidence, not a replacement for the Workbench shell.

Render title, version, source excerpts, question, current rule, contrasting cases, options, exact change scope, comments, none, defer and unanswered state; an audit-issue card also shows its origin partition and versions. No option is preselected. A custom answer requires text. Deferral is distinct from rejection. Show saved/submitted/awaiting integration states. Use a concise progress count and individual card navigation without forcing all cards to be answered.

Acceptance: keyboard selection, focus visibility, readable mobile layout, escaped user/source text, no executable generated HTML, no hidden default consent, recoverable save errors and distinguishable draft vs submitted version. Long excerpts expand without hiding the question. A stale report displays an explanation and cannot silently submit against a replacement.

### T04. Connect the real Workbench route

Owner B is the sole editor of W/labeling.py for this milestone. Add narrow draft-save and feedback-submit actions to the existing /_board/labeling/act route. Resolve Page/job/actor permissions on the server. Reuse current same-origin and request authentication mechanisms. Publishing and integrating reports remain engine tools, not browser response actions.

Render decision-report mode in the meaning Task's Preferences view on the focus page (labeling_focus.py; b15 s13 maps Step 3 to it, s58 C3 draws it: one turn's cards as a /haipipe-interaction collect Run, answered only in the meaning Task) and keep legacy item calibration intact in the Rounds view. The browser receives display data, not filesystem paths or private references. Return structured validation/stale/version errors and the durable submission receipt. Use the authentication evidence mode described in CONTRACTS.md. Do not describe a typed human_id as a verified person. R separately owns the narrow H/serve.py pre-parse body-size guard needed before this action receives the payload; B does not edit the host file. Verify malformed/oversized lengths fail before unbounded body reading and preserve unrelated endpoint limits.

Acceptance: allowed local operator saves and submits; unrelated job access, traversal, spoofed participant, unauthorized POST and reads of Test or confirmation evidence outside the assigned cards fail. Legacy first/final actions retain baseline behavior. Shared external respondents stay disabled until a narrow assigned-job response capability is implemented and tested; never grant broad SPACE owner permission to enable form submission.

### T05. Review the complete vertical slice

Owner R, with B fixing UI findings and A fixing store findings. Publish a synthetic report through the engine, open it in the meaning Task's Preferences view, answer several cards, save, reload, submit a partial form, inspect the persisted bundle, restart/reload and inspect the same receipt. A deterministic fake agent consumes the outbox and records a proposed next action. It cannot claim to have performed real model reasoning.

Acceptance evidence: real browser screenshots, action responses, persisted synthetic records and tests for the same actions. Check desktop, narrow screen, two-tab conflict, offline/save failure, double click and post-submit editing. Keep new edits as a new draft; do not mutate the earlier submission. Human approval of a rule is visibly different from approval of item labels. M1 is complete only after this path works within Workbench.

## 3. M2: Meaning Loop

### T06. Prepare items and enforce data custody

Owner C. Review E/items_task.py, corpus_preparation.py, fence_source.py and corpus_tools.py. Proposed E/split_access.py and synthetic tests. Preserve source identity, context windows, correlated groups and legacy labels while making stable items. Assign Train and Test roles by source group before exploration, retrieval, embedding or report generation, keeping related sources together. A fresh independent confirmation set, when one is needed, goes straight to custodian storage and never enters agent-visible roots. Exposed legacy data must carry that history.

Implement separate custody projections and allowlisted service capabilities. The refiner-visible root holds only Train content. Executors receive their assigned Train or Test items; the scorer and the auditor receive Test references and case-level records from custody; the Meaning Loop Agent and human review resolve only the Test cases a round report names. Confirmation content reaches only its authorized confirmation roles. Returning a text flag named split is not access control. Check files, search indexes, caches, logs, tool responses and shared conversation memory for leaks. Grouping/similarity checks must not introduce content hashes.

Acceptance: overlapping groups fail; duplicate/sibling items cannot cross silently; every retrieval route open to the expression rewriting step rejects Test and confirmation items; the Meaning Loop route resolves only Test cases a round report names; aggregate disclosure policy is enforceable. Existing legacy jobs retain their recorded split history. If secure process/filesystem isolation is unavailable, label the boundary as procedural, not enforced.

### T07. Collect human sources and retrieve evidence

Owner A. Proposed E/meaning_sources.py and associated tests, using corpus_tools through the authorized projection. Record original ideas, notes, chat excerpts, supplied sources and prior decisions with locations and authority. Preserve human wording separately from agent interpretation. Sources are read-only evidence until a scoped decision gives them authority.

Retrieve representative Train cases, contrasts, potential contradictions and missing contexts, and open the Train or Test cases a round report names, with their original context. Record why each case is selected and which rule/question it supports. Maintain coverage and redundancy information; do not present a score as proven uncertainty. Existing labels are evidence to investigate, not a clean reference set by default.

Acceptance: each quotation and item link resolves; inaccessible sources fail clearly; instructions inside corpus text do not control the harness; revisions preserve originals. confirmed_decision requires a valid scoped approval event; changing an input enum cannot grant authority. Retrieval cannot see confirmation content, or Test content beyond the cases a round report names. Check both rough-idea and legacy-labeled entry cases against the same source contract.

### T08. Plan and publish decision reports

Owner A. Proposed E/meaning_reports.py and tests. Build a queue of issues, including those round reports raise, and combine related questions into short, coherent reports. When a round report reopens the Meaning Loop, investigate related cases, earlier decisions and original context first, and prepare cards only for the questions that remain. Generate options with distinguishable consequences, neutral wording, examples and scope. Include none/custom/defer. Record exact proposed rule patches when feasible and dependencies between decisions.

Validate the report before publication. Source lineage, evidence eligibility (Train cases, or Test cases by audit-issue reference), version consistency and option completeness are deterministic checks. Model-generated reports may propose content but cannot manufacture human approval. Avoid a fixed ten-card requirement: batch size is configurable and evaluated by time and completion, not an arbitrary count.

Acceptance: an issue yields a valid report or a specific blocked reason. Contradictory options, missing supporting cases, confirmation examples, copied Test text and references to replaced rules fail validation. Synthetic fake-model outputs exercise publication without external calls. A published revision cannot be edited in place.

### T09. Integrate decisions and resolve contradictions

Owner A. Proposed E/meaning_integrate.py and tests. Consume submissions, resolve dependencies, construct scoped rule changes and run consistency checks. An explicitly submitted clear selection of an exact displayed patch can approve that patch. A conditional comment, custom answer or ambiguous interpretation produces a new proposal requiring confirmation. The prototype's rule_preference_only exports never gain broader authority during import.

Represent contradictions as issue records with source evidence, affected rules/items and choices: context distinction, explicit exception, priority, revised preference or unresolved. Do not accuse a human of inconsistency or automatically average conflicting preferences. Only dependent outputs are blocked. Track which older decisions a new confirmed rule supersedes.

Acceptance: no repeated confirmation for already exact approvals; no semantic expansion from broad comments; conflicting submissions remain inspectable; independent accepted decisions can release while one issue is deferred. Repeated partial submissions with different request IDs do not duplicate a rule effect; changed answers have explicit supersession/conflict lineage. Fault-inject each multi-artifact integration stage and prove readers see either the previous release or one complete committed release, never mixed policy/reference state. A new semantic release invalidates affected candidates/references without deleting history.

### T10. Produce references and diagnostic policy

Owner A, C reviews evaluation boundaries. Proposed E/meaning_references.py and tests. Associate task labels with semantic version, evidence, approval route and review state. Keep inferred labels separate from directly reviewed reference labels. Batch acceptance needs an explicit policy and audited scope; it does not turn every item into individually approved gold.

Add diagnostic fields for ambiguity, review effort, uncertainty reason and next action. Keep these separate from task label and raw model confidence. Write operational definitions and examples into the approved uncertainty policy. Train and Test items are both labeled, scored and audited, through separate roles. Human review of Test items may inform Meaning Loop decisions, but Test text, labels and case-level errors never flow into the expression rewriting context, logs, memory or examples. Confirmation items stay outside all development and adjudication feedback.

Acceptance: unclear context can abstain; difficult-but-clear differs from ambiguous; reference approval never follows merely from approving a rule; every reference binds an approved meaning version. Confirmation judgments are collected before showing executor predictions/model identity; assisted judgments, including Test corrections reviewed after executor disagreement, are recorded separately. Unresolved or obsolete references are excluded from scoring with counts disclosed. Test and confirmation adjudication and later schema changes follow EVALUATION.md.

### T11. Orchestrate asynchronous Meaning work

Owner A. Proposed E/meaning_harness.py and tests. Drive round report intake and source ingestion → investigation and retrieval → report preparation → publication → pending feedback → integration → semantic/reference release → compatible versions returned to Step 5. Tools do deterministic persistence; the agent selects and reasons. Store checkpoints and idempotent work IDs. A synthetic round report exercises the intake before T15 exists.

While waiting, allow independent case collection, previously approved labeling and other non-dependent work. Do not assume timeout means approval. New feedback triggers the affected branch. A later source can reopen a settled issue with explicit lineage. Publish budgets for tools, report count and retry behavior; stop with a readable reason when a budget is exhausted.

Acceptance: restart from pending feedback; duplicate event delivery has one integration; one deferred card does not freeze unrelated tasks; stale feedback is reconciled explicitly; rule, preference and reference-label questions from round reports reach humans only after Step 2 investigation, never directly. First validate with deterministic fake tools; real calls require a separately authorized Run.

## 4. M3: Step 5 staging loop and visible control

### T12. Call fixed executor models reliably

Owner C. Proposed E/executor_runtime.py and E/executor_schema.py. Adapt existing label.py transports without bypassing private-corpus rules. Accept a frozen meaning/expression, model configuration, Train or Test item batch and output schema. Return parsed task labels, diagnostics, timing, retries, invalid responses and per-attempt provenance.

Model context receives exactly its assigned item and allowed context, never reference answers. Distinguish invalid output, timeout, infrastructure failure and a legitimate abstention. Define batching, concurrency and retry limits. Do not log credentials, or raw Test or confirmation content, in refiner-visible errors.

Acceptance: deterministic fake transport covers malformed JSON, missing IDs, duplicate IDs, invalid labels, partial batches, timeouts, retries and cancellation. Account for all requested items. Pin settings by explicit config/version strings. No real executor campaign is started as an implementation test.

### T13. Score without leaking development examples

Owner C. Proposed E/evaluation_registry.py and E/scorecards.py. Bind predictions to reference, meaning, expression, corpus and split versions. Compute quality, coverage, invalidity, uncertainty routing and speed metrics by model and partition. Separate executor runs from scoring. The auditor receives Train and Test case-level results; the expression rewriting step receives only Train evidence and the allowed Test aggregates in aggregates.json.

Record every Test aggregate query, candidate family and feedback disclosure. Predetermine permitted strata and suppress small cells. The fresh independent confirmation set runs as a separate custodian service with its own frozen, authorized ticket. Confidence intervals must respect independent groups and paired comparisons. Denominators include failed and abstained cases according to the prespecified metric, with coverage always visible.

Acceptance: no per-item Test text, labels or errors in tool responses, logs or views available to the expression rewriting step; Test case-level records stay with the custodian and resolve only for the auditor, the Meaning Loop Agent and human review. J/staging, J/confirmation and J/gold expose only round reports with Test custody references, aggregates, safe Test and confirmation manifests and Train references; Test and confirmation predictions, attempts, diagnostics, logs and reference rows remain outside refiner-visible roots. Stale references fail rather than mixing versions. Missing classes, empty strata and insufficient groups produce explicit limitations. Repeated Test use is recorded as selection and development exposure, not proof for unseen data.

### T14. Generate expressions under a fixed meaning

Owner A. Proposed E/expression_candidates.py and E/meaning_fidelity.py. The expression rewriting step of the Execution & Audit Agent can reorganize, clarify terminology, make ordering explicit and choose approved Train examples. It cannot add a threshold, exception, label or default not present in approved meaning. Every clause maps back to rule IDs.

Check structural coverage, forbidden semantic changes and a regression set of approved Train cases. A model-based equivalence check can add evidence but is not proof by itself. Store the candidate's complete expression and change rationale. Distinguish expression changes from runtime/model settings so their effects can be evaluated separately.

Acceptance: omitted negation, broadened exception, changed label schema and unapproved priority are rejected, or reported in the round report as a rule question. Layout-only changes pass deterministic coverage tests. All examples are Train items; no Test or confirmation case appears in a candidate. Existing candidates retain original meaning bindings after a new semantic release.

### T15. Run the Step 5 staging loop and write round reports

Owner C. Proposed E/staging_loop.py, E/selection.py and E/round_report.py. Invoke candidate generation, fidelity checks, fixed executors on Train and Test, scoring by model and partition, error analysis, candidate selection and the round report within explicit budgets. Optimize the weakest model's quality subject to absolute quality/coverage floors and a limit on stronger-model regression. Gap reduction is secondary.

Train item errors can drive rewriting. Test supplies bounded aggregates for selection, and its case-level issues go to the Meaning Loop Agent in the round report. The confirmation set does not participate. Classify each error hypothesis as expression issue, rule gap or conflict, suspected reference-label error, executor limit or missing context; output formatting and infrastructure failures are operational. Only rule, preference, reference-label and diagnostic-policy questions reopen the Meaning Loop; expression-only issues continue in Step 5; a round that meets the declared criteria proceeds to Step 6. Every round writes its round report with its stop or continue reason.

Acceptance: no semantic change inside Step 5; a plateau can end as a stop with no qualifying candidate; a small gap with two bad models fails; a strong-model regression can reject a candidate; the latest candidate is not automatically the winner; no round reaches Step 6 without a round report whose criteria are met. Test issues reach the Meaning Loop Agent as custody references in the round report, and nothing from them enters the expression rewriting context, logs, memory or few-shot examples. A suspected reference-label error changes no label until the Meaning Loop decides.

### T16. Make both loops inspectable

Owner B. Extend new-mode views without changing engine authority. Show current approved meaning/reference/expression versions, pending human cards, submitted feedback, integration results, round reports and their routes, and release readiness status. Distinguish pending, blocked-by-dependency, running, failed, superseded and complete.

Provide links to the exact report/release/Run, concise diff explanations and permitted metric summaries. Explain what an action will approve. Show Train, Test and confirmation boundaries in the appropriate role-specific views, with performance for each partition shown separately. A shared participant sees only assigned reports, not staging results or administration.

Acceptance: no false green states from file existence; UI state survives reload; a Meaning update visibly invalidates affected Step 5 work; a pending report does not imply the whole system is stopped. Check actual browser transitions using synthetic records from T11/T15.

## 5. M4 and M5: release, scale and research

### T17. Freeze a version and check release readiness

Owner C. Proposed E/release_readiness.py and a handoff adapter. Start only from a round report routed to Step 6. Freeze meaning, expression, reference policy, executor configuration, routing rules, metric thresholds and evaluation protocol. Check version compatibility, reviewed issue dispositions, quality and coverage criteria, executor suitability, cost and audit policy. A failed gate returns to the responsible loop or holds release; it remains a failed result. A claim about unseen data needs the fresh independent confirmation set, run only when authorized and only after this freeze; revising after seeing its results starts a new development cycle and needs another fresh set for a new claim.

Create a handoff only from passing evidence and permitted human/policy approvals. Record known coverage limits, deployment scope, operational budgets and expiration/requalification triggers. Record whether Test findings guided approved revisions, since staging Test scores are then development exposure. No aggregate metric can substitute for an absent semantic approval.

Acceptance: mismatched versions, absent thresholds, a missing or unrouted round report, missing reference provenance and failed quality floors block release; a used or exposed confirmation set blocks any claim about unseen data. A complete handoff is immutable and readable by production without mutable development defaults.

### T18. Execute large-scale labeling with recovery

Owner C. Proposed E/production.py, E/reconciliation.py and E/risk_routes.py. Read the frozen handoff and new items, create batches and durable attempts, validate outputs and route uncertain/invalid cases. Use stable item/version identities, checkpoints and exact record comparison. Resume only missing or explicitly invalidated work.

Track requested, returned, parsed, routed, accepted and failed counts. A provider request may have completed before a local crash; record an uncertain attempt and reconcile it. Do not promise exactly-once remote calls. Budget limits stop cleanly. New meaning problems become issue records for the Meaning Loop Agent; production may continue only for unaffected scope allowed by policy.

Acceptance: restart mid-batch, partial provider response, duplicate return, budget stop and stale handoff are handled without silent item loss or double acceptance. Report real throughput including retries and review routing. A synthetic dry run demonstrates recovery; actual scale execution is a separately requested Run.

### T19. Audit and accept production results

Owner A with C reviewing sampling math. Proposed E/acceptance.py plus existing audit/final-label adapters. Combine probability-sampled audits across the population with targeted review of risky cases. Keep sample inclusion probabilities when estimating population error. Targeted disagreement cases alone cannot estimate overall quality.

Record who accepted which scope under which policy, individual overrides, unresolved cases and guideline version. Output a labeled corpus with transparent provenance categories: inferred, individually reviewed, accepted under batch policy, deferred or rejected. Human-approved reference data remains a separately identifiable subset.

Acceptance: low-risk strata remain eligible for random audit; independent sampled quality judgments are captured before revealing the executor label/model identity, with adjudication as a separate later step; assisted correction queues retain their distinct provenance. Failed audit triggers predefined containment/review; no unknown item disappears; reviewed contradictions route to the Meaning Loop Agent. A semantic revision invalidates affected production claims and identifies the necessary relabeling scope without destroying old results.

### T20. Update research tickets, skills and slides from evidence

Owner R. Prepare owner-native Run tickets for comparisons in EVALUATION.md. Build deterministic smoke/dry-run fixtures first. Do not launch the study without the user's instruction. Update applicable labeling skills only after behavior exists; follow the repository requirement for fresh-agent realistic skill validation.

Update the blueprint and slide sources to show forms, async integration, the two agents, Train and Test custody, the round report and its routes, diagnostics and large-scale output. Regenerate outputs through their existing generator. Preserve prior versions and label future capabilities as planned. No direct edits to generated HTML/PDF/PPTX.

Acceptance: documented links resolve, slide claims match implemented status, skill tests verify correct stopping/approval behavior, and study tickets state data/model/runtime budgets. Whole-Meaning comparisons specify a common independent outcome standard rather than scoring each method against its own generated labels; expression-only comparisons hold meaning/references fixed. Report engineering validation separately from evidence that the proposed method improves quality or cost.

## 6. Completion report template

Each agent returns a short report containing: package ID and status; files changed; exact checks executed and outcomes; behavior demonstrated; unresolved risks; dependent packages unblocked; and any deviation needing coordinator resolution. A package can be complete, partial, blocked or superseded. Planned tests must never be listed as passed tests.
