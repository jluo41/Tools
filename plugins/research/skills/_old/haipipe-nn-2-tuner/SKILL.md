Skill: haipipe-nn-2-tuner
=========================

Layer 2 of the 4-layer NN pipeline: Model Tuner.

The universal wrapper contract. Every algorithm gets wrapped in a Tuner
that provides a uniform interface. This is the ONLY layer that imports
external algorithm libraries.

---

Architecture Position
=====================

```
Layer 4: ModelSet/Pipeline    Packages everything. Config-driven.
    |
Layer 3: Instance             Thin orchestrator. Manages Tuner dict.
    |
Layer 2: Tuner    <---        Wraps ONE algorithm. Owns data conversion,
    |                         training, inference, serialization.
    |                         ONLY layer that imports external libraries.
Layer 1: Algorithm            Raw external library.
```

---

The Contract
============

**File:** code/hainn/model_tuner.py

Every Tuner MUST provide these 5 methods:

```python
class ModelTuner(ABC):
    domain_format = "base"              # Override: "nixtla", "sparse", "tensor", etc.

    def __init__(self, TfmArgs=None, **kwargs):
        self.TfmArgs = TfmArgs or {}
        self.model = None               # Raw algorithm instance (set after fit)

        # AUTO-STORES extra kwargs as instance attributes:
        for key, value in kwargs.items():
            if not hasattr(self, key):
                setattr(self, key, value)
        # e.g., MyTuner(TfmArgs=t, h=12, input_size=288)
        #   -> self.h = 12, self.input_size = 288

    @abstractmethod
    def get_tfm_data(self, dataset): ...   # Convert input -> domain format
    @abstractmethod
    def fit(self, dataset, TrainingArgs=None): ...
    @abstractmethod
    def infer(self, dataset, InferenceArgs=None): ...
    @abstractmethod
    def save_model(self, key: str, model_dir: str): ...
    @abstractmethod
    def load_model(self, key: str, model_dir: str): ...
```

**5 abstract methods, 1 class attribute, 2 instance attributes + auto-stored kwargs.**

Rules from the base class (model_tuner.py lines 18-32):
1. NO PRIVATE METHODS (self._xxx) in the **base class itself**
   (subclasses MAY use private helper methods, e.g., HFNTPTuner uses _ensure_model_loaded())
2. DATA CONVERSION via standalone transform_fn (not a method)
3. CACHING is handled by get_tfm_data() -- only AIData_Set gets cached

---

File Structure Template
=======================

Every Tuner file follows this layout:

```python
# tuner_my_algorithm.py
# (if wrapping custom nn.Module: also create algorithm_my_algorithm.py for Layer 1)

# ─── Layer 1 import (ONLY HERE) ───
import my_algorithm_lib

from hainn.model_tuner import ModelTuner

# ─── 1. Standalone transform_fn at TOP ───
def transform_fn(data, TfmArgs):
    """Convert HF Dataset / DataFrame / dict -> algorithm-native format."""
    # Your conversion logic
    return converted_data

# ─── 2. Optuna defaults (optional) ───
DEFAULT_OPTUNA_SPACE = {
    'n_estimators': {'type': 'int', 'low': 50, 'high': 500},
    ...
}

# ─── 3. Tuner class ───
class MyAlgorithmTuner(ModelTuner):
    domain_format = "my_domain"

    def __init__(self, TfmArgs=None, **model_specific_args):
        super().__init__(TfmArgs=TfmArgs, **model_specific_args)
        # NOTE: super().__init__ auto-stores all kwargs as attributes,
        # so self.h, self.input_size, etc. are already set.
        # You can still override or set defaults here if needed:
        self.h = model_specific_args.get('h', 24)
        ...

    def get_tfm_data(self, dataset):  # 5-case dispatch
    def fit(self, dataset, TrainingArgs=None):
    def infer(self, dataset, InferenceArgs=None):
    def save_model(self, key, model_dir):
    def load_model(self, key, model_dir):
```

---

The Standalone transform_fn Pattern
=====================================

**Why standalone?** Instance can call get_transform_fn(tuner_name) to
access it without instantiating the Tuner. It must be importable as a
top-level function.

**Input:** One of:
- HF Dataset (has .to_pandas())
- pd.DataFrame
- case_feature_dict (single case as dict)

**Output:** Algorithm-native format (Nixtla DataFrame, sparse matrix, tensor, etc.)

```python
# At TOP of tuner file, BEFORE the class:
def transform_fn(data, TfmArgs):
    target_col = TfmArgs.get('target_col', 'value')
    time_col = TfmArgs.get('time_col', 'ds')

    # Convert to pandas if HF Dataset
    if hasattr(data, 'to_pandas'):
        df = data.to_pandas()
    elif isinstance(data, pd.DataFrame):
        df = data
    else:
        df = pd.DataFrame([data])  # single case dict

    # Convert to domain format
    ...
    return domain_format_data
```

