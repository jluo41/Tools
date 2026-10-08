---
name: haipipe-insight-workflow
description: >-
  Plan and execute an InsightBoard as bounded owner-native Runs
  with explicit dependencies, Results, receipts, and completion rules. Owns
  GI0-GI6 assertions, question/partition projections, Run dispatch, and
  person-signed handoff settlement. Use to run, resume, or inspect an
  InsightBoard, answer its registered questions, or report blocked work.
metadata:
  version: "2.3.0"
  last_updated: "2026-10-01"
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

# /haipipe-insight-workflow · execute Runs and record their dependencies

Load `haipipe-insight`, `haipipe-folder`, and `haipipe-run`. This controller
owns the selected Run Spec graph, requested answer targets, GI0-GI6 assertion
policies, and aggregate Runtime. Folder skills own their resources; native
Run owners keep their Tickets, Results, receipts and closure rules. The
controller verifies and records a person-signed W handoff plus GI6 settlement.
Design consumes its exact signed version as Insight input and owns its own Brief.

Read [`ref/run-workflow.md`](ref/run-workflow.md) before planning, dispatch,
resume, or status; it defines concrete Spec templates, native Run inventory,
storage, control records and completion. Read
`../haipipe-insight/ref/question-groups.md` for register projections,
`../haipipe-insight/ref/page-v2-adapter.md` for Page/evidence boundaries, and
`ref/migration.md` when encountering old paths, fields or receipts.

Task-side topic/data instances keep `haipipe-page-insight`'s `riNN` item
workflow. An InsightBoard Runtime references an accepted Task item Result as a
Supporting Run dependency; it does not copy or recount that execution.

## Workflow model

```text
Workflow Definition = bounded Run Specs + dependency/Route graph + completion rules
Workflow Runtime    = workflow_runtime_id + actual owner-native Run instances
                      + receipt references + control records + ready/waiting work
Question Group      = partition × DIKW target, a derived scheduling/status view
```

There is no Phase object or current-Phase state. Meta, Question, Data,
Information, Knowledge and Wisdom are Folder kinds, not Run Types. Their
contracts describe inventory, registration, observations, derivations, claims
and counsel. Select work from missing targets and dependencies; a Folder may
need zero, one, or several native Runs. A Run Spec has one bounded target and
close rule; only an allocated native Ticket and receipt establish a Run.

