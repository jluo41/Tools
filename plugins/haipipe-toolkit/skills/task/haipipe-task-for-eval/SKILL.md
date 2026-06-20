---
name: haipipe-task-for-eval
description: "evaluation task-folder build specialist. Scaffolds {NN}_<name>/ task-folders under B-series task-groups that score a trained model against an AIData split — metrics land in results/<run>/metrics.json. Called by /haipipe-task orchestrator when task-type=eval. Cross-references /haipipe-end or future eval skill."
argument-hint: "[project_id] [group] [task-name]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "1.1.0"
  last_updated: "2026-06-09"
  summary: "evaluation task-folder build specialist."
  changelog:
    - "1.1.0 (2026-06-09): unwrap prose; fix agent names; add 4-stage lifecycle paragraph."
    - "1.0.0 (2026-05-31): baseline metadata added."
---

Skill: haipipe-task-for-eval
=================================

Scaffolds an **evaluation task-folder**. Consumes a trained ModelInstance + an AIData split; produces metrics + diagnostic plots under `results/<run>/`.

**Invocation modes:** interactive (human steers; missing fields get ASKed) OR headless (`haipipe-task-creator-agent` calls this skill during Stage 2: Build, then authors the `<TASK>.py` body). Always end with the structured return block (status / task_folder / run_name / files).



What this scaffolds
-------------------

```
tasks/B{NN}_<group_name>/                    ← B-series group (evaluation)
└── {NN}_<task_name>/
    ├── {NN}_<task_name>.py
    ├── configs/
    │   └── eval_<target>.yaml               seeded from ref/config-seed.yaml
    ├── runs/
    │   └── eval_<target>.sh
    ├── results/
    │   └── <run>/                           metrics.json, plots/, source_data.csv
    └── notebooks/
```

Group letter default: **B** (evaluation).
Heavy outputs: none — `results/<run>/` is all light artifacts.


Cross-reference to pipeline skill
----------------------------------

Currently no dedicated `/haipipe-eval` skill. Evaluation logic typically calls into `/haipipe-end` (Stage 6 inference + scoring) or a project-local eval script. This may grow into its own skill; for now, the eval code is project-owned.


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
next:      suggested next command (run.sh / next eval target)
```



Workflow plan
--------------

When `/haipipe-task plan` targets an existing task-folder of this type,
the generated plan-script YAML should follow the type-specific sample:

```
ref/workflow-plan-sample.yaml     ← script-level phases for this type
../haipipe-task/ref/workflow-template.yaml  ← task-level template (Run/Gate1/Gate2)
```

Schema source of truth:
  project/haipipe-workflow/ref/plan-schema.md
