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
TASK    jNN_{job_name}/tNN_{task_name}/       Task            one script pipeline = one PAGE
RUN     tNN_{task_name}/config/rNN_{stem}.yaml Run            one submission of one task
```

**The TASK is the PAGE (JL 260830).** A task folder is SELF-CONTAINED: its code, its
`config/`, its `runs/` tickets and its page `tNN_{task_name}.md` sit together, directly
under the job. It maps 1:1 onto a Board page, so the three document levels line up and
`haipipe-page` and `haipipe-task` address the same folder:

```
BOARD   diagram/<NN>-<topic>-<YYMMDD>/   ←→   BLOCK  tasks/bNN_<topic>/  (+ board.md)
  GROUP   1-QA-<slug>/                   ←→     JOB    jNN_<question_group>/
    PAGE    QA1-<slug>/QA1-<slug>.md     ←→       TASK   tNN_<name>/tNN_<name>.md
            (no counterpart)             ←→         RUN    rNN_<stem>  — an execution
```

The dividing line inside a job is **authored vs generated**: the task folder holds what a
person wrote; the job folder holds what a machine produced (`results/`, `notebooks/`,
`QA/`, `workflow/`). That is the same line mode ② already draws, which is why a
consumer-serving job still moves whole folders to its store.

⚠️ **Still open at 260830, do not read as settled**: (a) the Databricks column above, since
a Databricks Task is a DAG node that takes clusters and params from its Job and is not
self-contained; (b) "prefer FEW blocks" below, which pulls against a block being as
independent as a board; (c) whether a job's name should read as a question group rather
than as the store it fills; (d) the migration bill for the ~342 jobs still in the old shape.

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
├── board.md           ← the block's head: title · state · owner · Opening · Pages
├── jNN_{job1}/        ← jobs (= question groups), and NOTHING runnable beside them
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
│                               ┌─ AUTHORED: what a person wrote ────────────────
├── sbatch/                     batch-submit tickets ACROSS tasks (the job's DAG); never another
│                               job's, and never a sweep over ONE task — that one lives in the
│                               task, as tNN_{task_name}/sbatch/ (see "sbatch", below)
├── src/                        SHARED inside this job -- code, defaults, prompts, anything more
│                               than one task uses; job-wide defaults + `store:` live here.
│                               TWO WORDS, ON PURPOSE (JL 260831): `src/` at the JOB and
│                               `scripts/` at the TASK. The name alone says whether code is
│                               shared or owned, so a reader never has to work out which
│                               level a folder sits at to know what it means. One word for
│                               both was tried and rejected the same day. Not `code/`, which
│                               the SPACE's own package owns. `0-libs/` is the pre-260830
│                               name; it stays READABLE as `src/0-libs/` and is never scaffolded.
├── tNN_{task_name}/            ← TASKS (Level 4), directly under the job. AUTHORED side.
│   ├── tNN_{task_name}.md      the PAGE: Opening · Diagram · Content · Aims · States · Files
│   ├── scripts/                THE TASK'S OWN CODE (JL 260831), the word a Board Page uses,
│   │                           because a task folder IS a page folder with the execution
│   │                           family added. Shared code is the JOB's `src/`, one level up:
│   │                           the two folders have DIFFERENT names so the name alone says
│   │                           which it is. Code at the task ROOT was the pre-260831 shape.
│   │   ├── <stem>.py           the pipeline (or run-pipeline.do + step-*.do in the Stata dialect)
│   │   └── config/             ALWAYS a folder, INSIDE scripts/ (JL 260831): a config is read by
│   │                           the code beside it, so it sits beside that code. TWO KINDS:
│   │       │                   SHARED   loaded by several runs of this task — cohort.do,
│   │       │                            _defaults.yaml. NO rNN prefix: it is not a run.
│   │       │                   PER-RUN  rNN_{stem} — the NUMBER is the run's identity, the
│   │       │                            stem its description; pairs 1:1 with runs/rNN_{stem}
│   │       └── prompts/        PROMPTS ARE CONFIG (JL 260830): a prompt file sits beside the config that names it,
│   │                           and code resolves `prompts/x.md` relative to the CONFIG file, never to the code
│   └── runs/                   TICKETS. A ticket names its config, and MAY carry settings that
│       ├── rNN_{stem}.sh       SELECT A SLICE (year, source, fold). It must never restate a
│       │                       setting its config already holds: two sources of truth drift,
│       │                       and the drift is silent. Settings that change WHAT is computed
│       │                       (cohort, trait, spec family, outcome) belong in a config, where
│       │                       they can be reviewed and diffed.
│       └── (a task-scoped batcher, if any, sits in tNN_{task_name}/sbatch/)
│                               └─ GENERATED: what a machine produced ───────────
├── results/                    JOB level, two levels deep: results/<task>/<run>/
├── notebooks/                  papermill records, mirrored: notebooks/<task>/<run>.ipynb
│                               (+ the generated template notebooks/<task>/_source.ipynb)
├── QA/                         <n>-<slug>.md digests, when `qa` is called
├── CODE_REVIEW.md · RUN_AUDIT.md
├── workflow/                   plan/report artifacts (haipipe-workflow)
└── diagram/                    optional, only if the job diverges from the block narrative
```

