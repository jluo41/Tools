# Evaluation protocol: meaning, transfer, quality and throughput

Version: 2  
Reconciled on 2026-11-01 to slide deck version 12 (Train and Test, Execution & Audit Agent, round report); version 1 was written against version 8.

Design only. No performance numbers in this document are measured results. Thresholds, model choices and data quantities are study configuration, not facts to invent during implementation.

## 1. Separate the claims

| Claim | Evidence required | What does not establish it |
|---|---|---|
| Meaning captures the user's conception | Judgments on a fresh independent confirmation set, clear rule provenance, human review and consistency checks | A fluent guideline, high model confidence or a Test score after Test findings shaped the meaning |
| Forms make interaction easier | Human time, completion, comprehension and correction burden at comparable quality | Fewer chat messages alone |
| Expression rewriting improves executors | Paired comparisons under fixed meaning, reference labels and model weights | Changing the label definitions or correcting reference labels along with wording |
| A shared guideline transfers across models | One frozen expression evaluated on several executors, including unused model families | Tuning separately for each model and reporting their best runs as shared transfer |
| A staging Test score estimates unseen data | No Test finding has guided an approved revision; otherwise a fresh independent confirmation set | A Test score after Test issues reached the Meaning Loop and changed rules or labels |
| Smaller models become useful | Absolute quality and coverage floors, acceptable stronger-model regression and operational throughput | A smaller gap caused by making the stronger model worse |
| The workflow scales | Measured end-to-end throughput, review burden, recovery and audit outcomes | Tokens per second without rejected items, retries or human work |
| The system is training-free | No weight updates in the declared system boundary | No fine-tuning of the executor while secretly training another task-specific component |

Training-free here means the task-specific workflow changes guidelines, examples, decisions and permitted runtime configuration; it does not update model weights. Pretrained models and retrieval embeddings can still be used, with their versions and roles disclosed. Existing pretrained capabilities are not themselves a contribution of this workflow.

## 2. Data partitions and visibility

Prepare items and correlated groups before development. The current design (slide deck version 12) has two partition roles, Train and Test; a separate validation split is not part of this version. A third set is needed only for claims about unseen data:

1. Train: content, labels, mistakes and cases are available for rule discovery and expression development. Train case-level evidence may go to the expression rewriting step and to the Meaning Loop.
2. Test (the staging check): labeled, scored and audited like Train. Its issues (suspected reference-label errors, rule gaps, conflicts) go to the Meaning Loop Agent in the round report and may reach human review. No raw Test content, case-level errors or examples enter the expression rewriting context, logs, memory or few-shot examples. Selection between expression candidates uses Train evidence plus Test aggregates.
3. Fresh independent confirmation set: outside all development and adjudication feedback, needed only for claims about unseen data, and run at Step 6 only when authorized. It never sits in agent-visible roots. No iteration against this set.

Once Test findings guide approved revisions, Test is development exposure for later versions: its score is not an unbiased estimate for unseen data. Record that exposure in the split manifest and in every claim that cites a Test score.

Production is new deployment data; it is not automatically an evaluation set. A confirmation set that any development or adjudication step has inspected is no longer fresh, regardless of its folder name. Previous experiments that selected models or wording on their test data may be reported honestly as exploratory; do not rename old data to claim independence.

Train and Test items are both labeled. Keeping Test out of expression rewriting is compatible with that: a dedicated execution context labels Test items under the current expression; the scorer compares them with Test reference judgments held in custody; the auditor analyzes Test errors at case level and reports issues in the round report. The expression rewriting step does not receive those item-level contents. Confirmation items are labeled only in their authorized confirmation run. An agent with unrestricted access to the entire filesystem and shared memory cannot be described as technically isolated merely because its prompt says not to look.

Split correlated conversations, authors, documents or duplicated source records as groups according to the task, so related sources stay in one partition. The preparation record states why those groups are appropriate. Do not split turns from one conversation across Train, Test and the confirmation set. Check exact and near-duplicate exposure without introducing content hashes. Preserve known prior exposure and grouping limitations.

Partition sizes depend on independent groups, class coverage and uncertainty of the planned comparison. Do not standardize the method around a particular 400/100 example. Determine sample needs before claiming equivalence or cost-quality improvements.

## 3. Reference construction and approval

