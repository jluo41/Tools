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
  Q6. What dataset(s) are involved? (used for config/ YAML naming)
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

Create the four mandatory directories:

  examples/{PROJECT_ID}/cc-archive/
  examples/{PROJECT_ID}/config/
  examples/{PROJECT_ID}/scripts/
  examples/{PROJECT_ID}/results/

Create one placeholder file in cc-archive/ to mark the session:

  examples/{PROJECT_ID}/cc-archive/.gitkeep

Generate YAML skeleton files in config/ for each selected stage.
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

Create the docs/ directory and TODO.md planning tracker:

  examples/{PROJECT_ID}/docs/TODO.md

Populate TODO.md using the template from ref/project-structure.md,
filling in PROJECT_ID, YYMMDD, dataset names, stage selections from Q5-Q9,
and marking stages not selected as n/a.

Create scripts/INDEX.md — the mandatory script index for this project:

  examples/{PROJECT_ID}/scripts/INDEX.md

Content:

```markdown
# scripts/INDEX.md — {PROJECT_ID}
# Last updated: {YYMMDD}
# Purpose: index all scripts by data, functionality, and stage.
# Claude reads this before creating any new script to check for reuse.

| Script | Data | Functionality | Stage | Status |
|--------|------|---------------|-------|--------|
| (scripts will be added here as they are created) | | | | |
```

Create a .gitkeep in results/ so the folder is tracked by git:

  examples/{PROJECT_ID}/results/.gitkeep

---

Step 3: Create Track A — Code Stubs (if needed)
=================================================

Skip this step entirely if both Q7 and Q8 answered NO.

**A1 — Pipeline function stubs (if Q7 = YES)**

For each stage the user flagged as needing a new Fn, create TWO things:
  (a) a stub builder in code-dev/
  (b) a paired example script in examples/{PROJECT_ID}/scripts/

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

Auto-generated example script for Stage N Fn:
  Assign seq = next available number in scripts/
  File: examples/{PROJECT_ID}/scripts/{seq}_{YYMMDD}_example_{dataset}_stage{N}_fn.py

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

Add this example script to scripts/INDEX.md:

  | {seq}_{YYMMDD}_example_{dataset}_stage{N}_fn.py | {dataset} | Example usage of Stage {N} Fn | {N} | stub |

Check code/INDEX.md (read it first if it exists):
  - Search the Pipeline Functions table for any FnClass that works with {dataset} at Stage {N}.
  - If a match is found: inform the user before creating a stub:
      "Existing Fn found: {FnClassName} (used in {Projects}). Do you want to reuse it instead?"
    Wait for user decision. If reuse: skip stub creation, update config YAML with real class name.
  - If no match: proceed with stub creation, then add a new row to code/INDEX.md:
      | TODO_{dataset}Stage{N}Fn | {N} | {dataset} | (stub — not yet generated) | {PROJECT_ID} | stub |

**A2 — ML model stubs (if Q8 = YES)**

Create stub files in code/hainn/ AND a paired example script:

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

Auto-generated example script for the new model:
  File: examples/{PROJECT_ID}/scripts/{seq}_{YYMMDD}_example_{name}_model.py

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

Add this example script to scripts/INDEX.md:

  | {seq}_{YYMMDD}_example_{name}_model.py | {dataset} | Example usage of {name} model | 5 | stub |

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
  examples/{PROJECT_ID}/cc-archive/                    [created]
  examples/{PROJECT_ID}/config/                        [created]
    1_source_{dataset}.yaml                            [skeleton]
    ...
  examples/{PROJECT_ID}/scripts/                       [created, flat]
    INDEX.md                                           [created, {N} entries]
    {seq}_{YYMMDD}_example_{name}.py                   [auto-generated per stub]
  examples/{PROJECT_ID}/results/                       [created]
  examples/{PROJECT_ID}/docs/                          [created]
    TODO.md                                            [created, pre-filled]

Track A — code/ (if applicable)
  code-dev/1-PIPELINE/...                              [stubs created] or [skipped]
  code/hainn/...                                       [stubs created] or [skipped]

Next steps:
  1. Fill in the TODO fields in config/ YAML files.
  2. Open scripts/INDEX.md to see all auto-generated example scripts.
  3. Run /haipipe-data design-chef {stage} to implement pipeline Fns (if Track A).
  4. Run /haipipe-nn to implement ML model (if Track A A2).
  5. Update example scripts from "stub" to "wip" as implementation progresses.
  6. Save this session with /cc-session-summary -> cc-archive/.
```

---

Checkpoints
-----------

Print these at the end of Step 4 (verbatim — no extra analysis needed):

  [CH-2] scripts/INDEX.md in sync?
  "Quick check: does scripts/INDEX.md have an entry for every .py/.sh in
   scripts/? Are all status values (stub / wip / done) current?"

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
- Do NOT create notebooks (.ipynb) inside scripts/ — they go in cc-archive or a separate nb/ folder if needed.
