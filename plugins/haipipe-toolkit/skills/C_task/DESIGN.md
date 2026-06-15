C_task — Task-Type Specialist Series (DESIGN)
==============================================

Status: v4.0.0 (2026-06-11) — 5-stage lifecycle (Plan/Build/Execute/Report/Insight); 13 type specialists aligned
Owner:  jluo41
Scope:  task-folder lifecycle (Plan/Build/Execute/Report/Insight) + per-type scaffolding,
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
narratives/
tasks/               /haipipe-task-*               C_task/    <- THIS SECTION
probes/              /haipipe-probe-*              D_probe/
insights/            /haipipe-insight-*            E_insight/

paper/               /haipipe-paper-*              F_paper/
```

`B_project/` owns project-scope ops (the umbrella + inspect + organize + project/task-group scaffold).
`C_task/` owns task-scope ops — the orchestrator, 13 type specialists, and 2 shared agents.


Current State (v4.0.0)
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
|-- haipipe-task/                       🧭 task orchestrator (v4.0.0)
|   |-- SKILL.md                        scope resolution + 5-stage lifecycle dispatch
|   |-- ref/
|   |   |-- task-lifecycle.workflow.js  Workflow tool script for the 5-stage loop
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

- The 5-stage lifecycle (Plan / Build / Execute / Report / Insight)
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
                   |  5-stage lifecycle engine                |
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
  hub detects type -> reads spoke's ref/ as reference -> runs 5-stage lifecycle

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
INSIGHT    | (none — hub checks type eligibility, then calls E_insight directly)
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

What the hub reads from E_insight (cross-layer)
-------------------------------------------------

The Insight stage is the one place where C_task crosses into E_insight:

```
Resource                                 | What the hub reads / calls
-----------------------------------------+--------------------------------------------------
E_insight/haipipe-insight-data/SKILL.md  | Skill() call to file D_data observation card
E_insight/ref/insight-md-schema.md       | card schema (what fields the D card must have)
E_insight/agents/card-reviewer-data-agent| validates the filed card (accuracy + boundary)
insights/D_data/                         | checks existing card count for I-level suggestion
```


Two Lifecycles in One Pipeline
================================

The 5 stages serve two distinct purposes:

```
Plan / Build / Execute / Report   =   CODE lifecycle    "is the implementation right?"
Insight                           =   DATA lifecycle    "what did we learn from the data?"
```

Stages 1-4 care about the engineering: is the code correct, structured, runnable, documented? Stage 5 captures what the data actually told us — independent of the code that produced it. You can only say what you learned after you've run the code and verified the results, which is why Insight comes last.


The 5-Stage Lifecycle
======================

Every existing task folder goes through up to 5 stages. Stages 1-4 are the code lifecycle (always applicable). Stage 5 is optional — it only fires for insight-worthy task types that have produced results.

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

Stage 5: INSIGHT — what did the data teach us? (optional, insight-worthy types only)
  creates:   insights/D_data/D{NN}_{slug}.md (D-level observation card)
  reads:     results/<run>/metrics.json, workflow/report*.yaml, workflow/plan*.yaml
  calls:     Skill("haipipe-insight-data") to file the observation card
  review:    card-reviewer-data-agent validates the card (from E_insight/agents/)
  suggests:  if enough D cards in this task-group, suggest /haipipe-insight information
```

Stages 1-4 are orchestrated by `haipipe-task/ref/task-lifecycle.workflow.js` via the Workflow tool. The creator and reviewer agents in `agents/` are paired at each stage — creator never reviews, reviewer never creates.

Stage 5 crosses into E_insight territory — it calls `/haipipe-insight-data` to file the observation card and uses `card-reviewer-data-agent` (from E_insight/agents/) to validate it. This is the only stage where C_task writes to `insights/`.


Insight stage: when it fires, when it skips
---------------------------------------------

Not every task produces insight-worthy observations. The Insight stage fires only when:

1. **Results exist** — `results/<run>/metrics.json` must be present (Execute must have run).
2. **Task type is insight-worthy** — the task produces interpretable, quantitative results.

```
Task type     Insight stage?    Why
-----------   ---------------   ---
eval          YES               scored metrics — the core use case
fit           YES               training loss, convergence, validation curves
display       MAYBE             only if it produces quantitative summaries (not just plots)
stata-reg     YES               regression coefficients, standard errors, p-values
stata-data    YES               descriptive statistics, coverage counts
data          NO                builds a dataset — no interpretable outcome
algo          NO                smoke test — "didn't crash" is not an observation
individual    NO                single-subject view — too narrow for KB
agent         NO                LLM session output — not quantitative
inference     NO                profiling numbers, not domain findings
```

