fn-new: Scaffold a New Project (Both Tracks)
=============================================

Interactive flow for creating a new project from scratch.
Covers Track B (examples/ folder) and Track A (code-dev/ + hainn/ stubs)
in one unified pass. The user does not need to distinguish tracks.

---

Step 1: Collect Project Metadata
==================================

Ask the following questions one block at a time. Do not ask all at once.
Wait for user answers before moving to Step 2.

**Block 1 — Identity**

  Q1. What is the project Series letter?
      (A=misc/early, B=benchmarking, C=models, D=EHR, or new letter)
  Q2. What is the Category? (Bench / Model / EHR / Pretrain / or custom)
  Q3. What is the sequential Num within Series-Category?
      (check existing examples/ folders to avoid collision)
  Q4. What is the project Name? (CamelCase, e.g. FairGlucose, WeightPredict)

  -> Compose: PROJECT_ID = Proj{Series}-{Category}-{Num}-{Name}
  -> Confirm with user before proceeding.

**Block 2 — Scope**

  Q5. Which pipeline stages does this project use?
      (1=Source, 2=Record, 3=Case, 4=AIData, 5=Model, 6=Endpoint — list all that apply)
  Q6. What dataset(s) are involved? (used for config YAML naming)
  Q7. Does this project need a NEW pipeline function (new dataset/modality)?
      (YES -> Track A stubs for relevant stages; NO -> skip Track A for pipeline)
  Q8. Does this project need a NEW ML model architecture?
      (YES -> Track A stubs for hainn/; NO -> skip Track A for models)
  Q9. If new model: what model family and name?
      (family: tsforecast / mlpredictor / tefm / tediffusion / bandit)
      (name: snake_case, e.g. glucose_transformer)

After collecting all answers, display a summary and ask: "Does this look correct? Shall I create the project?"

Wait for explicit YES before Step 2.

---

Step 2: Create Track B — examples/ Folder
==========================================

Base path: examples/{PROJECT_ID}/

Create the mandatory top-level directories:

  examples/{PROJECT_ID}/tasks/
  examples/{PROJECT_ID}/paper/

Optionally created later (not at scaffold time unless user requests):

  examples/{PROJECT_ID}/docs/       (optional — project-level documentation)
  examples/{PROJECT_ID}/cc-archive/ (optional — Claude Code session logs)

Create one placeholder in paper/ to mark it:

  examples/{PROJECT_ID}/paper/.gitkeep

Create tasks/INDEX.md — the mandatory global task index for this project:

  examples/{PROJECT_ID}/tasks/INDEX.md

Content:

```markdown
# tasks/INDEX.md — {PROJECT_ID}
# Last updated: {YYMMDD}
# Purpose: global task index. Claude reads this before creating any new task
# folder to check for reuse. One row per task subfolder in tasks/.

| Task | Data | Stage | Description | Status |
|------|------|-------|-------------|--------|
| (task folders will be added here as they are created) | | | | |
```

Create the first task folder to hold pipeline config YAML files.
Task name: use clean snake_case — no sequence numbers, no date prefix.
Pick a name that reflects the first thing the project will do, e.g.
cook_source, cook_record, cook_modelinstance, etc.

First task folder structure (example: cook_modelinstance):

  examples/{PROJECT_ID}/tasks/cook_modelinstance/
  examples/{PROJECT_ID}/tasks/cook_modelinstance/cook_modelinstance.py
  examples/{PROJECT_ID}/tasks/cook_modelinstance/config/
  examples/{PROJECT_ID}/tasks/cook_modelinstance/runs/
  examples/{PROJECT_ID}/tasks/cook_modelinstance/results/
  examples/{PROJECT_ID}/tasks/cook_modelinstance/INDEX.md

Generate YAML skeleton files in that task's config/ for each selected stage.
Use the templates below. Replace {dataset} with the dataset name from Q6,
{name} with the model name from Q9.

  Stage 1 selected  ->  config/1_source_{dataset}.yaml
  Stage 2 selected  ->  config/2_record_{dataset}.yaml
  Stage 3 selected  ->  config/3_case_{dataset}.yaml
  Stage 4 selected  ->  config/4_aidata_{dataset}.yaml
  Stage 5 selected  ->  config/5_model_{name}.yaml

**YAML Skeleton Template (Stage 1 example):**

```yaml
# Stage 1: Source Config
# Project: {PROJECT_ID}
# Dataset: {dataset}
# Created: {YYMMDD}
# TODO: fill in all fields before running haistep-source

SourceFnClass: TODO_SourceFnClassName
SourceArgs:
  dataset_name: {dataset}
  # TODO: add dataset-specific args
```

Adapt the TODO fields to match the stage. For Stage 5 (model), include:

```yaml
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
```

When additional tasks are created later and need the same configs, they
symlink back to the owning task rather than duplicating files:

  cd examples/{PROJECT_ID}/tasks/eval_main_table/
  ln -s ../cook_modelinstance/config config

Create the task-level INDEX.md inside the first task folder:

  examples/{PROJECT_ID}/tasks/cook_modelinstance/INDEX.md

