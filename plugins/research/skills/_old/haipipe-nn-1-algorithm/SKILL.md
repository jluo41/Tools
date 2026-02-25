Skill: haipipe-nn-1-algorithm
==============================

Layer 1 of the 4-layer NN pipeline: Algorithm.

An algorithm is any external ML library that does the actual computation.
We don't write algorithms -- we wrap them in Tuners (Layer 2).

**Scope of this skill:** Framework patterns only. Does not catalog
project-specific state (which algorithms are installed, which models have
been trained). Concrete code examples are illustrative. This skill applies
equally to any domain or algorithm type.

---

Architecture Position
=====================

```
Layer 4: ModelSet/Pipeline    Packages everything. Config-driven.
    |
Layer 3: Instance             Thin orchestrator. Manages Tuner dict.
    |
Layer 2: Tuner                Wraps ONE algorithm. Owns data conversion.
    |
Layer 1: Algorithm  <---      Raw external library. Doesn't know the
                              pipeline exists.
```

---

What Is an Algorithm?
=====================

An algorithm is a third-party library installed via pip/conda that provides:
- A model class (e.g., xgb.XGBClassifier, PatchTST, AutoModelForCausalLM)
- A training method (e.g., .fit(), .train(), trainer.train())
- A prediction method (e.g., .predict(), .generate(), .forward())
- A serialization method (e.g., .save_model(), .save_pretrained(), pickle)

**For pure external libraries (XGBoost, sklearn, Nixtla), you never write
Layer 1 code.** You install the library and wrap it in a Tuner (Layer 2).

**When you need a custom nn.Module** (e.g., to add embeddings or fusion layers
on top of a HuggingFace model), you DO write Layer 1 code in an
`algorithm_<name>.py` file. See "When You Write Custom Layer 1 Code" below.

---

Algorithm Diversity
===================

Algorithms vary across every dimension. The Tuner layer absorbs all
this diversity and presents a uniform interface upward.

```
Dimension           Examples                           Tuner Handles Via
──────────────────  ────────────────────────────────   ─────────────────────
Input format        DataFrame, sparse matrix, tensor,  transform_fn()
                    HF Dataset, JSON payload

Training paradigm   .fit(X,y), Trainer.train(),        fit(dataset, TrainingArgs)
                    custom loop, API call

Output format       array, DataFrame, dict, tensor     infer(dataset, InferenceArgs)

Serialization       .save_model(), state_dict,          save_model(key, dir)
                    pickle, save_pretrained

Hyperparameter      Optuna, grid search, none           TrainingArgs + objective()
tuning

Compute             CPU, GPU, multi-GPU, API            Handled inside Tuner
```

**Concrete examples across the spectrum:**

```
Algorithm             Library           Input Format      Save Format
────────────────────  ────────────────  ────────────────  ──────────────
XGBoost               xgboost           sparse matrix     .json
LightGBM              lightgbm          sparse matrix     .txt / .json
CatBoost              catboost          DataFrame         .cbm
PatchTST              neuralforecast    Nixtla DataFrame  checkpoint dir
NBEATS                neuralforecast    Nixtla DataFrame  checkpoint dir
ARIMA                 statsforecast     Nixtla DataFrame  pickle
XGBForecast           mlforecast        Nixtla DataFrame  .json
DeepFM                deepctr-torch     tensor            state_dict
GPT-2/LLaMA (CLM)    transformers      HF Dataset        save_pretrained
EarlyFusionTEFM       custom PyTorch    tensor            state_dict
DiffusionTEFM         custom PyTorch    tensor            state_dict
LLM API               openai/anthropic  JSON              N/A (stateless)
```

---

Domain Formats
==============

Each algorithm family expects data in a specific format. We call this
the "domain format." The Tuner's transform_fn() handles the conversion.

