fn-deploy: Deploy Endpoint
===========================

Deploys a packaged Endpoint_Set to a serving platform.
Two supported platforms: Databricks (via MLflow + Unity Catalog) and local.

Always run /haipipe-end test first. Do NOT deploy an untested endpoint.

---

Platform Overview
==================

```
Platform      Wrapper              Registry              Auth
────────────  ───────────────────  ────────────────────  ──────────────────────────────────
Databricks    MLflow PythonModel   Unity Catalog (UC)    DATABRICKS_HOST + TOKEN + USER
Local         direct Python call   filesystem            none
SageMaker     Flask + Docker       S3 + SageMaker        AWS IAM
```

Both Databricks and SageMaker use identical core inference code:
  endpoint_set.inference(payload)
Only the wrapper (MLflow vs Flask) and registry differ.

---

DATABRICKS DEPLOYMENT
======================

The platform-databrick-inference/ submodule handles Databricks deployment.
It is a separate subproject from the main codebase.

**Scripts reference:**

```
scripts/package.py       Package Endpoint_Set to MLflow → Unity Catalog
scripts/deploy.py        Deploy UC model version to Databricks Model Serving
scripts/test.py          Test local MLflow model OR deployed endpoint URL
scripts/test_local.py    Test endpoint DIRECTLY (no MLflow — much faster for dev)
scripts/run_pipeline.py  Run all 3 steps (package + deploy + test) in one command
```

**Four-step process:**

```
Step 1: Set up environment (source env.sh)
Step 2: Test locally (direct, no MLflow -- fast)
Step 3: Package to Unity Catalog (endpoint → MLflow model → UC)
Step 4: Deploy to Model Serving + test deployed URL
```

---

Databricks Step 1: Set Up Environment
=======================================

```bash
cd platform-databrick-inference
source env.sh      # sets DATABRICKS_HOST, DATABRICKS_TOKEN, DATABRICKS_USER, etc.
```

NOTE: source env.sh does NOT persist across Bash tool calls.
Always chain: cd platform-databrick-inference && source env.sh && python <script>

Required env.sh variables:
```bash
export DATABRICKS_HOST="https://your-workspace.azuredatabricks.net"
export DATABRICKS_TOKEN="dapi..."
export DATABRICKS_USER="your.email@domain.com"
```

Verify connection:
```bash
cd platform-databrick-inference && source env.sh && python -c "
from databricks.sdk import WorkspaceClient
client = WorkspaceClient()
print('Connected to:', client.config.host)
"
```

---

Databricks Step 2: Test Locally (Direct — No MLflow)
======================================================

Before packaging to MLflow (which takes 5+ minutes), test the endpoint directly.
This simulates exactly what happens in EndpointSetMLflowModel.predict()
but without the MLflow overhead (~10 seconds vs 5+ minutes).

```bash
cd platform-databrick-inference && source env.sh && python scripts/test_local.py \
    --endpoint-path "../_WorkSpace/6-EndpointStore/endpoint_cgm_decoder_ohio_v0001" \
    --payload examples/cgm_payload.json \
    --profile
```

With performance testing (10 requests):
```bash
cd platform-databrick-inference && source env.sh && python scripts/test_local.py \
    --endpoint-path "../_WorkSpace/6-EndpointStore/endpoint_cgm_decoder_ohio_v0001" \
    --payload examples/cgm_payload.json \
    --num-requests 10
```

What test_local.py does:
  1. Constructs SPACE dict (same as MLflow wrapper)
  2. Loads Endpoint_Set from disk
  3. Calls warmup()
  4. Runs endpoint_set.inference(payload)
  5. Prints response + latency stats

If this fails, fix the endpoint before packaging. Do NOT proceed to MLflow.

---

Databricks Step 3: Create Config File
=======================================

Create or edit config/cgm_ohio_dev.yaml (or staging.yaml / prod.yaml):

