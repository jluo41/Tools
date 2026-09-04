---
name: haipipe-task
description: >-
  Task-family door for execution and reusable insight: runs Plan → Build →
  Execute → Report on jobs, iterates blocks, answers source
  questions through `qa`, and creates DIKW Insight Pages through `insight`.
  Use for task execution, Task Board status, QA files, or result
  interpretation. Hierarchy: block to job to task to run (task-group and
  task-folder are the pre-260829 names for block and job). Trigger: task,
  job, block, task folder, task group, Task Board, plan, build, execute,
  report, qa, insight, DIKW, /haipipe-task.
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill, Workflow
metadata:
  version: "0.12.6"
  last_updated: "2026-09-01"
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

Skill: haipipe-task (orchestrator)
===========================================

Build orchestrator organized around the **task hierarchy** (settled JL
260829; old names: task-group = BLOCK, task-folder = JOB):


```
project        examples/Proj{...}/
  └── block    tasks/bNN_{name}/           one large topic; prefer FEW blocks
        └── job    jNN_{name}/              self-contained, submittable (= Databricks Job)
              ├── tNN_<task>/              TASK = PAGE, self-contained (260830):
              │     ├── tNN_<task>.md          the page a reader opens
              │     ├── scripts/               THE TASK'S OWN CODE (260831); shared code is the job's src/
              │     │     ├── <stem>.py        the pipeline
              │     │     └── config/          INSIDE scripts/: a config sits beside the code that
              │     │                          reads it. SHARED (cohort.do) + PER-RUN rNN_<stem>, 1:1 with a ticket
              │     └── runs/rNN_<stem>.sh     TICKET: names its config; may carry SLICE settings
              │                                (year, source, fold), never a setting the config
              │                                already holds. Wherever a setting lives, the run
              │                                records it in results/<task>/<run>/runtime.yaml
              ├── src/                     SHARED by more than one task in this job. Two words on
              │                            purpose: `src/` is shared, `scripts/` is owned, so the
              │                            NAME says which without reading the path
              ├── sbatch/                  batcher that SPANS tasks (one for a single
              │                            task goes in tNN_<task>/sbatch/ instead)
              └── results/<task>/<run>/    a RUN is an execution, never a folder of its own
              ONE GRAMMAR at every level: <level letter b·j·t·r><NN>_<noun>_<qualifier>;
              the address is the prefixes joined, read off the path: b02j01t01r03
              (legacy: code at the task ROOT, pre-260831;
              FLAT job: .py at root + flat configs/ runs/ — one implicit task)
              TWO MODES:
              ① self-serving      output stays in the job     results/ notebooks/ QA/
              ② consumer-serving  output goes to a store      <store>/<job path>/
              the JOB's `store:` declaration picks ②; absent means ① (ref/hierarchy.md)
              ⚠️ HIGHEST PRIORITY: every name passes the STRANGER TEST — <noun>_<qualifier>,
              readable by someone who never opened the folder (ref/hierarchy.md "Naming").
              `jNN_<name>` is the shape of a NEW job (tNN_ for a task, rNN_ for a config);
              match the siblings in this block. It is NOT a filter: real jobs include B4_fit_scaling_law
              and C3-Visual-ForecastScaling. Detect a job by STRUCTURE, never by name.
```

