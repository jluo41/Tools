Subcommand: design-kitchen
==========================

Purpose: Upgrade Case_Pipeline infrastructure (code/haipipe/case_base/).
This is advanced -- most users do not need this.

Only use this when the pipeline framework itself needs changes, not when
you just need a new CaseFn (use design-chef for that).

---

What You Edit
=============

```
code/haipipe/case_base/
+-- case_pipeline.py      Pipeline orchestrator (run, trigger, extract)
+-- case_set.py           CaseSet asset class (save, load, I/O)
+-- case_utils.py         Utility functions
+-- builder/
    +-- triggerfn.py       TriggerFn dynamic loader
    +-- casefn.py          CaseFn dynamic loader
    +-- rotools.py         Record Object tools (data access helpers)
```

These files are **EDITABLE** (not generated). Changes take effect immediately.

---

Three-Class Architecture
========================

The Case layer follows the same three-class pattern as other pipeline layers:

```
+--------------------------------------------------+
|  Case_Pipeline  (case_pipeline.py)                |
|  - __init__(config, SPACE, context=None)          |
|  - run(df_case, df_case_raw, record_set,          |
|        use_cache, profile): Full batch processing  |
|  - CaseProgressPipeline: Single-case inference    |
|  - FeatureContext: Global external data cache      |
|  - Multiprocessing support (--n_cpus)             |
+------------------+-------------------------------+
                   | uses
+------------------v-------------------------------+
|  Fn Loaders                                       |
|                                                    |
|  TriggerFn loader  (builder/triggerfn.py)         |
|  - Dynamic import from code/haifn/fn_case/fn_trigger
|  - Calls get_CaseTrigger_from_RecordBase()        |
|  - Returns: {df_case, df_lts, df_Human_Info}      |
|                                                    |
|  CaseFn loader     (builder/casefn.py)            |
|  - Dynamic import from code/haifn/fn_case/case_casefn
|  - Calls fn_CaseFn() with 6 positional params    |
|  - Prefixes return keys with CaseFnName           |
|                                                    |
|  ROTools           (builder/rotools.py)            |
|  - Record Object data access helpers              |
|  - Temporal windowing (Bf24h, Af24h, etc.)        |
|  - 3-part ROName parsing (h/r/c)                  |
+------------------+-------------------------------+
                   | produces
+------------------v-------------------------------+
|  CaseSet  (case_set.py)                           |
|  - Inherits from Asset base class                 |
|  - df_case.parquet + @CaseFn.parquet at ROOT      |
|  - load_from_disk(path, SPACE, CaseFn_list)       |
|  - save_to_disk / push_to_remote                  |
|  - cf_to_cfvocab.json for vocabulary tracking     |
+--------------------------------------------------+
```

**Three-class pattern:** Pipeline + Fn Loaders (Trigger + CaseFn + ROTools) + Asset Set

---

Pipeline Flow Detail
====================

```
Case_Pipeline.run()
    |
    +-- 1. Load TriggerFn module (dynamic import)
    |   +-- Call get_CaseTrigger_from_RecordBase(record_set, Trigger_Args)
    |   +-- Returns: {df_case, df_lts, df_Human_Info}
    |
    +-- 2. Apply Filters (optional)
    |   +-- Remove cases by condition
    |
    +-- 3. For each CaseFn in CaseFn_list:
    |   +-- Load CaseFn module (dynamic import)
    |   +-- For each case row in df_case:
    |   |   +-- Extract ROData via ROTools (temporal windowing)
    |   |   +-- Call fn_CaseFn(case, ROName_list, ROName_to_ROData,
    |   |   |                  ROName_to_ROInfo, COVocab, context)
    |   |   +-- Prefix return keys: f"{cf_name}{feat_name}"
    |   +-- Save @{CaseFnName}.parquet at ROOT
    |
    +-- 4. Save CaseSet to disk
        +-- df_case.parquet
        +-- @CaseFn.parquet files at ROOT
        +-- cf_to_cfvocab.json
        +-- manifest.json
```

---

When To Use This
================

- **Adding** new Record Object windowing strategies (rotools.py)
- **Modifying** the trigger -> case extraction flow (case_pipeline.py)
- **Adding** new CaseProgressPipeline modes for inference
- **Changing** the FeatureContext caching strategy
- **Modifying** the CaseSet serialization format (case_set.py)
- **Adding** new multiprocessing strategies
- **Fixing** bugs in the pipeline orchestration

---

MUST DO
=======

- **Present** plan to user -> **get** approval
- **Maintain** backward compatibility with existing TriggerFn/CaseFn modules
- **Test** thoroughly with existing triggers and case functions
- **Keep** the Asset I/O contract: load_from_disk(path, SPACE, CaseFn_list)
- **Keep** CaseSet naming: `@v{N}CaseSet-{TriggerFolder}`
- **Preserve** ROName_to_ROData interface for all CaseFns
- **Preserve** 6-parameter fn_CaseFn signature
- **Preserve** suffix-only return key convention (pipeline adds prefix)
- **Preserve** get_CaseTrigger_from_RecordBase as trigger function name

---

MUST NOT
========

- **NEVER break** the Asset I/O contract (save/load must remain compatible)
- **NEVER change** stage-to-stage interface without updating Record and AIData layers
- **NEVER modify** code/haifn/ (that is generated code -- edit builders instead)
- **NEVER break** the ROName_to_ROData access pattern (all CaseFns depend on it)
- **NEVER change** Trigger -> CaseFn interface without updating all builders
- **NEVER change** df_case.parquet to a different filename
- **NEVER move** @CaseFn.parquet files into a subdirectory
