Layer 2: Record
===============

Architecture Position
---------------------

Layer 1: Source -> **Layer 2: Record** <- (SourceSet -> temporally-aligned records)
  -> Layer 3: Case -> Layer 4: AIData -> Layer 5: Model -> Layer 6: Endpoint


Cooking Metaphor
----------------

```
Kitchen  = Record_Pipeline class      (code/haipipe/record_base/)
Chef     = HumanFn + RecordFn         (code/haifn/fn_record/)  GENERATED
Recipe   = YAML config file           (config/ or tutorials/config/)
Dish     = RecordSet asset            (_WorkSpace/2-RecStore/)
Academy  = Builder scripts            (code-dev/1-PIPELINE/2-Record-WorkSpace/)
```


What Is a RecordSet
-------------------

Container with `Name_to_HRF` dict. Keys: string (Human) or tuple (Record).

```python
record_set.Name_to_HRF = {
    '<HumanFnName>': <Human object>,                          # string key
    ('<HumanFnName>', '<RecordFn1>'): <Record object>,        # tuple key
    ('<HumanFnName>', '<RecordFn2>'): <Record object>,
}
```

**Directory structure is FLAT (not hierarchical):**

```
_WorkSpace/2-RecStore/{RecordSetName}/
+-- Human-{HumanName}/                   # FLAT naming
|   +-- df_Human.parquet, schema.json
+-- Record-{HumanName}.{RecordName}/     # FLAT: one per (Human, Record) pair
|   +-- df_RecAttr.parquet, df_RecIndex.parquet
+-- Extra-{name}/  (optional)
+-- manifest.json, _cache/
```

**5-Minute Alignment (CGM domain):** `DT_s` column with 5-min intervals. Domain-specific.


Concrete Code
-------------

```python
from haipipe.record_base import Record_Pipeline

config = {
    'HumanRecords': {
        '<HumanFnName>': ['<RecordFn1>', '<RecordFn2>']
    },
    'record_set_version': 0
}

pipeline = Record_Pipeline(config, SPACE)
record_set = pipeline.run(
    source_set,
    partition_index=None,
    partition_number=None,
    record_set_label=1,
    use_cache=True,
    save_cache=True,
    profile=False
)
# Name auto-generated: "<CohortName>_v<N>RecSet"

record_set.save_to_disk()

record_set = RecordSet.load_from_disk(path='_WorkSpace/2-RecStore/<RecordSet>', SPACE=SPACE)
record_set = RecordSet.load_asset(path='<CohortName>_v<N>RecSet', SPACE=SPACE)
# WRONG: load_from_disk does NOT accept set_name= or store_key=

# Access via Name_to_HRF
for key in record_set.Name_to_HRF:
    print(key)  # string = Human, tuple = (HumanName, RecordName)

human  = record_set.Name_to_HRF['<HumanFnName>']
record = record_set.Name_to_HRF[('<HumanFnName>', '<RecordFnName>')]

record_set.info()
```


HumanFn Module Structure
------------------------

File: `code/haifn/fn_record/human/<HumanFnName>.py`

```python
OneHuman_Args = {
    'HumanName':     '<HumanFnName>',
    'HumanID':       '<HumanIDCol>',
    'RawHumanID':    '<RawIDCol>',
    'HumanIDLength': <N>               # integer length for ID generation (e.g., 10)
}
Excluded_RawNameList = ['<TableName1>', ...]

def get_RawHumanID_from_dfRawColumns(dfRawColumns): ...

MetaDict = {...}
```


RecordFn Module Structure
--------------------------

File: `code/haifn/fn_record/record/<RecordFnName>.py`

```python
OneRecord_Args = {
    'RecordName': '<RecordFnName>',
    'RecID':      '<RecordFnName>ID',
    ...
}
RawName_to_RawConfig = {
    '<SourceTableName>': {'raw_columns': [...], ...}
}
attr_cols = ['<IDCol>', '<DatetimeCol>', '<ValueCol>', ...]

def get_RawRecProc_for_HumanGroup(df_RawRec_for_HumanGroup, OneRecord_Args, df_Human): ...
```


Fn Type Overview
----------------

**HumanFn** -- defines the entity (who is tracked). One per entity type per project.

**RecordFn** -- processes one data table into time-aligned records. Falls into 4 signal patterns:

```
Pattern A: Dense/Continuous   regular-interval sensor    aggregation: FIRST
Pattern B: Sparse/Additive    accumulating events        aggregation: SUM
Pattern C: Sparse/Mean        repeat measurements        aggregation: MEAN
Pattern D: Sparse/First       discrete events            aggregation: FIRST
```


Discovering Available Fns
--------------------------

```bash
ls code/haifn/fn_record/human/
ls code/haifn/fn_record/record/
ls code-dev/1-PIPELINE/2-Record-WorkSpace/h*.py
ls code-dev/1-PIPELINE/2-Record-WorkSpace/r*.py
```


Prerequisites
-------------

```bash
source .venv/bin/activate && source env.sh
```

**NOTE:** `source .venv/bin/activate` does NOT persist across Bash tool calls.
Always chain: `source .venv/bin/activate && source env.sh && python <script>`
Or call venv python directly: `.venv/bin/python script.py`


MUST DO
-------

1. Activate .venv: chain in single call or use `.venv/bin/python` directly
2. Load environment (chain `source env.sh`)
3. Verify input SourceSet exists before running `Record_Pipeline`
4. Use correct load API: `RecordSet.load_from_disk(path=..., SPACE=SPACE)`
5. Access data via `Name_to_HRF` with string (Human) and tuple (Record) keys
6. Present plan and get approval before code changes
7. Remember: output of Layer 2 = input of Layer 3 (Case)


MUST NOT
--------

1. NEVER edit `code/haifn/` directly
2. NEVER run Python without `.venv` activated
3. NEVER skip `source env.sh`
4. NEVER use fabricated APIs like `record_set.items()`, `human.records`, `record.data`
5. NEVER assume hierarchical directory structure (it is FLAT: `Human-X/`, `Record-X.Y/`)
6. NEVER pass `cohort_name` to `pipeline.run()` (does not exist as parameter)
7. NEVER use `load_from_disk(set_name=..., store_key=...)` (does not exist)
8. NEVER change `attr_cols` without updating all downstream CaseFn references


Key File Locations
------------------

```
Pipeline framework:   code/haipipe/record_base/record_pipeline.py
                      code/haipipe/record_base/record_set.py
                      code/haipipe/assets.py
Fn loaders:           code/haipipe/record_base/builder/human.py
                      code/haipipe/record_base/builder/record.py
Generated HumanFns:   code/haifn/fn_record/human/     (discover with ls)
Generated RecordFns:  code/haifn/fn_record/record/    (discover with ls)
Builders (edit here): code-dev/1-PIPELINE/2-Record-WorkSpace/  (discover with ls)
Store path:           _WorkSpace/2-RecStore/
Config template:      templates/2-record/config.yaml
```
