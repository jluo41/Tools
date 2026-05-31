B_project — Changelog
=====================

Layer-scoped changelog for the B_project (project umbrella) layer. Newest first.
Rollup lives in the plugin-level `CHANGELOG.md`.


## [Unreleased] — 2026-05-31

### Changed
- **`ref/project-structure.md` notebooks/ rules** aligned with the new C_task
  notebook policy:
  - documented the `_meta.notebook: full | thin | off` retention knob (run.sh
    applies it; cross-ref to `C_task/haipipe-task/ref/authoring-conventions.md §7`);
  - commit policy now **defaults to gitignoring `notebooks/` and `_WorkSpace/`**
    (N×seeds×arms recorded notebooks bloat the repo); commit a rendered notebook
    only when collaborators benefit. The project scaffold should seed
    `.gitignore` with `notebooks/` and `_WorkSpace/`.
