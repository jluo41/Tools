---
name: haipipe-task
description: "Task-folder and task-group orchestrator. For a task-folder: runs the 4-stage code lifecycle (Plan → Build → Execute → Report) or dispatches to type specialists for scaffolding. For a task-group: iterates over each child task-folder and runs the lifecycle on each one. For insight (filing D_data observation cards from results), use /haipipe-insight with the task-folder path."
argument-hint: "[scope] [args...]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill, Workflow
metadata:
  version: "5.0.0"
  last_updated: "2026-06-11"
  summary: "Build orchestrator with 4-stage code lifecycle for task-folders and task-groups."
  changelog:
    - "1.0.0 (2026-05-31): baseline metadata added."
    - "2.0.0 (2026-06-08): add workflow lifecycle — audit, plan, report. New fn/ procedures. New ref: workflow-template.yaml."
    - "2.1.0 (2026-06-08): three-layer plans; per-script IPO; Stata four-sister; wire reviewer+auditor agents."
    - "3.0.0 (2026-06-09): 4-stage lifecycle (Plan/Build/Execute/Report) via task-lifecycle.workflow.js; creator-reviewer agent loop at each stage; all plans follow haipipe-workflow IPO schema; type-specific workflow-plan-sample.yaml in every specialist; project/task-group scope moved to haipipe-project."
    - "4.0.0 (2026-06-11): 5-stage lifecycle — add Stage 5 (Insight), optional, files D_data observation card via /haipipe-insight-data for insight-worthy types. Code lifecycle (1-4) + data lifecycle (5)."
    - "4.1.0 (2026-06-11): task-group iteration — when given a task-group path, enumerate child task-folders and run lifecycle on each one sequentially (Step 3d). Removed project/task-group redirects to /haipipe-project; this skill now owns both task-folder and task-group scope."
    - "5.0.0 (2026-06-11): remove Stage 5 (Insight) from task lifecycle — insight is /haipipe-insight's responsibility, not C_task's. This skill is now a pure 4-stage code lifecycle (Plan/Build/Execute/Report). Task-group iteration updated accordingly."
---

Skill: haipipe-task (orchestrator)
===========================================

Build orchestrator organized around the **task hierarchy**:

```
project           examples/Proj{...}/
  └── task-group  tasks/{G}{NN}_{name}/
        └── task-folder  {NN}_{name}/{*.py, configs/, runs/, results/, notebooks/}
```

This skill owns **task-folder** and **task-group** scope. For a task-folder, it runs the 4-stage code lifecycle (Plan → Build → Execute → Report) or dispatches to a type specialist for scaffolding. For a task-group, it iterates over each child task-folder and runs the lifecycle on each one. For filing observations from results, use `/haipipe-insight` separately. Type specialists (one per type):

```
task-type     Specialist                              Cross-skill
------------  --------------------------------------  --------------------------
data          /haipipe-task-for-data              /haipipe-data
algo          /haipipe-task-for-algo              /haipipe-nn-algo
fit           /haipipe-task-for-fit               /haipipe-nn-tuner+instance
eval          /haipipe-task-for-eval              (project-local; future)
display       /haipipe-task-for-display           (independent)
individual    /haipipe-task-for-individual        /haipipe-individual
agent         /haipipe-task-for-agent             (none yet)
endpoint      /haipipe-task-for-endpoint          /haipipe-end (package + deploy)
```

NOTE: group letters (A01_, B01_, C01_) are project-specific organizational prefixes, NOT type indicators. Each project defines its own letter scheme. Type is detected from script content, not from group letters. The recommended convention is A=data, B=fit, C=endpoint.

Stata specialist (engine = Stata + PowerShell + logs, NOT papermill):

```
engine = Stata   →  /haipipe-task-for-stata   (unified — handles cms/case/data/reg internally)
```

ANY engine=Stata request is delegated to **`/haipipe-task-for-stata`**, a unified Stata specialist that handles all 4 stages internally (cms/case/data/reg), owns the `{LNN}` stage-letter alphabet, and keeps the shared engine contract in **its own `ref/`** (`haipipe-task-for-stata/ref/`: `stata-dialect.md` + the Stata templates). This skill does NOT route stata stages itself — it hands off once the engine is detected as Stata.

