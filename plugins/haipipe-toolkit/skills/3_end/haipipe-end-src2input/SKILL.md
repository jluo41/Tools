---
name: haipipe-end-src2input
description: "Src2InputFn specialist — design and review of the record-to-wire-payload function in an Endpoint_Set (serializes a ProcessedDF record into JSON the model can ingest). One of 5 inference Fn-types. TARGET-AWARE: SageMaker uses builders d1_*, Databricks uses builders f2_* (different wire formats). Pass --target sagemaker (default) or --target databricks. Called by /haipipe-end orchestrator when intent references Src2InputFn, record-to-payload serialization, or `src2input` keyword."
argument-hint: [verb] [use_case] [--target sagemaker|databricks] [args...]
allowed-tools: Bash, Read, Write, Edit, Grep, Glob
---

Skill: haipipe-end-src2input
=============================

Per-Fn-type specialist for **Src2InputFn** — the inference function
that serializes a ProcessedDF record into the wire-format payload the
model expects. The "outbound" half of the wire I/O pair (paired with
Input2SrcFn). One of the 5 inference Fn-types inside an Endpoint_Set.
See `ref/concepts.md` for Src2InputFn semantics.

  Verb axis:    design | review | list | concepts
  Use case:     each Src2InputFn impl is scoped to ONE encoding (CGM, weight, generic
                inference). `design` and `review` take a use_case argument.
  Target flag:  --target sagemaker  (default — uses d1_build_src2inputfn_InferenceV*)
                --target databricks (uses f2_build_src2inputfn_databricks_v1)
                The two targets emit DIFFERENT wire formats. Pick deliberately.

---

Commands
--------

```
/haipipe-end-src2input                                                  -> show Src2InputFn ref
/haipipe-end-src2input concepts                                         -> same
/haipipe-end-src2input list                                             -> list use-case impls
/haipipe-end-src2input design <use_case> [endpoint_set]                 -> SageMaker variant (d1_*)
/haipipe-end-src2input design <use_case> --target databricks [es]       -> Databricks variant (f2_*)
/haipipe-end-src2input review <use_case> [endpoint_set]                 -> structural audit
```

Use cases (concrete impls in code/haifn/fn_endpoint/fn_src2input/, as of 2026-04-25)
-------------------------------------------------------------------------------------

```
CGMInverse_v260101                              CGM inverse encoder      (sagemaker)
InferenceInverseV1219                           generic inference v1219  (sagemaker)
WellDocWeight_Src2Payload_v260305               weight encoder           (sagemaker)
WellDocWeight_Src2OldFormat_v260318             weight encoder (legacy)  (sagemaker)
DatabricksV1                                🚩  generic Databricks       (databricks)
CGMDecoder_DBR_Src2Payload_v260101          🚩  CGM Databricks variant   (databricks)

🚩 = target-specific variant (Databricks)
```

If `<use_case>` is omitted, the skill should `Bash("ls code/haifn/fn_endpoint/fn_src2input/")`
and ask the user to pick. If `--target` is omitted on a use case that has both variants
(e.g. CGM has `CGMInverse_v260101` for SageMaker and `CGMDecoder_DBR_Src2Payload_v260101`
for Databricks), confirm before proceeding.

---

Dispatch Table
---------------

```
Verb       Reads
---------- ------------------------------------------------------------------
design     ref/concepts.md
           ../haipipe-end/fn/fn-design.md
           ../haipipe-end/ref/0-overview.md
review     ref/concepts.md
           ../haipipe-end-endpointset/fn/fn-review.md
concepts   ref/concepts.md  (only)
```

---

Step-by-Step Protocol
----------------------

Step 0:  Read `ref/concepts.md` — Src2InputFn semantics, payload schema, encoding rules.
Step 1:  For `design`, also read `../haipipe-end/fn/fn-design.md` + `../haipipe-end/ref/0-overview.md`.
         For `review`, also read `../haipipe-end-endpointset/fn/fn-review.md`.
Step 2:  Execute the procedure scoped to Src2InputFn. Should stay in sync with its
         inverse pair `/haipipe-end-input2src` — the two must round-trip.
Step 3:  Emit the structured tail.

---

Scope
------

Owns:
  - Src2InputFn concept ref (`ref/concepts.md`)
  - Src2InputFn design + review scoped to ONE Fn-type

Does NOT own:
  - Inverse Fn — see `/haipipe-end-input2src`
  - Other 3 Fn-types — `-meta`, `-trig`, `-post`
  - Whole-artifact verbs — `/haipipe-end-endpointset`
  - Deployment — `/haipipe-end-deploy-*`

Pair invariant
---------------
For any record R: `Input2SrcFn(Src2InputFn(R)) == R`.
Changes here typically require a paired update in `-input2src`.
