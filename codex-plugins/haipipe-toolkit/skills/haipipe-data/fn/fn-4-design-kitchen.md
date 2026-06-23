fn-design-kitchen: Modify the Pipeline Infrastructure (Base Classes)
=====================================================================

**Purpose**: Edit the `code/haipipe/` framework itself — base classes,
pipeline orchestrators, Asset I/O, and Fn loaders. This is an advanced
operation. Most users do NOT need this file.

**When to use this file**: Only when the framework behavior needs to change
(new caching strategy, new serialization format, new remote backend, new
windowing logic). For adding new feature functions, use `fn-design-chef.md`.

---

Overview
---------

The pipeline infrastructure lives in `code/haipipe/`, organized by stage:

```
code/haipipe/
├── source_base/       Stage 1: raw data loading
├── record_base/       Stage 2: patient record alignment
├── case_base/         Stage 3: case triggering and feature extraction
├── aidata_base/       Stage 4: ML dataset construction
├── assets.py          Unified Asset I/O base class (all stages)
└── base.py            YAML config resolution with @ references
```

Unlike `code/haifn/` (generated), everything in `code/haipipe/` is editable.
But changes here affect ALL Fns and ALL pipelines simultaneously, so
backward compatibility is critical.

---

Universal Protocol (All Stages)
---------------------------------

**Step 1: Present Plan to User, Get Approval**

Before touching any file, present:
- Which base class file you will edit
- What API or behavior changes
- Which existing Fns or configs will be affected
- How backward compatibility will be preserved

Do NOT proceed until the user approves.

**Step 2: Activate .venv and source env.sh**

```bash
source .venv/bin/activate
source env.sh
```

Both required. Tests and pipelines need SPACE paths.

**Step 3: Edit the Relevant Base Class File**

```
code/haipipe/<layer>_base/<specific_file>.py
```

Work within the three-class pattern for the stage (see per-stage reference
below). Keep the same class and function signatures unless you have a strong
reason to change them and have user approval.

**Step 4: Run Existing Tests to Verify Backward Compatibility**

```bash
pytest test/ -m unit -v
pytest test/ -m integration -v
```

All existing tests must continue to pass. If a test fails, fix the
regression before proceeding.

**Step 5: Test End-to-End with Real Data**

```bash
haistep-source --config config/test-haistep-ohio/1_test_source.yaml
haistep-record --config config/test-haistep-ohio/2_test_record.yaml
haistep-case   --config config/test-haistep-ohio/3_test_case.yaml
haistep-aidata --config config/test-haistep-ohio/4_test_aidata.yaml
```

Use the Ohio test config as the standard end-to-end validation path.

---

Stage Reference: 1-source
===========================

**What You Edit**:
```
code/haipipe/source_base/source_pipeline.py   — orchestration, caching, validation
code/haipipe/source_base/source_set.py        — SourceSet Asset I/O
code/haipipe/source_base/source_utils.py      — shared utilities
code/haipipe/source_base/builder/sourcefn.py  — dynamic SourceFn loader
```

**Three-Class Architecture**:

```
Source_Pipeline
    |-- dynamically loads SourceFn module from code/haifn/fn_source/
    |-- calls process_Source_to_Processed(...)
    |-- wraps result in SourceSet
    v
SourceFn Loader (builder/sourcefn.py)
    |-- reads: SourceFile_SuffixList, ProcName_List,
    |           ProcName_to_columns, process_Source_to_Processed, MetaDict
    |-- validates schema against ProcName_to_columns
    v
SourceSet (source_set.py)
    |-- inherits from Asset
    |-- save_to_disk / load_from_disk / load_asset
    |-- naming: {raw_data_name}/@{SourceFnName}
```

**API Contracts to Preserve**:

```python
# Source_Pipeline.run() — do not change this signature
Source_Pipeline.run(
    raw_data_name,
    raw_data_path=None,
    payload_input=None,
    use_cache=True,
    save_cache=True,
) -> SourceSet

# SourceSet I/O — do not change these signatures
SourceSet.load_from_disk(path, SPACE)
SourceSet.load_asset(path, SPACE)

# SourceFn loader contract — changing this breaks ALL SourceFns
# The loader reads these module-level attributes from each SourceFn:
#   SourceFile_SuffixList, ProcName_List, ProcName_to_columns,
#   process_Source_to_Processed, MetaDict

# Asset naming convention
asset_name = f"{raw_data_name}/@{SourceFnName}"
```

