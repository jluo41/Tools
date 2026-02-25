Subcommand: cook
================

Purpose: Run Case_Pipeline with a YAML config (recipe).
Kitchen (Case_Pipeline) + Chef (TriggerFn/CaseFn) already exist.
You write the Recipe (config YAML).
This subcommand applies to any domain.

---

Config Structure
================

The config uses `Case_Args` as a list of operations (trigger, filter, feature stages):

```yaml
# Replace <Placeholders> with actual values.
# To find registered TriggerFns: ls code/haifn/fn_case/fn_trigger/
# To find registered CaseFns:    ls code/haifn/fn_case/case_casefn/
# To find existing RecordSets:   ls _WorkSpace/2-RecStore/

record_set_name: "<RecordSetName>"          # e.g., <CohortName>_v0RecSet

CaseArgs:
  Case_Args:
    # Stage 1: Trigger -- identifies WHEN cases happen
    - TriggerName: <TriggerFnName>           # registered TriggerFn
      TriggerArgs:
          TriggerFolderName: "<TriggerFolder>"
          case_id_columns: ['<EntityID>', '<ObsDT>']
          case_raw_id_columns: ['<RawEntityID>', '<ObsDT>']
          HumanID_list: ['<EntityID>']
          ObsDT: '<ObsDT>'
          ROName_to_RONameArgs:
              'h<HumanFnName>.r<RecordFnName>':
                  attribute_columns: ['<EntityID>', '<DatetimeCol>', '<ValueCol>']
                  RecDT: '<DatetimeCol>'
          # Trigger-specific args (e.g., for LTS triggers):
          # min_segment_length: 288
          # stride: 12

    # Stage 2 (optional): Filter -- removes cases by condition
    # - FilterName: <FilterName>
    #   FilterArgs: {...}

    # Stage 3: Feature extraction -- WHAT features to extract
    - CaseFnName: <GroupLabel>
      CaseFnList:
          - <CaseFnName1>
          - <CaseFnName2>
      CaseFnArgs: {}

  # Also accepted: CaseFn_list at CaseArgs level
  CaseFn_list: ['<CaseFnName1>', '<CaseFnName2>']

  case_set_version: 0          # Output: @v0CaseSet-{TriggerFolderName}/
  use_cache: false              # Set true to reuse cached @CaseFn.parquet files
```

**Required keys:** `record_set_name`, `CaseArgs.Case_Args`, `CaseArgs.case_set_version`

See `templates/config.yaml` for a fully annotated template.

---

How To Run
==========

**CLI command:**

```bash
source .venv/bin/activate
source env.sh
haistep-case --config <your_config>.yaml

# Find existing configs:
ls config/   # look for test-haistep-* or caseset/ subdirectories
```

**Test script:**

```bash
source .venv/bin/activate
source env.sh
python test/test_haistep/test_3_case/test_case.py \
    --config <your_config>.yaml
```

**Python API:**

```python
from haipipe.case_base import Case_Pipeline

pipeline = Case_Pipeline(config, SPACE, context=None)

case_set = pipeline.run(
    df_case=None,           # Optional pre-generated case DataFrame
    df_case_raw=None,       # Optional raw trigger results
    record_set=record_set,  # RecordSet (required)
    use_cache=True,         # Load cached CaseFn features from disk
    profile=False           # Return (case_set, timing) if True
)
```

---

Available Triggers and CaseFns
==============================

Do not rely on a hardcoded list -- always discover at runtime:

```bash
ls code/haifn/fn_case/fn_trigger/    # registered TriggerFns
ls code/haifn/fn_case/case_casefn/   # registered CaseFns
ls code-dev/1-PIPELINE/3-Case-WorkSpace/  # builder scripts
```

To inspect a TriggerFn or CaseFn:
```bash
head -30 code/haifn/fn_case/fn_trigger/<TriggerFnName>.py
head -30 code/haifn/fn_case/case_casefn/<CaseFnName>.py
```

