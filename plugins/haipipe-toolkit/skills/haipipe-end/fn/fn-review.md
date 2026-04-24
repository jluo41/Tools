fn-review: Endpoint Review Protocol
=====================================

Reviews Fn files in code/haifn/fn_endpoint/ for correctness,
schema consistency, and cross-compatibility.

---

Step 0: Gather Scope
======================

Identify which Fn types to review:

```bash
ls code/haifn/fn_endpoint/fn_meta/
ls code/haifn/fn_endpoint/fn_trig/
ls code/haifn/fn_endpoint/fn_post/
ls code/haifn/fn_endpoint/fn_src2input/
ls code/haifn/fn_endpoint/fn_input2src/
```

For a targeted review, read only the relevant Fn file(s).
For a full endpoint review, read all 5 Fn files referenced in manifest.json.

---

Step 1: Read the Manifest
===========================

Get the Fn names currently in use from the packaged endpoint:

```bash
cat _WorkSpace/6-EndpointStore/{endpoint_name}/manifest.json | python -m json.tool
```

Extract the `inference_functions` block:

```json
{
  "inference_functions": {
    "MetaFn":      "CGMDecoder_DBR_v260101",
    "TrigFn":      "CGM5Min_v260101",
    "PostFn":      "CGMForecast_v260101",
    "Src2InputFn": "CGMDecoder_DBR_Src2Payload_v260101",
    "Input2SrcFn": "CGMDecoder_DBR_Payload2Src_v260101"
  }
}
```

Then read each file listed.

---

Step 2: Per-Fn Checklist
==========================

For each Fn file, apply the checklist specific to its type.

_______________________________________________
METAFN CHECK
_______________________________________________

File: code/haifn/fn_endpoint/fn_meta/{MetaFnName}.py

  [ ] Function signature is exactly: MetaFn(SPACE)
  [ ] Returns a dict with all 4 required keys:
        Local_to_External_ModelSeries   <- {ENDPOINT_NAME: modelName}
        External_to_Local_ModelSeries   <- {modelName: ENDPOINT_NAME}
        modelMetadata                   <- [{'modelName': ..., 'predictions': [...]}]
        metadata_response               <- {'body': {...}, 'contentType': ..., 'invokedProductionVariant': ...}
  [ ] modelName matches what clients use (case-sensitive)
  [ ] predictions list matches all action names from PostFn
  [ ] MetaDict = {"MetaFn": MetaFn} present at bottom
  [ ] No side effects (no I/O, no state mutations)

Cross-check:
  modelName must match the value in Src2InputFn's `"models"` JSON field

_______________________________________________
TRIGFN CHECK
_______________________________________________

File: code/haifn/fn_endpoint/fn_trig/{TrigFnName}.py

  [ ] Function signature is exactly: TrigFn(payload_input_json)
  [ ] Returns pd.DataFrame (trigger fires) or None (skip inference)
  [ ] Handles BOTH payload formats:
        - Databricks: payload_input_json.get('dataframe_records', [])
        - Legacy flat: payload_input_json itself
  [ ] Returns None gracefully if records list is empty
  [ ] The DataFrame columns include at minimum: PatientID, TriggerName
  [ ] MetaDict = {"TrigFn": TrigFn} present at bottom
  [ ] Trigger condition documented in a comment

Cross-check:
  TriggerName value in returned DataFrame should match the trigger
  configured in the PreFnPipeline inside the endpoint

_______________________________________________
POSTFN CHECK
_______________________________________________

File: code/haifn/fn_endpoint/fn_post/{PostFnName}.py

  [ ] Function signature is exactly: PostFn(ModelArtifactName_to_Inference, SPACE)
  [ ] Returns dict with keys: "models" (list) and "status" (dict with "code" and "message")
  [ ] "status.code" = 200 on success, != 200 on failure
  [ ] Each entry in "models" has:
        name        <- string (model artifact name)
        date        <- ISO timestamp string
        version     <- string
        action      <- {"name": ..., "score": ...}
        predictions <- [{"name": ..., "score": ...}]
  [ ] Scores are in display range [0, 100], not raw [0, 1]
  [ ] Handles None or empty DataFrames gracefully (skips, does not crash)
  [ ] Falls back to error status if model_entries is empty
  [ ] MetaDict = {"PostFn": PostFn} present at bottom

