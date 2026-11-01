# Meaning Loop implementation memo

Status: planning proposal based on read-only source inspection, 2026-10-27. No product code, skills, live jobs, model calls, corpus files or servers were changed. This memo is for the root reviewer to integrate into the implementation plan.

## 1. Decision to implement

Use two top-level agents with explicit tool permissions. The Meaning Loop Agent owns exploration, human communication, semantic decisions, rule integration and issue reopening. The Expression Loop Agent owns wording candidates and executor experiments under an approved meaning version. The agents exchange typed packets; neither requires a separate autonomous agent for every internal capability.

Keep the current step numbering:

- Step 0: transform a corpus into stable items and reserve disjoint data groups before development exposure.
- Step 1: frame the task, scope, context policy, label schema and human authority.
- Steps 2–4: collect human sources and learning evidence; publish a decision report; collect asynchronous responses; reconcile and apply approved meaning; recheck affected items.
- Step 5: improve expression using learning diagnostics and aggregate validation results.
- Step 6: freeze and qualify.
- Step 7: scale and audit; semantic issues return to Meaning.

The default human interface is a structured decision report rendered inside Workbench. Chat is supplemental context and can produce a proposed decision, not a silent override of an approved rule. A decision card is about a consequential rule, contrast, exception, conflict or acceptance policy. It is not necessarily a request to label one item.

## 2. Verified current capabilities and constraints

Paths below are relative to <Tools>.

| Inspected source | Verified current behavior | Reuse or migration implication |
| --- | --- | --- |
| plugins/haipipe-toolkit/skills/2_theme/labeling/engine/calibration.py: release_round | Only round_01 random development draw is supported. A later round explicitly refuses. | Do not promise that a new report renderer makes multi-round learning work. Introduce a versioned interaction mode and a real episode coordinator. |
| Same: open_item, record_first, record_final, verify_events | Implements show → first → lock → reveal → final item events; configured authority ID is checked but not authenticated. | Preserve these events as the legacy blinded item-review mode. Use it where an independently judged reference item is actually needed, not for all high-level form decisions. Bind real identity at the Workbench boundary. |
| Same: _eligible_ids, _item | Restricts item access to population_status=eligible. | A useful fail-closed precedent, but eligible currently means development; new learning/validation roles need a stricter split adapter. |
| engine/corpus_tools.py: stats, sample, search, find_neighbours, get | Eligible-only counts, seeded sample, keyword search, nearest-neighbor retrieval, exposure logging and reading budgets exist. Non-nearest ranking modes refuse; get refuses items currently waiting for legacy item judgment. | Reuse data-access concepts and exposure logging. Add a mode-aware learning scope; do not bypass waiting/blind guards globally. New ranks need implementation evidence. |
| engine/definition_discussion.py: start, say, decide, close | Label-level discussion before any released round or judged item; later decisions replace a label's projected decision; changed meaning retires prior G0 confirmation. | Not an asynchronous rule-patch engine. Retain it for legacy initial definition; do not stretch decide into an unrestricted semantic writer. |
| engine/job.py: write_once, runs_dir, results_dir, mint_labeling_run, matching_runs | Existing stable artifact and Run-address helpers; write_once compares existing bytes and refuses different content. | Reuse reviewed helpers that do not introduce forbidden digest dependencies. Avoid copying private helper chains blindly. |
| haipipe-labeling-rounds/SKILL.md | Explicitly marks weak-prelabel, guideline-learn, round-measure, round-close and round 2+ unbuilt. | Plan these as work, not configuration changes or already working features. |
| haipipe-labeling-guideline/SKILL.md and ref/guideline-format.md | Specifies conditions, actions, precedence, evidence, history; guideline.md and cheatsheet.md are rendered. rules.yaml is described but not yet an engine POLICY_COMPONENT. | Add source schema and keeper coverage before treating rules.yaml as authoritative. Separate immutable meaning from expression candidates. |
| s03-agent-role/decision-report | Local six-card synthetic prototype: choices, none, defer, comments, draft restore, review and JSON export. | UI behavior and sample data are examples, not authenticated Workbench storage, backend integration or automatic guideline learning. |
| s41-task-items-procedure | Older design acknowledges that future sealed items might already have been displayed. | Reserve groups before any development exposure; retain the old disclosure rather than rewriting historical evidence as clean. |
| s42-task-building-procedure | Item-by-item JUDGE, fixed H/L/N pools, hypothetical counts, broader future LEARN/CLOSE algorithms. | Treat as legacy design, not current implementation or a universal schema. New explicit user decisions supersede its interaction defaults. |

