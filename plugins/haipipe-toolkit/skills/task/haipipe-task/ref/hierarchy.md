Task Hierarchy — Block / Job / Task / Run
==========================================

Settled with JL 2026-08-29 (absorbing ref/block-job-task-run.md). Four levels,
named against Databricks so one word never means two things in a workspace
that deploys there:

```
LEVEL   FOLDER                                DATABRICKS      ONE-LINER
─────   ───────────────────────────────────   ─────────────   ─────────────────────────────
BLOCK   tasks/bNN_{block_name}/               (none — free)   one large topic
JOB     jNN_{job_name}/                       Job             self-contained, submittable
TASK    scripts/tNN_{task_name}/              Task            one script pipeline
RUN     config/rNN_{stem}.yaml                Run             one submission of one task
```

**One grammar at every level (JL 260829): `<level letter><NN>_<noun>_<qualifier>`.**
The level letter (b · j · t · r) says WHICH LEVEL a name is, the two digits give
its order, the words after pass the stranger test. No exceptions, no letter
families, no bare letters: `b02_llm_recommendation_runs`, `j01_A1_search_physicians`,
`t01_claude_agent_sdk`, `r03_fold00_opus.yaml`.

RUN is an EXECUTION, not a folder of its own: what distinguishes two runs is
which config the ticket named, plus when it was sent. One execution has one
ADDRESS: the four prefixes read off its path and joined — `b02j01t01r03`
compact, `b02.j01.t01.r03` readable, `llmrec:b02j01t01r03` across projects.
Nothing is computed, mapped or counted: `ls` shows the address. A legacy
folder without a level letter (pre-260829 `A01_…/01_…`) still resolves as
`A01.01`. Full rule: ref/block-job-task-run.md § Addressing.

The old vocabulary maps 1:1 and appears throughout older files and boards:
`task-group` = BLOCK, `task-folder` = JOB. The TASK level is NEW (2026-08-29);
a legacy flat job is a job with one implicit task (see "Two job shapes").


Level 1: Project
-----------------

```
examples/Proj{Series}-{Category}-{Num}-{Name}/
├── tasks/        ← all blocks live here
├── diagram/      ← project-level story (01-story, 02-boundary + project.excalidraw; empty until authored)
└── paper/        ← optional, one per target venue
```

A project is one cohesive research effort. Forbidden at top level:
README.md, docs/, cc-archive/, _old/, configs/, results/.


Level 2: Block
---------------

```
tasks/bNN_{block_name}/              b01_physician_ground_truth  ·  b02_llm_recommendation_runs
├── jNN_{job1}/        ← jobs, and NOTHING runnable beside them
├── jNN_{job2}/
└── diagram/           ← docs only (01-overview, 02-tasks, 03-progress, 04-design + group.excalidraw)
```

**A block is a folder of jobs and nothing else** (JL 260829): no `sbatch/`,
no shared code, no results at block level. Everything that runs lives inside
a job. Code that SEVERAL jobs import is a LIBRARY and lives in the SPACE's
shared package `code/haiutils/` (JL 260830) — never at project, block or
sibling-job level; a job imports it the way it imports pandas. **Order
between jobs is a DATA dependency, never a scheduler job** (JL 260830, the
j05 ruling): each job audits its OWN outputs at the tail of its run ticket
and writes a receipt; a downstream job's config names the exact upstream
run it needs (`required_audits`) and its ticket refuses to start without
that receipt. There is no orchestration-only job. A block holds related
jobs that share context (same model family, same evaluation suite, same
figure set) and one diagram narrative.

**Prefer FEW blocks** (JL 260829): a block is one large topic, and `bNN`
orders the topics along the pipeline (b01 what the LLMs see → b02 the LLM
runs → b03 parse → b04 analyses → b05 figures). A topic split across many
two-job blocks is one block written many times. (Audit 260829:
Project-LLMRec-Physician had 15 blocks holding 32 jobs, ~2 each —
A01_candidate_pool / A02_baseline_rank / A03_virtual_health_site were three
jobs wearing block names; five blocks, ~6 jobs each, say the same thing.) A
family of parallel blocks (OpioidRx's one regression stage over three
studies) shows the family in the NAME — `b05_reg_trait_opioid ·
b06_reg_trait_diabetesndc · b07_reg_trait_cabg` — never in a letter scheme.

