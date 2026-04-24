PostFn: Response Formatting
============================

One of the 5 inference function types at Stage 6.

PostFn takes the raw model output (per-action score DataFrame) and formats it
into the client-facing JSON response. It handles action filtering, score
scaling, ranking, and response schema construction.

---

Architecture Position
=====================

```
Endpoint_Set.inference()
  ...
  Step 6: ModelInfer    model_input -> DataFrame (score__{action} columns)
  Step 7: PostFn(ModelArtifactName_to_Inference, SPACE)
           -> response_json   <- the final return to the caller
```

PostFn is the last step in the inference pipeline. Its output is returned
directly by endpoint_set.inference().

---

Function Contract
=================

**Signature:** PostFn(ModelArtifactName_to_Inference, SPACE) -> Dict

**Input:**
  ModelArtifactName_to_Inference : Dict[str, pd.DataFrame]
    Keys:   External model name (e.g., "CGMDecoderOhio")
    Values: DataFrame from model_instance.infer()
            Columns: score__{action} (float), best_action (str),
                     uplift__{action} (float, optional)
            Rows:    One row per inference case (usually 1 row)

  SPACE : Dict
    Provides MODEL_ENDPOINT and any reference data paths needed

**Output:**
  Dict matching the standard response schema:
  ```json
  {
    "models": [{
      "name": "ExternalModelName",
      "date": "ISO timestamp",
      "version": "endpoint_name/version",
      "action": {"name": "best_action", "score": 85.42},
      "predictions": [{"name": "action", "score": 85.42}, ...]
    }],
    "status": {"code": 200, "message": "Success"}
  }
  ```

---

Score Conventions
=================

Scores from model_instance.infer() are raw float probabilities [0.0, 1.0].
PostFn typically scales these to a human-readable range [0, 100]:

```python
raw_score = dataset_ifr['score__authority'].iloc[0]   # e.g., 0.854
scaled_score = round(raw_score * 100, 2)              # e.g., 85.4
```

The scaling is Fn-specific. Document the convention in the Fn's MetaDict
comment or docstring.

---

File Structure
==============

```python
# code/haifn/fn_endpoint/fn_post/CGMForecast_v260101.py
# (GENERATED -- do not edit directly)

from datetime import datetime

def PostFn(ModelArtifactName_to_Inference, SPACE):
    """
    Format CGM forecast predictions into client response.
    """
    ENDPOINT_VERSION = SPACE.get('MODEL_ENDPOINT', 'unknown/v0001')
    predictions_list = []
    best_action_name = None
    best_action_score = None

    # Process each model's output
    for model_name, dataset_ifr in ModelArtifactName_to_Inference.items():
        if dataset_ifr is None or len(dataset_ifr) == 0:
            continue

        row = dataset_ifr.iloc[0]

        # Extract scores (columns: score__{action_name})
        score_cols = [c for c in dataset_ifr.columns if c.startswith('score__')]
        action_to_score = {
            col.replace('score__', ''): round(float(row[col]) * 100, 2)
            for col in score_cols
        }

        # Sort by score descending
        ranked = sorted(action_to_score.items(), key=lambda x: x[1], reverse=True)
        predictions_list = [{"name": name, "score": score} for name, score in ranked]

        best_action_name, best_action_score = ranked[0]

    if not predictions_list:
        return {
            "status": {"code": 500, "message": "No predictions generated"},
            "models": []
        }

    model_entry = {
        "name": list(ModelArtifactName_to_Inference.keys())[0],
        "date": datetime.now().isoformat(),
        "version": ENDPOINT_VERSION,
        "action": {"name": best_action_name, "score": best_action_score},
        "predictions": predictions_list,
    }

    return {
        "models": [model_entry],
        "status": {"code": 200, "message": "Success"}
    }


MetaDict = {
    "PostFn": PostFn
}
```

---

Action Filtering
================

PostFn can filter the full action list to only show relevant actions:

```python
# Show only top N actions
ranked = sorted(action_to_score.items(), key=lambda x: x[1], reverse=True)
top_n = ranked[:5]  # Only top 5

# Exclude actions below threshold
filtered = [(name, score) for name, score in ranked if score > 10.0]

# Exclude control action from predictions list but use it for uplift calc
action_list = [name for name in action_to_score if name != 'default']
```

The filtering logic is domain-specific and lives entirely in PostFn.

---

Multi-Model Response
====================

When multiple models are registered (multiple entries in ModelArtifactName_to_Inference),
PostFn can return one entry per model in the "models" list:

```python
model_entries = []
for model_name, dataset_ifr in ModelArtifactName_to_Inference.items():
    # ... process each model
    model_entries.append(model_entry)

return {
    "models": model_entries,
    "status": {"code": 200, "message": "Success"}
}
```

---

Naming Convention
=================

```
File:     fn_endpoint/fn_post/{FnName}.py
Function: PostFn (MUST be exactly this name)
MetaDict: {"PostFn": PostFn}
```

Builder naming convention: c1_build_postfn_{description}.py

Example names:
  OptimalMessage_Holistic_Greedy_v250721
  CGMForecast_v260101

---

Builder Pattern
===============

**Step 1: Edit builder:**

```
code-dev/1-PIPELINE/6-Endpoint-WorkSpace/c1_build_postfn_{description}.py
```

**Step 2: Configure at top:**

```python
OUTPUT_DIR = 'fn_endpoint/fn_post'
FN_NAME = 'CGMForecast_v260101'
RUN_TEST = True
```

**Step 3: Run builder:**

```bash
source .venv/bin/activate && source env.sh && python \
  code-dev/1-PIPELINE/6-Endpoint-WorkSpace/c1_build_postfn_{description}.py
```

NOTE: source .venv/bin/activate does NOT persist across Bash tool calls.
Always chain: source .venv/bin/activate && source env.sh && python <script>

Generates: code/haifn/fn_endpoint/fn_post/{FN_NAME}.py

**Step 4: Reference in YAML:**

```yaml
PostFn: "CGMForecast_v260101"
```

---

MUST DO
=======

1. Name the function exactly PostFn
2. Include MetaDict = {"PostFn": PostFn}
3. Return the standard response dict with "models" and "status" keys
4. Include "status": {"code": 200, "message": "Success"} on success
5. Return {"status": {"code": 500, ...}, "models": []} on error
6. Read ENDPOINT_VERSION from SPACE['MODEL_ENDPOINT']

---

MUST NOT
=========

1. NEVER edit code/haifn/fn_endpoint/fn_post/*.py directly
2. NEVER return raw scores without converting to the response schema
3. NEVER raise exceptions -- catch errors and return {"code": 500, ...} response
4. NEVER import model or pipeline classes inside PostFn
