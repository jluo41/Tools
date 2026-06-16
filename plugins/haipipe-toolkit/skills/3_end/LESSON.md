# Endpoint Lifecycle — Lessons Learned

## The Endpoint Lifecycle

The endpoint lifecycle has **4 phases**, each with clear ownership:

```
Phase 1: DESIGN        Author the 5 inference Fns (00_endpoint_set_fn_develop)
Phase 2: PACKAGE       ModelInstance_Set → Endpoint_Set → .tar.gz (01_endpoint)
Phase 3: VALIDATE      Local inference on saved examples (step 5 + 5b)
Phase 4: DEPLOY        Serve on a target (platform-*-inference/)
```

Phase 4 delegates to a **deployment platform** — the `.tar.gz` is the handoff:

```
                SageMaker                          Databricks
                ─────────                          ──────────
Input:          .tar.gz                            .tar.gz (same artifact!)
                    │                                  │
Upload:         S3 bucket                          Unity Catalog Volume
                    │                                  │
Runtime:        ECR Docker image                   (none — MLflow pyfunc)
                    │                                  │
Register:       SageMaker Model                    MLflow → Unity Catalog
                    │                                  │
Deploy:         Endpoint (serverless)              Model Serving endpoint
                    │                                  │
Smoke Test:     test_endpoint_sage.py              test_endpoint_databricks.py
                    │                                  │
Stress Test:    sagemaker_load_test.py             test_endpoint_databricks.py --benchmark
```

Verb lifecycle shared across platforms:
`VALIDATE → UPLOAD → REGISTER → DEPLOY → SMOKE TEST → STRESS TEST → PROMOTE`

- **Smoke test** = correctness (one call, assert format + values match)
- **Stress test** = capacity (concurrent load, throughput, latency p95/p99, error rate)

### Phase 1: Design (code-dev/ → code/haifn/fn_endpoint/)

Author 5 Fn files that define how raw data becomes a prediction response:

```
MetaFn       — model metadata (name, version, capabilities)
TrigFn       — should this request trigger inference? (optional gate)
Src2InputFn  — ProcName_to_ProcDf → JSON payload (serialization)
Input2SrcFn  — JSON payload → ProcName_to_ProcDf (deserialization)
PostFn       — raw model scores → client-facing JSON response
```

Tools: `/haipipe-end <fn-type> design` or manual builder scripts in `code-dev/`.

### Phase 2: Package (c_endpoint_nb.py steps 1-4)

```
[1] Load ModelInstance_Set (must have examples from ExampleConfig)
[2] Endpoint_Pipeline.run()
    — loads 5 Fn files
    — generates payload.json per example via Src2InputFn
    — packages everything into Endpoint_Set
[3] Save to 6-EndpointStore/
[4] Verify examples have payload.json
```

The Endpoint_Set is self-contained: model weights, PreFn pipeline, code
snapshot, examples with payloads — everything needed to serve.

### Phase 3: Validate (c_endpoint_nb.py steps 5-6)

```
[5] Load Endpoint_Set from disk
    Run endpoint.inference(payload) on each example's payload.json
    Verify predictions are valid (format, values, no errors)
[6] Package for deployment (.tar.gz)
```

### Phase 4: Deploy

```
/haipipe-end deploy local       — Flask/FastAPI on localhost
/haipipe-end deploy databricks  — Unity Catalog → Model Serving
/haipipe-end deploy sagemaker   — ECR → SageMaker Endpoint
```

---

## The 7-Step Inference Pipeline (inside Endpoint_Set.inference())

```
Step 1  TrigFn         payload_json           → should_process? (optional gate)
Step 2  Input2SrcFn    payload_json           → ProcName_to_ProcDf
Step 3  PreFnPipeline  ProcName_to_ProcDf     → RecordSet
Step 4  PreFnPipeline  RecordSet + df_case    → CaseSet (features)
Step 5  PreFnPipeline  CaseSet               → model_input (HF Dataset)
Step 6  model.infer()  model_input            → DataFrame (score__{action})
Step 7  PostFn         scores_df              → response_json
```

---

## Lessons from MIMIC-IV Mortality Endpoint Build (2026-06-13)

### L1: `.inference()` vs `.infer()` — unified to `.infer()`