Example (illustrative -- actual names from `ls code/haifn/fn_case/`):

```
TriggerFns: <TriggerFnName1>, <TriggerFnName2>     (discover with ls fn_trigger/)
CaseFns:    <CaseFnName1>, <CaseFnName2>, ...       (discover with ls case_casefn/)
```

If the TriggerFn or CaseFn you need does not exist yet, use: /haipipe-data-3-case design-chef

---

LTS Trigger Configuration
==========================

For CGM5MinLTS trigger, these parameters control case generation:

```yaml
# Segment filtering
min_segment_length: 288       # Min points (288 = 24 hours at 5-min intervals)
max_consecutive_missing: 3    # Max gaps to interpolate (3 = 15 min)

# Sampling strategy
stride: 12                    # Sampling frequency (12 x 5min = hourly)
buffer_start: 240             # Skip first 240 points (20 hours)
buffer_end: 240               # Skip last 240 points (20 hours)

# Event records to attach to LTS segments
event_record_names: ['Diet5Min', 'Med5Min', 'Exercise5Min']
```

---

ROName_to_RONameArgs Format
============================

Record Objects tell Case_Pipeline which data to load for each case:

```yaml
# Example (illustrative -- actual names depend on registered HumanFns/RecordFns):
ROName_to_RONameArgs:
  'h<HumanFnName>.r<RecordFnName>':  # Human(HumanFnName).Record(RecordFnName)
    attribute_columns:                # Columns to load from this record
      - '<EntityID>'
      - '<RawEntityID>'
      - '<DatetimeCol>'
      - '<ValueCol>'
    RecDT: '<DatetimeCol>'            # Datetime column for alignment
  'h<HumanFnName>.r<StaticRecord>':  # Static/demographic record
    attribute_columns:
      - '<EntityID>'
      - '<DemographicCol1>'
      - '<DemographicCol2>'
```

---

Naming Conventions
==================

**Output asset naming:** `@v{N}CaseSet-{TriggerFolderName}`
  Pattern: `@v<N>CaseSet-<TriggerFolder>`

**Store path:** `_WorkSpace/3-CaseStore/{RecSetName}/@v{N}CaseSet-{TriggerFolder}/`

**Feature column naming:** Pipeline auto-prefixes CaseFn returns:
  `<CaseFnName>` + `--<suffix>` -> column `<CaseFnName>--<suffix>`

---

Verification
============

After running, verify the output:

1. **Check** output directory exists in _WorkSpace/3-CaseStore/
2. **Verify** df_case.parquet has expected row count
3. **Verify** @CaseFn.parquet files exist at ROOT (not in subdirectory)
4. **Confirm** all @CaseFn.parquet files have same row count as df_case
5. **Check** manifest.json was created
6. **Load** and inspect (see 1-load.md for pattern)

---

Prerequisites
=============

Before running Case_Pipeline:

1. **Activate** .venv: `source .venv/bin/activate`
2. **Load** environment: `source env.sh`
3. Input RecordSet must **exist** at `_WorkSpace/2-RecStore/{record_set_name}/`
4. If patient_info_path is specified, that file must **exist**
5. If RecordSet does not exist, **run** Record_Pipeline first

---

MUST DO
=======

- **Use** only registered TriggerFn and CaseFn names (discover with ls)
- **Ensure** record_set_name matches an existing RecordSet
- **Specify** ROName_to_RONameArgs with correct attribute_columns
- **Follow** config key format exactly
- **Activate** .venv and **source** env.sh before running

---

MUST NOT
========

- **NEVER invent** TriggerFn/CaseFn names that do not exist in code/haifn/fn_case/
- **NEVER skip** required config keys
- **NEVER create** files in code/haifn/ -- use 3-design-chef if you need new functions
- **NEVER look** for case_data.parquet -- the file is df_case.parquet
- **NEVER expect** CaseFn files in a CaseFn/ subdirectory -- they are @-prefixed at ROOT
