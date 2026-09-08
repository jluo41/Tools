# Changelog

## 1.0.0 — 2026-09-08

- Establish one executable hierarchy: Project → Block → Job → Task Folder → Run.
- Define Task Folder = Page Folder at `tNN_<task>/`.
- Define Block = Task Board, Job = Board Group, and Task Folder = Board Page.
- Require the `bNN/jNN/tNN/rNN` name grammar and structural validation.
- Place Task-owned code in `scripts/`, Run config in `scripts/config/`, and
  Tickets in `runs/`.
- Place generated Results and notebooks under the parent Job's resolved
  `$OUTPUT_ROOT` with the exact `<task>/<run>` suffix.
- Make lifecycle execution accept only `task_folder` and reject malformed
  containers.
- Rename the Block scaffolding contract to `fn/block.md`.
- Add a repository gate that rejects non-v1 vocabulary and paths within this
  Skill package.
