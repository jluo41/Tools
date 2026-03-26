Track B: Project Folder Structure (examples/)
===============================================

Ground truth for the standard layout of every project under examples/.
This file is the authoritative reference for fn-new.md and fn-review.md.

---

Overview
========

Every project lives under:

  examples/Proj{Series}-{Category}-{Num}-{Name}/

Two mandatory folders:

  tasks/           <- Self-contained task folders (logic + config + runs + results)
  paper/           <- Manuscripts, figures, LaTeX (often a git submodule)

Three optional folders:

  docs/            <- Project planning and summary documents
  cc-archive/      <- Claude Code session history
  _old/            <- Archived legacy files (safe to ignore)

Heavy outputs (model weights, full metrics, large tensors) go to
_WorkSpace/ -- NOT inside task result folders. The _WorkSpace/ paths are
declared in env.sh, NOT in the project folder.

Note: there is NO top-level config/ or results/ folder. Configs live inside
task folders (with symlinks for sharing). Results live inside each task's
results/ subfolder.


---

Naming Convention
=================

**Project folder name**: Proj{Series}-{Category}-{Num}-{Name}

  Series    Single uppercase letter. Research area grouping.
            Examples: A (early/misc), B (benchmarking), C (models), D (EHR)

  Category  Short descriptor of the research type.
            Examples: Bench, Model, EHR, Pretrain

  Num       Sequential integer within the Series-Category pair.
            Examples: 0, 1, 2, 3

  Name      CamelCase descriptor of the specific project.
            Examples: FairGlucose, ScalingLaw, WeightPredict

Full examples:
  ProjB-Bench-1-FairGlucose
  ProjC-Model-1-ScalingLaw
  ProjD-EHR-Mimic


---

Standard Layout
================

```
examples/Proj{Series}-{Category}-{Num}-{Name}/
|
+-- tasks/                                <- MANDATORY: all work lives here
|   +-- INDEX.md                          <- MANDATORY: global task index
|   +-- {G}{N}_{task_name}/               <- Task folder: group letter + seq + snake_case
|   |   +-- {G}{N}_{task_name}.py         <- Python logic (source of truth)
|   |   +-- {G}{N}_{task_name}.ipynb      <- Demo notebook (optional, derived from .py)
|   |   +-- config/                       <- YAML configs (real files or symlinks)
|   |   |   +-- {name}.yaml              <- Pipeline/model configs for this task
|   |   +-- runs/                         <- Execution variants
|   |   |   +-- {variant}.sh             <- Batch run (e.g., phase1_gpu0.sh)
|   |   |   +-- {variant}.ipynb          <- Parameterized notebook run (optional)
|   |   +-- results/                      <- Light summaries for this task's runs
|   |   |   +-- {variant}/               <- Mirrors run name (without extension)
|   |   |       +-- report.md
|   |   |       +-- metrics.json
|   |   +-- INDEX.md                      <- Run inventory for this task
|   +-- sbatch/                           <- Cross-task SLURM scripts (shared)
|       +-- submit_{name}.sh
|
+-- paper/                                <- MANDATORY: manuscripts + figures
|   +-- Paper-{Name}-{venue}/             <- One subfolder per submission
|       +-- (LaTeX files, figures, etc.)  <- Often its own git repo/submodule
|
+-- docs/                                 <- OPTIONAL: planning + summary docs
|   +-- TODO.md                           <- Pipeline progress tracker
|   +-- project-summary.md                <- Post-development summary
|
+-- cc-archive/                           <- OPTIONAL: Claude Code session history
|   +-- cc_YYMMDD_h{HH}_*.md             <- Session exports (/cc-session-summary)
|   +-- di_YYMMDD_h{HH}_*.md             <- Discussion logs (/coding-by-logging)
|
+-- _old/                                 <- OPTIONAL: archived legacy files
    +-- (anything that was superseded)
```


---

tasks/ Rules
=============

tasks/ is the heart of the project. Every piece of active work lives here.
Each subfolder is a self-contained task with its own logic, config, runs,
and results.

**Global rules:**
  - tasks/INDEX.md is MANDATORY.
  - No flat .py or .sh files directly in tasks/ (only task subfolders + sbatch/).
  - Each task folder is self-contained: you should be able to understand
    and run the task by looking only at its folder.


