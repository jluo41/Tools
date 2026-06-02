---
name: haipipe-task
description: "Build orchestrator for haipipe-project. Routes scope=project / task-group / task-folder; for scope=task-folder, dispatches to one of seven task-type specialists (data / algo / training / eval / display / individual / agent). Replaces the older monolithic -task specialist with a router + per-type series. Called by /haipipe-project orchestrator. Direct invocation works for scaffold work."
argument-hint: "[scope] [args...]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "1.0.0"
  last_updated: "2026-05-31"
  summary: "Build orchestrator for haipipe-project."
  changelog:
    - "1.0.0 (2026-05-31): baseline metadata added."
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
task-type     Group letter   Specialist                              Cross-skill
------------  -------------  --------------------------------------  --------------------------
data          D              /haipipe-task-for-data              /haipipe-data
algo          X              /haipipe-task-for-algo              /haipipe-nn-algo
training      A              /haipipe-task-for-training          /haipipe-nn-tuner+instance
eval          B              /haipipe-task-for-eval              (project-local; future)
display       C              /haipipe-task-for-display           (independent)
individual    E              /haipipe-task-for-individual        /haipipe-individual
agent         F              /haipipe-task-for-agent             (none yet)
inference     P              /haipipe-task-for-inference         /haipipe-end-endpointset (profile)
```

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
and the shared engine contract (`ref/stata-dialect.md` + the three Stata ref
templates). This skill does NOT route stata stages itself — it hands off once
the engine is detected as Stata. The four children keep all structure invariants
(hierarchy, RUNNAME spine, light/heavy, diagram-as-doc) and emit `runtime.yaml`
for a unified `task-log.md` across Python and Stata tasks.

Called by `/haipipe-project` when the request is to **create** something
in the hierarchy. For audit / read see `-inspect`; for moves see `-organize`.

---

Commands
--------

```
/haipipe-project task                                ASK which scope
/haipipe-project task project [id]                   scaffold a new project (here)
/haipipe-project task task-group                     scaffold a new task-group (here)
/haipipe-project task task-folder                    ASK task-type, then dispatch
/haipipe-project task task-folder <type> [args...]   dispatch to type specialist
/haipipe-project task run [task-path] [run-name]     scaffold a new run (asks _meta)
```

Shorthand: `/haipipe-project task` with no scope and no args defaults to
`run` (most common ask once a task-folder exists; falls back to
`task-folder` if cwd is not a task-folder yet).

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
```

Task-type → specialist mapping (for scope=task-folder):

```
task-type     Group letter   Specialist                              Cross-skill
------------  -------------  --------------------------------------  --------------------------
data          D              /haipipe-task-for-data              /haipipe-data
algo          X              /haipipe-task-for-algo              /haipipe-nn-algo
training      A              /haipipe-task-for-training          /haipipe-nn-tuner+instance
eval          B              /haipipe-task-for-eval              (project-local; future)
display       C              /haipipe-task-for-display           (independent)
individual    E              /haipipe-task-for-individual        /haipipe-individual
agent         F              /haipipe-task-for-agent             (none yet)
inference     P              /haipipe-task-for-inference         /haipipe-end-endpointset (profile)
```

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

  (2) CWD-INFERRED — pwd matches
        `examples/Proj*/tasks/{LETTER}{NN}_*/`
      Group letter maps deterministically to task-type:

        A → training      D → data         E → individual
        B → eval          X → algo         F → agent
        C → display

      Confidence: high. Behavior:
        - AUTO         → accept; log "inferred from cwd: <type>"
        - interactive  → propose; one-line ASK to confirm

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
    GROUP_LETTER = the letter required by task-type (see Step 3a table):
                     A=training · B=eval · C=display · D=data ·
                     E=individual · F=agent · P=inference · X=algo
    GROUP_PATH   = `PROJECT_PATH/tasks/{GROUP_LETTER}{NN}_<group_name>/`
                     (or `PROJECT_PATH/tasks/X_algo/` for algo)

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
