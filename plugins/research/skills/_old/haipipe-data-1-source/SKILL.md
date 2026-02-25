Skill: haipipe-data-1-source
============================

Layer 1 of the 6-layer data pipeline: Source Processing.

Converts raw data files (CSV, XML, Parquet, JSON) into a standardized
SourceSet -- a dictionary of DataFrames keyed by table name.

**Scope of this skill:** Framework patterns only. It does not catalog
project-specific state (which SourceFns are registered, column names, cohort
names). That state is always discovered at runtime from the filesystem.
This skill applies equally to any domain: CGM, EHR, genomics, wearables, etc.

Four subcommands:

  /haipipe-data-1-source load           Inspect existing SourceSet
  /haipipe-data-1-source cook           Run Source_Pipeline with config
  /haipipe-data-1-source design-chef    Create new SourceFn via builder
  /haipipe-data-1-source design-kitchen Upgrade Source_Pipeline infra

On invocation, read this file for shared rules, then read the matching
subcommand file (1-load.md, 2-cook.md, 3-design-chef.md, 4-design-kitchen.md).

---

Architecture Position
=====================

```
Layer 6: Endpoint         Deployment package for inference
    |
Layer 5: ModelInstance    Trained model artifact
    |
Layer 4: AIData           ML-ready datasets (train/val/test splits)
    |
Layer 3: Case             Event-triggered feature extraction
    |
Layer 2: Record           Temporally-aligned patient records
    |
Layer 1: Source  <---     Raw files -> standardized tables
```

---

Cooking Metaphor
================

```
Concept    Pipeline Term              Location
---------  -------------------------  ------------------------------------------
Kitchen    Source_Pipeline class       code/haipipe/source_base/
Chef       SourceFn functions         code/haifn/fn_source/           (GENERATED)
Recipe     YAML config file           config/ or tutorials/config/
Dish       SourceSet asset            _WorkSpace/1-SourceStore/
Academy    Builder scripts            code-dev/1-PIPELINE/1-Source-WorkSpace/
```

The Kitchen (Source_Pipeline) orchestrates execution. The Chef (SourceFn) does
the actual data transformation. The Recipe (YAML config) tells the Kitchen
which Chef to use and where to find raw data. The Dish (SourceSet) is the
output. The Academy (builder scripts) is where you train new Chefs.

---

What Is a SourceSet?
====================

A SourceSet is an Asset that holds **ProcName_to_ProcDf** -- a dictionary
mapping table names to pandas DataFrames.

```python
# Example (illustrative -- actual ProcNames depend on domain and dataset):
source_set.ProcName_to_ProcDf = {
    '<TableName1>': DataFrame(columns=['<EntityID>', '<DatetimeCol>', '<ValueCol>', ...]),
    '<TableName2>': DataFrame(columns=['<EntityID>', '<DateCol>', '<DoseCol>', ...]),
    ...
}
```

Each key is a **ProcName** (processed table name). Which ProcNames exist
depends on the domain and dataset. Typical patterns:

```
Domain            Typical ProcNames
----------------  --------------------------------------------------
Diabetes / CGM    CGM, Medication, Diet, Exercise, Ptt, Height, Weight
EHR               Encounters, Labs, Vitals, Diagnoses, Procedures
Genomics          Variants, Samples, Annotations
Wearables         HeartRate, Steps, Sleep, SpO2
```

The SourceFn defines the full list in its **ProcName_List** attribute.

Always discover what ProcNames are available:
```bash
ls code/haifn/fn_source/                       # registered SourceFns
head -20 code/haifn/fn_source/<SourceFnName>.py  # see its ProcName_List
```

---

Schema Consistency
==================

Within a domain, all SourceFns MUST produce identical column sets for shared
table types. This is what makes Layer 2 (Record) work -- it expects the same
columns regardless of which dataset produced them.

**Example: CGM/Diabetes domain standard schemas (illustrative)**

These are real schemas used in the CGM domain. Other domains will define their
own schemas following the same Core + Extended Fields Pattern.

Medication (11 columns):

```python
['PatientID', 'MedAdministrationID',
 'AdministrationDate', 'EntryDateTime', 'UserAdministrationDate',
 'AdministrationTimeZoneOffset', 'AdministrationTimeZone',
 'MedicationID', 'Dose',
 'medication', 'external_metadata']
```

Exercise (13 columns):

```python
['PatientID', 'ExerciseEntryID',
 'ObservationDateTime', 'ObservationEntryDateTime',
 'TimezoneOffset', 'Timezone',
 'ExerciseType', 'ExerciseIntensity',
 'ExerciseDuration', 'CaloriesBurned', 'DistanceInMeters',
 'exercise', 'external_metadata']
```

Diet (15 columns):

```python
['PatientID', 'CarbsEntryID',
 'ObservationDateTime', 'ObservationEntryDateTime',
 'TimezoneOffset', 'Timezone',
 'FoodName', 'ActivityType',
 'Carbs', 'Calories', 'Protein', 'Fat', 'Fiber',
 'nutrition', 'external_metadata']
```

**Core + Extended Fields Pattern (domain-general):**

- Core fields: Kept as columns AND in JSON (e.g., Dose, Carbs, ExerciseDuration)
- Extended fields: Only in JSON (e.g., MedicationType, bwz_carb_input, HeartRate)
- Dataset-specific metadata: Only in the `external_metadata` JSON column

---

Concrete Code From the Repo
============================

**Loading an existing SourceSet:**

