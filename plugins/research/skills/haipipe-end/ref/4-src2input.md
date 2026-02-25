Src2InputFn: ProcessedDF to Payload
=====================================

One of the 5 inference function types at Stage 6.

Src2InputFn is the INVERSE of Input2SrcFn. It converts ProcessedDF tables
(the source data format used internally during training) into JSON payloads
(the format external clients send at inference time).

Src2InputFn is called during PACKAGING (Endpoint_Pipeline.run()), not during
inference. It generates the test payload.json files stored in each example
directory.

---

Architecture Position
=====================

```
Endpoint_Pipeline.run()
  Phase 1: Load examples from ModelInstance_Set.examples_data
             examples_data[i] = {
               'ProcName_to_ProcDf': {...},   <- internal source tables
               'prediction_results': {...},
             }
  Phase 2: Generate JSON payloads
             for each example:
               payload = Src2InputFn(ProcName_to_ProcDf, SPACE)
               save as examples/example_{i}_{uuid}/payload.json
  Phase 3: Package into Endpoint_Set
```

Src2InputFn IS NOT called at inference time.
Input2SrcFn IS called at inference time (opposite direction).

---

Function Contract
=================

**Signature:** Src2InputFn(ProcName_to_ProcDf, SPACE) -> Dict

**Input:**
  ProcName_to_ProcDf : Dict[str, pd.DataFrame]
    Internal source tables, e.g.:
      {'Ptt': df_patient, 'invitation': df_inv, 'Rx': df_rx, ...}
    These match the tables produced by the RecordSet pipeline.

  SPACE : Dict
    Workspace paths (may be needed for reference data lookups)

**Output:**
  Dict representing the JSON payload that a client would send:
  ```json
  {
    "dataframe_records": [{
      "patient_id": "12345",
      "timestamp": "2025-02-24T10:30:00",
      "models": "[\"ModelName\"]",
      ...
    }]
  }
  ```

---

File Structure
==============

```python
# code/haifn/fn_endpoint/fn_src2input/CGMDecoder_DBR_Src2Payload_v260101.py
# (GENERATED -- do not edit directly)

import json
from datetime import datetime

def Src2InputFn(ProcName_to_ProcDf, SPACE):
    """
    Convert ProcName_to_ProcDf (internal) -> Databricks payload JSON (external).

    This is the inverse of Input2SrcFn: given the source tables used during
    model training, reconstruct the JSON payload a client would send.
    """
    # Extract patient demographics from Ptt table
    df_ptt = ProcName_to_ProcDf.get('Ptt', None)
    patient_id = str(df_ptt['PatientID'].iloc[0]) if df_ptt is not None else ''

    # Extract trigger time from invitation or CGM table
    df_cgm = ProcName_to_ProcDf.get('CGM', None)
    if df_cgm is not None and len(df_cgm) > 0:
        trigger_time = df_cgm['ObservationDateTime'].max().isoformat()
    else:
        trigger_time = datetime.now().isoformat()

    # Build the Databricks-format payload
    record = {
        "patient_id": patient_id,
        "timestamp": trigger_time,
        "entry_type": "cgm_5min",
        "models": json.dumps(["CGMDecoderOhio"]),
    }

    return {
        "dataframe_records": [record]
    }


MetaDict = {
    "Src2InputFn": Src2InputFn
}
```

---

Key Design Principle: The Inverse Relationship
===============================================

Src2InputFn and Input2SrcFn must be consistent:

```
Training data side:   ProcName_to_ProcDf
                          |
                     Src2InputFn          (packaging time: source → payload)
                          |
                       payload.json       <- stored in examples/
                          |
                     Input2SrcFn          (inference time: payload → source)
                          |
                   ProcName_to_ProcDf     (matches the training tables)
```

If you round-trip through both Fns, the tables should approximately reconstruct.
They don't need to be perfect (some fields may be dropped), but the key fields
used by the model (all fields that feed into CaseFns) MUST survive the round-trip.

**Validate the round-trip:**

```python
original = ProcName_to_ProcDf
payload = Src2InputFn(original, SPACE)
reconstructed = Input2SrcFn(payload, SPACE)

# Key fields must match
for table_name in original:
    orig_df = original[table_name]
    recon_df = reconstructed.get(table_name)
    if recon_df is not None:
        # Check key columns match
        key_cols = ['PatientID', 'ObservationDateTime']
        for col in key_cols:
            if col in orig_df.columns and col in recon_df.columns:
                assert orig_df[col].iloc[0] == recon_df[col].iloc[0], f"Mismatch in {table_name}.{col}"
```

---

Naming Convention
=================

```
File:     fn_endpoint/fn_src2input/{FnName}.py
Function: Src2InputFn (MUST be exactly this name)
MetaDict: {"Src2InputFn": Src2InputFn}
```

Builder naming convention: d1_build_src2inputfn_{description}.py

Example names: CGMDecoder_DBR_Src2Payload_v260101, InferenceInverseV1219

---

Builder Pattern
===============

**Step 1: Edit builder:**

```
code-dev/1-PIPELINE/6-Endpoint-WorkSpace/d1_build_src2inputfn_{description}.py
```

**Step 2: Configure at top:**

```python
OUTPUT_DIR = 'fn_endpoint/fn_src2input'
FN_NAME = 'CGMDecoder_DBR_Src2Payload_v260101'
RUN_TEST = True
```

**Step 3: Run builder:**

```bash
source .venv/bin/activate && source env.sh && python \
  code-dev/1-PIPELINE/6-Endpoint-WorkSpace/d1_build_src2inputfn_{description}.py
```

NOTE: source .venv/bin/activate does NOT persist across Bash tool calls.
Always chain: source .venv/bin/activate && source env.sh && python <script>

Generates: code/haifn/fn_endpoint/fn_src2input/{FN_NAME}.py

**Step 4: Reference in YAML:**

```yaml
Src2InputFn: "CGMDecoder_DBR_Src2Payload_v260101"
```

---

Testing Src2InputFn
====================

After packaging, verify the round-trip:

```python
# Load the endpoint
endpoint_set = Endpoint_Set.load_from_disk(path, SPACE)

# Load a training example
import json
with open('examples/example_000_{uuid}/ProcName_to_ProcDf/Ptt.parquet', 'rb') as f:
    df_ptt = pd.read_parquet(f)
# Load other tables similarly

# Check payload was generated
with open('examples/example_000_{uuid}/payload.json') as f:
    payload = json.load(f)

print("Payload keys:", list(payload.keys()))
print("First record:", payload['dataframe_records'][0])
```

---

MUST DO
=======

1. Name the function exactly Src2InputFn
2. Include MetaDict = {"Src2InputFn": Src2InputFn}
3. Return a dict (not a string) -- Endpoint_Pipeline serializes it to JSON
4. Produce output in the same format Input2SrcFn expects as input
5. Include the "models" field in the record (clients use this to route requests)

---

MUST NOT
=========

1. NEVER edit code/haifn/fn_endpoint/fn_src2input/*.py directly
2. NEVER call Input2SrcFn inside Src2InputFn (they are separate functions)
3. NEVER return None -- always return a valid payload dict
4. NEVER import PreFnPipeline or model classes inside Src2InputFn
