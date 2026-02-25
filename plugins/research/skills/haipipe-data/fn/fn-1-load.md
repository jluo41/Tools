fn-load: Load and Inspect a Set Asset at Any Pipeline Stage
============================================================

This file is stage-agnostic. Stage-specific details are in the Per-Stage Reference
section below. When a dispatch table loads this file alongside a stage ref file,
the ref file provides the active stage context (store path, API, key checks).

Use this file to: load an existing Set from disk and inspect its contents.

---

Overview
--------

Every pipeline stage produces a Set asset saved to _WorkSpace/:

  1-source  -> SourceSet  -> _WorkSpace/1-SourceStore/
  2-record  -> RecordSet  -> _WorkSpace/2-RecStore/
  3-case    -> CaseSet    -> _WorkSpace/3-CaseStore/
  4-aidata  -> AIDataSet  -> _WorkSpace/4-AIDataStore/

All load APIs require SPACE (workspace root path). None of them accept
set_name= or store_key= arguments -- always use path= with the full
relative or absolute path to the asset directory.

---

Stage-Independent Protocol
---------------------------

**Step 1: Check Prerequisites**

  source .venv/bin/activate
  source env.sh

  NOTE: source .venv/bin/activate does NOT persist across Bash tool calls.
  Always chain: source .venv/bin/activate && source env.sh && python <script>
  Or call venv Python directly: .venv/bin/python script.py

  Verify env variables are set:
    echo $LOCAL_SOURCE_STORE
    echo $LOCAL_RECORD_STORE
    echo $LOCAL_CASE_STORE
    echo $LOCAL_AIDATA_STORE

  If SPACE is needed in Python:
    import os
    SPACE = os.environ.get('SPACE', '.')

**Step 2: Discover Available Assets**

  ls _WorkSpace/1-SourceStore/
  ls _WorkSpace/2-RecStore/
  ls _WorkSpace/3-CaseStore/
  ls _WorkSpace/4-AIDataStore/

  Drill into a specific asset:
    ls _WorkSpace/3-CaseStore/<RecSetName>/
    ls _WorkSpace/3-CaseStore/<RecSetName>/@v<N>CaseSet-<Trigger>/

  Look for manifest.json at each asset root to confirm it was saved cleanly.

**Step 3: Load the Set Using the Correct API**

  See Per-Stage Reference below for the exact import and load call.
  All stages follow the same pattern:

    from haipipe.<stage>_base import <SetClass>
    my_set = <SetClass>.load_from_disk(path='<path_to_asset>', SPACE=SPACE)

  Use the path= argument with the full path to the versioned asset directory.
  Do NOT pass set_name= or store_key= -- these are not supported.

**Step 4: Inspect Contents**

  Every Set has an .info() method:
    my_set.info()

  Stage-specific inspection patterns are in Per-Stage Reference below.

**Step 5: Verify Integrity**

  Check manifest.json exists:
    import json, os
    manifest_path = os.path.join('<asset_path>', 'manifest.json')
    with open(manifest_path) as f:
        manifest = json.load(f)
    print(json.dumps(manifest, indent=2))

  Check row counts are non-zero.
  Check schema matches expected columns (see per-stage key checks).

---

Per-Stage Reference
-------------------

_______________________________________________
STAGE 1-source
_______________________________________________

**Store path:**
  _WorkSpace/1-SourceStore/{CohortName}/@{SourceFnName}/

**Load API:**

  from haipipe.source_base import SourceSet

  source_set = SourceSet.load_from_disk(
      path='_WorkSpace/1-SourceStore/<CohortName>/@<SourceFnName>',
      SPACE=SPACE
  )

  # WRONG -- these arguments are NOT supported:
  # SourceSet.load_from_disk(set_name='...', store_key='...')

**Inspect:**

  # List all table names
  print(list(source_set.ProcName_to_ProcDf.keys()))

  # Row/col counts per table
  for name, df in source_set.ProcName_to_ProcDf.items():
      print(f'{name}: {df.shape[0]} rows, {df.shape[1]} cols')

  # Full summary
  source_set.info()

