Track B: Project Folder Structure (examples/)
===============================================

Ground truth for the standard layout of every project under examples/.
This file is the authoritative reference for fn-new.md and fn-review.md.

---

Overview
========

Every project lives under:

  examples/Proj{Series}-{Category}-{Num}-{Name}/

The four mandatory folders for all new projects:

  cc-archive/      <- Claude Code session history
  config/          <- YAML pipeline configs
  scripts/         <- Task folders (each self-contained: .py + runs/ + results/)
  docs/            <- Project planning and summary documents

One optional-but-standard folder (add when demo notebooks exist):

  nb/              <- Pipeline stage demo notebooks + INDEX.md

Heavy outputs (model weights, full metrics, large tensors) go to
_WorkSpace/ — NOT inside task result folders. The _WorkSpace/ paths are
declared in env.sh, NOT in the project folder.

Note: there is no top-level results/ folder. Light result summaries live
inside each task folder at scripts/{task}/results/.


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

Standard Layout (four mandatory + optional nb/)
================================================

```
examples/Proj{Series}-{Category}-{Num}-{Name}/
|
+-- cc-archive/                         <- Claude Code session history
|   +-- cc_YYMMDD_h{HH}_*.md           <- session exports (/cc-session-summary)
|   +-- di_YYMMDD_h{HH}_*.md           <- discussion logs (/coding-by-logging)
|
+-- config/                             <- YAML pipeline configs
|   +-- 1_source_{dataset}.yaml         <- Stage 1 (if used)
|   +-- 2_record_{dataset}.yaml         <- Stage 2 (if used)
|   +-- 3_case_{dataset}.yaml           <- Stage 3 (if used)
|   +-- 4_aidata_{dataset}.yaml         <- Stage 4 (if used)
|   +-- 5_model_{name}.yaml             <- Stage 5 (if used)
|
+-- scripts/                            <- Task-folder layout (one subfolder per task)
|   +-- INDEX.md                        <- MANDATORY: global task index
|   +-- {task_name}/                    <- One folder per task (clean snake_case name)
|   |   +-- INDEX.md                    <- MANDATORY: run inventory for this task
|   |   +-- {task_name}.py             <- Python logic (no seq/date prefix)
|   |   +-- runs/                       <- Bash/shell run scripts
|   |   |   +-- {variant}.sh           <- Named by variant (e.g., phase1_gpu0.sh)
|   |   +-- results/                   <- Light summaries for this task's runs
|   |       +-- {variant}/             <- Mirrors run script name (without .sh)
|   |           +-- report.md
|   |           +-- metrics.json
|   +-- sbatch/                         <- Cross-task SLURM scripts (shared)
|       +-- submit_{name}.sh            <- Calls multiple task Python scripts
|       +-- env.sh                      <- Optional: shared env setup
|
+-- docs/                               <- Project planning and summary documents
|   +-- TODO.md                         <- Pipeline progress tracker (created at scaffold)
|   +-- project-summary.md              <- Post-development summary + flow chart
|   +-- nb-plan.md                      <- Demo notebook planning reference (created by /haipipe-project nb)
|
+-- nb/                                 <- Demo notebooks (optional; add when demos exist)
    +-- INDEX.md                        <- MANDATORY if nb/ exists: notebook coverage index
    +-- 001_{YYMMDD}_{desc}.ipynb       <- Demo notebook (pipeline stage demo)
```


---

cc-archive/ Rules
=================

- Stores ALL Claude Code session context for this project.
- Two file types:
    cc_*.md    Session exports produced by /cc-session-summary
    di_*.md    Discussion/design logs produced by /coding-by-logging
- Naming format: {type}_{YYMMDD}_h{HH}_{emoji}_{topic}_{author}.md
    Example: di_260310_h16_map_haipipe-project-skill-design_jluo.md
- Do NOT put CLAUDE.md, README.md, or config files here.
- These files record WHY decisions were made, complementing the config/ YAMLs.


---

config/ Rules
=============

- Only YAML files. No Python, no notebooks, no scripts.
- Named by stage number + dataset or model name:
    1_source_{dataset}.yaml
    2_record_{dataset}.yaml
    3_case_{dataset}.yaml
    4_aidata_{dataset}.yaml
    5_model_{name}.yaml
- One YAML per stage per dataset/model combination.
- Stages not used by this project are simply absent (no placeholder files).
- These YAMLs are the Recipe in the cooking metaphor. They drive the pipeline.


