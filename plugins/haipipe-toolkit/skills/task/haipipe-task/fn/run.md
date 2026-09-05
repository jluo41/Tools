fn-run: Scaffold a New Run
==========================

A Run is one authored Ticket paired with one generated Result address and one
runtime receipt.
Load `haipipe-run`, `ref/hierarchy.md`, and
`ref/runtime-yaml-schema.md` before scaffolding.
This verb creates the pre-run contract and never executes it.


Step 1 — Resolve Job, Task, mode, and RUNNAME
----------------------------------------------

Resolve the Job by structure, never by its name.
For a canonical nested Job, resolve exactly one `tNN_<task>/`; cwd inside the
Task wins, one Task total is unambiguous, and otherwise interactive mode asks.
For a flat legacy Job, the Task segment is empty.

Resolve `$OUTPUT_ROOT` using the Task owner's mode law:

```text
RESULT_STORE from the dispatching caller      wins
Job `store:` declaration                     consumer-serving
neither                                      Job root, self-serving
```

Ask for the RUNNAME when it is not supplied.
New canonical names are `rNN_<family-bearing-stem>`, lowercase, immutable,
and unique within the Task.
Use the next free two-digit `rNN`; never renumber or overwrite.


Step 2 — Collect the Run contract
---------------------------------

Use supplied fields verbatim.
Ask only for genuinely missing fields when a person is present.
Headless mode returns blocked rather than inventing a required field.

```text
purpose          why this Run exists
family           Execution | Discovery | Page | Labeling
operation        independently closable operation
target           bounded target
input            authoritative inputs to freeze
output           expected Result payload
required_results relative files under Result dir that form the minimum gate
```

For a Page Evidence Item Run, set `family=Page`,
`operation=evidence-item`, `target=<full Evidence Item id>`, and
`required_results=("result.yaml")`; add its frozen Local Input path and LAND
hash to `RUN_INPUTS`.
For a page-serving aggregate Run, set `family=Execution`,
`operation=collect-page-values`, and
`required_results=("values.yaml")`.


Step 3 — Create the authored projections
-----------------------------------------

```text
flat legacy
  config   <job>/configs/<RUNNAME>.yaml
  Ticket   <job>/runs/<RUNNAME>.sh

canonical nested
  config   <job>/<task>/scripts/config/<RUNNAME>.yaml
  Ticket   <job>/<task>/runs/<RUNNAME>.sh
```

Copy `../ref/config-meta-template.yaml` for the config and fill its required
`_meta.purpose`.
Copy `../ref/run-sh-template.sh` for the Ticket and set all five contract
declarations: `TASK_NAME`, `RUN_FAMILY`, `RUN_OPERATION`, `RUN_TARGET`,
and `REQUIRED_RESULTS`.
Set `RUN_INPUTS` to every declared frozen input path/hash beyond the Run config;
the Ticket resolves any permitted `|auto` hash once at launch and preserves
that same binding in both running and terminal receipts.
Extend `result_gate()` when file existence is not the worker's full semantic
acceptance test.
Make the Ticket executable.


Step 4 — Create the planned generated projection
-------------------------------------------------

Create the resolved Result directory:

```text
flat legacy       $OUTPUT_ROOT/results/<RUNNAME>/
canonical nested  $OUTPUT_ROOT/results/<task>/<RUNNAME>/
```

At scaffold time write `runtime.yaml` atomically with `status: planned` and
the complete neutral identity fields from `ref/runtime-yaml-schema.md`.
Record the Ticket path, Result path, declared inputs, worker, config path/hash,
settings, `started_at: null`, `finished_at: null`, and `failure: null`.
The Ticket changes the same receipt to `running` before expensive work and to
a truthful terminal state after the declared Result gate.

Create the resolved `$OUTPUT_ROOT/notebooks/<task>/` parent only when the
selected notebook policy owns an execution record.
Do not create `runlogs/`; the Run inventory comes from Tickets and receipts,
and Page/Task Logs use their owning contracts.


Step 5 — Validate
-----------------

- Confirm the canonical Task script resolves at
  `<task>/scripts/<TASK_NAME>.py`.
- Confirm the Ticket and config share one RUNNAME.
- Confirm `_meta.purpose` is non-empty.
- Confirm all five required Ticket declarations and every `RUN_INPUTS`
  path/hash match the collected contract.
- Confirm the resolved planned receipt contains every required neutral and
  Task-dialect field.
- Confirm there is no collision in config, Ticket, Result, or notebook paths.
- Run `bash -n <ticket>`.


Step 6 — Report
---------------

```text
status:    ok | blocked | failed
summary:   Scaffolded <global Run id> as one Ticket → Result contract.
artifacts: [config, Ticket, planned runtime receipt]
next:      fill parameters, satisfy the code-review gate, then launch the Ticket
```


MUST NOT
--------

- Execute the Ticket.
- Create a Task-local `results/` directory in a canonical nested Task.
- Use `<task>/config/` or `<job>/runs/<task>/` for a new Run.
- Leave the copied Ticket's default family, operation, target, or Result gate
  unchanged when they do not match the commissioned Run.
- Mark the planned receipt complete.
- Touch another Run's files.
