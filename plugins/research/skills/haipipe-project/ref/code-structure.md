Track A: Code Development Structure (code/ + code-dev/)
=========================================================

Ground truth for the code-side of a new project.
Covers code-dev/1-PIPELINE/ workspace conventions and code/hainn/ layout.
This file is the authoritative reference for fn-new.md and fn-review.md.

---

Overview
========

Track A is the library side of haipipe. New pipeline functions and new ML
models are developed here. It is separate from Track B (examples/) but a
real project typically touches both: Track A builds the tools, Track B runs
the experiments using those tools.

Two sub-tracks within Track A:

  A1 — Pipeline functions (SourceFn, RecordFn, CaseFn, TfmFn, SplitFn)
       Developed in:  code-dev/1-PIPELINE/
       Generated to:  code/haifn/

  A2 — ML models (Algorithm, Tuner, Instance)
       Developed in:  code/hainn/
       Registered in: ModelInstance_Set via haipipe-nn skill


---

Builder Pattern (A1)
=====================

All production pipeline functions live in code/haifn/ as GENERATED Python
files. The source of truth is the builder workspaces in code-dev/1-PIPELINE/.

  Developer edits builder workspace  ->  runs builder script  ->  code/haifn/ updated

NEVER edit code/haifn/ directly. Always edit the builder workspace, then run
the builder to regenerate.

Workspace layout:

```
code-dev/1-PIPELINE/
+-- 1-Source-WorkSpace/      -> generates  code/haifn/fn_source/
+-- 2-Record-WorkSpace/      -> generates  code/haifn/fn_record/
+-- 3-Case-WorkSpace/        -> generates  code/haifn/fn_case/
+-- 4-AIData-WorkSpace/      -> generates  code/haifn/fn_aidata/
+-- 5-Instance-WorkSpace/    -> generates  code/haifn/fn_model/
+-- 6-Endpoint-WorkSpace/    -> generates  code/haifn/fn_endpoint/
```

Each WorkSpace contains:
  - Builder scripts (Python) that write the Fn class into code/haifn/
  - Test notebooks or test scripts for the Fn
  - Intermediate design notes (can also go to project cc-archive/)


---

Pipeline Function Types by Stage (A1)
=======================================

  Stage   Fn Type(s)                    Generated location
  ------  ----------------------------  ----------------------
  1       SourceFn, HumanFn             code/haifn/fn_source/
  2       RecordFn                      code/haifn/fn_record/
  3       TriggerFn, CaseFn             code/haifn/fn_case/
  4       TfmFn, SplitFn                code/haifn/fn_aidata/
  5       ModelInstanceFn               code/haifn/fn_model/
  6       EndpointFn                    code/haifn/fn_endpoint/

When a new project needs a new dataset or data modality, new Fns are added
to the relevant stages. Use the haipipe-data skill for design-chef guidance.


---

ML Model Layout (A2)
=====================

New ML models are added directly to code/hainn/ (not via a builder):

```
code/hainn/
+-- algo/                    <- Algorithm classes (model architecture)
|   +-- {family}/
|       +-- algorithm_{name}.py
|
+-- tuner/                   <- Tuner classes (training loop + transforms)
|   +-- {family}/
|       +-- tuner_{name}.py
|       +-- test-modeling-{name}/   <- test scripts for this tuner
|
+-- instance/                <- Instance classes (ties algo + tuner + config)
|   +-- {family}/
|       +-- instance_{name}.py
|       +-- configuration_{name}.py
|
+-- nn/                      <- Shared neural network building blocks
    +-- {component}.py
```

Model families in use:
  tsforecast    Time-series forecasting models
  mlpredictor   Classical ML predictors
  tefm          Time-event foundation models
  tediffusion   Time-event diffusion models
  bandit        Bandit / online learning models

Use the haipipe-nn skill for detailed guidance on adding Algorithm/Tuner/Instance.


---

When to Create Track A Stubs
==============================

During /haipipe-project new, ask:

  1. Does this project require a NEW dataset or data modality?
     YES -> need new SourceFn and/or HumanFn in 1-Source-WorkSpace/
            may need new RecordFn in 2-Record-WorkSpace/

  2. Does this project require new feature engineering?
     YES -> may need new CaseFn/TriggerFn or TfmFn/SplitFn

  3. Does this project require a NEW model architecture?
     YES -> need new algo/{family}/algorithm_{name}.py
             new tuner/{family}/tuner_{name}.py
             new instance/{family}/instance_{name}.py + configuration_{name}.py

  4. Is the project purely experimental (reusing existing Fns + models)?
     YES -> Track A is NOT needed. Only Track B (examples/) is created.


---

Track A Stub Files (created by fn-new.md)
==========================================

If Track A is needed, fn-new.md creates placeholder stubs — empty files with
correct naming and location. Actual implementation follows using the relevant
haipipe-data or haipipe-nn skill.

