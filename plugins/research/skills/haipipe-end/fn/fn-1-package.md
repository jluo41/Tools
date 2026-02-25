fn-package: Run Endpoint_Pipeline
===================================

Packages a trained ModelInstance_Set (Stage 5) into a self-contained
Endpoint_Set (Stage 6) ready for inference or deployment.

---

Step 1: Check Prerequisites
=============================

```bash
source .venv/bin/activate && source env.sh
```

NOTE: source .venv/bin/activate does NOT persist across Bash tool calls.
Always chain: source .venv/bin/activate && source env.sh && python <script>
Or call venv Python directly: .venv/bin/python script.py

Verify env vars:
  echo $LOCAL_MODELINSTANCE_STORE     <- Stage 5 input
  echo $LOCAL_ENDPOINT_STORE          <- Stage 6 output
  echo $CODE_FN                       <- fn_endpoint/ location

---

Step 2: Discover Available Stage 5 Assets
==========================================

```bash
ls _WorkSpace/5-ModelInstanceStore/
```

For the target model, confirm it was saved cleanly:

```bash
ls _WorkSpace/5-ModelInstanceStore/{model_name}/{version}/
# Must see: model/, training/, manifest.json
# Must also see: examples/ (required for payload generation)
```

If examples/ is missing from Stage 5, packaging will succeed but no
test payloads will be generated. Re-run model training with ExampleConfig.

---

Step 3: Verify All 5 Fn Files Exist
======================================

Before running Endpoint_Pipeline, confirm each Fn .py file exists:

```bash
ls code/haifn/fn_endpoint/fn_meta/{MetaFnName}.py
ls code/haifn/fn_endpoint/fn_trig/{TrigFnName}.py
ls code/haifn/fn_endpoint/fn_post/{PostFnName}.py
ls code/haifn/fn_endpoint/fn_src2input/{Src2InputFnName}.py
ls code/haifn/fn_endpoint/fn_input2src/{Input2SrcFnName}.py
```

If any file is missing, run the corresponding builder first:
  /haipipe-end design [fn-type]

---

Step 4: Prepare the YAML Config
=================================

Create or locate config/test-haistep-{cohort}/6_test_endpoint.yaml:

```yaml
# Stage 5 input
modelinstance_name: "Demo_Small_TSDecoder_ModelInstance"
modelinstance_version: "@v0001"

# Stage 6 output
endpoint_name: "endpoint_cgm_decoder_ohio"
endpoint_version: "v0001"

# Inference functions (exact .py filename without extension)
MetaFn: "CGMDecoder_DBR_v260101"
Input2SrcFn: "CGMDecoder_DBR_Payload2Src_v260101"
Src2InputFn: "CGMDecoder_DBR_Src2Payload_v260101"
TrigFn: "CGM5Min_v260101"
PostFn: "CGMForecast_v260101"

# Optional deployment target
deployment_config:
  environment: "test"
  platform: "local"
```

---

Step 5: Run the Pipeline
==========================

Use the CLI command:

```bash
source .venv/bin/activate && source env.sh && \
  haistep-endpoint --config config/test-haistep-{cohort}/6_test_endpoint.yaml
```

Or run directly in Python:

```python
import os, json
from haipipe.endpoint_base import Endpoint_Pipeline
from haipipe.model_base.modelinstance_set import ModelInstance_Set

SPACE = os.environ.copy()   # contains LOCAL_ENDPOINT_STORE, CODE_FN, etc.

# Load config
import yaml
with open('config/test-haistep-{cohort}/6_test_endpoint.yaml') as f:
    config = yaml.safe_load(f)

# Load Stage 5 model
modelinstance_set = ModelInstance_Set.load_asset(
    path=f"{config['modelinstance_name']}/{config['modelinstance_version']}",
    SPACE=SPACE
)

# Package
pipeline = Endpoint_Pipeline(config=config, SPACE=SPACE)
endpoint_set = pipeline.run(
    modelinstance_set=modelinstance_set,
    endpoint_name=config['endpoint_name'],
    endpoint_version=config['endpoint_version'],
    deployment_config=config.get('deployment_config')
)

# Save -- pipeline does NOT auto-save
saved_path = endpoint_set.save_to_disk()
print(f"Saved to: {saved_path}")
```

---

Step 6: Verify Output
=======================

After saving, check the directory structure:

```bash
ls _WorkSpace/6-EndpointStore/{endpoint_name}/
# Expected: model/ code/ external/ examples/ manifest.json meta.json

ls _WorkSpace/6-EndpointStore/{endpoint_name}/examples/
# Expected: example_000_{uuid}/ example_001_{uuid}/ ...

ls _WorkSpace/6-EndpointStore/{endpoint_name}/examples/example_000_{uuid}/
# Expected: ProcName_to_ProcDf/ payload.json prediction_results.json

cat _WorkSpace/6-EndpointStore/{endpoint_name}/manifest.json | python -m json.tool
# Check: endpoint_name, endpoint_version, inference_functions, created_at
```

Check that payload.json files were generated:

```python
import json, os

endpoint_dir = '_WorkSpace/6-EndpointStore/{endpoint_name}'
examples_dir = os.path.join(endpoint_dir, 'examples')

for ex_dir in os.listdir(examples_dir):
    payload_path = os.path.join(examples_dir, ex_dir, 'payload.json')
    if os.path.exists(payload_path):
        with open(payload_path) as f:
            payload = json.load(f)
        print(f"{ex_dir}: payload keys = {list(payload.keys())}")
    else:
        print(f"{ex_dir}: MISSING payload.json -- Src2InputFn may have failed")
```

---

Step 7: Quick Smoke Test
=========================

Run a quick inference to verify the endpoint works before proceeding to deploy:

```bash
source .venv/bin/activate && source env.sh && python -c "
import json, os
from haipipe.endpoint_base import Endpoint_Set

SPACE = os.environ.copy()
endpoint_set = Endpoint_Set.load_from_disk(
    path='_WorkSpace/6-EndpointStore/{endpoint_name}',
    SPACE=SPACE
)
endpoint_set.warmup()

# Use first example payload
import glob
payload_files = glob.glob('_WorkSpace/6-EndpointStore/{endpoint_name}/examples/*/payload.json')
with open(payload_files[0]) as f:
    payload = json.load(f)

response, timing = endpoint_set.inference(payload, profile=True)
print('Status:', response['status'])
print('Total ms:', timing['total_ms'])
print('Response models:', len(response.get('models', [])))
"
```

---

Troubleshooting
================

```
Error                                      Likely cause + fix
─────────────────────────────────────────  ────────────────────────────────────────
FileNotFoundError: fn_meta/{FnName}.py    Run builder for that Fn type first
examples/ empty in Stage 5               Retrain model with ExampleConfig enabled
payload.json missing in examples/        Src2InputFn returned None or raised error
manifest.json not found in Stage 5       Stage 5 was not saved cleanly; re-run
KeyError: 'MetaFn'                        YAML config missing required Fn name key
```
