haipipe-job · Changelog
=======================

## [0.1.0] · 2026-10-07 · New: the Job level (b03 s21)

- New skill (JL 261007: "haipipe-board, and haipipe-job, and also haipipe-studio and
  haipipe-report, and haipipe-run"). It owns the Job's face, its Tasks in order and its level
  of the frame; haipipe-task is unchanged and still builds each Task.
- `ref/job-contract.md`: the face (title, goal, close, answers:, Topic, `## Tasks`), the six
  Spaces at Job level and the buttons it owns, a theme's own Job and Task names
  (Theme.level_patterns).
- `scripts/new_job.py`: `job` (the scaffold), `task` (the next Task slot, listed in order),
  `check` (the list against the folders).