**Problem:** Two generations of model classes existed:
- Old (`code/hainn/mlpredictor/`): `.inference(Data, InferenceArgs)`
- New (`code/hainn/instance/mlpredictor/`): `.infer(Data, InferenceArgs)`

The model registry (`model_registry.py`) points exclusively to `instance/`
classes, but `modelinstance_pipeline.py` still called `.inference()`. This
caused silent failures (AttributeError caught by try/except) that left
`prediction_results.json` empty — making step 8 reproducibility checks
pass vacuously ("no saved predictions to compare").

**Fix:** Unified all model-level calls to `.infer()`. The method accepts
raw Dataset, DataFrame, or dict — no wrapper needed for single examples.

**Rule:** All model inference calls use `.infer()`. `Endpoint_Set.inference()`
is the endpoint-level API (JSON in → JSON out) and keeps its name — it's
a different abstraction level.

### L2: `df_case_raw` means "skip the trigger"

**Problem:** `Case_Pipeline.run(df_case_raw=...)` was calling
`execute_triggertask()` which runs the full TriggerFn expecting a
training-mode RecordSet with `Name_to_HRF`. In inference mode, the
RecordSet is built from parquet files and has no `Name_to_HRF`.

**Fix:** When `df_case_raw` is provided, use it directly as `df_case`.
The trigger's job is to extract cases from a RecordSet — `df_case_raw`
IS those cases. The subsequent `_extract_features(df_case, record_set)`
still uses the RecordSet for CaseFn feature extraction.

**Rule:** `df_case_raw` = "I already have the cases, just extract features."

### L3: PostFn output ≠ template display assumptions

**Problem:** `c_endpoint_nb.py` step 5 validation assumed predictions
have `{name, score}` per action (the WellDoc format). MIMIC PostFn
returns `{mortality_risk, risk_level, threshold_alerts}`. The format
string `pred.get('score', 'N/A'):6.2f` crashed with "Unknown format
code 'f' for object of type 'str'" because `score` key was missing.

**Fix:** Made the display code format-agnostic — iterate dict keys,
format floats as floats and everything else as strings.

**Rule:** Template display code must handle arbitrary PostFn output
schemas. Never hardcode field names from one project's PostFn.

### L4: `prediction_results.json` must be non-empty for reproducibility

**Problem:** Due to L1, `prediction_results.json` was `{}` for all
examples. Step 8 then printed "No saved predictions to compare" and
marked the example as passing — a false positive. The reproducibility
check was vacuously true.

**Fix:** Fixed L1 so predictions are actually saved during training.
Step 8 now does real score comparisons.

**Rule:** If `prediction_results.json` is empty after training, that's
a bug — the ExampleConfig pipeline failed silently. Check for it.

### L5: `SKIP_TRAINING` parameter for fast iteration

**Problem:** Every run of `b_model_nb.py` re-trains (15+ minutes for
3 Optuna trials). When debugging steps 6-9 (validation), this wastes
time.

**Fix:** Added `SKIP_TRAINING` parameter to `b_model_nb.py`. When
`"true"`, skips steps 2-3 (train + save) and uses existing model on
disk. Steps 4-9 run normally.

**Usage:**
```bash
papermill ... -p SKIP_TRAINING "true"
```

**Rule:** Every long-running template should have a skip mechanism
for the expensive step, gated on whether output already exists.

### L6: Copying shared packages overwrites local fixes

**Problem:** After copying `haipipe/` from WellDoc-SPACE to sync
changes, local fixes to `case_pipeline.py` and
`modelinstance_pipeline.py` were overwritten.

**Rule:** Before copying shared packages (`haipipe`, `hainn`), check
`git diff` for local modifications. Apply fixes to the source repo
first, then copy. Or better: make shared packages a git submodule.

### L7: Endpoint validation mismatch — root cause: Src2InputFn lost data

**Problem:** 2 of 6 examples showed different predictions between
training-time `prediction_results.json` and endpoint-time inference.

**Root cause (resolved):** Two issues in the Src2InputFn/Input2SrcFn
roundtrip:

1. **Src2InputFn serialized only 4 tables** (LabEvent, ChartEvent,
   Prescription, DiagnosisICD). The remaining 15-20 clinical tables
   were lost. Fix: serialize ALL non-empty tables under `source_tables`.

