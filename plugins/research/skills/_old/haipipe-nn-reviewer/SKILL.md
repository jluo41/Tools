Skill: haipipe-nn-reviewer
==========================

Two modes — run whichever fits your need:

  **Dashboard mode** (Step 0 only): Scan the full codebase and render a status
  table for all test directories. Use this to decide what to work on next.

  **Review mode** (Steps 1–8): Deep per-model review after the user picks one
  from the dashboard (or names one directly).

**Severity tags (review mode):**
  [BLOCK]  Must fix before the model can run at all
  [ERROR]  Will produce wrong results silently
  [WARN]   Pattern deviation -- works but inconsistent
  [NOTE]   Minor style / documentation gap

---

Step 0: Codebase Status Dashboard
===================================

Run this first — always. Even in review mode, the dashboard tells you the
context around the model you are about to review.

**0a. Discover all test directories**

Use the Glob tool to find every test directory:

  Pattern: `code/hainn/**/test-modeling-*`  (recursive, directories only)

Collect the full path for each result. Group them by family (the segment of
the path immediately after `code/hainn/`):

  mlpredictor, tefm, tsforecast, tediffusion, bandit, (others)

**0b. For each test directory, gather three signals**

For each directory PATH found above:

  Signal 1 — Layers present
    Glob: `PATH/scripts/*_[1234]_*.py`
    Count distinct layer numbers (1, 2, 3, 4) present in filenames.
    Result: e.g. "L1-L4" (all four) or "L1-L2" (only first two)

  Signal 2 — Summary format
    Grep for the string `key_metric` anywhere inside `PATH/scripts/`
    Found in ≥1 file  →  4-col  (canonical)
    Not found          →  2-col  (needs update)

  Signal 3 — Data source
    Grep for `AIDataSet|load_from_disk` in `PATH/scripts/`
    Found  →  AIData  (correct)
    Not found, but grep finds `RecStore|read_parquet`  →  RecStore  (gap)
    Neither found  →  Unknown (scripts may not load data at L1/L2)

**0c. Determine status for each directory**

Apply this decision table:

  ✅ DONE        — L1-L4 present + 4-col + AIData
  🔄 PARTIAL     — L1-L4 present + mix of 4-col and 2-col + AIData
  ⚠️ NEEDS UPDATE — L1-L4 present + 2-col + AIData  (just formatting work)
  📋 L1/L2 ONLY  — Only L1-L2 present (missing L3/L4 — engineering gap)
  ❌ BLOCKED     — L1-L4 present but RecStore load, OR architectural gap noted
                   in a TODO_*.md file in the directory

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
re-run the discovery commands above to get the live current state — the
table will drift as models are updated.

**0e. Print navigation paths**

After the table, print the absolute path to each test directory so the user
can click to open it directly:

```
PATHS
─────
mlpredictor / SLearner XGBoost
  code/hainn/mlpredictor/models/test-modeling-mlpredictor-slearner-xgboost/

mlpredictor / TLearner XGBoost
  code/hainn/mlpredictor/models/test-modeling-mlpredictor-tlearner-xgboost/

mlpredictor / BasePredictor XGBoost
  code/hainn/mlpredictor/models/test-modeling-mlpredictor-basepredictor-xgboost/

tefm / TE-CLM
  code/hainn/tefm/models/te_clm/test-modeling-ts_clm/

tefm / TE-MLM
  code/hainn/tefm/models/te_mlm/test-modeling_te_mlm/

tefm / TE-CLM-tod
  code/hainn/tefm/models/te_clm/test-modeling-ts_clm_tod/

tefm / TE-CLM-num
  code/hainn/tefm/models/te_clm/test-modeling-ts_clm_num/

tefm / TE-CLM-event
  code/hainn/tefm/models/te_clm/test-modeling-te_clm_event/

tefm / TE-MM
  code/hainn/tefm/models/te_mm/test-modeling-ts_mm/

tefm / TE-CTEP
  code/hainn/tefm/models/te_ctep/test-modeling-ctep/

tsforecast / MLForecast XGBoost
  code/hainn/tsforecast/models/mlforecast/test-modeling-nixtla_xgboost/

tsforecast / MLForecast LightGBM
  code/hainn/tsforecast/models/mlforecast/test-modeling-nixtla_lightgbm/

tsforecast / NeuralForecast NHits
  code/hainn/tsforecast/models/neuralforecast/test-modeling-nixtla_nhits/

tsforecast / NeuralForecast NBeats
  code/hainn/tsforecast/models/neuralforecast/test-modeling-nixtla_nbeats/

tsforecast / NeuralForecast Autoformer
  code/hainn/tsforecast/models/neuralforecast/test-modeling-nixtla_autoformer/

tsforecast / NeuralForecast DLinear
  code/hainn/tsforecast/models/neuralforecast/test-modeling-nixtla_dlinear/

tsforecast / NeuralForecast PatchTST
  code/hainn/tsforecast/models/neuralforecast/test-modeling-nixtla_patchtst/

tsforecast / NeuralForecast TFT
  code/hainn/tsforecast/models/neuralforecast/test-modeling-nixtla_tft/

tsforecast / NeuralForecast VanillaTransformer
  code/hainn/tsforecast/models/neuralforecast/test-modeling-nixtla_vanillatransformer/

tediffusion / GlucoStatCond
  code/hainn/tediffusion/models/glucostaticonddiffusion/test-modeling-glucostaticonddiffusion/

bandit / BanditV1
  code/hainn/bandit/test-modeling-bandit/
```

