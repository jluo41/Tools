---
name: notebook-cell-python
description: >-
  Author Python scripts with notebook cell markers, execute them with preserved
  artifacts and receipts, and derive Jupyter notebooks from the Python source.
  Use when code must run as a script for review or CI and also be viewable as
  a notebook, or for .py to .ipynb conversion and Jupytext-style cells.
allowed-tools: Bash, Read, Write, Edit
metadata:
  version: "0.3.0"
  last_updated: "2026-09-20"
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

Skill: notebook-cell-python
===========================

Cell-based `.py` ↔ `.ipynb` workflow. The `.py` is the source of truth;
the `.ipynb` is auto-derived for browser viewing of code + outputs +
figures.

Used in any project where code must be runnable both as a script (PR
review, CI) and as a notebook (Jupyter, embedded figures). Most common
home: `examples/<project>/tasks/<task>/`.


---

When to Use
===========

Trigger this skill when:
  - The user asks for cell-based `.py` files that convert to `.ipynb`.
  - A project has `*.py` next to a `notebook/` folder of derived `.ipynb`.
  - You need to author a script someone will read both as `.py` (in
    diff/PR) and as `.ipynb` (with embedded outputs).

Skip when:
  - It's a one-off `python foo.py` — no notebook is needed.
  - The user wants `.ipynb` as source-of-truth (use Jupyter directly).


---

Tools in this checkout
====================================

The converter shipped with this skill is at
`plugins/haipipe-toolkit/skills/0_utils/notebook-cell-python/convert_to_notebooks.py`.
That is the source-checkout path. For installed use, resolve
`NOTEBOOK_SKILL_DIR` from this loaded SKILL.md and use its bundled files. Keep
that absolute tool location separate from the target project directory.
Notebook execution and output clearing use Jupyter nbconvert; this package does not include a separate
cleaning script. Conversion preserves cell text; it does not compile or execute
the source. Syntax errors are reported by the execution Step, not conversion.

  ┌──────────────┬──────────────────────────────────────────┬────────────────────────────────────────────────────┐
  │ Action       │ Command                                  │ What it does                                       │
  ├──────────────┼──────────────────────────────────────────┼────────────────────────────────────────────────────┤
  │ CREATE       │ Claude writes the .py file               │ Follow the Cell Rules + Skeleton below.            │
  │              │                                          │ (No scaffolder — the skill IS the spec.)           │
  │              │                                          │                                                    │
  │ CONVERT      │ python plugins/haipipe-toolkit/skills/   │ Cell-based .py → .ipynb (cells only, no outputs).  │
  │              │   0_utils/notebook-cell-python/          │                                                    │
  │              │   convert_to_notebooks.py <script>.py    │                                                    │
  │              │   -o <notebook>.ipynb                    │                                                    │
  │              │                                          │                                                    │
  │ EXECUTE      │ jupyter nbconvert --to notebook          │ Run each cell, embed outputs + figures inline.     │
  │              │   --execute --inplace <notebook>.ipynb   │ (Optional — skip if you want the notebook to       │
  │              │                                          │ stay code-only.)                                   │
  │              │                                          │                                                    │
  │ CLEAN        │ jupyter nbconvert --to notebook          │ Clear outputs in place (optional; requires         │
  │              │ --ClearOutputPreprocessor.enabled=True   │ nbconvert).                                        │
  │              │ --inplace <notebook>.ipynb                │                                                    │
  └──────────────┴──────────────────────────────────────────┴────────────────────────────────────────────────────┘

Canonical sequence per script:

```
   .py  ──►  python <script>.py                   ⇒ side-effect artifacts (csv/png)
        ──►  convert_to_notebooks.py              ⇒ .ipynb with cells, no outputs
        [──► jupyter nbconvert --execute         ] ⇒ optional: embed outputs in .ipynb
        ──►  open <notebook>.ipynb in browser
```


---

Cell Rules
==========

Cell markers:

```
  # %%                code cell
  # %% Section name   code cell with label
  # %% [markdown]     markdown cell (ASCII diagrams, headers)
```

Authoring rules:

  1. **Run from repo root.** Scripts assume `cwd = repo root` and use
     relative paths (`_WorkSpace/...`, `examples/...`). Invoked as
     `python <task-path>/<N>-<topic>.py` from the repo root.
  2. **ASCII-heavy markdown.** Diagrams not paragraphs. Box chars
     `┌─┐│└─┘`, section markers `─§ ① ──`. See cross-ref below.
  3. **Self-documenting.** Top docstring: one-line purpose, input,
     output. First `# %% [markdown]` cell: title block + mini pipeline.
  4. **No magic, no IPython.** Pure Python — must work as a `python`
     invocation, not just inside Jupyter.
  5. **Print progress markers.** `print('=' * 80)` between steps.
     Each cell ends with a one-line `✓` confirmation when done.
  6. **Side effects to disk.** CSVs/PNGs go to the explicit `RUN_DIR`
     provided by the caller/helper. For direct execution, choose a fresh
     output directory first; do not silently reuse a shared fallback.


---

ASCII Style for Markdown Cells
================================

