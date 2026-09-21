---
name: haipipe-task-for-eval
description: "evaluation job specialist: scaffolds {NN}_<name>/ jobs in the eval block (default B-series) that score a trained model against an AIData split -> $OUTPUT_ROOT/<task>/results/rNN_<run>/metrics.json. Called by /haipipe-task when task-type=eval. Cross-references /haipipe-end or a future eval skill."
argument-hint: "[project_id] [group] [job-name]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "0.1.2"
  last_updated: "2026-07-04"
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

Skill: haipipe-task-for-eval
=================================

Scaffolds an **evaluation job**.
Consumes a trained ModelInstance + an AIData split; produces metrics + optional diagnostic plots under `$OUTPUT_ROOT/<task>/results/rNN_<run>/`.

**Invocation modes:** interactive (human steers; missing fields get ASKed) OR headless (`haipipe-task-creator-agent` calls this skill during Phase 2: Build, then authors the `<TASK>.py` body).
Always end with the structured return block (status / task_folder / run_name / files).



What this scaffolds
-------------------

```text
tasks/bNN_<block>/
├── board.md
└── jNN_<job>/
    ├── src/                         shared code + config-defaults.yaml
    └── tNN_<task>/
        ├── tNN_<task>.md
        ├── outline/
        ├── workflow/                plan.yaml + report.yaml
        ├── scripts/<worker>.py
        ├── scripts/config/rNN_<run>.yaml
        └── runs/rNN_<run>.sh

Generated: $OUTPUT_ROOT/tNN_<task>/results/rNN_<run>/
           $OUTPUT_ROOT/tNN_<task>/notebooks/rNN_<run>.ipynb
```

Hierarchy prefixes are bNN / jNN / tNN / rNN; domain belongs in the descriptive suffix.
Heavy outputs: none — `$OUTPUT_ROOT/<task>/results/rNN_<run>/` is all light artifacts.


Cross-reference to pipeline skill
----------------------------------

Currently no dedicated `/haipipe-eval` skill.
Evaluation logic typically calls into `/haipipe-end` (Stage 6 inference + scoring) or a project-local eval script.
This may grow into its own skill; for now, the eval code is project-owned.


Scaffold flow
-------------

See `fn/scaffold.md` for the detailed step-by-step.
Summary:

  1. Identify project + block.
  2. Collect metadata (NN, name, type-specific extras, _meta block).
  3. Create the canonical Task Page, workflow/, scripts/config/, worker and matching rNN Ticket; resolve generated output through OUTPUT_ROOT.
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
next:      suggested next command (run.sh / next eval target)
```



Workflow plan
--------------

When `/haipipe-task plan` targets an existing job of this type, the generated plan-script YAML should follow the type-specific sample:

```
ref/workflow-plan-sample.yaml     ← Run Spec example with internal domain steps
../../haipipe-task/ref/workflow-template.yaml  ← authoritative Run Spec template with entry/exit gates
```

Schema source of truth:
  task/haipipe-workflow/ref/plan-schema.md

Resolve `RESULT_STORE`, then the Job store declaration, then the Job root as OUTPUT_ROOT.
Use the same output-root contract as `haipipe-task`; no physical output is moved by scaffolding.
