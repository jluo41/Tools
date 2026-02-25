Skill: haipipe-nn-4-modelset
=============================

Layer 4 of the 4-layer NN pipeline: ModelSet & Pipeline.

Packages a trained Instance into a complete asset with training results,
evaluation, examples, and lineage tracking. Provides run versioning,
remote sync, and YAML-driven configuration. Model-type agnostic.

---

Architecture Position
=====================

```
Layer 4: ModelSet/Pipeline  <---  Packages everything. Asset with
    |                             save/load/remote. Run versioning.
Layer 3: Instance                 Config-driven. Model-type agnostic.
    |
Layer 2: Tuner                    Wraps ONE algorithm.
    |
Layer 1: Algorithm                Raw external library.
```

---

Two Classes at Layer 4
======================

**ModelInstance_Pipeline** -- Orchestrator (creates the asset)

```
__init__:
  - Training mode: Resolve ModelInstanceClass + ConfigClass from registry
  - Inference mode: ModelInstance_Set.load_asset(path, SPACE) → load existing

Training flow (_run_training):
  1. ConfigClass.from_aidata_set() → create config with auto-extracted metadata
  2. ModelInstanceClass(config, SPACE) → create instance
  3. model_instance.init() → create Tuner shells
  4. model_instance.fit(Name_to_Data) → train
  5. model_instance.evaluate(Name_to_Data, EvaluationArgs) → evaluate (if available)
  6. Collect training results (timestamps, model stats)
  7. PreFnPipeline.from_aidata_set() → create and attach feature pipeline
  8. ExampleFn → generate test examples (optional)
  9. Package into ModelInstance_Set → RETURN (caller saves to disk)

Inference flow (_run_inference):
  1. model_instance = self.modelinstance_set.get_model_instance()
  2. model_instance.infer(test_data, InferenceArgs) → predictions

Evaluate flow (_run_evaluation):
  1. Load existing model from ModelInstance_Set
  2. Pipeline wraps evaluate in _evaluate_model() which:
     a. Converts aidata_set.dataset_dict → Name_to_Data dict
     b. Calls model_instance.evaluate(Name_to_Data, EvaluationArgs)
     c. Returns evaluation_results
```

**IMPORTANT:** _run_training() RETURNS the ModelInstance_Set without
calling save_to_disk(). The caller must save explicitly:

```python
modelinstance_set = pipeline.run(aidata_set, mode='fit', ...)
modelinstance_set.save_to_disk()  # Caller's responsibility
```

**ModelInstance_Set** -- Asset (the saved package)

```
Inherits from Asset to get the framework:
  - save_to_disk() / load_from_disk() / load_asset()
  - push_to_remote() with S3/GCS/Databricks/GDrive support
  - Manifest handling with lineage tracking
  - Cache management

ModelInstance_Set implements 5 Asset abstract methods:
  - _get_set_name()              → returns modelinstance_set_name
  - _get_default_store_key()     → returns 'LOCAL_MODELINSTANCE_STORE'
  - _save_data_to_disk(path)     → writes model/ + training/ + evaluation/ + examples/
  - _load_data_from_disk(path, manifest) → reads them back
  - _generate_custom_manifest()  → adds lineage chain to manifest.json
Also overrides save_to_disk() for run versioning (@run-v000X).
```

---

YAML Configuration
==================

The YAML config drives ModelInstance_Pipeline. This is the primary
user-facing interface for training models.

**Required top-level keys:**

```yaml
ModelInstanceClass: "<type string from model registry>"
ModelArgs:
  model_tuner_name: "<tuner class name>"
  # ... tuner-specific args
TrainingArgs:
  TrainSetNames: ["train"]
  # ... training hyperparameters
```

**Optional keys:**

```yaml
EvaluationArgs:
  EvalSetNames: ["test"]
  metrics: ["mae", "rmse"]
InferenceArgs:
  InferSetNames: ["test"]
ExampleConfig:
  enabled: false
  ExampleFnName: "DiverseActionCoverage"
  num_examples: 10
```

**See haipipe-nn-0-overview for complete YAML templates per model type.**

---

ModelInstance_Pipeline
=====================

**File:** code/haipipe/model_base/modelinstance_pipeline.py

```python
class ModelInstance_Pipeline:
    def __init__(self, config: Dict, SPACE: Dict):
        # Case 1: Inference mode (load existing)
        if config.get('modelinstance_set_path'):
            self.modelinstance_set = ModelInstance_Set.load_asset(path, SPACE)
            self.mode = 'inference'
            return

        # Case 2: Training mode (create new)
        # Registry resolution happens HERE in __init__, not in _run_training.
        ModelInstanceClass = config['ModelInstanceClass']
        if isinstance(ModelInstanceClass, str):
            self.ModelInstanceClass, self.ConfigClass = load_model_instance_class(
                ModelInstanceClass
            )
        else:
            self.ModelInstanceClass = ModelInstanceClass
            self.ConfigClass = ModelInstanceClass._get_config_class()
        self.model_args = config.get('ModelArgs', {})
        self.training_args = config.get('TrainingArgs', {})
        self.evaluation_args = config.get('EvaluationArgs', {})
        self.inference_args = config.get('InferenceArgs', {})
        self.example_config = config.get('ExampleConfig', {})

        # Load ExampleFn if enabled
        if self.example_config.get('enabled', False):
            from haipipe.model_base.builder.examplefn import ExampleFn
            example_fn_name = self.example_config.get('ExampleFnName', 'DiverseActionCoverage')
            self.example_fn = ExampleFn(example_fn_name, SPACE)
        else:
            self.example_fn = None

        self.mode = 'training'

    def run(self, aidata_set, mode='fit',
            modelinstance_name=None, modelinstance_version='v0001'):
        if mode in ['fit', 'train']:
            return self._run_training(aidata_set, modelinstance_name, modelinstance_version)
        elif mode == 'inference':
            return self._run_inference(aidata_set)
        elif mode == 'evaluate':
            return self._run_evaluation(aidata_set)
```

