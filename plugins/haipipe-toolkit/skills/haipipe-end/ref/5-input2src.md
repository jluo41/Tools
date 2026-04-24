Input2SrcFn: Payload to ProcessedDF
=====================================

One of the 5 inference function types at Stage 6.

Input2SrcFn is the INVERSE of Src2InputFn and the ENTRY POINT of the inference
pipeline. It converts the incoming JSON payload into ProcName_to_ProcDf (the
internal source table format that PreFnPipeline expects).

Input2SrcFn is called at INFERENCE TIME (Step 2 of 7). It is the most critical
Fn type because it defines what fields the endpoint accepts from clients.

---

Architecture Position
=====================

```
Endpoint_Set.inference(payload_input_json)
  Step 1: TrigFn(payload_input_json)      -> df_case_raw | None
  Step 2: Input2SrcFn(payload_input_json) -> ProcName_to_ProcDf  <- HERE
  Step 3: PreFnPipeline(ProcDf)           -> RecordSet (in-memory)
  Step 4: PreFnPipeline(Record)           -> CaseSet (in-memory)
  Step 5: PreFnPipeline(Case)             -> model_input
  Step 6: ModelInfer(model_input)         -> DataFrame
  Step 7: PostFn(inference_df, SPACE)     -> response_json
```

---

Function Contract
=================

**Signature:** Input2SrcFn(payload_input_json, SPACE) -> Dict[str, pd.DataFrame]

**Input:**
  payload_input_json : Dict
    Raw JSON payload from client. Two supported formats:
    - Databricks: {"dataframe_records": [{...}]}
    - Legacy:     {"field1": ..., "field2": ..., "models": [...]}

  SPACE : Dict
    Workspace paths (needed for external data lookups, e.g., NDC, NPI tables)

**Output:**
  ProcName_to_ProcDf : Dict[str, pd.DataFrame]
    Internal source tables matching the schema expected by PreFnPipeline.
    Keys must match ProcName_List (see below).
    Schema per table must match ProcName_to_columns.

    Example:
    ```python
    {
      'Ptt': pd.DataFrame([{
          'PatientID': '12345',
          'Age': 45,
          'Gender': 'M',
          ...
      }]),
      'CGM': pd.DataFrame([{
          'PatientID': '12345',
          'ObservationDateTime': pd.Timestamp('2025-02-24 10:30:00'),
          'CGMValue': 142.5,
          ...
      }]),
    }
    ```

---

Module-Level Exports (CRITICAL)
=================================

In addition to the Input2SrcFn function, the generated .py file MUST export
three module-level variables that Endpoint_Pipeline reads to validate schema:

```python
# 1. List of table names (order matters -- must match RecordSet expectations)
ProcName_List = ['Ptt', 'CGM', 'Diet', ...]

# 2. Schema per table (column names only, no dtypes needed)
ProcName_to_columns = {
    'Ptt': ['PatientID', 'Age', 'Gender', 'DateOfBirth', ...],
    'CGM': ['PatientID', 'ObservationDateTime', 'CGMValue', ...],
    ...
}

# 3. Version string (for payload format validation)
SAMPLE_VERSION = 'v260101'
```

These are NOT inside MetaDict. They are top-level module variables.

---

File Structure
==============

```python
# code/haifn/fn_endpoint/fn_input2src/CGMDecoder_DBR_Payload2Src_v260101.py
# (GENERATED -- do not edit directly)

import pandas as pd
from datetime import datetime

# --- Module-level exports (read by Endpoint_Pipeline) ---
ProcName_List = ['Ptt', 'CGM']

ProcName_to_columns = {
    'Ptt': ['PatientID', 'Age', 'Gender'],
    'CGM': ['PatientID', 'ObservationDateTime', 'CGMValue', 'CGMUnit'],
}

SAMPLE_VERSION = 'v260101'


def Input2SrcFn(payload_input_json, SPACE):
    """
    Convert Databricks payload JSON -> ProcName_to_ProcDf (internal source tables).

    Inverse of Src2InputFn. Output must match ProcName_to_columns schema.
    """
    # Handle both payload formats
    if 'dataframe_records' in payload_input_json:
        records = payload_input_json['dataframe_records']
        record = records[0] if records else {}
    else:
        record = payload_input_json

    # Extract patient demographics -> Ptt table
    patient_id = str(record.get('patient_id', ''))
    df_ptt = pd.DataFrame([{
        'PatientID': patient_id,
        'Age': int(record.get('age', 0)),
        'Gender': str(record.get('gender', '')),
    }])

    # Extract CGM reading -> CGM table
    timestamp = record.get('timestamp', datetime.now().isoformat())
    cgm_value = float(record.get('cgm_value', 0.0))
    df_cgm = pd.DataFrame([{
        'PatientID': patient_id,
        'ObservationDateTime': pd.to_datetime(timestamp),
        'CGMValue': cgm_value,
        'CGMUnit': 'mg/dL',
    }])

    return {
        'Ptt': df_ptt,
        'CGM': df_cgm,
    }


MetaDict = {
    "Input2SrcFn": Input2SrcFn,
    "ProcName_List": ProcName_List,
    "ProcName_to_columns": ProcName_to_columns,
    "SAMPLE_VERSION": SAMPLE_VERSION,
}
```

