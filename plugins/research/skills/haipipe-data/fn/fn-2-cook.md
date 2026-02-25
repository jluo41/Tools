fn-cook: Run a Pipeline with a YAML Config at Any Pipeline Stage
================================================================

This file is stage-agnostic. Stage-specific details are in the Per-Stage Reference
section below. When a dispatch table loads this file alongside a stage ref file,
the ref file provides the active stage context (CLI command, config keys, output path).

Use this file to: write or find a YAML config and execute a pipeline stage.

---

Overview
--------

The Kitchen is already built. Your job is to write the Recipe (YAML config) and
execute it. Each pipeline stage has:

  - A registered set of Fn modules (SourceFns, RecordFns, CaseFns, etc.)
  - A CLI command (haistep-<stage>) that runs the stage end-to-end
  - A Python API for programmatic control
  - A config template at templates/<N>-<stage>/config.yaml

Stages run sequentially. Each stage consumes the output of the previous stage:

  1-source -> SourceSet
      |
      v
  2-record -> RecordSet
      |
      v
  3-case   -> CaseSet
      |
      v
  4-aidata -> AIDataSet

**Sequential Pipeline Note:**
  Do NOT run stage N+1 if stage N output does not exist.
  Always verify each stage output before proceeding to the next.

---

Stage-Independent Steps
-----------------------

**Step 1: Activate .venv and source env.sh**

  source .venv/bin/activate
  source env.sh

  # Verify Python environment
  python -c "import haipipe, hainn, haifn; print('OK')"

  NOTE: source .venv/bin/activate does NOT persist across Bash tool calls.
  Always chain: source .venv/bin/activate && source env.sh && <command>
  Or call venv Python directly: .venv/bin/python script.py

  # Verify env variables
  echo $LOCAL_SOURCE_STORE
  echo $LOCAL_RECORD_STORE
  echo $LOCAL_CASE_STORE
  echo $LOCAL_AIDATA_STORE

**Step 2: Discover Registered Fns**

  # Source functions (what raw data processors exist)
  ls code/haifn/fn_source/

  # Human and Record functions
  ls code/haifn/fn_record/human/
  ls code/haifn/fn_record/record/

  # Trigger functions and Case functions
  ls code/haifn/fn_case/fn_trigger/
  ls code/haifn/fn_case/case_casefn/

  # AIData input transforms and split functions
  ls code/haifn/fn_aidata/entryinput/
  ls code/haifn/fn_aidata/split/

**Step 3: Write or Find a Config YAML**

  Start from a template:
    templates/1-source/config.yaml
    templates/2-record/config.yaml
    templates/3-case/config.yaml
    templates/4-aidata/config.yaml

  Or copy an existing config from config/ and modify it.
  See Per-Stage Reference below for required config keys per stage.

**Step 4: Run the Pipeline**

  CLI (recommended for one-off runs):
    haistep-<stage> --config <your_config>.yaml

  Python API (recommended for programmatic control or scripting):
    See Per-Stage Reference below for the exact API call.

**Step 5: Verify Output**

  Check the output directory exists and contains expected files.
  Load and inspect the output Set using fn-load.md protocols.
  Check manifest.json was written.

---

Per-Stage Reference
-------------------

_______________________________________________
STAGE 1-source
_______________________________________________

**CLI command:**

  haistep-source --config <your_config>.yaml

**Python API:**

  from haipipe.source_base import Source_Pipeline

  pipeline = Source_Pipeline(config, SPACE)
  source_set = pipeline.run(
      raw_data_name='<CohortName>',
      raw_data_path=None,       # optional: override default raw data path
      payload_input=None,       # optional: pass data directly
      use_cache=True,
      save_cache=True
  )

**Required config keys:**

  SourceArgs:
    raw_data_name: '<CohortName>'       # name of the raw cohort directory
    SourceFnName:  '<SourceFnName>'     # name of the fn in code/haifn/fn_source/

**Output path:**

  _WorkSpace/1-SourceStore/{raw_data_name}/@{SourceFnName}/

**Config template:**

  templates/1-source/config.yaml

**Discover SourceFns:**

  ls code/haifn/fn_source/
  # Each .py file (minus .py) is a valid SourceFnName

