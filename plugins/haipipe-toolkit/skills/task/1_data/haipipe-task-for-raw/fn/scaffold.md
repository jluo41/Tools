fn-scaffold: Scaffold a raw extraction task-folder
===================================================

Extracts source tables from a Databricks catalog as wide parquet files.
Group letter default: **R**. Output: `tasks/R{NN}_<cohort>/{NN}_stage{S}_<desc>/`.


Step 1 — Identify project + task-group
---------------------------------------

- Auto-detect project from cwd (look for `examples/Proj*/`).
- ASK task-group if not given. Group letter must be **R**;
  scaffold a new `R{NN}_<cohort_name>/` if needed
  (see `../../../haipipe-task/fn/task-group.md`).


Step 2 — Collect metadata
--------------------------

- 2-digit NN: next free in this group (no gaps).
- snake_case task_name: `stage{N}_{description}`
  (e.g., `stage1_extract_tables`, `stage2_process`, `stage1_extract_claims`).
- Stage number (1, 2, 3, ...): which stage in the cohort extraction pipeline.
  - stage1 = SQL extraction to parquet (Databricks)
  - stage2 = Python processing of parquet (local)
  - stage3+ = further processing (optional)
- Cohort name: which raw data cohort (e.g., `prediabetes`, `adhd`).
- `_meta:` block (purpose / note / input / output).


Step 3 — Create skeleton
-------------------------

```
R{NN}_<cohort>/
└── {NN}_stage{S}_{desc}/
    ├── {NN}_stage{S}_{desc}.py              SQL strings in Python; # %% cells
    ├── configs/
    │   └── <run_name>.yaml                  from ref/config-seed.yaml
    ├── runs/
    │   └── <run_name>.sh                    from ref/run-databricks-sh-template.sh
    ├── results/                              runtime.yaml only
    └── notebooks/                            convert-only .ipynb
```


Step 4 — Seed config
---------------------

Copy `ref/config-seed.yaml` to `configs/<run_name>.yaml`.
Fill in:
- `_meta:` (purpose / input / output).
- `stage:` (1, 2, 3, ...).
- `execution:` (`databricks` for stage1, `local` for stage2+).
- Databricks params (catalog, schema, volume) for stage1.
- Local params (raw_store_path, cohort) for stage2+.


Step 5 — Run-script
--------------------

Copy `ref/run-databricks-sh-template.sh` to `runs/<run_name>.sh`.
Set `TASK_NAME="{NN}_stage{S}_{desc}"`.

This template converts `.py` → `.ipynb` only — no papermill execute.
The notebook is meant for Databricks upload.


Step 6 — Cross-skill link
--------------------------

After scaffolding, suggest:
- Upload notebook to Databricks and run (for stage1)
- `/haipipe-data-raw understand <cohort>` (to document the data)
- `/haipipe-data-source` (to wrap into Stage 1 SourceFn later)


Step 7 — Report
----------------

```
status:    ok
summary:   Scaffolded raw extraction task <NN>_stage<S>_<desc> under R{NN}_<cohort>.
artifacts: [paths created]
next:      Upload notebook to Databricks  OR  /haipipe-data-raw understand <cohort>
```


MUST NOT
---------

- Write complex multi-table JOINs in the SQL strings — one query per
  source table, keep it simple.
- Use `spark.sql()` for local processing — Spark is extraction-only.
  Once data is local, use pandas.
- Place `.parquet` files in `results/` — they go to `_WorkSpace/0-RawStore/`.
- Skip the `_meta:` block.
- Create `README.md`.