---

The 5-Case Data Dispatch (get_tfm_data)
========================================

get_tfm_data() is @abstractmethod -- you MUST implement it. The 5-case
dispatch below is the recommended structure (shown in base class docstring),
but the exact logic is not enforced -- each Tuner implements its own version.

```python
def get_tfm_data(self, dataset):
    # Case 1: AIData_Set (has .dataset_dict and .data_path)
    #   -> WITH caching (uses data_path for cache directory)
    if hasattr(dataset, 'dataset_dict') and hasattr(dataset, 'data_path'):
        cache_dir = os.path.join(dataset.data_path, f'_cache_{self.domain_format}')
        result = {}
        for split_name, hf_dataset in dataset.dataset_dict.items():
            cache_file = f'{self.domain_format}_{split_name}_{hash}.parquet'
            if os.path.exists(cache_file):
                result[split_name] = pd.read_parquet(cache_file)
            else:
                result[split_name] = transform_fn(hf_dataset, self.TfmArgs)
                result[split_name].to_parquet(cache_file)
        return result

    # Case 2: Dict[str, Dataset/DataFrame] -> transform each, no caching
    if isinstance(dataset, dict):
        return {split: transform_fn(ds, self.TfmArgs) for split, ds in dataset.items()}

    # Case 3: Single HF Dataset -> direct transform
    if hasattr(dataset, 'to_pandas'):
        return transform_fn(dataset, self.TfmArgs)

    # Case 4: pd.DataFrame -> direct transform
    if isinstance(dataset, pd.DataFrame):
        return transform_fn(dataset, self.TfmArgs)

    # Case 5: case_feature_dict (single case) -> direct transform
    return transform_fn(dataset, self.TfmArgs)
```

---

The Optuna Pattern
==================

Tuners optionally integrate Optuna for hyperparameter tuning:

```python
def fit(self, dataset, TrainingArgs=None):
    data = self.get_tfm_data(dataset)
    df_train, df_valid = ...  # extract train/valid

    n_trials = TrainingArgs.get('OptunaArgs', {}).get('n_trials', 0)

    if n_trials > 0:
        study = optuna.create_study(direction='minimize')
        study.optimize(
            lambda trial: self._objective(trial, df_train, df_valid),
            n_trials=n_trials
        )
        self.best_params = study.best_params
    else:
        self.best_params = {}  # use defaults

    # Train final model with best params
    self.model = MyAlgorithm(**{**default_params, **self.best_params})
    self.model.fit(df_train)
```

---

The save_model / load_model Pattern
=====================================

**Naming convention:** `model_{key}` prefix inside model_dir for all formats.
The format varies by algorithm:

```
Convention A: Directory (PyTorch, NeuralForecast, HuggingFace)
  model_dir/model_MAIN/          # Directory: model_{key}/
    best_params.json
    tfm_args.json
    model_weights/

Convention B: Flat file (XGBoost, LightGBM)
  model_dir/model_MAIN.json      # XGBoost: model_{key}.json
  model_dir/model_MAIN.txt       # LightGBM: model_{key}.txt

Convention C: Pickle (sklearn)
  model_dir/model_MAIN.pkl       # Pickled model: model_{key}.pkl
```

**Example (directory convention -- most common for new models):**

```python
def save_model(self, key: str, model_dir: str):
    save_path = os.path.join(model_dir, f'model_{key}')  # e.g., model_MAIN/
    os.makedirs(save_path, exist_ok=True)

    # Save tuner metadata alongside weights:
    json.dump(self.best_params, open(f'{save_path}/best_params.json', 'w'))
    json.dump(self.TfmArgs, open(f'{save_path}/tfm_args.json', 'w'))

    # Algorithm-specific save (varies):
    self.model.save(f'{save_path}/model_weights')

def load_model(self, key: str, model_dir: str):
    load_path = os.path.join(model_dir, f'model_{key}')

    self.best_params = json.load(open(f'{load_path}/best_params.json'))
    self.TfmArgs = json.load(open(f'{load_path}/tfm_args.json'))
    self.model = MyAlgorithm.load(f'{load_path}/model_weights')
```

---

Tuner Inheritance
=================

Tuners may inherit from other Tuner subclasses, not only directly from
ModelTuner. Use this when adding a new input channel to an existing Tuner.