```yaml
# platform-databrick-inference/config/cgm_ohio_dev.yaml

# Model and registry
model_name: "cgm-decoder-ohio"          # Short name -> UC: workspace.default.cgm_decoder_ohio
stage: "None"                           # MLflow stage: None | Staging | Production | Archived
model_version: null                     # null = use latest version

# Serving endpoint
endpoint_name: "cgm-decoder-ohio-dev"

# Source endpoint package (relative to platform-databrick-inference/)
endpoint_path: "../_WorkSpace/6-EndpointStore/endpoint_cgm_decoder_ohio_v0001"

# Compute
workload_size: "Small"                  # Small (4GB) | Medium (8GB) | Large (16GB)
scale_to_zero: true
min_instances: 0
max_instances: 5

# Optional: environment variables for the serving container
env_vars:
  LoggerLevel: "DEBUG"
  ENABLE_PROFILING: "True"

# MLflow tracking
experiment_name: "/databricks-inference/dev"

# Output format from EndpointSetMLflowModel
output_format: "dict"                   # dict (default) | dataframe
enable_profiling: true
```

Config variants:
```
config/dev.yaml        Small, scale-to-zero, debug logging, profiling on
config/staging.yaml    Small, 1-10 instances, info logging
config/prod.yaml       Medium, 2-20 instances, warn logging
```

---

Databricks Step 4: Package to Unity Catalog
============================================

```bash
cd platform-databrick-inference && source env.sh && python scripts/package.py \
    --endpoint-path "../_WorkSpace/6-EndpointStore/endpoint_cgm_decoder_ohio_v0001" \
    --model-name "cgm-decoder-ohio" \
    --uc-catalog "workspace" \
    --uc-schema "default"
```

Or using config file:
```bash
cd platform-databrick-inference && source env.sh && python scripts/package.py \
    --config config/cgm_ohio_dev.yaml
```

With --copy-to-local (copies endpoint to platform-databrick-inference/_WorkSpace/ first):
```bash
cd platform-databrick-inference && source env.sh && python scripts/package.py \
    --endpoint-path "../_WorkSpace/6-EndpointStore/endpoint_cgm_decoder_ohio_v0001" \
    --model-name "cgm-decoder-ohio" \
    --copy-to-local
```

Expected output:
```
✓ Packaging Complete
Model: workspace.default.cgm_decoder_ohio
Version: 3
URI: models:/workspace.default.cgm_decoder_ohio/3
```

Note the model version number -- you need it for the deploy step.

**What package.py does:**
- Cleans up macOS/cache artifacts from the endpoint directory
- Creates EndpointSetMLflowModel (MLflow PythonModel wrapper) with:
    load_context() → loads Endpoint_Set from artifacts, calls warmup()
    predict() → calls _prepare_payload() then endpoint_set.inference()
- Defines MLflow signature manually (auto-inference is disabled -- it fails)
- Logs model + artifacts to Databricks tracking (mlflow.set_experiment first)
- Registers in Unity Catalog with 3-level name: catalog.schema.model_name
- Note: model_name hyphens become underscores in UC: cgm-decoder-ohio → cgm_decoder_ohio
- Python 3.10 required (Databricks compatibility)

**SPACE dict inside EndpointSetMLflowModel:**
```python
SPACE = {
    'CODE':                  endpoint_path + '/code',
    'CODE_FN':               endpoint_path + '/code/haifn',
    'LOCAL_EXTERNAL_STORE':  endpoint_path + '/external',
    'LOCAL_REFERENCE_STORE': endpoint_path + '/external/@inference',
    'LOCAL_INFERENCE_STORE': endpoint_path + '/inference',
}
```

---

Databricks Step 5: Test MLflow Model Locally (Optional)
=========================================================

Test the MLflow model before committing to Databricks Model Serving:

```bash
cd platform-databrick-inference && source env.sh && python scripts/test.py \
    --model-uri "models:/workspace.default.cgm_decoder_ohio/3" \
    --payload "../_WorkSpace/6-EndpointStore/endpoint_cgm_decoder_ohio_v0001/examples/example_000_xxx/payload.json"
```

This loads the MLflow model and runs predict(), simulating the full Databricks path.

---

Databricks Step 6: Deploy to Model Serving
===========================================

