fn-design: Build New Inference Functions
==========================================

Guides creation of new inference function files via the builder pattern.
Applies to all 5 Fn types: MetaFn, TrigFn, PostFn, Src2InputFn, Input2SrcFn.

NEVER edit code/haifn/fn_endpoint/ directly.
Always use builders in code-dev/1-PIPELINE/6-Endpoint-WorkSpace/.

---

Decision Tree: Which Fn Type to Build?
========================================

```
What does your new Fn do?

Defines the model name mapping and available predictions?
  -> MetaFn    (a1_build_metafn_*.py)
  -> ref/1-meta.md

Determines whether to run inference at all?
  -> TrigFn    (b1_build_trigfn_*.py)
  -> ref/2-trig.md

Formats model scores into client JSON response?
  -> PostFn    (c1_build_postfn_*.py)
  -> ref/3-post.md

Converts source tables → payload for test examples?
  -> Src2InputFn   (d1_build_src2inputfn_*.py)
  -> ref/4-src2input.md

Converts payload → source tables at inference time?
  -> Input2SrcFn   (e1_build_input2srcfn_*.py)
  -> ref/5-input2src.md
```

---

Before Writing Any Builder
===========================

1. Identify which existing Fn to use as reference:
   ```bash
   ls code/haifn/fn_endpoint/fn_meta/      # MetaFn examples
   ls code/haifn/fn_endpoint/fn_trig/      # TrigFn examples
   ls code/haifn/fn_endpoint/fn_post/      # PostFn examples
   ls code/haifn/fn_endpoint/fn_src2input/ # Src2InputFn examples
   ls code/haifn/fn_endpoint/fn_input2src/ # Input2SrcFn examples
   ```

2. Read the ref file for your Fn type (loaded from dispatch table).

3. Check existing builders in code-dev/1-PIPELINE/6-Endpoint-WorkSpace/:
   ```bash
   ls code-dev/1-PIPELINE/6-Endpoint-WorkSpace/
   ```
   Find the builder prefix matching your Fn type (a1/b1/c1/d1/e1).

---

Universal Builder Template
============================

Every builder script follows this structure regardless of Fn type:

```python
# code-dev/1-PIPELINE/6-Endpoint-WorkSpace/{prefix}_build_{fn-type}_{description}.py

import os, sys
SPACE_ROOT = os.environ.get('SPACE', '.')
sys.path.insert(0, os.path.join(SPACE_ROOT, 'code'))

from haifn.base import Base   # For code generation

# ─── [CUSTOMIZE] ────────────────────────────────────────────────────────────
OUTPUT_DIR = 'fn_endpoint/fn_{type}'          # e.g., fn_endpoint/fn_meta
FN_NAME    = 'MyFn_v260101'                   # Exact output filename (no .py)
RUN_TEST   = True                             # Run validation after generation
# ─── [END CUSTOMIZE] ────────────────────────────────────────────────────────


def {FnName}({args}):
    """
    [Document what this Fn does]
    """
    # [Your Fn implementation]
    return result


MetaDict = {
    "{FnName}": {FnName},
    # For Input2SrcFn, also include:
    # "ProcName_List": ProcName_List,
    # "ProcName_to_columns": ProcName_to_columns,
    # "SAMPLE_VERSION": SAMPLE_VERSION,
}

# ─── Generate the .py file ───────────────────────────────────────────────────
if __name__ == '__main__':
    output_path = os.path.join(
        SPACE_ROOT, 'code', 'haifn', OUTPUT_DIR, f'{FN_NAME}.py'
    )
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    Base.convert_variables_to_pystring(
        variable_dict={'{FnName}': {FnName}, 'MetaDict': MetaDict},
        output_path=output_path
    )
    print(f"Generated: {output_path}")

    if RUN_TEST:
        # [Optional: run smoke test to verify the generated Fn loads]
        pass
```

---

Step-by-Step for Each Fn Type
================================

_______________________________________________
METAFN
_______________________________________________

Builder prefix: a1_build_metafn_*.py

Key things to customize:
  - modelName: the external name clients use to request this model
  - predictions list: all action names the model can return
  - metadata_response: pre-built JSON for metadata API requests

