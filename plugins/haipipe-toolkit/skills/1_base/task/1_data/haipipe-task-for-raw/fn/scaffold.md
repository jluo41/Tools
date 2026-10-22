fn-scaffold: Scaffold a raw extraction job
===================================================

Extracts source tables from a Databricks catalog as wide parquet files.
Output: `work/bNN_<raw_block>/jNN_<extraction_job>/tNN_<task>/`.


Step 0 — Pick the pattern (governance gate)
--------------------------------------------

Ask (or infer from the cohort): **is the raw data PHI?**

```
non-PHI  →  Pattern 1  extract-wide-process-local   (Steps 1-7 below, as written)
PHI      →  Pattern 2  server-resident              (Steps 1-7 with the P2 deltas
                                                     marked ⚡ below)
```

Pattern 2 in one line: nothing comes local — all stages are Spark on the cluster, output goes to `<VOLUME_BASE>/0-RawDataStore/<raw_data_name>/`, and the group carries an orchestrator + `_databricks/` bundle.
Full contract: `../SKILL.md` "Pattern 2" + `../../../haipipe-task/ref/databricks-execution.md`.
Live example: `examples/Project-REACH-ADHD/work/A00_rawstore_reachadhd/`.


Step 1 — Identify project + block
---------------------------------------

- Auto-detect project from cwd (look for `examples/Proj*/`).
- ASK block if not given; scaffold canonical `bNN_<cohort_raw>/` if needed
  (see `../../../haipipe-task/fn/block.md`).
- ⚡ P2: embedded rawstore groups are conventionally named
  `A00_rawstore_<cohort>/` (project-specific either way).


Step 2 — Collect metadata
--------------------------

- 2-digit NN: next free `tNN` in this Job (no gaps).
- snake_case task_name: `stage{N}_{description}`
  (e.g., `stage1_extract_tables`, `stage2_process`, `stage1_extract_claims`).
- Stage number (1, 2, 3, ...): which stage in the cohort extraction pipeline.
  - Pattern 1: stage1 = SQL extraction to parquet (Databricks);
    stage2 = Python processing of parquet (local); stage3+ = optional.
  - ⚡ P2: ALL stages run on Databricks (Spark); stage meaning is
    cohort-specific (e.g. stage1 universe, stage2 phenotype, stage3 features).
- Cohort name: which raw data cohort (e.g., `prediabetes`, `adhd`).
- `_meta:` block (purpose / note / input / output).


Step 3 — Create skeleton
-------------------------

```
bNN_<raw_block>/
└── jNN_<extraction_job>/
    ├── src/
    └── tNN_<raw_table_or_step>/
        ├── tNN_<raw_table_or_step>.md
        ├── scripts/<worker>.py
        ├── runs/r01_base/            one folder per Run
        │   ├── r01_base.sh           the Ticket
        │   ├── config.yaml
        │   ├── run.yaml              its card (haipipe-run)
        │   └── result/               written by the Ticket
        ├── notebooks/
        ├── draft/
        └── workflow/
```

⚡ P2's group root below is the older REACH shape (`work/A00_rawstore_reachadhd/`): read it where it
exists, never scaffold it for new work (SKILL.md § the older shape); a new raw Job is jNN_<cohort>_raw/:

```
A00_rawstore_<cohort>/
├── run_pipeline_<cohort>_raw.py(+.ipynb)    orchestrator sequencing the stages
├── _databricks/                             converted .ipynb of every stage
└── README.md                                allowed here (group is imported
                                             into Databricks standalone)
```


Step 4 — Seed config
---------------------

Copy `ref/config-seed.yaml` to `runs/rNN_<run>/config.yaml`.
Fill in:
- `_meta:` (purpose / input / output).
- `stage:` (1, 2, 3, ...).
- Pattern 1: `execution:` (`databricks` for stage1, `local` for stage2+);
  Databricks params (catalog, schema, volume) for stage1; local params
  (raw_store_path, cohort) for stage2+.
- ⚡ P2: `execution: databricks` for EVERY stage; output path =
  `<VOLUME_BASE>/0-RawDataStore/<raw_data_name>/` where `<raw_data_name>` is
  `<cohort>-v<yymmdd>` and EXACTLY what the Stage-1 SourceFn config reads
  (e.g. `reach-adhd-v260922`, not `REACH-ADHD`); OMIT the `local:` block entirely.


Step 5 — Run-script
--------------------

Copy `ref/run-databricks-sh-template.sh` to `runs/rNN_<run>/rNN_<run>.sh`.
Set `TASK_NAME="<worker>"` (the worker filename without .py).
Write the Run's card `runs/rNN_<run>/run.yaml` (haipipe-run; an extraction Run takes `role: make`).

This template converts `.py` → `.ipynb` only — no papermill execute.
The notebook is meant for Databricks upload. ⚡ P2: place the converted .ipynb in the group's `_databricks/` as well; ignore the template's "sync to local" hint (Pattern 1 only).


Step 6 — Cross-skill link
--------------------------

After scaffolding, suggest:
- Upload notebook to Databricks and run (for stage1; ⚡ P2: run the group
  orchestrator or the project's `run_<project>.py` driver)
- `/haipipe-data-raw understand <cohort>` (to document the data)
- `/haipipe-data-source` (to wrap into Stage 1 SourceFn later)


Step 7 — Report
----------------

```
status:    ok
summary:   Scaffolded raw extraction Task tNN_<task> under bNN_<block>/jNN_<job>.
artifacts: [paths created]
next:      Upload notebook to Databricks  OR  /haipipe-data-raw understand <cohort>
```


MUST NOT
---------

- Write complex multi-table JOINs in the SQL strings — one query per
  source table, keep it simple.
- (Pattern 1) Use `spark.sql()` for local processing — Spark is
  extraction-only. Once data is local, use pandas.
  (⚡ P2: all-Spark is the rule; nothing comes local.)
- Place `.parquet` files in a Run's `result/` — they go to
  `_WorkSpace/0-RawDataStore/` (P2: the catalog volume).
- ⚡ P2: sync PHI raw data to a laptop / local `_WorkSpace` — server-only;
  only aggregated outputs move.
- Skip the `_meta:` block.
- Create `README.md` in Block/Job/Task roots; use the canonical Board/Page surfaces.