**Training flow (_run_training) -- actual code:**

```python
def _run_training(self, aidata_set, modelinstance_name, modelinstance_version):
    # NOTE: self.ModelInstanceClass and self.ConfigClass were already resolved
    # in __init__ via load_model_instance_class(). _run_training uses them directly.

    # 1. Create config from aidata_set (metadata auto-extracted)
    config = self.ConfigClass.from_aidata_set(
        aidata_set=aidata_set,
        modelinstance_name=modelinstance_name,
        modelinstance_version=modelinstance_version,
        ModelArgs=self.model_args,
        TrainingArgs=self.training_args,
        EvaluationArgs=self.evaluation_args,
        InferenceArgs=self.inference_args,
        SPACE=self.SPACE
    )

    # 2. Create model instance
    model_instance = self.ModelInstanceClass(config=config, SPACE=self.SPACE)

    # 3. Initialize model architecture
    model_instance.init()

    # 4. Train -- NOTE: Pipeline passes NO TrainingArgs parameter.
    # Models read TrainingArgs from self.config instead.
    Name_to_Data = {split: ds for split, ds in aidata_set.dataset_dict.items()}
    model_instance.fit(Name_to_Data)

    # 5. Evaluate (if method exists and EvaluationArgs provided)
    # Uses _evaluate_model() wrapper which converts dataset_dict → Name_to_Data
    evaluation_results = None
    if hasattr(model_instance, 'evaluate') and config.EvaluationArgs:
        evaluation_results = self._evaluate_model(model_instance, aidata_set)
        # Internally calls: model_instance.evaluate(Name_to_Data, config.EvaluationArgs)

    # 6. Collect training results
    training_results = {
        'trained_at': datetime.now().isoformat(),
        'model_type': model_instance.__class__.__name__,
    }

    # 7. Create + attach PreFnPipeline
    prefn_pipeline = PreFnPipeline.from_aidata_set(aidata_set, SPACE=self.SPACE)
    model_instance.prefn_pipeline = prefn_pipeline

    # 8. Generate examples (optional)
    examples_data = None
    if self.example_fn:
        examples_data = self._generate_examples(model_instance, aidata_set, ...)

    # 9. Package into ModelInstance_Set
    # NOTE: Pipeline uses "/" (no @), while ConfigClass.from_aidata_set uses "/@".
    # This is a known code inconsistency -- the pipeline format is what gets saved.
    modelinstance_set_name = f"{modelinstance_name}/{modelinstance_version}"
    self.modelinstance_set = ModelInstance_Set(
        modelinstance_set_name=modelinstance_set_name,
        model_instance=model_instance,
        aidata_set_manifest=aidata_set.manifest,
        training_results=training_results,
        evaluation_results=evaluation_results,
        examples_data=examples_data,
        SPACE=self.SPACE
    )
    return self.modelinstance_set  # Caller calls save_to_disk()
```

---

ModelInstance_Set
=================

**File:** code/haipipe/model_base/modelinstance_set.py

```python
class ModelInstance_Set(Asset):
    asset_store_type = 'MODELINSTANCE'

    def __init__(self, modelinstance_set_name=None, model_instance=None,
                 aidata_set_manifest=None, training_results=None,
                 evaluation_results=None, inference_results=None,
                 examples_data=None, SPACE=None):
        super().__init__(SPACE)
        self.modelinstance_set_name = modelinstance_set_name
        self.model_instance = model_instance
        self.aidata_set_manifest = aidata_set_manifest or {}
        self.training_results = training_results or {}
        self.evaluation_results = evaluation_results or {}
        self.inference_results = inference_results or {}
        self.examples_data = examples_data or []

    # Asset abstract methods:
    def _get_set_name(self): ...
    def _get_default_store_key(self):
        return 'LOCAL_MODELINSTANCE_STORE'
    def _save_data_to_disk(self, path): ...
    def _load_data_from_disk(self, path, manifest): ...
    def _generate_custom_manifest(self): ...

    # ModelInstance_Set specific:
    def get_model_instance(self): ...
```

**Two API levels:**

```
ModelInstance_Set API (our Asset):
  save_to_disk()          → saves model/ + training/ + evaluation/ + manifest.json
  load_asset(name, SPACE) → loads everything via manifest auto-detection (PUBLIC API)
  push_to_remote()        → syncs to S3/GCS/GDrive

model_instance API (HuggingFace-style, nested inside):
  save_pretrained(model_dir)        → saves config.json + metadata.json + weights + prefn
  from_pretrained(model_dir, SPACE) → loads via metadata.json auto-detection
```