```python
FN_NAME = 'MyCGMDecoder_v260101'

def MetaFn(SPACE):
    ENDPOINT_NAME = SPACE['MODEL_ENDPOINT']
    modelName = 'CGMDecoderOhio'               # <- CUSTOMIZE
    predictions = ['normal', 'hypo', 'hyper']  # <- CUSTOMIZE: action names

    Local_to_External = {ENDPOINT_NAME: modelName}
    External_to_Local = {v: k for k, v in Local_to_External.items()}
    modelMetadata = [{'modelName': modelName, 'predictions': predictions}]
    metadata_response = {
        "body": {"modelMetadata": modelMetadata},
        "contentType": "application/json",
        "invokedProductionVariant": "AllTraffic"
    }
    return {
        'Local_to_External_ModelSeries': Local_to_External,
        'External_to_Local_ModelSeries': External_to_Local,
        'modelMetadata': modelMetadata,
        'metadata_response': metadata_response,
    }

MetaDict = {"MetaFn": MetaFn}
```

_______________________________________________
TRIGFN
_______________________________________________

Builder prefix: b1_build_trigfn_*.py

Key things to customize:
  - Trigger condition (what makes a request valid)
  - Trigger field in payload to check
  - Return a DataFrame (trigger fires) or None (skip inference)

```python
FN_NAME = 'CGM5Min_v260101'

def TrigFn(payload_input_json):
    records = payload_input_json.get('dataframe_records', [payload_input_json])
    record = records[0] if records else {}

    entry_type = record.get('entry_type', '')  # <- CUSTOMIZE: field name
    if entry_type != 'cgm_5min':               # <- CUSTOMIZE: trigger value
        return None

    import pandas as pd
    df_case_raw = pd.DataFrame([{
        'PatientID': record.get('patient_id', ''),
        'TriggerName': 'CGM5MinEntry',
    }])
    return df_case_raw

MetaDict = {"TrigFn": TrigFn}
```

_______________________________________________
POSTFN
_______________________________________________

Builder prefix: c1_build_postfn_*.py

Key things to customize:
  - Action list to include in predictions
  - Score scaling (raw [0,1] -> display [0,100])
  - Response model name (matches MetaFn modelName)

```python
FN_NAME = 'CGMForecast_v260101'

from datetime import datetime

def PostFn(ModelArtifactName_to_Inference, SPACE):
    ENDPOINT_VERSION = SPACE.get('MODEL_ENDPOINT', 'unknown')
    model_entries = []

    for model_name, dataset_ifr in ModelArtifactName_to_Inference.items():
        if dataset_ifr is None or len(dataset_ifr) == 0:
            continue
        row = dataset_ifr.iloc[0]

        score_cols = [c for c in dataset_ifr.columns if c.startswith('score__')]
        ranked = sorted(
            [(c.replace('score__', ''), round(float(row[c]) * 100, 2)) for c in score_cols],
            key=lambda x: x[1], reverse=True
        )
        if not ranked:
            continue

        best_name, best_score = ranked[0]
        model_entries.append({
            "name": model_name,         # <- from ModelArtifactName_to_Inference key
            "date": datetime.now().isoformat(),
            "version": ENDPOINT_VERSION,
            "action": {"name": best_name, "score": best_score},
            "predictions": [{"name": n, "score": s} for n, s in ranked],
        })

    if not model_entries:
        return {"status": {"code": 500, "message": "No predictions"}, "models": []}

    return {"models": model_entries, "status": {"code": 200, "message": "Success"}}

MetaDict = {"PostFn": PostFn}
```

_______________________________________________
SRC2INPUTFN
_______________________________________________

Builder prefix: d1_build_src2inputfn_*.py

Key things to customize:
  - Which tables to read from ProcName_to_ProcDf
  - Which columns to extract and how to map to payload fields
  - Output payload format (match Input2SrcFn input)

Read ref/4-src2input.md and ref/5-input2src.md together.
Src2InputFn MUST produce output that Input2SrcFn can parse.

