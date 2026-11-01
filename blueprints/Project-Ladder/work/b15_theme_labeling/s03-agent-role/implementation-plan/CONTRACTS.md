# Engine contracts and Workbench behavior

Version: 2  
Reconciled on 2026-11-01 to slide deck version 12 (Train and Test, Execution & Audit Agent, round report); version 1 was written against version 8.

Implementation specification. Coordinator dispositions and specialist re-review of version 1 are recorded in REVIEW.md, which cites version 1 section numbers; version 2 adds section 7 (RoundReport), so version 1 sections 7 to 14 are sections 8 to 15 here, and the version 2 reconciliation has not been re-reviewed. Paths and function names marked proposed do not yet exist; contract approval is not proof of implemented behavior.

## 1. Ownership and storage

Let J be the private labeling lane returned by the existing page resolver. For a canonical Page, J is <Page>/labeling/. The resolver, not a client-supplied absolute path, decides this address. Keep Run tickets at the Page's existing runs/ address and results at its existing results/ address; do not invent a second Run hierarchy.

Extend the existing lanes in decision-report mode:

    J/
      config.yaml                         existing job identity and mode
      corpus/                             authorized Train projection only
      splits/                             public-safe counts and custody references
        manifest-vNN.json                 Train/Test counts and source-group assignments
      meaning/
        sources/<source-id>/vNN.json       original human sources and provenance
        reports/<report-id>/vNN.json       immutable published report revision
        drafts/<report-id>/<actor-id>.json mutable, revision-checked draft
        feedback/transactions/<tx-id>/     atomic committed feedback bundle
        integration/<integration-id>/     proposed patch, checks and outcome
        events/<sequence>-<event-id>.json  immutable lifecycle/transition records
        releases/<release-id>.json         immutable semantic commit manifest
        view/                             derived report views only
      rounds/round_NN/                     unchanged legacy item calibration
      policy/
        versions/G_NN/                    approved semantic release
          manifest.yaml                   binds meaning version and approvals
          rules.json                      canonical structured meaning
          uncertainty.yaml                approved diagnostic criteria
          guideline.md                    rendered baseline expression
        expressions/mNN/eNN/              wording candidates under fixed meaning
      gold/versions/lNN/                   approved Train references; Test rows stay in custody
      issues/<issue-id>/                  immutable revisions and resolution
      staging/round-NN/                   one Step 5 round
        report.json                       the round report; Test cases by custody reference only
        aggregates.json                   performance by model and partition
      confirmation/                       custody references and permitted summaries of the fresh independent set only
      handoff/                            existing immutable crossing
      production/                         existing batch/attempt lineage
      audit/                              existing audit lineage
      cache/                              rebuildable views, never approval authority

Test and confirmation item stores and their reference labels remain under their designated custodian, outside refiner-visible roots; confirmation stores also stay outside every agent-visible root. J/splits exposes counts, versions, source-group assignments and custody state, not Test or confirmation texts, item identifiers or nearest-neighbor indexes.

Full Test and confirmation predictions, item-level diagnostics, failed responses, attempts, reasons and logs also remain in custodian storage. J/staging and J/confirmation are disclosure-controlled projections only, not custodian stores colocated with refiner-visible files: report.json names Test cases only by custody reference, and aggregates.json holds performance by model and partition. J/gold contains Train references; a Test or confirmation reference manifest visible here contains only safe counts, version/custody bindings and permitted status. Role permissions apply to backups and exports as well as live views.

Refiner-visible roots are the parts of J the expression rewriting step may read: corpus/, gold/, policy/ and staging/. The meaning/ and issues/ lanes are outside them; they cite Test cases by custody reference and keep human comments on Test cases as written. The auditor, the Meaning Loop Agent and the assigned human resolve Test references at read time through the audit role; derived views and caches never store the resolved content. Approved rules, guideline text and expression examples carry no Test text.

The new meaning/ lane isolates rule-level reports from legacy rounds/ item events. Each report still records its logical round_id and owner-native Run reference. staging/round-NN/ numbers Step 5 execution rounds; it is unrelated to the legacy rounds/round_NN/ lane and to a decision report's round_id. Do not replace historical G_00 records. A new-mode status adapter must not mistake a published report or submitted form for an old calibration checkpoint. The new policy manifest explicitly lists rules.json and its schema; do not silently assume the legacy POLICY_COMPONENTS list already accepts it.