The block prefix carries NO type information: the job's task-type is read
from its code (SKILL.md Step 3a), never from a letter. (The pre-260829
letter defaults — A=fit, B=eval, C=display, D=data, E=individual, F=agent,
R=raw, X=algo — are retired; `tasks/D_demo/` auto-example pairing becomes
`tasks/bNN_demo/`, task-structure.md "Auto-Example Rule".)

Index NN starts at 01; no gaps at scaffold time; forward-fill on deletion.


Level 3: Job
-------------

A job is THE unit of self-containment: the largest thing one sbatch submits,
the smallest thing that runs without reaching into a sibling. Only a job can
be scheduled. A job never reaches into a sibling job. (= Databricks Job: one
git source, one set of job_clusters; tasks reference, never redefine.)

### Two job shapes

**NESTED (canonical — every NEW job scaffolds this way):**

```
jNN_{job_name}/
├── sbatch/                     batch-submit THIS job's tickets (loops, locks, GPU assignment); never another job's
├── scripts/                    CODE
│   ├── 0-libs/                 shared inside this job (name it 0-libs/, src/ or code/ — any
│   │                           non-tNN_ folder under scripts/ is shared code); job-wide
│   │                           defaults + `store:` live here
│   └── tNN_{task_name}/        ← TASKS (Level 4)
│       ├── config/             ALWAYS a folder; rNN_{stem}.yaml — the NUMBER is the run's identity, the stem its description
│       │   └── prompts/        PROMPTS ARE CONFIG (JL 260830): a prompt file sits beside the config that names it,
│       │                       and code resolves `prompts/x.md` relative to the CONFIG file, never to the code
│       └── <stem>.py           the pipeline (or run-pipeline.do + step-*.do in the Stata dialect)
├── runs/                       TICKETS, carry NO params; mirrors scripts/ task names
│   └── tNN_{task_name}/
│       └── rNN_{stem}.sh       names a config, submits — nothing else
├── results/                    JOB level, two levels deep: results/<task>/<run>/
├── notebooks/                  papermill records, mirrored: notebooks/<task>/<run>.ipynb
│                               (+ the generated template notebooks/<task>/_source.ipynb)
├── QA/                         <n>-<slug>.md digests, when `qa` is called
├── CODE_REVIEW.md · RUN_AUDIT.md
├── workflow/                   plan/report artifacts (haipipe-workflow)
└── diagram/                    optional, only if the job diverges from the block narrative
```

**FLAT (legacy — a job with ONE implicit task; the pre-260829 shape):**

```
{NN}_{job_name}/                (pre-260829 names: no level letter)
├── {NN}_{job_name}.py          the script at job root
├── configs/  <run>.yaml        flat
├── runs/     <run>.sh          flat
├── results/  <run>/            one level
└── notebooks/ QA/ sbatch/ diagram/ workflow/
```

Tooling accepts BOTH (run-sh-template.sh detects the shape from the ticket's
own path: parent dir named `runs` = flat, else nested). The ~120 existing flat
jobs stay valid; migration is per-job, not forced. But a flat job that grows a
second pipeline converts to nested rather than piling a second .py at root.

### Two run modes

**A job runs in one of TWO MODES** (JL 260821). Both are first-class.
Neither is a fallback or a deprecation of the other, and the same job can be
run in either without being edited.

```
① SELF-SERVING · output STAYS in the job
   nobody but this job owns the answers: exploration, a one-off check,
   a fit, an eval nobody has commissioned.

② CONSUMER-SERVING · output goes to the CONSUMER'S STORE
   a board, a paper, anything that owns its own answers. The job becomes
   SHARED CODE and holds nothing generated at all:

jNN_{job_name}/                the SAME job, minus everything generated
├── scripts/  runs/  sbatch/  diagram/
├── CODE_REVIEW.md             stays: it reviews CODE at a git_sha, not a cohort

<store>/<this job's path under tasks/>/
├── results/  notebooks/  QA/
└── RUN_AUDIT.md               audits one RUN's results, so it follows them
```

**Where output lands is RESOLVED, never hardcoded.** `OUTPUT_ROOT` is the
job folder in mode ①, and `<store>/<path of this job under tasks/>` in mode
②, mirroring the block/job tree so store and repo map 1:1 both ways. The
`<task>/<run>` levels below OUTPUT_ROOT are identical in both modes, so a
job's output survives the move between them untouched.

