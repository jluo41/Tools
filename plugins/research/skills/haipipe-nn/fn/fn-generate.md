fn-generate: Code Generation Protocol
=======================================

This file tells you WHERE to write and WHAT to write at each layer.
It does not paste full code templates -- Claude Code will write the actual
code using the ref/*.md files as the specification.

---

Decision Tree: Which Layers Need New Code?
===========================================

Start here when asked to "add a new model" or "generate Layer N code":

```
Is this a pure external library (XGBoost, sklearn, Nixtla)?
  YES -> Skip Layer 1 (no algorithm file needed)
  NO  -> Write Layer 1 algorithm_<name>.py (custom nn.Module)

For all models:
  Write Layer 2:  tuner_<name>.py
  Write Layer 3:  instance_<name>.py + configuration_<name>.py
  Write Layer 4:  test scripts (generated) + YAML config
```

If user asks for a SPECIFIC layer only (e.g., `/haipipe-nn generate L2`),
generate only that layer and note what the adjacent layers must provide.

---

Before Writing Anything
========================

1. Identify the model family: mlpredictor | tefm | tsforecast | tediffusion
2. Choose a canonical reference implementation to imitate:
   - mlpredictor: instance_slearner.py + tuner_xgboost.py
   - tsforecast:  instance_tsforecast.py + models/neuralforecast/tuner_nhits.py
   - tefm:        instance_tefm.py + models/te_clm/tuner_ts_clm.py
3. Read ref/overview.md for the model registry format and YAML template
4. Read the ref/layer-N.md for each layer you will generate

---

Layer 1: Algorithm File (skip if external library)
====================================================

**Only write this if** the model needs a custom nn.Module (e.g., adding
embeddings, fusion layers, or a specialized forward pass on top of HuggingFace).

**WHERE to write:**

```
code/hainn/<family>/models/<variant>/algorithm_<name>.py
```

**WHAT to write (per ref/layer-1-algorithm.md):**

  - One or more nn.Module subclasses named <ComponentName>Algorithm
  - Only imports: torch, torch.nn, other algorithm_*.py files
  - Implements forward() as primary interface
  - No training loops, no data loading, no hainn.* imports
  - Inheritance chain allowed (e.g., base -> +ToD -> +Events)

**Reference:** ref/layer-1-algorithm.md "When You Write Custom Layer 1 Code"
**Example to read first:**
  code/hainn/tefm/models/te_clm/algorithm_ts_clm.py
  code/hainn/tefm/models/te_clm/algorithm_ts_clm_tod.py

---

Layer 2: Tuner File
====================

**WHERE to write:**

```
code/hainn/<family>/models/<variant>/tuner_<name>.py   (tefm, tsforecast-variant families)
code/hainn/<family>/models/tuner_<name>.py             (mlpredictor -- no variant subdirectory)
```

NOTE: mlpredictor Tuners live directly under models/ with no variant subdirectory
(e.g., code/hainn/mlpredictor/models/tuner_xgboost.py). Only tefm and similar
families use a variant sublevel (e.g., models/te_clm/tuner_ts_clm.py).

**WHAT to write (per ref/layer-2-tuner.md):**

Five abstract methods (ModelTuner contract):
  1. get_tfm_data(dataset)          -> domain-format data (e.g., sparse, nixtla df, tensor)
  2. fit(dataset, TrainingArgs)
  3. infer(dataset, InferenceArgs)  -> raw output (not yet DataFrame)
  4. save_model(key, model_dir)
  5. load_model(key, model_dir)

NOTE: _ensure_model_loaded() is NOT an abstract method. It is an optional
private helper that some Tuner subclasses use internally (e.g., HFNTPTuner).
Do not confuse it with the required contract above.

Plus required class attributes:
  - domain_format = "<format>"   (not "base")
  - transform_fn as standalone module-level function (not a method)

Key conventions to get right:
  - save_model path: os.path.join(model_dir, f"model_{key}")  [NOT {key}_model]
  - __init__ must pass **kwargs to super().__init__()
  - transform_fn is DESIGNED and validated at L1 test, then the final
    version is MOVED into this file as a standalone module-level function
    (not a method). Do not prototype it directly in the Tuner.

**Reference:** ref/layer-2-tuner.md -- read MUST DO + MUST NOT + standalone transform_fn
**Example to read first:**
  code/hainn/mlpredictor/models/tuner_xgboost.py
  code/hainn/tsforecast/models/neuralforecast/modeling_nixtla_nhits.py  (if tsforecast)

WARNING: tsforecast model files use the naming convention modeling_nixtla_<name>.py,
NOT tuner_<name>.py. Check actual files with:
  Glob: code/hainn/tsforecast/models/**/*.py

---

Layer 3a: Instance File
========================

**WHERE to write:**

```
code/hainn/<family>/instance_<name>.py
```

**WHAT to write (per ref/layer-3-instance.md):**

Five abstract methods (ModelInstance contract):
  1. init()                      -- builds self.model_base dict
  2. fit(Data, TrainingArgs)     -- calls tuner.fit() for each key
  3. infer(Data, InferenceArgs)  -- calls tuner.infer() + formats output
  4. _save_model_base(model_dir) -- calls tuner.save_model(key, model_dir)
  5. _load_model_base(model_dir) -- calls self.init() FIRST, then tuner.load_model()

Required class attribute:
  - MODEL_TYPE = "<string>"  (must match ModelInstanceClass in YAML exactly)

