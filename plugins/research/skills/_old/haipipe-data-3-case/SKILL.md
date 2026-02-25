Skill: haipipe-data-3-case
==========================

Layer 3 of the 6-layer data pipeline: Case Processing.

Converts a RecordSet into event-triggered cases (CaseSet). A TriggerFn
identifies time points of interest. CaseFn functions extract features
around each trigger point using Record Objects (RO).

**Scope of this skill:** Framework patterns only. It does not catalog
project-specific state (which TriggerFns/CaseFns are registered, feature names,
column names). That state is always discovered at runtime from the filesystem.
This skill applies equally to any domain: CGM, EHR, wearables, ecology, etc.

Four subcommands:

  /haipipe-data-3-case load           Inspect existing CaseSet
  /haipipe-data-3-case cook           Run Case_Pipeline with config
  /haipipe-data-3-case design-chef    Create new TriggerFn/CaseFn via builder
  /haipipe-data-3-case design-kitchen Upgrade Case_Pipeline infra

On invocation, read this file for shared rules, then read the matching
subcommand file (1-load.md, 2-cook.md, 3-design-chef.md, 4-design-kitchen.md).

---

Architecture Position
=====================

```
Layer 1: Source          Raw files -> standardized tables
    |
Layer 2: Record          SourceSet -> temporally-aligned entity records
    |
Layer 3: Case    <---    RecordSet -> event-triggered feature extraction
    |
Layer 4: AIData          CaseSet -> ML-ready datasets (train/val/test)
    |
Layer 5: Model           AIData -> trained model artifacts
    |
Layer 6: Endpoint        Model -> deployment packages
```

---

Cooking Metaphor
================

```
Kitchen  = Case_Pipeline class       (code/haipipe/case_base/)
Chef     = TriggerFn + CaseFn        (code/haifn/fn_case/)         -- GENERATED
Recipe   = YAML config file          (config/caseset/ or tutorials/config/)
Dish     = CaseSet asset             (_WorkSpace/3-CaseStore/)
Academy  = Builder scripts           (code-dev/1-PIPELINE/3-Case-WorkSpace/)
```

---

What Is a CaseSet?
==================

A CaseSet is the output of Layer 3. It contains one base table (df_case.parquet)
with trigger metadata, plus one @-prefixed parquet per CaseFn with extracted
features. All files live at the ROOT level of the CaseSet directory -- there
is NO CaseFn/ subdirectory.

**CaseSet directory structure:**

```
_WorkSpace/3-CaseStore/{RecSetName}/@v{N}CaseSet-{TriggerFolder}/
+-- df_case.parquet              Base case data (EntityID, ObsDT, trigger cols)
+-- df_lts.parquet               LTS segments (optional, for LTS triggers)
+-- df_Human_Info.parquet        Entity metadata (optional)
+-- @<CaseFnName1>.parquet       CaseFn features (at ROOT, NOT in subdirectory)
+-- @<CaseFnName2>.parquet       Another CaseFn (at ROOT)
+-- cf_to_cfvocab.json           Vocabulary per CaseFn
+-- manifest.json
```

**CRITICAL:** CaseFn files are `@{CaseFnName}.parquet` at ROOT level. The main
file is `df_case.parquet`, NOT `case_data.parquet`.

---

Feature Naming Convention
=========================

All CaseFn names follow `<Feature><Window>`:

**Window Suffixes:**

```
Suffix      | Meaning                  | Example
------------+--------------------------+--------------------------
Bf24h       | Before 24 hours          | <Feature>Bf24h
Af24h       | After 24 hours           | <Feature>Af24h
Bf2h        | Before 2 hours           | <Feature>Bf2h
Af2h        | After 2 hours            | <Feature>Af2h
Af2to8h     | After 2 to 8 hours       | <Feature>Af2to8h
CrntTime    | Current time features    | <Feature>CrntTime
Base        | Baseline (no window)     | <Feature>Base
Bf7d        | Before 7 days            | <Feature>Bf7d
Af30d       | After 30 days            | <Feature>Af30d
```

This convention is domain-general. The Feature prefix names are discovered
at runtime from the registered CaseFns:

```bash
ls code/haifn/fn_case/case_casefn/    # all registered CaseFns
```

---

ROName 3-Part Format
====================

CaseFn accesses entity data through Record Objects using a **3-part** ROName:

```
h<HumanFnName>.r<RecordFnName>.c<CkpdName>
|              |               +-- Checkpoint suffix (window)
|              +-- Record name
+-- Human name (h prefix)
```

The 3 parts map to ROName_to_RONameInfo:

