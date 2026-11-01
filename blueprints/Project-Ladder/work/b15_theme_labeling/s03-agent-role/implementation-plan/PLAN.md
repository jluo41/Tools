# Subjective labeling: implementation and delegation plan

Version: 2  
Reconciled on 2026-11-01 to slide deck version 12 (Train and Test, Execution & Audit Agent, round report); version 1 was written against version 8.  
Prepared: 2026-10-27  
Status: reviewed implementation specification (the review in REVIEW.md covers version 1; this reconciliation has not been re-reviewed); implementation not started in this planning turn  
Concept owner: Tools blueprint b15, Studio s03  
Implementation authority: the user's latest decisions in this conversation  
Delivery owner and final reviewer: the coordinating agent

## 1. Intended outcome

Build an end-to-end, training-free labeling system inside the existing Workbench. A person may enter with a rough idea or with previously labeled data. A Meaning Loop Agent helps that person articulate a standard through source evidence, cases and decision forms. An Execution & Audit Agent runs fixed-weight executor models on Train and Test, improves how the accepted standard is expressed using Train evidence only, analyzes errors and writes a round report for every round. A qualified executor then labels a larger corpus under explicit review and audit policies.

The two aligned outputs are a structured adaptive guideline and human-approved, guideline-consistent reference labels. A larger inferred or audited corpus has its own provenance. A rule approval must never silently certify all labels propagated from that rule.

Forms are the default interaction. Chat is supplementary. Both contribute to the same versioned decision record. The agent generates structured form content; Workbench renders, saves and submits it consistently. A fresh webpage implementation is not generated on every round.

This package is a plan, not a claim that the complete system is implemented. Its first delivery milestone is a real Workbench form connected to a durable engine store, with an inspectable human feedback record and a deterministic simulated next step. Model execution and full-scale studies follow separately.

## 2. Read this package in order

1. [PLAN.md](PLAN.md): scope, architecture, rollout and decisions.
2. [CONTRACTS.md](CONTRACTS.md): records, permissions, states, tools and transaction rules.
3. [WORK-PACKAGES.md](WORK-PACKAGES.md): dependency-ordered engineering assignments.
4. [EVALUATION.md](EVALUATION.md): data boundaries, research comparisons and quality/speed acceptance.
5. [DELEGATION-AND-REVIEW.md](DELEGATION-AND-REVIEW.md): agent prompts, file ownership and reviewer gates.
6. [REVIEW.md](REVIEW.md): independent findings, coordinator dispositions and residual decisions for version 1.

Supporting read-only audits are retained in reviews/. They are evidence for the plan, not competing specifications. If an audit suggests a different path or schema, the coordinator's disposition and the contracts in this package win. REVIEW.md and reviews/ record the review of version 1 and keep its section numbers and terms (learning, validation, final test, Expression Loop); version 2 adds CONTRACTS section 7, so version 1 CONTRACTS sections 7 to 14 are now sections 8 to 15.

## 3. Non-negotiable design decisions

| Decision | Implementation consequence |
|---|---|
| Step 0 transforms a corpus into items and assigns Train and Test roles; Step 1 frames the task | Item identity, context and source groups precede task-specific exploration; related sources stay in one partition |
| Steps 2–4 form the Meaning Loop; Step 5 is the staging loop of the Execution & Audit Agent | The two loops have separate tools, contexts and write authority; the round report connects them |
| Only the Meaning Loop Agent asks humans for semantic decisions | Step 5 issues travel in a round report to the whole Meaning Loop Agent, where Step 2 investigates first; the Execution & Audit Agent cannot change meaning or directly demand human answers |
| Human feedback is asynchronous | Pending questions block dependent decisions only; approved independent work continues |
| Workbench forms are primary; chat is supplemental | Both channels create source-linked decision records, without silent chat overrides |
| Train and Test items are both labeled, scored and audited | Executor and auditor visibility is separate from expression-rewriting visibility |
| Only Train case-level evidence reaches expression rewriting | Test issues go to the Meaning Loop Agent in the round report and may reach human review; candidate selection uses Train evidence plus Test aggregates |
| Test findings that guide approved revisions make Test development exposure | Later Test scores are staging checks, not unbiased estimates for unseen data; such claims need a fresh independent confirmation set, run at Step 6 only when authorized |
| Every Step 5 round writes a round report | It records versions, performance by model and partition, classified error hypotheses and its route; no round reaches Step 6 without one |
| Difficulty and uncertainty accompany the task label | Define diagnostic criteria, reasons and review actions; do not equate confidence with correctness |
| Model weights remain fixed | Optimize guidelines and allowed runtime settings; do not fine-tune executors |
| Quality, coverage and speed all matter | Reject fast solutions that miss quality floors or defer almost everything |
| One human judgment can affect many items | Rule-level forms are first-class; item-level review remains available for references and audits |
| No content hashes | Use explicit versions, event sequences, source item identities and exact equality where needed |
| Existing work is preserved | No broad rewrite of old jobs, closed Runs, skills or receipts |

