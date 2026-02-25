Subcommand: design-kitchen
==========================

Purpose: Upgrade Source_Pipeline infrastructure (code/haipipe/source_base/).
This is advanced -- most users do not need this.

Only use this when the pipeline framework itself needs changes, not when
you just need a new SourceFn (use design-chef for that).

---

What You Edit
=============

```
code/haipipe/source_base/
    source_pipeline.py    Pipeline orchestrator (run, cache, validate)
    source_set.py         SourceSet asset class (save, load, I/O)
    source_utils.py       Utility functions
    builder/
        sourcefn.py       SourceFn dynamic loader
```

These files are EDITABLE (not generated). Changes take effect immediately.

---

Architecture
============

```
Three-class pattern: Pipeline + Fn Loader + Asset Set

┌──────────────────────────────────────────────────┐
│  Source_Pipeline  (source_pipeline.py)            │
│  - __init__(config, SPACE)                        │
│  - run(raw_data_name, raw_data_path,              │
│        payload_input, use_cache, save_cache)       │
│  - Cache management: check / save / skip          │
│  - Schema validation: ProcName_to_columns check   │
│  - Remote fetch: S3 / GCS / Databricks support    │
└──────────────────┬───────────────────────────────┘
                   │ uses
┌──────────────────v───────────────────────────────┐
│  SourceFn loader  (builder/sourcefn.py)           │
│  - Dynamic import from code/haifn/fn_source/      │
│  - Loads: SourceFile_SuffixList, ProcName_List,   │
│    ProcName_to_columns, process_Source_to_Processed│
└──────────────────┬───────────────────────────────┘
                   │ produces
┌──────────────────v───────────────────────────────┐
│  SourceSet  (source_set.py)                       │
│  - Inherits from Asset base class                 │
│  - ProcName_to_ProcDf: Dict[str, DataFrame]      │
│  - save_to_disk() / load_from_disk(path, SPACE)  │
│  - load_asset(path, SPACE)                        │
│  - manifest.json tracking                         │
└──────────────────────────────────────────────────┘
```

---

When To Use This
================

- Adding new caching strategies to Source_Pipeline
- Modifying schema validation logic
- Adding new remote storage backends
- Changing the SourceSet serialization format
- Modifying the SourceFn dynamic loader
- Adding new pipeline execution modes (e.g., streaming)

---

Key API Contracts To Preserve
=============================

**Source_Pipeline.run() signature:**

```python
def run(self, raw_data_name, raw_data_path=None, payload_input=None,
        use_cache=True, save_cache=True) -> SourceSet:
```

**SourceSet I/O:**

```python
# Save
source_set.save_to_disk()                        # Auto path
source_set.save_to_disk(path='/custom/path')      # Custom path

# Load
SourceSet.load_from_disk(path='...', SPACE=SPACE)
SourceSet.load_asset(path='...', SPACE=SPACE)
```

**SourceFn loader expectations:**

The loader (builder/sourcefn.py) imports a module and reads these attributes:
- SourceFile_SuffixList
- ProcName_List
- ProcName_to_columns
- get_ProcName_from_SourceFile (function)
- process_Source_to_Processed (function)
- MetaDict (dict, may contain 'get_inference_entry')

**Asset naming convention:**

`{raw_data_name}/@{SourceFnName}` -- both Source_Pipeline and SourceSet
depend on this pattern.

---

MUST DO
=======

1. **Present plan** to user -> get approval before editing
2. **Maintain backward compatibility** with existing SourceFn files
3. **Test thoroughly** with existing cohorts (OhioT1DM, WellDoc, etc.)
4. **Keep the Asset I/O contract**: save_to_disk() / load_from_disk(path, SPACE)
5. **Keep the naming convention**: `{raw_data_name}/@{SourceFnName}`
6. **Preserve the run() signature** -- all five parameters

---

MUST NOT
========

1. **NEVER break** the Asset I/O contract (save/load must remain compatible)
2. **NEVER change** the stage-to-stage interface without updating the Record layer
3. **NEVER modify** code/haifn/ (that is generated code)
4. **NEVER change** ProcName_to_ProcDf schema without updating all SourceFns
5. **NEVER remove** cache support (many workflows depend on it)
6. **NEVER alter** the SourceFn loader contract without updating all builders