```
domain_format     What it means                   Used by
───────────────   ─────────────────────────────   ──────────────────────
"nixtla"          DataFrame: (unique_id, ds, y)   NeuralForecast,
                  + optional exogenous columns     MLForecast,
                                                   StatsForecast

"sparse"          scipy.sparse.csr_matrix for     XGBoost, LightGBM,
                  features + numpy array labels    DeepFM (via adapter)

"tensor"          PyTorch tensors, often           Custom PyTorch models,
                  (batch, seq_len, features)       TEFM architectures

"hf_clm"          HuggingFace Dataset with         GPT-2, LLaMA,
                  (input_ids, attention_mask,       HFNTPTuner
                  labels) for causal LM

"llmapi"          JSON payload for API call        OpenAI, Anthropic,
                                                   Nixtla TimeGPT API

"custom"          Any format your algorithm        Future models
                  needs -- you define it
```

When creating a new Tuner, pick the domain_format that matches your
algorithm. If none fit, define a new one.

---

Serialization Formats
=====================

```
Format              How to save                 How to load
──────────────────  ─────────────────────────   ─────────────────────────
JSON (tree models)  model.save_model(path)      model.load_model(path)
Pickle (sklearn)    pickle.dump(model, f)       pickle.load(f)
PyTorch state_dict  torch.save(state_dict, p)   model.load_state_dict(...)
HF save_pretrained  model.save_pretrained(dir)  AutoModel.from_pretrained(dir)
Checkpoint dir      model.save(dir)             Model.load(dir)
None (API models)   Save config only            Reconnect via API key
```

---

Concrete Code From the Repo
============================

These show actual algorithm calls inside Tuner files.
(Illustrative -- discover actual Tuner files at runtime):

```bash
ls code/hainn/<family>/models/    # e.g., ls code/hainn/tsforecast/models/
```

**xgboost** (illustrative -- from mlpredictor/models/tuner_xgboost.py):

```python
model = xgb.XGBClassifier(**param)
model.fit(X_train, y_train, eval_set=[(X_valid, y_valid)], verbose=False)
preds = model.predict_proba(X_valid)[:, 1]
```

**neuralforecast** (illustrative -- from tsforecast/models/neuralforecast/modeling_nixtla_patchtst.py):

```python
nf = NeuralForecast(models=[PatchTST(h=24, input_size=288, ...)], freq='5min')
nf.fit(df=df_nixtla)  # DataFrame with [unique_id, ds, y] columns
forecasts = nf.predict()
```

**HuggingFace Transformers** (illustrative -- from tefm/models/hfntp/modeling_hfntp.py):

```python
model = AutoModelForCausalLM.from_pretrained("gpt2")
tokenizer = AutoTokenizer.from_pretrained("gpt2")
trainer = Trainer(model=model, args=training_args, train_dataset=dataset)
trainer.train()
```

**LLM API** (illustrative -- from tsforecast/models/api/modeling_llmapi.py):

```python
client = ChatOpenAI(model="gpt-4o-mini", temperature=0.1)
response = client.invoke([SystemMessage(...), HumanMessage(prompt)])
predictions = json.loads(response.content)
```

---

How to Add a New Algorithm
==========================

**Case A: Pure external library (XGBoost, sklearn, Nixtla, etc.)**

You do NOT write code at Layer 1. Install the library and wrap it in a Tuner.

```
1. Install the library:
   pip install new-algorithm-lib

2. Create a Tuner file:
   code/hainn/<family>/models/tuner_<name>.py

3. Import the algorithm ONLY in that file

4. Implement the Tuner interface (see haipipe-nn-2-tuner)

5. Register the Tuner in the Instance's MODEL_TUNER_REGISTRY
```

**Case B: Custom nn.Module (adds embeddings, fusion, or custom forward pass)**

You DO write Layer 1 code. Create an algorithm file alongside the Tuner.

```
1. Create the Algorithm file (Layer 1):
   code/hainn/<family>/models/algorithm_<name>.py
   - Contains only nn.Module subclass(es)
   - Imports: torch, torch.nn, other algorithm_*.py files only
   - No training logic, no pipeline imports

2. Create the Tuner file (Layer 2):
   code/hainn/<family>/models/tuner_<name>.py
   - Imports Algorithm: from .algorithm_<name> import MyAlgorithm
   - Tuner instantiates Algorithm inside _ensure_model_loaded() or fit()

3. Implement the Tuner interface (see haipipe-nn-2-tuner)

4. Register the Tuner in the Instance's MODEL_TUNER_REGISTRY
```

---

When You Write Custom Layer 1 Code (algorithm_*.py)
====================================================