**Where a setting lives is free; RECORDING it is not (JL 260831).** The rule used
to be "a ticket carries no params", which was a means, not the end. The end is
that a person can open a results folder months later and know what produced it.
So a setting may sit in the config, in the ticket, or split across both — and
whichever it is, the RUN writes it down:

```
results/<task>/<run>/runtime.yaml
  run · started · host · user
  git_sha · git_dirty          was it built from committed code?
  ticket · config_file · config_sha256
  settings:                    every value that varied for this run
```

`config_sha256` is the load-bearing field: two runs named the same thing, produced
from a config that changed in between, are otherwise indistinguishable on disk.
Write it BEFORE the work starts, never after — a crashed run is exactly the one
whose identity you need. Audit a block with `_tools/check_runs.py <block>`:

```
R01  a results folder with no runtime.yaml       the run is unidentifiable
R02  same run name, different config_sha256      two different things share one name
R03  git_dirty: True                             produced from uncommitted code
R04  runtime.yaml missing a required field       the record is incomplete
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
├── src/  tNN_<task>/ (its scripts/ + runs/)  sbatch/  diagram/
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
Nested shape: in `src/` (config-defaults.yaml, or config-defaults.do
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

A task is one script pipeline: `tNN_{task_name}/`, runnable alone but
only inside its job, because it resolves the job's shared code (`../src/`).
Its task name is unique
WITHIN the job, not globally (= Databricks task_key).

```
jNN_{job_name}/
├── src/                        SHARED — whatever more than one task in this job uses;
│                               the rule is: `tNN_*` = exactly one task, anything else = shared.
└── tNN_{task_name}/            the task is SELF-CONTAINED and IS the page
    ├── tNN_{task_name}.md      the PAGE, named for its own folder, as a Board page is
    ├── config/                 ALWAYS a folder, even holding one file, so no
    │   ├── r01_base.yaml       reader ever stats the path to learn the rule.
    │   └── r02_wide.yaml       rNN is the run's identity; the stem describes it.
    ├── runs/                   the tickets, beside the configs they name
    │   ├── r01_base.sh
    │   └── r02_wide.sh
    ├── sbatch/                 OPTIONAL: a batcher that loops over THIS task's
    │                           tickets only (a sweep, a GPU partition). One that
    │                           spans tasks belongs at job level instead.
    ├── <stem>.py               code beside its config: a config is EXECUTED
    └── <stem>.ipynb            (or `include`d, in Stata), not passed in as a
                                payload, so it is debugged in the same session
                                as the steps beside it.
```

Rules (JL 260829):

- A TICKET CARRIES NO PARAMETERS. `<task>/runs/<run>.sh` names a config and
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
                                 stops sharing src/ and the store)
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
# every config has a ticket, every ticket has a config — now INSIDE one task folder,
# so the two can no longer drift across parallel trees; run it per task:
for t in t[0-9][0-9]_*/; do
  comm -3 <(ls "$t/config" 2>/dev/null | grep -v '^_' | sed 's/\.[^.]*$//' | sort) \
          <(ls "$t/runs"   2>/dev/null | sed 's/\.sh$//' | sort)
done

# every task's output is filed under its own name  (tNN_ only: src/ is not a task)
comm -3 <(ls -d t[0-9][0-9]_*/ | sed 's|/$||' | sort) <(ls results/ 2>/dev/null | sort)
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
Task      tNN_{task_name}            2 digits within the job
Run       rNN_{stem}.yaml            2 digits within the task's config/; a name, never a folder
Cross-ref "b02j01t01r03"             the four prefixes joined, read off the path;
                                     readable "b02.j01.t01.r03"; legacy "A01.01" still resolves
```

