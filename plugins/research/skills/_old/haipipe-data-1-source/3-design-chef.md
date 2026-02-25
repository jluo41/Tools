Subcommand: design-chef
=======================

Purpose: Create a new SourceFn via the builder pattern.
Edit builders in code-dev/ -> run -> generates code/haifn/fn_source/.

This skill documents FRAMEWORK PATTERNS only -- not project-specific state.
It applies to any domain: CGM, EHR, genomics, wearable data, or any tabular source.

---

Workflow
========

0. **Inspect existing builders** to understand what format they handle:
   ```bash
   ls code-dev/1-PIPELINE/1-Source-WorkSpace/    # existing builders
   ls code/haifn/fn_source/                       # already generated SourceFns
   head -30 code-dev/1-PIPELINE/1-Source-WorkSpace/<closest_builder>.py
   ```
1. **Present plan** to user -> get approval
2. **Activate environment**: `source .venv/bin/activate && source env.sh`
3. **Copy an existing builder** as starting point (pick the one closest to your format)
4. **Edit [CUSTOMIZE] sections** only (keep [BOILERPLATE] as-is)
5. **Run builder** to generate production code:
   ```bash
   python code-dev/1-PIPELINE/1-Source-WorkSpace/<your_builder>.py
   ```
6. **Verify** generated file in code/haifn/fn_source/
7. **Register** in config YAML (SourceFnName)
8. **Test** end-to-end with Source_Pipeline

---

Builder Location
================

```
code-dev/1-PIPELINE/1-Source-WorkSpace/
    c<N>_build_source_<SourceFnName>.py    (one per SourceFn -- discover with ls)
    old/                                    (Legacy builders)
```

Discover existing builders:
```bash
ls code-dev/1-PIPELINE/1-Source-WorkSpace/
```

**Best starting point** -- pick the builder closest to your data format:

```bash
ls code-dev/1-PIPELINE/1-Source-WorkSpace/    # see all available builders
head -20 code-dev/1-PIPELINE/1-Source-WorkSpace/<builder>.py  # check its format
```

Match your format to the builder that handles the same file type (CSV, XML, Parquet, etc.).

---

Builder Naming Convention
=========================

**Builder file:** `c<N>_build_source_<dataset><version>.py`

  Example: `c6_build_source_MyDataset250301.py`

**Generated output:** `code/haifn/fn_source/<SourceFnName>.py`

  Example: `code/haifn/fn_source/MyDatasetV250301.py`

**SourceFnName** must be unique and descriptive: `<Dataset><Format?><Date>`

---

Builder Template Structure
===========================

Every builder follows this layout with [BOILERPLATE] and [CUSTOMIZE] sections:

```python
# ==========================================================
# [BOILERPLATE] Configuration
# ==========================================================
OUTPUT_DIR = 'fn_source'
SOURCE_FN_NAME = 'MyDatasetV250301'     # [CUSTOMIZE] Unique name
TEST_SOURCE_NAME = 'MyDataset'          # [CUSTOMIZE] Cohort name
RUN_TEST = True                          # Always True

# ==========================================================
# [CUSTOMIZE] Schema Definition
# ==========================================================
SourceFile_SuffixList = ['.csv']         # File extensions to process
ProcName_List = ['CGM', 'Medication', 'Diet', 'Exercise']  # Output tables

# ==========================================================
# [CUSTOMIZE] Processing Functions (one per table)
# ==========================================================
def process_Medication(df_raw, SPACE):
    """Transform raw medication data to standard schema."""
    # MUST output exactly 11 columns for diabetes domain
    ...

def process_Diet(df_raw, SPACE):
    """Transform raw diet data to standard schema."""
    # MUST output exactly 15 columns for diabetes domain
    ...

def process_Exercise(df_raw, SPACE):
    """Transform raw exercise data to standard schema."""
    # MUST output exactly 13 columns for diabetes domain
    ...

# ==========================================================
# [CUSTOMIZE] Main ETL Orchestrator
# ==========================================================
def process_Source_to_Processed(SourceFile_List, get_ProcName_from_SourceFile, SPACE=None):
    """Main ETL: raw files -> standardized DataFrames."""
    ProcName_to_ProcDf = {}
    for filepath in SourceFile_List:
        proc_name = get_ProcName_from_SourceFile(filepath)
        df_raw = load_file(filepath)
        ProcName_to_ProcDf[proc_name] = process_fn(df_raw, SPACE)
    return ProcName_to_ProcDf

# ==========================================================
# [BOILERPLATE] Code Generation + Test
# ==========================================================
# Base.convert_variables_to_pystring() -> generates .py file
# Test: loads raw data, runs SourceFn, validates schema
```

