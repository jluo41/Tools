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

  No top-level: config/, results/, README.md, docs/, cc-archive/, _old/

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
  +-- project.excalidraw    bundle of the .txt sources (built by txt-to-canvas)

  PROJECT-LEVEL DIAGRAM IS HIGH-LEVEL ONLY.

  It captures the research narrative — story, boundary, exploration
  directions. It is NOT an operational dashboard:

    DOES belong here          DOES NOT belong here
    --------------------       ---------------------------
    why we are doing this      per-task status table  (-> {task}/diagram/03-runs)
    in/out scope               cross-task file dependencies (-> implicit in tasks)
    open questions             run-level metrics  (-> {task}/diagram/03-runs)
    directions tried/ruled-out daily progress log  (-> {task}/diagram/04-progress)

  Authored via /diagram-ascii. Bundled via /diagram-ascii-canvas:
    bin/txt-to-canvas.py examples/{PROJECT_ID}/diagram/ \
      --out examples/{PROJECT_ID}/diagram/project.excalidraw

  Refresh on substantive change to story / scope / exploration. Otherwise
  stable — most weeks the project diagram does not change.

---

Group Folders
=============

  Two-level hierarchy: tasks/ -> group folders -> task folders.

  {G}_{group_name}/            <- default form (one letter + name)
  {G}_{S}_{group_name}/        <- sub-ordered form (optional, when a group
                                  splits into ordered stages)

  G = uppercase letter (matches its tasks' prefix)
  S = single digit, optional, sort key when several groups share G
  group_name = snake_case descriptor

  Sub-ordered form — when to use:
    When multiple groups share the same G (e.g. "A = training") but one
    depends on another (e.g. finetuning depends on pretraining), use the
    {G}_{S}_ form so `ls` sorts them in dependency order:

      A_1_pretraining_clm/           <- stage 1: produces backbones
      A_2_finetuning_clm_for_clf/    <- stage 2: consumes backbones from A_1_*

    Without the digit, "A_finetuning_*" would sort before "A_pretraining_*"
    because 'f' < 'p', which inverts the logical dependency. One digit
    is enough; don't nest further. Task-folder prefix is still {G}{N}_
    (no sub-digit), so "A_1_pretraining_clm/A1_train_clm_num_modelsize/"
    has group "A_1_" and sub-task "A1_" — distinct by separator.

  Group folder contents:
    sbatch/          OPTIONAL — cross-task SLURM scripts within this group
    {G}{N}_{name}/   task folders (each owns its own config/, diagram/)

  GROUP FOLDERS DO NOT HAVE A README.md.

  Group-level documentation is redundant: the project-level story
  (in {PROJECT}/diagram/) describes what each group represents at a
  high level, and per-task diagrams describe operational detail. Group
  is purely an organizational layer for sorting + sbatch scope.

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
  config/         YAML configs (each task owns its own, no sharing/symlinks)
  runs/           Atomic run scripts (one config = one script, no CLI args)
  results/        Light summaries (name-paired with runs/)
  sbatch/         OPTIONAL: orchestration scripts (call runs/*.sh, assign GPUs)
  diagram/        MANDATORY: task-level operational detail (overview, design, runs, progress)

  TASKS DO NOT HAVE A README.md. The diagram/ folder is the doc surface.

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

  sbatch/ rules:
    - ORCHESTRATION: each .sh batches multiple runs/*.sh together.
    - Assigns GPU, sets CUDA_VISIBLE_DEVICES, loops over runs.
    - sbatch/ scripts call runs/*.sh, NOT *.py directly.
    - Can exist at task level AND at group level.

---

Skill-Runner Tasks (Exemption)
================================

  Some tasks are thin wrappers around a Claude Code skill (e.g., /dikw)
  rather than around a Python script. The executor IS the skill; the
  task folder's job is narrative + invocation pointers, not code.

  When does a task qualify as a skill-runner task?
    - A Claude Code skill (e.g., /dikw, /dikw-batch) executes the work.
    - The upstream artifacts already live in _WorkSpace/ (or any other
      canonical location), so the task does not need to host data/.
    - The skill writes its own structured outputs (e.g.,
      _agent_dikw_space/snapshot-<name>/sessions/NN_<slug>/) somewhere
      OUTSIDE the task folder — the task only references those paths.

  Exemptions from the standard task-folder rules:

    - NO *.py required.  The executor is the skill, not Python.
    - NO data/ required. Upstream artifacts stay where they live.
    - config/ becomes OPTIONAL but RECOMMENDED. With ≥2 questions
      against the same skill, use config/*.yaml — one per question —
      and a shared runs/_run.sh launcher. With a single one-off
      question, hardcoding inside runs/ask_<slug>.sh is acceptable.
      See "config/ rules (skill-runner mode)" and "runs/ rules
      (skill-runner mode)" below.
    - runs/ becomes a launcher folder, not a batch-execution folder.
    - results/ holds the raw session transcript only (debug record),
      NOT the substantive outputs. Substantive outputs live where the
      skill writes them (per skill's own SKILL.md).

  config/ rules (skill-runner mode):
    - One YAML per question: config/<slug>.yaml.
    - Optional config/_defaults.yaml holds shared defaults (dataset,
      snapshot name, symlink, persona, attendance).
      Per-question YAMLs override defaults by setting the same key.
    - YAMLs encode skill flags + question text — NOT task-script
      flags, since the executor is the skill itself.
    - Required keys (per merged YAML): the skill's own required
      arguments (e.g. for /dikw: dataset, snapshot_name, question).
    - Underscore-prefixed names (_defaults.yaml, _common.yaml) are
      reserved for shared/template files — not picked up as questions
      by the launcher.

  runs/ rules (skill-runner mode):
    - Pure launchers — thin shells that exec `claude "/<skill> ..."`.
      Do NOT use the standard `exec > >(tee log)` logging header —
      it pipes stdout and breaks the interactive Claude TUI.
    - Use `claude` (interactive TUI), not `claude -p` (headless).
      Skills like /dikw expect a human at gates by default.
    - Pass `--session-id $(uuidgen)` so the resulting session.jsonl
      can be located deterministically and copied to results/.
    - Pass `--dangerously-skip-permissions` (config-driven, default
      true) so the skill can run pandas / write files / edit YAML
      state without pausing at every Bash/Write/Edit. Make this a
      YAML key (`dangerously_skip_permissions`) so individual
      sensitive questions can revoke it.
    - After Claude exits, copy the session transcript to
      results/<run_name>/session.jsonl as a debug record.
    - Two-tier shape (recommended when config/ is used):
        * runs/_run.sh        shared launcher, takes <slug> arg, reads
                               config/_defaults.yaml + config/<slug>.yaml,
                               assembles flags, exec's claude.
        * runs/ask_<slug>.sh  one-line wrapper:
                               `exec "$(dirname "$0")/_run.sh" <slug>`
      Adding a new question = config/<slug>.yaml + 1-line ask wrapper.
    - Underscore-prefixed scripts (_run.sh, _common.sh) are reserved
      for shared launcher logic — not user-facing entrypoints.

  Skill-runner launcher template (two-tier, config-driven):

    # runs/ask_engagement_funnel.sh   ← one line per question
    #!/bin/bash
    exec "$(dirname "$0")/_run.sh" engagement_funnel

    # runs/_run.sh   ← shared, parses YAML and exec's claude
    #!/bin/bash
    set -u
    SLUG="$1"
    TASK_DIR="$(cd "$(dirname "$0")/.." && pwd)"
    REPO_ROOT="$(cd "${TASK_DIR}" && git rev-parse --show-toplevel)"
    RESULT_DIR="${TASK_DIR}/results/ask_${SLUG}"
    mkdir -p "${RESULT_DIR}"

    eval "$("${REPO_ROOT}/.venv/bin/python3" - \
        "${TASK_DIR}/config/_defaults.yaml" \
        "${TASK_DIR}/config/${SLUG}.yaml" <<'PYEOF'
    import sys, shlex, yaml
    d = yaml.safe_load(open(sys.argv[1])) or {}
    o = yaml.safe_load(open(sys.argv[2])) or {}
    m = {**d, **o}
    for k, v in m.items():
        s = "true" if v is True else "false" if v is False else "" if v is None else str(v)
        print(f"CFG_{k.upper()}={shlex.quote(s)}")
    PYEOF
    )"

    DATASET_DIR="${REPO_ROOT}/_WorkSpace/.../${CFG_DATASET}"
    SESSION_ID=$(uuidgen | tr '[:upper:]' '[:lower:]')
    PROJECT_DIR="$HOME/.claude/projects/$(echo "${REPO_ROOT}" | sed 's|/|-|g')"

    CLAUDE_FLAGS="--session-id $SESSION_ID"
    [ "$CFG_DANGEROUSLY_SKIP_PERMISSIONS" = "true" ] && \
        CLAUDE_FLAGS="$CLAUDE_FLAGS --dangerously-skip-permissions"

    claude $CLAUDE_FLAGS \
           "/dikw $DATASET_DIR --snapshot-name $CFG_SNAPSHOT_NAME \
            --symlink \"$CFG_QUESTION\""

    # Copy transcript after Claude exits
    if [ -f "${PROJECT_DIR}/${SESSION_ID}.jsonl" ]; then
        cp "${PROJECT_DIR}/${SESSION_ID}.jsonl" "${RESULT_DIR}/session.jsonl"
    fi

  Reading the audit trail (two layers):
    - Layer 1: structured artifacts written by the skill itself
        (e.g., for /dikw: gates/, plan/, output/final_output.md under
         _agent_dikw_space/snapshot-<name>/sessions/NN_<slug>/).
        This is the primary record of reasoning.
    - Layer 2: raw Claude transcript at results/<run_name>/session.jsonl.
        Verbose; useful for debugging skill behavior.

  Where this applies:
    - DIKW analysis tasks (e.g., examples/{PROJECT}/tasks/B_explore/B*/).
    - Any future "thin task wrapping a skill" pattern.

---

Task-level diagram/  (operational detail)
==========================================

  tasks/{G}_{group}/{G}{N}_{task}/diagram/
  +-- 01-overview.txt     what / why / inputs / outputs (replaces task README)
  +-- 02-design.txt       approach: model arch / algorithm / experiment setup
  +-- 03-runs.txt         | Run | Variant | Result Dir | Status | Notes |
  +-- 04-progress.txt     dated progress log (newest entry on top, append-only)
  +-- task.excalidraw     bundle (built by txt-to-canvas)

  01-overview.txt — four short blocks, each 1-3 lines:
    1. What     one-line purpose
    2. Why      paper section / rebuttal point / research question it serves
    3. Inputs   data paths or upstream tasks it reads from
    4. Outputs  result files or downstream tasks it feeds

  02-design.txt — approach in detail. Free-form, but for STAGE 5 (model
  training) tasks it MUST include an ASCII diagram of the forward pass
  plus an architecture sweep table when multiple sizes are trained:

    Architecture
    ============
      Input: [x_1, ..., x_L]   shape [B, L]
              |
        embed Linear(1 -> H)
              |
        Transformer (causal, N layers)
              |
        head Linear(H -> K)
              |
        Output [B, L, K]   loss = mean MSE over K horizons

    Architecture Sweep
      Size  | Hidden | Layers | Heads | FFN  | LR    | Batch
      ------+--------+--------+-------+------+-------+------
      1m    |    128 |      4 |     2 |  512 | 8e-4  |   32
      100m  |    768 |     11 |    12 | 3072 | 4e-4  |   64

  03-runs.txt — runs table:
    | Run        | Variant     | Result Dir       | Status | Notes |
    | run_1m     | 128h x 4l   | results/run_1m   | done   | OK    |
    | run_5m     | 256h x 6l   | results/run_5m   | done   |       |
    | run_100m   | 768h x 11l  | results/run_100m | wip    | OOM   |
    Status: planned | wip | done | failed | deprecated

  04-progress.txt — dated entries (newest on top, append-only):
    260426 — added run_5m; hit OOM at batch 64, downsized to 32, OK
    260425 — scaffolded task, smoke-tested run_1m on small split
    260424 — picked task scope, blocked by A2 alignment

  Authored via /diagram-ascii. Bundled via /diagram-ascii-canvas:
    bin/txt-to-canvas.py {task}/diagram/ --out {task}/diagram/task.excalidraw

  Refresh whenever 03-runs or 04-progress changes meaningfully (e.g.,
  after a run completes or a milestone is hit). Stale canvases are
  flagged by /haipipe-project review.

---

Run Script Logging Header
==========================

  Every runs/*.sh script starts with this standard header:

    #!/bin/bash
    TASK_DIR="$(cd "$(dirname "$0")/.." && pwd)"
    RUN_NAME="$(basename "$0" .sh)"
    RESULT_DIR="${TASK_DIR}/results/${RUN_NAME}"
    mkdir -p "${RESULT_DIR}"
    exec > >(tee "${RESULT_DIR}/0-${RUN_NAME}.log") 2>&1

  This ensures:
    - results/{RUN_NAME}/ directory created automatically
    - All stdout + stderr captured to results/{RUN_NAME}/0-{RUN_NAME}.log
    - The 0- prefix sorts the log to the top of `ls`
    - Output still prints to terminal
    - Works regardless of invocation (direct, tmux, sbatch)

  After the header, the script sources env, sets config path, and
  calls the task's *.py file with the matching config from config/.

---

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
                                         (many:1 — one sbatch calls many runs)

  - config/ holds the YAML for each run (config naming is freestyle)
  - runs/ holds one script per config (atomic, self-contained)
  - results/ holds one dir per run (name-paired with runs/, NOT config/)
  - sbatch/ groups runs by GPU or batch (orchestration only)
  - The run script hardcodes the path to its config YAML inside

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

Structure:
  [ ] Name matches Proj{Series}-{Category}-{Num}-{Name}
  [ ] tasks/ exists
  [ ] diagram/ exists at project root
  [ ] No top-level config/, results/, README.md, docs/, cc-archive/, _old/
  [ ] Tasks live under tasks/{G}_{group}/{G}{N}_{name}/

Project diagram (mandatory):
  [ ] {PROJECT}/diagram/01-story.txt exists and is non-trivial
  [ ] {PROJECT}/diagram/02-boundary.txt exists
  [ ] {PROJECT}/diagram/03-exploration.txt exists
  [ ] {PROJECT}/diagram/project.excalidraw exists
  [ ] project.excalidraw is fresher than the oldest .txt source
       (else canvas is stale; re-bundle)

Per group:
  [ ] No README.md in group folder
  [ ] Group letter G matches its tasks' prefix
  [ ] If sub-ordered: digit reflects actual dependency order

Per task (standard):
  [ ] At least one *.py exists in the task folder
  [ ] No README.md in task folder
  [ ] {task}/diagram/ exists with: 01-overview, 02-design, 03-runs, 04-progress
  [ ] {task}/diagram/task.excalidraw exists and is fresher than .txt sources
  [ ] config/ exists with own YAML (no symlinks)
  [ ] runs/ scripts atomic (1 config = 1 script, no loops)
  [ ] runs/foo.sh ↔ results/foo/ name pairing holds
  [ ] sbatch/ scripts call runs/*.sh, NOT *.py directly
  [ ] If no runs/: results/ has flat files or default/ subfolder
  [ ] No heavy files in results/ (heavy goes to _WorkSpace/)
  [ ] Every runs/*.sh starts with the standard logging header

Per task (skill-runner exemption — see "Skill-Runner Tasks" above):
  Replace the standard *.py / data/ / logging-header rules with:
  [ ] No *.py required (executor is a Claude Code skill)
  [ ] No data/ required (upstream lives in _WorkSpace/ or other canonical location)
  [ ] config/ optional but recommended for ≥2 questions:
        - one config/<slug>.yaml per question
        - optional config/_defaults.yaml for shared settings
        - YAMLs encode skill flags + question text (not task-script flags)
  [ ] runs/ask_<slug>.sh launchers exec `claude` (interactive, not `claude -p`)
  [ ] runs/*.sh do NOT use the standard tee logging header (would break TUI)
  [ ] runs/*.sh pass --session-id $(uuidgen) and copy session.jsonl to results/
  [ ] runs/*.sh pass --dangerously-skip-permissions (config-driven; default
      true; per-question YAML override allowed) so the skill can run
      pandas / write artifacts / edit state files without per-tool prompts
  [ ] If config/ used: runs/_run.sh is the shared launcher and ask_*.sh are
      one-line wrappers — `exec "$(dirname "$0")/_run.sh" <slug>`
  [ ] Underscore-prefixed names in config/ and runs/ (e.g. _defaults.yaml,
      _run.sh) are reserved for shared/template files — not user-facing
      questions or entrypoints
  [ ] diagram/ still mandatory (01-overview, 02-design, 03-runs, 04-progress, .excalidraw)
  [ ] 01-overview.txt Inputs/Outputs reference the skill's actual artifact paths

Paper (if applicable):
  [ ] paper/Paper-*/diagram/ exists with 01-overview, 02-figure-plan
  [ ] paper.excalidraw fresher than .txt sources
