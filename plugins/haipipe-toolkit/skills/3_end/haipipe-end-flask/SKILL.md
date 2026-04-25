---
name: haipipe-end-flask
description: "Local self-hosted HTTP target specialist for haipipe-end. Wraps an Endpoint_Set into a Flask (or FastAPI) app and runs it locally or in a container. Useful for development, integration testing, and DIY deployments. Reads Endpoint_Sets produced by haipipe-end-endpointset; never modifies them. Called by /haipipe-end orchestrator when target is flask / fastapi / local server."
argument-hint: [function] [endpoint_set_or_id] [args...]
allowed-tools: Bash, Read, Write, Edit, Grep, Glob
---

Skill: haipipe-end-flask
=========================

Local / self-hosted HTTP deployment specialist. Wraps an Endpoint_Set into
a small Flask (or FastAPI) HTTP server. Best for local development,
integration testing, and lightweight self-hosted deployments.

> Status: scaffolded. The Flask app shape and port conventions below are
> placeholders for the project to settle on.

  Function axis:  dashboard | deploy | test | monitor | teardown | review

  Sub-target:     `flask` (default) or `fastapi`. Both share most of the
                  procedure; only the framework boilerplate differs.

---

Commands
--------

```
/haipipe-end-flask                                  -> dashboard: locally-running servers
/haipipe-end-flask dashboard                        -> same
/haipipe-end-flask deploy <endpoint_set> [--port N] -> generate app, start server
/haipipe-end-flask deploy --fastapi <endpoint_set>  -> use FastAPI instead of Flask
/haipipe-end-flask test <endpoint_id>               -> POST a payload to local server
/haipipe-end-flask monitor <endpoint_id>            -> tail server logs
/haipipe-end-flask teardown <endpoint_id>           -> stop server (kill pid)
/haipipe-end-flask review <endpoint_id>             -> audit generated app code
```

`<endpoint_id>` for a local server is the `(endpoint_set_name, port)` tuple
or a generated short id; the dashboard shows the registry.

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

Step 0: Read `ref/concepts.md` for Flask/FastAPI app conventions.

Step 1: Parse args. Required arg per function:
          deploy: <endpoint_set_name> [--fastapi] [--port N] [--bg]
          test/monitor/teardown/review: <endpoint_id>

Step 2: Choose framework. Default `flask`; `--fastapi` switches.

Step 3: Execute the function.

Step 4: Emit the structured tail:

```
status:    ok | blocked | failed
summary:   2-3 sentences on the deploy / test / etc.
artifacts: [generated app path, pid, port, base URL]
next:      suggested next command
```

---

Procedures (placeholder — fill from project conventions)
---------------------------------------------------------

Deploy:
  1. Read Endpoint_Set at `_WorkSpace/6-EndpointStore/<endpoint_set>/`.
  2. Generate `app.py` (Flask) or `app.py` (FastAPI) that:
     - Imports `fn_endpoint/inference()`.
     - Exposes `POST /invoke` accepting the Endpoint_Set's expected payload.
     - Exposes `GET /healthz`.
  3. Optionally generate a `Dockerfile` for containerized deployment.
  4. Start the server (foreground for dev, background with `&` + pid file
     for daemon mode).
  5. Smoke test against `/healthz`.
  6. Record endpoint_id (set+port) in the local registry.

Test, Monitor, Teardown, Review:
  See `ref/concepts.md` for log paths, pid file conventions, and reload
  patterns the project uses.

---

Target Scope
-------------

Owns:
  - Flask / FastAPI app boilerplate generation
  - Optional Dockerfile generation
  - Local process management (start, pid file, port allocation)
  - Local server registry (which apps are running where)
  - Live invocation smoke tests against localhost

Does NOT own:
  - Endpoint_Set content (read-only input from `/haipipe-end-endpointset`)
  - Production-grade serving infra — this is a dev / DIY target. For
    managed serving, use SageMaker, Databricks, or MLflow targets.

If a deploy fails because of an Endpoint_Set issue, escalate to
`/haipipe-end-endpointset review`.