Stubs for new pipeline Fns (one per stage selected):
  code-dev/1-PIPELINE/1-Source-WorkSpace/build_{dataset}_source.py
  code-dev/1-PIPELINE/2-Record-WorkSpace/build_{dataset}_record.py
  code-dev/1-PIPELINE/3-Case-WorkSpace/build_{dataset}_case.py
  code-dev/1-PIPELINE/4-AIData-WorkSpace/build_{dataset}_aidata.py

Stubs for new ML model:
  code/hainn/algo/{family}/algorithm_{name}.py
  code/hainn/tuner/{family}/tuner_{name}.py
  code/hainn/instance/{family}/instance_{name}.py
  code/hainn/instance/{family}/configuration_{name}.py


---

code/INDEX.md — Codebase-Wide Code Registry
============================================

Location: code/INDEX.md  (top of the code/ directory, NOT inside any project)

Purpose: a single index of all implemented pipeline Fns and ML models across
the entire codebase. Claude reads this BEFORE creating any new Fn or model
to check whether an existing implementation can be reused — even from a
different project. Reuse across projects is the goal.

This is separate from tasks/INDEX.md (which is per-project, indexes tasks).
code/INDEX.md is shared across ALL projects.

Format:

```markdown
# code/INDEX.md — haipipe Code Registry
# Last updated: {YYMMDD}
# Read this before creating any new Fn or model.
# If a suitable Fn or model exists, reuse it — do not create a duplicate.

## Pipeline Functions (code/haifn/)

| FnClass | Stage | Dataset / Domain | Location | Projects Using | Status |
|---------|-------|------------------|----------|----------------|--------|
| GlucoseSourceFn | 1 | OhioT1DM, WellDoc CGM | fn_source/glucose_source.py | ProjB-Bench-1, ProjC-WeightPredict | done |
| MimicSourceFn | 1 | MIMIC-III EHR | fn_source/mimic_source.py | ProjD-EHR-Mimic | done |
| GlucoseRecordFn | 2 | OhioT1DM, WellDoc CGM | fn_record/glucose_record.py | ProjB-Bench-1, ProjC-WeightPredict | done |
| GlucoseCaseFn | 3 | OhioT1DM | fn_case/glucose_case.py | ProjB-Bench-1 | done |
| GlucoseTfmFn | 4 | OhioT1DM | fn_aidata/glucose_tfm.py | ProjB-Bench-1 | done |

## ML Models (code/hainn/)

| ModelInstanceClass | Family | Model Type | Tuner | Location | Projects Using | Status |
|--------------------|--------|------------|-------|----------|----------------|--------|
| TECLMInstance | tefm | TE-CLM | TECLMTuner | instance/tefm/instance_teclm.py | ProjC-Model-1-ScalingLaw | done |
| XGBoostInstance | mlpredictor | XGBoost | XGBoostTuner | instance/mlpredictor/instance_xgboost.py | ProjB-Bench-1 | done |
| NHitsInstance | tsforecast | N-HiTS | NHitsTuner | instance/tsforecast/instance_nhits.py | ProjC-WeightPredict | done |
```

Column definitions:
  FnClass / ModelInstanceClass   Exact Python class name (used in config YAMLs)
  Stage / Family                 Pipeline stage number or model family
  Dataset / Domain               What data this Fn or model works with
  Location                       Path relative to code/haifn/ or code/hainn/
  Projects Using                 Comma-separated list of PROJECT_IDs
  Status                         stub | wip | done

When to read code/INDEX.md:
  - Before /haipipe-project new asks Q7/Q8 (new Fn or model needed?)
  - During fn-review.md sync check (do config references resolve to real classes?)
  - During /haipipe-data design-chef or /haipipe-nn generate (avoid duplicates)

When to update code/INDEX.md:
  - fn-new.md: add stub entries when Track A stubs are created
  - /haipipe-data design-chef: upgrade status to wip/done, add location
  - /haipipe-nn: same for models
  - fn-review.md: update Projects Using column when a project references a Fn/model


---

Skill Handoff Points
=====================

Track A work is handled by specialized skills. haipipe-project creates stubs
and provides orientation. For actual implementation, hand off to:

  Stage 1-4 pipeline Fns  ->  /haipipe-data design-chef {stage}
  Stage 5 ML models       ->  /haipipe-nn (algorithm / tuner / instance)
  Stage 6 endpoints       ->  /haipipe-end


---

Review Checklist for Track A (used by fn-review.md)
=====================================================

**For each declared stage (from config/ YAML presence):**
  [ ] Corresponding builder workspace has at least one build_*.py file
  [ ] Generated code/haifn/{fn_layer}/ has the expected Fn class file
  [ ] Fn class file is not a stub (has actual implementation, not just pass)

**For new ML models (if 5_model_*.yaml exists in config/):**
  [ ] algo/{family}/algorithm_{name}.py exists (or uses shared algorithm)
  [ ] tuner/{family}/tuner_{name}.py exists
  [ ] instance/{family}/instance_{name}.py exists
  [ ] instance/{family}/configuration_{name}.py exists
  [ ] Model is registered in the ModelInstance_Set (check haipipe-nn dashboard)

**Builder consistency:**
  [ ] code-dev/ builder and code/haifn/ generated file are in sync
      (no manual edits to haifn/ that diverge from the builder)
