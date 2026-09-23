---
name: haipipe-task-for-raw
description: >-
  Raw-stage Task specialist with two kinds of Job. Extraction Job: moves
  cohort data from an operational database into RawStore as a versioned
  dataset <cohort>-v<yymmdd> (extract-wide-process-local for non-PHI,
  server-resident all-Spark for PHI). Raw understanding Block b00: one Job per
  dataset version that inventories, profiles each table, routes tables to
  ProcNames, and hands off to Source with a gated readiness. Called by
  /haipipe-task when task-type=raw. Cross-references /haipipe-data-raw.
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "0.4.0"
  last_updated: "2026-09-22"
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

Skill: haipipe-task-for-raw
=================================

Scaffolds a **raw extraction job** — a runnable example that extracts source tables from a Databricks catalog as wide parquet files.
In **Pattern 1** (non-PHI) the parquet is then processed locally with Python (pandas) and heavy outputs land in `_WorkSpace/0-RawDataStore/<cohort>/`; in **Pattern 2** (PHI, server-resident — see below) everything stays on the catalog volume.
The job keeps scripts, configs, and convert-only notebooks either way.

**Invocation modes (see `../../haipipe-task/ref/invocation-modes.md`):** interactive (a human steers; missing fields get ASKed) OR headless (a full spec → run silently, no ASK).
`haipipe-task-creator-agent` calls this skill headless during fan-out, then authors the `<TASK>.py` body.
Always end with the structured return block (status / task_folder / run_name / files).

Store boundary
--------------

```
Operational Database -- cohort extraction code --> 0-RawDataStore/<raw-data>/
Vendor/API source ---- ingestion/build code -----> ExternalStore/@raw/ -> @{release}/
```

Use this skill for the first line. Use `haipipe-data-external` for the second.
“Extract”, “landing”, and “ingestion” describe code/actions, not additional
stores between the database and RawStore. One delivered extraction is a Raw
Data version/snapshot; reserve “cohort” for the selected population.


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
tasks/bNN_<raw_block>/
└── jNN_<extraction_job>/
    ├── src/                                 shared extraction helpers
    └── tNN_<raw_table_or_step>/
        ├── tNN_<raw_table_or_step>.md
        ├── scripts/<worker>.py              SQL strings in Python; # %% cells
        ├── scripts/config/rNN_<run>.yaml
        ├── runs/rNN_<run>.sh
        ├── results/rNN_<run>/runtime.yaml
        └── notebooks/rNN_<run>.ipynb
```

Two kinds of raw Job, never in one Block (see `haipipe-task/ref/hierarchy.md` § Block
number ranges):
- **Extraction Job**: pulls tables from an operational database into
  `0-RawDataStore/<dataset>/`. It lives in its own extraction Project, e.g.
  REACH `Project-0-EHR-Description/tasks/b01_reach_jhu/j22_pd2d_raw_extraction`.
  The Job's `src/config-defaults.yaml` types `raw_data_name` once; a refresh
  changes that line and never writes into another version's folder.
- **Raw understanding Block `b00`**: in every Project that USES the data, one
  Job per dataset version reads what the extraction wrote. It never extracts
  and never writes RawStore. See § Raw understanding Block below.
Heavy outputs land in: `_WorkSpace/0-RawDataStore/<cohort>/` (or the catalog-volume equivalent for server-resident cohorts — see Pattern 2).


Raw understanding Block (`b00`)
-------------------------------

Reference implementations: REACH-SPACE `examples/Project-REACH-PD2D/tasks/b00_rawdata/`
and WellDoc-SPACE `examples-1-data/Proj01-CGM-RawData/tasks/b01_rawdata/`
(numbered before the ranges were fixed).

```
b00_rawdata/
└── jNN_<cohort>_v<yymmdd>_raw/           one raw dataset version = one Job
    ├── src/config-defaults.yaml          raw_data_name, upstream extraction, store path, min_cell
    ├── t01_intake_inventory/             every table: rows, columns, size; every upstream Run ok?
    ├── t02_table_catalog_schema/         per table: subject key, time columns, schema family
    ├── t03_profile_<table>/ …            ONE Task per observed table, from the inventory
    ├── tNN_audit_file_routing/           each raw table → exactly one ProcName
    ├── tNN_datapoint_timeline/           date ranges (years) + open questions with evidence
    └── tNN_source_handoff/               preserve / derive / ask lists + gated readiness
