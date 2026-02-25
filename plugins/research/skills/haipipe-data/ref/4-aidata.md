Layer 4: AIData
===============

Layer 4 of the 6-stage data pipeline: AIData (ML-Ready Dataset).

Takes a CaseSet (flat Parquet of extracted features) and transforms it
into an AIDataSet -- a HuggingFace DatasetDict with vocabularies, split
labels, and transform metadata that Layer 5 (Model) can train on directly.

---

Architecture Position
=====================

```
Layer 6: Endpoint         Deployment packaging.
    |
Layer 5: Model            Trains on AIDataSet from Layer 4.
    |
Layer 4: AIData      <--- Transforms CaseSet -> ML-ready DatasetDict.
    |                     Builds vocab, applies tfm_fn, splits rows.
Layer 3: Case             Extracts features at trigger points.
    |
Layer 2: Record           Processes raw data into patient records.
    |
Layer 1: Source           Loads raw data files.
```

---

Cooking Metaphor
================

```
Kitchen  = AIData_Pipeline class        (code/haipipe/aidata_base/)
Chef     = TfmFn + SplitFn             (code/haifn/fn_aidata/)  GENERATED
Recipe   = YAML config file            (config/aidata/ or tutorials/config/)
Dish     = AIDataSet asset             (_WorkSpace/4-AIDataStore/)
Academy  = Builder scripts             (code-dev/1-PIPELINE/4-AIData-WorkSpace/)
```

---

What Is an AIDataSet
====================

Output of Layer 4. Wraps a HuggingFace DatasetDict with vocab files.

**Core attributes:**

```python
aidata_set.dataset_dict    # DatasetDict with splits: 'train', 'validation',
                           #   'test-id', 'test-od'
aidata_set.CF_to_CFVocab   # Per-CaseFn vocabulary (saved as cf_to_cfvocab.json)
aidata_set.feat_vocab       # Feature vocabulary from build_vocab_fn
                           #   (saved as feat_vocab.json)
aidata_set.meta_info        # MetaArgs configuration
aidata_set.split_info       # Split configuration
aidata_set.transform_info   # Transform configuration
```

**On-disk layout:**

```
_WorkSpace/4-AIDataStore/{aidata_name}/@{aidata_version}/
+-- train/                    (HuggingFace Dataset, Parquet format)
+-- validation/
+-- test-id/
+-- test-od/                  (optional)
+-- cf_to_cfvocab.json        (Per-CaseFn vocabulary -- at ROOT)
+-- feat_vocab.json            (Feature vocabulary -- at ROOT)
+-- manifest.json
```

**CRITICAL:** Vocab files (`cf_to_cfvocab.json` and `feat_vocab.json`)
live at the ROOT of the version directory. There is NO `vocab/` subdirectory.

---

Three-Part Config Pattern
=========================

Every AIData YAML config has up to three sections:

**1. SplitArgs (optional) -- how to split cases into train/val/test:**

```yaml
SplitArgs:
  SplitMethod: '<SplitFnName>'          # ls code/haifn/fn_aidata/split/
  ColumnName: 'patient_id'
  Split_to_Selection:
    train:
      Rules: [['split_col', '==', 'train']]
      Op: 'AND'
    validation:
      Rules: [['split_col', '==', 'val']]
      Op: 'AND'
```

**2. InputArgs -- how to transform features into model inputs:**

```yaml
InputArgs:
  input_method: '<InputTfmFnName>'      # ls code/haifn/fn_aidata/entryinput/
  input_casefn_list:                    # CaseFn names that must exist in CaseSet
    - PAge5
    - CGMInfoBf24h
    - DietBaseNutriN2CTknBf24h
  input_args:
    vocab_size: 2000
    max_seq_len: 512
```

**3. OutputArgs (optional) -- how to extract labels:**

```yaml
OutputArgs:
  output_method: '<OutputTfmFnName>'    # ls code/haifn/fn_aidata/entryoutput/
  output_casefn_list:
    - OutcomeEngagement
  output_args:
    label_column: 'engaged'
    label_rule: 'binary'
```

---

Concrete Code
=============

**Input TfmFn -- build_vocab_fn (2 params):**

```python
def build_vocab_fn(InputArgs, CF_to_CFVocab) -> dict:
    # Returns feat_vocab dict used by tfm_fn
    ...
```

**Input TfmFn -- tfm_fn (4 params):**

```python
def tfm_fn(case_features, InputArgs, CF_to_CFvocab, feat_vocab=None) -> dict:
    # Transforms one case's features into model-input columns
    ...
```

**Output TfmFn -- tfm_fn (2 params, NOT 4):**