---

Required Module Attributes
===========================

The generated .py file in code/haifn/fn_source/ must define all of these:

```
Attribute                       Type                  Purpose
------------------------------  --------------------  --------------------------------
SourceFile_SuffixList           list[str]             File extensions (e.g., ['.xml'])
ProcName_List                   list[str]             Output table names
ProcName_to_columns             dict[str, list[str]]  Column schema per table
get_ProcName_from_SourceFile    function              Maps filepath -> table name
process_Source_to_Processed     function              Main ETL function
MetaDict                        dict                  Metadata (can be empty: {})
```

The **process_Source_to_Processed** function signature:

```python
def process_Source_to_Processed(SourceFile_List, get_ProcName_from_SourceFile, SPACE=None):
    """
    Args:
        SourceFile_List: List of file paths (batch) or payload dict (inference)
        get_ProcName_from_SourceFile: Function mapping filepath -> ProcName
        SPACE: Workspace configuration dict

    Returns:
        ProcName_to_ProcDf: Dict[str, pd.DataFrame]
    """
```

---

Schema Consistency Rules
========================

Within a domain, all SourceFns MUST output identical column sets for shared
table types. This ensures Layer 2 (Record) can process any dataset uniformly.

**Diabetes domain example:**

- Medication: 11 columns (see SKILL.md for full list)
- Exercise: 13 columns
- Diet: 15 columns

**Core + Extended Fields Pattern:**

- Core fields: Kept as BOTH columns AND in JSON (e.g., Dose, Carbs)
- Extended fields: ONLY in JSON (e.g., MedicationType, bwz_carb_input)
- Dataset-specific metadata: ONLY in `external_metadata` JSON column

**For a new domain** (e.g., EHR, genomics): Define your own schema standards,
then enforce them consistently across all SourceFns in that domain.

---

Auto-Schema Derivation
======================

The builder runs a test pass and derives `ProcName_to_columns` from actual
output. This means you do not need to manually list columns -- the builder
captures them automatically during the RUN_TEST phase.

---

MUST DO
=======

1. **Present plan** to user and get approval before starting
2. **Activate environment**: `source .venv/bin/activate && source env.sh`
3. **Follow the [BOILERPLATE] + [CUSTOMIZE] pattern** -- do not rewrite boilerplate
4. **Set RUN_TEST = True** -- the builder must test on generation
5. **Maintain schema consistency** within the domain (matching column counts)
6. **Include MetaDict** (even if empty: `MetaDict = {}`)
7. **Put core fields as columns AND in JSON** metadata
8. **Put extended fields ONLY in JSON** metadata columns
9. **Test end-to-end** with Source_Pipeline after generation

---

MUST NOT
========

1. **NEVER edit** code/haifn/fn_source/ directly -- always go through the builder
2. **NEVER skip** the builder -> generate -> test cycle
3. **NEVER break** schema consistency across datasets in the same domain
4. **NEVER skip** RUN_TEST (set it to True always)
5. **NEVER add** columns outside the domain's standard schema for shared tables
6. **NEVER skip** `source env.sh` -- the builder needs SPACE paths
