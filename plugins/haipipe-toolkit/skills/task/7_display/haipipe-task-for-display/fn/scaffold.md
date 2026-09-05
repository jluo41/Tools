fn-scaffold: Scaffold a display-input Job
=========================================

Produce one verified display-ready aggregate from governed upstream Results.
Load `haipipe-task`, its hierarchy, and `haipipe-run` first.
This specialist creates canonical nested Task structure and never creates the
final Page or Paper display asset.


Step 1 — Resolve Project, Block, and mode
-----------------------------------------

- Resolve the Project from cwd or the explicit path.
- Reuse a compatible existing Block when one owns display-input preparation.
- Otherwise create the next canonical `bNN_<noun>_<qualifier>/` Block through
  `haipipe-task block`; no project-independent C-series default exists.
- Decide self-serving versus consumer-serving through the Task owner's
  `store:` gate before writing generated paths.
- Return blocked rather than guessing any unresolved owner or store.


Step 2 — Collect the contract
-----------------------------

- Job name: `jNN_<noun>_<qualifier>`, passing the stranger test.
- Task name: normally `t01_display_input_summary`.
- Run name: `r01_<kind>_<slug>`.
- Display kind: `figure | table | diagram | illustration`.
- Source Runs: full Run ids plus resolved Result paths and hashes.
- Summary parameters: selected columns, grouping, filters, and unit of analysis.
- Output contract: `source_data.csv` plus `provenance.json`.


Step 3 — Create canonical authored structure
--------------------------------------------

```text
tasks/bNN_<display-input-block>/
└── jNN_<figure-or-table-name>/
    ├── src/
    └── t01_display_input_summary/
        ├── t01_display_input_summary.md
        ├── scripts/
        │   ├── prepare_display_input.py
        │   └── config/
        │       └── r01_<kind>_<slug>.yaml
        └── runs/
            └── r01_<kind>_<slug>.sh
```

Copy `ref/config-seed.yaml` into the canonical `scripts/config/` path and
fill every required field.
All source paths remain in that config; the Python worker hardcodes none.


Step 4 — Configure the Ticket and planned receipt
--------------------------------------------------

Copy `../../../haipipe-task/ref/run-sh-template.sh` into the Task's `runs/`
lane and set:

```bash
TASK_NAME="prepare_display_input"
RUN_FAMILY="Execution"
RUN_OPERATION="display-input"
RUN_TARGET="<kind>-<slug>"
REQUIRED_RESULTS=("source_data.csv" "provenance.json")
RUN_INPUTS=("<resolved-source-1>|<sha256>" "<resolved-source-2>|<sha256>")
```

The generic file-existence gate is necessary but not sufficient.
Extend `result_gate()` to require `provenance.json` to declare
`approved_for_display_intake: true`,
`contains_raw_or_phi: false`, and hashes matching `source_data.csv`.

Resolve the planned Result at
`$OUTPUT_ROOT/results/t01_display_input_summary/<RUNNAME>/`.
Write the scaffold-time `runtime.yaml` with `status: planned` according to
`haipipe-task/ref/runtime-yaml-schema.md`.
Do not create a Task-local `results/` directory.


Step 5 — Output contract
------------------------

The worker writes:

```text
$OUTPUT_ROOT/results/t01_display_input_summary/<RUNNAME>/
├── source_data.csv
├── provenance.json
├── runtime.yaml
└── diagnostics/          optional and never the canonical display asset
```

`provenance.json` follows `ref/provenance-template.json`.
It records the producing Task and Run, output hash, upstream artifacts,
selection and filter logic, and the two display-safety assertions.
A Page consumer sends this aggregate through its one page-serving collection
Job; LAND freezes the selected page-service Result into the Evidence Item's
Local Input. A non-Page holder may freeze the approved CSV directly into its
display Intake. In both cases the final renderer and visible asset remain
owned by the display unit.


Step 6 — Validate and report
----------------------------

- Run `bash -n` on the Ticket.
- Run the Task-tree checker on the touched tree.
- Confirm config/Ticket stems match and every source Run resolves.
- Confirm the planned receipt contains the neutral Run fields and config hash.
- Confirm no protected or heavy artifact is planned under `results/`.

```text
status:    ok | blocked | failed
summary:   Scaffolded one canonical display-input Task and Run.
artifacts: [Page, script, config, Ticket, planned runtime receipt]
next:      satisfy CODE_REVIEW, then launch <task>/runs/<RUNNAME>.sh
```


MUST NOT
--------

- Scaffold a flat `C{NN}/{NN}/configs/` shape for new work.
- Hardcode upstream paths in Python.
- Modify upstream Results.
- Put model training or the final PDF/PNG/TeX asset in this Task.
- Create a general README.
- Mark the planned receipt complete or bypass the provenance gate.
