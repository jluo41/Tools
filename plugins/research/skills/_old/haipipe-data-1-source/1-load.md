Subcommand: load
================

Purpose: Inspect existing SourceSet assets (read-only).

Use this when you need to understand what data exists, verify schemas,
check row counts, or debug data quality issues.
This subcommand applies to any domain -- any SourceSet, any cohort format.

---

What To Read
============

```
_WorkSpace/1-SourceStore/
    <CohortName1>/
        @<SourceFnName>/
            <ProcName1>.parquet
            <ProcName2>.parquet
            ...
            manifest.json
    <CohortName2>/
        @<SourceFnName>/
            ...
    ...
```

To see what actually exists:
```bash
ls _WorkSpace/1-SourceStore/                         # available cohorts
ls _WorkSpace/1-SourceStore/<CohortName>/@<SourceFnName>/  # its tables
```

**Directory naming convention:** `{raw_data_name}/@{SourceFnName}/`

---

Load API
========

There are two equivalent class methods for loading a SourceSet from disk.
Both take a **path** parameter (the full path to the asset directory) and
an optional **SPACE** dict.

```python
from haipipe.source_base import SourceSet

# Approach 1: load_from_disk
source_set = SourceSet.load_from_disk(
    path='_WorkSpace/1-SourceStore/<CohortName>/@<SourceFnName>',
    SPACE=SPACE
)

# Approach 2: load_asset (equivalent -- also handles remote paths)
source_set = SourceSet.load_asset(
    path='_WorkSpace/1-SourceStore/<CohortName>/@<SourceFnName>',
    SPACE=SPACE
)
```

**Both methods require a path argument** -- there is no `set_name` or
`store_key` parameter.

**WRONG -- this API does NOT exist:**

```python
# WRONG: load_from_disk does NOT accept set_name= or store_key=
source_set = SourceSet.load_from_disk(set_name='...', store_key='...')
```

---

ProcName_to_ProcDf Access Pattern
===================================

Once loaded, the main data lives in `source_set.ProcName_to_ProcDf`:

```python
# Check which tables are available
print('Tables:', list(source_set.ProcName_to_ProcDf.keys()))

# Access a specific table
df_cgm = source_set.ProcName_to_ProcDf['<ProcName>']
print('Columns:', list(df_cgm.columns))
print('Rows:', len(df_cgm))
```

---

Inspect SourceSet Contents
===========================

```python
# Inspect each table
for name, df in source_set.ProcName_to_ProcDf.items():
    print(f'{name}: {df.shape[0]} rows, {df.shape[1]} cols')
    print(f'  Columns: {list(df.columns)}')
    print(f'  EntityIDs: {df["<EntityIDCol>"].nunique()} unique')
    print()

# Pretty-print summary
source_set.info()
```

---

Inspection Checklist
====================

1. **Table existence** -- Check which ProcName tables are present
   (e.g., CGM, Medication, Diet, Exercise, Ptt)

2. **Schema match** -- Verify column counts match the domain standard:
   - Medication: 11 columns
   - Exercise: 13 columns
   - Diet: 15 columns
   - CGM, Ptt, Height, Weight: dataset-specific

3. **Row counts** -- Each table should have a reasonable number of rows

4. **PatientID consistency** -- The same set of PatientIDs should appear
   across tables (with possible exceptions for tables not every patient has)

5. **JSON metadata** -- Spot-check the `medication`, `nutrition`, `exercise`,
   and `external_metadata` columns for valid JSON strings

6. **DateTime columns** -- Verify temporal columns parse correctly

7. **Manifest** -- Check `manifest.json` for timestamp, source_fn name,
   and per-table row counts and checksums

---

Quick Inspection Commands (Shell)
=================================

```bash
# List available SourceSets
ls _WorkSpace/1-SourceStore/

# List SourceFn versions for a cohort
ls _WorkSpace/1-SourceStore/<CohortName>/

# Check file sizes
du -sh _WorkSpace/1-SourceStore/<CohortName>/@<SourceFnName>/*

# Read manifest
cat _WorkSpace/1-SourceStore/<CohortName>/@<SourceFnName>/manifest.json
```

---

MUST DO
=======

1. **Activate .venv and source env.sh** before any Python inspection
2. **Check existence first** -- use `ls` or try/except before loading
3. **Use the correct API** -- `load_from_disk(path=..., SPACE=...)` or
   `load_asset(path=..., SPACE=...)`

---

MUST NOT
========

1. **NEVER modify** loaded data or any files in _WorkSpace/1-SourceStore/
2. **NEVER assume** data exists -- always check first
3. **NEVER load** without activating .venv and sourcing env.sh
4. **NEVER use** `load_from_disk(set_name=..., store_key=...)` -- this
   signature does not exist; always pass `path=`
