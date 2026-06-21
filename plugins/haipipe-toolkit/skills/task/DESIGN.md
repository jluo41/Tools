task — Task-Type Specialist Series (DESIGN)
==============================================

Status: v5.0.0 (2026-06-11) — 4-stage code lifecycle (Plan/Build/Execute/Report); 13 type specialists aligned
Owner:  jluo41
Scope:  task-folder lifecycle (Plan/Build/Execute/Report) + per-type scaffolding,
        mirroring the /haipipe-data and /haipipe-nn pattern.


Conceptual Layering
====================

A `project` is the umbrella for one cohesive research effort. Inside it live
the core Narrative / Probe / Task stack plus downstream export layers:

For a concrete end-to-end project shape, see
`../../blueprints/end-to-end-sandwich-run.md`.

```
📦 examples/Proj{Series}-{Cat}-{Num}-{Name}/    <- project (umbrella)
|
|-- 📁 tasks/        <- 💼 the WORK         build & run things
|-- 📁 discoveries/  <- 🔍 the OUTSIDE      sources, notes, prior art verdicts
|-- 📁 probes/       <- 📊 the CLAIMS       cross-run aggregation
|-- 📁 paper/        <- 📰 the DELIVERABLE  what we publish
|-- 📁 applications/ <- 💬 the DELIVERABLE  audience-specific reports/messages/UI
|-- 📁 insights/     <- 🧠 deferred export layer (parked for now)
```

Each core layer has its own specialist family — different sections, no overlap:

```
project umbrella     /haipipe-project              project/ (sibling)
discoveries/         /haipipe-discover             discover/
tasks/               /haipipe-task-*               task/    <- THIS SECTION
probes/              /haipipe-probe-*              probe/
insights/            /haipipe-insight-*            insight/ (deferred)

paper/               /haipipe-paper-*              paper/
applications/        /haipipe-application-*        application/
```

`project/` owns project-scope ops (the umbrella + inspect + organize + project/task-group scaffold).
`task/` owns task-scope ops — the orchestrator, 13 type specialists, and 2 shared agents.

Structure note: `1_data`, `2_nn`, `3_end`, and `4_individual` remain
top-level task-domain families. They work with `task`, but they are not being
moved under it. See `../STRUCTURE.md`.


Current State (v5.0.0)
========================

```
task/                                 <- task-scope skills (THIS SECTION)
|-- DESIGN.md                           (this file)
|-- TODO.md                             open issues + future directions
|-- CHANGELOG.md
|
|-- agents/                             🤖 shared creator-reviewer pair
|   |-- haipipe-task-creator-agent.md   produces artifacts (plan, code, report)
|   |-- haipipe-task-reviewer-agent.md  evaluates artifacts (IPO, bugs, accuracy)
|   |-- README.md
|
|-- haipipe-task/                       🧭 task orchestrator (v5.0.0)
|   |-- SKILL.md                        scope resolution + 4-stage code lifecycle dispatch
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
|-- haipipe-task-for-fit/
|-- haipipe-task-for-eval/
|-- haipipe-task-for-inference/
|-- haipipe-task-for-display/
|-- haipipe-task-for-individual/
|-- haipipe-task-for-agent/             (LOW QUALITY — see TODO.md)
|
|-- haipipe-task-for-stata/             🔧 Stata (unified — handles cms/case/data/reg internally)
```


Backbone + Add-on Architecture
=================================

The relationship is **hub-and-spoke** — haipipe-task is the hub, specialists are spokes. The hub is the recommended entry point, but any spoke can be entered directly and it reaches back to the hub for shared resources.

**haipipe-task (hub)** owns everything that is type-agnostic:

- The 4-stage code lifecycle (Plan / Build / Execute / Report)
- The creator-reviewer agent loop (`task-lifecycle.workflow.js`)
- The IPO workflow schema (`ref/workflow-template.yaml`)
- Scope resolution, routing, AUTO_MODE detection
- Shared conventions (`ref/authoring-conventions.md`, `ref/run-sh-template.sh`, `ref/hierarchy.md`)

**haipipe-task-for-xxx (spokes)** provide type-specific knowledge:

- Phase templates for this type (`ref/workflow-plan-sample.yaml`)
- Type constraints and MUST NOT rules (`SKILL.md`)
- Config seeds for new folders (`ref/config-seed.yaml`)
- Scaffold procedure (`fn/scaffold.md`)

The arrows go **both ways**. The hub reads spokes for type knowledge; spokes read the hub for shared conventions.

