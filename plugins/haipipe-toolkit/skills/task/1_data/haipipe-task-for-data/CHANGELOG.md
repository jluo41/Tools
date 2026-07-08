haipipe-task-for-data — Changelog
=================================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match SKILL.md frontmatter `version:`. Newest first.


## [2.3.0] — 2026-07-08

- skill-diagnose fixes: dead `python -m scripts.haistep.*` invocations -> `scripts.haistepcli.*` (SKILL Path B block, execute-flow summary, fn/execute.md; the old module path raises ModuleNotFoundError — note pyproject's haistep-* console entry points carry the same rot upstream); CHANGELOG reordered newest-first.

## [2.2.0] — 2026-07-04

- ref/config-seed.yaml hub ref was 4-up (dangling) -> 3-up; scaffold Steps 4-5 artifact naming aligned to the Step-3 tree + SKILL.md (configs/run_<task_name>.yaml); notebook-templates group map a1/a2/a3/a4 (was aa/ab/ac/ad).

## [2.1.0] — 2026-07-04

- review sweep: plan-sample schema header task/haipipe-workflow; reviewer name haipipe-task-reviewer-agent; fn/ref relative hub paths ../../../haipipe-task; group letter D now a project-specific default.

## [2.0.0] — 2026-06-11

- add execute path, notebook template pattern, multi-partition support.

## [1.1.0] — 2026-06-09

- unwrap prose; fix agent names; add 4-stage lifecycle paragraph.

## [1.0.0] — 2026-05-31

- baseline metadata added.
