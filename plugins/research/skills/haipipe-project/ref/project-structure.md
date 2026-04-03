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
  |   +-- README.md       <- MANDATORY: project-level task overview (flow + structure + status)
  |   +-- {G}_{group}/    <- Group folders (each has its own README.md)
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
    - Evaluation scripts (belong in tasks/C_evaluation/)
    - Raw data or model outputs (belong in _WorkSpace/)
    - Pipeline configs (belong in tasks/{G}_{group}/{task}/config/)
  Data flow: tasks/ produces figures/tables -> copied or symlinked into paper/

---

Group Folders
=============

  Two-level hierarchy: tasks/ -> group folders -> task folders.

  {G}_{group_name}/

  G = uppercase letter (matches its tasks' prefix)
  group_name = snake_case descriptor

  Group folder contents:
    README.md        <- MANDATORY: group purpose, task list, internal flow
    sbatch/          <- OPTIONAL: cross-task SLURM scripts within this group
    {G}{N}_{name}/   <- task folders (each owns its own config/)

  Group README.md has three sections:
    1. Purpose -- one line
    2. Flow -- which tasks feed into which (within the group)
    3. Task list -- | Task | Description | Status |

  Example:
    tasks/
    +-- A_data/
    |   +-- README.md
    |   +-- A1_cook_data/
    |   +-- A2_data_event_alignment/
    +-- B_training/
    |   +-- README.md
    |   +-- B1_train_stats/
    |   +-- B2_train_ml/

---

Task Naming
===========

  {G}{N}_{task_name}

  G = uppercase letter, matches its group folder's letter
  N = digit (or multi-digit), sequence within group
  task_name = snake_case descriptor

---

Task Folder Contents
====================

  *.py            One or more Python scripts (freestyle naming, # %% cell format)
  README.md       Task-level documentation (mandatory, see format below)
  config/         YAML configs (each task owns its own, no sharing/symlinks)
  runs/           Self-contained .sh scripts (bash runs/{name}.sh -- no args)
  results/        Light summaries (run-result name pairing when runs/ exists)

  Python script rules:
    - Naming is freestyle: one file or many, any descriptive name.
    - Use # %% cell format for notebook compatibility.

  runs/ rules:
    - Each .sh is self-contained: all params hardcoded. No CLI args.
    - No .py in runs/ -- logic stays in *.py files.
    - Different runs = different .sh files.

  results/ rules:
    - LIGHT only: report.md, metrics.json, small PNGs, .csv, .tex
    - HEAVY goes to _WorkSpace/: weights, checkpoints, large arrays
    - With runs/:    runs/foo.sh <-> results/foo/  (name pairing, strip .sh)
    - Without runs/: results/ holds output directly (flat files or default/ subfolder)

---

README.md Formats
==================

tasks/README.md (project-level, mandatory):

  Three sections, in order:

  1. ASCII Flow Graph -- shows task dependencies and logic
     Use arrows (-->, +->), groups (--- Group Name ---), and short
     annotations to show WHY tasks connect, not just THAT they connect.

  2. ASCII Directory Tree -- shows folder structure with one-line descriptions
     Use +-- for tree branches, <- for annotations.
     Mark phases/groups (e.g., [original], [rebuttal], [demo]).

  3. Status Table -- tracks completion
     | Task | Description | Status |
     Status: stub | wip | done | deprecated

{G}_{group}/{task}/README.md (per-task, mandatory):

  Five sections, each 1-3 lines:

  1. What -- one-line purpose
  2. Why -- which paper section / rebuttal point / research question it serves
  3. Inputs -- data paths or upstream tasks it reads from
  4. Outputs -- result files or downstream tasks it feeds
  5. Runs -- (if runs/ exists) table of run variants and status

     | Run | Variant | Result Dir | Status | Notes |
     Status: planned | wip | done | failed | deprecated

---

Auto-Example Rule
==================

Every Track A stub gets a paired example task in tasks/ (group D by default).
Status in group README.md: "stub" until implemented.

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
  [ ] tasks/ exists with README.md (flow graph + tree + status table)
  [ ] No top-level config/ or results/
  [ ] Tasks are inside group folders (tasks/{G}_{group}/{G}{N}_{name}/)

Per group:
  [ ] {G}_{group}/README.md exists (purpose, flow, task list)
  [ ] Group letter matches its tasks' prefix

Per task:
  [ ] At least one *.py exists in the task folder
  [ ] {task}/README.md exists (what, why, inputs, outputs, runs)
  [ ] {task}/config/ exists with its own YAML files (no symlinks)
  [ ] If runs/ exists: runs/foo.sh <-> results/foo/ name pairing holds
  [ ] If no runs/: results/ has flat files or default/ subfolder
  [ ] No heavy files in results/

docs / paper:
  [ ] docs/TODO.md current (if docs/ exists)
  [ ] No eval scripts in paper/ (belong in tasks/)
