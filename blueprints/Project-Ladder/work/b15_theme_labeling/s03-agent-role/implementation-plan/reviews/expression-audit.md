# Expression Loop, Evaluation and Scale: Implementation Planning Memo

Status: read-only code audit and proposed implementation plan. No model calls, benchmarks, production edits, server changes, or skill changes were performed.

The user's latest design is authoritative: models keep fixed weights; both learning and evaluation items may be labeled; only learning item content and item-level errors inform guideline development; validation feedback can select a candidate; final test is reserved for independent assessment. Only the Meaning Agent asks humans for semantic decisions. The Expression Agent calls executors as tools and returns unresolved meaning issues to that agent.

## 1. Verified implementation inventory

All paths below are relative to <Tools>/.

| Current artifact | Verified behavior | Reuse or gap |
| --- | --- | --- |
| plugins/haipipe-toolkit/skills/2_theme/labeling/engine/label.py | lm_labeler() loads a versioned guideline, calls independent transports, returns label, optional region, confidence, reason, elapsed time and parser status. Engines include claude_sdk, codex, openai_api, openrouter and ollama. | Reuse transport adapters and strict label parsing, not the current wrapper as a final-test runner. |
| engine/label.py::_canonical_v2_items | Resolves submitted ids through canonical eligible development items and rejects substituted text or sealed ids. | Preserve this development fence. Add distinct, capability-bound evaluation access rather than weakening it. |
| engine/label.py::run_engine | Asynchronous semaphore concurrency and per-item elapsed times; gathers whole batch and writes results at the end. | No verified durable incremental resume, batch wall-clock telemetry, token accounting, hardware telemetry or immutable attempt journal. |
| engine/label.py::_make_parser | Strict JSON label and optional region membership; parser failures remain failures. | Existing confidence and reason fields are largely passed through without strong validation. Add typed diagnostic validation and unknown state. |
| engine/kappa.py::score_vs_gold, per_label_prf | Configurable categorical/ordinal metrics and explicit all-item failure accounting. | Reuse deterministic metric primitives. No verified complete independent evaluation registry, clustered intervals, coverage-constrained selection or weighted audit runner. |
| engine/converge.py::assess | Plateau is diagnostic, never a stop gate; below-floor plateau does not count as convergence. | Keep this distinction. Its historical anchor/heldout naming must map explicitly onto learning/validation, not final test. |
| engine/corpus_preparation.py::reserve | Whole split_group_id groups reserved before development exposure; custody artifacts remain at source owner. | Useful starting point for group-disjoint split construction. Current output has only development/sealed partitions, not separate learning/validation/final-test partitions. |
| engine/fence_source.py::draw_sealed/build | Legacy item-level reservation, development-only corpus and protected sealed manifest. | Do not use as the new default: item-level splitting may separate related conversation items. |
| engine/gates.py::require_gate | Explicitly implements only G0. | Later qualification/production gates are not made real merely by declaring them. |
| engine/run_catalog.py::plan_runs | Enumerates operation tickets including executor-predict, executor-score/select, scan and audit. | Planning inventory, not evidence those implementations exist. |
| 3_quality/haipipe-labeling-test/SKILL.md | test-reserve and test-gold-lock explicitly marked not built. | Missing independent test custody/release and blind-gold workflow. |
| 3_quality/haipipe-labeling-evaluation/SKILL.md | executor-predict, executor-score and executor-select explicitly marked not built. | Need complete implementation. |
| 4_delivery/haipipe-labeling-scan/SKILL.md | scan-preflight, scan-shard, risk-route, human-review, reconcile marked not built. | Need complete implementation. |
| 3_quality/haipipe-labeling-audit/SKILL.md | audit-sample, audit-human-gold, audit-analyze marked not built. | Need complete implementation. |

The existing test_lm_labeler.py already tests context inclusion, missing-key refusal, rejection of sealed ids, and invalid region parsing through fake transports. This is an appropriate regression foundation. It does not prove real model quality or protected final-test execution.

## 2. Resolve migration contradictions before connecting new runners

