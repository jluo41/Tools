---
name: haipipe-task-for-raw
description: "Raw extraction task-folder build specialist. Scaffolds {NN}_<name>/ task-folders in the project's raw-extraction task-group (default R-series; letters are project-specific). Two patterns: extract-wide-process-local (Databricks → parquet → local Python; non-PHI) and server-resident (all-Spark multi-stage pipeline that stays on the catalog volume; PHI cohorts, e.g. A00_rawstore_* groups). Called by /haipipe-task orchestrator when task-type=raw. Direct invocation works for scoped scaffolding. Cross-references /haipipe-data-raw."
argument-hint: "[project_id] [group] [task-name]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "1.4.0"
  last_updated: "2026-07-08"
  summary: "Raw extraction task-folder build specialist (Pattern 1 local / Pattern 2 PHI server-resident)."
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

Skill: haipipe-task-for-raw
=================================

Scaffolds a **raw extraction task-folder** — a runnable example that
extracts source tables from a Databricks catalog as wide parquet files.
In **Pattern 1** (non-PHI) the parquet is then processed locally with
Python (pandas) and heavy outputs land in `_WorkSpace/0-RawDataStore/<cohort>/`;
in **Pattern 2** (PHI, server-resident — see below) everything stays on the
catalog volume. The task-folder keeps scripts, configs, and convert-only
notebooks either way.

**Invocation modes (see `../../haipipe-task/ref/invocation-modes.md`):**
interactive (a human steers; missing fields get ASKed) OR headless (a full
spec → run silently, no ASK). `haipipe-task-creator-agent` calls this skill
headless during fan-out, then authors the `<TASK>.py` body. Always end with
the structured return block (status / task_folder / run_name / files).


Position in the series
----------------------