```
                   +------------------------------------------+
                   |         haipipe-task (hub)                |
                   |                                          |
                   |  4-stage lifecycle engine                |
                   |  creator-reviewer agent loop             |
                   |  scope resolution + routing              |
                   |  shared ref/ (templates, conventions)    |
                   +------------------------------------------+
                      |    ^       |    ^       |    ^
              reads   |    | reads |    | reads |    | reads
             type ref |    | hub   |    | hub   |    | hub
                      v    |       v    |       v    |
                   +------+    +------+    +------+
                   | eval |    | data |    |stata |    ...
                   +------+    +------+    +------+
```


Three ways to enter
--------------------

```
Path 1 — Via hub (lifecycle):   /haipipe-task <existing-path>
  hub detects type -> reads spoke's ref/ as reference -> runs 4-stage lifecycle

Path 2 — Via hub (scaffold):    /haipipe-task task-folder eval
  hub resolves type -> Skill("haipipe-task-for-eval") -> spoke runs fn/scaffold.md

Path 3 — Direct call:           /haipipe-task-for-stata <args>
  spoke runs on its own -> reads ../haipipe-task/ref/ for shared conventions
  (run-sh-template.sh, hierarchy.md, authoring-conventions.md, etc.)
```

Path 1 is the most common (lifecycle on existing tasks). Path 2 is for new task creation. Path 3 is a shortcut when you already know the type — the spoke reaches back to the hub for shared resources, so nothing is lost.

All three paths are valid. The hub is the **recommended** entry point because it handles type detection and lifecycle orchestration automatically, but direct spoke invocation works and is useful for scoped scaffolding or when the type is already known.


What the hub reads from each spoke
------------------------------------

```
Stage      | What hub reads from the spoke              | File
-----------+-------------------------------------------+-----------------------------
PLAN       | type-specific phase template               | ref/workflow-plan-sample.yaml
BUILD      | type constraints, MUST NOT rules           | SKILL.md
BUILD      | authoring guidance for this type            | fn/scaffold.md (reference)
SCAFFOLD   | config template for new folders             | ref/config-seed.yaml
SCAFFOLD   | step-by-step creation procedure             | fn/scaffold.md (executor)
INSIGHT    | none; insight export is deferred outside core task
```

What each spoke reads from the hub
------------------------------------

```
Resource                     | What the spoke gets from the hub
-----------------------------+--------------------------------------------------
ref/run-sh-template.sh       | papermill wrapper + pre-flight gate (copied to runs/)
ref/hierarchy.md             | project -> task-group -> task-folder -> run model
ref/authoring-conventions.md | cell markers, Intent docstring, config-driven rules
ref/config-meta-template.yaml| _meta block template for configs/
ref/workflow-template.yaml   | task-level IPO template (Run/Gate1/Gate2)
```

Boundary with probe / insight
==================================

task owns execution only. It does not decide what a run means for a
research claim, and it does not write narrative/probe conclusions. Discovery
work lives beside tasks in `discoveries/`; it is not a task stage.

In the sandwich model:

```
probe open     designs a research contract and dispatches discovery/task refs
discover       creates discoveries/<id> external-evidence artifacts
task           Plan / Build / Execute / Report
probe post     harvests discovery + task outputs and judges the claim
```

Task outputs are readiness signals for Probe-post: `runtime.yaml`,
`metrics.json`, `workflow/report*.yaml`, and `RUN_AUDIT.md`. A task may expose
completion status, but it should not interpret the probe or depend on
`probes/`.


The 4-Stage Lifecycle
======================

Every existing task folder goes through up to 4 stages. These stages care
about engineering: is the code correct, structured, runnable, and documented?
What the data means for delivery is handled by Probe-post and then backfilled
into paper/application lifecycle artifacts.

```
Stage 1: PLAN — the contract (what the script SHOULD do)
  creates:   workflow/plan.yaml, workflow/plan-script-<name>.yaml
  reads:     specialist's ref/workflow-plan-sample.yaml for type-specific phases
  agents:    creator drafts -> reviewer checks IPO compliance -> loop if revise

Stage 2: BUILD — the implementation (code that matches the plan)
  creates:   {NN}_{task}.py, configs/<run>.yaml, runs/<run>.sh, CODE_REVIEW.md
  reads:     specialist's SKILL.md for type constraints + MUST NOT rules
  agents:    creator writes code -> reviewer does Gate 1 code review -> loop if revise

Stage 3: EXECUTE — just run (no creation, no modification)
  generates: results/<run>/metrics.json, runtime.yaml, notebooks/<run>.ipynb
  runs:      bash runs/<run>.sh (human or autoExecute)

Stage 4: REPORT — summarize (what happened vs the plan)
  creates:   workflow/report.yaml, workflow/report-script-<name>.yaml, RUN_AUDIT.md
  reads:     workflow/plan*.yaml to mirror structure
  agents:    creator drafts -> reviewer checks accuracy -> loop if revise
```

