Skill: haipipe-data-4-aidata
=============================

Layer 4 of the 6-layer data pipeline: AIData Processing.

Converts a CaseSet into ML-ready datasets (AIDataSet). Handles train/val/test
splitting, input transforms (tabular, text, tensor, token embeddings), and
output transforms (labels, forecasts, next-token targets).

**Scope of this skill:** Framework patterns only. It does not catalog
project-specific state (which TfmFns/SplitFns are registered, CaseFn names,
aidata names). That state is always discovered at runtime from the filesystem.
This skill applies equally to any domain: CGM, EHR, wearables, NLP, etc.

Four subcommands:

  /haipipe-data-4-aidata load           Inspect existing AIDataSet
  /haipipe-data-4-aidata cook           Run AIData_Pipeline with config
  /haipipe-data-4-aidata design-chef    Create new TfmFn/SplitFn via builder
  /haipipe-data-4-aidata design-kitchen Upgrade AIData_Pipeline infra

On invocation, read this file for shared rules, then read the matching
subcommand file (1-load.md, 2-cook.md, 3-design-chef.md, 4-design-kitchen.md).

---

Architecture Position
=====================

```
Layer 6: Endpoint           Deployment packaging
    |
Layer 5: Model              Model training reads AIDataSet splits
    |
Layer 4: AIData  <---       CaseSet -> ML-ready datasets (train/val/test)
    |
Layer 3: Case               RecordSet -> event-triggered feature extraction
    |
Layer 2: Record             SourceSet -> temporally-aligned entity records
    |
Layer 1: Source             Raw files -> standardized tables
```

---

Cooking Metaphor
================

```
Kitchen  = AIData_Pipeline class     (code/haipipe/aidata_base/)
Chef     = TfmFn + SplitFn          (code/haifn/fn_aidata/)       -- GENERATED
Recipe   = YAML config file          (config/aidata/ or tutorials/config/)
Dish     = AIDataSet asset           (_WorkSpace/4-AIDataStore/)
Academy  = Builder scripts           (code-dev/1-PIPELINE/4-AIData-WorkSpace/)
```

---

What Is an AIDataSet?
=====================

An AIDataSet is the output of Layer 4. It wraps a HuggingFace DatasetDict
with vocabulary files and metadata. The model training layer (Layer 5)
reads this directly.

**Core attributes:**

```python
aidata_set.dataset_dict       # DatasetDict with split keys:
                              #   'train', 'validation', 'test-id', 'test-od'
aidata_set.CF_to_CFVocab      # Per-CaseFn vocabulary (saved as cf_to_cfvocab.json)
aidata_set.feat_vocab          # Feature vocabulary from build_vocab_fn (saved as feat_vocab.json)
aidata_set.meta_info           # MetaArgs configuration
aidata_set.split_info          # Split configuration used
aidata_set.transform_info      # Transform configuration used
```

**On-disk layout:**

```
_WorkSpace/4-AIDataStore/{aidata_name}/@{aidata_version}/
+-- train/                    HuggingFace Dataset (Parquet format)
|   +-- data-00000-of-00001.parquet
+-- validation/
|   +-- data-00000-of-00001.parquet
+-- test-id/                  In-distribution test
|   +-- data-00000-of-00001.parquet
+-- test-od/                  Out-of-distribution test (optional)
|   +-- data-00000-of-00001.parquet
+-- cf_to_cfvocab.json        Per-CaseFn vocabulary
+-- feat_vocab.json           Feature vocabulary from build_vocab_fn
+-- manifest.json             Lineage and metadata
+-- _cache_*/                 Cached domain-format data (optional)
```

**CRITICAL:** Vocab files are **cf_to_cfvocab.json** and **feat_vocab.json**
at the root of the AIDataSet directory. There is NO vocab/ subdirectory.

---

Three-Part Config Pattern
=========================

An AIData config has up to three sections. SplitArgs is optional (omit to
skip splitting). OutputArgs is optional (omit for inference-only pipelines).

**1. SplitArgs** -- How to split cases into train/val/test:

```yaml
SplitArgs:
  SplitMethod: '<SplitFnName>'         # discover: ls code/haifn/fn_aidata/split/
  ColumnName: '<split_column>'
  Split_to_Selection:
    train:
      Rules: [["<split_col>", "==", "train"]]
      Op: "and"
    validation:
      Rules: [["<split_col>", "==", "validation"]]
      Op: "and"
    test-id:
      Rules: [["<split_col>", "==", "test-id"]]
      Op: "and"
```

**2. InputArgs** -- How to transform case features into model inputs:

```yaml
InputArgs:
  input_method: "<InputTfmFnName>"     # discover: ls code/haifn/fn_aidata/entryinput/
  input_casefn_list:
    - '<CaseFnName1>'
    - '<CaseFnName2>'
  input_args:
    # Transform-specific args (depend on input_method)
    ...
```