```bash
cd platform-databrick-inference && source env.sh && python scripts/deploy.py \
    --model-name "workspace.default.cgm_decoder_ohio" \
    --version 3 \
    --endpoint-name "cgm-decoder-ohio-dev" \
    --workload-size "Small" \
    --scale-to-zero
```

Expected output:
```
Deploying Model to Model Serving
Model: workspace.default.cgm_decoder_ohio (version 3)
Endpoint: cgm-decoder-ohio-dev
Waiting for endpoint to be ready (this may take 5-10 minutes)...
  Status: IN_PROGRESS | Ready: NOT_READY | Elapsed: 0m
  Status: IN_PROGRESS | Ready: NOT_READY | Elapsed: 2m
  Status: READY | Ready: READY | Elapsed: 7m
✓ Endpoint ready after 7 minutes
URL: https://your-workspace.azuredatabricks.net/serving-endpoints/cgm-decoder-ohio-dev/invocations
```

Deployment timeline:
  Package: ~5 min
  Register to UC: ~3 min
  Deploy + container start: ~10 min
  Total: ~20 min first time, ~5-7 min for updates

---

Databricks Step 7: Test the Deployed Endpoint
===============================================

```bash
cd platform-databrick-inference && source env.sh && python scripts/test.py \
    --endpoint-url "https://your-workspace.azuredatabricks.net/serving-endpoints/cgm-decoder-ohio-dev/invocations" \
    --payload "../_WorkSpace/6-EndpointStore/endpoint_cgm_decoder_ohio_v0001/examples/example_000_xxx/payload.json" \
    --token "$DATABRICKS_TOKEN"
```

Or benchmark with multiple requests:
```bash
cd platform-databrick-inference && source env.sh && python scripts/test.py \
    --endpoint-url "..." \
    --payload "..." \
    --benchmark \
    --num-requests 100
```

---

Full Pipeline Script (Package + Deploy + Test in One Command)
==============================================================

```bash
cd platform-databrick-inference && source env.sh && python scripts/run_pipeline.py \
    --endpoint-path "../_WorkSpace/6-EndpointStore/endpoint_cgm_decoder_ohio_v0001" \
    --model-name "cgm-decoder-ohio" \
    --endpoint-name "cgm-decoder-ohio-dev" \
    --payload examples/cgm_payload.json
```

Skip packaging (use existing UC model version):
```bash
cd platform-databrick-inference && source env.sh && python scripts/run_pipeline.py \
    --skip-package \
    --model-name "workspace.default.cgm_decoder_ohio" \
    --model-version 3 \
    --endpoint-name "cgm-decoder-ohio-dev" \
    --payload examples/cgm_payload.json
```

Individual step flags: --skip-package, --skip-deploy, --skip-test

---

MLflow Payload Format: Critical Gotcha
========================================

MLflow converts `dataframe_records` format to a pandas DataFrame when passing
to predict(). This strips the outer `{"dataframe_records": [...]}` wrapper.

EndpointSetMLflowModel._prepare_payload() re-wraps it:

```python
# MLflow passes a DataFrame; _prepare_payload converts back:
if isinstance(model_input, pd.DataFrame):
    record = model_input.iloc[0].to_dict()
    return {'dataframe_records': [record]}   # <- re-wrap preserved
```

If you see `KeyError: 'cgm'` or TrigFn returning None for all requests,
the payload format was stripped and not re-wrapped. This is handled by the
EndpointSetMLflowModel but check that you are using the current version.

---

Unity Catalog Model Registry
==============================

After packaging, the model appears in the Unity Catalog registry:

```
Catalog: workspace
  Schema: default
    Model: cgm_decoder_ohio
      Version 1 (archived)
      Version 2 (archived)
      Version 3 (current)        <- most recently packaged
```

Unity Catalog requires 3-level naming: catalog.schema.model_name
  workspace.default.cgm_decoder_ohio
Hyphens in model_name are converted to underscores automatically.

To list versions:
```bash
cd platform-databrick-inference && source env.sh && python -c "
from mlflow import MlflowClient
client = MlflowClient()
versions = client.search_model_versions(\"name='workspace.default.cgm_decoder_ohio'\")
for v in versions:
    print(f'Version {v.version}: {v.current_stage} ({v.creation_timestamp})')
"
```

