project — Changelog
=====================

Layer-scoped changelog for the project (project umbrella) layer. Newest first.
Rollup lives in the plugin-level `CHANGELOG.md`.


## [Unreleased] - 2026-07-03

### Changed
- **`ref/project-structure.md` rewritten to the ownership principle** (583 -> ~115 lines). It now carries ONLY the top-level container: ProjX-*/Project-* naming, the standard layout (adds `discoveries/`; `papers/` plural for new scaffolds, legacy ProjA-D keep singular `paper/`), the seven-worlds table + one-way dependency map, the project-level `diagram/` contract, the `_WorkSpace` note, and a Structure Ownership pointer table.
- **tasks/ internals moved** to `task/haipipe-task/ref/task-structure.md`: group folders, task naming, task-folder contents, skill-runner exemption, group/task `diagram/` contracts, run script templates, the runs/results/notebooks/sbatch relationship, and the auto-example rule. Rules already covered by `task/haipipe-task/ref/authoring-conventions.md` (four-sister naming §1, heavy-artifact rule §3, notebook retention/commit policy §7) stay there as authority; task-structure.md only points at them.
- **Review Checklist archived** to `project/_archive/review-checklist.md` (it belonged to the retired review fn; originals in `_archive/haipipe-project-inspect/`).
- **probes/ / insights/ / applications/ / paper internals dropped** from project-structure.md; the ownership table points to each world's schema authority (probe-yaml-schema.md, insight-md-schema.md, application ref/, paper wiki + haipipe-paper-folder, discovery SKILL.md folder contract).


## [Unreleased] — 2026-05-31

### Changed
- **`ref/project-structure.md` notebooks/ rules** aligned with the new task notebook policy:
  - documented the `_meta.notebook: full | thin | off` retention knob (run.sh applies it; cross-ref to `task/haipipe-task/ref/authoring-conventions.md §7`);
  - commit policy now **defaults to gitignoring `notebooks/` and `_WorkSpace/`** (N×seeds×arms recorded notebooks bloat the repo); commit a rendered notebook only when collaborators benefit. The project scaffold should seed `.gitignore` with `notebooks/` and `_WorkSpace/`.
