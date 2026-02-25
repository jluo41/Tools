Architecture Overview (L0)
==========================

Architecture map, decision guide, and model registry for the NN pipeline.
Read this FIRST before any layer-specific reference.

**Scope:** Framework patterns only. Does not catalog project-specific state
(which datasets are available, which experiments have been run). Model registry
snapshots are labeled as such -- always discover current state at runtime.
This reference applies equally to any domain or model family.

---

The 4-Layer Architecture
========================

Every model in this pipeline follows the same 4-layer separation:

```
┌─────────────────────────────────────────────────────────────────┐
│  Layer 4: ModelSet / Pipeline                                   │
│  Packages everything into an Asset. Runs the training pipeline. │
│  Config-driven. Model-type agnostic.                            │
│  Files: code/haipipe/model_base/                                │
├─────────────────────────────────────────────────────────────────┤
│  Layer 3: Instance                                              │
│  Thin orchestrator. Manages one or more Tuners.                 │
│  HuggingFace-style save/load. Config class. Registry.           │
│  Files: code/hainn/<model_family>/instance_*.py                 │
├─────────────────────────────────────────────────────────────────┤
│  Layer 2: Tuner (Train / Optuna)                                │
│  Wraps ONE algorithm. Handles data conversion, training,        │
│  inference, serialization. The ONLY layer that imports           │
│  external libraries.                                            │
│  Files: code/hainn/<model_family>/models/tuner_*.py             │
│  Custom nn.Module: also algorithm_*.py (see ref/layer-1-algorithm.md)     │
├─────────────────────────────────────────────────────────────────┤
│  Layer 1: Algorithm                                             │
│  Two forms:                                                     │
│  (A) External library — XGBoost, PyTorch, HuggingFace, etc.    │
│      Installed via pip. No file to write at this layer.         │
│  (B) Custom algorithm_*.py — nn.Module subclass we write.       │
│      Must implement forward(x) → y. Created when the external   │
│      library alone doesn't cover the architecture we need.      │
│  The Tuner wraps whichever form is chosen.                      │
└─────────────────────────────────────────────────────────────────┘
```

**Layer numbering note:** Skills use bottom-up numbering (1=Algorithm,
2=Tuner, 3=Instance, 4=ModelSet). Source code docstrings use INVERTED
numbering: model_instance.py calls Instance "Layer 2" and model_tuner.py
calls Tuner "Layer 3". Both describe the same architecture stack -- the
numbering direction is simply reversed. Skills are the canonical reference.

---

Decision Tree: Integrating a New Algorithm
==========================================

```
START: I have an algorithm (e.g., diffusion model, LLM, tree model)
│
├─ Q1: What data format does the algorithm need?
│  ├─ Nixtla DataFrame (unique_id, ds, y)  →  domain_format = "nixtla"
│  ├─ Sparse matrix / flat features         →  domain_format = "sparse"
│  ├─ PyTorch tensors                       →  domain_format = "tensor"
│  ├─ HuggingFace Dataset (input_ids, ...)  →  domain_format = "hf_clm"
│  ├─ API call (JSON in, JSON out)          →  domain_format = "llmapi"
│  └─ Something else                        →  domain_format = "custom_name"
│
├─ Q2: How many Tuners does your model need?
│  ├─ ONE algorithm, one model
│  │  → Single Tuner pattern: model_base = {'MAIN': tuner}
│  ├─ ONE algorithm, but treatment/context encoded as input feature
│  │  → Single Tuner + Encoding pattern: model_base = {'MAIN': tuner}
│  │    (Instance handles the encoding before passing to Tuner)
│  └─ MULTIPLE algorithms (one per arm/variant)
│     → Multi-Tuner pattern: model_base = {'arm1': tuner, 'arm2': tuner}
│
│     Bandit note: Multi-arm bandit conceptually fits the Multi-Tuner
│     shape (one model per arm). However, the bandit family does NOT
│     use the canonical base class — no config class, different __init__
│     signature, no model_base dict. If you are adding a bandit-style
│     model, follow code/hainn/bandit/ directly rather than this tree.
│     For a new canonical implementation, prefer Multi-Tuner pattern
│     with one tuner per arm registered in model_base.
│
├─ Q3: Does your algorithm need Optuna hyperparameter tuning?
│  ├─ Yes → Implement objective() in Tuner.fit(), store best_params
│  └─ No  → Simple fit() in Tuner
│
└─ Q4: What serialization format?
   ├─ JSON (XGBoost, LightGBM)              →  model_{key}.json
   ├─ Pickle (sklearn, statsforecast ARIMA) →  model_{key}.pkl
   ├─ PyTorch state_dict                    →  model_{key}/ directory
   ├─ HuggingFace save_pretrained           →  model_{key}/ directory
   ├─ NeuralForecast nf.save()              →  model_{key}/ directory
   └─ Custom                                →  your choice in save_model()

   **Note:** The exact save/load API differs per algorithm. Always check
   the library's own docs before writing save_model() / load_model():
     XGBoost:        model.save_model(path)        / model.load_model(path)
     sklearn:        pickle.dump(model, f)          / pickle.load(f)
     NeuralForecast: nf.save(path=dir)              / NeuralForecast.load(path=dir)
     HuggingFace:    model.save_pretrained(dir)     / AutoModel.from_pretrained(dir)
     PyTorch:        torch.save(state_dict, path)   / model.load_state_dict(...)
```