2. **Src2InputFn picked wrong admission** — `Admission.iloc[0]` for
   top-level fields (patient_id, admission_id, admit_time), but patients
   with multiple admissions have the wrong one at index 0. The correct
   admission is identified by `df_case_raw` (which has `HadmID`, `ObsDT`).
   Fix: pass `df_case_raw` to Src2InputFn.

**Root cause of wrong admissions in ProcName_to_ProcDf (resolved):**
`extract_example_from_source` didn't filter by time — kept ALL patient
admissions including future ones. See haipipe-task-for-fit/LESSON.md L1
for the temporal filtering fix.

**After all fixes:** 6/6 examples match with zero delta:
```
example_000  | 0.346305 | 0.346305 | 0.000000 | YES
example_001  | 0.351480 | 0.351480 | 0.000000 | YES
```

**Rule:** Always compare training predictions with endpoint predictions
as a reproducibility gate. Mismatches reveal real pipeline bugs — never
dismiss as "floating point noise" without investigation.

### L8: Src2InputFn needs df_case_raw for case identity

**Problem:** `Src2InputFn(ProcName_to_ProcDf, SPACE)` doesn't know which
specific case (admission) the example represents. For multi-admission
patients, it picks the wrong admission for top-level payload fields.

**Fix:** Add `df_case_raw` parameter: `Src2InputFn(ProcName_to_ProcDf,
SPACE, df_case_raw=None)`. When provided, use `HadmID`/`ObsDT` from
df_case_raw for case identity. The pipeline passes `example_info` as
df_case_raw.

**Rule:** Src2InputFn must always receive case identity (df_case_raw)
to correctly populate the payload. The Endpoint_Pipeline should pass it.

### L9: Lossless payload roundtrip via `source_tables`

**Design:** `Src2InputFn` stores all source tables under a `source_tables`
key in the payload JSON. `Input2SrcFn` checks for `source_tables` first
(new lossless format), falls back to per-field extraction (legacy format
for real-time API calls with partial data).

```json
{
  "patient_id": "11213546",
  "admission_id": "27235432",
  "source_tables": {
    "Ptt": [...],
    "Admission": [...],
    "LabEvent": [...],
    ...
  }
}
```

**Rule:** Example payloads should use the `source_tables` format for
validation. Real-time API payloads may use the legacy flat format (only
demographics + available clinical data).

### L10: endpoint_pipeline.py must pass df_case_raw to Src2InputFn

**Problem:** `endpoint_pipeline.py` line 199 called
`Src2InputFn(ProcName_to_ProcDf, SPACE)` without `df_case_raw` during
payload generation. Even though Src2InputFn had the `df_case_raw` parameter
(L8), the pipeline never passed it. Multi-admission patients got wrong
admission identity in the payload → wrong features → wrong predictions.

**Fix:** `endpoint_pipeline.py` now extracts `example_info` from each
example and passes it as `df_case_raw`:
```python
_example_info = example_data.get('example_info', {})
_df_case_raw = pd.DataFrame([_example_info]) if _example_info else None
payload_json = Src2InputFn(ProcName_to_ProcDf, SPACE, df_case_raw=_df_case_raw)
```
With try/except TypeError fallback for Src2InputFns that don't accept
df_case_raw (backward compatibility).

**Result:** All 6 examples now match within Δ < 0.00003 (floating point
rounding only).

**Rule:** When the pipeline has case identity, always pass it through.
Don't let intermediate code lose context that downstream Fns need.

### L11: Roundtrip test with real data — enforced at 3 levels

**Problem:** The original builder scripts (`d1_build_src2inputfn_*.py`,
`e1_build_input2srcfn_*.py`) only tested with synthetic minimal payloads.
Synthetic tests pass trivially — they don't catch:
- Tables dropped during serialization (only 4 of 19)
- Multi-admission patients getting wrong admission at iloc[0]
- Dtype mismatches after JSON roundtrip
- CaseFns reading tables that weren't serialized

**Fix — three enforcement levels:**

1. **Design time** (`code-dev/f1_roundtrip_test_mimic.py`): Loads real
   examples from ModelInstanceStore, runs full roundtrip (Src2InputFn →
   Input2SrcFn → PreFn → model.infer()), compares predictions. Must pass
   before Fn is production-ready.