## 2. Common envelope

Every authoritative new record has:

| Field | Rule |
|---|---|
| schema / schema_version | Explicit record kind and version |
| job_id | Resolved server-side and matched to the route |
| id / revision | Stable record identity and monotonic revision |
| created_at | Real clock timestamp with timezone |
| created_by | Actor or service identity plus evidence level |
| parent_refs | Explicit logical references to prior versions |
| run_ref | Existing owner-native logical Run address when applicable |
| status | Enumerated state, never inferred from a file merely existing |

Identifiers must satisfy a bounded allowlist. Do not accept path separators, encoded traversal, symlinks escaping J, arbitrary output paths or secret-bearing model configuration in the browser payload.

Use ordinary source/model version strings, explicit version numbers and exact JSON-value comparison. Do not introduce checksums or content fingerprints.

## 3. SourceRecord

Required:

- source_id, revision, kind: human_idea | human_comment | chat_excerpt | prior_decision | train_item | test_item | supplied_document.
- provenance: author, capture channel, original location, source version, observed timestamp, access scope.
- original_text or a checked reference to original text.
- interpretation: optional agent summary kept distinct from the original.
- authority: context | proposed_preference | confirmed_decision.
- approval_refs: required for confirmed_decision; each must resolve to a valid committed human approval event for this exact source revision and scope.
- exposure_role and partition (Train or Test) where applicable. A test_item source holds a custody reference and the round report that named it, never a copy of the Test text.
- synthetic: explicit true for fixtures and demos.

A supplied document can be relevant evidence but is not automatically semantic authority. Instructions embedded in a corpus item are content to label, not instructions to the harness. A web/document source cannot silently replace the identified person's preferences.

The collector accepts context or proposed_preference; it cannot make itself authoritative by setting an enum. Promotion to confirmed_decision is a new source revision produced by checked integration with approval provenance. Original text stays intact. Unverified legacy authority is labeled as such, not invented as a confirmed event.

The approval references the source payload revision the person actually saw. The later derived confirmed-authority revision retains approved_source_revision and derived_from, with unchanged approved payload. It does not require approval of a not-yet-created metadata revision, and it cannot smuggle changed source text into the old approval scope.

Each displayed excerpt must resolve back to a source record and location. If the source is missing, the card is invalid or clearly marked as needing evidence; never fabricate a quotation.

## 4. Item and split contracts

Item:

- item_id, corpus_version, source_record_id, source_locator.
- split_group_id, item_unit, main_text or content reference.
- context_before, context_after, context_visibility_policy.
- legacy_labels in a separate evidence field, never silently treated as current gold.
- preparation_status with rejection reasons for malformed or unusable items.

SplitManifest:

- split_version, corpus_version, group_policy, assignment_method, random_seed when used.
- train / test / production counts, and the source-group assignment of each Train and Test group.
- confirmation: a custody reference and count only, when a fresh independent set exists.
- custody references, exposure policy, Test exposure history, assignment timestamp.
- overlap/duplicate-check result and any limits.

The trusted preparation service can group records before assignment. Use stable source/conversation identity, lineage and explicit exact or similarity checks without introducing content hashes. Group correlated turns, duplicates and related records together, so related sources stay in one partition. An already exposed group cannot later be advertised as fresh confirmation data, and a Test group whose findings guided approved revisions is development exposure for later versions.

Do not fix split sizes in this implementation. Choose them from label coverage, number of independent groups, uncertainty and evaluation precision. Insufficient support produces an explicit limitation.

## 5. DecisionReport and DecisionCard

DecisionReport:

- report_id, report_revision, round_id, publication_status (immutable state at publication).
- base: task_frame_version, meaning_version, reference_version, corpus_version, split_version.
- round_report_refs: the round reports whose issues this report answers, when applicable.
- intended_human_id or assigned participant binding.
- title, purpose, sources, ordered cards.
- dependencies and supersedes_report when applicable.
- published_at, publication_actor, budget or reading-load estimate if measured.

DecisionCard:

