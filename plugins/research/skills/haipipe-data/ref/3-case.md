Layer 3: Case
=============

Architecture Position
---------------------

Layer 1: Source -> Layer 2: Record -> **Layer 3: Case** <- (RecordSet -> event-triggered feature extraction)
  -> Layer 4: AIData -> Layer 5: Model -> Layer 6: Endpoint


Cooking Metaphor
----------------

```
Kitchen  = Case_Pipeline class        (code/haipipe/case_base/)
Chef     = TriggerFn + CaseFn         (code/haifn/fn_case/)  GENERATED
Recipe   = YAML config file           (config/caseset/ or tutorials/config/)
Dish     = CaseSet asset              (_WorkSpace/3-CaseStore/)
Academy  = Builder scripts            (code-dev/1-PIPELINE/3-Case-WorkSpace/)
```


What Is a CaseSet
-----------------

Output of Layer 3. Contains `df_case.parquet` + one `@`-prefixed parquet per CaseFn at ROOT level.

```
_WorkSpace/3-CaseStore/{RecSetName}/@v{N}CaseSet-{TriggerFolder}/
+-- df_case.parquet              (main file, NOT case_data.parquet)
+-- df_lts.parquet               (optional, for LTS triggers)
+-- df_Human_Info.parquet        (optional)
+-- @<CaseFnName1>.parquet       (at ROOT, NOT in subdirectory)
+-- @<CaseFnName2>.parquet
+-- cf_to_cfvocab.json
+-- manifest.json
```

**CRITICAL:** `df_case.parquet` NOT `case_data.parquet`. `@CaseFn.parquet` at ROOT, NOT in subdirectory.


Feature Naming Convention
--------------------------

Format: `<Feature><Window>`

```
Window suffixes:
  Bf24h    before 24h
  Af24h    after 24h
  Bf2h     before 2h
  Af2h     after 2h
  Af2to8h  after 2-8h
  CrntTime current time
  Base     static, no window
  Bf7d     before 7 days
  Af30d    after 30 days
```

Discover all registered CaseFns:

```bash
ls code/haifn/fn_case/case_casefn/
```


ROName 3-Part Format
--------------------

```
h<HumanFnName>.r<RecordFnName>.c<CkpdName>
```

Maps to `ROName_to_RONameInfo` with `HumanName`, `RecordName`, `CkpdName` keys.


Trigger vs CaseFn Separation
-----------------------------

**TriggerFn** -- identifies WHEN cases happen.
  Main function: `get_CaseTrigger_from_RecordBase()`
  Returns: `{'df_case': DataFrame, 'df_lts': DataFrame, 'df_Human_Info': DataFrame}`

**CaseFn** -- extracts WHAT features at trigger point.
  Main function: `fn_CaseFn()` with 6 params.
  Returns: dict with SUFFIX-ONLY keys (pipeline adds CaseFnName prefix automatically)


Concrete Code
-------------

**CaseFn module structure:**

```python
CaseFnName = "<CaseFnName>"

RO_to_ROName = {
    'RO': 'h<HumanFnName>.r<RecordFnName>.c<CkpdName>'
}

Ckpd_to_CkpdObsConfig = {
    '<CkpdName>': {
        'DistStartToPredDT': -1440,
        'DistEndToPredDT':   5,
        'TimeUnit':          'min',
        'StartIdx5Min':      -288,
        'EndIdx5Min':        1
    }
}

ROName_to_RONameInfo = {
    'h<HumanFnName>.r<RecordFnName>.c<CkpdName>': {
        'HumanName':  '...',
        'RecordName': '...',
        'CkpdName':   '...'
    }
}

HumanRecords = {'<HumanFnName>': ['<RecordFnName>']}

COVocab = {
    'tid2tkn': ['<Pad>', '<UNK>'],
    'tkn2tid': {'<Pad>': 0, '<UNK>': 1}
}

def fn_CaseFn(case_example, ROName_list, ROName_to_ROData, ROName_to_ROInfo, COVocab, context):
    # 6 positional params, returns SUFFIX-ONLY keys
    return {'--tid': [...], '--wgt': [...], '--val': [...]}

MetaDict = {...}
```

