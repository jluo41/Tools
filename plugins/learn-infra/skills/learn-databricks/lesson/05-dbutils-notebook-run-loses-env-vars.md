# Lesson 05: dbutils.notebook.run() Sub-notebooks Lose Environment Variables

## The Problem

When an orchestrator notebook calls sub-notebooks via `dbutils.notebook.run()`, the child notebooks **do not inherit `os.environ`** from the parent:

```python
# orchestrator.py
os.environ["VOLUME_BASE"] = "/Volumes/cdhai_welldoc_space/haipipe/reach_space/_WorkSpace"
os.environ["LOCAL_SOURCE_STORE"] = f"{os.environ['VOLUME_BASE']}/1-SourceStore"

# This sub-notebook CANNOT see the env vars set above
result = dbutils.notebook.run("1_source", timeout_seconds=3600)
```

The sub-notebook starts with a clean `os.environ` (only Databricks system vars). Any environment variables you set in the orchestrator are invisible to it.

## The Symptom

Stage notebooks appeared to "succeed" but wrote data to the **temp filesystem** instead of the Unity Catalog Volume. The `bootstrap.py` Volume detection fell back to local paths because the expected env vars were missing. Data was silently lost when the cluster terminated.

## The Solution

### Option A: Set env vars in EVERY notebook (recommended)

Each notebook must have its own bootstrap block that sets ALL required env vars:

```python
_vb = "/Volumes/cdhai_welldoc_space/haipipe/reach_space/_WorkSpace"
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
for _rk in [
    "REMOTE_SOURCE_STORE", "REMOTE_RECORD_STORE", "REMOTE_CASE_STORE",
    "REMOTE_AIDATA_STORE", "REMOTE_MODELINSTANCE_STORE",
    "REMOTE_ENDPOINT_STORE", "REMOTE_EXTERNAL_STORE", "REMOTE_REFERENCE_STORE",
]:
    os.environ.setdefault(_rk, "none")
os.environ.setdefault("EXTERNAL_VERSION", "v0001")
```

### Option B: Use separate job tasks instead of dbutils.notebook.run() (better)

See Lesson 06 — this eliminates the env var problem entirely.

## Why dbutils.notebook.run() Works This Way

`dbutils.notebook.run()` runs the child notebook in a **new Python interpreter context** on the same cluster. It's not a subprocess fork — it's closer to a fresh REPL session. The only data passing mechanism is:
- **Input**: `dbutils.widgets` (parameters passed as strings)
- **Output**: `dbutils.notebook.exit()` (single string return value)

There is no shared memory, no env var inheritance, no module cache sharing.

## The 18+ Env Vars haipipe Needs

The `setup_workspace()` function requires ALL of these to be set:

```
LOCAL_RAW_DATA_STORE, LOCAL_SOURCE_STORE, LOCAL_RECORD_STORE,
LOCAL_CASE_STORE, LOCAL_AIDATA_STORE, LOCAL_MODELINSTANCE_STORE,
LOCAL_MODEL_STORE, LOCAL_ENDPOINT_STORE, LOCAL_EXTERNAL_STORE,
LOCAL_REFERENCE_STORE, REMOTE_ROOT, REMOTE_SOURCE_STORE,
REMOTE_RECORD_STORE, REMOTE_CASE_STORE, REMOTE_AIDATA_STORE,
REMOTE_MODELINSTANCE_STORE, REMOTE_ENDPOINT_STORE,
REMOTE_EXTERNAL_STORE, REMOTE_REFERENCE_STORE, EXTERNAL_VERSION
```

Missing even one (e.g., `LOCAL_EXTERNAL_STORE`) causes a `KeyError` that's hard to debug because it happens deep inside the framework.

## When to Apply

- Any haipipe pipeline running on Databricks where multiple notebooks share a Volume workspace
- **Default to separate job tasks** (Lesson 06) to avoid this problem entirely
