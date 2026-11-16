fn-design-chef, stages 3 and 4: Case and AIData Fn references
==============================================================

The second half of the design-chef procedure. Read `fn-3-design-chef.md` first: it holds Rule #1,
the BUILDER HOME, the Universal Builder Workflow, the stage references for 1-source and 2-record,
and the Universal MUST DO and MUST NOT that also govern the two stages below.

---

Stage Reference: 3-case
=========================

**What You Build**: TriggerFn (when to create a case) OR CaseFn (what features to extract at the trigger point).
These are two separate types with different builders.

**Builder Locations**:
```
<BUILDER_HOME>/a{N}_build_trigger_{name}.py   (TriggerFn; seeds: haibuilder/3-case/)
<BUILDER_HOME>/c{N}_build_casefn_{feature}.py (CaseFn)
```

- - -

TriggerFn
----------

**Generated Output**:
```
code/haifn/fn_case/fn_trigger/{TriggerFnName}.py
```

**Required Attributes and Function**:

```python
Trigger        # str — trigger event type name (e.g., 'CGM5MinEntry')
Trigger_Args   # dict — args passed to the trigger function

def get_CaseTrigger_from_RecordBase(
    record_set,
    Trigger_Args,
    df_case_raw=None
) -> dict:
    # Returns dict with keys:
    #   'df_case'       — one row per triggered case
    #   'df_lts'        — longitudinal time series data
    #   'df_Human_Info' — one row per human entity
    ...
```

NOTE: The function MUST be named `get_CaseTrigger_from_RecordBase` exactly.
Do NOT name it `fn_TriggerFn` or anything else.

- - -

CaseFn
-------

**Generated Output**:
```
code/haifn/fn_case/case_casefn/{CaseFnName}.py
```

**Naming Convention**:
```
<Feature><Window>
Examples:
  CGMValueBf24h      (CGM value, before 24 hours)
  LabValueBf7d       (lab value, before 7 days)
  PDemoBase          (patient demographics, no window)
  InvCrntTimeFixedLen (invitation, current time features)
```

**Required Module Attributes**:

```python
CaseFnName              # str — must match file name
RO_to_ROName            # dict[str, str] — short alias -> ROName (3-part)
Ckpd_to_CkpdObsConfig  # dict — checkpoint observation config
ROName_to_RONameInfo    # dict — metadata per ROName
HumanRecords            # dict — which HumanFn/RecordFn this CaseFn uses
COVocab                 # dict — controlled vocabulary for tokenization
MetaDict                # dict — REQUIRED 7 keys (see below)

# MetaDict must contain exactly these 7 keys for builder code generation:
MetaDict = {
    "CaseFnName":              CaseFnName,
    "RO_to_ROName":            RO_to_ROName,
    "Ckpd_to_CkpdObsConfig":  Ckpd_to_CkpdObsConfig,
    "ROName_to_RONameInfo":    ROName_to_RONameInfo,
    "HumanRecords":            HumanRecords,
    "COVocab":                 COVocab,
    "fn_CaseFn":               fn_CaseFn
}

def fn_CaseFn(
    case_example,
    ROName_list,
    ROName_to_ROData,
    ROName_to_ROInfo,
    COVocab,
    context
) -> dict:
    # Returns dict with SUFFIX-ONLY keys.
    # Pipeline automatically prepends CaseFnName to each key.
    # Valid suffixes: --tid, --wgt, --val, --str
    ...
```

**ROName 3-Part Format**:
```
h<HumanFnName>.r<RecordFnName>.c<CkpdName>

Example:
  hOhioHuman.rOhioCGM.cBf24h

  where:
    hOhioHuman  = HumanFn name (with h prefix)
    rOhioCGM    = RecordFn name (with r prefix)
    cBf24h      = Checkpoint name (with c prefix)
```

**Return Key Format** (SUFFIX-ONLY):
```python
# CORRECT — suffix only, pipeline adds CaseFnName prefix
return {
    '--tid': token_id_array,
    '--wgt': weight_array,
    '--val': float_value,
    '--str': string_label,
}

# WRONG — do NOT include CaseFnName in the key
return {
    'CGMValueBf24h--tid': ...,   # <-- WRONG
}
```

**Common Ckpd Window Configurations** (use as reference when setting Ckpd_to_CkpdObsConfig):

```
Window   | DistStart | DistEnd | StartIdx | EndIdx | Meaning
---------+-----------+---------+----------+--------+------------------------
Bf24h    | -1440     | 5       | -288     | 1      | 24h before trigger
Af24h    | -5        | 1440    | -1       | 288    | 24h after trigger
Bf2h     | -120      | 5       | -24      | 1      | 2h before trigger
Af2h     | -5        | 120     | -1       | 24     | 2h after trigger
Af2to8h  | -5        | 480     | -1       | 96     | 2-8h after trigger
Bf7d     | -10080    | 5       | -2016    | 1      | 7 days before trigger
Base     | 0         | 0       | 0        | 0      | Static (no window)
```