Cross-check:
  Action names in predictions must match MetaFn's predictions list

_______________________________________________
SRC2INPUTFN CHECK
_______________________________________________

File: code/haifn/fn_endpoint/fn_src2input/{Src2InputFnName}.py

  [ ] Function signature is exactly: Src2InputFn(ProcName_to_ProcDf, SPACE)
  [ ] Returns dict in Databricks format: {"dataframe_records": [record_dict]}
  [ ] All ProcName keys accessed match Input2SrcFn's ProcName_List
  [ ] Output record fields map 1:1 to Input2SrcFn expected fields
  [ ] The `"models"` field contains a JSON string (json.dumps([modelName]))
  [ ] modelName in the "models" field matches MetaFn's modelName
  [ ] entry_type field matches TrigFn's trigger condition
  [ ] MetaDict = {"Src2InputFn": Src2InputFn} present at bottom
  [ ] Handles missing/None DataFrames safely (uses defaults, not crashes)

Cross-check:
  Run round-trip validation: Src2InputFn(Input2SrcFn(payload)) ≈ payload
  Key fields must survive the round-trip without data loss

_______________________________________________
INPUT2SRCFN CHECK
_______________________________________________

File: code/haifn/fn_endpoint/fn_input2src/{Input2SrcFnName}.py

  [ ] Function signature is exactly: Input2SrcFn(payload_input_json, SPACE)
  [ ] Returns dict: {ProcName: pd.DataFrame, ...}
  [ ] All keys in return dict are in ProcName_List
  [ ] Handles BOTH payload formats (dataframe_records and legacy flat)
  [ ] ProcName_List defined at module level (not inside function)
  [ ] ProcName_to_columns defined at module level (not inside function)
  [ ] SAMPLE_VERSION defined at module level (not inside function)
  [ ] DataFrame schemas match ProcName_to_columns exactly (column names + count)
  [ ] MetaDict = {"Input2SrcFn": ..., "ProcName_List": ..., "ProcName_to_columns": ..., "SAMPLE_VERSION": ...}
  [ ] All columns in ProcName_to_columns are present in each returned DataFrame
  [ ] Types are correct: timestamp fields are pd.Timestamp, numeric fields are float/int

Cross-check:
  ProcName_List and ProcName_to_columns must match what the PreFnPipeline
  and model training pipeline expected. If schemas mismatch, inference will fail.

---

Step 3: Cross-Fn Consistency Checks
======================================

After individual Fn checks, verify the 5 Fns are internally consistent.

**Name chain check:**

```
MetaFn.modelName
  == Src2InputFn output record["models"] JSON list entry
  == what the endpoint serves under

MetaFn.predictions
  == PostFn score column names (after stripping "score__" prefix)

TrigFn trigger field/value
  == Src2InputFn output record["entry_type"]

Input2SrcFn.ProcName_List
  == ProcName keys accessed in Src2InputFn

Input2SrcFn.ProcName_to_columns[ProcName]
  == columns in DataFrames returned by Input2SrcFn
  == columns expected by PreFnPipeline CaseFns
```

**Verify schema alignment with model:**

```python
# Read Input2SrcFn's ProcName_to_columns
from haipipe.endpoint_base.builder.input2srcfn import Input2SrcFnLoader
loader = Input2SrcFnLoader('{Input2SrcFnName}', SPACE)
print("ProcName_List:", loader.ProcName_List)
print("ProcName_to_columns:", loader.ProcName_to_columns)

# Compare against PreFnPipeline expected input in endpoint
import json
with open('_WorkSpace/6-EndpointStore/{endpoint_name}/manifest.json') as f:
    manifest = json.load(f)
print("Endpoint config:", manifest.get('deployment_config'))
```

---

Step 4: Round-Trip Test
=========================

Validate that Src2InputFn and Input2SrcFn are true inverses:

```python
import os, json
import pandas as pd
SPACE = os.environ.copy()

# Load both Fns
from haipipe.endpoint_base.builder.src2inputfn import Src2InputFnLoader
from haipipe.endpoint_base.builder.input2srcfn import Input2SrcFnLoader

src2input_loader = Src2InputFnLoader('{Src2InputFnName}', SPACE)
input2src_loader  = Input2SrcFnLoader('{Input2SrcFnName}', SPACE)

# Load a real example
with open('_WorkSpace/6-EndpointStore/{endpoint_name}/examples/example_000_xxx/payload.json') as f:
    payload = json.load(f)

# Round-trip: payload -> ProcDf -> payload2
proc_dfs   = input2src_loader.Input2SrcFn(payload, SPACE)
payload2   = src2input_loader.Src2InputFn(proc_dfs, SPACE)

# Compare key fields
r1 = payload['dataframe_records'][0]
r2 = payload2['dataframe_records'][0]

shared_keys = set(r1.keys()) & set(r2.keys())
for k in sorted(shared_keys):
    match = str(r1[k]) == str(r2[k])
    print(f"  {k}: {'OK' if match else 'MISMATCH'} ({r1[k]!r} vs {r2[k]!r})")
```

Expected: all shared_keys match.
Allowed discrepancies: float precision, timestamp format normalization.
Not allowed: missing keys, None vs value, wrong type.

---

Step 5: Load Test for All Fns
================================

Verify all Fns load cleanly before packaging:

```bash
source .venv/bin/activate && source env.sh && python -c "
import os
SPACE = os.environ.copy()

from haipipe.endpoint_base.builder.metafn     import MetaFnLoader
from haipipe.endpoint_base.builder.trigfn     import TrigFnLoader
from haipipe.endpoint_base.builder.postfn     import PostFnLoader
from haipipe.endpoint_base.builder.src2inputfn import Src2InputFnLoader
from haipipe.endpoint_base.builder.input2srcfn import Input2SrcFnLoader

print('Loading MetaFn...',    MetaFnLoader('{MetaFnName}', SPACE).MetaFn)
print('Loading TrigFn...',    TrigFnLoader('{TrigFnName}', SPACE).TrigFn)
print('Loading PostFn...',    PostFnLoader('{PostFnName}', SPACE).PostFn)
print('Loading Src2InputFn...', Src2InputFnLoader('{Src2InputFnName}', SPACE).Src2InputFn)
print('Loading Input2SrcFn...', Input2SrcFnLoader('{Input2SrcFnName}', SPACE).Input2SrcFn)
print('All 5 Fns loaded OK')
"
```

NOTE: source .venv/bin/activate does NOT persist across Bash tool calls.
Always chain: source .venv/bin/activate && source env.sh && python <script>

---

Step 6: Review Summary
========================

After running all checks, produce a summary:

```
Fn Review Summary: endpoint_cgm_decoder_ohio
=============================================

MetaFn      (CGMDecoder_DBR_v260101)        PASS
TrigFn      (CGM5Min_v260101)               PASS
PostFn      (CGMForecast_v260101)           PASS
Src2InputFn (CGMDecoder_DBR_Src2Payload_v260101)  PASS
Input2SrcFn (CGMDecoder_DBR_Payload2Src_v260101)  PASS

Cross-Fn Checks
  Name chain:      PASS
  Schema alignment: PASS
  Round-trip:      PASS

Load test:         PASS (all 5 Fns loaded)

Status: READY for /haipipe-end package
```

If any check fails, list the specific items:

```
Input2SrcFn  FAIL
  [ERROR] ProcName_to_columns["CGM"] has 4 columns but Input2SrcFn returns 5
  [WARN]  SAMPLE_VERSION not defined at module level (found inside __init__)
```

---

Common Issues
===============

```
Issue                                     Fix
────────────────────────────────────────  ───────────────────────────────────────────
MetaFn modelName case mismatch           Exact string match required; check client usage
TrigFn returns None for all payloads    Check entry_type field and trigger condition
PostFn scores > 100 or < 0             Raw [0,1] scores not scaled; multiply by 100
Src2InputFn "models" field wrong        Must be json.dumps([modelName]), not string
Input2SrcFn missing SAMPLE_VERSION      Define at module level, add to MetaDict
Round-trip fails on timestamp field     Normalize to ISO string before comparison
Schema mismatch (column count wrong)    Re-run Input2SrcFn builder; check ProcName_to_columns
```
