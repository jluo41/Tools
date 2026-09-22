---
name: haipipe-insight
description: >-
  Unified Insight door for Task-side topic/data instances and InsightBoards.
  Routes dataset-first requests to the Task Insight Page/RI contract and
  board-scoped requests to a graph of owner-native Runs. Meta declares the
  extract; Question registers ask; Data observes; Information derives;
  Knowledge claims; Wisdom counsels and exports a person-signed Design
  Handoff. Ends at the correct Insight boundary, never designs. Trigger:
  insight, InsightBoard, Insight Page, RI, question register, DIKW, climb,
  chain, partition, pooling verdict, Design Handoff, InsightBoard grooming,
  /haipipe-insight.
allowed-tools: Bash, Read, Write, Grep, Glob, Skill
metadata:
  version: "1.6.2"
  last_updated: "2026-09-20"
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

# /haipipe-insight · one public door, two Insight scopes

`/haipipe-insight` is the one user-facing entry for both kinds of Insight work.
It resolves the scope first, then loads exactly one owner:

```text
Task-side Insight       a neutral topic/data instance · item `riNN` Runs ·
                        versioned D/I/K/W/RF Results
InsightBoard scope       a named Insight-owned board · bounded Run Specs and native Runs
                         answering registered targets from exact accepted evidence
```

This is a router, not a third data or Page owner. Task-side execution remains
owned by `haipipe-task` + `haipipe-page-insight`; the InsightBoard route remains
owned by this door + `haipipe-insight-workflow`. The physical skill location
under `skills/insight/` does not change the Task-only status of
`page-type: insight`.

**Family boundary.** Insight and Design are independent peer families. An
InsightBoard is an Insight-owned resource; it is not nested under an Application
parent. The `application` route token below is a legacy scope selector for an
InsightBoard, not a family or authority layer.

For an InsightBoard execution, this door creates or resumes one
`workflow_runtime_id` and records native Runs, dependencies, Results and
receipts. The six Folder kinds describe resources. GI0-GI6 are assertion keys;
Question Groups project `partition × DIKW target` for scheduling/status.
Read `../haipipe-insight-workflow/ref/run-workflow.md` for the concrete model.
There is no Phase object or current-Phase state.

## One public door, two routes

Use the explicit form when the scope is known. The bare form is a convenience
for a topic whose board has not yet been named:

```text
/haipipe-insight task "<topic>" [<task-board>]                         Task-side
/haipipe-insight application <insightboard-root> <verb> [args...]        InsightBoard (legacy scope token)
/haipipe-insight "<topic>" [<task-board-or-context>]                    auto-route
```

The InsightBoard verbs (`enter`, `status`, `meta`, `sources`, `question`,
`ask`, `climb`, `chain`, `partition`, `verdict`, `settle`, `handoff`, `check`,
`review`, `workflow`, `run`) keep their existing meaning. For compatibility,
the existing verb-first form remains valid:

```text
/haipipe-insight <verb> [<insightboard-root>] [args...]
```

Resolve the route in this order:

| Signal | Route | First owner to load | Resulting unit |
|---|---|---|---|
| explicit `task` | Task-side | `haipipe-task` → `fn/insight.md` → `haipipe-page-insight` | one topic/data Page and its `riNN` items |
| explicit `application` | InsightBoard scope (legacy selector) | this door → `haipipe-insight-workflow` | requested targets and their native Run dependencies |
| an existing `*-InsightBoard` or InsightBoard root | InsightBoard scope | same InsightBoard route | existing board status or requested verb |
| an existing Task Board, dataset-first topic, or bare topic | Task-side | same Task route | create/resume a neutral Insight Page |
| ambiguous path/context | stop and ask for the scope | neither | never create a duplicate or guess an audience |

`/haipipe-task insight "<topic>" [<board>]` is the compatibility alias for
`/haipipe-insight task "<topic>" [<board>]`; it must produce the same
`scope: task`, `insight-layout: items-v2` Page and the same RI contract. Keep
`/haipipe-discovery` separate for literature and external-evidence discovery.

The `partition × DIKW target` Question Group exists on the InsightBoard route
only: it is a derived scheduling view over one stable register question and
its partition cell. Task-side Insight work has an item-level target and dataset
binding, but does not mint InsightBoard Question Groups or DIKW answer Folders.

After routing, the boundary is equally strict:

```text
Task-side       resolve/reuse the Page → select an item → bind `riNN` to one
                normal `rNN` + new frozen dataset → execute only after its
                ticket/receipt gates; finalize evidence input after dependencies arrive
InsightBoard    resolve the board and targets → reuse exact accepted Results →
                dispatch ready native Runs through `haipipe-insight-workflow`
```

The router does not execute a whole Task merely because a topic was named, and
it does not create an InsightBoard merely because a dataset was named.

## Working vocabulary

