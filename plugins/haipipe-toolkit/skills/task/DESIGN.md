task — Task-Type Specialist Series (DESIGN)
==============================================

Status: v5.1.0 (2026-06-21). 4-stage code lifecycle (Plan/Build/Execute/Report); 13 type specialists aligned; three-axes mental model documented.
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
|-- 📁 paper/        <- 📰 the DELIVERABLE  what we publish
|-- 📁 applications/ <- 💬 the DELIVERABLE  audience-specific reports/messages/UI
```

Each core layer has its own specialist family — different sections, no overlap:

```
project umbrella     /haipipe-project              project/ (sibling)

⚙️ THE EXECUTORS — the evidence bank; neither knows a consumer exists
discoveries/         /haipipe-discovery            discover/
tasks/               /haipipe-task-*               task/    <- THIS SECTION

📄 THE CONSUMERS — they ask; each owns its own evidence questions, privately
paper/               /haipipe-paper-*              paper/
applications/        /haipipe-application-*        application/
```

The executors answer questions through ONE door each (`/haipipe-task qa`,
`/haipipe-discovery qa`) and return a PATH to a readable digest. Nothing else crosses.

`project/` owns project-scope ops (the umbrella + inspect + organize + project/task-group scaffold).
`task/` owns the inside-execution layer — the lifecycle orchestrator, task-type
specialists, shared agents, and the numbered task-domain families.

Structure note: `1_data`, `2_nn`, `3_end`, and `4_individual` now live under
`task/`. They keep their skill names and user-facing commands, but their folder
home reflects that data, NN, endpoint, and individual inference are all task
execution domains. See `../STRUCTURE.md`.


Current State (v6.0.0 — Phase 1 landed 2026-06-21)
====================================================

Phase 1 of the Target Architecture migration has landed: the nine
`haipipe-task-for-xxx` specialists are now NESTED under their numbered domain
folders (skill `name:` fields unchanged, so all `/haipipe-*` commands and
`Skill("haipipe-task-for-xxx")` calls still resolve). Phase 2 (renaming the
skills) is REJECTED by decision (2026-06-21): the names stay
`haipipe-task-for-xxx` ON PURPOSE, because the `haipipe-task-` prefix keeps each
specialist clearly part of the haipipe-task family. The migration is COMPLETE.

```
task/                                 <- task-scope skills (THIS SECTION)
|-- DESIGN.md                           (this file)
|-- TODO.md                             open issues + future directions
|-- CHANGELOG.md
|
|-- agents/                             🤖 shared orchestrator/creator/reviewer triad
|   |-- haipipe-task-orchestrator-agent.md  dispatch target, coordinates the pair
|   |-- haipipe-task-creator-agent.md   produces artifacts (plan, code, report)
|   |-- haipipe-task-reviewer-agent.md  evaluates artifacts (IPO, bugs, accuracy)
|   |-- README.md
|
|-- haipipe-task/                       🧭 task orchestrator (v5.3.0)
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
|   |   |-- task-structure.md          group/task-folder layout contract (from project, 2026-07-03)
|   |   |-- scan_status/               status-scan scripts (from project, 2026-07-03)
|   |-- fn/
|   |   |-- workflow-plan.md           procedure for Plan stage
|   |   |-- workflow-report.md         procedure for Report stage
|   |   |-- run.md                     procedure for run scaffolding
|   |   |-- workflow-audit.md          procedure for auditing
|   |   |-- task-group.md              task-group scaffold (from project, 2026-07-03)
|   |   |-- scan-status.md             cross-group status scan (from project, 2026-07-03)
|   |   |-- feedback.md + digest.md    feedback capture + session harvest
|   |-- diagram/
|       |-- 01-architecture.txt
|
|-- haipipe-workflow/                   📐 IPO plan schema + Workflow API (moved in from project/, 2026-07-03)
|
|-- 1_data/                             📊 domain 1 — data
|   |-- haipipe-data + sub-skills          run library
|   |-- haipipe-task-for-data/             task-author leg
|   |-- haipipe-task-for-raw/              raw-extraction task-author leg
|-- 2_nn/                               🧠 domain 2 — nn (algorithm design + smoke)
|   |-- haipipe-nn + sub-skills            run library (shared with fit)
|   |-- haipipe-task-for-algo/             task-author leg
|-- 3_end/                              🚀 domain 3 — endpoint
|   |-- haipipe-end + sub-skills           run library
|   |-- haipipe-task-for-endpoint/         task-author leg
|-- 4_individual/                       🧍 domain 4 — individual
|   |-- haipipe-individual + sub-skills    run library
|   |-- haipipe-task-for-individual/       task-author leg
|-- 5_fit/                              🏋️ domain 5 — fit (train); shares 2_nn's /haipipe-nn lib
|   |-- haipipe-task-for-fit/               task-author leg
|-- 6_eval/                             📈 domain 6 — eval / statistical analysis
|   |-- haipipe-task-for-eval/              task-author leg
|-- 7_display/                          🖼️ domain 7 — display (figures / tables)
|   |-- haipipe-task-for-display/           task-author leg
|-- 8_stata/                            🔩 domain 8 — stata (engine; cms/case/data/reg internal)
|   |-- haipipe-task-for-stata/             task-author leg (unified)
|-- 9_agent/                            🤖 domain 9 — agent (LLM-driven compute)
|   |-- haipipe-task-for-agent/             task-author leg
|   |-- haipipe-task-llm-engine/            LLM call engine (shared runner)
```

(Domain ids are append-only; see "Target Architecture" for the rule. ids 1-4 are
the pre-existing folders, left unchanged; 5-9 were appended.)


Three Orthogonal Axes (read this first)
=======================================

The folder tree above mixes three DIFFERENT organizing axes. They look alike
(each is "a list of things under task/") but they are not the same kind of
thing, which is exactly why some carry numbers and some do not.

```
Axis              What it is                      Ordered?    Numbered?
----------------  ------------------------------  ----------  ----------------------------
A. Lifecycle      process stages a folder runs    yes (time)  yes: 1 Plan ... 4 Report
   Plan/Build/Execute/Report
