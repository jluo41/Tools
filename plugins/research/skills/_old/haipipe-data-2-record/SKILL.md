Skill: haipipe-data-2-record
=============================

Layer 2 of the 6-layer data pipeline: Record Processing.

Converts a SourceSet into temporally-aligned structured records (RecordSet).
Each entity gets a Human wrapper with linked Record objects.

**Scope of this skill:** Framework patterns only. It does not catalog
project-specific state (which Fns are registered, column names, cohort names).
That state is always discovered at runtime from the filesystem.
This skill applies equally to any domain: CGM, EHR, wearables, ecology, etc.

Four subcommands:

  /haipipe-data-2-record load           Inspect existing RecordSet
  /haipipe-data-2-record cook           Run Record_Pipeline with config
  /haipipe-data-2-record design-chef    Create new HumanFn/RecordFn via builder
  /haipipe-data-2-record design-kitchen Upgrade Record_Pipeline infra

On invocation, read this file for shared rules, then read the matching
subcommand file (1-load.md, 2-cook.md, 3-design-chef.md, 4-design-kitchen.md).

---

Architecture Position
=====================

```
Layer 1: Source           Raw files -> standardized tables (SourceSet)
    |
Layer 2: Record   <---   SourceSet -> temporally-aligned records (RecordSet)
    |
Layer 3: Case             RecordSet -> event-triggered feature extraction
    |
Layer 4: AIData           CaseSet -> ML-ready datasets (train/val/test)
    |
Layer 5: Model            DataSet -> trained model artifacts
    |
Layer 6: Endpoint         Model -> deployment packages
```

---

Cooking Metaphor
================

```
Kitchen  = Record_Pipeline class     (code/haipipe/record_base/)
Chef     = HumanFn + RecordFn        (code/haifn/fn_record/)        -- GENERATED
Recipe   = YAML config file          (config/ or tutorials/config/)
Dish     = RecordSet asset           (_WorkSpace/2-RecStore/)
Academy  = Builder scripts           (code-dev/1-PIPELINE/2-Record-WorkSpace/)
```

---

What Is a RecordSet?
====================

A RecordSet is a container that holds Human and Record objects in a flat
dictionary called **Name_to_HRF**. Keys are either strings (for Humans) or
tuples (for Records):

```python
# Example (illustrative -- actual names depend on which HumanFns/RecordFns were used)
record_set.Name_to_HRF = {
    '<HumanFnName>':                   <Human object>,   # string key
    ('<HumanFnName>', '<RecordFn1>'): <Record object>,   # tuple key
    ('<HumanFnName>', '<RecordFn2>'): <Record object>,   # tuple key
    ...
}
```

**The HumanRecords mapping is fully domain-configurable.** Any HumanFn can
be paired with any RecordFns that share the same RawHumanID. The actual
names depend on what is registered in code/haifn/fn_record/. Always
discover at runtime:
```bash
ls code/haifn/fn_record/human/    # available HumanFns
ls code/haifn/fn_record/record/   # available RecordFns
```

**Directory structure is FLAT** (not hierarchical by entity):

```
_WorkSpace/2-RecStore/{RecordSetName}/
+-- Human-{HumanName}/              # One per Human (FLAT naming)
|   +-- df_Human.parquet
|   +-- schema.json
+-- Record-{HumanName}.{RecordName}/  # FLAT: one per (Human, Record) pair
|   +-- df_RecAttr.parquet
|   +-- df_RecIndex.parquet
+-- ...                             # one per additional (Human, Record) pair
+-- Extra-{name}/                   # Optional extra DataFrames
+-- manifest.json
+-- _cache/
```

**It is NOT hierarchical** like `{HumanName}/{EntityID}/{RecordName}/`. It is flat.

---

5-Minute Alignment (CGM Domain-Specific)
=========================================

In the CGM domain, all records are aligned to a 5-minute time grid:

- **DT_s**: Datetime column with 5-min intervals (00:00, 00:05, 00:10, ...)
- Continuous records (CGM): One row per 5-min interval
- Event records (Diet, Med, Exercise): Snapped to nearest 5-min boundary
- Missing intervals: Left as gaps (not filled with NaN)

**Note:** 5-minute alignment is specific to the CGM domain. Other domains
(e.g., EHR with daily encounters) may use different temporal alignment.

---

Concrete Code From the Repo
=============================

**Creating and running a pipeline** (code/haipipe/record_base/record_pipeline.py):