| Term | Meaning |
|---|---|
| Run Spec | One bounded piece of executable work and its completion rule |
| Run | An actual execution allocated by its native owner, with Ticket and receipt |
| Runtime | The controller's index of actual Runs, controls, and remaining work |
| Folder kind | What a resource contains and which skill owns it |
| GI control | A recorded resource assertion, without a Run identity |
| Question Group | A derived view of one partition's cells at one DIKW rung |

**Who owns what**:

```text
haipipe-insight               public Insight router + InsightBoard one-dataset/register/
                              handoff laws · InsightBoard verbs
haipipe-task/fn/insight       Task-side route procedure (compatibility alias included)
haipipe-page-insight          Task-side topic/data Page, item, RI, and DIKW/RF Result contract
haipipe-insight-meta         the head: source inventory only, holds NO question
haipipe-insight-question     the four registers MT01-MT04: asked and tracked, never concluded
haipipe-insight-data/-information/-knowledge/-wisdom     what each rung IS
haipipe-page-workflow         the loop every page here runs, like every page anywhere
haipipe-insight-workflow      Run Specs, native Run inventory, dependencies,
                              GI assertions, control records and completion
haipipe-folder                the shared two-face Folder contract
```

Read `ref/page-v2-adapter.md` whenever creating, reopening, or checking a rung
Page. Read `ref/question-groups.md` for question registration, status, or
dispatch. The first separates Page closure from epistemic advancement; the
second defines the derived `partition × DIKW target` grouping without adding a
Folder or second Queue.

`page-type: insight` stays TASK-ONLY: a consumer-neutral topic/data instance
with item Runs, each carrying a versioned DIKW/RF Result. The unified Task
route delegates to `/haipipe-task insight` and `haipipe-page-insight`; this
InsightBoard route never mints a Task-side Page or RI. Its own Folders are Meta,
Question, Data, Information, Knowledge, and Wisdom. A settled Wisdom-targeted
Task RF may enter only as the workflow's pre-climbed external parent: Question
registers its exact instance/item/execution-version/RF reference and a local
Wisdom Folder contextualizes the Insight Design Handoff for a person to sign.
RF never reaches Design directly.

## Resource laws

- One board owns one source extract. A subgroup is a partition; a child board
  requires a SPLIT verdict and its own consumer.
- D observes; I derives from exact D rows; K claims from I; W counsels from K.
  X permits the declared mirrored-I contrast and K-from-K pooling verdict:
  `POOL`, `SPLIT`, or evidence-supported `UNDETERMINED`.
- The register writes identity/state, answer Pages write findings, and Wisdom
  exports a person-signed handoff. Queue cells remain the settlement authority.
- Question prefixes fix their rung. A rung change creates a linked successor
  id in the destination register, preserving the original row and receipts.
- Design consumes an exact current signed W payload and its GI6 receipt.
  Signature presence alone does not establish current eligibility.

For board layout, question births, the three writing authorities, and citation
exceptions, read [`ref/board-contract.md`](ref/board-contract.md). For partition
scaffolding, read [`ref/partition.md`](ref/partition.md). For the Task Wisdom RF
bridge, read [`../haipipe-insight-workflow/ref/task-rf-bridge.md`](../haipipe-insight-workflow/ref/task-rf-bridge.md).

## Verbs

```text
task | topic | instance
                    dispatch a dataset-first request to the Task Insight Page/RI route ·
                    create/resume a neutral topic/data instance, never an InsightBoard
application | board  resolve an InsightBoard root using the legacy `application` scope token,
                    then use the InsightBoard verbs below
enter | status      resolve the board · derive Question Groups from MT00 × the four
                    rung registers · report native Runs/blockers plus derived group status
meta | sources      create/resume the one MT00 (`haipipe-insight-meta`)
question | ask      register one question from plain words: the verb decides level, partitions
                    and lineage, then writes the row (`haipipe-insight-question`) ·
                    NEVER answer it there
climb | chain       open or extend the frontier rung for one question (`haipipe-insight-workflow` + selected Folder owner) ·
                    Evidence Items planned · honor the native owner’s release requirements
partition           register a partition on MT00 and insert its group before X
                    (the umbrella's ref/partition.md)
verdict             drive the X group XI → XK → a POOL/SPLIT/UNDETERMINED
                    verdict page under the partition's predeclared thresholds
                    (`haipipe-insight-workflow` + Information/Knowledge owners) · every W waits for it
settle              flip the register cell ✅, 🚫 with a reason, or 🟡 <page> final
                    (haipipe-insight-question's exit), citing the closing page
handoff             draft the W page's Design Handoff division · ✋ a person signs its
                    `signed:` row — `signed: ✅ <initials> <YYMMDD>`, never a machine ·
                    the door RECORDS a signature the person states, never decides one
check | review      CHECK selected rung pages in a fresh context through haipipe-page-check
workflow | run      execute selected Run Specs and controls (§Execution): pin → dispatch → receipt → settle
```

