fn-test: Test Protocol
=======================

How to write, run, and fix tests for any layer of the 4-layer NN pipeline.

---

Universal 7-Step Test Structure
=================================

ALL test scripts (L1 through L4) follow this same 7-step structure.
Only the labels for Steps 5-6 differ by layer (see table below).

```
Step 1: Load config
        display_df with key architecture params
        (vocab_size, seq_len, model_class, n_estimators, etc.)

Step 2: Load real AIData
        AIDataSet.load_from_disk(...)  -- NEVER synthetic data
        print(aidata) to show dataset schema + split sizes
        print(aidata.dataset_dict['train'][0]) to show one row

Step 3: Create model from config
        display_df with model class name, param count (or n_estimators)

Step 4: Prepare / transform data
        4a: Tokenizer / preprocessor setup (display_df)
            For tree models: feature column discovery
        4b: Design and validate transform_fn -- BEFORE/AFTER pattern
            print(raw_data[0])  -- before
            -> run transform_fn ->
            print(transformed[0])  -- after
            sample_input_row = transformed[0]   (captured for Step 7)
        4c: Verify token/feature ranges (assertions + display_df)

Step 5: <Layer-specific label -- see table below>
        print(input_batch) before calling model
        -> call model ->
        display_df with result (loss, predictions, shape, time)

Step 6: <Layer-specific label -- see table below>
        sample_output_row = {...}  (capture key metric values for Step 7)
        display_df with result

Step 7: Save / load roundtrip
        Save to _WorkSpace/5-ModelInstanceStore/{name}/{version}/
        Reload from the same path
        Verify weight_delta == 0.0 (or prediction_delta == 0.0)
        CAVEAT: stochastic models (diffusion, dropout-enabled NN at eval)
        will not produce == 0.0. For these, call model.eval() before both
        forward passes, or assert weight_delta == 0.0 only (weights must
        match even if outputs don't due to sampling noise).
        display_df with weight_delta, cfg_match
```

**Layer-specific labels for Steps 5 and 6:**

```
Layer   Step 5 label        Step 6 label
──────  ──────────────────  ─────────────────────
L1      Forward pass        Gradient flow verify
L2      Fit                 Infer
L3      Fit                 Infer
L4      Fit (full run)      Infer (full run)
```

---

4-Column Summary Table (Canonical Format)
==========================================

Every test script must print a 4-column table at the end of each step.
This is the "4-col" format checked by fn-dashboard Signal 2.

```python
display_df([
    {"step": "1_config",   "status": "PASS", "key_metric": n_estimators,  "artifact": "config loaded"},
    {"step": "2_aidata",   "status": "PASS", "key_metric": n_train_rows,  "artifact": "AIData loaded"},
    {"step": "3_model",    "status": "PASS", "key_metric": n_model_params,"artifact": "model created"},
    {"step": "4_prepare",  "status": "PASS", "key_metric": n_features,    "artifact": "transform_fn ok"},
    {"step": "5_fit",      "status": "PASS", "key_metric": train_loss,    "artifact": "model trained"},
    {"step": "6_infer",    "status": "PASS", "key_metric": rmse,          "artifact": "predictions ok"},
    {"step": "7_save",     "status": "PASS", "key_metric": weight_delta,  "artifact": model_dir},
])
# step 1 key_metric: config-level hyperparams (n_estimators, seq_len, hidden_size, etc.)
# step 3 key_metric: actual model object param count (different from config-level params)
```

Rules:
  - key_metric MUST be a numeric value (not "N/A", not a string)
  - step names use format: "<number>_<label>" (e.g., "5_fit", "6_infer")
  - status: "PASS" | "FAIL" | "SKIP"
  - artifact: path, object name, or short human-readable string
  - Print the table using display_df() (imported from haipipe or local util)

**2-col format (old, needs update):**

```python
# Only has step + status -- lacks key_metric and artifact
# fn-dashboard flags this as "NEEDS UPDATE"
display_df([{"step": "1_config", "status": "PASS"}, ...])
```

---

Script Naming Convention
=========================

```
test_<model_name>_1_algorithm.py   -- Layer 1 (skip if no custom algorithm)
test_<model_name>_2_tuner.py       -- Layer 2
test_<model_name>_3_instance.py    -- Layer 3  (may have _realdata suffix)
test_<model_name>_4_modelset.py    -- Layer 4
```

The number in the filename is what fn-dashboard's Signal 1 detects with:
  Glob: `PATH/scripts/*_[1234]_*.py`

If you name a file `test_foo_instance.py` (no number), it won't appear
in Signal 1 and the directory will look like "L1/L2 ONLY".

---

Where Test Scripts Live
========================

```
code/hainn/<family>/models/test-modeling-<name>/
  scripts/
    test_<name>_1_algorithm.py
    test_<name>_2_tuner.py
    test_<name>_3_instance.py      (or test_<name>_3_instance_realdata.py)
    test_<name>_4_modelset.py
  config/
    config_<name>_smoke.yaml       (minimal YAML for the test run)
```

For config path: use a relative path or env-var-based path so the test
can be run from any working directory after `source env.sh`.

---

How to Run Tests
=================

Always activate the virtual environment first:

```bash
source .venv/bin/activate && source env.sh
```