**3. OutputArgs** -- How to extract labels/targets:

```yaml
OutputArgs:
  output_method: "<OutputTfmFnName>"   # discover: ls code/haifn/fn_aidata/entryoutput/
  output_casefn_list: []
  output_args:
    label_column: "<label_col>"
    label_rule: ["<label_col>", ">", 0]
```

---

Two-Stage TEToken Example
=========================

The TEToken transform (one option for time series) uses a two-stage pipeline.
This is a general temporal encoding -- applicable to any time series domain,
not just CGM.

```
Stage 1: window_build
  CaseFn fields -> TEWindow
  +-- time_series: concat <CaseFnName>Bf + <CaseFnName>Af -> [N_timesteps]
  +-- static_feat: <StaticCaseFn> -> key-value pairs
  +-- event_list: <EventCaseFn>Bf + <EventCaseFn>Af -> event list

Stage 2: tetoken
  TEWindow -> 4 output types:
  +-- singlevalue_timestep:      [batch, N_timesteps, N_fields]  continuous
  +-- singletoken_timestep:      [batch, N_timesteps, N_tokens]  discrete
  +-- multitoken_sparsetimestep: event dicts with positions
  +-- multitoken_global:         static text or token IDs
```

---

Concrete Code From the Repo
============================

**Input TfmFn -- build_vocab_fn** (2 parameters):

```python
# Example (illustrative -- actual module name depends on input_method):
# code/haifn/fn_aidata/entryinput/<InputTfmFnName>.py

def build_vocab_fn(InputArgs, CF_to_CFVocab):
    """Build vocabulary from config and per-CaseFn vocabularies.

    Args:
        InputArgs:      Transform configuration dict
        CF_to_CFVocab:  Per-CaseFn vocabulary dict

    Returns:
        feat_vocab dict (saved as feat_vocab.json)
    """
    input_args = InputArgs.get('input_args', {})
    # ... build vocabulary from config and per-CaseFn vocab ...
    return feat_vocab
```

**Input TfmFn -- tfm_fn** (4 parameters):

```python
# code/haifn/fn_aidata/entryinput/<InputTfmFnName>.py

def tfm_fn(case_features, InputArgs, CF_to_CFvocab, feat_vocab=None):
    """Transform one case's features into model-ready input.

    Args:
        case_features:  Dict with CaseFn data for one case
        InputArgs:      Transform configuration
        CF_to_CFvocab:  Per-CaseFn vocabulary
        feat_vocab:     Built vocabulary from build_vocab_fn (optional)

    Returns:
        dict with model-ready input features
    """
    ...
```

**Output TfmFn -- tfm_fn** (2 parameters):

```python
# code/haifn/fn_aidata/entryoutput/<OutputTfmFnName>.py

def tfm_fn(case, OutputArgs):
    """Extract label/target from case.

    Args:
        case:        Single case dict with all features
        OutputArgs:  Config with output_args

    Returns:
        dict with output features (e.g., {'label': np.int64(0 or 1)})
    """
    output_args = OutputArgs.get('output_args', {})
    label_column = output_args['label_column']
    value = case[label_column]
    return {'label': np.int64(int(value))}
```

**SplitFn -- dataset_split_tagging_fn** (adds split_ai column):

```python
# code/haifn/fn_aidata/split/<SplitFnName>.py

def dataset_split_tagging_fn(df_tag, SplitArgs):
    """Add 'split_ai' column to df_tag.

    Args:
        df_tag:     DataFrame with metadata columns
        SplitArgs:  Split configuration dict

    Returns:
        df_tag with 'split_ai' column added.
        Values: 'train', 'validation', 'test-id', 'test-od', or None
    """
    # ... maps source values to target splits ...
    df_tag['split_ai'] = mapped_values
    return df_tag
```

**AIData_Pipeline -- initialization and run:**

```python
# code/haipipe/aidata_base/aidata_pipeline.py

pipeline = AIData_Pipeline(config, SPACE, cache_combined_case=True)

# Three processing paths:
# Path 1: CaseSet(s) or cached dataset -> AIDataSet
aidata_set = pipeline.run(
    case_set=my_case_set,
    aidata_name='<aidata_name>',     # choose a name for the output
    aidata_version='v0'
)

# Path 2: DataFrame -> transformed DataFrame
df_transformed = pipeline.run(df_case=test_df, mode='inference')

# Path 3: Single case dict -> transformed dict
result = pipeline.run(case_example=single_case, mode='inference')
```

**Load an existing AIDataSet:**