Stages 1-4 are orchestrated by `haipipe-task/ref/task-lifecycle.workflow.js` via the Workflow tool. The creator and reviewer agents in `agents/` are paired at each stage — creator never reviews, reviewer never creates.

Task completion signal for Probe-post
-------------------------------------

When a task is part of a probe sandwich, task's job is still only to
finish execution cleanly. The handoff back to Probe-post is based on concrete
artifacts:

```
required:
  results/<run>/runtime.yaml      status=ok
  results/<run>/metrics.json      contains the metric requested by probe.yaml aggregation.metric
  workflow/report*.yaml           mirrors the plan and records what happened
  RUN_AUDIT.md                    reviewer pass/warn unless explicitly exempt

forbidden:
  task reads probes/
  task writes narrative/probe conclusions
  task decides whether the probe claim holds
```

Probe-post consumes these artifacts later and writes the probe result/claim
verdict. Insight export is deferred while the core N/P/T stack is being shaped.


Per-Specialist Responsibilities
================================

Every type specialist (add-on) owns:

```
SKILL.md                        type invariants + MUST NOT constraints (read by BUILD stage)
ref/workflow-plan-sample.yaml   type-specific IPO phases (read by PLAN stage)
ref/config-seed.yaml            config template (read by SCAFFOLD path)
fn/scaffold.md                  scaffold procedure (run by SCAFFOLD path, read by BUILD stage)
```

Shared content stays in `haipipe-task/ref/` (the backbone) and is read by all specialists. The Stata specialist keeps its `.do` config templates and workflow samples in `haipipe-task-for-stata/ref/` (including `stata-dialect.md`).


Critical Distinction: algo-dev vs training
===========================================

```
+-----------------+-------------------------------+----------------------------------+
|                 | task-algo (dev)               | task-fit (production)            |
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

Any engine=Stata request is delegated to `/haipipe-task-for-stata`, a unified specialist that owns stage disambiguation and the shared engine contract. It handles all 4 stages internally:

```
haipipe-task-for-stata           unified (handles all 4 stages internally)
  stages: cms (A) / case (B) / data (C) / reg (D)
  ref/config-seed-{stage}.do     Stata config templates (.do is source of truth)
  ref/workflow-plan-sample-{stage}.yaml
