# Workbench integration implementation memo

Status: read-only design audit, 2026-10-27. No production file was changed, server started, model called, or new Run executed for this audit.

Repository root: <Tools>

This memo translates the user's latest design into implementation tasks: the Meaning Agent generates a structured decision report each round; Workbench renders and stores it; the human answers asynchronously, normally through forms and optionally through chat; the agent integrates confirmed preferences while keeping unresolved choices explicit. Rule-level approval is distinct from item-level reference-label approval.

## 1. Verified implementation truth

The following paths are relative to the repository root.

| Capability | Verified implementation | Gap for the proposed system |
| --- | --- | --- |
| Existing browser surface | plugins/haipipe-toolkit/servers/workbench-labeling/workbench-task-labeling/labeling.py, render(), _labeling_space(), _rounds_view() | The Rounds view displays legacy item batches and copy-to-chat guidance, not generated rule-level decision forms. |
| Existing frame integration | servers/workbench-labeling/workbench-task-labeling/task_labeling.py, _build_spaces(), _build_cards(), _build_input(), _task_spaces(), spaces() | Frame cards and progress still describe item-level rounds, fixed pools and sequential sign gates. They need capability-aware reporting of the new form workflow. |
| Existing single write door | labeling.py, LabelingMixin.labeling_act(); routed by servers/_host/serve.py do_POST() at /_board/labeling/act | Supported actions include confirm_meaning, release_round, open_item, first, final, embedding and corpus reads. There is no decision-report draft, submit, or import action. Preserve this one write endpoint. |
| Existing writer placement | skills/2_theme/labeling/engine/; server imports its functions through cached module adapters | Add an engine-owned report/feedback writer, not a second writer in browser code or server templates. |
| Canonical storage root | labeling.py, _labeling_lane() and _job_root() | Resolve to the existing Page-local labeling/ lane. Legacy nested field-test roots remain read-only compatibility projections. Do not create a second canonical data tree in the blueprint. |
| Existing human decisions | engine/calibration.py record_first(), record_final(), add_feedback(); engine/definition_discussion.py start(), say(), decide(), close() | These encode blind first-item judgment and initial label-definition discussion. They are not a generic rule-decision report engine. |
| Item confidentiality | calibration._eligible_ids() accepts only eligible development items; calibration._item() rejects other population statuses; host rejects direct private static files | Report references must be resolved through a learning-only reader. Browser-provided split flags cannot prove eligibility. Validation and final-test detail must remain inaccessible to this development surface. |
| Existing persistence primitives | calibration._locked() uses fcntl; job.write_once(); job._atomic_write() near job.py line 1009; calibration._append_event() called inside a round lock | Reuse the patterns, but add compare-and-swap revisions, complete transaction semantics, idempotency, and recovery for report feedback. Do not assume current item-event locking already solves report concurrency. |
| Current source prototype | blueprints/Project-Ladder/work/b15_theme_labeling/s03-agent-role/decision-report/ | Working local six-card form: no selected defaults, alternatives, none/defer, comments, browser drafts, review, JSON download. It is synthetic and not integrated with the live server, storage, identity or agent ingestion. |
| Host authentication | servers/_host/live/auth.py AuthMixin.require_request_auth(), require_auth(); share.py ShareMixin.share_gate() | A logged-in server session exists in some deployments, but labeling_act explicitly treats human_id and attest as caller assertions, not authenticated semantic identity. |
| Shared participant access | share.py share_gate() derives share_user from signed cookie; owners may write; all other POST requests are rejected | External respondents cannot submit today. A narrow assigned-job response permission is a separate rollout gate. Never make a participant a SPACE owner to enable form submission. |

Production code had unrelated dirty files before this audit. Each implementation task must re-read git status, preserve them and claim exclusive ownership of the files it edits.

## 2. Main integration decision

Use the existing Labeling Workbench and its existing Labeling / Rounds view. Add decision reports inside that view, with a truthful empty state. Keep the existing workbench picker entry, four-space shell, Runs panel and source-path routing. Do not add another application shell, arbitrary standalone service, top-level workbench or generic HTML execution mechanism.