```
ModelTuner (ABC)
  └── TSCLMTuner            (tuner_ts_clm.py)         domain = "ts_clm"
  └── TECLMTuner            (tuner_te_clm_event.py)   domain = "te_clm"
        └── TECLMEventTuner (same file)                domain = "te_clm"
        └── TECLMToDTuner   (tuner_ts_clm_tod.py)     domain = "te_clm_tod"
```

Rules for Tuner subclasses:
- Override only the methods that differ (get_tfm_data, fit, infer, save/load)
- Call super().method() when the parent behaviour is still needed
- The domain_format may differ per variant (e.g., "te_clm_tod")
- A child Tuner file may import from its parent Tuner file

Multiple related Tuners (base + variants) may coexist in one file when
they share most logic and only diverge on one input channel.

---

Algorithm Splitting (algorithm_*.py)
=====================================

When your Tuner wraps a **custom nn.Module** (not a pure external library),
split into two files:

```
algorithm_<name>.py   ← Layer 1: nn.Module only (no training logic)
tuner_<name>.py       ← Layer 2: Tuner class + transform_fn
```

The Tuner imports the Algorithm:

```python
# tuner_te_clm_event.py
from .algorithm_te_clm_event import TECLMAlgorithm
```

Algorithm files form an inheritance chain when building capabilities
incrementally:

```
nn.Module
  └── TSCLMAlgorithm              (algorithm_ts_clm.py)
        └── TSCLMWithToDAlgorithm (algorithm_ts_clm_tod.py)
              └── TECLMAlgorithm  (algorithm_te_clm_event.py)
```

Rules:
- Algorithm files import ONLY torch and other algorithm files
- The Instance and above NEVER import algorithm_*.py directly
- Algorithm class naming: <ComponentName>Algorithm

---

transform_fn Naming for Variants
=================================

When a file contains multiple Tuners with different data formats, use:

```python
def transform_fn(data, TfmArgs):     # base / canonical name
    ...

def transform_fn_te(data, TfmArgs):  # suffix for TE variant
    ...

def transform_fn_tod(data, TfmArgs): # suffix for ToD variant
    ...
```

The base is always named `transform_fn`. Variants use `transform_fn_<suffix>`.

---

Known Deviations (existing code)
================================

- **MLPredictor XGBoostTuner**: Now canonical — inherits ModelTuner, implements
  all 5 abstract methods, domain_format = 'xgboost'. Other mlpredictor tuners
  (DeepFM, LightGBM) still have Instance-level save/load (partial deviation).
- **HFNTPTuner**: Inherits ModelTuner but does not pass **kwargs to
  super().__init__(), only passes TfmArgs.

These are non-canonical. New Tuners MUST follow the standard contract.

---

MUST DO
=======

1. **Inherit from ModelTuner**
2. **Set domain_format class attribute** -- "nixtla", "sparse", "tensor", "hf_clm", etc.
3. **Define transform_fn() as STANDALONE function at TOP of file** -- not a class method
4. **Implement 5 abstract methods:**
   get_tfm_data(), fit(), infer(), save_model(), load_model()
5. **Call super().__init__(TfmArgs=TfmArgs, **kwargs)** --
   pass **kwargs through so the base class auto-stores them as attributes
6. **Store raw algorithm in self.model** -- base class initializes to None;
   this is the expected convention (set after fit or load)
7. **Save to model_{key}/ subfolder** inside model_dir
8. **Save tuner metadata alongside weights** (e.g., tfm_args.json, tuner_config.json,
   or best_params.json -- the exact filename varies, but tuner state must be persisted)
9. **Import the raw algorithm ONLY in this file**

---

MUST NOT
========

1. **NEVER know about ModelInstance, ModelInstance_Set, or ModelInstance_Pipeline**
2. **NEVER know about PreFnPipeline** -- that is above your scope
3. **NEVER know about modelinstance_dir** -- you receive model_dir only
4. **NEVER import Tuners from a different model family** -- cross-family Tuner
   imports create circular dependencies. Within the same family, a child Tuner
   may import from its parent Tuner (see Tuner Inheritance above)
5. **NEVER put transform_fn as a class method** -- it must be importable standalone

**infer() return type (Tuner level):** Family-specific. Check existing Tuners
in your model family for the expected format. The Instance above you handles
output routing — see haipipe-nn-3-instance for the standard routing contract.

---

Key File Locations
==================

```
Base class:               code/hainn/model_tuner.py

TSForecast tuners:        code/hainn/tsforecast/models/
  neuralforecast/:        PatchTST, NBEATS, NHITS, Autoformer, DLinear, TFT
  mlforecast/:            XGBoost, LightGBM, CatBoost, Linear
  statsforecast/:         ARIMA, AutoETS, Naive
  api/:                   LLMAPITuner, NixtlaAPITuner (TimeGPT)

MLPredictor tuners:       code/hainn/mlpredictor/models/
  XGBoost, LightGBM, CatBoost, RandomForest, GradientBoosting, Logistic, DeepFM

TEFM tuners:              code/hainn/tefm/models/
  hfntp/:                 HFNTPTuner (HuggingFace causal language modeling)
```

