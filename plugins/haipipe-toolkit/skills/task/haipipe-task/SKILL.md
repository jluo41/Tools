---
name: haipipe-task
description: "Internal-execution EXECUTOR: runs the 4-phase lifecycle (Plan → Build → Execute → Report) on a task-folder, iterates it over a task-group, or dispatches to a type specialist to scaffold; the `qa` verb is its one question door (fn/qa.md). Trigger: task, task folder, task group, plan, build, execute, report, run, scan-status, qa, QA file, state, /haipipe-task."
argument-hint: "[scope] [args...] | qa \"<question>\" [<task-folder>] [--check-only]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill, Workflow
metadata:
  version: "0.6.3"
  last_updated: "2026-07-19"
  summary: "Build orchestrator: the 4-phase code lifecycle (Plan → Build → Execute → Report) for task-folders and task-groups, plus the `qa` question door. v6.x — the task layer is CONSUMER-UNAWARE, and a QA file is a TICKET that becomes a RECEIPT: it carries ONE mutable `state:` line (working | answered | superseded-by), claimed at the qa gate's ③ decision and completed at Report. THE LOAD-BEARING INVARIANT IS *ONE WRITER*, NOT *WRITE-ONCE*. Full contract: fn/qa.md."
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

Skill: haipipe-task (orchestrator)
===========================================

Build orchestrator organized around the **task hierarchy**:


```
project           examples/Proj{...}/
  └── task-group  tasks/{G}{NN}_{name}/
        └── task-folder  <name>/{*.py, configs/, runs/, results/, notebooks/}
              QA/                              OPTIONAL — appears only when `qa` is called
              `{NN}_<name>` is the RECOMMENDED name for a NEW folder — match the siblings
              in this group. It is NOT a filter: real task-folders include B4_fit_scaling_law
              and C3-Visual-ForecastScaling. Detect a task-folder by STRUCTURE, never by name.
```

This skill owns **task-folder** and **task-group** scope. 
For a task-folder, it runs the 4-phase code lifecycle (Plan → Build → Execute → Report) or dispatches to a type specialist for scaffolding. 
For a task-group, it iterates over each child task-folder and runs the lifecycle on each one. Type specialists (one per type):

```
task-type     Specialist                              Cross-skill
------------  --------------------------------------  --------------------------
data          /haipipe-task-for-data              /haipipe-data
raw           /haipipe-task-for-raw               /haipipe-data-raw (Stage 0: Databricks → parquet)
algo          /haipipe-task-for-algo              /haipipe-nn-algo
fit           /haipipe-task-for-fit               /haipipe-nn-tuner+instance
eval          /haipipe-task-for-eval              (project-local; future)
display       /haipipe-task-for-display           (independent)
individual    /haipipe-task-for-individual        /haipipe-individual
agent         /haipipe-task-for-agent             /haipipe-task-llm-engine (LLM call runtime)
endpoint      /haipipe-task-for-endpoint          /haipipe-end (package + deploy)
```

NOTE: group letters (A01_, B01_) are project-specific, NOT type indicators — detect type from script content, never the letter. Per-type default letters + the "project scheme wins" rule: `ref/hierarchy.md`.

Stata specialist (engine = Stata, NOT papermill):
`engine = Stata → /haipipe-task-for-stata` — on detection, hand off WHOLESALE; the specialist owns cms/case/data/reg, its `{LNN}` stage-letter alphabet, and the engine contract in its own `ref/`.


Routing principle: this skill is the HIGH-LEVEL router. 
It owns only the engine-agnostic invariants (`ref/hierarchy.md`, `ref/task-structure.md` for task-group / task-folder / diagram / run-script layout, authoring conventions). 
Each `/haipipe-task-for-<engine>` child owns its OWN `ref/` (templates + dialect); route to the child and read the child's `ref/`, never keep engine specifics here.

Project setup (Project-*/ProjX-* containers) lives in `/haipipe-project`. 


---

Commands
--------

Each verb's full contract lives in its own `fn/` file (cited below) — read that, do not re-derive from here.

