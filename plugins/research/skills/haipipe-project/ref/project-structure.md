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
    |   +-- sbatch/                      <- group-level orchestration (optional)
    |   +-- A1_cook_data/
    |   |   +-- README.md
    |   |   +-- cook.py                  <- task logic
    |   |   +-- config/                  <- YAML configs
    |   |   +-- runs/                    <- atomic scripts (one per config)
    |   |   |   +-- run_source_a.sh
    |   |   |   +-- run_source_b.sh
    |   |   +-- results/                 <- name-paired with runs/
    |   |   |   +-- run_source_a/
    |   |   |   |   +-- 0-run_source_a.log
    |   |   |   +-- run_source_b/
    |   |   |       +-- 0-run_source_b.log
    |   |   +-- sbatch/                  <- task-level orchestration (optional)
    |   |       +-- all_gpu0.sh
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
  runs/           Atomic run scripts (one config = one script, no CLI args)
  results/        Light summaries (name-paired with runs/)
  sbatch/         Orchestration scripts (call runs/*.sh, assign GPUs)

  Python script rules:
    - Naming is freestyle: one file or many, any descriptive name.
    - Use # %% cell format for notebook compatibility.

  runs/ rules:
    - ATOMIC: each .sh runs exactly ONE config / ONE model. No loops.
    - Self-contained: all params hardcoded inside. No CLI args.
      Run with: bash runs/{name}.sh
    - No .py in runs/ -- logic stays in *.py files at task root.
    - Naming: descriptive of the single run.
      Examples: run_1m.sh, run_5m_ep0.1.sh, run_hybridA_5m.sh
    - The script sources env, sets paths, and calls the task's *.py
      with the matching config from config/.
    - Every run script MUST include the standard logging header
      (see "Run Script Logging Header" below).

  results/ rules:
    - LIGHT only: report.md, metrics.json, small PNGs, .csv, .tex
    - HEAVY goes to _WorkSpace/: weights, checkpoints, large arrays
    - Name-paired with runs/:
        runs/run_1m.sh    <->  results/run_1m/
        runs/run_5m.sh    <->  results/run_5m/
      (strip .sh from run name to get result dir name)
    - Without runs/: results/ holds output directly (flat or default/)

  sbatch/ rules:
    - ORCHESTRATION: each .sh batches multiple runs/*.sh together.
    - Assigns GPU, sets CUDA_VISIBLE_DEVICES, loops over runs.
    - Naming describes the batch scope:
      Examples: phase1_gpu0.sh, epoch_small_gpu0.sh, all_gpu1.sh
    - sbatch/ scripts call runs/*.sh (or source them), NOT *.py directly.
    - Can be run via SLURM (sbatch sbatch/foo.sh) or tmux.
    - sbatch/ can exist at task level AND at group level:
        Task-level sbatch/:  orchestrates runs within that task
        Group-level sbatch/: orchestrates runs across tasks in the group

  Run Script Logging Header
  =========================

    Every runs/*.sh script starts with this standard header:

      #!/bin/bash
      TASK_DIR="$(cd "$(dirname "$0")/.." && pwd)"
      RUN_NAME="$(basename "$0" .sh)"
      RESULT_DIR="${TASK_DIR}/results/${RUN_NAME}"
      mkdir -p "${RESULT_DIR}"
      exec > >(tee "${RESULT_DIR}/0-${RUN_NAME}.log") 2>&1

    This ensures:
      - results/{RUN_NAME}/ directory is created automatically
      - All stdout + stderr is captured to results/{RUN_NAME}/0-{RUN_NAME}.log
      - The 0- prefix sorts the log file to the top of the directory listing
      - Output still prints to terminal (visible in tmux / sbatch logs)
      - Works regardless of invocation method (direct, tmux, sbatch, or via sbatch/*.sh)

    After the header, the script sources env.sh, sets config path, and
    calls the task's *.py file.

  Relationship: runs/ <-> results/ <-> sbatch/
  =============================================

    config/B5_model_cgm_num_1m.yaml  --.
    runs/run_1m.sh -------------------+--> results/run_1m/    (1:1 pairing)
                                      |      +-- 0-run_1m.log
                                      |      +-- metrics.json (optional)
    config/B5_model_cgm_num_5m.yaml  --.
    runs/run_5m.sh -------------------+--> results/run_5m/    (1:1 pairing)
                                      |      +-- 0-run_5m.log
                                      |
    sbatch/gpu0.sh -------------------+--> calls runs/run_1m.sh, runs/run_5m.sh
                                           (many:1 -- one sbatch calls many runs)

    - config/ holds the YAML for each run (config naming is freestyle)
    - runs/ holds one script per config (atomic, self-contained)
    - results/ holds one dir per run (name-paired with runs/, NOT config/)
    - sbatch/ groups runs by GPU or batch (orchestration only)
    - The run script hardcodes the path to its config YAML inside

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

  Stage 5 tasks (model training, ModelArgs configs) should also include:

  Architecture -- ASCII diagram of the model forward pass.
    Show: input -> embedding -> backbone -> head -> output -> loss.
    Include an architecture sweep table when multiple sizes are trained.

    Example format:

      Architecture
      ============

        Input: [x_1, x_2, ..., x_L]      shape [B, L]
                      |
              embed   Linear(1 -> H)
                      |
              Transformer  (causal, N layers)
              +- Multi-Head Attn
              +- FFN (H -> 4H -> H)
                      |
              Hidden: [h_1, h_2, ..., h_L]  shape [B, L, H]
                      |
              head    Linear(H -> K)
                      |
              Output: [p_{t+1}, ..., p_{t+K}]   shape [B, L, K]
                      |
              Loss: mean MSE over K horizons

      Architecture Sweep (when multiple sizes are trained):

        Size  | Hidden | Layers | Heads | FFN  | LR    | Batch
        ------+--------+--------+-------+------+-------+------
        1m    |    128 |      4 |     2 |  512 | 8e-4  |   32
        100m  |    768 |     11 |    12 | 3072 | 4e-4  |   64

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
  [ ] runs/ scripts are atomic (one config = one script, no loops)
  [ ] runs/foo.sh <-> results/foo/ name pairing holds
  [ ] sbatch/ scripts call runs/*.sh (not *.py directly)
  [ ] If no runs/: results/ has flat files or default/ subfolder
  [ ] No heavy files in results/

docs / paper:
  [ ] docs/TODO.md current (if docs/ exists)
  [ ] No eval scripts in paper/ (belong in tasks/)
