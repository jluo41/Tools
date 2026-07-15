---
name: haipipe-task
description: "Internal-execution EXECUTOR: runs the 4-phase lifecycle (Plan → Build → Execute → Report) on a task-folder, iterates it over a task-group, or dispatches to a type specialist to scaffold; the `qa` verb is its one question door (fn/qa.md). Trigger: task, task folder, task group, plan, build, execute, report, run, scan-status, qa, QA file, state, /haipipe-task."
argument-hint: "[scope] [args...] | qa \"<question>\" [<task-folder>] [--check-only]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill, Workflow
metadata:
  version: "6.2.0"
  last_updated: "2026-07-14"
  summary: "Build orchestrator: the 4-phase code lifecycle (Plan → Build → Execute → Report) for task-folders and task-groups, plus the `qa` question door. v6.x — the task layer is CONSUMER-UNAWARE, and a QA file is a TICKET that becomes a RECEIPT: it carries ONE mutable `state:` line (working | answered | superseded-by), claimed at the qa gate's ③ decision and completed at Report. THE LOAD-BEARING INVARIANT IS *ONE WRITER*, NOT *WRITE-ONCE*. Full contract: fn/qa.md."
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

Skill: haipipe-task (orchestrator)
===========================================

Build orchestrator organized around the **task hierarchy**:


> JL: I think we can also add the QA folder. but QA folder is optional, only when we have haipipe-task qa is called. 
>> CC 22:40: [SOLVED] Added QA/ to the structure, marked OPTIONAL (appears only once `qa` writes a digest).
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

