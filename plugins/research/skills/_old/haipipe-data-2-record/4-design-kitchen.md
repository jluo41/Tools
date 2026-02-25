Subcommand: design-kitchen
==========================

Purpose: Upgrade Record_Pipeline infrastructure (code/haipipe/record_base/).
This is advanced -- most users do not need this.

Only use this when the pipeline framework itself needs changes, not when
you just need a new RecordFn (use design-chef for that).

---

What You Edit
=============

```
code/haipipe/record_base/
+-- record_pipeline.py    Pipeline orchestrator (run, cache, process)
+-- record_set.py         RecordSet asset class (save, load, I/O)
+-- builder/
    +-- human.py           HumanFn dynamic loader
    +-- record.py          RecordFn dynamic loader
```

These files are EDITABLE (not generated). Changes take effect immediately.

---

Three-Class Architecture
=========================

```
+--------------------------------------------------+
|  Record_Pipeline  (record_pipeline.py)            |
|  - __init__(config, SPACE): Pre-loads Fn loaders  |
|  - run(source_set, partition_index=None,          |
|        partition_number=None, record_set_label=1, |
|        use_cache=True, save_cache=True,           |
|        profile=False)                             |
|  - HumanFn + RecordFn orchestration               |
|  - Temporal alignment enforcement                 |
|  - Multiprocessing support (--n_cpus)             |
+-------------------+------------------------------+
                    | uses
+-------------------v------------------------------+
|  HumanFn loader   (builder/human.py)              |
|  - Dynamic import from code/haifn/fn_record/human/|
|  - Maps raw entity ID -> internal ID             |
|  - Defines entity roster (Excluded_RawNameList)   |
|                                                    |
|  RecordFn loader  (builder/record.py)             |
|  - Dynamic import from code/haifn/fn_record/record|
|  - Processes each time-series table from SourceSet|
+-------------------+------------------------------+
                    | produces
+-------------------v------------------------------+
|  RecordSet  (record_set.py)                       |
|  - Inherits from Asset base class                 |
|  - Name_to_HRF: mixed string/tuple key dict      |
|    {  # Example (illustrative)                    |
|      '<HumanFnName>': <Human>,                    |
|      ('<HumanFnName>', '<RecordFn1>'): <Record>,  |
|      ('<HumanFnName>', '<RecordFn2>'): <Record>,  |
|    }                                              |
|  - FLAT directory: Human-X/, Record-X.Y/          |
|  - save_to_disk() / load_from_disk(path, SPACE)   |
+--------------------------------------------------+
```

**Three-class pattern:** Pipeline + Fn Loaders (Human + Record) + Asset Set

---

Key Implementation Details
===========================

**Record_Pipeline.__init__(config, SPACE):**
- Reads `config['HumanRecords']` and `config.get('record_set_version', 0)`
- Pre-loads HumanFn and RecordFn into `self.reusable_Name_to_Fn`
  with keys like `'H:<HumanFnName>'` and `'R:<RecordFnName>'`

**Record_Pipeline.run(source_set, ...):**
- Auto-generates record_set_name via `_generate_record_set_name()`
  (strips @SourceFnName, appends _v{N}RecSet)
- Calls `_process_human_and_records()` which iterates HumanRecords,
  creates Human objects, then creates Record objects for each human
- Returns a RecordSet instance

**RecordSet.__init__(record_set_name, source_set_manifest, Name_to_HRF, SPACE, ...):**
- Pure container -- no processing logic
- Auto-computes `Human_to_columns` and `Record_to_columns` from Name_to_HRF
- Builds `Base_HumanToRecIndex` for downstream CaseFn access

**RecordSet._save_data_to_disk(path):**
- Saves Human objects to `Human-{HumanName}/` subdirectories
- Saves Record objects to `Record-{HumanName}.{RecordName}/` subdirectories
- Saves extra DataFrames to `Extra-{name}/` subdirectories
- FLAT structure, NOT hierarchical by patient

**RecordSet._load_data_from_disk(path, manifest):**
- Reads directory listing to discover `Human-*` and `Record-*` folders
- Reconstructs Name_to_HRF with string keys (Human) and tuple keys (Record)

---

When To Use This
================

- **Adding** new time alignment strategies (beyond 5-minute)
- **Modifying** the Human/Record object structure
- **Adding** new multiprocessing strategies
- **Changing** the RecordSet serialization format
- **Adding** new HumanFn/RecordFn loader features
- **Modifying** partition-based processing logic
- **Extending** the Asset I/O contract (e.g., new storage backends)

---

MUST DO
=======

- **Present** plan to user -> **get** approval
- **Maintain** backward compatibility with existing HumanFn/RecordFn files
- **Test** thoroughly with existing cohorts
- **Keep** the Asset I/O contract: `save_to_disk()` / `load_from_disk(path, SPACE)`
- **Preserve** the FLAT directory naming: `Human-{X}/`, `Record-{X}.{Y}/`
- **Preserve** the Name_to_HRF key convention: string for Human, tuple for Record
- **Activate** .venv and **load** env.sh before any Python operations

---

MUST NOT
========

- **NEVER break** the Asset I/O contract (save/load must remain compatible)
- **NEVER change** stage-to-stage interface without updating Source and Case layers
- **NEVER modify** code/haifn/ (that is generated code)
- **NEVER break** temporal alignment (downstream CaseFn depend on it)
- **NEVER change** Human/Record interface without updating all RecordFn builders
- **NEVER change** the Name_to_HRF key convention (string/tuple)
- **NEVER introduce** fabricated APIs (e.g., `record_set.items()`, `human.records`)
