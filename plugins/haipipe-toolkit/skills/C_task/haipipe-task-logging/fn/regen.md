fn-regen: Regenerate task-log.md
=================================

Re-render the aggregated task-folder log from per-run `runtime.yaml`
files. The actual rendering logic lives in `ref/regen_task_log.py`
(no PyYAML dependency; hand-parses the flat key:value schema).


Inputs
------

- `<task-path>` (required positional, or cwd if inside a task-folder)
- `--print` (optional): cat the regenerated file after writing


Step 1 — Resolve task-path
---------------------------

- Use the first positional arg.
- If missing, check if cwd contains `runs/` AND `configs/` (cheap sniff
  for a task-folder). If yes, use cwd.
- Else:
    AUTO         → status: blocked, reason: "no task-path"
    interactive  → ASK.


Step 2 — Validate
------------------

```bash
test -d "$TASK_PATH" || fail "task-folder not found: $TASK_PATH"
```

It is fine if `<task-path>/results/` does not exist yet — the script
will emit a minimal task-log.md with `runs: 0`.


Step 3 — Run the regen script
------------------------------

```bash
python3 \
  Tools/plugins/haipipe-toolkit/skills/C_task/haipipe-task-logging/ref/regen_task_log.py \
  "$TASK_PATH"
```

The script:
  1. Globs `<task-path>/results/*/runtime.yaml`.
  2. Parses each (10-field flat schema; no dep on PyYAML).
  3. Sorts newest-first by `started`.
  4. Flags `status=running` entries older than 24h as "abandoned".
  5. Detects task-type from parent folder letter (A/B/C/D/E/F/X).
  6. Detects `<task-path>/CODE_REVIEW.md` presence.
  7. Writes `<task-path>/task-log.md` (overwrite).


Step 4 — Optional print
------------------------

If `--print` was passed:

```bash
cat "$TASK_PATH/task-log.md"
```


Step 5 — Return contract
-------------------------

```
status:    ok | blocked | failed
summary:   "Regenerated task-log.md for <task-name>; N runs (M ok, K failed[, A abandoned])."
artifacts: [<TASK_PATH>/task-log.md]
next:      (none typically)
```

Failure modes:
  - Script not found → blocked: "regen script missing at expected path"
  - Python error → failed: quote stderr; nothing written
  - task-path doesn't exist → blocked: "task-folder not found"


MUST NOT
---------

- Edit any `results/<RUN>/runtime.yaml` (source of truth, atomic-write
  by `runs/<RUN>.sh` only).
- Edit any notebook in `notebooks/`.
- Touch `configs/`, `CODE_REVIEW.md`, or anything outside `task-log.md`.
- Append to `task-log.md` — always full overwrite to keep it derived.