The existing preparation code has digest-bound legacy receipts. The new protocol must use explicit version IDs, monotonic event sequences, exact expected-value comparisons and server-side locks. Do not add digest fields or repurpose existing digest helpers. Any compatibility adapter must preserve old records without claiming a no-digest new path can validate every old receipt unmodified.

## 3. Architecture and file ownership proposal

Use a versioned mode, for example config.interaction.meaning_mode = decision_reports_v1. This name is proposed, not an existing field. Default existing jobs to legacy behavior until explicitly migrated. A read-only adapter may expose old events inside new history, but must preserve their original event kinds and authority scope.

Proposed source modules under plugins/haipipe-toolkit/skills/2_theme/labeling/engine/:

- meaning_contracts.py: schemas, enums, pure validators and compatibility conversions.
- meaning_store.py: locks, append-only events, immutable report publication, drafts, idempotent submission and atomic promotion journal.
- meaning_reports.py: source ledger, report validation, learning-only evidence assembly, selection coverage and card validation.
- meaning_integrate.py: decision normalization, conflict objects, patch plans, impact analysis, approved-version commit and dependency invalidation.
- meaning_harness.py: bounded operation state machine, tool permissions, async human queue, retry/resume and handoff to Expression.

Each module has a same-directory test_meaning_*.py owner. Existing shared files job.py, calibration.py, run_catalog.py, gates.py and page_plugin.py have one designated integration owner, not simultaneous edits by multiple agents. Workbench adapter and API files belong to the UI/backend owner, consuming the public contracts above.

Proposed authority locations inside a labeling Task's existing labeling/ domain:

    meaning/
      sources/source_NNN.json
      events/events.jsonl
      drafts/<report-id>/<authority-id>.json
      pending/issues.jsonl
      commits/commit_NNN.json
      state.json                         derived projection only
    rounds/round_NN/
      decision_reports/report_NNN/
        report.json                      immutable after publication
        submissions/submission_NNN.json  immutable human receipts
        integration/plan_NNN.json         proposed patch + impact
    policy/versions/G_NNN/
      manifest.yaml
      rules.yaml                         authoritative approved meaning
      procedure.yaml
      uncertainty.yaml
      casebook.jsonl
      guideline.md                       rendered, not edited directly
      cheatsheet.md                      initial rendering, not an expression authority
    policy/current                       current approved version pointer

This is a proposed address amendment to the existing domain contract. Keep one canonical source per record; Results reference these artifacts instead of maintaining independent editable copies. Run Tickets and runtime Results continue using job.runs_dir/job.results_dir and the owner-native operation dialect. Do not allocate future Runs prematurely or fabricate completed receipts.

## 4. Human-source provenance

A HumanSource is evidence about intent, not automatically semantic authority:

- source_id, source_version, job_id, created_at.
- kind: initial_brief, source_note, chat_turn, prior_decision, external_guideline, legacy_annotation.
- actor_id and actor_role: authenticated authority, collaborator, agent, external/unknown.
- origin reference: Workbench entry ID, chat message ID, document path plus locator, or imported record address.
- original_text preserved exactly; separate agent_summary and summary_status.
- purpose: task_context, candidate_preference, approved_decision, background_evidence.
- linked_decision_ids, supersedes_source_id where the human corrected a source.
- visibility/sensitivity and allowed_consumers; do not copy private study text into the public Tools repository.

An agent may summarize, cluster and cite sources. It cannot relabel an agent summary as the person's original words. Collaborator opinions may be evidence, but the configured authority determines meaning. An external guideline does not outrank an explicit human rule unless the task contract says so.

Both entry cases use this ledger:

1. Rough idea: an initial brief is provisional context; contrastive learning cases elicit operational rules.
2. Existing labels: import labels as legacy observations with source/annotator/version if known. Agent infers candidate patterns and inconsistency groups; it does not assign error status until a standard and approval basis exist. Internal consistency and fitness for the current human's intended use are separate questions.

## 5. Learning-only development boundary

The partition contract names learning, validation and final_test by role, not by a fixed numerical split.

