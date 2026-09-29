notebook-cell-python — Changelog
================================

Skill-scoped changelog (never loaded at invocation; read on demand). Versions match SKILL.md frontmatter `version:`. Newest first.


## [0.4.4] - 2026-09-29 - Generated output and encoded ids (JL 260929)

- Rule 7: a notebook that changed because its .py changed and its Ticket reran is reported that way, never as an edit to the notebook.

## [0.4.3] - 2026-09-28 - Reader notebooks open on their title

- Rule 7: `convert_to_notebooks.py` leaves the module docstring out of a `# notebook: hide-code` notebook; the docstring is written for whoever edits the .py, and the reader saw it before the notebook's own title (JL 260928, the b51 external galleries).

## [0.4.2] - 2026-09-28 - No content hashes (JL 260928)

- AGENTS.md rule 9: `convert_to_notebooks.py` gives each cell the id `cell-NNN` from its position instead of a SHA-256 prefix; ids stay stable and unique, and nbformat validates them.

## [0.4.1] — 2026-09-27

- Rule 7: a `# notebook: hide-code` line after the docstring makes `convert_to_notebooks.py` mark every code cell hidden (`jupyter.source_hidden`) when it creates the notebook, so a reader-facing notebook shows outputs only without any post-run rewrite (JL 260927).

## [0.4.0] — 2026-09-27

- Rule 2: a section is a Markdown heading (`#` title, `##` section, `###` part) in its own markdown cell, so the notebook outline lists it; `─§` text markers are gone (JL 260927). Only a diagram or aligned text is fenced; prose is plain Markdown.
- Rule 2: sections are numbered in plain digits (`## 1. Step`), never circled digits (JL 260927).
- Rule 4: tables with `display()`, never `print(df.to_string())`; a plain `python` run falls back to text.
- `convert_to_notebooks.py`: the module docstring opens the notebook as a fenced `txt` markdown cell. As a code cell its output was the escaped string itself, so every notebook opened on a block of `\n` text.


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