```
Boxes:     ┌ ┐ └ ┘ │ ─
Arrows:    → ↓ ← ↑
Tree:      ├ └ │ ─
Double:    ═ ║ ╔ ╗ ╚ ╝
```

For ASCII diagrams in `# %% [markdown]` cells, follow the
`diagram-ascii` style at
`plugins/haipipe-toolkit/skills/0_utils/diagram-ascii/SKILL.md`: box
characters above and section markers like `─§ ① ──` for cell headers.
Emoji are optional; use them only when they improve scanability and keep
labels readable in plain-text and assistive-technology contexts.


---

Standard Skeleton (Claude follows this when writing .py files)
================================================================

```python
"""
N-topic.py — One-line purpose.

Input:  path/to/input
Output: $RUN_DIR (provided by run_notebook.py)
"""

# %% [markdown]
# ┌──────────────────────────────────────────────────────────────┐
# │   N-topic   ←→   short title                                 │
# └──────────────────────────────────────────────────────────────┘
#
#    input ──► step ──► step ──► output
#                                   │
#                                   ▼
#                             $RUN_DIR

# %% Setup
import os
from pathlib import Path
import pandas as pd
# ... other imports ...

OUT = Path(os.environ['RUN_DIR'])
OUT.mkdir(parents=True, exist_ok=True)

print('=' * 80)
print(f'Output: {OUT}')
print('=' * 80)

# %% [markdown]
# ─§ ① Step one ─────────────────────────────────────────────────

# %% Step one
result = ...
print(result.to_string())
result.to_csv(OUT / 'step_one.csv', index=False)

# %% [markdown]
# ─§ ② Step two ─────────────────────────────────────────────────

# %% Step two
# ...

# %% Done
print()
print(f'✓ Wrote: {OUT}')
```


---

Bash Wrapper Convention
========================

Each script may have a `run-N.sh` wrapper in the task's `runs/` folder.
The bundled `run_notebook.py` executes the source once and converts it without
executing the notebook a second time. Each invocation creates a unique
execution directory, including on the same day, and an `execution.json`
receipt with status, exit code, timestamps, logs, and output paths. Once preflight has accepted the input, failed
attempts remain on disk. Missing input or interpreter is rejected before an
execution directory is created. A fixed notebook path or `_LATEST` may be a separate
presentation pointer; it must not replace these saved attempts.

This helper is a Step inside the caller's Run. It does not allocate or close a
haipipe Run. Pass `--run-id` only for a real identity already supplied by its
Run owner; an execution UUID is not a substitute Ticket or Run ID. Execution,
conversion, and any explicitly requested notebook execution remain internal
Steps serving the same target.

Resolve `NOTEBOOK_SKILL_DIR` to the absolute directory of the loaded skill,
following installation symlinks. When authoring a saved wrapper, persist that
verified path in the wrapper or its documented local configuration. Select a
Python interpreter with the target script's dependencies (`NOTEBOOK_PYTHON`
below); use an existing project environment when available. Do not assume an
`env.sh` or `.venv` exists or source an unknown environment file.

```bash
#!/usr/bin/env bash
set -euo pipefail
: "${NOTEBOOK_SKILL_DIR:?Set the absolute directory of the loaded notebook skill}"
TASK_DIR="$(cd "$(dirname "$0")/.." && pwd)"
# Use the confirmed project root; Git can resolve it for a Git-backed task.
PROJECT_DIR="$(git -C "$TASK_DIR" rev-parse --show-toplevel)"
"${NOTEBOOK_PYTHON:-python3}" "$NOTEBOOK_SKILL_DIR/run_notebook.py" \
  "$TASK_DIR/N-topic.py" \
  --project-dir "$PROJECT_DIR" \
  --output-root "$TASK_DIR/runs/executions"
```

For a non-Git project, set `PROJECT_DIR` to its confirmed absolute directory.
Check the helper's exit code and the exact receipt path printed on stdout.
A nonzero exit is a failed/interrupted Step, even if some outputs exist. The
notebook in a successful attempt contains cells without execution outputs.
Only run nbconvert with `--execute` when that additional execution is wanted;
it executes source side effects again and needs the same project cwd and
`RUN_DIR`. Output clearing does not execute the source.



---

Quick Reference
================

```
File layout per task:
  <task>/
    N-topic.py                   ← source of truth (cell-based)
    notebook/N-topic.ipynb       ← derived (CONVERT output)
    runs/run-N.sh                ← bash wrapper (one per script)
    runs/executions/<unique-id>/ ← one preserved execution attempt
      artifacts/                ← side-effect artifacts (csv/png/txt)
      N-topic.ipynb             ← derived notebook for this attempt
      execution.json            ← status, timestamps, logs, optional Run link

Cell markers (Python):
  # %%               code cell
  # %% Section       labeled code cell
  # %% [markdown]    markdown cell

Tools in this checkout:
  plugins/haipipe-toolkit/skills/0_utils/notebook-cell-python/convert_to_notebooks.py
                              .py → .ipynb (no execution)
  jupyter nbconvert --to notebook \
    --ClearOutputPreprocessor.enabled=True --inplace <notebook>.ipynb
                              optionally strip outputs (requires nbconvert)
```


---

End of Skill Definition