---

Test Notebook: What Layer 2 Tests
==================================

The tuner test exercises the Tuner wrapper in isolation (NO Instance).
It verifies transform_fn, fit, infer, and save/load work correctly.

**Expected steps (unified 7-step structure):**

```
Step 1: Load config
        display_df with tuner_name, architecture params

Step 2: Load real AIData
        print(aidata), print(aidata.dataset_dict['train'][0])

Step 3: Create Tuner
        display_df with tuner class, domain_format, mode, params

Step 4: Prepare data
        4a: transform_fn -- BEFORE/AFTER pattern:
            print(raw_data), print(raw_data[0])
            -> run transform_fn ->
            print(ds_tfm), print(ds_tfm[0])
            sample_input_row = ds_tfm[0]    # capture for artifacts block
            + verify token range assertions
        4b: get_tfm_data -- BEFORE/AFTER pattern:
            print(aidata)
            -> run get_tfm_data ->
            print each split dataset
            + display_df with split summary (n_rows per split, n_features)

Step 5: Fit
        print(data_fit) before calling
        -> tuner.fit(data_fit, TrainingArgs) ->
        display_df with training time, [family-specific metric]
        Key metric is family-specific:
          XGBoost:       time=2.1s, best_iter=127, val_auc=0.821
          Nixtla Neural: time=12s, val_loss=0.041
          TSForecast:    time=1.8s, is_fitted=True

Step 6: Infer (test multiple input types)
        Type A: Dict[str, Dataset]
            print(input_dict) before -> tuner.infer(input) ->
            print(output keys, shapes) after
        Type B: Single Dataset
            print(dataset) before -> tuner.infer(dataset) ->
            print(output) after
        sample_output_row = first row of output   # capture for artifacts block
        display_df with both results

Step 7: Save/load roundtrip
        7a: Save weights + tuner metadata (best_params.json, tfm_args.json)
        7b: Reload + verify weight_delta == 0.0
        7c: YAML config validation (display_df comparing original vs reloaded)
        model_dir = _WorkSpace/5-ModelInstanceStore/{name}/{version}/
        display_df with weight_delta, cfg match
```

```python
display_df(pd.DataFrame([
    {'step': '1. Load config',        'status': 'PASSED', 'key_metric': tuner_str,    'artifact': config_path},
    {'step': '2. Load AIData',        'status': 'PASSED', 'key_metric': aidata_str,   'artifact': AIDATA_PATH},
    {'step': '3. Create Tuner',       'status': 'PASSED', 'key_metric': class_str,    'artifact': domain_str},
    {'step': '4. Prepare data',       'status': 'PASSED', 'key_metric': shape_str,    'artifact': str(sample_input_row)},
    {'step': '5. Fit',                'status': 'PASSED', 'key_metric': metric_str,   'artifact': 'is_fitted=True'},
    {'step': '6. Infer',              'status': 'PASSED', 'key_metric': infer_str,    'artifact': str(sample_output_row)},
    {'step': '7. Save/load roundtrip','status': 'PASSED', 'key_metric': 'weight_delta=0.0, cfg=True', 'artifact': model_dir},
]).set_index('step'))

# ─── Artifacts (click to open in VS Code) ───────────────────────────────
print(f"\n--- Artifacts ---")
print(f"  Config:        {config_path}")
print(f"  AIData:        {AIDATA_PATH}")
print(f"  Saved model:   {model_dir}")   # _WorkSpace/5-ModelInstanceStore/...
print(f"\n--- Input sample (Step 4a: first transformed row) ---")
print(sample_input_row)   # captured at Step 4a
print(f"\n--- Output sample (Step 6: first infer result row) ---")
print(sample_output_row)  # captured at Step 6
```

**Key display rules for Layer 2:**

- Step 4 is the most important -- it tests BOTH transform_fn directly
  AND get_tfm_data via the Tuner (which calls transform_fn internally)
- Step 6 must test multiple input types (Dict vs single Dataset)
  because the Tuner's infer() dispatches based on input type
- Always print the actual data dict before calling fit/infer:
  ```python
  print("--- data_fit ---")
  for k, v in data_fit.items():
      print(f"  {k}: {v}")
  ```

**Reference** (read the file for a full copy-paste template):

```bash
cat code/hainn/tefm/models/te_clm/test-modeling-ts_clm/scripts/test_te_clm_2_tuner.py
```

---

See Also
