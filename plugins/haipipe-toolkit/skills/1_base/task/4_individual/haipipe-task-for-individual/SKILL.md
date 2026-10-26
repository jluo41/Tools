---
name: haipipe-task-for-individual
description: "individual-query Task specialist: scaffolds jNN_<job>/tNN_<task>/ Task folders in the individual Block that query/visualize ONE individual's data (CGM trace, meal timeline, treatment events) -> $OUTPUT_ROOT/<task>/runs/rNN_<run>/result/{plot.pdf, table.csv}. Called by /haipipe-task when task-type=individual. Cross-references /haipipe-individual."
argument-hint: "[project_id] [bNN_<block>/jNN_<job>] [tNN_<task>]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
disable-model-invocation: true
metadata:
  version: "0.2.1"
  last_updated: "2026-10-26"
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

Skill: haipipe-task-for-individual
=======================================

Scaffolds an **individual-centric query job**.
Pulls one individual's Source / Record data, applies a view (timeline, treatment-event plot, meal-vs-glucose overlay), and writes a small PDF + CSV to `$OUTPUT_ROOT/<task>/runs/rNN_<run>/result/`.

**Invocation modes:** interactive (human steers; missing fields get ASKed) OR headless (`haipipe-task-creator-agent` calls this skill during Phase 2: Build, then authors the `<TASK>.py` body).
Always end with the structured return block (status / summary / artifacts / next — the same tail every task skill emits).

## Type contract

```yaml
task-type: individual
skill: haipipe-task-for-individual
does: Queries one subject's Source, Record or Case data over a time window and draws one view of it (timeline, meal overlay, treatment events).
worker: scripts/<worker>.py (Python), calling /haipipe-individual helpers; subject_id comes from the Run's config, never the code
config: runs/<run>/config.yaml (seeded from ref/config-seed.yaml), or scripts/config/<run>.yaml in a Block not yet moved
ticket: runs/<run>/<run>.sh, from ../../haipipe-task/ref/run-sh-template.sh (REQUIRED_RESULTS plot.pdf, plus table.csv when the view exports it)
result: $OUTPUT_ROOT/<task>/runs/<run>/result/, with runtime.yaml and plot.pdf (and table.csv when exported) before the receipt says complete; no metrics.json
heavy: none
roles: [make]
companions: [haipipe-individual, haipipe-individual-inference]
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
            ├── run.yaml                 its card (role: make)
            └── result/                  runtime.yaml (the receipt) + plot.pdf, table.csv

Generated: $OUTPUT_ROOT/tNN_<task>/runs/rNN_<run>/result/
           $OUTPUT_ROOT/tNN_<task>/notebooks/rNN_<run>.ipynb
A Block not yet moved still has the flat runs/rNN_<run>.sh, scripts/config/rNN_<run>.yaml
and results/rNN_<run>/; the ticket template runs both.
```

Hierarchy prefixes are bNN / jNN / tNN / rNN; domain belongs in the descriptive suffix.
Heavy outputs: none.


Cross-reference to pipeline skill
----------------------------------

`/haipipe-individual` owns per-individual data access (Subject-* folders under `_WorkSpace/A-User-Store/`).
This skill scaffolds the example view; the view logic typically calls `/haipipe-individual` helpers.


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
next:      suggested next command (run.sh / /haipipe-individual)
```



Workflow plan
--------------

When `/haipipe-task plan` targets an existing job of this type, the generated plan-script YAML should follow the type-specific sample:

```
ref/workflow-plan-sample.yaml     ← Run Spec example with internal domain steps
../../haipipe-task/ref/workflow-template.yaml  ← authoritative Run Spec template with entry/exit gates
```

Schema source of truth:
  ../../../project/haipipe-run/ref/plan-schema.md

Resolve `RESULT_STORE`, then the Job store declaration, then the Job root as OUTPUT_ROOT.
Use the same output-root contract as `haipipe-task`; no physical output is moved by scaffolding.
