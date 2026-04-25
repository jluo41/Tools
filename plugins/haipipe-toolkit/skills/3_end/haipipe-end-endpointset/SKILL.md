---
name: haipipe-end-endpointset
description: "Endpoint_Set artifact specialist. Owns the target-agnostic lifecycle: package ModelInstance into Endpoint_Set, design inference functions (MetaFn / TrigFn / PostFn / Src2InputFn / Input2SrcFn), run local inference() smoke tests, review packaging. Called by /haipipe-end orchestrator when the request is about the artifact itself, not deployment to a specific target."
argument-hint: [function] [args...]
allowed-tools: Bash, Read, Write, Edit, Grep, Glob
---

Skill: haipipe-end-endpointset
===============================

Stage 6 artifact specialist. Owns the **Endpoint_Set** — the deployable
package built from a Stage 5 ModelInstance. Target-agnostic: this skill
produces the artifact; deployment to a specific target (SageMaker /
Databricks / Flask / MLflow) belongs to the corresponding target sibling.

  Function axis:  dashboard | package | test | design | review

  Fn-type axis:   meta | trig | post | src2input | input2src
                  (used by `design` to scope which inference Fn is being built)

---

Commands
--------

```
/haipipe-end-endpointset                       -> dashboard: 6-EndpointStore status
/haipipe-end-endpointset dashboard             -> same
/haipipe-end-endpointset package               -> run Endpoint_Pipeline (Stage 5 -> 6)
/haipipe-end-endpointset test [payload_path]   -> local inference() with profiling
/haipipe-end-endpointset design <fn-type>      -> build new inference Fn via builder
/haipipe-end-endpointset review [fn-type]      -> structural review of generated Fn files
/haipipe-end-endpointset 0-overview            -> architecture + inference pipeline + YAML
/haipipe-end-endpointset meta                  -> MetaFn ref
/haipipe-end-endpointset trig                  -> TrigFn ref
/haipipe-end-endpointset post                  -> PostFn ref
/haipipe-end-endpointset src2input             -> Src2InputFn ref
/haipipe-end-endpointset input2src             -> Input2SrcFn ref
```

---

Dispatch Table
--------------

```
Invocation              Ref file(s)                         Function file
----------------------  ----------------------------------  ----------------------
dashboard               ref/0-overview.md                   fn/fn-0-dashboard.md
package                 ref/0-overview.md + ALL ref/*       fn/fn-1-package.md
test                    ref/0-overview.md                   fn/fn-2-test.md
design (no fn-type)     ref/0-overview.md + ALL ref/*       fn/fn-3-design.md
design meta             ref/1-meta.md                       fn/fn-3-design.md
design trig             ref/2-trig.md                       fn/fn-3-design.md
design post             ref/3-post.md                       fn/fn-3-design.md
design src2input        ref/4-src2input.md                  fn/fn-3-design.md
design input2src        ref/5-input2src.md                  fn/fn-3-design.md
review (no fn-type)     ref/0-overview.md                   fn/fn-review.md
review <fn-type>        ref/<n>-<fn-type>.md                fn/fn-review.md
0-overview / overview   ref/0-overview.md                   (none)
meta                    ref/1-meta.md                       (none)
trig                    ref/2-trig.md                       (none)
post                    ref/3-post.md                       (none)
src2input               ref/4-src2input.md                  (none)
input2src               ref/5-input2src.md                  (none)
```

---

Step-by-Step Protocol
----------------------

Step 0: Read `ref/0-overview.md` first. Mandatory. Contains the Endpoint_Set
        layout, inference pipeline, and YAML conventions.

Step 1: Parse args. Function vocabulary above. Fn-type vocabulary:
          meta | trig | post | src2input | input2src

Step 2: Read the relevant ref file(s) per the dispatch table.

Step 3: Read the fn doc per the dispatch table.

Step 4: Execute the procedure. For `design`, the chosen fn-type scopes which
        inference Fn is built. For `package`, run the Endpoint_Pipeline using
        the Endpoint_Set name passed in args.

Step 5: Emit the structured tail (orchestrator parses this):

```
status:    ok | blocked | failed
summary:   2-3 sentences on what was done (artifact built / Fn designed / etc.)
artifacts: [paths created or modified, Endpoint_Set path]
next:      suggested next command — typically a target deploy:
             /haipipe-end deploy sagemaker <Endpoint_Set>
```

---

Artifact Scope
---------------

Owns:
  - `code/haifn/fn_endpoint/` — generated inference Fn code
  - `code-dev/1-PIPELINE/6-Endpoint-WorkSpace/` — builders for the 5 Fn types
  - `_WorkSpace/6-EndpointStore/Endpoint-*/` — packaged Endpoint_Sets
  - Local `inference()` smoke tests

Does NOT own:
  - Target-specific packaging (model.tar.gz, MLflow pyfunc, Flask app)
  - Credentials / IAM / workspace auth
  - Deploy CLI invocation
  - Live endpoint monitoring or teardown

These belong to `/haipipe-end-<target>` siblings.

---

Hand-off contract (Endpoint_Set -> target deployers)
-----------------------------------------------------

Each Endpoint_Set in `_WorkSpace/6-EndpointStore/Endpoint-{name}/` is the
SINGLE artifact that flows downstream. Layout:

```
Endpoint-{name}/
├── meta.json                  configuration + model registry pointers
├── fn_endpoint/               compiled inference Fn code
├── ModelInstance/             trained weights snapshot (or pointer)
└── manifest.yaml              everything a target deployer needs to know
```

Target deployers (sagemaker / databricks / flask / mlflow) READ this
artifact and never modify it. If a target deployer needs a missing field,
the fix lives here in `endpointset`, not in the target skill.