---

Adding a New Model: Step-by-Step Checklist
==========================================

```
YAML Config Note:
   All 4 layers share ONE YAML file. Write it once at Step 4 and it covers
   all layers. Each layer reads the section relevant to it:

     Layer 1 (Algorithm):  ModelArgs.model_tuner_args
                           e.g., architecture_config, vocab_size,
                           model_name_or_path, TfmArgs
     Layer 2 (Tuner):      ModelArgs.model_tuner_name + model_tuner_args
                           + TrainingArgs hyperparams
     Layer 3 (Instance):   ModelInstanceClass, ModelArgs, TrainingArgs,
                           InferenceArgs, EvaluationArgs
     Layer 4 (Pipeline):   the full config -- drives ModelInstance_Pipeline
                           end-to-end

Step 1: Algorithm (Layer 1)
   [ ] Identify the external library (e.g., xgboost, diffusers, transformers)
   [ ] Determine domain_format and serialization format
   [ ] This library is NEVER imported above the Tuner layer
   [ ] Pure external library (XGBoost, sklearn, Nixtla): no file to create here
   [ ] Custom nn.Module (adds embeddings, fusion, etc.): create
       code/hainn/<family>/models/algorithm_<name>.py
       See ref/layer-1-algorithm.md for the algorithm_*.py pattern.

Step 2: Tuner (Layer 2)
   [ ] Create file: code/hainn/<family>/models/tuner_<name>.py
   [ ] Define standalone transform_fn() at TOP of file
   [ ] Create class inheriting from ModelTuner
   [ ] Set domain_format class attribute
   [ ] Implement 5 abstract methods:
       - get_tfm_data(dataset)
       - fit(dataset, TrainingArgs)
       - infer(dataset, InferenceArgs)
       - save_model(key, model_dir)
       - load_model(key, model_dir)
   [ ] Import algorithm library ONLY in this file

Step 3: Instance (Layer 3)
   [ ] Create file: code/hainn/<family>/instance_<name>.py
   [ ] Create class inheriting from ModelInstance
   [ ] Set MODEL_TYPE class attribute (string for metadata.json)
   [ ] Create MODEL_TUNER_REGISTRY dict mapping name → module path
   [ ] Implement 5 abstract methods:
       - init()                  → create Tuner from registry
       - fit(Name_to_Data)       → delegate to Tuner(s)
       - infer(dataset)          → delegate to Tuner(s)
       - _save_model_base(dir)   → call tuner.save_model() for each
       - _load_model_base(dir)   → init() then tuner.load_model() for each
   [ ] Create @dataclass Config: code/hainn/<family>/configuration_<name>.py
       - Inherit from ModelInstanceConfig
       - Include: ModelArgs, TrainingArgs, InferenceArgs, EvaluationArgs (all Dict)
       - Implement from_aidata_set() factory classmethod
       - Implement from_yaml() factory classmethod (base raises NotImplementedError)
   [ ] Register in code/hainn/model_registry.py:
       elif model_instance_type in ('MyModel', 'MyModelInstance'):
           from hainn.<family>.instance_<name> import MyModelInstance
           from hainn.<family>.configuration_<name> import MyModelConfig
           return MyModelInstance, MyModelConfig

Step 4: ModelSet / Pipeline (Layer 4)
   [ ] Write the single shared YAML config (see templates below)
       This one file drives all 4 layers -- no separate YAML per layer
   [ ] Run through ModelInstance_Pipeline -- no code changes needed at this layer
   [ ] Pipeline handles: config creation, init, fit, evaluate, PreFn, examples, packaging
```