Routing principle: this skill is the HIGH-LEVEL router — it owns only the engine-agnostic invariants (`ref/hierarchy.md`, authoring conventions). Each `/haipipe-task-for-<engine>` child owns its OWN `ref/` (templates + dialect); route to the child and read the child's `ref/`, never keep engine specifics here.

For audit / read see `/haipipe-project-inspect`; for moves see `/haipipe-project-organize`.

---

Commands
--------

```
/haipipe-task plan <task-folder-path>                Stage 1: design the IPO contract
/haipipe-task build <task-folder-path>               Stage 2: implement the contract as code
/haipipe-task execute <task-folder-path>              Stage 3: run the code (or human runs manually)
/haipipe-task report <task-folder-path>               Stage 4: summarize results vs plan
/haipipe-task <existing-task-folder-path>             full lifecycle (all 4 stages)
/haipipe-task <existing-task-group-path>              iterate: full lifecycle on each child task-folder
/haipipe-task <stage> <existing-task-group-path>      iterate: that stage on each child task-folder
/haipipe-task task-folder <type> [args...]            scaffold a NEW task-folder via type specialist
```

For project scaffolding (creating `examples/Proj{...}/`), use `/haipipe-project`.

---

Four Stages (code lifecycle)
------------------------------

All four stages answer one question: **"is the implementation right?"**

```
Stage 1: PLAN — the contract (what the script SHOULD do)
  creates:   workflow/plan.yaml              task-level IPO (Run/Gate1/Gate2)
             workflow/plan-script-<name>.yaml script-level IPO (type-specific phases)
  reads:     *.py (if exists), haipipe-task-for-<type>/ref/workflow-plan-sample.yaml
  agents:    creator drafts plan → reviewer checks IPO compliance → ↺ revise

Stage 2: BUILD — the implementation (code that matches the plan)
  creates:   {NN}_{task_name}.py             main script (or fixes existing)
             configs/<run>.yaml              frozen parameters
             runs/<run>.sh                   papermill wrapper
             notebooks/                      empty dir (populated at runtime)
             CODE_REVIEW.md                  Gate 1 review (reviewer creates)
  reads:     workflow/plan.yaml, haipipe-task/ref/authoring-conventions.md
  agents:    creator writes code → reviewer does Gate 1 code review → ↺ revise
  after:     human can run directly: bash runs/<run>.sh

Stage 3: EXECUTE — just run (no creation, no modification)
  generates: results/<run>/metrics.json      output metrics
             results/<run>/runtime.yaml      run status/timing
             results/<run>/*.md, *.csv       other outputs
             notebooks/<run>.ipynb           papermill execution record
  runs:      bash runs/<run>.sh (human or autoExecute)
  agents:    none — this is a run, not an agent task

Stage 4: REPORT — summarize (what actually happened vs the plan)
  creates:   workflow/report.yaml            task-level report mirroring plan
             workflow/report-script-<name>.yaml script-level report
             RUN_AUDIT.md                    Gate 2 review (reviewer creates)
  reads:     workflow/plan*.yaml, results/<run>/*, CODE_REVIEW.md
  agents:    creator drafts report → reviewer checks accuracy → ↺ revise
```

File ownership is strict: Plan touches only `workflow/plan*.yaml`. Build touches only code/configs/runs. Execute touches only `results/` and `notebooks/`. Report touches only `workflow/report*.yaml` and `RUN_AUDIT.md`.

To file observations from task results ("what did the data teach us?"), use `/haipipe-insight <task-folder-path>` after the code lifecycle completes.

---

Agents
------

Two agents in `C_task/agents/` power stages 1, 2, and 4. They always work as a pair — creator produces, reviewer evaluates, loop if revise.

```
C_task/agents/
  haipipe-task-creator-agent.md     produces artifacts (plan, code, report)
  haipipe-task-reviewer-agent.md    evaluates artifacts (IPO compliance, code bugs, result accuracy)
```

The lifecycle workflow (`ref/task-lifecycle.workflow.js`) orchestrates the loop:
1. Creator agent produces the stage's artifact
2. Reviewer agent evaluates → `pass` / `warn` / `revise` / `fail`
3. First `warn` → feeds issues back to creator for one retry
4. Second `warn` or `pass` → advance to next stage
5. `fail` → stop, human decides

The creator never reviews its own work. The reviewer never produces artifacts. This separation is the core invariant.

