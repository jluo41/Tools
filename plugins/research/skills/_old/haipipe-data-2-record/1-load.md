Subcommand: load
================

Purpose: Inspect existing RecordSet assets (read-only).

Use this when you need to understand record structure, verify temporal
alignment, check record counts, or debug data quality issues.

This subcommand applies to any domain. RecordSet and record names are
always discovered at runtime -- not listed here.

---

What To Read
============

RecordSets live under `_WorkSpace/2-RecStore/`. The directory structure
is **FLAT** (not hierarchical by entity):

```
# Discover what RecordSets exist
ls _WorkSpace/2-RecStore/
```

Directory naming convention: `<CohortName>_v<N>RecSet/`

Each RecordSet has this flat internal structure
(example below is illustrative -- actual Human/Record names depend on
what HumanFns and RecordFns were used when the RecordSet was built):

```
_WorkSpace/2-RecStore/<CohortName>_v<N>RecSet/
+-- Human-<HumanFnName>/              # FLAT: Human-{HumanName}
|   +-- df_Human.parquet
|   +-- schema.json
+-- Record-<HumanFnName>.<RecordFnName>/  # FLAT: Record-{HumanName}.{RecordName}
|   +-- df_RecAttr.parquet
|   +-- df_RecIndex.parquet
+-- Record-<HumanFnName>.<OtherRecordFn>/
|   +-- df_RecAttr.parquet
|   +-- df_RecIndex.parquet
+-- Extra-{name}/                     # Optional extra DataFrames
+-- manifest.json
```

**Important:** It is NOT `<HumanFnName>/<EntityID>/<RecordFnName>/`. It is flat.

---

Load Pattern (Correct API)
===========================

```python
source .venv/bin/activate
source env.sh

python -c "
from haipipe.record_base import RecordSet

# Discover available RecordSets first
import os
print(os.listdir('_WorkSpace/2-RecStore/'))

# Load by path (example illustrative -- replace with actual RecordSet name)
record_set = RecordSet.load_from_disk(
    path='_WorkSpace/2-RecStore/<CohortName>_v<N>RecSet',
    SPACE=SPACE
)

# Alternative: load_asset (handles both local and remote paths)
record_set = RecordSet.load_asset(
    path='<CohortName>_v<N>RecSet',
    SPACE=SPACE
)

# Print summary info
record_set.info()
"
```

**Correct signature:** `RecordSet.load_from_disk(path=..., SPACE=...)`
**WRONG (does not exist):** `RecordSet.load_from_disk(set_name=..., store_key=...)`

---

Name_to_HRF Access Pattern
============================

The core data structure is `record_set.Name_to_HRF`, a flat dictionary
with string keys (Humans) and tuple keys (Records):

```python
# List all available keys first -- names depend on what was registered
for key in record_set.Name_to_HRF:
    if isinstance(key, str):
        print(f'Human: {key}')
    elif isinstance(key, tuple):
        print(f'Record: {key[0]}.{key[1]}')

# Access Human by string key (example illustrative)
human = record_set.Name_to_HRF['<HumanFnName>']
# Human has: human.df_Human (DataFrame with entity demographics)

# Access Record by tuple key (example illustrative)
my_record = record_set.Name_to_HRF[('<HumanFnName>', '<RecordFnName>')]
# Record has: my_record.df_RecAttr (DataFrame with record attributes)
#             my_record.df_RecIndex (DataFrame with record index)
```

**WRONG (these do NOT exist):**
- `record_set.items()` -- use `record_set.Name_to_HRF` directly
- `human.records` -- no such attribute
- `record.data` -- use `record.df_RecAttr` instead

---

Schema Inspection
=================

```python
# Replace argument values with actual HumanFn/RecordFn names from ls
human_cols = record_set.get_human_columns('<HumanFnName>')
print('Human columns:', human_cols)

record_cols = record_set.get_record_columns('<HumanFnName>', '<RecordFnName>')
print('Record columns:', record_cols)

# Full schema summary (no arguments needed)
print('Human_to_columns:', record_set.Human_to_columns)
print('Record_to_columns:', record_set.Record_to_columns)
```

---

Inspection Checklist
====================

1. **Patient count**: Check human.df_Human for number of patients
2. **Record types**: Verify expected Records exist as tuple keys in Name_to_HRF
3. **Temporal alignment**: Verify DT_s column has consistent intervals
   (5-min for CGM domain)
4. **attr_cols consistency**: Check attribute columns match the RecordFn definition
5. **Date ranges**: Verify temporal coverage per patient
6. **Data density**: Check CGM5Min record coverage (gaps indicate missing data)
7. **Manifest**: Check manifest.json for lineage back to SourceSet

---

Quick Inspection Commands (Bash)
=================================

```bash
# List available RecordSets
ls _WorkSpace/2-RecStore/

# List contents of a RecordSet (FLAT structure)
# Replace <RecordSetName> with actual name from ls above
ls _WorkSpace/2-RecStore/<RecordSetName>/
# Shows: Human-<HumanFnName>/  Record-<HumanFnName>.<RecordFnName>/  ...

# Check file sizes
du -sh _WorkSpace/2-RecStore/<RecordSetName>/

# Read manifest (shows lineage, build config, timestamps)
cat _WorkSpace/2-RecStore/<RecordSetName>/manifest.json
```

---

MUST DO
=======

- **Activate** .venv and **load** env.sh before any Python operations
- **Use** path-based loading: `RecordSet.load_from_disk(path=..., SPACE=SPACE)`
- **Access** data through `record_set.Name_to_HRF` with correct key types
- **Check** manifest.json for lineage and metadata

---

MUST NOT
========

- **NEVER modify** loaded data or any files in _WorkSpace/2-RecStore/
- **NEVER assume** data exists -- **check** first with ls or try/except
- **NEVER use** `load_from_disk(set_name=..., store_key=...)` -- does not exist
- **NEVER use** `record_set.items()`, `human.records`, or `record.data` -- do not exist
- **NEVER assume** hierarchical directory layout (it is FLAT)
