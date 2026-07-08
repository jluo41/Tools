task: Running Tasks on Databricks (Template C)
================================================

The two run-script templates in ref/task-structure.md assume a bash runner
(local machine or HPC). When a task runs ON Databricks there is no bash
runner: the unit of execution is a notebook on a cluster, params arrive via
widgets, and the platform may forbid child jobs. This ref defines that third
execution dialect. Deep Databricks material lives in the learn-databricks
skill (Tools/plugins/learn-infra/skills/learn-databricks/) — this file only
covers what task authors must do differently; each rule links the lesson
that explains why.

Canonical live example: examples/Project-REACH-ADHD/run_reach_adhd.py
(driver) + tasks/A00_rawstore_reachadhd/ (Databricks-native group).

---

The dual-mode driver (one file, three environments)
====================================================

Each project ships ONE driver at project root (run_<project>.py) that is
simultaneously a Databricks notebook and a local script. An ENV param picks
a profile; the profile decides VOLUME_BASE, which stages run, and how:

  ENV                VOLUME_BASE                          Stages    How
  -----------------  -----------------------------------  --------  ----------
  local              <repo>/_WorkSpace                    A01-C01   subprocess
  cdhai-databricks   /Volumes/<catalog>/.../_WorkSpace    A01-C01   in-notebook
  reach-databricks   /Volumes/reach_users/jluo41/_reach_workspace  A00-C01   in-notebook

Profile fields worth standardizing: volume_base, stages (ordered list of
task .py paths relative to repo root), pip (packages to install when the
cluster runtime lacks the ML stack), and whether raw extraction (A00) is in
scope for that environment.

Repo-root resolution on Databricks: notebooks know their own workspace path
(dbutils.notebook.entry_point...notebookPath()); derive REPO_ROOT by
splitting at the known anchor, e.g. nb.rsplit("/examples/", 1)[0].

---

Parameter passing: widget -> env var -> default
================================================

dbutils.widgets is the notebook-native param surface; os.environ is the
script-native one. Read BOTH so the same file works everywhere:

```python
def _param(name, default):
    try:
        v = dbutils.widgets.get(name)          # Databricks widget
        if v: return v
    except Exception:
        pass
    return os.environ.get(name, default)        # local / injected env
```

When a driver launches a stage, it hands params down by setting BOTH
os.environ[k] and dbutils.widgets.text(k, v). Env vars do NOT cross
dbutils.notebook.run() boundaries (learn-databricks Lessons 05/07) — inline
exec (below) sidesteps this because the child shares the parent's process.

---

Stage launching: jobs-capable vs policy-locked clusters
========================================================

Two ways a driver can run a stage notebook, chosen PER CLUSTER:

1. dbutils.notebook.run("<stage>", timeout) — launches the child as an
   ephemeral JOB. Requires a jobs-capable cluster. Preferred when available
   (learn-databricks Lesson 06).

2. Inline exec — read the stage's .py source and exec() it in-process,
   injecting the live spark/dbutils into the exec namespace. REQUIRED when
   the cluster is policy-locked Standard/USER_ISOLATION and errors with
   "does not support jobs workload" (learn-databricks Lesson 15 has the
   full recipe and caveats).

Inline-exec rules that bite task authors:
  - Patch EVERY nesting level (driver -> group orchestrator -> sub-stage);
    one un-patched dbutils.notebook.run() deeper down still fails.
  - Force sequential execution (PARALLEL=False). ThreadPoolExecutor fan-out
    over one shared Spark session is not safe inline.
  - `# MAGIC %pip` cells are comments to exec() — install deps from the
    driver profile instead.
  - dbutils.notebook.exit() in a child aborts the parent when inlined —
    strip or wrap it.

---

Task-folder deltas for Databricks-native groups
================================================

A task group that runs ON Databricks (e.g. A00_rawstore_<cohort>) keeps the
standard task-folder layout (configs/ runs/ results/ notebooks/) and adds:

  _databricks/        .ipynb copies of every stage + orchestrator, converted
                      from the .py sources — this is what the workspace
                      import actually executes. Rebuild after editing .py;
                      the .py stays the source of truth.
  run_pipeline_*.py   group-root orchestrator (plus its .ipynb twin) that
                      sequences the stage sub-folders. This is the
                      group-level analogue of sbatch/ for a platform with
                      no shell.

runs/*.sh for such groups are CONVERT-ONLY (build the .ipynb, record
runtime.yaml; no papermill execute) — the run itself happens on the cluster.
See 1_data/haipipe-task-for-raw ref/run-databricks-sh-template.sh.

Heavy outputs go to the Unity Catalog Volume (VOLUME_BASE), which plays the
role of _WorkSpace/: same 0-RawDataStore ... 6-EndpointStore layout, same
heavy-artifact rule (authoring-conventions.md §3). PHI cohorts: raw stores
NEVER leave the server/volume; only aggregated results move.

---

Memory on small single-node clusters
=====================================

Typical shared clusters are small (e.g. 4 cores / 16 GB). Two rules:

  - Never load a huge table wholesale to fingerprint or count it — read
    parquet footer metadata for rows/schema, stream bytes for checksums
    (fixed in code/haipipe/source_base/source_pipeline.py).
  - Chunk big raw tables at build time: declare them in a CHUNKED_TABLES
    map and read with pd.read_csv(chunksize=...) / pyarrow iter_batches,
    writing part_NNNN.parquet + a _SUCCESS marker for resume. Canonical
    pattern: Project-EHR-Mimic .../c7_build_source_mimiciv31.py.

---

Deploy without a CLI (browser-only workspaces)
===============================================

When the workspace allows no CLI and no repos integration, ship code as a
self-contained zip attached to a GitHub Release (NOT the auto "Source code"
zip — that leaves submodules empty). Exclude secrets (.databrickscfg, env.sh,
*.pem), _WorkSpace/, .git/, .venv/. Import the zip via Workspace -> Import,
open the project driver, set widgets, Run All.

---

Related
=======

  learn-databricks Lesson 05/07   env vars don't cross notebook.run
  learn-databricks Lesson 06      prefer job tasks on jobs-capable clusters
  learn-databricks Lesson 15      USER_ISOLATION blocks jobs -> inline exec
  ref/task-structure.md           Templates A/B (bash runners) + folder rules
  1_data/haipipe-task-for-raw     raw-extraction scaffold + convert-only run.sh