```
/haipipe-task plan <task-folder-path>                Phase 1: design the IPO contract (fn/stage-plan.md)
/haipipe-task build <task-folder-path>               Phase 2: implement the contract as code
/haipipe-task execute <task-folder-path>              Phase 3: run the code (or human runs manually)
/haipipe-task report <task-folder-path>               Phase 4: summarize results vs plan (fn/stage-report.md)

/haipipe-task <existing-task-folder-path>             full lifecycle (all 4 phases)
/haipipe-task <existing-task-group-path>              iterate: full lifecycle on each child task-folder
/haipipe-task <phase> <existing-task-group-path>      iterate: that phase on each child task-folder

/haipipe-task task-folder <type> [args...]            scaffold a NEW task-folder via type specialist
/haipipe-task task-group <group-path|name>            scaffold a NEW task-group (fn/task-group.md)

/haipipe-task run <task-folder-path> [run-name]       execute one runs/*.sh with logging conventions (fn/run.md)
/haipipe-task audit <task-group-or-folder-path>       structural audit vs the four-sister contract (fn/audit.md)
/haipipe-task scan-status [project-path]              status scan across task-groups (fn/scan-status.md)

/haipipe-task qa "<question>" [<task-folder>]         THE QUESTION DOOR: one general question in, a QA-file PATH out (fn/qa.md)

/haipipe-task feedback "<text>"                       capture skill feedback (merge-or-create), ROUTED to the domain folder it concerns
/haipipe-task feedback list [unit]                    aggregate open feedback across ALL inboxes (grouped by unit)
/haipipe-task feedback move <file> <unit>             re-route a mis-filed feedback item
/haipipe-task digest ["<session-name|id>"] [--dry-run]  digest a session (current, or a PAST one named/id'd, run from fresh): harvest feedback, dedup, confirm-gate, route to inboxes
```

---

Four Phases (code lifecycle)
------------------------------

All four phases answer one question: **"is the implementation right?"**

```
Plan (规)     creates   workflow/plan.yaml + workflow/plan-script-<name>.yaml (task + script IPO)
              agents    creator drafts → reviewer checks IPO compliance → ↺
Build (建)    creates   <NN>_<task>.py · configs/<run>.yaml · runs/<run>.sh · notebooks/ ·
                        CODE_REVIEW.md (Gate 1)
              agents    creator writes → reviewer Gate-1 review → ↺   · then human: bash runs/<run>.sh
Execute (行)  generates results/<run>/{metrics.json, runtime.yaml, *.md, *.csv} · notebooks/<run>.ipynb
              agents    none — just `bash runs/<run>.sh` (human or autoExecute)
Report (报)   creates   workflow/report.yaml + report-script-<name>.yaml · RUN_AUDIT.md (Gate 2)
              completes QA/<n>-<slug>.md when the qa gate ③ claimed one (see "The QA/ folder")
              agents    creator drafts → reviewer checks accuracy → ↺
```
Each phase READS the prior phase's output + its type's `ref/` (plan-sample · authoring-conventions · plan-schema); the exact per-phase reads live in `fn/stage-plan.md` and `fn/stage-report.md`.


File ownership is strict: 
Plan touches only `workflow/plan*.yaml`. 
Build touches only code/configs/runs. 
Execute touches only `results/` and `notebooks/`. 
Report touches only `workflow/report*.yaml`, `RUN_AUDIT.md`, and — when one is due — `QA/`.

**QA is the DIRECTION-POINTER above the four phases — it WRAPS them and decides whether to enter them at all.** 
A `qa` question hits a 3-way gate: ① an existing `QA/` answer → return it; ② the answer already sits in `results/` → digest it, no run; ③ neither → ENTER Plan → Build → Execute → Report at the shallowest depth that answers it. 
So QA sits ONE LEVEL ABOVE the lifecycle: ①/② read what already exists, ③ enters the phases (writing a `working` claim before Plan, the answer at Report). See `fn/qa.md`.

The `workflow/` folder is the task's observability surface: Plan = intent, Report = evidence, same IPO shape at both levels (schema: `task/haipipe-workflow/ref/plan-schema.md`).

A task ends at Report: it produces `results/` and stops. 

The readable answer to any question about those results is the `QA/` digest this layer writes; a consumer reads THAT, never `results/` directly. This layer tracks no consumers.

---

The task session's two modes
-----------------------------