**Prerequisite:**

  Raw data must exist at _WorkSpace/0-RawDataStore/{raw_data_name}/
  If raw data is on remote, pull it first:
    hai-remote-sync --pull --rawdata --path 0-RawDataStore/{CohortName}
  SourceFnName must match an existing file in code/haifn/fn_source/

**Test script:**

  source .venv/bin/activate && source env.sh
  python test/test_haistep/test_1_source/test_source.py \
      --config <your_config>.yaml

**Verify:**

  ls _WorkSpace/1-SourceStore/{raw_data_name}/@{SourceFnName}/
  # Expected: one .parquet file per table + manifest.json

  # Load and inspect:
  # -> see fn-load.md STAGE 1-source section

_______________________________________________
STAGE 2-record
_______________________________________________

**CLI command:**

  haistep-record --config <your_config>.yaml

**Test script:**

  source .venv/bin/activate && source env.sh
  python test/test_haistep/test_2_record/test_record.py \
      --config <your_config>.yaml

**Python API:**

  from haipipe.record_base import Record_Pipeline

  pipeline = Record_Pipeline(config, SPACE)
  record_set = pipeline.run(
      source_set,                  # SourceSet from stage 1
      partition_index=None,        # optional: run only one partition
      partition_number=None,       # optional: total number of partitions
      record_set_label=1,          # version label (int)
      use_cache=True,
      save_cache=True
  )

**Required config keys:**

  source_set_name: '<CohortName>/@<SourceFnName>'  # REQUIRED: input SourceSet

  HumanRecords:                         # dict mapping Human -> [Record list]
    '<HumanFnName>':
      - '<RecordFnName1>'
      - '<RecordFnName2>'

  record_set_version: <N>               # integer version number

  # Alternative: keys nested under RecordArgs (both forms accepted)
  # source_set_name: '<CohortName>/@<SourceFnName>'
  # RecordArgs:
  #   HumanRecords:
  #     '<HumanFnName>': ['<RecordFnName1>', '<RecordFnName2>']
  #   record_set_version: 0
  #   record_set_label: 1
  #   use_cache: false
  #   save_cache: true

**Output name pattern:**

  {CohortName}_v{N}RecSet
  Saved to: _WorkSpace/2-RecStore/{CohortName}_v{N}RecSet/

**Config template:**

  templates/2-record/config.yaml

**Discover HumanFns and RecordFns:**

  ls code/haifn/fn_record/human/
  ls code/haifn/fn_record/record/

**Prerequisite:**

  SourceSet must exist:
    ls _WorkSpace/1-SourceStore/{CohortName}/@{SourceFnName}/
  If missing: run stage 1-source first.

**Verify:**

  ls _WorkSpace/2-RecStore/
  # Expected: {CohortName}_v{N}RecSet/ directory present

  ls _WorkSpace/2-RecStore/{CohortName}_v{N}RecSet/
  # Expected: Human-{Name}/ and Record-{Name}.{RecFn}/ dirs (FLAT) + manifest.json

  # Load and inspect:
  # -> see fn-load.md STAGE 2-record section

_______________________________________________
STAGE 3-case
_______________________________________________

**CLI command:**

  haistep-case --config <your_config>.yaml

**Test script:**

  source .venv/bin/activate && source env.sh
  python test/test_haistep/test_3_case/test_case.py \
      --config <your_config>.yaml

**Python API:**

  from haipipe.case_base import Case_Pipeline

  pipeline = Case_Pipeline(config, SPACE, context=None)
  case_set = pipeline.run(
      df_case=None,            # optional: pass existing df_case directly
      df_case_raw=None,        # optional: pass raw trigger dataframe
      record_set=record_set,   # RecordSet from stage 2
      use_cache=True,
      profile=False
  )

**Required config keys:**

  record_set_name: '<CohortName>_v<N>RecSet'

  CaseArgs:
    Case_Args:                          # list of case extraction configs
      - TriggerName: '<TriggerFnName>'
        CaseFnList:
          - '<CaseFnName1>'
          - '<CaseFnName2>'
        case_set_version: <N>           # integer version number

**LTS Trigger extra config (CGM5MinLTS only):**

  # Add inside Case_Args entry when TriggerName is CGM5MinLTS:
  min_segment_length: 288       # min points (288 = 24h at 5-min intervals)
  max_consecutive_missing: 3    # max gaps to interpolate (3 = 15 min)
  stride: 12                    # sampling frequency (12 x 5min = hourly)
  buffer_start: 240             # skip first 240 points (20 hours)
  buffer_end: 240               # skip last 240 points (20 hours)
  event_record_names: ['Diet5Min', 'Med5Min', 'Exercise5Min']

