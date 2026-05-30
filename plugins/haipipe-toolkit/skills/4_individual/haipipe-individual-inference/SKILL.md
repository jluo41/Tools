---
name: haipipe-individual-inference
description: "Per-individual endpoint inference test. Loads one individual from _WorkSpace/A-User-Store, builds an Endpoint_Set dataframe_records payload, POSTs it to a deployed endpoint URL (local FastAPI / Databricks / SageMaker — same wire contract), and prints the forecast response. Sibling of haipipe-individual (which loads data only). Use to smoke-test that a deployed endpoint accepts individual data correctly. Trigger: individual inference, test endpoint with individual, /haipipe-individual-inference."
argument-hint: "--individual <id_or_path> [--endpoint-url URL] [--json]"
allowed-tools: Bash, Read
---

Skill: haipipe-individual-inference
=================================

Single-individual inference smoke test against a deployed Endpoint_Set.

Pipeline:

```
  Subject-XX/                                            (haipipe-individual layout)
    ├── 1-SourceStore/{CGM,Diet,Ptt,...}.parquet
    └── manifest.yaml
            │
            ▼  load_patient_ctx()
       patient_ctx dict
            │
            ▼  build_payload()                 (Endpoint_Set wire contract)
       {dataframe_records: [{TriggerName_to_CaseTriggerList, inference_form: {ElogBGEntry, Patient}}]}
            │
            ▼  call_predict()  ── HTTP POST ──► <endpoint_url>/invocations
       forecast JSON
```

The wire payload matches the Endpoint_Set's documented `Input2SrcFn`
contract (Format 1 — dataframe_records). Same payload Databricks Model
Serving and SageMaker would consume; only `endpoint_url` differs.

---

Layout
-------

```
src/
  load_patient.py    Subject-XX → patient_ctx dict (parquet → DataFrames)
  build_payload.py   patient_ctx → dataframe_records JSON (Endpoint_Set contract)
  client.py          POST dataframe_records → forecast (auth + retry-friendly)

scripts/
  show_ctx_cli.py            inspect a individual's loaded context
  test_individual_predict.py    end-to-end: individual id → POST → forecast
```

---

Quickstart
-----------

Spin up a local endpoint server (skill: `haipipe-end-deploy-local`):

```
ENDPOINT_PATH=_WorkSpace/6-EndpointStore/<endpoint_name> \
    python Tools/plugins/haipipe-toolkit/skills/3_end/haipipe-end-deploy-local/scripts/serve_local.py
```

In another shell, hit it with a individual:

```
python Tools/plugins/haipipe-toolkit/skills/5_individual/haipipe-individual-inference/scripts/test_individual_predict.py \
    --individual Subject-18
```

Override the URL to test against a Databricks endpoint:

```
CGM_ENDPOINT_URL=https://<workspace>/serving-endpoints/<name>/invocations \
    python ...test_individual_predict.py --individual Subject-18
```

---

Individual resolution
------------------

`--individual` accepts:

| Form | Example |
|------|---------|
| absolute path | `/home/.../UserGroup-WellDoc2022CGM/Subject-18` |
| `UserGroup-X/Subject-Y` | `UserGroup-WellDoc2022CGM/Subject-18` |
| `Subject-Y` (auto-resolved if unique) | `Subject-18` |

Ambiguous bare ids raise `ValueError` listing the candidates.

---

Wire contract
-------------

```json
{
  "models": ["endpoint_cgm_patchtst_ohio/v0001"],
  "dataframe_records": [{
    "TriggerName_to_CaseTriggerList": {
      "CGM5MinEntry": [{"PatientID": "...", "ObsDT_UTC": "...", "TimezoneOffset": -240}]
    },
    "inference_form": {
      "ElogBGEntry": {"PatientID": [...], "ObservationDateTime": [...], "BGValue": [...]},
      "Patient":     {"PatientID": [...], "Gender": [...], "YearOfBirth": [...]},
      "PatientID":   "..."
    }
  }]
}
```

NaN / NaT in source parquet → `null` in JSON (handled by `_df_to_columnar`).

---

Failure modes
-------------

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| 500 `Inference error: 'TriggerName'` | Endpoint is missing `prefn_config.json` | Regenerate the Endpoint_Set with PreFnPipeline artifacts |
| `No model to call in current ModelSeries` | Payload `models` field doesn't match endpoint's `External_to_Local_ModelSeries` | Check `meta.json` and pass the right model id |
| `ValueError: Cannot resolve individual` | `--individual` shorthand matched 0 or >1 paths | Use full path or `UserGroup-X/Subject-Y` |
| `ValueError: No CGM data` | Individual parquet empty/missing | Check `1-SourceStore/CGM.parquet` exists and has rows |

---

Reuses
------

- Loads the individual layout produced by `haipipe-individual` (sibling skill).
- Targets endpoints produced by `haipipe-end-endpointset` and served by
  `haipipe-end-deploy-{local,databricks,sagemaker}`.
- Used by agent projects (e.g. `agent-cgm`) as the patient-data loader and
  payload builder for their LangGraph nodes.