**PRIMARY — autonomous P-B-E-R.** 
The task session runs Plan → Build → Execute → Report for its own sake: 
train, sweep, profile, scan. No question is pending. 
No one asked. 
This IS the project's research, and the bank grows here, autonomously.

**ANSWERABILITY WORK — also task-native, also with no question pending.** 
A task session may legitimately:
- write a `QA/` digest for a finding worth digesting, and
- build or refactor code so that FUTURE questions are cheap to answer.

It does not know WHICH questions will come. 
It makes the bank EASIER TO ASK. 
Making the bank easy to query is the executor's OWN work — a consumer (paper/application) never reaches in to do it.


**THE SIDE DOOR — the `qa` verb.** 
Questions arrive through exactly ONE door: one question in general language (no id, no stake, no reference to whoever asked), a QA-file PATH out. 
The verb answers it via the ①②③ gate above, or REFUSES it (out of scope — e.g. a literature question). 
Three callers — a human, the orchestrator agent (self-directed), a relayed question — one identical door; none gets a special path. 
It never learns who asked, or why. Full contract: `fn/qa.md`.

---

The QA/ folder (OPTIONAL, per task-folder)
-------------------------------------------

The readable answer, per task-folder: `QA/<n>-<slug>.md` — one mutable `state:` line, ONE WRITER (this layer); a CONSUMER (probe/paper/application) NEVER writes one.
Plain prose + `[→ results/…]` anchors, no consumer vocabulary (no claim ids, no "the paper"). Not every task-folder has a `QA/`, and that is normal.
The file template, the state-line + `started:`/TTL, supersession, and the checker codes live in `fn/qa.md` — read it before touching a QA file.

---

Agents
------

Three agents in `task/agents/` form the orchestrator/creator/reviewer triad. 
Creator and reviewer always work as a pair — creator produces, reviewer evaluates, loop if revise; the orchestrator agent is the non-interactive dispatch target that coordinates them.

```
task/agents/
  haipipe-task-orchestrator-agent.md  dispatch target — runs the lifecycle by coordinating the pair
  haipipe-task-creator-agent.md       produces artifacts (plan, code, report)
  haipipe-task-reviewer-agent.md      evaluates artifacts (IPO compliance, code bugs, result accuracy)
```

The lifecycle workflow (`ref/task-lifecycle.workflow.js`) orchestrates the loop:
1. Creator agent produces the stage's artifact
2. Reviewer agent evaluates → `pass` / `warn` / `revise` / `fail`
3. First `warn` → feeds issues back to creator for one retry
4. Second `warn` or `pass` → advance to next stage
5. `fail` → stop, human decides

The creator never reviews its own work. The reviewer never produces artifacts. This separation is the core invariant.

The reviewer catches **intent-vs-implementation mismatches** — silent semantic bugs where the code runs but doesn't measure what the writer intended. 
Independence comes from fresh-agent reasoning: the reviewer starts with clean context, never the creator's 

Author convention: `<TASK_NAME>.py` MUST have an `Intent` section in its docstring (template: `ref/intent-docstring-template.py`). Skip mechanisms for the run.sh pre-flight gate: `_meta.skip_review: true` in config, or `HAIPIPE_SKIP_REVIEW=1` env var.

---

Guardrails (learned the hard way — do NOT skip)
------------------------------------------------