---

scripts/ Rules
==============

Layout: task-folder paradigm. scripts/ contains one subfolder per logical task.
There are no flat .py or .sh files directly in scripts/ (except sbatch/).

Task folder rules:
  - Name: clean snake_case descriptor only. No seq number, no date prefix.
      Good: train_num, eval_all, gen_phase2_epoch_yamls
      Bad:  001_260310_train_num, train-num
  - Contents: one .py file + runs/ + results/ subdirectories + INDEX.md
  - The .py filename matches the folder name exactly: train_num/train_num.py

runs/ rules (inside each task folder):
  - Contains bash scripts only (.sh). No Python here.
  - Each script represents one execution variant (device, phase, ablation, etc.)
  - Naming: {variant}.sh — named by what makes it distinct, not by date.
      Good: phase1_gpu0.sh, ablation_cpu.sh, eval_phase1.sh
      Bad:  run_train_num.sh, 001_train.sh

results/ rules (inside each task folder):
  - Light summaries only. Committed to git.
  - Each subfolder mirrors a run script name (without .sh extension):
      runs/phase1_gpu0.sh  <->  results/phase1_gpu0/
  - Contents: report.md, metrics.json, plots/ (small PNGs < 1 MB), config_used.yaml
  - Heavy outputs (weights, checkpoints, large arrays) go to _WorkSpace/ instead.

sbatch/ rules (inside scripts/, shared across tasks):
  - Use for bash/SLURM scripts that call multiple task Python scripts.
  - Also use for shared env setup scripts (env.sh, submit wrappers).
  - A script belongs here if it is cross-task (calls train_num.py AND train_tkn.py, etc.)
  - SLURM log directories (logs/) generated at runtime should be in .gitignore.

scripts/INDEX.md Rules (MANDATORY — global task index)
=======================================================

- Required at scripts/INDEX.md in every project.
- Purpose: global task list — allows Claude to scan for existing tasks before
  creating new ones. Claude MUST read this before creating any new task folder.
- Created by fn-new.md at scaffold time. Updated whenever a task is added.

Format:

  # scripts/INDEX.md — {PROJECT_ID}
  # Last updated: {YYMMDD}

  | Task | Data | Stage | Description | Status |
  |------|------|-------|-------------|--------|
  | train_num  | OhioT1DM | 5 | Train TE-CLM num-token model | done |
  | train_tkn  | OhioT1DM | 5 | Train TE-CLM token model     | done |
  | eval_all   | OhioT1DM | 5 | Evaluate all trained models  | wip  |

  Column definitions:
    Task          Task folder name (same as scripts/{task}/)
    Data          Dataset(s) the task operates on
    Stage         Pipeline stage(s): 1 / 2 / 3 / 4 / 5 / 6 / all
    Description   Short description of what the task does
    Status        stub | wip | done | deprecated

scripts/{task}/INDEX.md Rules (MANDATORY — per-task run inventory)
===================================================================

- Required at scripts/{task}/INDEX.md in every task folder.
- Purpose: run inventory — maps each run script to its result folder and records outcome.
- Created when the task folder is created. Updated after each run.

Format:

  # {task}/INDEX.md — {PROJECT_ID}
  # Last updated: {YYMMDD}

  | Run Script | Variant | Result Dir | Status | Notes |
  |------------|---------|------------|--------|-------|
  | phase1_gpu0.sh | Phase 1, GPU 0 | results/phase1_gpu0/ | done | loss 0.42 |
  | phase2_gpu0.sh | Phase 2, GPU 0 | results/phase2_gpu0/ | wip  | running   |

  Column definitions:
    Run Script   Filename in runs/ (without path)
    Variant      Human-readable description of what distinguishes this run
    Result Dir   Relative path to the result folder (results/{variant}/)
    Status       planned | wip | done | failed | deprecated
    Notes        Key outcome, loss, or short note (optional)

Auto-Example Rule
==================

- Every new Track A stub (pipeline Fn builder or ML model stub) MUST have a
  paired example task automatically created in scripts/.
- Place in: scripts/example_{fn_or_model_name}/example_{fn_or_model_name}.py
- The task folder follows the same task-folder structure as any other task.
- Status in scripts/INDEX.md: "stub" (upgrades to "wip" or "done" as implementation progresses).

Example task Python file template:

