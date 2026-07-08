Task Hierarchy — Conceptual Model
==================================

Every piece of work in a project lives at one of three levels.


Level 1: Project
-----------------

```
examples/Proj{Series}-{Category}-{Num}-{Name}/
├── tasks/        ← all task-groups live here
├── diagram/      ← project-level story (01-story, 02-boundary + project.excalidraw; empty until authored)
└── paper/        ← optional, one per target venue
```

A project is one cohesive research effort. Forbidden at top level:
README.md, docs/, cc-archive/, _old/, configs/, results/.


Level 2: Task-group
--------------------

```
tasks/{G}{NN}_{group_name}/
├── {NN}_{task1}/      ← task-folders
├── {NN}_{task2}/
├── sbatch/            ← env.sh + cross-task batchers
└── diagram/           ← group-level (01-overview, 02-tasks, 03-progress, 04-design + group.excalidraw)
```

A task-group holds related task-folders that share context (same model
family, same evaluation suite, same figure set). They share one diagram
narrative and one sbatch coordinator.

Group letter (G) signals the **dominant task-type** in the group. Letters
are PROJECT-SPECIFIC — each project defines its own scheme, and the
project's scheme always wins. Specialist DEFAULTS for projects with none:

```
A-series   fit / model-run   pretraining, finetuning      (A01_pretraining_clm)
B-series   evaluation        eval, inference, scoring     (B01_evaluation_clm)
C-series   display           paper figures / tables       (C01_paper_figures)
D-series   data              pipeline builds              (D01_build_source)
E-series   individual        per-subject query/view       (E01_cgm_traces)
F-series   agent             LLM-agent compute            (F01_llm_labeling)
R-series   raw               Databricks raw extraction    (R01_extract_claims)
X_algo     algo-dev          smoke-test demos             (X_algo/*)
```

(`D` doubles as the default home for auto-example DEMO tasks —
`tasks/D_demo/D{N}_test_*` pairing `code/hainn` stubs, see
task-structure.md "Auto-Example Rule"; a data-pipeline D-group and a
D_demo group can coexist.)

Index NN starts at 01 within each letter; no gaps. A21 is allowed for
"finetuning bucket within A-series" — it groups a sub-family without
breaking the letter convention.


Level 3: Task-folder
---------------------

```
{NN}_{task_name}/
├── {NN}_{task_name}.py    ← the script (or notebook source via # %% cells)
├── configs/               ← <run>.yaml — _meta: block + params (frozen pre-run)
├── runs/                  ← <run>.sh — copies of ../../ref/run-sh-template.sh (haipipe-task)
├── results/               ← <run>/runtime.yaml + light artifacts; pairs with runs/<run>.sh
├── notebooks/             ← papermill output, one .ipynb per run
├── sbatch/                ← optional, for within-task GPU partitioning
└── diagram/               ← optional, only if task diverges from group narrative
```

A task-folder is one runnable unit. Run-script ↔ result-dir name pairing
is mandatory: `runs/run_foo.sh` produces `results/run_foo/`.

NO README.md anywhere.


Indexing & Naming
------------------

```
Project     Proj{Series}-{Category}-{Num}-{Name}
Task-group  {G}{NN}_{group_name}     G = letter (A/B/C/D), NN = 2 digits
Task-folder {NN}_{task_name}         NN = 2 digits within the group
Cross-ref   "A01.01"                 group A01 / task 01 (project-wide shorthand)
```

Rules:

- **2 digits.** Always `01`, `02`, ..., `09`, `10`, ... — never `1`, `2`,
  never `001`. Sorts cleanly up to 99 per bucket.
- **Start at 01.** Indices are 1-based; `00` is reserved for slots that
  must sort at the very top: `00-index.txt` in `diagram/`, a group-level
  `00` index for stage-0 work that precedes the pipeline (e.g. the
  embedded raw-extraction group `A00_rawstore_<cohort>/` sorting above
  `A01_data_pipeline_*`), and `00_*_fn_develop_*` builder tasks.
- **No gaps when scaffolding.** Pick the next free NN within the bucket.
- **Forward-fill on deletion.** If `02_foo` is removed, do NOT renumber
  `03_bar` → `02_bar`. Existing references (papers, runs, notebooks)
  point at task names; renaming breaks them. Just leave the gap.
- **Sub-buckets** for within-letter sub-families: jump by ten to signal
  a new sub-bucket within the same letter. `A01..A09` = pretraining;
  `A21..A29` = finetuning; `A41..` = next sub-family. The letter stays
  the same (still "model-run"); the leading digit groups the sub-family.
- **Project Num** counts projects within `{Series}-{Category}` only,
  not globally. Same composer rules: 2-3 digits, start at 1, no gaps
  on creation, forward-fill on deletion.

Validation responsibility:

- `/haipipe-task` (task-group / task-folder scaffolds) checks "no collision"
  at scaffold time; refuses to overwrite an existing index.
  (Project-level audit verbs were retired 2026-07-03; originals in project/_archive.)


Task-types (orthogonal to group letter)
----------------------------------------

A task-folder is one of these. Letter convention is a hint, not a hard
rule — a B-group can hold a display task if it makes narrative sense.

```
TYPE            CONFIG SKELETON (contents)  RESULTS LAND IN
--------------- --------------------------  --------------------------------------
fit (model-run) model/training keys         _WorkSpace/5-ModelInstanceStore/
evaluation      eval-target keys            results/<run>/{metrics.json, ...}
display         figure/table keys           results/<run>/{*.pdf, *.png, *.tex}
data-pipeline   Stage 1-4 pipeline keys     _WorkSpace/{1..4}-*Store/
other           (none required)             results/<run>/
```

