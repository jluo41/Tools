Skill: haipipe-data-0-overview
===============================

Navigation hub and design reference for the haipipe system.

Use this skill to understand:
- How haipipe is architected and why
- What the 6-layer data pipeline does at each stage
- How the skill system is designed and what skills exist
- What code and data currently exist in this project

On invocation, read this file in full. No subcommand routing needed.

---

What Is haipipe
===============

haipipe is a healthcare AI platform built around a **6-layer sequential data
pipeline** that takes raw clinical data all the way to deployed ML models.
The system is entirely config-driven and follows a consistent cooking metaphor
at every layer.

The three core packages:

```
haipipe    Core pipeline framework (EDITABLE)
           code/haipipe/

hainn      ML models and predictors (EDITABLE)
           code/hainn/

haifn      Production functions (GENERATED -- NEVER edit directly)
           code/haifn/
```

The builder pattern bridges haipipe and haifn:

```
code-dev/1-PIPELINE/           <-- edit these (Academy)
    |  run builder scripts
    v
code/haifn/                    <-- auto-generated (DO NOT EDIT)
```

---

Design Principles
=================

**1. Sequential layers with persisted intermediate assets**

Each layer reads from the previous layer's output and saves its own output
to _WorkSpace/. Nothing is recomputed unless explicitly requested. The Asset
base class (code/haipipe/assets.py) handles all I/O uniformly.

**2. Cooking metaphor — consistent across all 6 layers**

```
Kitchen  = Pipeline class         (code/haipipe/<layer>_base/)
Chef     = Domain function (Fn)   (code/haifn/<fn_layer>/)     GENERATED
Recipe   = YAML config file       (config/)
Dish     = Set asset              (_WorkSpace/<N>-<Layer>Store/)
Academy  = Builder scripts        (code-dev/1-PIPELINE/<N>-WorkSpace/)
```

The metaphor makes the roles unambiguous: you write the Recipe (config) and
choose which Chefs (Fns) to use. The Kitchen (Pipeline) does the rest.

**3. Builder pattern — generated code, never edited directly**

All domain-specific functions (SourceFn, HumanFn, RecordFn, TriggerFn,
CaseFn, TfmFn, SplitFn, EndpointFn) live in code/haifn/ as generated Python
files. The source of truth is the builder scripts in code-dev/1-PIPELINE/.

```
Developer edits builder -> runs builder -> production Fn is regenerated
```

This enforces consistency (schema, interface) across all Fns.

**4. Config-driven execution**

All pipelines read YAML configs. The @ reference system resolves cross-config
dependencies at runtime (e.g., "@meta.selected_actions" pulls a list from
another section). Every pipeline stage has its own config format.

**5. Schema consistency within a domain**

All SourceFns for a domain must produce identical column schemas for shared
table types. This is what allows Layer 2 (Record) to process any dataset
from a domain without knowing which specific SourceFn produced it.

**6. Human-AI collaboration mandatory**

All code changes require:
1. AI presents plan (files to edit, changes to make, builders to run)
2. User approves
3. AI executes

Never edit code/haifn/ directly. Never commit without explicit request.

---

The 6-Layer Pipeline
====================

```
Raw Data
    |
    v
Layer 1: Source  ------  Raw files -> standardized SourceSet tables
    |                    (code/haipipe/source_base/)
    |                    Chefs: code/haifn/fn_source/
    v
Layer 2: Record  ------  SourceSet -> temporally-aligned RecordSet
    |                    (code/haipipe/record_base/)
    |                    Chefs: code/haifn/fn_record/
    v
Layer 3: Case  --------  RecordSet -> event-triggered CaseSet
    |                    (code/haipipe/case_base/)
    |                    Chefs: code/haifn/fn_case/
    v
Layer 4: AIData  ------  CaseSet -> ML-ready AIDataSet (train/val/test)
    |                    (code/haipipe/aidata_base/)
    |                    Chefs: code/haifn/fn_aidata/
    v
Layer 5: Model  -------  AIDataSet -> trained ModelInstance
    |                    (code/haipipe/model_base/ + code/hainn/)
    v
Layer 6: Endpoint  ----  ModelInstance -> deployment EndpointSet
                         (code/haipipe/endpoint_base/)
                         Chefs: code/haifn/fn_endpoint/
```

Each layer has a matching skill:
- Layer 1: /haipipe-data-1-source
- Layer 2: /haipipe-data-2-record
- Layer 3: /haipipe-data-3-case
- Layer 4: /haipipe-data-4-aidata
- Layer 5+: /haipipe-nn-* skills

---

Current Code Structure
======================

Discover at runtime (always prefer ls over relying on this snapshot):

```bash
ls code/haipipe/          # core pipeline base classes
ls code/hainn/            # ML models and predictors
ls code/haifn/            # generated production functions
ls code-dev/1-PIPELINE/   # builder workspaces
```