```

- Table Tasks come from the observed inventory, never a fixed topic list.
- Runs are passes: `r01_structure_schema` (local, from receipts or headers),
  `r02_profile_semantics` (types, nulls, distincts, year ranges), `full_scan`
  only where needed. Only the passes that apply exist.
- Privacy: metadata only. For PHI the profile pass is a server `.cmd` Run;
  dates leave as years, counts 1 to 10 as `<11`, and no row value leaves.
- `datapoint_timeline` and `source_handoff` are `haipipe-data-raw`'s
  `understand` and `hand-off` as Tasks. Readiness is computed from gates
  (every table routed once, every table profiled, no blocking question), never
  declared: `ready_for_sourcefn_review` or `blocked` with the failing gate.
- `b01_sourcestore` starts from `audit_file_routing`: one contract Task per
  routed ProcName.


Two patterns — pick by data-governance
---------------------------------------

  Pattern 1  extract-wide-process-local   data may leave the server
             (doctrine below)             (de-identified / synthetic / licensed-local)
  Pattern 2  server-resident              PHI: raw data NEVER leaves the
             (A00 rawstore)               server/volume; all stages run on Databricks


Pattern 1: Extract-Wide-Process-Local Doctrine
-----------------------------------------------

The default for non-PHI cohorts.
Every such task MUST follow it:

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

When the cohort is PHI, step 3 above is FORBIDDEN — raw data never leaves the server.
The whole extraction pipeline runs on Databricks and writes to the catalog volume.
Legacy example: Project-REACH-ADHD `tasks/A00_rawstore_reachadhd/`.

Legacy shape (readable, never scaffolded for new work):

```
tasks/A00_rawstore_<cohort>/
├── run_pipeline_<cohort>_raw.py(+.ipynb)   ← group-root orchestrator (sequences stages)
├── 01_stage1_universe/                     ← cohort universe (Spark SQL on deid tables)
├── 02_stage2_phenotype/                    ← phenotype definition (parallelizable sub-steps)
├── 03_stage3_features/                     ← feature tables
├── _databricks/                            ← .ipynb copies of every stage (what the
│                                             workspace import executes)
└── README.md                               ← legacy documentation only
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

Unlike other task-types that use papermill for local execution, raw extraction tasks run on **Databricks**.
The run script only converts the `.py` to `.ipynb` — it does NOT execute locally.

Extraction Run procedure:
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

The run-script template is `ref/run-databricks-sh-template.sh`: conversion is a Step inside the extraction Run.
Its successful exit means notebook preparation only; the Run remains blocked awaiting external execution.
Read `../../haipipe-task/ref/databricks-execution.md` before the upload/run handoff.
Bind the external job/run id, config hash, cluster logs, output manifest, and Result checks to the same bNNjNNtNNrNN receipt.
No separate converter Run is allocated by default. Only actual cluster completion plus the Result gate can close extraction.
On timeout preserve the external run id and report still-running; inspect it before any retry.


Task naming within a cohort extraction Job
-------------------------------------------

Each cohort's extraction pipeline is organized as numbered stages:

```
b01_prediabetes_raw/
└── j01_operational_extract/
    ├── t01_encounters_extract/
    ├── t02_medications_extract/
    └── t03_raw_snapshot_validate/
```

Convention (Pattern 1):
  - `stage1` = extract SQL tables → parquet (Databricks)
  - `stage2` = read parquet, clean/transform with pandas (local)
  - `stage3+` = optional further processing stages

Convention (Pattern 2, all stages on Databricks — see A00 shape above):
  - `stage1` = cohort universe, `stage2` = phenotype, `stage3` = features;
    stage meaning is cohort-specific, ordering is what matters.

Stage numbering is cohort-specific.
Different cohorts may have different numbers of stages depending on complexity.


Cross-reference to pipeline skill
----------------------------------

`/haipipe-data-raw` owns the understanding of raw cohort data — the datapoint-timeline lifecycle documentation.
After extraction, suggest `/haipipe-data-raw understand <cohort>` to document what was extracted, then `/haipipe-data-source` to wrap into Stage 1.


Commands
--------

```
/haipipe-task-for-raw                              ASK project / group / name
/haipipe-task-for-raw <project> <group> <name>     scaffold direct
```


Scaffold flow
-------------

See `fn/scaffold.md` for the detailed step-by-step.
Summary:

  1. Identify project + block.
  2. Collect metadata (NN, name, stage number, _meta block).
  3. Create canonical Task skeleton (`scripts/`, `scripts/config/`, `runs/`,
     `results/`, `notebooks/`, `outline/`, `workflow/`).
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
- Create `README.md` at Block, Job, or Task root. Use `board.md`, the Task Page,
  and `diagram/`; legacy Databricks-native READMEs remain readable.


First-run gate
---------------

`runs/<RUN>.sh` does NOT execute the notebook — it only converts.
The code-review gate is still present (inherited from the base template pattern) but uses `skip_review: true` by default for initial scaffolding since the notebook will be reviewed manually before Databricks upload.
