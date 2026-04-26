fn-new: Scaffold Project, Group, or Task
==========================================

Three scopes, one command:

  /haipipe-project new project   -> full project from scratch
  /haipipe-project new group     -> add group to existing project
  /haipipe-project new task      -> add task to existing group

If scope is omitted: ask which one the user wants.

The doc surface is diagram/, NOT README.md. This scaffolder DELEGATES
diagram authoring to /diagram-ascii (.txt sources) and /diagram-ascii-canvas
(bundling). The scaffolder itself never writes diagram .txt content
inline — it calls the skill so the diagram-ascii conventions stay in one
place.

===================================================================
Scope 1: New Project
===================================================================

Creates a full project: project folder + first group + first task.
Output shape (mandatory):

  examples/{PROJECT_ID}/
  ├── tasks/
  │   └── {first group + first task, see Scopes 2 + 3}
  ├── diagram/             <- project-level story (high-level)
  │   ├── 01-story.txt
  │   ├── 02-boundary.txt
  │   ├── 03-exploration.txt
  │   └── project.excalidraw
  └── (paper/ optional)

NO top-level: README.md, docs/, cc-archive/, _old/, config/, results/.

---

Step 1P: Collect Project Metadata
------------------------------------

Ask in two blocks. Wait for answers before proceeding.

**Block 1 — Identity**

  Q1. Series letter? (A=misc, B=benchmarking, C=models, D=EHR, or new)
  Q2. Category? (Bench / Model / EHR / Pretrain / custom)
  Q3. Sequential Num? (check existing examples/ to avoid collision)
  Q4. Project Name? (CamelCase, e.g. FairGlucose)

  -> Compose: PROJECT_ID = Proj{Series}-{Category}-{Num}-{Name}
  -> Confirm with user.

**Block 2 — Scope**

  Q5. Which pipeline stages? (1=Source, 2=Record, 3=Case, 4=AIData, 5=Model, 6=Endpoint)
  Q6. Dataset(s)? (for config YAML naming)
  Q7. Need a NEW pipeline function? (YES -> Track A stubs for pipeline)
  Q8. Need a NEW ML model architecture? (YES -> Track A stubs for hainn/)
  Q9. If new model: family and name?
      (family: tsforecast / mlpredictor / tefm / tediffusion / bandit)

**Block 3 — Project story (for diagram/)**

  S1. Research question (one sentence)
  S2. Why does this matter? (one sentence; expected impact / venue)
  S3. In-scope (3-5 bullets)
  S4. Out-of-scope (2-3 bullets)
  S5. Initial exploration directions (2-4 bullets)

  These five answers seed the project-level diagram. They are HIGH LEVEL —
  the Q for "story", not for "what tasks will exist". Tasks are answered
  by Scope 2/3 below.

Display summary and wait for explicit YES before creating anything.

---

Step 2P: Create Project Skeleton
------------------------------------

Create the mandatory shape:

  examples/{PROJECT_ID}/tasks/
  examples/{PROJECT_ID}/diagram/

Optionally created (only if user requests):

  examples/{PROJECT_ID}/paper/Paper-{Name}-{venue}/

DO NOT create: README.md (any level), docs/, cc-archive/, _old/.

---

Step 3P: Author Project-level diagram/
----------------------------------------

This is HIGH LEVEL ONLY — story, boundary, exploration. NOT operational state.