The reviewer catches **intent-vs-implementation mismatches** — silent semantic bugs where the code runs but doesn't measure what the writer intended. Two-stage internally: Claude drafts, Codex (xhigh, out-of-family) independently reviews.

Author convention: `<TASK_NAME>.py` MUST have an `Intent` section in its docstring (template: `ref/intent-docstring-template.py`). Skip mechanisms for the run.sh pre-flight gate: `_meta.skip_review: true` in config, or `HAIPIPE_SKIP_REVIEW=1` env var.

---

Dispatch Table
--------------

```
Scope            Owner / route                              Function file
---------------- ------------------------------------------ ----------------------
task-group       → this skill: iterate children             Step 3d
task-folder      → dispatch by task-type to one of:
                     /haipipe-task-for-data
                     /haipipe-task-for-algo
                     /haipipe-task-for-fit
                     /haipipe-task-for-eval
                     /haipipe-task-for-display
                     /haipipe-task-for-individual
                     /haipipe-task-for-agent
                 (legacy monolithic flow at fn/task-folder.md is DEPRECATED)
run              this skill                                 fn/run.md
                 reads: ref/hierarchy.md, ref/config-meta-template.yaml, ref/run-sh-template.sh
audit            this skill                                 fn/workflow-audit.md
plan             this skill                                 fn/workflow-plan.md
                 reads: ref/workflow-template.yaml
                        type specialist's ref/workflow-plan-sample.yaml
report           this skill                                 fn/workflow-report.md
                 reads: workflow/plan.yaml, results/*/runtime.yaml
```

---

Step-by-Step Protocol
----------------------

Step 0: Read `ref/hierarchy.md` first. It's the conceptual model for the task hierarchy (project → task-group → task-folder → run).

Step 1: Detect AUTO_MODE. Any of these flips it on: `--auto` anywhere in args, env var `CLAUDE_AUTO_HANDOFF=1` or `AUTO_MODE=1`, parent skill passed `--auto`. AUTO_MODE changes "ASK" steps into "accept best inference or return blocked"; it never changes what gets written.

Step 2: Resolve scope. Cascade:
  (1) explicit stage command (`plan` / `build` / `execute` / `report`) as first positional → check the path argument:
      - path is an existing task-folder → scope=single-stage on that folder (Step 3c).
      - path is an existing task-group → scope=task-group-iterate with stages=[that stage] (Step 3d).
  (2) `task-folder` as first positional → scope=new task-folder (scaffold).
  (3) first positional is a known task-type (`data` / `algo` / `fit` / `eval` / `display` / `individual` / `agent`) → scope=task-folder, task-type=that positional.
  (4) first positional is a path to an existing task-group → scope=task-group-iterate (Step 3d).
  (5) first positional is a path to an existing task-folder → scope=full lifecycle (all 4 stages via Step 3c).
  (6) no args at all → default:
      - cwd is inside a task-folder → scope=full lifecycle (Step 3c).
      - cwd is inside a task-group (but not inside a task-folder) → scope=task-group-iterate (Step 3d).
      - else → scope=task-folder (scaffold).
  (7) still missing: AUTO → status: blocked. Interactive → ASK.

  Task-group detection: a path is a task-group if it matches `tasks/{G}{NN}_{name}/`, contains at least one `{NN}_*/` subdirectory, and has NO `.py` script at its root. This distinguishes it from a task-folder (which has `{NN}_{task_name}.py`).

Step 3: Branch by scope:
  - scope=plan → run Stage 1 only (creator drafts plan.yaml, reviewer checks)
  - scope=build → run Stage 2 only (creator writes code, reviewer does Gate 1)
  - scope=execute → run Stage 3 only (bash runs/<run>.sh)
  - scope=report → run Stage 4 only (creator drafts report.yaml, reviewer checks)
  - scope=full lifecycle → run all 4 stages via Step 3c (Workflow tool)
  - scope=task-group-iterate → enumerate children, run per-child via Step 3d
  - scope=task-folder (new) → resolve task-type via Step 3a cascade, then Skill("haipipe-task-<type>", args="<remaining_args> [--auto]")