**IMPORTANT — use load_asset(), not _load_data_from_disk():**

`load_asset(name, SPACE)` is the public API for loading a saved ModelInstance_Set.
`_load_data_from_disk(path, manifest)` is an internal Asset method — it requires
you to manually read the manifest first and bypasses auto-detection.

The te_clm L4 test snapshot below uses `_load_data_from_disk()` directly (as a
lower-level roundtrip verification). New tests SHOULD use the public API:

```python
# CORRECT — public API (production pattern):
loaded_modelset = ModelInstance_Set.load_asset(
    modelinstance_set_name, SPACE
)

# ACCEPTABLE in tests — lower-level roundtrip (verify internal structure):
loaded_modelset = ModelInstance_Set(SPACE=SPACE)
loaded_modelset.modelinstance_set_name = modelinstance_set_name
with open(os.path.join(save_path, 'manifest.json')) as f:
    manifest = json.load(f)
loaded_modelset._load_data_from_disk(save_path, manifest)
```

Use `_load_data_from_disk()` only in L4 tests that need to verify the
directory structure explicitly (e.g., checking manifest fields directly).
For production inference, always use `load_asset()`.

---

Directory Structure
===================

```
Demo_AIData_SLearner_20251217/              # ModelInstance_Set root
├── @run-v0001/                             # Archived run 1
├── @run-v0002/                             # Archived run 2
├── model/                                  # Latest model (HuggingFace-style)
│   ├── config.json                         # Model config (architecture + settings)
│   ├── metadata.json                       # {"model_type": "...", "created_at": "..."}
│   ├── model_MAIN/                         # Tuner weights (subfolder per key)
│   ├── prefn_config.json                   # InputArgs, OutputArgs, TriggerArgs
│   ├── prefn_cf_to_cfvocab.json           # Per-CaseFn vocabulary
│   ├── prefn_feat_vocab.json              # Combined vocabulary with offsets
│   ├── checkpoint_best/                    # Best checkpoint during training
│   └── checkpoint_final/                   # Final checkpoint
├── training/                               # Training results
│   └── results.json
├── evaluation/                             # Evaluation results
│   ├── df_case_eval.pkl
│   └── df_report_*.pkl
├── inference_results.pkl                   # Inference output (when run)
├── examples/                               # Test examples (optional)
│   ├── example_000/
│   │   ├── example_info.json
│   │   ├── prediction_results.json
│   │   ├── df_case_example.json
│   │   └── ProcName_to_ProcDf/
│   └── example_001/
└── manifest.json                           # Lineage chain
```

---

Run Versioning
==============

```
First run:   Files saved directly to root (no @run- folder)
Second run:  Current root → @run-v0001, new files → @run-v0002, copied to root
Third run:   New files → @run-v0003, copied to root
...
Root contains the latest run (copied, not symlinked).
NOTE: Only model/, training/, evaluation/, manifest.json, and inference_results.pkl
are copied to root. examples/ is NOT copied (only in @run-vXXXX).
```

Two modes controlled by overwrite parameter:

- **overwrite=True** (default): Deletes existing, saves fresh
- **overwrite=False**: Creates @run-v000X subdirectories for version history

---

PreFnPipeline (Feature Pipeline Attachment)
============================================

Created from AIDataSet and attached to model_instance before saving.
Ensures the feature engineering pipeline travels with the model.

```python
# In ModelInstance_Pipeline._run_training():
prefn_pipeline = PreFnPipeline.from_aidata_set(aidata_set, SPACE=SPACE)
model_instance.prefn_pipeline = prefn_pipeline
```

When model_instance.save_pretrained() is called, it saves:

```
model/
  prefn_config.json           # InputArgs, OutputArgs, TriggerArgs, MetaArgs,
                              # ProcName_to_columns, and other pipeline metadata
  prefn_cf_to_cfvocab.json   # Per-CaseFn vocabulary
  prefn_feat_vocab.json      # Combined vocabulary with offsets
```

---

Manifest and Lineage
=====================

Every ModelInstance_Set saves manifest.json with full lineage chain:

```json
{
    "modelinstance_set_name": "MyModel/v0001",
    "model_type": "TSForecast",
    "aidata_set_manifest": {
        "aidata_set_name": "Demo_AIData",
        "case_set_manifest_list": [
            {
                "case_set_name": "Demo_CaseSet",
                "record_set_manifest": {
                    "record_set_name": "Demo_RecordSet",
                    "source_set_manifest": {
                        "source_set_name": "WellDoc2022CGM",
                        "source_fn": "SMSParquetV250211"
                    }
                }
            }
        ]
    },
    "created_at": "2025-12-17T14:30:00"
}
```

This allows tracing: model -> aidata -> caseset -> recordset -> source.

---

Auto-Detection on Load
======================

Loading uses metadata.json to auto-detect the correct class:

```python
# Via ModelInstance_Set (Asset API)
modelinstance_set = ModelInstance_Set.load_asset('MyModel/v0001', SPACE)
model = modelinstance_set.get_model_instance()

# Via AutoModelInstance (HuggingFace API)
from hainn.model_instance import AutoModelInstance
model = AutoModelInstance.from_pretrained('path/to/model', SPACE)

# Internal flow:
# 1. Read metadata.json -> {"model_type": "TSForecast"}
# 2. load_model_instance_class("TSForecast")
#    -> (TSForecastInstance, TSForecastConfig)
# 3. TSForecastInstance.from_pretrained(model_dir, SPACE)
```

