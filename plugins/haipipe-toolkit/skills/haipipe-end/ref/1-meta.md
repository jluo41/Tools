MetaFn: Model Metadata
=======================

One of the 5 inference function types at Stage 6.

MetaFn returns model metadata: the external model name mapping, the list of
available predictions, and the pre-built metadata response for API callers.
It is called once during packaging (Endpoint_Pipeline.run()) and its output
is stored in meta.json at the endpoint root.

---

Architecture Position
=====================

```
Endpoint_Pipeline.run()
  ├── MetaFn(SPACE)             <- called ONCE during packaging
  │     -> meta_results stored in meta.json
  ├── Src2InputFn(ProcDF, SPACE) <- generates test payloads
  └── Endpoint_Set
        └── inference()
              Step 1: TrigFn
              Step 2: Input2SrcFn
              Steps 3-5: PreFnPipeline
              Step 6: ModelInfer
              Step 7: PostFn
```

MetaFn is NOT called per-request. It runs at packaging time only.

---

Function Contract
=================

**Signature:** MetaFn(SPACE) -> Dict

**Input:**
  SPACE : Dict
    Must contain: MODEL_ENDPOINT (set by pipeline before calling MetaFn)
    Format: MODEL_ENDPOINT = "{endpoint_name}/{endpoint_version}"
    e.g., "endpoint_cgm_decoder_ohio/v0001"

**Required output keys:**

```python
{
  'Local_to_External_ModelSeries': Dict[str, str],
    # Maps internal endpoint path -> external model name
    # e.g., {"endpoint_cgm_decoder_ohio/v0001": "CGMDecoderOhio"}

  'External_to_Local_ModelSeries': Dict[str, str],
    # Reverse mapping (auto-derive from above)
    # e.g., {"CGMDecoderOhio": "endpoint_cgm_decoder_ohio/v0001"}

  'modelMetadata': List[Dict],
    # List of model metadata dicts, one per model
    # Required keys per entry: modelName, predictions (list of action names)

  'metadata_response': Dict,
    # Pre-built response for metadata API requests
    # Structure: {"body": {"modelMetadata": [...]}, "contentType": ..., ...}
}
```

---

File Structure
==============

```python
# code/haifn/fn_endpoint/fn_meta/MyCGMDecoder_v260101.py
# (GENERATED -- do not edit directly)

def MetaFn(SPACE):
    ENDPOINT_NAME = SPACE['MODEL_ENDPOINT']   # e.g., 'endpoint_cgm_decoder/v0001'

    # Step 1: Define external model name
    modelName = 'CGMDecoderOhio'              # Name used in client requests

    # Step 2: Name mappings
    Local_to_External_ModelSeries = {
        ENDPOINT_NAME: modelName
    }
    External_to_Local_ModelSeries = {
        v: k for k, v in Local_to_External_ModelSeries.items()
    }

    # Step 3: Model metadata
    modelMetadata = [{
        'modelName': modelName,
        'predictions': [
            'normal_range',
            'approaching_hypo',
            'approaching_hyper',
        ]
    }]

    # Step 4: Pre-built metadata response
    metadata_response = {
        "body": {"modelMetadata": modelMetadata},
        "contentType": "application/json",
        "invokedProductionVariant": "AllTraffic"
    }

    return {
        'Local_to_External_ModelSeries': Local_to_External_ModelSeries,
        'External_to_Local_ModelSeries': External_to_Local_ModelSeries,
        'modelMetadata': modelMetadata,
        'metadata_response': metadata_response,
    }

MetaDict = {
    "MetaFn": MetaFn
}
```

---

Naming Convention
=================

```
File:    fn_endpoint/fn_meta/{FnName}.py
Class:   (no class -- standalone function)
Function: MetaFn (MUST be exactly this name)
MetaDict key: "MetaFn"
```

Builder naming convention: a1_build_metafn_{description}.py

Example names: SMSR2_13Messages, CGMDecoder_DBR_v260101, BanditSMS_v250225

---

How MetaFn Is Loaded
=====================

```python
# Via the loader at Endpoint_Pipeline init time:
from haipipe.endpoint_base.builder.metafn import MetaFn as MetaFnLoader
loader = MetaFnLoader(config['MetaFn'], SPACE)
# loader.MetaFn is the callable
result = loader.MetaFn(SPACE)
```

The loader uses Base.load_module_variables(pypath) to dynamically import the
generated .py file and extract the MetaFn function from MetaDict.

---

Where meta.json Is Written
===========================

After MetaFn(SPACE) is called during packaging, the result is stored as
meta.json at the Endpoint_Set root:

```
_WorkSpace/6-EndpointStore/{endpoint_name}/
└── meta.json     <- written by Endpoint_Pipeline.run()
```

Content is the full return dict from MetaFn(SPACE).

---

Builder Pattern
===============

**Step 1: Edit builder in code-dev/6-Endpoint-WorkSpace/**

```
code-dev/1-PIPELINE/6-Endpoint-WorkSpace/a1_build_metafn_{description}.py
```

**Step 2: Configure at top of builder:**

```python
OUTPUT_DIR = 'fn_endpoint/fn_meta'
FN_NAME = 'MyCGMDecoder_v260101'
RUN_TEST = True
```

**Step 3: Define MetaFn:**

Define the MetaFn function exactly as shown in "File Structure" above.

**Step 4: Run builder:**

```bash
source .venv/bin/activate && source env.sh && python \
  code-dev/1-PIPELINE/6-Endpoint-WorkSpace/a1_build_metafn_{description}.py
```

NOTE: source .venv/bin/activate does NOT persist across Bash tool calls.
Always chain the commands as shown above.

This generates: code/haifn/fn_endpoint/fn_meta/{FN_NAME}.py

**Step 5: Reference in YAML config:**

```yaml
MetaFn: "MyCGMDecoder_v260101"
```

---

MUST DO
=======

1. Name the function exactly MetaFn (not meta_fn, not MetaFunction)
2. Include MetaDict = {"MetaFn": MetaFn} at the bottom of the file
3. Return all 4 required keys: Local_to_External_ModelSeries,
   External_to_Local_ModelSeries, modelMetadata, metadata_response
4. Read MODEL_ENDPOINT from SPACE (do not hardcode the endpoint path)
5. Include at least one entry in modelMetadata with modelName + predictions list

---

MUST NOT
=========

1. NEVER edit code/haifn/fn_endpoint/fn_meta/*.py directly -- use the builder
2. NEVER call MetaFn at inference time -- it runs during packaging only
3. NEVER hardcode the endpoint name string -- always use SPACE['MODEL_ENDPOINT']
4. NEVER omit MetaDict -- the loader extracts the function via MetaDict
