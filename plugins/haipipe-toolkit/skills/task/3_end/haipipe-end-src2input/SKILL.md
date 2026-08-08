---
name: haipipe-end-src2input
description: "Src2InputFn specialist -- designs/reviews the record->wire-payload function in an Endpoint_Set (serializes a ProcessedDF record into JSON the model can ingest). Platform-specific: one impl per deploy platform (SageMaker flat JSON vs Databricks dataframe_records); --platform picks (default sagemaker). Called by /haipipe-end when intent references Src2InputFn, record-to-payload serialization, or `src2input`."
argument-hint: "[verb] [use_case] [--platform sagemaker|databricks] [args...]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob
metadata:
  version: "0.2.1"
  last_updated: "2026-07-08"
  summary: "Src2InputFn specialist — design and review of the record-to-wire-payload function in an Endpoint_Set (serializes a ProcessedDF record into JSON the model can ingest)."
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

Skill: haipipe-end-src2input
=============================

Per-Fn-type specialist for **Src2InputFn** — the inference function that serializes a ProcessedDF record into the wire-format payload the model expects.
The "outbound" half of the wire I/O pair (paired with Input2SrcFn).
One of the 5 inference Fn-types inside an Endpoint_Set.
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
<YourDatabricksFn>                                🚩  generic Databricks       (databricks)
CGMDecoder_Databricks_Src2Payload_v260101          🚩  CGM Databricks variant   (databricks)

🚩 = Databricks-platform impl (one wire-Fn per platform by design; sagemaker unmarked)
```

If `<use_case>` is omitted, the skill should `Bash("ls code/haifn/fn_endpoint/fn_src2input/")` and confirm the impl with the user before proceeding (the snapshot above goes stale; disk is the truth).

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

Step 0: Read `ref/concepts.md` — Src2InputFn semantics, payload schema, encoding rules.
Step 1: For `design`, also read `../haipipe-end/fn/fn-design.md` + `../haipipe-end/ref/0-overview.md`.
         For `review`, also read `../haipipe-end-endpointset/fn/fn-review.md`.
Step 2: Execute the procedure scoped to Src2InputFn.
         Should stay in sync with its inverse pair `/haipipe-end-input2src` — the two must round-trip.
Step 3: Emit the structured tail.

---

Guardrails (learned the hard way — do NOT skip)
------------------------------------------------

```
SRC-1  A column this Fn DECLARES it reads must RAISE if absent. `safe_get(row, name,
       default)` and a `format_date` that falls back to `datetime.now()` turn a wrong
       column name into a plausible value with no error.
       InferenceInverseV1219 read SEVEN names that exist in no source frame:

           created_date              -> created_date_utc
           invitation_date           -> invitation_date_utc     (read in TWO sections)
           patient_zipcode_3         -> zipcode3
           pharmacy_zipcode_3, ther_eq_hierarchy_level,
           ther_eq_ult_child_ind, ther_eq_ult_parent_etc_id     -> no source at all

       Result: every generated payload carried dateOfBirth 1980-01-01 and a null
       zipCode, blanking PAge5 + PZip3FixedLen + InvCrntTimeFixedLen +
       Zip3EngFixedLen = 371 of 1995 vocab slots, 18.6% of the model's input, for
       months. Use a `col()` that raises for declared reads and an `opt()` for the
       genuinely optional ones. Audit an existing Fn with:

           check every safe_get/format_date name against
           set(Ptt.columns) | set(invitation.columns) | set(Rx.columns)

SRC-2  The emitted payload's KEY SET must equal the real production payload's key
       set, asserted at build time against a captured reference. A generated payload
       that carries the old rich training-era contract (46 fields production no
       longer sends, 20 it does send but the writer omits) cannot test production.
       Keep a masked real payload in the repo as the reference and diff key paths.

SRC-3  A field with no source column is emitted as NULL, never omitted. Production
       sends the key; the parser's fill/tolerance logic depends on its presence.

SRC-4  Coerce numpy scalars to native Python. Parquet hands back bool_/int64/float64
       and json.dump cannot serialize them.
```

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
For any record R and platform P: `Input2SrcFn_P(Src2InputFn_P(R)) == R` (the SAME-platform pair must roundtrip).
Changes here typically require a paired update in `-input2src` for the same platform.

Roundtrip test (REQUIRED for design and review)
-------------------------------------------------

Every `design` or `review` MUST include a roundtrip test against **real example data** from the ModelInstanceStore — not synthetic/minimal payloads.

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

**Why real data:** Synthetic payloads only test happy-path parsing.
Real data catches: tables dropped by Src2InputFn (only 4 of 19 serialized), datetime serialization issues, multi-admission patients getting wrong admission at iloc[0], dtype mismatches (int vs float vs string).

The builder script (d1_build_* in the endpoint fn_develop task folder) must include this test.
If the roundtrip fails, the Fn is not production-ready.

**⚠️ Comparing scores is NOT sufficient — also compare the SERVED arm.** The response
carries every arm in `predictions[]` and separately names one in `action.name`. A PostFn
with a broken candidate list leaves all scores correct and still serves the wrong message,
so a score-only comparison passes a broken endpoint. Assert all three:

```python
assert served == max(model_scores, key=model_scores.get)          # action.name
assert argmax(model_scores) == argmax(endpoint_scores)            # the ranking
assert max(abs(model[a] - endpoint[a]/100) for a in arms) < 0.001  # per-arm, SAME arm
```

**⚠️ This test must be run against a KNOWN-BROKEN build first.** A round-trip check that
has never failed is not yet a check. The pre-existing one in `c_endpoint_nb.py` matched ANY
train score to ANY endpoint score, across DIFFERENT arms, with the two sides scaled 100x
apart, and was non-fatal — so it caught none of four real defects. A working reference
implementation is `examples/Project-ExpModel-ClickPred/tasks/C_endpoint/C5_src2input_fn_develop/c1_roundtrip_gate.py`
(in-process/Docker) and `platform-sagemaker-inference/scripts/build_endpoint/roundtrip_gate_sage.py`
(live endpoint).
