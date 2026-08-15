# Lesson 07: Set ALL Env Vars Explicitly in Every Notebook

## The Problem

The haipipe framework's `setup_workspace()` and `bootstrap()` functions rely on a comprehensive set of environment variables to locate data stores. Missing even one variable causes either:

- `KeyError: 'LOCAL_EXTERNAL_STORE'` — hard crash
- Silent fallback to local temp paths — data written to ephemeral storage and lost when cluster terminates

On a local machine, `source env.sh` sets all of these. On Databricks, there is no equivalent — you must set them yourself.

## The Complete Env Var List

Every Databricks notebook that uses haipipe must set **all** of these before calling `bootstrap()`:

```python
VOLUME_BASE = "/Volumes/cdhai_welldoc_space/haipipe/reach_space/_WorkSpace"

# 10 LOCAL_* store paths
os.environ["LOCAL_RAW_DATA_STORE"]      = f"{VOLUME_BASE}/0-RawDataStore"
os.environ["LOCAL_SOURCE_STORE"]        = f"{VOLUME_BASE}/1-SourceStore"
os.environ["LOCAL_RECORD_STORE"]        = f"{VOLUME_BASE}/2-RecStore"
os.environ["LOCAL_AIDATA_STORE"]        = f"{VOLUME_BASE}/4-AIDataStore"
os.environ["LOCAL_CASE_STORE"]          = f"{VOLUME_BASE}/3-CaseStore"
os.environ["LOCAL_MODELINSTANCE_STORE"] = f"{VOLUME_BASE}/5-ModelInstanceStore"
os.environ["LOCAL_MODEL_STORE"]         = f"{VOLUME_BASE}/5-ModelInstanceStore"
os.environ["LOCAL_ENDPOINT_STORE"]      = f"{VOLUME_BASE}/6-EndpointStore"
os.environ["LOCAL_EXTERNAL_STORE"]      = f"{VOLUME_BASE}/7-ExternalStore"
os.environ["LOCAL_REFERENCE_STORE"]     = f"{VOLUME_BASE}/8-ReferenceStore"

# REMOTE_* paths (set to "none" when not using remote sync)
os.environ["REMOTE_ROOT"]              = "none"
os.environ["REMOTE_SOURCE_STORE"]      = "none"
os.environ["REMOTE_RECORD_STORE"]      = "none"
os.environ["REMOTE_CASE_STORE"]        = "none"
os.environ["REMOTE_AIDATA_STORE"]      = "none"
os.environ["REMOTE_MODELINSTANCE_STORE"] = "none"
os.environ["REMOTE_ENDPOINT_STORE"]    = "none"
os.environ["REMOTE_EXTERNAL_STORE"]    = "none"
os.environ["REMOTE_REFERENCE_STORE"]   = "none"

# Version
os.environ["EXTERNAL_VERSION"]         = "v0001"
```

## The Bootstrap Pattern

Standard boilerplate for the top of every Databricks notebook:

```python
import os, sys

# Detect Databricks + set paths
try:
    nb_path = dbutils.notebook.entry_point.getDbutils() \
        .notebook().getContext().notebookPath().get()
    _ws_root = "/Workspace" + nb_path.rsplit("/examples/", 1)[0]
    _code = os.path.join(_ws_root, "code")
    if _code not in sys.path:
        sys.path.insert(0, _code)
    os.environ.setdefault("REPO_ROOT", _ws_root)
except NameError:
    pass  # not on Databricks

# Set ALL Volume env vars
_vb = "/Volumes/cdhai_welldoc_space/haipipe/reach_space/_WorkSpace"
os.environ.setdefault("VOLUME_BASE", _vb)
for _k, _p in [
    ("LOCAL_RAW_DATA_STORE",        "0-RawDataStore"),
    ("LOCAL_SOURCE_STORE",          "1-SourceStore"),
    ("LOCAL_RECORD_STORE",          "2-RecStore"),
    ("LOCAL_CASE_STORE",            "3-CaseStore"),
    ("LOCAL_AIDATA_STORE",          "4-AIDataStore"),
    ("LOCAL_MODELINSTANCE_STORE",   "5-ModelInstanceStore"),
    ("LOCAL_MODEL_STORE",           "5-ModelInstanceStore"),
    ("LOCAL_ENDPOINT_STORE",        "6-EndpointStore"),
    ("LOCAL_EXTERNAL_STORE",        "7-ExternalStore"),
    ("LOCAL_REFERENCE_STORE",       "8-ReferenceStore"),
]:
    os.environ.setdefault(_k, f"{_vb}/{_p}")
os.environ.setdefault("REMOTE_ROOT", "none")
for _rk in ["REMOTE_SOURCE_STORE", "REMOTE_RECORD_STORE",
            "REMOTE_CASE_STORE", "REMOTE_AIDATA_STORE",
            "REMOTE_MODELINSTANCE_STORE", "REMOTE_ENDPOINT_STORE",
            "REMOTE_EXTERNAL_STORE", "REMOTE_REFERENCE_STORE"]:
    os.environ.setdefault(_rk, "none")
os.environ.setdefault("EXTERNAL_VERSION", "v0001")

# NOW import and bootstrap
from haiutils.haistep.bootstrap import bootstrap
WORKSPACE_PATH, SPACE, config, logger = bootstrap(CONFIG, REPO_ROOT)
```

## Why `setdefault` Instead of Direct Assignment

Using `os.environ.setdefault()` means:
- If the variable is already set (e.g., by a Databricks job parameter), it's preserved
- If it's missing, the default Volume path is used
- This makes the same notebook work both interactively and as a job task

## When to Apply

- Every single haipipe notebook that runs on Databricks
- Copy-paste the boilerplate block — don't try to factor it out (it needs to run before any imports)
