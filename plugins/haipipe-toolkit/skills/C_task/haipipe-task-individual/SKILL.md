---
name: haipipe-task-individual
description: "individual-query task-folder build specialist. Scaffolds {NN}_<name>/ task-folders under E-series task-groups that query / visualize ONE subject's data (CGM trace, meal timeline, treatment events) — outputs to results/<run>/{plot.pdf, table.csv}. Called by /haipipe-task orchestrator when task-type=individual. Cross-references /haipipe-subject."
argument-hint: [project_id] [group] [task-name]
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
---

Skill: haipipe-task-individual
=======================================

Scaffolds a **subject-centric query task-folder**. Pulls one
patient's Source / Record data, applies a view (timeline,
treatment-event plot, meal-vs-glucose overlay), and writes a small
PDF + CSV to `results/<run>/`.


Position in the series
----------------------

```
/haipipe-task-data            data-pipeline
/haipipe-task-algo            algo-dev demo
/haipipe-task-training        model training
/haipipe-task-eval            model evaluation
/haipipe-task-display         paper figure / table
/haipipe-task-individual  ◀── you are here (subject query)
/haipipe-task-agent           LLM agent call
```


What this scaffolds
-------------------

```
tasks/E{NN}_<group_name>/                    ← E-series group (individual)
└── {NN}_<task_name>/
    ├── {NN}_<task_name>.py
    ├── configs/
    │   └── subject_<view>.yaml              seeded from ref/config-seed.yaml
    ├── runs/
    │   └── subject_<view>.sh
    ├── results/
    │   └── <run>/                           plot.pdf, table.csv
    └── notebooks/
```

Group letter default: **E** (individual).
Heavy outputs: none.


Cross-reference to pipeline skill
----------------------------------

`/haipipe-subject` owns per-subject data access (Subject-* folders
under `_WorkSpace/A-User-Store/`). This skill scaffolds the example
view; the view logic typically calls `/haipipe-subject` helpers.


Scaffold flow
-------------

See `fn/scaffold.md` for the detailed step-by-step. Summary:

  1. Identify project + task-group.
  2. Collect metadata (NN, name, type-specific extras, _meta block).
  3. Create skeleton (.py, configs/, runs/, results/, notebooks/).
  4. Seed config from `ref/config-seed.yaml`.
  5. Copy run-script from `../haipipe-task/ref/run-sh-template.sh`.
  6. Suggest next via cross-skill link.
  7. Emit return contract.


Return contract
---------------

```
status:    ok | blocked | failed
summary:   2-3 sentences on what was scaffolded
artifacts: [paths created]
next:      suggested next command (run.sh / /haipipe-subject)
```