- Meaning writer/retrieval/report tools may receive learning item contents and learning reference labels only.
- Independent executors may label either learning or evaluation items in fresh contexts.
- Evaluation scorer may see protected reference labels; label executors must not see answers.
- The coordinator may receive approved aggregate validation results, but the next guideline-writing call must not inherit evaluation texts, reference labels, error rationales or item-level diagnostic tags.
- Repeated candidate selection against aggregate scores makes that partition validation. Final test is a separate qualification operation under its own release policy.
- A source group, conversation and declared near-duplicate group stay within one partition. Do not make a “learning source note” by copying an evaluation example into it.
- Report publication resolves all cited item IDs against the partition manifest server-side. A client-supplied split string is not enough.
- Retrieval uses a learning-only index or a verified learning allowlist at query and materialization time. Corpus-wide embedding access is not an exemption.
- Every developer-context build records the source IDs and item IDs it included. Validation exports record only approved aggregates and their provenance.

Do not use the legacy “no prelabel at all before freeze” rule for ordinary validation. Preserve final-test custody while enabling evaluation executors as the user requested. Runtime context isolation is required; merely hiding a panel in the UI does not isolate an agent prompt.

## 6. DecisionReport contract

Report header:

- schema_version, report_id, report_revision, job_id, episode_id.
- base_meaning_version, base_expression_version if applicable, itemset_version, partition_version.
- human_authority_id, generated_by, created_at, published_at.
- objective, source_ids, decision_ids, status, predecessor_report_id.
- selection_plan: random/coverage/challenge strata and reasons, budgets and omitted/open regions.
- No arbitrary executable HTML from the agent. The agent supplies structured content; Workbench owns rendering.

DecisionCard:

- decision_id, revision, title, question, kind.
- kind values: define_label, rule_boundary, exception, precedence, conflict, context_policy, diagnostic_definition, reference_item_review, audit_policy, stopping.
- current_rule_refs, human_source_refs.
- evidence[]: item_id, item_version, split_role=learning, context policy, excerpt locator, evidence_role=support/contrast/counterexample/missing_context, provenance.
- candidate_options[]: option_id, label, rationale, exact proposed patch or proposal reference, expected_effect, affected_scope.
- selection_mode single by default; explicit multiple-choice only where combinations have defined meanings.
- requiredness, decision_dependencies, allowed_responses=[choose, custom, defer], optional comments.
- approval_scope: preference_only or exact_rule_patch or item_review or acceptance_policy. UI must display the distinction.
- expected_base_rule_versions and impact_summary; if an exact impact count has not been computed, use “scope” rather than inventing a count.

Quality constraints:

- No preselected answer; no hidden “recommended” default used to bias preference collection.
- Provide materially different alternatives, including a custom proposal and defer.
- Keep ordinary negative task labels distinct from “none of these options.”
- At least one meaningful contrast or explicit reason that evidence is absent; do not manufacture cases and imply they were retrieved.
- Synthetic illustrations, if used, are explicitly marked; they cannot become observed error statistics or reference gold.
- Prompt questions neutrally; present an apparent contradiction as an issue to explain, not an accusation.
- Limit the batch by decision complexity and human effort, not an invariant ten-card quota.

## 7. Human response and approval semantics

DraftResponse is mutable and private to its owner until submitted:

- report_id/revision, authority_id, draft_revision, updated_at.
- answers keyed by decision ID: selected option or response_kind=custom/defer, comments, optional reason for defer.
- new_source_notes.

Submission is immutable:

- submission_id, idempotency_key, actor derived from authenticated session, submitted_at.
- report_id/revision and base versions.
- submitted answers, explicit pending/unanswered IDs, prior_submission_id if amended.
- scope acknowledged by the human.

A partial submission is legal. Unanswered, deferred, custom-proposal, approved, rejected and superseded are different states. “None” requires a written alternative or is changed to defer by the user. A custom response is not assigned an executable meaning until the agent presents the interpretation and receives confirmation.

Avoid an unnecessary second click for an exact choice already approved:

- If the published card binds the exact rule patch, scope, base version and stated effects, the human's selection is approval of that exact payload. Deterministic integration need not ask again.
- If only a broad preference was collected, the agent drafts the operational rule and presents it for confirmation.
- If comments qualify or contradict the selected option, preserve both and open clarification; do not discard the comment.
- The existing prototype's rule_preference_only exports remain preference-only. Never silently import them as exact-rule-patch approval.