The agent authors structured data, not executable HTML. A stable renderer turns that data into questions, sources, alternatives, comments, progress and submission controls. This allows a report to be validated before showing it and avoids HTML/script generation becoming an implicit execution channel.

Preserve legacy item-calibration rounds as a separate mode, selected by an explicit workflow/schema capability. Do not silently reinterpret old first/final item events as rule decisions. A new job can adopt decision reports; an old job needs an explicit migration decision if it changes protocol.

## 3. Proposed source ownership

One implementation agent owns each row. File names below that do not exist are proposals, not verified capabilities.

| Owner | Source files | Responsibility |
| --- | --- | --- |
| Contract/storage agent | skills/2_theme/labeling/engine/decision_reports.py; test_decision_reports.py | Schema, read/write invariants, revisions, immutable published reports, draft and submission persistence, replay, domain errors. |
| Learning evidence agent | engine/meaning_evidence.py; test_meaning_evidence.py | Resolve allowed item/source references, enforce learning-only access, provide minimum display evidence and exposure recording. |
| UI agent | servers/workbench-labeling/workbench-task-labeling/decision_report_view.py; assets/js/decision-reports.js; assets/css/decision-reports.css | Static renderer and client form controller. No policy or ledger writes outside engine APIs. |
| Single integration owner | existing labeling.py and task_labeling.py; servers/workbench-labeling/tests/test_decision_reports.py | Cached engine adapter, narrow action dispatch, Rounds view insertion, frame progress and route compatibility. Other agents must not concurrently edit these files. |
| Principal/access owner | servers/_host/live/auth.py, share.py and associated tests, only if multi-user rollout is commissioned | Server-derived actor mapping and narrow respondent permission. Isolate from form rendering; preserve all existing share read restrictions. |
| Reviewer/integrator | cross-package integration tests, migration notes and acceptance report | Audit code, run focused tests, inspect real UI and verify the negative cases. The maker's own pass claim is insufficient. |

Keep the blueprint prototype as design evidence. Do not promote its localStorage into canonical production storage, and do not copy its whole document shell into Workbench.

## 4. Proposed artifact grammar

Confirm this grammar jointly with the overall contract owner before coding it. It intentionally avoids using legacy calibration sessions/events.jsonl for rule judgments.

    <Page>/labeling/
      config.yaml
      meaning/
        sources/
          source_0001.json
        reports/
          report_0001/
            v01/
              report.json
            drafts/
              <authority-key>.json
            submissions/
              submission_0001.json
              submission_0002.json
            operations.jsonl
        integrations/
          integration_0001.json
      policy/
        versions/<existing-version-grammar>/
      rounds/
        <legacy item-calibration artifacts unchanged>

This is domain storage inside the existing lane, not an additional top-level Workbench. A report's generation operation still has the existing Run ticket and Result receipt at the locations returned by job.runs_dir() and job.results_dir(); those point to the report artifact instead of duplicating its contents. Follow the final parent plan's Run/Result grammar if it selects a different canonical address.

Published report v01 is immutable. A changed question, choice, evidence example or expected rule effect requires v02. Draft answers are mutable per semantic authority and report revision. Submitted answers are immutable. Chat sources are immutable records retaining author kind and provenance. Integration is another explicit operation, never a side effect of the submission endpoint.

The browser receives logical IDs, not arbitrary filesystem paths to write. The writer resolves all IDs under the canonical lane and rejects absolute paths, traversal, malformed IDs and symlinks escaping the lane. No report file or feedback is directly exposed by the static file server.

## 5. Required contracts

### Report

Required fields:

- schema_version, report_id, report_version, generation_run_id, created_at.
- job_id, corpus_version, split_version, base_meaning_version, base_expression_version when applicable.
- semantic_authority_id and identity_policy.
- status: draft_generation, published, superseded, withdrawn.
- source_refs with source_id, author_kind, provenance_kind, exact excerpt or safe summary, original location identifier and display authorization.
- decisions: stable decision_id, question, decision_kind, current_rule_refs, evidence_refs, options, expected_scope, unresolved_dependencies.