1. The current evaluation/scanning contract selects an executor on the sealed test after registry freeze. The new method should select guideline expression and deployment candidate on validation, then assess the preregistered selection on final test. Rename stage semantics explicitly. A final-test comparison across a predeclared model panel may be reported, but post-hoc choosing the best performer is not an independent confirmation of a prior selection.
2. The current preparation and fence implementation computes content-derived identifiers and checks using hashing. This conflicts with the user's explicit no-hashes instruction. Assign one migration owner for corpus_preparation.py, fence_source.py, gates/job readers and their tests. New interfaces must use source/item ids, split_group_id, explicit version/date, immutable manifests, event sequence and direct value comparisons where needed. Do not execute the old writer as part of a new workflow, silently weaken validation, or rewrite historical generated artifacts by hand.
3. H/L/N and seven diagnostic regions are currently emphasized in some skills. Executor output schemas should read the task's approved label vocabulary. Do not force binary or ordinal tasks into H/L/N. Keep uncertainty and abstention outside ordinary task-label values.
4. Fixed weights does not mean no optimization. The guideline, wrapper, routing rules and runtime configuration all require versioning and controlled evaluation.
5. Existing source-level custody hides the test from development. The user's phrase that the agent “sees both” should be implemented as separate tool executions and contexts: the orchestrator sees run status and aggregate feedback, the evaluation executor sees item content, and the guideline writer does not receive those item-level evaluation details.

These are explicit plan decisions requiring updates to the appropriate skills before their new execution flows can be advertised as supported. Skill changes require a fresh-agent realistic-task test under repository rules.

## 3. Versioned artifacts and interfaces

Use the existing Page/labeling owner and typed Run layout rather than a second standalone experiment tree. Proposed subpaths below are provisional until the shared contract owner reconciles them with ref-assets.md and the Workbench storage roster.

- MeaningVersion: meaning_id, parent_meaning_id, schema_version, rule_ids and revisions, human authority, approved decision ids, unresolved scope, created_at, status.
- ExpressionVersion: expression_id, meaning_id, parent_expression_id, exact rendered guideline, output schema version, writer rationale, learning evidence ids, approved reference version, status.
- ReferenceSet: reference_version, meaning_id, split, item_id, human label or allowed set, review provenance, reviewer authority, decision id, resolved/ambiguous/insufficient-evidence status. Model predictions cannot enter this set as human gold.
- ExecutorSpec: executor_id, provider, model identifier/version, tokenizer/chat-template version where available, precision/quantization, serving engine/version, decoding settings, context limits, output limit, hardware profile, dependencies, frozen-weight declaration.
- EvaluationRegistry: registry_id, target meaning/expression versions, split version, candidate pool, baseline, predeclared model-family holdouts, metric definitions, floors, noninferiority margins, repeats, validation query budget, exclusion rules, abstention handling, selection rule, resource limits, final-test release conditions.
- PredictionAttempt: attempt_id, logical run_id, item_id, split authorization, meaning/expression/executor versions, attempt_number, start/end times, label nullable, status, reason code, uncertainty and difficulty diagnostics, token counts nullable, elapsed seconds, error category. No raw private provider error response or secrets.
- Scorecard: registry and prediction references, denominators, resolved-reference count, exclusions with reasons, failures, coverage, quality metrics with intervals, diagnostic strata, runtime metrics, limits, qualification status.
- EscalationPacket: issue_id, meaning/expression versions, learning examples only, implicated rules, observed mismatch, rewrite attempts, alternative explanations, severity/scope, requested semantic question, status. Validation failure may trigger a learning investigation but must not attach hidden validation examples.
- ReleaseBundle: accepted meaning and expression versions, approved reference version, selected executor/runtime, final qualification record, production policy and audit design, human approval records, invalidation state.

Logical proposed tool contracts:

1. rewrite_expression(meaning_id, parent_expression_id, learning_feedback_ref) -> candidate expression.
2. check_meaning_fidelity(candidate_expression_id, meaning_id) -> evidence-based pass/provisional/fail with rule mapping. A language-model check is supporting evidence, not sole authority.
3. predict_learning(expression_id, executor_id, learning_item_ids, run_id) -> durable prediction attempts.
4. evaluate_validation(expression_id, executor_id, registry_id) -> aggregate scorecard only for developer context; detailed predictions remain in evaluator custody.
5. diagnose_learning_errors(prediction_ref, approved_learning_reference_ref) -> typed causes and candidate remedies.
6. select_candidate(registry_id, scorecard_refs) -> selected candidate or no-qualified-candidate; deterministic decision.
7. escalate_meaning(issue_packet_ref) -> queued Meaning Agent task. It does not contact the human directly or update meaning.
8. qualify_final_test(frozen_registry_id, selected_candidate_id, custodian_release_id) -> independent pass/fail/inconclusive.