B. Task domains   pipeline layers (the engine)    yes (DAG)   yes: 1_data 2_nn 3_end 4_individual
   1_data / 2_nn / 3_end / 4_individual
C. Type spokes    classification of a folder      no (enum)   no: for-data, for-eval, ...
   haipipe-task-for-xxx
```

A and B carry numbers because their position carries meaning:

  - A is temporal. You cannot Build before you Plan; the order is the process.
  - B is a data-flow DAG. 1_data produces AIData, fed to 2_nn for training, fed
    to 3_end for deployment, used by 4_individual for inference. The number
    encodes the dependency order.

C is NOT sequenced. It is a type ENUM. The hub detects ONE type per task-folder
and routes to that single spoke. A project may run only display tasks, or only
eval tasks, in any order; there is no canonical "for-data then for-algo then
..." pipeline. Numbering C would:

  1. imply a false ordering that no project actually follows;
  2. break whenever a new type is added (the whole set re-numbers);
  3. collide with the 1/2/3/4 already used by axes A and B, putting three
     competing number lines inside one folder.

Rule of thumb: number a thing only when its position carries meaning. Lifecycle
stages and pipeline layers have meaningful positions; task types do not.


B and C overlap by domain, not by identity
-------------------------------------------

The type spokes (C) pair with the task domains (B) by subject matter, but they
are two LAYERS, not duplicates:

```
domain (B): pipeline engine          type spoke (C): how to author a task-folder
1_data       /haipipe-data       <->  for-data
2_nn         /haipipe-nn         <->  for-algo, for-fit
3_end        /haipipe-end        <->  for-endpoint, for-eval
4_individual /haipipe-individual <->  for-individual
(no domain)                      <->  for-display, for-agent, for-stata
```

  - A domain (B) is the pipeline primitive itself: build a SourceSet, train a
    model, deploy an endpoint. It is a standalone, user-facing umbrella skill.
  - A type spoke (C) is the lifecycle hub's knowledge of how to scaffold, build,
    and lint a TASK-FOLDER that exercises that primitive (scaffold.md,
    config-seed.yaml, workflow-plan-sample.yaml, type constraints).

So C is keyed by the same subjects as B, but it lives on the authoring side and
is consumed by the hub at the Plan / Build / Scaffold steps.

NOTE (2026-06-21): the analysis above is kept because it is the reasoning that
LED to the decision below. The decision went the other way. Rather than keep C
as a separate unnumbered enum, we DISSOLVE C into B and give every task kind a
numbered domain. See "Target Architecture" next. The "Backbone + Add-on" /
hub-spoke / for-xxx sections that follow described the PRE-MIGRATION on-disk
state and are kept as history; the migration landed 2026-06-21.


Target Architecture: B as the Unified Domain Family (v6.0.0, LANDED 2026-06-21)
=====================================================================

Decided 2026-06-21; Phase 1 landed the same day (see Current State above).
SUPERSEDED the hub-and-spoke "for-xxx type spoke" model.

Decision: dissolve axis C (the `haipipe-task-for-xxx` spokes) into axis B. B
becomes the single, flat, NUMBERED family of task DOMAINS. There is no parallel
type-spoke family. Each domain owns both legs:

  - run / library leg   the pipeline capability (e.g. /haipipe-data)
  - task-author leg     how to scaffold/build/lint a task-folder of this kind
                        (the content that used to live in haipipe-task-for-xxx)

Numbering rule (APPEND-ONLY)
----------------------------
This family will keep growing, so the numbering is append-only and NEVER
renumbered.

  - id = creation order, PERMANENT. A domain keeps its number forever. A new
    domain takes the next free integer and is appended; nothing is renumbered,
    so no existing folder or reference ever moves because of a new domain.
  - id does NOT encode flow position. The pipeline-flow order is a SEPARATE
    documented attribute (the "flow group" below), carried in prose, not in the
    number. ids 1-4 are the pre-existing folders, left unchanged; 5+ are
    appended in the order we add them.

Founding assignment keeps existing folders fixed (data=1, nn=2, endpoint=3,
individual=4) and appends the rest (fit=5, eval=6, display=7, stata=8, agent=9).
The alternative (a one-time renumber so ids match flow order) was rejected: it
buys a tidy base once but contradicts the append-only rule the day we add the
next domain.

Coverage rule (relaxed, per 2026-06-21)
---------------------------------------
Domains do NOT need clean, non-overlapping boundaries. Overlap is fine. The only
requirement is COVERAGE: every task type must fall into exactly one domain. When
a task could fit two domains, pick one and move on. Do not redesign the taxonomy
to remove an overlap.

The nine domains
----------------
Listed in id order (= creation order). The "flow" column is the SEPARATE
pipeline-order attribute, not the id.
```
id  domain      flow         role                         output                     run library / engine
--  ----------  -----------  ---------------------------  -------------------------  -------------------------
1   data        flow         build data                   AIData -> store 1-4        /haipipe-data · python
2   nn          flow         algorithm design + smoke     runs + 1 loss (no durable) /haipipe-nn (algo side) · python
3   endpoint    flow         package + deploy             endpoint -> store 6        /haipipe-end · python
4   individual  flow         per-subject inference        inference                  /haipipe-individual · python
5   fit         flow         real train + sweep           checkpoint -> store 5      /haipipe-nn (tuner/instance) · python
6   eval        flow         eval / statistical analysis  metrics / tables           (new; none yet) · python
7   display     flow         figures / tables             figure / table             (none; reads results/) · python
8   stata       cross-cut    full Stata-engine work       by internal stage          standalone (no python lib) · stata
9   agent       cross-cut    LLM-driven compute           results / metrics          /claude-api · LLM
```

Pipeline-flow order (independent of id):
  data(1) -> nn(2) -> fit(5) -> endpoint(3) -> eval(6) -> display(7) -> individual(4)
  cross-cutting (no flow position): stata(8), agent(9)

nn (2) and fit (5) are the ONLY two domains sharing one underlying library
(/haipipe-nn): nn draws on the algo side, fit on the tuner+instance side. This
is the concrete meaning of "fit belongs to nn." agent (9) is scoped to LLM
compute that produces task evidence (results/metrics); audience-facing delivery
stays in the application family, not here.

for-xxx -> domain mapping
-------------------------
Each `haipipe-task-for-xxx` becomes the task-author leg of one domain:
```
for-data       -> 1 data          for-display    -> 7 display
for-algo       -> 2 nn            for-stata      -> 8 stata
for-endpoint   -> 3 endpoint      for-agent      -> 9 agent
for-individual -> 4 individual
for-fit        -> 5 fit
for-eval       -> 6 eval
```

Migration plan
--------------
Blast radius (measured 2026-06-21): ~40 files reference the old for-xxx names.
MOST are skill-NAME references (invocations) that survive a folder move because
skill identity is the `name:` field, not the folder path (see ../STRUCTURE.md).
Only folder-PATH citations need editing. for-stata's 19 hits are mostly internal
self-references that move with the folder.

```
Phase 1 (low-risk: folders only, skill names UNCHANGED, append-only)
  1. Existing run-library folders are LEFT UNCHANGED: 1_data, 2_nn, 3_end,
     4_individual keep their numbers (they are domains 1-4). No renumber.
  2. Append 5 NEW domain folders: 5_fit, 6_eval, 7_display, 8_stata, 9_agent.
  3. git mv each haipipe-task-for-xxx into its domain folder (NO rename):
     for-data->1_data, for-algo->2_nn, for-endpoint->3_end,
     for-individual->4_individual, for-fit->5_fit, for-eval->6_eval,
     for-display->7_display, for-stata->8_stata, for-agent->9_agent.
  4. Fix folder-PATH references only (DESIGN, STRUCTURE, orchestrator prose,
     agents, diagram). /haipipe-* command + Skill("haipipe-task-for-xxx") calls
     keep working untouched.
  5. Update the orchestrator to think in "domain id" terms for routing.

