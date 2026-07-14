---
name: haipipe-task
description: "Internal-execution layer, and one of the two EXECUTORS (discovery is the other — same shape, same rules). Task-folder and task-group orchestrator: for a task-folder it runs the 4-stage code lifecycle (Plan → Build → Execute → Report) or dispatches to type specialists for scaffolding; for a task-group it iterates the lifecycle over each child. Its PRIMARY mode is autonomous P-B-E-R — no question pending. CONSUMER-UNAWARE but not question-deaf: the `qa` verb (/haipipe-task qa \"<question>\" [<leaf>]) takes ONE question in general language and returns tasks/<leaf>/QA/<n>-<slug>.md — the leaf's readable digest of a direction it has explored. A QA file is a TICKET that becomes a RECEIPT: it carries ONE mutable `state:` line (working | answered | superseded-by:), CLAIMED at the qa gate's ③ decision and COMPLETED at Report — ONE WRITER, this layer, always. A `working` file means SOMEONE IS ALREADY ON IT: do not duplicate the work. Trigger: task, task folder, task group, plan, build, execute, report, run, scan-status, qa, QA file, question, state, working, claim, superseded, /haipipe-task."
argument-hint: "[scope] [args...] | qa \"<question>\" [<leaf>] [--check-only]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill, Workflow
metadata:
  version: "6.2.0"
  last_updated: "2026-07-14"
  summary: "Build orchestrator with the 4-stage code lifecycle (Plan → Build → Execute → Report) for task-folders and task-groups. v6.1 — THE QA FILE GAINS ONE MUTABLE FIELD, a `state:` line, and becomes a TICKET THAT BECOMES A RECEIPT (JL ruling 2026-07-14; probe SKILL 8.2.0 PART 3a R19/R20/R21). THE HOLE IT CLOSES: two consumers ask the same question a week apart; the first dispatches an expensive P-B-E-R run; the second, while that run is STILL GOING, sees no QA file and dispatches THE SAME RUN AGAIN — because a QA file used to be written ONCE, at Report, complete, and its EXISTENCE was the only signal. Now: `- state: working | answered | superseded-by: QA/<m>-<slug>.md` + `- started: YYYY-MM-DDTHH:MM` (MANDATORY on a working file) + optional `- by:`. Gate ③ P-B-E-R now CLAIMS FIRST (writes the QA file with `state: working` + `started:` + an EMPTY `## Answer` under `set -C` noclobber) and COMPLETES it at Report (`state: answered` + the body). Gate ① SCAN branches on the state line (answered → path · working → 'in progress since <started>', DO NOT RE-RUN · working+EXPIRED → zombie, RECLAIM · superseded-by → follow the chain to the live answer). Gate ② DIGEST still writes ONCE, complete, `answered` — no claim, nothing to race. THE LOAD-BEARING INVARIANT IS *ONE WRITER*, NOT *WRITE-ONCE*: two writes by the same owner is fine; a CONSUMER creating/claiming/editing a QA file is the retired _ASK/ stub in a QA/ costume and is FORBIDDEN. TTL = the named constant QA_CLAIM_TTL_HOURS = 24 (a claim with no `started:` can never expire and is a zombie by construction). RACE GUARD = `set -C` and nothing more — the loser re-scans and defers; no lock dirs, no lease servers, no ledgers. SUPERSESSION: a re-run whose answer CHANGES writes QA/<n+1> and APPENDS `superseded-by:` to the old file's state line — R15 (ENRICH never mutates) still holds FOR THE BODY; only the state line is mutable, and only its own owner edits it. Checker HARD-FAILs: qa-working-no-started · qa-working-expired · qa-answered-empty (+ the consumer-side read-target-working / read-target-superseded). v6.0 (Tools/plugins/haipipe-toolkit/diagram/260714-probe-qa/ v3): THE TASK LAYER IS CONSUMER-UNAWARE — _ASK/ stubs, _ANS/, `answers:`, PP ids and the probe-aware `asks` verb all DELETED; PRIMARY mode is autonomous P-B-E-R; ANSWERABILITY WORK is legitimate task-native work with no question pending; the `qa` verb (fn/qa.md) is the one question door — ① QA SCAN · ② DIGEST · ③ P-B-E-R at the SHALLOWEST depth (0 read | 1 new run+config | 2 new script | 3 new leaf) · 🚫 REFUSE; three callers, one identical door; QA/<n>-<slug>.md, numbering IS the index, slug only, no consumer vocabulary, three legal reasons only (commissioned · digest-only · executor's own). v6.2/v3.2 (R19 HARDENING): gate ① now READS THE STATE LINE **BEFORE** the literally-answers test. A `working` file's ## Answer is EMPTY BY CONSTRUCTION, so testing it for an answer is a guaranteed miss that drops through to ③ and RE-RUNS the job someone is already running (a new <n>, a different slug, `set -C` never fires) — the duplicate run, executed by obeying the rules. A `working` file is matched on its `# Q —` LINE instead. A QA file with NO `- state:` line is MALFORMED, not legacy (checker: qa-no-state): this layer OWNS it, so it REPAIRS it (tag `answered` if the Answer has a body, else RECLAIM as a zombie). The same-<n>/different-slug claim race is NON-FATAL BY RULING and is NOT a reviewer REVISE — the reviewers now carry the exemption explicitly."
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