- decision_id and question_type: define_rule | boundary | exception | precedence | inconsistency | reference_label | diagnostic | acceptance_policy.
- question, why_now, current_rule_refs.
- evidence: Train item references, Test case custody references (their excerpts are resolved at read time for the assigned human), human source references, contrast roles and exact excerpts.
- origin: for a card raised by an audit issue, the round report reference and origin partition (Train or Test).
- candidate_options: stable option_id, neutral label, explanation, expected effect, affected scope.
- optional exact_rule_patch for an option whose meaning can be approved directly.
- none_allowed, defer_allowed, comments_allowed, comment_requirements.
- diagnostic_context: ambiguity, missing context, rule overlap or other reason.
- dependencies: other decision IDs or meaning versions required before applying this choice.
- approval_scope: exact_rule_patch | preference_only | diagnostic_definition | explicit_item_set | explicit_audit_policy.

All options start unselected. Do not rank options by a persuasive visual treatment. An agent may explain its recommendation when explicitly requested, but the provenance and alternative interpretations remain visible.

No fixed limit of ten cards. Start with a configurable small batch and test completion burden. Split a question with multiple independent judgments into separate cards; merge redundant cards covering the same rule.

Published revisions are immutable. Updating a question, option, scope or evidence creates a new report revision. A user's draft stays bound to the revision they saw; it must not be silently applied to changed choices.

Later report and submission transitions are immutable lifecycle events under meaning/events/, with event_id, monotonic sequence, actor, timestamp, target identity/revision, prior event reference, transition and reason. Committed integration receipts supply integration outcomes. A read projection returns current_status separately from the original payload. Indexes and status views can be reconstructed from committed records; they are not authority.

## 6. HumanDraft and HumanSubmission

Draft:

- report_id, report_revision, actor_id, draft_revision.
- answers keyed by decision_id: kind = chosen | reject_options | custom | defer | unanswered, with selected_option_id only for chosen.
- Each saved answer has a stable answer_id and monotonic answer_revision under its report/card/actor binding. Submission embeds that exact revision; a direct submit without a prior draft allocates it server-side.
- comments and additional_context.
- base_meaning_version, last_saved_at.

Submission:

- submission_id, request_id, report_id, report_revision, draft_revision.
- actor: principal_id, authority_id, verification_mode.
- base meaning/reference versions.
- immutable answer snapshot with the exact visible option/patch and source references.
- explicit confirmation event and timestamp.
- per-card disposition: chosen | rejected_options | custom_proposal | deferred | unanswered.
- approval scope and conditions; comments are not discarded.
- integration status projection: received | queued | integrating | applied | needs_clarification | stale | failed. Later transitions are separate immutable events; they never rewrite the submitted answer snapshot.
- acknowledgement containing durable submission identity.

Participant-entered human_id is not proof of identity. In trusted-local mode, record verification_mode: local_attestation and do not claim verified participant identity. In shared mode, derive the actor from the authenticated server session and verify assignment to this job.

Explicitly submitting a clear selection of an exact published patch can approve that patch within its displayed scope. Merely selecting an option or saving a draft is not approval. A comment such as “only for adults” changes the selected scope and requires reconciliation; the system must not apply the unqualified option and ignore the comment.

Custom prose is authoritative as what the person said, but newly inferred executable conditions are not automatically approved. Preserve the prose and present the interpretation if needed. Do not force another click when the exact already-visible change was unambiguously approved.

The prototype's historical exports say rule_preference_only. Import them as preferences, never upgrade them into exact-rule approvals.

Rejecting all options is distinct from proposing a custom answer, deferring, or leaving the card unanswered. A card may request a reason for rejection independently of its custom-answer text requirement. Rejected options leave the issue open and apply no semantic patch. All four states survive save, reload and submission without conversion.

## 7. RoundReport

Every Step 5 round writes one round report, at J/staging/round-NN/report.json, with its performance at J/staging/round-NN/aggregates.json. The Execution & Audit Agent's auditor context writes both through the round reporter. No round proceeds to Step 6 without a round report, and none ends without a recorded stop or continue reason.

RoundReport:

- id: round-NN (the Step 5 round); parent_refs names the previous round report and run_ref the owner-native Step 5 Run.
- versions: meaning mNN, expression eNN (every candidate tried), reference labels lNN, execution xNN, and the corpus and split versions of the item set.
- performance: a reference to aggregates.json, which holds quality, coverage, abstention, invalid and failure counts with their denominators, by model and partition (Train and Test shown separately). It holds only predefined metrics and sufficiently supported strata, with small cells suppressed (section 11).
- changes_attempted: the expression candidates tried this round and their outcomes.
- error_hypotheses: each with class, evidence, alternative explanations, affected scope and origin partition. class: expression_issue | rule_gap_or_conflict | suspected_reference_label_error | executor_limit | missing_context.
- unresolved_questions, with their uncertainty.
- recommended_next_action, with candidate actions and their affected scope.
- route: continue_in_step_5 | reopen_meaning_loop | proceed_to_step_6 | stop, with route_reason (the round's stop or continue reason).

Error hypotheses are hypotheses. Executor consensus alone cannot establish that a reference label is wrong; a suspected reference-label error changes no label until the Meaning Loop decides through its approval route. Genuine item ambiguity is recorded with the diagnostic fields of section 8, not forced into a rule change. A report may find that no change is warranted.

Routes:

- continue_in_step_5: expression-only issues. The next round rewrites from Train evidence while the approved rules stay unchanged.
- reopen_meaning_loop: rule, preference or reference-label questions from either partition. The report goes to the whole Meaning Loop Agent, never straight to a human: Step 2 investigates related cases, earlier decisions and original context first, Step 3 collects preferences again on the questions that remain, and Step 4 returns compatible versions for a new Step 5 round.
- proceed_to_step_6: the declared criteria are met for this round's exact versions. A changed standard is not released because an earlier version passed.
- stop: a budget is exhausted, or no candidate can meet the floors because of executor limits or missing context that neither rewriting nor a rule change can fix. The report names the decision needed (another executor, more human review or no deployment), and nothing proceeds to Step 6.

Train evidence appears in report.json directly. Test entries in report.json are custody references with their class; the Test case-level records (items, predictions, references, errors and evidence) stay in custodian storage outside refiner-visible roots. The expression rewriting step reads Train evidence and aggregates.json, never Test case-level records. A comparison between rounds states whether references or meaning changed between them, so expression-only gains under unchanged references stay apart from reference-label corrections and semantic changes.

A written round report is immutable. Later investigation outcomes and issue dispositions are separate records that reference it.

## 8. Diagnostics accompanying an item label

| Field | Meaning / values |
|---|---|
| task_label | A label from the job's substantive schema, or null when unresolved |
| label_status | predicted, provisional, human_reviewed, accepted_by_audit, deferred |
| ambiguity | low, high, unknown, using approved criteria |
| review_effort | easy, hard, unknown, if this dimension is collected |
| uncertainty_status | resolved, ambiguous, insufficient_evidence, unknown |
| uncertainty_reasons | missing_context, overlapping_rules, unclear_boundary, unfamiliar_case, conflicting_evidence, other |
| review_action | accept_candidate, inspect, request_context, defer |
| assessor | Human identity or executor identity and version |
| guideline_binding | Meaning and expression versions used |
| evidence_refs | Sources and applicable rule IDs |

These are proposed defaults, not a universal schema. A task can use a single difficulty field only if its definition is explicit. Do not mix intrinsic ambiguity, human effort, model self-reported confidence and cross-model disagreement into one unexplained score.

Confidence numbers are optional. Do not label them calibrated probabilities without evidence. Unknown diagnostic values must remain possible. Models can be confidently wrong; random audits and coverage sampling remain part of the design.

## 9. Meaning, expression and reference contracts

MeaningSnapshot:

- meaning_version, parent_meaning_version, task_frame_version.
- rules: rule_id, text, conditions, action, exceptions, precedence, applicability.
- diagnostic schema and review policy.
- approval_refs and unresolved exclusions.
- conflict-check outcome and affected dependencies.

For new-mode releases, the policy manifest explicitly maps its G_NN directory to one unique meaning_version mNN. Readers resolve that mapping through the committed release, not by assuming the legacy G_00 reader supports later versions. A human-approved principle may be released with reference_status: pending or partial; rules without suitable approved reference coverage remain ineligible for scored claims. Do not require the user to label every affected item merely to record an accepted rule.

ExpressionCandidate:

- expression_version, meaning_version, source_expression_version.
- rendered instructions, examples, output schema and formatting choices.
- change classification: wording_only or semantic_issue_detected.
- Train evidence and Train examples used, fidelity checks, model trials on Train and Test, and the selection record (Train evidence plus Test aggregates).

ReferenceSet:

- reference_version, meaning_version, corpus/split version.
- each row's item ID, label, reason, reviewer/authority, approval event and scope.
- provenance tier; direct reference labels are distinct from accepted production labels.
- exclusions, unresolved items and revision reasons.

The complete row-level ReferenceSet exists only in the permitted custody lane for its partition: Train rows under J/gold, Test and confirmation rows in custodian storage. Refiner-visible manifests for Test and confirmation omit item identities, labels and reasons. A Test reference-label correction approved through the Meaning Loop creates a new reference version in custody. Record reference presentation mode: blind_first, model_assisted or legacy_unknown. Confirmation references, and any reference described as independent, use blind-first judgment before revealing candidate predictions or model identity; a Test correction reviewed after executor disagreement flagged the case is model_assisted. Assisted references remain identifiable and cannot silently be described as independent.

Handoff:

- Exact meaning, expression, reference, executor, runtime, schema and split versions.
- Release readiness evidence (the round reports and staging results it relies on, Test exposure status, and confirmation design and results when an authorized confirmation ran), allowed corpus scope, coverage and quality limits.
- Human freeze decision, invalidation state and lineage.

Meaning and references form a pair. Do not score a new guideline against stale references without explicitly testing and resolving whether their semantics still match.

## 10. State machines

Report:

    draft -> validated -> published -> partially_answered -> submitted
                                      |                     |
                                      +-> superseded        +-> integration_pending
                                                           +-> resolved
                                                           +-> follow_up_required

Individual cards can remain open while other submitted cards are integrated. A single report-level state is a summary of per-card states, not a global stop flag.

Decision:

    open -> draft_answer -> submitted -> checked
                                        |-> exact_patch_approved -> applied
                                        |-> custom_or_qualified -> clarification_needed
                                        |-> conflict -> clarification_needed
                                        |-> deferred -> open_in_later_report
                                        |-> stale -> rebase_review

Expression:

    proposed -> fidelity_checked -> train_tested -> test_scored
                  |                    |               |
                  +-> meaning_issue    +-> diagnose    +-> selected / rejected
                                                         |
                                                         +-> frozen_candidate

Round:

    running -> scored -> analyzed -> reported
                                    |-> continue_in_step_5
                                    |-> reopen_meaning_loop
                                    |-> proceed_to_step_6
                                    |-> stop

A failed expression attempt may stay within the Step 5 staging loop. Route a round to the Meaning Loop, with its evidence in the round report, only when a rule, preference or reference-label decision is needed; difficulty alone does not prove the guideline is ambiguous. Every round ends in reported with exactly one route and its reason.

## 11. Access matrix

| Role | Train content | Train references | Test content | Test references | Confirmation content/references | Meaning writes |
|---|---|---|---|---|---|---|
| Meaning Loop Agent | Yes | Yes, with provenance | Cases a round report names, with context | Those cases, with provenance | No | Candidate patches only |
| Expression rewriting step (Execution & Audit Agent) | Yes | Yes | No | No; Test aggregates only | No | No |
| Auditor (Execution & Audit Agent) | Yes | Yes | Yes, case level | Yes, case level | No | No |
| Train executor | Assigned items | No | No | No | No | No |
| Test executor | No | No | Assigned items | No | No | No |
| Staging scorer | Fixed scoring inputs only | Yes | Fixed scoring inputs only | Yes | No | No |
| Confirmation executor/scorer | No | No | No | No | Authorized confirmation roles only, references hidden from executor | No |
| Human decision UI | Train evidence | Scoped reviewed evidence | Cases named in assigned cards | Scoped, for those cases | No | Explicit assigned approvals only |
| Reference adjudicator | Assigned reference collection | Scoped | Assigned Test reference review | Assigned | Separate authorized confirmation workflow | Reference judgments only |
| Production executor | Production items only | No | No | No | No | No |

The expression rewriting step may read a whitelist of Test aggregates in staging/round-NN/aggregates.json, such as predefined metrics by model and sufficiently supported strata, for candidate selection. It may not request arbitrary slices that identify individual Test cases or reconstruct their labels, and no raw Test content, case-level errors or examples enter its context, logs, memory or few-shot examples. Test is case-level visible to the auditor, to the Meaning Loop Agent for the cases a round report names, and to human review. Record which Test cases reached the Meaning Loop or human review; once their findings guide approved revisions, later Test scores are development exposure, not unbiased estimates for unseen data.

Role is bound by the trusted tool/session, not accepted as a client-controlled role parameter. Separate model-call contexts, histories, retrieval indexes, log readers and caches; the auditor and the expression rewriting step are separate contexts even inside one Execution & Audit Agent. A single orchestrator can coordinate all roles but must not forward Test case-level records into expression rewriting prompts, or confirmation artifacts into any agent prompt.

Application checks do not constrain an unrestricted agent that can read the entire disk. For a strong isolation claim, custodian stores need separate worker permissions or mounts: the expression rewriting step must lack direct filesystem access to Test stores, and every agent must lack it for confirmation stores. Record the actual isolation level.

## 12. Proposed tool surface

| Tool | Inputs | Outputs | Critical refusal |
|---|---|---|---|
| collect_source | job, source text/ref, provenance | SourceRecord | unauthorized source path |
| search_train | query, filters, budget | Train evidence refs | Test or confirmation items, or unrestricted raw dump |
| read_audit_issue | round report issue reference, trusted role | The named Train or Test case with context and reference provenance | expression rewriting role, a case no round report names, or confirmation content |
| build_decision_report | base versions, cards | Validated report draft | unsupported source, confirmation content, Test content without an audit-issue reference, malformed options |
| publish_decision_report | report revision | Published immutable report | stale bases or invalid evidence |
| save_human_draft | expected revision, answers | New draft revision | concurrent edit / wrong principal |
| submit_human_feedback | request ID, expected revisions | Durable receipt | stale/changed report, forged authority |
| integrate_feedback | submission IDs, expected meaning | Patch/check result | conflict, unapproved reinterpretation |
| approve_reference_items | explicit item scope, judgments and committed scoped approval events | Reference revision | inferred rule approval, missing approval evidence or unauthorized actor |
| run_executor | assigned role, versions, item batch | Predictions + diagnostics + runtime | reference labels in executor prompt |
| score_staging | frozen predictions, scoring spec, partition | Aggregates by model and partition; Test case-level results to custody | Test case-level results to the expression rewriting step |
| write_round_report | round versions, scores by model and partition, classified error hypotheses, route | Immutable round report | Test case content inline, a route to Step 6 without met criteria, or a missing stop or continue reason |
| freeze_candidate | selected versions, round report routed to Step 6, release criteria, confirmation protocol if authorized | Immutable release candidate | mutable protocol or pending prerequisites |
| issue_handoff | frozen candidate, passing release readiness check, required approvals | Immutable production handoff | failed, absent or stale release check |

Tool names are a proposed interface. Keep the existing public skill door and current HTTP write entry point; do not expose all these tools as new top-level product navigation.

## 13. HTTP and rendering integration

Serve decision-report mode in the meaning Task's Preferences view on the focus page (labeling_focus.py; b15 s13 maps Step 3 to it, s58 C3 draws it: one turn's cards as a /haipipe-interaction collect Run, answered only in the meaning Task); the legacy Rounds view keeps item calibration. A dedicated decision_report_view.py owns markup/view-model composition; its scoped JavaScript handles draft state and form interaction. The existing labeling.py remains the one route integrator.

