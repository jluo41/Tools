---
name: haipipe-task-for-eval
description: "evaluation Task specialist: scaffolds jNN_<job>/tNN_<task>/ Task folders in the eval Block that score a trained model against an AIData split -> $OUTPUT_ROOT/<task>/runs/rNN_<run>/result/metrics.json. Called by /haipipe-task when task-type=eval. Cross-references /haipipe-end or a future eval skill."
argument-hint: "[project_id] [bNN_<block>/jNN_<job>] [tNN_<task>]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "0.2.0"
  last_updated: "2026-10-21"
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

Skill: haipipe-task-for-eval
=================================

Scaffolds an **evaluation job**.
Consumes a trained ModelInstance + an AIData split; produces metrics + optional diagnostic plots under `$OUTPUT_ROOT/<task>/runs/rNN_<run>/result/`.

**Invocation modes:** interactive (human steers; missing fields get ASKed) OR headless (`haipipe-task-creator-agent` calls this skill during Phase 2: Build, then authors the `<TASK>.py` body).
Always end with the structured return block (status / task_folder / run_name / files).

## Type contract

```yaml
task-type: eval
skill: haipipe-task-for-eval
does: Scores one pinned ModelInstance on one AIData split (val, test_id or test_od) and writes its metrics.
worker: scripts/<worker>.py (Python), project-owned eval code that may call /haipipe-end inference and scoring helpers
config: runs/<run>/config.yaml (seeded from ref/config-seed.yaml), or scripts/config/<run>.yaml in a Block not yet moved
ticket: runs/<run>/<run>.sh, from ../../haipipe-task/ref/run-sh-template.sh (REQUIRED_RESULTS metrics.json, the template default)
result: $OUTPUT_ROOT/<task>/runs/<run>/result/, with runtime.yaml and metrics.json before the receipt says complete; per-case predictions, diagnostic plots or policy_comparison.md when asked
heavy: none
roles: [make, check]
companions: [haipipe-end, haipipe-task-for-display]
plan_sample: ref/workflow-plan-sample.yaml
```


What this scaffolds
-------------------

```text
work/bNN_<block>/
├── board.md
└── jNN_<job>/
    ├── src/                         shared code + config-defaults.yaml
    └── tNN_<task>/
        ├── tNN_<task>.md
        ├── draft/
        ├── workflow/                plan.yaml + report.yaml
        ├── scripts/<worker>.py
        └── runs/rNN_<run>/              one folder per Run
            ├── rNN_<run>.sh             the ticket
            ├── config.yaml              this Run's settings
            ├── run.yaml                 its card (role: make | check)
            └── result/                  runtime.yaml (the receipt) + metrics.json

Generated: $OUTPUT_ROOT/tNN_<task>/runs/rNN_<run>/result/
           $OUTPUT_ROOT/tNN_<task>/notebooks/rNN_<run>.ipynb
A Block not yet moved still has the flat runs/rNN_<run>.sh, scripts/config/rNN_<run>.yaml
and results/rNN_<run>/; the ticket template runs both.
```

Hierarchy prefixes are bNN / jNN / tNN / rNN; domain belongs in the descriptive suffix.
Heavy outputs: none — `$OUTPUT_ROOT/<task>/runs/rNN_<run>/result/` is all light artifacts.


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
  3. Create the canonical Task Page, workflow/, worker and one Run folder runs/rNN_<run>/ (Ticket, config.yaml, run.yaml); resolve generated output through OUTPUT_ROOT.
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
  project/haipipe-run/ref/plan-schema.md

Resolve `RESULT_STORE`, then the Job store declaration, then the Job root as OUTPUT_ROOT.
Use the same output-root contract as `haipipe-task`; no physical output is moved by scaffolding.
