# Running a Task on Databricks

Use this reference when the canonical Task executes on a Databricks cluster.
The Block/Job/Task/Run hierarchy does not change.

```text
bNN_<block>/jNN_<job>/tNN_<task>/
├── tNN_<task>.md
├── scripts/
│   ├── <worker>.py
│   └── config/rNN_<run>.yaml
└── runs/rNN_<run>.sh
```

The `.py` source remains authoritative. A generated notebook bundle and cluster
execution logs belong under the Run's resolved generated projection, not at
Block or Job root.

## Parameters

Read notebook widgets first and environment variables second so one worker can
run on a cluster and in local validation:

```python
def parameter(name, default):
    try:
        value = dbutils.widgets.get(name)
        if value:
            return value
    except Exception:
        pass
    return os.environ.get(name, default)
```

The Run config remains the authority for what is computed. The Ticket or
cluster launcher may set an execution slice, but must record every effective
value in `runtime.yaml`.

## Execution choices

Use a Databricks Job Task when the cluster policy permits Jobs workloads. On a
policy-locked cluster, a Task may execute its own generated notebook inline in
the active process. Inline execution must remain sequential, preserve the live
Spark/dbutils handles, and prevent child `notebook.exit()` calls from aborting
the parent.

A Job-level batcher may coordinate two or more canonical Task Folders. It calls
their Tickets or submits their notebook artifacts; it never hosts worker code.

## Generated artifacts

```text
$OUTPUT_ROOT/results/<task>/<run>/runtime.yaml
$OUTPUT_ROOT/results/<task>/<run>/<light-results>
$OUTPUT_ROOT/notebooks/<task>/_source.ipynb
$OUTPUT_ROOT/notebooks/<task>/<run>.ipynb
```

For cluster execution, `runtime.yaml` records the Databricks Run id, workspace
path, cluster identity, config hash, source git SHA, start/finish times, and
Result-gate verdict.

Heavy data lands in the configured Unity Catalog Volume using the same store
families as `_WorkSpace/`. PHI remains on the approved server or Volume; only
approved aggregate Results may leave it.

## Memory discipline

- Read Parquet metadata for row/schema checks instead of loading large tables.
- Stream checksums.
- Chunk large source tables and write a success marker for resumability.
- Keep inline execution sequential on a shared Spark session.

## Validation

Before launch, verify the Task Folder with `ref/check_task_tree.py`, confirm the
Run config/Ticket stem pair, and verify that cluster output resolves to the
same `<task>/<run>` Result identity used locally.