Rule approval is not approval of every inferred item label. A request to accept labels requires its own displayed item-review or explicit batch-audit scope and evidence.

## 8. State machines and events

Report state:

    draft → validated → published → awaiting_response
      → partly_answered → response_complete
      → integrated | superseded

Published content is immutable. A change creates a report revision and preserves original drafts/receipts; the UI flags the new revision before old answers can be interpreted under it.

Decision state:

    proposed → awaiting_human
      → selected → approved_exact_patch → integrated
      → preference_received → clarification_pending → approved_exact_patch
      → custom_proposal → clarification_pending
      → deferred → carried_forward
      → rejected
      → stale_needs_rebase

An episode can be parked awaiting selected human decisions while the scheduler runs independent exploration. “Episode complete” is not global semantic closure. Publish an approved checkpoint only for resolved scope, carrying unresolved scope explicitly; do not call unresolved coverage accepted.

Append-only event envelope:

- event_id, sequence, occurred_at, job_id, episode_id.
- event_type: source_added, report_published, draft_saved, response_submitted, decision_normalized, conflict_opened, patch_approved, patch_committed, reference_approved, issue_deferred, report_superseded, expression_issue_received, dependent_artifact_invalidated.
- actor_id/role, channel, correlation_id, causation_event_id.
- object ID and revision, expected prior revision, payload.

Sequence is allocated under the job's writer lock. Idempotency uses caller action IDs, report/version binding and exact payload comparison, not content fingerprints. Same action ID and identical content returns the existing receipt. Same action ID and different content is a conflict. Do not append a second semantic decision after a network retry.

## 9. Integration transaction and failure recovery

For each submitted response:

1. Verify actor authority, report identity, immutable revision and base versions.
2. Classify selections and comments without changing meaning.
3. Resolve cited sources and learning-only item references.
4. Produce a proposed patch with conditions, action, exceptions, precedence and acceptance scope.
5. Check old decisions, rule dependencies and concrete counterexamples. Distinguish missing context, changed preference, recording error, multiple dimensions and unresolved disagreement.
6. Compute an impact plan: potentially affected items, prior approved references, expression candidates, scorecards and production batches. Report uncertainty in the impact search.
7. If exact semantic approval already exists and no unresolved qualification changes the payload, commit it. Otherwise publish a clarification card.
8. Re-label impacted learning items as candidate predictions. Keep reference changes pending until their appropriate approval scope is satisfied.
9. Write new immutable policy version, versioned reference membership and an explicit unresolved-scope record.
10. Commit the authority event, then advance the current pointer; regenerate views.

Use a transaction journal with prepared/committed state and exact expected prior pointer. Recovery either finishes the same approved transaction or leaves the prior approved version active. A crash between an event and a view refresh must not duplicate a human decision or overwrite a later version. Store authoritative writes in one process-safe writer path, then expose read projections.

Failure cases:

- Two browser tabs submit conflicting choices: accept first under revision check; show second as stale conflict, preserving its human text.
- New meaning arrives while expression is running: do not splice it into the live run. Mark results with old version, invalidate affected eligibility and schedule a separate run under the new version.
- Report is partially answered while sources change: retain answered receipt; publish a new version only for changed decisions, with explicit dependency effects.
- A tool times out after successful submission: retry same action ID and return original receipt.
- Unknown schema or unreadable event sequence: hold the affected writer, preserve last approved version and expose repair details.
- No authority is available: produce provisional audit findings only; no approved standard is claimed.

## 10. Rules, labels and diagnostic annotations

ApprovedRule:

- rule_id, revision, semantic_version, status active/narrowed/retired.
- condition, task_label_action, context_requirements, exceptions, precedence.
- human_decision_refs, supporting_learning_evidence, counterexamples, rationale.
- approved_by, approved_at, supersedes, approval_scope.
- Known applicability limits and unresolved issue references.

Allow a clearly approved human principle before a concrete reference example exists. Mark evidence_status=human_principle_unvalidated and request examples; do not invent a reference item to satisfy the old “no rule without gold” rule. Evidence coverage limits qualification rather than silently nullifying the person's explicit rule.

LabelRecord:

