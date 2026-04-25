---
name: haipipe-end-input2src
description: "Input2SrcFn specialist — design and review of the wire-payload-to-record function in an Endpoint_Set (deserializes JSON request into a ProcessedDF row). One of 5 inference Fn-types. TARGET-AWARE: SageMaker uses builders e1_*, Databricks uses builders f1_* (different wire formats). Pass --target sagemaker (default) or --target databricks. Called by /haipipe-end orchestrator when intent references Input2SrcFn, payload-to-record deserialization, or `input2src` keyword."
argument-hint: [verb] [use_case] [--target sagemaker|databricks] [args...]
allowed-tools: Bash, Read, Write, Edit, Grep, Glob
---

Skill: haipipe-end-input2src
=============================

Per-Fn-type specialist for **Input2SrcFn** — the inference function
that deserializes a wire-format JSON payload back into a ProcessedDF
row. The "inbound" half of the wire I/O pair (paired with
Src2InputFn). One of the 5 inference Fn-types inside an Endpoint_Set.
See `ref/concepts.md` for Input2SrcFn semantics.

  Verb axis:    design | review | list | concepts
  Use case:     each Input2SrcFn impl is scoped to ONE decoding (CGM, weight, generic
                inference). `design` and `review` take a use_case argument.
  Target flag:  --target sagemaker  (default — uses e1_build_input2srcfn_inferencev*)
                --target databricks (uses f1_build_input2srcfn_databricks_v1)
                The two targets parse DIFFERENT wire formats. Pick deliberately.

---

Commands
--------

```
/haipipe-end-input2src                                                  -> show Input2SrcFn ref
/haipipe-end-input2src concepts                                         -> same
/haipipe-end-input2src list                                             -> list use-case impls
/haipipe-end-input2src design <use_case> [endpoint_set]                 -> SageMaker variant (e1_*)
/haipipe-end-input2src design <use_case> --target databricks [es]       -> Databricks variant (f1_*)
/haipipe-end-input2src review <use_case> [endpoint_set]                 -> structural audit
```

Use cases (concrete impls in code/haifn/fn_endpoint/fn_input2src/, as of 2026-04-25)
-------------------------------------------------------------------------------------

```
InferenceV240727                                generic inference         (sagemaker)
CGMExamples_v260101                             CGM examples decoder      (sagemaker)
WellDocWeight_Payload2Src_v260305               weight decoder            (sagemaker)
WellDocWeight_OldFormat2Src_v260318             weight decoder (legacy)   (sagemaker)
DatabricksV1                                🚩  generic Databricks         (databricks)
CGMDecoder_DBR_Payload2Src_v260101          🚩  CGM Databricks variant     (databricks)

🚩 = target-specific variant (Databricks)
```

If `<use_case>` is omitted, the skill should `Bash("ls code/haifn/fn_endpoint/fn_input2src/")`
and ask the user to pick. If `--target` is omitted on a use case that has both variants
(e.g. CGM has `CGMExamples_v260101` for SageMaker and `CGMDecoder_DBR_Payload2Src_v260101`
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

Step 0:  Read `ref/concepts.md` — Input2SrcFn semantics, schema validation, decoding rules.
Step 1:  For `design`, also read `../haipipe-end/fn/fn-design.md` + `../haipipe-end/ref/0-overview.md`.
         For `review`, also read `../haipipe-end-endpointset/fn/fn-review.md`.
Step 2:  Execute the procedure scoped to Input2SrcFn. Must stay in sync with its
         inverse pair `/haipipe-end-src2input`.
Step 3:  Emit the structured tail.

---

Scope
------

Owns:
  - Input2SrcFn concept ref (`ref/concepts.md`)
  - Input2SrcFn design + review scoped to ONE Fn-type

Does NOT own:
  - Inverse Fn — see `/haipipe-end-src2input`
  - Other 3 Fn-types — `-meta`, `-trig`, `-post`
  - Whole-artifact verbs — `/haipipe-end-endpointset`
  - Deployment — `/haipipe-end-deploy-*`

Pair invariant
---------------
For any record R: `Input2SrcFn(Src2InputFn(R)) == R`.
Changes here typically require a paired update in `-src2input`.
