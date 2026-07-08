---
name: haipipe-end-deploy-databricks
description: "Databricks Model Serving deploy specialist for haipipe-end. Wraps an Endpoint_Set into MLflow pyfunc + Unity Catalog model, deploys to Databricks Model Serving, runs live smoke tests, monitors, and tears down. Backed by platforms/platform-databrick-inference/. Reads Endpoint_Sets produced by haipipe-end-endpointset; never modifies them. Called by /haipipe-end orchestrator when deploy target is databricks."
argument-hint: "[function] [endpoint_set_or_id] [args...]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob
metadata:
  version: "1.2.0"
  last_updated: "2026-07-08"
  summary: "Databricks Model Serving deploy specialist for haipipe-end."
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

Skill: haipipe-end-deploy-databricks
==============================

Databricks Model Serving deployment specialist — one of **two production
deployment platforms** (the other is SageMaker via `haipipe-end-deploy-sagemaker`).

Consumes an Endpoint_Set built by `haipipe-end-endpointset` (canonical
input = the folder `_WorkSpace/6-EndpointStore/<endpoint_set>/`; the
`.tar.gz` twin is only the wire form uploaded to Databricks)
(its wire pair must be the Databricks one; Src2InputFn/Input2SrcFn are
per-platform by owner decision 2026-07-05), registers it as an MLflow pyfunc in Unity Catalog,
deploys to Databricks Model Serving, tests live, and cleans up.

**Backing repo:** `platforms/platform-databrick-inference/` (submodule of the main repo).
Contains `opt_program/mlflow_model.py` (MLflow wrapper), `opt_program/mlflow_packaging.py`
(UC registration), `scripts/build_endpoint/` (deploy pipeline), and per-product
configs under `config/<product>/<version>/dev.yaml`.

> Status: active. Deployment scripts implemented and tested with CGM + MIMIC
> endpoints. See `platforms/platform-databrick-inference/CLAUDE.md` for full reference.

  Function axis:  dashboard | deploy | test | monitor | teardown | review

---

Commands
--------

```
/haipipe-end-deploy-databricks                              -> dashboard: Databricks serving endpoints
/haipipe-end-deploy-databricks dashboard                    -> same
/haipipe-end-deploy-databricks deploy <endpoint_set>        -> register + deploy to Databricks
/haipipe-end-deploy-databricks test <endpoint_id>           -> hit live serving endpoint
/haipipe-end-deploy-databricks monitor <endpoint_id>        -> serving logs + invocation metrics
/haipipe-end-deploy-databricks teardown <endpoint_id>       -> stop endpoint, archive model version
/haipipe-end-deploy-databricks review <endpoint_id>         -> audit serving config + permissions
```

---

Dispatch Table
--------------

```
Invocation     Ref file(s)                              Function block
-------------- ---------------------------------------- -----------------------------------
dashboard      ../haipipe-end/ref/deploy-overview.md                          dashboard procedure
deploy         ../haipipe-end/ref/deploy-overview.md +
               ../haipipe-end/ref/
                 0-overview.md                          deploy procedure
test           ../haipipe-end/ref/deploy-overview.md                          test procedure
monitor        ../haipipe-end/ref/deploy-overview.md                          monitor procedure
teardown       ../haipipe-end/ref/deploy-overview.md                          teardown procedure
review         ../haipipe-end/ref/deploy-overview.md                          review procedure
```

---

Step-by-Step Protocol
----------------------

Step 0: Read `../haipipe-end/ref/deploy-overview.md` for Databricks-specific conventions.

Step 1: Parse args. Required arg per function:
          deploy: <endpoint_set_name>
          test/monitor/teardown/review: <serving_endpoint_id>

HOST NOTE: CLI + Model Serving require a serving-capable workspace — the
CDHAI host (`databricks.yml` profile `cdhai-new`), where the live
`reach-adhd-prediction-dev` endpoint runs. The REACH workspace itself is
browser-only, policy-locked USER_ISOLATION, no jobs/serving
(learn-databricks Lesson 15) — it cannot host what this skill deploys.

Step 2: Verify Databricks context:
          - DATABRICKS_HOST + DATABRICKS_TOKEN available
          - Unity Catalog reachable; catalog + schema configured
          - Workspace permissions for serving endpoints

Step 3: Execute the function.

Step 4: Emit the structured tail:

```
status:    ok | blocked | failed
summary:   2-3 sentences on the deploy / test / etc.
artifacts: [model URI, serving endpoint URL, registered version]
next:      suggested next command
```

---

Procedures (placeholder — fill from project's actual Databricks setup)
-----------------------------------------------------------------------

Deploy:
  1. Read Endpoint_Set at `_WorkSpace/6-EndpointStore/<endpoint_set>/`.
  2. Wrap `fn_endpoint/` + ModelInstance into an `mlflow.pyfunc` model. (logical bundle name; physically materialized as code/ + model/ in the set)
  3. Log model to MLflow tracking; register into Unity Catalog
     (`<catalog>.<schema>.<endpoint_set>`).
  4. Promote new version through configured stage transitions.
  5. Create or update Databricks Model Serving endpoint pointing at the
     registered model version.
  6. Wait for endpoint to reach READY.
  7. Run 1-payload smoke invocation; verify response.
  8. Record endpoint URL + model version in the project's deploy log.

Test, Monitor, Teardown, Review:
  See `../haipipe-end/ref/deploy-overview.md` for the Databricks-specific commands the project uses
  (`databricks` CLI or REST API patterns).

---

Platform repo and scripts
--------------------------

The actual deployment scripts live in `platforms/platform-databrick-inference/`
(git submodule). The platform-level skill doc is at
`Tools/skills/databricks-deploy/SKILL.md` (inside the platform repo).

### Verb lifecycle

```
VALIDATE → UPLOAD → REGISTER → DEPLOY → SMOKE TEST → STRESS TEST
```

### Script mapping

```
Verb           Script
-------------- -----------------------------------------------------------
validate       scripts/test_local.py
deploy (3ph)   scripts/build_endpoint/build_run_endpoint_databricks.py
smoke test     scripts/build_endpoint/test_smoke_endpoint_databricks.py
stress test    scripts/pressure_test/test_stress_endpoint_databricks.py
teardown       scripts/build_endpoint/teardown_endpoint_databricks.py
```

### Config

- Per-product config at `config/<product>/<release>/dev.yaml` with
  `uc_catalog`, `uc_schema`, `endpoint_name`.
- MIMIC example config: `config/mimic-mortality/v0001/dev.yaml`.

### Gotchas

- D-prefix tables must be excluded from payload (33 MB Databricks limit).
- Set `DATABRICKS_USER` env var for the MLflow experiment path.


Target Scope
-------------

Owns:
  - MLflow pyfunc wrapping of the Endpoint_Set
  - Unity Catalog registration (catalog / schema / model name)
  - Databricks Model Serving endpoint config
  - Workspace authentication
  - Live invocation smoke tests

Does NOT own:
  - Endpoint_Set content (read-only input from `/haipipe-end-endpointset`)

If a deploy fails because of an Endpoint_Set issue, escalate to
`/haipipe-end-endpointset review`.
