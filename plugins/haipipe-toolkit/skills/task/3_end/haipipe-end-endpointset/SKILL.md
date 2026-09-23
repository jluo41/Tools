---
name: haipipe-end-endpointset
description: "Endpoint_Set artifact-as-whole specialist: target-agnostic operations on the deployable artifact -- package from Stage 5 to 6, local inference smoke test, structural review, and dashboard. Per-Fn-type design/review lives in haipipe-end specialists; deployment lives in haipipe-end-deploy specialists."
allowed-tools: Bash, Read, Write, Edit, Grep, Glob
metadata:
  version: "0.2.1"
  last_updated: "2026-09-13"
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

Skill: haipipe-end-endpointset
===============================

Stage 6 **artifact-as-whole** specialist.
Handles operations on the Endpoint_Set as a unit — packaging, local smoke test, structural review, dashboard.
Target-agnostic: produces / inspects the artifact; deploying it is the deploy specialists' job.

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

The umbrella's `ref/0-overview.md` (cross-cutting Stage 6 architecture + inference pipeline + YAML) is mandatory context for every verb.

---

Step-by-Step Protocol
----------------------

Step 0: Read `../haipipe-end/ref/0-overview.md`.
Mandatory.
         Contains the Endpoint_Set layout + inference pipeline + YAML conventions.

Step 1: Parse args.
Verb vocabulary: dashboard / package / test / profile / review.

Step 2: Read the relevant fn doc per the dispatch table.

Step 3: Execute the procedure scoped to the WHOLE artifact (not any
         single Fn-type). For per-Fn-type review, route the user to the
         relevant sibling specialist instead.

Step 4: Emit the structured tail (orchestrator parses):

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
  - endpoint fn_develop builders (artifact-level; legacy: `code-dev/1-PIPELINE/6-Endpoint-WorkSpace/`)
  - `_WorkSpace/6-EndpointStore/{endpoint_name}/` packaged Endpoint_Sets
  - Local `inference()` smoke tests (artifact-level)
  - Structural review of the artifact as a whole

Does NOT own:
  - **Per-Fn-type design / review** — see `/haipipe-end-{meta,trig,post,src2input,input2src}`
  - **Target-specific packaging** (model.tar.gz, MLflow pyfunc, Flask app)
    — see `/haipipe-end-deploy-*`
  - Credentials / IAM / workspace auth — owned by deploy specialists

---

Lessons learned (MIMIC-IV endpoint session)
---------------------------------------------

### Step 5b reproducibility check

`c_endpoint_nb.py` step 5b compares endpoint predictions against training `prediction_results.json`.
Warns on mismatch (does not block).
This catches roundtrip data loss early — before the artifact ships to a deploy specialist.

### D-prefix exclusion

`Src2InputFn` and `extract_example_from_source` now skip D-prefix tables (`DRGCode`, `DLabItems`, `DIcdDiagnoses`, `DIcdProcedures`, `DHcpcs`, `DItems`).
This reduced `.tar.gz` from 160 MB to 14 MB.

### Three-level Src2InputFn / Input2SrcFn roundtrip enforcement

1. **Design time:** builder roundtrip test (`f1_roundtrip_test` in the builder folder).
2. **Packaging time:** step 5b in `c_endpoint_nb.py`.
3. **Skill docs:** required in `haipipe-end-src2input` + `haipipe-end-input2src`
   SKILL.md.


Hand-off Contract (Endpoint_Set → deploy specialists)
------------------------------------------------------

Each Endpoint_Set in `_WorkSpace/6-EndpointStore/{endpoint_name}/` is the SINGLE artifact that flows downstream:

```
_WorkSpace/6-EndpointStore/{endpoint_name}/
├── model/                     trained ModelInstance snapshot
├── code/                      codebase snapshot (haipipe, hainn, haifn/fn_endpoint — 5 Fn-types + fn_example helper dir)
├── examples/                  test examples + payload.json
├── meta.json                  MetaFn output (name mappings + metadata)
└── manifest.json              config + lineage — everything a deploy specialist needs
```

When SourceFn/Input2SrcFn uses external data, the artifact also contains an
immutable `external/` snapshot. `manifest.json` records its release, checksums,
and Source vector schema/order versions. Packaging fails when those identities
are absent or a parity fixture cannot reproduce the training ProcessDF contract.
Under the asset model (`../../1_data/haipipe-data-external/ref/asset-model.md`)
`external/` holds only the asset versions the SourceFn's lock names (plus
their `asset.yaml`), never a whole release and never `@raw/`; `manifest.json`
records the lock name, each asset's version and sha256, and which assets
serve from a live provider (`providers.serve`) with their `max_staleness`.
A hard-coded list of external files inside the endpoint code is legacy.
(Canonical layout: `../haipipe-end/ref/0-overview.md` "Stage 6 (output)" — do not restate elsewhere.)

Deploy specialists (`-deploy-*`) READ this artifact and never modify it.
If a deploy fails because of a missing/malformed field here, the fix lives in this skill (or a per-Fn-type sibling), not in the deploy skill.

---

Job lifecycle (develop → package)
---------------------------------

New endpoint work uses canonical BJTR. A development Job owns one Task per Fn
or gate; a packaging Job owns the Endpoint_Set task:

```
tasks/bNN_<endpoint_block>/
├── j01_endpoint_functions_<qualifier>/
│   ├── t01_metafn_<qualifier>/
│   ├── t02_trigfn_<qualifier>/
│   ├── t03_postfn_<qualifier>/
│   ├── t04_src2inputfn_<qualifier>/
│   ├── t05_input2srcfn_<qualifier>/
│   └── t06_source_roundtrip_<qualifier>/
└── j02_endpoint_package_<qualifier>/
    └── t01_endpoint_set_<qualifier>/
        ├── scripts/<worker>.py
        ├── scripts/config/r01_base.yaml
        ├── runs/r01_base.sh
        ├── results/r01_base/runtime.yaml
        └── notebooks/r01_base.ipynb
```

**Flow:** every required development Task passes → package Task → deploy.
Legacy flat/C-series trees remain readable but are never scaffolded.
Step 5b in `c_endpoint_nb.py` (reproducibility check) is the runtime safety net that catches any remaining roundtrip issues.

Start new builders from templates in `code/scripts/haibuilder/6-endpoint/`.