Phase 2 (REJECTED 2026-06-21: names stay haipipe-task-for-xxx)
  Renaming was considered and dropped. The skills KEEP the haipipe-task-for-xxx
  names on purpose: the haipipe-task- prefix signals membership in the
  haipipe-task family, and a rename buys zero functional gain for a risky atomic
  sweep of ~40 references. The migration ends at Phase 1.
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

Boundary: the task layer is CONSUMER-UNAWARE
=============================================

task owns EXECUTION. It does not decide what a run means for anyone's argument, and it
writes no conclusions on anyone's behalf. Discovery is its SIBLING, not its superior:
task and discovery are the two EXECUTORS — same shape, same rules, one runs code, the
other reads the outside world.

```
   ⚙️ THE EXECUTORS                        📄 SOMEWHERE ELSE
   tasks/       code, runs, metrics        a consumer, weeks apart
   discoveries/ literature, prior art      it asks. That is all we ever see of it.
```

Nothing under `tasks/` names a consumer, points at one, or is shaped by one. There is no
mailbox, no id, no return field. That is not an accident of layering — it is what makes a
result REUSABLE: evidence shaped by one consumer's frame is evidence the next one cannot
use.

TWO SESSION MODES:

```
   PRIMARY        autonomous Plan → Build → Execute → Report. No question pending, no ask.
                  This IS the project's research, and the bank grows here.
   ANSWERABILITY  also task-native, also with no question pending: write readable digests
                  for findings worth digesting, and build code so FUTURE questions are
                  cheap. We do not know which questions will come. We make the bank
                  easier to ask.
```