Skill: haipipe-task (orchestrator)
===========================================

Build orchestrator organized around the **task hierarchy**:

```
project           examples/Proj{...}/
  └── task-group  tasks/{G}{NN}_{name}/
        └── task-folder  {NN}_{name}/{*.py, configs/, runs/, results/, notebooks/}
```

This skill owns **task-folder** and **task-group** scope. For a task-folder, it runs the 4-stage code lifecycle (Plan → Build → Execute → Report) or dispatches to a type specialist for scaffolding. For a task-group, it iterates over each child task-folder and runs the lifecycle on each one. Type specialists (one per type):

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

NOTE: group letters (A01_, B01_, C01_) are project-specific organizational prefixes, NOT type indicators. Each project defines its own letter scheme. Type is detected from script content, not from group letters. Specialists carry a DEFAULT letter for projects with no scheme (data D, fit A, eval B, display C, individual E, agent F, raw R, algo group X_algo); the project's existing scheme always wins.

Stata specialist (engine = Stata + PowerShell + logs, NOT papermill):

```
engine = Stata   →  /haipipe-task-for-stata   (unified — handles cms/case/data/reg internally)
```

This skill does NOT route stata stages itself — once the engine is detected as Stata it hands off wholesale; the specialist owns the `{LNN}` stage-letter alphabet and the engine contract in its own `ref/` (`stata-dialect.md` + templates).

Routing principle: this skill is the HIGH-LEVEL router. It owns only the engine-agnostic invariants (`ref/hierarchy.md`, `ref/task-structure.md` for task-group / task-folder / diagram / run-script layout, authoring conventions). Each `/haipipe-task-for-<engine>` child owns its OWN `ref/` (templates + dialect); route to the child and read the child's `ref/`, never keep engine specifics here.

