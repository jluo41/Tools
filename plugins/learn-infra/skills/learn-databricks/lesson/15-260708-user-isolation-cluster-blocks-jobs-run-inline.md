# Lesson 15: Policy-Locked "Standard" (USER_ISOLATION) Clusters Forbid Jobs — Run Stages In-Process

## The Problem

On the **REACH** Databricks workspace (not WellDoc/CDHAI), the only available
cluster is **"REACH Small Compute"** — access mode **Standard (Shared /
USER_ISOLATION)**, locked by a compute **policy** the user cannot edit. This
policy disallows *jobs workload*.

The whole pipeline orchestration is built on `dbutils.notebook.run()` (the
per-project `run_reach_*` driver → the A00 `run_pipeline_*_raw` orchestrator →
each stage). Every one of those calls launches the child notebook as an
**ephemeral job** — which the policy blocks. So the pipeline dies at the very
first stage.

> Note: this is the mirror image of Lesson 06. Lesson 06 says "use separate job
> tasks, not the orchestrator." That advice assumes a **jobs-capable** cluster
> (WellDoc/CDHAI had one). When the cluster is policy-locked to interactive-only,
> **jobs are not an option at all** — neither `dbutils.notebook.run()` nor a
> Databricks Job. You must run everything inside the one interactive notebook.

## The Symptom

```
com.databricks.WorkflowException:
  DatabricksServiceHttpClientException: INVALID_PARAMETER_VALUE:
  The cluster 0527-155652-i27u42oy does not support jobs workload
    at com.databricks.workflow.WorkflowDriver.run(...)
    at com.databricks.dbutils_v1.impl.NotebookUtilsImpl.run(...)
```

Confirm the cause: **Edit cluster → Advanced → Access mode = Standard (🔒
locked)**. There is no jobs / `workload_type` toggle to flip. The policy owner
(REACH IT / workspace admin) would have to change it — usually not possible.

## The Solution

Stop launching stages as child jobs. **Execute each stage's `.py` source
in-process**, inside the current notebook's Spark session, via `exec()`:

```python
def _run_notebook(nb_rel, cfg):
    """In-process stage run — USER_ISOLATION clusters block dbutils.notebook.run()."""
    py = os.path.join(REPO_ROOT, nb_rel + ".py")        # REPO_ROOT = /Workspace/... on Databricks
    if not os.path.exists(py):
        raise FileNotFoundError(py)
    # hand params to the stage via env vars + widgets (its _param()/bootstrap reads them)
    for k, v in {"REPO_ROOT": REPO_ROOT, "VOLUME_BASE": VOLUME_BASE,
                 "ENV": ENV, "COHORT": COHORT, "CONFIG": cfg or ""}.items():
        os.environ[k] = str(v)
        try:
            dbutils.widgets.text(k, str(v))
        except Exception:
            pass
    with open(py) as f:
        src = f.read()
    g = {"__name__": "__main__", "__file__": py, "__builtins__": __builtins__}
    for name in ("spark", "dbutils", "display", "sc", "sqlContext"):
        if name in globals():
            g[name] = globals()[name]          # inject the live Spark session + dbutils
    exec(compile(src, py, "exec"), g)
    return "ok"
```

Two critical details:

1. **Patch EVERY level.** The nesting is `driver → A00 orchestrator → sub-stage`.
   Fixing only the outer driver makes A00's own `run()` (which also calls
   `dbutils.notebook.run("./sub")`) fail one level deeper. The A00 orchestrators
   (`run_pipeline_adhd_raw.py` / `_pd2d_raw.py`) must be patched the same way.

2. **Inject `spark`/`dbutils` into the exec namespace.** A plain subprocess
   (`%sh python stage.py`) or web terminal has **no Spark session**, so A00's
   `spark.sql(deid.derived.*)` fails. Inline `exec` shares the notebook's live
   `spark`/`dbutils`, which is exactly what the stages need.

## Why It Works

A "job" is an unattended, isolated run the platform manages — it requires jobs
workload permission. `dbutils.notebook.run()` starts one. `exec()` does not: it
just runs more code inside the notebook you already started, so to the policy it
is still ordinary **interactive notebook** work, which is allowed.

```
❌ dbutils.notebook.run("A01")  →  "start a JOB"              →  blocked by policy
✅ exec(A01 source in this cell) →  "more of MY notebook"      →  allowed
```

Same code, same results — no child jobs, so the policy is satisfied.

## When to Apply

- Access mode is **Standard / Shared / USER_ISOLATION** and 🔒 policy-locked.
- Error contains **`does not support jobs workload`**.
- You cannot get the admin to set `workload_type.clients.jobs = true` or give
  you a **Dedicated (single-user)** cluster.
- Any nested `dbutils.notebook.run()` orchestration on such a cluster.

## Caveats

- **Parallelism**: the A00 orchestrator used `ThreadPoolExecutor` to run
  sub-notebooks in parallel via `dbutils.notebook.run`. Inline `exec` sharing one
  Spark session is not thread-safe that way — force **sequential** (`PARALLEL=False`)
  when converting to inline.
- **`# MAGIC %pip` cells are skipped** by `exec` (they're comments). Ensure deps
  are installed another way (the driver's profile `pip` step, or the stage's own
  `subprocess pip install`).
- **`dbutils.notebook.exit()`** in a child raises and would abort the parent if
  exec'd inline; wrap or strip it. (Leaf stages A01–C01 don't call it; the A00
  orchestrator does at the end.)
- Sub-notebook layout: A00 sub-stages ship as `.ipynb` under `_databricks/`, not
  as sibling `.py` — resolve the real path when converting the orchestrator.
- This is a **workaround for a governance constraint**, not a better architecture.
  On a jobs-capable cluster, Lesson 06 (separate job tasks) is still preferable.

## Related

- **Lesson 06** — the opposite case (jobs-capable cluster → prefer job tasks).
- **Lesson 05 / 07** — env vars don't cross `dbutils.notebook.run`; inline exec
  sidesteps this since the child shares the parent's `os.environ`.