Task Group Naming Convention
-----------------------------

Tasks are named with a group-letter + sequence-number prefix:

  {G}{N}_{task_name}

  G           Single uppercase letter (A-Z). Groups related tasks by category.
              The project decides what each letter means. Common patterns:
                A = data pipeline, B = training, C = evaluation, D = demo
              But this is not prescribed -- any grouping that makes the project
              clear is valid.

  N           Single digit (0-9). Sequence within the group.
              0 is often reserved for cross-group utilities (e.g., B0_batch_evaluate).

  task_name   snake_case descriptor of what the task does.

  Examples:
    B1_train_stats          B3_train_neural         C2_eval_main_table
    B2_train_ml             B4_run_api              D1_demo_modeltuner

  The .py filename matches the folder name exactly:
    B1_train_stats/B1_train_stats.py

Tasks within a group sort naturally by the number prefix. Groups sort by letter.
tasks/INDEX.md uses one section per group (see INDEX.md rules below).


**Task folder contents in detail:**

  {G}{N}_{task_name}.py -- Main logic file (MANDATORY)
    - Source of truth for the task's logic.
    - Uses # %% cell markers for notebook compatibility (jupytext format).
    - Parameterized via --config or argparse arguments.

  {G}{N}_{task_name}.ipynb -- Demo notebook (OPTIONAL)
    - Derived from the .py file: jupytext --to notebook {name}.py -o {name}.ipynb
    - Same logic as the .py, just interactive. For walkthrough/documentation.
    - The .py is always the source of truth. Edit .py first, then convert.

  config/ — Task configs (OPTIONAL)
    - YAML files that parameterize the task.
    - Can be real files (if configs are unique to this task) or symlinks
      (if shared with other tasks).
    - Naming is flexible — use descriptive names that match the project's
      domain (e.g., fairglucose-per6h-h288l24-noevent-neural-patchtst.yaml).
    - Subdirectory structure within config/ is allowed for organization
      (e.g., config/demo/, config/fairglucose/neural/).

  runs/ — Execution variants (OPTIONAL)
    - Each .sh script is SELF-CONTAINED: all parameters, paths, and config
      references are hardcoded inside the script. No command-line arguments.
      Run with: bash runs/{name}.sh — that's it.
    - .sh files: batch execution. Each script is a complete, standalone run.
        Naming: {name}.sh — descriptive of what this specific run does.
        Good: build_v0003_per6h.sh, train_patchtst_noevent.sh
        Bad:  run.sh, 001_train.sh
    - .ipynb files: interactive parameterized runs (optional).
        Same principle — all parameters baked in, no external args needed.
    - No Python scripts (.py) in runs/ — logic stays in {task_name}.py.
    - The .py file contains the FUNCTIONS (logic). The .sh file calls them
      with hardcoded arguments. Different runs = different .sh files,
      not different arguments to the same .sh.

  results/ — Light summaries (OPTIONAL)
    - **Run name = result folder name** (drop the extension):
        runs/build_v0003_per6h.sh  <->  results/build_v0003_per6h/
        runs/train_patchtst.sh     <->  results/train_patchtst/
    - The .sh script writes output to its matching results/ folder.
    - Contents: report.md, metrics.json, plots/ (small PNGs), config_used.yaml
    - LIGHT only. Heavy outputs go to _WorkSpace/.

  INDEX.md — Run inventory (MANDATORY if runs/ exists)
    - Maps each run to its result folder and records outcome.


---

Config Sharing via Symlinks
============================

When multiple tasks use the same config files, ONE task holds the real
files and other tasks symlink to them.

Convention:
  - The task that is the most central or complete "owns" the real configs.
  - Other tasks symlink the entire config/ directory or specific subdirs.
  - Always use RELATIVE symlinks for git portability.

Example — FairGlucose project:

  tasks/cook_modelinstance/config/           <- REAL files (owner)
    demo/demo-neural-patchtst.yaml
    fairglucose/neural/per6h-h288l24-noevent/...

  tasks/cook_modeltuner/config               <- SYMLINK
    -> ../cook_modelinstance/config

  tasks/cook_modelpipeline/config            <- SYMLINK
    -> ../cook_modelinstance/config

  tasks/batch_evaluate/config                <- SYMLINK
    -> ../cook_modelinstance/config