Snapshot (as of 2026-02-21):

```
code/
+-- haipipe/                        Core pipeline framework
|   +-- source_base/                Layer 1: SourceSet
|   +-- record_base/                Layer 2: RecordSet
|   +-- case_base/                  Layer 3: CaseSet
|   +-- aidata_base/                Layer 4: AIDataSet
|   +-- model_base/                 Layer 5: ModelInstance orchestration
|   +-- endpoint_base/              Layer 6: EndpointSet
|   +-- assets.py                   Base Asset class (unified save/load/push)
|   +-- base.py                     YAML @ reference resolver
|
+-- hainn/                          ML models and predictors
|   +-- mlpredictor/                S-Learner / T-Learner (XGBoost, LightGBM, DeepFM, ...)
|   +-- bandit/                     Bandit algorithms (Thompson sampling, DROPO)
|   +-- tefm/                       Time-Event Foundation Model (CLM, MLM, CTEP, MM)
|   +-- tediffusion/                Diffusion model for time series
|   +-- tsforecast/                 Time series forecasting (NeuralForecast, MLForecast, ...)
|   +-- model_instance.py           Unified model wrapper (fit/predict/explain)
|   +-- prefn_pipeline.py           Feature preprocessing pipeline
|
+-- haifn/                          GENERATED production functions (DO NOT EDIT)
    +-- fn_source/                  SourceFn: raw data extractors
    +-- fn_record/                  HumanFn + RecordFn: entity + record processors
    |   +-- human/                  HumanFn files
    |   +-- record/                 RecordFn files
    +-- fn_case/                    TriggerFn + CaseFn: feature extractors
    |   +-- fn_trigger/             TriggerFn files
    |   +-- case_casefn/            CaseFn files
    +-- fn_aidata/                  TfmFn + SplitFn: ML transforms
    |   +-- entryinput/             Input TfmFn files
    |   +-- entryoutput/            Output TfmFn files
    |   +-- split/                  SplitFn files
    +-- fn_endpoint/                EndpointFn: inference functions
    |   +-- fn_meta/                MetaFn files
    |   +-- fn_post/                PostFn files
    |   +-- fn_trig/                TrigFn files
    |   +-- fn_src2input/           Src2InputFn files
    |   +-- fn_input2src/           Input2SrcFn files
    +-- fn_model/                   ModelFn: model-specific preprocessing
```

---

Current Builder Structure
=========================

```bash
ls code-dev/1-PIPELINE/    # all builder workspaces
```

Snapshot (as of 2026-02-21):

```
code-dev/1-PIPELINE/
+-- 1-Source-WorkSpace/     SourceFn builders      (c<N>_build_source_*.py)
+-- 2-Record-WorkSpace/     HumanFn + RecordFn builders
|                               h<N>_build_human_*.py
|                               r<N>_build_record_*.py
+-- 3-Case-WorkSpace/       TriggerFn + CaseFn builders
|                               a<N>_build_trigger_*.py
|                               c<N>_build_casefn_*.py
+-- 4-AIData-WorkSpace/     TfmFn + SplitFn builders
|                               c<N>_build_transforms_*.py
|                               s<N>_build_splitfn_*.py
+-- 5-Instance-WorkSpace/   ExampleFn builders for ModelInstance
+-- 6-Endpoint-WorkSpace/   EndpointFn builders
                                a<N>_build_metafn_*.py
                                b<N>_build_trigfn_*.py
                                c<N>_build_postfn_*.py
                                d<N>_build_src2inputfn_*.py
                                e<N>_build_input2srcfn_*.py
```

---

Current Data Structure
======================

```bash
ls _WorkSpace/     # all intermediate data stores
```

Snapshot (as of 2026-02-21):

```
_WorkSpace/
+-- 0-RawDataStore/         Raw input files (CSV, XML, Parquet)
+-- 1-SourceStore/          Layer 1 output: SourceSets
|       {CohortName}/@{SourceFnName}/
+-- 2-RecStore/             Layer 2 output: RecordSets
|       {CohortName}_v{N}RecSet/
+-- 3-CaseStore/            Layer 3 output: CaseSets
|       {RecSetName}/@v{N}CaseSet-{TriggerFolder}/
+-- 4-AIDataStore/          Layer 4 output: AIDataSets
|       {aidata_name}/@{aidata_version}/
+-- 5-ModelInstanceStore/   Layer 5 output: trained models
|       {model_name}/
+-- 6-EndpointStore/        Layer 6 output: deployment packages
        {endpoint_name}/
```

To see what is currently available at each layer:

```bash
ls _WorkSpace/1-SourceStore/            # available cohorts (Source)
ls _WorkSpace/2-RecStore/               # available RecordSets
ls _WorkSpace/3-CaseStore/             # available CaseSets
ls _WorkSpace/4-AIDataStore/            # available AIDataSets
ls _WorkSpace/5-ModelInstanceStore/     # available trained models
```