```python
from haipipe.source_base import SourceSet

# Load by full path (replace with actual path from ls _WorkSpace/1-SourceStore/)
source_set = SourceSet.load_from_disk(
    path='_WorkSpace/1-SourceStore/<CohortName>/@<SourceFnName>',
    SPACE=SPACE
)

# Equivalent approach
source_set = SourceSet.load_asset(
    path='_WorkSpace/1-SourceStore/<CohortName>/@<SourceFnName>',
    SPACE=SPACE
)

# Inspect
for name, df in source_set.ProcName_to_ProcDf.items():
    print(f'{name}: {df.shape[0]} rows, {df.shape[1]} cols')
```

**Running the pipeline:**

```python
from haipipe.source_base import Source_Pipeline

pipeline = Source_Pipeline(config, SPACE)
source_set = pipeline.run(
    raw_data_name='<CohortName>',              # Folder name in SourceStore
    raw_data_path=None,                         # None=check store, or S3 URL, or abs path
    payload_input=None,                         # Dict for inference mode (no caching)
    use_cache=True,                             # Load cached if available
    save_cache=True                             # Save results to cache
)
```

**Saving:**

```python
source_set.save_to_disk()                       # Auto path from SPACE
source_set.save_to_disk(path='/custom/path')    # Custom path
```

**SourceFn module structure** (code/haifn/fn_source/<SourceFnName>.py):

```python
# Module-level attributes (required):
SourceFile_SuffixList = ['.xml']  # or ['.csv'], ['.parquet'], etc.
ProcName_List = ['<Table1>', '<Table2>', '<Table3>']   # all output tables
ProcName_to_columns = {
    '<Table1>': ['<EntityID>', '<DatetimeCol>', '<ValueCol>', ...],
    '<Table2>': ['<EntityID>', '<DateCol>', ...],
}

# Main function (required):
def process_Source_to_Processed(SourceFile_List, get_ProcName_from_SourceFile, SPACE=None):
    ProcName_to_ProcDf = {}
    # ... processing logic ...
    return ProcName_to_ProcDf
```

---

SourceSet On-Disk Layout
========================

```
_WorkSpace/1-SourceStore/{raw_data_name}/@{SourceFnName}/
    {ProcName1}.parquet
    {ProcName2}.parquet
    ...
    manifest.json
```

Example (illustrative -- actual ProcNames depend on domain and SourceFn):

```
_WorkSpace/1-SourceStore/<CohortName>/@<SourceFnName>/
    <Table1>.parquet
    <Table2>.parquet
    <Table3>.parquet
    manifest.json
```

To see what exists for a real SourceSet:
```bash
ls _WorkSpace/1-SourceStore/          # available cohorts
ls _WorkSpace/1-SourceStore/<CohortName>/@<SourceFnName>/  # its tables
```

---

Discovering Available Fns
==========================

Do not rely on a hardcoded list -- always discover at runtime:

```bash
# Registered SourceFns
ls code/haifn/fn_source/

# Corresponding builder scripts
ls code-dev/1-PIPELINE/1-Source-WorkSpace/

# Inspect a SourceFn's ProcName_List
head -20 code/haifn/fn_source/<SourceFnName>.py
```

---

Prerequisites (Before MUST DO)
==============================

```bash
# 1. Activate the virtual environment
source .venv/bin/activate

# 2. Load workspace paths
source env.sh

# 3. Verify installation
python -c "import haipipe, haifn; print('OK')"
```

---

MUST DO (All Subcommands)
=========================

1. **Activate .venv first**: `source .venv/bin/activate`
2. **Load environment**: `source env.sh`
3. **Respect the golden rule**: output of Layer 1 = input of Layer 2 (Record)
4. **Maintain schema consistency** per domain -- all SourceFns for a domain
   must produce identical column sets for shared table types
5. **Keep core fields as columns AND in JSON** metadata columns
6. **Store extended fields ONLY in JSON** metadata columns
7. **Present plan to user and get approval** before any code changes

---

MUST NOT (All Subcommands)
==========================

1. **NEVER edit** code/haifn/ directly -- 100% generated from builders
2. **NEVER run** Python without .venv activated
3. **NEVER skip** `source env.sh` -- store paths come from environment variables
4. **NEVER break** cross-dataset schema consistency within a domain
5. **NEVER invent** column names outside the domain's standard schema
6. **NEVER skip** RUN_TEST = True in builders

---

Key File Locations
==================

```
Pipeline framework:   code/haipipe/source_base/source_pipeline.py
                      code/haipipe/source_base/source_set.py
                      code/haipipe/source_base/source_utils.py
Fn loader:            code/haipipe/source_base/builder/sourcefn.py

Generated SourceFns:  code/haifn/fn_source/          <- discover with ls
Builders (edit here): code-dev/1-PIPELINE/1-Source-WorkSpace/  <- discover with ls

Test configs:         config/                         <- discover with ls config/
Store path:           _WorkSpace/1-SourceStore/
```

---

File Layout
===========

```
haipipe-data-1-source/
    SKILL.md              This file (router + shared rules)
    README.md             Quick reference
    1-load.md             /haipipe-data-1-source load
    2-cook.md             /haipipe-data-1-source cook
    3-design-chef.md      /haipipe-data-1-source design-chef
    4-design-kitchen.md   /haipipe-data-1-source design-kitchen
    templates/
        config.yaml       Config template for cook subcommand
```

---

See Also
========

- **haipipe-data-0-overview**: Architecture map and decision guide
- **haipipe-data-2-record**: How SourceSets become RecordSets (Layer 2)
- **haipipe-data-3-case**: How RecordSets become CaseSets (Layer 3)
- **haipipe-data-4-aidata**: How CaseSets become ML-ready datasets (Layer 4)
