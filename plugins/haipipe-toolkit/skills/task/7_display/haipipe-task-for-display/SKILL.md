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
  version: "0.3.3"
  last_updated: "2026-09-04"
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

Skill: haipipe-task-for-display
====================================

Scaffolds a **display-input job** — the verified summary data a paper figure or table needs.
It consumes governed Result artifacts from upstream Runs and produces a small,
display-ready `source_data.csv` plus `provenance.json`.
A non-Page display holder may materialize that input into its Intake directly.
A Board Page must first route every numeric value through its one
`task-type: page` collection Job; the page-service Result, not this upstream
aggregate directly, becomes the Supporting Run edge.

## Output contract

Every successful Run writes:

```text
$OUTPUT_ROOT/results/<task>/<run>/source_data.csv   small display-safe aggregate
$OUTPUT_ROOT/results/<task>/<run>/provenance.json   Task, Run, sources, selection, and SHA-256
```

`provenance.json` follows `ref/provenance-template.json`.
It must declare `approved_for_display_intake: true` and `contains_raw_or_phi: false` before a
paper Display stage may snapshot the CSV.
The snapshot manifest repeats the task holder and artifact hash so the paper can be audited even
when the task folder is remote or later changes.

**Invocation modes:** interactive (human steers; missing fields get ASKed) OR headless (`haipipe-task-creator-agent` calls this skill during Phase 2: Build, then authors the `<TASK>.py` body).
Always end with the structured return block (status / summary / artifacts / next — the same tail every task skill emits).



What this scaffolds
-------------------

```
tasks/b<NN>_<display-input-block>/
└── j<NN>_<figure-or-table-name>/
    ├── src/
    └── t01_display_input_summary/
        ├── t01_display_input_summary.md
        ├── scripts/
        │   ├── prepare_display_input.py
        │   └── config/r01_<kind>_<name>.yaml
        └── runs/r01_<kind>_<name>.sh

$OUTPUT_ROOT/results/t01_display_input_summary/r01_<kind>_<name>/
├── source_data.csv
├── provenance.json
├── runtime.yaml
└── diagnostics/                              optional
```

Heavy outputs: none.


Cross-reference to pipeline skill
----------------------------------

No corresponding pipeline skill: display-input Tasks are independent; they
read upstream governed Results and write a verified aggregate, not a
publication asset. A non-Page display holder may consume it through an Intake
manifest. A Page routes it through `haipipe-task-for-page` first, preserving
the Page family's one numeric door.


Scaffold flow
-------------

See `fn/scaffold.md` for the detailed step-by-step.
Summary:

  1. Identify project + block.
  2. Collect metadata (NN, name, type-specific extras, _meta block).
  3. Create the canonical Job/Task skeleton (`scripts/`, `scripts/config/`, `runs/`).
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
next:      suggested next command (usually bash <task>/runs/<run>.sh)
```



Workflow plan
--------------

When `/haipipe-task plan` targets an existing job of this type, the generated plan-script YAML should follow the type-specific sample:

```
ref/workflow-plan-sample.yaml     ← script-level phases for this type
../../haipipe-task/ref/workflow-template.yaml  ← task-level template (Run/Gate1/Gate2)
```

Schema source of truth:
  task/haipipe-workflow/ref/plan-schema.md
