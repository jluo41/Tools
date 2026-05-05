---
name: haipipe-end-deploy-local
description: "Local self-hosted deploy specialist for haipipe-end. Wraps an Endpoint_Set into a local HTTP server — Flask (default), FastAPI, or local Docker container. For dev, integration testing, demos, and DIY deployments. Backed in part by platform-sagemaker-inference/scripts/build_endpoint/run_endpoint_{system,docker}.py for the Flask + Docker testing ladder. Reads Endpoint_Sets produced by haipipe-end-endpointset; never modifies them. Called by /haipipe-end orchestrator when deploy target is local / flask / fastapi / localhost."
argument-hint: [verb] [endpoint_set_or_id] [args...]
allowed-tools: Bash, Read, Write, Edit, Grep, Glob
---

Skill: haipipe-end-deploy-local
================================

Local / self-hosted HTTP deployment specialist. Wraps an Endpoint_Set
into a small HTTP server running on the local machine. "Local" is the
deployment target; the framework (Flask / FastAPI) and the optional
Docker wrap are implementation choices.

> Status: scaffolded. Procedures below are placeholders to be wired
> through `platform-sagemaker-inference/scripts/build_endpoint/run_endpoint_{system,docker}.py`
> (the Flask + Docker testing scripts that already exist in this project)
> when the project picks a stable local-deploy convention.

  Verb axis:        dashboard | deploy | test | monitor | teardown | review

  Framework flag:   --framework flask  (default)
                    --framework fastapi
                    --with-docker      (wrap in a local Docker container instead
                                         of running directly with the framework)

---

Commands
--------

```
/haipipe-end-deploy-local                                  -> dashboard: locally-running servers
/haipipe-end-deploy-local dashboard                        -> same
/haipipe-end-deploy-local deploy <endpoint_set>            -> generate app, start Flask on :5000
/haipipe-end-deploy-local deploy <es> --framework fastapi  -> use FastAPI instead of Flask
/haipipe-end-deploy-local deploy <es> --with-docker        -> run inside a local Docker container
/haipipe-end-deploy-local deploy <es> --port 8080          -> custom port
/haipipe-end-deploy-local test <endpoint_id>               -> POST a payload to local server
/haipipe-end-deploy-local monitor <endpoint_id>            -> tail server / container logs
/haipipe-end-deploy-local teardown <endpoint_id>           -> stop server (kill pid or `docker stop`)
/haipipe-end-deploy-local review <endpoint_id>             -> audit generated app code
```

`<endpoint_id>` for a local server is the `(endpoint_set_name, port)` tuple
or a generated short id; the dashboard lists the local registry.

---

Dispatch Table
--------------

```
Verb        Ref                                       Backing platform script (when wired)
----------- ----------------------------------------- -------------------------------------
dashboard   ref/concepts.md                           (none — local registry)
deploy      ref/concepts.md
            ../haipipe-end/ref/0-overview.md
              flask:        platform-sagemaker-inference/scripts/build_endpoint/run_endpoint_system.py
              with-docker:  platform-sagemaker-inference/scripts/build_endpoint/run_endpoint_docker.py
              fastapi:      project-specific (TBD)
test        ref/concepts.md                           POST a JSON payload to localhost:port/invocations
monitor     ref/concepts.md                           tail logs (`--logs` flag or `docker logs`)
teardown    ref/concepts.md                           `--stop` flag or `docker stop`
review      ref/concepts.md                           Read of generated app + Dockerfile
```

---

Step-by-Step Protocol
----------------------

Step 0:  Read `ref/concepts.md` for local server conventions (port allocation,
         pid-file layout, log paths, framework boilerplate).

Step 1:  Parse args. Required arg per verb:
           deploy: <endpoint_set_name> [--framework flask|fastapi]
                                       [--with-docker] [--port N] [--bg]
           test/monitor/teardown/review: <endpoint_id>

