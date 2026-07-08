---
name: haipipe-end-src2input
description: "Src2InputFn specialist — design and review of the record-to-wire-payload function in an Endpoint_Set (serializes a ProcessedDF record into JSON the model can ingest). One of 5 inference Fn-types. PLATFORM-SPECIFIC by owner decision 2026-07-05 (supersedes LESSON L16): ONE Src2InputFn per deploy platform per use-case — SageMaker payload gets a SageMaker impl (flat JSON), Databricks its own (dataframe_records envelope); --platform selects which platform's Fn to design/review (default sagemaker). Called by /haipipe-end orchestrator when intent references Src2InputFn, record-to-payload serialization, or `src2input` keyword."
argument-hint: "[verb] [use_case] [--platform sagemaker|databricks] [args...]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob
metadata:
  version: "2.0.0"
  last_updated: "2026-07-05"
  summary: "Src2InputFn specialist — design and review of the record-to-wire-payload function in an Endpoint_Set (serializes a ProcessedDF record into JSON the model can ingest)."
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
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
  Platform:     ONE Src2InputFn PER PLATFORM per use-case (owner decision
                2026-07-05, supersedes LESSON L16): a SageMaker payload gets
                a SageMaker impl (flat JSON); a Databricks payload gets its
                own impl ({'dataframe_records': [...]} envelope). Put the
                platform in the impl name (e.g. *_Databricks_*; sagemaker
                unmarked). Keep variants thin over a shared body: every fix
                must be applied to each platform's file; that cost is
                accepted (L16 history + supersession note).
                `--platform sagemaker|databricks` picks which platform's Fn
                a design/review targets (default sagemaker).

---

Commands
--------

```
/haipipe-end-src2input                                                  -> show Src2InputFn ref
/haipipe-end-src2input concepts                                         -> same
/haipipe-end-src2input list                                             -> list use-case impls
/haipipe-end-src2input design <use_case> [endpoint_set] [--platform sagemaker|databricks]  -> design that platform's Fn
/haipipe-end-src2input review <use_case> [endpoint_set] [--platform sagemaker|databricks]  -> structural audit of that platform's Fn
# --platform selects WHICH platform's impl to design/review (default sagemaker);
# one Fn per platform per use-case (owner decision 2026-07-05)
```

Use cases (concrete impls in code/haifn/fn_endpoint/fn_src2input/, as of 2026-04-25)
-------------------------------------------------------------------------------------

```
CGMInverse_v260101                              CGM inverse encoder      (sagemaker)
InferenceInverseV1219                           generic inference v1219  (sagemaker)
WellDocWeight_Src2Payload_v260305               weight encoder           (sagemaker)
WellDocWeight_Src2OldFormat_v260318             weight encoder (legacy)  (sagemaker)
DatabricksV1                                🚩  generic Databricks       (databricks)
CGMDecoder_Databricks_Src2Payload_v260101          🚩  CGM Databricks variant   (databricks)

🚩 = Databricks-platform impl (one wire-Fn per platform by design; sagemaker unmarked)
```

If `<use_case>` is omitted, the skill should `Bash("ls code/haifn/fn_endpoint/fn_src2input/")`
and confirm the impl with the user before proceeding (the snapshot above goes stale;
disk is the truth).

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
For any record R and platform P: `Input2SrcFn_P(Src2InputFn_P(R)) == R`
(the SAME-platform pair must roundtrip). Changes here typically require
a paired update in `-input2src` for the same platform.

Roundtrip test (REQUIRED for design and review)
-------------------------------------------------

Every `design` or `review` MUST include a roundtrip test against **real
example data** from the ModelInstanceStore — not synthetic/minimal payloads.

```python
# Load a real example from training
example_path = f"{MODELINSTANCE_STORE}/{name}/@{version}/examples/example_000"
ProcName_to_ProcDf = {
    f.replace('.parquet',''): pd.read_parquet(os.path.join(example_path, 'ProcName_to_ProcDf', f))
    for f in os.listdir(os.path.join(example_path, 'ProcName_to_ProcDf'))
    if f.endswith('.parquet')
}

# Roundtrip: serialize → deserialize
payload = Src2InputFn(ProcName_to_ProcDf, SPACE)
reconstructed = Input2SrcFn(payload, SPACE)

# Verify: all non-empty source tables survived
for table_name, original_df in ProcName_to_ProcDf.items():
    if len(original_df) == 0:
        continue
    recon_df = reconstructed.get(table_name, pd.DataFrame())
    assert len(recon_df) > 0, f"Table {table_name} lost in roundtrip ({len(original_df)} rows → 0)"

# Verify: features produce same model prediction
result_original = prefn(df_case_raw, ProcName_to_ProcDf, mode='inference')
result_roundtrip = prefn(df_case_raw, reconstructed, mode='inference')
pred_original = model.infer(result_original['all'])
pred_roundtrip = model.infer(result_roundtrip['all'])
# Compare scores — delta must be < 0.001
```

**Why real data:** Synthetic payloads only test happy-path parsing. Real data
catches: tables dropped by Src2InputFn (only 4 of 19 serialized), datetime
serialization issues, multi-admission patients getting wrong admission at
iloc[0], dtype mismatches (int vs float vs string).

The builder script (d1_build_* in the endpoint fn_develop task folder) must include this test. If the
roundtrip fails, the Fn is not production-ready.
