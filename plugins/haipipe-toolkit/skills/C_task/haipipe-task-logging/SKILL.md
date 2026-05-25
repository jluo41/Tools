---
name: haipipe-task-logging
description: "Task-folder-scope logging specialist. Regenerates <task-folder>/task-log.md — an aggregated markdown view of every run in a task-folder, derived from results/<RUN>/runtime.yaml. Called automatically by runs/<RUN>.sh at finalize, or invoked directly to re-render. Read-only on runtime.yaml (source of truth); writes only task-log.md. Scope: task-folder. Group/project rollups are not in scope."
argument-hint: [task-path] [--print]
allowed-tools: Bash, Read, Glob
---

Skill: haipipe-task-logging
============================

**Task-folder-scope** observability specialist. Owns the derived
`<task-folder>/task-log.md` — a one-glance summary of every run in a
task. Reads from `results/<RUN>/runtime.yaml` (the per-run source of
truth, written atomically by `runs/<RUN>.sh`); writes only `task-log.md`.

Scope is **deliberately narrow**: this skill operates on ONE task-folder
at a time. Group-level (`group-log.md`) and project-level
(`project-log.md`) rollups are intentionally out of scope here — they
would be separate skills if/when needed.


Position in the section
------------------------

```
C_task/
├── haipipe-task              🧭 task orchestrator (creation)
├── haipipe-task-{data, algo, training, eval, display, individual, agent}
│                             🏗️  7 task-type specialists (creation)
└── haipipe-task-logging      📜 task-folder observability (READ-only) ⭐
```

Distinction: the 7 task-type specialists are **creation** (scaffold new
task-folders). This skill is **observation** (summarize what's been run).


Commands
--------

```
/haipipe-task-logging <task-path>            regen <task-path>/task-log.md
/haipipe-task-logging <task-path> --print    regen + cat the file
/haipipe-task-logging                        ASK which task-path (or cwd if inside one)
```

Auto-invocation: `runs/<RUN>.sh` calls `ref/regen_task_log.py` directly
at finalize (no Skill dispatch needed in the hot path). This skill is
the **manual / ad-hoc** entry point.


What gets written
------------------

```
<task-folder>/
├── results/
│   ├── run_a/runtime.yaml      📊 source of truth (per-run, atomic)
│   ├── run_b/runtime.yaml
│   └── ...
└── task-log.md                 📜 derived (this skill writes only this file)
```

Contents of `task-log.md`:
  - task / group / type header (type inferred from group letter)
  - one row per run, newest first
    (status · started · duration · exit · headline · notebook)
  - `Abandoned runs` block when any `status=running` is older than 24h
  - presence of `CODE_REVIEW.md` flagged in the header


Function map
-------------

```
regen / log / refresh        → fn/regen.md
(default — no verb)          → same as `regen`
```

Future commands (NOT implemented, placeholders for the same surface):

```
status   <task-path>   one-line "task last run X minutes ago: ok"
runs     <task-path> --status failed   filter the table
inspect  <task-path> <run-name>        cat one runtime.yaml + headline
```

Add only when the demand is concrete; don't speculate.


Step-by-Step Protocol
----------------------

Step 0: Read `fn/regen.md` for the detailed flow.

Step 1: Parse args:
          - first positional → task-path. If missing and cwd is inside a
            task-folder (has `runs/` + `configs/`), use cwd.
          - `--print` flag → cat the regenerated file after writing.
          - other positionals → ignored (current single-function scope).
        If still no task-path:
          AUTO        → status: blocked, reason: "no task-path given and cwd not in a task-folder"
          interactive → ASK.

Step 2: Validate task-path exists and looks like a task-folder
        (must contain `results/` OR be eligible to receive one).

Step 3: Invoke `ref/regen_task_log.py <task-path>`. Capture stderr
        for non-fatal warnings.

Step 4: If `--print`, `cat <task-path>/task-log.md`.

Step 5: Emit return contract:

```
status:    ok | blocked | failed
summary:   "Regenerated task-log.md for <task>; N runs (M ok, K failed)."
artifacts: [<task-path>/task-log.md]
next:      (none typically — log is a leaf observation)
```


Risk profile
-------------

Reads `results/<RUN>/runtime.yaml` and `CODE_REVIEW.md` (read-only).
Writes ONLY `<task-folder>/task-log.md` (overwrites, atomic via Python
file write). Never touches `results/<RUN>/` contents, notebooks/, or
configs/.

Non-fatal: if `ref/regen_task_log.py` errors, the skill returns
`status: failed` with the stderr quoted; nothing else is modified.


Why a dedicated specialist
---------------------------

  - **Single responsibility**: regen is one task; future log-related ops
    have a clear home.
  - **Non-conflicting with creation**: the 7 task-type specialists own
    "what kind of task to make"; this skill owns "summarize what's been run."
  - **Discoverability**: `/haipipe-task-logging` is grep-able as the
    log entrypoint.
  - **Symmetric with project layer**: B_project has `-inspect` for
    project-scope reads; this is the task-scope equivalent.