Tuner registry -- use Style A (dict) for simple cases:
  MODEL_TUNER_REGISTRY = {
      "XGBoostTuner": "hainn.<family>.models.tuner_xgboost",
  }

infer() routing contract:
  - If input is AIDataSet with splits -> return {split_name: pd.DataFrame}
  - If input is plain Dataset         -> return pd.DataFrame

Critical: _load_model_base must call self.init() BEFORE tuner.load_model()

**Reference:** ref/layer-3-instance.md -- all sections
**Example to read first:**
  code/hainn/mlpredictor/instance_slearner.py

---

Layer 3b: Configuration File
==============================

**WHERE to write:**

```
code/hainn/<family>/configuration_<name>.py
```

**WHAT to write (per ref/layer-3-instance.md "Config Class Contract"):**

Dataclass with 4 required Dict fields:
  - ModelArgs: Dict
  - TrainingArgs: Dict
  - InferenceArgs: Dict
  - EvaluationArgs: Dict

Plus standard fields:
  - aidata_name, aidata_version, modelinstance_name, modelinstance_version

Two class methods to implement:
  1. from_yaml(yaml_path) -> <ConfigClass>
  2. from_aidata_set(aidata_set, **kwargs) -> <ConfigClass>

from_aidata_set must build:
  modelinstance_set_name = f"{modelinstance_name}/{modelinstance_version}"
  (version already has @ prefix; do NOT add it again)

**Reference:** ref/layer-3-instance.md "Config Class Contract" + from_aidata_set() section
**Example to read first:**
  code/hainn/mlpredictor/configuration_slearner.py

---

Layer 3c: Register in model_registry.py
=========================================

**WHERE to write:**

```
code/hainn/model_registry.py
```

Add an elif branch inside load_model_instance_class():

```python
elif model_type == "<MODEL_TYPE_STRING>":
    from hainn.<family>.instance_<name> import <InstanceClass>
    from hainn.<family>.configuration_<name> import <ConfigClass>
    return <InstanceClass>, <ConfigClass>
```

Also add to the MODEL_REGISTRY dict at the top of the file.

**Reference:** ref/overview.md "Model Registry" section

---

Test Scripts (All Layers)
==========================

**WHERE to write:**

```
code/hainn/<family>/models/test-modeling-<name>/
  scripts/
    test_<name>_1_algorithm.py    (only if custom algorithm)
    test_<name>_2_tuner.py
    test_<name>_3_instance.py
    test_<name>_4_modelset.py
  config/
    config_<name>_smoke.yaml      (minimal config for tests)
```

**WHAT each test script must contain:**

All 4 scripts share the same 7-step structure. See ref/layer-N.md for
the exact step list, display rules, and key_metric requirements.

Critical for test scripts:
  - ALWAYS use real AIData (load from _WorkSpace/4-AIDataStore/)
  - 4-column summary table: step | status | key_metric | artifact
  - key_metric must be a numeric value (loss, rmse, count, etc.)
  - L1 uses "Forward pass" / "Gradient flow" (not "Fit" / "Infer")
  - L2-L4 use "Fit" / "Infer" labels

**Reference:** ref/layer-2-tuner.md / layer-3.md / layer-4.md -- each has a
"Test Notebook: What Layer N Tests" section with the full 7-step structure

---

Layer 4: YAML Config
=====================

**WHERE to write:**

```
config/test-haistep-<cohort>/5-test-<family>/<model_name>.yaml
```

Use one of the YAML templates from ref/overview.md "YAML Config Templates":
  - Template A: External library (XGBoost-style) -- flat ModelArgs
  - Template B: HuggingFace Tuner -- nested with model_name_or_path
  - Template C: Custom nn.Module -- adds algorithm_class key
  - Template D: Multi-tuner Instance -- model_tuner_registry with multiple entries

Key fields to set:
  - ModelInstanceClass: "<MODEL_TYPE_STRING>"  (from Instance.MODEL_TYPE)
  - modelinstance_version: "@v0001-<name>"     (@ prefix required)
  - model_tuner_name: "<TunerClassName>"       (exact match to Tuner class)
  - aidata_name + aidata_version: matching real AIData in _WorkSpace

---

Generation Order
=================

Always write in this order (each layer depends on the one below):

  1. algorithm_<name>.py   (if needed)
  2. tuner_<name>.py
  3. configuration_<name>.py
  4. instance_<name>.py
  5. model_registry.py     (add elif + dict entry)
  6. YAML config
  7. test scripts (L2 -> L3 -> L4)

Run tests bottom-up: L2 first, then L3, then L4. Fix each layer before
moving up. If L2 fails, do not proceed to L3.

---

Post-Generation Verification
==============================

After writing all files, run the registry smoke test:

```bash
source .venv/bin/activate && source env.sh
```

NOTE: source .venv/bin/activate does NOT persist across Bash tool calls.
Always chain: source .venv/bin/activate && source env.sh && python <script>
Or call venv Python directly: .venv/bin/python script.py

```bash
source .venv/bin/activate && source env.sh && python -c "
from hainn.model_registry import load_model_instance_class
cls, cfg = load_model_instance_class('<MODEL_TYPE_STRING>')
print('Instance:', cls.__name__)
print('Config:  ', cfg.__name__)
print('REGISTRY OK')
"
```

Then run fn-review Steps 1-8 to do a full quality pass before declaring done.
