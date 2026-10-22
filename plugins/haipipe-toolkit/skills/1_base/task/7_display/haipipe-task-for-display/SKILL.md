---
name: haipipe-task-for-display
description: >-
  Display-input Job specialist: scaffolds canonical b/j/t/r Task folders
  producing a verified display-ready
  summary CSV plus provenance. The Paper Display stage snapshots that input;
  this task does not own the final paper asset. Called by /haipipe-task when
  task-type=display.
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "0.4.0"
  last_updated: "2026-10-21"
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

Skill: haipipe-task-for-display
====================================

Scaffolds a **display-input job** — the verified summary data a paper figure or table needs.
It consumes governed Result artifacts from upstream Runs and produces a small,
display-ready `source_data.csv` plus `provenance.json`.
A non-Page display holder may materialize that input into its Intake directly.
A Board Page must first route every numeric value through its one
`task-type: evidence` collection Job; the page-service Result, not this upstream
aggregate directly, becomes the Supporting Run edge.

## Type contract

```yaml
task-type: display
skill: haipipe-task-for-display
does: Turns governed upstream Results into one small display-safe summary table, source_data.csv, and its provenance.json for a figure or table.
worker: scripts/prepare_display_input.py (Python), which reads every source path from the Run's config and hardcodes none
config: runs/<run>/config.yaml (seeded from ref/config-seed.yaml), or scripts/config/<run>.yaml in a Block not yet moved
ticket: runs/<run>/<run>.sh, from ../../haipipe-task/ref/run-sh-template.sh (TASK_NAME prepare_display_input, REQUIRED_RESULTS source_data.csv and provenance.json)
result: $OUTPUT_ROOT/<task>/runs/<run>/result/, with runtime.yaml, source_data.csv and provenance.json before the receipt says complete; result_gate() also requires approved_for_display_intake true, contains_raw_or_phi false and a row_count matching the CSV
heavy: none
roles: [make]
companions: [haipipe-run, haipipe-task-for-evidence]
plan_sample: ref/workflow-plan-sample.yaml
```

## Output contract

Every successful Run writes:

```text
$OUTPUT_ROOT/<task>/runs/<run>/result/source_data.csv   small display-safe aggregate
$OUTPUT_ROOT/<task>/runs/<run>/result/provenance.json   Task, Run, sources, selection, and row count
```

`provenance.json` follows `ref/provenance-template.json`.
It must declare `approved_for_display_intake: true` and `contains_raw_or_phi: false` before a
paper Display stage may snapshot the CSV.
The snapshot manifest repeats the task holder, Run, and artifact path so the paper can be audited
even when the task folder is remote or later changes.

**Invocation modes:** interactive (human steers; missing fields get ASKed) OR headless (`haipipe-task-creator-agent` calls this skill during Phase 2: Build, then authors the `<TASK>.py` body).
Always end with the structured return block (status / summary / artifacts / next — the same tail every task skill emits).



What this scaffolds
-------------------

```
work/b<NN>_<display-input-block>/
└── j<NN>_<figure-or-table-name>/
    ├── src/
    └── t01_display_input_summary/
        ├── t01_display_input_summary.md
        ├── scripts/
        │   └── prepare_display_input.py
        └── runs/r01_<kind>_<name>/               one folder per Run
            ├── r01_<kind>_<name>.sh              the ticket
            ├── config.yaml                       this Run's settings
            └── run.yaml                          its card (role: make)

$OUTPUT_ROOT/t01_display_input_summary/runs/r01_<kind>_<name>/result/
├── source_data.csv
├── provenance.json
├── runtime.yaml
└── diagnostics/                              optional
```

A Block not yet moved still has the flat `runs/<run>.sh`, `scripts/config/<run>.yaml` and
`results/<run>/`; the ticket template runs both.

Heavy outputs: none.


Cross-reference to pipeline skill
----------------------------------

No corresponding pipeline skill: display-input Tasks are independent; they
read upstream governed Results and write a verified aggregate, not a
publication asset. A non-Page display holder may consume it through an Intake
manifest. A Page routes it through `haipipe-task-for-evidence` first, preserving
the Page family's one numeric door.


Scaffold flow
-------------

See `fn/scaffold.md` for the detailed step-by-step.
Summary:

  1. Identify project + block.
  2. Collect metadata (NN, name, type-specific extras, _meta block).
  3. Create the canonical Job/Task skeleton (`scripts/`, and one Run folder `runs/<run>/` with its
     Ticket, `config.yaml` and `run.yaml` card).
  4. Seed config from `ref/config-seed.yaml`.
  5. Copy the Ticket template and set family `Execution`, operation
     `display-input`, target, and both required Result files.
  6. For a Page consumer, route the aggregate into its page-serving collection
     Job; otherwise suggest materializing it into the holder's Display Intake.
  7. Emit return contract.


Return contract
---------------

```
status:    ok | blocked | failed
summary:   2-3 sentences on what was scaffolded
artifacts: [paths created]
next:      suggested next command (usually bash <task>/runs/<run>/<run>.sh)
```



Workflow plan
--------------

When `/haipipe-task plan` targets an existing job of this type, the generated plan-script YAML should follow the type-specific sample:

```
ref/workflow-plan-sample.yaml     ← script-level phases for this type
../../haipipe-task/ref/workflow-template.yaml  ← authoritative Run Spec template with entry/exit gates
```

Schema source of truth:
  project/haipipe-run/ref/plan-schema.md