Each option has option_id, short label, exact proposed semantic effect, scope and optional prerequisites. Do not store only A/B/C: text and semantic effect must survive option reordering. No default selected option. None/custom and defer are explicit dispositions, not substantive target labels.

Each evidence item is resolved server-side against the frozen learning membership and source versions. A report may include human source notes or synthetic illustrative cases with their provenance, but never describe a synthetic case as retrieved corpus evidence. Difficulty and uncertainty are separate fields.

### Draft

Required fields: report_id, report_version, authority_id, draft_revision, updated_at, answers, additional_context and client_request_id. Each answer contains decision_id, selected_option_id or null, response_disposition, comment and optional requested_evidence. Pending cards may remain unanswered.

Saving a draft never changes a policy, approved labels, a human-confirmation gate, or an executor qualification.

### Submission

Required fields: submission_id, report_id, report_version, base_meaning_version, authority_id, actor_evidence, draft_revision, submitted_at, request_id and complete submitted answer snapshot.

Actor evidence explicitly records one of trusted_local_attestation or authenticated_principal plus its provider and server-resolved subject. A value typed into human_id is not authenticated_principal.

Per decision, preserve selected option text and proposed effect from the server's published report, not from the client request. Dispositions are confirmed_preference, custom_proposal, deferred or unanswered. approval_scope is rule_preference_only unless a separate explicitly scoped item-review action is used. item_labels_approved is false.

### Integration receipt

Required fields: submission_refs, prior_meaning_version, accepted_decision_ids, pending_decision_ids, conflict_refs, affected_rule_ids, affected_item_query or item IDs, resulting_meaning_version if any, resulting_reference_version if any, actor/procedure, and downstream invalidation scope.

Do not allow a report writer or UI submitter to mint approved labels by filling these fields. A meaning-integration operation validates them and retains the person's original answers.

## 6. API shape under the one write door

All mutations remain POST /_board/labeling/act. Reuse current page-target resolution, mode, path/file/page identity and domain errors, while extending authority checks.

Proposed actions:

| Action | Inputs | Output and rule |
| --- | --- | --- |
| decision_report_state | report_id/version or current | Checked report view plus the caller's draft and submission state. Read only; no mutation on rendering. |
| save_decision_draft | report_id, report_version, expected_draft_revision, request_id, answers, additional_context | New draft_revision and saved_at, or 409 with current revision. Never overwrites an unseen edit. |
| submit_decision_feedback | report_id, report_version, expected_draft_revision, request_id, attest | Immutable submission receipt assembled from server state; empty/invalid custom answers rejected. Partial/deferred allowed. |
| decision_feedback_status | submission_id | submitted, awaiting_integration, needs_clarification, integrated, stale or superseded with evidence. |

The current endpoint already mixes narrow reads with mutations. Keeping checked reads under it minimizes routes, but read actions must not falsely require a human decision attestation. If the integrator elects a dedicated GET reader, route registration must update both GET and HEAD, host allowlists, short routes and tests; no second write door.

Agent-only report publish and feedback integration are engine functions or CLI operations initially, not browser actions. The browser must not impersonate the report author or semantic integrator.

Errors: 400 malformed payload or unknown option; 401 unauthenticated where identity is required; 403 unauthorized actor/cross-origin; 404 inaccessible target; 409 stale revision/base or incompatible state; 413 payload size limit. Return actionable structured codes without echoing private item contents into logs.

## 7. Concurrency, retries and crash recovery

