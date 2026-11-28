# Ideation Workflow: Tasks, Runs and owner bindings

For new work, read [idea-block.md](idea-block.md). A direction is a Block,
an idea is a Job, and evaluation/development questions are Tasks. Generate,
Test and Select are capability groups, not hierarchy levels or Run IDs.
Load `hai-run` before commissioning a Run; merely invoking this skill
allocates none. A Task may apply several skills as Steps.

## Commission types

| Commission | Owner and output | Inputs and closure |
|---|---|---|
| Assess one question about an idea | Evaluation Task in its Idea Job; a shared soft `run-assess-<target>` writes authored assessments/receipts | Frozen Card revision, evidence pointers, criterion and evaluator; closes with supported conclusion or explicit uncertainty/next action |
| Acquire missing external evidence | Discovery Task/Run; verified owner Result/Card/Bib | Bounded source question; closes by Discovery's evidence and access rules |
| Execute a minimum experiment | Work Task/hard Run; owner Result/runtime | Frozen design, inputs and acceptance rule; closes with positive, negative or truthful non-success outcome |
| Select a tested idea | Human decision recorded by Select; a soft Run only when independently commissioned | Exact reviewed semantic revision, evidence and target; explicit select/defer/abandon, with unanswered questions still open |
| Project a bound Paper Idea view | Paper/Page owner; normal projection receipt | Source packet and consumed revision; no Run solely for sync |

Assessment is local reasoning about evidence. It never creates a second
scientific evidence bank. A Task Result produced by an existing external
portfolio commission stays at that owner; consume it by pointer. Legacy
multi-card Task units may continue using their existing Task-owned portfolio
Runs. Do not move or wrap them just to fit the new layout.

## Bindings and repeat work

1. Define the Task's question, expected artifact, inputs and acceptance rule.
   Select methods appropriate to that question; do not create one Task per skill.
2. When commissioning an assessment, the shared soft-Run Ticket freezes the
   Card/semantic revision, criterion id/version, evaluator/model build and
   input paths. Follow `hai-run` for its sole writer, card, ticket, passes
   and close rule. No private execution engine is introduced.
3. Retain raw specialist receipts. In a soft assessment, keep the full
   assessment binding using `mode: direct`, with an additional `assessment_run`
   link to the soft Run. A legacy hard Task assessment can inherit the binding
   from its real Result using `mode: owning_run`; see [receipts.md](receipts.md).
4. Multiple reviewers keep separate receipts and an explicit reconciliation.
   Agreement does not erase evidence gaps; unresolved disagreement remains
   undetermined. Never average labels or overwrite the dissenting receipt.
5. Changed frozen inputs, target or acceptance rule follow the shared new-Run
   rule. A retry on unchanged inputs is a pass; a human reply resumes the
   pending interaction. Matrix/card refreshes are bookkeeping, not new Runs.
6. Missing sources route to Discovery and missing computation to Work within
   the authorized scope. Otherwise record the missing input and its next owner.
7. Selection consumes the exact I2 revision and the explicit human answer.
   A new Idea Job needs no existing Paper projection. Later scientific changes
   require a new decision before another handoff; preserve previous snapshots.

Block comparison reads Job Cards and assessments by pointer. It does not
invent a shared score or duplicate a Job's decision. A generation batch admits
one Job per new scientific question; a wording refinement stays in the same
Job. A separate Paper is the default destination of each selected Job.

## Boundaries

- Inline brainstorming, a read-only audit, or a projection can allocate zero
  Runs. Retain artifacts only when requested or within already authorized work.
- A Run's output and close rule determine its identity; internal tool calls,
  reviewers, capability labels and receipts do not create additional Runs.
- A local soft assessment has authored outcomes, not a fabricated hard Result.
  A scientific measurement or LLM experiment belongs to a Work Task's hard Run.
- Source Results, pilot Results, Idea assessments and Paper prose have different
  owners. Cite each at its original address and report its actual limitations.
