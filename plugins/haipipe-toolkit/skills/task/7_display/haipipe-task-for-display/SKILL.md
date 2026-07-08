---
name: haipipe-task-for-display
description: "display task-folder build specialist. Scaffolds {NN}_<name>/ task-folders in the project's display task-group (default C-series; letters are project-specific) that produce paper figures and tables — outputs to results/<run>/{*.pdf, *.png, *.tex, source_data.csv}. Called by /haipipe-task orchestrator when task-type=display."
argument-hint: "[project_id] [group] [task-name]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "1.2.0"
  last_updated: "2026-07-04"
  summary: "display task-folder build specialist."
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

Skill: haipipe-task-for-display
====================================

Scaffolds a **display task-folder** — paper figures or paper tables. Consumes `results/<run>/` artifacts from upstream eval / training tasks; produces publication-ready PDF / PNG / TeX.

**Invocation modes:** interactive (human steers; missing fields get ASKed) OR headless (`haipipe-task-creator-agent` calls this skill during Stage 2: Build, then authors the `<TASK>.py` body). Always end with the structured return block (status / task_folder / run_name / files).



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

No corresponding pipeline skill — display tasks are independent; they read from upstream `results/<run>/` and write final artifacts (paper-ready figures/tables). Which document consumes them is the caller's business; this skill names no upper-layer skill.


Scaffold flow
-------------

See `fn/scaffold.md` for the detailed step-by-step. Summary:

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
