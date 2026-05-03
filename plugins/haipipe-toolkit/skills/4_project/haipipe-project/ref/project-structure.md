Track B: Project Folder Structure (examples/)
===============================================

Every project lives under: examples/Proj{Series}-{Category}-{Num}-{Name}/

The doc surface is `diagram/`, NOT `README.md`. Three levels of `diagram/`
folders (project, task, paper) replace what used to be README.md and docs/.

  Diagrams are authored via /diagram-ascii (.txt sources, ASCII + emoji)
  and bundled into .excalidraw via /diagram-ascii-canvas (txt-to-canvas.py).
  Both .txt and .excalidraw are committed to git: .txt is grep-able and
  LLM-readable; .excalidraw is the human-readable + annotatable canvas.

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
  +-- tasks/          <- MANDATORY: all task work here
  +-- diagram/        <- MANDATORY: project-level story (high-level only)
  +-- paper/          <- OPTIONAL: manuscripts (each Paper-* gets own diagram/)

  No top-level: configs/, results/, README.md, docs/, cc-archive/, _old/

  Project-level state lives in three places:
    - SHAPE       project layout enforced by haipipe-project specialists
    - STORY       in {PROJECT}/diagram/  (this folder, high-level)
    - DETAIL      in {task}/diagram/     (per-task, operational)

---

Project-level diagram/  (high-level story)
============================================

  examples/{PROJECT_ID}/diagram/
  +-- 01-story.txt          motivation, research question, expected impact
  +-- 02-boundary.txt       in-scope / out-of-scope / definitions / assumptions
  +-- 03-exploration.txt    directions tried / active / backlog / ruled out
  +-- project.excalidraw    bundle (built by txt-to-canvas)

  HIGH-LEVEL ONLY — research narrative, NOT an operational dashboard.
  Status tables, run metrics, daily logs belong in {task}/diagram/.

  Authored via /diagram-ascii, bundled via /diagram-ascii-canvas. Refresh
  on substantive narrative change; otherwise stable.

---

Group Folders
=============

  Two-level hierarchy: tasks/ -> group folders -> task folders.

  {G}{NN}_{group_name}/{NN}_{task_name}/

  G   uppercase series letter (A=training, B=evaluation, ...)
  NN  2-digit index (group: unique within series; task: sequential within group)
  *_name  snake_case descriptor

  Index lets ls sort by dependency: A01 (pretraining) < A21 (finetuning) < B01.
  Reserve ranges by stage: A01-A09 stage 1, A20-A29 stage 2, etc.

  Examples:
    A01_pretraining_clm/01_train_clm_num_modelsize/
    A21_finetuning_clm_for_event_reg/01_ft_clm_num_tar_next1h/
  Reference globally as "A01.01".

  Group folder contents:
    diagram/        MANDATORY when group is cohesive (siblings share a
                    narrative); covers per-task diagram so tasks stay thin.
                    See "Group-level diagram/" below.
    sbatch/         Cross-task orchestration (env.sh + batchers).
    {NN}_{name}/    task folders.

  No README.md in group folders. If sibling tasks are unrelated, fall back
  to per-task diagrams instead of group/diagram/.

---

Task Naming
===========

  {NN}_{task_name}

  NN = 2-digit zero-padded index (sequence within the group)
  task_name = snake_case descriptor

  Tasks are numeric-only — they live inside their group folder, so the
  group letter is implicit in the path. Globally referenced as
  "{group_id}.{task_id}" (e.g. "A01.01").

---