New Supporting computation is released by a person through the owning Page's
SURVEY `Decide`; a W handoff is signed by a person. Prior explicit durable
release may be consumed, never inferred. Page passes use `mode: copilot` and
retain their native outline, evidence-verification and acceptance rules.

## Execution

[`Run execution procedure`](../haipipe-insight-workflow/ref/run-workflow.md) owns the full procedure:

1. Resolve the requested questions/partitions, inventory and exact accepted
   parents. Registration is a Question-owned resource update, not a Run.
2. Reuse current Results and resume compatible open Runs. Freeze a definition
   containing only the bounded Specs and dependencies this request needs.
3. Dispatch a ready native Run through its owner and Ticket. Supporting
   computations, local Evidence, and selected Page writing/delivery keep their
   existing identities; internal Steps and Page controller passes add no Run.
4. Read the native Result and receipt; evaluate the owner's exit rules and the
   applicable Page/GI conditions. Record control-only actions as such. A pass
   that needs no new work truthfully reports zero new Runs.
5. For an exported W handoff, verify the person's signature; a valid POOL
   deferral needs no signature. Under `UNDETERMINED`, a licensed partial-final
   non-answer has no GI5 pass or Design handoff. The Question owner records the
   applicable GI6 settlement with the exact answering Page and receipts.
6. Continue independent ready work in scope. A required blocker leaves the
   Runtime held; complete only when the requested targets, required work and
   final acceptance satisfy the frozen definition.

DIKW dependencies require accepted parent evidence; they do not require
reexecuting already accepted work or a fixed number of Runs. Question Group
status remains derived from its cells. The aggregate Run inventory records a
shared computation once even when several cells consume its Result.

## Ownership across workflows

```text
this door         routing, one-dataset/evidence/register/handoff laws and verbs
insight-workflow   Run Spec graph, actual Runs, GI controls, dispatch and completion
Folder owner      resource contract, Page/Task faces, citation and settlement rules
native Run owner  Ticket, worker, Result, receipt, retry/version and closure
page-workflow     bounded Page coordination and its own native writing/evidence Runs
Design            exact signed Insight input; Design Brief and Design Runs
```

Cross-board handoff receipts belong to the source Insight and consuming Design
owners. No Application parent workflow or synthetic handoff Run is created.

## Bounded standing authorization

A person may preauthorize mechanical register operations for one Workflow
Runtime. Read
[`../haipipe-insight-workflow/ref/authorization.md`](../haipipe-insight-workflow/ref/authorization.md)
when a user requests such batching. The record must name the person, board,
runtime, exact target scope, permitted actions, evidence of authorization and
expiry. Each action's control receipt cites the authorization and licensing
rule. A missing or ambiguous grant is not standing authorization.

Handoff signatures and release of new computation remain individually
person-reserved; no standing authorization extends to them. Existing explicit
session authorization remains effective for its stated scope and is recorded
without asking the person to repeat it.

## Board grooming is an audit, not a hidden writer

When a user asks to groom an InsightBoard, first identify the real board path
and read its `board.md`, MT01–MT04 registers, current D/I/K/W pages, and the
mechanical Insight checks. Report the current frontier, partial or open
register cells, dead or malformed references, and the Wisdom Handoffs that
are actually bindable. Keep the report linked to the exact source paths so a
demo is evidence-backed rather than generated from an empty fixture.

The board-level Insight workbench presents this as the read-only Check Space.
It may propose the next Question Group or identify a safe repair, but it does
not rewrite a finding, promote a register cell, overwrite evidence, or write a
person's `signed:` row. Those are explicit owner actions in the Insight
workflow. The Page-level Design workbench reads only the DesignBoard's declared
`reads:` InsightBoard and accepts only a currently eligible signed Wisdom Handoff with exact owner receipts; it never
binds directly to D, I, or K.

## Ends at a signed handoff

A signed Design Handoff is an insight decision, not a design: it names finding,
strength plus its Knowledge-grounded evidence basis, boundary, source versions,
design consequence and forbidden overreach, and never message copy. Design
consumes its exact frozen path/version/hash and GI6 settlement receipt under
`ref/page-v2-adapter.md`; it does not create a new PageX lane or synthetic Run.
The read-only binding projection uses
[`handoff-record.md`](../haipipe-insight-workflow/ref/handoff-record.md).
Shipping and measuring are task-layer work, and the effect read back lands HERE
— a refreshed source row on MT00, a reopened chain, and a handoff v2 whose
staleness reopens exactly the design divisions that cited it.

A licensed `UNDETERMINED` partial-final W non-answer stops before this export
boundary. It has no signature or Design binding; its Question cell records the
partial exit and the evidence or decision that could reopen it.
