---
name: haipipe-end-deploy-mlflow
description: "MLflow deploy specialist for haipipe-end. STATUS: DEFERRED — no platform-mlflow-inference repo backs this yet; SKILL.md kept as a placeholder. Would register an Endpoint_Set into an MLflow Model Registry and serve via `mlflow models serve`. Reads Endpoint_Sets produced by haipipe-end-endpointset; never modifies them. The umbrella's no-args dashboard skips this skill while deferred."
argument-hint: [function] [endpoint_set_or_id] [args...]
allowed-tools: Bash, Read, Write, Edit, Grep, Glob
---

Skill: haipipe-end-mlflow
==========================

MLflow registry + serving specialist. Wraps an Endpoint_Set into an
MLflow `pyfunc` model, logs and registers it, and (optionally) serves it
via `mlflow models serve`. The registered model can also be the input
artifact for downstream MLflow-aware deployers.

> Status: scaffolded. Tracking server URI, registry name, and stage
> transition policy below are placeholders for the project to fill in.

  Function axis:  dashboard | deploy | test | monitor | teardown | review

---

Commands
--------

```
/haipipe-end-mlflow                              -> dashboard: registered models + versions
/haipipe-end-mlflow dashboard                    -> same
/haipipe-end-mlflow deploy <endpoint_set>        -> log + register, optionally `mlflow models serve`
/haipipe-end-mlflow deploy <es> --register-only  -> register but do not start a server
/haipipe-end-mlflow test <endpoint_id>           -> hit local `mlflow models serve` server
/haipipe-end-mlflow monitor <endpoint_id>        -> tail mlflow serve logs
/haipipe-end-mlflow teardown <endpoint_id>       -> stop server, archive model version
/haipipe-end-mlflow review <endpoint_id>         -> audit registered model + signature
```

---

Dispatch Table
--------------

```
Invocation     Ref file(s)                              Function block
-------------- ---------------------------------------- -----------------------------------
dashboard      ref/concepts.md                          dashboard procedure
deploy         ref/concepts.md +
               ../haipipe-end-endpointset/ref/
                 0-overview.md                          deploy procedure
test           ref/concepts.md                          test procedure
monitor        ref/concepts.md                          monitor procedure
teardown       ref/concepts.md                          teardown procedure
review         ref/concepts.md                          review procedure
```

---

Step-by-Step Protocol
----------------------

Step 0: Read `ref/concepts.md` for MLflow tracking URI, registry conventions,
        and stage transition policy.

Step 1: Parse args. Required arg per function:
          deploy: <endpoint_set_name> [--register-only] [--port N]
          test/monitor/teardown/review: <endpoint_id> (model name + version)

Step 2: Verify MLflow context:
          - MLFLOW_TRACKING_URI set
          - Registry credentials available (if using a remote backend)

Step 3: Execute the function.

Step 4: Emit the structured tail:

```
status:    ok | blocked | failed
summary:   2-3 sentences on the deploy / test / etc.
artifacts: [model URI, model name + version, serve URL if started]
next:      suggested next command
```

---

Procedures (placeholder — fill from project conventions)
---------------------------------------------------------

Deploy:
  1. Read Endpoint_Set at `_WorkSpace/6-EndpointStore/<endpoint_set>/`.
  2. Wrap `fn_endpoint/` + ModelInstance into an `mlflow.pyfunc.PythonModel`.
  3. `mlflow.start_run()` and log:
     - The pyfunc model with signature inferred from Endpoint_Set's manifest.
     - The Endpoint_Set's manifest as a run artifact.
     - Hyperparameters / training config from ModelInstance.
  4. Register the logged model into the MLflow Model Registry under
     `<endpoint_set>` name.
  5. Transition new version to the configured stage (e.g. `Staging`).
  6. If not `--register-only`: spawn `mlflow models serve` on the chosen port.
  7. Smoke-test the served endpoint or the registry record.
  8. Record endpoint_id (model_name + version) in the project's deploy log.

Test, Monitor, Teardown, Review:
  See `ref/concepts.md` for the `mlflow` CLI patterns the project uses.

---

Target Scope
-------------

Owns:
  - MLflow pyfunc wrapping of the Endpoint_Set
  - MLflow tracking run + registered model version
  - Stage transitions (Staging / Production / Archived)
  - `mlflow models serve` local serving
  - Model URI emission for downstream MLflow-aware deployers

Does NOT own:
  - Endpoint_Set content (read-only input from `/haipipe-end-endpointset`)
  - Downstream platform deploy (Databricks Model Serving uses
    `/haipipe-end-databricks` even though it consumes MLflow registry under
    the hood — keep concerns split for clarity)

If a deploy fails because of an Endpoint_Set issue, escalate to
`/haipipe-end-endpointset review`.