```
GATE-1  PROVE A NEW GATE FAILS BEFORE YOU TRUST IT.
        Any new check, assertion, or verification task must be run against a
        KNOWN-BROKEN artifact FIRST and must report failure. A gate that has
        never failed is not yet a gate; it is an unverified claim that happens
        to print a tick.

        Three real cases, one session (SMSR4 v4 shadow, 260807):
          - A pipeline "reproducibility check" matched ANY score on one side to
            ANY score on the other, across DIFFERENT labels, with the two sides
            scaled 100x apart, and was non-fatal. It could not fail, and caught
            none of three shipped defects.
          - A newly written round-trip gate PASSED a known-broken live endpoint
            14/14, because it compared argmax(model) with argmax(returned scores)
            while the actual defect was in the SERVED label. Only running it
            against the broken artifact exposed the hole.
          - Fourteen test fixtures deliberately selected to have seven DIFFERENT
            correct answers had been flattened upstream to one, so the suite
            reported fourteen passes on something it could not observe.

        Practical form: give the gate an `--expect-fail` flag, run it on the old
        artifact, and only then run it on the new one. Record BOTH numbers.

GATE-2  A "pass" that compares the output to NOTHING is a smoke test, not a
        correctness test. Say which it is. "N/N passed" meaning "the response
        parsed and did not raise" must never be reported as evidence that the
        result is right.

GATE-3  A NAME THAT DOES NOT RESOLVE MUST RAISE. Across this codebase the common
        defect shape is a lookup that silently substitutes a default: an arm name
        filtered out by membership, a column read via `safe_get(row, name,
        default)`, a date falling back to `datetime.now()`. Each produces a
        plausible value and no error, so the bug ships looking healthy. When
        authoring or reviewing any task that reads names from a config, a schema,
        or a frame, assert the declared set resolves before using it, and name the
        missing entries in the message.

GATE-4  When a fixture is de-identified or regenerated, re-check that it still
        EXERCISES what it is meant to test. De-identification that pins a birth
        date to a constant and nulls a zip code removed 18.6% of a model's input
        and collapsed seven distinct expected answers into one.
```

---

Step-by-Step Protocol
----------------------

Step 0: Read `ref/hierarchy.md` first. 
It's the conceptual model for the task hierarchy (project → task-group → task-folder → run).

Step 1: Detect AUTO_MODE. 
Any of these flips it on: `--auto` anywhere in args, env var `CLAUDE_AUTO_HANDOFF=1` or `AUTO_MODE=1`, parent skill passed `--auto`. 
AUTO_MODE changes "ASK" steps into "accept best inference or return blocked"; it never changes what gets written.

Step 2: Resolve scope. Cascade:
  (0) UTILITY VERB — first positional is `feedback` or `digest` (route this BEFORE any other parsing; neither is a lifecycle scope, so do not continue to Step 3).
      `feedback` → read `fn/feedback.md` and run it inline (capture / list / move; routing rules, merge-or-create, inbox paths all live THERE). Stop.
      `digest` → read `fn/digest.md` and run it inline (resolve the target session first; mandatory confirm gate before filing). Stop.
  (0.5) UTILITY VERB `scan-status` — first positional is `scan-status` → read `fn/scan-status.md` and run it inline. Stop.
  (0.6) QUESTION DOOR `qa` — first positional is `qa` → read `fn/qa.md` and run it inline (the ①②③ gate; remaining args = the question, an OPTIONAL task-folder, OPTIONAL `--check-only`). Not a lifecycle scope: do not continue to Step 3. Stop.
        `--check-only` = DETECTION only (report the path, write nothing incl. NO CLAIM, never fall through to ③) — the probe MATCH step's free pass. Gate ①'s state-line branches, the strip-any-external-id rule, and the identical discovery-twin spelling all live in `fn/qa.md`.
  (1) explicit stage command (`plan` / `build` / `execute` / `report`) as first positional → check the path argument:
      - path is an existing task-folder → scope=single-phase on that folder (Step 3c).
      - path is an existing task-group → scope=task-group-iterate with stages=[that stage] (Step 3d).
  (2) `task-folder` as first positional → scope=new task-folder (scaffold). `task-group` as first positional → scope=new task-group: read `fn/task-group.md` and run it inline. Stop.
  (3) first positional is a known task-type (`data` / `raw` / `algo` / `fit` / `eval` / `display` / `individual` / `agent` / `endpoint`) → scope=task-folder, task-type=that positional.
  (4) first positional is a path to an existing task-group → scope=task-group-iterate (Step 3d).
  (5) first positional is a path to an existing task-folder → scope=full lifecycle (all 4 phases via Step 3c).
  (6) no args at all → default:
      - cwd is inside a task-folder → scope=full lifecycle (Step 3c).
      - cwd is inside a task-group (but not inside a task-folder) → scope=task-group-iterate (Step 3d).
      - else → scope=task-folder (scaffold).
  (7) still missing: AUTO → status: blocked. Interactive → ASK.

  Task-group vs task-folder — detect by STRUCTURE, never by NAME. A path is a task-FOLDER if it
  holds a `.py` at its root (or `workflow/`, `results/`, `configs/`, `runs/`). It is a task-GROUP
  if it holds task-folders and has no `.py` of its own.

  ⛔ NEVER key this on a name pattern. `{NN}_<name>` is the majority convention (235 of 342 real
  task-folders) but it is NOT a law: `B4_fit_scaling_law`, `C3-Visual-ForecastScaling`, `B6f_crosscompare`
  and `A4_data_population_comparison` are all real task-folders on disk, and a `{NN}_` filter skips
  every one of them — 31% of the bank. Structure is the truth; the name is a habit.

