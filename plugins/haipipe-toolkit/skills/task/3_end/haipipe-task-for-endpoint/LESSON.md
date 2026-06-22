# Endpoint Task Lifecycle — Lessons Learned

## From MIMIC-IV Mortality Endpoint Build (2026-06-13)

### L1: Training → Endpoint consistency is the critical gate

The endpoint task's #1 job is verifying that the model produces
identical predictions through the endpoint inference path as it did
during training. Any mismatch means data is lost or transformed
differently in the roundtrip.

**Verification flow:**
```
training: ProcName_to_ProcDf → PreFn → model.infer() → score A
endpoint: payload.json → Input2SrcFn → ProcName_to_ProcDf → PreFn → model.infer() → score B
score A == score B?  ← this is the gate
```

### L2: Src2InputFn must serialize ALL source tables

The first version serialized only 4 tables (LabEvent, ChartEvent,
Prescription, DiagnosisICD). The remaining 15-20 clinical tables
were silently dropped. This caused 2/6 examples to produce different
predictions — the missing tables contained features that affected
the model's score.

**Rule:** Serialize every non-empty table under `source_tables` in
the payload JSON. Use `_to_records(df)` with datetime→string
conversion for JSON safety.

### L3: Src2InputFn needs df_case_raw for case identity

Multi-admission patients: `Admission.iloc[0]` picks the wrong
admission for payload top-level fields. The correct admission
is identified by `df_case_raw` (HadmID, ObsDT).

**Rule:** `Src2InputFn(ProcName_to_ProcDf, SPACE, df_case_raw=None)`.
`Endpoint_Pipeline` must pass `example_info` as `df_case_raw`.

### L4: PostFn output format varies — template must be format-agnostic

`c_endpoint_nb.py` step 5 validation assumed `{name, score}` per
prediction (WellDoc format). MIMIC PostFn returns `{mortality_risk,
risk_level, threshold_alerts}`. Format string `:6.2f` crashed on
string values.

**Rule:** Template display code should iterate dict keys, detect
types, and format accordingly. Never hardcode field names.

### L5: Two payload formats — lossless vs lightweight

```
Lossless (source_tables):  For example validation, full roundtrip
Lightweight (flat fields):  For real-time API, only available data
```

`Input2SrcFn` should check for `source_tables` first, fall back to
flat field extraction. Both formats must produce valid ProcName_to_ProcDf.

### L6: Upstream example quality determines endpoint quality

If training examples have future data leak (records after ObsDT) or
wrong PatientID format, the endpoint inherits those problems. Fix
upstream in `extract_example_from_source` (temporal filtering) before
building the endpoint.

See `haipipe-task-for-fit/LESSON.md` L1 (temporal filtering) and
L2 (PatientID format).

### L7: endpoint_pipeline.py must pass df_case_raw to Src2InputFn

**Status:** NOT YET FIXED. This is the last remaining piece.

**Problem:** `endpoint_pipeline.py` line ~199 calls:
```python
payload_json = self.src2input_fn.Src2InputFn(ProcName_to_ProcDf, temp_space)
```
Without `df_case_raw`, Src2InputFn picks `Admission.iloc[0]` for the
top-level payload fields. For multi-admission patients, this is the wrong
admission. TrigFn then builds df_case_raw with wrong HadmID/ObsDT, causing
the PreFn to process the wrong case → different predictions.

**Fix needed** (in `haipipe/endpoint_base/endpoint_pipeline.py`):
```python
df_case_raw = pd.DataFrame([example_data.get('example_info', {})])
payload_json = self.src2input_fn.Src2InputFn(ProcName_to_ProcDf, temp_space, df_case_raw=df_case_raw)
```

**Current state:** 3/6 examples match (single-admission patients), 3/6
mismatch (multi-admission patients where iloc[0] picks wrong admission).
After this fix, expect 6/6 match.

**Process:** Fix via `code-dev/1-PIPELINE/6-Endpoint-WorkSpace/` builder
flow, not direct edit to `haipipe/`.
