C_task — Task-Type Specialist Series (DESIGN)
==============================================

Status: v3.0.0 (2026-06-09) — 4-stage lifecycle with creator-reviewer agents; 13 type specialists aligned
Owner:  jluo41
Scope:  task-folder lifecycle (Plan/Build/Execute/Report) + per-type scaffolding,
        mirroring the /haipipe-data and /haipipe-nn pattern.


Conceptual Layering
====================

A `project` is the umbrella for one cohesive research effort. Inside it live THREE parallel worlds:

```
📦 examples/Proj{Series}-{Cat}-{Num}-{Name}/    <- project (umbrella)
|
|-- 📁 tasks/        <- 💼 the WORK         build & run things
|-- 📁 paper/        <- 📰 the DELIVERABLE  what we publish
|-- 📁 probes/       <- 📊 the CLAIMS       cross-run aggregation
|-- 📁 insights/     <- 🧠 the KNOWLEDGE    DIKW cards from probes
```

Each world has its own specialist family — different sections, no overlap:

```
project umbrella     /haipipe-project              B_project/ (sibling)
tasks/               /haipipe-task-*               C_task/    <- THIS SECTION
paper/               /haipipe-paper-*              F_paper/
probes/              /haipipe-probe-*              D_probe/
insights/            /haipipe-insight-*            E_insight/
```

`B_project/` owns project-scope ops (the umbrella + inspect + organize + project/task-group scaffold).
`C_task/` owns task-scope ops — the orchestrator, 13 type specialists, and 2 shared agents.


Current State (v3.0.0)
========================

```
C_task/                                 <- task-scope skills (THIS SECTION)
|-- DESIGN.md                           (this file)
|-- TODO.md                             open issues + future directions
|-- CHANGELOG.md
|
|-- agents/                             🤖 shared creator-reviewer pair
|   |-- haipipe-task-creator-agent.md   produces artifacts (plan, code, report)
|   |-- haipipe-task-reviewer-agent.md  evaluates artifacts (IPO, bugs, accuracy)
|   |-- README.md
|
|-- haipipe-task/                       🧭 task orchestrator (v3.0.0)
|   |-- SKILL.md                        scope resolution + 4-stage lifecycle dispatch
|   |-- ref/
|   |   |-- task-lifecycle.workflow.js  Workflow tool script for the 4-stage loop
|   |   |-- hierarchy.md               project -> task-group -> task-folder -> run
|   |   |-- authoring-conventions.md   cell markers, Intent docstring, config-driven
|   |   |-- workflow-template.yaml     task-level IPO template (Run/Gate1/Gate2)
|   |   |-- run-sh-template.sh         papermill wrapper + pre-flight gate
|   |   |-- config-meta-template.yaml  _meta block template
|   |   |-- metrics-json-schema.md     CI-aware metrics format
|   |   |-- runtime-yaml-schema.md     run status format
|   |   |-- intent-docstring-template.py
|   |   |-- invocation-modes.md        interactive vs headless
|   |-- fn/
|   |   |-- workflow-plan.md           procedure for Plan stage
|   |   |-- workflow-report.md         procedure for Report stage
|   |   |-- run.md                     procedure for run scaffolding
|   |   |-- workflow-audit.md          procedure for auditing
|   |-- diagram/
|       |-- 01-architecture.txt
|
|-- haipipe-task-for-data/              🔧 Python specialists (8)
|-- haipipe-task-for-algo/
|-- haipipe-task-for-training/
|-- haipipe-task-for-eval/
|-- haipipe-task-for-inference/
|-- haipipe-task-for-display/
|-- haipipe-task-for-individual/
|-- haipipe-task-for-agent/             (LOW QUALITY — see TODO.md)
|
|-- haipipe-task-for-stata/             🔧 Stata sub-family (5)
|   |-- haipipe-task-for-stata-cms/     1-CMS-Store (per year)
|   |-- haipipe-task-for-stata-case/    2-Case-Store (cohort x year)
|   |-- haipipe-task-for-stata-data/    *-Data-Store (cross-year)
|   |-- haipipe-task-for-stata-reg/     results/ (LIGHT coef tables)
```