Freeze a semantic version before constructing a scored reference release. Train judgments can develop meaning, and so can Test issues, but only through the Meaning Loop and its approval route. Confirmation adjudication applies the frozen meaning and produces labels, diagnostics, exclusions and reasons without sending case-specific details back to any development step.

For independent reference construction (the confirmation set, and any reference described as independent), collect the human's initial judgment under the frozen guideline before revealing the candidate prediction, confidence or executor identity. Store that initial judgment separately from later reconciliation. Model-assisted or legacy references may be useful, but their presentation mode is recorded and they are not silently called independent. This blinding requirement applies to evaluative judgments, not to all Meaning Loop decision cards, which intentionally discuss candidate interpretations. A Test reference correction reviewed after executor disagreement flagged the case is model-assisted; record it that way.

Keep at least four statuses distinct:

- Directly human-reviewed item judgment.
- Independently adjudicated judgment with recorded policy and reviewer evidence.
- Agent-inferred label under an approved guideline.
- Batch-accepted production label under an explicit audit policy.

The last two are not automatically gold references. A selected rule option approves the exact displayed rule scope, not every inferred item. The source of a legacy label may be uncertain; record it as evidence until the applicable acceptance process validates it.

If Test auditing finds a missing or contradictory rule or a suspected reference-label error, the round report carries it to the Meaning Loop Agent, which investigates before any human decision. If confirmation adjudication finds one, the custodian records it; acting on it, even through an aggregate issue that triggers new Train-side investigation, starts a new development cycle, and the set is no longer fresh for the revised version. Once the meaning changes, dependent references and executor results are stale. Re-adjudication creates a new reference release. Test cases whose findings guided approved revisions are development exposure for later versions. If any development step has seen confirmation cases or case-specific explanations, those cases cannot remain a fresh confirmation set. Choose a fresh set or transparently downgrade the claim.

Freeze the criteria for ambiguity, review effort, uncertainty reason and review routing along with meaning. Do not let each executor invent incompatible definitions of easy/hard. Human-perceived effort, model disagreement and missing context are different measurements. They may correlate, but the system must not conflate them.

## 4. Development and selection protocol

For each candidate, record:

- meaning_version, reference_version, expression_version, corpus/split_version;
- exact expression source, approved examples and rule coverage mapping;
- executor ID and explicit runtime settings;
- Train tool calls, Test aggregate queries and disclosed aggregates;
- generation/selection budgets, stop condition, error-hypothesis classes and the round report that covers the candidate.

Use Train errors to create candidate wording changes. Run semantic fidelity checks before execution. Evaluate all candidates with the same declared protocol on Train and Test, reported by model and partition. Test aggregates can guide selection, but repeated queries still create selection bias. Limit and record the expression rewriting step's queries; predeclare available strata, suppress small cells and do not allow interactive subgroup drilling until individual cases become identifiable. The auditor's case-level Test analysis goes to the round report, never back into rewriting.

Maintain a best-qualified candidate, not merely the newest candidate. Stop the Step 5 loop on a prespecified budget or qualifying plateau, and route an unresolved rule, preference or reference-label problem to the Meaning Loop. Every round records its stop or continue reason in its round report. If nothing qualifies, return no qualifying candidate with reasons. A system must be allowed to fail rather than automatically relaxing the target.

Confirmation execution is a separate authorized ticket at Step 6. Freeze the candidate, settings, metrics and thresholds before the scorer runs it. A failed confirmation is a result, not a request to tune on its examples. Subsequent development needs another fresh independent confirmation set for a new confirmatory claim.

The confirmation reference release is adjudicated and locked before candidate execution, using the blind-first protocol. Check the ordering and reveal transitions, not only a metadata field that says blind_first. The scorer later joins predictions to those frozen references; executors never receive the references.

## 5. Quality, coverage and model-gap criteria

Choose the task metric to match its label schema. For mutually exclusive categorical labels, report at least accuracy and macro-F1 with class-wise support and confusion information in custodian-visible outputs. For multilabel or ordinal tasks, define appropriate metrics before experimentation. Do not force all tasks into H/L/N or binary classification.

Report task quality together with:

- results by model and partition, with Train and Test reported separately;
- task coverage: fraction assigned a valid task label;
- abstention and human-review routing rates;
- invalid schema, timeout, missing response and failure rates;
- class-wise performance and uncertainty/difficulty strata where sufficiently supported;
- diagnostic quality against independently reviewed diagnostic criteria;
- overall denominator and excluded/unresolved reference counts.