---

Current Config Structure
========================

```bash
ls config/    # all YAML config directories
```

Snapshot (as of 2026-02-21):

```
config/
+-- haipipe-process-aidata/    Production AIData configs
+-- haipipe-process-record/    Production Record configs
+-- test-haistep-fairglucose/  Test configs for WellDoc FairGlucose project
+-- test-haistep-ohio/         Test configs for OhioT1DM dataset
```

---

Skill System Design
===================

Each haipipe-data-* skill follows these principles:

**Framework patterns only**
Skills document HOW the framework works. They do NOT catalog what is
currently registered (which Fns exist, which cohorts are set up). That
state is discovered at runtime with `ls`.

**Discovery over enumeration**
Instead of a hardcoded list of Fns, every skill says:
```bash
ls code/haifn/<fn_layer>/    # discover at runtime
```

**Placeholders, not project names**
Config examples use `<CohortName>`, `<SourceFnName>` — not hardcoded names.
This keeps the skill usable for any domain or project.

**Examples labeled illustrative**
When a concrete example is needed to teach structure, it is labeled:
```
# Example (illustrative -- actual names from ls commands)
```

**Numbered subcommand files**
Each skill has 4 numbered subcommand files:
```
1-load.md          Inspect existing Set asset
2-cook.md          Run Pipeline with config
3-design-chef.md   Create new Fn via builder
4-design-kitchen.md Modify Pipeline infrastructure
```

**No "update this skill" step**
Skills do not grow with the project. Project-specific state lives in the
filesystem; skills stay general and reusable across domains.

---

Skill Index
===========

**Data pipeline skills:**

```
/haipipe-data-0-overview    This file -- architecture + navigation
/haipipe-data-1-source      Layer 1: Raw files -> SourceSet
/haipipe-data-2-record      Layer 2: SourceSet -> RecordSet
/haipipe-data-3-case        Layer 3: RecordSet -> CaseSet
/haipipe-data-4-aidata      Layer 4: CaseSet -> AIDataSet
```

**ML model skills:**

```
/haipipe-nn-0-overview      Model system architecture
/haipipe-nn-1-algorithm     Algorithm selection (XGBoost, LightGBM, tefm, ...)
/haipipe-nn-2-tuner         Hyperparameter tuning with Optuna
/haipipe-nn-3-instance      ModelInstance: fit/predict/explain
/haipipe-nn-4-modelset      ModelSet: packaging and evaluation
```

**Other skills:**

```
/coding-by-logging          Code generation via structured logging
/evaluation-display-skill   Evaluation display and reporting
/notebook-cell-python       Jupyter notebook cell management
/paper-incubator            Research paper writing support
```

To discover all available skills:
```bash
ls Tools/plugins/research/skills/
```

---

Key Entry Points
================

**Start a new layer from scratch:**
```bash
# Discover what Fns are registered for that layer
ls code/haifn/fn_source/     # Layer 1
ls code/haifn/fn_record/     # Layer 2
ls code/haifn/fn_case/       # Layer 3
ls code/haifn/fn_aidata/     # Layer 4

# Invoke the matching skill
# /haipipe-data-1-source cook
# /haipipe-data-2-record cook
# /haipipe-data-3-case cook
# /haipipe-data-4-aidata cook
```

**Need a new Fn that doesn't exist yet:**
```
/haipipe-data-1-source design-chef    # new SourceFn
/haipipe-data-2-record design-chef    # new HumanFn or RecordFn
/haipipe-data-3-case design-chef      # new TriggerFn or CaseFn
/haipipe-data-4-aidata design-chef    # new TfmFn or SplitFn
```

**Inspect existing assets:**
```
/haipipe-data-1-source load
/haipipe-data-2-record load
/haipipe-data-3-case load
/haipipe-data-4-aidata load
```

---

Prerequisites (Universal)
==========================

Every haipipe operation requires:

```bash
source .venv/bin/activate    # ALWAYS first
source env.sh                # ALWAYS second (sets _WorkSpace paths)
```

Never run Python without .venv activated. Never skip env.sh.

---

MUST DO
=======

1. **Read this file** when starting any haipipe task to orient yourself
2. **Check the layer order** -- always work sequentially (1→2→3→4)
3. **Discover Fns with ls** -- never assume what is registered
4. **Use the skill for the specific layer** after reading this overview
5. **Present plan to user and get approval** before any code changes

---

MUST NOT
========

1. **NEVER edit** code/haifn/ directly -- it is 100% generated
2. **NEVER run** Python without .venv activated and env.sh sourced
3. **NEVER skip layers** -- output of layer N is input to layer N+1
4. **NEVER create** new skill files with project-specific state
5. **NEVER commit** without explicit user request