**When to Use**:
- New caching strategies (e.g., content-hash-based invalidation)
- Schema validation logic changes
- New remote storage backends (S3, GCS, Databricks)
- SourceSet serialization format changes
- SourceFn loader contract changes (requires updating ALL SourceFn builders)

---

Stage Reference: 2-record
===========================

**What You Edit**:
```
code/haipipe/record_base/record_pipeline.py   — orchestration, partitioning, caching
code/haipipe/record_base/record_set.py        — RecordSet Asset I/O
code/haipipe/record_base/assets.py            — record-specific Asset extensions
code/haipipe/record_base/builder/human.py     — HumanFn loader
code/haipipe/record_base/builder/record.py    — RecordFn loader
```

**Three-Class Architecture**:

```
Record_Pipeline
    |-- loads HumanFn from code/haifn/fn_record/human/
    |-- loads RecordFn from code/haifn/fn_record/record/
    |-- partitions processing across CPUs
    |-- aligns signals to 5-minute time grid
    v
HumanFn Loader + RecordFn Loader
    |-- HumanFn reads: OneHuman_Args, Excluded_RawNameList,
    |                  get_RawHumanID_from_dfRawColumns, MetaDict
    |-- RecordFn reads: OneRecord_Args, RawName_to_RawConfig,
    |                   attr_cols, get_RawRecProc_for_HumanGroup
    v
RecordSet (record_set.py)
    |-- inherits from Asset
    |-- FLAT directory layout (no nesting):
    |     Human-{Name}/             <- one dir per HumanFn
    |     Record-{Name}.{RecFn}/    <- one dir per RecordFn
    |-- save_to_disk / load_from_disk / load_asset
```

**API Contracts to Preserve**:

```python
# Record_Pipeline.run() — do not change this signature
Record_Pipeline.run(
    source_set,
    partition_index,
    partition_number,
    record_set_label,
    use_cache,
    save_cache,
    profile,
) -> RecordSet

# RecordSet I/O
RecordSet.load_from_disk(path, SPACE)
RecordSet.load_asset(path, SPACE)

# Name_to_HRF dict structure — key type encodes entity type
Name_to_HRF = {
    'HumanFnName': ...,            # string key -> Human entity
    ('HumanFnName', 'RecFn'): ..., # tuple key  -> Record entity
}

# FLAT directory layout — must not add nesting
#   Human-{Name}/
#   Record-{Name}.{RecFn}/
#   (both at same directory level in RecordSet root)
```

**When to Use**:
- New temporal alignment strategies (e.g., variable-interval grids)
- New entity ID mapping logic
- RecordSet serialization format changes
- New partitioning modes (e.g., patient-stratified vs. time-stratified)
- Changes to how attr_cols are validated against downstream CaseFns

---

Stage Reference: 3-case
=========================

**What You Edit**:
```
code/haipipe/case_base/case_pipeline.py        — orchestration, trigger, multiprocessing
code/haipipe/case_base/case_set.py             — CaseSet Asset I/O
code/haipipe/case_base/case_utils.py           — shared utilities
code/haipipe/case_base/builder/triggerfn.py    — TriggerFn loader
code/haipipe/case_base/builder/casefn.py       — CaseFn loader
code/haipipe/case_base/builder/rotools.py      — Record Object windowing utilities
```

**Three-Class Architecture**:

```
Case_Pipeline
    |-- loads TriggerFn from code/haifn/fn_case/fn_trigger/
    |-- calls get_CaseTrigger_from_RecordBase -> {df_case, df_lts, df_Human_Info}
    |-- loads CaseFns from code/haifn/fn_case/case_casefn/
    |-- for each case row: assembles ROName_to_ROData, calls fn_CaseFn(...)
    |-- prepends CaseFnName to each returned key
    |-- supports multiprocessing via CaseProgressPipeline
    v
TriggerFn Loader + CaseFn Loader + ROTools
    |-- TriggerFn: reads Trigger, Trigger_Args,
    |              get_CaseTrigger_from_RecordBase
    |-- CaseFn: reads CaseFnName, RO_to_ROName, Ckpd_to_CkpdObsConfig,
    |           ROName_to_RONameInfo, HumanRecords, COVocab, fn_CaseFn
    |-- ROTools: windowing logic for Record Objects (before/after/range)
    v
CaseSet (case_set.py)
    |-- inherits from Asset
    |-- ROOT layout:
    |     df_case.parquet           <- one row per triggered case
    |     @{CaseFnName}.parquet     <- feature columns for each CaseFn
    |     cf_to_cfvocab.json        <- controlled vocabularies
    |-- save_to_disk / load_from_disk / load_asset
```

