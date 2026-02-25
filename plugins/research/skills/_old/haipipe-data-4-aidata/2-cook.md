Subcommand: cook
================

Purpose: Run AIData_Pipeline with a YAML config (recipe).
Kitchen (AIData_Pipeline) + Chef (TfmFn/SplitFn) already exist.
You write the Recipe (config YAML).
This subcommand applies to any domain.

---

How AIData_Pipeline Works
=========================

```
AIData_Pipeline.__init__(config, SPACE, cache_combined_case=True)
    |
    +-- Loads SplitFn from SplitArgs.SplitMethod       (optional)
    +-- Loads Input TfmFn from InputArgs.input_method   (required)
    +-- Loads Output TfmFn from OutputArgs.output_method (optional)
    +-- Builds CF_to_CFVocab from CaseFn definition files
    +-- Builds feat_vocab via input TfmFn's build_vocab_fn
    |
AIData_Pipeline.run(...)
    |
    +-- Path 1: case_set_list / case_set / ds_case_combined -> AIDataSet
    +-- Path 2: df_case -> transformed DataFrame
    +-- Path 3: case_example -> transformed dict
```

---

Three Processing Paths (Correct API)
=====================================

```python
from haipipe.aidata_base.aidata_pipeline import AIData_Pipeline

pipeline = AIData_Pipeline(config, SPACE, cache_combined_case=True)

# ---------------------------------------------------------------
# Path 1: CaseSet(s) or cached dataset -> AIDataSet
# For training. Produces split HuggingFace DatasetDict.
# ---------------------------------------------------------------
aidata_set = pipeline.run(
    case_set_list=None,              # List of CaseSets
    case_set=None,                   # Single CaseSet
    ds_case_combined=None,           # Pre-combined HF Dataset (fastest)
    case_set_manifest_list=None,     # Required with ds_case_combined
    aidata_name='<aidata_name>',
    aidata_version='v0'
)

# ---------------------------------------------------------------
# Path 2: DataFrame -> transformed DataFrame
# For batch inference. No splitting, no saving.
# ---------------------------------------------------------------
df_transformed = pipeline.run(df_case=test_df, mode='inference')

# ---------------------------------------------------------------
# Path 3: Single case -> transformed dict
# For single-case inference. No splitting, no saving.
# ---------------------------------------------------------------
result = pipeline.run(case_example=single_case, mode='inference')
```

---

Config Structure
================

```yaml
# Replace <Placeholders> with actual values.
# To find registered SplitFns:  ls code/haifn/fn_aidata/split/
# To find registered Input Tfms: ls code/haifn/fn_aidata/entryinput/
# To find registered Output Tfms: ls code/haifn/fn_aidata/entryoutput/
# To find CaseFns in a CaseSet: ls _WorkSpace/3-CaseStore/<RecordSetName>/@*/

case_set_name: "<RecordSetName>/@v<N>CaseSet-<TriggerFolder>"

aidata_name: "<aidata_name>"
aidata_version: "v0"

SplitArgs:        # Optional: omit to skip splitting
  SplitMethod: <SplitFnName>           # discover: ls code/haifn/fn_aidata/split/
  ColumnName: <split_column>

InputArgs:        # Required
  input_method: <InputTfmFnName>       # discover: ls code/haifn/fn_aidata/entryinput/
  input_casefn_list:
    - <CaseFnName1>                     # must exist in the CaseSet
  input_args: { ... }

OutputArgs:       # Optional: omit for inference-only pipelines
  output_method: <OutputTfmFnName>     # discover: ls code/haifn/fn_aidata/entryoutput/
  output_casefn_list:
    - <CaseFnName2>
  output_args: { ... }
```

See `templates/config.yaml` for a fully annotated template.

---

How To Run
==========

**CLI command:**

```bash
source .venv/bin/activate
source env.sh
haistep-aidata --config <your_config>.yaml

# Find existing configs:
ls config/   # look for test-haistep-* or aidata/ subdirectories
```

**Test script:**

```bash
source .venv/bin/activate
source env.sh
python test/test_haistep/test_4_aidata/test_aidata.py \
    --config <your_config>.yaml
```

**Python API:**

```python
from haipipe.aidata_base.aidata_pipeline import AIData_Pipeline

pipeline = AIData_Pipeline(config, SPACE)
aidata_set = pipeline.run(
    case_set=case_set,
    aidata_name='<aidata_name>',
    aidata_version='v0'
)
```

---

Available Transforms
====================

**SplitFn (data splitters):**

```
SplitFn Name          Description                       Key Config Params
----------------------+----------------------------------+-----------------------
SplitByTimeBin        Temporal split by time bins        ColumnName, Split_to_Selection
RandomByPatient       Random split respecting patients   PatientID column, ratios
RandomByStratum       Stratified random split            stratum column, ratios
```

