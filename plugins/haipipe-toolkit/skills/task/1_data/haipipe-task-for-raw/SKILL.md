---
name: haipipe-task-for-raw
description: "Raw extraction task-folder build specialist. Scaffolds {NN}_<name>/ task-folders under R-series task-groups that extract source tables from Databricks as single parquet files, then process locally with Python. Called by /haipipe-task orchestrator when task-type=raw. Direct invocation works for scoped scaffolding. Cross-references /haipipe-data-raw."
argument-hint: "[project_id] [group] [task-name]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "1.0.0"
  last_updated: "2026-06-10"
  summary: "Raw extraction task-folder build specialist (Databricks → parquet → local Python)."
  changelog:
    - "1.0.0 (2026-06-10): initial version — extract-wide-process-local doctrine."
---

Skill: haipipe-task-for-raw
=================================

Scaffolds a **raw extraction task-folder** — a runnable example that
extracts source tables from a Databricks catalog as wide parquet files,
then optionally processes them locally with Python (pandas). Heavy
outputs land in `_WorkSpace/0-RawStore/<cohort>/`; the task-folder keeps
scripts, configs, and convert-only notebooks.

**Invocation modes (see `../../haipipe-task/ref/invocation-modes.md`):**
interactive (a human steers; missing fields get ASKed) OR headless (a full
spec → run silently, no ASK). `haipipe-task-creator-agent` calls this skill
headless during fan-out, then authors the `<TASK>.py` body. Always end with
the structured return block (status / task_folder / run_name / files).


Position in the series
----------------------

```
/haipipe-task-for-data            data-pipeline (Stages 1-4)
/haipipe-task-for-raw         ◀── you are here (Stage 0 — raw extraction)
/haipipe-task-for-algo            algo-dev demo
/haipipe-task-for-training        model training
/haipipe-task-for-eval            model evaluation
/haipipe-task-for-display         paper figure / table
/haipipe-task-for-individual      individual-centric query
/haipipe-task-for-agent           LLM agent call
/haipipe-task-for-inference       inference profiling
```


What this scaffolds
-------------------

```
tasks/R{NN}_<cohort_name>/                   ← group (R-series)
└── {NN}_stage{S}_{description}/             ← task-folder this scaffold creates
    ├── {NN}_stage{S}_{description}.py       source + # %% cells (SQL strings in Python)
    ├── configs/
    │   └── <run_name>.yaml                  seeded from ref/config-seed.yaml
    ├── runs/
    │   └── <run_name>.sh                    from ref/run-databricks-sh-template.sh
    ├── results/                             runtime.yaml + light artifacts
    └── notebooks/                           .ipynb for Databricks upload (convert-only)
```

Group letter default: **R** (raw extraction).
Heavy outputs land in: `_WorkSpace/0-RawStore/<cohort>/`.


Extract-Wide-Process-Local Doctrine
------------------------------------

This is the core philosophy. Every raw extraction task MUST follow it:

  1. **One SQL query per source table → one large parquet file.**
     Keep SQL simple: `SELECT columns FROM single_table WHERE filters`.
     Avoid complex JOINs in SQL. If you need joins, extract both tables
     as separate parquet files and join in Python.

  2. **Save parquet to Databricks catalog volume.**
     Path pattern: `/Volumes/<catalog>/<schema>/<volume>/<cohort>/<table>.parquet`

  3. **Download/sync parquet to local `_WorkSpace/0-RawStore/<cohort>/`.**
     One parquet file per source table. No partitioned directories.

  4. **Process with Python (pandas), NOT Spark.**
     Local reads, local transforms, local output. Spark is for extraction
     only (because the data lives in Databricks). Once the parquet is
     local, everything is pandas.


Execution model — Databricks notebooks
---------------------------------------

Unlike other task-types that use papermill for local execution, raw
extraction tasks run on **Databricks**. The run script only converts
the `.py` to `.ipynb` — it does NOT execute locally.

Workflow:
  1. `runs/<RUN>.sh` converts `.py` → `.ipynb` and writes `runtime.yaml`
  2. User uploads `.ipynb` to Databricks workspace (or uses dbx CLI)
  3. User runs the notebook on a Databricks cluster
  4. Extracted parquet files land in the catalog volume
  5. User syncs parquet to local `_WorkSpace/0-RawStore/<cohort>/`

The run-script template is `ref/run-databricks-sh-template.sh` —
convert-only, no papermill execute.


Stage naming within a cohort group
-----------------------------------

Each cohort's extraction pipeline is organized as numbered stages:

```
R01_prediabetes/
├── 01_stage1_extract_tables/     ← SQL extraction (runs on Databricks)
├── 02_stage2_process/            ← Python processing (runs locally)
└── sbatch/
```

Convention:
  - `stage1` = extract SQL tables → parquet (Databricks)
  - `stage2` = read parquet, clean/transform with pandas (local)
  - `stage3+` = optional further processing stages

Stage numbering is cohort-specific. Different cohorts may have different
numbers of stages depending on complexity.


Cross-reference to pipeline skill
----------------------------------

`/haipipe-data-raw` owns the understanding of raw cohort data —
the datapoint-timeline lifecycle documentation. After extraction,
suggest `/haipipe-data-raw understand <cohort>` to document what
was extracted, then `/haipipe-data-source` to wrap into Stage 1.


Commands
--------

```
/haipipe-task-for-raw                              ASK project / group / name
/haipipe-task-for-raw <project> <group> <name>     scaffold direct
```


Scaffold flow
-------------

See `fn/scaffold.md` for the detailed step-by-step. Summary:

  1. Identify project + task-group.
  2. Collect metadata (NN, name, stage number, _meta block).
  3. Create skeleton (.py, configs/, runs/, results/, notebooks/).
  4. Seed config from `ref/config-seed.yaml`.
  5. Copy run-script from `ref/run-databricks-sh-template.sh`.
  6. Suggest next via cross-skill link.
  7. Emit return contract.


Return contract
---------------

```
status:    ok | blocked | failed
summary:   2-3 sentences on what was scaffolded
artifacts: [paths created]
next:      /haipipe-data-raw understand <cohort>  OR  run on Databricks
```


MUST NOT
---------

- Place heavy artifacts (`.parquet`, `.csv` > 1 MB) in `results/`.
  Heavy outputs land in `_WorkSpace/0-RawStore/<cohort>/`.
- Write complex multi-table JOINs in SQL — extract tables separately,
  join in Python downstream.
- Use Spark for local processing — pandas only once data is local.
- Skip the `_meta:` block.
- Create `README.md`.


First-run gate
---------------

`runs/<RUN>.sh` does NOT execute the notebook — it only converts.
The code-review gate is still present (inherited from the base
template pattern) but uses `skip_review: true` by default for
initial scaffolding since the notebook will be reviewed manually
before Databricks upload.