When the stage fires, it files a single D_data observation card capturing what the task run produced. D cards are the atomic unit of E_insight — they record "what we observed" without interpretation. Higher DIKW levels accumulate from D cards over time:

```
D (observation)    filed automatically by Insight stage    "task X produced metric A = 0.85"
I (pattern)        filed when enough D cards accumulate    "5 eval tasks all show the same trend"
K (knowledge)      filed when a probe confirms a claim     stays in D_probe's lane
W (wisdom)         filed from K cards                      stays in G_application's lane
```


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
task-agent        <->  /claude-api (adjacent; overlap with G_application — see TODO.md)
task-stata        <->  (project-local .do files; no pipeline skill)
```


Group Letter Convention
========================

Group letters (A, B, C, D, ...) are **project-specific organizational prefixes**, NOT tied to task types. Each project defines its own letter scheme. The orchestrator detects type from script content analysis, not from group letters.

Historical defaults (from Phase 2, now advisory only):

```
A = training, B = evaluation, C = display, D = data, E = individual, F = agent, X = algo-dev
```


Orchestrator Routing (v4.0.0)
==============================

```
/haipipe-task plan <path>              Stage 1 only
/haipipe-task build <path>             Stage 2 only
/haipipe-task execute <path>           Stage 3 only
/haipipe-task report <path>            Stage 4 only
/haipipe-task insight <path>           Stage 5 only (files D card if results exist + type eligible)
/haipipe-task <existing-path>          full lifecycle (all 5 stages)
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
Phase 7 — Insight stage                                       OPEN (2026-06-11)
  - Add Stage 5 (Insight) to task-lifecycle.workflow.js
  - Type eligibility check (eval, fit, stata-reg, stata-data → yes; data, algo, etc. → skip)
  - Calls Skill("haipipe-insight-data") to file D_data observation card
  - card-reviewer-data-agent validates the card
  - Suggest I-level synthesis when enough D cards accumulate in a task-group
  - Update haipipe-task SKILL.md, architecture diagram, Excalidraw canvas
Phase 8 — Next                                                OPEN (see TODO.md)
  - rethink for-agent (low quality, overlap with G_application)
  - extract shared scaffold-base to reduce duplication
  - broaden for-eval to cover analysis scripts
  - resolve scaffold-vs-lifecycle tension


Downstream Consumer Contract (D_probe)
========================================

C_task artifacts are consumed by D_probe (the research probe pipeline). Tasks never reference probes — but probes READ task outputs, making certain file formats a **contract**. If you change these formats, check D_probe/MENTAL_MODEL.md for impact.

**What D_probe reads from C_task runs:**

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

**What D_probe creates in C_task (via bridge, one direction only):**

```
Artifact                           Created by               Notes
─────────────────────────────────  ───────────────────────  ────────────────────────────
new task-folders under tasks/      probe-bridge             via Skill("haipipe-task")
configs/<RUN>.yaml                 probe-bridge             wired from probe arm run_specs
runs/<RUN>.sh                      probe-bridge             generated run wrapper
CODE_REVIEW.md                     probe-bridge             pre-flight via haipipe-task-reviewer-agent (GATE 1)
```

**What D_probe delegates back to C_task:**

```
Per-run quality auditing           haipipe-task-reviewer-agent (C_task GATE 2)
                                   probe-review "review run" dispatches to this agent
                                   "did THIS run produce a trustworthy artifact?" is a C_task question
```

Full boundary rules: **D_probe/MENTAL_MODEL.md**.


Decision Log
============

2026-05-24  Approved: split into 7 type specialists; group letters A-F + X.
2026-06-08  Approved: 4-stage lifecycle (Plan/Build/Execute/Report) with creator-reviewer agents.
2026-06-08  Approved: move project/task-group scope to B_project/haipipe-project.
2026-06-09  Approved: remove haipipe-task-batch (batch = multiple configs in one Build, not a separate skill).
2026-06-09  Approved: remove haipipe-task-logging (superseded by Report stage).
2026-06-09  Approved: add Stata specialist (1 unified specialist handling all 4 stages internally).
2026-06-09  Aligned: all 13 specialists consistent with orchestrator v3 (agent names, lifecycle paragraph, IPO samples).
2026-06-11  Added: "Downstream Consumer Contract (D_probe)" section — makes the metrics.json / runtime.yaml / configs contract visible from C's side.
2026-06-11  Approved: Stage 5 (Insight) — after Report, file a D_data observation card via /haipipe-insight-data for insight-worthy task types. Captures what the DATA taught us, not what the CODE did. Only fires when results exist + type is eligible (eval, fit, stata-reg, stata-data). First cross-layer call from C_task into E_insight.
