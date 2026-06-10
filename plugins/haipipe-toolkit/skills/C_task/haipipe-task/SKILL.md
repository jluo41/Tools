---
name: haipipe-task
description: "Task-folder orchestrator. For new tasks, dispatches to type specialists (data/algo/training/eval/display/individual/agent). For existing tasks, runs the 4-stage lifecycle (Plan → Build → Execute → Report) via ref/task-lifecycle.workflow.js, with haipipe-task-creator-agent and haipipe-task-reviewer-agent paired at each stage in a creator-reviewer loop."
argument-hint: "[scope] [args...]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill, Workflow
metadata:
  version: "3.0.0"
  last_updated: "2026-06-09"
  summary: "Build orchestrator with automated workflow lifecycle for existing tasks."
  changelog:
    - "1.0.0 (2026-05-31): baseline metadata added."
    - "2.0.0 (2026-06-08): add workflow lifecycle — audit, plan, report. New fn/ procedures. New ref: workflow-template.yaml."
    - "2.1.0 (2026-06-08): three-layer plans; per-script IPO; Stata four-sister; wire reviewer+auditor agents."
    - "3.0.0 (2026-06-09): 4-stage lifecycle (Plan/Build/Execute/Report) via task-lifecycle.workflow.js; creator-reviewer agent loop at each stage; all plans follow haipipe-workflow IPO schema; type-specific workflow-plan-sample.yaml in every specialist; project/task-group scope moved to haipipe-project."
---

Skill: haipipe-task (orchestrator)
===========================================

Build orchestrator organized around the **task hierarchy**:

```
project           examples/Proj{...}/
  └── task-group  tasks/{G}{NN}_{name}/
        └── task-folder  {NN}_{name}/{*.py, configs/, runs/, results/, notebooks/}
```

Project and task-group scaffolding belong to `/haipipe-project`. This skill owns **task-folder** and below. For task-folder scaffolding, it dispatches to one of seven task-type specialists (one per type):

```
task-type     Specialist                              Cross-skill
------------  --------------------------------------  --------------------------
data          /haipipe-task-for-data              /haipipe-data
algo          /haipipe-task-for-algo              /haipipe-nn-algo
training      /haipipe-task-for-training          /haipipe-nn-tuner+instance
eval          /haipipe-task-for-eval              (project-local; future)
display       /haipipe-task-for-display           (independent)
individual    /haipipe-task-for-individual        /haipipe-individual
agent         /haipipe-task-for-agent             (none yet)
inference     /haipipe-task-for-inference         /haipipe-end-endpointset (profile)
```

NOTE: group letters (A00_, B01_, C01_, D01_) are project-specific organizational prefixes, NOT type indicators. Each project defines its own letter scheme. Type is detected from script content, not from group letters.

Stata sub-family (engine = Stata + PowerShell + logs, NOT papermill):

```
engine = Stata   →  /haipipe-task-for-stata   (sub-orchestrator / father skill)
                       ├── /haipipe-task-for-stata-cms     A · 1-CMS-Store   (heavy, per year)
                       ├── /haipipe-task-for-stata-case    B · 2-Case-Store  (heavy, cohort × year)
                       ├── /haipipe-task-for-stata-data    C · *-Data-Store  (heavy, cross-year)
                       └── /haipipe-task-for-stata-reg     D · results/      (LIGHT coef tables)
```

ANY engine=Stata request is delegated to **`/haipipe-task-for-stata`**, which owns the stage disambiguation (cms/case/data/reg), the `{LNN}` stage-letter alphabet, and the shared engine contract in **its own `ref/`** (`haipipe-task-for-stata/ref/`: `stata-dialect.md` + the three Stata templates). This skill does NOT route stata stages itself — it hands off once the engine is detected as Stata.

Routing principle: this skill is the HIGH-LEVEL router — it owns only the engine-agnostic invariants (`ref/hierarchy.md`, authoring conventions). Each `/haipipe-task-for-<engine>` child owns its OWN `ref/` (templates + dialect); route to the child and read the child's `ref/`, never keep engine specifics here.

Called by `/haipipe-project` when the request is to **create** something in the hierarchy. For audit / read see `-inspect`; for moves see `-organize`.

---

Commands
--------