- item_id/version, meaning_version, expression_version, executor_id/config version.
- task_label (nullable), disposition labeled/abstain/needs_context/deferred/out_of_scope.
- provenance model_prediction, legacy_observation, human_item_review, human_group_review, audit_accepted.
- approval scope and decision IDs where appropriate.
- diagnostics with assessor and criteria version.

Suggested diagnostics are extensible, task-specific schemas:

- difficulty.value: easy/hard/unknown, with basis and assessor. Do not equate length with difficulty.
- uncertainty.status: resolved/ambiguous/insufficient_evidence/unknown.
- uncertainty.reasons: missing_context, rule_overlap, unclear_boundary, conflicting_evidence, unfamiliar_content, other.
- plausible_labels: optional allowed task labels; no fabricated calibrated probability.
- review_action: none/review/request_context/defer.
- model self-assessment, human judgment and measured model disagreement stored in separate fields.

The guideline defines these fields, their criteria, examples, precedence and required action. Easy is not proof of correctness, hard is not an automatic abstention, and task NONE is not a synonym for uncertainty. Avoid evaluating a model's uncertainty against its own correctness claim. An independently defined diagnostic quality study is separate work.

## 11. Agent tool contracts

| Tool | Permitted input/output | Authority and failure behavior |
| --- | --- | --- |
| collect_human_source | Human text/reference → source record | Preserves original words; agent summaries separately typed; cannot create approval. |
| search_learning / sample_learning / get_learning | Query/group/IDs → allowed learning evidence | Enforces partition and context scope at backend; logs exposure; refuses evaluation IDs. |
| label_learning_items | Current approved or clearly provisional guideline + learning item batch → predictions/diagnostics | Calls fixed-weight executors; no gold promotion; version every output. |
| propose_decision_report | Approved sources + learning evidence → draft structured report | Agent writes candidate content only. |
| validate_report | Draft → errors/warnings or publication-ready snapshot | Checks sources, options, scope, dependencies, leakage and synthetic labels. |
| publish_report | Validated immutable revision → Workbench report | No invented human response or automatic selected options. |
| read_submitted_feedback | Published report → authenticated immutable response records | Read drafts only under explicit draft access policy; drafts never approval. |
| detect_conflicts | Responses + rules + decision history → issue packets | “Possible conflict” is not a user error verdict. |
| preview_semantic_patch | Approved response + proposed interpretation → exact patch + impact | Read-only preview; exposes reference flips. |
| commit_approved_patch | Exact approved patch + expected version → new approved meaning version | Deterministic keeper, not a model discretion tool. |
| approve_reference | Explicit scoped human item/group event → reference version | Does not infer approval from rule selection or model consensus. |
| export_expression_handoff | Compatible meaning + references + limits → immutable bundle | Refuses stale or unresolved required scope; includes no evaluation examples. |
| receive_expression_issue | Concrete learning cases, rule refs, attempted rewrites, errors → pending meaning issue | Does not automatically reopen every error as semantic; deduplicates known issues. |

## 12. Dependency-ordered implementation work packages

M1: contracts and mode adapter
- Owner: domain-contract agent.
- Files: meaning_contracts.py, test_meaning_contracts.py; integration owner changes config validation and operation catalog.
- Deliver: typed schemas above, rejected unknown/extra authority values, versioned serialization, read-only import of existing prototype feedback, explicit legacy mapping.
- Acceptance: fixtures for rough idea and existing labels; arbitrary label values work; H/L/N not required; malformed and incompatible schemas fail without writes.

M2: record store and publication
- Depends M1.
- Owner: domain-store agent.
- Files: meaning_store.py, test_meaning_store.py.
- Deliver: immutable report revisions, draft ownership, action-ID idempotency, revision-aware submissions, append-only events, journal recovery.
- Acceptance: concurrent/stale writes, interrupted commit and retry matrix; no duplicate approvals; source and submitted text survive restart.

M3: sources and evidence-bound reports
- Depends M1; storage hooks from M2.
- Owner: Meaning report agent.
- Files: meaning_reports.py, test_meaning_reports.py; corpus_tools.py changes through integration owner.
- Deliver: source ledger, learning-only evidence assembly, neutral candidate options, coverage/random/challenge annotations and budget records.
- Acceptance: both entry cases; no implicit gold from legacy labels; a validation item hidden in a source note or report payload is rejected when reference-resolvable; no arbitrary agent HTML executed.