**0f. Suggest the next action**

After the table and paths, recommend what to work on next using this priority:

  1. ⚠️ NEEDS UPDATE directories first — pure formatting work, low risk, high ROI
     (Recommended order: BasePredictor L1/L2/L3, TE-CLM, TE-MLM, TSForecast XGBoost)
  2. 📋 L1/L2 ONLY — building L3/L4 is real engineering; ask user before starting
  3. ❌ BLOCKED — do not attempt until the blocker is resolved; refer to TODO_*.md

Then ask: "Which model would you like to review in depth? (Or type 'update' to
start updating the next NEEDS UPDATE directory.)"

**0g. Fill in slots for per-model review (if user selects a model)**

Once the user picks a model, fill in these slots using discovered paths above.
All steps 1–8 below use these:

```
FAMILY             = "..."    # e.g., tsforecast, mlpredictor, tefm
MODEL_TYPE_STRING  = "..."    # MODEL_TYPE value in Instance class
INSTANCE_FILE      = "code/hainn/<family>/instance_<name>.py"
CONFIG_FILE        = "code/hainn/<family>/configuration_<name>.py"
TUNER_FILE         = "code/hainn/<family>/models/tuner_<name>.py"
ALGORITHM_FILE     = "code/hainn/<family>/models/algorithm_<name>.py"  # or N/A
YAML_FILE          = "config/.../my_model.yaml"
TEST_DIR           = "code/hainn/<family>/test-modeling-<name>/"
```

---

Step 1: Review the YAML Config
================================

**Load skill: haipipe-nn-0-overview**
Read the "YAML Config Templates" section and "Complete Model Registry" section.