Some model families write their own nn.Module classes rather than wrapping
a pure external library. These live in `algorithm_*.py` files.

**When to create algorithm_*.py:**
- Adding custom embedding layers on top of a HuggingFace model
  (e.g., time-of-day embedding, event-type embedding)
- Building a custom fusion architecture (early fusion, cross-attention)
- Creating a specialized forward pass that doesn't fit the library's defaults

**File naming:**

```
algorithm_<component_name>.py
class <ComponentName>Algorithm(nn.Module):
```

**Real examples from te_clm:**

```python
# algorithm_ts_clm.py
class TSCLMAlgorithm(nn.Module):
    """Wraps a HuggingFace CausalLM, adding resize_token_embeddings helper."""
    def __init__(self, hf_model): ...
    def forward(self, input_ids, attention_mask, labels, **kwargs): ...

# algorithm_ts_clm_tod.py
class TSCLMWithToDAlgorithm(TSCLMAlgorithm):
    """Adds time-of-day embedding injection to base CLM."""
    def __init__(self, hf_model, hidden_size, tod_num_bins=288):
        super().__init__(hf_model)
        self.tod_embedding = nn.Embedding(tod_num_bins, hidden_size)

# algorithm_te_clm_event.py
class TECLMAlgorithm(TSCLMWithToDAlgorithm):
    """Adds sparse event-type embedding (padding_idx=0 = no_event)."""
    def __init__(self, hf_model, hidden_size, tod_num_bins=288, event_num_types=4):
        super().__init__(hf_model, hidden_size, tod_num_bins)
        self.event_embedding = nn.Embedding(event_num_types, hidden_size, padding_idx=0)
```

Algorithm classes can form an inheritance chain when building capabilities
incrementally. Each subclass adds one concern (ToD, events, etc.).

**Rules for algorithm_*.py:**

```
MUST:
  - Inherit from nn.Module or another Algorithm class
  - Only import: torch, torch.nn, other algorithm_*.py files
  - Implement forward() as the primary interface
  - Be stateless with respect to training (no optimizer, no loss computation)

MUST NOT:
  - Import ModelTuner, ModelInstance, or any pipeline class
  - Contain training loops or data conversion logic
  - Be imported by any layer above the Tuner
```

---

MUST DO
=======

1. **Identify the algorithm's native interface** --
   What does .fit() expect? What does .predict() return? What format?
2. **Determine domain_format** --
   Nixtla DataFrame? Sparse matrix? Tensor? HF Dataset? API payload?
3. **Determine serialization format** --
   JSON? Pickle? state_dict? save_pretrained? None?
4. **Create ONE Tuner per algorithm** --
   Each Tuner wraps exactly one algorithm

---

MUST NOT
========

1. **NEVER import algorithm libraries above the Tuner layer** --
   No xgboost, torch, neuralforecast, sklearn at Instance or Pipeline level
2. **NEVER modify algorithm internals** --
   Use the library's public API as-is; adaptation logic goes in the Tuner
3. **NEVER assume a specific algorithm in upper layers** --
   Pipeline must work with any algorithm that has a Tuner

---

Key File Locations
==================

Discover at runtime:

```bash
ls code/hainn/                          # all model families
ls code/hainn/<family>/models/          # tuner files for a family
cat code/hainn/model_tuner.py           # base class contract
```

Fixed locations:

```
Tuner base class:       code/hainn/model_tuner.py
Tuners (discover):      code/hainn/<family>/models/    <- ls to find
```

---

Test Notebook: What Layer 1 Tests
==================================

The algorithm test exercises the raw library in isolation (NO Tuner wrapper).
It verifies the external API works before wrapping it.

**ALWAYS use real AIData — no synthetic data at any layer.**
Step 2 loads real AIData from disk (same source as L2–L4). This is where
shape mismatches, dtype errors, and vocab size bugs surface before wrapping.

**Unified 7-step structure (L1 uses layer-appropriate labels for Steps 5-6):**

