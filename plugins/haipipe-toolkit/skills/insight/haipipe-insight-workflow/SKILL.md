---
name: haipipe-insight-workflow
description: >-
  Plan and execute an InsightBoard as bounded owner-native Runs
  with explicit dependencies, Results, receipts, and completion rules. Owns
  GI0-GI6 assertions, question/partition projections, Run dispatch, and
  person-signed handoff settlement. Use to run, resume, or inspect an
  InsightBoard, answer its registered questions, or report blocked work.
metadata:
  version: "1.3.2"
  last_updated: "2026-09-20"
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

The runtime enumerates Supporting Runs, Page Evidence Runs and explicitly
commissioned Page Writing/Delivery Runs. Page passes, registration, GI checks,
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

After native Results and receipts land, evaluate the relevant Page/GI
conditions. Settle one cell only after its Page CHECK/CLOSE and exact predicates
pass. When requested answer targets are terminal, requested control actions meet
their own acceptance rules, and the completion policy passes,
close the Runtime. A required unresolved gate leaves it `held`, never complete.

## Folder ownership

| Kind | Owner | Persistent resource |
|---|---|---|
| Meta | `haipipe-insight-meta` | MT00 source inventory, grain, window, freshness, limits and partition register |
| Question | `haipipe-insight-question` | MT01–MT04 stable questions and per-partition Queue cells |
| Data | `haipipe-insight-data` | observations from exact accepted source evidence |
| Information | `haipipe-insight-information` | reproducible derivations from accepted parent rows |
| Knowledge | `haipipe-insight-knowledge` | bounded claims, rivals, strength and pooling verdict |
| Wisdom | `haipipe-insight-wisdom` | contextual counsel and person-signed Design Handoff |

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
COLUMN/X/F-only routing, pooling, or late partition arrival. MT00 alone
registers a partition; Question owns its asks and cell state. X owns comparisons,
has no raw D rows, and every partition-major W depends on the current verdict.

## 🔁 Semantic dependencies across answer targets

The Climb Law constrains evidence dependencies: I cites accepted D, K cites
accepted I, and W cites accepted K. It does not require a new Run for an
already accepted parent. A partition-major board adds a dependency because X
consumes mirrored results and every W cites the pooling verdict:

```text
F's D/I/K first ─▶ each partition's D/I/K mirror, in parallel ─▶ X group
                                                                  │ XI → XK → verdict
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
GI0  inventory ready      MT00 has Page CHECK/CLOSE and its sources resolve through
                          accepted Results or governed frozen local inputs · the four
                          registers exist · on partition-major the partition register
                          and the shared-threshold pointer exist
GI1  question registered      the cell's row carries target, raiser, what-would-answer,
                          and a state cell · its partition group exists on disk
GI2  observations citable   the D Page reached CHECK/CLOSE; every value is bound by
                          path to either accepted Supporting Result → frozen Local Input →
                          ready typed local Result, or governed static local source →
                          frozen Local Input → ready typed local Result. The latter
                          owes no Supporting Run; Data owns both acceptance branches
GI3  derivation citable   the I Page reached CHECK/CLOSE and derives only from
                          exact version/hash-pinned D parent rows (X contrast:
                          mirrored I rows, the one exception)
GI4  parent/verdict ready   the local K Page reached CHECK/CLOSE and cites exact
                          version/hash-pinned I parent rows · OR the pre-climbed
                          external-parent bridge passes all five bridge assertions ·
                          on partition-major the X group's current POOL, SPLIT, or
                          UNDETERMINED verdict cites the predeclared shared thresholds
                          and is current against the partition register — a late
                          partition voids this gate
GI5  handoff authorized      ✋ the handoff's `signed:` row reads `✅ <initials> <YYMMDD>`
                          (haipipe-insight-wisdom) · `⬜` blocks · no machine
                          writes it · receipt pins the exact Page and dependencies
                          (`ref/handoff-record.md`) · under POOL a non-template W closes as a DEFERRAL
                          by id, exports no handoff, and owes no signature · a
                          licensed UNDETERMINED partial-final non-answer likewise
                          has no GI5 pass or Design handoff; Question records GI6
                          under its two-receipt rule
GI6  answer settled               the register cell flips ✅, or 🚫 with a reason, or 🟡 <page>
                          final when the page states why the remainder cannot close
                          (haipipe-insight-question) — always citing the closing page ·
                          gaps remain → the next lap
```

A value produced by EXTENDING an already-used task Run binds to the new artifact
paths; the consumer records the new full Run id as a Supporting Run and reruns
its Local Run when the focal evidence changes.

The DERIVED-HEADER rule (`haipipe-insight-question`) covers every on-register
restatement of the Queue — headers, Diagrams, Openings, status words, and counts.
Reconciling one is Question Task-Face work citing the Queue.

**New computation release and handoff signing remain person-reserved.** A new
Supporting computation is released through the owning Page Evidence Item's
SURVEY `Decide`; legacy Probe records are read-only history. Handoff
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
D/I/K     rung-major:       1-D-data/ · 2-I-information/ · 3-K-knowledge/
          partition-major:  <N>-<L>-<partition>/ with the partition letter prefixed
                            to every page id · X-cross/ for the contrast and verdict
                            (index-free, letters sort last · legacy: 9-X-cross/)
Wisdom        rung-major 4-W-wisdom/, or each partition group's W page
```

These are disk groups, not Question Groups. The derived projection cuts across
them: an MT02 column exposes `QG-<partition>-I`, while partition group B exposes
`QG-B-D`, `QG-B-I`, `QG-B-K`, and `QG-B-W`.

## 🧾 Runtime records

The aggregate envelope and frozen definitions live under
`<board>/_runs/insight/<workflow_runtime_id>/`; native Tickets, Results and
Run receipts remain in their owners' stores. The Runtime indexes rather than
duplicates their authority. `ref/run-workflow.md` defines the envelope.

A GI/resource update leaves one dated control receipt in the granting Folder's
`outline/<stem>-log.md`, except a 🟡 final settlement, which leaves two (see migration rules).
MT00 records GI0 and partition registration; Question registers record GI1 and
GI6; answer Folders record GI2-GI4; Wisdom records GI5. Include the runtime id,
exact target, evidence/version/hash, assertion, actor, outcome and next action.
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
- **Refusal is convergence.** A 🚫 with a reason is a terminal state equal in rank to ✅: the lane terminates because refusing is answering, and a board rich in refusal reasons (thin, F-only, defer, no-measure) is converging, not failing. The defect is the cell that can neither answer nor refuse.

## ↩ Return

Runtime id and definition revision; actual Run inventory with native receipt
links; new/reused exact Results; unallocated Specs; requested cell settlements;
derived Question Group status; held dependencies/person decisions; next ready
Run or control action. State whether the Runtime is held or complete and why.