## 4. What exists and what must be built

The following source paths use E = plugins/haipipe-toolkit/skills/2_theme/labeling/engine and W = plugins/haipipe-toolkit/servers. Blueprint paths are relative to Tools. Verify them again before an implementation agent edits them; the shared workspace may advance.

| Area | Verified starting point | Important limitation |
|---|---|---|
| Corpus preparation | E/items_task.py, E/corpus_preparation.py, E/fence_source.py | Existing preparation has a development/protected-test boundary; Train and Test role assignment by source group, confirmation-set custody and new access roles need an explicit migration |
| Retrieval | E/corpus_tools.py: stats, sample, search, find_neighbours, get | Reuse its development-item eligibility checks for Train; do not broaden them to expose Test or confirmation content to expression rewriting |
| Labeling job authority | E/job.py: status, confirm_meaning, revise_meanings, policy_version | Existing revision restrictions and legacy gates do not implement the proposed asynchronous rule-level loop |
| Human meaning discussion | E/definition_discussion.py: start, say, decide, close | Current meaning discussion is constrained to early stages; it is not a general repeated decision-report service |
| Calibration | E/calibration.py: release_round, record_first, record_final | Only first-round random release is implemented; item events cannot stand in for rule-form submissions |
| Model calling | E/label.py: lm_labeler and transport helpers | Development-oriented wrapper is not a complete staging evaluation, release readiness or production service |
| Run vocabulary | E/run_catalog.py | Naming an operation does not establish that an implementation exists |
| Workbench | W/workbench-labeling/workbench-task-labeling/labeling.py | Rounds currently show item-oriented work; no decision-report draft/submit actions |
| Write route | labeling.py: LabelingMixin.labeling_act | Existing human_id and attest are caller assertions, not verified identity |
| Sharing | W/_host/live/share.py | Non-owner shared users currently have read-only access; participant responses need a narrow permission |
| Form prototype | blueprints/Project-Ladder/work/b15_theme_labeling/s03-agent-role/decision-report | Working local draft/save/export interaction with synthetic examples; no production persistence or receiving agent |
| Slides | blueprints/Project-Ladder/work/b15_theme_labeling/s03-agent-role/delivery/deck, version 12 | Design communication, not implementation evidence; versions 1 to 11 are in blueprints/Project-Ladder/work/b15_theme_labeling/_archive/20261031/slides-v1-v11 |

Targeted baseline tests and review evidence are recorded in REVIEW.md. Production readiness cannot be inferred from this table.

## 5. Architecture and ownership

Use one coordinator with two domain agents: the Meaning Loop Agent (Steps 2 to 4) and the Execution & Audit Agent (Step 5). Slide deck version 11 called the Meaning Loop Agent the Alignment Agent, a name some version 12 Workbench screens still show; both name the same human-facing responsibility. Internal functions start as tools or deterministic services, not a swarm of separate autonomous agents.

### Meaning Loop Agent

Read: authorized human sources, prior decisions, Train items and predictions, round reports, the Train or Test cases a round report names (with their context and reference provenance), the current approved meaning and open issues. No confirmation content.

Tools:

- Source collector: record ideas, notes, comments, conversations and source locations.
- Corpus explorer: retrieve, compare and sample Train cases; open the Train or Test cases a round report names.
- Issue organizer: group boundaries, missing context, apparent contradictions, suspected reference-label errors and uncertain cases.
- Report composer: create neutral alternatives with exact candidate rule patches when possible.
- Decision integrator: reconcile submitted choices with existing meaning and approval scope.
- Consistency checker: distinguish human inconsistency from different context or incorrect agent summarization.
- Impact checker: identify rules, examples, predictions and downstream results affected by a meaning change, across Train and Test.