---

Complete Model Registry
=======================

Snapshot (discover current registry at runtime):

```bash
cat code/hainn/model_registry.py
ls code/hainn/
```

Snapshot (as of 2026-02-21 -- always verify with commands above):
(file: code/hainn/model_registry.py)

```
Type String(s)                          Instance Class                  Config Class              Family
───────────────────────────────────     ─────────────────────────────   ────────────────────────  ──────────
'BanditV1'                              BanditInstance                  None (no config class)    bandit
'MLSLearnerPredictor'                   MLSLearnerPredictorInstance     MLSLearnerConfig          mlpredictor
  alias: 'MLSLearnerPredictorInstance'
'MLTLearnerPredictor'                   MLTLearnerPredictorInstance     MLTLearnerConfig          mlpredictor
  alias: 'MLTLearnerPredictorInstance'
'TSDecoderInstance'                     TSDecoderInstance               TSDecoderConfig           tsfm
  alias: 'TSDecoder'              *** NON-FUNCTIONAL: import targets do not exist on disk ***
'TEFMInstance'                          TEFMInstance                    TEFMConfig                tefm
  alias: 'TEFM'
'TEFMForecastInstance'                  TEFMForecastInstance            TEFMForecastConfig        tsforecast
  alias: 'TEFMForecast'           *** NON-FUNCTIONAL: import targets do not exist on disk ***
'TSForecastInstance'                    TSForecastInstance              TSForecastConfig          tsforecast
  aliases: 'DLForecastInstance',
           'TSForecast'
```

**When writing YAML configs:** Use any of the type strings listed above as
the value for ModelInstanceClass. The registry resolves aliases automatically.

**ACTION REQUIRED -- NON-FUNCTIONAL entries:** TSDecoderInstance and
TEFMForecastInstance are registered but their import targets do not exist on disk.
They will throw ImportError at runtime if anyone tries to load them.
Before removing: verify no production config references 'TSDecoder', 'TSDecoderInstance',
'TEFMForecast', or 'TEFMForecastInstance' as ModelInstanceClass. Then delete the
corresponding elif blocks from code/hainn/model_registry.py.

---

YAML Config Templates
=====================

The YAML config drives ModelInstance_Pipeline. The required top-level keys:

```yaml
# Required
ModelInstanceClass: "<type string from registry>"
ModelArgs:
  model_tuner_name: "<tuner class name>"
  # ... tuner-specific args
TrainingArgs:
  # ... training hyperparameters

# Optional
EvaluationArgs:
  # ... evaluation settings
InferenceArgs:
  # ... inference settings
ExampleConfig:
  enabled: false
```

**modelinstance_set_name format:** `f"{name}/{version}"` where version includes the `@` prefix.
Standard: `"MyModel/@v0001-demo"`. Always write `modelinstance_version: '@v0001-...'` in YAML.

**Template A: Time-Series Forecasting (TSForecast)**

```yaml
ModelInstanceClass: "TSForecast"       # or "DLForecastInstance"
ModelArgs:
  model_tuner_name: "NixtlaPatchTSTTuner"
  model_tuner_args:
    h: 12
    input_size: 288
  TfmArgs:
    target_col: "cgm_value"
    time_col: "date"
    id_col: "PatientID"
TrainingArgs:
  max_steps: 100
  learning_rate: 0.001
  early_stopping_patience: 10
  TrainSetNames: ["train"]
  ValSetNames: ["validation"]
InferenceArgs:
  InferSetNames: ["test"]
EvaluationArgs:
  metrics: ["mae", "rmse", "mape"]
```