**ROName_to_RONameArgs (controls which Record Object data to load):**

  # Specify in Case_Args entry to control data loading per case:
  ROName_to_RONameArgs:
    'h<HumanFnName>.r<RecordFnName>':  # Human.Record pair
      attribute_columns:                # columns to load from this record
        - '<EntityID>'
        - '<DatetimeCol>'
        - '<ValueCol>'
      RecDT: '<DatetimeCol>'            # datetime column for alignment
    'h<HumanFnName>.r<StaticRecord>':  # static/demographic record
      attribute_columns:
        - '<EntityID>'
        - '<DemographicCol>'

**Output path:**

  _WorkSpace/3-CaseStore/{record_set_name}/@v{N}CaseSet-{TriggerFolder}/

**Config template:**

  templates/3-case/config.yaml

**Discover TriggerFns and CaseFns:**

  ls code/haifn/fn_case/fn_trigger/
  ls code/haifn/fn_case/case_casefn/

**Prerequisite:**

  RecordSet must exist:
    ls _WorkSpace/2-RecStore/{record_set_name}/
  If missing: run stage 2-record first.

**Verify:**

  ls _WorkSpace/3-CaseStore/{record_set_name}/
  # Expected: @v{N}CaseSet-{Trigger}/ directory present

  ls _WorkSpace/3-CaseStore/{record_set_name}/@v{N}CaseSet-{Trigger}/
  # Expected:
  #   df_case.parquet          (main case table -- NOT case_data.parquet)
  #   @{CaseFnName}.parquet    (one per CaseFn, at ROOT)
  #   cf_to_cfvocab.json
  #   manifest.json

  # Load and inspect:
  # -> see fn-load.md STAGE 3-case section

_______________________________________________
STAGE 4-aidata
_______________________________________________

**CLI command:**

  haistep-aidata --config <your_config>.yaml

**Test script:**

  source .venv/bin/activate && source env.sh
  python test/test_haistep/test_4_aidata/test_aidata.py \
      --config <your_config>.yaml

**Python API:**

  from haipipe.aidata_base import AIData_Pipeline

  pipeline = AIData_Pipeline(config, SPACE, cache_combined_case=True)

  # Path 1: CaseSet -> AIDataSet  (training — creates train/val/test splits)
  aidata_set = pipeline.run(
      case_set=my_case_set,      # CaseSet from stage 3
      aidata_name='<name>',      # name for this AIDataSet
      aidata_version='v0'        # version string (e.g., 'v0001')
  )

  # Path 2: DataFrame -> transformed DataFrame  (batch inference, no splitting)
  df_transformed = pipeline.run(df_case=test_df, mode='inference')

  # Path 3: Single case dict -> transformed dict  (single-case inference)
  result = pipeline.run(case_example=single_case, mode='inference')

**Config structure (3 parts):**

  SplitArgs:                              # optional
    SplitMethod: '<SplitFnName>'          # SplitFn name (capital M)
    ColumnName: '<split_column>'          # column assigned by SplitFn
    Split_to_Selection:
      train:
        Rules: [["split_ai", "==", "train"]]
        Op: "and"
      validation:
        Rules: [["split_ai", "==", "validation"]]
        Op: "and"
      test-id:
        Rules: [["split_ai", "==", "test-id"]]
        Op: "and"
      test-od:
        Rules: [["split_ai", "==", "test-od"]]
        Op: "and"

  InputArgs:                              # required
    input_method: '<InputTfmFnName>'
    input_casefn_list:
      - '<CaseFnName1>'
      - '<CaseFnName2>'

  OutputArgs:                             # optional
    output_method: '<OutputTfmFnName>'    # e.g., OutputSingleLabel
    output_casefn_list: []
    output_args: {}

**Output path:**

  _WorkSpace/4-AIDataStore/{aidata_name}/@{aidata_version}/

**Config template:**

  templates/4-aidata/config.yaml

**Discover Input TfmFns and SplitFns:**

  ls code/haifn/fn_aidata/entryinput/
  ls code/haifn/fn_aidata/split/