Step 2:  Choose backing path based on framework + Docker flags. For Flask
         without Docker, defer to `run_endpoint_system.py`. For local Docker,
         defer to `run_endpoint_docker.py`. For FastAPI, project-specific.

Step 3:  Execute the procedure.

Step 4:  Emit the structured tail:

```
status:    ok | blocked | failed
summary:   2-3 sentences on the deploy / test / etc.
artifacts: [generated app path, pid, port, base URL, container id]
next:      suggested next command
```

---

Procedures (placeholder — fill in once local-deploy convention settles)
------------------------------------------------------------------------

Deploy (Flask, default):
  1. Read Endpoint_Set at `_WorkSpace/6-EndpointStore/<endpoint_set>/`.
  2. Defer to `python platform-sagemaker-inference/scripts/build_endpoint/run_endpoint_system.py
     --endpoint-path <path> --test` for the Flask path (it already does
     env setup, port :5000, /ping + /invocations smoke).
  3. Record (endpoint_set, port=5000, pid) in the local registry.

Deploy (Docker):
  1. Read Endpoint_Set at `_WorkSpace/6-EndpointStore/<endpoint_set>/`.
  2. Build (or reuse) a local Docker image via the SageMaker Docker scripts
     (`build_docker_inference.py --image docker-inference-lite --variant lite`).
  3. Defer to `python platform-sagemaker-inference/scripts/build_endpoint/run_endpoint_docker.py
     --endpoint-path <path> --image docker-inference-lite --test` for the
     Docker path (port :8080).
  4. Record (endpoint_set, port=8080, container_id) in the local registry.

Deploy (FastAPI):
  1. Read Endpoint_Set at `_WorkSpace/6-EndpointStore/<endpoint_set>/`.
  2. Run `scripts/serve_local.py` — generic FastAPI wrapper that calls
     `Endpoint_Set.inference()` behind `POST /invocations`. Routes:
       GET  /health       — liveness + endpoint_loaded flag
       GET  /meta         — mirrors MetaFn metadata_response.body
       POST /invocations  — accepts the Endpoint_Set's documented payload
                            (typically `dataframe_records` per Input2SrcFn)
  3. Invocation:
       ENDPOINT_PATH=_WorkSpace/6-EndpointStore/<endpoint_set> \
       PORT=8765 \
           python scripts/serve_local.py
  4. Smoke-test with `haipipe-subject-inference` (per-subject test) or
     curl `POST http://127.0.0.1:8765/invocations` with a payload.json
     pulled from `<endpoint_set>/inference/`.
  5. Record (endpoint_set, port=8765, pid) in the local registry.

  Notes:
   - The script is intentionally endpoint-agnostic — same script serves
     any Endpoint_Set produced by `haipipe-end-endpointset`.
   - Inference errors propagate as HTTP 500 (no internal fallback);
     incomplete endpoints (e.g. missing `prefn_config.json`) surface as
     500 from `Endpoint_Set.inference()` so the caller sees them.

Test, Monitor, Teardown, Review:
  See `ref/concepts.md` for log paths, pid file conventions, port allocation,
  and the `--logs` / `--stop` / `--cleanup` flags on the backing scripts.

---

Target Scope
-------------

Owns:
  - Local app generation (Flask, FastAPI, optional Docker wrap)
  - Local process management (start, pid file, port allocation)
  - Local server registry (which apps are running where)
  - Live smoke tests against localhost
  - Log tailing / shutdown of local instances

Does NOT own:
  - Endpoint_Set content — read-only input from `/haipipe-end-endpointset`
  - Production-grade serving infra — for managed serving see `-deploy-sagemaker`
    or `-deploy-databricks`
  - SageMaker / ECR / cloud auth — those are `-deploy-sagemaker`'s concerns.
    This skill MAY shell out to `platform-sagemaker-inference/scripts/build_endpoint/`
    for the Flask + local-Docker paths, since those scripts work fine without
    any cloud creds.

If a deploy fails because of an Endpoint_Set issue, escalate to
`/haipipe-end-endpointset review`.