Step 3: Branch by scope:
  - scope=plan → run Stage 1 only (creator drafts plan.yaml, reviewer checks)
  - scope=build → run Stage 2 only (creator writes code, reviewer does Gate 1)
  - scope=execute → run Stage 3 only (bash runs/<run>.sh)
  - scope=report → run Stage 4 only (creator drafts report.yaml, reviewer checks)
  - scope=full lifecycle → run all 4 phases via Step 3c (Workflow tool)
  - scope=task-group-iterate → enumerate children, run per-child via Step 3d
  - scope=task-folder (new) → resolve task-type via Step 3a cascade, then Skill("haipipe-task-for-<type>", args="<remaining_args> [--auto]")


Step 3a (scope=task-folder only): Task-type inference cascade.

  Highest-to-lowest confidence:

  (1) EXPLICIT — type given as positional after `task-folder`, or already pinned at Step 2 cascade (2). Done.

  (2) SCRIPT-INFERRED — if pwd is inside an existing task-folder, read the main `*.py` script and `scripts/*.py` files. Detect type from imports and content:
    - `from haipipe` / `SourceFn` / `RecordFn` → data
    - `databricks` / `spark.sql` / `dbutils` / catalog extract → raw
    - `import torch` / `Trainer` / `sweep` → fit
    - `eval` / `metrics` / `score` → eval
    - `plt.` / `fig` / `savefig` / `.tex` → display
    - `stata` / `.do` / `preserve` → stata (delegate)
    - `agent` / `claude` / `anthropic` → agent
    - `Endpoint_Set` / `deploy` / `sagemaker` / `serve` → endpoint
  Confidence: high. AUTO → accept; log "inferred from script: <type>". Interactive → propose; one-line ASK to confirm.
  NOTE: never infer task-type from the group letter (letters are project-specific — see the NOTE under the type table).

  (3) KEYWORD-INFERRED — scan free-text args; first match (left-to-right) wins. Quick map
      (FULL keyword lists per type → `ref/type-inference.md`):
        raw·ingest·extract·catalog → raw       · build·source·record·dataset·cgm → data
        smoke·algo·forward-pass → algo          · train·fit·sweep·finetune → fit
        eval·score·metrics·mae·rmse → eval      · figure·table·plot·panel → display
        subject·patient·cgm-trace → individual  · agent·llm·prompt·claude → agent
        endpoint·deploy·package·serve → endpoint
      STATA (stata·.do·cms·case·reg·ols·iv) → DELEGATE to `/haipipe-task-for-stata`
        (it owns stage disambiguation): `Skill("haipipe-task-for-stata", args="… [--auto]")`.
  Confidence: medium. AUTO → accept. Interactive → propose; one-line ASK to confirm.

  (4) STILL UNKNOWN: AUTO → status: blocked. Interactive → ASK with all 9 type options (plus Stata engine).


Step 3b (scope=task-folder only): Parent existence cascade.

  Before dispatching to `/haipipe-task-<type>`, verify all ancestors exist. Order: project → task-group → task-folder.

  Resolve target paths: PROJECT_PATH = `examples/{PROJECT_ID}/`, GROUP_PATH = `PROJECT_PATH/tasks/{LETTER}{NN}_<group_name>/` (letter is project-specific, NOT tied to task-type).

  (1) Project check: EXISTS → continue. MISSING + `--project-id` given → scaffold via `Skill("haipipe-project", args="<PROJECT_ID> --auto")` (project setup lives in /haipipe-project). MISSING + no `--project-id` → blocked (AUTO) or ASK (interactive).

  (2) Group check: EXISTS → continue. MISSING + `--group` given → scaffold via `Skill("haipipe-task", args="task-group <group> --auto")` (fn/task-group.md). MISSING + no `--group` → blocked (AUTO) or ASK (interactive).

  Only after both checks pass: `Skill("haipipe-task-for-<type>", args="<remaining_args> --project-id <PROJECT_ID> --group <group_id> [--auto]")`