The runtime enumerates the page tickets that answer questions (an answering
page's `runs/run_bNNjNNtNNrNN_<partition>_<task>.sh`, which sets `RESULT_DIR`
to the page's `results/<ticket>/` and calls a task run in the Project's DIKW
Block whose config's `answers:` cross-checks the question), the Report runs
that write or refresh the answering page's `.md` from its own results, and the
Wisdom pages' writing and delivery Runs (JL 261001; `haipipe-insight` `ref/board-contract.md`). Page passes, registration, GI checks,
signature recording and settlement are controller/resource actions without
Run ids. A control-only execution may have an empty Run inventory. Completed
Results are reused by exact address; a Page pass never becomes a wrapper Run.

## 🚚 Dispatch by ready Run

Use `ref/run-workflow.md` as the execution procedure. Resolve the request's
cells, reuse exact accepted inputs, and freeze a concrete Run Spec graph.
Prefer already-computed targets (`⬜ calc`) where no new computation is needed.
Select a ready native Run by its target and dependencies; load the exact worker
and Folder owner. Before dispatch, verify its Ticket, release, input pins and
Result/receipt paths. A missing input is a named blocker.

A bounded Page pass uses `mode: copilot` and reports its native child Runs to
the aggregate Runtime. It allocates no RP merely because the controller ran;
an RP requires an actual selected writing goal. The dispatcher can also perform
an explicit control-only action, such as registration or a CHECK over an
existing Page. Report that action without inventing a Run.

After native Results and receipts land, evaluate the relevant GI
conditions. Settle one cell only after its answering page
passes its check and the exact predicates pass. When requested answer targets are terminal, requested control actions meet
their own acceptance rules, and the completion policy passes,
close the Runtime. A required unresolved gate leaves it `held`, never complete.

## Folder ownership

| Kind | Owner | Persistent resource |
|---|---|---|
| Meta | `haipipe-insight-meta` | MT00 source inventory, grain, window, freshness, limits and partition register |
| Question | `haipipe-insight-question` | MT01–MT04 stable questions and per-partition Queue cells |
| Data | `haipipe-insight-data` | observations: the answering page's ticket results; the page says them in words |
| Information | `haipipe-insight-information` | reproducible derivations: the answering page's ticket results and the page that reads them |
| Knowledge | `haipipe-insight-knowledge` | a page: bounded claim, rivals, strength, pooling verdict |
| Wisdom | `haipipe-insight-wisdom` | a Page: contextual counsel and person-signed Design Handoff |

Each owner selects its native Run work through `ref/run-workflow.md`; ownership
alone creates no Run. A pooling verdict is Knowledge about exchangeability and
ends as `POOL`, `SPLIT`, or a supported `UNDETERMINED` result. Missing or stale
inputs keep GI4 held; a completed but inconclusive comparison is not forced
into either branch.
SETTLE is a Question-owned resource update. GI0-GI6 are stable predicate keys,
not execution positions. Passing a predicate authorizes only the exact
resource/version/target named in its receipt.

## Question Groups and partitions

A Question Group is a derived `partition × DIKW target` view of Queue cells;
its state never allocates a Run or settles its members together. Load
[`ref/partition-policy.md`](ref/partition-policy.md) for audience eligibility,
COLUMN/cross/full-only routing, pooling, or late partition arrival. MT00 alone
registers a partition; Question owns its asks and cell state. `cross` owns comparisons,
has no raw D rows, and every partition-major W depends on the current verdict.

## 🔁 Semantic dependencies across answer targets

The Climb Law constrains evidence dependencies: an Information page reads
its own current results, a Knowledge page cites results and Information pages,
and a Wisdom page cites Knowledge pages. It does not require a new Run for an
already accepted parent. A partition-major board adds a dependency because `cross`
consumes mirrored results and every W cites the pooling verdict:

```text
full's D/I/K first ─▶ each partition's D/I/K mirror, in parallel ─▶ cross group
                                                                     │ I → K → verdict
                                                                     ▼
                                                 every W page last, template
                                                 included, all citing the verdict
```

Compile these prerequisites into the selected Run Specs. They constrain when
a target is ready; independent work may proceed concurrently under its owner.

### Task RF bridge

For a Task Wisdom RF input, load [`ref/task-rf-bridge.md`](ref/task-rf-bridge.md)
and check all five assertions. The exact accepted Task item owns its D/I/K/W
chain; local Wisdom adds board applicability and counsel, then owes GI5 and
Question-owned GI6. A bare R, below-Wisdom RF, stale Result, or incomplete chain
cannot satisfy this bridge.

## 🚦 Runtime control keys · GI0-GI6

Each GI key names a testable resource assertion. Its owning Folder log records
the evaluation, authority, exact evidence and resulting action; the Runtime
indexes it under `resource_controls`. Run-owned gates/routes remain on native
Run receipts and are indexed under `control`. No GI check gets a synthetic Run id. Controls are per-CELL except GI0, which is per-board, and GI4's verdict
clause, which is per-column-set.

```text
GI0  inventory ready      MT00 names the board's ONE extract and it resolves · the four
                          registers exist · on partition-major the partition register
                          (with one config stem per cut) and the shared-threshold
                          pointer exist
GI1  question registered      the cell's row carries target, raiser, what-would-answer
                          with its evidence needs (kinds legal at the level;
                          haipipe-insight ref/evidence-needs.md), and a state cell · its partition is on MT00's register (a W
                          cell also needs its partition's folder for the W page)
GI2  observations citable   the answering page's ticket for the QD question has a
                          current `ok` receipt for the board's extract in the page's
                          `results/<ticket>/`; haipipe-insight-check finds every need
                          planned with its work spec, bound, fit, cited and current; the
                          page is adopted from its Draft, `page.py health` has no FAIL and
                          a page CHECK by an agent that did not write it passed; unit,
                          window and coverage are stated; no interpretation has entered
GI3  derivation citable   the same for a QI question (needs, specs, health and page CHECK
                          included), and its page (required for
                          Information) traces every number to a file in its own results and keeps
                          nulls visible (cross contrast: mirrored Information results of
                          each partition, the one exception)
GI4  parent/verdict ready   the Knowledge page passed a fresh-context check: every
                          number traces to a current named result, haipipe-insight-check
                          finds every need bound, fit, cited and current (no compute
                          need reasoned away, every refusal shown by a probe run),
                          `page.py health` has no FAIL, a page CHECK by a different agent
                          passed, strength, rivals and boundary are stated · OR the pre-climbed external-parent
                          bridge passes all five bridge assertions · on
                          partition-major the cross group's current POOL, SPLIT, or
                          UNDETERMINED verdict page cites the predeclared shared
                          thresholds and is current against the partition register —
                          a late partition voids this gate
GI5  handoff authorized      ✋ the handoff's `signed:` row reads `✅ <initials> <YYMMDD>`
                          (haipipe-insight-wisdom) · `⬜` blocks · no machine
                          writes it · receipt pins the exact Page and dependencies
                          (`ref/handoff-record.md`) · under POOL a non-template W closes as a DEFERRAL
                          by id, exports no handoff, and owes no signature · a
                          licensed UNDETERMINED partial-final non-answer likewise
                          has no GI5 pass or Design handoff; Question records GI6
                          under its two-receipt rule
GI6  answer settled               no overclaim from haipipe-insight-check on the cell, then the
                          register cell flips ✅ <page id> (`✅ <L><NN>-<partition>`), or 🚫 with a reason, or
                          🟡 <page id> final when the answer states why the remainder cannot
                          close (haipipe-insight-question) — always naming the answering
                          page, whose state line names the question back (`answers QI2`) ·
                          gaps remain → the next lap
```

A value produced by EXTENDING an already-used task Run binds to the new artifact
paths; the consumer records the new full Run id as a Supporting Run and reruns
its Local Run when the focal evidence changes.

The DERIVED-HEADER rule (`haipipe-insight-question`) covers every on-register
restatement of the Queue — headers, Diagrams, Openings, status words, and counts.
Reconciling one is Question Task-Face work citing the Queue.

**New computation release and handoff signing remain person-reserved.** A new
computation is a new task config (and, when needed, a new task) in the DIKW
Block, authored through `haipipe-task`; the person presses Run. Legacy Probe
records and Page Evidence Items on boards made before page tickets are read-only
history. Handoff
signing is GI5. Page Workflow may also require local Shape approval, CITE
verification, or Page acceptance while authoring that Folder. Those nested
Page-Face controls may pause a copilot pass, but they do not create extra Insight
transitions or GI numbers. Every dispatch pins `mode: copilot`. A blocked gate
is a clean stop: report the affected Run id/Spec, target cell, exact waiting artifact and
person's owed decision; preserve other independently ready work in the frontier.

For the shared Page Workflow's owner RULING, Meta, Question, Data, Information and Knowledge declare none beyond their
mechanical GI closure; Wisdom reuses the GI5 signature receipt. This never creates
a duplicate human tick. Historical Probe records remain read-only migration
input.

## 🗃 Group mapping

```text
Meta        0-MT-meta/MT00-meta/
Question        0-MT-meta/MT01-MT04/
D/I/K     <N>-<partition>/<R><NN>-<partition>-<slug>/ (Job/Task): <slug>.md (Report) ·
          runs/<ticket>.sh + results/<ticket>/ (Work) · 9-cross/ (pinned
          last) for cross pages · old level-major
          boards: 1-D-data/ · 2-I-information/ · 3-K-knowledge/
Wisdom    each partition's folder <N>-<partition>/W<NN>-<partition>-<slug>/ (no runs/
          when it reasons only from other pages)
```

These are disk groups, not Question Groups. The derived projection cuts across
them: an MT02 column exposes `QG-<partition>-I`, while partition group `<partition>` exposes
`QG-<partition>-D`, `QG-<partition>-I`, `QG-<partition>-K`, and `QG-<partition>-W`.

## 🧾 Runtime records

The aggregate envelope and frozen definitions live under
`<board>/_runs/insight/<workflow_runtime_id>/`; native Tickets, Results and
Run receipts remain in their owners' stores. The Runtime indexes rather than
duplicates their authority. `ref/run-workflow.md` defines the envelope.

A GI/resource update leaves one dated control receipt in the granting Folder's
`draft/records/<stem>-log.md`, except a 🟡 final settlement, which leaves two (see migration rules).
MT00 records GI0 and partition registration; Question registers record GI1,
GI2-GI4 (the register facing the answer's level, since a run or a run result has no
Folder log) and GI6; Wisdom records GI5. Include the runtime id,
exact target, evidence/version, assertion, actor, outcome and next action.
For GI5/GI6 and Design eligibility, use [`ref/handoff-record.md`](ref/handoff-record.md).
Link any consumed native Run receipt; the Folder log cannot replace it.

## ⏱ Advancement is never scheduled

A gate test may be run any time; a gate may only be DECLARED passed by the human tick or CHECK verdict it names. Nothing here may be wired to a timer or a loop that advances cells on wall-clock time.

## 🔀 Status

Report the `workflow_runtime_id`, frozen definition revision and actual Runs:
full native id, Spec, owner, target, managed/reused participation, state, exact
Result, receipt, dependencies and next action. Unallocated Specs have no Run id.
List control-only work and unresolved person decisions explicitly.

Then project Question Groups as `EMPTY | RUNNABLE | BLOCKED | SETTLED` from
their cells and ready/waiting work. A CELL/Folder kind never substitutes for a
Run identity. Multiple cells may cite the same Run; count it once.

## Version changes and historical marks

Read [`ref/migration.md`](ref/migration.md) when touching an older contract or
stale record. Preserve old Results, signatures and settled marks. A changed
current-use payload holds its dependent handoff until owners recheck it; never
rewrite history to align a projection. Partial-final settlement leaves reciprocal
register and answering-Page receipts quoting the licensing sentence.

## 🛑 Stop rules

- GI5 is the outward-export boundary: after signature, never compose or design
  in this lane. The dispatcher must still perform the Question-owned GI6 register
  settlement, leave its receipt, and only then stop that cell.
- HOLD the affected target at an unresolved gate. Continue only independent
  ready work already in scope; if none remains, record blockers and return.
- STOP on contradiction: conflicting Queue, Page or receipt state is a named
  defect with exact sources; never overwrite history to make projections agree.
- **Known-stale is marked, not repaired.** A line known stale but deliberately left (a frozen handoff, a fenced page) is marked `🧊 <staling event>` where it stands, so frozen debt is distinguishable from unnoticed drift; an unmarked stale line remains a finding.
- **Refusal is convergence.** A 🚫 with a reason is a terminal state equal in rank to ✅: the lane terminates because refusing is answering, and a board rich in refusal reasons (thin, full-only, defer, no-measure) is converging, not failing. The defect is the cell that can neither answer nor refuse.

## ↩ Return

Runtime id and definition revision; actual Run inventory with native receipt
links; new/reused exact Results; unallocated Specs; requested cell settlements;
derived Question Group status; held dependencies/person decisions; next ready
Run or control action. State whether the Runtime is held or complete and why.