```
RESULT_STORE env      set by a DISPATCHING CONSUMER          wins
`store:` declaration  a standing property of the JOB → MODE ②
neither               OUTPUT_ROOT = the job folder → MODE ①
```

**`store:` is a JOB property, declared ONCE — never per-run** (JL 260829).
Nested shape: in `scripts/0-libs/` (config-defaults.yaml, or config-defaults.do
in the Stata dialect). Flat shape: in the run's config, but one value across
all of them. The moment two runs of one job land in two places,
`ls results/*/*/` stops being the job's output inventory, which is the whole
reason results sits at job level.

Three mechanisms set it, each covering what the others cannot (JL 260823):

```
DISPATCH   a consumer's board.md carries `store:`; the probe resolves it and
           sends RESULT_STORE with the batch. Automatic, and the only one that
           works for board-driven runs nobody typed a config for.
SCAFFOLD   creating a job ASKS once, when a board with a store exists,
           and persists the answer as the job's `store:`. Blocking, not
           defaulting — see SKILL.md § Which mode.
GUARD      a run about to write job-local WARNS when a store already holds a
           QA bank for this same job. Catches what the first two missed.
```

`OUTPUT_BASE` travels beside `OUTPUT_ROOT` and is the base a SIBLING job's
output resolves against: the store in mode ②, the `tasks/` tree in mode ①. One
config key, `<job-rel>/results/...`, then resolves correctly in both.

**Which mode is right is decided by WHO OWNS THE ANSWER**, not by how big the
job is or who launched it. Mode ① when the answer is only about the code that
produced it; mode ② when a consumer's evidence base is what the answer joins.
The test is: if a second cohort ran through this same code, would the two sets
of answers need to be kept apart? Yes means mode ②, because one job cannot
hold two cohorts' results without one overwriting the other.

In mode ② the task layer is handed a PATH and never a consumer identity, so a
dispatching probe can supply it without breaching the stake wall — the executor
writes where it is told and still cannot learn whose claim it serves.

Nothing DATA-DEPENDENT may sit in the job in mode ②, and that includes
the converted `_source.ipynb` and `RUN_AUDIT.md`, which audits one run's
results. `CODE_REVIEW.md` is the exception and stays with the code in both
modes: it reviews the code at a `git_sha` and returns the same verdict no
matter which cohort the code is pointed at, which is why the pre-flight gate
checks it against `git_sha` and not against an extract date. Being generated is
not the test; being data-dependent is. In mode ① all of it stays exactly where
it always has.

NO README.md anywhere.


Level 4: Task
--------------

A task is one script pipeline: `scripts/tNN_{task_name}/`, runnable alone but
only inside its job, because it resolves the job's shared code (`../0-libs/`,
`../src/`). Its task name is unique
WITHIN the job, not globally (= Databricks task_key).

```
scripts/
├── 0-libs/                     SHARED code — call it 0-libs/ (Stata), src/ or code/ (Python);
│                               the rule is: `tNN_*` = exactly one task, anything else = shared.
└── tNN_{task_name}/
    ├── config/                 ALWAYS a folder, even holding one file, so no
    │   ├── r01_base.yaml       reader ever stats the path to learn the rule.
    │   └── r02_wide.yaml       rNN is the run's identity; the stem describes it.
    ├── <stem>.py               code beside its config: a config is EXECUTED
    └── <stem>.ipynb            (or `include`d, in Stata), not passed in as a
                                payload, so it is debugged in the same session
                                as the steps beside it.
```

Rules (JL 260829):

- A TICKET CARRIES NO PARAMETERS. `runs/<task>/<run>.sh` names a config and
  submits; it defines nothing of its own and never repeats its own name —
  derive task and run from the ticket's path ($0), so a rename breaks nothing.
- A VARIANT IS A CONFIG, NOT A NEW TICKET SCHEME. Two runs of one task differ
  only by config stem. Two DIFFERENT pipelines are two tasks.
- ZERO-PAD the index to two digits: single digits sort wrong
  (`10_` sorts before `2_`).

### What earns a TASK

**A task is one FUNCTION: one computation, one output contract, one code
path.** Its identity is WHAT IT COMPUTES, never what data it computes on
(JL 260821). Three tests; a candidate task must pass all three.