This skill owns **job**, **block**, and the Task/Insights Board entry surface.
For a job, it runs the 4-phase code lifecycle (Plan → Build → Execute → Report) or dispatches to a type specialist for scaffolding. 
For a block, it iterates over each child job and runs the lifecycle on each one. Type specialists (one per type):

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
page          /haipipe-task-for-page              (serves ONE Board Page's task-route probe cards: values.yaml + QA + proposals)
```

NOTE: a block prefix (bNN_) carries no type information — detect type from script content, never from a name. Per-type default letters + the "project scheme wins" rule: `ref/hierarchy.md`.

Stata specialist (engine = Stata, NOT papermill):
`engine = Stata → /haipipe-task-for-stata` — on detection, hand off WHOLESALE; the specialist owns cms/case/data/reg, its `{LNN}` stage-letter alphabet, and the engine contract in its own `ref/`.


Routing principle: this skill is the HIGH-LEVEL router. 
It owns only the engine-agnostic invariants (`ref/hierarchy.md`, `ref/task-structure.md` for block / job / task / ticket layout, authoring conventions). 
Each `/haipipe-task-for-<engine>` child owns its OWN `ref/` (templates + dialect); route to the child and read the child's `ref/`, never keep engine specifics here.

Project setup (Project-*/ProjX-* containers) lives in `/haipipe-project`. 


---

Commands
--------

Each verb's full contract lives in its own `fn/` file (cited below) — read that, do not re-derive from here.

```
/haipipe-task plan <job-path>                        Phase 1: design the IPO contract (fn/stage-plan.md)
/haipipe-task build <job-path>                        Phase 2: implement the contract as code
/haipipe-task execute <job-path>                      Phase 3: run the code (or human runs manually)
/haipipe-task report <job-path>                       Phase 4: summarize results vs plan (fn/stage-report.md)

/haipipe-task <existing-job-path>                     full lifecycle (all 4 phases)
/haipipe-task <existing-block-path>                   iterate: full lifecycle on each child job
/haipipe-task <phase> <existing-block-path>           iterate: that phase on each child job

/haipipe-task job <type> [args...]                    scaffold a NEW job via type specialist
/haipipe-task block <block-path|name>                 scaffold a NEW block (fn/task-group.md)
   (`task-folder` and `task-group` are accepted ALIASES for `job` and `block` — the pre-260829 names)

/haipipe-task run <job-path> [run-name]               execute one ticket with logging conventions (fn/run.md)
/haipipe-task audit <block-or-job-path>               structural audit vs the runname-spine contract (fn/audit.md)
/haipipe-task scan-status [project-path]              status scan across blocks (fn/scan-status.md)

/haipipe-task qa "<question>" [<job-path>]            THE QUESTION DOOR: one general question in, a QA-file PATH out (fn/qa.md)
/haipipe-task insight "<question-or-topic>" [<board>]  create or resume one DIKW Insight Page (fn/insight.md)

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
Build (建)    creates   <task>/{code + config/<run>.yaml} · <task>/runs/<run>.sh ·
                        CODE_REVIEW.md (Gate 1)   (flat legacy: .py at root, configs/ + runs/ flat)
              agents    creator writes → reviewer Gate-1 review → ↺   · then human: bash <task>/runs/<run>.sh
Execute (行)  generates results/<task>/<run>/{metrics.json, runtime.yaml, *.md, *.csv} · notebooks/<task>/<run>.ipynb
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

## Which mode? Ask ONCE, at scaffold (JL 260823)

A job's mode is a property of what it is FOR, not of each execution, so it is
settled when the job is created and persisted as the JOB's `store:` declaration
(src/config-defaults.yaml nested, configs/_defaults.yaml flat —
never per-run, JL 260829). Run time never asks again.

Four branches. Only ONE of them prompts:

```
RESULT_STORE set in the env?   ─yes─▶  ② a consumer dispatched · SILENT
job `store:` already declared? ─yes─▶  ② already decided · SILENT
any board.md carrying `store:`  ─no──▶  ① nothing to serve · SILENT
under this project?
        │
      yes │  ◀── the ONLY branch that asks
        ▼
   🧑 "N board(s) here own a store. Does this job serve one?
       [1] <board> → <its store>
       [2] <board> → <its store>
       [n] no — keep output in the job"
        │
        ▼
   write the answer as the job's `store:` declaration, or omit it for [n]
```

Detection is one glob: `board.md` files under the project whose head carries a
`store:` line. Three of four branches stay silent, so the prompt is rare rather
than a tax.

**The ask BLOCKS; it does not default.** The entire class of bug this mechanism
addresses is silent misrouting, and a default that guesses ① reintroduces it in
the one situation where a person was present to prevent it. Scaffolding already
confirms new files, so the mode question rides along in a conversation that is
happening anyway.

A SECOND cohort of an existing job is a new config, so it passes through this
ask again — which is correct, because that is exactly when the answer can differ
from last time.

Everything after Build that is DATA-DEPENDENT lands under `$OUTPUT_ROOT`;
`CODE_REVIEW.md` is the exception and stays with the code, because it reviews
the code at a `git_sha` rather than a cohort's results. A job
runs in one of TWO first-class modes (JL 260821, `ref/hierarchy.md` § "Two run modes"):
SELF-SERVING keeps output in the job, the classic shape, unchanged;
CONSUMER-SERVING sends it to a store the consumer owns, which is what lets one
job answer the same question on a second cohort without being copied. Which
one applies is decided by who owns the answer, not by who launched the run.
Build's outputs stay in the job either way, because code and config ARE
the job.

**QA is the DIRECTION-POINTER above the four phases — it WRAPS them and decides whether to enter them at all.** 
A `qa` question hits a 3-way gate: ① an existing `QA/` answer → return it; ② the answer already sits in `results/` → digest it, no run; ③ neither → ENTER Plan → Build → Execute → Report at the shallowest depth that answers it. 
So QA sits ONE LEVEL ABOVE the lifecycle: ①/② read what already exists, ③ enters the phases (writing a `working` claim before Plan, the answer at Report). See `fn/qa.md`.

The `workflow/` folder is the task's observability surface: Plan = intent, Report = evidence, same IPO shape at both levels (schema: `task/haipipe-workflow/ref/plan-schema.md`).

**The unit symmetry (JL 260831)**: a task folder is a special page folder, and both carry the same two process lanes. `workflow/` is the MACHINE half (this folder, unchanged). `outline/` is the HUMAN half and is now legal in a task folder too: the prose plan a person ticks, the open `D<nn>` threads, and the log, in the page family's record shape (`haipipe-plugin-outline/ref/record-shape.md`). The board renders a task's `tNN_<task>.md` as a page already; `outline/` gives its human decisions the same home a page's have. First real instance: the page-serving collection job (`haipipe-task-for-page`).

Load `haipipe-run` for the neutral Level-4 identity and pairing contract.
The optional Task-side presenter is `haipipe-plugin-runs`, not Execution.
Execute remains phase 3 of P-B-E-R; **Runs** lists the durable attempts. For a
canonical nested Task Page it resolves the authored
`<task>/runs/<run>.sh` ticket against the Job-owned generated
`results/<task>/<run>/` and optional `notebooks/<task>/<run>.ipynb`. It never
copies those outputs into the Task Folder. A standalone/Discovery Folder uses
the Folder-local `runs/<run>.sh ↔ results/<run>/` dialect instead.

A task ends at Report: it produces `results/` and stops. 

The readable answer to any question about those results is the `QA/` digest this layer writes; a consumer reads THAT, never `results/` directly. This layer tracks no consumers.

**Insight is the KNOWLEDGE SURFACE above Task and Discovery evidence.** A Task Page reads one run against one task question; an Insight Folder may synthesize several Task Pages, QA answers, Discovery Pages, or prior Insight Folders around one consumer-neutral question. It carries the trace `D → I → K → W → RF`. Its Task Face may PageX-link the producing Folder and acquire an accepted QA answer through Probe, but it never executes that Folder or reads raw `results/` when QA/report is owed. Paper and Application read only settled **Reusable Findings** through PageX; they never cross into the producing Task Folder. An RF is unsigned, consumer-neutral evidence—not an Application Design Handoff, not a `serves:` decision, and never direct Design authority. An Application that uses it must own the downstream I1 registration and contextual, signed I5 Wisdom bridge.

### Incoming Application candidates

An accepted Design candidate may cross into an explicitly named executable
Folder at `workflow/inbox/application/<packet-id>.yaml`. The Application
crossing writer may add this immutable raw-material packet plus a reciprocal
PageX binding; it may not edit the target's plan, code, runs, results, QA, or
terminal state. The packet remains `state: proposed` until the target Task
owner validates it and enters its own Plan. Its grammar is owned by
`haipipe-application-workflow` X2. There is no Task plugin and no invisible
direct dispatch behind this inbox.

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

The QA/ folder (OPTIONAL, per job)
-------------------------------------------

The readable answer, per job: `QA/<n>-<slug>.md` — one mutable `state:` line, ONE WRITER (this layer); a CONSUMER (probe/paper/application) NEVER writes one.
Plain prose + `[→ results/…]` anchors, no consumer vocabulary (no claim ids, no "the paper"). Not every job has a `QA/`, and that is normal.
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
It's the conceptual model for the task hierarchy (project → block → job → task → run).

Step 1: Detect AUTO_MODE. 
Any of these flips it on: `--auto` anywhere in args, env var `CLAUDE_AUTO_HANDOFF=1` or `AUTO_MODE=1`, parent skill passed `--auto`. 
AUTO_MODE changes "ASK" steps into "accept best inference or return blocked"; it never changes what gets written.

Step 2: Resolve scope. Cascade:
  (0) UTILITY VERB — first positional is `feedback` or `digest` (route this BEFORE any other parsing; neither is a lifecycle scope, so do not continue to Step 3).
      `feedback` → read `fn/feedback.md` and run it inline (capture / list / move; routing rules, merge-or-create, inbox paths all live THERE). Stop.
      `digest` → read `fn/digest.md` and run it inline (resolve the target session first; mandatory confirm gate before filing). Stop.
  (0.5) UTILITY VERB `scan-status` — first positional is `scan-status` → read `fn/scan-status.md` and run it inline. Stop.
  (0.6) QUESTION DOOR `qa` — first positional is `qa` → read `fn/qa.md` and run it inline (the ①②③ gate; remaining args = the question, an OPTIONAL job path, OPTIONAL `--check-only`). Not a lifecycle scope: do not continue to Step 3. Stop.
        `--check-only` = DETECTION only (report the path, write nothing incl. NO CLAIM, never fall through to ③) — the probe MATCH step's free pass. Gate ①'s state-line branches, the strip-any-external-id rule, and the identical discovery-twin spelling all live in `fn/qa.md`.
  (0.7) KNOWLEDGE DOOR `insight` — first positional is `insight` → read `fn/insight.md`, resolve the Task/Insights Board, and create or resume one `page-type: insight` Page through `haipipe-page`. This is not P-B-E-R scope: do not continue to Step 3. Stop.
  (1) explicit stage command (`plan` / `build` / `execute` / `report`) as first positional → check the path argument:
      - path is an existing job → scope=single-phase on that job (Step 3c).
      - path is an existing block → scope=block-iterate with stages=[that stage] (Step 3d).
  (2) `job` (alias `task-folder`) as first positional → scope=new job (scaffold). `block` (alias `task-group`) as first positional → scope=new block: read `fn/task-group.md` and run it inline. Stop.
  (3) first positional is a known task-type (`data` / `raw` / `algo` / `fit` / `eval` / `display` / `individual` / `agent` / `endpoint` / `page`) → scope=job, task-type=that positional.
  (4) first positional is a path to an existing block → scope=block-iterate (Step 3d).
  (5) first positional is a path to an existing job → scope=full lifecycle (all 4 phases via Step 3c).
  (6) no args at all → default:
      - cwd is inside a job → scope=full lifecycle (Step 3c).
      - cwd is inside a block (but not inside a job) → scope=block-iterate (Step 3d).
      - else → scope=job (scaffold).
  (7) still missing: AUTO → status: blocked. Interactive → ASK.

  Block vs job — detect by STRUCTURE, never by NAME. A path is a JOB if it
  holds a `.py` at its root (or `scripts/`, `src/`, `workflow/`, `results/`, `configs/`, `runs/`). It is a
  BLOCK if it holds jobs and has none of those of its own.

  ⛔ NEVER key this on a name pattern. `{NN}_<name>` is the majority convention (235 of 342 real
  jobs) but it is NOT a law: `B4_fit_scaling_law`, `C3-Visual-ForecastScaling`, `B6f_crosscompare`
  and `A4_data_population_comparison` are all real jobs on disk, and a `{NN}_` filter skips
  every one of them — 31% of the bank. Structure is the truth; the name is a habit.

Step 3: Branch by scope:
  - scope=plan → run Stage 1 only (creator drafts plan.yaml, reviewer checks)
  - scope=build → run Stage 2 only (creator writes code, reviewer does Gate 1)
  - scope=execute → run Stage 3 only (bash the ticket)
  - scope=report → run Stage 4 only (creator drafts report.yaml, reviewer checks)
  - scope=full lifecycle → run all 4 phases via Step 3c (Workflow tool)
  - scope=block-iterate → enumerate children, run per-child via Step 3d
  - scope=job (new) → resolve task-type via Step 3a cascade, then Skill("haipipe-task-for-<type>", args="<remaining_args> [--auto]")


Step 3a (scope=job only): Task-type inference cascade.

  Highest-to-lowest confidence:

  (1) EXPLICIT — type given as positional after `job` (alias `task-folder`), or already pinned at Step 2 cascade (2). Done.

  (2) SCRIPT-INFERRED — if pwd is inside an existing job, read the main `*.py` script plus the task's `scripts/` and the job's `src/` code. Detect type from imports and content:
    - `from haipipe` / `SourceFn` / `RecordFn` → data
    - `databricks` / `spark.sql` / `dbutils` / catalog extract → raw
    - `import torch` / `Trainer` / `sweep` → fit
    - `eval` / `metrics` / `score` → eval
    - `plt.` / `fig` / `savefig` / `.tex` → display
    - `stata` / `.do` / `preserve` → stata (delegate)
    - `agent` / `claude` / `anthropic` → agent
    - `Endpoint_Set` / `deploy` / `sagemaker` / `serve` → endpoint
  Confidence: high. AUTO → accept; log "inferred from script: <type>". Interactive → propose; one-line ASK to confirm.
  NOTE: never infer task-type from the block letter (letters are project-specific — see the NOTE under the type table).

  (3) KEYWORD-INFERRED — scan free-text args; first match (left-to-right) wins. Quick map
      (FULL keyword lists per type → `ref/type-inference.md`):
        raw·ingest·extract·catalog → raw       · build·source·record·dataset·cgm → data
        smoke·algo·forward-pass → algo          · train·fit·sweep·finetune → fit
        eval·score·metrics·mae·rmse → eval      · figure·table·plot·panel → display
        subject·patient·cgm-trace → individual  · agent·llm·prompt·claude → agent
        endpoint·deploy·package·serve → endpoint
        collect·values·page-serving·probe-batch → page
      STATA (stata·.do·cms·case·reg·ols·iv) → DELEGATE to `/haipipe-task-for-stata`
        (it owns stage disambiguation): `Skill("haipipe-task-for-stata", args="… [--auto]")`.
  Confidence: medium. AUTO → accept. Interactive → propose; one-line ASK to confirm.

  (4) STILL UNKNOWN: AUTO → status: blocked. Interactive → ASK with all 10 type options (plus Stata engine).


Step 3b (scope=job only): Parent existence cascade.

  Before dispatching to `/haipipe-task-<type>`, verify all ancestors exist. Order: project → block → job.

  Resolve target paths: PROJECT_PATH = `examples/{PROJECT_ID}/`, BLOCK_PATH = `PROJECT_PATH/tasks/bNN_<block_name>/` (next free NN in pipeline order; the prefix carries no type information). Before minting a NEW block, check whether an existing one already owns the topic — prefer FEW blocks (ref/hierarchy.md § Level 2).

  (1) Project check: EXISTS → continue. MISSING + `--project-id` given → scaffold via `Skill("haipipe-project", args="<PROJECT_ID> --auto")` (project setup lives in /haipipe-project). MISSING + no `--project-id` → blocked (AUTO) or ASK (interactive).

  (2) Block check: EXISTS → continue. MISSING + `--group` given → scaffold via `Skill("haipipe-task", args="block <block> --auto")` (fn/task-group.md). MISSING + no `--group` → blocked (AUTO) or ASK (interactive).

  (0) NAME GATE, ⚠️ HIGHEST PRIORITY and checked BEFORE anything else at scaffold — every new block, job or task name must pass the stranger test (ref/hierarchy.md "Naming"): `<noun>_<qualifier>`, the noun a concrete thing, the qualifier what separates it from siblings; a shape word alone (pool, rank, data, analysis) FAILS. On failure: interactive → ASK "what thing? which one?" and compose the name; AUTO → status: blocked with the two questions. Never mint a name that a stranger cannot read.

  Only after both checks pass: `Skill("haipipe-task-for-<type>", args="<remaining_args> --project-id <PROJECT_ID> --group <block_id> [--auto]")`


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


Step 3d: Block iteration (scope=block-iterate).

  The lifecycle scope stays at job — this step just loops over children. No workflow/ artifacts are ever created at the block level.

  (1) ENUMERATE — list child jobs in the block directory:
      ```
      for d in <block-path>/*/; do
        # a JOB is a directory that holds work — not one whose NAME matches a pattern
        [ -n "$(find "$d" -maxdepth 1 -name '*.py' -print -quit)" ] || [ -d "$d/src" ] ||
        [ -d "$d/scripts" ] || [ -d "$d/workflow" ] || [ -d "$d/results" ] ||
        [ -d "$d/configs" ] || [ -d "$d/runs" ] || continue
        echo "$d"
      done | sort
      ```
      ⛔ Do NOT glob `{NN}_*/` — see the STRUCTURE-not-NAME rule in Step 2 (it skips 31% of
      the bank). The structural test also excludes `__pycache__/`, `figures/`, `sbatch/` and
      `diagram/` for free, because they hold no work.

  (2) CONFIRM — log the block path, the N children found (numbered `[i/N]`), and the stages
      to run. In interactive mode, ASK to confirm before proceeding. In AUTO_MODE, proceed
      directly.

  (3) ITERATE — for each child job, in order:
      - Log: `── [i/N] <child_name> ──`
      - Call the SAME `Workflow(...)` as Step 3c, with `task_folder: "<block-path>/<child>/"`,
        `type: null`, and the requested `stages` (default all four).
      - Collect the result. If a child fails (status=failed), log the failure and continue to the next child — do NOT stop the block iteration.

  (4) AGGREGATE — after all children complete, emit a block summary: one `[i/N] <child> —
      ok|failed (<per-phase verdicts>)` line per child, then an `Overall: N ok, M failed` tally.


Step 4: RUN THE CHECKLIST before reporting anything.

  Any verb that CREATED or RENAMED a block, job, task, config or ticket ends by
  checking the tree it just touched. A structural claim made without running this
  is an unverified claim that happens to print a tick (GATE-1).

  ```
  python3 <project>/tasks/_tools/check_task_tree.py <block>
  ```

  Thirteen codes, each one a break this repo actually hit:

  ```
  N1  a name that does not stand alone     a job/task name read in a queue or a log
  N2  a run name with no stage or kind     rNN_<A|B|C|D>_<cms|case|data|reg>_...
  N4  unordered alternatives                the folders a config picks between
  N5  shape words only                      data, table, pipeline, pool, rank
  N6  two tasks in one block sharing a name one rename map hits both
  N7  a ticket and its config disagree      the pair can no longer be checked
  N8  not exactly one shared config         a script cannot find what it must not spell
  S1  a do-path that does not resolve       from the JOB root, which is Stata's cwd
  S2  a ticket naming a config that is gone
  S3  a config naming a missing spine/steps
  S5  a task with no page
  S6  a file that RESTATES the tree         its drift guard is the proof it should not exist
  S7  an sbatch that never says one-by-one   or parallel, or says it inconsistently
  S8  a doc naming something that is gone    every rename so far left one behind
  S9  an entry point splatting @Rest         -WhatIf binds positionally and it fails
  S10 code at the wrong LEVEL              a job holding scripts/, a task holding src/,
                                           or config/ left at a task root
  ```

  S8 is the one that pays for itself: a page listing what the tree already holds
  drifts on the next rename. Generate those pages instead of typing them, and let
  S8 catch the ones nobody regenerated.

  Naming rules in prose, with the break behind each: `tasks/_tools/NAMING.md`.
  Non-zero exit means findings; fix them BEFORE emitting the tail below. To prove
  the checker can still fail, run it with `--expect-fail` against a broken copy.

Step 5: Emit the structured tail:

```
status:    ok | blocked | failed
summary:   2-3 sentences on what was done
artifacts: [paths created/modified]
next:      suggested next command
```


Invocation examples
--------------------

```
# the SAME path is a JOB or a BLOCK; the verb is identical, the scope differs
/haipipe-task       .../tasks/b03_band4/j01_band4    JOB:   all 4 phases
/haipipe-task plan  .../tasks/b03_band4/j01_band4    JOB:   one stage
/haipipe-task       .../tasks/b03_band4              BLOCK: all 4 phases on EACH child
/haipipe-task plan  .../tasks/b03_band4              BLOCK: that phase on EACH child

# scaffold a NEW job (dispatches to the type specialist; `task-folder` = alias)
/haipipe-task job data
/haipipe-task job eval --project-id Project-REACH-ADHD --group b03_band4

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
