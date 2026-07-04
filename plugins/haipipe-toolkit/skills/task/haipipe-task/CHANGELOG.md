haipipe-task — Changelog
========================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match SKILL.md frontmatter `version:`. Newest first.


## [5.0.0] — 2026-06-11

- remove Stage 5 (Insight) from task lifecycle — insight is /haipipe-insight's responsibility, not task's. This skill is now a pure 4-stage code lifecycle (Plan/Build/Execute/Report). Task-group iteration updated accordingly.

## [4.1.0] — 2026-06-11

- task-group iteration — when given a task-group path, enumerate child task-folders and run lifecycle on each one sequentially (Step 3d). Removed project/task-group redirects to /haipipe-project; this skill now owns both task-folder and task-group scope.

## [4.0.0] — 2026-06-11

- 5-stage lifecycle — add Stage 5 (Insight), optional, files D_data observation card via /haipipe-insight-data for insight-worthy types. Code lifecycle (1-4) + data lifecycle (5).

## [3.0.0] — 2026-06-09

- 4-stage lifecycle (Plan/Build/Execute/Report) via task-lifecycle.workflow.js; creator-reviewer agent loop at each stage; all plans follow haipipe-workflow IPO schema; type-specific workflow-plan-sample.yaml in every specialist; project/task-group scope moved to haipipe-project.

## [2.1.0] — 2026-06-08

- three-layer plans; per-script IPO; Stata four-sister; wire reviewer+auditor agents.

## [2.0.0] — 2026-06-08

- add workflow lifecycle — audit, plan, report. New fn/ procedures. New ref: workflow-template.yaml.

## [1.0.0] — 2026-05-31

- baseline metadata added.

## [4.2.0] — 2026-07-03

- received fn/task-group.md + fn/scan-status.md (+ ref/scan_status scripts) from haipipe-project (project skill reduced to setup-only). haipipe-workflow also moved into task/.

## [4.3.0] — 2026-07-03

- received ref/task-structure.md from project/haipipe-project/ref/project-structure.md (ownership refactor: project owns only the top-level container). Carries group folders, task naming, task-folder contents, skill-runner exemption, group/task diagram contracts, run script templates, runs/results/notebooks/sbatch relationship, auto-example rule; rules already in ref/authoring-conventions.md stay there and are only pointed to.