Include failed and abstained items in a prespecified all-item measure, and report conditional quality among answered items separately. Otherwise a model can look excellent by answering only easy cases. Do not silently drop failed requests from timing or quality comparisons.

Let Q_m(g) be the prespecified quality score for executor m under expression g at fixed meaning. Candidate selection should consider the vector of quality, coverage and cost rather than a gap alone. A useful rule is:

1. Meet absolute quality and coverage floors for each required executor.
2. Improve or maximize the weakest executor's quality among feasible candidates.
3. Keep stronger-executor regression within a prespecified noninferiority margin.
4. Prefer smaller cross-model gaps and lower cost among similarly qualified candidates.

Formally, a gap can be reported as max_m Q_m(g) minus min_m Q_m(g), but it is not the sole objective. If both models fall to poor quality, a zero gap is failure. If the cheap model is useful yet still materially worse, report that tradeoff rather than calling it equivalent.

Use paired comparisons on the same evaluation items and group-aware uncertainty estimates. Report confidence intervals for model differences. A nonsignificant difference does not establish equivalence. Prespecify an acceptable margin, adequate precision and the relevant one-sided or two-sided decision rule. Separate sampling uncertainty from repeated-execution randomness; deterministic-looking settings do not justify treating repeated identical runs as independent datasets.

## 6. Throughput and resource measurements

The proposed local scenario is an 8-billion-parameter executor on one RTX 4090 with 24 GB memory. This is a target configuration to test, not a guarantee that a particular model/context/batch fits or performs well. Record the actual model, weight format, quantization, context length, runtime, driver, batch/concurrency settings and hardware.

Measure at least:

- valid labeled items per second and accepted items per minute;
- total wall time, warm-up time, p50/p95 item or batch latency;
- peak device memory, out-of-memory failures and retry counts;
- input/output tokens when available, paid API cost when applicable;
- human review minutes and agent-development cost;
- coverage and quality for the exact measured configuration.

Accepted items per minute must specify what acceptance means, whether human review is included and when audit results became available. Report a machine-only rate separately from end-to-end delivery rate. No made-up GPU hourly price or unverified API price is needed in implementation; pricing belongs to the actual execution record.

Run two controlled sweeps separately. First tune expression with runtime settings fixed. Then tune batching/concurrency/quantization with the chosen expression fixed. Quantization and changed context are new execution configurations requiring quality rechecking. Compare like-for-like workload distributions and report cold/warm conditions.

If the cheap executor cannot meet the quality floor, plausible outcomes include more human review, a stronger fallback or no deployment. Record the cost/coverage consequence. Do not redefine success after the fact merely to retain the cheapest model.

## 7. Study comparisons and ablations

Use the same task frame, source data access and reasonable budgets when comparing workflows. Record any unavoidable difference. Do not assume the old workflow is ineffective; measure where it costs time or fails.

| Condition | Meaning formation | Expression | Purpose |
|---|---|---|---|
| Conventional baseline | Human writes guideline and labels items | Initial human wording | Establish time, consistency and quality baseline |
| Agent with chat | Agent asks and summarizes through chat | Fixed or same optimization protocol | Isolate interaction format where feasible |
| Meaning forms only | Decision reports plus human choices/comments | Baseline rendering of approved meaning | Measure the Meaning Loop contribution |
| Full two-loop system | Same accepted meaning and reference process | Shared optimized expression | Measure expression contribution and end-to-end outcome |
| Per-model wording comparator | Fixed accepted meaning | Separately tuned expression per executor | Compare portability with specialized prompts |
| Expression without approved case examples | Same meaning | Rules-only candidate space | Measure the value of Train examples |

Primary contrasts should be specified before the study, not chosen after seeing results. Keep the number of experiments within budget. Include a model family that was not used for expression optimization when claiming transfer. A per-model wrapper can format outputs, but any model-specific semantic instructions must be disclosed and evaluated as a different condition.

For whole-Meaning-workflow comparisons, define a common independent outcome standard tied to the same task frame and intended person's judgments. Do not let each method create its own reference answers and then compare agreement with those different answers as accuracy. Obtain a shared judgment protocol on a fresh independent confirmation set, independent of method outputs and hidden method identity where feasible. Report agreement with intended human judgments separately from consistency with each method's own guideline. If the person's conception changes during elicitation, record that evolution and use a prespecified adjudication/sensitivity approach; do not silently choose the final standard that favors one method. If a common target cannot be established, compare effort, usability and within-method consistency without making an unsupported cross-method accuracy claim. Expression-only comparisons hold the accepted meaning and reference release fixed.

