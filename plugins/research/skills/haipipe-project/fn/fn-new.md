fn-new: Scaffold a New Project (Both Tracks)
=============================================

Interactive flow for creating a new project from scratch.
Covers Track B (examples/) and Track A (code-dev/ + hainn/) in one pass.

---

Step 1: Collect Project Metadata
==================================

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

Step 2: Create Track B -- examples/ Folder
============================================

Create the mandatory structure:

  examples/{PROJECT_ID}/tasks/
  examples/{PROJECT_ID}/tasks/INDEX.md

Optionally created (only if user requests):

  examples/{PROJECT_ID}/paper/       (with .gitkeep)
  examples/{PROJECT_ID}/docs/
  examples/{PROJECT_ID}/cc-archive/

**tasks/INDEX.md content:**

  # tasks/INDEX.md -- {PROJECT_ID}
  # Last updated: {YYMMDD}

  | Task | Data | Stage | Description | Status |
  |------|------|-------|-------------|--------|

**First task folder** -- name reflects the project's first action
(e.g., cook_modelinstance, cook_source):

  tasks/{first_task}/
    {first_task}.py       (stub)
    config/               (YAML skeletons per selected stage)
    runs/
    results/
    INDEX.md

**YAML skeletons** in config/ for each selected stage:

  Stage 1: config/1_source_{dataset}.yaml
  Stage 2: config/2_record_{dataset}.yaml
  Stage 3: config/3_case_{dataset}.yaml
  Stage 4: config/4_aidata_{dataset}.yaml
  Stage 5: config/5_model_{name}.yaml

YAML skeleton -- stages 1-4 example:

  # Stage 1: Source Config
  # Project: {PROJECT_ID}
  # Dataset: {dataset}
  # Created: {YYMMDD}
  # TODO: fill in all fields before running haistep-source
  SourceFnClass: TODO_SourceFnClassName
  SourceArgs:
    dataset_name: {dataset}
    # TODO: add dataset-specific args

YAML skeleton -- Stage 5 (model):

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

**Config sharing:** later tasks symlink to the owning task's config/:

  cd tasks/{other_task} && ln -s ../{first_task}/config config

Add task row to tasks/INDEX.md.

---

Step 3: Create Track A -- Code Stubs (if needed)
==================================================

Skip if both Q7 and Q8 answered NO.

**A1 -- Pipeline Fn stubs (Q7 = YES)**

For each stage needing a new Fn, create:
  (a) Builder stub: code-dev/1-PIPELINE/{N}-*-WorkSpace/build_{dataset}_{layer}.py
  (b) Paired example task: tasks/example_{dataset}_stage{N}_fn/
      Contains: example .py with commented-out usage, INDEX.md, config/, runs/, results/

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

Paired example task: tasks/example_{name}_model/
  Contains: example .py with commented-out usage, INDEX.md, config/, runs/, results/

Add rows to tasks/INDEX.md and code/INDEX.md.

---

Step 4: Report to User
=======================

Print a structured summary:
  - Track B files created (project folder, tasks, config YAMLs)
  - Track A stubs created (if any)
  - Next steps: fill TODO_ placeholders, implement via /haipipe-data or /haipipe-nn

---

MUST NOT
---------

- Do NOT create files outside examples/{PROJECT_ID}/ and code/ without asking
- Do NOT generate actual implementation in stubs -- stubs only
- Do NOT run pipeline commands during scaffolding
