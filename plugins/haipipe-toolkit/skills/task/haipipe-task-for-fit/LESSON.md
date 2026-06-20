# Training (Fit) Lifecycle — Lessons Learned

## From MIMIC-IV Mortality XGBoost Build (2026-06-13)

### L1: ExampleConfig temporal filtering — no future data leak

**Problem:** `extract_example_from_source` filters patient data by `PatientID`
but did not filter by time. MIMIC source tables (`Admission`, `LabEvent`, etc.)
use domain-specific temporal columns (`AdmitTime`, `ChartTime`, `StartTime`) that
weren't in the hardcoded `common_temporal_columns` list. Result: examples contained
ALL patient data including future admissions — data that wouldn't exist at
prediction time.

Example: a patient with 12 admissions kept all 12 in `ProcName_to_ProcDf`, even
when the case's ObsDT was the 10th admission. The last 2 admissions are future leak.

**Fix:** Added `_detect_temporal_column()` that auto-detects datetime columns by
scanning column names for `*Time`, `*Date`, `*DT` suffixes. Added optional
`ProcName_to_columns` parameter (from `prefn_config.json`) to guide detection.
Changed default `lookforward_days` from 30 to 0 — examples should only contain
data ≤ ObsDT.

**Rule:** Every example's `ProcName_to_ProcDf` must only contain records with
`temporal_col <= ObsDT`. Verify by checking `Admission` row count — if a patient
has N admissions but the case is admission K, expect K rows (not N).

### L2: PatientID format mismatch — PID (int) vs PatientID (string)

**Problem:** The pipeline uses two patient ID formats:
- `PID` = internal integer (e.g., `10000002948`) — used in AIData/CaseSet
- `PatientID` = source format (e.g., `mimic-11213546`) — used in SourceSet

`TriggerArgs.case_raw_id_columns` = `['PID', 'HadmID', 'ObsDT']`. The code
picks `PID` as `rawhuman_id_column` but SourceSet tables use `PatientID`.
Result: `df_full[PatientID_col] == PID_int` matches nothing — examples had
only dictionary tables (D*), no clinical data.

**Fix:** `row.get('PatientID', row[rawhuman_id_column])` — prefer `PatientID`
(source format) over `PID` (internal format) when both exist in df_case.

**Rule:** The ExampleFn must include `PatientID` in its output. The pipeline
must pass the source-format patient ID to `extract_example_from_source`.

### L3: `.infer()` is the unified model inference API

**Problem:** Two generations of model classes exist:
- Old (`code/hainn/mlpredictor/`): `.inference(Data, InferenceArgs)`
- New (`code/hainn/instance/`): `.infer(Data, InferenceArgs)`

The model registry resolves exclusively to `instance/` classes. Calling
`.inference()` throws `AttributeError`, caught silently by try/except,
leaving `prediction_results.json` = `{}`.

**Fix:** All callers unified to `.infer()`. The method handles:
- Raw `Dataset` or `DataFrame` → direct inference
- `{split: Dataset}` dict → per-split inference
- `AIData_Set` → auto-extract splits

For single-example validation (step 8), pass the Dataset directly:
`model_instance.infer(test_data)` — no dict wrapper needed.

**Rule:** Never call `.inference()` on model instances. Always `.infer()`.
`Endpoint_Set.inference()` is a different level (JSON in → JSON out).

### L4: `prediction_results.json` empty = silent bug

**Problem:** When `.inference()` call failed silently (L3), predictions
weren't saved. Step 8 reproducibility check printed "No saved predictions
to compare" and passed — a false positive.

**Rule:** After training with `ExampleConfig.enabled: true`, verify:
```bash
cat examples/example_000/prediction_results.json
# Must NOT be {} — should have score__default or similar
```

### L5: `SKIP_TRAINING` parameter for fast iteration

Added `SKIP_TRAINING` parameter to `b_model_nb.py`. When `"true"`:
- Skips steps 2-3 (Optuna training + save) if model exists on disk
- Steps 4-9 run normally (verify examples, reload, validate, infer)

**Limitation:** Example generation is inside `pipeline.run(mode='fit')`.
`SKIP_TRAINING=true` skips `pipeline.run()` entirely, so examples are NOT
regenerated. To regenerate examples without retraining, you currently need
a full run. Future improvement: separate `pipeline.generate_examples()`.

**Usage:**
```bash
papermill ... -p SKIP_TRAINING "true"   # skip training, validate only
papermill ... -p SKIP_TRAINING ""       # full training (default)
```

### L6: Step 8 reproducibility — what it actually tests

Step 8 loads each saved example, runs the full PreFn pipeline
(Source→Record→Case→AIData), runs model inference, and compares
predictions to `prediction_results.json`.

This tests:
- PreFn pipeline determinism (same input → same features)
- Model inference determinism (same features → same score)
- Data serialization fidelity (parquet save/load roundtrip)

A mismatch means the pipeline is non-deterministic or data was
corrupted during save. Zero-delta is the target:
```
example_000  | 0.346305 | 0.346305 | 0.000000 | YES
```

### L7: AUC baseline for MIMIC-IV mortality

With 68 sparse features (demographics + labs + vitals + meds + admit type),
3 Optuna trials, XGBoost S-Learner:

```
Validation:  AUC=0.884  Brier=0.022  (N=82,027, pos_rate=2.15%)
Test:        AUC=0.887  Brier=0.022  (N=82,025, pos_rate=2.12%)
```

This is the quick-validation baseline (3 trials). Production runs
should use `n_trials: 20+` for better hyperparameter search.