2. **Packaging time** (`c_endpoint_nb.py` step 5b): Compares endpoint
   predictions against training `prediction_results.json`. Warns on
   mismatch so the issue is always visible.

3. **Skill docs** (`haipipe-end-src2input/SKILL.md`,
   `haipipe-end-input2src/SKILL.md`): Roundtrip test with real data is
   REQUIRED in the design and review protocol. Also documented in
   `haipipe-end/ref/0-overview.md` as a first-class invariant.

**Rule:** Every Src2InputFn/Input2SrcFn pair must pass a roundtrip test
on real ModelInstanceStore examples before deployment. Synthetic-only
testing is insufficient — it catches parsing bugs but not data loss bugs.

### L12: code-dev builders must test with real ModelInstanceStore data

**Problem:** Builder scripts in `code-dev/1-PIPELINE/6-Endpoint-WorkSpace/`
are the design-time authoring environment for inference Fns. They wrote
files to `code/haifn/fn_endpoint/` but only tested with hardcoded minimal
inputs. The gap between "builder passes" and "endpoint works" was invisible.

**Fix:** Builder scripts should follow this pattern:

```
Phase 1: AUTHOR  — write the Fn to code/haifn/fn_endpoint/
Phase 2: TEST    — load real example from 5-ModelInstanceStore
                   run full roundtrip with Src2InputFn + Input2SrcFn
                   run PreFn → model.infer() on both original and roundtrip
                   assert predictions match
Phase 3: REPORT  — print table/row/feature/prediction comparison
```

The `f1_roundtrip_test_*.py` script is the Phase 2+3 template.

**Rule:** No Fn is production-ready until it passes Phase 2 on real data.
The builder's quick test (synthetic payload) is necessary but not sufficient.

### L13: Three-layer builder pattern — templates → project → production

**Problem:** Builder scripts lived in `code-dev/1-PIPELINE/6-Endpoint-WorkSpace/`
as a flat directory mixing WellDoc, CGM, and MIMIC builders. No clear separation
between generic templates and project-specific implementations. New projects
had to guess which file to copy.

**Fix — three-layer pattern:**

```
Layer 1: TEMPLATES     code/scripts/haibuilder/6-endpoint/
                       └── canonical WellDoc references (copy-and-customize)

Layer 2: PROJECT       examples/<project>/tasks/C01_*/00_endpoint_set_fn_develop/
                       └── project-specific builders, each as own run
                           (configs/ + runs/ + results/ per builder)

Layer 3: PRODUCTION    code/haifn/fn_endpoint/fn_*/*.py
                       └── generated output (NEVER edit directly)
```

**Workflow:**
1. Copy closest template from Layer 1 → Layer 2
2. Customize the `[CUSTOMIZE]` sections, keep `[BOILERPLATE]` as-is
3. Run builder: `bash runs/run_a1_metafn.sh` → generates Layer 3
4. Builder tests with real ModelInstanceStore data (not synthetic)
5. After all builders pass → run endpoint packaging task (`01_endpoint_*`)

**Task-folder convention:** The `00_endpoint_set_fn_develop` folder follows
/haipipe-task structure: each builder is an independent run with its own
config/run/results. Can run one at a time or all sequentially.

**Rule:** Templates (Layer 1) are WellDoc references — don't modify them.
Project builders (Layer 2) are where customization happens. Production
files (Layer 3) are generated — never hand-edit.

### L14: Every Fn that reads payload must handle `dataframe_records`

**Problem:** `TrigFn` read `payload_input.get('patient_id')` directly.
In Databricks Model Serving, the payload is wrapped:
`{'dataframe_records': [{'patient_id': '...', ...}]}`. TrigFn got empty
strings for all fields → PreFn saw the same empty case for every patient
→ all 6 patients returned the same score (0.5752).

`Input2SrcFn` had the unwrapping (line 94-95), but `TrigFn` did not.
The two Fns see the same `payload_input_json` but handled it differently.

**Fix:** Every Fn that reads from `payload_input` must start with:
```python
if 'dataframe_records' in payload_input and payload_input['dataframe_records']:
    payload_input = payload_input['dataframe_records'][0]
```

Affected Fns: `TrigFn`, `Input2SrcFn`. PostFn is not affected (reads
model output, not payload).

