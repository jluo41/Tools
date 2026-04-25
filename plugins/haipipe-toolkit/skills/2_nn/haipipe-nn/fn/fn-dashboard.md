fn-dashboard: Codebase Status Dashboard
=========================================

Two modes -- run whichever fits your need:

  **Dashboard mode** (Step 0 only): Scan the full codebase and render a status
  table for all test directories. Use this to decide what to work on next.

  **Review mode** (Steps 1-8 in fn-review.md): Deep per-model review after
  the user picks one from the dashboard (or names one directly).

**Severity tags (review mode):**
  [BLOCK]  Must fix before the model can run at all
  [ERROR]  Will produce wrong results silently
  [WARN]   Pattern deviation -- works but inconsistent
  [NOTE]   Minor style / documentation gap

---

Step 0: Codebase Status Dashboard
===================================

Run this first -- always. Even in review mode, the dashboard tells you the
context around the model you are about to review.

**0a. Discover all test directories**

Use the Glob tool to find every test directory:

  Pattern: `code/hainn/**/test-modeling-*`  (recursive, directories only)

Collect the full path for each result. Group them by family (the segment of
the path immediately after `code/hainn/`):

  mlpredictor, tefm, tsforecast, tediffusion, bandit, (others)

**0b. For each test directory, gather three signals**

For each directory PATH found above:

  Signal 1 -- Layers present
    Glob: `PATH/*_[1234]_*.py`
    Count distinct layer numbers (1, 2, 3, 4) present in filenames.
    Result: e.g. "L1-L4" (all four) or "L1-L2" (only first two)

    IMPORTANT: Some older test directories use non-numbered script names
    (e.g., test_nhits_algorithm.py, test_nhits_tuner.py) that do NOT match
    the glob pattern. For these directories, also check for keyword patterns:
      Glob: `PATH/*algorithm*.py`  -> present means L1 exists
      Glob: `PATH/*tuner*.py`      -> present means L2 exists
    If numbered scripts are missing but keyword scripts exist, record
    the layer set from keyword detection and flag the directory as having
    a naming gap (scripts need to be renamed to *_1_*, *_2_*, etc.).

  Signal 2 -- Summary format
    Grep for the string `key_metric` anywhere inside `PATH/`
    Found in >=1 .py file  ->  4-col  (canonical)
    Not found              ->  2-col  (needs update)

  Signal 3 -- Data source
    Grep for `AIDataSet|load_from_disk` in `PATH/*.py`
    Found  ->  AIData  (correct)
    Not found, but grep finds `RecStore|read_parquet`  ->  RecStore  (gap)
    Neither found  ->  Unknown (scripts may not load data at L1/L2)

**0c. Determine status for each directory**

Apply this decision table:

  DONE        -- L1-L4 present + 4-col + AIData
  PARTIAL     -- L1-L4 present + mix of 4-col and 2-col + AIData
  NEEDS UPDATE -- L1-L4 present + 2-col + AIData  (just formatting work)
  L1/L2 ONLY  -- Only L1-L2 present (missing L3/L4 -- engineering gap)
               NOTE: includes dirs where L1/L2 detected via keyword glob
               (non-numbered names) -- these also need script renaming
  BLOCKED     -- L1-L4 present but RecStore load, OR architectural gap noted
                 in a TODO_*.md file in the directory
  NO SCRIPTS  -- zero script files found at all (new/empty directory)

**0d. Render the dashboard**

Print this table (fill in real values from signals above):

```
HAIPIPE-NN STATUS DASHBOARD
============================

 Family         Model                    Layers   4-col   AIData   Status
 ─────────────  ───────────────────────  ───────  ──────  ───────  ──────────────────
 mlpredictor    SLearner XGBoost         L1-L4    ✅      ✅       ✅ DONE
 mlpredictor    TLearner XGBoost         L1-L4    ✅      ✅       ✅ DONE
 mlpredictor    BasePredictor XGBoost    L1-L4    🔄      ✅       🔄 PARTIAL
 tefm           TE-CLM                   L1-L4    ❌      ✅       ⚠️ NEEDS UPDATE
 tefm           TE-MLM                   L1-L4    ❌      ✅       ⚠️ NEEDS UPDATE
 tefm           TE-CLM-tod               L1-L2    ❌      ?        📋 L1/L2 ONLY
 tefm           TE-CLM-num               L1-L2    ❌      ?        📋 L1/L2 ONLY
 tefm           TE-CLM-event             L1-L2    ❌      ?        📋 L1/L2 ONLY
 tefm           TE-MM                    L1-L2    ❌      ?        📋 L1/L2 ONLY
 tefm           TE-CTEP                  L1-L2    ❌      ?        📋 L1/L2 ONLY
 tsforecast     MLForecast XGBoost       L1-L4    ❌      ✅       ⚠️ NEEDS UPDATE
 tsforecast     MLForecast LightGBM      L1-L2    ❌      ?        📋 L1/L2 ONLY
 tsforecast     NeuralForecast NHits     L1-L2    ❌      ?        📋 L1/L2 ONLY
 tsforecast     NeuralForecast NBeats    L1-L2    ❌      ?        📋 L1/L2 ONLY
 tsforecast     NeuralForecast Autoformer L1-L2   ❌      ?        📋 L1/L2 ONLY
 tsforecast     NeuralForecast DLinear   L1-L2    ❌      ?        📋 L1/L2 ONLY
 tsforecast     NeuralForecast PatchTST  L1-L2    ❌      ?        📋 L1/L2 ONLY
 tsforecast     NeuralForecast TFT       L1-L2    ❌      ?        📋 L1/L2 ONLY
 tsforecast     NeuralForecast VanillaTr L1-L2    ❌      ?        📋 L1/L2 ONLY
 tediffusion    GlucoStatCond            L1-L4    ❌      ❌       ❌ BLOCKED
 bandit         BanditV1                 L2 only  ❌      ❌       ❌ BLOCKED

 Legend:  ✅ canonical   ❌ needs work   🔄 partial   ? not applicable at L1/L2
```