The task TYPE decides the config's SKELETON (which keys it carries), never
its FILENAME — the filename is always the run name (configs/<run>.yaml,
matching runs/<run>.sh; see RUNNAME below and run-sh-template.sh).

Running process — papermill, always
------------------------------------

Every task-folder runs the same way. There is one template; no A vs B.

### Three identity axes: (Project, Task, Run)

A single execution is fully named by **three** axes — Project / Task / Run.
The first two are folders in the hierarchy; **Run is a name**, not a folder.

  Project   examples/Proj{...}/                         (Level 1)
  Task      tasks/{G}{NN}_{name}/{NN}_{task_name}/      (Level 3)
  Run       <run_name>                                  (e.g. "run_1m", "run_eval_holdout")

### RUNNAME — the spine of one execution

The Run axis appears as one shared `<run_name>` token across **four files
in four folders**. Pairing them by name is mandatory; tooling depends on it.

```
RUNNAME = run-xxxx

  configs/<run>.yaml          📥 inputs            (config + args)
  runs/<run>.sh               ▶️  entry             (bash: auto-generate + run notebook)
  results/<run>/              📊 light outputs     (eval.json, model-path pointer)
  notebooks/<run>.ipynb       📓 execution record  (papermill output, reviewable)
```

If you change the run name, you change all four. They are one entity in
four projections.

### Two notebooks, two roles — don't confuse them

```
{task}/{NN}_{task_name}.ipynb       TEMPLATE        (auto-converted from .py;
                                                     no execution state;
                                                     regenerated every run)

{task}/notebooks/<run>.ipynb        EXECUTION       (papermill output;
                                                     contains cell outputs,
                                                     errors, logs;
                                                     IS the run record)
```

The template lives at the task **root** alongside the .py source. Execution
records live in `notebooks/`, one per run. Never edit either by hand —
edit the .py.

### Authoring loop (offline, before any run)

```
   🧑 author
       │
       ▼ edits
   🐍 {task}/{NN}_{task_name}.py     (notebook-cell source, # %% blocks)
       │
       ▼ convert (one-shot, auto by run.sh — but you can preview)
   📓 {task}/{NN}_{task_name}.ipynb  (template, for visual review)
       │
       ▼ author reads the .ipynb, identifies what to change
       ↺  back to .py edits
```

Authoring happens in `.py` (diff-friendly). The `.ipynb` template exists
so the author can **read** the cell flow during review, not edit it.
Whether the .py edits are typed by hand or done with an assistant is an
implementation detail — the loop is the same.

### Execution flow (what `run.sh` does)

```
▶️  /runs/<run>.sh
   │
   ▼ Step 1: convert .py → template .ipynb at task root
       python code/scripts/convert_to_notebooks.py \
              {task}/{NN}_{task_name}.py
              -o {task}/{NN}_{task_name}.ipynb
   │
   ▼ Step 2: papermill inject parameters + execute
       papermill {task}/{NN}_{task_name}.ipynb \
                 {task}/notebooks/<run>.ipynb \
                 -p config configs/<run>.yaml \
                 -p key value ...
   │
   ▼ outputs split by weight
       📊 light artifacts  →  {task}/results/<run>/{eval.json, model_path.txt}
       💾 heavy artifacts  →  _WorkSpace/{N}-*Store/             (out-of-repo)
```

### Light vs heavy outputs

Two destinations, decided by file size and repo policy.

  📊 LIGHT (in-repo, under `results/<run>/`)
     metrics JSON, eval logs, figure files (.pdf/.png/.tex), source CSVs,
     **pointers** to heavy artifacts (e.g. `model_path.txt`).

  💾 HEAVY (out-of-repo, under `_WorkSpace/`)
     model checkpoints (.pt/.ckpt/.safetensors), large arrays (.npy/.pkl/.h5),
     trained-instance folders, raw cohort tables.

Heavy artifacts in `results/` is a hard error — caught by `-inspect`.

### sbatch — exogenous to the task

`sbatch/` is **outside** any single task-folder. It lives at the
**group** level (`tasks/{G}{NN}_{name}/sbatch/`) and coordinates multiple
runs across the group. A within-task `sbatch/` is allowed only for
GPU-partitioning a single sweep — it's secondary, not primary.

### Task-types decide

  1. Which group letter the task likely belongs to (A/B/C/D).
  2. Which YAML skeleton to seed in configs/.
  3. Where results actually land (results/ vs _WorkSpace/).
  4. Which parameters the run.sh injects.

The **process is invariant**; only the contents change.

### Where the workflow diagram lives

A visual of the complete flow (authoring loop + execution + outputs) is
in `ref/running-process.txt`.


Mandatory rules (cross-cutting)
--------------------------------

- Two-level hierarchy: tasks always live inside a task-group; never flat
  under `tasks/`.
- Each task-folder owns its YAMLs (no symlinks into other tasks).
- Run ↔ result name pairing is mandatory.
- Heavy artifacts (.pt / .ckpt / .safetensors / .npy / .pkl / .bin / .h5)
  go under `_WorkSpace/`, never `results/`.
- The doc surface is `diagram/`, never `README.md`. Diagram .txt content
  is authored via `/diagram-ascii`, bundled via `/diagram-ascii-canvas`.
- Code stubs in `code/hainn/` (or a legacy `code-dev/`) get a paired example
  task in `tasks/D_demo/` (Track A ↔ Track B coupling). Fn builders live in
  the project's `NN_<stage>_fn_develop_<cohort>/` task folders, which are
  their own runnable tasks — no extra demo pairing needed.