For the human-with-idea use case, measure time to an accepted standard, decisions per report, rule coverage, correction effort and final labeling outcomes. For the legacy-corpus use case, measure the precision of flagged issues, discovered rule gaps, adjudicated corrections and downstream usefulness. Flags are questions until adjudicated. If using planted errors, disclose their construction and also evaluate naturally occurring issues where feasible.

Human-effort studies should record active review time, reading burden, completion, defer/custom-answer rates, later reversals and comprehension. Fewer clicks alone can conceal worse understanding. If the same person sees multiple interfaces, account for practice and order effects; randomize or counterbalance where feasible. Applicable real-participant research requirements belong to the study's actual approved protocol, not an invented approval flow in the engineering prototype.

## 8. Routing from the round report

| Finding (round report class) | Immediate owner/action | Route |
|---|---|---|
| Expression issue: wording is unclear but rule is settled | The expression rewriting step rewrites from Train evidence, checks and retries within budget | Continue in Step 5 |
| Rule gap or conflict on Train or Test cases | Record it in the round report with source-linked evidence | Reopen the Meaning Loop |
| Suspected reference-label error on Train or Test | Record the hypothesis and evidence; preserve the original label and result | Reopen the Meaning Loop; executor consensus alone never corrects a label |
| Test performance is poor while Train looks adequate | The auditor analyzes Test errors at case level; rewriting sees only Test aggregates | Reopen the Meaning Loop if a rule, preference or reference-label question explains it; Test cases never enter the rewriting context |
| Missing context prevents a justified label | Apply existing abstain/context policy | Reopen the Meaning Loop if the policy itself is absent or inadequate |
| Invalid JSON or transport failure | Executor/schema service repairs operational issue | Continue in Step 5, unless output semantics are underspecified |
| Executor limit: a weak model cannot execute despite faithful wording | Record the capability/budget limit; consider permitted fallback or deferral | No automatic meaning relaxation; stop with a reason if no candidate can meet the floors |
| Declared criteria met for the round's exact versions | Record the evidence in the round report | Proceed to Step 6 |

The round report (CONTRACTS section 7) contains the versions, performance by model and partition, classified error hypotheses with evidence, affected scope, attempted expression changes, unresolved questions, recommended next action and route. A report that reopens the Meaning Loop goes to the whole Meaning Loop Agent, never straight to a human: Step 2 investigates related cases, earlier decisions and original context first, and the Meaning Loop Agent decides whether a human decision report is needed. After an approved semantic or reference change, Step 4 rechecks affected items and Step 5 reruns the affected fidelity and evaluation checks under the new versions; do not compare incompatible meaning versions as if only wording changed.

## 9. Large-scale audit and acceptance

Freeze an explicit production policy: which items may be accepted automatically, which require review, batch size, quality floors, sampling design, stop conditions and who may approve a scope. Include a probability sample across the population, including low-risk items. Add targeted high-risk review for discovery, but do not use that biased sample alone to estimate population error.

Record inclusion probabilities or strata so the estimator matches the sampling design. Report uncertainty and unresolved cases. If an audit fails, apply the prespecified containment/review action, identify affected batches and open Meaning Loop issues if appropriate. A new standard may require relabeling prior production items; versioned lineage makes that scope inspectable.

For the probability-sampled quality audit, collect independent initial judgments before showing the executor's label or identity, then reconcile disagreements separately. A targeted assisted correction queue can show predictions, but its correction outcomes are not an unqualified independent accuracy estimate. Preserve both the original judgment and the final adjudication, and disclose the presentation protocol.

The final delivery should include the adaptive structured guideline, the identifiable human-approved reference subset, the larger labeled corpus with acceptance provenance, unresolved items, executor settings and audit evidence. Avoid presenting all machine-produced labels as individually human-approved.

## 10. What may run during implementation

Allowed engineering checks: synthetic fixtures, fake executors, deterministic scoring examples, local UI interactions and targeted regression tests. These validate behavior, not scientific benefit.

Prepare but do not start unasked: paid model experiments, local GPU campaigns, real data labeling, production scans and human studies. Each actual Run needs its native ticket, selected inputs, frozen protocol, budget and user instruction to start. Report research results only after observing the real outputs.