Content:

```markdown
# cook_modelinstance/INDEX.md — {PROJECT_ID}
# Last updated: {YYMMDD}

| File | Description | Status |
|------|-------------|--------|
| cook_modelinstance.py | Main task script | stub |
```

Add a row for this task to tasks/INDEX.md:

  | cook_modelinstance | {dataset} | 5 | Cook model instance for {name} | stub |

---

Step 3: Create Track A — Code Stubs (if needed)
=================================================

Skip this step entirely if both Q7 and Q8 answered NO.

**A1 — Pipeline function stubs (if Q7 = YES)**

For each stage the user flagged as needing a new Fn, create TWO things:
  (a) a stub builder in code-dev/
  (b) a paired example task in examples/{PROJECT_ID}/tasks/

Builder stubs:

  code-dev/1-PIPELINE/1-Source-WorkSpace/build_{dataset}_source.py  (Stage 1)
  code-dev/1-PIPELINE/2-Record-WorkSpace/build_{dataset}_record.py  (Stage 2)
  code-dev/1-PIPELINE/3-Case-WorkSpace/build_{dataset}_case.py      (Stage 3)
  code-dev/1-PIPELINE/4-AIData-WorkSpace/build_{dataset}_aidata.py  (Stage 4)

Builder stub content (same pattern for all):

```python
# Builder stub for {dataset} - Stage N
# Project: {PROJECT_ID}
# Created: {YYMMDD}
# TODO: implement this builder using /haipipe-data design-chef {stage}
# Run this script after implementation to generate code/haifn/fn_{layer}/

# See: Tools/plugins/research/skills/haipipe-data/SKILL.md
# Command: /haipipe-data design-chef {stage}
```

Auto-generated example task for Stage N Fn:
  Task name: example_{dataset}_stage{N}_fn   (clean snake_case, no seq numbers)
  Dir:  examples/{PROJECT_ID}/tasks/example_{dataset}_stage{N}_fn/
  Files inside the task folder:
    example_{dataset}_stage{N}_fn.py          (main task script)
    INDEX.md                                  (task-level index)
    config/                                   -> symlink to owning task if configs already exist,
                                                 otherwise create config/ with relevant YAML
    runs/                                     (parameterized notebook runs)
    results/                                  (output artifacts)

```python
# Example: {dataset} Stage {N} Fn — {PROJECT_ID}
# Stage: {N}
# Data: {dataset}
# Created: {YYMMDD}
# Auto-generated by /haipipe-project new
# TODO: fill in after implementing the Fn via /haipipe-data design-chef {stage}

from haipipe.base import setup_workspace
# from haifn.fn_{layer}.{fn_module} import {FnClassName}  # uncomment after builder runs

SPACE = setup_workspace()

# Step 1: Inspect the input to this stage
# prev_set = {PrevSetClass}.load_asset(SPACE, name='{dataset}', version='@v0001-{dataset}')
# print(prev_set)

# Step 2: Run the Fn
# fn = {FnClassName}()
# output = fn.run(prev_set)
# print(output)
```

Add this task to tasks/INDEX.md:

  | example_{dataset}_stage{N}_fn | {dataset} | {N} | Example usage of Stage {N} Fn | stub |

Check code/INDEX.md (read it first if it exists):
  - Search the Pipeline Functions table for any FnClass that works with {dataset} at Stage {N}.
  - If a match is found: inform the user before creating a stub:
      "Existing Fn found: {FnClassName} (used in {Projects}). Do you want to reuse it instead?"
    Wait for user decision. If reuse: skip stub creation, update config YAML with real class name.
  - If no match: proceed with stub creation, then add a new row to code/INDEX.md:
      | TODO_{dataset}Stage{N}Fn | {N} | {dataset} | (stub — not yet generated) | {PROJECT_ID} | stub |

**A2 — ML model stubs (if Q8 = YES)**

Create stub files in code/hainn/ AND a paired example task:

  code/hainn/algo/{family}/algorithm_{name}.py
  code/hainn/tuner/{family}/tuner_{name}.py
  code/hainn/tuner/{family}/test-modeling-{name}/   (directory + .gitkeep)
  code/hainn/instance/{family}/instance_{name}.py
  code/hainn/instance/{family}/configuration_{name}.py

Stub content for algorithm_{name}.py:

```python
# Algorithm stub: {name}
# Family: {family}
# Project: {PROJECT_ID}
# Created: {YYMMDD}
# TODO: implement using /haipipe-nn algorithm

class {NameCamelCase}Algorithm:
    pass
```

Stub content for instance_{name}.py:

```python
# Instance stub: {name}
# Family: {family}
# Project: {PROJECT_ID}
# Created: {YYMMDD}
# TODO: implement using /haipipe-nn instance

class {NameCamelCase}Instance:
    MODEL_TYPE = "TODO_{name}"
```