---

Example Generation
==================

Optional step that creates test examples for PreFn validation:

```yaml
ExampleConfig:
  enabled: true
  ExampleFnName: 'DiverseActionCoverage'
  num_examples: 10
  lookback_days: 90
  lookforward_days: 30
  validate: true
```

**Flow:**

1. ExampleFn selects representative test cases from evaluation results
2. Traces lineage: AIDataSet -> CaseSet -> RecordSet -> SourceSet
3. Extracts raw ProcName_to_ProcDf from SourceSet
4. Validates PreFn pipeline: raw data -> features -> predictions
5. Saves to examples/ directory in ModelInstance_Set

---

Usage Patterns
==============

**Training a new model:**

```python
pipeline = ModelInstance_Pipeline(
    config={
        'ModelInstanceClass': 'TSForecast',
        'ModelArgs': {'model_tuner_name': 'NixtlaPatchTSTTuner', ...},
        'TrainingArgs': {'max_steps': 100, 'TrainSetNames': ['train']},
        'EvaluationArgs': {'metrics': ['mae', 'rmse']},
    },
    SPACE=SPACE
)
modelinstance_set = pipeline.run(
    aidata_set, mode='fit',
    modelinstance_name='MyModel', modelinstance_version='v0001'
)
modelinstance_set.save_to_disk()  # Explicit save -- pipeline does NOT auto-save
```

**Loading for inference:**

```python
pipeline = ModelInstance_Pipeline(
    config={'modelinstance_set_path': 'MyModel/v0001'},
    SPACE=SPACE
)
results = pipeline.run(aidata_set, mode='inference')
```

**Direct Asset loading:**

```python
modelinstance_set = ModelInstance_Set.load_asset('MyModel/v0001', SPACE)
model = modelinstance_set.get_model_instance()
predictions = model.infer(test_data)
```

**Remote sync:**

```python
# push_to_remote() auto-resolves paths from SPACE if remote_path not given.
modelinstance_set.push_to_remote()

# Or specify a custom remote path:
modelinstance_set.push_to_remote(remote_path='gdrive:models/MyModel/v0001')
```

---

MUST DO
=======

1. **Inherit ModelInstance_Set from Asset** --
   gets save_to_disk/load_from_disk/push_to_remote for free
2. **Set asset_store_type = 'MODELINSTANCE'** --
   used by Asset for default store key resolution
3. **Implement Asset abstract methods:**
   _get_set_name(), _get_default_store_key(),
   _save_data_to_disk(), _load_data_from_disk(), _generate_custom_manifest()
4. **Save manifest.json with full lineage chain** --
   aidata_set_manifest containing case/record/source chain
5. **Use model_instance.save_pretrained() for the model/ folder** --
   delegate HuggingFace-style saving to the Instance (Layer 3)
6. **Attach PreFnPipeline before saving** --
   model_instance.prefn_pipeline = PreFnPipeline.from_aidata_set(...)
7. **Use load_model_instance_class() from model_registry** --
   string -> (InstanceClass, ConfigClass) resolution
8. **Use ConfigClass.from_aidata_set()** --
   auto-extracts metadata (action_to_id, num_actions, InputArgs, etc.)
9. **Support both overwrite and versioned save modes** --
   overwrite=True deletes existing; overwrite=False creates @run-v000X
10. **Pipeline returns ModelInstance_Set without saving** --
    caller must call save_to_disk() explicitly

---

MUST NOT
========

1. **NEVER import algorithm libraries** --
   No xgboost, torch, sklearn, neuralforecast at Layer 4
2. **NEVER call tuner methods directly** --
   Always go through model_instance.init() / .fit() / .infer()
3. **NEVER create model weights directly** --
   Always through pipeline flow: init() -> fit()
4. **NEVER hardcode model types** --
   Use registry lookup via load_model_instance_class()
5. **NEVER skip PreFnPipeline attachment** --
   Model without prefn_pipeline cannot do inference from raw data
6. **NEVER break the lineage chain** --
   Always include aidata_set_manifest in manifest.json

---

Key File Locations
==================

```
ModelInstance_Set:       code/haipipe/model_base/modelinstance_set.py
ModelInstance_Pipeline:  code/haipipe/model_base/modelinstance_pipeline.py
Asset base class:       code/haipipe/assets.py
PreFnPipeline:          code/hainn/prefn_pipeline.py
Model registry:         code/hainn/model_registry.py
```

---

Test Notebook: What Layer 4 Tests
==================================

The modelset test exercises the full packaging pipeline: train an Instance,
package into ModelInstance_Set, save/load to disk, inference from loaded model.

**Expected steps (unified 7-step structure with sub-steps):**