Project setup (Project-*/ProjX-* containers) lives in `/haipipe-project`. This skill received fn/task-group.md and fn/scan-status.md (+ ref/scan_status/ scripts) from the project layer 2026-07-03.

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
/haipipe-task task-group <group-path|name>            scaffold a NEW task-group (fn/task-group.md)
/haipipe-task run <task-folder-path> [run-name]       execute one runs/*.sh with logging conventions (fn/run.md)
/haipipe-task audit <task-group-or-folder-path>       structural audit vs the four-sister contract (fn/workflow-audit.md)
/haipipe-task scan-status [project-path]              status scan across task-groups (fn/scan-status.md)
/haipipe-task qa "<question>" [<leaf>]                THE QUESTION DOOR: one general question in, a QA-file PATH out (fn/qa.md)
/haipipe-task feedback "<text>"                       capture skill feedback (merge-or-create), ROUTED to the domain folder it concerns
/haipipe-task feedback list [unit]                    aggregate open feedback across ALL inboxes (grouped by unit)
/haipipe-task feedback move <file> <unit>             re-route a mis-filed feedback item
/haipipe-task digest ["<session-name|id>"] [--dry-run]  digest a session (current, or a PAST one named/id'd, run from fresh): harvest feedback, dedup, confirm-gate, route to inboxes
```

---

Four Stages (code lifecycle)
------------------------------

All four stages answer one question: **"is the implementation right?"**

```
Stage 1: PLAN — the contract (what the script SHOULD do)
  creates:   workflow/plan.yaml              task-level IPO (Run/Gate1/Gate2)
             workflow/plan-script-<name>.yaml script-level IPO (type-specific phases)
  reads:     *.py (if exists),
             **/haipipe-task-for-<type>/ref/workflow-plan-sample.yaml (nested under its domain folder)
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
  completes: QA/<n>-<slug>.md                the CLAIM raised at the qa gate's ③ decision
                                             becomes the RECEIPT here: `state: answered`
                                             + the `## Answer` body. On gate ② (digest) it
                                             is CREATED here, once, complete.
                                             (see "The QA/ folder" below)
  reads:     workflow/plan*.yaml, results/<run>/*, CODE_REVIEW.md
  agents:    creator drafts report → reviewer checks accuracy → ↺ revise
```

File ownership is strict: Plan touches only `workflow/plan*.yaml`. Build touches only code/configs/runs. Execute touches only `results/` and `notebooks/`. Report touches only `workflow/report*.yaml`, `RUN_AUDIT.md`, and — when one is due — `QA/`.

**The ONE exception, and it is the qa gate's:** on gate ③ the QA file is CLAIMED before Plan runs — `state: working` + `started:`, an empty `## Answer` — and COMPLETED at Report. That is TWO writes, by the SAME owner (this layer), to a file in its OWN folder. It does not break file ownership; it is what file ownership MEANS. See `fn/qa.md` (Step 3a).

The `workflow/` folder is the task's observability surface: Plan = intent, Report = evidence, same IPO shape at both levels (schema: `task/haipipe-workflow/ref/plan-schema.md`).

A task ends at Report: it produces `results/` and stops. Whoever consumes those results records the link on THEIR side — this layer tracks no consumers.

---

The task session's two modes
-----------------------------

**PRIMARY — autonomous P-B-E-R.** The task session runs Plan → Build → Execute → Report for its own sake: train, sweep, profile, scan. No question is pending. No one asked. This IS the project's research, and the bank grows here, autonomously.

**ANSWERABILITY WORK — also task-native, also with no question pending.** A task session may legitimately:

- write a `QA/` digest for a finding worth digesting, and
- build or refactor code so that FUTURE questions are cheap to answer.

It does not know WHICH questions will come. It makes the bank EASIER TO ASK. That is task work, not anyone else's.

**THE SIDE DOOR — the `qa` verb.** Questions arrive through exactly one door, `fn/qa.md`, and they arrive as ONE QUESTION IN GENERAL LANGUAGE — never an id, never a stake, never a reference to whoever asked. The verb answers it or REFUSES it, and returns a path. It never learns who asked, or why, and must not try to find out.

```
/haipipe-task qa "<question>" [<leaf>]

  ① QA SCAN    grep <leaf>/QA/*.md — READ THE STATE LINE:                       ~0
                 state: answered  → return the PATH
                 state: working   → SOMEONE IS ALREADY ON IT. Return the path +
                                    "in progress since <started>". DO NOT RE-RUN.
                 working, EXPIRED past QA_CLAIM_TTL_HOURS → 🧟 zombie: RECLAIM it
                 superseded-by: X → follow the chain, return the LIVE answer
  ② DIGEST     results/ answer it, no readable digest? → write QA/<n>-<slug>.md cheap
               ONCE, COMPLETE, `state: answered`, from EXISTING artifacts; run no code
  ③ P-B-E-R    neither → ⚑ CLAIM FIRST (write the QA file with `state: working` +
               `started:` under `set -C`), then run the lifecycle at the SHALLOWEST depth
               that answers it (0 READ · 1 NEW RUN+config · 2 NEW SCRIPT · 3 NEW LEAF),
               and COMPLETE the same file at Report (`state: answered` + `## Answer`)
  🚫 REFUSE    out of scope for the task layer (e.g. a literature question) — say so;
               RELEASE any claim; the caller re-routes
```

Three callers, one identical door: a human steering an exploration, the orchestrator agent self-directed, or a relayed question from elsewhere. None of them gets a special path.

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

**A QA file is a TICKET that becomes a RECEIPT.** It carries exactly ONE mutable field — the **state line** — and everything below it is written once and never touched again:

```markdown
# Q — <the question, restated by the executor in its own words>
- state:   working | answered | superseded-by: QA/<m>-<slug>.md
- started: 2026-07-14T09:12          ← MANDATORY when state: working
- by:      <run id | agent | human>  ← optional provenance

## Answer     EMPTY while state: working. Filled at REPORT.
## Caveats
## Not-done
```

- `QA/<n>-<slug>.md`, `<n>` = creation order. **The numbering IS the index** — `ls QA/` is the index; there is no INDEX file. `QA/` now reads as a menu of BOTH: what this leaf has established, **and what it is establishing right now**.
- **SLUG ONLY.** No external id ever appears in a bank filename.
- **⚠️ THE LOAD-BEARING INVARIANT IS *ONE WRITER*, NOT *WRITE-ONCE*.** This layer writes the file TWICE — the CLAIM at the qa gate's ③ decision, the COMPLETION at Report. Two writes by the same owner is fine. **A CONSUMER (probe/paper/application) must NEVER create, claim, edit, complete, or supersede a QA file** — a consumer-planted `working` file is the retired `_ASK/` stub wearing a `QA/` costume, and it is FORBIDDEN.
- **WRITER: this layer.** Only gate ③ ever produces a `working` file, and only transiently. Gate ① writes nothing; gate ② writes once, complete.
- **THE CLAIM MUST EXPIRE.** `started:` is MANDATORY on a `working` file (a claim that cannot expire is a zombie by construction). TTL = the named constant **`QA_CLAIM_TTL_HOURS = 24`**. Past it the claim is STALE and the next qa call may RECLAIM it.
- **RACE GUARD:** create the claim under `set -C` (noclobber). The loser re-scans and defers. No lock dirs, no lease servers, no ledgers.
- **SUPERSESSION:** a later run whose answer CHANGES writes `QA/<n+1>-<slug>.md` and APPENDS `superseded-by:` to the old file's state line — by this layer, never by a consumer. A QA file's BODY is never edited.
- **THREE REASONS a QA file may exist, and no fourth:** a question arrived · a digest was missing though `results/` already answered it · a task session judged a finding worth digesting. A `QA/` that mirrors every result file is noise, not an index.
- **NO CONSUMER VOCABULARY.** A QA file carries no claim ids, no hypothesis ids, no "the paper". This layer never saw one and cannot honestly write one.

STATUS is derived from the STATE LINE, not from mere existence: no file = not answered · `working` = IN PROGRESS since `<started>` · `answered` = answered · `superseded-by: X` = answered but STALE, the live answer is X.

The checker (`check-probe-cards.sh`) HARD-FAILs three defects this layer can write: `qa-working-no-started` (unexpirable claim) · `qa-working-expired` (zombie past `QA_CLAIM_TTL_HOURS`) · `qa-answered-empty` (a lying receipt).

Not every leaf has a `QA/`. That is fine and normal.

---

Agents
------

Three agents in `task/agents/` form the orchestrator/creator/reviewer triad. Creator and reviewer always work as a pair — creator produces, reviewer evaluates, loop if revise; the orchestrator agent is the non-interactive dispatch target that coordinates them.

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

The reviewer catches **intent-vs-implementation mismatches** — silent semantic bugs where the code runs but doesn't measure what the writer intended. Independence comes from fresh-agent reasoning: the reviewer starts with clean context, never the creator's (Codex two-stage was removed in reviewer v1.1.0).

Author convention: `<TASK_NAME>.py` MUST have an `Intent` section in its docstring (template: `ref/intent-docstring-template.py`). Skip mechanisms for the run.sh pre-flight gate: `_meta.skip_review: true` in config, or `HAIPIPE_SKIP_REVIEW=1` env var.

---

Dispatch Table
--------------

```
Scope            Owner / route                              Function file
---------------- ------------------------------------------ ----------------------
task-group (iterate)  → this skill: iterate children        Step 3d
task-folder      → dispatch by task-type to its specialist
                 (the 9-row type table at the top of this file)
task-group (scaffold) this skill                            fn/task-group.md
qa               this skill                                 fn/qa.md
                 reads: <leaf>/QA/*.md, results/, workflow/plan.yaml
scan-status      this skill                                 fn/scan-status.md
                 reads: ref/scan_status/ scripts
run              this skill                                 fn/run.md
                 reads: ref/invocation-modes.md, ref/config-meta-template.yaml, ref/run-sh-template.sh
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
  (0) UTILITY VERB — first positional is `feedback` or `digest` (route this BEFORE any other parsing; neither is a lifecycle scope, so do not continue to Step 3).
      `feedback` → read `fn/feedback.md` and run it inline (capture / list / move; routing rules, merge-or-create, inbox paths all live THERE). Stop.
      `digest` → read `fn/digest.md` and run it inline (resolve the target session first; mandatory confirm gate before filing). Stop.
  (0.5) UTILITY VERB `scan-status` — first positional is `scan-status` → read `fn/scan-status.md` and run it inline. Stop.
  (0.6) QUESTION DOOR `qa` — first positional is `qa` → read `fn/qa.md` and run it inline (the ①②③ gate; the remaining args are the question, an OPTIONAL leaf path, and the OPTIONAL flag `--check-only`). It is not a lifecycle scope: do not continue to Step 3. Stop.
        `--check-only` runs ① and ② DETECTION only: report which path the question would take, execute nothing, write nothing — including NO CLAIM — and NEVER fall through to ③. This is the door the probe's MATCH step calls, and MATCH is defined as a FREE detection pass — a qa call that fell through to ③ there would spawn an unbudgeted P-B-E-R run, plant a claim, and write into the bank during a step whose whole purpose was to cost nothing. The discovery twin spells the flag IDENTICALLY; keep them in step.
        On gate ① the state line decides, not the file's existence: `state: answered` → return the path · `state: working` → SOMEONE IS ALREADY ON IT, return the path + "in progress since <started>" and DO NOT RE-RUN (this is the duplicate-work fix) · `working` past `QA_CLAIM_TTL_HOURS` → a zombie claim, RECLAIM it · `superseded-by:` → follow the chain to the live answer.
        If the question arrives carrying an external id, a claim reference, or a stake, IGNORE those tokens — answer the question on its own terms or REFUSE. This layer does not know what they mean and must not try to find out.
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

  Task-group detection: a path is a task-group if it matches `tasks/{G}{NN}_{name}/`, contains at least one `{NN}_*/` subdirectory, and has NO `.py` script at its root. This distinguishes it from a task-folder (which has `{NN}_{task_name}.py`).

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
          scriptPath: "Tools/plugins/haipipe-toolkit/skills/task/haipipe-task/ref/task-lifecycle.workflow.js"
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
/haipipe-task examples/Project-REACH-ADHD/tasks/B03_band4/01_band4

# single stage
/haipipe-task plan examples/Project-REACH-ADHD/tasks/B03_band4/01_band4
/haipipe-task build examples/Project-REACH-ADHD/tasks/B03_band4/01_band4
/haipipe-task execute examples/Project-REACH-ADHD/tasks/B03_band4/01_band4
/haipipe-task report examples/Project-REACH-ADHD/tasks/B03_band4/01_band4

# task-GROUP: iterate lifecycle over all children (01_band4, 02_eval, ...)
/haipipe-task examples/Project-REACH-ADHD/tasks/B03_band4

# task-GROUP with single stage: run that stage on each child
/haipipe-task plan examples/Project-REACH-ADHD/tasks/B03_band4
/haipipe-task report examples/Project-REACH-ADHD/tasks/B03_band4

# scaffold a NEW task-folder (dispatches to type specialist)
/haipipe-task task-folder data
/haipipe-task task-folder eval --project-id Project-REACH-ADHD --group B03_band4

# the QUESTION DOOR — one general question in, a QA-file PATH out
/haipipe-task qa "Do any WellDoc tables carry a menstrual or cycle column?"
/haipipe-task qa "What is the fit exponent on the 4-model sweep?" examples/ProjA/tasks/B01_scaling/B4_fit_scaling_law

# direct specialist (bypass orchestrator)
/haipipe-task-for-data
/haipipe-task-for-fit
```

