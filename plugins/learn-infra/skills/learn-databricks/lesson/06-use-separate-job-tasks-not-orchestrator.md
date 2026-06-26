# Lesson 06: Use Separate Job Tasks, Not Orchestrator Pattern

## The Problem

The natural instinct is to write one orchestrator notebook that calls all pipeline stages:

```python
# run_pipeline.py — the WRONG approach
dbutils.notebook.run("1_source",   3600, {"VOLUME_BASE": vb})
dbutils.notebook.run("2_record",   3600, {"VOLUME_BASE": vb})
dbutils.notebook.run("3_case",     3600, {"VOLUME_BASE": vb})
dbutils.notebook.run("4_aidata",   3600, {"VOLUME_BASE": vb})
dbutils.notebook.run("1_train_xgb",3600, {"VOLUME_BASE": vb})
dbutils.notebook.run("01_endpoint",3600, {"VOLUME_BASE": vb})
```

This fails because:
1. Sub-notebooks don't inherit `os.environ` (Lesson 05)
2. Sub-notebooks share the same Python process module cache — stale imports cause subtle bugs
3. Widget parameters only pass strings — can't pass complex config
4. Error handling is limited (one failure kills the chain with a cryptic stack trace)

## The Solution

Define each stage as a **separate task** in a Databricks Job (`resources.yml`):

```yaml
resources:
  jobs:
    reach_adhd_pipeline:
      name: "REACH-ADHD Full Pipeline"
      tasks:
        - task_key: stage1_source
          notebook_task:
            notebook_path: notebooks/1_source.py
          existing_cluster_id: "0620-193941-dx4kf6oy"

        - task_key: stage2_record
          depends_on:
            - task_key: stage1_source
          notebook_task:
            notebook_path: notebooks/2_record.py
          existing_cluster_id: "0620-193941-dx4kf6oy"

        - task_key: stage3_case
          depends_on:
            - task_key: stage2_record
          notebook_task:
            notebook_path: notebooks/3_case.py
          existing_cluster_id: "0620-193941-dx4kf6oy"

        # ... and so on
```

## Why Separate Tasks Are Better

| Aspect | Orchestrator (`dbutils.notebook.run`) | Separate Job Tasks |
|--------|---------------------------------------|--------------------|
| Env vars | Not inherited — must set in each child | Each task = fresh Python process |
| Module cache | Shared, stale imports possible | Clean per task |
| Error handling | Chain dies, hard to debug | Each task has own logs, retries |
| Parallelism | Sequential only | DAG-based, can parallelize independent stages |
| Monitoring | One big notebook log | Per-task status in Databricks Jobs UI |
| Retry | Must restart from beginning | Can retry individual failed tasks |
| Cost | Runs serially even if stages could overlap | Independent stages can run in parallel |

## DAG Example for REACH-ADHD

```
stage1_source
      │
      ▼
stage2_record
      │
      ▼
stage3_case
      │
      ▼
stage4_aidata
      │
      ▼
stage5_train ──────▶ stage6_endpoint
                           │
                           ▼
                     deploy_serving
```

Each arrow is a `depends_on` relationship. If stage3 fails, stages 4-6 don't run, but you can see exactly which stage failed and retry from there.

## When to Apply

- **Always** for multi-stage pipelines (more than 2 notebooks)
- Even for 2-notebook pipelines, separate tasks give you better logs and retry
- The only reason to use `dbutils.notebook.run()` is for truly dynamic notebook selection at runtime (rare)
