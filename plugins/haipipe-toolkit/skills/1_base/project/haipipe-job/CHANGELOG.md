haipipe-job · Changelog
=======================

## [0.2.1] · 2026-10-09 · Theme folders are singular

- Docs name the singular Theme folders (s01-D29, JL 261007): `work/`, `discovery/`, `paper/`, `insight/`,
  `design/`, `labeling/`, `ideation/`; the older plural names still read.

## [0.2.0] · 2026-10-09 · Face for an existing Job or Task

- `scripts/new_job.py face <job|task>`: writes the face of an existing folder that has none, from disk
  (goal and close left open; a Job lists its Tasks with their titles; a Task lists its Runs).

## [0.1.0] · 2026-10-07 · New: the Job level (b03 s21)

- New skill (JL 261007: "haipipe-board, and haipipe-job, and also haipipe-studio and
  haipipe-report, and haipipe-run"). It owns the Job's face, its Tasks in order and its level
  of the frame; haipipe-task is unchanged and still builds each Task.
- `ref/job-contract.md`: the face (title, goal, close, answers:, Topic, `## Tasks`), the six
  Spaces at Job level and the buttons it owns, a theme's own Job and Task names
  (Theme.level_patterns).
- `scripts/new_job.py`: `job` (the scaffold), `task` (the next Task slot, listed in order),
  `check` (the list against the folders).