NOTE: source .venv/bin/activate does NOT persist across Bash tool calls.
Always chain: source .venv/bin/activate && source env.sh && python <script>
Or call venv Python directly: .venv/bin/python script.py

```bash
# Run a single layer
source .venv/bin/activate && source env.sh && python code/hainn/<family>/models/test-modeling-<name>/scripts/test_<name>_2_tuner.py

# Run all layers in sequence (bottom-up)
source .venv/bin/activate && source env.sh && python code/hainn/<family>/models/test-modeling-<name>/scripts/test_<name>_2_tuner.py
source .venv/bin/activate && source env.sh && python code/hainn/<family>/models/test-modeling-<name>/scripts/test_<name>_3_instance.py
source .venv/bin/activate && source env.sh && python code/hainn/<family>/models/test-modeling-<name>/scripts/test_<name>_4_modelset.py
```

Fix L2 failures before running L3. Fix L3 failures before running L4.

---

Layer-Specific Notes
=====================

**L1 (Algorithm) test -- ref/layer-1-algorithm.md:**
  - Step 4b is the most important: this is where transform_fn is DESIGNED
  - Once validated here, move the final transform_fn into tuner_<name>.py
  - Step 5 = "Forward pass" (not Fit)
  - Step 6 = "Gradient flow verify" -- check grad coverage + params changed
  - sample_output_row = {'loss': loss.item(), 'grad_params': n_updated}

**L2 (Tuner) test -- ref/layer-2-tuner.md:**
  - Tests the Tuner with real AIData, no Instance wrapper
  - Step 4 converts AIData to domain_format (nixtla, sparse, tensor, etc.)
  - Step 5 (Fit): call tuner.fit(dataset, TrainingArgs); capture train_loss
  - Step 6 (Infer): call tuner.infer(dataset, InferenceArgs); capture rmse
  - Step 7: call tuner.save_model(key, dir), tuner.load_model(key, dir)

**L3 (Instance) test -- ref/layer-3-instance.md:**
  - Tests the Instance orchestrator via instance.fit() and instance.infer()
  - Verify infer() returns pd.DataFrame (single) or dict of DataFrames (splits)
  - Verify _load_model_base calls init() first (check model_base is not empty)
  - Step 6 key_metric: a real numeric score (e.g., AUC, RMSE, accuracy)

**L4 (ModelSet) test -- ref/layer-4-modelset.md:**
  - Tests the full packaging pipeline (ModelInstance_Pipeline + ModelInstance_Set)
  - 7a: run_versions list -- verify all runs execute in order
  - 7b: versioned save -- verify manifest.json written alongside model
  - 7c: reload from ModelInstance_Set -- verify auto-detection works
  - 7d: prediction from loaded set -- verify outputs match pre-save outputs
  - key_metric at Step 7 = prediction_delta (should be 0.0 for deterministic models)

---

AIData Source
==============

ALWAYS use real AIData from _WorkSpace/4-AIDataStore/. Never use synthetic data.

```python
import os
from haipipe.aidata_base.aidata_set import AIDataSet

SPACE = os.environ.get('SPACE', '.')

# CORRECT -- use path= and SPACE=
aidata = AIDataSet.load_from_disk(
    path='_WorkSpace/4-AIDataStore/Demo_Small_AIData/@v0001',
    SPACE=SPACE
)
print(aidata)                           # shows splits + schema
print(aidata.dataset_dict['train'][0])  # shows one row

# WRONG -- these arguments are NOT supported:
# AIDataSet.load_from_disk(set_name='...', store_key='...')
```

The AIData name and version come from the test config YAML:
  aidata_name: "Demo_Small_AIData"
  aidata_version: "@v0001"

Build the path from config:
  path = f"_WorkSpace/4-AIDataStore/{config.aidata_name}/{config.aidata_version}"

---

Common Failures and Fixes
===========================

```
Failure                               Fix
────────────────────────────────────  ────────────────────────────────────────────
ImportError: no module named 'hainn'  Activate .venv: source .venv/bin/activate
FileNotFoundError on AIData load      Run source env.sh to set LOCAL_AIDATA_STORE
display_df not found                  Add at top of script: from hainn.utils import display_df
                                      OR define locally: display_df = lambda rows: pd.DataFrame(rows)
key_metric is "N/A" in table          Replace string with actual numeric value
Step 7 weight_delta != 0.0            Key mismatch in save_model/load_model
Steps 1-4 pass, Step 5 crashes        transform_fn incompatible with domain_format
Script not found by fn-dashboard      Add layer number to filename: test_foo_2_...
4-col test reports 2-col in dashboard Missing key_metric/artifact columns in table
AssertionError on feature count       AIData version mismatch or wrong split used
```

---

Updating from 2-col to 4-col
==============================

If fn-dashboard shows "NEEDS UPDATE" (2-col format), the fix is:

1. Read the existing test script
2. Find the summary display_df call (usually at the end of each step)
3. Add key_metric and artifact columns with real numeric values
4. Re-run the script to confirm it passes
5. Re-run fn-dashboard to confirm the signal changes to 4-col

The actual result values (loss, rmse, etc.) should already be computed
by the script -- just capture them and put them in the table.

Do NOT change the test logic. Only update the summary display.