Every tool rejects mismatched meaning/reference/schema versions and unknown status. Missing versions or metrics mean unavailable, not zero or success.

## 4. Split and access design

No default percentage should be treated as universal. Choose sample sizes from population coverage, rare-label needs, intended confidence precision and feasible human review; protect grouped independence before considering counts.

| Role or call | Learning contents | Learning references | Validation contents | Validation references | Final-test contents/references |
| --- | --- | --- | --- | --- | --- |
| Meaning/report writer | Yes | Approved scope only | No | No | No |
| Expression writer/diagnoser | Yes | Approved scope only | No | No | No |
| Learning executor | Yes | No | No | No | No |
| Validation executor | No need | No | Yes, authorized batch | No | No |
| Independent validation scorer | Prediction ids | No need | Only if required by authorized scoring | Yes | No |
| Orchestrator/selector | Allowed learning context | Allowed learning context | Aggregate status only | Aggregate scores only | Release status and final aggregate report only |
| Final-test executor | No need | No | No | No | Final item content only after freeze/release; gold hidden |
| Final scorer/custodian | As authorized | As authorized | As authorized | As authorized | Protected gold and prediction joins; no content return to developers |

Implementation requirements:

- Split at the conversation/source/duplicate-family group level before retrieval, embedding, form generation or model-assisted error analysis.
- Exact duplicate and near-duplicate family discovery belongs to the source custodian before partitioning. Preserve group ids and the declared grouping method. Do not reopen sealed content through development deduplication.
- A rule writer must not share the same model session/context with evaluation execution. Tool-result redaction alone is insufficient if hidden items are still in the writer's memory.
- Validation metrics are development feedback. Repeated selection may overfit even without item examples. Freeze query budget/stopping rules, record every query and candidate, and avoid adaptive per-item slices. Coarse predeclared strata are permissible; suppress tiny groups that expose an individual answer.
- Reserve final test independently. Freeze candidate and registry before test release. If test reveals a defect, record the failed assessment and reopen development; that test cannot be reused as untouched confirmation for the repaired version.
- Ambiguous or unanswerable references remain visible. Separate the estimand for resolved labels from abstention/review behavior on unresolved items.
- Do not make a UI promise of strict blindness until server routes, tool contexts, logs, reports, search and filesystem paths all enforce it.

## 5. Expression loop state machine

States: waiting_for_approved_meaning -> ready -> candidate_drafted -> fidelity_checked -> learning_scored -> validation_scored -> selected / revise / meaning_escalated / executor_limited / budget_exhausted.

For each approved meaning version:

1. Resolve a frozen input bundle: rules, baseline expression, approved learning reference labels, diagnostic definitions and unresolved scope.
2. Generate a candidate expression using learning evidence only. Candidate modifications may reorder rules, make precedence explicit, tighten wording, reduce redundant tokens or clarify output instructions. They cannot add a new exception or alter a label definition.
3. Check all rule ids and conditions/exceptions against the meaning version; retain semantic-diff evidence.
4. Run the same declared learning items with designated cheap and strong executors, isolated contexts and fixed runtime. Include baseline expression.
5. Score against approved references. Classify failures into expression ambiguity, semantic gap/conflict, questionable reference, missing context, output/parser issue, executor limitation or infrastructure issue.
6. Improve expression on learning diagnoses. Semantic gaps, conflicting human references and new intended exceptions return as an EscalationPacket to Meaning.
7. For eligible candidates, use aggregate validation quality/coverage/resource metrics to select and stop. Do not send item-level validation diagnoses back to the writer.
8. Freeze the selected expression and executor configuration; then run independent qualification.

If the cheap model fails a clear rule that a stronger model executes reliably, do not keep rewriting indefinitely or weaken the rule to inflate its score. Mark the cheap executor unsupported for that scope, try a separately registered runtime/model, or define a transparent review route. If the rule itself is underdetermined, return to Meaning. Both diagnoses can coexist.

