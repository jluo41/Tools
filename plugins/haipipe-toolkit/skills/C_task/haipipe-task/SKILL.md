---
name: haipipe-task
description: "Build orchestrator for haipipe-project. Routes scope=project / task-group / task-folder; for scope=task-folder, dispatches to one of seven task-type specialists (data / algo / training / eval / display / individual / agent). Replaces the older monolithic -task specialist with a router + per-type series. Called by /haipipe-project orchestrator. Direct invocation works for scaffold work."
argument-hint: "[scope] [args...]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "2.0.0"
  last_updated: "2026-06-08"
  summary: "Build orchestrator for haipipe-project. Now includes workflow lifecycle (audit/plan/report) for existing task folders."
  changelog:
    - "1.0.0 (2026-05-31): baseline metadata added."
    - "2.0.0 (2026-06-08): add workflow lifecycle — audit (four-sister check), plan (generate plan.yaml), report (mirror plan with results). New fn/ procedures: workflow-audit.md, workflow-plan.md, workflow-report.md. New ref: workflow-template.yaml."
---

Skill: haipipe-task (orchestrator)
===========================================

Build orchestrator organized around the **task hierarchy**:

```
project           examples/Proj{...}/
  └── task-group  tasks/{G}{NN}_{name}/
        └── task-folder  {NN}_{name}/{*.py, configs/, runs/, results/, notebooks/}
```

This skill OWNS scaffolding for **project** and **task-group**. For
**task-folder** scaffolding, it dispatches to one of seven task-type
specialists (one per type):

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

NOTE: group letters (A00_, B01_, C01_, D01_) are project-specific
organizational prefixes, NOT type indicators. Each project defines
its own letter scheme. Type is detected from script content, not
from group letters.

Stata sub-family (engine = Stata + PowerShell + logs, NOT papermill):

```
engine = Stata   →  /haipipe-task-for-stata   (sub-orchestrator / father skill)
                       ├── /haipipe-task-for-stata-cms     A · 1-CMS-Store   (heavy, per year)
                       ├── /haipipe-task-for-stata-case    B · 2-Case-Store  (heavy, cohort × year)
                       ├── /haipipe-task-for-stata-data    C · *-Data-Store  (heavy, cross-year)
                       └── /haipipe-task-for-stata-reg     D · results/      (LIGHT coef tables)
```

ANY engine=Stata request is delegated to **`/haipipe-task-for-stata`**, which owns
the stage disambiguation (cms/case/data/reg), the `{LNN}` stage-letter alphabet,
and the shared engine contract in **its own `ref/`**
(`haipipe-task-for-stata/ref/`: `stata-dialect.md` + the three Stata templates).
This skill does NOT route stata stages itself — it hands off once the engine is
detected as Stata. The four children keep all structure invariants (hierarchy,
RUNNAME spine, light/heavy, diagram-as-doc).

Routing principle: this skill is the HIGH-LEVEL router — it owns only the
engine-agnostic invariants (`ref/hierarchy.md`, authoring conventions). Each
`/haipipe-task-for-<engine>` child owns its OWN `ref/` (templates + dialect);
route to the child and read the child's `ref/`, never keep engine specifics here.

Called by `/haipipe-project` when the request is to **create** something
in the hierarchy. For audit / read see `-inspect`; for moves see `-organize`.

---

Commands
--------

```
/haipipe-task                                        ASK which scope
/haipipe-task project [id]                           scaffold a new project (here)
/haipipe-task task-group                             scaffold a new task-group (here)
/haipipe-task task-folder                            ASK task-type, then dispatch
/haipipe-task task-folder <type> [args...]           dispatch to type specialist
/haipipe-task run [task-path] [run-name]             scaffold a new run (asks _meta)
/haipipe-task audit <task-folder-path>               four-sister check + type detect
/haipipe-task plan <task-folder-path>                generate workflow/plan.yaml
/haipipe-task report <task-folder-path>              generate workflow/report.yaml
```

Shorthand: `/haipipe-task` with no scope and no args defaults to
`run` (most common ask once a task-folder exists; falls back to
`task-folder` if cwd is not a task-folder yet).

When targeting an **existing** task folder (not scaffolding new), the
workflow layer activates automatically:
  audit → fix → plan → dispatch → report
See Step 3c below.

---

Dispatch Table
--------------