```python
# Example: {FnClassName} — {PROJECT_ID}
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

results/ Rules
==============

There is NO top-level results/ folder. Results live inside each task folder:

  scripts/{task}/results/{variant}/

Light/heavy boundary (applies inside every task's results/):
  LIGHT — commit to git:
    report.md        Markdown summary of the run
    metrics.json     Key numbers (loss, accuracy, F1, etc.)
    plots/           Small PNGs or SVGs (< 1 MB each)
    config_used.yaml Copy of the config that produced this result
  HEAVY — goes to _WorkSpace/ instead (do NOT put in results/):
    Model weights (.pt, .pth, .ckpt, .safetensors)
    Full prediction arrays (.npy, .pkl for large tensors)
    Checkpoint directories
    Anything > a few MB

Run-result pairing: each result subfolder mirrors a run script name (no extension):
  scripts/train_num/runs/phase1_gpu0.sh  <->  scripts/train_num/results/phase1_gpu0/
  scripts/train_num/runs/phase2_gpu0.sh  <->  scripts/train_num/results/phase2_gpu0/

A run script without a result folder is incomplete work (flagged by review).
A result folder without a matching run script is orphaned (flagged by review).


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

docs/ Rules
============

- Contains planning and summary documents only. No code, no data, no configs.
- Two standard files:

  TODO.md              Created at scaffold time by fn-new.md.
                       Tracks all required files and pipeline progress.
                       Updated by fn-review.md after each review run.
                       Format: see template below.

  project-summary.md   Created at end of development by fn-summarize.md.
                       Human-readable summary + ASCII flow chart + key metrics.
                       Designed to be readable by someone with zero prior context.

  nb-plan.md           Created and updated by fn-nb.md (/haipipe-project nb).
                       One section per demo notebook in nb/.
                       Linked from every notebook's opening markdown cell so
                       the user and Claude always have a reference for what
                       each notebook should demonstrate.
                       Format: see fn/fn-nb.md Step 4 for section template.

- Additional docs (design notes, meeting notes, references) may be added here
  as plain .md files. No strict naming convention for extras.

docs/TODO.md Template:

```markdown
# TODO — {PROJECT_ID}
# Created: {YYMMDD}
# Last reviewed: {YYMMDD}

## Required Files

| File | Status | Notes |
|------|--------|-------|
| cc-archive/ | done | Created at scaffold |
| config/1_source_{dataset}.yaml | todo | Fill in SourceFnClass and args |
| config/2_record_{dataset}.yaml | todo | Fill after Stage 1 done |
| scripts/INDEX.md | done | Created at scaffold |
| scripts/{task_name}/ | todo | First task folder |
| scripts/{task_name}/INDEX.md | todo | Run inventory for first task |
| scripts/{task_name}/{task_name}.py | todo | First experiment script |
| scripts/{task_name}/runs/{variant}.sh | todo | First run script |
| scripts/{task_name}/results/{variant}/ | todo | Created after first run |
| docs/project-summary.md | todo | Run /haipipe-project summarize |
| docs/nb-plan.md | n/a | Created by /haipipe-project nb when first demo notebook is added |
| nb/INDEX.md | n/a | Create nb/ + INDEX.md when demo notebooks are added |

## Track A Stubs

| Stub File | Paired Example | Status |
|-----------|----------------|--------|
| build_{dataset}_source.py | example_{dataset}_stage1_fn.py | todo |
| algorithm_{name}.py | example_{name}_model.py | todo |

## Pipeline Progress