Report publication and integration initially use engine tools or the existing owner-native command-line route. They are not browser response actions and cannot record human choices.

Proposed actions through POST /_board/labeling/act:
- decision_draft_save: assigned human, expected report/draft revisions.
- decision_feedback_submit: assigned human, explicit confirmation, request ID.

Read projections use the existing checked page target and canonical lane resolution. Define read actions or a narrow checked GET route under the same workbench family; no raw static file serving.

Response requirements:

- 200: saved or durably received, with exact versions.
- 400/422: malformed envelope or invalid field-level choice.
- 403: actor lacks permission or origin/session checks fail.
- 404: unavailable or out-of-scope job, without disclosure of private existence.
- 409: stale draft/report/meaning binding or conflicting reuse of a request ID.
- 413: configured payload bound exceeded.
- Temporary agent failure after receipt: submission remains received/queued; do not erase it or report it never saved.

Use server-derived principal mappings in shared deployments. Preserve existing origin and page checks; do not rely solely on them as authentication. Add request-forgery protection appropriate to the existing session design.

The host currently parses the body in _host/serve.py before labeling_act. The coordinator owns a narrow endpoint-specific pre-parse size guard or verifies an existing equivalent before T04 completes. Reject malformed, negative or oversized Content-Length before unbounded reading/JSON parsing; handle unsupported transfer framing explicitly. Action-level field validation remains B's responsibility. Preserve unrelated endpoints and their legitimate limits.