The 4-Stage Lifecycle
======================

Every existing task folder goes through 4 stages. Each stage has strict file ownership.

```
Stage 1: PLAN — the contract (what the script SHOULD do)
  creates:   workflow/plan.yaml, workflow/plan-script-<name>.yaml
  agents:    creator drafts -> reviewer checks IPO compliance -> loop if revise

Stage 2: BUILD — the implementation (code that matches the plan)
  creates:   {NN}_{task}.py, configs/<run>.yaml, runs/<run>.sh, CODE_REVIEW.md
  agents:    creator writes code -> reviewer does Gate 1 code review -> loop if revise

Stage 3: EXECUTE — just run (no creation, no modification)
  generates: results/<run>/metrics.json, runtime.yaml, notebooks/<run>.ipynb
  runs:      bash runs/<run>.sh (human or autoExecute)

Stage 4: REPORT — summarize (what happened vs the plan)
  creates:   workflow/report.yaml, workflow/report-script-<name>.yaml, RUN_AUDIT.md
  agents:    creator drafts -> reviewer checks accuracy -> loop if revise
```

Orchestrated by `haipipe-task/ref/task-lifecycle.workflow.js` via the Workflow tool. The creator and reviewer agents in `agents/` are paired at each stage — creator never reviews, reviewer never creates.


Two Paths Through the System
==============================

**Path 1: NEW task (scaffold)**

```
/haipipe-task task-folder <type>
  -> orchestrator resolves type (Step 3a)
  -> Skill("haipipe-task-for-<type>") — specialist runs fn/scaffold.md
  -> folder created, ready for lifecycle
```

The specialist IS the executor. It creates dirs, seeds configs, returns the contract.

**Path 2: EXISTING task (lifecycle)**

```
/haipipe-task <existing-task-folder-path>
  -> orchestrator detects existing folder (Step 2)
  -> Workflow(task-lifecycle.workflow.js)
  -> creator agent reads specialist's ref/workflow-plan-sample.yaml (Plan stage)
  -> creator agent reads specialist's SKILL.md (Build stage)
  -> 4-stage creator-reviewer loop
```

The specialist is a REFERENCE LIBRARY. The workflow never calls the specialist as a Skill — the creator agent reads its files directly for type-specific guidance.


Per-Specialist Responsibilities
================================

Every type specialist owns:

```
SKILL.md                        entry + type invariants + group-letter default + MUST NOT
ref/config-seed.yaml            YAML template seeded into configs/ (scaffold path)
ref/workflow-plan-sample.yaml   type-specific IPO phases (lifecycle path)
fn/scaffold.md                  scaffold flow + cross-skill links (scaffold path)
```

Shared content stays in `haipipe-task/ref/` and is read by all type specialists. The Stata sub-family additionally shares `haipipe-task-for-stata/ref/stata-dialect.md`.


Critical Distinction: algo-dev vs training
===========================================

```
+-----------------+-------------------------------+----------------------------------+
|                 | task-algo (dev)               | task-training (production)       |
+-----------------+-------------------------------+----------------------------------+
| Purpose         | verify the algorithm runs     | train a real model + sweep       |
|                 | end-to-end (smoke test)       |                                  |
| Config scale    | minimal (1-batch / tiny)      | full hyperparam grid             |
| Runtime         | minutes                       | hours-to-days                    |
| Outputs         | "didn't crash" + 1 loss val   | checkpoint -> _WorkSpace/5       |
| Pipeline skill  | /haipipe-nn-algo              | /haipipe-nn-tuner + -instance    |
+-----------------+-------------------------------+----------------------------------+
```


Stata Sub-Family
=================

Any engine=Stata request is delegated to `/haipipe-task-for-stata`, which owns stage disambiguation and the shared engine contract. It routes to one of 4 children:

```
haipipe-task-for-stata           sub-orchestrator (router)
  |-- haipipe-task-for-stata-cms     A: 1-CMS-Store (heavy, per year)
  |-- haipipe-task-for-stata-case    B: 2-Case-Store (heavy, cohort x year)
  |-- haipipe-task-for-stata-data    C: *-Data-Store (heavy, cross-year)
  |-- haipipe-task-for-stata-reg     D: results/ (LIGHT coef tables)
```

Engine = Stata + PowerShell + logs (NOT Python/papermill). All children share `ref/stata-dialect.md`.


Cross-Skill References
=======================

```
task-data         <->  /haipipe-data (-source / -record / -case / -aidata)
task-algo         <->  /haipipe-nn-algo (Layer 1)
task-training     <->  /haipipe-nn-tuner + /haipipe-nn-instance (Layer 2+3)
task-eval         <->  /haipipe-end (or future eval skill)
task-inference    <->  /haipipe-end-endpointset (profile verb)
task-display      <->  (none — independent; pulls from results/<run>/)
task-individual   <->  /haipipe-individual
task-agent        <->  /claude-api (adjacent; overlap with G_application — see TODO.md)
task-stata-*      <->  (project-local .do files; no pipeline skill)
```


Group Letter Convention
========================

Group letters (A, B, C, D, ...) are **project-specific organizational prefixes**, NOT tied to task types. Each project defines its own letter scheme. The orchestrator detects type from script content analysis, not from group letters.

Historical defaults (from Phase 2, now advisory only):

```
A = training, B = evaluation, C = display, D = data, E = individual, F = agent, X = algo-dev
```


Orchestrator Routing (v3.0.0)
==============================

```
/haipipe-task plan <path>              Stage 1 only
/haipipe-task build <path>             Stage 2 only
/haipipe-task execute <path>           Stage 3 only
/haipipe-task report <path>            Stage 4 only
/haipipe-task <existing-path>          full lifecycle (all 4 stages)
/haipipe-task task-folder <type>       scaffold NEW folder via specialist
project / task-group scope             -> redirect to /haipipe-project
```


Migration Plan
==============

Phase 1 — DESIGN review                                      DONE (2026-05-24)
Phase 2 — Skeleton (7 specialist directories)                 DONE (2026-05-24)
Phase 3 — Per-type content (scaffold + config-seed)           DONE (2026-05-24)
Phase 4 — Cleanup                                             DONE (2026-06-08)
  - removed legacy fn/task-folder.md from orchestrator
  - moved fn/project.md + fn/task-group.md to B_project/haipipe-project/fn/
Phase 5 — 4-stage lifecycle                                   DONE (2026-06-09)
  - task-lifecycle.workflow.js with creator-reviewer loop
  - workflow-plan-sample.yaml in all 13 specialists
  - haipipe-task-batch removed (batch = multiple configs in one Build)
  - haipipe-task-logging removed (superseded by Report stage)
Phase 6 — Consistency alignment                               DONE (2026-06-09)
  - all 13 specialists: unwrap prose, fix agent names, add lifecycle paragraph
  - Stata children: add workflow-plan-sample.yaml + Workflow plan section
  - agents/README.md: remove stale batch reference
Phase 7 — Next                                                OPEN (see TODO.md)
  - rethink for-agent (low quality, overlap with G_application)
  - extract shared scaffold-base to reduce duplication
  - broaden for-eval to cover analysis scripts
  - resolve scaffold-vs-lifecycle tension


Decision Log
============

2026-05-24  Approved: split into 7 type specialists; group letters A-F + X.
2026-06-08  Approved: 4-stage lifecycle (Plan/Build/Execute/Report) with creator-reviewer agents.
2026-06-08  Approved: move project/task-group scope to B_project/haipipe-project.
2026-06-09  Approved: remove haipipe-task-batch (batch = multiple configs in one Build, not a separate skill).
2026-06-09  Approved: remove haipipe-task-logging (superseded by Report stage).
2026-06-09  Approved: add Stata sub-family (5 specialists: parent router + 4 stage children).
2026-06-09  Aligned: all 13 specialists consistent with orchestrator v3 (agent names, lifecycle paragraph, IPO samples).