```python
# Example (illustrative -- actual names depend on registered HumanFns/RecordFns):
ROName_to_RONameInfo = {
    'h<HumanFnName>.r<RecordFnName>.c<CkpdName>': {
        'HumanName': '<HumanFnName>',
        'RecordName': '<RecordFnName>',
        'CkpdName': '<CkpdName>'
    }
}
```

Discover available HumanFn and RecordFn names:

```bash
ls code/haifn/fn_record/human/    # registered HumanFns
ls code/haifn/fn_record/record/   # registered RecordFns
```

---

Trigger vs CaseFn Separation
=============================

```
+-------------------------------------------+
|  TriggerFn                                |
|  - Identifies WHEN cases happen           |
|  - Outputs: df_case, df_lts, df_Human_Info|
|  - Function: get_CaseTrigger_from_RecordBase()
+---------------------+---------------------+
                      |
                      v
+-------------------------------------------+
|  CaseFn (one or more per trigger)         |
|  - Extracts WHAT features at trigger      |
|  - Accesses Record Objects (RO)           |
|  - Function: fn_CaseFn() with 6 params   |
|  - Returns: dict with SUFFIX-ONLY keys    |
+-------------------------------------------+
```

---

Concrete Code From the Repo
============================

**CaseFn module structure** (code/haifn/fn_case/case_casefn/<CaseFnName>.py):

```python
# Example (illustrative -- actual names/values depend on domain and data):
CaseFnName = "<CaseFnName>"

RO_to_ROName = {'RO': 'h<HumanFnName>.r<RecordFnName>.c<CkpdName>'}  # 3-PART format!

Ckpd_to_CkpdObsConfig = {'<CkpdName>': {
    'DistStartToPredDT': -1440,     # Minutes from trigger to window start
    'DistEndToPredDT': 5,           # Minutes from trigger to window end
    'TimeUnit': 'min',
    'StartIdx5Min': -288,           # Index offset (domain-unit) for start
    'EndIdx5Min': 1                 # Index offset for end
}}

ROName_to_RONameInfo = {
    'h<HumanFnName>.r<RecordFnName>.c<CkpdName>': {
        'HumanName': '<HumanFnName>',
        'RecordName': '<RecordFnName>',
        'CkpdName': '<CkpdName>'
    }
}

HumanRecords = {'<HumanFnName>': ['<RecordFnName>']}

COVocab = {'tid2tkn': ['<Pad>', '<UNK>'], 'tkn2tid': {'<Pad>': 0, '<UNK>': 1}}

# Main function -- 6 POSITIONAL PARAMETERS:
def fn_CaseFn(case_example, ROName_list, ROName_to_ROData,
              ROName_to_ROInfo, COVocab, context):
    """Extract features from the Record Object data."""
    ROName = ROName_list[0]
    ROData = ROName_to_ROData.get(ROName)

    if ROData is None or len(ROData) == 0:
        return {'--<suffix>': <empty_value>}         # SUFFIX-ONLY key!

    # ... feature extraction logic ...

    return {'--<suffix>': <feature_value>}           # SUFFIX-ONLY key!
```

**CRITICAL:** Return keys are SUFFIX-ONLY (e.g., `'--tid'`, `'--wgt'`, `'--val'`).
The pipeline adds the CaseFnName prefix automatically:

```python
# Inside Case_Pipeline (case_pipeline.py):
feature_result = fn_CaseFn(
    case, ROName_list, ROName_to_ROData, ROName_to_RONameInfo, COVocab, context
)
for feat_name, feat_value in feature_result.items():
    col_name = f"{cf_name}{feat_name}"    # e.g., "<CaseFnName>--tid"
    case_features[col_name] = feat_value
```

**TriggerFn module structure** (code/haifn/fn_case/fn_trigger/<TriggerFnName>.py):

```python
# Example (illustrative -- actual names/values depend on domain and trigger type):
Trigger = "<TriggerFnName>"

Trigger_Args = {
    'Trigger': '<TriggerFnName>',
    'case_id_columns': ['<EntityID>', '<ObsDT>'],
    'case_raw_id_columns': ['<RawEntityID>', '<ObsDT>'],
    'HumanID_list': ['<EntityID>'],
    'ObsDT': '<ObsDT>',
    'ROName_to_RONameArgs': {
        'h<HumanFnName>.r<RecordFnName>': {
            'attribute_columns': ['<EntityID>', '<DatetimeCol>', '<ValueCol>'],
            'RecDT': '<DatetimeCol>'
        }
    },
    # Trigger-specific args (e.g., for LTS triggers):
    'min_segment_length': 36,
    'stride': 12,
    ...
}

# CRITICAL: Function name is get_CaseTrigger_from_RecordBase, NOT fn_TriggerFn!
def get_CaseTrigger_from_RecordBase(record_set, Trigger_Args, df_case_raw=None):
    """Returns dict: {'df_case': ..., 'df_lts': ..., 'df_Human_Info': ...}"""
    ...
```