## 14. Transactions, concurrency and recovery

One engine store owns durable writes. Select and test a platform-appropriate lock abstraction; existing calibration uses POSIX fcntl and cannot simply be assumed portable to every executor host.

Under the job write lock:

1. Resolve and validate caller, job and report bindings.
2. For submission, look up request_id scoped to job and authorized actor before current revision checks. A committed request with the same normalized immutable request envelope returns the original receipt; changed reuse returns conflict. Do not reconstruct the comparison from a changed draft. Exact equality is sufficient; no hash.
3. Only a new request compares expected draft/report/meaning revisions. A replay can recover its committed receipt after the draft advances or report is superseded, subject to current authorization. Revoked authority may deny access without deleting the committed record.
4. Write the immutable submission payload and its event/outbox record into a temporary transaction directory on the same filesystem.
5. Flush as required and atomically rename that directory into the committed transaction store.
6. Update rebuildable indexes. A crash after commit but before indexing is repaired from committed bundles.
7. Return the durable submission identity.

The queue processes by submission ID with an integration receipt. Retry after timeout must not apply a semantic patch twice. Receiving a submission and integrating it are separate transitions.

Submission idempotency is not enough for repeated partial forms. Maintain a decision history keyed by job, report revision, decision_id and semantic scope. If a new request repeats an already committed answer with the same patch, comment and scope, reference its existing decision effect rather than applying it again. Changed answers create a new answer revision with explicit supersession/conflict lineage; they never undo a prior effect merely by arriving later. Independent newly answered cards can proceed. Check repeated partial submissions, separate request IDs, edited comments, conflicting principals and overlapping rule patches.