**API Contracts to Preserve**:

```python
# Case_Pipeline.run() — do not change this signature
Case_Pipeline.run(
    df_case,
    df_case_raw,
    record_set,
    use_cache,
    profile,
) -> CaseSet

# fn_CaseFn contract — 6 positional params, suffix-only return keys
def fn_CaseFn(
    case_example,       # dict: one case row
    ROName_list,        # list[str]: which ROs to load
    ROName_to_ROData,   # dict[str, DataFrame]: windowed data per RO
    ROName_to_ROInfo,   # dict[str, dict]: metadata per RO
    COVocab,            # dict: controlled vocabulary
    context,            # dict: pipeline context (date, config, etc.)
) -> dict:              # suffix-only keys: --tid, --wgt, --val, --str
    ...

# TriggerFn function name — must be exactly this string
"get_CaseTrigger_from_RecordBase"

# CaseSet directory layout (ROOT-level, no subdirectories)
#   df_case.parquet
#   @CGMValueBf24h.parquet
#   @PDemoBase.parquet
#   cf_to_cfvocab.json

# ROName_to_ROData interface — dict keyed by 3-part ROName
ROName_to_ROData = {
    'hOhioHuman.rOhioCGM.cBf24h': pd.DataFrame(...),
    ...
}
```

**When to Use**:
- New RO windowing strategies in `rotools.py` (e.g., new window types)
- New CaseProgressPipeline modes (e.g., incremental case generation)
- FeatureContext cache changes
- CaseSet serialization format changes
- New multiprocessing strategies for large case sets

---

Stage Reference: 4-aidata
===========================

**What You Edit**:
```
code/haipipe/aidata_base/aidata_pipeline.py    — orchestration, split, transform
code/haipipe/aidata_base/aidata_set.py         — AIDataSet Asset I/O
code/haipipe/aidata_base/aidata_utils.py       — shared utilities
code/haipipe/aidata_base/builder/tfmfn.py      — InputTfmFn/OutputTfmFn loaders
code/haipipe/aidata_base/builder/splitfn.py    — SplitFn loader
```

**Three-Class Architecture**:

```
AIData_Pipeline
    |-- three run modes:
    |     Mode A: from CaseSet (full pipeline)
    |     Mode B: from DataFrame (skip trigger/case)
    |     Mode C: single case (inference)
    |-- loads SplitFn -> calls dataset_split_tagging_fn(df_tag, SplitArgs)
    |-- loads InputTfmFn -> calls build_vocab_fn, then tfm_fn per case
    |-- loads OutputTfmFn -> calls tfm_fn per case
    v
TfmFn Loader + SplitFn Loader
    |-- InputTfmFn: reads build_vocab_fn (2 params), tfm_fn (4 params)
    |-- OutputTfmFn: reads tfm_fn (2 params)
    |-- SplitFn: reads dataset_split_tagging_fn (2 params)
    v
AIDataSet (aidata_set.py)
    |-- inherits from Asset
    |-- HuggingFace DatasetDict (train/val/test splits)
    |-- ROOT layout (no vocab/ subdirectory):
    |     dataset/                  <- HuggingFace DatasetDict
    |     feat_vocab.json           <- at ROOT, not in vocab/
    |     cf_to_cfvocab.json        <- at ROOT
    |-- save_to_disk / load_from_disk / load_asset
```

**API Contracts to Preserve**:

```python
# AIData_Pipeline three run modes — all must continue to work
# Mode A: from CaseSet (full pipeline)
pipeline.run(case_set=case_set, aidata_name='<name>', aidata_version='v0')
# Mode B: from DataFrame (skip trigger/case, pass df directly)
pipeline.run(df_case=test_df, mode='inference')
# Mode C: single case (inference)
pipeline.run(case_example=single_case, mode='inference')

# build_vocab_fn — 2 params exactly
def build_vocab_fn(InputArgs, CF_to_CFVocab) -> dict: ...

# InputTfmFn tfm_fn — 4 params exactly
def tfm_fn(case_features, InputArgs, CF_to_CFvocab, feat_vocab=None) -> dict: ...

# OutputTfmFn tfm_fn — 2 params exactly (NOT 4!)
def tfm_fn(case, OutputArgs) -> dict: ...

# SplitFn — adds split_ai column
def dataset_split_tagging_fn(df_tag, SplitArgs) -> pd.DataFrame:
    # df_tag gains 'split_ai' column with values 'train'/'validation'/'test-id'/'test-od'
    ...

# AIDataSet vocabulary file location — ROOT level, not in subdirectory
#   feat_vocab.json          <- at ROOT
#   cf_to_cfvocab.json       <- at ROOT
#   (NOT at vocab/feat_vocab.json)
```

