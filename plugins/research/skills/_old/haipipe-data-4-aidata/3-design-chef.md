Subcommand: design-chef
=======================

Purpose: Create a new TfmFn or SplitFn via the builder pattern.
Edit builders in code-dev/ -> run -> generates code/haifn/fn_aidata/.

This skill documents FRAMEWORK PATTERNS only -- not project-specific state.
It applies to any domain: tabular features, time series tokens, text, sparse tensors.

---

Workflow
========

0. **Inspect existing builders and registered Fns:**
   ```bash
   ls code-dev/1-PIPELINE/4-AIData-WorkSpace/c*.py   # TfmFn builders
   ls code-dev/1-PIPELINE/4-AIData-WorkSpace/s*.py   # SplitFn builders
   ls code/haifn/fn_aidata/entryinput/               # registered Input TfmFns
   ls code/haifn/fn_aidata/entryoutput/              # registered Output TfmFns
   ls code/haifn/fn_aidata/split/                    # registered SplitFns
   ```
1. **Present** plan to user -> get approval
2. **Copy** an existing builder as starting point (pick one closest to your use case)
3. **Edit** [CUSTOMIZE] sections only (keep [BOILERPLATE] as-is)
4. **Run** builder:
   ```bash
   source .venv/bin/activate
   source env.sh
   python code-dev/1-PIPELINE/4-AIData-WorkSpace/<your_builder>.py
   ```
5. **Verify** generated file in code/haifn/fn_aidata/entryinput/, entryoutput/, or split/
6. **Register** in config YAML (input_method, output_method, or SplitMethod)
7. **Test** end-to-end with AIData_Pipeline

---

Builder Location
================

```
code-dev/1-PIPELINE/4-AIData-WorkSpace/
+-- c<N>_build_transforms_<type>.py   (Input/Output TfmFn builders -- discover with ls)
+-- s<N>_build_splitfn_<method>.py    (SplitFn builders -- discover with ls)
+-- old/                               (Legacy builders)
```

Discover existing builders at runtime:

```bash
ls code-dev/1-PIPELINE/4-AIData-WorkSpace/c*.py   # TfmFn builders
ls code-dev/1-PIPELINE/4-AIData-WorkSpace/s*.py   # SplitFn builders
```

**Three types of builders:**

- **Input TfmFn builders (c* prefix):** Transform case features -> model inputs
- **Output TfmFn builders (c* prefix):** Transform case features -> labels
- **SplitFn builders (s* prefix):** Split cases into train/val/test

---

Naming Convention
=================

**Input TfmFn builder:** `c<N>_build_transforms_<type>.py`
  Example: `c8_build_transforms_multimodal.py`

**Output TfmFn builder:** `c<N>_build_transforms_<type>.py`
  Example: `c9_build_output_regression.py`

**SplitFn builder:** `s<N>_build_splitfn_<method>.py`
  Example: `s2_build_splitfn_crossval.py`

**Generated locations:**
- Input: `code/haifn/fn_aidata/entryinput/<TfmFnName>.py`
- Output: `code/haifn/fn_aidata/entryoutput/<TfmFnName>.py`
- Split: `code/haifn/fn_aidata/split/<SplitFnName>.py`

---

Correct Function Signatures
============================

**CRITICAL:** The function signatures below are verified from actual source code.
Getting these wrong will cause runtime errors.

---

Input TfmFn: build_vocab_fn (2 parameters)
============================================

```python
def build_vocab_fn(InputArgs, CF_to_CFVocab):
    """Build vocabulary from config and per-CaseFn vocabularies.

    Called ONCE during pipeline initialization (not per case).

    Args:
        InputArgs:      Transform configuration dict
                        Contains input_method, input_casefn_list, input_args
        CF_to_CFVocab:  Per-CaseFn vocabulary dict
                        Format: {CaseFnName: {vocab_size, tid2tkn, tkn2tid}}

    Returns:
        feat_vocab dict (saved as feat_vocab.json)
    """
    input_args = InputArgs.get('input_args', {})
    # Build vocabulary from config...
    return feat_vocab
```