---

Schema Consistency Requirements
=================================

The columns in ProcName_to_columns MUST match what the trained model's
PreFnPipeline expects. These come from the SourceSet schema used during training.

**Verify schema matches training:**

```python
# Load the endpoint
endpoint_set = Endpoint_Set.load_from_disk(path, SPACE)

# Get expected schema from prefn_pipeline
prefn = endpoint_set.get_prefn_pipeline()
expected_columns = prefn.ProcName_to_columns  # From training

# Get schema from Input2SrcFn
from haipipe.endpoint_base.builder.input2srcfn import Input2SrcFn as Input2SrcFnLoader
loader = Input2SrcFnLoader(config['Input2SrcFn'], SPACE)
actual_columns = loader.ProcName_to_columns  # From Fn

# Check for mismatches
for table in expected_columns:
    exp_cols = set(expected_columns[table])
    act_cols = set(actual_columns.get(table, []))
    missing = exp_cols - act_cols
    if missing:
        print(f"WARNING: {table} missing columns: {missing}")
```

---

Handling External Data Lookups
================================

Input2SrcFn can look up reference data using SPACE:

```python
def Input2SrcFn(payload_input_json, SPACE):
    # Look up NDC code -> medication name
    external_path = SPACE.get('LOCAL_EXTERNAL_STORE', '')
    ndc_path = os.path.join(external_path, 'ndc', 'ndc_lookup.parquet')
    if os.path.exists(ndc_path):
        df_ndc = pd.read_parquet(ndc_path)
        ndc_code = record.get('ndc_code', '')
        med_name = df_ndc[df_ndc['ndc'] == ndc_code]['name'].iloc[0]
    ...
```

This is valid. Input2SrcFn may need external data to enrich the payload.
External data is available at SPACE['LOCAL_EXTERNAL_STORE'] inside the endpoint.

---

Naming Convention
=================

```
File:     fn_endpoint/fn_input2src/{FnName}.py
Function: Input2SrcFn (MUST be exactly this name)
MetaDict: {"Input2SrcFn": Input2SrcFn, "ProcName_List": ..., ...}
```

Builder naming convention: e1_build_input2srcfn_{description}.py

Example names: CGMDecoder_DBR_Payload2Src_v260101, InferenceV240727

---

Builder Pattern
===============

**Step 1: Edit builder:**

```
code-dev/1-PIPELINE/6-Endpoint-WorkSpace/e1_build_input2srcfn_{description}.py
```

**Step 2: Configure at top:**

```python
OUTPUT_DIR = 'fn_endpoint/fn_input2src'
FN_NAME = 'CGMDecoder_DBR_Payload2Src_v260101'
RUN_TEST = True
```

**Step 3: Run builder:**

```bash
source .venv/bin/activate && source env.sh && python \
  code-dev/1-PIPELINE/6-Endpoint-WorkSpace/e1_build_input2srcfn_{description}.py
```

NOTE: source .venv/bin/activate does NOT persist across Bash tool calls.
Always chain: source .venv/bin/activate && source env.sh && python <script>

Generates: code/haifn/fn_endpoint/fn_input2src/{FN_NAME}.py

**Step 4: Reference in YAML:**

```yaml
Input2SrcFn: "CGMDecoder_DBR_Payload2Src_v260101"
```

---

MUST DO
=======

1. Name the function exactly Input2SrcFn
2. Export ProcName_List, ProcName_to_columns, SAMPLE_VERSION as module-level vars
3. Include all exported vars in MetaDict too
4. Output dict keys must exactly match ProcName_List entries
5. All DataFrame columns must match ProcName_to_columns schema
6. Handle both payload formats (dataframe_records and legacy flat)
7. Parse timestamps with pd.to_datetime() -- not raw strings

---

MUST NOT
=========

1. NEVER edit code/haifn/fn_endpoint/fn_input2src/*.py directly
2. NEVER return raw strings for timestamps -- use pd.Timestamp / pd.to_datetime
3. NEVER return None -- always return a dict of DataFrames
4. NEVER omit ProcName_List or ProcName_to_columns (Endpoint_Pipeline reads them)
5. NEVER import PreFnPipeline or model classes inside Input2SrcFn
