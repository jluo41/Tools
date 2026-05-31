---
name: haipipe-task-for-display
description: "display task-folder build specialist. Scaffolds {NN}_<name>/ task-folders under C-series task-groups that produce paper figures and tables — outputs to results/<run>/{*.pdf, *.png, *.tex, source_data.csv}. Called by /haipipe-task orchestrator when task-type=display."
argument-hint: "[project_id] [group] [task-name]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
---

Skill: haipipe-task-for-display
====================================

Scaffolds a **display task-folder** — paper figures or paper tables.
Consumes `results/<run>/` artifacts from upstream eval / training
tasks; produces publication-ready PDF / PNG / TeX.


Position in the series
----------------------

```
/haipipe-task-for-data            data-pipeline
/haipipe-task-for-algo            algo-dev demo
/haipipe-task-for-training        model training
/haipipe-task-for-eval            model evaluation
/haipipe-task-for-display     ◀── you are here (figure / table)
/haipipe-task-for-individual      individual-centric query
/haipipe-task-for-agent           LLM agent call
```


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
    │   └── <run>/                           *.pdf, *.png, *.tex, source_data.csv
    └── notebooks/
```

Group letter default: **C** (display).
Heavy outputs: none.


Cross-reference to pipeline skill
----------------------------------

No corresponding pipeline skill — display tasks are independent;
they read from upstream `results/<run>/` and write final artifacts.
Useful adjacent skills: `/paper-figure`, `/paper-illustration`.


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
next:      suggested next command (run.sh / /paper-figure)
```
