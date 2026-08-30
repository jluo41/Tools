fn-run: Scaffold a New Run
============================


> JL: do not break the sentences. One line one sentence.
>> CC 23:17: [SOLVED] Done — this file is authored one sentence per line (verified: reflow is a no-op). Now a standing convention in haipipe-task/PREFERENCES.md.

A run is the unit of execution within a job.
The four sister files share one NAME token:

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

This scaffold creates the **pre-run** half (config + run.sh); the rest is auto-created by `runs/<NAME>.sh` at execution.


Step 1 — Resolve job + shape + NAME
------------------------------------

Auto-detect job from cwd.
If cwd is not a job, ASK.

Detect the job SHAPE (hierarchy.md "Two job shapes"): a scripts/ dir with
{NN}_* children = NESTED, else FLAT legacy. In a nested job also resolve
TASK_SEG — which scripts/<task>/ this run belongs to (cwd inside one wins;
one task total = that one; else ASK). Never scaffold a flat ticket into a
nested job: the template's own auto-detect would then resolve the wrong
config and script paths.

ASK for `<NAME>` if not given.
Constraints:
  - Convention: prefix with `run_` (e.g. `run_seed42_baseline`)
  - Descriptive — encodes the variant (seed/arch/data slice)
  - Unique within this job (refuse on collision)
  - Lowercase, snake_case, `[a-z0-9_]+`


Step 2 — Collect _meta fields (4 questions)
--------------------------------------------

**Dual-mode (see `../ref/invocation-modes.md`):** if the spec already carries these fields (agent / headless path), DO NOT ASK — use them verbatim and run silently.
Only ASK for fields genuinely missing AND when a user is present.
If `purpose` is missing and there is no user (agent path), return `status: blocked, missing: [purpose]` — never invent it.

ASK (interactive path only) in this order.
`purpose` is REQUIRED:

```
1. purpose  — One sentence: why does this run exist?
              (required; if user can't answer, halt)
2. note     — Free-form thoughts / discussion-derived rationale (multi-line ok)
3. input    — Semantic description of data + ckpt origin
4. output   — Expected artifacts + headline guess
```

End every invocation with the structured return block from `../ref/invocation-modes.md` (status / task_folder / run_name / files), so an agent caller can locate the scaffolded folder to author into.


Step 3 — Create files
----------------------

```
config — configs/<NAME>.yaml (flat) · scripts/<TASK_SEG>/config/<NAME>.yaml (nested)
  Copy from ../ref/config-meta-template.yaml.
  Fill in _meta: block with values from Step 2.
  Leave params section as a comment placeholder for user to fill.

ticket — runs/<NAME>.sh (flat) · runs/<TASK_SEG>/<NAME>.sh (nested)
  Copy from ../ref/run-sh-template.sh (it detects the shape from its own path).
  Edit line `TASK_NAME=...` to match the .py basename.
  chmod +x.

results/<NAME>/ (flat) · results/<TASK_SEG>/<NAME>/ (nested)
  mkdir -p (empty; the ticket will populate runtime.yaml at launch).

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
```


Risk profile
-------------

CREATES files under existing job.
Refuses to overwrite.
For moving / renaming an existing run, see `-organize` specialist.


MUST NOT
---------

- Create `<NAME>` without a `_meta.purpose` value.
- Touch other runs' files.
- Run the script (this is scaffold-only — separate concern).
- Modify the run.sh wrapper template (always copy-and-edit per-run).
- Skip the auto-meta wrapper (every run.sh must have it).
