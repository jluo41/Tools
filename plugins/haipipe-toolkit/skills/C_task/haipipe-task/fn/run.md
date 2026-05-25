fn-run: Scaffold a New Run
============================

A run is the unit of execution within a task-folder. The four sister files
share one NAME token:

```
configs/<NAME>.yaml             📥 frozen input (_meta + params)
runs/<NAME>.sh                  ▶️  entry (wraps papermill + auto-logs)
results/<NAME>/                 📊 light artifacts + runtime.yaml
notebooks/<NAME>.ipynb          📓 papermill executed-notebook record
```

Plus the shared daily file:

```
runlogs/<DATE>-runlog.md        📝 daily index + narrative (run.sh appends)
```

This scaffold creates the **pre-run** half (config + run.sh); the rest is
auto-created by `runs/<NAME>.sh` at execution.


Step 1 — Resolve task-folder + NAME
------------------------------------

Auto-detect task-folder from cwd. If cwd is not a task-folder, ASK.

ASK for `<NAME>` if not given. Constraints:
  - Convention: prefix with `run_` (e.g. `run_seed42_baseline`)
  - Descriptive — encodes the variant (seed/arch/data slice)
  - Unique within this task-folder (refuse on collision)
  - Lowercase, snake_case, `[a-z0-9_]+`


Step 2 — Collect _meta fields (4 questions)
--------------------------------------------

ASK in this order. `purpose` is REQUIRED; others optional but recommended.

```
1. purpose  — One sentence: why does this run exist?
              (required; if user can't answer, halt)
2. note     — Free-form thoughts / discussion-derived rationale (multi-line ok)
3. input    — Semantic description of data + ckpt origin
4. output   — Expected artifacts + headline guess
```

If invoked from a Claude conversation where these are already implicit,
the LLM may pre-fill from context and let user confirm.


Step 3 — Create files
----------------------

```
configs/<NAME>.yaml
  Copy from ../ref/config-meta-template.yaml.
  Fill in _meta: block with values from Step 2.
  Leave params section as a comment placeholder for user to fill.

runs/<NAME>.sh
  Copy from ../ref/run-sh-template.sh.
  Edit line `TASK_NAME=...` to match the task .py basename.
  chmod +x.

results/<NAME>/
  mkdir -p (empty; run.sh will populate runtime.yaml at launch).

notebooks/
  mkdir -p if missing (shared per task, not per run).

runlogs/
  mkdir -p if missing (shared per task, not per run).
```


Step 4 — Validate
------------------

  - Confirm task .py basename matches `runs/<NAME>.sh` TASK_NAME line
  - Confirm `configs/<NAME>.yaml` has non-empty `_meta.purpose`
  - Confirm no name collision in `configs/`, `runs/`, `results/`,
    `notebooks/`


Step 5 — Report
----------------

Print:

```
✅ Scaffolded run: <NAME>
   configs/<NAME>.yaml      (filled _meta, params TODO)
   runs/<NAME>.sh           (executable, auto-meta wrapper)
   results/<NAME>/          (empty)

Next:
   1. Fill params in configs/<NAME>.yaml (below _meta:)
   2. bash runs/<NAME>.sh
   3. /haipipe-project log task         (after run completes, for narrative)
```


Risk profile
-------------

CREATES files under existing task-folder. Refuses to overwrite. For
moving / renaming an existing run, see `-organize` specialist.


MUST NOT
---------

- Create `<NAME>` without a `_meta.purpose` value.
- Touch other runs' files.
- Run the script (this is scaffold-only — separate concern).
- Modify the run.sh wrapper template (always copy-and-edit per-run).
- Skip the auto-meta wrapper (every run.sh must have it).
