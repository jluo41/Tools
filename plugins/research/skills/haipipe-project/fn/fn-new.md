fn-new: Scaffold Project, Group, or Task
==========================================

Three scopes, one command:

  /haipipe-project new project   -> full project from scratch
  /haipipe-project new group     -> add group to existing project
  /haipipe-project new task      -> add task to existing group

If scope is omitted: ask which one the user wants.

===================================================================
Scope 1: New Project
===================================================================

Creates a full project: project folder + first group + first task.

---

Step 1P: Collect Project Metadata
------------------------------------

Ask in two blocks. Wait for answers before proceeding.

**Block 1 -- Identity**

  Q1. Series letter? (A=misc, B=benchmarking, C=models, D=EHR, or new)
  Q2. Category? (Bench / Model / EHR / Pretrain / custom)
  Q3. Sequential Num? (check existing examples/ to avoid collision)
  Q4. Project Name? (CamelCase, e.g. FairGlucose)

  -> Compose: PROJECT_ID = Proj{Series}-{Category}-{Num}-{Name}
  -> Confirm with user.

**Block 2 -- Scope**

  Q5. Which pipeline stages? (1=Source, 2=Record, 3=Case, 4=AIData, 5=Model, 6=Endpoint)
  Q6. Dataset(s)? (for config YAML naming)
  Q7. Need a NEW pipeline function? (YES -> Track A stubs for pipeline)
  Q8. Need a NEW ML model architecture? (YES -> Track A stubs for hainn/)
  Q9. If new model: family and name?
      (family: tsforecast / mlpredictor / tefm / tediffusion / bandit)

Display summary and wait for explicit YES before creating anything.

---

Step 2P: Create Project Structure
------------------------------------

Create the mandatory structure:

  examples/{PROJECT_ID}/tasks/
  examples/{PROJECT_ID}/tasks/README.md

Optionally created (only if user requests):

  examples/{PROJECT_ID}/paper/       (with .gitkeep)
  examples/{PROJECT_ID}/docs/
  examples/{PROJECT_ID}/cc-archive/

**tasks/README.md content:**

  # {PROJECT_ID} Tasks
  # Last updated: {YYMMDD}

  (flow graph, directory tree, and status table -- see project-structure.md)

Then proceed to create the first group (-> Scope 2) and first task (-> Scope 3)
using the metadata collected above. No need to re-ask questions.

---

Step 3P: Create Track A -- Code Stubs (if needed)
----------------------------------------------------

Skip if both Q7 and Q8 answered NO.

**A1 -- Pipeline Fn stubs (Q7 = YES)**

For each stage needing a new Fn, create:
  (a) Builder stub: code-dev/1-PIPELINE/{N}-*-WorkSpace/build_{dataset}_{layer}.py
  (b) Paired example task: tasks/D_demo/example_{dataset}_stage{N}_fn/
      Contains: example .py with commented-out usage, README.md, config/, runs/, results/

Before creating: check code/INDEX.md for existing Fn at same stage+dataset.
  Match found -> ask user: "Existing Fn {name} found. Reuse instead?"
  No match -> create stub, add row to code/INDEX.md.

**A2 -- ML model stubs (Q8 = YES)**

Create stubs:
  code/hainn/algo/{family}/algorithm_{name}.py
  code/hainn/tuner/{family}/tuner_{name}.py
  code/hainn/instance/{family}/instance_{name}.py
  code/hainn/instance/{family}/configuration_{name}.py

Before creating: check code/INDEX.md for existing model in same family+dataset.

Paired example task: tasks/D_demo/example_{name}_model/
  Contains: example .py with commented-out usage, README.md, config/, runs/, results/

Add rows to group README.md, tasks/README.md, and code/INDEX.md.

---

Step 4P: Report
-----------------

Print a structured summary:
  - Track B files created (project folder, group, task, config YAMLs)
  - Track A stubs created (if any)
  - Next steps: fill TODO_ placeholders, implement via /haipipe-data or /haipipe-nn


===================================================================
Scope 2: New Group
===================================================================

Adds a group folder to an existing project.

---

Step 1G: Identify Project
----------------------------

If inside a project: auto-detect from cwd or git status.
Otherwise: list Proj* directories and ask.
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
    README.md

**Group README.md content:**

  {G}_{group_name}
  =================

  **Purpose:** {one-line from user or inferred}

  Flow
  ----
  (to be filled as tasks are added)

  Tasks
  -----
  | Task | Description | Status |
  |------|-------------|--------|

Add group to tasks/README.md directory tree.

---

Step 4G: Optionally Create First Task
----------------------------------------

Ask: "Create the first task inside this group? (yes/no)"
  YES -> proceed to Scope 3 (auto-fill project and group, skip re-asking)
  NO  -> done


===================================================================
Scope 3: New Task
===================================================================

Adds a task folder to an existing group.

---

Step 1T: Identify Project and Group
--------------------------------------

If inside a project: auto-detect from cwd.
If inside a group folder: auto-detect both.
Otherwise: ask for project, then list groups and ask which one.
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

---

Step 3T: Create Task Folder
------------------------------

  tasks/{G}_{group}/{G}{N}_{task_name}/
    {G}{N}_{task_name}.py     (stub with # %% cells)
    README.md
    config/                   (task's own YAML configs)
    runs/                     (empty)
    results/                  (empty)

**Task README.md content:**

  {G}{N}_{task_name}
  ====================

  **What:** {one-line from user or inferred}
  **Why:** TODO
  **Inputs:** TODO
  **Outputs:** TODO

**Stub .py content:**

  # %% [markdown]
  # # {G}{N}_{task_name}
  # TODO: implement

  # %%
  # Setup
  import os, sys

  # %%
  # Main logic

**Config handling:**

  Create config/ dir. If pipeline stages known, add YAML skeletons (see below).
  Each task owns its own config files. No sharing or symlinks between tasks.

---

Step 4T: Update README.md Files
----------------------------------

Add task row to:
  - tasks/{G}_{group}/README.md task list
  - tasks/README.md status table and directory tree

---

YAML Skeletons (shared across scopes)
========================================

Created in config/ when pipeline stages are known.

  Stage 1: config/1_source_{dataset}.yaml
  Stage 2: config/2_record_{dataset}.yaml
  Stage 3: config/3_case_{dataset}.yaml
  Stage 4: config/4_aidata_{dataset}.yaml
  Stage 5: config/5_model_{name}.yaml

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

- Do NOT create files outside examples/{PROJECT_ID}/ and code/ without asking
- Do NOT generate actual implementation in stubs -- stubs only
- Do NOT run pipeline commands during scaffolding
