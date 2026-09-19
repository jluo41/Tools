# Running a Task on Databricks

Use this reference when the canonical Task executes on a Databricks cluster.
The Block/Job/Task/Run hierarchy does not change. Every rule marked *proven*
was hit and fixed on a live workspace (REACH-SPACE, SAFER desktop, 260907 to
260918); the project's own `safer/README.md` holds the evidence.

```text
bNN_<block>/jNN_<job>/
├── sbatch/                      flat lists of Run tickets (see Batches)
└── tNN_<task>/
    ├── tNN_<task>.md
    ├── scripts/
    │   ├── <entry>.py           notebook source: line 1 is `# Databricks notebook source`
    │   └── config/rNN_<run>.yaml
    ├── runs/rNN_<run>.sh        or rNN_<run>.cmd where only cmd.exe runs
    └── results/rNN_<run>/       fetched from the Volume; aggregates only
```

The `.py` source remains authoritative. Anything generated from it (a run
record, cluster logs) lives outside the Task Folder or under the Run's
resolved projection, never at Block or Job root.

## The ticket

A ticket carries no parameters. Block, job, task and run are read from its own
path, and its stem is the Run and the config stem. It drives the whole loop:

```text
1 DEPLOY   local -> workspace          databricks bundle deploy
2 RUN      on the cluster              as a Job, or inline (Execution choices)
3 FETCH    Volume -> <task>/results/<run>/   this Run's folder only
```

On a locked-down Windows desktop the ticket is `.cmd`: there is no bash, a
`.ps1` on a mapped drive is refused by Constrained Language Mode, and AppLocker
refuses a venv's `python.exe` there. cmd.exe runs. *Proven.*

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

- **The entry notebook binds `RUN` in its own globals.** An inline runner reads
  it after the run and fails when it is not the Run asked for, so r01's numbers
  cannot be filed under r02. An entry that hands everything to an imported
  worker and never binds `RUN` does its work and is then reported failed.
  *Proven:* 56 of 58 Runs in one Job, caught by a laptop harness.
- **`dbutils` and `display` are notebook globals**, invisible from an imported
  module. The entry passes them in: `run_task(HERE, dbutils=globals().get("dbutils"),
  display=globals().get("display"))`, and the worker returns `(run, summary)`.
- **Run all by hand passes nothing.** The entry builds a `RUN` dropdown of its
  configs only when neither a widget nor the `RUN` environment variable has
  answered. Building it when a Job already set the widget can reset it to its
  default and silently run r01 for every ticket.

## Execution choices

Use a Databricks Job Task when the cluster policy permits Jobs workloads.

A Notebooks-only policy (the Personal Compute family, `workload_type:
Notebooks`) refuses every job, and `dbutils.notebook.run()` is a job too: it
starts its child as an ephemeral job and dies with `does not support jobs
workload`. Serverless may be allowed Jobs but refused the data. When both
hold, the one route is an INLINE notebook run, driven by the ticket. *Proven.*

1. Copy the entry's source and a small runner onto the Volume.
2. Open an execution context on the cluster (the 1.2 Command Execution API,
   the one VS Code's *Upload and Run File* uses).
3. The runner `exec`s the source cell by cell, splitting where Run all would
   (`# COMMAND ----------` or `# %%`), with `RUN` set.
4. Poll until it finishes; print what the notebook printed, line by line, and
   its `notebook.exit()` summary.

- Keep inline runs sequential on one Spark session; never a thread pool.
- A child's `notebook.exit()` ends that child, never the runner.
- **Never destroy the execution context on a client-side timeout:** destroying
  it kills the running command. Stop watching, exit with a distinct
  still-running code, and fetch later. Never advise running it again by hand,
  which starts a second copy. *Proven:* a one-hour wait killed a longer run.
- Pass a still-running or failed outcome up as a literal exit code. In cmd.exe,
  `exit /b %errorlevel%` inside a parenthesized block expands before the block
  runs and always reports the value from before it.

## Results

```text
Volume   <VB>/task-results/<block>/<job>/<task>/<run>/
local    <task>/results/<run>/
```

- **Each Run delivers its own Result folder**, and its ticket fetches that one
  folder, never the whole Job. A whole-Job fetch in a batch of twenty tickets
  copies the Job twenty times.