```
① REUSE    could this run unchanged on a different cohort?
           NO → the cohort leaked into the code. Move it to config/.

② OUTPUT   does it own result files nobody else writes?
           NO → it is not a task, it is a division of one.

③ RERUN    when the source refreshes, is this the smallest thing you re-run?
           always re-run together with another → they are ONE task.
```

Tests ② and ③ apply in both modes. **Test ① is BINDING in mode ② and merely
good hygiene in mode ①**: a self-serving job that hardcodes its cohort is
untidy, while a consumer-serving one that does the same cannot serve a second
store at all. A mode-① job that later gets commissioned must pass ① before it
can be, and that promotion is the usual moment the leak is discovered.

What splits, and into what:

```
what changed                     you create            you do NOT create
─────────────────────────────────────────────────────────────────────────
new cohort / extract date        a new CONFIG          a new task
new segment (age, gender, site)  a new CONFIG          a new task
new consumer (board, paper)      a new STORE key       anything else
different columns AND outputs    a new TASK
a different output contract      a new TASK (or a new JOB, if it also
                                 stops sharing 0-libs and the store)
```

Name the task for what is computed, as a noun that passes the stranger
test ("Indexing & Naming"): `message_corpus`, never `young_male_corpus` and
never `qd1_corpus`. A cohort, a segment or a consumer's
question id appearing in a task name is exactly the leak test ① catches, and
it is visible before the code is even read.

Duplication is the smell that says the rule was applied too finely. Ten tasks
each carrying near-identical scaffolding and differing only in a column list
are one parameterised function wearing ten hats; prefer a config over an
eleventh task once that pattern is visible.

### Drift checks (nested shape)

Every link in the shape is a folder name, so every link is checkable:

```
# every task has tickets, every ticket has a task  (tNN_ only: src/, 0-libs/ are not tasks)
comm -3 <(ls runs/) <(ls scripts/ | grep '^t[0-9][0-9]_')

# every config has a ticket, every ticket has a config
comm -3 <(find scripts -path "*/config/*" -type f \
            | sed "s|^scripts/||; s|/config/|/|; s|\.[^./]*$||" | sort) \
        <(find runs -type f | sed "s|^runs/||; s|\.[^./]*$||" | sort)
```

Both must print nothing (left column = config with no ticket, right = ticket
with no config; verified 260829). Under the flat shape neither check is
possible, which is why 42 flat jobs silently drifted configs/ against runs/.


Indexing & Naming
------------------

### ⚠️ HIGHEST PRIORITY — Naming: the stranger test (JL 260829)

Read this before any index rule below: a wrong index sorts badly, a wrong
name misleads every reader forever.

Every block, job and task name must let a reader who has NEVER opened the
folder answer two questions from the name alone:

```
① WHAT THING   the concrete noun the folder is about or produces —
               physicians, reviews, rankings, directory pages. A SHAPE word
               may follow a noun, never replace it: pool, set, list, table,
               data, rank, baseline, analysis, scope, processing, pipeline.
② WHICH ONE    the qualifier separating it from its siblings — the source
               (from_review_platforms, from_search_engines), the grain
               (by_region_specialty), the scope (nationwide), the variant
               (full_grid).
```

Pattern `<noun>_<qualifier>`, snake_case, at most 5 words after the index.

```
⛔ candidate_pool          pool of what, for what?
⛔ baseline_rank           baseline of what, from where?
⛔ google_rank             vague AND wrong: the task also queries Brave
✅ physician_pool_by_region_specialty
✅ physician_ranks_from_review_platforms
✅ physician_ranks_from_search_engines
```

A project's coined term (VirtualHealthSite, Smoke50, eval400) may carry a
name only if the block's `diagram/01-overview.txt` defines it; a name whose
key word is private vocabulary is not self-explaining. Scaffolding REFUSES a
name that fails ① or ②: it asks for the noun and the qualifier and composes
the name itself (SKILL.md Step 3b).


```
Project   Proj{Series}-{Category}-{Num}-{Name}
Block     bNN_{block_name}           2 digits, pipeline order
Job       jNN_{job_name}             2 digits within the block
Task      tNN_{task_name}            2 digits within the job's scripts/
Run       rNN_{stem}.yaml            2 digits within the task's config/; a name, never a folder
Cross-ref "b02j01t01r03"             the four prefixes joined, read off the path;
                                     readable "b02.j01.t01.r03"; legacy "A01.01" still resolves
```