Auto-generated example task for the new model:
  Task name: example_{name}_model   (clean snake_case, no seq numbers)
  Dir:  examples/{PROJECT_ID}/tasks/example_{name}_model/
  Files inside the task folder:
    example_{name}_model.py                   (main task script)
    INDEX.md                                  (task-level index)
    config/                                   -> symlink to owning task if configs already exist,
                                                 otherwise create config/ with relevant YAML
    runs/                                     (parameterized notebook runs)
    results/                                  (output artifacts)

```python
# Example: {name} model — {PROJECT_ID}
# Family: {family}
# Data: {dataset}
# Created: {YYMMDD}
# Auto-generated by /haipipe-project new
# TODO: fill in after implementing model via /haipipe-nn

from haipipe.base import setup_workspace
# from hainn.instance.{family}.instance_{name} import {NameCamelCase}Instance  # after impl

SPACE = setup_workspace()

# Step 1: Load AIData
# aidata_set = AIDataSet.load_asset(SPACE, name='{dataset}', version='@v0001-{dataset}')
# print(aidata_set)

# Step 2: Load model instance
# instance = {NameCamelCase}Instance.from_yaml('config/5_model_{name}.yaml', SPACE)
# print(instance)

# Step 3: Train
# instance.fit(aidata_set)

# Step 4: Evaluate
# results = instance.evaluate(aidata_set)
# print(results)
```

Add this task to tasks/INDEX.md:

  | example_{name}_model | {dataset} | 5 | Example usage of {name} model | stub |

Check code/INDEX.md ML Models table for any existing model in the same {family}
that works with {dataset}:
  - If a match is found: inform the user:
      "Existing model found: {ModelInstanceClass} (used in {Projects}). Reuse instead?"
    Wait for decision. If reuse: skip model stubs, update config YAML with real class name.
  - If no match: proceed with stubs, then add a new row to code/INDEX.md:
      | TODO_{NameCamelCase}Instance | {family} | {name} | TODO_{NameCamelCase}Tuner | (stub) | {PROJECT_ID} | stub |

---

Step 4: Report to User
=======================

Print a structured summary of everything created:

```
Project Created: {PROJECT_ID}
========================

Track B — examples/
  examples/{PROJECT_ID}/tasks/                       [created, task-folder layout]
    INDEX.md                                         [created, global task index]
    cook_modelinstance/                              [first task — owns config YAMLs]
      cook_modelinstance.py                          [stub]
      config/                                        [YAML skeletons for selected stages]
        1_source_{dataset}.yaml                      [skeleton]
        ...
      runs/                                          [for parameterized .ipynb runs]
      results/                                       [output artifacts]
      INDEX.md                                       [task-level index]
    example_{name}/                                  [auto-generated task per stub]
      example_{name}.py                              [stub]
      config/  -> ../cook_modelinstance/config       [symlink to owning task]
      runs/
      results/
      INDEX.md
  examples/{PROJECT_ID}/paper/                       [created, mandatory]
  examples/{PROJECT_ID}/docs/                        [created] or [skipped — add when needed]
  examples/{PROJECT_ID}/cc-archive/                  [created] or [skipped — add when needed]

Track A — code/ (if applicable)
  code-dev/1-PIPELINE/...                            [stubs created] or [skipped]
  code/hainn/...                                     [stubs created] or [skipped]

Task folder layout (each task in tasks/):
  {task}.py          main script (source of truth)
  {task}.ipynb       optional demo notebook
  config/            YAML configs (owned or symlinked)
  runs/              parameterized runs as {variant}.ipynb
  results/           output artifacts
  INDEX.md           task-level file index

Next steps:
  1. Fill in the TODO fields in config/ YAML files.
  2. Open tasks/INDEX.md to see all auto-generated example tasks.
  3. Run /haipipe-data design-chef {stage} to implement pipeline Fns (if Track A).
  4. Run /haipipe-nn to implement ML model (if Track A A2).
  5. Update example tasks from "stub" to "wip" as implementation progresses.
  6. Save this session with /cc-session-summary -> cc-archive/.
```

---

Checkpoints
-----------

Print these at the end of Step 4 (verbatim — no extra analysis needed):

  [CH-2] tasks/INDEX.md in sync?
  "Quick check: does tasks/INDEX.md have a row for every task subfolder?
   Does each {task}/INDEX.md exist with at least a stub row? Are all status
   values (stub / wip / done) current?"

  [CH-4] code/INDEX.md updated?
  "Quick check: if new Track A stubs were created, confirm code/INDEX.md has
   stub-status rows for them (so future projects can find them for reuse)."

  [CH-5] YAML placeholders filled?
  "Quick check: search config/ for any remaining TODO_ values — all placeholder
   class names must be replaced before running the pipeline."

---

MUST NOT
---------

- Do NOT create files outside examples/{PROJECT_ID}/ and code/ without asking.
- Do NOT generate actual implementation in stub files — stubs only.
- Do NOT run any pipeline commands during scaffolding.
- Do NOT create CLAUDE.md inside the project folder (not part of the standard).
- Do NOT create notebooks (.ipynb) at scaffold time — they are added later
  as {task}.ipynb (demo) or runs/{variant}.ipynb (parameterized) inside task folders.