---

Risk Profile
-------------

CREATES files under `examples/{PROJECT_ID}/`. Refuse to overwrite existing names — abort and recommend `-organize`.

When dispatching to a task-type specialist, the same blast radius applies — specialists also CREATE files under `examples/`.

---

## Feedback

`/haipipe-task feedback "<text>"` captures a complaint / confusion / wish about THIS skill, not the work it produces.
Each item is routed at capture time into the `feedback/` inbox of the domain folder it concerns (9 domains + `agents/`; the folder IS the record), with the orchestrator's own `feedback/` as the cross-cutting fallback.
`feedback list [unit]` aggregates open items across all inboxes; `feedback move <file> <unit>` re-routes a mis-filed one.
`/haipipe-task digest ["<session-name|id>"] [--dry-run]` is the bulk harvester: it scans a session transcript for conversational feedback and routes each confirmed item through the same capture.
ALL mechanics (cross-cutting guard, keyword→unit map, merge-or-create, lazy inboxes, session resolution, confirm gate) live in `fn/feedback.md` and `fn/digest.md` — read those, do not re-derive from here.

## Behavioral Preferences (portable)

ALWAYS read and honor `PREFERENCES.md` in this skill's own folder.
It holds git-tracked global behavioral preferences (e.g. communicate via ASCII diagrams) that survive a machine change, unlike the machine-local `~/.claude` auto-memory.
Global prefs are kept in sync across all orchestrators by the toolkit-wide digest global-pref fan-out (merge-or-create; one entry per topic).