Then check:

  [ ] ModelInstanceClass is present and matches MODEL_TYPE_STRING exactly
      (or a known alias listed in haipipe-nn-0-overview's registry table)
      [BLOCK if missing or unregistered]
  [ ] modelinstance_version starts with @ (e.g., '@v0001-my-model')
      [WARN if bare 'v0001-my-model' without @]
  [ ] model_tuner_name value exactly matches the Tuner class name
      [BLOCK if typo -- Instance registry lookup will KeyError]
  [ ] Required top-level keys present:
        ModelInstanceClass, ModelArgs, TrainingArgs, InferenceArgs,
        EvaluationArgs, aidata_name, aidata_version,
        modelinstance_name, modelinstance_version
  [ ] No unresolved @ YAML references left in the file

```bash
cat <YAML_FILE>
```

---

Step 2: Review the Tuner (Layer 2)
====================================

**Load skill: haipipe-nn-2-tuner**
Apply its MUST DO checklist and MUST NOT checklist in full.

Additional checks (cross-verify against YAML):

  [ ] Tuner class name in the file matches model_tuner_name in YAML exactly
  [ ] domain_format class attribute is set (not the default "base")
  [ ] save_model uses model_{key} naming (e.g., model_MAIN/, model_MAIN.json)
      NOT {key}_model -- [ERROR if inverted; from_pretrained will fail]

```bash
# Verify save_model naming convention:
grep -n "model_\|os\.path\.join" <TUNER_FILE> | grep -i "save\|load"
# Should show:  f'model_{key}' or os.path.join(model_dir, f'model_{key}')
```

  [ ] __init__ passes **kwargs to super().__init__()
      [ERROR if missing -- model-specific args silently lost]

---

Step 3: Review the Instance (Layer 3)
=======================================

**Load skill: haipipe-nn-3-instance**
Apply its MUST DO checklist, MUST NOT list, and infer() routing contract.

Additional checks:

  [ ] MODEL_TYPE in Instance exactly matches the ModelInstanceClass string
      used in the YAML
  [ ] _load_model_base() calls self.init() BEFORE calling tuner.load_model()
      [BLOCK if missing -- Tuner shells don't exist when load is attempted]
  [ ] infer() output follows the routing contract from haipipe-nn-3-instance:
        Single input  → pd.DataFrame
        Multi-split   → {split_name: pd.DataFrame}
  [ ] No algorithm library imports (torch, xgboost, sklearn, etc.) at the
      module level or inside any method
      [ERROR -- violates layer boundary]

---

Step 4: Review the Config (Layer 3)
=====================================

**Load skill: haipipe-nn-3-instance**
Read the "Config Class Contract" section, including from_aidata_set() and
from_yaml() requirements.

  [ ] from_yaml() is implemented (base class raises NotImplementedError)
      [BLOCK if missing]
  [ ] from_aidata_set() builds modelinstance_set_name as f"{name}/{version}"
      where version already contains the @ prefix
  [ ] Config dataclass has all 4 required Dict fields:
        ModelArgs, TrainingArgs, InferenceArgs, EvaluationArgs
      [ERROR if any missing]

```bash
# Quick import + from_yaml smoke test:
python -c "
from hainn.<family>.configuration_<name> import <ConfigClass>
config = <ConfigClass>.from_yaml('<YAML_FILE>')
print('ModelArgs:', config.ModelArgs)
print('model_tuner_name:', config.ModelArgs.get('model_tuner_name'))
print('CONFIG SMOKE TEST PASSED')
"
```
  [ ] Smoke test passes
      [BLOCK if fails]

---

Step 5: Review the Algorithm (Layer 1)
========================================

Skip this step if no custom algorithm_*.py was created (external library only).

**Load skill: haipipe-nn-0-overview**
Read the "Layer 1: Algorithm" description in the architecture diagram.

  [ ] nn.Module subclass with forward(x) -> y implemented
  [ ] Contains ONLY architecture logic -- no training loops, no data loading
      [ERROR if training logic present]
  [ ] Does not import anything from hainn.* or haipipe.*
      [ERROR -- circular imports]
  [ ] Named <ComponentName>Algorithm (e.g., TECLMAlgorithm)

---

Step 6: Cross-Layer Consistency
=================================

These checks span multiple files. No single skill covers all of them.

**6a. YAML → Registry → Instance → Config chain**

```bash
python -c "
from hainn.model_registry import load_model_instance_class
cls, cfg = load_model_instance_class('<MODEL_TYPE_STRING>')
print('Instance:', cls.__name__)
print('Config:  ', cfg.__name__)
"
```
  [ ] Resolves without ImportError or KeyError
      [BLOCK if fails]
  [ ] cls.__name__ matches INSTANCE_FILE class name
  [ ] cfg.__name__ matches CONFIG_FILE class name

**6b. YAML → Instance → Tuner chain**

```bash
python -c "
# Simulate what Instance.init() does
import importlib
# Get the registry from the Instance file:
from hainn.<family>.instance_<name> import MODEL_TUNER_REGISTRY
tuner_name = '<model_tuner_name_from_yaml>'
module_path = MODEL_TUNER_REGISTRY[tuner_name]
module = importlib.import_module(module_path)
tuner_cls = getattr(module, tuner_name)
print('Tuner:', tuner_cls)
print('domain_format:', tuner_cls.domain_format)
"
```
  [ ] Resolves without error
      [BLOCK if KeyError -- tuner name not in registry]
  [ ] domain_format is set and meaningful (not "base")

**6c. save_model / load_model key consistency**

```bash
grep -n "save_model\|load_model" <INSTANCE_FILE>
```
  [ ] Same key string (e.g., 'MAIN') used in both _save_model_base
      and _load_model_base
  [ ] Key matches what Tuner's save_model(key, ...) will create
      (e.g., 'MAIN' → model_MAIN/ directory)

**6d. YAML TrainingArgs flow**

```bash
grep -n "TrainingArgs" <INSTANCE_FILE>
```
  [ ] fit() reads `TrainingArgs = TrainingArgs or self.config.TrainingArgs`
      (pipeline passes no TrainingArgs; Instance must fall back to config)
      [ERROR if missing -- training will use empty/None args]

**6e. modelinstance_set_name format**

```bash
grep -n "modelinstance_set_name\|modelinstance_version" <CONFIG_FILE>
```
  [ ] from_aidata_set builds set_name as f"{name}/{version}"
      (NOT f"{name}/@{version}" -- that would double the @)
  [ ] Default modelinstance_version parameter is '@v0001' (with @)

---

Step 7: Test Run Sequence
==========================

Run in this order. Fix failures before proceeding to the next layer.

```bash
source .venv/bin/activate && source env.sh

# (optional) Layer 1 -- only for custom nn.Module
python <TEST_DIR>/scripts/test_<name>_1_algorithm.py

# Layer 2 -- Tuner in isolation
python <TEST_DIR>/scripts/test_<name>_2_tuner.py

# Layer 3 -- Instance orchestration
python <TEST_DIR>/scripts/test_<name>_3_instance.py

# Layer 4 -- Full ModelInstance_Set packaging
python <TEST_DIR>/scripts/test_<name>_4_modelset.py
```

For what each test script should verify, load the relevant skill:
- Layer 2 test structure → **haipipe-nn-2-tuner** "Test Notebook: What Layer 2 Tests"
- Layer 3 test structure → **haipipe-nn-3-instance** "Test Notebook: What Layer 3 Tests"
- Layer 4 test structure → **haipipe-nn-4-modelset** "Test Notebook: What Layer 4 Tests"

---

Step 8: Sign-Off
=================

Complete this table. PASS requires all rows green.

```
Area             Check                                             Status
──────────────   ───────────────────────────────────────────────   ──────
YAML             ModelInstanceClass registered + @ in version       [ ]
YAML             model_tuner_name resolves to Tuner class           [ ]
L2 Tuner         5 abstract methods + transform_fn standalone       [ ]
L2 Tuner         save_model uses model_{key} naming                 [ ]
L3 Instance      5 abstract methods + MODEL_TYPE set                [ ]
L3 Instance      _load_model_base calls init() first                [ ]
L3 Instance      infer() routing contract (single/multi → correct)  [ ]
L3 Config        from_yaml implemented (not NotImplementedError)    [ ]
L3 Config        4 required Dict fields present                     [ ]
L3 Registry      import smoke test passes                           [ ]
L1 Algorithm     No training logic, no hainn imports (if custom)    [ ]
X-layer          YAML→Registry→Instance chain verified              [ ]
X-layer          YAML→Tuner chain verified                          [ ]
X-layer          save/load key consistent across Instance+Tuner     [ ]
X-layer          TrainingArgs fallback to self.config in fit()      [ ]
Tests            Layer 2 test: all steps PASSED                     [ ]
Tests            Layer 3 test: all steps PASSED                     [ ]
Tests            Layer 4 test: all steps PASSED                     [ ]
```

**PASS**: Zero [BLOCK] or [ERROR] issues. All test layers green.
**WARN-PASS**: Zero [BLOCK]/[ERROR]. Some [WARN]/[NOTE] -- document and proceed.
**FAIL**: Any [BLOCK] or [ERROR], or any test layer failing.

---

Quick Error Lookup
==================

Error seen                               Most likely cause
───────────────────────────────────────  ─────────────────────────────────────────────────────
ImportError on registry lookup           Registry elif block missing, or module path typo in it
NotImplementedError from from_yaml       Config class missing from_yaml() override
AttributeError: model_base has no key   _load_model_base() missing self.init() call before load
KeyError on model_tuner_name             Tuner not in Instance registry; name typo in YAML
FileNotFoundError on load_model          save_model used {key}_model vs correct model_{key}
infer() returns raw dict not DataFrame   Instance.infer() missing output routing / conversion
set_name has @@ double prefix            from_aidata_set still has /@{version} pattern
fit() ignores TrainingArgs               fit() not doing `TrainingArgs or self.config.TrainingArgs`
Weights mismatch after roundtrip         Key mismatch between _save_model_base and _load_model_base
AssertionError: model_base == {}         init() not populating self.model_base dict

---

See Also
========

Skills actively used by this reviewer:
- **haipipe-nn-0-overview**: Architecture map, registry, YAML templates
- **haipipe-nn-2-tuner**: Tuner MUST DO / MUST NOT checklists
- **haipipe-nn-3-instance**: Instance + Config MUST DO checklists, infer() routing
- **haipipe-nn-4-modelset**: Pipeline flow, packaging, Layer 4 test structure