```python
FN_NAME = 'CGMDecoder_DBR_Src2Payload_v260101'
import json

def Src2InputFn(ProcName_to_ProcDf, SPACE):
    df_ptt = ProcName_to_ProcDf.get('Ptt')
    df_cgm = ProcName_to_ProcDf.get('CGM')

    patient_id = str(df_ptt['PatientID'].iloc[0]) if df_ptt is not None else ''
    timestamp  = df_cgm['ObservationDateTime'].max().isoformat() if df_cgm is not None else ''
    cgm_value  = float(df_cgm['CGMValue'].iloc[-1]) if df_cgm is not None else 0.0

    record = {
        "patient_id": patient_id,
        "timestamp": timestamp,
        "cgm_value": cgm_value,
        "entry_type": "cgm_5min",       # <- matches TrigFn trigger condition
        "models": json.dumps(["CGMDecoderOhio"]),  # <- matches MetaFn modelName
    }
    return {"dataframe_records": [record]}

MetaDict = {"Src2InputFn": Src2InputFn}
```

_______________________________________________
INPUT2SRCFN
_______________________________________________

Builder prefix: e1_build_input2srcfn_*.py

Key things to customize:
  - ProcName_List: table names expected by the model
  - ProcName_to_columns: schema per table
  - Parsing logic: extract payload fields -> DataFrame rows

Read ref/5-input2src.md carefully. ProcName_List and ProcName_to_columns
MUST match the schema the model was trained on.

```python
FN_NAME = 'CGMDecoder_DBR_Payload2Src_v260101'
import pandas as pd

ProcName_List = ['Ptt', 'CGM']
ProcName_to_columns = {
    'Ptt': ['PatientID', 'Age', 'Gender'],
    'CGM': ['PatientID', 'ObservationDateTime', 'CGMValue', 'CGMUnit'],
}
SAMPLE_VERSION = 'v260101'

def Input2SrcFn(payload_input_json, SPACE):
    if 'dataframe_records' in payload_input_json:
        record = payload_input_json['dataframe_records'][0]
    else:
        record = payload_input_json

    patient_id = str(record.get('patient_id', ''))
    timestamp  = pd.to_datetime(record.get('timestamp'))
    cgm_value  = float(record.get('cgm_value', 0.0))

    return {
        'Ptt': pd.DataFrame([{'PatientID': patient_id, 'Age': 0, 'Gender': ''}]),
        'CGM': pd.DataFrame([{
            'PatientID': patient_id,
            'ObservationDateTime': timestamp,
            'CGMValue': cgm_value,
            'CGMUnit': 'mg/dL',
        }]),
    }

MetaDict = {
    "Input2SrcFn": Input2SrcFn,
    "ProcName_List": ProcName_List,
    "ProcName_to_columns": ProcName_to_columns,
    "SAMPLE_VERSION": SAMPLE_VERSION,
}
```

---

Running the Builder
====================

```bash
source .venv/bin/activate && source env.sh && python \
  code-dev/1-PIPELINE/6-Endpoint-WorkSpace/{prefix}_build_{fn-type}_{description}.py
```

NOTE: source .venv/bin/activate does NOT persist across Bash tool calls.
Always chain the activation + env + python in a single command.

Verify the generated file:
```bash
cat code/haifn/fn_endpoint/fn_{type}/{FN_NAME}.py
```

---

Post-Generation Checklist
===========================

After running the builder, verify:

  [ ] Generated .py file exists in code/haifn/fn_endpoint/fn_{type}/
  [ ] Function is named exactly {FnType} (MetaFn, TrigFn, etc.)
  [ ] MetaDict = {"{FnType}": {FnType}} present at bottom
  [ ] For Input2SrcFn: ProcName_List, ProcName_to_columns, SAMPLE_VERSION present
  [ ] Quick load test passes:
      ```bash
      source .venv/bin/activate && source env.sh && python -c "
      from haipipe.endpoint_base.builder.{loader} import {LoaderClass}
      loader = {LoaderClass}('{FN_NAME}', {})
      print('Loaded:', loader.{FnType})
      "
      ```
  [ ] YAML config updated to reference the new Fn name

---

Generation Order (when building all 5 Fns for a new endpoint)
===============================================================

Always write in this order (Input2SrcFn first since it defines the schema):

  1. Input2SrcFn  (e1)  <- defines ProcName_List + ProcName_to_columns
  2. Src2InputFn  (d1)  <- inverse of Input2SrcFn; write after to ensure consistency
  3. MetaFn       (a1)  <- model name mapping
  4. TrigFn       (b1)  <- trigger condition
  5. PostFn       (c1)  <- response format

Then package: /haipipe-end package
Then test:    /haipipe-end test