**When to Use**:
- New split strategies at the framework level (new SplitFn base behavior)
- New vocabulary building logic that affects all InputTfmFns
- AIDataSet serialization format changes (e.g., switching from HuggingFace)
- New inference pipeline modes (e.g., streaming inference)
- Changes to how `feat_vocab` is cached and reused across runs

---

Universal MUST DO (All Stages)
================================

1. Present plan to user and get approval before editing any base class
2. Activate .venv: `source .venv/bin/activate && source env.sh`
3. Maintain backward compatibility with all existing Fns in `code/haifn/`
4. Run `pytest test/ -m unit -v` after changes — all must pass
5. Test end-to-end with `haistep-*` commands on the Ohio test config
6. Keep the Asset I/O contract: `save_to_disk / load_from_disk / load_asset`
7. Keep stage-to-stage naming conventions (asset naming, directory layout)

---

Universal MUST NOT (All Stages)
=================================

1. NEVER modify `code/haifn/` (generated code — use builders instead)
2. NEVER break stage-to-stage interface without updating both neighboring layers
3. NEVER change the Fn loader contract without updating all corresponding builders
   - Changing SourceFn loader contract -> must update all SourceFn builders
   - Changing CaseFn loader contract -> must update all CaseFn builders
4. NEVER remove cache support — many workflows depend on `use_cache=True`
5. NEVER change directory naming conventions without updating all config readers
6. NEVER change `fn_CaseFn` param count (must stay 6) without updating all CaseFn builders
7. NEVER change vocab file location from ROOT to a subdirectory without updating
   all AIDataSet load paths

---

Quick Reference: Base Class File Map
======================================

```
Stage | What Changed            | Edit File
------+-------------------------+------------------------------------------
  1   | Caching / validation    | source_base/source_pipeline.py
  1   | SourceSet serialization | source_base/source_set.py
  1   | SourceFn loader         | source_base/builder/sourcefn.py
------+-------------------------+------------------------------------------
  2   | Temporal alignment      | record_base/record_pipeline.py
  2   | RecordSet serialization | record_base/record_set.py
  2   | HumanFn loader          | record_base/builder/human.py
  2   | RecordFn loader         | record_base/builder/record.py
------+-------------------------+------------------------------------------
  3   | Trigger / extraction    | case_base/case_pipeline.py
  3   | CaseSet serialization   | case_base/case_set.py
  3   | RO windowing            | case_base/builder/rotools.py
  3   | TriggerFn loader        | case_base/builder/triggerfn.py
  3   | CaseFn loader           | case_base/builder/casefn.py
------+-------------------------+------------------------------------------
  4   | Split / transform       | aidata_base/aidata_pipeline.py
  4   | AIDataSet serialization | aidata_base/aidata_set.py
  4   | TfmFn loader            | aidata_base/builder/tfmfn.py
  4   | SplitFn loader          | aidata_base/builder/splitfn.py
```

```
Stage | Key API to Never Break
------+--------------------------------------------------------
  1   | Source_Pipeline.run(raw_data_name, ...) -> SourceSet
  2   | Record_Pipeline.run(source_set, partition_index, ...) -> RecordSet
  3   | Case_Pipeline.run(df_case, df_case_raw, record_set, ...) -> CaseSet
  3   | fn_CaseFn(case, ROName_list, ROData, ROInfo, COVocab, ctx) -> dict
  4   | AIData_Pipeline three run modes (caseset / dataframe / single)
  4   | build_vocab_fn(InputArgs, CF_to_CFVocab) -> dict (2 params)
  4   | input tfm_fn(case_features, InputArgs, CF_to_CFvocab, feat_vocab) (4 params)
  4   | output tfm_fn(case, OutputArgs) -> dict (2 params)
```
