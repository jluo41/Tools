---
name: haipipe-end-develop-local
description: "Local develop specialist for haipipe-end. Thin wrapper that runs Stage 5 training on the local machine and produces an Endpoint_Set under 6-EndpointStore/. For dev iteration, smoke tests, and DIY builds without managed pipelines. Mostly delegates to /haipipe-nn modelset for the actual training; this skill exists for symmetry with -deploy-local and to give the haipipe-end umbrella a uniform develop axis. Reads from /haipipe-nn output; writes Endpoint_Sets that haipipe-end-endpointset and the deploy specialists consume."
argument-hint: [verb] [config_or_modelset] [args...]
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
---

Skill: haipipe-end-develop-local
=================================

Local development specialist. Builds an Endpoint_Set on the local machine
without any managed training pipeline. Most heavy lifting is done by
`/haipipe-nn modelset` — this skill is a thin orchestration layer that:

  1. Invokes the project's local ModelSet pipeline.
  2. Packages the resulting trained model into an Endpoint_Set under
     `_WorkSpace/6-EndpointStore/<endpoint_set>/` via the standard
     `haipipe-end-endpointset package` flow.

It exists for symmetry with `-deploy-local` and to give `/haipipe-end` a
uniform develop axis (sagemaker / databricks / local). When local develop
is sufficient, prefer this skill over `-develop-sagemaker` for fast iteration.

  Verb axis:        dashboard | develop | test | monitor | teardown | review

---

Commands
--------

```
/haipipe-end-develop-local                                 -> dashboard: locally-built endpoint sets
/haipipe-end-develop-local dashboard                       -> same
/haipipe-end-develop-local develop <modelset_or_config>    -> full local build → Endpoint_Set
/haipipe-end-develop-local test <modelset_or_config>       -> dry-run / smoke (no Endpoint_Set written)
/haipipe-end-develop-local monitor <run_id>                -> tail local logs
/haipipe-end-develop-local teardown <run_id>               -> stop background run, optional cleanup
/haipipe-end-develop-local review <endpoint_set>           -> audit a locally-built Endpoint_Set
```

`<run_id>` for local runs is a generated short id; the dashboard lists the
local develop registry.

---

Dispatch Table
--------------

```
Verb        Ref                                   Backing call
----------- ------------------------------------- ----------------------------------------
dashboard   ref/concepts.md                       (none — local develop registry)
develop     ref/concepts.md                       Skill("haipipe-nn", "modelset run <args>")
            ../haipipe-end/ref/0-overview.md      then Skill("haipipe-end-endpointset",
                                                              "package <args>")
test        ref/concepts.md                       Skill("haipipe-nn", "modelset test <args>")
monitor     ref/concepts.md                       tail local log file
teardown    ref/concepts.md                       kill pid + optional rm of intermediate dirs
review      ref/concepts.md                       Skill("haipipe-end-endpointset",
                                                              "review <endpoint_set>")
```

This skill **delegates** rather than reimplementing. The "local develop"
flow is just `nn modelset run` followed by `endpointset package` — both are
already first-class skills, so this wrapper just sequences them.

---

Step-by-Step Protocol
----------------------

Step 0: Read `ref/concepts.md` for local develop conventions (pid file
        layout, log paths, registry location).

Step 1: Parse args. Required arg per verb:
          develop / test:           <modelset_or_config>
          monitor / teardown:       <run_id>
          review:                   <endpoint_set_name>

Step 2: For `develop`:
          a) Dispatch:  Skill("haipipe-nn", args="modelset run <modelset>")
             Capture status / artifacts. If status != ok, abort and return.
          b) Dispatch:  Skill("haipipe-end-endpointset",
                              args="package <endpoint_set_args>")
             Capture status / artifacts.
          c) Record (run_id, modelset, endpoint_set_path) in the local registry.

        For `test`:
          Dispatch:    Skill("haipipe-nn", args="modelset test <modelset>")
          (No Endpoint_Set written — fast iteration.)

        For `review`:
          Dispatch:    Skill("haipipe-end-endpointset", args="review <endpoint_set>")

Step 3: Emit the structured tail (composing the chained tails):

```
status:    ok | blocked | failed   (failed if either delegate failed)
summary:   2-3 sentences; mention which step succeeded / failed
artifacts: [run_id, modelset run output, endpoint_set path]
next:      suggested next command (typically /haipipe-end deploy local <endpoint_set>)
```

---

Why this skill is thin
-----------------------

The actual training work lives in `/haipipe-nn` and the actual packaging
lives in `/haipipe-end-endpointset`. This skill exists for two reasons:

  1. **Symmetry.** `-deploy-local` exists alongside `-deploy-sagemaker /
     -databricks / -mlflow`. For the `-develop-` axis to be uniform,
     `-develop-local` must also exist.
  2. **Uniform routing.** `/haipipe-end develop sagemaker <args>` and
     `/haipipe-end develop local <args>` should both work without the
     orchestrator special-casing local. Having this specialist gives the
     develop dispatch table a uniform shape.

If you find yourself adding non-trivial local-only logic here, that's a
signal it probably belongs in `/haipipe-nn` or `/haipipe-end-endpointset`
instead. Keep this skill thin.

---

Target Scope
-------------

Owns:
  - The `nn modelset` → `endpointset package` sequencing for local builds
  - Local develop registry (which builds were produced when, where they live)
  - Local pid / log management for background develop runs

Does NOT own:
  - ANY actual training logic — that's `/haipipe-nn modelset`.
  - ANY actual Endpoint_Set packaging logic — that's `/haipipe-end-endpointset`.
  - Cloud / managed training — see `-develop-sagemaker` (or future
    `-develop-databricks`).

If a develop fails because of a training issue, escalate to `/haipipe-nn
modelset review`. If it fails because of a packaging issue, escalate to
`/haipipe-end-endpointset review`. This skill should not patch either.
