---
name: haipipe-end-databricks
description: "Databricks Model Serving target specialist for haipipe-end. Wraps an Endpoint_Set into MLflow pyfunc + Unity Catalog model, deploys to Databricks Model Serving, runs live smoke tests, monitors, and tears down. Reads Endpoint_Sets produced by haipipe-end-endpointset; never modifies them. Called by /haipipe-end orchestrator when target is databricks."
argument-hint: [function] [endpoint_set_or_id] [args...]
allowed-tools: Bash, Read, Write, Edit, Grep, Glob
---

Skill: haipipe-end-databricks
==============================

Databricks Model Serving deployment specialist. Consumes an Endpoint_Set
built by `haipipe-end-endpointset`, registers it as an MLflow pyfunc in
Unity Catalog, deploys to Databricks Model Serving, tests live, and cleans up.

> Status: scaffolded. Procedures below are placeholders to be filled with
> the project's actual Databricks conventions (workspace URL, catalog/schema
> names, serving endpoint config).

  Function axis:  dashboard | deploy | test | monitor | teardown | review

---

Commands
--------

```
/haipipe-end-databricks                              -> dashboard: Databricks serving endpoints
/haipipe-end-databricks dashboard                    -> same
/haipipe-end-databricks deploy <endpoint_set>        -> register + deploy to Databricks
/haipipe-end-databricks test <endpoint_id>           -> hit live serving endpoint
/haipipe-end-databricks monitor <endpoint_id>        -> serving logs + invocation metrics
/haipipe-end-databricks teardown <endpoint_id>       -> stop endpoint, archive model version
/haipipe-end-databricks review <endpoint_id>         -> audit serving config + permissions
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

Step 0: Read `ref/concepts.md` for Databricks-specific conventions.

Step 1: Parse args. Required arg per function:
          deploy: <endpoint_set_name>
          test/monitor/teardown/review: <serving_endpoint_id>

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
  2. Wrap `fn_endpoint/` + ModelInstance into an `mlflow.pyfunc` model.
  3. Log model to MLflow tracking; register into Unity Catalog
     (`<catalog>.<schema>.<endpoint_set>`).
  4. Promote new version through configured stage transitions.
  5. Create or update Databricks Model Serving endpoint pointing at the
     registered model version.
  6. Wait for endpoint to reach READY.
  7. Run 1-payload smoke invocation; verify response.
  8. Record endpoint URL + model version in the project's deploy log.

Test, Monitor, Teardown, Review:
  See `ref/concepts.md` for the Databricks-specific commands the project uses
  (`databricks` CLI or REST API patterns).

---

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