**Input TfmFn (feature transforms):**

```
TfmFn Name                 Description                     Domain
---------------------------+-------------------------------+-----------------------
InputTEToken               Token embedding (general)       Any time series
InputMultiCGMSeqNumeric    Multi-sequence numeric          Numeric sequences
InputMultiCGMSeqConcat     Multi-sequence concatenated     Numeric sequences
InputMultiCF               Multi case-feature tabular      Tabular features
InputCGMEventText          Time series + events as text    Text models
InputCGMEventJSON          Time series + events as JSON    JSON-based models
InputCGMWithEventChannels  Time series with event channels Multi-channel sequences
InputMultiSeqConcat        Multi sequences concatenated    Numeric sequences
InputTemporalInterleaving  Temporally interleaved          Interleaved sequences
CatInputMultiCFSparse      Sparse categorical features     Sparse tensors
```

**Output TfmFn (label transforms):**

```
TfmFn Name              Description                     Output Format
------------------------+-------------------------------+-----------------------
OutputNextToken         Next-token prediction labels     token ID sequence
OutputNumericForecast   Numeric forecasting labels       float array
OutputSingleLabel       Single classification label      int
```

---

SplitArgs Format
================

SplitFn adds a `split_ai` column to df_tag. It does NOT return a dict
of split DataFrames. The Split_to_Selection block then filters by that column.

```yaml
SplitArgs:
  SplitMethod: 'SplitByTimeBin'     # SplitFn name
  ColumnName: 'split_timebin'       # Column to split on

  Split_to_Selection:
    train:
      Rules: [["split_ai", "==", "train"]]
      Op: "and"
    validation:
      Rules: [["split_ai", "==", "validation"]]
      Op: "and"
    test-id:
      Rules: [["split_ai", "==", "test-id"]]
      Op: "and"
    test-od:
      Rules: [["split_ai", "==", "test-od"]]
      Op: "and"
```

Each Rule: `[column_name, operator, value]`
Operators: `==`, `!=`, `>`, `<`, `>=`, `<=`, `in`, `not in`
Op: `and` or `or` (combine multiple rules)

---

InputArgs Format
================

```yaml
InputArgs:
  input_method: "InputTEToken"       # TfmFn name
  input_casefn_list:                  # CaseFn fields to load
    - 'CGMValueBf24h'
    - 'CGMValueAf24h'
    - 'PDemoBase'
  input_args:                         # Transform-specific config
    window_build: { ... }             # Stage 1: Build TEWindow
    tetoken: { ... }                  # Stage 2: Convert to model format
```

**input_casefn_list** must reference CaseFn names present in the input CaseSet.

---

OutputArgs Format
=================

```yaml
OutputArgs:
  output_method: "OutputSingleLabel"       # TfmFn name
  output_casefn_list: []                   # Additional CaseFn fields (optional)
  output_args:                              # Transform-specific config
    label_column: "clicked"
    label_rule: ["clicked", ">", 0]
```

---

Naming Conventions
==================

**Output asset naming:** `<aidata_name>/@<aidata_version>`
  Pattern: `<aidata_name>/@<aidata_version>`

**Store path:** `_WorkSpace/4-AIDataStore/<aidata_name>/@<aidata_version>/`

---

Verification
============

After running, verify the output:

1. **Check** splits exist: train/, validation/, test-id/, test-od/
2. **Verify** sample counts per split
3. **Check** feature columns match expected transform output
4. **Verify** cf_to_cfvocab.json and feat_vocab.json at root (NOT vocab/)
5. **Check** manifest.json was created
6. **Load** and inspect (see load.md for pattern)

---

Prerequisites
=============

Before running AIData_Pipeline:

1. **Input CaseSet** must exist at the path specified in case_set_name
2. **All CaseFn names** in input_casefn_list must be present in the CaseSet
3. **If CaseSet does not exist**, run Case_Pipeline first (Layer 3)

---

MUST DO
=======

- **Activate** .venv and run `source env.sh` before running
- **Use** only registered SplitFn, InputTfm, and OutputTfm names
- **Ensure** case_set_name matches an existing CaseSet
- **Ensure** input_casefn_list references existing CaseFn columns
- **Provide** aidata_name and aidata_version for training paths

---

MUST NOT
========

- **NEVER invent** TfmFn/SplitFn names that do not exist in code/haifn/fn_aidata/
- **NEVER reference** CaseFn names not present in the CaseSet
- **NEVER create** files in code/haifn/ -- use design-chef if you need new transforms
- **NEVER assume** SplitArgs is required -- it is optional (omit to skip splitting)
- **NEVER assume** OutputArgs is required -- it is optional for inference pipelines