**WRONG -- this signature does NOT exist:**

```python
# WRONG: build_vocab_fn does NOT take case_set as first param
def build_vocab_fn(case_set, InputArgs):  # WRONG!
```

---

Input TfmFn: tfm_fn (4 parameters)
====================================

```python
def tfm_fn(case_features, InputArgs, CF_to_CFvocab, feat_vocab=None):
    """Transform one case's features into model-ready input format.

    Called ONCE per case during the map operation.

    Args:
        case_features:  Dict with CaseFn data for one case
                        Keys like 'CGMValueBf24h--tid', 'PDemoBase--gender'
        InputArgs:      Config from YAML (input_method, input_args)
        CF_to_CFvocab:  Per-CaseFn vocabulary dict
        feat_vocab:     Built vocabulary from build_vocab_fn (optional)

    Returns:
        Dict with model input keys (e.g., input_ids, attention_mask)
    """
    input_args = InputArgs.get('input_args', {})
    # Transform case_features to model format...
    return {'input_ids': [...], 'attention_mask': [...]}
```

---

Output TfmFn: tfm_fn (2 parameters)
=====================================

```python
def tfm_fn(case, OutputArgs):
    """Extract labels/targets from a single case.

    Called ONCE per case. NOTE: Only 2 parameters, unlike input tfm_fn.

    Args:
        case:        Single case dict with all features
        OutputArgs:  Config from YAML with output_method, output_args

    Returns:
        Dict with output features (e.g., {'label': np.int64(0 or 1)})
    """
    output_args = OutputArgs.get('output_args', {})
    label_column = output_args['label_column']
    value = case[label_column]
    return {'label': np.int64(int(value))}
```

**CRITICAL:** Output tfm_fn takes only **2 params** (case, OutputArgs).
It does NOT take case_features, CF_to_CFvocab, or feat_vocab.

---

SplitFn: dataset_split_tagging_fn (adds column)
=================================================

```python
def dataset_split_tagging_fn(df_tag, SplitArgs):
    """Add 'split_ai' column to df_tag.

    Does NOT return a dict of split DataFrames. Returns the SAME df_tag
    with a new 'split_ai' column added.

    Args:
        df_tag:     DataFrame with metadata columns (no features)
        SplitArgs:  Split configuration dict with ColumnName, etc.

    Returns:
        df_tag with 'split_ai' column added.
        Values: 'train', 'validation', 'test-id', 'test-od', or None
    """
    column_name = SplitArgs.get('ColumnName', 'split_timebin')
    # Map source column values to split assignments...
    df_tag['split_ai'] = mapped_values
    return df_tag
```

**WRONG -- SplitFn does NOT return a dict of splits:**

```python
# WRONG: SplitFn does NOT return dict of DataFrames
def dataset_split_tagging_fn(df_tag, SplitArgs):
    return {'train': df_train, 'validation': df_val}  # WRONG!
```

---

Builder Template: Input TfmFn
==============================

```python
# ==========================================================
# [BOILERPLATE] Configuration
# ==========================================================
OUTPUT_DIR = 'fn_aidata/entryinput'
TFM_FN_NAME = 'InputMyTransform'     # [CUSTOMIZE] Name
RUN_TEST = True

# ==========================================================
# [CUSTOMIZE] Vocabulary Builder (2 params)
# ==========================================================
def build_vocab_fn(InputArgs, CF_to_CFVocab):
    """Build vocabulary from config (optional).

    Called once during pipeline init.
    Returns vocabulary dict for use in tfm_fn.
    """
    input_args = InputArgs.get('input_args', {})
    return {}

# ==========================================================
# [CUSTOMIZE] Transform Function (4 params)
# ==========================================================
def fn_InputMyTransform(case_features, InputArgs, CF_to_CFVocab, feat_vocab):
    """Transform case features into model-ready input format."""
    input_args = InputArgs.get('input_args', {})
    cgm_values = case_features['CGMValueBf24h--tid']
    return {
        'input_ids': cgm_values,
        'attention_mask': [1] * len(cgm_values),
    }

# ==========================================================
# [BOILERPLATE] Code Generation + Test
# ==========================================================
```