Semantic integration uses a second transaction protocol. Under the job lock, check the base meaning and approval dependencies; stage the new immutable policy, compatible reference manifest (carried-forward, newly approved, pending or excluded scopes), dependency invalidations, issue dispositions and integration outcome; flush and place every artifact at its new version address. Publish an immutable meaning/releases/<release-id>.json commit manifest last. That manifest binds the complete artifact set, approval/decision-effect IDs, expected predecessor and changed scopes. Unchanged references may be carried forward only with an explicit compatibility decision and their original approval provenance; affected references remain excluded until separately resolved. New-mode readers treat a version as released only through a valid committed manifest. A policy directory alone is not a release. Current-version pointers and UI projections are derived from those manifests.

A crash before the final manifest leaves unpublished artifacts, which recovery can verify and resume or mark abandoned. A crash after it is repaired by rebuilding projections. No reader may observe half of a semantic/reference release. Recheck approval and base preconditions before resuming a pre-commit attempt. Do not generate a reference change when only a rule was approved. Legacy readers stay on their legacy lane; migration tests prove that new-mode code never bypasses this release boundary. Inject a failure after each artifact placement and before/after manifest publication, and check recovery without content hashes.

On a stale meaning base, preserve the submitted human intent as an unapplied stale record when appropriate, show the conflict, and require explicit rebasing. Never silently map old option A to a new option A.

Concurrent comments can be preserved independently, but conflicting rule patches require a semantic resolution. A stale draft must be recoverable for the user even when the save is rejected.

## 15. Invalidation

Maintain dependency edges from rules and meaning versions to reports, references, expressions, execution results, round reports, handoffs and audit claims.

- A changed rule invalidates affected expressions and score claims until rechecked.
- References under changed semantics require review; do not silently relabel the gold.
- A report with unaffected dependencies may continue; a changed relevant rule makes it stale.
- Current production batches retain their frozen version. Stop or quarantine affected work according to policy; do not blend versions into one unlabeled “latest” result.
- Unknown dependency scope triggers conservative invalidation and an explicit explanation.
- Once Test findings guide an approved revision, later Test scores are development exposure; record it, and require the fresh independent confirmation set for claims about unseen data.

Store the invalidation event and replacement version. Do not delete history.