```
/haipipe-task                                        ASK which scope
/haipipe-task task-folder                            ASK task-type, then dispatch
/haipipe-task task-folder <type> [args...]           dispatch to type specialist
/haipipe-task run [task-path] [run-name]             scaffold a new run (asks _meta)
/haipipe-task audit <task-folder-path>               four-sister check + type detect (read-only)
/haipipe-task plan <task-folder-path>                audit + fix + generate workflow/plan.yaml
/haipipe-task report <task-folder-path>              generate workflow/report.yaml
/haipipe-task <existing-task-folder-path>            full lifecycle via workflow engine
```

For project and task-group scaffolding, use `/haipipe-project` instead.

Shorthand: `/haipipe-task` with no scope and no args defaults to `run` (most common ask once a task-folder exists; falls back to `task-folder` if cwd is not a task-folder yet).

---

Agents
------

Two agents in `C_task/agents/` power the lifecycle. They always work as a pair — creator produces an artifact, reviewer evaluates it, loop if the reviewer says revise.

```
C_task/agents/
  haipipe-task-creator-agent.md     produces artifacts (plan, code, report)
  haipipe-task-reviewer-agent.md    evaluates artifacts (IPO compliance, code bugs, result integrity)
```

The creator-reviewer pair operates at every stage of the task lifecycle:

```
Stage 1: PLAN      creator → plan.yaml + plan-script     reviewer → IPO schema check       ↺ revise
Stage 2: BUILD     creator → code + configs + structure   reviewer → Gate 1 code review     ↺ revise
Stage 3: EXECUTE   (run, no creator)                      reviewer → Gate 2 result audit
Stage 4: REPORT    creator → report.yaml                  reviewer → accuracy check          ↺ revise
```

The lifecycle workflow (`ref/task-lifecycle.workflow.js`) orchestrates the loop:
1. Creator agent produces the artifact for the current stage
2. Reviewer agent evaluates it → returns `pass` / `warn` / `revise` / `fail`
3. `revise` → reviewer feedback is passed back to creator, who tries again (up to `maxRetries`)
4. `pass` / `warn` → advance to next stage
5. `fail` → stop, human decides

The creator never reviews its own work. The reviewer never produces artifacts. This separation is the core invariant.

The reviewer catches **intent-vs-implementation mismatches** — silent semantic bugs where the code runs and produces numbers but doesn't measure what the writer intended. Two-stage internally: Claude drafts, Codex (xhigh, out-of-family) independently reviews.

Author convention: `<TASK_NAME>.py` MUST have an `Intent` section in its docstring (template: `ref/intent-docstring-template.py`). Skip mechanisms for the run.sh pre-flight gate: `_meta.skip_review: true` in config, or `HAIPIPE_SKIP_REVIEW=1` env var.

When targeting an **existing** task folder (not scaffolding new), the workflow lifecycle activates automatically via `ref/task-lifecycle.workflow.js`. See Step 3c below.

---

Dispatch Table
--------------

