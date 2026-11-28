---
title: 'Design Job Main: Overview, Tasks, Findings'
date: 2026-11-27 09:21
topic: s11-design-job-preview
aim: 'Align execution Job Main with Work: one Brief fold under Overview, actual Task folds under Tasks, and recorded outputs under Findings, preserving human approval and original Run identities.'
closed: false
plan:
- do: add
  path: examples/Project-Ladder/blueprint/b12_theme_design/trace/261127/0921_design_job_main_bands.md
  what: this trace's own record, written first
- do: edit
  path: plugins/haipipe-toolkit/servers/workbench-design/design_jobs.py
  what: Use Overview Tasks Findings bands and contextual approval
- do: edit
  path: plugins/haipipe-toolkit/servers/workbench-design/tests/test_design_jobs.py
  what: Guard bands Task folds outputs and approval
- do: edit
  path: plugins/haipipe-toolkit/skills/3_theme/design/workbench-design/SKILL.md
  what: Document aligned Main and original Task Runs
- do: add
  path: plugins/haipipe-toolkit/skills/3_theme/design/workbench-design/CONSTITUTION.md
  what: Keep the shared Job Main rule and guard
- do: edit
  path: plugins/haipipe-toolkit/skills/3_theme/design/workbench-design/ref/topics.md
  what: Record feedback cause validation and remaining work
- do: edit
  path: examples/Project-Ladder/blueprint/b12_theme_design/delivery/page-spec/job-views.md
  what: Align embedded Main bands folds and sources
- do: edit
  path: examples/Project-Ladder/blueprint/b12_theme_design/delivery/page-spec/structure.md
  what: Describe shared Job Main organization
- do: edit
  path: examples/Project-Ladder/blueprint/b12_theme_design/delivery/page-spec/view-guide.json
  what: Align embedded Main guidance with current implementation
- do: edit
  path: examples/Project-Ladder/blueprint/b12_theme_design/s11-design-job-preview/s11-design-job-preview.md
  what: Record Main layout decision and live acceptance
- do: edit
  path: examples/Project-Ladder/blueprint/b12_theme_design/s11-design-job-preview/s11-design-job-preview.html
  what: Add live Overview Tasks Findings preview marks
changed:
- examples/Project-Ladder/blueprint/b12_theme_design/trace/261127/0921_design_job_main_bands.md
---

# Design Job Main: Overview, Tasks, Findings

## Prompts

- **exact message time unavailable** 你的这个Job的界面要有几个fold呀？现在的fold有点太多了，我感觉。然后fold里面下面有几个banner呢，就是有几个banner呢。
- **exact message time unavailable** 你说的这个Jobman，我觉得应该是放一个task吧。你看看别人的那个Job怎么设计的。别人的job它有，对吧？但我觉得，对，你看看Inside和Work是怎么设计的，Jobman是怎么设计的，Result，肯定我觉得Job写肯定有task，它一般是Overview、Task和Finding，Finding Result。
- **exact message time unavailable** ok go ahead and update according . Could you make the plan and use trace?

## Check

## Summary

## Plan details

- Overview: one Brief fold with top views for Goal, Method and Inputs/requirements; retain setup context without a separate Workflow fold.
- Tasks: one fold per actual Task, with recorded Run information and an in-place Task selection control. Do not invent method-step Tasks or copy Task records.
- Findings: show designs, evaluation and reports/delivery only when backed by existing records. Keep the existing human attestation and release gate beside the applicable output. Avoid standalone Ranking, Workflow and Runs folds on Main.
- Use the existing shared band/fold/top-view components; preserve the Block title and use Block-owned selection links.
- This episode changes the Board execution Job Main. The method-type Job contract and selected Task step bodies remain outside the layout rewrite.
- Validate representative ready, empty and released records, read-only rendering, Task navigation and approval controls; inspect the running example through Tailscale and return inline screenshots.
- Existing unrelated staged and working-tree changes are preserved. The earlier AGENTS.md preference proposal is a separate pending change, not silently included here.

## Approval

The user authorized the layout direction and requested this Trace. The concrete file list is now prepared for confirmation under AGENTS.md and hai-trace A01/A04; implementation has not started. The filename records plan creation time because exact earlier message timestamps are unavailable.