**Key checks:**
  1. All expected tables exist in ProcName_to_ProcDf
  2. Schema column counts: Medication=11, Exercise=13, Diet=15
  3. Row counts are non-zero for all expected tables
  4. PatientID column present and consistent across all tables
  5. JSON metadata columns present (external_metadata, medication, nutrition, exercise)
     -- spot-check: print(df['medication'].iloc[0]) to verify JSON is parseable
  6. DateTime columns parseable as datetime (not raw strings):
     -- pd.to_datetime(df['ObservationDateTime'], errors='coerce').isna().sum() should be 0
  7. manifest.json exists at _WorkSpace/1-SourceStore/{CohortName}/@{SourceFnName}/

**Common gotchas:**
  - load_from_disk takes path=, NOT set_name= or store_key=
  - The @ prefix in the directory name (@{SourceFnName}) is literal -- include it in path
  - ProcName_to_ProcDf is a dict; iterate .items() not .keys() alone

_______________________________________________
STAGE 2-record
_______________________________________________

**Store path:**
  _WorkSpace/2-RecStore/{CohortName}_v{N}RecSet/

  CRITICAL: The directory layout is FLAT, not hierarchical.
  Human-{Name}/ and Record-{Name}.{RecFn}/ are all at the SAME level
  inside the RecSet directory. Do not expect nested subdirectories.

**Load API:**

  from haipipe.record_base import RecordSet

  # Option A: full path
  record_set = RecordSet.load_from_disk(
      path='_WorkSpace/2-RecStore/<CohortName>_v<N>RecSet',
      SPACE=SPACE
  )

  # Option B: relative asset path
  record_set = RecordSet.load_asset(
      path='<CohortName>_v<N>RecSet',
      SPACE=SPACE
  )

  # WRONG -- these arguments are NOT supported:
  # RecordSet.load_from_disk(set_name='...', store_key='...')

**Inspect:**

  # List all keys in the set
  for key in record_set.Name_to_HRF:
      print(key)
  # String keys = Human entries (e.g., 'OhioHuman')
  # Tuple keys  = Record entries (e.g., ('OhioHuman', 'OhioCGMRecord'))

  # Access a Human entry (string key)
  human = record_set.Name_to_HRF['<HumanFnName>']

  # Access a Record entry (tuple key)
  record = record_set.Name_to_HRF[('<HumanFnName>', '<RecordFnName>')]

  # Full summary
  record_set.info()

**Key checks:**
  - Name_to_HRF contains both string (Human) and tuple (Record) keys
  - Each Human entry contains patient demographics
  - Each Record entry is time-indexed with 5-min alignment
  - manifest.json exists at _WorkSpace/2-RecStore/{CohortName}_v{N}RecSet/
  - _cache/ directory present (HuggingFace Datasets cache)

**Common gotchas:**
  - FLAT layout: do not look for nested Human/{name}/Record/{name}/ hierarchy
  - Access via Name_to_HRF dict, not record_set.humans or record_set.records
  - String keys vs tuple keys: Human uses string, Record uses 2-tuple
  - load_from_disk takes path=, NOT set_name= or store_key=

_______________________________________________
STAGE 3-case
_______________________________________________

**Store path:**
  _WorkSpace/3-CaseStore/{RecSetName}/@v{N}CaseSet-{TriggerFolder}/

  CRITICAL layout:
    df_case.parquet           <- main case table (NOT case_data.parquet)
    @{CaseFnName}.parquet     <- one file per CaseFn, at ROOT (NOT in subdirectory)
    cf_to_cfvocab.json        <- token vocabulary per CaseFn
    manifest.json

**Load API:**

  from haipipe.case_base import CaseSet

  # Full load
  case_set = CaseSet.load_from_disk(
      path='_WorkSpace/3-CaseStore/<RecSetName>/@v<N>CaseSet-<Trigger>',
      SPACE=SPACE
  )

  # Selective load (only specific CaseFns)
  case_set = CaseSet.load_from_disk(
      path='_WorkSpace/3-CaseStore/<RecSetName>/@v<N>CaseSet-<Trigger>',
      SPACE=SPACE,
      CaseFn_list=['<CaseFnName1>', '<CaseFnName2>']
  )

  # WRONG -- these arguments are NOT supported:
  # CaseSet.load_from_disk(set_name='...', store_key='...')

**Inspect:**

  # Total case count
  print('Cases:', len(case_set.df_case))

  # Columns in the main case table
  print('Case columns:', list(case_set.df_case.columns))

  # Each CaseFn dataframe
  for cf_name, cf_df in case_set.CaseFn_to_df.items():
      print(f'{cf_name}: {cf_df.shape[0]} rows, {cf_df.shape[1]} cols')

  # Full summary
  case_set.info()