---

Builder Template: Output TfmFn
===============================

```python
# ==========================================================
# [BOILERPLATE] Configuration
# ==========================================================
OUTPUT_DIR = 'fn_aidata/entryoutput'
TFM_FN_NAME = 'OutputMyLabels'      # [CUSTOMIZE] Name
RUN_TEST = True

# ==========================================================
# [CUSTOMIZE] Output Transform Function (2 params only!)
# ==========================================================
def fn_OutputMyLabels(case, OutputArgs):
    """Extract labels/targets from case.

    NOTE: Only 2 params -- (case, OutputArgs).
    Do NOT add case_features, CF_to_CFVocab, or feat_vocab.
    """
    output_args = OutputArgs.get('output_args', {})
    return {'label': np.int64(case[output_args['label_column']])}

# ==========================================================
# [BOILERPLATE] Code Generation + Test
# ==========================================================
```

---

Builder Template: SplitFn
=========================

```python
# ==========================================================
# [BOILERPLATE] Configuration
# ==========================================================
OUTPUT_DIR = 'fn_aidata/split'
SPLIT_FN_NAME = 'MySplitMethod'     # [CUSTOMIZE] Name
RUN_TEST = True

# ==========================================================
# [CUSTOMIZE] Split Function (adds split_ai column)
# ==========================================================
def fn_MySplitMethod(df_tag, SplitArgs):
    """Add 'split_ai' column to df_tag.

    Returns df_tag with 'split_ai' column, NOT a dict of DataFrames.
    """
    column = SplitArgs['ColumnName']
    # Map values to split assignments...
    df_tag['split_ai'] = df_tag[column].map(split_mapping)
    return df_tag

# ==========================================================
# [BOILERPLATE] Code Generation + Test
# ==========================================================
```

---

TEToken Transform Architecture
===============================

The TEToken transform (most complex) uses a two-stage pipeline:

```
Stage 1: window_build
  CaseFn fields -> TEWindow
  +-- time_series: concat CGMValueBf24h + CGMValueAf24h -> [576]
  +-- static_feat: PDemoBase -> key-value pairs
  +-- event_list: DEMEventBf24h + DEMEventAf24h -> event list

Stage 2: tetoken
  TEWindow -> 4 output types:
  +-- singlevalue_timestep:      [batch, 576, N_fields]  continuous
  +-- singletoken_timestep:      [batch, 576, N_tokens]  discrete
  +-- multitoken_sparsetimestep: event dicts with positions
  +-- multitoken_global:         static text or token IDs
```

---

MUST DO
=======

- **Present** plan to user -> get approval -> execute
- **Activate** .venv and run `source env.sh` before running builders
- **Follow** [BOILERPLATE] + [CUSTOMIZE] pattern
- **Set** RUN_TEST = True
- **Use** correct signatures: build_vocab_fn(InputArgs, CF_to_CFVocab)
- **Use** correct signatures: input tfm_fn(case_features, InputArgs, CF_to_CFvocab, feat_vocab)
- **Use** correct signatures: output tfm_fn(case, OutputArgs) -- only 2 params
- **Use** correct signatures: dataset_split_tagging_fn(df_tag, SplitArgs) -- adds column
- **Include** build_vocab_fn if transform needs vocabulary

---

MUST NOT
========

- **NEVER edit** code/haifn/fn_aidata/ directly -- always use builders
- **NEVER skip** the builder -> generate -> test cycle
- **NEVER use** wrong signatures (build_vocab_fn does NOT take case_set)
- **NEVER return** a dict of split DataFrames from SplitFn (add split_ai column instead)
- **NEVER give** output tfm_fn more than 2 params (case, OutputArgs)
- **NEVER skip** `source env.sh` (workspace paths are required)
- **NEVER skip** RUN_TEST
- **NEVER break** existing transform interfaces
