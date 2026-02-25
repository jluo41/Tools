Subcommand: design-chef
=======================

Purpose: Create a new TriggerFn or CaseFn via the builder pattern.
Edit builders in code-dev/ -> run -> generates code/haifn/fn_case/.

This skill documents FRAMEWORK PATTERNS only -- not project-specific state.
It applies to any domain: CGM, EHR, labs, wearables, or any event-triggered feature.

---

Workflow
========

0. **Inspect existing builders and registered Fns:**
   ```bash
   ls code-dev/1-PIPELINE/3-Case-WorkSpace/a*.py   # TriggerFn builders
   ls code-dev/1-PIPELINE/3-Case-WorkSpace/c*.py   # CaseFn builders
   ls code/haifn/fn_case/fn_trigger/               # already registered TriggerFns
   ls code/haifn/fn_case/case_casefn/              # already registered CaseFns
   ```
1. **Present** plan to user -> **get** approval
2. **Activate** environment:
   ```bash
   source .venv/bin/activate
   source env.sh
   ```
3. **Copy** an existing builder as starting point (pick one closest to your use case)
4. **Edit** [CUSTOMIZE] sections only (keep [BOILERPLATE] as-is)
5. **Run** builder:
   ```bash
   python code-dev/1-PIPELINE/3-Case-WorkSpace/<your_builder>.py
   ```
6. **Verify** generated file in code/haifn/fn_case/fn_trigger/ or case_casefn/
7. **Register** in config YAML (TriggerName or CaseFn_list)
8. **Test** end-to-end with Case_Pipeline

---

Builder Location
================

```
code-dev/1-PIPELINE/3-Case-WorkSpace/
+-- a<N>_build_trigger_<triggername>.py  (TriggerFn builders -- discover with ls)
+-- c<N>_build_casefn_<feature>.py       (CaseFn builders -- discover with ls)
+-- old/                                  (Legacy builders)
```

Discover existing builders:
```bash
ls code-dev/1-PIPELINE/3-Case-WorkSpace/a*.py   # TriggerFn builders
ls code-dev/1-PIPELINE/3-Case-WorkSpace/c*.py   # CaseFn builders
```

**Two types of builders:**

- **TriggerFn builders (a* prefix):** Define WHEN cases are created
- **CaseFn builders (c* prefix):** Define WHAT features are extracted

---

Naming Convention
=================

**TriggerFn builder:** `a{N}_build_trigger_{triggername}.py`
  Example: `a4_build_trigger_mealentry.py`

**CaseFn builder:** `c{N}_build_casefn_{feature}.py`
  Example: `c5_build_casefn_insulindose.py`

**Generated TriggerFn:** `code/haifn/fn_case/fn_trigger/{TriggerFnName}.py`
**Generated CaseFn:** `code/haifn/fn_case/case_casefn/{CaseFnName}.py`

**CaseFn naming:** `<Feature><Window>` convention:
- `CGMValueBf24h` = CGM Value, Before 24 hours
- `DEMEventAf24h` = Diet/Exercise/Med Event, After 24 hours
- `PDemoBase` = Patient Demographics, Baseline (no window)
- `LabValueBf7d` = Lab Value, Before 7 days (any domain works)

---

TriggerFn Module Structure
===========================

**CRITICAL:** The main function is `get_CaseTrigger_from_RecordBase`, NOT `fn_TriggerFn`.

```python
# Module-level metadata (all required):
# Example (illustrative -- actual TriggerFn/HumanFn/RecordFn names from ls commands):
Trigger = "<TriggerFnName>"

Trigger_Args = {
    'Trigger': '<TriggerFnName>',
    'case_id_columns': ['<EntityID>', '<ObsDT>'],
    'case_raw_id_columns': ['<RawEntityID>', '<ObsDT>'],
    'HumanID_list': ['<EntityID>'],
    'ObsDT': '<ObsDT>',
    'ROName_to_RONameArgs': {
        'h<HumanFnName>.r<RecordFnName>': {
            'attribute_columns': ['<EntityID>', '<RawEntityID>', '<DatetimeCol>', '<ValueCol>'],
            'RecDT': '<DatetimeCol>'
        }
    },
    'min_segment_length': 36,
    'max_consecutive_missing': 3,
    'stride': 12,
    'buffer_start': 48,
    'buffer_end': 48,
}

# Main function -- MUST be named get_CaseTrigger_from_RecordBase:
def get_CaseTrigger_from_RecordBase(record_set, Trigger_Args, df_case_raw=None):
    """Find trigger timestamps in the RecordSet.

    Args:
        record_set: RecordSet instance
        Trigger_Args: Dict with trigger configuration
        df_case_raw: Optional pre-existing raw case DataFrame

    Returns:
        dict: {'df_case': DataFrame, 'df_lts': DataFrame, 'df_Human_Info': DataFrame}
    """
    ...
```