**Key checks:**
  - Row counts match across df_case and each @CaseFn dataframe
  - Feature columns have expected suffixes: --tid (token ID), --wgt (weight), --val (value)
  - ObsDT column present and date range is reasonable
  - cf_to_cfvocab.json has entries for each loaded CaseFn
  - @CaseFn.parquet files exist at ROOT (not in a subdirectory)
  - manifest.json exists at the CaseSet root

**Common gotchas:**
  - Main file is df_case.parquet -- do NOT look for case_data.parquet
  - @CaseFn.parquet files are at ROOT, not inside a casefn/ or data/ subdirectory
  - The @ prefix in @CaseFn.parquet is literal
  - load_from_disk takes path=, NOT set_name= or store_key=
  - CaseFn_list for selective loading uses CaseFn names WITHOUT the @ prefix

_______________________________________________
STAGE 4-aidata
_______________________________________________

**Store path:**
  _WorkSpace/4-AIDataStore/{aidata_name}/@{aidata_version}/

  CRITICAL layout:
    train/                  <- HuggingFace Dataset split
    validation/             <- HuggingFace Dataset split
    test-id/                <- HuggingFace Dataset split (in-distribution)
    test-od/                <- HuggingFace Dataset split (out-of-distribution, may not exist)
    cf_to_cfvocab.json      <- vocab at ROOT (NO vocab/ subdirectory)
    feat_vocab.json         <- feature vocab at ROOT (NO vocab/ subdirectory)
    manifest.json

**Load API:**

  from haipipe.aidata_base.aidata_set import AIDataSet

  # Option A
  aidata_set = AIDataSet.load_from_disk(
      path='_WorkSpace/4-AIDataStore/<aidata_name>/@<version>',
      SPACE=SPACE
  )

  # Option B
  aidata_set = AIDataSet.load_asset(
      path='_WorkSpace/4-AIDataStore/<aidata_name>/@<version>',
      SPACE=SPACE
  )

  # WRONG -- these arguments are NOT supported:
  # AIDataSet.load_from_disk(set_name='...', store_key='...')

**Inspect:**

  # All splits with sizes and features
  for split_name, dataset in aidata_set.dataset_dict.items():
      print(f'{split_name}: {len(dataset)} samples')
      print(f'  features: {dataset.column_names}')

  # Vocabulary info
  print('feat_vocab keys:', list(aidata_set.feat_vocab.keys()))
  print('CF_to_CFVocab keys:', list(aidata_set.CF_to_CFVocab.keys()))

  # Full summary
  aidata_set.info()

**Key checks:**
  - Splits present: train, validation, test-id (test-od optional)
  - Feature column dimensions match model input expectations
  - cf_to_cfvocab.json and feat_vocab.json at ROOT (not in vocab/ subdir)
  - manifest.json exists at the AIDataSet version root
  - Sample counts are non-zero for train and validation

**Common gotchas:**
  - No vocab/ subdirectory -- vocab files are at ROOT of the version dir
  - load_from_disk takes path=, NOT set_name= or store_key=
  - dataset_dict is a HuggingFace DatasetDict; iterate .items() not .values()
  - test-od split may not exist if no out-of-distribution data was configured

---

MUST DO (All Stages)
---------------------

1. Activate .venv AND source env.sh before any Python load call
2. Use path= argument with the full path -- never set_name= or store_key=
3. Include the @ prefix in paths where required (e.g., @{SourceFnName}, @v0CaseSet-*)
4. Run .info() on the loaded Set to get a structured summary before deep inspection
5. Check manifest.json exists -- if missing, the asset was not saved cleanly (re-run stage)
6. For Stage 3: look for @-prefixed .parquet files at ROOT, not in a subdirectory
7. For Stage 4: look for vocab files (cf_to_cfvocab.json, feat_vocab.json) at ROOT

---

MUST NOT (All Stages)
----------------------

1. NEVER pass set_name= or store_key= to any load_from_disk call
2. NEVER look for case_data.parquet -- the Stage 3 file is df_case.parquet
3. NEVER expect a vocab/ subdirectory in Stage 4 -- vocab files are at ROOT
4. NEVER assume assets exist -- always run ls first to discover
5. NEVER skip checking row counts -- zero rows means a bug in the upstream stage