DistStart/DistEnd are in minutes from trigger.
StartIdx/EndIdx are in domain time units (5-min slots for CGM domain).
Positive = after trigger, Negative = before.

**Register in Config**:
```yaml
CaseArgs:
  Case_Args:
    - CaseFnList:
        - CGMValueBf24h
        - PDemoBase
        - MyNewCaseFn
```

**Downstream Contract** (satisfies 4-aidata stage):

Output suffix keys (`--tid`, `--wgt`) must match what downstream InputTfmFns expect via `input_casefn_list`.
If you rename a suffix, update the AIData config and TfmFn accordingly.

**MUST**:
- Use 3-part ROName format exactly: `h<Human>.r<Record>.c<Ckpd>`
- Return SUFFIX-ONLY keys from `fn_CaseFn`
- Include all required attributes: MetaDict, HumanRecords, Ckpd_to_CkpdObsConfig
- Name trigger function exactly `get_CaseTrigger_from_RecordBase`

---

Stage Reference: 4-aidata
===========================

**What You Build**: InputTfmFn (feature transforms), OutputTfmFn (label/target transforms), or SplitFn (train/val/test splitting).
Three separate types.

**Builder Location**:
```
<BUILDER_HOME>  (b10_aidatastore/j0N_{tfmfn,splitfn}_*/tNN_*/scripts/; seeds: code/scripts/haibuilder/4-aidata/)
  c<N>_build_transforms_<type>.py    (Input/Output TfmFn builders -- discover with ls)
  s<N>_build_splitfn_<method>.py     (SplitFn builders -- discover with ls)
```

**Builder Script Structure** (what you [CUSTOMIZE] vs [BOILERPLATE]):

```
[BOILERPLATE]  Output dir setup, builder infrastructure, generate-and-save logic
[CUSTOMIZE]    FnName, build_vocab_fn body, tfm_fn body (InputTfmFn)
[CUSTOMIZE]    FnName, tfm_fn body (OutputTfmFn)
[CUSTOMIZE]    FnName, dataset_split_tagging_fn body (SplitFn)
```

Start by copying the closest existing builder:

```bash
ls <BUILDER_HOME>/c*.py   # TfmFn builders
ls <BUILDER_HOME>/s*.py   # SplitFn builders
```

- - -

InputTfmFn
-----------

**Generated Output**:
```
code/haifn/fn_aidata/entryinput/{InputTfmFnName}.py
```

**Required Functions**:

```python
def build_vocab_fn(InputArgs, CF_to_CFVocab) -> dict:
    # Builds the feature vocabulary from case features.
    # Params: InputArgs (config), CF_to_CFVocab (per-CaseFn vocab dicts)
    # Returns: feat_vocab dict used during tfm_fn
    ...

def tfm_fn(case_features, InputArgs, CF_to_CFvocab, feat_vocab=None) -> dict:
    # Transforms raw case features into model-ready input tensors/arrays.
    # Params (4 total):
    #   case_features — dict of raw features from CaseFns
    #   InputArgs     — config dict
    #   CF_to_CFvocab — per-CaseFn vocab dicts
    #   feat_vocab    — vocab built by build_vocab_fn (optional at build time)
    # Returns: dict of transformed features
    ...
```

**Register in Config**:
```yaml
InputArgs:
  input_method: MyInputTfmFn
```

- - -

OutputTfmFn
------------

**Generated Output**:
```
code/haifn/fn_aidata/entryoutput/{OutputTfmFnName}.py
```

**Required Function**:

```python
def tfm_fn(case, OutputArgs) -> dict:
    # Transforms a case into label/target output.
    # Params (2 total — NOT 4!):
    #   case       — the raw case dict
    #   OutputArgs — config dict
    # Returns: dict with label or target key
    ...
```

NOTE: OutputTfmFn `tfm_fn` takes ONLY 2 params, unlike InputTfmFn which takes 4.

**Register in Config**:
```yaml
OutputArgs:
  output_method: MyOutputTfmFn
```

- - -

SplitFn
--------

**Generated Output**:
```
code/haifn/fn_aidata/split/{SplitFnName}.py
```

**Required Function**:

```python
def dataset_split_tagging_fn(df_tag, SplitArgs) -> pd.DataFrame:
    # Assigns train/validation/test-id/test-od splits to each row.
    # Params: df_tag (DataFrame with one row per case), SplitArgs (config)
    # Returns: df_tag with 'split_ai' column added
    #   Values: 'train', 'validation', 'test-id', 'test-od'
    ...
```

**Register in Config**:
```yaml
SplitArgs:
  SplitMethod: MySplitFn
```