Rules:

- **2 digits.** Always `01`, `02`, ..., `09`, `10`, ... — never `1`, `2`,
  never `001`. Sorts cleanly up to 99 per bucket. (Real bug: `10_` sorting
  before `2_` in a single-digit scripts/ tree.)
- **Start at 01.** Indices are 1-based; `00` is reserved for slots that
  must sort at the very top: `00-index.txt` in `diagram/`, a block-level
  `00` index for stage-0 work that precedes the pipeline (e.g. the
  embedded raw-extraction block `A00_rawstore_<cohort>/` sorting above
  `A01_data_pipeline_*`), and `00_*_fn_develop_*` builder jobs. Inside a
  job's scripts/, `0-` (with a dash) marks SHARED NON-TASK folders.
- **No gaps when scaffolding.** Pick the next free NN within the bucket.
- **Forward-fill on deletion.** If `02_foo` is removed, do NOT renumber
  `03_bar` → `02_bar`. Existing references (papers, runs, notebooks)
  point at names; renaming breaks them. Just leave the gap.
- **Sub-buckets** for within-letter sub-families: jump by ten to signal
  a new sub-bucket within the same letter. `A01..A09` = pretraining;
  `A21..A29` = finetuning; `A41..` = next sub-family.
- **Project Num** counts projects within `{Series}-{Category}` only,
  not globally.


Validation responsibility:

- `/haipipe-task` (block / job scaffolds) checks "no collision" AND the
  stranger test at scaffold time; refuses to overwrite an existing index.
  (Project-level audit verbs were retired 2026-07-03 and deleted 260822; see git.)


Task-types (orthogonal to block letter)
----------------------------------------

("task-type" is the JOB's computational CATEGORY — a historical name kept
because the whole family is /haipipe-task; it is NOT the Level-4 TASK.)

A job is one of these. Letter convention is a hint, not a hard
rule — a B-block can hold a display job if it makes narrative sense.

```
TYPE            CONFIG SKELETON (contents)  RESULTS LAND IN
--------------- --------------------------  --------------------------------------
fit (model-run) model/training keys         _WorkSpace/5-ModelInstanceStore/
evaluation      eval-target keys            results/<task>/<run>/{metrics.json, ...}
display         figure/table keys           results/<task>/<run>/{*.pdf, *.png, *.tex}
data-pipeline   Stage 1-4 pipeline keys     _WorkSpace/{1..4}-*Store/
other           (none required)             results/<task>/<run>/
```

(Flat legacy jobs: drop the `<task>/` segment.) The task TYPE decides the
config's SKELETON (which keys it carries), never its FILENAME — the filename
is always the run name (config/<run>.yaml pairing runs/<task>/<run>.sh).

Running process — papermill, always
------------------------------------

Every Python job runs the same way. There is one template; the Stata dialect
has its own (haipipe-task-for-stata).

### Four identity axes: (Project, Job, Task, Run)

A single execution is fully named by **four** axes. The first three are
folders in the hierarchy; **Run is a name**, not a folder.

  Project   examples/Proj{...}/                          (Level 1)
  Job       tasks/bNN_{block}/jNN_{job}/                (Levels 2-3)
  Task      scripts/tNN_{task_name}/                     (Level 4; implicit in flat jobs)
  Run       rNN_{stem}                                   (e.g. "r03_fold00_opus"; flat legacy: "run_1m")

### RUNNAME — the spine of one execution

The Run axis appears as one shared `<task>/<run>` path across **four
projections**. Pairing them by name is mandatory; tooling depends on it.

```
NESTED                                 FLAT (legacy, task segment dropped)
scripts/<task>/config/<run>.yaml  📥   configs/<run>.yaml       inputs
runs/<task>/<run>.sh              ▶️    runs/<run>.sh            entry (ticket)
results/<task>/<run>/             📊   results/<run>/           light outputs
notebooks/<task>/<run>.ipynb      📓   notebooks/<run>.ipynb    execution record
```

If you change the run name, you change all four. They are one entity in
four projections. Because every segment is a real folder name, the pairing
is CHECKABLE (see "Drift checks") — under flat naming it was only a habit.

