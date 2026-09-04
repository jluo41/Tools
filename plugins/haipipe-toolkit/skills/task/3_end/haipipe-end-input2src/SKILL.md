---
name: haipipe-end-input2src
description: "Input2SrcFn specialist -- designs/reviews the wire-payload->record function in an Endpoint_Set (deserializes a JSON request into a ProcessedDF row). Platform-specific: one impl per deploy platform (SageMaker flat JSON vs Databricks dataframe_records); --platform picks (default sagemaker). Called by /haipipe-end when intent references Input2SrcFn, payload-to-record deserialization, or `input2src`."
argument-hint: "[verb] [use_case] [--platform sagemaker|databricks] [args...]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob
metadata:
  version: "0.2.1"
  last_updated: "2026-07-08"
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

Skill: haipipe-end-input2src
=============================

Per-Fn-type specialist for **Input2SrcFn** — the inference function that deserializes a wire-format JSON payload back into a ProcessedDF row.
The "inbound" half of the wire I/O pair (paired with Src2InputFn).
One of the 5 inference Fn-types inside an Endpoint_Set.
See `ref/concepts.md` for Input2SrcFn semantics.

  Verb axis:    design | review | list | concepts
  Use case:     each Input2SrcFn impl is scoped to ONE decoding (CGM, weight, generic
                inference). `design` and `review` take a use_case argument.
  Platform:     ONE Input2SrcFn PER PLATFORM per use-case (owner decision
                2026-07-05, supersedes LESSON L16): a SageMaker payload gets
                a SageMaker impl (flat JSON); a Databricks payload gets its
                own impl that owns the {'dataframe_records': [...]} envelope.
                Put the platform in the impl name (e.g. *_Databricks_*;
                sagemaker unmarked). Keep variants thin over a shared body;
                the duplicate-fix cost is accepted (L16 history +
                supersession note).
                `--platform sagemaker|databricks` picks which platform's Fn
                a design/review targets (default sagemaker).

---

Commands
--------

```
/haipipe-end-input2src                                                  -> show Input2SrcFn ref
/haipipe-end-input2src concepts                                         -> same
/haipipe-end-input2src list                                             -> list use-case impls
/haipipe-end-input2src design <use_case> [endpoint_set] [--platform sagemaker|databricks]  -> design that platform's Fn
/haipipe-end-input2src review <use_case> [endpoint_set] [--platform sagemaker|databricks]  -> structural audit of that platform's Fn
# --platform selects WHICH platform's impl to design/review (default sagemaker);
# one Fn per platform per use-case (owner decision 2026-07-05)
```

Use cases (concrete impls in code/haifn/fn_endpoint/fn_input2src/, as of 2026-04-25)
-------------------------------------------------------------------------------------

```
InferenceV240727                                generic inference         (sagemaker)
CGMExamples_v260101                             CGM examples decoder      (sagemaker)
WellDocWeight_Payload2Src_v260305               weight decoder            (sagemaker)
WellDocWeight_OldFormat2Src_v260318             weight decoder (legacy)   (sagemaker)
<YourDatabricksFn>                                🚩  generic Databricks         (databricks)
CGMDecoder_Databricks_Payload2Src_v260101          🚩  CGM Databricks variant     (databricks)

🚩 = Databricks-platform impl (one wire-Fn per platform by design; sagemaker unmarked)
```

If `<use_case>` is omitted, the skill should `Bash("ls code/haifn/fn_endpoint/fn_input2src/")` and confirm the impl with the user before proceeding (the snapshot above goes stale; disk is the truth).

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

Step 0: Read `ref/concepts.md` — Input2SrcFn semantics, schema validation, decoding rules.
Step 1: For `design`, also read `../haipipe-end/fn/fn-design.md` + `../haipipe-end/ref/0-overview.md`.
         For `review`, also read `../haipipe-end-endpointset/fn/fn-review.md`.
Step 2: Execute the procedure scoped to Input2SrcFn.
         Must stay in sync with its inverse pair `/haipipe-end-src2input`.
Step 3: Emit the structured tail.

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
For any record R and platform P: `Input2SrcFn_P(Src2InputFn_P(R)) == R` (the SAME-platform pair must roundtrip).
Changes here typically require a paired update in `-src2input` for the same platform.

Roundtrip test (REQUIRED for design and review)
-------------------------------------------------

Every `design` or `review` MUST include a roundtrip test against **real example data** from the ModelInstanceStore.
See the paired skill `haipipe-end-src2input` for the full test protocol.

The test verifies:
1. All non-empty source tables survive the roundtrip
2. Features produced from original vs reconstructed data are identical
3. Model predictions match within tolerance (< 0.001)

**Why this matters:** Input2SrcFn must reconstruct ALL tables that CaseFns read — not just the ones that seem important.
If Src2InputFn serializes only 4 of 19 tables and Input2SrcFn creates empty stubs for the rest, CaseFns that read the missing tables produce zero features → different predictions.
This is silent — no error, just wrong scores.

The builder script (e1_build_* in the endpoint fn_develop task folder) must include this test paired with the Src2InputFn.
If the roundtrip fails, neither Fn is production-ready.
