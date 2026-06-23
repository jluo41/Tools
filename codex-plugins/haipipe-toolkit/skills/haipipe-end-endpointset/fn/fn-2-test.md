fn-test: Inference Test Protocol
==================================

Tests Endpoint_Set.inference() with real payloads and profiling.
Always run this after packaging (/haipipe-end package) and before
deployment (/haipipe-end deploy).

---

Step 1: Check Prerequisites
=============================

```bash
source .venv/bin/activate && source env.sh
```

NOTE: source .venv/bin/activate does NOT persist across Bash tool calls.
Always chain: source .venv/bin/activate && source env.sh && python <script>
Or call venv Python directly: .venv/bin/python script.py

Verify the endpoint was packaged:
```bash
ls _WorkSpace/6-EndpointStore/{endpoint_name}/manifest.json
ls _WorkSpace/6-EndpointStore/{endpoint_name}/examples/
```

---

Step 2: Load the Endpoint
===========================

```python
import os, json
from haipipe.endpoint_base import Endpoint_Set

SPACE = os.environ.copy()

endpoint_set = Endpoint_Set.load_from_disk(
    path='_WorkSpace/6-EndpointStore/{endpoint_name}',
    SPACE=SPACE
)
print("Loaded endpoint:", endpoint_set.endpoint_name)
```

---

Step 3: Warmup
===============

Always warmup before running inference. Warmup pre-loads all components
to eliminate cold-start latency on the first real request.

```python
import time
t0 = time.time()
endpoint_set.warmup()
warmup_ms = (time.time() - t0) * 1000
print(f"Warmup complete: {warmup_ms:.0f}ms")
```

Expected warmup time: 100-2000ms depending on model size and external data.
If warmup takes > 5s, investigate which component is slow.

---

Step 4: Load Test Payloads
============================

Use the payloads generated during packaging from training examples:

```python
import glob

payload_files = sorted(glob.glob(
    '_WorkSpace/6-EndpointStore/{endpoint_name}/examples/*/payload.json'
))
print(f"Found {len(payload_files)} test payloads")

# Load first payload for inspection
with open(payload_files[0]) as f:
    test_payload = json.load(f)

print("Payload format:", list(test_payload.keys()))
if 'dataframe_records' in test_payload:
    print("Format: Databricks dataframe_records")
    print("Record fields:", list(test_payload['dataframe_records'][0].keys()))
else:
    print("Format: Legacy flat")
    print("Fields:", list(test_payload.keys()))
```

---

Step 5: Run Inference with Profiling
======================================

```python
# Run single inference with profiling
response, timing = endpoint_set.inference(test_payload, profile=True)

# Check response
print("\n--- Response ---")
print("Status:", response['status'])
print("Models:", len(response.get('models', [])))
if response.get('models'):
    model = response['models'][0]
    print("  Model name:", model.get('name'))
    print("  Best action:", model.get('action', {}).get('name'))
    print("  Best score:", model.get('action', {}).get('score'))
    print("  N predictions:", len(model.get('predictions', [])))

# Check timing
print("\n--- Timing ---")
print(f"Total: {timing['total_ms']:.1f}ms")
print(f"Slowest step: {timing['slowest_step']}")
print("\nPer-step breakdown:")
for step, ms in timing['steps'].items():
    if isinstance(ms, (int, float)):
        print(f"  {step}: {ms:.1f}ms")

# Print full timing summary table if available
if 'summary' in timing:
    print(timing['summary'])
```

---

Step 6: Run All Test Payloads
================================

Test every available payload to catch edge cases:

```python
results = []
for i, payload_path in enumerate(payload_files):
    with open(payload_path) as f:
        payload = json.load(f)

    try:
        response, timing = endpoint_set.inference(payload, profile=True)
        status_code = response['status']['code']
        n_models = len(response.get('models', []))
        best_action = response['models'][0]['action']['name'] if n_models > 0 else 'N/A'
        results.append({
            'example': i,
            'status': 'PASS' if status_code == 200 else 'FAIL',
            'total_ms': round(timing['total_ms'], 1),
            'best_action': best_action,
        })
    except Exception as e:
        results.append({
            'example': i,
            'status': 'ERROR',
            'total_ms': 0.0,
            'best_action': str(e)[:40],
        })

import pandas as pd
df_results = pd.DataFrame(results)
print(df_results.to_string(index=False))

# Summary stats
print(f"\nPASS: {(df_results['status']=='PASS').sum()}/{len(df_results)}")
print(f"Mean latency: {df_results['total_ms'].mean():.1f}ms")
print(f"Max latency:  {df_results['total_ms'].max():.1f}ms")
```

---

Step 7: Verify Response Schema
================================

Check the response matches the expected schema:

```python
def check_response_schema(response, example_idx):
    issues = []

    # Top-level keys
    if 'status' not in response:
        issues.append("[BLOCK] Missing 'status' key")
    if 'models' not in response:
        issues.append("[BLOCK] Missing 'models' key")

    # Status
    status = response.get('status', {})
    if status.get('code') != 200:
        issues.append(f"[ERROR] status.code = {status.get('code')} (expected 200)")

    # Models
    for m_idx, model in enumerate(response.get('models', [])):
        if 'name' not in model:
            issues.append(f"[WARN] models[{m_idx}] missing 'name'")
        if 'action' not in model:
            issues.append(f"[ERROR] models[{m_idx}] missing 'action'")
        if 'predictions' not in model:
            issues.append(f"[WARN] models[{m_idx}] missing 'predictions'")
        action = model.get('action', {})
        if 'name' not in action or 'score' not in action:
            issues.append(f"[ERROR] models[{m_idx}].action missing name or score")

    if not issues:
        print(f"  example_{example_idx}: PASS (schema OK)")
    else:
        for issue in issues:
            print(f"  example_{example_idx}: {issue}")

for i, payload_path in enumerate(payload_files[:3]):
    with open(payload_path) as f:
        payload = json.load(f)
    response, _ = endpoint_set.inference(payload, profile=True)
    check_response_schema(response, i)
```

---

Step 8: Performance Benchmarking (Optional)
=============================================

Run repeated inferences to measure steady-state latency:

```python
import time

N_RUNS = 20
with open(payload_files[0]) as f:
    payload = json.load(f)

latencies = []
for _ in range(N_RUNS):
    t0 = time.time()
    response, _ = endpoint_set.inference(payload, profile=False)
    latencies.append((time.time() - t0) * 1000)

print(f"Benchmark ({N_RUNS} runs):")
print(f"  Mean:   {sum(latencies)/len(latencies):.1f}ms")
print(f"  Median: {sorted(latencies)[N_RUNS//2]:.1f}ms")
print(f"  P95:    {sorted(latencies)[int(N_RUNS*0.95)]:.1f}ms")
print(f"  Max:    {max(latencies):.1f}ms")
```

Target latencies (rough guidelines):
  < 50ms  : excellent (simple tabular model + small external data)
  50-200ms: good (HF model or large PreFnPipeline)
  200-500ms: acceptable (large NN or heavy external lookups)
  > 500ms : investigate (profile to find bottleneck)

---

Troubleshooting
================

```
Error                                      Likely cause + fix
─────────────────────────────────────────  ────────────────────────────────────────
Response has status code 500              TrigFn, Input2SrcFn, or PostFn raised exception
TrigFn returns None for all payloads     Payload format doesn't match TrigFn expectations
PreFnPipeline step takes > 200ms         CaseFn bottleneck -- check casefn_breakdown
Model inference takes > 300ms            Large model -- consider caching or smaller model
key_metric score = 0.0 for all actions   Model is untrained or InferenceArgs mismatch
warmup() failed with ImportError         Fn .py file not in code/haifn/fn_endpoint/
```