**Rule:** Databricks `dataframe_records` unwrapping is not optional —
it's part of the Fn contract. Builder tests must cover BOTH formats:
```python
# Direct format test
result = TrigFn({'patient_id': '10001', ...})
assert result['HadmID'].iloc[0] == '21001'

# Databricks format test  
result = TrigFn({'dataframe_records': [{'patient_id': '10001', ...}]})
assert result['HadmID'].iloc[0] == '21001'
```

### L15: `02_deploy_local` catches what `00_develop` and `01_endpoint` miss

**Problem:** The `00_develop` builders tested each Fn in isolation (direct
format only). The `01_endpoint` packaging tested inference (direct format
only). Neither tested the Databricks wire format. The bug was invisible
until `02_deploy_local` ran both formats side-by-side and compared.

**The testing pyramid for endpoints:**
```
00_develop    — per-Fn unit tests (direct + Databricks format)
01_endpoint   — integration test (packaging + step 5b reproducibility)
02_deploy     — system test (simulates real deployment wire format)
```

Each layer catches different classes of bugs:
- 00: Fn logic bugs, roundtrip data loss
- 01: packaging bugs, prediction_results.json consistency
- 02: wire format bugs, format unwrapping, end-to-end latency

**Rule:** All three tasks must pass before deploying to cloud. The
`02_deploy_local` task is NOT optional — it's the only one that tests
the exact format the cloud endpoint will receive.

### L16: Fns are platform-agnostic — no Databricks/SageMaker variants

**Problem:** The CGM endpoint had separate Fn files for "Databricks" and
non-Databricks (e.g., `CGMDecoder_Databricks_v260101` vs `CGMDecoder_v260101`).
The only real difference was the `dataframe_records` unwrapping in Input2SrcFn.
This creates maintenance burden — every Fn fix must be applied to two files.

**Root cause:** The Databricks variant was created before L14 established
that ALL Fns must handle both wire formats. Once `dataframe_records`
unwrapping became part of the Fn contract, there is no reason for
platform-specific Fn variants.

**Architecture:**

```
Fns (platform-agnostic, one set)      Deploy wrappers (platform-specific)
├── MetaFn                             ├── platform-databrick-inference/  (MLflow pyfunc)
├── TrigFn                             └── platform-sagemaker-inference/  (Docker + Flask)
├── Input2SrcFn
├── Src2InputFn                        Both call: endpoint_set.inference(payload)
└── PostFn
```

The platform distinction is a **deploy-time** concern, not an Fn-level
concern. The `.tar.gz` Endpoint_Set is the universal handoff artifact:

```
haipipe pipeline → .tar.gz → Databricks (MLflow + UC + Model Serving)
                           → SageMaker  (Docker + ECR + Endpoint)
                           → Local      (direct Python call)
```

**Rule:** Write ONE set of Fns that handle all wire formats. The deploy
platform is chosen at `02_deploy` time, not at `00_develop` Fn authoring
time. The "Databricks" suffix on a Fn name (e.g., `CGMDecoder_Databricks_*`)
indicates this is the variant used for the Databricks-deployed endpoint —
NOT that the Fn itself has Databricks-specific logic.

### L14: D-prefix dictionary tables must not enter examples or payloads

**Problem:** `extract_example_from_source` copied ALL tables from SourceSet
into each example's `ProcName_to_ProcDf/` — including D-prefix dictionary
tables (DRGCode 761K rows, DIcdDiagnoses 112K rows, etc.). These are
full-database lookup tables shared across all patients, not patient data.

Impact:
- Each example: 11MB → should be ~300KB (37x bloat)
- `.tar.gz`: 160MB → should be 14MB (11x bloat)
- Databricks payload: 201MB → rejected (33MB limit)

**Fix:**
1. `extract_example_from_source`: skip `D*` tables (D-prefix + uppercase)
2. `Src2InputFn`: skip `D*` tables during serialization
3. Delete existing D-prefix parquets from ModelInstanceStore examples

**Verification:** No CaseFn reads any D-prefix table. The model uses only
5 tables: Ptt, Admission, LabEvent, ChartEvent, Prescription. Predictions
are identical with or without D-prefix tables (6/6 Databricks smoke test pass).

**Rule:** Before extracting examples, check which tables the CaseFns
actually read. Only store patient-specific clinical tables. Dictionary/
reference tables belong in `external/` (if needed at all), never in
per-patient examples.