**Available SplitFns:**

  SplitFn Name        Description                       Key Config Params
  ------------------  --------------------------------  ----------------------------
  SplitByTimeBin      Temporal split by time bins       ColumnName, Split_to_Selection
  RandomByPatient     Random split respecting patients  PatientID column, ratios
  RandomByStratum     Stratified random split           stratum column, ratios

**Available Input TfmFns (feature transforms):**

  TfmFn Name                  Description                     Domain
  --------------------------  ------------------------------  ---------------------
  InputTEToken                Token embedding (general)       Any time series
  InputMultiCGMSeqNumeric     Multi-sequence numeric          Numeric sequences
  InputMultiCGMSeqConcat      Multi-sequence concatenated     Numeric sequences
  InputMultiCF                Multi case-feature tabular      Tabular features
  InputCGMEventText           Time series + events as text    Text models
  InputCGMEventJSON           Time series + events as JSON    JSON-based models
  InputCGMWithEventChannels   Time series with event channels Multi-channel sequences
  InputMultiSeqConcat         Multi sequences concatenated    Numeric sequences
  InputTemporalInterleaving   Temporally interleaved          Interleaved sequences
  CatInputMultiCFSparse       Sparse categorical features     Sparse tensors

**Available Output TfmFns (label transforms):**

  TfmFn Name             Description                    Output Format
  ---------------------  -----------------------------  --------------------
  OutputNextToken        Next-token prediction labels   token ID sequence
  OutputNumericForecast  Numeric forecasting labels     float array
  OutputSingleLabel      Single classification label    int

**Prerequisite:**

  CaseSet must exist with all required CaseFns:
    ls _WorkSpace/3-CaseStore/{record_set_name}/@v{N}CaseSet-{Trigger}/
  All CaseFn names in input_casefn_list must have a corresponding
  @{CaseFnName}.parquet at the CaseSet root.
  If missing CaseFns: re-run stage 3-case with the required CaseFns added.

**Verify:**

  ls _WorkSpace/4-AIDataStore/{aidata_name}/@{aidata_version}/
  # Expected:
  #   train/
  #   validation/
  #   test-id/
  #   test-od/              (may not exist if not configured)
  #   cf_to_cfvocab.json    <- at ROOT, no vocab/ subdirectory
  #   feat_vocab.json       <- at ROOT, no vocab/ subdirectory
  #   manifest.json

  # Load and inspect:
  # -> see fn-load.md STAGE 4-aidata section

---

MUST DO (All Stages)
---------------------

1. Activate .venv AND source env.sh in every Bash call that runs Python
2. Discover registered Fns with ls before writing config (Step 2)
3. Verify stage N output exists before running stage N+1
4. Use use_cache=False when you want to force a re-run after a bug fix
5. Check manifest.json exists after every successful run
6. Load and inspect the output Set after cooking (see fn-1-load.md)

---

MUST NOT (All Stages)
----------------------

1. NEVER run stage N+1 before verifying stage N output
2. NEVER invent Fn names -- only use what ls code/haifn/... shows
3. NEVER use the inference paths (df_case=, case_example=) for training
4. NEVER skip source env.sh -- store paths come from environment variables
5. NEVER look for case_data.parquet -- the Stage 3 file is df_case.parquet
6. NEVER expect a vocab/ subdirectory in Stage 4 -- vocab files are at ROOT

---

Sequential Pipeline Note
-------------------------

Stages MUST run in order: 1-source -> 2-record -> 3-case -> 4-aidata.
Each stage's output is the next stage's required input.

  Stage 1 produces: SourceSet  -> consumed by Stage 2
  Stage 2 produces: RecordSet  -> consumed by Stage 3
  Stage 3 produces: CaseSet    -> consumed by Stage 4
  Stage 4 produces: AIDataSet  -> consumed by Stage 5 (model training)

Before running stage N+1, verify stage N output exists:

  ls _WorkSpace/1-SourceStore/<CohortName>/@<SourceFnName>/manifest.json
  ls _WorkSpace/2-RecStore/<CohortName>_v<N>RecSet/manifest.json
  ls _WorkSpace/3-CaseStore/<RecSetName>/@v<N>CaseSet-<Trigger>/manifest.json
  ls _WorkSpace/4-AIDataStore/<aidata_name>/@<version>/manifest.json

If a manifest.json is missing, the asset was not saved cleanly.
Re-run the stage that produced it before proceeding.
