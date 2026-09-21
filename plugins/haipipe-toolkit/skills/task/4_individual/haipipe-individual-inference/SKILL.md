---
name: haipipe-individual-inference
description: >-
  Per-individual endpoint inference test: loads one individual from
  A-User-Store, builds an Endpoint_Set payload, POSTs it to a deployed
  endpoint (local FastAPI / Databricks / SageMaker), and prints the forecast.
  Use to smoke-test that an endpoint accepts individual data. Trigger:
  individual inference, test endpoint with individual.
argument-hint: "--individual <id_or_path> [--endpoint-url URL] [--json]"
allowed-tools: Bash, Read
metadata:
  version: "0.1.1"
  last_updated: "2026-07-04"
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
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

The wire payload matches the deployed Endpoint_Set's platform-specific `Input2SrcFn`.
Select Databricks dataframe_records or SageMaker flat JSON; a local wrapper follows its packaged pair.

---

Layout
-------

```
src/
  load_patient.py    Subject-XX → patient_ctx dict (parquet → DataFrames)
  build_payload.py   individual path → platform-specific JSON (Endpoint_Set contract)
  client.py          POST selected JSON → forecast (auth + retry-friendly)

scripts/
  show_ctx_cli.py            inspect an individual's loaded context
  test_individual_predict.py    end-to-end: individual id → POST → forecast
```

---

Quickstart
-----------

Use an already deployed endpoint when one is available.
For a new local server, follow `haipipe-end-deploy-local`: copy its reference
`serve_local.py` into the canonical serving Task's `scripts/` before launch.
Choose the platform of the packaged Src2InputFn/Input2SrcFn pair.

```sh
python Tools/plugins/haipipe-toolkit/skills/task/4_individual/haipipe-individual-inference/scripts/test_individual_predict.py \
    --workspace-root /path/to/project \
    --individual UserGroup-OhioT1DM/Subject-559 \
    --platform sagemaker \
    --endpoint-model endpoint_cgm_patchtst_ohio/v0001 \
    --endpoint-url http://127.0.0.1:8765/invocations
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

## Workspace and platform selection

Pass `workspace_root` (or CLI `--workspace-root`) as the project containing `_WorkSpace`.
Resolution is explicit argument, then `HAIPIPE_WORKSPACE_ROOT`, then the nearest ancestor
of cwd containing `_WorkSpace`. Absolute Subject paths resolve directly. Ambiguous
Subject shorthands raise; no developer machine root is built in.
`build_payload(..., platform="databricks" | "sagemaker")` selects the wire shape;
Databricks remains the compatibility default. Local wrappers use the deployed pair's
platform setting. Direct SageMaker calls require AWS SDK/SigV4 transport; the included
HTTP client supports ordinary JSON HTTP endpoints and optional bearer authentication.

Use `--endpoint-model` for the deployed model id. In the report CLI, `--model` selects the report-writing LLM and is a different setting.
