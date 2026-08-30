task: Block and Job Folder Structure
=============================================

Renamed onto Block / Job / Task / Run on 2026-08-29 (JL; was "Task-Group and
Task-Folder Structure"). The conceptual model, the four-word table, the two
job shapes, and the drift checks live in ref/hierarchy.md; this file is the
concrete folder-by-folder contract.

Read together with the sister refs, which stay authoritative for what they
already cover; where a rule lives in one of them, this file points at it and
does not restate it:

  ref/hierarchy.md               conceptual model: project -> block -> job -> task -> run; 2-digit indexing; RUNNAME spine; two notebooks two roles
  ref/authoring-conventions.md   cross-type code conventions: four sister files (§1), _meta contract (§2), heavy-artifact rule (§3), reproducibility (§4), first-run gate (§5), author scope (§6), notebooks + papermill retention/commit policy (§7)
  ref/run-sh-template.sh         canonical papermill ticket template (shape auto-detect, runtime.yaml snapshot, pre-flight CODE_REVIEW gate, notebook policy)
  ref/databricks-execution.md    Template C: running jobs ON Databricks (dual-mode drivers, widgets, inline exec, _databricks/ bundles)

---

Block Folders
=============

Two-level container: tasks/ -> blocks -> jobs.

  bNN_{block_name}/jNN_{job_name}/

  b, j    the LEVEL letter (b block · j job · t task · r run) — one grammar at every level (JL 260829)
  NN      2-digit index: blocks in pipeline order, jobs sequential within the block
  *_name  snake_case, <noun>_<qualifier>, passes the stranger test (hierarchy.md "Naming")

Index lets ls sort by dependency: A01 (pretraining) < A21 (finetuning) < B01.
Reserve ranges by stage: A01-A09 stage 1, A20-A29 stage 2, etc. Full indexing
rules (2 digits, start at 01, forward-fill on deletion, sub-buckets by tens):
ref/hierarchy.md "Indexing & Naming". Prefer FEW blocks — the letter is the
block's identity; three sibling blocks sharing one letter and holding ~2 jobs
each are one block written three times (hierarchy.md "Level 2: Block").

Examples:
  b01_pretraining_clm/j01_train_clm_num_modelsize/
  b02_finetuning_clm_for_event_reg/j01_ft_clm_num_tar_next1h/
Reference globally as "b01j01" (block.job), or down to one execution as
"b01j01t01r01" (block.job.task.run) — the prefixes joined, read off the path.

Block folder contents (a block is a folder of jobs and nothing else, JL 260829):
  jNN_{name}/     jobs.
  diagram/        docs only, MANDATORY when the block is cohesive (sibling jobs share a narrative). See "Block-level diagram/" below.
  ⛔ no sbatch/, no shared code, no results at block level: what runs lives in a job.

No README.md in block folders. If sibling jobs are unrelated, fall back to
per-job diagrams instead of block/diagram/.

Databricks-native block exceptions (blocks whose stages run ON a cluster,
e.g. A00_rawstore_<cohort>/ — full dialect: ref/databricks-execution.md):
  run_pipeline_*.py(+.ipynb)   orchestrator at the root of the Databricks-imported
                               folder (the platform has no shell, so this stands in
                               for a job's sbatch/).
  _databricks/                 converted .ipynb copies of every stage; what
                               the workspace import executes (.py stays the
                               source of truth).
  README.md                    allowed at block root — the block is imported
                               into Databricks standalone, where diagram/
                               .txt files don't render.

Workflow artifacts (written by /haipipe-workflow when it plans/audits a
block): stage-report.md at block root, workflow/ inside jobs. Legitimate
residents — do not flag them as structure violations; they are generated
records, regenerate rather than hand-edit.

---

Job Naming
===========

  jNN_{job_name}

  j  = the level letter; NN = 2-digit zero-padded index (sequence within the block)
  job_name = snake_case, <noun>_<qualifier>; a stranger must read WHAT THING and
             WHICH ONE off the name alone (hierarchy.md "Naming: the stranger test")

Jobs are numeric-only: they live inside their block folder, so the block
prefix is implicit in the path. Globally referenced as the prefixes joined
(e.g. "b01j01").

---

Job Folder Contents
====================

Two shapes (ref/hierarchy.md "Two job shapes"). NESTED is canonical and what
every NEW job scaffolds; FLAT is the pre-260829 single-task legacy, still
valid, detected by tooling from the ticket's own path.

NESTED (canonical):

  scripts/        CODE. `tNN_*` children are TASKS, one script pipeline
                  each, holding config/ + code (nothing generated); ANY other
                  child is SHARED code — 0-libs/ (Stata), src/ or code/
                  (Python) — holding job-wide libs + the defaults that carry
                  the job's `store:`.
  runs/           TICKETS, mirroring scripts/ task names: runs/<task>/<run>.sh
                  names a config and submits; carries NO parameters and never
                  repeats its own name (derive task + run from $0).
  results/        light summaries, two levels: results/<task>/<run>/
  notebooks/      MANDATORY runtime record, mirrored: notebooks/<task>/<run>.ipynb
                  (papermill injects params and writes the executed result here;
                  it is the canonical "what happened during this run" record).
  QA/             OPTIONAL: the job's READABLE digests — QA/<n>-<slug>.md,
                  <n> = creation order, so `ls QA/` IS the index (no INDEX
                  file). One file per DIRECTION this job has explored:
                  `# Q — <question>` + `## Answer` (with [→ results/<file>]
                  anchors) + `## Caveats` + `## Not-done`. Write-once; a later
                  question ADDS QA/<n+1>-<slug>.md. Written at Report, by THIS
                  layer, for one of three reasons only (a question arrived ·
                  results/ already answered one but no digest existed · a
                  finding was judged worth digesting) — a QA/ mirroring every
                  result is noise. Slug only: no external id, and no vocabulary
                  this layer could not have produced. Contract: fn/qa.md.
  sbatch/         OPTIONAL: submit this job's own DAG, or split this job's
                  runs across GPUs. The only sbatch there is: a batcher that
                  would span jobs says those jobs are one job.
  workflow/       plan/report artifacts (haipipe-workflow).
  diagram/        OPTIONAL: only when this job diverges from the block
                  narrative. If block/diagram/ covers it, skip.

FLAT (legacy): the .py at job root, configs/ + runs/ + results/ + notebooks/
all flat with one shared <run> stem (the four-sister pairing,
authoring-conventions.md §1). A flat job that grows a second pipeline converts
to nested rather than piling a second .py at root.

JOBS DO NOT HAVE A README.md. The doc surface is block/diagram/ (cohesive
blocks) or job/diagram/ (divergent jobs).

Task-folder rules (scripts/tNN_{task_name}/):
  - config/ is ALWAYS a folder, even holding one file; the STEM is the run
    name. Prompts are config: config/prompts/<x>.md beside the config that
    names it, resolved relative to the config file (JL 260830). A config is EXECUTED (or `include`d), not passed as a payload, so it
    is debugged in the same session as the code beside it.
  - a VARIANT is a config, not a new ticket scheme: two runs of one task
    differ only by config stem; two different pipelines are two tasks.
  - zero-pad the index: single digits sort wrong (10_ before 2_).
  - code naming is freestyle: one .py or many, any descriptive name, `# %%`
    cell format for notebook compatibility. In the Stata dialect a task is
    run-pipeline.do + step-*.do (haipipe-task-for-stata owns that contract).

runs/ rules (tickets):
  - ATOMIC: each ticket submits exactly ONE config of ONE task. No loops.
  - NO parameters, no CLI args, no name repetition: the ticket derives task
    and run from its own path and hands off. Parameters live only in config/.
  - no .py in runs/; logic stays in scripts/.
  - orchestration (loops, GPU assignment) belongs in sbatch/, which calls
    tickets, never code directly.

results/ rules:
  - LIGHT only: report.md, metrics.json, small PNGs, .csv, .tex. HEAVY
    (weights, checkpoints, large arrays) goes to _WorkSpace/; authority:
    authoring-conventions.md §3.
  - path-paired with runs/: runs/<task>/<run>.sh <-> results/<task>/<run>/
    (flat: runs/run_1m.sh <-> results/run_1m/).
  - where results/ ROOTS is resolved, never hardcoded: $OUTPUT_ROOT is the
    job in mode ①, <store>/<job path under tasks/> in mode ② — the `store:`
    key is a JOB property declared once (hierarchy.md "Two run modes").

notebooks/ rules:
  - two files, both under notebooks/: the generated template
    notebooks/<task>/_source.ipynb, and the runtime record
    notebooks/<task>/<run>.ipynb paired with runs/<task>/<run>.sh.
    Source of truth is always the .py; both .ipynb are build artifacts.
    Conceptual model: ref/hierarchy.md "Two notebooks, two roles".
  - two build modes:
      papermill   parameterized: one .py + many runs differing in config.
                  The ticket converts via convert_to_notebooks.py then
                  papermill-executes into notebooks/<task>/<run>.ipynb.
      nbconvert   single-render: one .py = one execution, no knobs.
                  `python <stem>.py` then `jupyter nbconvert --execute`.
                  Use for data-audit / insights / exploration.
  - papermill .py conventions: first cell after the docstring is
    `# %% [parameters]`, declaring all tunable knobs with defaults
    (convert_to_notebooks.py tags it for injection). Setup cell auto-detects
    the job dir for portability: __file__ (script) -> __vsc_ipynb_file__
    (VS Code) -> os.environ['TASK_DIR'] (exported by the ticket).
  - retention knob (`_meta.notebook: full | thin | off`) and the
    commit/gitignore policy (default gitignore notebooks/ and _WorkSpace/):
    authoring-conventions.md §7.

sbatch/ rules:
  - ORCHESTRATION: each .sh coordinates one or several tickets; assigns GPU,
    sets CUDA_VISIBLE_DEVICES, loops over runs.
  - sbatch/ scripts call tickets in runs/, NOT scripts/ code directly.
  - one level only: job/sbatch/ (submit the DAG, or GPU-split this job's
    own tickets). A batcher that would span jobs says those jobs are one job.

Drift checks (nested shape — run from the job root; both must print nothing):

  comm -3 <(ls runs/) <(ls scripts/ | grep '^t[0-9][0-9]_')

  comm -3 <(find scripts -path "*/config/*" -type f \
              | sed "s|^scripts/||; s|/config/|/|; s|\.[^./]*$||" | sort) \
          <(find runs -type f | sed "s|^runs/||; s|\.[^./]*$||" | sort)

Left column = a config with no ticket; right column = a ticket with no config.
Verified 260829; details + why flat naming could not be checked:
ref/hierarchy.md "Drift checks".

---

Skill-Runner Jobs (Exemption)
================================

When a job wraps a Claude Code skill instead of a .py, the skill executes the
work and writes its structured outputs elsewhere (wherever that skill's own
contract puts them). The job folder is narrative + launcher.

Exemptions:
  - no *.py, no data/ required.
  - config optional but recommended: one <slug>.yaml per question;
    _defaults.yaml for shared keys.
  - the ticket runs/<slug>.sh is a thin launcher around `claude "/<skill> ..."`:
      * use `claude` (interactive TUI), NOT `claude -p`.
      * pass `--session-id $(uuidgen)`, copy session.jsonl to the run's
        results dir after exit (debug record only; substantive output lives
        wherever the skill writes it).
      * pass `--dangerously-skip-permissions` (config-driven; default true)
        so the skill can run pandas / write files freely.
      * do NOT use `exec > >(tee log)`; it breaks the TUI.
  - two-tier shape recommended for >=2 questions: runs/_run.sh shared launcher
    reads YAML + exec's claude; runs/ask_<slug>.sh one-line wrapper.
    Underscore prefix reserved for shared/template files.
  - results/ holds the session transcript (debug); substantive outputs live
    at the skill's own artifact paths.

---

Block-level diagram/  (cohesive-block narrative)
==================================================

  tasks/bNN_{block}/diagram/
  ├── 01-overview.txt    what this block is, why it exists, narrative binding sibling jobs
  ├── 02-tasks.txt       | Job | What it sweeps | Status |  (one row per sibling job)
  ├── 03-progress.txt    cross-job runs / progress table
  ├── 04-design.txt      shared script logic when jobs share a .py / approach
  └── group.excalidraw   bundle (built by txt-to-canvas)

Use block-level diagram/ when sibling jobs form a coherent story (e.g.
"scaling-law sweeps across model size, epochs, datasize"). Each job is then
thin (artifacts only) and references back to block docs.

When the block is heterogeneous (sibling jobs unrelated), skip block/diagram/
and put diagram/ at job level instead.

Authored via /diagram-ascii. Bundled via /diagram-ascii-canvas:
  bin/txt-to-canvas.py {block}/diagram/ --out {block}/diagram/group.excalidraw

---

Job-level diagram/  (operational detail)
==========================================

  tasks/bNN_{block}/jNN_{job}/diagram/
  ├── 01-overview.txt     what / why / inputs / outputs (replaces job README)
  ├── 02-design.txt       approach: model arch / algorithm / probe setup
  ├── 03-runs.txt         | Run | Variant | Result Dir | Status | Notes |
  ├── 04-progress.txt     dated progress log (newest entry on top, append-only)
  └── task.excalidraw     bundle (built by txt-to-canvas)

01-overview.txt: four blocks, 1-3 lines each: What / Why / Inputs / Outputs.

02-design.txt: approach detail (free-form). For model-training jobs, include
an ASCII forward-pass diagram + architecture-sweep table.

03-runs.txt: runs table | Run | Variant | Result Dir | Status | Notes | with
Status values: planned | wip | done | failed | deprecated. In nested jobs the
Run column is the `<task>/<run>` path.

04-progress.txt: dated log, newest on top, append-only. Format:
`260426: added run_5m; OOM at batch 64, downsized to 32`

Authored via /diagram-ascii. Bundled via /diagram-ascii-canvas:
  bin/txt-to-canvas.py {job}/diagram/ --out {job}/diagram/task.excalidraw

Refresh whenever 03-runs or 04-progress changes meaningfully (e.g. after a
run completes or a milestone is hit).

---

Ticket Templates
=====================

One canonical template: ref/run-sh-template.sh (papermill; auto-detects the
nested vs flat shape from its own path, snapshots runtime.yaml, runs the
pre-flight CODE_REVIEW gate, converts + papermill-executes, applies the
notebook policy, resolves $OUTPUT_ROOT). Copy it rather than writing from
scratch.

nbconvert-mode variant (Template A, no notebooks/): same identity resolution,
then `exec > >(tee "${RESULT_DIR}/0-${RUN_NAME}.log") 2>&1`, source the venv +
env.sh, `python` the script directly, and keep the Files-generated footer:

    # --- Files-generated footer (runs on EXIT, success or failure) ---------
    START_TS=$(date +%s)
    print_run_footer() {
      local rc=$?
      set +e
      echo ""
      echo "============================================================"
      echo "Files generated by ${RUN_NAME} (exit=${rc})"
      echo "============================================================"
      echo "[local ${RESULT_DIR}]"
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

The footer prints on success AND on error (bash EXIT trap), lists local
artifacts + cross-stage writes under _WorkSpace stores, needs GNU find for
`-newermt`, and caps at `head -50`. Papermill mode does NOT use
`exec > >(tee log)` — the recorded notebook IS the log. Never mix the two
modes within one task.

Template C: Databricks execution (no bash runner). When the job runs ON a
Databricks cluster — dual-mode drivers, widget params, inline exec on
policy-locked clusters, `_databricks/` .ipynb bundles, convert-only runs/ —
see ref/databricks-execution.md.

Stata dialect (PowerShell tickets, .do pipelines): haipipe-task-for-stata
owns the whole engine contract, including its ticket template.

---

Relationship: scripts/ <-> runs/ <-> results/ <-> notebooks/
===========================================================

  scripts/01_train_num/train_num.py ────> notebooks/01_train_num/_source.ipynb
                                          (template, rebuilt by every ticket)

  scripts/01_train_num/config/run_1m.yaml ─┐
  runs/01_train_num/run_1m.sh ─────────────┼──> notebooks/01_train_num/run_1m.ipynb
                                           │    results/01_train_num/run_1m/
  scripts/01_train_num/config/run_5m.yaml ─┐
  runs/01_train_num/run_5m.sh ─────────────┼──> notebooks/01_train_num/run_5m.ipynb
                                           │    results/01_train_num/run_5m/
                                           │
  sbatch/gpu0.sh ──────────────────────────┴──> calls runs/01_train_num/run_1m.sh, ...
                                                (one sbatch coordinates one or several tickets)

  - config/ holds the YAML for each run; CONFIG STEM == RUN NAME == TICKET STEM
  - runs/ holds one ticket per config (atomic, parameterless)
  - notebooks/ and results/ repeat the same <task>/<run> path
  - one task = one .py pipeline, multiple configs, multiple runs; sbatch/
    scripts orchestrate which tickets go on which GPU.
  - flat legacy jobs: drop the <task>/ segment everywhere above
    (the four-sister <NAME> token, authoring-conventions.md §1).

---

Auto-Example Rule
==================

Every Track A stub gets a paired example task in tasks/ (block D by default).
Track A side of the rule: project/haipipe-project/ref/code-structure.md.

  Track A stub                              Track B paired job
  --------------------                      -------------------------
  code/hainn/algo/{family}/*.py         ->  tasks/D_demo/D{N}_test_{name}/
  code/hainn/tuner/{family}/*.py
  code/hainn/instance/{family}/*.py

Fn builders (build_*.py) need no demo pairing: they live in the project's
NN_<stage>_fn_develop_<cohort>/ jobs, which are already runnable jobs with
the standard layout. (Legacy workspaces keeping builders in
code-dev/1-PIPELINE/ still pair them with tasks/D_demo/D{N}_test_*/.)

The paired job contains the standard layout including diagram/. Status
tracked in:
  - {job}/diagram/03-runs.txt             (Status = "stub" until implemented)