Creating symlinks:
  cd tasks/cook_modeltuner
  ln -s ../cook_modelinstance/config config

Git stores symlinks as text (the relative target path). Works on Linux/Mac.
Windows needs core.symlinks=true.


---

tasks/INDEX.md Rules (MANDATORY -- global task index)
=====================================================

- Required at tasks/INDEX.md in every project.
- Purpose: global task list -- allows Claude to scan for existing tasks before
  creating new ones. Claude MUST read this before creating any new task folder.
- Created by fn-new.md at scaffold time. Updated whenever a task is added.

Format — one section per task group:

  # tasks/INDEX.md -- {PROJECT_ID}
  # Last updated: {YYMMDD}

  ## {G} -- {Group Description}

  | Task | Data | Stage | Description | Status |
  |------|------|-------|-------------|--------|
  | {G}{N}_{name} | {dataset} | {stage} | {description} | {status} |

  Example:

  ## B -- Model Training & Inference

  | Task | Data | Stage | Description | Status |
  |------|------|-------|-------------|--------|
  | B1_train_stats  | FairGlucose | 5 | Train stats models (naive, arima, autoets) | done |
  | B2_train_ml     | FairGlucose | 5 | Train ML models (xgboost, catboost, ...)   | done |
  | B3_train_neural | FairGlucose | 5 | Train neural models (patchtst, tft, ...)   | done |
  | B4_run_api      | FairGlucose | 5 | Run API/LLM models (claude, gpt, ...)      | done |

  ## C -- Evaluation & Paper Analysis

  | Task | Data | Stage | Description | Status |
  |------|------|-------|-------------|--------|
  | C1_eval_main_table | FairGlucose | eval | Generate main results table | done |

  Column definitions:
    Task          Task folder name (same as tasks/{G}{N}_{name}/)
    Data          Dataset(s) the task operates on
    Stage         Pipeline stage(s): 1 / 2 / 3 / 4 / 5 / 6 / eval / all
    Description   Short description of what the task does
    Status        stub | wip | done | deprecated


tasks/{task}/INDEX.md Rules (MANDATORY when runs/ exists)
==========================================================

- Required at tasks/{task}/INDEX.md in every task folder that has runs/.
- Purpose: run inventory -- maps each run to its result folder and outcome.
- Created when the task folder is created. Updated after each run.

Format:

  # {task}/INDEX.md -- {PROJECT_ID}
  # Last updated: {YYMMDD}

  | Run | Variant | Result Dir | Status | Notes |
  |-----|---------|------------|--------|-------|
  | phase1_gpu0.sh | Phase 1, GPU 0 | results/phase1_gpu0/ | done | loss 0.42 |
  | explore_patchtst.ipynb | Interactive PatchTST | results/explore_patchtst/ | done | |

  Column definitions:
    Run          Filename in runs/ (with extension)
    Variant      Human-readable description of what distinguishes this run
    Result Dir   Relative path to the result folder
    Status       planned | wip | done | failed | deprecated
    Notes        Key outcome, loss, or short note (optional)


---

Auto-Example Rule
==================

- Every new Track A stub (pipeline Fn builder or ML model stub) MUST have a
  paired example task automatically created in tasks/.
- Use the D group (demo/utility) by default: tasks/D{N}_example_{fn_or_model_name}/
- The task folder follows the same task-folder structure as any other task.
- Status in tasks/INDEX.md: "stub" (upgrades to "wip" or "done" as implementation progresses).

Example task Python file template:

```python
# Example: {FnClassName} -- {PROJECT_ID}
# Stage: {N}
# Data: {dataset}
# Created: {YYMMDD}
# Auto-generated by /haipipe-project new
# TODO: fill in after implementing the Fn via /haipipe-data design-chef {stage}

from haipipe.base import setup_workspace
# from haifn.fn_{layer}.{fn_module} import {FnClassName}  # uncomment after builder runs

SPACE = setup_workspace()

# Step 1: Load the source set
# source_set = SourceSet.load_asset(SPACE, name='{dataset}', version='@v0001-{dataset}')
# print(source_set)

# Step 2: Run the Fn
# fn = {FnClassName}()
# output = fn.run(source_set)
# print(output)
```