Human input is asynchronous: unaffected optimization can continue on the approved meaning version. Candidate results based on a pending semantic decision are provisional and cannot qualify. When meaning changes, dependency-based invalidation marks affected candidates, references, scorecards and release claims stale; an explicit verifier must decide whether unaffected results can be retained.

## 6. Quality, speed, cost and model transfer

### Quality

Choose primary metrics by the actual label type: accuracy and macro/per-class precision-recall-F1 for nominal categories; declared ordinal agreement and error metrics for ordered labels. Keep confusion matrices, minority-class recall, failures and denominators visible. Report performance on all eligible resolved reference items, not just successfully parsed predictions.

Report answer coverage, abstention rate, review rate and unresolved-reference rate alongside quality. A model cannot win by returning only easy cases. Compare selective quality at matched coverage or under a preregistered coverage floor. Distinguish confidence from calibrated correctness; human difficulty, model uncertainty and cross-model disagreement are separate variables.

Use paired comparisons on the same items and cluster-aware intervals at split_group_id. Repeated model executions estimate stochastic instability separately from uncertainty due to the sampled corpus. Predeclare whether uncertain human references are excluded, set-valued, or adjudicated; do not silently select whichever treatment makes a model look better.

### Selection objective

Use constrained selection, not gap minimization alone:

- Every intended deployment executor must meet absolute quality and coverage floors and protected-class requirements.
- The strong reference executor must not fall beyond the declared noninferiority margin relative to its baseline expression.
- Improving the weakest supported executor is a primary development target.
- Among qualifying candidates, prefer the fastest or cheapest route under the declared objective; show the quality/throughput Pareto frontier.
- A small cheap-versus-strong gap is useful only when both have acceptable quality. Two equally poor models do not establish portability.
- For a claim that a cheap model is close enough, the paired confidence interval must support the preregistered margin. Overlapping intervals or a nonsignificant difference alone is not a noninferiority result.

Thresholds and margins are task decisions, not invented default performance targets.

### Proposed local hardware benchmark

The user's proposed profile is one RTX 4090 with 24 GB memory and a candidate around 8B parameters. This memo makes no fit, speed or quality claim. Verify actual hardware, installed model, serving runtime and feasible context before a real run.

Register model identity, parameter description, precision/quantization, serving engine, tokenizer, prompt/output lengths, context window, concurrency, batch size, prefix caching, warmup, hardware/software versions and competing load.

Measure end-to-end batch wall time, completed valid labels per second, all attempted items per second, p50/p95 item latency, retries, parser failures, peak accelerator memory, token counts when available, and manual-review burden. Separate cold-start from warmed throughput and distinguish cache hits. Retry and repair overhead count toward end-to-end cost.

Hold runtime fixed while comparing guideline wording. Hold expression fixed when tuning batching/concurrency/runtime. Quantized and unquantized variants are separate registered executor configurations. Fixed-weight deployment is allowed, but configuration changes do not inherit an earlier qualification automatically.

Keep development cost, production cost and human effort separate. Report the volume at which extra development cost might be amortized using observed inputs, not invented cost savings. For local hardware, GPU-seconds and wall time are useful even when monetary cost is unavailable; do not call local inference free.

### Transfer and evaluation study

- Development model pool: one strong facilitator/reference executor and intended low-cost executors.
- Transfer pool: predeclared model families or versions unseen during expression optimization.
- Freeze one shared expression before transfer scoring to test a portable guideline. If model-specific wrappers are used, report them as another condition.
- Compare seed guideline, meaning-refined baseline, and meaning-plus-expression version under matched meaning/reference scope. A meaning change is not a pure expression comparison.
- Suggested ablations: no expression refinement; single-executor optimization; no targeted hard-case retrieval while retaining random coverage; chat-only versus forms-plus-optional-chat human interaction. The interaction comparison needs its own order/carryover and human-effort design.
- Research outcomes: quality, human minutes, decisions resolved per human response, coverage, throughput, total cost, consistency, unseen-model transfer. Do not infer human effort savings solely from fewer clicks.

## 7. Production and audit

Freeze a release bundle before any large-scale labeling. Preflight is a real run on an authorized small batch, not a successful dry-run claim. New runtime/model/expression, risk threshold, or meaning version creates an explicitly new episode.