THE ONE DOOR IN — the `qa` verb (`haipipe-task/fn/qa.md`). A question arrives as ONE
QUESTION IN GENERAL LANGUAGE and nothing else. The verb answers it (① QA SCAN → ② DIGEST →
③ P-B-E-R at the shallowest depth) or REFUSES it, and returns a path to
`<task-folder>/QA/<n>-<slug>.md`. It never learns who asked or why, and must not try to find out.

The pen never leaves this layer: WE write the QA file. A file in this bank authored by an
outsider carries the outsider's vocabulary — that is exactly how a task result on disk
today ended up asserting a consumer's claim ids.


The 4-Stage Lifecycle
======================

Every existing task folder goes through up to 4 stages. These stages care
about engineering: is the code correct, structured, runnable, and documented?
What the numbers MEAN for some downstream argument is not decided here, and
never has been.

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

What a finished task leaves behind
-----------------------------------

A task's job is to finish execution CLEANLY and stop. It leaves concrete artifacts, and
whoever reads them later does so on their own schedule, without us knowing:

```
required:
  results/<run>/runtime.yaml      status=ok
  results/<run>/metrics.json      the measured numbers, under stable keys
  workflow/report*.yaml           mirrors the plan and records what happened
  RUN_AUDIT.md                    reviewer pass/warn unless explicitly exempt

optional:
  QA/<n>-<slug>.md                the READABLE digest of a direction this task-folder explored.
                                  Three reasons only: a question arrived · results/ already
                                  answered one but no digest existed · we judged a finding
                                  worth digesting. A QA/ mirroring every result is noise.

forbidden:
  reading a consumer's files, of any kind
  writing conclusions on anyone's behalf
  deciding whether someone's claim holds
  putting an external id, a claim id, or a hypothesis id in ANY file under tasks/
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


The read surface (what a later reader can rely on)
==================================================

A task never references anyone downstream. But its outputs ARE read later — by a future
task session, by a cross-run comparison, by a QA digest, by a human — which makes certain
file FORMATS a contract. Change them deliberately.

```
File                          Guarantee
────────────────────────────  ──────────────────────────────────────────────────────────
results/<RUN>/metrics.json    the measured numbers under STABLE KEYS. Scalar, or
                              {point, ci_lower, ci_upper, N}. Keys are the contract —
                              a renamed key silently breaks every reader.
                              (schema: haipipe-task/ref/metrics-json-schema.md)