```python
# code/haipipe/aidata_base/aidata_set.py

from haipipe.aidata_base.aidata_set import AIDataSet

aidata_set = AIDataSet.load_from_disk(path='/full/path/to/aidata', SPACE=SPACE)
# or
aidata_set = AIDataSet.load_asset(path='/full/path/to/aidata', SPACE=SPACE)
```

---

Fn Types Overview
=================

Three Fn types registered under code/haifn/fn_aidata/:

**Input Transforms (entryinput/):** Convert case features into model inputs.
Each has `build_vocab_fn(InputArgs, CF_to_CFVocab)` and
`tfm_fn(case_features, InputArgs, CF_to_CFvocab, feat_vocab)`.

**Output Transforms (entryoutput/):** Extract labels/targets from cases.
Each has `tfm_fn(case, OutputArgs)` (2 params, not 4).

**Split Functions (split/):** Tag cases with train/val/test assignments.
Each has `dataset_split_tagging_fn(df_tag, SplitArgs)`.

Discover registered Fns at runtime:

```bash
ls code/haifn/fn_aidata/entryinput/    # registered Input TfmFns
ls code/haifn/fn_aidata/entryoutput/   # registered Output TfmFns
ls code/haifn/fn_aidata/split/         # registered SplitFns
ls code-dev/1-PIPELINE/4-AIData-WorkSpace/  # builder scripts
```

These transforms and splits are domain-agnostic:
- Input transforms work for **any feature type**, not just time series
- Split strategies require **no domain knowledge**
- Output transforms handle **classification**, **regression**, and **generation**
- Everything is config-driven: change input_casefn_list and input_args for a different domain

---

Prerequisites
=============

Before working with AIData:

1. **Activate .venv**: `source .venv/bin/activate`
2. **Load environment**: `source env.sh`
3. **Input CaseSet must exist** at the path specified in case_set_name
4. **All CaseFn names** in input_casefn_list must be present in the CaseSet
5. **Layer 3 (Case) must be complete** before running Layer 4

---

MUST DO (All Subcommands)
=========================

1. **Activate** .venv first: `source .venv/bin/activate`
2. **Load** environment: `source env.sh`
3. **Remember** that output of Layer 4 = input of Model training (Layer 5)
4. **Ensure** input_casefn_list references CaseFn names that exist in the CaseSet
5. **Ensure** InputArgs.input_method matches a registered TfmFn name
6. **Present** plan to user and get approval before any code changes
7. **Use** correct API signatures (build_vocab_fn takes 2 params, not case_set)

---

MUST NOT (All Subcommands)
==========================

1. **NEVER edit** code/haifn/ directly (100% generated from builders)
2. **NEVER run** Python without .venv activated
3. **NEVER skip** `source env.sh` (store paths come from environment variables)
4. **NEVER invent** CaseFn names in input_casefn_list (must match actual CaseSet)
5. **NEVER assume** a vocab/ subdirectory exists (files are cf_to_cfvocab.json and feat_vocab.json at root)
6. **NEVER mix up** input tfm_fn (4 params) with output tfm_fn (2 params)
7. **NEVER assume** SplitFn returns a dict of split DataFrames (it adds a split_ai column to df_tag)

---

Key File Locations
==================

```
Pipeline framework:   code/haipipe/aidata_base/aidata_pipeline.py
                      code/haipipe/aidata_base/aidata_set.py
                      code/haipipe/aidata_base/aidata_utils.py
Fn loaders:           code/haipipe/aidata_base/builder/tfmfn.py
                      code/haipipe/aidata_base/builder/splitfn.py

Generated Input Tfms:  code/haifn/fn_aidata/entryinput/   <- discover with ls
Generated Output Tfms: code/haifn/fn_aidata/entryoutput/  <- discover with ls
Generated SplitFns:    code/haifn/fn_aidata/split/        <- discover with ls

Builders (edit these): code-dev/1-PIPELINE/4-AIData-WorkSpace/  <- discover with ls

Test configs:         config/                 <- discover with ls config/
Store path:           _WorkSpace/4-AIDataStore/
```

---

File Layout
===========

```
haipipe-data-4-aidata/
+-- SKILL.md              This file (router + shared rules)
+-- README.md             Quick reference
+-- 1-load.md             /haipipe-data-4-aidata load
+-- 2-cook.md             /haipipe-data-4-aidata cook
+-- 3-design-chef.md      /haipipe-data-4-aidata design-chef
+-- 4-design-kitchen.md   /haipipe-data-4-aidata design-kitchen
+-- templates/
    +-- config.yaml       Config template for cook subcommand
```

---

See Also
========

- **haipipe-data-1-source**: How raw data becomes SourceSets
- **haipipe-data-2-record**: How SourceSets become RecordSets
- **haipipe-data-3-case**: How RecordSets become CaseSets (input to this layer)
- **haipipe-nn-0-overview**: How AIDataSets feed into model training (Layer 5)