Production writer must use append-only attempts and idempotent item/run identity, bounded retries and durable checkpoints. After a crash, resume uncompleted attempts without duplicating accepted terminal records. Keep input version, model, expression, decision source, diagnostic status and acceptance provenance on every item.

Risk routing combines declared uncertainty, missing context, parse failures, model disagreement, novelty and coverage sampling; agreement alone does not establish correctness. Only Meaning Agent seeks semantic decisions. Item-specific human correction can override a prediction without changing a rule. A generalized rule defect opens a Meaning issue and invalidates relevant downstream claims.

Audit design is frozen before auditors see predictions. Use probability sampling including apparently easy/low-risk items, retain inclusion probabilities, and weight estimates correctly. A targeted review queue does not estimate population error. Independent human audit references remain blind to production labels. Audit results route to pass, repair, rescan, semantic reopen, or an explicitly accepted bounded limitation.

The completed corpus contains exactly one terminal disposition per in-scope item. Unresolved is distinct from a negative/no-evidence label. A final accepted corpus is materialized only after the required audit and explicit handling of limitations.

## 8. Dependency-ordered work packages

Suggested file names are proposals, not claims of existing modules. One owner per module; integration owner changes shared exports/gates after review.

| Package | Owner responsibility | Inputs/dependencies | Candidate files | Done when |
| --- | --- | --- | --- | --- |
| E00: contract reconciliation | Contract lead | Meaning/report schemas; latest user design | labeling building/scanning/workflow skills, ref-assets, ref-space-mapping, engine/run_catalog.py | Learning/validation/final-test semantics and operation ownership agree; legacy readers documented; no obsolete test-selection promise remains. |
| E01: split custody | Data-boundary agent | E00 and Step 0 item schema | engine/corpus_preparation.py, fence_source.py, job.py, new split_access.py, related tests | Group-disjoint three-way manifest; protected accesses refused; no new content hashes; no real private data required for tests. |
| E02: executor attempt layer | Runtime agent | E00, E01 | engine/label.py adapters, new executor_runtime.py and executor_schema.py | Fake adapters prove isolated inputs, strict outputs, durable attempts, retries, timeout, resume, telemetry and fixed config identity. |
| E03: scoring and registry | Evaluation agent | E00, E01, E02 | engine/kappa.py reuse, new evaluation_registry.py, scorecards.py, selection.py | Exact denominator accounting, intervals, quality/coverage floors, deterministic tie rule, aggregate-only developer result. |
| E04: expression orchestration | Expression agent | Approved meaning/reference contract, E02/E03 | new expression_loop.py, expression_versions.py, meaning_fidelity.py | Tool sequence uses learning-only diagnoses; semantic escalations queue to Meaning; budget/stop/failure states work; fixed model weights. |
| E05: final qualification | Evaluation agent | E03/E04 frozen candidates | new final_qualification.py, gate integration | Registry freeze precedes release; gold hidden from prediction; failed test does not trigger automatic same-test retuning. |
| E06: production | Production agent | E05 and release bundle | new production.py, risk_routes.py, reconciliation.py | Crash/resume and exactly-one terminal disposition verified; stale versions fail closed; uncertain cases retain status. |
| E07: audit | Audit agent | E06, declared human session interface | new audit.py and acceptance.py | Probability weights, blind judgments, repair lineage and final acceptance gates verified on fixtures. |
| E08: Workbench quality views | UI owner | E03–E07 read models | existing workbench-task-labeling presenter and declared quality/delivery views | Scores show denominators and pending/stale states; no protected item leakage into developer views; real route responses verified. |
| E09: hardware experiment ticket | Experiment owner, execution by user | E02–E05, real model/hardware inventory | project-owned Run ticket/config, never private data in public Tools | Dry-run plan names workload, models, hardware, metrics, budgets and output locations; user has not been falsely told a benchmark ran. |
| E10: research comparison ticket | Study owner | E09 plus human protocol and untouched references | study-owned evaluation plan and Run tickets | Baselines, ablations, transfer models and decision criteria preregistered; no unasked compute or human experiment launched. |

Do not run E04 before the split/custody boundary is enforced. Do not make E08 UI labels imply production capabilities before E05–E07 exist.

## 9. Acceptance test matrix