Task Folder Contents
====================

  *.py            One or more Python scripts (freestyle naming, # %% cell format)
  configs/         YAML configs (each task owns its own, no sharing/symlinks)
  runs/           Atomic run scripts (one config = one script, no CLI args)
  results/        Light summaries (name-paired with runs/)
  <stem>.ipynb    Template notebook(s) at TASK ROOT, one per cell-format *.py
                  (e.g. train_num_nb.py ↔ train_num_nb.ipynb). Built by
                  convert_to_notebooks.py from the .py source. Sits next to
                  its .py so opening the task folder shows source + template
                  side-by-side.
  notebooks/       MANDATORY: runtime-recording folder. Holds one
                  <run_name>.ipynb per runs/<run_name>.sh — papermill injects
                  params from the runs/*.sh and writes the executed result
                  here. Each run's notebook captures full execution +
                  injected params + outputs — it's the canonical "what
                  happened during this run" record. Use papermill mode for
                  parameterized ML training, nbconvert mode for single-render
                  data-audit / DIKW / exploration.
  sbatch/         OPTIONAL: task-internal orchestration — e.g. splitting
                  this task's runs across multiple GPUs. Group/sbatch/ is
                  for cross-task orchestration; task/sbatch/ is for
                  within-task. Both levels can coexist.
  diagram/        OPTIONAL: only when this task diverges from the group
                  narrative. If group/diagram/ covers it, skip.

  TASKS DO NOT HAVE A README.md. The doc surface is group/diagram/ (for
  cohesive groups) or task/diagram/ (for divergent tasks).

  Python script rules:
    - Naming is freestyle: one file or many, any descriptive name.
    - Use # %% cell format for notebook compatibility.

  runs/ rules:
    - ATOMIC: each .sh runs exactly ONE config / ONE model. No loops.
    - Self-contained: all params hardcoded inside. No CLI args.
      Run with: bash runs/{name}.sh
    - No .py in runs/ — logic stays in *.py files at task root.
    - Naming: descriptive of the single run.
      Examples: run_1m.sh, run_5m_ep0.1.sh, run_hybridA_5m.sh
    - Every run script MUST include the standard logging header (see below).

  results/ rules:
    - LIGHT only: report.md, metrics.json, small PNGs, .csv, .tex
    - HEAVY goes to _WorkSpace/: weights, checkpoints, large arrays
    - Name-paired with runs/:
        runs/run_1m.sh    <->  results/run_1m/
        runs/run_5m.sh    <->  results/run_5m/
      (strip .sh from run name to get result dir name)
    - Without runs/: results/ holds output directly (flat or default/)

  notebooks/ rules:
    - Two locations:
        <task>/<stem>.ipynb            template, paired 1:1 with <stem>.py
        <task>/notebooks/<run>.ipynb   runtime record, paired 1:1 with runs/<run>.sh
      Stems match exactly (no rename). Source of truth is always the .py;
      both .ipynb files are build artifacts.

    - Two build modes:
        papermill   (parameterized: one .py + many runs differing in hyperparams)
                    runs/<run>.sh: convert_to_notebooks.py → <stem>.ipynb,
                    then `papermill <stem>.ipynb notebooks/<run>.ipynb -p ...`
                    Output bakes stdout/stderr + injected params + figures.
        nbconvert   (single-render: one .py = one execution, no knobs)
                    `python <stem>.py` then `jupyter nbconvert --execute`.

    - Papermill .py conventions:
        First cell after docstring is `# %% [parameters]` — declares all
        tunable knobs with defaults. convert_to_notebooks.py tags it for
        papermill injection.
        Setup cell auto-detects TASK_DIR for portability:
          __file__ (script) → __vsc_ipynb_file__.parent.parent (VS Code)
            → os.environ['TASK_DIR']  (exported by run.sh)
        runs/<run>.sh in papermill mode does NOT use `exec > >(tee log)`;
        the recorded notebook IS the log. exports TASK_DIR before papermill.

    - Commit policy: per-project. Commit when collaborators benefit from
      the rendered form; gitignore when churn dominates. Template <stem>.ipynb
      is usually safe to gitignore (regenerates from .py).

  sbatch/ rules:
    - ORCHESTRATION: each .sh coordinates one or several runs/*.sh.
    - Assigns GPU, sets CUDA_VISIBLE_DEVICES, loops over runs.
    - sbatch/ scripts call runs/*.sh, NOT *.py directly.
    - Two levels — both valid, at different scopes:
        group/sbatch/   cross-task orchestration: env.sh + batchers that
                        loop over runs from multiple sibling tasks.
        task/sbatch/    task-internal orchestration: GPU split or batch
                        across this task's own runs/*.sh only.
      Group/sbatch/ is the more common case (env.sh + cross-task batchers
      live there). Task/sbatch/ is fine when orchestration is genuinely
      task-scoped and would awkwardly leak siblings into a group script.

---

Skill-Runner Tasks (Exemption)
================================

  When a task wraps a Claude Code skill (e.g. /dikw) instead of a .py,
  the skill executes the work and writes structured outputs elsewhere
  (e.g. _agent_dikw_space/...). The task folder is narrative + launcher.

  Exemptions:
    - No *.py, no data/ required.
    - configs/ optional but recommended: one configs/<slug>.yaml per
      question; configs/_defaults.yaml for shared keys.
    - runs/<slug>.sh is a thin launcher around `claude "/<skill> ..."`:
        * Use `claude` (interactive TUI), NOT `claude -p`.
        * Pass `--session-id $(uuidgen)`, copy session.jsonl to
          results/<run>/ after exit (debug record only — substantive
          output lives wherever the skill writes it).
        * Pass `--dangerously-skip-permissions` (config-driven; default
          true) so the skill can run pandas / write files freely.
        * Do NOT use `exec > >(tee log)` — breaks the TUI.
    - Two-tier shape recommended for ≥2 questions: runs/_run.sh shared
      launcher reads YAML + exec's claude; runs/ask_<slug>.sh one-line
      wrapper. Underscore prefix reserved for shared/template files.
    - results/ holds the session transcript (debug); substantive
      outputs live at the skill's own artifact paths.

---

Group-level diagram/  (cohesive-group narrative)
==================================================

  tasks/{G}_{group}/diagram/
  +-- 01-overview.txt    what this group is, why it exists, narrative
                          binding sibling tasks
  +-- 02-tasks.txt       | Task | What it sweeps | Status |  (one row per
                          sibling task)
  +-- 03-progress.txt    cross-task runs / progress table
  +-- 04-design.txt      shared script logic when tasks share a .py / approach
  +-- group.excalidraw   bundle (built by txt-to-canvas)

  Use group-level diagram/ when sibling tasks form a coherent story
  (e.g. "scaling-law sweeps across model size, epochs, datasize"). Each
  task is then thin (artifacts only) and references back to group docs.

  When the group is heterogeneous (sibling tasks unrelated), skip
  group/diagram/ and put diagram/ at task level instead.

  Authored via /diagram-ascii. Bundled via /diagram-ascii-canvas:
    bin/txt-to-canvas.py {group}/diagram/ --out {group}/diagram/group.excalidraw

---

Task-level diagram/  (operational detail)
==========================================

  tasks/{G}{GN}_{group}/{NN}_{task}/diagram/
  +-- 01-overview.txt     what / why / inputs / outputs (replaces task README)
  +-- 02-design.txt       approach: model arch / algorithm / experiment setup
  +-- 03-runs.txt         | Run | Variant | Result Dir | Status | Notes |
  +-- 04-progress.txt     dated progress log (newest entry on top, append-only)
  +-- task.excalidraw     bundle (built by txt-to-canvas)

  01-overview.txt — four blocks, 1-3 lines each: What / Why / Inputs / Outputs.

  02-design.txt — approach detail (free-form). For model-training tasks,
  include an ASCII forward-pass diagram + architecture-sweep table.

  03-runs.txt — runs table: | Run | Variant | Result Dir | Status | Notes |
    Status values: planned | wip | done | failed | deprecated.

  04-progress.txt — dated log, newest on top, append-only.
    Format: `260426 — added run_5m; OOM at batch 64, downsized to 32`

  Authored via /diagram-ascii. Bundled via /diagram-ascii-canvas:
    bin/txt-to-canvas.py {task}/diagram/ --out {task}/diagram/task.excalidraw

  Refresh whenever 03-runs or 04-progress changes meaningfully (e.g.,
  after a run completes or a milestone is hit). Stale canvases are
  flagged by /haipipe-project review.

---

Run Script Templates
=====================

  Two templates, picked by notebooks/ build mode (see notebooks/ rules).

  Template A — direct .py + tee log (nbconvert mode / no notebooks/):

    #!/bin/bash
    TASK_DIR="$(cd "$(dirname "$0")/.." && pwd)"
    RUN_NAME="$(basename "$0" .sh)"
    RESULT_DIR="${TASK_DIR}/results/${RUN_NAME}"
    mkdir -p "${RESULT_DIR}"
    exec > >(tee "${RESULT_DIR}/0-${RUN_NAME}.log") 2>&1
    # ... source env, call <task>.py with matching config

  Template B — papermill (notebooks/ papermill mode):
    Same TASK_DIR/RUN_NAME header, but:
      - NO `exec > >(tee log)` — recorded notebook IS the log
      - `export TASK_DIR` before papermill (notebook kernel inherits it)
      - Step 1: `convert_to_notebooks.py <task>.py -o <task>.ipynb`
      - Step 2: `papermill <task>.ipynb notebooks/${RUN_NAME}.ipynb -p ...`
    results/${RUN_NAME}/ still produced by the .py for light artifacts.

---

Relationship: runs/ <-> results/ <-> notebooks/ <-> sbatch/
===========================================================

  train_num_nb.py ──────────────────────> train_num_nb.ipynb  (template, task root)
                                          (rebuilt by every run via convert_to_notebooks.py)

  configs/B5_model_cgm_num_1m.yaml  ──┐
  runs/run_1m.sh ────────────────────┼──> notebooks/run_1m.ipynb        (runtime record)
                                     │    results/run_1m/              (light artifacts)
                                     │      ├─ 0-run_1m.log (nbconvert mode only)
                                     │      └─ metrics.json (optional)
  configs/B5_model_cgm_num_5m.yaml  ──┐
  runs/run_5m.sh ────────────────────┼──> notebooks/run_5m.ipynb
                                     │    results/run_5m/
                                     │
  sbatch/gpu0.sh ────────────────────┴──> calls runs/run_1m.sh, runs/run_5m.sh, ...
                                          (one sbatch coordinates one or several runs)

  - configs/ holds the YAML for each run (config naming is freestyle)
  - runs/ holds one script per config (atomic, self-contained)
  - notebooks/ holds one template <stem>.ipynb per task .py, plus one
    <run_name>.ipynb per runs/<run_name>.sh (runtime record with outputs)
  - results/ holds one dir per run (name-paired with runs/, NOT configs/)
  - sbatch/ coordinates one or several runs (orchestration only)
  - One task = one .py template, multiple configs, multiple runs, multiple
    runtime-recorded notebooks. sbatch/ scripts orchestrate which runs go
    on which GPU.

---

Paper-level diagram/  (manuscript plan)
=========================================

  paper/Paper-{Name}-{venue}/diagram/
  +-- 01-overview.txt        sections + main claims
  +-- 02-figure-plan.txt     what each figure shows + status
  +-- 03-rebuttal.txt        reviewer-response sketches (when applicable)
  +-- paper.excalidraw       bundle

  01-overview.txt   manuscript structure: sections, headline claims per section
  02-figure-plan.txt | Fig | Title | Source task | Status | (planned/draft/final)
  03-rebuttal.txt   per-reviewer comment + planned response sketch (during rebuttal)

  The paper subfolder is often a git submodule; its diagram/ lives
  inside the submodule and is committed to the paper repo.

  Authored via /diagram-ascii. Bundled via /diagram-ascii-canvas.

---

Auto-Example Rule
==================

Every Track A stub gets a paired example task in tasks/ (group D by default).

  Track A stub                              Track B paired task
  --------------------                       -------------------------
  code-dev/1-PIPELINE/.../build_*.py    ->  tasks/D_demo/D{N}_test_*/
  code/hainn/algo/{family}/*.py         ->  tasks/D_demo/D{N}_test_{name}/
  code/hainn/tuner/{family}/*.py
  code/hainn/instance/{family}/*.py

The paired task contains the standard task layout including diagram/.
Status tracked in:
  - {PROJECT}/diagram/03-exploration.txt  (under "active" or "backlog")
  - {task}/diagram/03-runs.txt            (Status = "stub" until implemented)

---

_WorkSpace Paths
=================

Declared in env.sh, read by setup_workspace() in code/haipipe/base.py.
NEVER inside the project folder.

---

Review Checklist
=================

Project structure:
  [ ] Name matches Proj{Series}-{Category}-{Num}-{Name}
  [ ] tasks/ + diagram/ exist at project root
  [ ] No top-level configs/, results/, README.md, docs/, cc-archive/, _old/
  [ ] Tasks live under tasks/{G}{NN}_{group}/{NN}_{name}/
  [ ] {PROJECT}/diagram/ has 01-story, 02-boundary, 03-exploration,
      project.excalidraw (canvas fresher than .txt sources)

Per group:
  [ ] No README.md
  [ ] Group letter G matches its tasks' series
  [ ] sbatch/ exists for cross-task orchestration (env.sh + batchers)
  [ ] If cohesive: {group}/diagram/ has 01-overview, 02-tasks,
      03-progress, 04-design, group.excalidraw

Per task (standard):
  [ ] >=1 *.py at task root, no README.md
  [ ] Either group/diagram/ or task/diagram/ covers this task
  [ ] configs/ has own YAMLs (no symlinks)
  [ ] runs/ scripts atomic (1 config = 1 script, no loops, no CLI args)
  [ ] runs/<run>.sh ↔ results/<run>/ name pairing holds
  [ ] sbatch/ scripts call runs/*.sh, never *.py
  [ ] No heavy files in results/ (heavy → _WorkSpace/)
  [ ] notebooks/ has <run>.ipynb per runs/<run>.sh; template
      <stem>.ipynb sits at task root next to <stem>.py
  [ ] runs/*.sh consistently use Template A (tee log) OR Template B
      (papermill); never mix on same task
  [ ] Papermill-mode .py: # %% [parameters] cell as first cell;
      auto-detects TASK_DIR via __file__ → __vsc_ipynb_file__
      → os.environ['TASK_DIR']

Per task (skill-runner exemption):
  [ ] No *.py / data/ required
  [ ] runs/<slug>.sh execs `claude` (interactive, not `-p`); no tee header;
      passes --session-id $(uuidgen) and copies session.jsonl to results/
  [ ] If ≥2 questions: configs/<slug>.yaml + runs/_run.sh shared launcher
      + runs/ask_<slug>.sh one-line wrappers (`_`-prefix = shared/template)

Paper (if applicable):
  [ ] paper/Paper-*/diagram/ has 01-overview, 02-figure-plan
  [ ] paper.excalidraw fresher than .txt sources