NOTE: The table above is a starting snapshot (as of 2026-02-22). Always
re-run the discovery commands above to get the live current state -- the
table will drift as models are updated.

**0e. Print navigation paths**

After the table, print the absolute path to each test directory so the user
can click to open it directly:

```
PATHS
─────
mlpredictor / SLearner XGBoost
  code/hainn/tuner/mlpredictor/test-modeling-mlpredictor-slearner-xgboost/

mlpredictor / TLearner XGBoost
  code/hainn/tuner/mlpredictor/test-modeling-mlpredictor-tlearner-xgboost/

mlpredictor / BasePredictor XGBoost
  code/hainn/tuner/mlpredictor/test-modeling-mlpredictor-basepredictor-xgboost/

tefm / TE-CLM
  code/hainn/tuner/tefm/te_clm/test-modeling-ts_clm/

tefm / TE-MLM
  code/hainn/tuner/tefm/te_mlm/test-modeling_te_mlm/

tefm / TE-CLM-tod
  code/hainn/tuner/tefm/te_clm/test-modeling-ts_clm_tod/

tefm / TE-CLM-num
  code/hainn/tuner/tefm/te_clm/test-modeling-ts_clm_num/

tefm / TE-CLM-event
  code/hainn/tuner/tefm/te_clm/test-modeling-te_clm_event/

tefm / TE-MM
  code/hainn/tuner/tefm/te_mm/test-modeling-ts_mm/

tefm / TE-CTEP
  code/hainn/tuner/tefm/te_ctep/test-modeling-ctep/

tsforecast / MLForecast XGBoost
  code/hainn/tuner/tsforecast/mlforecast/test-modeling-nixtla_xgboost/

tsforecast / MLForecast LightGBM
  code/hainn/tuner/tsforecast/mlforecast/test-modeling-nixtla_lightgbm/

tsforecast / NeuralForecast NHits
  code/hainn/tuner/tsforecast/neuralforecast/test-modeling-nixtla_nhits/

tsforecast / NeuralForecast NBeats
  code/hainn/tuner/tsforecast/neuralforecast/test-modeling-nixtla_nbeats/

tsforecast / NeuralForecast Autoformer
  code/hainn/tuner/tsforecast/neuralforecast/test-modeling-nixtla_autoformer/

tsforecast / NeuralForecast DLinear
  code/hainn/tuner/tsforecast/neuralforecast/test-modeling-nixtla_dlinear/

tsforecast / NeuralForecast PatchTST
  code/hainn/tuner/tsforecast/neuralforecast/test-modeling-nixtla_patchtst/

tsforecast / NeuralForecast TFT
  code/hainn/tuner/tsforecast/neuralforecast/test-modeling-nixtla_tft/

tsforecast / NeuralForecast VanillaTransformer
  code/hainn/tuner/tsforecast/neuralforecast/test-modeling-nixtla_vanillatransformer/

tediffusion / GlucoStatCond
  code/hainn/tuner/tediffusion/glucostaticonddiffusion/test-modeling-glucostaticonddiffusion/

bandit / BanditV1
  code/hainn/tuner/bandit/test-modeling-bandit/
```

**0f. Suggest the next action**

After the table and paths, recommend what to work on next using this priority:

  1. NEEDS UPDATE directories first -- pure formatting work, low risk, high ROI
     (Recommended order: BasePredictor L1/L2/L3, TE-CLM, TE-MLM, TSForecast XGBoost)
  2. L1/L2 ONLY -- building L3/L4 is real engineering; ask user before starting
  3. BLOCKED -- do not attempt until the blocker is resolved; refer to TODO_*.md

Then ask: "Which model would you like to review in depth? (Or type 'update' to
start updating the next NEEDS UPDATE directory.)"

**0g. Fill in slots for per-model review (if user selects a model)**

Once the user picks a model, fill in these slots using discovered paths above.
All steps in fn-review.md use these:

```
FAMILY             = "..."    # e.g., tsforecast, mlpredictor, tefm
MODEL_TYPE_STRING  = "..."    # MODEL_TYPE value in Instance class
INSTANCE_FILE      = "code/hainn/instance/<family>/instance_<name>.py"
CONFIG_FILE        = "code/hainn/instance/<family>/configuration_<name>.py"
TUNER_FILE         = "code/hainn/tuner/<family>/tuner_<name>.py"
ALGORITHM_FILE     = "code/hainn/algo/<family>/algorithm_<name>.py"  # or N/A
YAML_FILE          = "config/.../my_model.yaml"
TEST_DIR           = "code/hainn/tuner/<family>/test-modeling-<name>/"
```
