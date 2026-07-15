---
name: haipipe-end-develop-databricks
description: "Databricks develop specialist for haipipe-end. STATUS: DEFERRED — the backing repo platforms/platform-databrick-training/ EXISTS (submit_job.py, setup_cluster.sh, notebooks/) but this skill is not wired to it yet, and the job-based design must be reconciled with jobs-blocked clusters (learn-databricks Lesson 15). Would run Stage 5 training as a Databricks Job (notebook or wheel task) with model logged to Unity Catalog and exported as an Endpoint_Set under 6-EndpointStore/. The umbrella's no-args dashboard skips this skill while deferred."
argument-hint: "[verb] [config_or_run_id] [args...]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob
metadata:
  version: "1.2.0"
  last_updated: "2026-07-08"
  summary: "Databricks develop specialist for haipipe-end."
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

Skill: haipipe-end-develop-databricks
======================================

Databricks development specialist (DEFERRED).
Runs Stage 5 training as a Databricks Job, logs the resulting model to Unity Catalog (or the workspace MLflow registry), and exports an Endpoint_Set under `6-EndpointStore/` for the deploy specialists to consume.

> Status: DEFERRED — but the backing repo `platforms/platform-databrick-training/`
> EXISTS (scripts/{submit_job.py, setup_cluster.sh, build_wheels.sh}, config/,
> notebooks/; README: "runs data prep pipeline (Stages 1-4)"). Deferral is now
> about WIRING, not existence: (a) this skill's verbs are not yet mapped to the
> repo's scripts, and (b) the job-based ladder below only works on jobs-capable
> hosts (WellDoc/CDHAI) — policy-locked USER_ISOLATION clusters (REACH) forbid
> jobs entirely and need the inline-exec pattern instead (learn-databricks
> Lesson 15; ../../haipipe-task/ref/databricks-execution.md). The `/haipipe-end`
> umbrella's no-args dashboard skips this skill while deferred.

  Verb axis:        dashboard | develop | test | monitor | teardown | review

  Stage flag:       --stage system   (local Python, no cluster — fastest)
                    --stage cluster  (Databricks all-purpose / job cluster)
                    --stage job      (managed Databricks Job — default for `develop`
                                      on jobs-capable hosts ONLY; on USER_ISOLATION
                                      clusters use inline exec, Lesson 15)

---

Commands (planned shape)
-------------------------

```
/haipipe-end-develop-databricks                                 -> dashboard: jobs + UC models
/haipipe-end-develop-databricks dashboard                       -> same
/haipipe-end-develop-databricks develop <config.yaml>           -> submit Databricks Job
/haipipe-end-develop-databricks test <config.yaml>              -> local-system test (no cluster)
/haipipe-end-develop-databricks test <config.yaml> --stage cluster -> attached-cluster smoke
/haipipe-end-develop-databricks monitor <run_id>                -> tail Job run logs
/haipipe-end-develop-databricks teardown <run_id>               -> cancel Job, optional UC version cleanup
/haipipe-end-develop-databricks review <run_id_or_uc_uri>       -> audit Job run / UC model version
```

---

Dispatch Table (planned)
-------------------------

```
Verb        Ref file(s)                              Backing platform script (when wired)
----------- ---------------------------------------- -------------------------------------
dashboard   ref/concepts.md                          (none — list Jobs + UC models via databricks CLI)
develop     ref/concepts.md +                        platforms/platform-databrick-training/scripts/
            ../haipipe-end/ref/            run_training_job/run_databricks_job.py  (TBD)
              0-overview.md
test        ref/concepts.md                          --stage system:  run_train_local_system.py (TBD)
                                                     --stage cluster: databricks notebook run (TBD)
monitor     ref/concepts.md                          databricks runs get / databricks runs get-output
teardown    ref/concepts.md                          databricks runs cancel + optional UC delete
review      ref/concepts.md                          databricks runs get + UC model description
```

---

Step-by-Step Protocol (deferred — to be implemented)
------------------------------------------------------

Step 0: Read `ref/concepts.md` for Databricks training conventions
        (Unity Catalog vs workspace registry, cluster spec, job parameters,
        wheel-vs-notebook task choice, MLflow integration).

Step 1: Parse args.
Same shape as `-develop-sagemaker`.

Step 2: Verify Databricks context:
          - Workspace URL + token (env or `databricks configure`)
          - Cluster spec resolvable (or job cluster definition supplied)
          - Unity Catalog target schema exists (else workspace MLflow)

Step 3: Submit the Job (or skip to local-system test for `test --stage system`).

Step 4: Emit the structured tail:

```
status:    ok | blocked | failed
summary:   2-3 sentences on the develop / test / etc.
artifacts: [Job run id, UC model URI, Endpoint_Set path under 6-EndpointStore/]
next:      suggested next command
```

---

Target Scope (planned)
-----------------------

Owns:
  - Databricks Job submission (notebook or wheel task)
  - Cluster lifecycle for the training job
  - MLflow tracking + Unity Catalog registration
  - Local-system test of the same training entry point
  - Endpoint_Set export from the trained model

Does NOT own:
  - Endpoint_Set CONTENT — owned by `/haipipe-end-endpointset` and per-Fn-type
    specialists.
  - Inference / serving — see `-deploy-databricks` (which consumes the UC
    model URI this skill produces).
  - Model class / Tuner / Instance code — see `/haipipe-nn`.

---

Why deferred
-------------

The `platforms/platform-databrick-training/` repo doesn't exist yet.
When it does, the expected pattern is the same 3-stage testing ladder used for SageMaker:

```
local-system  →  attached-cluster  →  managed-Job
```

with the final stage equivalent to SageMaker's RegisterModel (UC version registration via `mlflow.set_registry_uri("databricks-uc")`).

Until that repo lands, the umbrella surfaces this skill in routing-axis listings but reports `status: deferred` if invoked, with a pointer to `-develop-sagemaker` as the active alternative.