```
Scope            Owner / route                              Function file
---------------- ------------------------------------------ ----------------------
project          this skill                                 fn/project.md
                 reads: ref/hierarchy.md
                        ../../B_project/haipipe-project/ref/project-structure.md
                        ../../B_project/haipipe-project/ref/code-structure.md
task-group       this skill                                 fn/task-group.md
                 reads: ref/hierarchy.md
                        ../../B_project/haipipe-project/ref/project-structure.md
task-folder      → dispatch by task-type to one of:
                     /haipipe-task-for-data
                     /haipipe-task-for-algo
                     /haipipe-task-for-training
                     /haipipe-task-for-eval
                     /haipipe-task-for-display
                     /haipipe-task-for-individual
                     /haipipe-task-for-agent
                 (legacy monolithic flow at fn/task-folder.md is DEPRECATED;
                  kept as transition fallback only)
run              this skill                                 fn/run.md
                 reads: ref/hierarchy.md
                        ref/config-meta-template.yaml
                        ref/run-sh-template.sh
audit            this skill                                 fn/workflow-audit.md
                 reads: task folder configs/ runs/ results/ notebooks/
plan             this skill                                 fn/workflow-plan.md
                 reads: fn/workflow-audit result
                        ref/workflow-template.yaml
                        type specialist's ref/workflow-template.yaml (if exists)
report           this skill                                 fn/workflow-report.md
                 reads: workflow/plan.yaml
                        results/*/runtime.yaml, manifest.json
```

Task-type → specialist mapping (for scope=task-folder):
same as the table above (type → specialist → cross-skill).

---

Step-by-Step Protocol
----------------------

Step 0: Read `ref/hierarchy.md` first. It's the conceptual model.
        Then read `../../B_project/haipipe-project/ref/project-structure.md`.
        For scope=project, also read `../../B_project/haipipe-project/ref/code-structure.md`.

Step 1: Detect AUTO_MODE. Any of these flips it on:
          - `--auto` anywhere in args
          - env var `CLAUDE_AUTO_HANDOFF=1` or `AUTO_MODE=1`
          - parent skill passed `--auto` when invoking us
        AUTO_MODE changes "ASK" steps into "accept best inference or
        return blocked"; it never changes what gets written.

Step 2: Resolve scope. Cascade:
          (1) explicit scope token (`project` / `task-group` / `task-folder` / `run`)
              as first positional                        → use it.
          (2) first positional is a known task-type
              (`data` / `algo` / `training` / `eval` /
               `display` / `individual` / `agent`)       → scope=task-folder,
                                                            task-type=that positional.
          (3) no args at all                             → default to `run` if cwd
                                                            is inside a task-folder
                                                            (has runs/ + configs/),
                                                            else `task-folder`.
          (4) still missing
                AUTO         → status: blocked, reason: "scope unknown"
                interactive  → ASK.

Step 3: Branch by scope:
          - scope=project       → read fn/project.md, execute here
          - scope=task-group    → read fn/task-group.md, execute here
          - scope=task-folder   → resolve task-type via Step 3a cascade,
                                  then Skill("haipipe-task-<type>",
                                              args="<remaining_args> [--auto]")
          - scope=run           → read fn/run.md, execute here


Step 3a (scope=task-folder only): Task-type inference cascade.

  Highest-to-lowest confidence:

  (1) EXPLICIT — type given as positional after `task-folder`, or already
      pinned at Step 2 cascade (2).  ✅ done.

  (2) SCRIPT-INFERRED — if pwd is inside an existing task-folder,
      read the main `*.py` script and `scripts/*.py` files. Detect type
      from imports and content:
        - `from haipipe` / `SourceFn` / `RecordFn`  → data
        - `import torch` / `Trainer` / `sweep`       → training
        - `eval` / `metrics` / `score`                → eval
        - `plt.` / `fig` / `savefig` / `.tex`        → display
        - `stata` / `.do` / `preserve`                → stata (delegate)
        - `agent` / `claude` / `anthropic`            → agent
      Confidence: high. Behavior:
        - AUTO         → accept; log "inferred from script: <type>"
        - interactive  → propose; one-line ASK to confirm

      NOTE: the group letter ({A}{NN}, {B}{NN}, etc.) is purely
      organizational — each project chooses its own letter scheme.
      Do NOT infer task-type from the group letter. ProjA uses
      different letters than ProjB. Always use script analysis
      or explicit type instead.

  (3) KEYWORD-INFERRED — scan free-text args for keywords (table below).
      First match (left-to-right in args) wins.

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

      Stata engine-detect → DELEGATE: the keyword `stata` (or a `.do` file, or
      any stage word cms/case/data/reg) signals the Stata engine. Do NOT pick a
      stage here — hand off the whole request to `/haipipe-task-for-stata`, which
      owns stage disambiguation and routes to the right
      `/haipipe-task-for-stata-<stage>` child:
        Skill("haipipe-task-for-stata", args="<remaining_args> [--auto]")

      Confidence: medium. Behavior:
        - AUTO         → accept; log "inferred from keyword '<kw>': <type>"
        - interactive  → propose; one-line ASK to confirm

  (4) STILL UNKNOWN:
        - AUTO         → status: blocked, reason:
                         "cannot infer task-type. Pass one of
                         data/algo/training/eval/display/individual/agent
                         as positional, OR cd into a tasks/{LETTER}{NN}_*/
                         group folder, OR include a keyword hint in args."
        - interactive  → ASK with all 7 options.