Step 3c: Full lifecycle or single phase.

  Run via the Workflow tool:

  ```
  Workflow({
    scriptPath: "Tools/plugins/haipipe-toolkit/skills/task/haipipe-task/ref/task-lifecycle.workflow.js"
  }, {
    task_folder: "<path>",
    type: "<detected from Step 3a, or null for auto-detect>",
    stages: ["plan", "build", "execute", "report"],
    autoExecute: false
  })
  ```

  For single-phase commands (`/haipipe-task plan <path>`), pass only that phase: `stages: ["plan"]`.

  All generated plan/report files follow the haipipe-workflow IPO schema at `task/haipipe-workflow/ref/plan-schema.md`. Every plan YAML starts with an IPO tree preview comment with emojis.


Step 3d: Task-group iteration (scope=task-group-iterate).

  The lifecycle scope stays at task-folder — this step just loops over children. No workflow/ artifacts are ever created at the group level.

  (1) ENUMERATE — list child task-folders in the group directory:
      ```
      for d in <group-path>/*/; do
        # a TASK-FOLDER is a directory that holds work — not one whose NAME matches a pattern
        [ -n "$(find "$d" -maxdepth 1 -name '*.py' -print -quit)" ] ||
        [ -d "$d/workflow" ] || [ -d "$d/results" ] || [ -d "$d/configs" ] || [ -d "$d/runs" ] || continue
        echo "$d"
      done | sort
      ```
      ⛔ Do NOT glob `{NN}_*/` — see the STRUCTURE-not-NAME rule in Step 2 (it skips 31% of
      the bank). The structural test also excludes `__pycache__/`, `figures/`, `sbatch/` and
      `diagram/` for free, because they hold no work.

  (2) CONFIRM — log the group path, the N children found (numbered `[i/N]`), and the stages
      to run. In interactive mode, ASK to confirm before proceeding. In AUTO_MODE, proceed
      directly.

  (3) ITERATE — for each child task-folder, in order:
      - Log: `── [i/N] <child_name> ──`
      - Call the SAME `Workflow(...)` as Step 3c, with `task_folder: "<group-path>/<child>/"`,
        `type: null`, and the requested `stages` (default all four).
      - Collect the result. If a child fails (status=failed), log the failure and continue to the next child — do NOT stop the group iteration.

  (4) AGGREGATE — after all children complete, emit a group summary: one `[i/N] <child> —
      ok|failed (<per-phase verdicts>)` line per child, then an `Overall: N ok, M failed` tally.


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
# the SAME path is a task-FOLDER or a task-GROUP; the verb is identical, the scope differs
/haipipe-task       .../tasks/B03_band4/01_band4    task-FOLDER: all 4 phases
/haipipe-task plan  .../tasks/B03_band4/01_band4    task-FOLDER: one stage
/haipipe-task       .../tasks/B03_band4            task-GROUP:  all 4 phases on EACH child
/haipipe-task plan  .../tasks/B03_band4            task-GROUP:  that phase on EACH child

# scaffold a NEW task-folder (dispatches to the type specialist)
/haipipe-task task-folder data
/haipipe-task task-folder eval --project-id Project-REACH-ADHD --group B03_band4

# the QUESTION DOOR — one general question in, a QA-file PATH out
/haipipe-task qa "Do any WellDoc tables carry a menstrual or cycle column?"
/haipipe-task qa "What is the fit exponent on the 4-model sweep?" examples/ProjA/tasks/B01_scaling/B4_fit_scaling_law

# direct specialist (bypass orchestrator)
/haipipe-task-for-data
```

---

Risk Profile
-------------

CREATES files under `examples/{PROJECT_ID}/`. Refuse to overwrite existing names — abort and recommend `-organize`.

When dispatching to a task-type specialist, the same blast radius applies — specialists also CREATE files under `examples/`.
