---
name: develop-local
part-of: hai-end
description: "Local develop specialist for hai-end: runs Stage 5 training on the local machine and produces an Endpoint_Set under 6-EndpointStore/, for dev iteration, smoke tests, and DIY builds. Mostly delegates to /hai-nn modelset for training; exists for symmetry with hai-end deploy local and a uniform develop axis. Reads /hai-nn output; writes Endpoint_Sets that endpointset + deploy specialists consume."
argument-hint: "[verb] [config_or_modelset] [args...]"
metadata:
  version: "0.1.2"
  last_updated: "2026-10-25"
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

Skill: hai-end develop local
=================================

Local development specialist.
Builds an Endpoint_Set on the local machine without any managed training pipeline.
Most heavy lifting is done by `/hai-nn modelset` — this skill is a thin orchestration layer that:

  1. Invokes the project's local ModelSet pipeline.
  2. Packages the resulting trained model into an Endpoint_Set under
     `_WorkSpace/6-EndpointStore/<endpoint_set>/` via the standard
     `hai-end endpointset package` flow.

It exists for symmetry with `hai-end deploy local` and to give `/hai-end` a uniform develop axis (sagemaker / databricks / local).
When local develop is sufficient, prefer this skill over `hai-end develop sagemaker` for fast iteration.

  Verb axis:        dashboard | develop | test | monitor | teardown | review

---

Commands
--------

```
/hai-end develop local                                 -> dashboard: locally-built endpoint sets
/hai-end develop local dashboard                       -> same
/hai-end develop local develop <modelset_or_config>    -> full local build → Endpoint_Set
/hai-end develop local test <modelset_or_config>       -> dry-run / smoke (no Endpoint_Set written)
/hai-end develop local monitor <run_id>                -> tail local logs
/hai-end develop local teardown <run_id>               -> stop background run, optional cleanup
/hai-end develop local review <endpoint_set>           -> audit a locally-built Endpoint_Set
```

`<run_id>` for local runs is a generated short id; the dashboard lists the local develop registry.

---

Dispatch Table
--------------

```
Verb        Ref                                   Backing call
----------- ------------------------------------- ----------------------------------------
dashboard   ref/concepts.md                       (none — local develop registry)
develop     ref/concepts.md                       Skill("hai-nn", "modelset run <args>")
            ../../ref/0-overview.md      then read ../endpointset/PART.md,
                                                              args "package <args>"
test        ref/concepts.md                       Skill("hai-nn", "modelset test <args>")
monitor     ref/concepts.md                       tail local log file
teardown    ref/concepts.md                       kill pid + optional rm of intermediate dirs
review      ref/concepts.md                       read ../endpointset/PART.md,
                                                              args "review <endpoint_set>"
```

This skill **delegates** rather than reimplementing.
The "local develop" flow is just `nn modelset run` followed by `endpointset package` — both are already first-class skills, so this wrapper just sequences them.

---

Step-by-Step Protocol
----------------------

Step 0: Read `ref/concepts.md` for local develop conventions (pid file
        layout, log paths, registry location).

Step 1: Parse args.
Required arg per verb:
          develop / test:           <modelset_or_config>
          monitor / teardown:       <run_id>
          review:                   <endpoint_set_name>

Step 2: For `develop`:
          a) Dispatch:  Skill("hai-nn", args="modelset run <modelset>")
             Capture status / artifacts. If status != ok, abort and return.
          b) Dispatch:  Read ../endpointset/PART.md, args "package <endpoint_set_args>"
             Capture status / artifacts.
          c) Record (run_id, modelset, endpoint_set_path) in the local registry.

        For `test`:
          Dispatch:    Skill("hai-nn", args="modelset test <modelset>")
          (No Endpoint_Set written — fast iteration.)

        For `review`:
          Dispatch:    Read ../endpointset/PART.md, args "review <endpoint_set>"

Step 3: Emit the structured tail (composing the chained tails):

```
status:    ok | blocked | failed   (failed if either delegate failed)
summary:   2-3 sentences; mention which step succeeded / failed
artifacts: [run_id, modelset run output, endpoint_set path]
next:      suggested next command (typically /hai-end deploy local <endpoint_set>)
```

---

Why this skill is thin
-----------------------

The actual training work lives in `/hai-nn` and the actual packaging lives in `/hai-end endpointset`.
This skill exists for two reasons:

  1. **Symmetry.** `hai-end deploy local` exists alongside `hai-end deploy sagemaker /
     -databricks / -mlflow`. For the `-develop-` axis to be uniform,
     `hai-end develop local` must also exist.
  2. **Uniform routing.** `/hai-end develop sagemaker <args>` and
     `/hai-end develop local <args>` should both work without the
     orchestrator special-casing local. Having this specialist gives the
     develop dispatch table a uniform shape.

If you find yourself adding non-trivial local-only logic here, that's a signal it probably belongs in `/hai-nn` or `/hai-end endpointset` instead.
Keep this skill thin.

---

Target Scope
-------------

Owns:
  - The `nn modelset` → `endpointset package` sequencing for local builds
  - Local develop registry (which builds were produced when, where they live)
  - Local pid / log management for background develop runs

Does NOT own:
  - ANY actual training logic — that's `/hai-nn modelset`.
  - ANY actual Endpoint_Set packaging logic — that's `/hai-end endpointset`.
  - Cloud / managed training — see `hai-end develop sagemaker` (or future
    `hai-end develop databricks`).

If a develop fails because of a training issue, escalate to `/hai-nn modelset review`.
If it fails because of a packaging issue, escalate to `/hai-end endpointset review`.
This skill should not patch either.