### Two notebooks, two roles — don't confuse them

```
notebooks/<task>/_source.ipynb      TEMPLATE        (auto-converted from .py;
  (flat: notebooks/_source.ipynb)                    no execution state;
                                                     regenerated every run)

notebooks/<task>/<run>.ipynb        EXECUTION       (papermill output;
  (flat: notebooks/<run>.ipynb)                      contains cell outputs,
                                                     errors, logs;
                                                     IS the run record)
```

Both are GENERATED, so both live under $OUTPUT_ROOT/notebooks/ — never in
scripts/, which in mode ② holds nothing generated (run-sh-template.sh
NOTEBOOK_TEMPLATE). Never edit either by hand — edit the .py. (An author may
preview-convert beside the .py while writing; that file is untracked scratch.)

### Authoring loop (offline, before any run)

```
   🧑 author
       │
       ▼ edits
   🐍 scripts/<task>/<stem>.py        (notebook-cell source, # %% blocks)
       │
       ▼ convert (one-shot, auto by the ticket — but you can preview)
   📓 notebooks/<task>/_source.ipynb  (template, for visual review)
       │
       ▼ author reads the .ipynb, identifies what to change
       ↺  back to .py edits
```

Authoring happens in `.py` (diff-friendly). The `.ipynb` template exists
so the author can **read** the cell flow during review, not edit it.

### Execution flow (what a ticket does)

```
▶️  runs/<task>/<run>.sh
   │
   ▼ Step 1: convert .py → template .ipynb beside it
   ▼ Step 2: papermill inject parameters + execute
       papermill <template>.ipynb notebooks/<task>/<run>.ipynb \
                 -p config scripts/<task>/config/<run>.yaml ...
   │
   ▼ outputs split by weight
       📊 light artifacts  →  results/<task>/<run>/{eval.json, model_path.txt}
       💾 heavy artifacts  →  _WorkSpace/{N}-*Store/             (out-of-repo)
```

### Light vs heavy outputs

Two destinations, decided by file size and repo policy.

  📊 LIGHT (under `results/<task>/<run>/`)
     metrics JSON, eval logs, figure files (.pdf/.png/.tex), source CSVs,
     **pointers** to heavy artifacts (e.g. `model_path.txt`).

  💾 HEAVY (out-of-repo, under `_WorkSpace/`)
     model checkpoints (.pt/.ckpt/.safetensors), large arrays (.npy/.pkl/.h5),
     trained-instance folders, raw cohort tables.

Heavy artifacts in `results/` is a hard error — caught by `-inspect`.

### sbatch — exogenous to the task

`sbatch/` coordinates, never computes, and lives in the JOB: it submits
this job's DAG or GPU-partitions a sweep. There is no block-level sbatch —
a batcher that spans jobs is proof those jobs are one job. It carries no
parameters — tickets do not either; parameters live only in config/.

### Task-types decide

  1. Which block letter the job likely belongs to (A/B/C/D).
  2. Which YAML skeleton to seed in config/.
  3. Where results actually land (results/ vs _WorkSpace/).
  4. Which parameters the ticket injects.

The **process is invariant**; only the contents change.

### Where the workflow diagram lives

A visual of the complete flow (authoring loop + execution + outputs) is
in `ref/running-process.txt`.


Mandatory rules (cross-cutting)
--------------------------------

- Two-level container: jobs always live inside a block; never flat
  under `tasks/`.
- Each job owns its configs (no symlinks into other jobs).
- Run ↔ result name pairing is mandatory, at the `<task>/<run>` path level
  in nested jobs.
- Heavy artifacts (.pt / .ckpt / .safetensors / .npy / .pkl / .bin / .h5)
  go under `_WorkSpace/`, never `results/`.
- The doc surface is `diagram/`, never `README.md`. Diagram .txt content
  is authored via `/diagram-ascii`, bundled via `/diagram-ascii-canvas`.
- Code stubs in `code/hainn/` (or a legacy `code-dev/`) get a paired example
  task in `tasks/D_demo/` (Track A ↔ Track B coupling). Fn builders live in
  the project's `NN_<stage>_fn_develop_<cohort>/` jobs, which are
  their own runnable jobs — no extra demo pairing needed.
