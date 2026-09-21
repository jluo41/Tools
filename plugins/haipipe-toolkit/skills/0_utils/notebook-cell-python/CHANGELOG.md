notebook-cell-python — Changelog
================================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match SKILL.md frontmatter `version:`. Newest first.


## [0.3.0] — 2026-09-20

- Return failing exit codes for missing input and partial batch conversion.
- Add run_notebook.py: unique preserved attempts, per-step logs, execution receipts, and failure/interruption outcomes.
- Keep helper execution distinct from caller-owned Run identity; execute source once before conversion.
- Resolve installed tools separately from the target project and optional interpreter.
- Supply stable notebook cell IDs and remove an unverified Python version claim.

## [0.2.0] — 2026-09-20

- Point conversion and diagram references to files shipped in this checkout.
- Replace the missing cleaner with the documented nbconvert output-clearing
  command, and distinguish one Run from its conversion/execution Steps.


## [0.1.0] — 2026-07-24

Renumbered under the 0.x policy — the whole haipipe-toolkit is pre-1.0 until JL says otherwise (was 1.0.0; older entries below keep their original numbers).

## [1.0.0] — 2026-05-31

- baseline metadata added.
