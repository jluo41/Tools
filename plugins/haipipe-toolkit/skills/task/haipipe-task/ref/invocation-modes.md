Invocation modes — interactive vs headless (dual-mode contract)
===============================================================

Every `haipipe-task-for-<type>` skill is callable two ways over ONE body.
The mode is chosen by **input completeness**, NOT by who calls — a human
who supplies everything also gets headless; an agent always supplies
everything.

```
              ┌────────────────────────────────────────┐
  human ─────▶│   haipipe-task-for-<type>  (one body)   │
  (usually    │   input gate:  spec complete?           │
   partial)   │      ✅ yes → SILENT  (skip all ASK)     │◀──── haipipe-task-builder-agent
              │      ❌ no  → ASK the missing fields     │      (always passes full spec → SILENT)
  agent ─────▶│   rest of scaffold logic is identical   │
  (full spec) └────────────────────────────────────────┘
```

What "spec complete" means
--------------------------

The required inputs for a silent run:

```
□ run NAME              (run_-prefixed, snake_case)
□ _meta.purpose         (the one hard-required field)
□ Job target            (resolved parent container, not "ASK from cwd")
□ Task Folder target    (`tNN_<task>/`, also the Page Folder)
□ type params           (the type's hyperparams / pipeline config)
```

`_meta.note / input / output` are recommended but NOT blocking — a silent
run may proceed with them empty (they default to "" and log a warning into
the structured result, never an ASK).

`_meta.notebook: full | thin | off` is optional (default `full`). It controls
how much of the per-run papermill notebook is retained — `thin` for heavy
compute (training/data), `full` for read-output types (display/eval/...),
`off` for rare pure-artifact runs. See `authoring-conventions.md` §7. A creator
authoring a heavy-type task should set `thin` in the config it writes.

Rules
-----

1. **Silent (headless):** if all required inputs are present, DO NOT ASK
   anything. Use the provided values verbatim. No "next:" human prompts.
2. **Interactive:** if any required input is missing AND a user is present,
   ASK only for the missing fields (not the ones already given).
3. **Missing input, no user (agent path):** do NOT hang on an ASK. Return a
   structured `status: blocked` naming the missing field — the caller (agent)
   re-dispatches with it filled. Never silently invent `purpose`.

Structured return (so an agent caller can consume it)
-----------------------------------------------------

Every invocation ends by emitting this block (in addition to any prose for
a human):

```
status:       ok | blocked | failed
job:          <absolute path to the parent jNN_<job>>      (on ok)
task_folder:  <absolute path to tNN_<task>>                (on ok; same as Page Folder)
run_name:     <NAME>
files:        [scripts/config/<NAME>.yaml, runs/<NAME>.sh, $OUTPUT_ROOT/results/<task>/<NAME>/]
missing:      [<field>, ...]                                (on blocked)
note:         <one line>
```

A creator agent reads `task_folder` to know where to author
`scripts/<TASK>.py` and the same-stem Page. It reads `job` only for shared
`src/`, batch orchestration, and resolved Result/Notebook roots. A new
specialist may not return the Job path in `task_folder`.