```
Step 1: Load config
        display_df with ModelInstanceClass, tuner_name, model_dir path

Step 2: Load real AIData
        print(aidata), print(aidata.dataset_dict['train'][0])

Step 3: Create Instance + init()
        display_df with instance class, tuner class, model_base keys

Step 4: Prepare data
        print(data_fit) and print(data_infer)
        sample_input_row = data_fit['train'][0]   # capture for artifacts block
        display_df with split summary (n_rows per split)

Step 5: Fit
        print(data_fit) before calling
        -> instance.fit(data_fit, TrainingArgs) ->
        display_df with fit status, [family-specific metric]

Step 6: Infer (from fitted instance, before packaging)
        print(data_infer) before calling
        -> instance.infer(data_infer) ->
        print(results) after -- show keys, shapes
        sample_output_row = first row of output   # capture for artifacts block
        display_df with n_rows, n_cols, output shape

Step 7: Package + save/load roundtrip
        7a: Package into ModelInstance_Set
            ModelInstance_Set(instance, training_results, aidata_manifest)
            display_df with modelset class, set_name, training/manifest presence
        7b: Save to _WorkSpace/5-ModelInstanceStore/{name}/{version}/
            modelset.save_to_disk() -> verify directory structure
            model_dir = actual save path
            display_df with save_path, top-level items, manifest fields
        7c: Load from disk + verify metadata + config
            Load manifest, _load_data_from_disk() -> verify weights match
            display_df with loaded class, set_name, weight_delta
        7d: Infer from loaded model + weight equality check
            -> loaded_model.infer(data_infer) ->
            verify output matches pre-save output
            display_df with weight_delta=0.0, infer output shape
```

```python
display_df(pd.DataFrame([
    {'step': '1. Load config',        'status': 'PASSED', 'key_metric': tuner_str,      'artifact': config_path},
    {'step': '2. Load AIData',        'status': 'PASSED', 'key_metric': aidata_str,     'artifact': AIDATA_PATH},
    {'step': '3. Create Instance',    'status': 'PASSED', 'key_metric': class_str,      'artifact': model_base_str},
    {'step': '4. Prepare data',       'status': 'PASSED', 'key_metric': split_str,      'artifact': str(sample_input_row)},
    {'step': '5. Fit',                'status': 'PASSED', 'key_metric': metric_str,     'artifact': 'is_fitted=True'},
    {'step': '6. Infer',              'status': 'PASSED', 'key_metric': infer_str,      'artifact': str(sample_output_row)},
    {'step': '7. Pkg+save/load',      'status': 'PASSED', 'key_metric': 'weight_delta=0.0, cfg=True', 'artifact': model_dir},
]).set_index('step'))

# ─── Artifacts (click to open in VS Code) ───────────────────────────────
print(f"\n--- Artifacts ---")
print(f"  Config:        {config_path}")
print(f"  AIData:        {AIDATA_PATH}")
print(f"  Saved model:   {model_dir}")   # _WorkSpace/5-ModelInstanceStore/...
print(f"\n--- Input sample (Step 4: first data_fit row) ---")
print(sample_input_row)   # captured at Step 4
print(f"\n--- Output sample (Step 6: first infer result row) ---")
print(sample_output_row)  # captured at Step 6
```

**Key display rules for Layer 4:**

- Step 7 is unique to Layer 4: the packaging + roundtrip chain.
  Show the directory structure (top-level items, model/ items) and verify
  manifest.json, training/results.json, config.json, metadata.json.
- Step 7d is the end-to-end proof: load a saved model from disk and run
  infer(). Verify output matches Step 6 and weight_delta == 0.0.
- Sub-steps (7a/7b/7c/7d) keep the 7 main steps clean while preserving detail.
- Use `instance.infer()` — the canonical method name (not `inference()`).

**Reference:** `code/hainn/tefm/models/te_clm/test-modeling-ts_clm/scripts/test_te_clm_4_modelset.py`

**Note on the code snapshot below:** The snapshot shows the old 9-step style
(Steps 6–9 as separate steps). The canonical pattern above collapses these into
Step 6 (Infer before packaging) + Step 7 with sub-steps (7a–7d).
New tests should follow the 7-step structure. The snapshot is kept for reference.

**Snapshot** (from te_clm, for quick reference -- canonical source is the file above):