| Stage | Status | Notes |
|-------|--------|-------|
| Stage 1 Source | todo | |
| Stage 2 Record | todo | |
| Stage 3 Case | n/a | |
| Stage 4 AIData | todo | |
| Stage 5 Model | todo | |
```

Status values: todo | wip | done | n/a


---

Light / Heavy Boundary Summary
================================

  Location                        What goes here                    In git?
  ------------------------------  --------------------------------  -------
  scripts/{task}/results/         report.md, metrics.json, plots    YES
  _WorkSpace/                     weights, checkpoints, arrays      NO
  cc-archive/                     CC session md files               YES
  config/                         YAML configs                      YES
  scripts/{task}/{task}.py        Python logic                      YES
  scripts/{task}/runs/*.sh        Run scripts                       YES
  nb/                             demo notebooks (.ipynb)           YES


---

nb/ Rules (optional folder)
===========================

- nb/ is optional. Create it only when demo notebooks exist or are planned.
- Once nb/ exists, nb/INDEX.md is MANDATORY — same principle as scripts/INDEX.md.
- Only .ipynb files. No .py, .yaml, or .md files other than INDEX.md.
- Naming: {seq}_{YYMMDD}_{desc}.ipynb
    seq      3-digit zero-padded integer (001, 002, ...)
    YYMMDD   Date the notebook was written
    desc     Snake_case description of what the notebook demos
  Example: 001_260315_demo_source_to_record.ipynb

nb/INDEX.md Rules (MANDATORY when nb/ exists)
----------------------------------------------

- Purpose: documents what portion of the pipeline each notebook covers,
  and tracks planned-but-not-yet-created notebooks.
- Claude reads nb/INDEX.md in fn-organize Phase 2e to detect coverage gaps.
- Created when nb/ is first created. Updated whenever a notebook is added or changes status.

Format:

  # nb/INDEX.md — {PROJECT_ID}
  # Last updated: {YYMMDD}
  # Purpose: track pipeline demo notebooks by stages covered, input, and output.

  | Notebook | Stages | Input | Output | Status |
  |----------|--------|-------|--------|--------|
  | 001_260315_demo_s1_to_s2.ipynb | S1→S2 | raw visit records | RecordStore | done |
  | 002_260320_demo_case_build.ipynb | S2→S3 | RecordStore | CaseStore | wip |
  | (planned) | S3→S4 | CaseStore | AIDataStore | planned |

  Column definitions:
    Notebook   Filename (without path); use "(planned)" for not-yet-created entries
    Stages     Pipeline stages covered: S1→S2, S2→S3, S3→S4, S4→S5, S5→S6, etc.
    Input      Description of the input data or asset the notebook starts from
    Output     Description of the output data or intermediate result produced
    Status     planned | wip | done | deprecated

  Rows with status=planned represent intended demos not yet implemented.
  fn-organize Phase 2e flags all planned rows and uncovered stage transitions.


---

Review Checklist (used by fn-review.md)
========================================

**Structure checks:**
  [ ] Folder name matches Proj{Series}-{Category}-{Num}-{Name} pattern
  [ ] cc-archive/ directory exists
  [ ] config/ directory exists
  [ ] scripts/ directory exists
  [ ] results/ directory exists
  [ ] docs/ directory exists

**docs/ checks:**
  [ ] docs/TODO.md exists
  [ ] docs/TODO.md pipeline progress rows are current (no done stages marked todo)
  [ ] docs/project-summary.md exists (warn if absent, not block — generated at end)

**cc-archive/ checks:**
  [ ] Contains at least one cc_*.md or di_*.md file
  [ ] No non-archive files mixed in (no .py, .yaml, .ipynb)

**config/ checks:**
  [ ] All files are .yaml
  [ ] YAML filenames start with stage number prefix (1_, 2_, 3_, 4_, 5_)

**scripts/ checks:**
  [ ] scripts/INDEX.md exists (global task index)
  [ ] INDEX.md has a row for every task subfolder (no orphan tasks)
  [ ] No flat .py or .sh files directly in scripts/ (only sbatch/ and task subfolders)
  [ ] No notebooks (.ipynb) in scripts/ (notebooks belong in nb/)
  [ ] Every Track A stub has a paired example_{name}/ task folder

**Per-task checks (for each scripts/{task}/ folder):**
  [ ] {task}/INDEX.md exists (run inventory)
  [ ] {task}/{task}.py exists (Python logic file)
  [ ] {task}/runs/ exists and contains at least one .sh file
  [ ] {task}/INDEX.md has an entry for every run script in {task}/runs/
  [ ] Every {task}/runs/{variant}.sh has a matching {task}/results/{variant}/ folder
  [ ] No heavy files in {task}/results/ (.pt, .pth, .ckpt, .safetensors, .npy > 1MB)
  [ ] Each {task}/results/{variant}/ contains at least a report.md or metrics.json

**nb/ checks (if nb/ exists):**
  [ ] nb/INDEX.md exists (mandatory when nb/ exists)
  [ ] INDEX.md has an entry for every .ipynb in nb/
  [ ] No non-.ipynb files in nb/ other than INDEX.md
  [ ] All notebooks follow {seq}_{YYMMDD}_{desc}.ipynb naming
  [ ] No planned rows remain indefinitely (flag if status=planned for > 2 stages)

**script-result alignment:**
  [ ] Every script has a corresponding result folder
  [ ] Every result folder has a corresponding script
  [ ] seq numbers are consistent between scripts/ and results/