Step 3b (scope=task-folder only): Parent existence cascade.

  Before dispatching to `/haipipe-task-<type>`, verify all ancestors
  exist. Order: project → task-group → task-folder.

  Resolve target paths:
    PROJECT_PATH = `examples/{PROJECT_ID}/`
    GROUP_PATH   = `PROJECT_PATH/tasks/{LETTER}{NN}_<group_name>/`
                     (letter is project-specific, NOT tied to task-type)

  (1) Project check
        EXISTS                                  → continue.
        MISSING + `--project-id` given
          AUTO        → Skill("haipipe-task", args="project <PROJECT_ID> --auto")
                        then continue.
          interactive → propose "scaffold project <PROJECT_ID>?", confirm, then proceed.
        MISSING + no `--project-id`
          AUTO        → status: blocked,
                        reason: "no project in cwd and no --project-id given."
          interactive → ASK which project (or scaffold one).

  (2) Group check
        EXISTS + letter matches task-type       → continue.
        EXISTS + letter MISMATCH
          AUTO        → status: blocked,
                        reason: "group <{LETTER}{NN}_...> has letter <X>, but
                        task-type <type> requires letter <Y>. Pick a different
                        group, or move/rename via /haipipe-project-organize."
          interactive → warn; ASK (override / pick different group).
        MISSING + `--group` given
          AUTO        → Skill("haipipe-task",
                              args="task-group <group_id>
                                    --project-id <PROJECT_ID>
                                    --letter <GROUP_LETTER> --auto")
                        then continue.
          interactive → propose "scaffold group <group_id>?", confirm, then proceed.
        MISSING + no `--group`
          AUTO        → status: blocked,
                        reason: "no --group given; specify which group to
                        create or scaffold under."
          interactive → ASK.

  Only after both checks pass:
      Skill("haipipe-task-<type>",
            args="<remaining_args> --project-id <PROJECT_ID>
                  --group <group_id> [--auto]")


Step 3c (existing task-folder): Workflow layer.

  When the target task-folder ALREADY EXISTS (has configs/ or runs/ or
  results/), the workflow layer activates. This is distinct from
  scaffolding (Step 3b) — here we're auditing and working with an
  existing task, not creating a new one.

  Detect: task-folder exists if any of these are present:
    - <target>/configs/
    - <target>/runs/
    - <target>/results/
    - <target>/*.py (main script)

  If task-folder exists, run the workflow lifecycle:

  (1) AUDIT — read fn/workflow-audit.md, execute it.
      Scan four-sister consistency (configs/runs/results/notebooks).
      Detect task type (from group letter or script analysis).
      Check if workflow/plan.yaml exists.
      Report: issues found, type detected, plan status.

      Progress:
        📋 Audit: <task-folder>
           type: <detected>
           four-sister: N runs, M issues (K fixable)

  (2) FIX — if audit found fixable issues:
      - missing per-run configs → split shared config into per-run
        (read fn/workflow-plan.md Step 4 for the split procedure)
      - missing .ps1 counterpart → generate from .sh
      - stale results/ with no runner → flag for user decision

      Progress:
        🔧 Fixed: 3 per-run configs generated from shared config
           Flagged: run_build_roberta (stale result, no runner)

  (3) PLAN — if workflow/plan.yaml missing or stale:
      Read fn/workflow-plan.md, execute it.
      Infer phases and steps from task state.
      Write workflow/plan.yaml.

      Progress:
        📍 Plan: workflow/plan.yaml written
           phases: 2, steps: 5, files tracked: 8 in / 12 out

  (4) DISPATCH — same as before (Skill("haipipe-task-<type>", ...))
      BUT now the specialist has workflow context:
      - It can read workflow/plan.yaml to know the intended phases
      - It can report progress per step

  (5) REPORT — after execution completes:
      Read fn/workflow-report.md, execute it.
      Read plan.yaml + results/ → write workflow/report.yaml.

      Progress:
        📋 Report: 2/2 phases, 4/5 steps done, 1 skipped

  For explicit audit/plan/report commands (/haipipe-task audit, etc.),
  run ONLY that step, not the full lifecycle.

  For the full lifecycle, report progress at each boundary:
    📋 Audit → 🔧 Fix → 📍 Plan → ⏳ Execute → 📋 Report


Step 4: For locally-executed scopes, follow the function file step-by-step.
        ASK for any metadata not provided (AUTO mode: best-effort defaults,
        or blocked if a required field has no sensible default). For
        dispatched scopes, capture the specialist's return contract and
        surface it as our own.

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
$ /haipipe-task task-folder           ← type=data inferred from cwd D01_

# keyword-inferred: free-text hint
/haipipe-task "build CGM 5min record dataset for wellreadi v3"
   → keyword "build" + "record" + "dataset"  → type=data

/haipipe-task "evaluate clm at h24 on test-id split"
   → keyword "evaluate"  → type=eval

# auto mode: same as above but no confirm prompts
/haipipe-task data --auto
/haipipe-task "train clm baseline" --auto

# direct specialist (bypass orchestrator entirely; skips cascade check)
/haipipe-task-for-data
/haipipe-task-for-training

# end-to-end with auto-cascade (creates project + group if missing)
/haipipe-task data --auto \
    --project-id ProjA-Bench-1-FairGlucose \
    --group D01_data \
    --task 01_build_source_wellreadi
#  ↓
#  Step 3b cascade:
#    ▪ ProjA-Bench-1-FairGlucose missing  → Skill(haipipe-task, project ..., --auto)
#    ▪ D01_data missing                    → Skill(haipipe-task, task-group ..., --auto)
#    ▪ both now exist                      → Skill(haipipe-task-for-data, ..., --auto)
```

---

Per-task aggregate log
-----------------------

Each run's `runs/<RUN>.sh` calls the regen script at finalize to
(re)build `<task-folder>/task-log.md` — a markdown summary of every
run in the task, derived from `results/*/runtime.yaml`.

Owned by sibling specialist **`/haipipe-task-logging`** (read-only at
task-folder scope). See `C_task/haipipe-task-logging/SKILL.md` for:
  - the schema of `task-log.md`
  - manual re-render command
  - future status / runs / inspect commands (TBD)

The orchestrator does NOT need to invoke `-logging` directly during
scaffold; the run-script wrapper handles regen automatically.


---

Pre-flight code review
-----------------------

Every scaffolded `run.sh` (from `ref/run-sh-template.sh`) carries a
**pre-flight gate** that blocks launch until a fresh `CODE_REVIEW.md`
exists in the task-folder. The review is produced by the
**Run Script Reviewer** agent at:

```
Tools/plugins/haipipe-toolkit/skills/C_task/agents/reviewers/run-script-reviewer-agent.md
```

What it catches: **intent-vs-implementation mismatches** — silent
semantic bugs where the code runs and produces numbers but doesn't
measure what the writer intended (e.g. scope misaligned to full input
vs horizon-only, masking direction reversed, eval horizon shifted,
patient-split actually sample-split, etc.). Two-stage: Claude drafts,
Codex (xhigh, out-of-family) independently reviews; the merge surfaces
agreements and disagreements.

Author convention — `<TASK_NAME>.py` MUST have a top-of-file docstring
with an `Intent` section. Template:

```
ref/intent-docstring-template.py
```

Skip mechanisms (any one will bypass the gate):

```
_meta.skip_review: true        in configs/<RUN_NAME>.yaml
HAIPIPE_SKIP_REVIEW=1          env var at run.sh launch
```

This is the only currently-wired trigger. Future trigger points
(scaffold-time auto-review, claim-gate re-review, manual /run-script-reviewer-agent
slash command) are noted as TODOs in the agent's Roadmap section.


Risk Profile
-------------

CREATES files under `examples/{PROJECT_ID}/`. For scope=project with
new code stubs, also creates files under `code-dev/` and `code/hainn/`.
Refuse to overwrite existing names — abort and recommend `-organize`.

When dispatching to a task-type specialist, the same blast radius
applies — specialists also CREATE files under `examples/`.