**Template B: Treatment Effect S-Learner (MLPredictor)**

```yaml
# Pipeline identity (read by test scripts and ModelInstance_Pipeline)
aidata_name: My_AIData
aidata_version: '@v0001'
modelinstance_name: My-SLearner-XGB
modelinstance_version: '@v0001-my-slearner-xgb'

ModelInstanceClass: MLSLearnerPredictor

ModelArgs:
  model_tuner_name: XGBoostTuner
  model_tuner_args:           # all tuner hyperparams go INSIDE model_tuner_args
    n_trials: 20
    validation_size: 0.2
    random_state: 42
    eval_metric: auc
    use_gpu: false
  TfmArgs: {}                 # vocab_size injected by Instance at fit time

TrainingArgs:
  TrainSetNames: [train]

InferenceArgs:
  InferenceSetNames: [test]

EvaluationArgs: {}

InputArgs:
  action_column: experiment_config

meta:
  # action_to_id is auto-extracted from AIData by from_aidata_set().
  # If provided here, it MUST exactly match the AIData value -- the pipeline
  # validates consistency and raises an error on mismatch (no silent failure).
  action_to_id:
    default:    0
    authority:  1
    # ... add all action names with sequential integer IDs
```

**Template C: Foundation Model (TEFM with Tuner)**

```yaml
ModelInstanceClass: "TEFM"
ModelArgs:
  model_tuner_name: "HFNTPTuner"
  model_tuner_args:
    model_name_or_path: "gpt2"
    max_seq_length: 576
  TfmArgs:
    tetoken_config:
      feature_channels: ["cgm", "temporal"]
TrainingArgs:
  num_train_epochs: 10
  per_device_train_batch_size: 32
  learning_rate: 0.0004
  weight_decay: 0.1
InferenceArgs:
  per_device_eval_batch_size: 64
```

**Template D: TEFM Direct Architecture (no Tuner)**

```yaml
ModelInstanceClass: "TEFM"
ModelArgs:
  model_type: "early_fusion"           # No model_tuner_name → direct mode
  d_model: 256
  n_heads: 8
  n_layers: 6
  task_config:                          # task_type lives inside task_config dict
    task_type: "forecasting"
    forecast_horizon: 12
TrainingArgs:
  learning_rate: 0.0001
  batch_size: 128
  num_epochs: 50
  early_stopping_patience: 10
```

---

Existing Model Families: Summary
=================================

Snapshot (discover current families at runtime):

```bash
ls code/hainn/
```

Snapshot (as of 2026-02-21 -- verify with ls above):

```
┌──────────────┬───────────────────────────────────────────────────────────┐
│ Family       │ Description                                             │
├──────────────┼───────────────────────────────────────────────────────────┤
│ tsforecast   │ Time-series forecasting. 15+ Tuners via dict registry.  │
│              │ Clean 4-layer separation. THE REFERENCE IMPLEMENTATION.  │
│              │ Models: PatchTST, NBEATS, NHITS, XGBoost, ARIMA, LLM... │
│              │ Files: code/hainn/tsforecast/                            │
├──────────────┼───────────────────────────────────────────────────────────┤
│ tefm         │ Time-Event Foundation Model. Multi-modal (timeseries +  │
│              │ events + static). Dual-mode: Tuner-based (HFNTPTuner)   │
│              │ or direct architecture (early_fusion, clip, diffusion).  │
│              │ Direct mode has torch imports in Instance (deviation).   │
│              │ Files: code/hainn/tefm/                                  │
├──────────────┼───────────────────────────────────────────────────────────┤
│ mlpredictor  │ Treatment effect estimation. S-Learner (single model,   │
│              │ treatment as feature) and T-Learner (separate models).   │
│              │ Non-canonical pattern: doesn't follow base class          │
│              │ conventions but still actively used in production.        │
│              │ Files: code/hainn/mlpredictor/                           │
├──────────────┼───────────────────────────────────────────────────────────┤
│ bandit       │ Multi-arm bandit. Thompson sampling. No config class.    │
│              │ Different __init__ signature (no config object).         │
│              │ Files: code/hainn/bandit/                                │
├──────────────┼───────────────────────────────────────────────────────────┤
│ tsfm         │ Time-Series Foundation Model (decoder). TSDecoder.      │
│              │ Files: code/hainn/tsfm/tsdecoder/                       │
└──────────────┴───────────────────────────────────────────────────────────┘
```

