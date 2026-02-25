fn-review: Deep Per-Model Review Protocol
==========================================

Steps 1-8 for a thorough review of a single model after picking it from
the dashboard. Run fn-dashboard first to fill in the slots below.

**Severity tags:**
  [BLOCK]  Must fix before the model can run at all
  [ERROR]  Will produce wrong results silently
  [WARN]   Pattern deviation -- works but inconsistent
  [NOTE]   Minor style / documentation gap

**Slot variables (filled from dashboard Step 0g):**

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

Read ref/overview.md "YAML Config Templates" and "Complete Model Registry".

Then check:

  [ ] ModelInstanceClass is present and matches MODEL_TYPE_STRING exactly
      (or a known alias listed in overview "model registry" table)
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

NOTE: Before diving into the Tuner, check whether a custom algorithm_*.py
exists (grep for "from .algorithm_" in the Tuner file). If it does, note it
now and plan to review it in Step 5 -- the Tuner's transform_fn and forward
call will reference it.

Read ref/layer-2-tuner.md. Apply its MUST DO checklist and MUST NOT checklist in full.

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

Read ref/layer-3-instance.md. Apply its MUST DO checklist, MUST NOT list, and
infer() routing contract.

Additional checks:

  [ ] MODEL_TYPE in Instance exactly matches the ModelInstanceClass string
      used in the YAML
  [ ] _load_model_base() calls self.init() BEFORE calling tuner.load_model()
      [BLOCK if missing -- Tuner shells don't exist when load is attempted]
  [ ] infer() output follows the routing contract:
        Single input  -> pd.DataFrame
        Multi-split   -> {split_name: pd.DataFrame}
  [ ] No algorithm library imports (torch, xgboost, sklearn, etc.) at the
      module level or inside any method
      [ERROR -- violates layer boundary]

---

Step 4: Review the Config (Layer 3)
=====================================

Read ref/layer-3-instance.md "Config Class Contract" section, including
from_aidata_set() and from_yaml() requirements.

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

Read ref/layer-1-algorithm.md "When You Write Custom Layer 1 Code" section.

  [ ] nn.Module subclass with forward(x) -> y implemented
  [ ] Contains ONLY architecture logic -- no training loops, no data loading
      [ERROR if training logic present]
  [ ] Does not import anything from hainn.* or haipipe.*
      [ERROR -- circular imports]
  [ ] Named <ComponentName>Algorithm (e.g., TECLMAlgorithm)

---

Step 6: Cross-Layer Consistency
=================================

These checks span multiple files.

**6a. YAML -> Registry -> Instance -> Config chain**

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

**6b. YAML -> Instance -> Tuner chain**

```bash
python -c "
from hainn.<family>.instance_<name> import MODEL_TUNER_REGISTRY
tuner_name = '<model_tuner_name_from_yaml>'
module_path = MODEL_TUNER_REGISTRY[tuner_name]
import importlib
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
      (e.g., 'MAIN' -> model_MAIN/ directory)

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

NOTE: source .venv/bin/activate does NOT persist across Bash tool calls.
Always chain: source .venv/bin/activate && source env.sh && python <script>
Or call venv Python directly: .venv/bin/python script.py

```bash
# (optional) Layer 1 -- only for custom nn.Module
source .venv/bin/activate && source env.sh && python <TEST_DIR>/scripts/test_<name>_1_algorithm.py

# Layer 2 -- Tuner in isolation
source .venv/bin/activate && source env.sh && python <TEST_DIR>/scripts/test_<name>_2_tuner.py

# Layer 3 -- Instance orchestration
source .venv/bin/activate && source env.sh && python <TEST_DIR>/scripts/test_<name>_3_instance.py

# Layer 4 -- Full ModelInstance_Set packaging
source .venv/bin/activate && source env.sh && python <TEST_DIR>/scripts/test_<name>_4_modelset.py
```

For test structure details, read:
  L1 structure -> ref/layer-1-algorithm.md "Test Notebook: What Layer 1 Tests"
  L2 structure -> ref/layer-2-tuner.md "Test Notebook: What Layer 2 Tests"
  L3 structure -> ref/layer-3-instance.md "Test Notebook: What Layer 3 Tests"
  L4 structure -> ref/layer-4-modelset.md "Test Notebook: What Layer 4 Tests"

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
L3 Instance      infer() routing contract (single/multi -> correct) [ ]
L3 Config        from_yaml implemented (not NotImplementedError)    [ ]
L3 Config        4 required Dict fields present                     [ ]
L3 Registry      import smoke test passes                           [ ]
L1 Algorithm     No training logic, no hainn imports (SKIP if external-only) [ ]
X-layer          YAML->Registry->Instance chain verified            [ ]
X-layer          YAML->Tuner chain verified                         [ ]
X-layer          save/load key consistent across Instance+Tuner     [ ]
X-layer          TrainingArgs fallback to self.config in fit()      [ ]
Tests            Layer 2 test: all steps PASSED                     [ ]
Tests            Layer 3 test: all steps PASSED                     [ ]
Tests            Layer 4 test: all steps PASSED                     [ ]
```

PASS:      Zero [BLOCK] or [ERROR] issues. All test layers green.
WARN-PASS: Zero [BLOCK]/[ERROR]. Some [WARN]/[NOTE] -- document and proceed.
FAIL:      Any [BLOCK] or [ERROR], or any test layer failing.

---

Quick Error Lookup
==================

```
Error seen                               Most likely cause
───────────────────────────────────────  ──────────────────────────────────────────────────────
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
```