- **The REST API is the route down.** Workspace UI downloads may be disabled,
  which also removes the arrow above a `display()` table; `databricks fs cp`
  still works. *Proven.*
- **A Volume file exists only once its handle closes.** Always `with
  open(...)`. `fs cp` does not create parent folders.
- **Only aggregates leave the server.** Counts from 1 to `min_cell - 1` are
  written `<min_cell`. A count whose complement is small is a small cell too
  (995 nulls in 1,000 rows names the 5 with a value), so it is written as a
  bound. A per-year series needs secondary suppression, or its total gives the
  masked year back. Terminal output and run records are not masked; they stay
  on the approved desktop and workspace.

Heavy data lands in the configured Unity Catalog Volume using the same store
families as `_WorkSpace/`. PHI remains on the approved server or Volume; only
approved aggregate Results may leave it.

## Run record

An inline run leaves the deployed notebook without output, because the code
ran in its own execution context. So the runner records each cell's source and
output (stdout, `display()` as HTML, and a failing cell's error) as an nbformat
4.4 notebook. The ticket imports it to `/Users/<you>/<repo>-runs/<task path>/<run>`
and prints its link as `RESULTS`. It lives beside the bundle, not in its
`files/`, which every deploy rewrites. A failing Run's record shows the error,
and the Run still fails.

## Batches

- **A batch is a flat list of Run tickets:** one call per ticket, in the order
  they run. No loop and no `if exist` skip, because either decides the Runs
  from whatever exists on the day.
- Only `run_all` calls other batches, so no list is written twice, and a Job's
  `run_all` must reach every ticket that Job has.
- Order a batch by what a reader needs complete. A table group runs its shape,
  columns and time-coverage Runs back to back; a roll-up that combines the
  groups runs after them, and only when the Runs it reads have passed.
- Each ticket opens and closes with a full-width rule naming its Run and its
  outcome (`OK`, `FAILED`, `FETCH-FAILED`, `STILL-RUNNING`). Each batch has its
  own rule and closes with a table of every Run's outcome.
- **A batch deploys once**, at its start, and its tickets skip their own
  DEPLOY; a ticket run alone still deploys. Nothing changes between two tickets
  of one batch, so one deploy and twenty leave the same workspace, and one
  means every Run of the batch ran the same code.
- **Resume is opt-in.** A `resume` mode skips a Run whose receipt already says
  `status: ok` (and still fetches it), so a stopped batch picks up where it
  stopped. It is never the default: a skipped Run keeps what an older version
  of the code wrote.

## Deploy pitfalls

- A notebook-source `.py` and an `.ipynb` of the same stem both upload as the
  same notebook path, and `bundle deploy` stops: `both ... point to the same
  remote file location`. `bundle validate` does not catch it. *Proven.*
- A `sync.exclude` pattern matches at any depth unless it starts with `/`.
  `scripts/**` removed every Task's `scripts/`. *Proven.*
- `bundle deploy` validates every included resource file, so one project's
  missing notebook stops another's deploy. Include a list of file names, never
  a `*.yml` glob. *Proven.*

## runtime.yaml

For cluster execution, `runtime.yaml` records `status`, the Run, the end time,
the counts written (with the `min_cell` applied), and where available the
Databricks Run id, workspace path, cluster identity, config hash, source git
SHA, and Result-gate verdict.

## Memory discipline

- Read Parquet metadata for row/schema checks instead of loading large tables.
- Stream checksums.
- Chunk large source tables and write a success marker for resumability.
- Keep inline execution sequential on a shared Spark session.

## Validation

Before launch, verify the Task Folder with `ref/check_task_tree.py`, confirm the
Run config/Ticket stem pair, and verify that cluster output resolves to the
same `<task>/<run>` Result identity used locally.

A project that runs this way keeps two laptop-side guards, because the desktop
may have no working Python. REACH-SPACE's are the pattern:

- `safer/scripts/check_run_tickets.py`: every ticket has its config, its bundle
  job, its uploaded notebook, no `.py`/`.ipynb` twin, and every batch is a flat
  list whose `run_all` reaches every ticket.
- `safer/selftest/j01_inline_contract.py`: every Run of a Job through the real
  inline runner with a stand-in Spark, checking the `RUN` binding, one Result
  folder per Run, no small cell, the by-hand dropdown, and the run record.