---

LOCAL DEPLOYMENT
=================

For local testing without any cloud infrastructure:

```python
import os, json
from haipipe.endpoint_base import Endpoint_Set

SPACE = os.environ.copy()
endpoint_set = Endpoint_Set.load_from_disk(
    path='_WorkSpace/6-EndpointStore/endpoint_cgm_decoder_ohio_v0001',
    SPACE=SPACE
)
endpoint_set.warmup()

# Serve locally (simple loop)
with open('test_payload.json') as f:
    payload = json.load(f)

response = endpoint_set.inference(payload)
print(json.dumps(response, indent=2))
```

Or use test_local.py directly (no VENV change needed):
```bash
source .venv/bin/activate && source env.sh && python platform-databrick-inference/scripts/test_local.py \
    --endpoint-path "_WorkSpace/6-EndpointStore/endpoint_cgm_decoder_ohio_v0001" \
    --payload "_WorkSpace/6-EndpointStore/endpoint_cgm_decoder_ohio_v0001/examples/example_000_xxx/payload.json" \
    --profile
```

---

Troubleshooting
================

```
Error                                         Likely cause + fix
────────────────────────────────────────────  ──────────────────────────────────────────────────────────────
ModuleNotFoundError: No module named 'mlflow_model'   code_paths not included in log_model call; re-package
"Legacy registry is disabled"                 Use 3-level UC naming: workspace.default.model_name
"Experiment not found"                        Set experiment before logging: mlflow.set_experiment(path)
"DATABRICKS_USER not set"                     Add DATABRICKS_USER to env.sh; re-source
Inference error: KeyError 'cgm'              Payload format stripped by MLflow; check _prepare_payload()
TrigFn returns None for all requests         entry_type not matching after format strip; see above
"Endpoint not found" after deploy            endpoint_name arg doesn't match what was deployed
"Failed to infer signature"                  Auto-inference disabled; define signature manually
Slow cold start (>10s first request)         Increase min_instances or disable scale_to_zero
"meta.json not found" during packaging       Run /haipipe-end package first; check endpoint dir
Authentication error                         Run: source env.sh; verify DATABRICKS_TOKEN not expired
Python version mismatch                      Use Python 3.10 for packaging (Databricks compatibility)
"MLflow model too large"                     Endpoint + external data large; consider Databricks Volumes
Endpoint limit reached                       Delete old endpoint or update existing: w.serving_endpoints.delete(name=...)
Deployment takes 15-20 min                   Normal for first deploy or cold container start
```

Debugging checklist:
  1. Packaging: code_paths set? Python 3.10? All deps listed?
  2. Unity Catalog: 3-level naming? experiment path set? DATABRICKS_USER in env.sh?
  3. Payload: dataframe_records wrapper preserved? Matches inputSchema?
  4. Environment: source env.sh run? DATABRICKS_TOKEN valid?

---

MUST DO
========

1. Always run /haipipe-end test before deploying
2. Run test_local.py first -- it's 30x faster than packaging to MLflow
3. Source env.sh in platform-databrick-inference/ before running scripts
4. Set DATABRICKS_HOST, DATABRICKS_TOKEN, DATABRICKS_USER in env.sh (all 3 required)
5. Note the Unity Catalog model version after packaging -- needed for deploy
6. Wait for endpoint to reach READY state (5-10 min) before testing
7. Test the deployed endpoint with real payloads after deployment
8. Deploy dev → staging → prod, never skip stages

---

MUST NOT
=========

1. NEVER deploy without running /haipipe-end test first
2. NEVER use Python 3.12 for packaging -- use 3.10 (Databricks compatibility)
3. NEVER hardcode DATABRICKS_TOKEN in scripts -- read from env.sh
4. NEVER skip warmup() in load_context() -- it eliminates cold-start latency
5. NEVER use 2-level model names in Unity Catalog -- always catalog.schema.model
6. NEVER auto-infer MLflow signature -- define it manually in package.py
