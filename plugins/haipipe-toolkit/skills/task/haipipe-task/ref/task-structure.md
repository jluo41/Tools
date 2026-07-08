task: Task-Group and Task-Folder Structure
=============================================

Moved from project/haipipe-project/ref/project-structure.md on 2026-07-03. The project skill owns only the top-level project container; the internal structure of tasks/ is owned HERE by the task skill family.

Read together with the sister refs, which stay authoritative for what they already cover; where a rule lives in one of them, this file points at it and does not restate it:

  ref/hierarchy.md               conceptual model: project -> task-group -> task-folder -> run; 2-digit indexing rules; RUNNAME spine; two notebooks two roles
  ref/authoring-conventions.md   cross-type code conventions: four sister files (§1), _meta contract (§2), heavy-artifact rule (§3), reproducibility (§4), first-run gate (§5), author scope (§6), notebooks + papermill retention/commit policy (§7)
  ref/run-sh-template.sh         canonical papermill run.sh template (runtime.yaml snapshot, pre-flight CODE_REVIEW gate, notebook policy)
  ref/databricks-execution.md    Template C: running tasks ON Databricks (dual-mode drivers, widgets, inline exec, _databricks/ bundles)

---

Group Folders
=============

Two-level hierarchy: tasks/ -> group folders -> task folders.

  {G}{NN}_{group_name}/{NN}_{task_name}/

  G       uppercase series letter (e.g. A=training, B=evaluation; letters are project-specific organizational prefixes, not type indicators)
  NN      2-digit index (group: unique within series; task: sequential within group)
  *_name  snake_case descriptor

Index lets ls sort by dependency: A01 (pretraining) < A21 (finetuning) < B01. Reserve ranges by stage: A01-A09 stage 1, A20-A29 stage 2, etc. Full indexing rules (2 digits, start at 01, forward-fill on deletion, sub-buckets by tens): ref/hierarchy.md "Indexing & Naming".

Examples:
  A01_pretraining_clm/01_train_clm_num_modelsize/
  A21_finetuning_clm_for_event_reg/01_ft_clm_num_tar_next1h/
Reference globally as "A01.01".

Group folder contents:
  diagram/        MANDATORY when group is cohesive (siblings share a narrative); covers per-task diagram so tasks stay thin. See "Group-level diagram/" below.
  sbatch/         cross-task orchestration (env.sh + batchers).
  {NN}_{name}/    task folders.

No README.md in group folders. If sibling tasks are unrelated, fall back to per-task diagrams instead of group/diagram/.

Databricks-native group exceptions (groups whose stages run ON a cluster,
e.g. A00_rawstore_<cohort>/ — full dialect: ref/databricks-execution.md):
  run_pipeline_*.py(+.ipynb)   group-root orchestrator (the platform has no
                               shell, so this replaces group/sbatch/).
  _databricks/                 converted .ipynb copies of every stage; what
                               the workspace import executes (.py stays the
                               source of truth).
  README.md                    allowed at group root — the group is imported
                               into Databricks standalone, where diagram/
                               .txt files don't render.

Workflow artifacts (written by /haipipe-workflow when it plans/audits a
group): workflow-report.md at group root, workflow/ inside task folders.
Legitimate residents — do not flag them as structure violations; they are
generated records, regenerate rather than hand-edit.

---

Task Naming
===========

  {NN}_{task_name}

  NN = 2-digit zero-padded index (sequence within the group)
  task_name = snake_case descriptor

Tasks are numeric-only: they live inside their group folder, so the group letter is implicit in the path. Globally referenced as "{group_id}.{task_id}" (e.g. "A01.01").

---