```
/haipipe-task-for-raw         ◀── you are here (Stage 0 — raw extraction)
/haipipe-task-for-data            data-pipeline (Stages 1-4)
/haipipe-task-for-algo            algo-dev demo
/haipipe-task-for-fit             model training
/haipipe-task-for-eval            model evaluation
/haipipe-task-for-display         paper figure / table
/haipipe-task-for-individual      individual-centric query
/haipipe-task-for-agent           LLM agent call
/haipipe-task-for-endpoint        package + deploy (absorbed inference profiling)
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

Group letter default: **R** (raw extraction). When raw extraction is
embedded in a cohort project as pipeline stage 0, the group is commonly
named `A00_rawstore_<cohort>/` (e.g. Project-REACH-ADHD) — the letter is
project-specific either way.
Heavy outputs land in: `_WorkSpace/0-RawDataStore/<cohort>/` (or the
catalog-volume equivalent for server-resident cohorts — see Pattern 2).


Two patterns — pick by data-governance
---------------------------------------

  Pattern 1  extract-wide-process-local   data may leave the server
             (doctrine below)             (de-identified / synthetic / licensed-local)
  Pattern 2  server-resident              PHI: raw data NEVER leaves the
             (A00 rawstore)               server/volume; all stages run on Databricks


Pattern 1: Extract-Wide-Process-Local Doctrine
-----------------------------------------------

The default for non-PHI cohorts. Every such task MUST follow it:

  1. **One SQL query per source table → one large parquet file.**
     Keep SQL simple: `SELECT columns FROM single_table WHERE filters`.
     Avoid complex JOINs in SQL. If you need joins, extract both tables
     as separate parquet files and join in Python.

  2. **Save parquet to Databricks catalog volume.**
     Path pattern: `/Volumes/<catalog>/<schema>/<volume>/<cohort>/<table>.parquet`

  3. **Download/sync parquet to local `_WorkSpace/0-RawDataStore/<cohort>/`.**
     One parquet file per source table. No partitioned directories.

  4. **Process with Python (pandas), NOT Spark.**
     Local reads, local transforms, local output. Spark is for extraction
     only (because the data lives in Databricks). Once the parquet is
     local, everything is pandas.


Pattern 2: Server-resident rawstore (PHI cohorts)
--------------------------------------------------

When the cohort is PHI, step 3 above is FORBIDDEN — raw data never leaves
the server. The whole extraction pipeline runs on Databricks and writes to
the catalog volume. Live example: Project-REACH-ADHD
`tasks/A00_rawstore_reachadhd/`.

Shape:

```
tasks/A00_rawstore_<cohort>/
├── run_pipeline_<cohort>_raw.py(+.ipynb)   ← group-root orchestrator (sequences stages)
├── 01_stage1_universe/                     ← cohort universe (Spark SQL on deid tables)
├── 02_stage2_phenotype/                    ← phenotype definition (parallelizable sub-steps)
├── 03_stage3_features/                     ← feature tables
├── _databricks/                            ← .ipynb copies of every stage (what the
│                                             workspace import executes)
└── README.md                               ← allowed here (Databricks-native group)
```

Rules:
  - Stages can be all-Spark (the local-pandas rule of Pattern 1 does not
    apply — nothing comes local).
  - **Output path MUST align to what the Stage-1 SourceFn reads**:
    `<VOLUME_BASE>/0-RawDataStore/<cohort-slug>/...` with the exact
    `<cohort-slug>` the SourceFn config expects (e.g. `reach-adhd`, not
    `REACH-ADHD`). Misalignment here is the classic silent failure.
  - Orchestration + stage launching (jobs vs inline exec, sequential-only
    caveats, widget params): `../../haipipe-task/ref/databricks-execution.md`.
  - Only aggregated/derived summaries may move off-server; raw and
    row-level intermediates stay on the volume.


Execution model — Databricks notebooks
---------------------------------------

Unlike other task-types that use papermill for local execution, raw
extraction tasks run on **Databricks**. The run script only converts
the `.py` to `.ipynb` — it does NOT execute locally.

Workflow:
  1. `runs/<RUN>.sh` converts `.py` → `.ipynb` and writes `runtime.yaml`
  2. User uploads `.ipynb` to Databricks workspace (browser Import when no
     CLI is allowed; keep converted stage notebooks in the group's
     `_databricks/` folder)
  3. User runs the notebook on a Databricks cluster (Pattern 2: run the
     group orchestrator or the project's `run_<project>.py` driver instead
     of individual notebooks)
  4. Extracted parquet files land in the catalog volume
  5. Pattern 1 only: user syncs parquet to local
     `_WorkSpace/0-RawDataStore/<cohort>/` (Pattern 2 skips this — PHI
     stays on the volume and Stage 1 reads it there)

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

Convention (Pattern 1):
  - `stage1` = extract SQL tables → parquet (Databricks)
  - `stage2` = read parquet, clean/transform with pandas (local)
  - `stage3+` = optional further processing stages

Convention (Pattern 2, all stages on Databricks — see A00 shape above):
  - `stage1` = cohort universe, `stage2` = phenotype, `stage3` = features;
    stage meaning is cohort-specific, ordering is what matters.

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
  Heavy outputs land in `_WorkSpace/0-RawDataStore/<cohort>/` (or the
  catalog volume for Pattern 2).
- Write complex multi-table JOINs in SQL — extract tables separately,
  join in Python downstream.
- Use Spark for local processing — pandas only once data is local.
- Sync PHI raw data to a laptop / local `_WorkSpace` (Pattern 2 cohorts are
  server-only; only aggregated outputs move).
- Skip the `_meta:` block.
- Create `README.md` in task folders. (Pattern 2 exception: a group-root
  README is allowed for Databricks-native groups.)


First-run gate
---------------

`runs/<RUN>.sh` does NOT execute the notebook — it only converts.
The code-review gate is still present (inherited from the base
template pattern) but uses `skip_review: true` by default for
initial scaffolding since the notebook will be reviewed manually
before Databricks upload.
