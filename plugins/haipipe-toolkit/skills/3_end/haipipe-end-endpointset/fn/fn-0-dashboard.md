fn-dashboard: Endpoint Store Status
=====================================

Scans _WorkSpace/6-EndpointStore/ and renders a status table showing
what endpoints are packaged, their health signals, and readiness for
inference or deployment.

---

Step 0: Discover Available Endpoints
======================================

**0a. Check prerequisites**

```bash
source .venv/bin/activate && source env.sh
```

NOTE: source .venv/bin/activate does NOT persist across Bash tool calls.
Always chain: source .venv/bin/activate && source env.sh && python <script>
Or call venv Python directly: .venv/bin/python script.py

Verify env vars are set:
  echo $LOCAL_ENDPOINT_STORE

**0b. Discover all endpoint directories**

Use Bash (ls) or Glob:

```bash
ls _WorkSpace/6-EndpointStore/
```

Each top-level directory is an endpoint package.
Group by model family (from manifest.json if available).

**0c. For each endpoint, gather four signals**

For each endpoint directory PATH:

Signal 1 -- Structural completeness
  Check for required top-level items:
    model/          <- model weights (required)
    code/           <- codebase snapshot (required)
    external/       <- reference data (required)
    examples/       <- test payloads (required)
    manifest.json   <- config + lineage (required)
    meta.json       <- MetaFn output (required)

  Status: COMPLETE | PARTIAL | BROKEN

Signal 2 -- Test payloads present
  For each subdirectory in examples/:
    Check for payload.json in that subdirectory

  Report: N/M examples have payload.json
  If all M examples have payload.json: READY
  If some missing: PARTIAL
  If none: NOT READY (packaging may have failed)

Signal 3 -- Inference function names (from manifest.json)
  Read manifest.json -> inference_functions key
  Report: MetaFn, TrigFn, PostFn, Src2InputFn, Input2SrcFn names

Signal 4 -- Deployment status
  Check for Databricks-specific artifacts:
    If mlruns/ or mlflow_model/ exists alongside: DEPLOYED (MLflow)
    Check platform-databrick-inference/ for recent deploy configs
  Report: LOCAL | DATABRICKS | SAGEMAKER | UNKNOWN

**0d. Render the status table**

```
Endpoint                                  Examples  Signals 1-4       Platform
────────────────────────────────────────  ────────  ────────────────  ──────────
endpoint_cgm_decoder_ohio                 3/3       COMPLETE READY    LOCAL
endpoint_sms_recommender_v0002           5/5       COMPLETE READY    DATABRICKS
endpoint_sms_recommender_v0001           5/5       COMPLETE READY    LOCAL
endpoint_demo_draft                       0/2       PARTIAL  PARTIAL  LOCAL
```

**0e. Show manifest summary for each endpoint**

For any endpoint with status COMPLETE, print the key manifest fields:

```json
{
  "endpoint_name": "endpoint_cgm_decoder_ohio",
  "endpoint_version": "v0001",
  "inference_functions": {
    "MetaFn": "CGMDecoder_DBR_v260101",
    "Input2SrcFn": "CGMDecoder_DBR_Payload2Src_v260101",
    "Src2InputFn": "CGMDecoder_DBR_Src2Payload_v260101",
    "TrigFn": "CGM5Min_v260101",
    "PostFn": "CGMForecast_v260101"
  },
  "created_at": "2026-02-24T14:30:00",
  "modelinstance_manifest": {
    "model_type": "TSForecast",
    "modelinstance_set_name": "Demo_TSDecoder/v0001"
  }
}
```

---

Step 0f: Summarize and Recommend Next Action
=============================================

After rendering the table, always provide a one-line recommendation:

- If no COMPLETE endpoints: "No packaged endpoints found. Run /haipipe-end package."
- If COMPLETE endpoints with no test: "Endpoints ready. Run /haipipe-end test."
- If COMPLETE + tested: "Endpoints ready for deployment. Run /haipipe-end deploy."
- If PARTIAL or BROKEN: "Fix packaging issues. Check manifest.json and examples/."

---

Checking Stage 5 (ModelInstance_Set) Availability
===================================================

The dashboard can optionally report what Stage 5 assets are available
to be packaged into Stage 6:

```bash
ls _WorkSpace/5-ModelInstanceStore/
```

If Stage 5 has trained models but Stage 6 has none matching them:
  "Stage 5 models available but not yet packaged: [model_name_list]"
  "Run /haipipe-end package to create endpoints."