Rules:

- **2 digits.** Always `01`, `02`, ..., `09`, `10`, ... — never `1`, `2`,
  never `001`. Sorts cleanly up to 99 per bucket. (Real bug: `10_` sorting
  before `2_` in a single-digit tree.)
- **Start at 01.** Indices are 1-based; `00` is reserved for slots that
  must sort at the very top: `00-index.txt` in `diagram/`, a block-level
  `00` index for stage-0 work that precedes the pipeline (e.g. the
  embedded raw-extraction block `A00_rawstore_<cohort>/` sorting above
  `A01_data_pipeline_*`), and `00_*_fn_develop_*` builder jobs. Inside a
  job's `src/`, `0-` (with a dash) marks SHARED NON-TASK folders.
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
is always the run name (config/<run>.yaml pairing <task>/runs/<run>.sh).

Running process — papermill, always
------------------------------------

Every Python job runs the same way. There is one template; the Stata dialect
has its own (haipipe-task-for-stata).

### Four identity axes: (Project, Job, Task, Run)

A single execution is fully named by **four** axes. The first three are
folders in the hierarchy; **Run is a name**, not a folder.

  Project   examples/Proj{...}/                          (Level 1)
  Job       tasks/bNN_{block}/jNN_{job}/                (Levels 2-3)
  Task      tNN_{task_name}/                     (Level 4; implicit in flat jobs)
  Run       rNN_{stem}                                   (e.g. "r03_fold00_opus"; flat legacy: "run_1m")

### RUNNAME — the spine of one execution

The Run axis appears as one shared `<task>/<run>` path across **four
projections**. Pairing them by name is mandatory; tooling depends on it.