```python
#!/usr/bin/env python3
"""
TE-CLM ModelInstance_Set (Layer 4) Step-by-Step Test
====================================================

Test ModelInstance_Set wrapping TEFMInstance with TECLMTuner -- the
Layer 4 asset packaging layer.

Following the config -> data -> model pipeline pattern:

  Step 1: Setup workspace and load config
  Step 2: Load AIData (real OhioT1DM)
  Step 3: Create TEFMInstance + init()
  Step 4: Prepare data (real subsets)
  Step 5: Fit (train the instance for packaging)
  Step 6: Package into ModelInstance_Set
  Step 7: Save to disk (save_to_disk)
  Step 8: Load from disk and verify
  Step 9: Inference from loaded model

Usage:
    source .venv/bin/activate && source env.sh
    python code/hainn/tefm/models/te_clm/test-modeling-te_clm/scripts/test_te_clm_4_modelset.py
"""

# %% [markdown]
# # TE-CLM ModelInstance_Set (Layer 4) Step-by-Step Test
#
# Tests the full packaging pipeline,
# following the config -> data -> model pipeline pattern.
#
# Uses real OhioT1DM AIData.

# %% Step 1: Setup and Load Config
import os
import json
import yaml
import shutil

from pathlib import Path

import torch
import pandas as pd

from haipipe import setup_workspace

WORKSPACE_PATH, SPACE, logger = setup_workspace()

TEST_DIR = Path(WORKSPACE_PATH) / 'code' / 'hainn' / 'tefm' / 'models' / 'te_clm' / 'test-modeling-te_clm'


def load_yaml(filename):
    with open(TEST_DIR / filename) as f:
        return yaml.safe_load(f)


def display_df(df):
    try:
        from IPython.display import display, HTML
        display(HTML(df.to_html()))
    except Exception:
        print(df.to_string())


config = load_yaml('config_te_clm_from_scratch.yaml')
ModelArgs = config['ModelArgs']
tuner_args = ModelArgs['model_tuner_args']
arch = tuner_args['architecture_config']
TfmArgs = ModelArgs.get('TfmArgs', {})

# Build model_dir from env + config (same structure as real pipeline)
model_store = os.environ.get('LOCAL_MODELINSTANCE_STORE', '_WorkSpace/5-ModelInstanceStore')
model_name = config.get('modelinstance_name', 'Demo-TECLM')
model_version = config.get('modelinstance_version', '@v0001-demo-te_clm-from-scratch')
model_dir = os.path.join(WORKSPACE_PATH, model_store, model_name, model_version)

display_df(pd.DataFrame([
    {'key': 'WORKSPACE_PATH',     'value': WORKSPACE_PATH},
    {'key': 'TEST_DIR',           'value': str(TEST_DIR)},
    {'key': 'model_dir',          'value': model_dir},
    {'key': 'ModelInstanceClass',  'value': config['ModelInstanceClass']},
    {'key': 'model_tuner_name',   'value': ModelArgs['model_tuner_name']},
    {'key': 'vocab_size',         'value': arch['vocab_size']},
    {'key': 'max_seq_length',     'value': tuner_args['max_seq_length']},
    {'key': 'special_tokens',     'value': f"PAD={TfmArgs.get('special_tokens', {}).get('pad_token_id', 0)}, num_special={TfmArgs.get('special_tokens', {}).get('num_special_tokens', 10)}"},
    {'key': 'CUDA available',     'value': torch.cuda.is_available()},
]).set_index('key'))


# %% [markdown]
# ## Step 2: Load AIData
#
# Load real OhioT1DM AIData from disk.

# %% Step 2: Load AIData

from haipipe.aidata_base import AIDataSet

aidata_name = config.get('aidata_name', 'OhioT1DM')
aidata_version = config.get('aidata_version', '@v0002_events_per1h_tewindow')
AIDATA_PATH = os.path.join(SPACE['LOCAL_AIDATA_STORE'], aidata_name, aidata_version)
assert os.path.exists(AIDATA_PATH), f"AIData not found at {AIDATA_PATH}"

aidata = AIDataSet.load_from_disk(AIDATA_PATH)

print(f"AIData: {aidata_name}/{aidata_version}")
print(f"  Splits: {list(aidata.dataset_dict.keys())}")
for split, ds in aidata.dataset_dict.items():
    print(f"    {split}: {len(ds)} cases")

display_df(pd.DataFrame([
    {'key': 'aidata_name',    'value': aidata_name},
    {'key': 'aidata_version', 'value': aidata_version},
    {'key': 'AIDATA_PATH',    'value': AIDATA_PATH},
]).set_index('key'))

# %% Display AIData structure

print(aidata)

# %% Check a sample from train split

if len(aidata.dataset_dict.get('train', [])) > 0:
    sample = aidata.dataset_dict['train'][0]
    print(sample)


# %% [markdown]
# ## Step 3: Create TEFMInstance + init()
#
# Create a TEFMConfig, instantiate TEFMInstance, call init().

# %% Step 3: Create TEFMInstance + init()

from hainn.tefm.instance_tefm import TEFMInstance
from hainn.tefm.configuration_tefm import TEFMConfig

tefm_config = TEFMConfig(
    ModelArgs=config['ModelArgs'],
    TrainingArgs=config['TrainingArgs'],
    InferenceArgs=config.get('InferenceArgs', {}),
    EvaluationArgs=config.get('EvaluationArgs', {}),
)

instance = TEFMInstance(config=tefm_config, SPACE=SPACE)
instance.init()

assert instance.model_tuner is not None

display_df(pd.DataFrame([
    {'property': 'instance class', 'value': type(instance).__name__},
    {'property': 'tuner class',    'value': type(instance.model_tuner).__name__},
    {'property': 'status',         'value': 'PASSED'},
]).set_index('property'))


# %% [markdown]
# ## Step 4: Prepare Data
#
# Use real data subsets for fit and inference.

# %% Step 4: Prepare Data

seq_len = tuner_args['max_seq_length']
vocab_size = arch['vocab_size']

train_ds = aidata.dataset_dict['train'].select(
    range(min(100, len(aidata.dataset_dict['train']))))
test_split_name = 'test-id' if 'test-id' in aidata.dataset_dict else list(aidata.dataset_dict.keys())[-1]
test_ds = aidata.dataset_dict[test_split_name].select(
    range(min(50, len(aidata.dataset_dict[test_split_name]))))

data_fit = {'train': train_ds, test_split_name: test_ds}
# Use 'test' as key for inference -- must match InferenceArgs.InferenceSetNames
data_infer = {'test': test_ds.select(range(min(8, len(test_ds))))}

print("--- data_fit ---")
for k, v in data_fit.items():
    print(f"  {k}: {v}")
print()
print("--- data_infer ---")
for k, v in data_infer.items():
    print(f"  {k}: {v}")

display_df(pd.DataFrame([
    {'property': 'fit splits',  'value': ', '.join(f'{k}({len(v)})' for k, v in data_fit.items())},
    {'property': 'infer splits','value': ', '.join(f'{k}({len(v)})' for k, v in data_infer.items())},
    {'property': 'status',      'value': 'PASSED'},
]).set_index('property'))


# %% [markdown]
# ## Step 5: Fit
#
# Train the instance to get a fitted model for packaging.

# %% Step 5: Fit

train_output_dir = os.path.join(model_dir, 'train_checkpoints')

print("--- fit input ---")
for k, v in data_fit.items():
    print(f"  {k}: {v}")

instance.fit(
    data_fit,
    TrainingArgs={
        'num_train_epochs': 1,
        'per_device_train_batch_size': 4,
        'per_device_eval_batch_size': 8,
        'save_strategy': 'no',
        'logging_steps': 5,
        'report_to': [],
        'output_dir': train_output_dir,
        'gradient_checkpointing': False,
        'fp16': False,
    },
)

assert instance.model_tuner.model is not None
shutil.rmtree(train_output_dir, ignore_errors=True)

display_df(pd.DataFrame([
    {'property': 'instance class', 'value': type(instance).__name__},
    {'property': 'tuner class',    'value': type(instance.model_tuner).__name__},
    {'property': 'model fitted',   'value': instance.model_tuner.model is not None},
    {'property': 'status',         'value': 'PASSED'},
]).set_index('property'))


# %% [markdown]
# ## Step 6: Package into ModelInstance_Set
#
# Create a ModelInstance_Set with the trained instance,
# training results, and AIData manifest.

# %% Step 6: Package into ModelInstance_Set

from haipipe.model_base.modelinstance_set import ModelInstance_Set

modelinstance_set_name = 'test_TECLM_ModelSet'

training_results = {
    'train_loss': 5.89,
    'eval_loss': 5.92,
    'epochs': 1,
    'total_steps': 10,
}

aidata_set_manifest = {
    'aidata_name': aidata_name,
    'created_at': '2026-02-18T00:00:00',
    'splits': {k: len(v) for k, v in data_fit.items()},
}

modelset = ModelInstance_Set(
    modelinstance_set_name=modelinstance_set_name,
    model_instance=instance,
    aidata_set_manifest=aidata_set_manifest,
    training_results=training_results,
    SPACE=SPACE,
)

assert modelset is not None
assert modelset.modelinstance_set_name == modelinstance_set_name
assert modelset.model_instance is instance
assert modelset.training_results == training_results
assert modelset.aidata_set_manifest == aidata_set_manifest

display_df(pd.DataFrame([
    {'property': 'modelset class',         'value': type(modelset).__name__},
    {'property': 'modelinstance_set_name', 'value': modelset.modelinstance_set_name},
    {'property': 'model_instance class',   'value': type(modelset.model_instance).__name__},
    {'property': 'has training_results',   'value': bool(modelset.training_results)},
    {'property': 'has aidata_manifest',    'value': bool(modelset.aidata_set_manifest)},
    {'property': 'status',                 'value': 'PASSED'},
]).set_index('property'))


# %% [markdown]
# ## Step 7: Save to Disk
#
# Use save_to_disk() which creates the full directory structure:
# model/, training/, evaluation/, manifest.json

# %% Step 7: Save to Disk

save_path = os.path.join(model_dir, modelinstance_set_name)

modelset.save_to_disk(path=save_path, overwrite=True)

assert os.path.isdir(save_path)
assert os.path.isdir(os.path.join(save_path, 'model'))
assert os.path.exists(os.path.join(save_path, 'manifest.json'))
assert os.path.isdir(os.path.join(save_path, 'training'))
assert os.path.exists(os.path.join(save_path, 'training', 'results.json'))

# Verify model subdirectory
model_subdir = os.path.join(save_path, 'model')
assert os.path.exists(os.path.join(model_subdir, 'config.json'))
assert os.path.exists(os.path.join(model_subdir, 'metadata.json'))

# Verify manifest
with open(os.path.join(save_path, 'manifest.json')) as f:
    manifest = json.load(f)

assert manifest.get('modelinstance_set_name') == modelinstance_set_name
assert manifest.get('model_type') == 'TEFMInstance'

# Verify training results
with open(os.path.join(save_path, 'training', 'results.json')) as f:
    saved_training = json.load(f)
assert saved_training['train_loss'] == training_results['train_loss']

top_items = sorted(os.listdir(save_path))
model_items = sorted(os.listdir(model_subdir))

display_df(pd.DataFrame([
    {'property': 'save_path',           'value': save_path},
    {'property': 'top-level items',     'value': ', '.join(top_items)},
    {'property': 'model/ items',        'value': ', '.join(model_items[:6])},
    {'property': 'manifest model_type', 'value': manifest.get('model_type')},
    {'property': 'manifest set_name',   'value': manifest.get('modelinstance_set_name')},
    {'property': 'training saved',      'value': saved_training == training_results},
    {'property': 'status',              'value': 'PASSED'},
]).set_index('property'))


# %% [markdown]
# ## Step 8: Load from Disk
#
# Load the saved ModelInstance_Set back. Verify all components:
# model_instance, training_results, manifest, weights.

# %% Step 8: Load from Disk

loaded_modelset = ModelInstance_Set(SPACE=SPACE)
loaded_modelset.modelinstance_set_name = modelinstance_set_name

# Load manifest
with open(os.path.join(save_path, 'manifest.json')) as f:
    loaded_manifest = json.load(f)

loaded_modelset._load_data_from_disk(save_path, loaded_manifest)

assert loaded_modelset.model_instance is not None
assert loaded_modelset.training_results is not None
assert loaded_modelset.aidata_set_manifest is not None
assert loaded_modelset.modelinstance_set_name == modelinstance_set_name

loaded_instance = loaded_modelset.model_instance
assert type(loaded_instance).__name__ == 'TEFMInstance'

# Verify weights match (move to CPU for comparison)
orig_state = {k: v.cpu().float() for k, v in instance.model_tuner.model.state_dict().items()}
loaded_state = {k: v.cpu().float() for k, v in loaded_instance.model_tuner.model.state_dict().items()}

assert set(orig_state.keys()) == set(loaded_state.keys())
mismatched = [
    k for k in orig_state
    if not torch.allclose(orig_state[k], loaded_state[k], atol=1e-4)
]
assert len(mismatched) == 0, f"Weight mismatch: {mismatched[:5]}"

display_df(pd.DataFrame([
    {'property': 'loaded class',          'value': type(loaded_modelset).__name__},
    {'property': 'loaded model class',    'value': type(loaded_instance).__name__},
    {'property': 'loaded set_name',       'value': loaded_modelset.modelinstance_set_name},
    {'property': 'training_results keys', 'value': ', '.join(loaded_modelset.training_results.keys())},
    {'property': 'aidata_manifest keys',  'value': ', '.join(loaded_modelset.aidata_set_manifest.keys())},
    {'property': 'state_dict keys',       'value': len(loaded_state)},
    {'property': 'weight mismatches',     'value': len(mismatched)},
    {'property': 'status',                'value': 'PASSED'},
]).set_index('property'))


# %% [markdown]
# ## Step 9: Inference from Loaded Model
#
# Use get_model_instance() to extract the loaded model, then
# run inference on test data.

# %% Step 9: Inference from Loaded Model

import math

model_for_infer = loaded_modelset.get_model_instance()
assert model_for_infer is not None

print("--- inference input ---")
for k, v in data_infer.items():
    print(f"  {k}: {v}")

infer_results = model_for_infer.inference(data_infer)

print()
print("--- inference output ---")
for k, v in infer_results.items():
    print(f"  {k}: keys={list(v.keys())}, loss={v['loss']:.4f}, embeddings={v['embeddings'].shape}")

assert infer_results is not None
# Inference uses InferenceSetNames from config (default: ['test'])
infer_key = 'test'
assert infer_key in infer_results, f"Missing '{infer_key}' in results, got: {list(infer_results.keys())}"

test_metrics = infer_results[infer_key]
assert 'loss' in test_metrics
assert 'embeddings' in test_metrics
assert 'predicted_tokens' in test_metrics
assert test_metrics['loss'] > 0

n_infer = len(data_infer[infer_key])
assert test_metrics['embeddings'].shape[0] == n_infer
assert test_metrics['predicted_tokens'].shape[0] == n_infer

perplexity = math.exp(test_metrics['loss'])

display_df(pd.DataFrame([
    {'property': 'infer model class',      'value': type(model_for_infer).__name__},
    {'property': 'test samples',           'value': n_infer},
    {'property': 'test loss',              'value': f'{test_metrics["loss"]:.4f}'},
    {'property': 'test perplexity',        'value': f'{perplexity:.2f}'},
    {'property': 'embeddings shape',       'value': str(test_metrics['embeddings'].shape)},
    {'property': 'predicted_tokens shape', 'value': str(test_metrics['predicted_tokens'].shape)},
    {'property': 'status',                 'value': 'PASSED'},
]).set_index('property'))

# Cleanup modelset save/load test
shutil.rmtree(os.path.join(model_dir, modelinstance_set_name), ignore_errors=True)


# %% [markdown]
# ## Summary

# %% Summary

results_summary = pd.DataFrame([
    {'test': '1. Load Config',                 'status': 'PASSED'},
    {'test': '2. Load AIData',                 'status': 'PASSED'},
    {'test': '3. Create TEFMInstance',         'status': 'PASSED'},
    {'test': '4. Prepare Data',                'status': 'PASSED'},
    {'test': '5. Fit',                         'status': 'PASSED'},
    {'test': '6. Package ModelInstance_Set',   'status': 'PASSED'},
    {'test': '7. Save to Disk',                'status': 'PASSED'},
    {'test': '8. Load from Disk',              'status': 'PASSED'},
    {'test': '9. Inference from Loaded Model', 'status': 'PASSED'},
]).set_index('test')

display_df(results_summary)

# Cleanup model_dir
shutil.rmtree(model_dir, ignore_errors=True)
```

---

See Also
========

- **haipipe-nn-0-overview**: Architecture map, decision guide, YAML templates
- **haipipe-nn-1-algorithm**: What algorithms are and their diversity
- **haipipe-nn-2-tuner**: The universal Tuner contract (5 abstract methods)
- **haipipe-nn-3-instance**: The orchestrator contract (5 abstract methods)