**Compliance with canonical pattern:**

The canonical interface requires: inherit base class, call super().__init__(),
use model_base dict, implement all 5 abstract methods (init, fit, infer,
_save_model_base, _load_model_base), use model_tuner_name in config.

```
                 Canonical?   Notes
tsforecast       YES          The reference implementation. Follow this.
tefm (tuner)     partial      Stubs for _save/_load_model_base. Has inference() not infer().
tefm (direct)    NO           Torch imports in Instance. Training loops in Instance.
mlpredictor      partial      S-Learner (XGBoostTuner) now canonical: inherits ModelTuner,
                              dict registry, model_base dict, save_pretrained/from_pretrained.
                              Uses inference() not infer() (to be unified). Other tuners partial.
bandit           NO           No super().__init__(), no config class, different __init__ signature.
tsfm/tsdecoder   N/A          Registry entry exists but import targets missing.
```

**For new models:** Follow the tsforecast pattern. Existing non-canonical code
should be migrated toward the standard over time.

---

Key File Locations
==================

```
Base classes:
  ModelTuner:           code/hainn/model_tuner.py
  ModelInstance:        code/hainn/model_instance.py
  ModelInstanceConfig:  code/hainn/model_configuration.py
  Model Registry:       code/hainn/model_registry.py

Pipeline (Layer 4):
  ModelInstance_Set:      code/haipipe/model_base/modelinstance_set.py
  ModelInstance_Pipeline: code/haipipe/model_base/modelinstance_pipeline.py
  PreFnPipeline:         code/hainn/prefn_pipeline.py
  Asset base class:      code/haipipe/assets.py

AutoModelInstance:
  code/hainn/model_instance.py (AutoModelInstance class)

Existing families:
  tsforecast:    code/hainn/tsforecast/
  tefm:          code/hainn/tefm/
  mlpredictor:   code/hainn/mlpredictor/
  bandit:        code/hainn/bandit/
  tsfm:          code/hainn/tsfm/
```

---

Test Notebook Conventions
=========================

Every model family has a `test-modeling-<name>/` directory with test scripts
(one per applicable layer) that double as reviewable notebooks.

**Base model: full 4-layer test suite**

```
test-modeling-ts_clm/              # base ts_clm model -- full suite
├── config_ts_clm_from_scratch.yaml
├── scripts/
│   ├── test_ts_clm_1_algorithm.py   # Layer 1: raw Algorithm
│   ├── test_ts_clm_2_tuner.py       # Layer 2: Tuner + transform_fn
│   ├── test_ts_clm_3_instance.py    # Layer 3: Instance orchestration
│   └── test_ts_clm_4_modelset.py    # Layer 4: ModelInstance_Set packaging
└── notebooks/                        # Auto-generated from scripts (all 4)
```

**Variant model: Layer 1+2 only (shares L3/L4 with base via same Instance)**

```
test-modeling-te_clm_event/        # event variant -- new components only
├── config_te_clm_event_from_scratch.yaml
├── scripts/
│   ├── test_te_clm_event_1_algorithm.py  # Layer 1: new Algorithm
│   └── test_te_clm_event_2_tuner.py      # Layer 2: new Tuner
└── notebooks/                             # 2 notebooks
```

**External-algorithm model: no Layer 1 script needed**

```
test-modeling-mlpredictor-slearner-xgboost/  # mlpredictor -- XGBoost wraps
├── config_mlpredictor_slearner_xgboost.yaml  # external library, no L1 file
├── scripts/
│   ├── test_mlpredictor_slearner_xgboost_3_instance_realdata.py  # L3 real-data
│   └── test_mlpredictor_slearner_xgboost_4_modelset.py           # L4 packaging
└── notebooks/                                                      # auto-generated
```

**Pattern summary:**