```
Step 1: Load config
        display_df with architecture params (vocab_size, seq_len, model_class)

Step 2: Load real AIData
        print(aidata), print(aidata.dataset_dict['train'][0])

Step 3: Create model from config
        display_df with model class, param count

Step 4: Prepare — tokenizer/preprocessor + design transform_fn
        4a: Tokenizer/preprocessor setup (display_df with pad_token, vocab)
        4b: Design & prototype transform_fn -- BEFORE/AFTER pattern:
            The Layer 1 test is where transform_fn is developed and validated.
            Once working here, it is moved into the Tuner file (Layer 2) as
            a standalone module-level function.
            print(raw_data), print(raw_data[0])
            -> run transform_fn ->
            print(transformed), print(transformed[0])
            sample_input_row = transformed[0]    # capture for artifacts block
        4c: Verify token/feature ranges (assertions + display_df)
        display_df with split summary, n_features/vocab_size

Step 5: Forward pass  [L1 label for the unified "Fit" slot]
        print(batch) before calling forward
        -> model.forward(inputs) ->
        display_df with loss, logits shape, time

Step 6: Gradient flow verify  [L1 label for the unified "Infer" slot]
        optimizer.zero_grad(); loss.backward()
        verify grad coverage, params changed
        sample_output_row = {'loss': loss.item(), 'grad_params': n_updated}
        display_df with grad coverage, params changed

Step 7: Save/load roundtrip
        Save state_dict, reload, verify weight_delta == 0.0
        display_df with weight_delta, cfg match
        model_dir = _WorkSpace/5-ModelInstanceStore/{name}/{version}/
```

```python
display_df(pd.DataFrame([
    {'step': '1. Load config',        'status': 'PASSED', 'key_metric': arch_str,     'artifact': config_path},
    {'step': '2. Load AIData',        'status': 'PASSED', 'key_metric': aidata_str,   'artifact': AIDATA_PATH},
    {'step': '3. Create model',       'status': 'PASSED', 'key_metric': class_str,    'artifact': f'params={n_params}'},
    {'step': '4. Prepare data',       'status': 'PASSED', 'key_metric': vocab_str,    'artifact': str(sample_input_row)},
    {'step': '5. Forward pass',       'status': 'PASSED', 'key_metric': loss_str,     'artifact': logits_shape_str},
    {'step': '6. Gradient flow',      'status': 'PASSED', 'key_metric': grad_str,     'artifact': str(sample_output_row)},
    {'step': '7. Save/load roundtrip','status': 'PASSED', 'key_metric': 'weight_delta=0.0', 'artifact': model_dir},
]).set_index('step'))

# ─── Artifacts (click to open in VS Code) ───────────────────────────────
print(f"\n--- Artifacts ---")
print(f"  Config:        {config_path}")
print(f"  AIData:        {AIDATA_PATH}")
print(f"  Saved model:   {model_dir}")   # _WorkSpace/5-ModelInstanceStore/...
print(f"\n--- Input sample (Step 4b: first transformed row) ---")
print(sample_input_row)   # captured at Step 4b
print(f"\n--- Output sample (Step 6: grad flow result) ---")
print(sample_output_row)  # captured at Step 6
```

**Key display rules for Layer 1:**

- Step 4b is the most important step -- this is where transform_fn is
  DESIGNED, not just tested. Prototype it here, validate with actual data,
  then move the final version into tuner_<name>.py as a standalone function
- Use `print(dataset_object)` to show HF Dataset schema + row count
- Use `print(dataset_object[0])` to show one concrete sample
- Step 5 uses "Forward pass" label (not "Fit"); Step 6 uses "Gradient flow" (not "Infer")
  This is the only layer-appropriate deviation from the L2–L4 naming
- The before/after in Step 4b should clearly show:
  raw feature values -> transformed/tokenized values

**Reference** (discover at runtime):

```bash
ls code/hainn/<family>/test-modeling-<name>/scripts/
# e.g.:
# ls code/hainn/tefm/models/te_clm/test-modeling-te_clm/scripts/
```

See the actual test file (discover with ls above) for a concrete example.
The "Expected steps" and display rules above are the framework pattern.

---

See Also
========

- **haipipe-nn-0-overview**: Architecture map and decision guide
- **haipipe-nn-2-tuner**: How to wrap an algorithm into a Tuner
- **haipipe-nn-3-instance**: How Tuners are managed by Instances
- **haipipe-nn-4-modelset**: How Instances are packaged into assets