Tests should use synthetic fixtures and fake executors by default. Real model/hardware runs are separately authorized execution tickets.

1. Same conversation and duplicate-family members cannot land in different partitions; seed/version reproduce the manifest without content hashes.
2. Development retrieval, embedding and report construction reject validation/final-test ids, aliases and content substitutions.
3. Validation executor receives only guideline, target item/context and output contract; it never receives reference labels, facilitator chat, examples from protected gold or previous evaluator diagnoses.
4. Validation scorer returns only approved aggregate fields to the writer; hidden text cannot escape through logs, tracebacks, export files, small adaptive slices or tool exception messages.
5. Parser rejects out-of-vocabulary labels, invalid difficulty/status/reason types and malformed output. Unknown uncertainty stays unknown; it is not silently confidence 0 or 1.
6. Scorecard includes missing, timeout, parser-error and abstained items in the correct denominators; a model cannot qualify through excluded hard items.
7. A mocked model with equal but bad quality fails the absolute floor even when cross-model gap is zero.
8. A fast candidate below quality or coverage floor is not selected. A candidate outside the strong-model noninferiority margin is not accepted as a general improvement.
9. Candidate scoring on learning data may produce item-level diagnoses; scoring on validation must not. All candidate/validation queries are logged.
10. An expression that changes a rule's exception or precedence is blocked and escalated, even if learning accuracy rises.
11. A new meaning/reference/schema version invalidates dependent scores and releases. A late result from an older expression remains historical and cannot overwrite current status.
12. Pending human semantics do not block unrelated work, but provisional candidates cannot qualify as approved.
13. Final-test release refuses an unfrozen registry, missing blind gold, changed selected candidate or unauthorized executor. Reusing a revealed final test must be labeled reused, not untouched.
14. Two simultaneous attempt writes cannot duplicate the same item/run terminal record; a crash after provider response but before durable completion is represented as an uncertain attempt and handled explicitly.
15. Production resume does not re-run completed items; changing executor/runtime opens a new episode rather than patching the previous manifest.
16. Human review overrides one item's prediction without mutating the meaning rule; a semantic correction routes to Meaning.
17. Weighted audit fixture returns the expected population estimate under unequal sampling; low-risk items are eligible. Targeted risk-review results cannot masquerade as probability audit results.
18. Audit failure preserves prior results and creates a new repair/audit lineage. Final accepted-corpus materialization refuses an absent or invalid audit.
19. Telemetry distinguishes per-item service time, queued time and batch wall time; token counts unavailable from a provider remain null, not guessed.
20. Provider errors are sanitized; client-side model text cannot change authorization, source scope, or file paths.

Suggested baseline regression command after implementation changes:

    <workspace>/.venv/bin/python -m pytest plugins/haipipe-toolkit/skills/2_theme/labeling/engine/test_lm_labeler.py plugins/haipipe-toolkit/skills/2_theme/labeling/engine/test_stats.py plugins/haipipe-toolkit/skills/2_theme/labeling/engine/test_gates.py plugins/haipipe-toolkit/skills/2_theme/labeling/engine/test_corpus_preparation.py

Run it from Tools-SPACE with the workspace interpreter. This command is a proposed review check, not a claimed result in this memo. Add targeted new test files per package, then run the Workbench owner’s actual browser integration checks. Fresh-context skill validation is required after skill edits. The lead reviewer inspects code paths and data-flow evidence in addition to test output.

## 10. Lead-review gates and handoff expectations

Every implementing agent returns: exact files touched, current-source evidence used, schema/API changes, fake-executor test evidence, browser evidence where relevant, unresolved issues, migration impact, and confirmation that no production/model run occurred.

Lead review blocks integration if:

- an agent conflates declarations with implemented gates;
- protected item-level evaluation information enters guideline writing;
- a rule preference is treated as human gold for all propagated labels;
- final-test performance drives unrecorded revision or post-hoc selection;
- missing outcomes are dropped, or speed is reported without coverage/failure accounting;
- a capability depends on model confidence or agreement as proof of correctness;
- a new file duplicates another owner's authoritative artifact;
- current-scope work starts real model experiments or writes private data into public Tools.

Release acceptance is separate from research success. A fake-transport and UI pass means the system paths work; it does not establish cheap-model parity, hardware throughput, human-effort savings or final-corpus quality.