```python
from haipipe.record_base import Record_Pipeline

# Config keys: HumanRecords (dict), record_set_version (int, default 0)
config = {
    # Example (illustrative -- use actual HumanFn/RecordFn names from ls command)
    'HumanRecords': {'<HumanFnName>': ['<RecordFn1>', '<RecordFn2>']},
    'record_set_version': 0
}
pipeline = Record_Pipeline(config, SPACE)

record_set = pipeline.run(
    source_set,                          # SourceSet (required)
    partition_index=None,                # 0-based partition index
    partition_number=None,               # Total partitions
    record_set_label=1,                  # Label for ID generation
    use_cache=True,                      # Load cached if available
    save_cache=True,                     # Save to cache
    profile=False                        # Return timing if True
)
# Name is auto-generated by _generate_record_set_name()
# Pattern: "<CohortName>_v<N>RecSet"
# e.g., source_set_name "<Cohort>/@<SourceFn>" + version 0 -> "<Cohort>_v0RecSet"
```

**Saving a RecordSet** (code/haipipe/assets.py):

```python
record_set.save_to_disk()  # auto-generates path from SPACE
```

**Loading a RecordSet** (code/haipipe/assets.py):

```python
record_set = RecordSet.load_from_disk(path='/full/path/to/record_set', SPACE=SPACE)
record_set = RecordSet.load_asset(path='<CohortName>_v<N>RecSet', SPACE=SPACE)
```

**Accessing data via Name_to_HRF** (code/haipipe/record_base/record_set.py):

```python
# Always list keys first -- names depend on what was registered
for key in record_set.Name_to_HRF:
    print(key)   # string = Human, tuple = (HumanName, RecordName)

# Access Human (string key -- example illustrative)
human = record_set.Name_to_HRF['<HumanFnName>']

# Access Record (tuple key -- example illustrative)
record = record_set.Name_to_HRF[('<HumanFnName>', '<RecordFnName>')]

# RecordSet info summary
record_set.info()
```

**HumanFn module structure** (code/haifn/fn_record/human/<HumanFnName>.py):

```python
# Module-level (example illustrative -- field values vary by domain):
OneHuman_Args = {'HumanName': '<HumanFnName>', 'HumanID': '<HumanIDCol>',
                 'RawHumanID': '<RawIDCol>', ...}
Excluded_RawNameList = ['<TableName1>', '<TableName2>', ...]

def get_RawHumanID_from_dfRawColumns(dfRawColumns):
    # Returns the raw entity ID column name given available columns
    ...

MetaDict = {
    "OneHuman_Args": OneHuman_Args,
    "Excluded_RawNameList": Excluded_RawNameList,
    "get_RawHumanID_from_dfRawColumns": get_RawHumanID_from_dfRawColumns
}
```

**RecordFn module structure** (code/haifn/fn_record/record/<RecordFnName>.py):

```python
# Module-level (example illustrative -- field values vary by record type):
OneRecord_Args = {'RecordName': '<RecordFnName>', 'RecID': '<RecordFnName>ID', ...}
RawName_to_RawConfig = {'<SourceTableName>': {'raw_columns': [...], ...}}
attr_cols = ['<IDCol>', '<DatetimeCol>', '<ValueCol>', ...]

def get_RawRecProc_for_HumanGroup(df_RawRec_for_HumanGroup, OneRecord_Args, df_Human):
    # Process raw data into aligned records
    # See 3-design-chef.md for decision tree and pattern templates
    ...
```

---

Discovering Available Fns
==========================

Do not rely on a hardcoded list -- always discover at runtime:

```bash
# Registered HumanFns
ls code/haifn/fn_record/human/

# Registered RecordFns
ls code/haifn/fn_record/record/

# Corresponding builder scripts
ls code-dev/1-PIPELINE/2-Record-WorkSpace/h*.py   # HumanFn builders
ls code-dev/1-PIPELINE/2-Record-WorkSpace/r*.py   # RecordFn builders
```

Each RecordFn in code/haifn/fn_record/record/ has a matching builder in
code-dev/1-PIPELINE/2-Record-WorkSpace/. The builder is the source of truth.

---

Fn Type Overview
=================

**HumanFn** -- defines the entity (who is tracked):
- One per entity type per project (e.g., HmPatient, HmAnimal, HmDevice)
- Customizes: entity ID mapping, which tables to exclude from entity roster
- Build when: new entity type, or existing entity with different ID column name

**RecordFn** -- processes one data table into time-aligned records:
- Many per project (one per source data type)
- Falls into four signal patterns (see 3-design-chef.md):

