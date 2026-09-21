meal-cam-logger — Changelog
===========================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match SKILL.md frontmatter `version:`. Newest first.


## [0.3.0] — 2026-09-20

- Label first-bite vision results as inferred visible-food candidates; distinguish no-food-visible, uncertainty, and service errors.
- Record model, rubric, timestamp, and in-memory frame hash without saving the image.
- Add append-only, attributed correction sidecars that retain prior labels.

## [0.2.1] — 2026-09-20

- Resolve the loaded skill and selected interpreter independently of the target project.
- Restore per-session controls with PID, process start time, and script identity checks.
- Stop paused sessions with TERM followed by CONT and report delayed shutdown honestly.
- Clarify elapsed duration and possible camera-backend diagnostics.

## [0.2.0] — 2026-09-20

- Aligned the skill instructions with the current MediaPipe bite and episode
  detector, its `--fps` CLI, and first-bite-only Anthropic vision calls.
- Added a unique per-Run receipt created at startup and finalized with the
  Run ID, graceful stop time, duration, and status, including sessions with no
  bites.
- Added a SIGUSR1 control to remove the most recent episode during a session;
  documented process and privacy limits. Removed an unused retained frame
  buffer and added local environment configuration for camera sources.


## [0.1.0] — 2026-07-24

Renumbered under the 0.x policy — the whole haipipe-toolkit is pre-1.0 until JL says otherwise (was 1.0.0; older entries below keep their original numbers).

## [1.0.0] — 2026-05-31

- baseline metadata added.