```
Situation                              Scripts to write
──────────────────────────────────     ────────────────────────────────────────
Base model (custom algorithm)          L1 + L2 + L3 + L4 (full suite)
Variant (new algorithm / tuner only)   L1 + L2 (shares L3/L4 with base)
External-only algorithm (XGBoost etc.) L2 + L3 + L4 (no L1 — library is L1)
Real-data-only testing                 L3 may use real AIData (no synthetic step)
```

**Core display principle:** At every step, the reviewer should see the actual
data -- what goes IN and what comes OUT. Not just computed summaries.

Two display mechanisms used together:

1. **`print()`** -- Show actual data objects (datasets, samples, dicts)
2. **`display_df()`** -- Show key-value summary tables (config, metrics, status)

**Variable naming convention** (`type_qualifier`):

```
Single HF Dataset:
  ds_raw         raw dataset before transform_fn
  ds_tfm         dataset after transform_fn (has input_ids, attention_mask, labels)

Dict of datasets:
  data_tfm       output of get_tfm_data() -- {split_name: transformed_dataset}
                 (L2 tuner test only -- tests get_tfm_data directly)
  data_fit       raw datasets for fit -- {split_name: raw_dataset}
                 (passed to tuner.fit / instance.fit, which transforms internally)
  data_infer     raw datasets for inference -- {split_name: raw_dataset}
                 (L3/L4; passed to instance.inference)

Inference (L2 tuner, testing multiple input types):
  ds_infer_a     single raw dataset used to build data_infer_a
  data_infer_a   dict input for Type A: {split_name: dataset}
  ds_infer_b     single raw dataset for Type B (passed directly to tuner.infer)
```

**Before/after pattern** (the key convention):

```python
# BEFORE: show what goes into the operation
print("--- BEFORE transform_fn ---")
print(ds_raw)                  # the dataset object
print()
print("Sample [0]:")
print(ds_raw[0])               # one concrete sample

# Run the operation
ds_tfm = transform_fn(ds_raw, TfmArgs)

# AFTER: show what comes out
print("--- AFTER transform_fn ---")
print(ds_tfm)                  # the transformed dataset
print()
print("Sample [0]:")
print(ds_tfm[0])               # one concrete transformed sample
```

**Summary table + Artifacts** (last cell in every notebook):

The 4-column template -- use this in every layer's test:

```
step                             status    key_metric                       artifact / sample
───────────────────────────────  ────────  ───────────────────────────────  ────────────────────────────────────────────────────
1. Load config                   PASSED    tuner=XGBoostTuner, h=12         /abs/path/to/config.yaml
2. Load AIData                   PASSED    train=2475, test=636             /abs/path/to/AIDataStore/
3. Create [object]               PASSED    class=Instance, model_base=MAIN  domain=sparse
4. Prepare data                  PASSED    n_rows=1200, n_features=512      {'uid':'S559','y':1.0}
5. Fit / Forward pass            PASSED    time=2.1s, [model metric]        is_fitted=True
6. Infer / Gradient flow         PASSED    splits=3, total_rows=636         {'uid':'S559','yhat':0.82}
7. Save/load roundtrip           PASSED    weight_delta=0.0, cfg=True       _WorkSpace/5-ModelInstanceStore/{name}/{version}/
```

**Step 5 key_metric is family-specific:**

```
Family              Step 5 key_metric example
──────────────────  ──────────────────────────────────────────
HF Transformer      time=4.2s, final_loss=0.034
XGBoost             time=2.1s, best_iter=127, val_auc=0.821
TSForecast XGB      time=1.8s, is_fitted=True
Nixtla Neural       time=12s, val_loss=0.041
```

**L1 step labels** (layer-appropriate within the unified 7 slots):

- Step 5: "Forward pass (loss)" — not "Fit"
- Step 6: "Gradient flow verify" — not "Infer"
- L2–L4 use the standard "Fit" / "Infer" labels

**Save path:** Step 7 artifact MUST use the proper workspace location:
`_WorkSpace/5-ModelInstanceStore/{modelinstance_name}/{modelinstance_version}/`
Never /tmp/.

**Notebook regeneration** (after any script change):

```bash
python code/scripts/convert_to_notebooks.py \
    --dir <model>/test-modeling-<name>/scripts/ \
    -o <model>/test-modeling-<name>/notebooks/
```
