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




 Option B 完整设计                                                                                
                                                                                                   
  总体架构                                                                                         
                                            
  Stage 3 CaseSet (已完成，3569 cases)
    每个 case 有 39 个 CaseFn 的 --val 列
      ↓
  Stage 4 AIData (要建)
    ├─ Split:   RandomByPatient (80/20)
    ├─ Input:   InputValFlatMultiCF   → 33个 feature CaseFn → feat-val (float32[~175])
    └─ Output:  OutputWeightLabel     → WeightAf1M--val → weight_loss_pct (float)
      ↓
  AIDataSet 输出 (每个 horizon 一份，共 6 份):
    train/ 和 test/ 各有:
      feat-val:          [0.55, 65.0, 2.0, 170.5, ..., 8200, ...]   ← 175维 float32
      weight_loss_pct:   4.2  (或 NaN 表示无效)                      ← 1维 float
      split:             "train" / "test"
      PID, ObsDT:        metadata
      ↓
  Stage 5 Model (以后建)
    读取 AIDataSet
    df = df[df['weight_loss_pct'].notna()]      # 过滤无效
    df['label'] = (df['weight_loss_pct'] > 4.0)  # 阈值二值化
    XGBoost.fit(X=feat-val, y=label)

  ---
  Thing 1: InputValFlatMultiCF

  作用：把 33 个 feature CaseFn 的 --val dict 拍平成一个 numpy array。

  参考对象：CatInputMultiCFSparse.py — 它把 --idx/--wgt 拼成 sparse vector。我们把 --val dict 拼成
  dense float vector。

  两个函数：

  def build_vocab_fn(InputArgs, CF_to_CFVocab):
      """
      从 config 的 input_val_keys 构建特征列表。
   
      InputArgs['input_val_keys'] = {
          'PDemoBase': ['gender', 'age', 'disease_type'],
          'HeightBase': ['height', 'days_since'],
          'RecNumBf1d': ['cgm_count', 'diet_count', ...],
          ...
      }
      """
      input_val_keys = InputArgs['input_val_keys']
      CF_list = InputArgs['input_casefn_list']    # 33 个 CaseFn, 决定顺序

      feat_columns = []        # [(CF, key), (CF, key), ...]
      column_names = []        # ['PDemoBase:gender', 'PDemoBase:age', ...]

      for cf in CF_list:
          keys = input_val_keys.get(cf, [])
          for key in keys:
              feat_columns.append((cf, key))
              column_names.append(f"{cf}:{key}")

      return {
          'feat-val': {
              'feat_columns': feat_columns,
              'column_names': column_names,
              'n_features': len(feat_columns),
          }
      }

  def tfm_fn(case_features, InputArgs, CF_to_CFVocab, feat_vocab):
      """
      每个 case → 一个 float32 array。
   
      case_features['PDemoBase--val'] = {'gender': 1, 'age': 55, 'disease_type': 2}
      case_features['HeightBase--val'] = {'height': 170.5, 'days_since': 30}
      ...
   
      → feat-val: np.array([1.0, 55.0, 2.0, 170.5, 30.0, ...], dtype=float32)
      """
      feat_columns = feat_vocab['feat-val']['feat_columns']
      values = []

      for cf, key in feat_columns:
          val_col = f"{cf}--val"
          val_dict = case_features.get(val_col, {})

          # HuggingFace Dataset 可能把 dict 存成 JSON string
          if isinstance(val_dict, str):
              import json
              val_dict = json.loads(val_dict)

          if isinstance(val_dict, dict):
              v = val_dict.get(key, float('nan'))
          else:
              v = float('nan')

          values.append(float(v) if v is not None else float('nan'))

      return {'feat-val': np.array(values, dtype=np.float32)}

  特点：
  - 用 feat_vocab 保存特征顺序 → 模型训练和推理时知道每一维是什么
  - 缺失值 → NaN（XGBoost 原生支持 NaN）
  - 不需要 tokenization，不需要 vocab offset — 直接 float

  ---
  Thing 2: OutputWeightLabel

  作用：从 label CaseFn 的 --val dict 提取 raw weight_loss_pct。

  参考对象：OutputSingleLabel.py — 它输出 {'label': np.int64(0/1)}。我们输出 {'weight_loss_pct':
  float}。

  def tfm_fn(case_features, OutputArgs):
      """
      提取 raw weight_loss_pct, 不做二值化。
   
      case_features['WeightAf1M--val'] = {
          'weight_loss_pct': 4.2,
          'no_future_weight': 0,
          'current_weight': 220.0,
          'future_weight': 210.8
      }
   
      → {'weight_loss_pct': 4.2}
      → 无效时: {'weight_loss_pct': NaN}
      """
      output_args = OutputArgs.get('output_args', {})
      weight_outcome_col = output_args['weight_outcome_col']   # 'WeightAf1M--val'

      val_dict = case_features.get(weight_outcome_col, {})

      if isinstance(val_dict, str):
          import json
          val_dict = json.loads(val_dict)

      if not isinstance(val_dict, dict):
          return {'weight_loss_pct': float('nan')}

      no_future = val_dict.get('no_future_weight', 1)
      if no_future == 1:
          return {'weight_loss_pct': float('nan')}

      pct = val_dict.get('weight_loss_pct', float('nan'))
      return {'weight_loss_pct': float(pct) if pct is not None else float('nan')}

  关键：只有一个输出列 weight_loss_pct，NaN 表示该 case 无效（没有未来体重）。

  ---
  Thing 3: Config YAML

  先做 Af1M 一个 horizon：

  # 4_aidata_welldoc2023cvsderx_af1m.yaml

  record_set_name: "WellDoc2023CVSDeRx_v0RecSet"
  case_set_name: "WellDoc2023CVSDeRx_v0RecSet/@v0CaseSet-WeightDayEntry"

  aidata_set_version: 0
  aidata_set_suffix: "WeightAf1M"

  SplitArgs:
    SplitMethod: RandomByPatient
    Split_Part:
      SplitRatio:
        train: 0.8
        valid: 0.0
        test: 0.2
        random_state: 42
    Split_to_Selection:
      train:
        Rules: [["split", "==", "train"]]
      test:
        Rules: [["split", "==", "test"]]

  InputArgs:
    input_method: InputValFlatMultiCF
    input_casefn_list:        # 33 个 feature CaseFn (决定特征顺序)
      - PDemoBase
      - HeightBase
      - WeightBf1d
      - WeightBf7d
      - WeightBf14d
      - WeightBf30d
      - WeightBf90d
      - CGMStatsBf1d
      - CGMStatsBf7d
      - CGMStatsBf14d
      - CGMStatsBf30d
      - CGMStatsBf60d
      - CGMStatsBf90d
      - DietStatsBf1d
      - DietStatsBf7d
      - DietStatsBf30d
      - DietStatsBf90d
      - ExerciseStatsBf1d
      - ExerciseStatsBf7d
      - ExerciseStatsBf30d
      - ExerciseStatsBf90d
      - MedStatsBf1d
      - MedStatsBf7d
      - MedStatsBf30d
      - MedStatsBf90d
      - StepStatsBf7d
      - StepStatsBf30d
      - StepStatsBf90d
      - SleepStatsBf7d
      - SleepStatsBf30d
      - SleepStatsBf90d
      - RecNumBf1d
      - RecNumBf30d
    input_val_keys:
      PDemoBase:        [gender, age, disease_type]
      HeightBase:       [height, days_since]
      WeightBf1d:       [weight_last, weight_mean, weight_std, weight_trend, n_days, days_since]
      WeightBf7d:       [weight_last, weight_mean, weight_std, weight_trend, n_days, days_since]
      WeightBf14d:      [weight_last, weight_mean, weight_std, weight_trend, n_days, days_since]
      WeightBf30d:      [weight_last, weight_mean, weight_std, weight_trend, n_days, days_since]
      WeightBf90d:      [weight_last, weight_mean, weight_std, weight_trend, n_days, days_since]
      CGMStatsBf1d:     [mean, std, cv, tir, tar, tbr, n_readings]
      CGMStatsBf7d:     [mean, std, cv, tir, tar, tbr, n_readings]
      CGMStatsBf14d:    [mean, std, cv, tir, tar, tbr, n_readings]
      CGMStatsBf30d:    [mean, std, cv, tir, tar, tbr, n_readings]
      CGMStatsBf60d:    [mean, std, cv, tir, tar, tbr, n_readings]
      CGMStatsBf90d:    [mean, std, cv, tir, tar, tbr, n_readings]
      DietStatsBf1d:    [n_events, carbs_per_day, calories_per_day, protein_per_day, fat_per_day,
  fiber_per_day]
      DietStatsBf7d:    [n_events, carbs_per_day, calories_per_day, protein_per_day, fat_per_day,
  fiber_per_day]
      DietStatsBf30d:   [n_events, carbs_per_day, calories_per_day, protein_per_day, fat_per_day,
  fiber_per_day]
      DietStatsBf90d:   [n_events, carbs_per_day, calories_per_day, protein_per_day, fat_per_day,
  fiber_per_day]
      ExerciseStatsBf1d:  [n_events, n_active_days, duration_mean, calories_burned_mean,
  active_day_rate]
      ExerciseStatsBf7d:  [n_events, n_active_days, duration_mean, calories_burned_mean,
  active_day_rate]
      ExerciseStatsBf30d: [n_events, n_active_days, duration_mean, calories_burned_mean,
  active_day_rate]
      ExerciseStatsBf90d: [n_events, n_active_days, duration_mean, calories_burned_mean,
  active_day_rate]
      MedStatsBf1d:     [n_events, dose_total, dose_per_day, dose_mean_per_event]
      MedStatsBf7d:     [n_events, dose_total, dose_per_day, dose_mean_per_event]
      MedStatsBf30d:    [n_events, dose_total, dose_per_day, dose_mean_per_event]
      MedStatsBf90d:    [n_events, dose_total, dose_per_day, dose_mean_per_event]
      StepStatsBf7d:    [n_active_days, steps_mean, steps_per_day, active_day_rate]
      StepStatsBf30d:   [n_active_days, steps_mean, steps_per_day, active_day_rate]
      StepStatsBf90d:   [n_active_days, steps_mean, steps_per_day, active_day_rate]
      SleepStatsBf7d:   [n_sleep_sessions, sleep_mean, sleep_per_day, active_night_rate]
      SleepStatsBf30d:  [n_sleep_sessions, sleep_mean, sleep_per_day, active_night_rate]
      SleepStatsBf90d:  [n_sleep_sessions, sleep_mean, sleep_per_day, active_night_rate]
      RecNumBf1d:       [cgm_count, diet_count, exercise_count, med_count, sleep_count, step_count,
   weight_count]
      RecNumBf30d:      [cgm_count, diet_count, exercise_count, med_count, sleep_count, step_count,
   weight_count]

  OutputArgs:
    output_method: OutputWeightLabel
    output_args:
      weight_outcome_col: WeightAf1M--val

  做其他 horizon 时，只改两个地方：
  - aidata_set_suffix: "WeightAf0p5M"
  - weight_outcome_col: WeightAf0p5M--val

  ---
  特征数量确认

  ┌──────────────────┬──────┬───────────┬──────┐
  │   CaseFn 类型    │ 数量 │ 每个 keys │ 小计 │
  ├──────────────────┼──────┼───────────┼──────┤
  │ PDemoBase        │ 1    │ 3         │ 3    │
  ├──────────────────┼──────┼───────────┼──────┤
  │ HeightBase       │ 1    │ 2         │ 2    │
  ├──────────────────┼──────┼───────────┼──────┤
  │ WeightBf*        │ 5    │ 6         │ 30   │
  ├──────────────────┼──────┼───────────┼──────┤
  │ CGMStatsBf*      │ 6    │ 7         │ 42   │
  ├──────────────────┼──────┼───────────┼──────┤
  │ DietStatsBf*     │ 4    │ 6         │ 24   │
  ├──────────────────┼──────┼───────────┼──────┤
  │ ExerciseStatsBf* │ 4    │ 5         │ 20   │
  ├──────────────────┼──────┼───────────┼──────┤
  │ MedStatsBf*      │ 4    │ 4         │ 16   │
  ├──────────────────┼──────┼───────────┼──────┤
  │ StepStatsBf*     │ 3    │ 4         │ 12   │
  ├──────────────────┼──────┼───────────┼──────┤
  │ SleepStatsBf*    │ 3    │ 4         │ 12   │
  ├──────────────────┼──────┼───────────┼──────┤
  │ RecNumBf*        │ 2    │ 7         │ 14   │
  ├──────────────────┼──────┼───────────┼──────┤
  │ 合计             │ 33   │           │ 175  │
  └──────────────────┴──────┴───────────┴──────┘

  feat-val 是一个 175 维的 float32 array。

  ---
  AIDataSet 最终输出长什么样

  存储路径：_WorkSpace/4-AIDataStore/WellDoc2023CVSDeRx_WeightDayEntry/@v0AIData-WeightAf1M/

  dataset_dict/
    train/    (~2855 rows, 80%)
    test/     (~714 rows, 20%)

  每行的列:
    PID:               "patient_001"          # metadata
    ObsDT:             "2023-05-15 08:30"     # metadata
    split:             "train"                # from RandomByPatient
    feat-val:          [1.0, 55.0, 2.0, ...]  # 175-dim float32 array (input)
    weight_loss_pct:   4.2                    # raw float (output), NaN=无效

  cf_to_cfvocab.json   # 每个 CaseFn 的 vocab (我们的 CaseFn 用不上，但格式要有)
  feat_vocab.json      # feat_columns 的顺序和命名 → 训练时可查每维是什么
  manifest.json        # 血统追溯

  ---
  Stage 5 使用方式（以后写，现在只是示意）

  # 加载 AIDataSet
  aidata = AIDataSet.load_from_disk('WellDoc2023CVSDeRx_WeightDayEntry/@v0AIData-WeightAf1M')
  df_train = aidata['train'].to_pandas()
  df_test  = aidata['test'].to_pandas()

  # 过滤无效 case
  df_train = df_train[df_train['weight_loss_pct'].notna()]
  df_test  = df_test[df_test['weight_loss_pct'].notna()]

  # 对于 threshold=4.0 的模型
  threshold = 4.0
  y_train = (df_train['weight_loss_pct'] > threshold).astype(int)
  y_test  = (df_test['weight_loss_pct'] > threshold).astype(int)

  # 特征
  X_train = np.stack(df_train['feat-val'].values)  # shape: (n, 175)
  X_test  = np.stack(df_test['feat-val'].values)

  # 训练
  model = xgb.XGBClassifier()
  model.fit(X_train, y_train)

  改 threshold 只是改一个数字，不需要重跑 Stage 4。

  ---
  要建的 builder 文件

  ┌─────────────────────────────────────────────────────────┬──────────────────────────────────┐
  │                          文件                           │               产出               │
  ├─────────────────────────────────────────────────────────┼──────────────────────────────────┤
  │ code-dev/1-PIPELINE/4-AIData-WorkSpace/c8_build_input_v │ → code/haifn/fn_aidata/entryinpu │
  │ alflatmulticf.py                                        │ t/InputValFlatMultiCF.py         │
  ├─────────────────────────────────────────────────────────┼──────────────────────────────────┤
  │ code-dev/1-PIPELINE/4-AIData-WorkSpace/c9_build_output_ │ → code/haifn/fn_aidata/entryoutp │
  │ weightlabel.py                                          │ ut/OutputWeightLabel.py          │
  ├─────────────────────────────────────────────────────────┼──────────────────────────────────┤
  │ (手写) examples/ProjC-Model-WeightPredict/1-hainn-data/ │ Config                           │
  │ config/4_aidata_welldoc2023cvsderx_af1m.yaml            │                                  │
  └─────────────────────────────────────────────────────────┴──────────────────────────────────┘

  ---
  这就是 Option B 的完整设计。要开始写 builder 吗？