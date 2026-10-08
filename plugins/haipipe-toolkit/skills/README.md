HAI-Pipe Toolkit Skill Structure
================================

Status: current contract (2026-09-08)
Scope: the live mental model for the toolkit. A folder has two faces: a
reader-facing Page Face and an execution-oriented Task Face. The same folder
may therefore be opened as a Page or executed as a Task; it is not two stores.


The three layers
================

The skill folders sit in three layers:

```text
skills/
├── 0_utils/    generic helpers, not tied to the Block -> Job -> Task ladder
│               (response-format, diagram-ascii, table-workbench, table-papers, ...)
├── 1_base/     what every theme is built on: project (the ladder, Runs) · task (the work
│               Task) · page (the Page Task) · question · writing · display · ideation · search
└── 2_theme/    one folder per theme: cowork · design · discovery · insight · labeling · paper,
                each holding its haipipe-<theme> skills and its workbench-<theme>
```

A skill in `0_utils` is one folder deep (`0_utils/<skill>/`); a skill in `1_base`
or `2_theme` sits in its family (`1_base/page/haipipe-page/`, `2_theme/paper/workbench-paper/`).
Code finds the skills root by its folder name and a skill by its folder name
(`servers/_host/host_paths.py` `skill_dir`, `1_base/page/haipipe-page/src/skill_paths.py`),
never by counting parent folders, so moving a family to another layer breaks no path.
The servers pair with the layers the same way: `servers/workbench` is the base
every workbench reuses, and each `servers/workbench-<theme>` gives its theme.


The neutral spine
=================

```text
Block (bNN) -> Job (jNN) -> Task Page (tNN) -> Run (rNN)
                                           └── Result(s)
```

`haipipe-run` is the shared Level-4 contract. A Run records one bounded
commission with preserved Steps/attempts; its Result records the outcome.
A Workflow lists planned Run Specs and actual Instances, connected by
dependencies and routes. A Task or Discovery
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

`2_theme/insight/haipipe-page-insight` owns a consumer-neutral topic/data
instance Page Folder. Its items are runnable questions, not extra Pages.

| Contract | Owner | Unit |
|---|---|---|
| Research topic/data context | haipipe-page-insight | One instance Page Folder |
| Shared analysis | haipipe-task | Reusable recipe; isolated instance inputs and outputs |
| Insight work | haipipe-page-insight + haipipe-run | Item ticket and versioned DIKW/RF Results |
| Item table / Runs view | haipipe-page | Read projections of intent and receipts |
| Consumer-specific Design authority | haipipe-insight-workflow | Exact item/RF evidence contextualized in person-signed Wisdom |

The detailed contracts are the Insight skill's `ref/instance-items.md`,
`ref/workflow-table.md`, and `ref/task-calls.md`. The same recipe can serve A/B/C
without a patient roster in the shared Task. Citation pins identify instance,
item, execution version, RF, Result path and hash; they never mean “latest”.


The Page workflow
=================

The Page family is canonical under `skills/1_base/page/` (the Board family was retired
into it, JL 261005): `haipipe-page`, `haipipe-folder`, `haipipe-sentence`, `workbench`,
`haipipe-page-workflow` with its Run skills under `workflow-runs/`, and the two Page workbench skills, `workbench-page` and `workbench-studio`. The Page runtime owns file intake,
individual rendering and standalone editing/hosting, the Board checker and the
Run CLIs. A Board is a folder of Pages read live in the workbench; nothing is built.
Old Board paths are compatibility links, not a second implementation.

The Page Face is a small, numbered workflow. The numbers are records, not
extra folder levels:

```text
00 CONTEXT   -> haipipe-page-context   gather policy, requirements, audience,
                                         source scope, and freeze the brief
01 OUTLINE   -> haipipe-page-structure   SHAPE the plan; SURVEY evidence items
02 EVIDENCE  -> haipipe-page-evidence LAND Supporting/Local Run Results;
                                         EMBED accepted evidence
03 CONTENT   -> haipipe-page-writing  WRITE -> DRAFT -> REVISE -> BUILD
04 CHECK     -> haipipe-page-check    whole-page consistency and readiness
```

The outline workbench owns the Draft and Evidence Spaces. The evidence
workbench consumes the Survey table and lands the two Run kinds. Page CHECK is a
read-only whole-page gate; it is not a QA folder or a replacement for a Run.


Run families
============

```text
Runs/
├── Execution    code, data, models, calculations
├── Discovery    search, source review, external evidence
├── Insight      instance-local item interpretation and reusable findings
├── Page         RP writing, RE evidence, RD delivery, delegated writing/display
├── Design       Commission, Generate, Verify
├── Paper        bounded judgments, compile and response work
└── Labeling     the domain's 25 independently closable operation kinds

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
A board's own Questions are a different thing: topics recorded in its
`reports/qNN_<topic>/` folders, each answered by a report Page. They are owned
by `1_base/question/haipipe-question`.


Current skill buckets
=====================

```text
0_connect / 0_utils   connectors and shared helpers
board                 Board format, renderer, Page/Folder contracts
question              questions on any board: a topic and its asks, reports/qNN_<topic>/, the register,
                      shaping an ask (question-asking methods), reviewing it (Q1-Q7), chat matching
project               project container setup
task                  internal execution and task-domain families
discovery             Search, Review, and Synthesize external evidence
run                   neutral Level-4 Run/Result contract
ideation              evidence bundles and research directions
paper                 academic composition and Page Types
insight               evidence-led understanding: native Runs, dependencies, DIKW resources
design                creative production: Brief -> Commission -> Generate -> Verify
display / writing     rendering and prose engines
```

The old `probe` name is compatibility-only. New work goes through the Page
Evidence Space and its Supporting/Local Run records. `PageX`, QA Probe,
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
* `skills/1_base/project/haipipe-run/SKILL.md` — the neutral Level-4 contract.
* `skills/1_base/page/haipipe-page-workflow/SKILL.md` — the Page loop.
* `skills/1_base/page/workbench-page/` — Bullet/Evidence
  Workspaces, the evidence-item table, and `ref/run-space.md`, the
  read-only Runs view.
* `skills/2_theme/paper/workbench-paper/` — the Paper Board's Setup, Ideation,
  Story, and Run-Type work console.
