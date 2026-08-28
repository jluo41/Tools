---
name: haipipe-task-for-individual
description: "individual-query task-folder specialist: scaffolds {NN}_<name>/ task-folders in the individual task-group (default E-series) that query/visualize ONE individual's data (CGM trace, meal timeline, treatment events) -> results/<run>/{plot.pdf, table.csv}. Called by /haipipe-task when task-type=individual. Cross-references /haipipe-individual."
argument-hint: "[project_id] [group] [task-name]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "0.1.2"
  last_updated: "2026-07-04"
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

Skill: haipipe-task-for-individual
=======================================

Scaffolds an **individual-centric query task-folder**.
Pulls one individual's Source / Record data, applies a view (timeline, treatment-event plot, meal-vs-glucose overlay), and writes a small PDF + CSV to `results/<run>/`.

**Invocation modes:** interactive (human steers; missing fields get ASKed) OR headless (`haipipe-task-creator-agent` calls this skill during Phase 2: Build, then authors the `<TASK>.py` body).
Always end with the structured return block (status / task_folder / run_name / files).



What this scaffolds
-------------------

```
tasks/E{NN}_<group_name>/                    ← E-series group (individual)
└── {NN}_<task_name>/
    ├── {NN}_<task_name>.py
    ├── configs/
    │   └── individual_<view>.yaml              seeded from ref/config-seed.yaml
    ├── runs/
    │   └── individual_<view>.sh
    ├── results/
    │   └── <run>/                           plot.pdf, table.csv
    └── notebooks/
```

Group letter default: **E** (individual).
Heavy outputs: none.


Cross-reference to pipeline skill
----------------------------------

`/haipipe-individual` owns per-individual data access (Subject-* folders under `_WorkSpace/A-User-Store/`).
This skill scaffolds the example view; the view logic typically calls `/haipipe-individual` helpers.


Scaffold flow
-------------

See `fn/scaffold.md` for the detailed step-by-step.
Summary:

  1. Identify project + task-group.
  2. Collect metadata (NN, name, type-specific extras, _meta block).
  3. Create skeleton (.py, configs/, runs/, results/, notebooks/).
  4. Seed config from `ref/config-seed.yaml`.
  5. Copy run-script from `../../haipipe-task/ref/run-sh-template.sh`.
  6. Suggest next via cross-skill link.
  7. Emit return contract.


Return contract
---------------

```
status:    ok | blocked | failed
summary:   2-3 sentences on what was scaffolded
artifacts: [paths created]
next:      suggested next command (run.sh / /haipipe-individual)
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