1. Publish the report under a job/report lock. Allocate monotonic report/version IDs under the same lock. Use a temporary file plus atomic rename for the complete artifact. A reader sees the previous complete version or the new complete version.
2. Draft save is compare-and-swap: read expected revision, validate current report and actor, validate answers, increment revision, atomically persist. Two tabs editing revision 3 cannot both succeed. Do not auto-merge semantic answers.
3. Submission uses a client-generated request_id that survives retries. Under a report lock, first check whether that request_id already produced a submission. Identical semantic request returns the same receipt. Reuse with different answers or version is a 409. Compare normalized fields directly; no hashes.
4. Submission snapshot is the source of truth. The event ledger must refer to a real immutable snapshot. If a crash occurs between artifact write and event append, recovery discovers the committed snapshot and completes the missing event without duplicating the decision. Do not infer human consent from an incomplete draft.
5. Stale meaning version: accept neither an invisible rebase nor a silent overwrite. Preserve the draft and show the changed base. Offer review of the new version, or retain the old submission as historical feedback needing an explicit integration decision.
6. Published report withdrawn or replaced: keep submitted history readable; block new submissions against a withdrawn report; preserve unsent draft and provide a visible superseding-report link.
7. Partial submission keeps deferred/unanswered decisions open. Independent questions can proceed. Drafts for the next report must not inherit previous choices without explicit review.
8. A second submission may supersede the respondent's earlier one, but it must name the earlier submission and remain a distinct immutable event. Already-integrated decisions require a new meaning-change proposal, not edit-in-place.
9. Existing locks are fcntl-based. Initial acceptance can explicitly cover the current macOS/Linux runtime. Claim Windows support only after selecting and testing a compatible lock implementation. Do not launch a cross-platform rewrite as an incidental task.

## 8. Authentication and participant rollout gates

Gate A: trusted local research workflow. The configured semantic authority explicitly attests. Receipts clearly say trusted_local_attestation. Reuse existing local deployment constraints, same-origin checks and canonical job authority. No claim of verified identity.

Gate B: authenticated individual response. Add a principal adapter deriving identity from a validated server auth session, not request JSON. Map that principal to the job's semantic authority and/or explicitly assigned respondent role. Add tests for forged human_id, unrelated job, expired session and revoked assignment.

Gate C: shared non-owner participation. Current share_gate blocks all non-owner POST requests. Add only a narrow authorization capability for assigned report draft/submit actions. It must inspect resolved target scope and action; it must not enable general Board, file, chat, terminal, meaning integration or report publication writes. A participant cannot become a SPACE owner as a workaround.

Gate D: sensitive real-user deployment. Confirm the selected identity policy, source storage boundary, retention and visibility are appropriate to the actual project. Do not introduce patient data into the public Tools repository. This gate is deployment-specific, not a reason to stop the local synthetic prototype.

## 9. UI behavior and states

Reuse the current Workbench shell and design tokens. Put round/report selection and progress inside the Rounds view. Deep links include the current space/view and report ID. The existing frame's _build_cards() should link directly to the pending decision report, without duplicating its form.

Essential states: no report yet; report generation underway; published waiting for human; draft saved; save failed; unsaved changes; partial submission; submitted awaiting integration; clarification requested; integrated; report superseded; stale base; read-only viewer.

Card ordering should reflect dependencies and importance, not a hard-coded ten-question count. Show question and essential contrastive evidence first; expand source detail, current rule and expected impact. Include a scope statement. Alternatives are unselected and should be neutrally worded. None/custom requires either an explanation or switching to defer; defer may carry a request for more examples.

Prefer server-confirmed autosave with a visible state. Browser local storage is optional recovery, not authority. On reconnect, do not overwrite a newer server revision. Save draft and Submit are different actions. Review before submission summarizes selected effects, custom text and unresolved decisions. Reload must restore server state.

Chat supplement must retain provenance. The first slice can support an explicit additional-context field with optional source references. Later integration can offer an explicit “Add this chat passage to the decision record” action that preserves the original source and author. Do not scrape arbitrary conversations or treat every chat statement as confirmed preference.

Accessibility: native radio groups, labels, keyboard movement, focus-visible, meaningful validation errors, status announcements, no color-only statuses, readable text at mobile width, sticky controls not covering final card content. Do not use raw HTML from the model or render source text through unsafe innerHTML.

## 10. Dependency-ordered work packages

W0: freeze interface contract. Owner: reviewer plus contract agent. Deliver schema, status machine, storage paths, authority modes, single writer and migration mode. Acceptance: independent reviewers can trace a form answer to a versioned rule without fabricating item approval; all later agents use the same action/field names.