Step 3a (scope=task-folder only): Task-type inference cascade.

  Highest-to-lowest confidence:

  (1) EXPLICIT — type given as positional after `task-folder`, or already pinned at Step 2 cascade (2). Done.

  (2) SCRIPT-INFERRED — if pwd is inside an existing task-folder, read the main `*.py` script and `scripts/*.py` files. Detect type from imports and content:
    - `from haipipe` / `SourceFn` / `RecordFn` → data
    - `import torch` / `Trainer` / `sweep` → fit
    - `eval` / `metrics` / `score` → eval
    - `plt.` / `fig` / `savefig` / `.tex` → display
    - `stata` / `.do` / `preserve` → stata (delegate)
    - `agent` / `claude` / `anthropic` → agent
  Confidence: high. AUTO → accept; log "inferred from script: <type>". Interactive → propose; one-line ASK to confirm.
  NOTE: the group letter ({A}{NN}, {B}{NN}, etc.) is purely organizational — each project chooses its own letter scheme. Do NOT infer task-type from the group letter. Always use script analysis or explicit type instead.

  (3) KEYWORD-INFERRED — scan free-text args for keywords (table below). First match (left-to-right in args) wins.

        ┌────────────┬─────────────────────────────────────────────────────────────────┐
        │ data       │ build · source · record · dataset · cgm · raw · ingest ·        │
        │            │ pipeline 1·2·3·4 · fn build                                     │
        │ algo       │ smoke · smoke-test · verify algorithm · test algo · algo dev ·  │
        │            │ algo class · forward pass · loss class                          │
        │ fit        │ train · training · fit · sweep · hyperparam · lr · epoch ·      │
        │            │ model size · pretrain · finetune · ft                           │
        │ eval       │ eval · evaluate · evaluation · score · scoring · metrics ·      │
        │            │ mae · rmse · accuracy · horizon                                 │
        │ display    │ figure · table · plot · paper figure · paper table · panel ·    │
        │            │ main figure · ablation table                                    │
        │ individual │ subject · patient · individual · one user · single subject ·    │
        │            │ cgm trace · treatment event · view                              │
        │ agent      │ agent · llm · prompt · claude · gpt · tool use · system prompt  │
        ├────────────┼─────────────────────────────────────────────────────────────────┤
        │ STATA      │ stata · do-file · .do · cms · case-pipeline · trigger cases ·   │
        │ (engine)   │ analysis table · reg · regression · ols · iv · neat · bene_info │
        └────────────┴─────────────────────────────────────────────────────────────────┘

  Stata engine-detect → DELEGATE: hand off to `/haipipe-task-for-stata` which owns stage disambiguation: `Skill("haipipe-task-for-stata", args="<remaining_args> [--auto]")`
  Confidence: medium. AUTO → accept. Interactive → propose; one-line ASK to confirm.

  (4) STILL UNKNOWN: AUTO → status: blocked. Interactive → ASK with all 7 options.


Step 3b (scope=task-folder only): Parent existence cascade.

  Before dispatching to `/haipipe-task-<type>`, verify all ancestors exist. Order: project → task-group → task-folder.

  Resolve target paths: PROJECT_PATH = `examples/{PROJECT_ID}/`, GROUP_PATH = `PROJECT_PATH/tasks/{LETTER}{NN}_<group_name>/` (letter is project-specific, NOT tied to task-type).

  (1) Project check: EXISTS → continue. MISSING + `--project-id` given → scaffold via `Skill("haipipe-task", args="project <PROJECT_ID> --auto")`. MISSING + no `--project-id` → blocked (AUTO) or ASK (interactive).

  (2) Group check: EXISTS → continue. MISSING + `--group` given → scaffold via `Skill("haipipe-task", args="task-group ...")`. MISSING + no `--group` → blocked (AUTO) or ASK (interactive).

  Only after both checks pass: `Skill("haipipe-task-<type>", args="<remaining_args> --project-id <PROJECT_ID> --group <group_id> [--auto]")`


Step 3c: Full lifecycle or single stage.

  Run via the Workflow tool:

  ```
  Workflow({
    scriptPath: "Tools/plugins/haipipe-toolkit/skills/C_task/haipipe-task/ref/task-lifecycle.workflow.js"
  }, {
    task_folder: "<path>",
    type: "<detected from Step 3a, or null for auto-detect>",
    stages: ["plan", "build", "execute", "report"],
    autoExecute: false
  })
  ```

  For single-stage commands (`/haipipe-task plan <path>`), pass only that stage: `stages: ["plan"]`.

  All generated plan/report files follow the haipipe-workflow IPO schema at `B_project/haipipe-workflow/ref/plan-schema.md`. Every plan YAML starts with an IPO tree preview comment with emojis.