**Case_Pipeline** (code/haipipe/case_base/case_pipeline.py):

```python
pipeline = Case_Pipeline(config, SPACE, context=None)

case_set = pipeline.run(
    df_case=None,           # Optional pre-generated case DataFrame
    df_case_raw=None,       # Optional raw trigger results
    record_set=record_set,  # RecordSet (required)
    use_cache=True,         # Load cached CaseFn features
    profile=False           # Return timing if True
)
```

---

Discovering Available Fns
==========================

Do not rely on a hardcoded list -- always discover at runtime:

```bash
# Registered TriggerFns
ls code/haifn/fn_case/fn_trigger/

# Registered CaseFns
ls code/haifn/fn_case/case_casefn/

# Corresponding builder scripts
ls code-dev/1-PIPELINE/3-Case-WorkSpace/a*.py   # TriggerFn builders
ls code-dev/1-PIPELINE/3-Case-WorkSpace/c*.py   # CaseFn builders

# Inspect a CaseFn's ROName and Ckpd config
head -30 code/haifn/fn_case/case_casefn/<CaseFnName>.py
```

---

Prerequisites
=============

Before working with Layer 3:

1. **Activate** .venv: `source .venv/bin/activate`
2. **Load environment**: `source env.sh`
3. **Input RecordSet** must exist at `_WorkSpace/2-RecStore/<record_set_name>/`
4. **Packages** installed: `pip install -e ".[dev]"`

---

MUST DO (All Subcommands)
=========================

1. **Activate** .venv first: `source .venv/bin/activate`
2. **Load** environment: `source env.sh`
3. **Remember** that output of Layer 3 = input of Layer 4 (AIData)
4. **Follow** feature naming `<Feature><Window>` convention
5. **Declare** ROName_to_RONameInfo with all data dependencies in CaseFn
6. **Use** 3-part ROName format: `h<HumanFnName>.r<RecordFnName>.c<CkpdName>`
7. **Return** suffix-only keys from fn_CaseFn (e.g., `'--tid'`, not `'<CaseFnName>--tid'`)
8. **Name** trigger function `get_CaseTrigger_from_RecordBase` (not fn_TriggerFn)
9. **Present** plan to user and **get approval** before any code changes

---

MUST NOT (All Subcommands)
==========================

1. **NEVER edit** code/haifn/ directly (100% generated from builders)
2. **NEVER run** Python without .venv activated
3. **NEVER skip** `source env.sh` (store paths come from environment variables)
4. **NEVER invent** feature names outside `<Feature><Window>` convention
5. **NEVER access** Record data without going through ROName_to_ROData
6. **NEVER skip** the TriggerFn + CaseFn separation
7. **NEVER prefix** return keys with CaseFnName -- pipeline does that automatically
8. **NEVER assume** CaseFn parquets live in a CaseFn/ subdirectory -- they are at ROOT

---

Key File Locations
==================

```
Pipeline framework:   code/haipipe/case_base/case_pipeline.py
                      code/haipipe/case_base/case_set.py
                      code/haipipe/case_base/case_utils.py
Fn loaders:           code/haipipe/case_base/builder/triggerfn.py
                      code/haipipe/case_base/builder/casefn.py
                      code/haipipe/case_base/builder/rotools.py

Generated TriggerFns: code/haifn/fn_case/fn_trigger/    <- discover with ls
Generated CaseFns:    code/haifn/fn_case/case_casefn/   <- discover with ls

Builders (edit these): code-dev/1-PIPELINE/3-Case-WorkSpace/  <- discover with ls

Test configs:         config/                 <- discover with ls config/
Store path:           _WorkSpace/3-CaseStore/
```

---

See Also
========

- **haipipe-data-1-source**: How raw data becomes SourceSets
- **haipipe-data-2-record**: How SourceSets become RecordSets (input to this layer)
- **haipipe-data-4-aidata**: How CaseSets become ML-ready datasets (output of this layer)

---

File Layout
===========

```
haipipe-data-3-case/
+-- SKILL.md              This file (router + shared rules)
+-- README.md             Quick reference
+-- 1-load.md             /haipipe-data-3-case load
+-- 2-cook.md             /haipipe-data-3-case cook
+-- 3-design-chef.md      /haipipe-data-3-case design-chef
+-- 4-design-kitchen.md   /haipipe-data-3-case design-kitchen
+-- templates/
    +-- config.yaml       Config template for cook subcommand
```