```
Pattern A: Dense/Continuous  -- regular-interval sensor signals; aggregation: FIRST
Pattern B: Sparse/Additive   -- accumulating events;            aggregation: SUM
Pattern C: Sparse/Mean       -- repeat measurements;            aggregation: MEAN
Pattern D: Sparse/First      -- discrete events;                aggregation: FIRST
```

To build either type: /haipipe-data-2-record design-chef

---

Prerequisites
=============

1. Python virtual environment activated (see note below)
2. Environment variables loaded: `source env.sh`
3. Input SourceSet must exist at `_WorkSpace/1-SourceStore/<source_set_name>/`
4. If SourceSet does not exist, run Source_Pipeline first (see haipipe-data-1-source cook)

**Venv Usage in Claude Code**

`source .venv/bin/activate` does NOT persist across Bash tool calls in Claude Code.
Always use one of these two approaches instead:

```bash
# Approach 1: chain in a single call (for scripts)
source .venv/bin/activate && source env.sh && python <script.py>

# Approach 2: call venv python directly (for one-liners)
.venv/bin/python <script.py>
.venv/bin/python -c "import pandas; ..."

# Discover the exact binary name first (may differ by project)
ls .venv/bin/python*    # e.g., python, python3, python3.14
```

---

MUST DO (All Subcommands)
=========================

1. **Activate** .venv: use `source .venv/bin/activate && source env.sh` in one call,
   OR call venv python directly: `.venv/bin/python script.py`
   (discover binary with `ls .venv/bin/python*`)
2. **Load** environment: `source env.sh` (always chain with activate in one call)
3. **Verify** that input SourceSet exists before running Record_Pipeline
4. **Use** the correct load API: `RecordSet.load_from_disk(path=..., SPACE=SPACE)`
5. **Access** data via Name_to_HRF with string keys (Human) and tuple keys (Record)
6. **Present** plan to user and **get** approval before any code changes
7. **Remember** that output of Layer 2 = input of Layer 3 (Case)

---

MUST NOT (All Subcommands)
==========================

1. **NEVER edit** code/haifn/ directly (100% generated from builders)
2. **NEVER run** Python without .venv activated
3. **NEVER skip** `source env.sh` (store paths come from environment variables)
4. **NEVER use** fabricated APIs like `record_set.items()`, `human.records`, or `record.data`
5. **NEVER assume** hierarchical directory structure (it is FLAT: Human-X/, Record-X.Y/)
6. **NEVER pass** `cohort_name` to `pipeline.run()` (does not exist as a parameter)
7. **NEVER use** `load_from_disk(set_name=..., store_key=...)` (does not exist)
8. **NEVER change** attr_cols without updating all downstream CaseFn references

---

Key File Locations
==================

```
Pipeline framework:   code/haipipe/record_base/record_pipeline.py
                      code/haipipe/record_base/record_set.py
                      code/haipipe/assets.py
Fn loaders:           code/haipipe/record_base/builder/human.py
                      code/haipipe/record_base/builder/record.py

Generated HumanFns:   code/haifn/fn_record/human/          <- discover with ls
Generated RecordFns:  code/haifn/fn_record/record/          <- discover with ls

Builders (edit these): code-dev/1-PIPELINE/2-Record-WorkSpace/h*.py   <- HumanFn builders
                       code-dev/1-PIPELINE/2-Record-WorkSpace/r*.py   <- RecordFn builders

Test configs:         config/                  <- discover with ls config/
Store path:           _WorkSpace/2-RecStore/
```
> JL: config can be anywhere. Maybe we can put the config yaml to the code-dev it make it more consistent in the future for an easier reference. 
---

See Also
========

- **haipipe-data-1-source**: How raw data becomes SourceSets (input to this layer)
- **haipipe-data-3-case**: How RecordSets become CaseSets (output of this layer)
- **haipipe-data-4-aidata**: How CaseSets become ML-ready datasets

---

File Layout
===========

```
haipipe-data-2-record/
+-- SKILL.md              This file (router + shared rules)
+-- README.md             Quick reference
+-- 1-load.md               /haipipe-data-2-record load
+-- 2-cook.md               /haipipe-data-2-record cook
+-- 3-design-chef.md        /haipipe-data-2-record design-chef
+-- 4-design-kitchen.md     /haipipe-data-2-record design-kitchen
+-- templates/
    +-- config.yaml       Config template for cook subcommand
```
