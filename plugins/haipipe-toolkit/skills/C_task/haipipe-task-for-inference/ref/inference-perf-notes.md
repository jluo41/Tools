Inference Performance — harness shape + anti-patterns
======================================================

What an inference-perf task body looks like, the per-step timing model, and
the known bottlenecks this task type exists to catch. Source of truth for
the profiler the `haipipe-task-creator-agent` writes.


The per-step timing model
-------------------------

`endpoint_set.inference(payload, profile=True)` returns `(response, timing)`.
`timing` keys (ms), in execution order:

```
  load_functions    one-time fn loaders (cached after first call)        per-request
  trig_fn           trigger detection on the raw payload                 per-request
  input2src_fn      JSON payload → ProcessedDF source frames             per-request
  prefn_pipeline    Record→Case→AIData feature extraction (1 case)       per-request
                    (+ prefn_details sub-breakdown: record/case/aidata)
  model_inference   the model scores every arm                           PER-ARM  ← watch this
  post_fn           format the response                                  per-arm (cheap)
  total_ms          sum
  slowest_step      the bottleneck key
```

Only `model_inference` (and trivially `post_fn`) scale with the number of
arms. Everything else is per-request and arm-independent.


The harness (what <TASK>.py must do)
------------------------------------

```python
import json, time, copy, statistics
from haipipe import setup_workspace
from haipipe.endpoint_base import Endpoint_Set
import logging; logging.disable(logging.INFO)

_, SPACE, _ = setup_workspace()
ep = Endpoint_Set.load_from_disk(ENDPOINT_SET_PATH, SPACE)
payload = {k: v for k, v in json.load(open(PAYLOAD_PATH)).items() if k != '_metadata'}

ep.inference(copy.deepcopy(payload))                 # 1. warm-up (cold model load)
runs = [ep.inference(copy.deepcopy(payload), profile=True)[1]   # 2. warm × N
        for _ in range(WARM_ITERS)]
per_step = {k: statistics.median(r[k] for r in runs if k in r) for k in runs[0]
            if isinstance(runs[0][k], (int, float))}

# 3. DECOMPOSE model_inference (the arm-dependent step)
mi = ep._model_instance
orig_add, orig_infer = mi._add_treatment_columns, mi.model_tuner.infer
acc = {'add_ms': 0.0, 'infer_ms': 0.0}
mi._add_treatment_columns = lambda d: (_t(lambda: orig_add(d), acc, 'add_ms'))
mi.model_tuner.infer       = lambda d: (_t(lambda: orig_infer(d), acc, 'infer_ms'))
ep.inference(copy.deepcopy(payload))                 # one run to fill acc
# acc['add_ms']  = per-arm dataset-transform cost (the HF-Dataset trap)
# acc['infer_ms'] = csr build + xgb predict cost
```

(`_t` is a tiny timer wrapper that adds elapsed ms to acc[key] and returns the
result.) Always restore the monkeypatched methods after.


KNOWN ANTI-PATTERN #1 — HuggingFace Dataset in the per-arm loop  (the big one)
-----------------------------------------------------------------------------

Symptom: `model_inference` dominates total (e.g. 98%), and within it the
dataset-transform (`_add_treatment_columns`) dwarfs the actual xgb predict.

Cause: `instance_slearner._compute_scores` rebuilds a HuggingFace `Dataset`
per arm and `_add_treatment_columns` calls `Dataset.add_column` once PER ARM
inside that loop → O(arms²) Arrow-table copies. Measured on the 40-arm SMS
ClickPred endpoint (2026-06-01):

```
    model_inference  3692 ms
      ├─ _add_treatment_columns (HF Dataset.add_column)  3005 ms  (80% of TOTAL)
      └─ model_tuner.infer (csr build + xgb predict)      602 ms  (40 predicts)
    everything else (data transform, trig, etc.)           54 ms
    -------------------------------------------------------------
    TOTAL warm                                            3746 ms
```

HuggingFace Dataset (Arrow) is built for large, memory-mapped BATCH
processing — NOT tight per-request loops. Each `.add_column` / `.remove_columns`
copies the whole table.

THE FIX — stay in numpy + scipy.sparse, build shared work once, batch the
arm variants into ONE predict:

```python
from scipy.sparse import csr_matrix, hstack, identity, vstack
import numpy as np
# base feature vector is identical across arms (same patient) — build ONCE
base = csr_matrix((feat_wgt, ([0]*len(feat_idx), feat_idx)), shape=(1, vocab))
actions = sorted(action_to_id.keys())            # match transform_fn's sorted order
X = hstack([vstack([base] * len(actions)),       # N × vocab  (tile the base)
            identity(len(actions), format='csr')],  # N × N    (one-hot block)
           format='csr')                          # N × (vocab + N)
probs  = model_tuner.model.predict_proba(X)[:, 1] # ONE batched predict over N arms
scores = {actions[i]: np.array([probs[i]]) for i in range(len(actions))}
```

VERIFIED (2026-06-01, smsr4 endpoint, applied to instance_slearner._compute_scores):
    model_inference  3692 ms → 9.8 ms     (377× faster)
    total warm       3746 ms → 60.6 ms    (62× faster)
    scores: BYTE-IDENTICAL to the loop (max|Δ| = 0.000e+00 over 40 arms × 3 examples)
    all 40 arms kept. prefn_pipeline (the data transform, ~44 ms) is now the
    largest single step — the arm loop is no longer the bottleneck.
This is the SAME vectorization the offline eval uses to score 40 arms ×
13,529 patients in ~1 s.

  → Reducing 40 arms to 10 ALSO lowers latency (the cost is super-linear in
    arms), but it throws away message coverage and leaves the O(arms²) bug in
    place. Prefer the vectorization fix; cut arms only for a product reason.


KNOWN ANTI-PATTERN #2 — cold-start reported as steady-state
-----------------------------------------------------------

The first `inference()` loads + caches the model (seconds). Reporting that as
"the latency" overstates it. Always warm up once, then median the warm calls.
Note cold vs warm separately if cold matters (serverless scale-from-zero).


KNOWN ANTI-PATTERN #3 — per-request data transform when it could be cached
--------------------------------------------------------------------------

`prefn_pipeline` (Record→Case→AIData) does NDC/NPI/ZIP index lookups. If those
indexes are rebuilt per request, warm them once at load (see
`_warmup_external_data_indexes`). On the SMS endpoint this was already cheap
(~46 ms) — but on heavier feature sets it can dominate; profile before assuming.


Where the actual code fix lives (NOT in this task)
--------------------------------------------------

This task MEASURES; it does not patch the model. The vectorization fix for
anti-pattern #1 belongs in `code/hainn/instance/mlpredictor/instance_slearner.py`
(`_compute_scores` / `_add_treatment_columns`) — editable `hainn`, no `haifn`
regeneration. After the fix, re-run this task to confirm the speedup.
