---
name: haipipe-task-for-display
description: "display-input task-folder specialist: scaffolds {NN}_<name>/ task-folders in the display task-group (default C-series) that produce a verified display-ready summary CSV plus provenance -> results/<run>/{source_data.csv, provenance.json}. The Paper Display stage snapshots that input into a display unit; this task does not own the final paper asset. Called by /haipipe-task when task-type=display."
argument-hint: "[project_id] [group] [task-name]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "0.2.0"
  last_updated: "2026-07-27"
  summary: "display-input task-folder build specialist: task produces verified summary data; Display owns paper-facing rendering."
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

Skill: haipipe-task-for-display
====================================

Scaffolds a **display-input task-folder** — the verified summary data a paper figure or table needs.
It consumes `results/<run>/` artifacts from upstream tasks and produces a small,
display-ready `source_data.csv` plus `provenance.json`.
The Paper Display stage materializes that input into `displays/displayNN-<slug>/intake/` and
commissions the renderer that produces the publication-facing asset.

## Output contract

Every successful run writes:

```text
results/<run>/source_data.csv   small display-safe aggregate
results/<run>/provenance.json   task holder, run, source artifacts, selection, and SHA-256
```

`provenance.json` follows `ref/provenance-template.json`.
It must declare `approved_for_display_intake: true` and `contains_raw_or_phi: false` before a
paper Display stage may snapshot the CSV.
The snapshot manifest repeats the task holder and artifact hash so the paper can be audited even
when the task folder is remote or later changes.

**Invocation modes:** interactive (human steers; missing fields get ASKed) OR headless (`haipipe-task-creator-agent` calls this skill during Phase 2: Build, then authors the `<TASK>.py` body).
Always end with the structured return block (status / task_folder / run_name / files).



What this scaffolds
-------------------

```
tasks/C{NN}_<group_name>/                    ← C-series group (display)
└── {NN}_<figure_or_table_name>/
    ├── {NN}_<name>.py
    ├── configs/
    │   └── figure_<name>.yaml               or table_<name>.yaml
    ├── runs/
    │   └── figure_<name>.sh
    ├── results/
    │   └── <run>/                           source_data.csv, provenance.json, diagnostics/ (optional)
    └── notebooks/
```

Group letter default: **C** (display).
Heavy outputs: none.


Cross-reference to pipeline skill
----------------------------------

No corresponding pipeline skill — display-input tasks are independent; they read upstream
`results/<run>/` and write a verified aggregate, not a publication asset.
The output can be consumed by any display holder through an Intake manifest.


Scaffold flow
-------------

See `fn/scaffold.md` for the detailed step-by-step.
Summary:

  1. Identify project + task-group.
  2. Collect metadata (NN, name, type-specific extras, _meta block).
  3. Create skeleton (.py, configs/, runs/, results/, notebooks/).
  4. Seed config from `ref/config-seed.yaml`.
  5. Copy run-script from `../../haipipe-task/ref/run-sh-template.sh`.
  6. Suggest materializing the verified aggregate into a Display Intake.
  7. Emit return contract.


Return contract
---------------

```
status:    ok | blocked | failed
summary:   2-3 sentences on what was scaffolded
artifacts: [paths created]
next:      suggested next command (usually bash runs/<run>.sh)
```



Workflow plan
--------------

When `/haipipe-task plan` targets an existing task-folder of this type, the generated plan-script YAML should follow the type-specific sample:

```
ref/workflow-plan-sample.yaml     ← script-level phases for this type
../../haipipe-task/ref/workflow-template.yaml  ← task-level template (Run/Gate1/Gate2)
```

Schema source of truth:
  task/haipipe-workflow/ref/plan-schema.md
