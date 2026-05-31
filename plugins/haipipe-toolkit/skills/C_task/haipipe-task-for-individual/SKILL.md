---
name: haipipe-task-for-individual
description: "individual-query task-folder build specialist. Scaffolds {NN}_<name>/ task-folders under E-series task-groups that query / visualize ONE individual's data (CGM trace, meal timeline, treatment events) — outputs to results/<run>/{plot.pdf, table.csv}. Called by /haipipe-task orchestrator when task-type=individual. Cross-references /haipipe-individual."
argument-hint: "[project_id] [group] [task-name]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
---

Skill: haipipe-task-for-individual
=======================================

Scaffolds a **individual-centric query task-folder**. Pulls one
patient's Source / Record data, applies a view (timeline,
treatment-event plot, meal-vs-glucose overlay), and writes a small
PDF + CSV to `results/<run>/`.


Position in the series
----------------------

```
/haipipe-task-for-data            data-pipeline
/haipipe-task-for-algo            algo-dev demo
/haipipe-task-for-training        model training
/haipipe-task-for-eval            model evaluation
/haipipe-task-for-display         paper figure / table
/haipipe-task-for-individual  ◀── you are here (individual query)
/haipipe-task-for-agent           LLM agent call
```


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

`/haipipe-individual` owns per-individual data access (Subject-* folders
under `_WorkSpace/A-User-Store/`). This skill scaffolds the example
view; the view logic typically calls `/haipipe-individual` helpers.


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
next:      suggested next command (run.sh / /haipipe-individual)
```