results/<RUN>/runtime.yaml    machine facts: status (ok|failed|running), git_sha, exit_code
configs/<RUN>.yaml            frozen parameters + _meta.git_sha — what this run actually ran
workflow/report*.yaml         the plan, mirrored, filled with what happened
RUN_AUDIT.md                  Gate 2: did THIS run produce a trustworthy artifact?
QA/<n>-<slug>.md              OPTIONAL. The readable digest: # Q / ## Answer (with
                              [→ results/…] anchors) / ## Caveats / ## Not-done.
                              Numbering IS the index. Write-once. Slug only.
```

WRITER RULE — every one of these files has exactly ONE writer: THIS LAYER. Nothing outside
the task layer writes anything under `tasks/`. Not a config, not a run script, not a QA
file. A caller that needs work done here DISPATCHES it —
`Agent(haipipe-task-orchestrator-agent)`, clean context, one question or one spec — and
reads the result afterwards. It does not reach in.

The reverse direction does not exist. There is no field pointing outward, no id, no
notification, no back-reference. The question comes in through `fn/qa.md`; a PATH goes
back; the conversation is over.


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
2026-06-21  Documented: three orthogonal axes (lifecycle / task domains / type spokes). Type spokes stay an unnumbered enum by design; only lifecycle stages and pipeline domains are numbered, because only they are sequenced.
2026-06-21  Approved (supersedes the line above): dissolve C (for-xxx spokes) into B. B becomes a single flat NUMBERED domain family of 9 domains; every task kind gets a stable domain id. Coverage over clean boundaries: overlap is fine, every task type must fall into exactly one domain. nn and fit split but share /haipipe-nn. stata and agent are their own domains. Migration staged: Phase 1 folder move with skill names unchanged, Phase 2 optional rename. See "Target Architecture" section.
2026-07-14  Approved (Tools/plugins/haipipe-toolkit/diagram/260714-probe-qa/ v3, rulings R1-R18): the task layer is CONSUMER-UNAWARE, but not question-deaf. DELETED: _ASK/ stubs, _ANS/, the `answers:` report field, external ids anywhere under tasks/, and the probe-aware `asks` verb. ADDED: the `qa` verb (fn/qa.md) — one question in general language in, a path to <task-folder>/QA/<n>-<slug>.md out; gate ① QA SCAN ② DIGEST ③ P-B-E-R at the shallowest depth (read | new run | new script | new task-folder), or REFUSE. ADDED: the OPTIONAL QA/ folder — the task-folder's readable, numbered map of the directions it has explored; authored by THIS layer at Report; three reasons only; no consumer vocabulary. AFFIRMED: the task session's PRIMARY mode is autonomous P-B-E-R with no question pending, and answerability work (digests + code that makes future questions cheap) is task-native. Supersedes the "sandwich model" (2026-06-19) and the "Downstream Consumer Contract" (2026-06-11) entries below.
2026-06-21  Decided: Phase 2 (rename for-xxx skills) REJECTED. Names stay haipipe-task-for-xxx by design; the haipipe-task- prefix keeps each specialist clearly inside the haipipe-task family. Migration is complete at Phase 1 (folder nesting). No skill rename.
2026-06-21  Refined (per "we will keep adding domains"): numbering is APPEND-ONLY, never renumbered. id = creation order, permanent; pipeline-flow order is a separate documented attribute, not the id. Founding assignment keeps existing folders fixed (data=1, nn=2, endpoint=3, individual=4) and appends fit=5, eval=6, display=7, stata=8, agent=9. New domains take the next integer; Phase 1 touches zero existing folders. Rejected the one-time tidy renumber as inconsistent with append-only.