M4: integration and scoped promotion
- Depends M1–M3.
- Owner: Meaning integration agent.
- Files: meaning_integrate.py, test_meaning_integrate.py; policy component changes through integration owner.
- Deliver: exact-option approval path, custom/qualified-comment clarification, conflicts, rule patch/impact plan, version commit, label provenance and reference promotion.
- Acceptance: exact selected patch does not demand redundant approval; imported preference-only payload cannot bypass approval; changed meaning invalidates only declared dependency scope and retains history.

M5: asynchronous Meaning harness
- Depends M2–M4 and Workbench API.
- Owner: orchestration agent.
- Files: meaning_harness.py, test_meaning_harness.py.
- Deliver: bounded cycles, pending human queue, independent work scheduling, durable resume, typed issue exchange with Expression.
- Acceptance: stop/restart mid-question without losing state; no busy-loop when waiting for humans; unrelated approved-version work continues; no direct Expression-to-human message.

M6: contract and skill migration
- Depends working M1–M5 evidence.
- Owner: root integrator with domain agent suggestions.
- Files: relevant building/rounds/guideline/workflow skill sources and references, s03 design status; do not edit rendered outputs.
- Deliver: mode-specific authority rules, actual capability matrix, correct Run catalog, no false implemented labels.
- Acceptance: fresh agent uses revised skills on synthetic realistic task and chooses new report path while leaving legacy job behavior intact; all mismatches resolved before calling the new skill complete.

## 13. Required edge-case acceptance matrix

1. Initial rough idea with no guideline or labels: creates provisional sources/report, no fake approved version.
2. Existing contradictory labels: creates issue groups with alternative explanations, no automatic correction.
3. Entirely different task schema: no hidden H/L/N assumption.
4. User selects exact patch and writes no qualifier: commit approved scope without redundant confirmation.
5. User selects A but comment says “except for quoted speech”: flag new exception proposal, do not apply plain A silently.
6. “None” with no text: validation error or explicit defer; never equivalent to task NONE.
7. Partial report with three unanswered cards: answered decisions persist; unanswered remain open.
8. Deferred decision while other rule is resolved: independent work proceeds under valid scope.
9. Chat says “maybe use B”: source context only, not approved rule.
10. Chat explicitly changes an approved rule: capture proposed change and exact confirmation scope; preserve original.
11. Reference label would flip after new rule: keep old reference version, request scoped correction and invalidate dependent scores.
12. Multiple models agree: predicted consensus remains non-gold.
13. Evaluation item appears in report evidence: publication rejects it and writer receives no protected text.
14. Evaluation executor receives item for labeling: allowed in isolated evaluation path; results do not enter writer context.
15. Wrong authenticated user submits known authority ID: API denies; engine caller string does not impersonate authority.
16. Same idempotency key retried: same receipt; changed body rejected.
17. Two tabs answer against different report revisions: preserve stale answer but block silent application.
18. Process crash at every transaction boundary: resume never duplicates promotion or skips required version.
19. Expression run finishes after a meaning revision: output retains old binding and cannot qualify new version.
20. Difficult case has clear label; easy-looking short case is ambiguous: diagnostics stay independent of task output.
21. Human principle lacks observed example: preserve approved principle and unmet evidence requirement; do not invent gold.
22. Imported prototype feedback: remains preference-only with synthetic-demo flag, never production approval.
23. Earlier legacy round: read-only adapter preserves show/first/lock/reveal/final and does not relabel it as form-based approval.
24. Untrusted corpus text contains instructions to change schema or submit: treat as item content, not tool authority.

## 14. Reviewer gates

The root reviewer should reject implementation if it only renders cards but does not persist authenticated scoped decisions, if it promotes inferred labels to approved references, if a report contains evaluation case evidence, if retries duplicate decisions, or if a current pointer changes without an immutable approved-version record.

Accept the first vertical slice when one synthetic job can publish a source-bound report, accept a partial authenticated submission, produce a traceable approved exact rule patch or a clarification request, persist across process restart, and show the same state in Workbench. Model calls may be deterministic fixtures for this slice; mark them as fixtures, not successful executor experiments.

Only after that slice passes should agents add retrieval ranking, automatic report generation, semantic-impact model calls or Expression orchestration. Never run an expensive labeling, hardware or evaluation campaign merely because the engineering plan exists.