---

CaseFn Module Structure
========================

**CRITICAL:** fn_CaseFn takes 6 positional parameters and returns SUFFIX-ONLY keys.

```python
# Module-level metadata (all required):
# Example (illustrative -- actual HumanFn/RecordFn/CaseFn names from ls commands):
CaseFnName = "<CaseFnName>"

RO_to_ROName = {'RO': 'h<HumanFnName>.r<RecordFnName>.c<CkpdName>'}  # 3-PART ROName format!

Ckpd_to_CkpdObsConfig = {'<CkpdName>': {
    'DistStartToPredDT': -1440,     # Minutes from trigger to window start
    'DistEndToPredDT': 5,           # Minutes from trigger to window end
    'TimeUnit': 'min',
    'StartIdx5Min': -288,           # Index offset (domain unit) for start
    'EndIdx5Min': 1                 # Index offset for end
}}

ROName_to_RONameInfo = {
    'h<HumanFnName>.r<RecordFnName>.c<CkpdName>': {  # 3-part: h{Human}.r{Record}.c{Ckpd}
        'HumanName': '<HumanFnName>',
        'RecordName': '<RecordFnName>',
        'CkpdName': '<CkpdName>'
    }
}

HumanRecords = {'<HumanFnName>': ['<RecordFnName>']}

COVocab = {
    'tid2tkn': ['<Pad>', '<UNK>'],
    'tkn2tid': {'<Pad>': 0, '<UNK>': 1}
}

# Main function -- 6 POSITIONAL PARAMETERS:
def fn_CaseFn(case_example, ROName_list, ROName_to_ROData,
              ROName_to_ROInfo, COVocab, context):
    """Extract features at the trigger timepoint.

    Args:
        case_example: Current case being processed (pd.Series or dict)
        ROName_list: List of RONames (e.g., ['h<HumanFnName>.r<RecordFnName>.c<CkpdName>'])
        ROName_to_ROData: Dict mapping ROName to extracted DataFrame
        ROName_to_ROInfo: Dict mapping ROName to parsed info dict
        COVocab: Vocabulary dict {tid2tkn: [...], tkn2tid: {...}}
        context: FeatureContext for external data access

    Returns:
        dict with SUFFIX-ONLY keys:
        {'--tid': [...], '--wgt': [...], '--val': [...]}
        Pipeline adds CaseFnName prefix: <CaseFnName>--tid
    """
    ROName = ROName_list[0]
    ROData = ROName_to_ROData.get(ROName)

    if ROData is None or len(ROData) == 0:
        return {'--tid': [1] * 288}          # SUFFIX-ONLY!

    values = ROData['BGValue'].fillna(1).astype(int).values.tolist()
    return {'--tid': values}                  # SUFFIX-ONLY!

# MetaDict -- required for builder code generation:
MetaDict = {
    "CaseFnName": CaseFnName,
    "RO_to_ROName": RO_to_ROName,
    "Ckpd_to_CkpdObsConfig": Ckpd_to_CkpdObsConfig,
    "ROName_to_RONameInfo": ROName_to_RONameInfo,
    "HumanRecords": HumanRecords,
    "COVocab": COVocab,
    "fn_CaseFn": fn_CaseFn
}
```

---

How Pipeline Calls CaseFn
==========================

The pipeline adds the CaseFnName prefix to your suffix-only return keys:

```python
# Inside Case_Pipeline (case_pipeline.py, lines 438-453):
feature_result = fn_CaseFn(
    case, ROName_list, ROName_to_ROData, ROName_to_RONameInfo, COVocab, context
)
for feat_name, feat_value in feature_result.items():
    col_name = f"{cf_name}{feat_name}"    # e.g., "CGMValueBf24h" + "--tid"
    case_features[col_name] = feat_value
```

So if your CaseFn returns `{'--tid': [...], '--wgt': [...]}`, the pipeline
creates columns `CGMValueBf24h--tid` and `CGMValueBf24h--wgt`.

---

CaseFn Output Suffixes
========================

```
Suffix     | Meaning              | Example
-----------+----------------------+-----------------------------------
--tid      | Token ID list        | [120, 125, 130, ...]
--wgt      | Weight list          | [1.0, 1.0, 0.5, ...]
--val      | Value dict/list      | {"gender": "M", "age": 45}
--str      | String/JSON          | '[{"type":"diet","carbs":30}]'
(none)     | Raw scalar value     | "M_40-64_T1D"
```

