Track B: Project Folder Structure (examples/)
===============================================

Ground truth for the standard layout of every project under examples/.
This file is the authoritative reference for fn-new.md and fn-review.md.

---

Overview
========

Every project lives under:

  examples/Proj{Series}-{Category}-{Num}-{Name}/

The five mandatory folders for all new projects:

  cc-archive/      <- Claude Code session history
  config/          <- YAML pipeline configs
  scripts/         <- All executable scripts (py + sh)
  results/         <- Light summaries only (committed to git)
  docs/            <- Project planning and summary documents

One optional-but-standard folder (add when demo notebooks exist):

  nb/              <- Pipeline stage demo notebooks + INDEX.md

Heavy outputs (model weights, full metrics, large tensors) go to
_WorkSpace/ — NOT results/. The _WorkSpace/ paths are declared in
env.sh, NOT in the project folder.


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

Standard Layout (five mandatory + optional nb/)
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
+-- scripts/                            <- All executable scripts (FLAT layout)
|   +-- INDEX.md                        <- MANDATORY: script index for reuse scanning
|   +-- 001_{YYMMDD}_{desc}.py          <- Python script
|   +-- 002_{YYMMDD}_{desc}.sh          <- Shell/bash script
|   +-- 003_{YYMMDD}_example_{name}.py  <- Auto-generated example for Track A stubs
|   +-- sbatch/                         <- Optional: SLURM job scripts
|       +-- 001_{YYMMDD}_{desc}.sh
|
+-- results/                            <- Light summaries only (in git)
|   +-- 001_{YYMMDD}_{desc}/           <- Mirrors script name exactly
|   |   +-- report.md
|   |   +-- metrics.json
|   +-- 002_{YYMMDD}_{desc}/
|       +-- report.md
|       +-- metrics.json
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

- All executable scripts live here, regardless of type. Layout is FLAT:
    .py      Main Python logic (training, evaluation, analysis)
    .sh      Shell scripts (env setup, data prep)
    .sbatch  SLURM batch submission scripts
- If there are many SLURM scripts, use an sbatch/ subdirectory (only exception).
- Rule: a script triggers execution. Its output goes to results/ (light)
  or _WorkSpace/ (heavy).
- Naming format: {seq}_{YYMMDD}_{desc}.{ext}
    seq      3-digit zero-padded integer (001, 002, ...)
             Represents the logical execution order, not creation order.
    YYMMDD   Date the script was written (YY = 2-digit year)
    desc     Snake_case description of what the script does
  Examples:
    001_260310_train_baseline.py
    002_260310_eval_results.sh
    003_260315_example_glucose_source_fn.py   <- auto-generated for Track A stub

scripts/INDEX.md Rules (MANDATORY)
====================================

- INDEX.md is a required file in every project's scripts/ directory.
- Purpose: allows Claude to scan for existing scripts BEFORE creating new ones,
  to maximize code reuse and avoid duplication.
- Created by fn-new.md at scaffold time. Updated whenever a script is added or changes status.
- Claude MUST read scripts/INDEX.md before creating any new script in a project.

Format:

  # scripts/INDEX.md — {PROJECT_ID}
  # Last updated: {YYMMDD}

  | Script | Data | Functionality | Stage | Status |
  |--------|------|---------------|-------|--------|
  | 001_260310_train_baseline.py | OhioT1DM | Train baseline TE-CLM model | 5 | done |
  | 002_260310_eval_results.sh   | OhioT1DM | Evaluate and export metrics  | 5 | done |
  | 003_260315_example_source_fn.py | OhioT1DM | Example usage of GlucoseSourceFn | 1 | stub |

  Column definitions:
    Script        Filename (without path)
    Data          Dataset(s) the script operates on
    Functionality Short description of what the script does
    Stage         Pipeline stage(s): 1 / 2 / 3 / 4 / 5 / 6 / all
    Status        stub | wip | done | deprecated

Auto-Example Rule
==================

- Every new Track A stub (pipeline Fn builder or ML model stub) MUST have a
  paired example script automatically created in scripts/.
- Purpose: makes it easy to examine and test the new code immediately.
- Naming: {seq}_{YYMMDD}_example_{fn_or_model_name}.py
- The example script is created by fn-new.md at scaffold time alongside the stub.
- Contents: minimal working example showing how to load and call the Fn or model.
- Status in INDEX.md: "stub" (upgrades to "wip" or "done" as implementation progresses).

Example script content template:

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

- Light summaries only. Committed to git.
- What belongs here:
    report.md        Markdown summary of the run
    metrics.json     Key numbers (loss, accuracy, F1, etc.)
    plots/           Small PNGs or SVGs (< 1 MB each)
    config_used.yaml Copy of the config that produced this result
- What does NOT belong here (goes to _WorkSpace/ instead):
    Model weights (.pt, .pth, .ckpt, .safetensors)
    Full prediction arrays (.npy, .pkl for large tensors)
    Checkpoint directories
    Anything > a few MB
- Naming: each result folder mirrors its script name exactly:
    scripts/001_260310_train_baseline.py  <->  results/001_260310_train_baseline/
    scripts/002_260310_eval_results.sh    <->  results/002_260310_eval_results/
- A script without a result folder is incomplete work (flagged by review).
- A result folder without a matching script is orphaned (flagged by review).


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
| scripts/001_{YYMMDD}_{desc}.py | todo | First experiment script |
| results/001_{YYMMDD}_{desc}/ | todo | Created after first run |
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

  Location             What goes here                    In git?
  -------------------  --------------------------------  -------
  results/             report.md, metrics.json, plots    YES
  _WorkSpace/          weights, checkpoints, arrays      NO
  cc-archive/          CC session md files               YES
  config/              YAML configs                      YES
  scripts/             .py, .sh, .sbatch scripts         YES
  nb/                  demo notebooks (.ipynb)           YES


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
  [ ] scripts/INDEX.md exists
  [ ] INDEX.md has an entry for every script in scripts/ (no orphan scripts)
  [ ] INDEX.md has no entries for scripts that no longer exist
  [ ] All scripts follow {seq}_{YYMMDD}_{desc}.{ext} naming
  [ ] seq values are 3-digit zero-padded (001, not 1)
  [ ] No notebooks (.ipynb) in scripts/ (notebooks belong in nb/)
  [ ] Every Track A stub has a paired example_{name}.py script

**results/ checks:**
  [ ] Each result folder name matches a script name (without extension)
  [ ] No heavy files present (.pt, .pth, .ckpt, .safetensors, .npy > 1MB)
  [ ] Each result folder contains at least a report.md or metrics.json

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
