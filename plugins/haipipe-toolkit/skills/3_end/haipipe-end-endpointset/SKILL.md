---
name: haipipe-end-endpointset
description: "Endpoint_Set artifact-as-whole specialist. Owns target-agnostic operations on the deployable artifact: package (Stage 5 → 6), local inference() smoke test, structural review, dashboard. Per-Fn-type design/review lives in sibling skills (haipipe-end-{meta,trig,post,src2input,input2src}); deployment lives in haipipe-end-deploy-*. Called by /haipipe-end orchestrator when the request is about the artifact itself."
argument-hint: "[verb] [args...]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob
metadata:
  version: "1.1.0"
  last_updated: "2026-06-01"
  summary: "Endpoint_Set artifact-as-whole specialist."
  changelog:
    - "1.0.0 (2026-05-31): baseline metadata added."
    - "1.1.0 (2026-06-01): added `profile` verb (latency breakdown + per-arm decomposition; fn-3-profile.md). Durable/reproducible version of the same profile lives in C_task /haipipe-task-for-inference."
---

Skill: haipipe-end-endpointset
===============================

Stage 6 **artifact-as-whole** specialist. Handles operations on the
Endpoint_Set as a unit — packaging, local smoke test, structural review,
dashboard. Target-agnostic: produces / inspects the artifact; deploying
it is the deploy specialists' job.

  Verb axis:  package | test | profile | review | dashboard

  `test`    = does inference WORK (smoke test, correctness)
  `profile` = where does inference TIME go (latency breakdown + per-arm decomposition)

  This skill does NOT cover per-Fn-type design / review. For that, use:
    /haipipe-end-meta        /haipipe-end-trig        /haipipe-end-post
    /haipipe-end-src2input   /haipipe-end-input2src

---

Commands
--------

```
/haipipe-end-endpointset                       -> dashboard: 6-EndpointStore status
/haipipe-end-endpointset dashboard             -> same
/haipipe-end-endpointset package               -> run Endpoint_Pipeline (Stage 5 -> 6)
/haipipe-end-endpointset test [payload_path]   -> local inference() smoke test (does it work?)
/haipipe-end-endpointset profile [endpoint]    -> latency breakdown (where does the time go?)
/haipipe-end-endpointset review                -> structural review of the whole artifact
```

---

Dispatch Table
---------------

```
Verb       Reads
---------- ------------------------------------------------------------
dashboard  ../haipipe-end/ref/0-overview.md  +  fn/fn-0-dashboard.md
package    ../haipipe-end/ref/0-overview.md  +  fn/fn-1-package.md
test       ../haipipe-end/ref/0-overview.md  +  fn/fn-2-test.md
profile    ../haipipe-end/ref/0-overview.md  +  fn/fn-3-profile.md
review     ../haipipe-end/ref/0-overview.md  +  fn/fn-review.md
```

The umbrella's `ref/0-overview.md` (cross-cutting Stage 6 architecture +
inference pipeline + YAML) is mandatory context for every verb.

---

Step-by-Step Protocol
----------------------

Step 0:  Read `../haipipe-end/ref/0-overview.md`. Mandatory.
         Contains the Endpoint_Set layout + inference pipeline + YAML conventions.

Step 1:  Parse args. Verb vocabulary: dashboard / package / test / profile / review.

Step 2:  Read the relevant fn doc per the dispatch table.

Step 3:  Execute the procedure scoped to the WHOLE artifact (not any
         single Fn-type). For per-Fn-type review, route the user to the
         relevant sibling specialist instead.

Step 4:  Emit the structured tail (orchestrator parses):

```
status:    ok | blocked | failed
summary:   2-3 sentences (artifact built / tested / reviewed)
artifacts: [Endpoint_Set path, test payload, profiling output]
next:      suggested next command — typically a target deploy:
             /haipipe-end deploy sagemaker <Endpoint_Set>
```

---

Artifact Scope
---------------

Owns:
  - `code/haifn/fn_endpoint/` packaging (running the pipeline)
  - `code-dev/1-PIPELINE/6-Endpoint-WorkSpace/` builders (artifact-level)
  - `_WorkSpace/6-EndpointStore/Endpoint-*/` packaged Endpoint_Sets
  - Local `inference()` smoke tests (artifact-level)
  - Structural review of the artifact as a whole

Does NOT own:
  - **Per-Fn-type design / review** — see `/haipipe-end-{meta,trig,post,src2input,input2src}`
  - **Target-specific packaging** (model.tar.gz, MLflow pyfunc, Flask app)
    — see `/haipipe-end-deploy-*`
  - Credentials / IAM / workspace auth — owned by deploy specialists

---

Hand-off Contract (Endpoint_Set → deploy specialists)
------------------------------------------------------

Each Endpoint_Set in `_WorkSpace/6-EndpointStore/Endpoint-{name}/` is the
SINGLE artifact that flows downstream:

```
Endpoint-{name}/
├── meta.json                  configuration + model registry pointers
├── fn_endpoint/               compiled inference Fn code (5 Fn-types)
├── ModelInstance/             trained weights snapshot (or pointer)
└── manifest.yaml              everything a deploy specialist needs
```

Deploy specialists (`-deploy-*`) READ this artifact and never modify it.
If a deploy fails because of a missing/malformed field here, the fix
lives in this skill (or a per-Fn-type sibling), not in the deploy skill.

---

Task-folder lifecycle (00_develop → 01_package)
-------------------------------------------------

In the /haipipe-task convention, endpoint work lives under C-series groups:

```
examples/<project>/tasks/C01_endpoint_*/
├── 00_endpoint_set_fn_develop/         ← DEVELOP: build + test all Fns
│   ├── a1_build_metafn.py              ← each builder is its own run
│   ├── b1_build_trigfn.py
│   ├── c1_build_postfn.py
│   ├── d1_build_src2inputfn.py         ← roundtrip test with real data
│   ├── e1_build_input2srcfn.py         ← roundtrip test with real data
│   ├── e4_build_examplefn.py           ← tests with real model + AIData
│   ├── f1_roundtrip_test.py            ← prediction-level verification
│   ├── configs/run_*.yaml              ← one config per builder
│   ├── runs/run_*.sh                   ← one run script per builder
│   └── results/run_*/runtime.yaml      ← per-builder pass/fail
│
└── 01_endpoint_<name>/                 ← PACKAGE: Endpoint_Set + validate + .tar.gz
    ├── 01_endpoint_<name>.py           ← exact copy of c_endpoint_nb.py
    ├── configs/run_endpoint_<name>.yaml
    └── runs/run_endpoint_<name>.sh
```

**Flow:** develop (00_) → package (01_) → deploy.

The `00_develop` task must pass all 7 runs before the `01_package` task
is executed. Step 5b in `c_endpoint_nb.py` (reproducibility check) is
the runtime safety net that catches any remaining roundtrip issues.

Start new builders from templates in `code/scripts/haibuilder/6-endpoint/`.