---

ROName 3-Part Format
====================

ROName uses a **3-part** format: `h{Human}.r{Record}.c{Checkpoint}`

```
h<HumanFnName>.r<RecordFnName>.c<CkpdName>
|               |               +-- Checkpoint suffix (window)
|               +-- Record name
+-- Human name (h prefix)
```

This maps to ROName_to_RONameInfo:

```python
# Example (illustrative -- discover actual HumanFn/RecordFn names with ls):
ROName_to_RONameInfo = {
    'h<HumanFnName>.r<RecordFnName>.c<CkpdName>': {
        'HumanName': '<HumanFnName>',
        'RecordName': '<RecordFnName>',
        'CkpdName': '<CkpdName>'
    }
}
```

The 3-part format is domain-general. Any Human/Record/Checkpoint combination works:
- `h<HumanFn>.r<LabRecord>.cBf7d` -- Lab values, 7 days before
- `h<HumanFn>.r<VitalSign>.cBf1h` -- Vital signs, 1 hour before

---

Ckpd_to_CkpdObsConfig Keys
=============================

Each checkpoint (window) is defined by these keys:

```python
Ckpd_to_CkpdObsConfig = {'Bf24h': {
    'DistStartToPredDT': -1440,     # Minutes from trigger to window START
    'DistEndToPredDT': 5,           # Minutes from trigger to window END
    'TimeUnit': 'min',              # Time unit for Dist fields
    'StartIdx5Min': -288,           # Index offset (5-min units) for start
    'EndIdx5Min': 1                 # Index offset for end
}}
```

**Common configurations:**

```
Window  | DistStart | DistEnd | StartIdx | EndIdx | Meaning
--------+-----------+---------+----------+--------+-------------------
Bf24h   | -1440     | 5       | -288     | 1      | 24h before trigger
Af24h   | -5        | 1440    | -1       | 288    | 24h after trigger
Bf2h    | -120      | 5       | -24      | 1      | 2h before trigger
Af2h    | -5        | 120     | -1       | 24     | 2h after trigger
Base    | 0         | 0       | 0        | 0      | Static (no window)
```

---

Record Object Access Pattern
==============================

CaseFn accesses data through ROName_to_ROData:

```python
# Access data for the case's entity (windowed by checkpoint)
ROName = ROName_list[0]                           # 'h<HumanFnName>.r<RecordFnName>.c<CkpdName>'
ROData = ROName_to_ROData.get(ROName)             # DataFrame with windowed data

# Access specific columns (discover actual column names with head -30 on the RecordFn file)
values = ROData['<ValueCol>'].values
timestamps = ROData['<DatetimeCol>'].values

# Access ROName info
ROInfo = ROName_to_ROInfo[ROName]                 # {'HumanName', 'RecordName', 'CkpdName'}
```

---

MUST DO
=======

- **Present** plan to user -> **get** approval -> **execute**
- **Activate** .venv and **source** env.sh before running builders
- **Follow** [BOILERPLATE] + [CUSTOMIZE] pattern in builders
- **Set** RUN_TEST = True in builder
- **Follow** `<Feature><Window>` naming convention for CaseFn names
- **Use** 3-part ROName format: `h<HumanFnName>.r<RecordFnName>.c<CkpdName>`
- **Declare** ROName_to_RONameInfo with all data dependencies
- **Return** suffix-only keys from fn_CaseFn (e.g., `'--tid'`, NOT `'<CaseFnName>--tid'`)
- **Name** trigger function `get_CaseTrigger_from_RecordBase` (NOT fn_TriggerFn)
- **Include** Ckpd_to_CkpdObsConfig with DistStartToPredDT/StartIdx5Min keys
- **Include** MetaDict at end of CaseFn module
- **Include** HumanRecords mapping Human -> Record list

---

MUST NOT
========

- **NEVER edit** code/haifn/fn_case/ directly -- always use builders
- **NEVER skip** builder -> generate -> test cycle
- **NEVER invent** feature names outside `<Feature><Window>` convention
- **NEVER access** Record data without declaring in ROName_to_RONameInfo
- **NEVER prefix** return keys with CaseFnName -- pipeline does that automatically
- **NEVER use** 2-part ROName (must be 3-part: h{Human}.r{Record}.c{Ckpd})
- **NEVER skip** RUN_TEST in builder
- **NEVER break** existing CaseFn schemas
- **NEVER skip** `source env.sh` -- store paths depend on environment variables