Step 3d: Task-group iteration (scope=task-group-iterate).

  The lifecycle scope stays at task-folder — this step just loops over children. No workflow/ artifacts are ever created at the group level.

  (1) ENUMERATE — list child task-folders in the group directory, sorted by numeric prefix:
      ```
      ls -d <group-path>/{NN}_*/ | sort
      ```
      Filter: only directories whose name matches `{NN}_{name}` (2-digit prefix + underscore). Skip `sbatch/`, `diagram/`, and any non-task directories.

  (2) CONFIRM — log the children found:
      ```
      Task-group: <group-path>
      Children (N task-folders):
        [1/N] 01_foo
        [2/N] 02_bar
      Stages: <plan|build|...|all>
      ```
      In interactive mode, ASK to confirm before proceeding. In AUTO_MODE, proceed directly.

  (3) ITERATE — for each child task-folder, in order:
      - Log: `── [i/N] <child_name> ──`
      - Call Workflow with the existing `task-lifecycle.workflow.js`, passing the child path and the requested stages:
        ```
        Workflow({
          scriptPath: "Tools/plugins/haipipe-toolkit/skills/C_task/haipipe-task/ref/task-lifecycle.workflow.js"
        }, {
          task_folder: "<group-path>/<child>/",
          type: null,
          stages: <requested stages or ["plan", "build", "execute", "report"]>,
          autoExecute: false
        })
        ```
      - Collect the result. If a child fails (status=failed), log the failure and continue to the next child — do NOT stop the group iteration.

  (4) AGGREGATE — after all children complete, emit a group summary:
      ```
      Task-group: <group-path>
      Results:
        [1/N] 01_foo — ok (plan: pass, build: pass, ...)
        [2/N] 02_bar — failed (build: fail)
      Overall: N-1 ok, 1 failed
      ```


Step 4: Emit the structured tail:

```
status:    ok | blocked | failed
summary:   2-3 sentences on what was done
artifacts: [paths created/modified]
next:      suggested next command
```


Invocation examples
--------------------

```
# 4-stage lifecycle on existing task folder
/haipipe-task examples/ProjA/tasks/B03_band4/01_band4

# single stage
/haipipe-task plan examples/ProjA/tasks/B03_band4/01_band4
/haipipe-task build examples/ProjA/tasks/B03_band4/01_band4
/haipipe-task execute examples/ProjA/tasks/B03_band4/01_band4
/haipipe-task report examples/ProjA/tasks/B03_band4/01_band4

# task-GROUP: iterate lifecycle over all children (01_band4, 02_eval, ...)
/haipipe-task examples/ProjA/tasks/B03_band4

# task-GROUP with single stage: run that stage on each child
/haipipe-task plan examples/ProjA/tasks/B03_band4
/haipipe-task report examples/ProjA/tasks/B03_band4

# scaffold a NEW task-folder (dispatches to type specialist)
/haipipe-task task-folder data
/haipipe-task task-folder eval --project-id ProjA-Timing-01-OptTime --group B03_band4

# direct specialist (bypass orchestrator)
/haipipe-task-for-data
/haipipe-task-for-fit
```

---

Per-task observability (workflow/ folder)
------------------------------------------

Task-level observability is handled by the **workflow/ folder**:

```
<task-folder>/workflow/
  plan.yaml                            task-level IPO (Run/Gate1/Gate2 phases)
  plan-script-<name>.yaml              per-script IPO (type-specific phases)
  report.yaml                          task-level report mirroring plan
  report-script-<name>.yaml            per-script report mirroring plan-script
```

Plan = intent. Report = evidence. Same IPO shape at both levels, following `B_project/haipipe-workflow/ref/plan-schema.md`.

Generated by the lifecycle workflow (`ref/task-lifecycle.workflow.js`) or manually via `/haipipe-task plan` and `/haipipe-task report`.

---

Risk Profile
-------------

CREATES files under `examples/{PROJECT_ID}/`. For scope=project with new code stubs, also creates files under `code-dev/` and `code/hainn/`. Refuse to overwrite existing names — abort and recommend `-organize`.

When dispatching to a task-type specialist, the same blast radius applies — specialists also CREATE files under `examples/`.