```

Engine = Stata + PowerShell + logs (NOT Python/papermill). All 4 stages share `ref/stata-dialect.md`.


Cross-Skill References
=======================

```
task-data         <->  /haipipe-data (-source / -record / -case / -aidata)
task-algo         <->  /haipipe-nn-algo (Layer 1)
task-fit          <->  /haipipe-nn-tuner + /haipipe-nn-instance (Layer 2+3)
task-eval         <->  /haipipe-end (or future eval skill)
task-inference    <->  /haipipe-end-endpointset (profile verb)
task-display      <->  (none — independent; pulls from results/<run>/)
task-individual   <->  /haipipe-individual
task-agent        <->  /claude-api (adjacent; overlap with application — see TODO.md)
task-stata        <->  (project-local .do files; no pipeline skill)
```


Group Letter Convention
========================

Group letters (A, B, C, D, ...) are **project-specific organizational prefixes**, NOT tied to task types. Each project defines its own letter scheme. The orchestrator detects type from script content analysis, not from group letters.

Historical defaults (from Phase 2, now advisory only):

```
A = training, B = evaluation, C = display, D = data, E = individual, F = agent, X = algo-dev
```


Orchestrator Routing (v5.0.0)
==============================

```
/haipipe-task plan <path>              Stage 1 only
/haipipe-task build <path>             Stage 2 only
/haipipe-task execute <path>           Stage 3 only
/haipipe-task report <path>            Stage 4 only
/haipipe-task <existing-path>          full lifecycle (all 4 stages)
/haipipe-task task-folder <type>       scaffold NEW folder via specialist
task-group scope                       -> iterate child task folders
project scope                          -> use /haipipe-project
```


Migration Plan
==============

Phase 1 — DESIGN review                                      DONE (2026-05-24)
Phase 2 — Skeleton (7 specialist directories)                 DONE (2026-05-24)
Phase 3 — Per-type content (scaffold + config-seed)           DONE (2026-05-24)
Phase 4 — Cleanup                                             DONE (2026-06-08)
  - removed legacy fn/task-folder.md from orchestrator
  - moved fn/project.md + fn/task-group.md to project/haipipe-project/fn/
Phase 5 — 4-stage lifecycle                                   DONE (2026-06-09)
  - task-lifecycle.workflow.js with creator-reviewer loop
  - workflow-plan-sample.yaml in all 13 specialists
  - haipipe-task-batch removed (batch = multiple configs in one Build)
  - haipipe-task-logging removed (superseded by Report stage)
Phase 6 — Consistency alignment                               DONE (2026-06-09)
  - all 13 specialists: unwrap prose, fix agent names, add lifecycle paragraph
  - Stata children: add workflow-plan-sample.yaml + Workflow plan section
  - agents/README.md: remove stale batch reference
Phase 7 — Insight stage proposal                               CLOSED (2026-06-19)
  - Superseded by sandwich model: task does not own insight filing.
  - probe post handles probe result/claim verdict after linked tasks complete.
  - Insight export is deferred while focusing on Narrative/Probe/Discovery/Task.
Phase 8 — Next                                                OPEN (see TODO.md)
  - rethink for-agent (low quality, overlap with application)
  - extract shared scaffold-base to reduce duplication
  - broaden for-eval to cover analysis scripts
  - resolve scaffold-vs-lifecycle tension


Downstream Consumer Contract (probe)
========================================

task artifacts are consumed by probe (the research probe pipeline). Tasks never reference probes — but probes READ task outputs alongside discovery evidence, making certain file formats a **contract**. If you change these formats, check probe/MENTAL_MODEL.md for impact.

**What probe reads from task runs:**

```
File                               Read by                  Contract
─────────────────────────────────  ───────────────────────  ────────────────────────────
results/<RUN>/metrics.json         probe-result aggregate   scalar value OR {point, ci_lower, ci_upper, N}
                                                            key must match probe's aggregation.metric
results/<RUN>/runtime.yaml         probe-result aggregate   status field (ok | failed | running)
                                   probe-review structural  git_sha, exit_code
configs/<RUN>.yaml                 probe-review structural  _meta.git_sha, AIData version
                                                            must be consistent across arms
```

**What probe creates in task (via bridge, one direction only):**

```
Artifact                           Created by               Notes
─────────────────────────────────  ───────────────────────  ────────────────────────────
new task-folders under tasks/      probe-bridge             via Skill("haipipe-task")
configs/<RUN>.yaml                 probe-bridge             wired from probe arm run_specs
runs/<RUN>.sh                      probe-bridge             generated run wrapper
CODE_REVIEW.md                     probe-bridge             pre-flight via haipipe-task-reviewer-agent (GATE 1)
```

**What probe delegates back to task:**

```
Per-run quality auditing           haipipe-task-reviewer-agent (task GATE 2)
                                   probe-review "review run" dispatches to this agent
                                   "did THIS run produce a trustworthy artifact?" is a task question
```

Full boundary rules: **probe/MENTAL_MODEL.md**.


Decision Log
============

2026-05-24  Approved: split into 7 type specialists; group letters A-F + X.
2026-06-08  Approved: 4-stage lifecycle (Plan/Build/Execute/Report) with creator-reviewer agents.
2026-06-08  Approved: move project/task-group scope to project/haipipe-project.
2026-06-09  Approved: remove haipipe-task-batch (batch = multiple configs in one Build, not a separate skill).
2026-06-09  Approved: remove haipipe-task-logging (superseded by Report stage).
2026-06-09  Approved: add Stata specialist (1 unified specialist handling all 4 stages internally).
2026-06-09  Aligned: all 13 specialists consistent with orchestrator v3 (agent names, lifecycle paragraph, IPO samples).
2026-06-11  Added: "Downstream Consumer Contract (probe)" section — makes the metrics.json / runtime.yaml / configs contract visible from C's side.
2026-06-11  Proposed: Stage 5 (Insight) after Report, filing D_data via /haipipe-insight-data.
2026-06-19  Superseded: Stage 5 removed from task. Sandwich model adopted: probe open dispatches discoveries/tasks, discover and task do their own work, probe post resumes and judges the claim. Insights deferred while focusing on Narrative/Probe/Discovery/Task.
