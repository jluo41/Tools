fn-3-profile: Latency breakdown of an Endpoint_Set's inference
==============================================================

The `profile` verb answers "where does the inference wall-clock go?" — a
per-step timing breakdown + a decomposition of the arm-dependent step. This
is distinct from `test` (which asks "does inference work?").

Two ways to run it; same instrumentation underneath
(`endpoint_set.inference(payload, profile=True)`):

  1. LOCAL (this verb)          — load the Endpoint_Set from disk, profile here.
  2. LOCAL DOCKER               — set `ENABLE_PROFILING=true` on the container;
                                  app_predictor logs the timing summary per request.

For a DURABLE, versioned profile (tracked across model releases, or to A/B a
vectorization fix), scaffold a task instead via `/haipipe-task-for-inference`
(C_task) — same breakdown, recorded as `results/<run>/latency.json`. Preferred
placement: co-locate it in the project's ENDPOINT group as a sibling of the
endpoint-build task (e.g. `tasks/C_endpoint/C2_inference_profile/` next to
`C1_endpoint/`), so the group owns build → profile. Real example:
`examples/ProjA-Click-01-ClickPred/tasks/C_endpoint/C2_inference_profile/`.


Procedure (local)
-----------------

```
Step 0:  Read ../haipipe-end/ref/0-overview.md (Endpoint_Set layout).
Step 1:  Resolve the Endpoint_Set path under _WorkSpace/6-EndpointStore/
         and a sample payload (its own examples/example_001/payload.json).
Step 2:  Run the harness (below). WARM UP once, then median N warm calls.
Step 3:  DECOMPOSE model_inference into dataset-ops vs xgb-predict.
Step 4:  Report the per-step table + slowest_step + the decomposition,
         and flag any known anti-pattern (see below).
```

Harness:

```python
import json, time, copy, statistics
from haipipe import setup_workspace
from haipipe.endpoint_base import Endpoint_Set
import logging; logging.disable(logging.INFO)

_, SPACE, _ = setup_workspace()
ep = Endpoint_Set.load_from_disk(EP_DIR, SPACE)
payload = {k: v for k, v in json.load(open(f"{EP_DIR}/examples/example_001/payload.json")).items()
           if k != '_metadata'}

ep.inference(copy.deepcopy(payload))                                   # warm-up (cold load)
runs = [ep.inference(copy.deepcopy(payload), profile=True)[1] for _ in range(5)]
for k in ('load_functions','trig_fn','input2src_fn','prefn_pipeline',
          'model_inference','post_fn','total_ms'):
    if k in runs[0]:
        print(f"{k:18s} {statistics.median(r[k] for r in runs if k in r):8.1f} ms")

# decompose the arm-dependent step
mi = ep._model_instance
oa, oi = mi._add_treatment_columns, mi.model_tuner.infer
acc = {'add':0.0,'inf':0.0}
def w(f,key):
    def g(x):
        t=time.perf_counter(); r=f(x); acc[key]+=(time.perf_counter()-t)*1000; return r
    return g
mi._add_treatment_columns, mi.model_tuner.infer = w(oa,'add'), w(oi,'inf')
ep.inference(copy.deepcopy(payload))
print(f"  model_inference split → add_treatment_cols {acc['add']:.0f} ms | tuner.infer {acc['inf']:.0f} ms")
mi._add_treatment_columns, mi.model_tuner.infer = oa, oi              # restore
```

Local docker variant: run the container with `-e ENABLE_PROFILING=true`,
hit `/invocations`, then read the timing summary from the container logs
(`app_predictor` logs `timing['summary']` per request).


Anti-patterns to flag (the reason this verb exists)
---------------------------------------------------

If the breakdown shows `model_inference` dominating AND its
`add_treatment_cols` component dwarfing `tuner.infer`, you have hit the
**HuggingFace-Dataset-in-the-per-arm-loop** trap — `_add_treatment_columns`
calls `Dataset.add_column` per arm, O(arms²) Arrow copies. Measured on the
40-arm SMS ClickPred endpoint (2026-06-01): model_inference 3692 ms, of which
3005 ms (80% of total) was the HF-Dataset ops, only 602 ms was XGBoost.

Fix (NOT in this skill — it is a `hainn` change): replace the HF-Dataset loop
with scipy.sparse — build the base feature matrix ONCE, append the N one-hot
variants as a single sparse identity block, run ONE batched `predict_proba`.
~80-150× faster, all arms kept. Full sketch + numbers:
`skills/C_task/haipipe-task-for-inference/ref/inference-perf-notes.md`.
The code site is `code/hainn/instance/mlpredictor/instance_slearner._compute_scores`.

Other flags: cold-call reported as steady-state (always warm up); per-request
external-index rebuilds in prefn_pipeline (warm them at load).


Return contract
---------------

```
status:    ok
summary:   Profiled <endpoint>: warm total <X> ms, slowest_step <step>.
           model_inference split: add_cols <A> ms / predict <B> ms.
artifacts: [endpoint path, the per-step breakdown]
next:      if add_cols dominates → vectorize _compute_scores (hainn fix),
           then /haipipe-task-for-inference to record the speedup.
```