**TriggerFn module structure:**

```python
Trigger = "<TriggerFnName>"

Trigger_Args = {
    'Trigger':            '...',
    'case_id_columns':    [...],
    'case_raw_id_columns':[...],
    'HumanID_list':       [...],
    'ObsDT':              '...',
    'ROName_to_RONameArgs': {...}
}

def get_CaseTrigger_from_RecordBase(record_set, Trigger_Args, df_case_raw=None):
    return {'df_case': df, 'df_lts': df, 'df_Human_Info': df}
```

**Case_Pipeline:**

```python
pipeline  = Case_Pipeline(config, SPACE, context=None)
case_set  = pipeline.run(
    df_case=None,
    df_case_raw=None,
    record_set=record_set,
    use_cache=True,
    profile=False
)
```


CaseFn Output Suffixes
-----------------------

```
--tid    token ID list
--wgt    weight list
--val    value dict/list
--str    string/JSON
(none)   raw scalar
```


Ckpd_to_CkpdObsConfig Common Configurations
--------------------------------------------

```
Bf24h:  DistStart=-1440, DistEnd=5,    StartIdx=-288, EndIdx=1
Af24h:  DistStart=-5,    DistEnd=1440, StartIdx=-1,   EndIdx=288
Bf2h:   DistStart=-120,  DistEnd=5,    StartIdx=-24,  EndIdx=1
Base:   all 0 (static, no window)
```


Discovering Available Fns
--------------------------

```bash
ls code/haifn/fn_case/fn_trigger/
ls code/haifn/fn_case/case_casefn/
ls code-dev/1-PIPELINE/3-Case-WorkSpace/a*.py    # TriggerFn builders
ls code-dev/1-PIPELINE/3-Case-WorkSpace/c*.py    # CaseFn builders
```


MUST DO
-------

**NOTE:** `source .venv/bin/activate` does NOT persist across Bash tool calls.
Always chain: `source .venv/bin/activate && source env.sh && python <script>`
Or call venv python directly: `.venv/bin/python script.py`

1.  Activate `.venv` and `source env.sh`
2.  Remember: output of Layer 3 = input of Layer 4 (AIData)
3.  Follow `<Feature><Window>` naming convention
4.  Declare `ROName_to_RONameInfo` with all data dependencies in CaseFn
5.  Use 3-part ROName format: `h<HumanFnName>.r<RecordFnName>.c<CkpdName>`
6.  Return suffix-only keys from `fn_CaseFn` (e.g., `'--tid'`, not `'<CaseFnName>--tid'`)
7.  Name trigger function `get_CaseTrigger_from_RecordBase` (not `fn_TriggerFn`)
8.  Include `MetaDict` at end of CaseFn module
9.  Include `HumanRecords` mapping Human -> Record list
10. Present plan and get approval before code changes


MUST NOT
--------

1. NEVER edit `code/haifn/` directly
2. NEVER invent feature names outside `<Feature><Window>` convention
3. NEVER access Record data without going through `ROName_to_ROData`
4. NEVER prefix return keys with CaseFnName (pipeline does that automatically)
5. NEVER use 2-part ROName (must be 3-part: `h.r.c`)
6. NEVER skip `RUN_TEST` in builder
7. NEVER look for `case_data.parquet` (the file is `df_case.parquet`)
8. NEVER look for CaseFn files in a subdirectory (they are `@`-prefixed at ROOT)


Key File Locations
------------------

```
Pipeline framework:   code/haipipe/case_base/case_pipeline.py
                      code/haipipe/case_base/case_set.py
                      code/haipipe/case_base/case_utils.py
Fn loaders:           code/haipipe/case_base/builder/triggerfn.py
                      code/haipipe/case_base/builder/casefn.py
                      code/haipipe/case_base/builder/rotools.py
Generated TriggerFns: code/haifn/fn_case/fn_trigger/      (discover with ls)
Generated CaseFns:    code/haifn/fn_case/case_casefn/     (discover with ls)
Builders (edit here): code-dev/1-PIPELINE/3-Case-WorkSpace/  (discover with ls)
Store path:           _WorkSpace/3-CaseStore/
Config template:      templates/3-case/config.yaml
```
