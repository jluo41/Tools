fn-design-chef: Create a New Pipeline Fn via the Builder Pattern
================================================================

**Purpose**: Build new pipeline functions (Chef-Fns) for any of the 4 data
pipeline stages. This covers SourceFn, HumanFn/RecordFn, TriggerFn/CaseFn,
and InputTfmFn/OutputTfmFn/SplitFn — all via the builder pattern.

**Rule #1**: NEVER edit `code/haifn/` directly. All production functions are
generated. Edit builders in `code-dev/1-PIPELINE/`, run them, and the output
lands in `code/haifn/`.

---

Overview: The Builder Pattern
------------------------------

```
code-dev/1-PIPELINE/          <-- SOURCE OF TRUTH (edit here)
    1-Source-WorkSpace/
    2-Record-WorkSpace/
    3-Case-WorkSpace/
    4-AIData-WorkSpace/
         |
         | (run builder script)
         v
code/haifn/                   <-- GENERATED (never edit directly)
    fn_source/
    fn_record/
    fn_case/
    fn_aidata/
```

Each builder script has two tagged sections:
- `[BOILERPLATE]` — copy as-is, do NOT modify
- `[CUSTOMIZE]`   — change for your specific dataset/feature

---

Universal Builder Workflow (All Stages)
----------------------------------------

Apply these steps regardless of which stage you are building.

**Step 0: Inspect Existing Builders and Source Table**

```bash
ls code-dev/1-PIPELINE/1-Source-WorkSpace/   # stage 1
ls code-dev/1-PIPELINE/2-Record-WorkSpace/   # stage 2
ls code-dev/1-PIPELINE/3-Case-WorkSpace/     # stage 3
ls code-dev/1-PIPELINE/4-AIData-WorkSpace/   # stage 4
```

Find the closest existing builder to use as a starting point.

For stages 2-3 (RecordFn, CaseFn): also inspect the input data before writing
any logic. This reveals column names, dtypes, and density of the raw data:

```python
from haipipe.source_base import SourceSet
source_set = SourceSet.load_asset('<cohort>/@<SourceFnName>', SPACE=SPACE)
print(list(source_set.ProcName_to_ProcDf.keys()))  # available tables
df = source_set['<TableName>']
print(df.dtypes)
print(df.describe())
print(df.head(3))
```

Key questions to answer before writing processing logic:
- What is the primary datetime column? Is there a separate entry datetime?
- What is the timezone column (offset in minutes, named zone, or IANA string)?
- What is the signal density (rows per entity per day)?
- If two rows land in the same 5-min slot: sum / average / first?
- What is the valid value range for each numeric field?

**Step 1: Present Plan to User, Get Approval**

Before touching any file, present:
- Which builder you will copy/edit
- What `[CUSTOMIZE]` sections you will change
- What the generated output file will be named
- Which config YAML will need updating
- Expected downstream contract impact

Do NOT proceed until the user approves.

**Step 2: Activate .venv and source env.sh**

```bash
source .venv/bin/activate
source env.sh
```

Both are required. Builders need SPACE paths from `env.sh`.

NOTE: source .venv/bin/activate does NOT persist across Bash tool calls.
Always chain: source .venv/bin/activate && source env.sh && python <script>
Or call venv Python directly: .venv/bin/python script.py

**Step 3: Copy Closest Existing Builder as Starting Point**

```bash
cp code-dev/1-PIPELINE/3-Case-WorkSpace/c2_build_casefn_cgmvalue.py \
   code-dev/1-PIPELINE/3-Case-WorkSpace/c5_build_casefn_myfeature.py
```

Do not start from scratch. Always copy and modify.

**Step 4: Edit [CUSTOMIZE] Sections Only**

Open the copied builder. Change only the `[CUSTOMIZE]` tagged sections:
- Output file name / Fn name
- Schema definitions
- Processing logic
- Feature extraction logic

Leave all `[BOILERPLATE]` sections unchanged.

**Step 5: Set RUN_TEST = True and Run Builder**

Always set `RUN_TEST = True` at the top of the builder before running:

```python
RUN_TEST = True   # <-- must be True
```

Then run:

```bash
python code-dev/1-PIPELINE/3-Case-WorkSpace/c5_build_casefn_myfeature.py
```

**Step 6: Verify Generated File in code/haifn/**

```bash
ls code/haifn/fn_case/case_casefn/MyFeatureBf24h.py
python -c "import haifn.fn_case.case_casefn.MyFeatureBf24h as m; print(m.CaseFnName)"
```

**Step 7: Register in Config YAML**

Add the new Fn name to the appropriate config file (stage-specific, see below).
Do not skip this — the pipeline will not pick up unregistered Fns.

**Step 8: Test End-to-End with the Matching Pipeline**

```bash
haistep-case   --config config/test-haistep-ohio/3_test_case.yaml
haistep-aidata --config config/test-haistep-ohio/4_test_aidata.yaml
```

Use the matching haistep-* command for your stage.

---

Stage Reference: 1-source
===========================

**What You Build**: SourceFn — loads raw files from disk and produces
standardized DataFrames per table type (CGM, Diet, Medication, Exercise, ...).

**Builder Location**:
```
code-dev/1-PIPELINE/1-Source-WorkSpace/
```

**Builder Naming**:
```
c{N}_build_source_{dataset}{version}.py
Example: c3_build_source_Ohio251226.py
```

**Generated Output**:
```
code/haifn/fn_source/{SourceFnName}.py
Example: code/haifn/fn_source/OhioT1DMxmlv250302.py
```

**Required Module Attributes** (must be present in generated file):

```python
SourceFile_SuffixList          # list[str] — file suffix patterns to load
ProcName_List                  # list[str] — table names this source produces
ProcName_to_columns            # dict[str, list[str]] — columns per table
MetaDict                       # dict — metadata about this SourceFn

def get_ProcName_from_SourceFile(source_file) -> str:
    # maps a raw file path to its ProcName (table type)
    ...

def process_Source_to_Processed(
    SourceFile_List,
    get_ProcName_from_SourceFile,
    SPACE=None
) -> dict[str, pd.DataFrame]:
    # main ETL function: raw files -> {ProcName: DataFrame}
    ...
```

**Register in Config**:
```yaml
SourceArgs:
  SourceFnName: OhioT1DMxmlv250302
```

**Downstream Contract** (satisfies 2-record stage):

All SourceFns for the same domain MUST output identical column schemas
for shared table types. Schema consistency is mandatory across all source
versions of the same domain.

Standard column counts to check before designing:

```
Medication: 11 columns
  ['PatientID', 'MedAdministrationID',
   'AdministrationDate', 'EntryDateTime', 'UserAdministrationDate',
   'AdministrationTimeZoneOffset', 'AdministrationTimeZone',
   'MedicationID', 'Dose', 'medication', 'external_metadata']

Exercise: 13 columns
  ['PatientID', 'ExerciseEntryID',
   'ObservationDateTime', 'ObservationEntryDateTime',
   'TimezoneOffset', 'Timezone',
   'ExerciseType', 'ExerciseIntensity', 'ExerciseDuration',
   'CaloriesBurned', 'DistanceInMeters', 'exercise', 'external_metadata']

Diet: 15 columns
  ['PatientID', 'CarbsEntryID',
   'ObservationDateTime', 'ObservationEntryDateTime',
   'TimezoneOffset', 'Timezone',
   'FoodName', 'ActivityType',
   'Carbs', 'Calories', 'Protein', 'Fat', 'Fiber',
   'nutrition', 'external_metadata']
```

**Core vs Extended Field Rule**:
- Core fields: kept as DataFrame columns AND embedded in the JSON column
- Extended fields: stored ONLY in the JSON column (e.g., `external_metadata`)
- Dataset-specific metadata goes ONLY in JSON fields

**MUST**:
- Set `RUN_TEST = True` before running
- Check domain's standard column counts before designing schema
- Put core fields as columns AND in JSON
- Put extended/dataset-specific fields ONLY in JSON

---

Stage Reference: 2-record
===========================

**What You Build**: HumanFn (patient identity mapping) OR RecordFn (time-series
signal alignment for one signal type).

**Which to Build: HumanFn or RecordFn?**

```
Is this about defining the ENTITY itself (who/what is tracked)?
    YES  -->  HumanFn  (new entity type, new ID scheme, or new ID length)
    NO   -->  RecordFn (new data table for an existing entity type)
```

Build a **HumanFn** when:
- The entity type is new (different patient ID scheme, new cohort)
- The raw entity ID column name differs from any existing HumanFn
- In practice: one HumanFn per entity type per project; most new data just needs a RecordFn

Build a **RecordFn** when:
- You have a new data table (new signal type) for an existing entity
- The entity already has a HumanFn; you only need to add the time-series data

**Builder Locations**:
```
code-dev/1-PIPELINE/2-Record-WorkSpace/h{N}_build_human_{name}.py   (HumanFn)
code-dev/1-PIPELINE/2-Record-WorkSpace/r{N}_build_record_{name}.py  (RecordFn)
```

**Generated Output**:
```
code/haifn/fn_record/human/{HumanFnName}.py      (HumanFn)
code/haifn/fn_record/record/{RecordFnName}.py    (RecordFn)
```

**HumanFn Required Module Attributes**:

```python
OneHuman_Args               # dict — args for building one Human entity
                            # required keys:
                            #   HumanName:     '<HumanFnName>'
                            #   HumanID:       '<InternalIDCol>'  (e.g., PID)
                            #   RawHumanID:    '<RawIDCol>'       (e.g., PatientID)
                            #   HumanIDLength: <N>                (integer, e.g., 10)
Excluded_RawNameList        # list[str] — event/time-series ProcNames to exclude
                            # from entity roster building (keep only static tables)
MetaDict                    # dict — metadata

def get_RawHumanID_from_dfRawColumns(df_raw_columns) -> str:
    # Returns the entity ID column name if this table contains entity-level rows.
    # Returns None if the table does NOT contain the entity ID (pipeline skips it).
    ...
```

**RecordFn Required Module Attributes**:

```python
OneRecord_Args              # dict — args for this signal type
RawName_to_RawConfig        # dict[str, dict] — per-source raw file config
attr_cols                   # list[str] — columns exposed to downstream CaseFns

def get_RawRecProc_for_HumanGroup(df_RawRec_for_HumanGroup, OneRecord_Args, df_Human) -> pd.DataFrame:
    # processes raw data for one human group into aligned time series
    # params: (raw records DataFrame, record args dict, human demographics DataFrame)
    ...
```

**4 RecordFn Signal Patterns** (choose the correct one):

```
Pattern A: Dense / Continuous (regular-interval sensor data)
  Example: CGM readings every 5 minutes
  Aggregation: FIRST (take first value in window)
  Use when: signal has regular cadence, only one value expected per window

Pattern B: Sparse / Additive (accumulating events)
  Example: insulin doses, meal carbs
  Aggregation: SUM (sum all events in window)
  Use when: multiple events should be summed (total carbs eaten, total dose)

Pattern C: Sparse / Mean (repeated measurements)
  Example: lab values, weight readings
  Aggregation: MEAN (average all readings in window)
  Use when: multiple measurements represent the same quantity

Pattern D: Sparse / First (discrete events)
  Example: one-time diagnoses, enrollment events
  Aggregation: FIRST (take first occurrence)
  Use when: event has no meaningful aggregation, only presence matters
```

**RecordFn Processing Skeleton** (all 4 patterns share this; only step 8 aggregation differs):

```python
def get_RawRecProc_for_HumanGroup(df_RawRec_for_HumanGroup, OneRecord_Args, df_Human):
    import pandas as pd, numpy as np
    df = df_RawRec_for_HumanGroup

    # Define empty return schema once; reuse at every early-exit point
    EMPTY_COLS = ['<RawHumanID>', 'DT_s', 'DT_r', 'DT_tz',
                  '<ValueCol>', 'time_to_last_entry']

    # 1. Timezone filter (strict: abs < 840 for single-country; loose: abs < 1000)
    df = df[df['<TimezoneCol>'].abs() < <THRESHOLD>].reset_index(drop=True)
    if len(df) == 0: return pd.DataFrame(columns=EMPTY_COLS)

    # 2. Parse datetime
    df['<DatetimeCol>'] = pd.to_datetime(df['<DatetimeCol>'], format='mixed', errors='coerce')
    df = df[df['<DatetimeCol>'].notna()].reset_index(drop=True)
    if len(df) == 0: return pd.DataFrame(columns=EMPTY_COLS)

    # 3. Resolve timezone: prefer explicit offset -> fallback user_tz -> default 0
    a = len(df)
    df = pd.merge(df, df_Human[['<RawHumanID>', 'user_tz']], how='left')
    assert len(df) == a   # row count must not change after merge
    df['DT_tz'] = df['<TimezoneCol>'].replace(0, None).fillna(df['user_tz']).infer_objects(copy=False)

    # 4. Build DT_s; filter implausible dates
    df['DT_s'] = pd.to_datetime(df['<DatetimeCol>'], format='mixed', errors='coerce')
    df = df[df['DT_s'] > pd.to_datetime('<DATE_CUTOFF>')].reset_index(drop=True)
    df['DT_tz'] = df['DT_tz'].fillna(0).astype(int)
    df['DT_s'] = df['DT_s'] + pd.to_timedelta(df['DT_tz'], 'm')
    df = df[df['DT_s'].notna()].reset_index(drop=True)
    if len(df) == 0: return pd.DataFrame(columns=EMPTY_COLS)

    # 5. DT_r: record entry time (same as DT_s if no separate entry datetime)
    df['DT_r'] = df['DT_s']
    # If a separate entry datetime column exists:
    # df['DT_r'] = pd.to_datetime(df['<EntryDatetimeCol>'], ...) + pd.to_timedelta(df['DT_tz'], 'm')

    # 6. Value filter (set range to what is physically plausible)
    df['<ValueCol>'] = pd.to_numeric(df['<ValueCol>'], errors='coerce')
    df = df[(df['<ValueCol>'] > <MIN>) & (df['<ValueCol>'] < <MAX>)].reset_index(drop=True)
    if len(df) == 0: return pd.DataFrame(columns=EMPTY_COLS)

    # 7. Round DT_s and DT_r to domain time unit (e.g., 5-min for CGM)
    for col in ['DT_s', 'DT_r']:
        date = df[col].dt.date.astype(str)
        hour = df[col].dt.hour.astype(str)
        mins = ((df[col].dt.minute / <INTERVAL_MIN>).astype(int) * <INTERVAL_MIN>).astype(str)
        df[col] = pd.to_datetime(date + ' ' + hour + ':' + mins + ':00')

    # 8. Aggregate by (RawHumanID, DT_s) -- ONLY THIS LINE changes per pattern:
    RawHumanID = OneRecord_Args['RawHumanID']
    df = df.groupby([RawHumanID, 'DT_s']).agg({
        'DT_r':       'first',
        'DT_tz':      'first',
        '<ValueCol>': '<AGG>',   # 'first' / 'sum' / 'mean' per pattern table above
    }).reset_index()

    # 9. time_to_last_entry in domain time units
    df = df.sort_values([RawHumanID, 'DT_s'])
    df['time_to_last_entry'] = (
        df.groupby(RawHumanID, group_keys=False)['DT_s']
        .diff().dt.total_seconds() / 60 / <INTERVAL_MIN>
    )
    return df
```

**RecordFn Processing Invariants** (every get_RawRecProc_for_HumanGroup must satisfy these):

```
1. Define EMPTY_COLS once at top; return it at every filter that empties the DataFrame
2. Parse datetimes with: pd.to_datetime(..., format='mixed', errors='coerce')
3. Filter implausible dates with a filter, not an assertion
4. Assert row count unchanged after merging df_Human
5. Resolve timezone: prefer explicit offset -> fallback user_tz -> default 0
6. Round both DT_s and DT_r to the domain time unit
7. Return only columns listed in attr_cols -- no extras
```

**Register in Config**:
```yaml
HumanRecords:
  MyHumanFn:
    - MyRecordFn_CGM
    - MyRecordFn_Diet
```

**Downstream Contract** (satisfies 3-case stage):

`attr_cols` must include all columns that downstream CaseFns will access
via `ROName_to_RONameInfo`. Changing `attr_cols` after CaseFns are built
breaks all CaseFns that reference removed columns.

**MUST**:
- Choose the correct signal pattern (A/B/C/D) before writing any code
- Never change `attr_cols` without auditing and updating all downstream CaseFns
- Verify that HumanFn produces the correct patient ID mapping

---

Stage Reference: 3-case
=========================

**What You Build**: TriggerFn (when to create a case) OR CaseFn (what features
to extract at the trigger point). These are two separate types with different
builders.

**Builder Locations**:
```
code-dev/1-PIPELINE/3-Case-WorkSpace/a{N}_build_trigger_{name}.py   (TriggerFn)
code-dev/1-PIPELINE/3-Case-WorkSpace/c{N}_build_casefn_{feature}.py (CaseFn)
```

- - -

TriggerFn
----------

**Generated Output**:
```
code/haifn/fn_case/fn_trigger/{TriggerFnName}.py
```

**Required Attributes and Function**:

```python
Trigger        # str — trigger event type name (e.g., 'CGM5MinEntry')
Trigger_Args   # dict — args passed to the trigger function

def get_CaseTrigger_from_RecordBase(
    record_set,
    Trigger_Args,
    df_case_raw=None
) -> dict:
    # Returns dict with keys:
    #   'df_case'       — one row per triggered case
    #   'df_lts'        — longitudinal time series data
    #   'df_Human_Info' — one row per human entity
    ...
```

NOTE: The function MUST be named `get_CaseTrigger_from_RecordBase` exactly.
Do NOT name it `fn_TriggerFn` or anything else.

- - -

CaseFn
-------

**Generated Output**:
```
code/haifn/fn_case/case_casefn/{CaseFnName}.py
```

**Naming Convention**:
```
<Feature><Window>
Examples:
  CGMValueBf24h      (CGM value, before 24 hours)
  LabValueBf7d       (lab value, before 7 days)
  PDemoBase          (patient demographics, no window)
  InvCrntTimeFixedLen (invitation, current time features)
```

**Required Module Attributes**:

```python
CaseFnName              # str — must match file name
RO_to_ROName            # dict[str, str] — short alias -> ROName (3-part)
Ckpd_to_CkpdObsConfig  # dict — checkpoint observation config
ROName_to_RONameInfo    # dict — metadata per ROName
HumanRecords            # dict — which HumanFn/RecordFn this CaseFn uses
COVocab                 # dict — controlled vocabulary for tokenization
MetaDict                # dict — REQUIRED 7 keys (see below)

# MetaDict must contain exactly these 7 keys for builder code generation:
MetaDict = {
    "CaseFnName":              CaseFnName,
    "RO_to_ROName":            RO_to_ROName,
    "Ckpd_to_CkpdObsConfig":  Ckpd_to_CkpdObsConfig,
    "ROName_to_RONameInfo":    ROName_to_RONameInfo,
    "HumanRecords":            HumanRecords,
    "COVocab":                 COVocab,
    "fn_CaseFn":               fn_CaseFn
}

def fn_CaseFn(
    case_example,
    ROName_list,
    ROName_to_ROData,
    ROName_to_ROInfo,
    COVocab,
    context
) -> dict:
    # Returns dict with SUFFIX-ONLY keys.
    # Pipeline automatically prepends CaseFnName to each key.
    # Valid suffixes: --tid, --wgt, --val, --str
    ...
```

**ROName 3-Part Format**:
```
h<HumanFnName>.r<RecordFnName>.c<CkpdName>

Example:
  hOhioHuman.rOhioCGM.cBf24h

  where:
    hOhioHuman  = HumanFn name (with h prefix)
    rOhioCGM    = RecordFn name (with r prefix)
    cBf24h      = Checkpoint name (with c prefix)
```

**Return Key Format** (SUFFIX-ONLY):
```python
# CORRECT — suffix only, pipeline adds CaseFnName prefix
return {
    '--tid': token_id_array,
    '--wgt': weight_array,
    '--val': float_value,
    '--str': string_label,
}

# WRONG — do NOT include CaseFnName in the key
return {
    'CGMValueBf24h--tid': ...,   # <-- WRONG
}
```

**Common Ckpd Window Configurations** (use as reference when setting Ckpd_to_CkpdObsConfig):

```
Window   | DistStart | DistEnd | StartIdx | EndIdx | Meaning
---------+-----------+---------+----------+--------+------------------------
Bf24h    | -1440     | 5       | -288     | 1      | 24h before trigger
Af24h    | -5        | 1440    | -1       | 288    | 24h after trigger
Bf2h     | -120      | 5       | -24      | 1      | 2h before trigger
Af2h     | -5        | 120     | -1       | 24     | 2h after trigger
Af2to8h  | -5        | 480     | -1       | 96     | 2-8h after trigger
Bf7d     | -10080    | 5       | -2016    | 1      | 7 days before trigger
Base     | 0         | 0       | 0        | 0      | Static (no window)
```

DistStart/DistEnd are in minutes from trigger. StartIdx/EndIdx are in domain
time units (5-min slots for CGM domain). Positive = after trigger, Negative = before.

**Register in Config**:
```yaml
CaseArgs:
  Case_Args:
    - CaseFnList:
        - CGMValueBf24h
        - PDemoBase
        - MyNewCaseFn
```

**Downstream Contract** (satisfies 4-aidata stage):

Output suffix keys (`--tid`, `--wgt`) must match what downstream InputTfmFns
expect via `input_casefn_list`. If you rename a suffix, update the AIData
config and TfmFn accordingly.

**MUST**:
- Use 3-part ROName format exactly: `h<Human>.r<Record>.c<Ckpd>`
- Return SUFFIX-ONLY keys from `fn_CaseFn`
- Include all required attributes: MetaDict, HumanRecords, Ckpd_to_CkpdObsConfig
- Name trigger function exactly `get_CaseTrigger_from_RecordBase`

---

Stage Reference: 4-aidata
===========================

**What You Build**: InputTfmFn (feature transforms), OutputTfmFn (label/target
transforms), or SplitFn (train/val/test splitting). Three separate types.

**Builder Location**:
```
code-dev/1-PIPELINE/4-AIData-WorkSpace/
  c<N>_build_transforms_<type>.py    (Input/Output TfmFn builders -- discover with ls)
  s<N>_build_splitfn_<method>.py     (SplitFn builders -- discover with ls)
```

**Builder Script Structure** (what you [CUSTOMIZE] vs [BOILERPLATE]):

```
[BOILERPLATE]  Output dir setup, builder infrastructure, generate-and-save logic
[CUSTOMIZE]    FnName, build_vocab_fn body, tfm_fn body (InputTfmFn)
[CUSTOMIZE]    FnName, tfm_fn body (OutputTfmFn)
[CUSTOMIZE]    FnName, dataset_split_tagging_fn body (SplitFn)
```

Start by copying the closest existing builder:

```bash
ls code-dev/1-PIPELINE/4-AIData-WorkSpace/c*.py   # TfmFn builders
ls code-dev/1-PIPELINE/4-AIData-WorkSpace/s*.py   # SplitFn builders
```

- - -

InputTfmFn
-----------

**Generated Output**:
```
code/haifn/fn_aidata/entryinput/{InputTfmFnName}.py
```

**Required Functions**:

```python
def build_vocab_fn(InputArgs, CF_to_CFVocab) -> dict:
    # Builds the feature vocabulary from case features.
    # Params: InputArgs (config), CF_to_CFVocab (per-CaseFn vocab dicts)
    # Returns: feat_vocab dict used during tfm_fn
    ...

def tfm_fn(case_features, InputArgs, CF_to_CFvocab, feat_vocab=None) -> dict:
    # Transforms raw case features into model-ready input tensors/arrays.
    # Params (4 total):
    #   case_features — dict of raw features from CaseFns
    #   InputArgs     — config dict
    #   CF_to_CFvocab — per-CaseFn vocab dicts
    #   feat_vocab    — vocab built by build_vocab_fn (optional at build time)
    # Returns: dict of transformed features
    ...
```

**Register in Config**:
```yaml
InputArgs:
  input_method: MyInputTfmFn
```

- - -

OutputTfmFn
------------

**Generated Output**:
```
code/haifn/fn_aidata/entryoutput/{OutputTfmFnName}.py
```

**Required Function**:

```python
def tfm_fn(case, OutputArgs) -> dict:
    # Transforms a case into label/target output.
    # Params (2 total — NOT 4!):
    #   case       — the raw case dict
    #   OutputArgs — config dict
    # Returns: dict with label or target key
    ...
```

NOTE: OutputTfmFn `tfm_fn` takes ONLY 2 params, unlike InputTfmFn which takes 4.

**Register in Config**:
```yaml
OutputArgs:
  output_method: MyOutputTfmFn
```

- - -

SplitFn
--------

**Generated Output**:
```
code/haifn/fn_aidata/split/{SplitFnName}.py
```

**Required Function**:

```python
def dataset_split_tagging_fn(df_tag, SplitArgs) -> pd.DataFrame:
    # Assigns train/validation/test-id/test-od splits to each row.
    # Params: df_tag (DataFrame with one row per case), SplitArgs (config)
    # Returns: df_tag with 'split_ai' column added
    #   Values: 'train', 'validation', 'test-id', 'test-od'
    ...
```

**Register in Config**:
```yaml
SplitArgs:
  SplitMethod: MySplitFn
```

---

Universal MUST DO (All Stages)
================================

1. Present plan to user and get approval before starting any file changes
2. Activate .venv: `source .venv/bin/activate && source env.sh`
3. Copy closest existing builder — do NOT start from scratch
4. Edit only `[CUSTOMIZE]` sections — leave `[BOILERPLATE]` unchanged
5. Set `RUN_TEST = True` in builder before running
6. Verify generated file exists in `code/haifn/` after running builder
7. Register the new Fn in the appropriate config YAML
8. Test end-to-end with the matching `haistep-*` command after generation

---

Universal MUST NOT (All Stages)
=================================

1. NEVER edit `code/haifn/` directly — always go through the builder
2. NEVER skip the builder -> generate -> verify cycle
3. NEVER set `RUN_TEST = False` or omit the RUN_TEST step
4. NEVER skip `source env.sh` — builders need SPACE paths to run
5. NEVER break downstream contracts:
   - Source: maintain schema consistency across all SourceFns for the same domain
   - Record: do not change `attr_cols` without updating downstream CaseFns
   - Case: use suffix-only return keys from `fn_CaseFn`
   - AIData: match `input_casefn_list` expected suffixes

---

Quick Reference: Stage Summary
================================

```
Stage | What You Build         | Builder Dir            | Generated In
------+------------------------+------------------------+---------------------------
  1   | SourceFn               | 1-Source-WorkSpace/    | fn_source/
  2   | HumanFn or RecordFn    | 2-Record-WorkSpace/    | fn_record/human/ or record/
  3   | TriggerFn or CaseFn    | 3-Case-WorkSpace/      | fn_case/fn_trigger/ or
      |                        |                        |   case_casefn/
  4   | InputTfmFn, OutputTfmFn| 4-AIData-WorkSpace/    | fn_aidata/entryinput/,
      | or SplitFn             |                        |   entryoutput/, or split/
```

```
Stage | Register Key           | Config Field
------+------------------------+--------------------------------
  1   | SourceFnName           | SourceArgs.SourceFnName
  2   | HumanFnName + list     | HumanRecords dict
  3   | CaseFnName             | CaseArgs.Case_Args[*].CaseFnList
  4   | method name            | InputArgs.input_method
      |                        | OutputArgs.output_method
      |                        | SplitArgs.SplitMethod
```