For each diagram file, call /diagram-ascii with a focused brief:

  Skill("diagram-ascii", args=
    "Write the project story diagram for {PROJECT_ID}. Save to
     examples/{PROJECT_ID}/diagram/01-story.txt.

     Include three sections separated by ─§ markers:

       ─§ Research question ──────
         {S1 answer}

       ─§ Why it matters ─────────
         {S2 answer + expected venue}

       ─§ At a glance ─────────────
         {1-line motivation, audience, key claim}

     Emoji-rich. ASCII boxes for any flow."
  )

  Skill("diagram-ascii", args=
    "Write the project boundary diagram for {PROJECT_ID}. Save to
     examples/{PROJECT_ID}/diagram/02-boundary.txt.

     Sections:
       ─§ In scope ──────────────  {S3 bullets}
       ─§ Out of scope ──────────  {S4 bullets}
       ─§ Definitions ───────────  (key terms used in this project)
       ─§ Assumptions ───────────  (what we're taking as given)

     Use a 2-column table for in-vs-out where useful."
  )

  Skill("diagram-ascii", args=
    "Write the project exploration diagram for {PROJECT_ID}. Save to
     examples/{PROJECT_ID}/diagram/03-exploration.txt.

     Sections:
       ─§ Active ────────────────  (what we're doing right now)
       ─§ Backlog ───────────────  (planned next)
       ─§ Tried ─────────────────  (done; what we learned)
       ─§ Ruled out ─────────────  (with one-line reason)

     Seed with: {S5 answers} (all in 'Active' or 'Backlog')."
  )

After all three .txt files exist, bundle:

  Skill("diagram-ascii-canvas", args=
    "Bundle examples/{PROJECT_ID}/diagram/ into
     examples/{PROJECT_ID}/diagram/project.excalidraw"
  )

---

Step 4P: Create First Group + First Task
------------------------------------------

Proceed to Scope 2 (group) then Scope 3 (task) using metadata collected
in Block 1+2. No need to re-ask identity questions.

---

Step 5P: Track A — Code Stubs (if needed)
--------------------------------------------

Skip if both Q7 and Q8 answered NO.

**A1 — Pipeline Fn stubs (Q7 = YES)**

For each stage needing a new Fn, create:
  (a) Builder stub: code-dev/1-PIPELINE/{N}-*-WorkSpace/build_{dataset}_{layer}.py
  (b) Paired example task: tasks/D_demo/D{N}_test_{dataset}_stage{N}_fn/
      Layout follows Scope 3 (including diagram/, NO README.md).

Before creating: check code/INDEX.md for existing Fn at same stage+dataset.
  Match found -> ask user: "Existing Fn {name} found. Reuse instead?"
  No match -> create stub, add row to code/INDEX.md.

**A2 — ML model stubs (Q8 = YES)**

Create stubs:
  code/hainn/algo/{family}/algorithm_{name}.py
  code/hainn/tuner/{family}/tuner_{name}.py
  code/hainn/instance/{family}/instance_{name}.py
  code/hainn/instance/{family}/configuration_{name}.py

Before creating: check code/INDEX.md for existing model in same family+dataset.

Paired example task: tasks/D_demo/D{N}_test_{name}_model/
  Layout follows Scope 3 (including diagram/, NO README.md).

Add row to code/INDEX.md. Update {PROJECT}/diagram/03-exploration.txt
to add a "Backlog" entry: "Implement {name} via /haipipe-nn (currently stub)".

---

Step 6P: Report
-----------------

Print a structured summary:
  - Track B files created (project folder, first group, first task)
  - {PROJECT}/diagram/ files (01-story, 02-boundary, 03-exploration, project.excalidraw)
  - Track A stubs created (if any)
  - Next steps: implement via /haipipe-data or /haipipe-nn; refresh diagrams
    after milestones.


===================================================================
Scope 2: New Group
===================================================================

Adds a group folder to an existing project. Group folders are PURELY
ORGANIZATIONAL — they do NOT contain a README.md.

---

Step 1G: Identify Project
----------------------------

Follow the auto-detection rules in SKILL.md.
Confirm PROJECT_PATH.

---

Step 2G: Collect Group Metadata
---------------------------------

  Q1. Group letter? (show existing groups to avoid collision)
  Q2. Group name? (snake_case, e.g. data, training, evaluation, demo)

  -> Compose: {G}_{group_name}  (e.g. A_data, B_training)
  -> Confirm with user.

---

Step 3G: Create Group Folder
-------------------------------

  tasks/{G}_{group_name}/

That's it. NO README.md. NO group-level diagram. The project-level
diagram describes what each group represents at a high level; the
per-task diagrams cover operational detail.

If the group represents a new exploration direction, append it as a
bullet under "Active" or "Backlog" in {PROJECT}/diagram/03-exploration.txt
via a /diagram-ascii edit + re-bundle. Don't write group-level docs.

---

Step 4G: Optionally Create First Task
----------------------------------------

Ask: "Create the first task inside this group? (yes/no)"
  YES -> proceed to Scope 3 (auto-fill project and group, skip re-asking)
  NO  -> done


===================================================================
Scope 3: New Task
===================================================================

Adds a task folder to an existing group. Task folder DOES include a
diagram/ folder. Task folder does NOT include a README.md.

---

Step 1T: Identify Project and Group
--------------------------------------

Follow the auto-detection rules in SKILL.md for project.
If inside a group folder: auto-detect group too.
Otherwise: list groups and ask which one.
Confirm PROJECT_PATH and GROUP_PATH.

---

Step 2T: Collect Task Metadata
---------------------------------

  Q1. Task number? (show existing tasks in this group to avoid collision)
  Q2. Task name? (snake_case, e.g. cook_data, train_ml, eval_main_table)

  -> Compose: {G}{N}_{task_name}  (e.g. B3_train_neural)
  -> Confirm with user.

  Q3. Which pipeline stages does this task use? (for config YAML skeletons)
      If none: create empty config/ dir.

  Q4. Task one-line purpose?  (seeds 01-overview "What")
  Q5. Why this task?          (seeds 01-overview "Why" — paper section, etc.)
  Q6. Inputs (data + upstream tasks)?
  Q7. Outputs (results + downstream tasks)?

---

Step 3T: Create Task Skeleton
--------------------------------

  tasks/{G}_{group}/{G}{N}_{task_name}/
    {G}{N}_{task_name}.py     (stub with # %% cells)
    config/                    (task's own YAML configs)
    runs/                      (empty)
    results/                   (empty)
    diagram/                   (mandatory, populated next step)

DO NOT create README.md in the task folder.

**Stub .py content:**

  # %% [markdown]
  # # {G}{N}_{task_name}
  # TODO: implement

  # %%
  # Setup
  import os, sys

  # %%
  # Main logic

**Config handling:** Create config/ dir. If pipeline stages known, add YAML
skeletons (see "YAML Skeletons" below). Each task owns its own config files.
No sharing or symlinks between tasks.

---

Step 4T: Author Task-level diagram/
--------------------------------------

Call /diagram-ascii for each .txt file:

  Skill("diagram-ascii", args=
    "Write the task overview diagram for {G}{N}_{task_name}.
     Save to {task_path}/diagram/01-overview.txt.

     Sections (each 1-3 lines):
       ─§ What ────────  {Q4 answer}
       ─§ Why ─────────  {Q5 answer}
       ─§ Inputs ──────  {Q6 answer}
       ─§ Outputs ─────  {Q7 answer}"
  )

  Skill("diagram-ascii", args=
    "Write the task design diagram for {G}{N}_{task_name}.
     Save to {task_path}/diagram/02-design.txt.

     Free-form approach diagram. If this is a Stage 5 (model training)
     task per Q3, MUST include an ASCII forward-pass diagram and an
     architecture sweep table. For other stages, capture the core
     algorithmic idea or experiment design in 1-2 ASCII diagrams.
     Seed with TODO if Q5 implies the design isn't yet decided."
  )

  Skill("diagram-ascii", args=
    "Write the task runs table diagram for {G}{N}_{task_name}.
     Save to {task_path}/diagram/03-runs.txt.

     One section with the runs table:
       | Run | Variant | Result Dir | Status | Notes |

     Seed empty (no runs yet). Status values: planned | wip | done | failed | deprecated."
  )

  Skill("diagram-ascii", args=
    "Write the task progress log for {G}{N}_{task_name}.
     Save to {task_path}/diagram/04-progress.txt.

     Single section, dated entries newest on top, append-only format.
     Seed with one line:
       {YYMMDD} — scaffolded by /haipipe-project new"
  )

After all four .txt files exist, bundle:

  Skill("diagram-ascii-canvas", args=
    "Bundle {task_path}/diagram/ into {task_path}/diagram/task.excalidraw"
  )

---

YAML Skeletons (shared across scopes)
========================================

Created in config/ when pipeline stages are known.

  Stage 1: config/1_source_{dataset}.yaml
  Stage 2: config/2_record_{dataset}.yaml
  Stage 3: config/3_case_{dataset}.yaml
  Stage 4: config/4_aidata_{dataset}.yaml
  Stage 5: config/5_model_{name}.yaml
  Stage 6: config/6_endpoint_{name}.yaml

Stages 1-4 skeleton:

  # Stage {N}: {Layer} Config
  # Project: {PROJECT_ID}
  # Dataset: {dataset}
  # Created: {YYMMDD}
  # TODO: fill in all fields before running haistep-{layer}
  {Layer}FnClass: TODO_{Layer}FnClassName
  {Layer}Args:
    dataset_name: {dataset}
    # TODO: add dataset-specific args

Stage 5 skeleton:

  # Stage 5: Model Config
  # Project: {PROJECT_ID}
  # Model: {name}
  # Created: {YYMMDD}
  ModelInstanceClass: TODO_ModelInstanceClassName
  modelinstance_name: {name}
  modelinstance_version: "@v0001-{name}"
  model_tuner_name: TODO_TunerClassName
  aidata_name: {dataset}
  aidata_version: "@v0001-{dataset}"
  ModelArgs:
    # TODO: model hyperparameters
  TrainingArgs:
    # TODO: training settings
  InferenceArgs:
    # TODO: inference settings
  EvaluationArgs:
    # TODO: evaluation settings

---

MUST NOT
---------

- Do NOT create README.md at any level (project, group, or task).
- Do NOT create docs/, cc-archive/, or _old/.
- Do NOT write diagram .txt content inline — always delegate to /diagram-ascii.
- Do NOT skip the canvas bundle step — .excalidraw must exist before reporting done.
- Do NOT create files outside examples/{PROJECT_ID}/ and code/ without asking.
- Do NOT generate actual implementation in stubs — stubs only.
- Do NOT run pipeline commands during scaffolding.

---

Next Steps
-----------

After scaffolding:
  - Fill TODO placeholders in config/ YAMLs
  - Implement pipeline functions: run /haipipe-data or /haipipe-nn
  - Implement endpoints: run /haipipe-end
  - Refresh task.excalidraw after meaningful run/progress changes
  - To validate structure: run /haipipe-project review
