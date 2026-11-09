---
name: haipipe-work
description: "Create, route, or update work-theme Blocks. /haipipe-work update <Block> aligns an existing Block and its Job/Task pages with the current focus UI, preserving source records and checking the live views. Distinguishes Work Block from Blueprint Block; routes execution to its owning skills. Trigger: update work block, align work format, work theme, /haipipe-work."
metadata:
  version: "0.2.1"
  last_updated: "2026-11-09"
---

# Work theme

The work theme runs bounded execution work: code, data, models, calculations.
It is one of the themes in `skills/2_theme/` (beside cowork, design, discovery,
insight, labeling and paper). Its current focus pages use the shared
`servers/workbench/focus_page.py` and `work_frame.py`; `servers/workbench-work`
also retains the classic workbench. It was
called the task theme until 2026-10-07; the Task as a ladder level (Block ->
Job -> Task -> Run) belongs to every theme and keeps its name.

```text
work/bNN_<topic>/                    a work Block: board.md, Questions, reports/, sNN topics
└── jNN_<series>/                     a Job: one series of Tasks (j0N, j1N, j5N ...)
    └── tNN_<task>/                   a work Task: plan -> build -> run -> read -> close
        └── runs/rNN_<noun>_<qualifier>/      Run card, ticket and config
            └── result/                     returned artifacts and runtime receipt
```

Legacy flat tickets and `results/` remain readable; a format update does not move them.

## Update an existing Block

```text
/haipipe-work update <Block path>
/haipipe-work update <Block path> --check
/haipipe-work update <Block A> <Block B>
```

These are instructions to the skill-running agent, not a new executable or flags
for `wb.py`. `update` inspects, applies supported content/link fixes within the named
Blocks, then verifies their pages. `--check` only inspects and reports differences.
With no path, use an unambiguous Block from the conversation; otherwise ask for the
target. Multiple paths limit the batch to those Blocks, never every SPACE by default.

Read [ref/update.md](ref/update.md) and `../workbench-work/SKILL.md` first.
The update procedure here coordinates the owning skills; read the relevant owner
before changing its records. Do not automatically run `/wb update --apply`: its
older structural migration can move files and impose the classic workflow layout.

## Two Block UI types within Work

| UI type | Purpose | Views |
|---|---|---|
| 🧩 Work Block | Carry out work and return results: paper results, data pipelines, model experiments | Overview · Status · Findings · Delivery |
| 📐 Blueprint Block | Develop and check a theme's pages and supporting skills | The same four views, plus configured Block UI · Job UI · Task UI · Run UI |

Both remain work-theme Blocks on the same B–J–T–R ladder. `Blueprint Block` is a
presentation distinction, not a new theme or a new `board-kind`. Determine it from
the Block's authored purpose and page-example configuration, never from its folder
being under `blueprints/` alone: a demonstration Work Block there is still Work.
Only a Blueprint's applicable `ui-block:`, `ui-job:`, `ui-task:`, `ui-run:` entries expose those
extra views. Never copy them to ordinary work to make its screen look like b17.
An intended Blueprint with missing examples is incomplete, not evidence of a working UI.

The current reference is `blueprints/Project-Ladder/work/b17_theme_work/ui/block-views.md`
and its `view-guide.json` (from the Tools root). `b90_example_paper_results` is the
ordinary Work example; `b17_theme_work` is the Blueprint example. Compare their
structure, not their sample content. Data pipelines and model experiments are use
cases, not additional Job types; task execution types remain their owners' contracts.

Every view has **📋 Review Content** (numbered, view-specific sections), followed by
**🧭 Around the Work** (Studio, Interactions, Decisions, Things to Know, Checklist,
Timeline, Skills, Files; unnumbered). Report incorporates work actions; Work is no
longer a separate right-rail entry in the current work focus UI. Shared sections
inside a view show its linked records; the corresponding right-rail section rolls
up this Block, Job or Task across views. Keep meaningful content differences.


Route
-----

| You want to | Skill | Where |
|---|---|---|
| create, run, audit or close a Task folder; Plan, Build, Execute, Report; read a Run's Result | `haipipe-task` | `1_base/task/` (base: other themes call it too) |
| align an existing Work or Blueprint Block with the current focus UI | this skill's `ref/update.md`, coordinating the owners below | `2_theme/work/haipipe-work/` |
| open or read a Block, Job or Task on screen (Overview, Status, Findings, Delivery) | `workbench-work` | `2_theme/work/` |
| create a Work Block | `haipipe-block`, with the work-specific Task contract | `1_base/project/`; `1_base/task/` |
| edit the Block face; edit its Job faces | `haipipe-block`; `haipipe-job` | `1_base/project/` |
| scope or maintain Studio topics and their records | `haipipe-studio` | `1_base/project/` |
| a Task of one kind | `haipipe-task`'s `ref/types.md`, then the named type skill (data, raw, description, algo, fit, eval, endpoint, individual, display, stata, agent, evidence, draft) | `1_base/task/` |
| plan a Run graph: Run Specs, dependencies, gates, routes | `haipipe-run` (`ref/workflow.md`) | `1_base/project/` |
| a Block Question, its register and its report folder | `haipipe-report` | `1_base/project/haipipe-report/` |
| write a Question's report Page | `haipipe-draft` | `1_base/draft/` |
| the stage pipelines a Task runs (data, nn, end, individual) | `haipipe-data`, `haipipe-nn`, `haipipe-end`, `haipipe-individual` | `1_base/task/<N>_<stage>/`; not part of the theme |

Read the owning skill before acting. This door coordinates an update; it does not
replace the owners' record formats, execution procedures, or acceptance rules.


Boundary
--------

- This door owns the work-theme update procedure and UI-type distinction, not a
  second folder contract or scaffold. `haipipe-block`, `haipipe-job` and
  `haipipe-task` own their levels; Run tickets and receipts keep their existing owners.
- Which `1_base/task` skills move into this theme (the kinds, the task agents)
  is still open; the table above names where each one is
  today.
- The ladder itself (what every level holds and its six Spaces) is shared by
  every theme and owned by `haipipe-project`.
