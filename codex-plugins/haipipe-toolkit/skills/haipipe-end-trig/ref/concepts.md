TrigFn: Trigger Detection
==========================

One of the 5 inference function types at Stage 6.

TrigFn determines whether a given payload should trigger model inference.
It is the first step in Endpoint_Set.inference(). If TrigFn returns None,
inference is skipped and a default response is returned immediately.

---

Architecture Position
=====================

```
Endpoint_Set.inference(payload_input_json)
  Step 1: TrigFn(payload_input_json)
    -> df_case_raw    (trigger condition MET: continue to Step 2)
    -> None           (trigger condition NOT MET: skip inference, return default)
  Step 2: Input2SrcFn(payload_input_json)  <- only reached if Step 1 returns df_case_raw
  ...
```

TrigFn is called per-request at inference time (unlike MetaFn which runs at packaging).

---

Function Contract
=================

**Signature:** TrigFn(payload_input_json) -> DataFrame | None

**Input:**
  payload_input_json : Dict
    The raw incoming JSON payload (same object passed to inference())

**Output:**
  DataFrame : df_case_raw
    Contains trigger detection results. Schema is Fn-specific but must be
    a valid pandas DataFrame (non-empty means trigger fires).

  None
    Inference should be skipped. Endpoint_Set returns a default "no-inference"
    response without calling Input2SrcFn or the model.

---

File Structure
==============

```python
# code/haifn/fn_endpoint/fn_trig/CGM5Min_v260101.py
# (GENERATED -- do not edit directly)

import pandas as pd
from datetime import datetime

def TrigFn(payload_input_json):
    """
    Fire on every 5-minute CGM reading.
    Returns df_case_raw with trigger info, or None if payload is not a CGM entry.
    """
    # Parse the incoming payload
    records = payload_input_json.get('dataframe_records', [payload_input_json])
    if not records:
        return None

    record = records[0]

    # Check trigger condition
    entry_type = record.get('entry_type', '')
    if entry_type != 'cgm_5min':
        return None    # Not a CGM reading -- skip inference

    # Build df_case_raw (trigger metadata)
    df_case_raw = pd.DataFrame([{
        'ObsDT': pd.to_datetime(record.get('timestamp', datetime.now().isoformat())),
        'PatientID': record.get('patient_id', ''),
        'TriggerName': 'CGM5MinEntry',
    }])

    return df_case_raw


MetaDict = {
    "TrigFn": TrigFn
}
```

---

Skip Logic
==========

When TrigFn returns None, Endpoint_Set.inference() returns a standard
"no-trigger" response immediately:

```python
# Inside Endpoint_Set.inference():
df_case_raw = self._trig_fn(payload_input_json)
if df_case_raw is None:
    return {
        "status": {"code": 200, "message": "No trigger -- inference skipped"},
        "models": []
    }
```

Use None returns for:
- Wrong payload type (e.g., a lab result arriving at a CGM endpoint)
- Outside triggering hours (if the model only applies at certain times)
- Missing required fields that make inference impossible

---

When TrigFn Can Be Omitted
============================

If EVERY request should trigger inference (no filtering), TrigFn can be a
pass-through that always returns a non-None DataFrame:

```python
def TrigFn(payload_input_json):
    """Always trigger inference."""
    return pd.DataFrame([{'triggered': True}])
```

Even a pass-through must follow the signature (return DataFrame, not True).

---

Naming Convention
=================

```
File:     fn_endpoint/fn_trig/{FnName}.py
Function: TrigFn (MUST be exactly this name)
MetaDict: {"TrigFn": TrigFn}
```

Builder naming convention: b1_build_trigfn_{description}.py

Example names: AnyInv_v250205, CGM5Min_v260101

---

Builder Pattern
===============

**Step 1: Edit builder:**

```
code-dev/1-PIPELINE/6-Endpoint-WorkSpace/b1_build_trigfn_{description}.py
```

**Step 2: Configure at top:**

```python
OUTPUT_DIR = 'fn_endpoint/fn_trig'
FN_NAME = 'CGM5Min_v260101'
RUN_TEST = True
```

**Step 3: Run builder:**

```bash
source .venv/bin/activate && source env.sh && python \
  code-dev/1-PIPELINE/6-Endpoint-WorkSpace/b1_build_trigfn_{description}.py
```

NOTE: source .venv/bin/activate does NOT persist across Bash tool calls.
Always chain: source .venv/bin/activate && source env.sh && python <script>

Generates: code/haifn/fn_endpoint/fn_trig/{FN_NAME}.py

**Step 4: Reference in YAML:**

```yaml
TrigFn: "CGM5Min_v260101"
```

---

MUST DO
=======

1. Name the function exactly TrigFn
2. Include MetaDict = {"TrigFn": TrigFn}
3. Return a pandas DataFrame (non-None) when trigger fires
4. Return None (not False, not empty DataFrame) when trigger does NOT fire
5. Handle both payload formats: dataframe_records and legacy flat

---

MUST NOT
=========

1. NEVER edit code/haifn/fn_endpoint/fn_trig/*.py directly
2. NEVER return an empty DataFrame to mean "skip" -- use None
3. NEVER call Input2SrcFn or the model inside TrigFn
4. NEVER raise exceptions for normal "skip" cases -- return None