```
NESTED                                 FLAT (legacy, task segment dropped)
<task>/config/<run>.yaml          📥   configs/<run>.yaml       inputs      ┐ authored,
<task>/runs/<run>.sh              ▶️    runs/<run>.sh            entry       ┘ in the task
results/<task>/<run>/             📊   results/<run>/           light out   ┐ generated,
notebooks/<task>/<run>.ipynb      📓   notebooks/<run>.ipynb    exec record ┘ at job level
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
the job's own tree, which in mode ② holds nothing generated (run-sh-template.sh
NOTEBOOK_TEMPLATE). Never edit either by hand — edit the .py. (An author may
preview-convert beside the .py while writing; that file is untracked scratch.)

### Authoring loop (offline, before any run)

```
   🧑 author
       │
       ▼ edits
   🐍 <task>/<stem>.py        (notebook-cell source, # %% blocks)
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
▶️  <task>/runs/<run>.sh
   │
   ▼ Step 1: convert .py → template .ipynb beside it
   ▼ Step 2: papermill inject parameters + execute
       papermill <template>.ipynb notebooks/<task>/<run>.ipynb \
                 -p config <task>/config/<run>.yaml ...
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

`sbatch/` coordinates, never computes. It carries no parameters — tickets do
not either; parameters live only in config/. There is no block-level sbatch: a
batcher that spans jobs is proof those jobs are one job.

**WHICH sbatch, and where (JL 260830).** Since a task is now self-contained, the
same question the rest of the folder answers decides this one: does the batcher
span tasks, or serve exactly one?

```
jNN_{job}/sbatch/              SPANS TASKS — submits the job's DAG, t01 then t02
                               then t03; orders work no single task can order.
jNN_{job}/tNN_{task}/sbatch/   SERVES ONE TASK — a sweep over that task's own
                               tickets, a GPU partition of its configs. It sits
                               beside the runs/ it loops over, so the task still
                               moves, copies and reviews in one piece.
```

Test: if you deleted every other task in the job, would this batcher still make
sense? Yes means it belongs in the task. A `sbatch/<task>/` folder at job level
is the older mirrored spelling and stays readable, but a new task-scoped batcher
scaffolds inside the task.

**ONE BY ONE OR ALL AT ONCE IS DECLARED, NOT ASSUMED (JL 260831).** A batcher
that does not say how it runs its runs is telling the reader nothing: a job whose
runs overwrite each other and a job whose runs are independent look identical from
outside, and "sequential" is not a safe guess for either. So every `sbatch/` carries
a declaration beside its engine, and the engine REFUSES TO START without one.

```
jNN_{job}/sbatch/batch.psd1     Mode          'sequential' or 'parallel'
                                Ceiling       the most that may run at once
                                CollisionKey  the fields that, if two runs AGREE
                                              on all of them, mean those two write
                                              the same files
                                Why           one line, printed before every batch
```

Two halves, and they are not the same question:

- **Ceiling is CAPACITY.** How many Stata/python processes the host will take.
  `-Parallel <N>` may lower it and may never exceed it; raising it is an edit to
  the file, with the reason, not a longer command line.
- **CollisionKey is CORRECTNESS.** The engine builds WAVES: two runs that agree on
  every key field land in different waves however wide the job runs. In
  Physician-SPACE's stage B this is real, not theoretical — a `full` run and a
  `synth` run of one task-year write the same `BENE-*` and `BFAF-*` files, because
  only `CASES-*` carries the source in its name.

The banner states the mode on EVERY invocation, and `-WhatIf` prints the waves off
disk, so what a reader is told can never drift from what will happen.

**A named entry point forwards BY NAME.** `@Rest` / `@args` splat an ARRAY, which
PowerShell binds positionally: an entry point written that way bound `-WhatIf` to
the next axis parameter and failed on every call. Forward `@PSBoundParameters`,
which is a hashtable. Checker code S9.

**Code at the wrong LEVEL is silent.** A job holding `scripts/`, a task holding
`src/`, or a `config/` left at a task root all run perfectly and cost a reader the
one thing the two words buy: knowing the level from the name. Checker code S10,
proven against a tree broken all three ways before it was trusted (GATE-1).

Reference copies: `ref/run_slice-template.ps1` (the engine, identical in all nine
Physician-SPACE jobs), `ref/batch-psd1-template.psd1` (a filled declaration with its
reasoning in comments), `ref/write_pages.py` (regenerates entry points, task pages
and sbatch READMEs from the tree), `ref/check_task_tree.py` (codes N* and S*).

### `0-libs/`: the one older name

`0-libs/` was the pre-260830 name for a job's shared folder. It survives in one
tree, `Project-Personality-OpioidRx` (Physician-SPACE), and it is no longer an
exemption with a rule of its own: under `src/` it is an ORDINARY SUBFOLDER,
`src/0-libs/`, and needs no law. That is what the exemption cost and what
retiring it bought. Tooling READS it and never writes it.

`src/` and `scripts/` are NOT two names for one idea (JL 260831). `src/` is the
JOB's shared code; `scripts/` is the TASK's own code; `config/` sits inside
`scripts/`. The different word IS the mechanism: a reader knows which level a
folder belongs to from its name alone, without walking the path back up. Both
are WRITTEN. A job never scaffolds `scripts/`, and a task never scaffolds `src/`.

**MANY .sh in one sbatch/ (JL 260830).** A batcher folder usually grows past one
file, and the files are ALTERNATIVE ENTRY POINTS, not a sequence — a person picks
one. So they are NOT numbered: numbering implies an order that does not exist and
invites `01_` to be run before `02_` when they are two ways to do the same thing.

```
sbatch/
├── run_job_dag.sh          the default: every task of this job, in order
├── run_from_t03.sh         a partial DAG — resume, or re-do a tail
└── run_job_dag.slurm.sh    an ENGINE VARIANT of a run_ script: <name>.<engine>.sh
```

**NO `env.sh` here (JL 260830).** The environment is the SPACE's, not the job's:
`<SPACE>/env.sh` at the repo root, sourced by the TICKET
(`source "$REPO_ROOT/env.sh"`), which is where it already happens. A per-job
`env.sh` would be a second place for the same settings to disagree, and a
batcher that sets environment is doing the ticket's job.

Three rules, all checkable:

```
① every file in sbatch/ starts with `run_`      it is an entry point, or it is
                                                 not a batcher — no env, no libs
② an engine variant is <name>.<engine>.sh        slurm · local · databricks
③ a job-level run_ script must reference at least TWO different tNN_ task
  folders. One means it serves a single task, and it belongs in that task's
  own sbatch/ instead — the rule that keeps the job-level folder from
  silently becoming a dumping ground.
```

Check ③ mechanically, from the job folder:

```
for f in sbatch/run_*.sh; do
  n=$(grep -oE 't[0-9][0-9]_[a-z0-9_]+' "$f" | sort -u | wc -l)
  [ "$n" -ge 2 ] || echo "$f spans $n task(s) — move it into that task"
done
```

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