Write: candidate reports, issue records and proposed rule patches through engine tools. Human semantic approvals are recorded only through the approved human action route. The agent never fabricates an attestation. Rules and examples it proposes carry no Test text: a rule decided from a Test case is stated in general terms, and the Test evidence stays in the decision record by reference.

### Execution & Audit Agent

Read: a particular approved meaning snapshot, the initial expression, Train references and predictions, and model configurations. Its auditor context also reads Test predictions, references and case-level errors. Its expression rewriting step (the deck's expression refiner) reads Train evidence and Test aggregates only; it never receives Test content, case-level errors or examples. The two contexts stay separate, and neither reads confirmation content.

Tools:

- Expression writer: reorganize instructions, examples, decision steps and output format, from Train evidence only; examples are Train items.
- Meaning-fidelity checker: detect omitted conditions, changed precedence and altered exceptions.
- Executor runner: call fixed-weight models on Train and Test with the current expression and the assigned item view.
- Scorer: calculate quality and coverage by model and partition against references through the permitted role.
- Failure diagnoser: classify each error hypothesis as expression issue, rule gap or conflict, suspected reference-label error, executor limit or missing context.
- Candidate selector: choose within predefined quality, coverage and resource rules, using Train evidence plus Test aggregates.
- Round reporter: write the round report and its route (CONTRACTS section 7).

Write: expression candidates, experiment requests, selection records and round reports. No semantic edits, human approval records or reference-label rewrites. A suspected reference-label error is a hypothesis in the round report, never a correction.

### Shared deterministic services

Versioned storage, access checks, decision report and round report validation, transactions, model adapters, scoring, queue recovery and Workbench rendering belong in code. Prompts guide reasoning; they do not enforce access control or durable writes.

The Workbench is the human surface. Engine modules remain independent of server imports. Do not add a new top-level workbench or competing application shell.

## 6. End-to-end workflow

| Step | Input | Work | Output / exit condition |
|---|---|---|---|
| 0. Itemize | Source corpus and optional legacy labels | Define item unit/context; retain lineage and original annotations; validate items; assign Train and Test roles by source group, keeping related sources together | Versioned item manifest, split manifest (Train/Test counts and source-group assignments), rejected-item list |
| 1. Frame the task | Human idea, prepared Train items, intended use | Define target construct, label schema, semantic authority, uncertainty and acceptance policy | Approved task frame, provisional starting guideline, open questions |
| 2. Investigate | Train evidence, round reports with Train or Test issues, sources, earlier judgments | Investigate related cases, earlier decisions and original context; retrieve contrasts; include random coverage; group consequential questions; prepare a decision report | Versioned decision report containing evidence-backed cards, or a recorded reason that no human decision is needed |
| 3. Collect preferences | Published Workbench report | Human confirms, clarifies, revises, selects, rejects, comments, defers or supplies a custom answer on Workbench decision cards; may save and return later | Durable, scoped, source-linked feedback events |
| 4. Update and check | Submitted feedback and current meaning | Reconcile with earlier decisions; apply exact confirmed changes; review reinterpretations; recheck affected Train and Test items and queue their labels for review | Compatible approved meaning and reference versions for Step 5, plus unresolved questions |
| 5. Execute, evaluate and analyze errors | Approved meaning and references | Rewrite expression from Train evidence only; call fixed-weight executors on Train and Test; evaluate by partition and model; analyze errors | One round report per round, routed to continue in Step 5, reopen the Meaning Loop, proceed to Step 6 or stop |
| 6. Freeze and check release readiness | Selected candidate, its round report routed to Step 6, acceptance specification | Freeze meaning/expression/runtime/reference versions; check version compatibility, issue dispositions, quality/coverage criteria, executor suitability, cost and audit policy; run the fresh independent confirmation set only when authorized | Approved handoff with recorded authority and a bounded claim; a failed gate returns to the responsible loop or holds release |
| 7. Label at scale and audit | Qualified handoff and target corpus | Shard, resume, validate outputs, route uncertain items, sample audits, reconcile dispositions | Audited labeled data with lineage and unresolved limitations |

Meaning cycles repeat 2 → 3 → 4 → 2. Step 5 staging rounds repeat while the remaining issues are expression-only. Every round writes a round report with its stop or continue reason, and the report routes the work: continue in Step 5; reopen the Meaning Loop for rule, preference or reference-label questions (the report goes to the whole Meaning Loop Agent, Step 2 investigates first, never straight to a human); proceed to Step 6 when the declared criteria are met; or stop when a budget is exhausted or no candidate can meet the floors. Step 4 returns compatible guideline and reference versions to Step 5 for a new round; a changed standard is never released because an earlier version passed. Scaling can reopen meaning through a new version; it never changes the frozen rule midway through a batch.

## 7. Human decision-report workflow

Each report is a small batch selected for expected decision value and reading burden, not a fixed number of cards. When a round report reopens the Meaning Loop, Step 2 first investigates related cases, earlier decisions and original context; the cards then ask about newly exposed boundaries, exceptions and conflicts, not only whether a model prediction should replace a label.

1. Bind a report to the task frame, meaning version, reference version, corpus and split versions, and the round reports it answers.
2. For each card, state one question, why it matters, the current rule, source evidence, candidate alternatives, affected scope and any dependencies; a card raised by an audit issue also names its origin partition (Train or Test).
3. Present no preselected option. Include a custom alternative, comments and defer.
4. Save drafts on the server with revision checks. Browser storage can recover a draft but is not the canonical record.
5. Submit explicit answered decisions; keep unanswered or deferred cards open. Return a durable receipt even if the agent worker is offline.
6. Record the exact choice, visible rule patch, comment, source links, actor evidence, report revision and timestamp.
7. If an option already showed the exact rule change and scope, explicitly submitting that selection is approval for that exact change, subject to conflict checks. Do not ask for a redundant second confirmation.
8. If a custom answer or qualifying comment requires interpretation, keep the person's original words and return the proposed interpretation for confirmation.
9. A newer answer does not silently overwrite an earlier answer. Show the conflicting scope and ask whether the person is revising, adding an exception or distinguishing contexts.
10. Build the next report from remaining issues, new round reports and newly found Train evidence. Do not ask already-settled questions without a reason; earlier decisions stay visible.

Forms can also collect diagnostic preferences: what constitutes a hard case, what evidence is insufficient, when an executor should abstain, and what should be reviewed. The substantive label and those diagnostics remain separate fields.

## 8. Version strategy

- Corpus snapshot: cNN plus date and source location.
- Split manifest: vNN, with Train/Test counts and source-group assignments.
- Task frame: fNN.
- Meaning snapshot: mNN, with parent and explicit approved changes.
- Reference subset: lNN (Labels, the deck's own letter, slides 19 and 22; rNN stays a Run), bound to a meaning version and approval events.
- Expression: eNN, bound to mNN and a development record.
- Report: stable report_id plus report_revision and base versions.
- Draft: per-report, per-author revision.
- Submission: immutable id and sequence, linked to the exact draft revision.
- Execution configuration: xNN, including model identity, runtime and decoding settings.
- Round report: one per Step 5 round (round-NN), binding the meaning mNN, expression eNN, reference labels lNN, execution xNN, corpus and split versions it ran on.
- Handoff: hNN, binding all qualified components.

Versions are monotonic logical identifiers, not content fingerprints. Model providers' ordinary model names/versions can be recorded; do not invent local hashes.

A semantic change creates mNN+1 and triggers dependency invalidation. Wording-only changes create eNN+1 under the same mNN. A reference-label correction creates lNN+1. A changed diagnostic definition is semantic if it changes task decisions, review routing or acceptance. Round reports keep expression-only gains under unchanged references apart from gains that follow reference-label corrections or semantic changes.

## 9. Rollout in reviewable milestones

| Milestone | Demonstration required | What it does not claim |
|---|---|---|
| M0. Design and baseline | Contracts, source audit, task assignments and runnable acceptance plan | Production implementation |
| M1. Workbench vertical slice | Publish a synthetic report, save across reload, submit once, inspect durable record, show next-step state | Real corpus search or live model reasoning |
| M2. Meaning Loop | Real authorized sources and Train evidence → investigated cards → human decisions → versioned meaning and reviewed references | Executor portability |
| M3. Step 5 staging loop | Fixed-weight calls on Train and Test, Train-only rewrites, selection with Test aggregates, round reports with correct routes | Generalization to unseen data |
| M4. Release and scale | Frozen candidate, release readiness check, confirmation run only when authorized, resumable labeling and audit | Unlimited transfer to unseen tasks or models |
| M5. Research evaluation | Preregistered comparisons, time/quality measurements and transfer/ablation analyses | Benefits without measurements |

M1 is the first implementation target. It must be served inside the meaning Task's Preferences view on the focus page (labeling_focus.py; b15 s13 maps Step 3 to it, s58 C3 draws it: one turn's cards as a /haipipe-interaction collect Run, answered only in the meaning Task), not merely linked as an external HTML demo. The legacy Rounds view of the Labeling workbench stays readable for item calibration jobs (decided 2026-11-01, when the workbench pages were redesigned from the slide deck).

## 10. Parallel work and integration order

Use at most three implementation agents alongside the coordinator. Assign file ownership before each wave.

- Foundation: contract owner first; reviewer freezes the interface version.
- Parallel foundation consumers: split/access service, durable store, and UI renderer against fixtures.
- Integration: the coordinator or one designated integrator alone edits labeling.py and shared action dispatch.
- Meaning: source/explorer work can proceed alongside report composition once the access API is stable.
- Step 5: executor adapter, staging scorer and round report writer can proceed in parallel against frozen contracts.
- Final release: migration, end-to-end acceptance and research ticket preparation follow integration.

Every work package has a stable ID, dependencies, inputs, file scope, tests, negative tests and review gate in WORK-PACKAGES.md. A successful unit test is not a substitute for clicking the actual Workbench.

## 11. Compatibility and migration

Introduce an explicit decision-report mode for new jobs, proposed as meaning_mode: decision_reports_v1. Keep existing item-calibration jobs readable. Do not reinterpret historical item judgments or convert old prototype exports from rule_preference_only into exact-rule approval.

Keep existing H/L/N schemas as legacy job schemas. New jobs use their own declared label schemas; this project is not universally a three-class task. NONE as a substantive label, unknown evidence, abstention and deferred human decisions must be distinct.

Map old development data to Train only when its exposure history is known. Do not silently split an already viewed pool and call the remainder an unexposed Test or a fresh confirmation set. Introduce selection with Train evidence plus Test aggregates explicitly; legacy test-based selection results remain historical exploratory results.

Current meaning revision restrictions, first-round-only implementation and unimplemented later gate services require adapters and new capabilities. A missing implementation must show an honest unavailable state. Do not generate successful receipts to satisfy a presenter.

Legacy hash fields may be read for historical compatibility if necessary, but new contracts do not require or generate hashes. Broad cleanup of other tasks' historical records is outside scope.

## 12. Product and deployment boundaries

Initial milestone uses synthetic content and a trusted local operator. Existing caller attestation is labeled as such. A shared multi-user deployment needs an authenticated principal, a narrow permission to respond to an assigned labeling job, and tests proving other jobs and write operations remain inaccessible.

Never make a participant a SPACE owner merely so they can submit a form. Do not widen the existing share door's global permissions. Runtime human responses and corpus content belong to private job storage, never the public Tools repository.

Use the configured host, origin and existing workbench routes. No ad-hoc server port or public tunnel. Server edits require an authorized restart and verification of the actual served behavior.

## 13. Completion criteria

The complete system is accepted only when:

- Both entry cases reach the same governed downstream workflow.
- A person completes a Workbench report asynchronously and durable integration applies each approved change once, despite retried processing.
- Meaning changes, expression changes and reference approvals have distinct provenance.
- Train, Test and confirmation access boundaries pass direct, indirect and negative tests; no Test content reaches expression rewriting.
- Model calls, parsing failures, retries, coverage and runtime are accounted for.
- Every Step 5 round writes a round report whose route matches its findings.
- A versioned candidate can pass its release readiness check, resume at scale and be audited without silent semantic drift.
- The coordinator reviews code, behavior, test evidence and claim wording.
- Real data/model Runs occur only after the user authorizes their tickets.

Engineering completion and research success are different. The system can be correctly implemented even if an experiment finds that a weaker model remains inadequate. Such a result is retained, not hidden by changing the reference standard.
