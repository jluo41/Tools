HAI-Pipe Toolkit Skill Structure
================================

Status: current contract (2026-09-08)
Scope: the live mental model for the toolkit. A folder has two faces: a
reader-facing Page Face and an execution-oriented Task Face. The same folder
may therefore be opened as a Page or executed as a Task; it is not two stores.


The neutral spine
=================

```text
Block (bNN) -> Job (jNN) -> Task Page (tNN) -> Run (rNN)
                                           └── Result(s)
```

`haipipe-run` is the one Level-4 contract. A Run records one bounded attempt;
its immutable Result records what that attempt produced. A Task or Discovery
folder owns its own `runs/` and `results/` (plus scripts and workflow metadata).
Scripts are engines for Runs, not a second evidence system.

Task and Discovery are sibling executors:

```text
Task       Plan -> Build -> Execute -> Report
Discovery  Scope -> Acquire -> Synthesize -> Close
```

Both return the same Run/Result shape. A consumer Page records a source Run as
`Supporting` and creates a consumer-owned `Local Run` when a focal evidence item
needs normalization, extraction, or a page-specific artifact. The resulting
evidence table is the observable hand-off: item name/type, expectation, status,
Supporting Run ids, Local Run id, Result, and any decision or feedback note.


Insight topic instances
=======================

`task/page-types/haipipe-page-insight` owns a consumer-neutral topic/data
instance Page Folder. Its items are runnable questions, not extra Pages.

| Contract | Owner | Unit |
|---|---|---|
| Research topic/data context | haipipe-page-insight | One instance Page Folder |
| Shared analysis | haipipe-task | Reusable recipe; isolated instance inputs and outputs |
| Insight work | haipipe-page-insight + haipipe-run | Item ticket and versioned DIKW/RF Results |
| Item table / Runs view | haipipe-board | Read projections of intent and receipts |
| Consumer-specific Design authority | haipipe-insight-workflow | Exact item/RF evidence contextualized in signed I5 Wisdom |

The detailed contracts are the Insight skill's `ref/instance-items.md`,
`ref/workflow-table.md`, and `ref/task-calls.md`. The same recipe can serve A/B/C
without a patient roster in the shared Task. Citation pins identify instance,
item, execution version, RF, Result path and hash; they never mean “latest”.


The Page workflow
=================

The Page Face is a small, numbered workflow. The numbers are records, not
extra folder levels:

```text
00 CONTEXT   -> haipipe-page-context   gather policy, requirements, audience,
                                         source scope, and freeze the brief
01 OUTLINE   -> haipipe-page-outline   SHAPE the plan; SURVEY evidence items
02 EVIDENCE  -> haipipe-page-evidence LAND Supporting/Local Run Results;
                                         EMBED accepted evidence
03 CONTENT   -> haipipe-page-content  WRITE -> DRAFT -> REVISE -> BUILD
04 CHECK     -> haipipe-page-check    whole-page consistency and readiness
```

The outline plugin owns the Bullet and Evidence Workspaces. The evidence
plugin consumes the Survey table and lands the two Run kinds. Page CHECK is a
read-only whole-page gate; it is not a QA folder or a replacement for a Run.


Run families
============

```text
Runs/
├── Execution    code, data, models, calculations
├── Discovery    search, source review, external evidence
├── Insight      instance-local item interpretation and reusable findings
└── Page         page-local division writing and display work

Scripts/         the files that execute a Run (one path per script/engine)
```

Execution, Discovery, and accepted Insight Runs can be reused by id. A Page Local Run makes one
named Evidence Item ready for the consumer; it may cite several Supporting
Runs, but it owns the page-specific transformation and Result.


Project folder contract
=======================

```text
examples/<PROJECT>/
├── tasks/          internal execution (haipipe-task)
├── discoveries/    external evidence (haipipe-discovery)
├── papers/         academic Page composition (haipipe-paper)
├── applications/  other Page consumers
└── diagram/        non-runtime design records
```

A canonical Task or Discovery leaf is addressed as
`bNN_<block>/jNN_<job>/tNN_<task>/`. Its runtime surface is deliberately
small:

```text
<task-page>/
├── scripts/                  code/config engines
├── runs/<run-id>/             Run declarations and runtime receipts
├── results/<run-id>/          Result Card and produced artifacts
├── workflow/                  plan/report projections, when useful
└── <page>.md                  Page Face / outline and content records
```

There is no `QA/` directory, QA answer bank, QA digest, QA command, or QA
binding in this contract. Questions are ordinary bounded Run requests: reuse
an existing immutable Result or open the shallowest new Run. The consuming
Page, not the executor, records the Supporting/Local relationship.


Current skill buckets
=====================

```text
0_connect / 0_utils   connectors and shared helpers
board                 Board format, renderer, Page/Folder contracts
project               project container setup
task                  internal execution and task-domain families
discovery             Search, Review, and Synthesize external evidence
run                   neutral Level-4 Run/Result contract
ideation              evidence bundles and research directions
paper                 academic composition and Page Types
application           non-academic Page consumers
display / writing     rendering and prose engines
```

The old `probe` name is compatibility-only. New work goes through the Page
Evidence Workspace and its Supporting/Local Run records. `PageX`, QA Probe,
and the former Task/Discovery QA collector are not live workflow stages.
Historical design diagrams may mention the retired vocabulary; they are
non-runtime records and must not be used as routing instructions.


Retirement rule
===============

When a contract is retired, remove its live skill, command, folder, and active
references in the same change. Recovery is through git history. Generated
delivery QA snapshots and Task/Discovery `QA/` folders are not part of the
current project surface; the canonical replacement is a typed Run/Result plus
the consumer's Supporting/Local evidence row.


Where to read next
==================

* `README.md` — user-facing doors and the Run/Result overview.
* `skills/run/haipipe-run/SKILL.md` — the neutral Level-4 contract.
* `skills/board/page-workflows/haipipe-page-workflow/SKILL.md` — the Page loop.
* `skills/board/page-plugins/haipipe-plugin-outline/` — Bullet/Evidence
  Workspaces and the evidence-item table.
* `skills/board/page-plugins/haipipe-plugin-runs/` — the read-only Runs view.
