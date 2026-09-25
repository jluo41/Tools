haipipe Architecture Overview
==============================

Condensed reference for the haipipe system.
Covers architecture, design principles, and current project structure.

---

What Is haipipe
===============

haipipe is a healthcare AI platform built around a **6-layer sequential data pipeline** that takes raw clinical data all the way to deployed ML models.
The system is entirely config-driven and follows a consistent cooking metaphor at every layer.

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
tasks/bNN_<block>/jNN_<job>/tNN_<fn-task>/scripts/   <-- edit these (Academy)
    |  run builder scripts
    v
code/haifn/                    <-- auto-generated (DO NOT EDIT)
```

---

Design Principles
=================

**1.
Sequential layers with persisted intermediate assets**

Each layer reads from the previous layer's output and saves its own output to _WorkSpace/.
Nothing is recomputed unless explicitly requested.
The Asset base class (code/haipipe/assets.py) handles all I/O uniformly.

**2.
Cooking metaphor -- consistent across all 6 layers**

```
Kitchen  = Pipeline class         (code/haipipe/<layer>_base/)
Chef     = Domain function (Fn)   (code/haifn/<fn_layer>/)     GENERATED
Recipe   = YAML config file       (the Task's scripts/config/)
Dish     = Set asset              (_WorkSpace/<N>-<Layer>Store/)
Academy  = Builder scripts        (tasks/bNN_*/jNN_*/tNN_*/scripts/)
```

The metaphor makes the roles unambiguous: you write the Recipe (config) and choose which Chefs (Fns) to use.
The Kitchen (Pipeline) does the rest.

**3.
Builder pattern -- generated code, never edited directly**

All domain-specific functions (SourceFn, HumanFn, RecordFn, TriggerFn, CaseFn, TfmFn, SplitFn, EndpointFn) live in code/haifn/ as generated Python files.
The source of truth is each Fn's Run config in a topic Job of its stage Block (`bNN_<stage>/j0N_<fnkind>_<topic>/tNN_<fnkind>_<FnName>/scripts/config/r01_build.yaml`) plus the Block's shared generator in `bNN_<stage>/src/`; the build Run regenerates the Fn and fails unless the committed file matches (legacy workspaces: code-dev/1-PIPELINE/).

```
Developer edits builder -> runs builder -> production Fn is regenerated
```

This enforces consistency (schema, interface) across all Fns.

**4.
Config-driven execution**

All pipelines read YAML configs.
The @ reference system resolves cross-config dependencies at runtime (e.g., "@meta.selected_actions" pulls a list from another section).
Every pipeline stage has its own config format.

**5.
Schema consistency within a domain**

All SourceFns for a domain must produce identical column schemas for shared table types.
This is what allows Layer 2 (Record) to process any dataset from a domain without knowing which specific SourceFn produced it.

**6.
Human-AI collaboration mandatory**

All code changes require:
1. AI presents plan (files to edit, changes to make, builders to run)
2. User approves
3. AI executes

Never edit code/haifn/ directly.
Never commit without explicit request.

**7. External data is versioned input to Source**

ExternalStore is a sideways governed store, not another sequential layer.
SourceFn may attach pinned ZIP/NPI/NDC/NCPDP and engagement snapshots to
ProcessDFs. RecordFn aligns those fields in entity/time; CaseFn gives them
feature semantics; AIData assembles the final model vector.

Each external asset has one contract (`asset.yaml`) and its own versions
(`ExternalStore/<asset>/<version>/`); a lock pins the versions a SourceFn
uses. SourceFn looks each asset up explicitly by key and `obs_dt` and assigns
the fields by name. Training reads frozen versions only; live feature-store
or API providers are reached only when serving. Model:
`haipipe-data-external/ref/asset-model.md`.

---

The 6-Layer Pipeline
====================

```
Raw Data ----------------+
                         v
ExternalStore ------> Layer 1: Source  -- Raw + pinned external -> SourceSet tables
    |                    (code/haipipe/source_base/)
    |                    Chefs: code/haifn/fn_source/[<fn_version>/]
    v
Layer 2: Record  ------  SourceSet -> temporally-aligned RecordSet
    |                    (code/haipipe/record_base/)
    |                    Chefs: code/haifn/fn_record/[<fn_version>/]
    v
Layer 3: Case  --------  RecordSet -> event-triggered CaseSet
    |                    (code/haipipe/case_base/)
    |                    Chefs: code/haifn/fn_case/[<fn_version>/]
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

---

Current Code Structure
======================

Discover at runtime (always prefer ls over relying on this snapshot):

```bash
ls code/haipipe/          # core pipeline base classes
ls code/hainn/            # ML models and predictors
ls code/haifn/            # generated production functions
ls examples/*/tasks/b*/j*/t*/scripts/   # builder Task scripts (per project)
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
    |   +-- <fn_version>/           optional version folder (see Fn Versions below)
    +-- fn_record/                  HumanFn + RecordFn: entity + record processors
    |   +-- human/                  HumanFn files
    |   +-- record/                 RecordFn files
    |   +-- <fn_version>/{human,record}/
    +-- fn_case/                    TriggerFn + CaseFn: feature extractors
    |   +-- fn_trigger/             TriggerFn files
    |   +-- case_casefn/            CaseFn files
    |   +-- <fn_version>/{fn_trigger,case_casefn}/
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

New builders live inside canonical BJTR Task Folders:

```bash
ls examples/*/tasks/b*/j*/t*/scripts/    # all canonical Task script lanes
```

```text
tasks/bNN_<stage>store/jNN_<fnkind>_<topic>/tNN_<fnkind>_<FnName>/scripts/<builder>.py
```

Where each Fn kind lives (rule and reasons: `haipipe-task/ref/hierarchy.md`
§ Block number ranges; Block trees: `haipipe-task-for-data` § SourceFn Block
pattern):

```text
Fn kind     Block             topic Job (j01-j49, built once)   dataset Job (j51-j99)
raw         b00_rawdata       none                              j5N_<cohort>_v<yymmdd>_raw
SourceFn    b01_sourcestore   j0N_procdf_<topic> (contracts)    j5N_<cohort>_v<yymmdd>_source (t01 builds the SourceFn)
HumanFn     b02_recordstore   j01_recordfn_cohort, t01_humanfn  j5N_<cohort>_v<yymmdd>_record
RecordFn    b02_recordstore   j0N_recordfn_<topic>              (same as above)
TriggerFn   b03_casestore     j0N_triggerfn_<name>              j5N_<cohort>_v<yymmdd>_case
CaseFn      b03_casestore     j0N_casefn_<family>               (same as above)
TfmFn       b10_aidatastore   j0N_tfmfn_<name>                  j5N_<aidataset>_aidata (merges datasets)
SplitFn     b10_aidatastore   j0N_splitfn_<name>                (same as above)
```

A `j5N` number is the same raw dataset in `b00` to `b03`. In `b10` it names an
AIDataSet, which may merge several raw datasets, so it has its own number;
the AIData Block is `b10`, not `b04`, so the numbers are never read as the
same dataset (JL 260925). Task
folders keep the real CamelCase Fn name (`t02_recordfn_REACHPatientUniverse`).
Reference: REACH-SPACE `examples/Project-REACH-PD2D/tasks/`.

---

Fn Versions
===========

One dataset's Source, Record and Case Fns can live in ONE shared version
folder, so a set of Fns that belong together changes together:

```text
code/haifn/fn_source/<fn_version>/<SourceFnName>.py
code/haifn/fn_record/<fn_version>/human/<HumanFnName>.py
code/haifn/fn_record/<fn_version>/record/<RecordFnName>.py
code/haifn/fn_case/<fn_version>/fn_trigger/<TriggerFnName>.py
code/haifn/fn_case/<fn_version>/case_casefn/<CaseFnName>.py
```

Name it `v<Label><yymmdd>`. The first one is `vDfExt260923` (DrFirst
OptTimeR1 Extended).

Selection. A Run config says `fn_version: vDfExt260923` at its top level.
A haistep cook Run (`haistep-source`, `-record`, `-case`) gets it from the
step bootstrap, which copies it into `SPACE['FN_VERSION']`. Every Fn loader
then resolves its folder with `haipipe.base.fn_dir(SPACE, '<fn_stage>/<sub>')`.
With `FN_VERSION` unset, `fn_dir` returns the flat folder. The flat folders stay the default,
so a project that never sets `fn_version` is unchanged. SourceSet, RecordSet
and CaseSet manifests record the `fn_version` they were built with.

When to make a new version. The version is the contract of the
`ProcName_to_ProcDf` a SourceFn returns. While the SourceFn's output keeps the
same ProcNames and columns, keep the version, even if its code changes. When
that shape changes, make a new version and rebuild the SourceFn, RecordFns and
CaseFns into it together. They share one version because the RecordFns read
the ProcDf columns and the CaseFns read the RecordFn outputs. `fn_aidata`,
`fn_endpoint` and `fn_model` are not versioned this way.

Rules.
- Every b01, b02 and b03 Run of one dataset Job (`j5N_*`) carries the same
  `fn_version:`.
- A builder writes to `fn_dir(SPACE, '<fn_stage>/<sub>')` and never hard-codes
  the flat path. A builder Run sets `fn_version:` in its own config and reads
  it itself:

  ```python
  from haipipe.base import fn_dir, fn_version_from_config
  FN_VERSION = fn_version_from_config()          # top-level fn_version: of $RUN_CONFIG
  if FN_VERSION:
      SPACE['FN_VERSION'] = FN_VERSION
  output_dir = fn_dir(SPACE, 'fn_record/record')  # fn_record/<fn_version>/record
  ```

- One builder serves both layouts: its flat Run (`r01_regen_fn`) has no
  `fn_version:`, and its version Run (`r02_build_<fn_version>`) has one.
- A new version starts as a copy of the builders, never a hand-edit of
  generated Fns.
- An endpoint Input2SrcFn that reuses a versioned SourceFn loads it from
  `fn_source/<fn_version>/` by name and records the version it expects.

The following pre-BJTR tree is a legacy snapshot and remains readable only:

```
examples/Project-REACH-ADHD/tasks/
+-- A01_data_pipeline_reachadhd/
|   +-- 01_source_fn_develop_reachadhd/    SourceFn builders   (c<N>_build_source_*.py)
|   +-- 02_record_fn_develop_reachadhd/    HumanFn + RecordFn builders
|   |                                          h<N>_build_human_*.py
|   |                                          r<N>_build_records_*.py
|   +-- 03_case_fn_develop_reachadhd/      TriggerFn + CaseFn builders
|   |                                          a<N>_build_trigger_*.py
|   |                                          c<N>_build_casefn_*.py
|   +-- 04_aidata_fn_develop_reachadhd/    TfmFn + SplitFn builders
|                                              c<N>_build_transforms_*.py
|                                              s<N>_build_splitfn_*.py
+-- B01_training_xgboost_adhd/
|   +-- 00_model_fn_develop_reachadhd/     ModelFn builders
+-- C01_endpoint_reachadhd/
    +-- 00_endpoint_set_fn_develop_reachadhd/  EndpointFn builders
                                               a<N>_build_metafn_*.py
                                               b<N>_build_trigfn_*.py ...
```

Do not scaffold that legacy shape. Canonical Tasks keep builders in `scripts/`,
Run configs in `scripts/config/`, Tickets in `runs/`, and receipts in
`results/rNN_<run>/`.
Legacy workspaces (e.g.
WellDoc-SPACE) may still keep builders in a central `code-dev/1-PIPELINE/<N>-<Stage>-WorkSpace/` — same builder pattern, different home.

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
+-- ExternalStore/          Versioned reusable data inputs to SourceFn
|       <asset>/asset.yaml + <asset>/<version>/ ; _locks/ ; legacy @{tag}/
+-- 1-SourceStore/          Layer 1 output: SourceSets
|       {CohortName}/@{SourceFnName}/
+-- 2-RecStore/             Layer 2 output: RecordSets
|       {CohortName}_v{N}RecSet/
+-- 3-CaseStore/            Layer 3 output: CaseSets
|       {RecSetName}/@v{N}CaseSet-{TriggerFolder}/
+-- 4-AIDataStore/          Layer 4 output: AIDataSets
|       {ParentSetName}/@v{N}AIData-{aidata_name}/
+-- 5-ModelInstanceStore/   Layer 5 output: trained models
|       {model_name}/
+-- 6-EndpointStore/        Layer 6 output: deployment packages
        {endpoint_name}/
```

To see what is currently available at each layer:

```bash
ls _WorkSpace/1-SourceStore/            # available cohorts (Source)
ls _WorkSpace/2-RecStore/               # available RecordSets
ls _WorkSpace/3-CaseStore/              # available CaseSets
ls _WorkSpace/4-AIDataStore/            # available AIDataSets
ls _WorkSpace/5-ModelInstanceStore/     # available trained models
```

---

Current Config Structure
========================

Pipeline configs live INSIDE each pipeline task folder — there is no repo-root config/ directory:

```bash
ls examples/*/tasks/b*/j*/t*/scripts/config/  # all pipeline Run configs
ls code/scripts/haistepconfig/            # framework reference templates ONLY
                                          # (never put real project configs here)
```

---

Prerequisites (Universal)
==========================

Every haipipe operation requires these two commands run together:

```bash
source .venv/bin/activate && source env.sh
```

Never run Python without .venv activated.
Never skip env.sh.
The env.sh sets all _WorkSpace path environment variables.

---

MUST DO
=======

1. **Read this file** when starting any haipipe task to orient yourself
2. **Check the layer order** -- always work sequentially (1->2->3->4), with
   ExternalStore entering through SourceFn
3. **Discover Fns with ls** -- never assume what is registered
4. **Use the layer-specific ref file** after reading this overview
5. **Present plan to user and get approval** before any code changes

---

MUST NOT
========

1. **NEVER edit** code/haifn/ directly -- it is 100% generated
2. **NEVER run** Python without .venv activated and env.sh sourced
3. **NEVER skip layers** -- output of layer N is input to layer N+1
4. **NEVER create** new skill files with project-specific state
5. **NEVER commit** without explicit user request