---

paper/ Rules
=============

- Contains manuscript source files (LaTeX, figures, tables, .bib).
- Often a separate git repository added as a submodule.
- Each submission gets its own subfolder:
    paper/Paper-{Name}-{venue}/
    Example: paper/Paper-FairGlucose-icml2026/
- Paper repos have their own lifecycle (branches for revisions, rebuttals, etc.)
  independent of the main project workflow.
- Evaluation scripts that generate paper figures/tables live in tasks/
  (e.g., tasks/eval_main_table/), NOT inside paper/. The paper/ folder
  only contains the final outputs that go into the manuscript.
- Large binary files (PDFs, compiled papers) follow the paper repo's own
  .gitignore rules.


---

results/ Rules
===============

There is NO top-level results/ folder. Results live inside each task folder:

  tasks/{task}/results/{variant}/

Light/heavy boundary (applies inside every task's results/):
  LIGHT -- commit to git:
    report.md        Markdown summary of the run
    metrics.json     Key numbers (loss, accuracy, F1, etc.)
    plots/           Small PNGs or SVGs (< 1 MB each)
    config_used.yaml Copy of the config that produced this result
    *.csv            Small summary tables
    *.tex            LaTeX table outputs
  HEAVY -- goes to _WorkSpace/ instead (do NOT put in results/):
    Model weights (.pt, .pth, .ckpt, .safetensors)
    Full prediction arrays (.npy, .pkl for large tensors)
    Checkpoint directories
    Anything > a few MB

Run name = result folder name (drop extension):
  tasks/A1_cook_data/runs/build_v0003_per6h.sh  <->  tasks/A1_cook_data/results/build_v0003_per6h/
  tasks/C2_eval_main_table/runs/all_noevent.sh  <->  tasks/C2_eval_main_table/results/all_noevent/

Each .sh is self-contained — bash runs/{name}.sh writes to results/{name}/.
No command-line arguments needed.

A run without a result folder is incomplete work (flagged by review).
A result folder without a matching run is orphaned (flagged by review).


---

_WorkSpace/ Path Resolution
============================

_WorkSpace/ paths are NOT declared inside the project folder.
They come from env.sh environment variables, read at runtime by setup_workspace()
in code/haipipe/base.py:

  local_source_store          = os.environ['LOCAL_SOURCE_STORE']
  local_record_store          = os.environ['LOCAL_RECORD_STORE']
  local_case_store            = os.environ['LOCAL_CASE_STORE']
  local_aidata_store          = os.environ['LOCAL_AIDATA_STORE']
  local_modelinstance_store   = os.environ['LOCAL_MODELINSTANCE_STORE']
  local_endpoint_store        = os.environ['LOCAL_ENDPOINT_STORE']

Every script calls setup_workspace() at the top and receives a SPACE dict
with all resolved paths. No project-level path declarations are needed.


---

docs/ Rules (OPTIONAL)
=======================

- Contains planning and summary documents only. No code, no data, no configs.
- Create docs/ when the project needs planning docs or summaries.
- Standard files (all optional):

  TODO.md              Pipeline progress tracker.
                       Created at scaffold time or by fn-review.md.
                       Format: see template below.

  project-summary.md   Post-development summary + flow chart.
                       Created by fn-summarize.md.
                       Readable by someone with zero prior context.

- Additional docs (design notes, meeting notes, references) may be added
  as plain .md files.

docs/TODO.md Template:

```markdown
# TODO -- {PROJECT_ID}
# Created: {YYMMDD}
# Last reviewed: {YYMMDD}

## Task Progress

| Task | Status | Notes |
|------|--------|-------|
| cook_modeltuner | done | |
| cook_modelinstance | done | |
| eval_main_table | wip | Missing LLM results |

## Track A Stubs

| Stub File | Paired Example | Status |
|-----------|----------------|--------|
| build_{dataset}_source.py | example_{dataset}_stage1_fn | todo |
| algorithm_{name}.py | example_{name}_model | todo |

## Pipeline Progress

| Stage | Status | Notes |
|-------|--------|-------|
| Stage 1 Source | done | |
| Stage 2 Record | done | |
| Stage 3 Case | n/a | |
| Stage 4 AIData | done | |
| Stage 5 Model | wip | |
```

Status values: todo | wip | done | n/a


---

cc-archive/ Rules (OPTIONAL)
==============================

- Stores Claude Code session context for this project.
- Create cc-archive/ when you start using /cc-session-summary or /coding-by-logging.
- Two file types:
    cc_*.md    Session exports produced by /cc-session-summary
    di_*.md    Discussion/design logs produced by /coding-by-logging
- Naming format: {type}_{YYMMDD}_h{HH}_{emoji}_{topic}_{author}.md
    Example: di_260310_h16_map_haipipe-project-skill-design_jluo.md
- Do NOT put code, config, or notebook files here.


---

_old/ Rules (OPTIONAL)
=======================

- Archive folder for superseded files from previous project iterations.
- Preserves git history while keeping the active project folder clean.
- No structure rules inside _old/ -- it is a catch-all.
- Content in _old/ is ignored by review and organize commands.


---

Light / Heavy Boundary Summary
================================

  Location                          What goes here                    In git?
  --------------------------------  --------------------------------  -------
  tasks/{task}/results/             report.md, metrics.json, plots    YES
  tasks/{task}/{task}.py            Python logic                      YES
  tasks/{task}/{task}.ipynb         Demo notebook (derived)           YES
  tasks/{task}/config/              YAML configs (real or symlink)    YES
  tasks/{task}/runs/*.sh            Run scripts                       YES
  tasks/{task}/runs/*.ipynb         Parameterized notebook runs       YES
  _WorkSpace/                       weights, checkpoints, arrays      NO
  cc-archive/                       CC session md files               YES
  paper/                            LaTeX, figures, .bib              YES


---

sbatch/ Rules (inside tasks/, shared across tasks)
===================================================

  - Use for bash/SLURM scripts that call multiple task Python scripts.
  - Also use for shared env setup scripts (env.sh, submit wrappers).
  - A script belongs here if it is cross-task (calls cook_modeltuner.py
    AND cook_modelinstance.py, etc.)
  - SLURM log directories (logs/) generated at runtime should be in .gitignore.


---

Review Checklist (used by fn-review.md)
========================================

**Structure checks:**
  [ ] Folder name matches Proj{Series}-{Category}-{Num}-{Name} pattern
  [ ] tasks/ directory exists
  [ ] tasks/INDEX.md exists
  [ ] paper/ directory exists (or acknowledged as n/a)
  [ ] No top-level config/ directory (configs live inside task folders)
  [ ] No top-level results/ directory (results live in tasks/{task}/results/)

**Per-task checks (for each tasks/{task}/ folder):**
  [ ] {task}/{task}.py exists (main logic file)
  [ ] {task}/INDEX.md exists (if runs/ exists)
  [ ] {task}/config/ exists (real or symlink) if task uses YAML configs
  [ ] Config symlinks resolve correctly (target exists)
  [ ] {task}/runs/ contains at least one .sh or .ipynb (if task has been run)
  [ ] Every run has a matching result folder in results/
  [ ] No heavy files in results/ (.pt, .pth, .ckpt, .safetensors, .npy > 1MB)
  [ ] Each results/{variant}/ contains at least a report.md or metrics.json

**Notebook checks (per task):**
  [ ] If {task}.ipynb exists, {task}.py also exists (source of truth)
  [ ] .ipynb in runs/ have descriptive names (not just "notebook.ipynb")

**docs/ checks (if docs/ exists):**
  [ ] docs/TODO.md exists
  [ ] docs/TODO.md task progress rows are current

**cc-archive/ checks (if cc-archive/ exists):**
  [ ] Contains at least one cc_*.md or di_*.md file
  [ ] No non-.md files mixed in

**paper/ checks (if paper/ exists):**
  [ ] Contains at least one Paper-{Name}-{venue}/ subfolder
  [ ] Evaluation outputs in paper/ have matching source tasks in tasks/

**Run-result alignment (per task):**
  [ ] Every run in runs/ has a matching results/{variant}/ folder
  [ ] Every results/{variant}/ has a matching run in runs/