```
Scope            Owner / route                              Function file
---------------- ------------------------------------------ ----------------------
project          → /haipipe-project                         (not this skill)
task-group       → /haipipe-project                         (not this skill)
task-folder      → dispatch by task-type to one of:
                     /haipipe-task-for-data
                     /haipipe-task-for-algo
                     /haipipe-task-for-training
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
  (1) explicit scope token (`task-folder` / `run` / `audit` / `plan` / `report`) as first positional → use it.
  (2) `project` or `task-group` → redirect: `Skill("haipipe-project", args="<remaining_args>")`.
  (3) first positional is a known task-type (`data` / `algo` / `training` / `eval` / `display` / `individual` / `agent`) → scope=task-folder, task-type=that positional.
  (4) first positional is a path to an existing task-folder → scope=existing (Step 3c).
  (5) no args at all → default to `run` if cwd is inside a task-folder (has runs/ + configs/), else `task-folder`.
  (6) still missing: AUTO → status: blocked, reason: "scope unknown". Interactive → ASK.

Step 3: Branch by scope:
  - scope=task-folder (new) → resolve task-type via Step 3a cascade, then Skill("haipipe-task-<type>", args="<remaining_args> [--auto]")
  - scope=existing → run full lifecycle via Step 3c (Workflow tool)
  - scope=run → read fn/run.md, execute here
  - scope=audit/plan/report → run single step via corresponding fn/ procedure


Step 3a (scope=task-folder only): Task-type inference cascade.

  Highest-to-lowest confidence:

  (1) EXPLICIT — type given as positional after `task-folder`, or already pinned at Step 2 cascade (2). Done.

  (2) SCRIPT-INFERRED — if pwd is inside an existing task-folder, read the main `*.py` script and `scripts/*.py` files. Detect type from imports and content:
    - `from haipipe` / `SourceFn` / `RecordFn` → data
    - `import torch` / `Trainer` / `sweep` → training
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
        │ training   │ train · training · sweep · hyperparam · lr · epoch ·            │
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


Step 3c (existing task-folder): Automated workflow lifecycle.

  When the target task-folder ALREADY EXISTS (has configs/ or runs/ or results/ or *.py), the workflow lifecycle activates. This is distinct from scaffolding (Step 3b) — here we're auditing and working with an existing task, not creating a new one.

  Run the lifecycle via the Workflow tool:

  ```
  Workflow({
    scriptPath: "Tools/plugins/haipipe-toolkit/skills/C_task/haipipe-task/ref/task-lifecycle.workflow.js"
  }, {
    task_folder: "<path>",
    type: "<detected from Step 3a, or null for auto-detect>",
    autoRun: false
  })
  ```

  The workflow script (`ref/task-lifecycle.workflow.js`) drives 4 stages. Each stage pairs a **creator agent** (`haipipe-task-creator-agent`) with a **reviewer agent** (`haipipe-task-reviewer-agent`) in a loop: creator produces → reviewer evaluates → revise if needed.

  ```
  Stage 1: PLAN      creator drafts plan.yaml        → reviewer checks  → loop if revise
  Stage 2: BUILD     creator writes/fixes code+config → reviewer checks  → loop if revise
  Stage 3: EXECUTE   run the task (optional)          → reviewer audits  → (no loop)
  Stage 4: REPORT    creator drafts report.yaml       → reviewer checks  → loop if revise
  ```

  Stages 3 and 4 are optional (`autoExecute=false`, `autoReport=false` by default). The creator-reviewer loop retries up to `maxRetries` (default 2) per stage. `fail` from the reviewer stops the lifecycle; `revise` feeds back to the creator with specific issues to fix.

  Agents: `C_task/agents/haipipe-task-creator-agent.md`, `C_task/agents/haipipe-task-reviewer-agent.md`.

  All generated plan/report files follow the haipipe-workflow IPO schema at `B_project/haipipe-workflow/ref/plan-schema.md`. Steps use canonical fields: `label`, `type`, `required`, `prompt`, `files_in`, `files_out`.

  For explicit single-step commands (`/haipipe-task plan`, `/haipipe-task report`), run ONLY that step via the corresponding `fn/` procedure, not the full lifecycle.


Step 4: For locally-executed scopes, follow the function file step-by-step. ASK for any metadata not provided (AUTO mode: best-effort defaults, or blocked if a required field has no sensible default). For dispatched scopes, capture the specialist's return contract and surface it as our own.

Step 5: Emit the structured tail:

```
status:    ok | blocked | failed
summary:   2-3 sentences on what was scaffolded
artifacts: [paths created]
next:      suggested next command
```


Invocation examples
--------------------

```
# explicit (most precise — always works)
/haipipe-task task-folder data
/haipipe-task task-folder training A01_pretraining 02_train_d128

# shorthand: first positional is a task-type → scope=task-folder inferred
/haipipe-task data
/haipipe-task training

# cwd-inferred: cd into the group folder first
$ cd examples/Proj-X/tasks/D01_data_wellreadi/
$ /haipipe-task task-folder           ← type=data inferred from script

# keyword-inferred: free-text hint
/haipipe-task "build CGM 5min record dataset for wellreadi v3"   → type=data
/haipipe-task "evaluate clm at h24 on test-id split"             → type=eval

# auto mode: same as above but no confirm prompts
/haipipe-task data --auto
/haipipe-task "train clm baseline" --auto

# existing task-folder: full lifecycle via Workflow tool
/haipipe-task evaluate and plan examples/ProjA/tasks/B03_band4/01_band4

# direct specialist (bypass orchestrator entirely; skips cascade check)
/haipipe-task-for-data
/haipipe-task-for-training
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