W1: report storage and validation. Owner: contract/storage agent. Depends W0. Implement validate_report(), publish_report(), get_report(), get_draft(), save_draft(), submit_feedback(), list_pending_feedback(). Use explicit versions, atomic writes and idempotency. No model/API calls. Acceptance: immutable published reports, correct stale writes, exact replay and rejection of invalid options/foreign decision IDs.

W2: learning evidence adapter. Owner: evidence agent. Depends W0; can run alongside W1 in separate files. Implement resolve_learning_evidence() with corpus/split version matching and source provenance. Refuse evaluation/test item references even when the agent claims split=learning. Acceptance: sealed and validation sentinels never appear in report JSON, HTML, browser state, debug errors or source previews.

W3: engine integration of feedback. Owner: Meaning Agent implementation owner. Depends W1/W2 and the separate meaning contract. Deliver a pending-feedback queue and integration plan artifact. First slice may stop at a inspectable integration proposal. It must not pretend complete automatic rule application if semantic reconciliation is absent. Acceptance: same submission is integrated once; conflicts/custom text return to human; rule and reference versions remain aligned.

W4: Workbench rendering. Owner: UI agent. Depends W0; initial fixture development may run alongside W1/W2. Build renderer and controller against versioned static fixtures; no local shell copy. Acceptance: all explicit states work, no preselected options, draft/error/review behavior at desktop and mobile, content escaped.

W5: single-door integration. Owner: integration owner, exclusive labeling.py and task_labeling.py edits. Depends W1/W2/W4. Add capability-aware module loading, checked dispatch and UI entry. Existing Rounds mode remains readable. Update frame prompt text and progress from engine state, not browser assumptions. Acceptance: same-origin and canonical target checks; disabled or missing engine yields truthful unavailable state; no duplicate picker or service.

W6: principal and permissions adapter. Owner: access owner. Gate A can ship first with accurate attestation semantics. Gates B/C are separate tasks. Acceptance: spoofed identity rejected in authenticated mode; no external participant gets generic write privileges; read-only share behavior unchanged elsewhere.

W7: integration and adversarial review. Owner: reviewer, distinct from maker. Depends W3/W5 and chosen identity gate. Run targeted tests, browser workflow and failure recovery. Verify real server response, persisted file, subsequent engine read and reload all agree. UI green alone is insufficient; wire green alone is insufficient.

W8: production pilot ticket. Owner: reviewer/user. Depends W7. Prepare a real project task and Run ticket; user starts any model/compute Run. Do not perform an unasked live corpus or model experiment. Keep real data out of Tools.

## 11. Meaningful acceptance tests

Engine tests:

- Published report is immutable; a new version can be published without replacing earlier feedback.
- Report points to nonexistent/validation/test item: rejected before publication; textual split spoofing does not pass.
- Cross-job decision IDs and unknown option IDs rejected.
- Two drafts based on the same revision: one succeeds, one receives conflict and retains recoverable text.
- Same request replay returns exactly one submission; same request ID with different normalized answer fails.
- Crash after immutable submission write but before ledger event: restart recovers one submission and one eventual event.
- None/custom without an explanation cannot be submitted; defer and unanswered remain distinct.
- Partial submission preserves unresolved cards and never emits item gold.
- Old base meaning is explicitly stale; no silent rebase.
- A chat source marked model-authored cannot become a human-confirmed preference without the explicit user action.
- Human-decision submission and policy integration are distinct events; neither is allowed to update the other's artifact in place.

HTTP tests:

- Shared host route, dedicated labeling host route and canonical Page path resolution.
- Malformed body, oversized input, missing Origin, cross-origin, illegal mode and invalid/mismatched Page URL.
- Authenticated-mode human_id spoof, wrong assigned job, read-only viewer and non-owner share denial.
- Static GET and HEAD to the new report/draft/submission storage return no private data.
- Error responses do not echo held-out text or private comments.

Browser tests:

- Initial load has no selected preference; required evidence and source labels visible.
- Select, comment, save, reload, recover draft, edit from another tab, receive conflict.
- Review and submit once; simulated response loss then retry returns original receipt.
- Existing pending records survive switching Workbench tabs and reconnecting.
- None, defer, comments and partial submission yield the documented state.
- Source text containing script-like markup is shown as text.
- Narrow mobile layout, keyboard-only completion and save-error state.
- Real backend submission is then read by the engine's pending-feedback listing.

## 12. Concrete commands for the implementation reviewer

Run from <workspace> using its interpreter. These are planned commands, not claims that the new tests already exist or passed.

    .venv/bin/python -m pytest Tools/plugins/haipipe-toolkit/skills/2_theme/labeling/engine/test_decision_reports.py Tools/plugins/haipipe-toolkit/skills/2_theme/labeling/engine/test_meaning_evidence.py -q

    .venv/bin/python -m pytest Tools/plugins/haipipe-toolkit/skills/2_theme/labeling/engine/test_calibration.py Tools/plugins/haipipe-toolkit/skills/2_theme/labeling/engine/test_definition_discussion.py Tools/plugins/haipipe-toolkit/skills/2_theme/labeling/engine/test_preparation_workbench.py -q

    .venv/bin/python -m pytest Tools/plugins/haipipe-toolkit/servers/workbench-labeling/tests/test_decision_reports.py Tools/plugins/haipipe-toolkit/servers/workbench-labeling/tests/test_labeling_theme.py Tools/plugins/haipipe-toolkit/servers/_host/tests/test_auth.py Tools/plugins/haipipe-toolkit/servers/_host/tests/test_share.py Tools/plugins/haipipe-toolkit/servers/_host/tests/test_private_static.py Tools/plugins/haipipe-toolkit/servers/_host/tests/test_workbench_conformance.py -q

The browser acceptance script should be a new fixture-backed test under workbench-labeling/tests/, using an isolated test server or the approved configured host. Do not prescribe a made-up production origin. For the actual configured host, use the existing /wb opener and DOMAIN verification. Restart only the affected server after server-code edits; never create an ad-hoc public tunnel.

A smoke test that only imports a module, checks file existence, or asserts HTML contains “Submit” is insufficient. Require an accepted HTTP submission, the exact stored semantic response, engine visibility, and UI reload proof.

## 13. Migration issues that require explicit design decisions

1. Existing definition_discussion.py is initial-label-only: it refuses rounds after release, forbids round examples and closes only after every label is settled. Reuse history concepts, not its lifecycle as the rule-report engine.
2. Existing calibration.py is item-major: show → first → lock → reveal → final. Preserve it for direct reference-label collection; do not route each rule decision through fake item IDs.
3. Current workbench frame copy assumes H/L/N and seven pools. The new system should render a task-declared schema and diagnostic definitions. Keep old jobs readable; update new-mode labels without silently rewriting existing schema.
4. The current engine's single P1 frontier and UI “finish discussion first” behavior may block unrelated work. The new report engine needs per-decision dependencies and approved-version execution; do not simply remove old gates globally.
5. Current holder semantics seal a final test and hide text from Building. The user's new training-free method also needs development validation, separately from final test. Do not rename the sealed test to validation or expose sealed items through report sources.
6. Current caller attestation is not verified identity. Preserve truthful receipts in local mode and add identity as a separate capability.
7. Some legacy helpers return text_hash fields. New contracts must not introduce, calculate or rely on content hashes. Do not perform an unrelated hash-removal sweep.

## 14. Recommended first deliverable

One end-to-end vertical slice with synthetic data and no model calls:

Publish one structured learning-only report through the engine → show it within the actual Rounds view → save/reload a server draft → submit partial feedback idempotently → read the pending feedback through the Meaning Agent's engine interface → show “awaiting integration” without changing the approved guideline.

This slice proves the core interface and ownership before implementing automatic mining, rule reconciliation, model qualification or large-scale labeling. It is the right first agent assignment after the parent plan freezes the contracts.