```
/haipipe-task plan <task-folder-path>                Phase 1: design the IPO contract
/haipipe-task build <task-folder-path>               Phase 2: implement the contract as code
/haipipe-task execute <task-folder-path>              Phase 3: run the code (or human runs manually)
/haipipe-task report <task-folder-path>               Phase 4: summarize results vs plan

/haipipe-task <existing-task-folder-path>             full lifecycle (all 4 stages)
/haipipe-task <existing-task-group-path>              iterate: full lifecycle on each child task-folder
/haipipe-task <stage> <existing-task-group-path>      iterate: that stage on each child task-folder

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
Phase 1: PLAN — the contract (what the script SHOULD do)
  creates:   workflow/plan.yaml              task-level IPO (Run/Gate1/Gate2)
             workflow/plan-script-<name>.yaml script-level IPO (type-specific phases)
  reads:     *.py (if exists),
             **/haipipe-task-for-<type>/ref/workflow-plan-sample.yaml (nested under its domain folder)
  agents:    creator drafts plan → reviewer checks IPO compliance → ↺ revise

Phase 2: BUILD — the implementation (code that matches the plan)
  creates:   {NN}_{task_name}.py             main script (or fixes existing)
             configs/<run>.yaml              frozen parameters
             runs/<run>.sh                   papermill wrapper
             notebooks/                      empty dir (populated at runtime)
             CODE_REVIEW.md                  Gate 1 review (reviewer creates)
  reads:     workflow/plan.yaml, haipipe-task/ref/authoring-conventions.md
  agents:    creator writes code → reviewer does Gate 1 code review → ↺ revise
  after:     human can run directly: bash runs/<run>.sh

Phase 3: EXECUTE — just run (no creation, no modification)
  generates: results/<run>/metrics.json      output metrics
             results/<run>/runtime.yaml      run status/timing
             results/<run>/*.md, *.csv       other outputs
             notebooks/<run>.ipynb           papermill execution record
  runs:      bash runs/<run>.sh (human or autoExecute)
  agents:    none — this is a run, not an agent task

Phase 4: REPORT — summarize (what actually happened vs the plan)
  creates:   workflow/report.yaml            task-level report mirroring plan
             workflow/report-script-<name>.yaml script-level report
             RUN_AUDIT.md                    Gate 2 review (reviewer creates)
  completes: QA/<n>-<slug>.md                the CLAIM raised at the qa gate's ③ decision
                                             becomes the RECEIPT here: `state: answered`
                                             + the `## Answer` body. On gate ② (digest) it
                                             is CREATED here, once, complete.
                                             (see "The QA/ folder" below)
  reads:     workflow/plan*.yaml, results/<run>/*, CODE_REVIEW.md
  agents:    creator drafts report → reviewer checks accuracy → ↺ revise
```


File ownership is strict: 
Plan touches only `workflow/plan*.yaml`. 
Build touches only code/configs/runs. 
Execute touches only `results/` and `notebooks/`. 
Report touches only `workflow/report*.yaml`, `RUN_AUDIT.md`, and — when one is due — `QA/`.

**QA is the DIRECTION-POINTER above the four phases — it WRAPS them and decides whether to enter them at all.** 
A `qa` question hits a 3-way gate: ① an existing `QA/` answer → return it; ② the answer already sits in `results/` → digest it, no run; ③ neither → ENTER Plan → Build → Execute → Report at the shallowest depth that answers it. 
So QA sits ONE LEVEL ABOVE the lifecycle: ①/② read what already exists, ③ enters the phases (writing a `working` claim before Plan, the answer at Report). See `fn/qa.md`.
> JL: 我觉得这 QA 的描述不是很准确，你更应该说它是一个指明方向的东西。 就是说，QA 可以去“要不要进入 Plan、Build、Execution、Report”的东西，当然也可以直接去读现有 Task Folder 内部的结果。
所以它更像是 workflow 上面一层的东西，包裹这个phase。你想想这个 logic。
>> CC 22:40: [SOLVED] Agreed — your framing is better; rewrote it above. QA is NOT a 5th phase; it is the ENTRY-DECISION layer that WRAPS the four phases and points the direction — ①/② read what already exists, ③ decides whether (and how deep) to enter Plan→Build→Execute→Report. Exactly fn/qa.md's gate.
> JL: I still have a question: for Plan, Build, Execute, Report, do we call them "Stage" or call them "Phase"? I prefer to use Phase. 
>> CC 22:40: [DONE in this file · specialist sweep PENDING] Phase — it reads right with "QA wraps the phases" above. THE LOGIC (one snag): three things want two words — (a) the lifecycle P/B/E/R, (b) the IPO chunks inside a plan.yaml (Run/Gate1/Gate2), (c) the 6-stage DATA pipeline (0-RawDataStore…6-EndpointStore). haipipe-workflow already reserves "Phase" for (b) and "Stage" for (c). RESOLUTION: P/B/E/R = PHASE (your call); "Stage" stays for the 6-stage data pipeline ONLY; Run/Gate1/Gate2 remain the plan's internal IPO detail. Renamed P/B/E/R Stage→Phase in THIS file; the /haipipe-task-for-* scaffold docs still say "Stage 1: PLAN" — that careful cross-file sweep (must NOT touch data-pipeline Stage 0-6) is the next step. NOTE: the dispatch machinery + the workflow.js `stages:` PARAM stay `stages:` for now — that's CODE, renamed only in the deeper sweep. (haipipe-workflow calls P/B/E/R "acts" — cross-skill alignment left for R1.)

The `workflow/` folder is the task's observability surface: Plan = intent, Report = evidence, same IPO shape at both levels (schema: `task/haipipe-workflow/ref/plan-schema.md`).

A task ends at Report: it produces `results/` and stops. 

> JL: for the following, saying: if QA is called, it will use results to answer the QA-task.md.
>> CC 22:40: [SOLVED] Yes — that's gate ②: when `qa` is called and `results/` already hold the answer, it READS results/ and writes the readable `QA/<n>-<slug>.md` digest (no run). That digest IS the answer a consumer reads — never `results/` directly.
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
That is task work, not anyone else's. 
> JL: That is task work, not anyone else's.  这句话有点奇怪，你怎么理解这句话呀？要删掉吗？
> JL: for QA, we might also want to include P-B-E-R, when we need to do it.


**THE SIDE DOOR — the `qa` verb.** 
Questions arrive through exactly one door, `fn/qa.md`, 
and they arrive as ONE QUESTION IN GENERAL LANGUAGE — never an id, never a stake, never a reference to whoever asked. 
The verb answers it or REFUSES it, and returns a path. 
It never learns who asked, or why, and must not try to find out.


```
/haipipe-task qa "<question>" [<task-folder>]

  ① QA SCAN    grep <task-folder>/QA/*.md — READ THE STATE LINE:                       ~0
                 state: answered  → return the PATH
                 state: working   → SOMEONE IS ALREADY ON IT. Return the path +
                                    "in progress since <started>". DO NOT RE-RUN.
                 working, EXPIRED past QA_WORKING_TTL_HOURS → zombie: RESTART it
                 superseded-by: X → follow the chain, return the LIVE answer
  ② DIGEST     results/ answer it, no readable digest? → write QA/<n>-<slug>.md cheap
               ONCE, COMPLETE, `state: answered`, from EXISTING artifacts; run no code
  ③ P-B-E-R    neither → ⚑ CLAIM FIRST (write the QA file with `state: working` +
               `started:` under `set -C`), then run the lifecycle at the SHALLOWEST depth
               that answers it (0 READ · 1 NEW RUN+config · 2 NEW SCRIPT · 3 NEW TASK-FOLDER),
               and COMPLETE the same file at Report (`state: answered` + `## Answer`)
  🚫 REFUSE    out of scope for the task layer (e.g. a literature question) — say so;
               RELEASE any claim; the caller re-routes
```

Three callers, one identical door: a human steering an exploration, the orchestrator agent self-directed, or a relayed question from elsewhere. 
None of them gets a special path.

Full contract: `fn/qa.md`.

---

The QA/ folder (OPTIONAL, per task-folder)
-------------------------------------------

```
tasks/<group>/<NN>_<name>/
  ├── workflow/plan.yaml       the question, code-oriented       (task layer's own)
  ├── results/                 the answer, code-oriented         (task layer's own)
  └── QA/                      the answer, READABLE + indexed    (task layer's own) — OPTIONAL
        ├── 1-cycle-indicator.md
        └── 2-female-cgm-volume.md
```

**A QA file is a TICKET that becomes a RECEIPT** — ONE mutable `state:` line (`working | answered | superseded-by:`) that this layer CLAIMS at the qa gate's ③ decision and COMPLETES at Report; the body below it is written once.
⚠️ ONE WRITER = this layer. A CONSUMER (probe/paper/application) must NEVER create, claim, edit, or supersede a QA file — a consumer-planted `working` file is the retired `_ASK/` stub in a `QA/` costume, and is FORBIDDEN.
It is the HUMAN-readable answer: plain prose + `[→ results/…]` anchors, and NO consumer vocabulary (no claim ids, no "the paper").
Everything mechanical — the file template, `<n>`-numbering (the index), the `set -C` race guard, `started:`/TTL expiry, supersession, the three reasons a QA file may exist, status derivation, the checker codes — lives in `fn/qa.md`. Read it before touching a QA file.

Not every task-folder has a `QA/`. That is fine and normal.

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

Dispatch Table
--------------

Each verb's inputs and full contract live in its own `fn/` file — read that, do not re-derive from here.

```
Scope                  Owner / route                         Function file
---------------------- ------------------------------------- ----------------------
task-folder            dispatch by task-type to its           (the 9-row type table
                       specialist                              at the top of this file)
task-group (iterate)   this skill: iterate children           Step 3d
task-group (scaffold)  this skill                             fn/task-group.md
qa                     this skill                             fn/qa.md
scan-status            this skill                             fn/scan-status.md
run                    this skill                             fn/run.md
audit                  this skill                             fn/audit.md
plan                   this skill                             fn/stage-plan.md
report                 this skill                             fn/stage-report.md
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
      - path is an existing task-folder → scope=single-stage on that folder (Step 3c).
      - path is an existing task-group → scope=task-group-iterate with stages=[that stage] (Step 3d).
  (2) `task-folder` as first positional → scope=new task-folder (scaffold). `task-group` as first positional → scope=new task-group: read `fn/task-group.md` and run it inline. Stop.
  (3) first positional is a known task-type (`data` / `raw` / `algo` / `fit` / `eval` / `display` / `individual` / `agent` / `endpoint`) → scope=task-folder, task-type=that positional.
  (4) first positional is a path to an existing task-group → scope=task-group-iterate (Step 3d).
  (5) first positional is a path to an existing task-folder → scope=full lifecycle (all 4 stages via Step 3c).
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
  - scope=full lifecycle → run all 4 stages via Step 3c (Workflow tool)
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

  (3) KEYWORD-INFERRED — scan free-text args for keywords (table below). First match (left-to-right in args) wins.

        ┌────────────┬─────────────────────────────────────────────────────────────────┐
        │ raw        │ raw · ingest · extract table · databricks pull · catalog ·      │
        │            │ 0-RawDataStore · database 拿数据                                     │
        │ data       │ build · source · record · dataset · cgm ·                       │
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
        │ endpoint   │ endpoint · deploy · package · serve · sagemaker · databricks ·  │
        │            │ mlflow · Endpoint_Set · inference api                           │
        ├────────────┼─────────────────────────────────────────────────────────────────┤
        │ STATA      │ stata · do-file · .do · cms · case-pipeline · trigger cases ·   │
        │ (engine)   │ analysis table · reg · regression · ols · iv · neat · bene_info │
        └────────────┴─────────────────────────────────────────────────────────────────┘

  Stata engine-detect → DELEGATE: hand off to `/haipipe-task-for-stata` which owns stage disambiguation: `Skill("haipipe-task-for-stata", args="<remaining_args> [--auto]")`
  Confidence: medium. AUTO → accept. Interactive → propose; one-line ASK to confirm.

  (4) STILL UNKNOWN: AUTO → status: blocked. Interactive → ASK with all 9 type options (plus Stata engine).


Step 3b (scope=task-folder only): Parent existence cascade.

  Before dispatching to `/haipipe-task-<type>`, verify all ancestors exist. Order: project → task-group → task-folder.

  Resolve target paths: PROJECT_PATH = `examples/{PROJECT_ID}/`, GROUP_PATH = `PROJECT_PATH/tasks/{LETTER}{NN}_<group_name>/` (letter is project-specific, NOT tied to task-type).

  (1) Project check: EXISTS → continue. MISSING + `--project-id` given → scaffold via `Skill("haipipe-project", args="<PROJECT_ID> --auto")` (project setup lives in /haipipe-project). MISSING + no `--project-id` → blocked (AUTO) or ASK (interactive).

  (2) Group check: EXISTS → continue. MISSING + `--group` given → scaffold via `Skill("haipipe-task", args="task-group <group> --auto")` (fn/task-group.md). MISSING + no `--group` → blocked (AUTO) or ASK (interactive).

  Only after both checks pass: `Skill("haipipe-task-for-<type>", args="<remaining_args> --project-id <PROJECT_ID> --group <group_id> [--auto]")`


Step 3c: Full lifecycle or single stage.

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

  For single-stage commands (`/haipipe-task plan <path>`), pass only that stage: `stages: ["plan"]`.

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
      - Call Workflow with the existing `task-lifecycle.workflow.js`, passing the child path and the requested stages:
        ```
        Workflow({
          scriptPath: "Tools/plugins/haipipe-toolkit/skills/task/haipipe-task/ref/task-lifecycle.workflow.js"
        }, {
          task_folder: "<group-path>/<child>/",
          type: null,
          stages: <requested stages or ["plan", "build", "execute", "report"]>,
          autoExecute: false
        })
        ```
      - Collect the result. If a child fails (status=failed), log the failure and continue to the next child — do NOT stop the group iteration.

  (4) AGGREGATE — after all children complete, emit a group summary: one `[i/N] <child> —
      ok|failed (<per-stage verdicts>)` line per child, then an `Overall: N ok, M failed` tally.


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
/haipipe-task       .../tasks/B03_band4/01_band4    task-FOLDER: all 4 stages
/haipipe-task plan  .../tasks/B03_band4/01_band4    task-FOLDER: one stage
/haipipe-task       .../tasks/B03_band4            task-GROUP:  all 4 stages on EACH child
/haipipe-task plan  .../tasks/B03_band4            task-GROUP:  that stage on EACH child

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