```python
def tfm_fn(case, OutputArgs) -> {'label': np.int64(0 or 1)}:
    # Extracts label from one case row
    ...
```

**SplitFn -- adds split_ai column to df_tag (does NOT return split DataFrames):**

```python
def dataset_split_tagging_fn(df_tag, SplitArgs) -> df_tag:
    # Adds 'split_ai' column in-place, returns the tagged DataFrame
    ...
```

---

AIData_Pipeline
===============

```python
from haipipe.aidata_base import AIData_Pipeline

pipeline = AIData_Pipeline(config, SPACE, cache_combined_case=True)

# Path 1: CaseSet -> AIDataSet  (training)
aidata_set = pipeline.run(
    case_set=my_case_set,
    aidata_name='<aidata_name>',
    aidata_version='v0'
)

# Path 2: DataFrame -> transformed DataFrame  (inference)
df_transformed = pipeline.run(df_case=test_df, mode='inference')

# Path 3: Single case dict -> transformed dict  (inference)
result = pipeline.run(case_example=single_case, mode='inference')
```

---

Load AIDataSet
==============

```python
from haipipe.aidata_base.aidata_set import AIDataSet

# Correct: load by full path
aidata_set = AIDataSet.load_from_disk(path='/full/path/to/aidata', SPACE=SPACE)
aidata_set = AIDataSet.load_asset(path='/full/path/to/aidata', SPACE=SPACE)
```

**WRONG:** `load_from_disk` does NOT accept `set_name=` or `store_key=`.
Always pass a full absolute path.

---

Fn Types Overview
=================

```
Input Transforms   (entryinput/):   build_vocab_fn(InputArgs, CF_to_CFVocab)
                                    tfm_fn(case_features, InputArgs, CF_to_CFvocab, feat_vocab)
                                    -- 4 params

Output Transforms  (entryoutput/):  tfm_fn(case, OutputArgs)
                                    -- 2 params, NOT 4

Split Functions    (split/):        dataset_split_tagging_fn(df_tag, SplitArgs)
                                    -- adds split_ai column, does NOT return split DataFrames
```

---

Discovering Available Fns
=========================

```bash
ls code/haifn/fn_aidata/entryinput/
ls code/haifn/fn_aidata/entryoutput/
ls code/haifn/fn_aidata/split/
ls code-dev/1-PIPELINE/4-AIData-WorkSpace/
```

---

MUST DO
=======

**NOTE:** `source .venv/bin/activate` does NOT persist across Bash tool calls.
Always chain: `source .venv/bin/activate && source env.sh && python <script>`
Or call venv python directly: `.venv/bin/python script.py`

1. Activate .venv: `source .venv/bin/activate && source env.sh`
2. Remember: output of Layer 4 = input of Model training (Layer 5)
3. Ensure `input_casefn_list` references CaseFn names that exist in the CaseSet
4. Ensure `InputArgs.input_method` matches a registered TfmFn name
5. Use correct API signatures:
   - `build_vocab_fn` takes 2 params
   - input `tfm_fn` takes 4 params
   - output `tfm_fn` takes 2 params
6. Vocab files are at ROOT of the version dir -- no subdirectory
7. Present plan and get approval before any code changes

---

MUST NOT
========

1. NEVER edit `code/haifn/` directly -- edit builders in `code-dev/1-PIPELINE/4-AIData-WorkSpace/`
2. NEVER run Python without `.venv` activated
3. NEVER invent CaseFn names that don't exist in the CaseSet
4. NEVER assume a `vocab/` subdirectory exists (files are at ROOT)
5. NEVER mix up input `tfm_fn` (4 params) with output `tfm_fn` (2 params)
6. NEVER assume SplitFn returns split DataFrames -- it adds `split_ai` column to df_tag

---

Key File Locations
==================

```
Pipeline framework:
  code/haipipe/aidata_base/aidata_pipeline.py
  code/haipipe/aidata_base/aidata_set.py
  code/haipipe/aidata_base/aidata_utils.py

Fn loaders:
  code/haipipe/aidata_base/builder/tfmfn.py
  code/haipipe/aidata_base/builder/splitfn.py

Generated Input Transforms:   code/haifn/fn_aidata/entryinput/  (discover with ls)
Generated Output Transforms:  code/haifn/fn_aidata/entryoutput/ (discover with ls)
Generated SplitFns:           code/haifn/fn_aidata/split/       (discover with ls)

Builders (edit here):         code-dev/1-PIPELINE/4-AIData-WorkSpace/  (discover with ls)

Store path:                   _WorkSpace/4-AIDataStore/
Config template:              templates/4-aidata/config.yaml
```