Task Folder Contents
====================

  *.py            one or more Python scripts (freestyle naming, # %% cell format)
  configs/        YAML configs (each task owns its own, no sharing/symlinks)
  runs/           atomic run scripts (one config = one script, no CLI args)
  results/        light summaries (name-paired with runs/)
  <stem>.ipynb    template notebook(s) at TASK ROOT, one per cell-format *.py (e.g. train_num_nb.py <-> train_num_nb.ipynb). Built by convert_to_notebooks.py from the .py source; sits next to its .py so opening the task folder shows source + template side by side.
  notebooks/      MANDATORY: runtime-recording folder. One <run_name>.ipynb per runs/<run_name>.sh; papermill injects params from the runs/*.sh and writes the executed result here. Each run's notebook captures full execution + injected params + outputs; it is the canonical "what happened during this run" record.
  sbatch/         OPTIONAL: task-internal orchestration (e.g. splitting this task's runs across GPUs). Group/sbatch/ is for cross-task orchestration; task/sbatch/ is for within-task. Both levels can coexist.
  diagram/        OPTIONAL: only when this task diverges from the group narrative. If group/diagram/ covers it, skip.

TASKS DO NOT HAVE A README.md. The doc surface is group/diagram/ (cohesive groups) or task/diagram/ (divergent tasks).

Four-sister file naming and the <NAME> token (run_-prefixed snake_case, unique within the task-folder): authoring-conventions.md §1.

Python script rules:
  - naming is freestyle: one file or many, any descriptive name.
  - use # %% cell format for notebook compatibility.

runs/ rules:
  - ATOMIC: each .sh runs exactly ONE config / ONE model. No loops.
  - self-contained: all params hardcoded inside, no CLI args. Run with: bash runs/{name}.sh
  - no .py in runs/; logic stays in *.py files at task root.
  - naming: descriptive of the single run. Examples: run_1m.sh, run_5m_ep0.1.sh, run_hybridA_5m.sh
  - every run script MUST include the standard logging header AND the "Files-generated footer" (see Run Script Templates below). The footer runs on EXIT (success or failure) and prints local results/ contents + cross-stage _WorkSpace writes, keeping every run self-documenting.

results/ rules:
  - LIGHT only: report.md, metrics.json, small PNGs, .csv, .tex. HEAVY (weights, checkpoints, large arrays) goes to _WorkSpace/; authority: authoring-conventions.md §3.
  - name-paired with runs/: runs/run_1m.sh <-> results/run_1m/ (strip .sh from the run name to get the result dir name).
  - without runs/: results/ holds output directly (flat or default/).

notebooks/ rules:
  - two locations: <task>/<stem>.ipynb template paired 1:1 with <stem>.py, and <task>/notebooks/<run>.ipynb runtime record paired 1:1 with runs/<run>.sh. Stems match exactly (no rename). Source of truth is always the .py; both .ipynb files are build artifacts. Conceptual model: ref/hierarchy.md "Two notebooks, two roles".
  - two build modes:
      papermill   parameterized: one .py + many runs differing in hyperparams. runs/<run>.sh converts via convert_to_notebooks.py then papermill-executes into notebooks/<run>.ipynb (stdout/stderr + injected params + figures baked in).
      nbconvert   single-render: one .py = one execution, no knobs. `python <stem>.py` then `jupyter nbconvert --execute`. Use for data-audit / insights / exploration.
  - papermill .py conventions: first cell after the docstring is `# %% [parameters]`, declaring all tunable knobs with defaults (convert_to_notebooks.py tags it for injection). Setup cell auto-detects TASK_DIR for portability: __file__ (script) -> __vsc_ipynb_file__.parent.parent (VS Code) -> os.environ['TASK_DIR'] (exported by run.sh). Papermill-mode run.sh does NOT use `exec > >(tee log)`; the recorded notebook IS the log.
  - retention knob (`_meta.notebook: full | thin | off`) and the commit/gitignore policy (default gitignore notebooks/ and _WorkSpace/): authoring-conventions.md §7.

sbatch/ rules:
  - ORCHESTRATION: each .sh coordinates one or several runs/*.sh; assigns GPU, sets CUDA_VISIBLE_DEVICES, loops over runs.
  - sbatch/ scripts call runs/*.sh, NOT *.py directly.
  - two levels, both valid at different scopes: group/sbatch/ = cross-task orchestration (env.sh + batchers looping over runs from multiple sibling tasks; the common case); task/sbatch/ = task-internal only (GPU split or batch across this task's own runs/*.sh). Task/sbatch/ is fine when orchestration is genuinely task-scoped and would awkwardly leak siblings into a group script.

---

Skill-Runner Tasks (Exemption)
================================

When a task wraps a Claude Code skill instead of a .py, the skill executes the work and writes its structured outputs elsewhere (wherever that skill's own contract puts them). The task folder is narrative + launcher.

Exemptions:
  - no *.py, no data/ required.
  - configs/ optional but recommended: one configs/<slug>.yaml per question; configs/_defaults.yaml for shared keys.
  - runs/<slug>.sh is a thin launcher around `claude "/<skill> ..."`:
      * use `claude` (interactive TUI), NOT `claude -p`.
      * pass `--session-id $(uuidgen)`, copy session.jsonl to results/<run>/ after exit (debug record only; substantive output lives wherever the skill writes it).
      * pass `--dangerously-skip-permissions` (config-driven; default true) so the skill can run pandas / write files freely.
      * do NOT use `exec > >(tee log)`; it breaks the TUI.
  - two-tier shape recommended for >=2 questions: runs/_run.sh shared launcher reads YAML + exec's claude; runs/ask_<slug>.sh one-line wrapper. Underscore prefix reserved for shared/template files.
  - results/ holds the session transcript (debug); substantive outputs live at the skill's own artifact paths.

---

Group-level diagram/  (cohesive-group narrative)
==================================================

  tasks/{G}{NN}_{group}/diagram/
  ├── 01-overview.txt    what this group is, why it exists, narrative binding sibling tasks
  ├── 02-tasks.txt       | Task | What it sweeps | Status |  (one row per sibling task)
  ├── 03-progress.txt    cross-task runs / progress table
  ├── 04-design.txt      shared script logic when tasks share a .py / approach
  └── group.excalidraw   bundle (built by txt-to-canvas)

Use group-level diagram/ when sibling tasks form a coherent story (e.g. "scaling-law sweeps across model size, epochs, datasize"). Each task is then thin (artifacts only) and references back to group docs.

When the group is heterogeneous (sibling tasks unrelated), skip group/diagram/ and put diagram/ at task level instead.

Authored via /diagram-ascii. Bundled via /diagram-ascii-canvas:
  bin/txt-to-canvas.py {group}/diagram/ --out {group}/diagram/group.excalidraw

---

Task-level diagram/  (operational detail)
==========================================

  tasks/{G}{GN}_{group}/{NN}_{task}/diagram/
  ├── 01-overview.txt     what / why / inputs / outputs (replaces task README)
  ├── 02-design.txt       approach: model arch / algorithm / probe setup
  ├── 03-runs.txt         | Run | Variant | Result Dir | Status | Notes |
  ├── 04-progress.txt     dated progress log (newest entry on top, append-only)
  └── task.excalidraw     bundle (built by txt-to-canvas)

01-overview.txt: four blocks, 1-3 lines each: What / Why / Inputs / Outputs.

02-design.txt: approach detail (free-form). For model-training tasks, include an ASCII forward-pass diagram + architecture-sweep table.

03-runs.txt: runs table | Run | Variant | Result Dir | Status | Notes | with Status values: planned | wip | done | failed | deprecated.

04-progress.txt: dated log, newest on top, append-only. Format: `260426: added run_5m; OOM at batch 64, downsized to 32`

Authored via /diagram-ascii. Bundled via /diagram-ascii-canvas:
  bin/txt-to-canvas.py {task}/diagram/ --out {task}/diagram/task.excalidraw

Refresh whenever 03-runs or 04-progress changes meaningfully (e.g. after a run completes or a milestone is hit).

---

Run Script Templates
=====================

Two templates, picked by notebooks/ build mode (see notebooks/ rules above).

Template A: direct .py + tee log (nbconvert mode / no notebooks/):

    #!/bin/bash
    set -e
    TASK_DIR="$(cd "$(dirname "$0")/.." && pwd)"
    RUN_NAME="$(basename "$0" .sh)"
    RESULT_DIR="${TASK_DIR}/results/${RUN_NAME}"
    mkdir -p "${RESULT_DIR}"
    exec > >(tee "${RESULT_DIR}/0-${RUN_NAME}.log") 2>&1

    PROJ_ROOT="$(cd "${TASK_DIR}/../../../../.." && pwd)"
    source "${PROJ_ROOT}/.venv/bin/activate"
    source "${PROJ_ROOT}/env.sh"
    source "${TASK_DIR}/../sbatch/env.sh"

    # --- Files-generated footer (runs on EXIT, success or failure) ---------
    # Prints local results/ contents + _WorkSpace stage writes since start.
    # Keeps the run honest: every run reveals what it produced.
    START_TS=$(date +%s)
    print_run_footer() {
      local rc=$?
      set +e
      echo ""
      echo "============================================================"
      echo "Files generated by ${RUN_NAME} (exit=${rc})"
      echo "============================================================"
      echo "[local results/${RUN_NAME}/]"
      ls -la "${RESULT_DIR}" 2>/dev/null
      echo ""
      echo "[_WorkSpace stage writes since run start]"
      find "${WORKSPACE_PATH:-${PROJ_ROOT}/_WorkSpace}" \
           -maxdepth 6 -type f -newermt "@${START_TS}" \
           \( -path "*/0-RawDataStore/*" -o -path "*/1-SourceStore/*" -o -path "*/2-RecStore/*" \
              -o -path "*/3-CaseStore/*" -o -path "*/4-AIDataStore*/*" \
              -o -path "*/5-ModelInstanceStore*/*" -o -path "*/6-EndpointStore/*" \) \
           -not -path "*/__pycache__/*" -not -name "*.pyc" \
           2>/dev/null | head -50
      echo "============================================================"
    }
    trap print_run_footer EXIT
    # ------------------------------------------------------------------------

    export TASK_DIR
    python "${TASK_DIR}/<task>.py"

The footer:
  - prints on success AND on Python error (via bash EXIT trap).
  - lists local artifacts (results/<run>/) + cross-stage writes under _WorkSpace/{1-SourceStore,2-RecStore,3-CaseStore,4-AIDataStore*,5-ModelInstanceStore*,6-EndpointStore}.
  - `-newermt "@<unix_ts>"` requires GNU find (default on Linux).
  - `head -50` caps spammy output; raise if a real sweep produces more.

Template B: papermill (notebooks/ papermill mode). The canonical template is ref/run-sh-template.sh (runtime.yaml snapshot, pre-flight CODE_REVIEW gate, convert + papermill, notebook policy); copy it rather than writing from scratch. Key deltas from Template A:
  - NO `exec > >(tee log)`; the recorded notebook IS the log.
  - `export TASK_DIR` before papermill (notebook kernel inherits it).
  - Step 1: `convert_to_notebooks.py <task>.py -o <task>.ipynb`; Step 2: `papermill <task>.ipynb notebooks/${RUN_NAME}.ipynb -p ...`
  - results/${RUN_NAME}/ still produced by the .py for light artifacts.

Never mix Template A and Template B within the same task.

Template C: Databricks execution (no bash runner). When the task runs ON a
Databricks cluster — dual-mode drivers, widget params, inline exec on
policy-locked clusters, `_databricks/` .ipynb bundles, convert-only runs/ —
see ref/databricks-execution.md.

---

Relationship: runs/ <-> results/ <-> notebooks/ <-> sbatch/
===========================================================

  train_num_nb.py ──────────────────────> train_num_nb.ipynb  (template, task root)
                                          (rebuilt by every run via convert_to_notebooks.py)

  configs/run_1m.yaml ───────────────┐
  runs/run_1m.sh ────────────────────┼──> notebooks/run_1m.ipynb        (runtime record)
                                     │    results/run_1m/              (light artifacts)
                                     │      ├─ 0-run_1m.log (nbconvert mode only)
                                     │      └─ metrics.json (optional)
  configs/run_5m.yaml ───────────────┐
  runs/run_5m.sh ────────────────────┼──> notebooks/run_5m.ipynb
                                     │    results/run_5m/
                                     │
  sbatch/gpu0.sh ────────────────────┴──> calls runs/run_1m.sh, runs/run_5m.sh, ...
                                          (one sbatch coordinates one or several runs)

  - configs/ holds the YAML for each run; CONFIG FILENAME == RUN FILENAME
    (run-sh-template.sh hard-codes CONFIG="configs/${RUN_NAME}.yaml")
  - runs/ holds one script per config (atomic, self-contained)
  - notebooks/ holds one <run_name>.ipynb per runs/<run_name>.sh (runtime record with outputs); the template <stem>.ipynb sits at task root
  - results/ holds one dir per run (name-paired with runs/ AND configs/ — all four sisters share the <NAME> token)
  - sbatch/ coordinates one or several runs (orchestration only)
  - one task = one .py template, multiple configs, multiple runs, multiple runtime-recorded notebooks; sbatch/ scripts orchestrate which runs go on which GPU.

The shared <NAME> token that binds the four sister files: authoring-conventions.md §1 (also ref/hierarchy.md "RUNNAME").

---

Auto-Example Rule
==================

Every Track A stub gets a paired example task in tasks/ (group D by default). Track A side of the rule: project/haipipe-project/ref/code-structure.md.

  Track A stub                              Track B paired task
  --------------------                      -------------------------
  code/hainn/algo/{family}/*.py         ->  tasks/D_demo/D{N}_test_{name}/
  code/hainn/tuner/{family}/*.py
  code/hainn/instance/{family}/*.py

Fn builders (build_*.py) need no demo pairing: they live in the project's
NN_<stage>_fn_develop_<cohort>/ task folders, which are already runnable
tasks with the standard layout. (Legacy workspaces keeping builders in
code-dev/1-PIPELINE/ still pair them with tasks/D_demo/D{N}_test_*/.)

The paired task contains the standard task layout including diagram/. Status tracked in:
  - {task}/diagram/03-runs.txt            (Status = "stub" until implemented)
