Track B: Project Folder Structure (examples/)
===============================================

Every project lives under:  examples/Proj{Series}-{Category}-{Num}-{Name}/

---

Naming Convention
=================

  Proj{Series}-{Category}-{Num}-{Name}

  Series    Single uppercase letter (A=misc, B=benchmarking, C=models, D=EHR)
  Category  Short descriptor (Bench, Model, EHR, Pretrain)
  Num       Sequential integer within Series-Category
  Name      CamelCase (FairGlucose, ScalingLaw, WeightPredict)

---

Standard Layout
================

  examples/{PROJECT_ID}/
  +-- tasks/              <- MANDATORY: all work lives here
  |   +-- INDEX.md        <- MANDATORY: global task index
  |   +-- {G}{N}_{name}/  <- Task folders
  |   +-- sbatch/         <- Cross-task SLURM scripts (optional)
  +-- paper/              <- OPTIONAL: manuscripts, LaTeX (often git submodule)
  +-- docs/               <- OPTIONAL: TODO.md, project-summary.md
  +-- cc-archive/         <- OPTIONAL: CC session history (cc_*.md, di_*.md)
  +-- _old/               <- OPTIONAL: archived legacy files (ignored by tools)

  No top-level config/ or results/.
  paper/ = external-facing (manuscript, reviews). docs/ = internal-facing (TODO, notes).

  paper/ contains ONLY:
    - LaTeX source (.tex, .bib, .sty), final figures/tables, submission materials
    - Often its own git repo/submodule: paper/Paper-{Name}-{venue}/
  paper/ does NOT contain:
    - Evaluation scripts (belong in tasks/C*_eval_*)
    - Raw data or model outputs (belong in _WorkSpace/)
    - Pipeline configs (belong in tasks/{task}/config/)
  Data flow: tasks/ produces figures/tables -> copied or symlinked into paper/

---

Task Naming
===========

  {G}{N}_{task_name}

  G = uppercase letter, groups related tasks (project decides letter meaning)
  N = digit, sequence within group
  task_name = snake_case descriptor
  Filename matches folder: B1_train_stats/B1_train_stats.py

---

Task Folder Contents
====================

  {task}.py       Main logic (source of truth, # %% cell format)
  config/         YAML configs (real files or symlinks to another task's config/)
  runs/           Self-contained .sh scripts (bash runs/{name}.sh -- no args)
  results/        Light summaries (run name = result folder name)
  INDEX.md        Run inventory (mandatory if runs/ exists)

  runs/ rules:
    - Each .sh is self-contained: all params hardcoded. No CLI args.
    - No .py in runs/ -- logic stays in {task}.py.
    - Different runs = different .sh files.

  results/ rules:
    - LIGHT only: report.md, metrics.json, small PNGs, .csv, .tex
    - HEAVY goes to _WorkSpace/: weights, checkpoints, large arrays
    - Run-result mapping: runs/foo.sh <-> results/foo/

---

Config Sharing via Symlinks
============================

One task owns real config files; others symlink using relative paths.

  tasks/B1_train_stats/config/     <- REAL (owner)
  tasks/B2_train_ml/config         <- SYMLINK -> ../B1_train_stats/config

---

INDEX.md Formats
=================

tasks/INDEX.md (global, mandatory):

  | Task | Data | Stage | Description | Status |
  |------|------|-------|-------------|--------|
  Status: stub | wip | done | deprecated

tasks/{task}/INDEX.md (per-task, mandatory when runs/ exists):

  | Run | Variant | Result Dir | Status | Notes |
  |-----|---------|------------|--------|-------|
  Status: planned | wip | done | failed | deprecated

---

Auto-Example Rule
==================

Every Track A stub gets a paired example task in tasks/ (group D by default).
Status in INDEX.md: "stub" until implemented.

---

_WorkSpace Paths
=================

Declared in env.sh, read by setup_workspace() in code/haipipe/base.py.
NEVER inside the project folder.

---

Review Checklist
=================

Structure:
  [ ] Name matches Proj{Series}-{Category}-{Num}-{Name}
  [ ] tasks/ exists with INDEX.md
  [ ] No top-level config/ or results/

Per task:
  [ ] {task}/{task}.py exists
  [ ] {task}/INDEX.md exists (if runs/ present)
  [ ] Config symlinks resolve
  [ ] Run-result pairs match
  [ ] No heavy files in results/

docs / paper:
  [ ] docs/TODO.md current (if docs/ exists)
  [ ] No eval scripts in paper/ (belong in tasks/)
