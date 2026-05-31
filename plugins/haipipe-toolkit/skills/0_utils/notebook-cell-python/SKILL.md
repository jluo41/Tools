---
name: notebook-cell-python
description: "Cell-based .py ↔ .ipynb workflow — the .py is source-of-truth, the .ipynb is auto-derived for browser viewing of code + outputs + figures. Use when authoring a script that must run as a script (PR/CI) AND be viewable as a notebook; common home examples/<project>/tasks/<task>/. Trigger: cell-based py, .py to .ipynb, notebook from script, jupytext-style cells."
allowed-tools: Bash, Read, Write, Edit
metadata:
  version: "1.0.0"
  last_updated: "2026-05-31"
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

The Tools (all in `code/scripts/`)
====================================

This skill DELEGATES to canonical tools in `code/scripts/`. Do not
duplicate their logic in the skill.

  ┌──────────────┬──────────────────────────────────────────┬────────────────────────────────────────────────────┐
  │ Action       │ Command                                  │ What it does                                       │
  ├──────────────┼──────────────────────────────────────────┼────────────────────────────────────────────────────┤
  │ CREATE       │ Claude writes the .py file               │ Follow the Cell Rules + Skeleton below.            │
  │              │                                          │ (No scaffolder — the skill IS the spec.)           │
  │              │                                          │                                                    │
  │ CONVERT      │ python code/scripts/convert_to_notebooks │ Cell-based .py → .ipynb (cells only, no outputs).  │
  │              │   .py <script>.py -o <notebook>.ipynb    │                                                    │
  │              │                                          │                                                    │
  │ EXECUTE      │ jupyter nbconvert --to notebook          │ Run each cell, embed outputs + figures inline.     │
  │              │   --execute --inplace <notebook>.ipynb   │ (Optional — skip if you want the notebook to       │
  │              │                                          │ stay code-only.)                                   │
  │              │                                          │                                                    │
  │ CLEAN        │ python code/scripts/clean_notebook.py    │ Strip outputs (use before committing).             │
  │              │   <notebook>.ipynb                       │                                                    │
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
  5. **Print progress markers.** `print('=' * 80)` between phases.
     Each cell ends with a one-line `✓` confirmation when done.
  6. **Side effects to disk.** CSVs/PNGs go to an output dir (default
     read from `RUN_DIR` env var, else a sane fallback). Keeps the
     `.ipynb` reproducible without depending on the runtime env.


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
`Tools/plugins/diagram-skill/skills/diagram-ascii`: box characters
above + section markers like `─§ ① ──` for cell headers.


---

Standard Skeleton (Claude follows this when writing .py files)
================================================================

```python
"""
N-topic.py — One-line purpose.

Input:  path/to/input
Output: $RUN_DIR (defaults to <task>/runs/_LATEST/N-topic/)
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

OUT = Path(os.environ.get('RUN_DIR', 'runs/_LATEST/N-topic'))
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

Each script gets its own `run-N.sh` in the task's `runs/` folder.
Run them one at a time so each result is reviewable before the next.

```bash
#!/usr/bin/env bash
# run-N.sh — run N-topic.py and convert it to a notebook.
set -euo pipefail

TASK_DIR="$(cd "$(dirname "$0")/.." && pwd)"
REPO_ROOT="$(git -C "$TASK_DIR" rev-parse --show-toplevel)"
cd "$REPO_ROOT"

source .venv/bin/activate
source env.sh

DATE=$(date +%Y-%m-%d)
SCRIPT="$TASK_DIR/N-topic.py"
NOTEBOOK="$TASK_DIR/notebook/N-topic.ipynb"
RUN_DIR="$TASK_DIR/runs/$DATE/N-topic"

mkdir -p "$RUN_DIR" "$TASK_DIR/notebook"
ln -sfn "$DATE" "$TASK_DIR/runs/_LATEST"

# 1. Run the .py (side-effect artifacts → $RUN_DIR)
RUN_DIR="$RUN_DIR" python "$SCRIPT"

# 2. Convert .py → .ipynb
python code/scripts/convert_to_notebooks.py "$SCRIPT" -o "$NOTEBOOK"

echo "✓ Done."
echo "  Artifacts: $RUN_DIR"
echo "  Notebook:  $NOTEBOOK"
```


---

Quick Reference
================

```
File layout per task:
  <task>/
    N-topic.py                   ← source of truth (cell-based)
    notebook/N-topic.ipynb       ← derived (CONVERT output)
    runs/run-N.sh                ← bash wrapper (one per script)
    runs/<YYYY-MM-DD>/N-topic/   ← side-effect artifacts (csv/png/txt)
    runs/_LATEST -> <date>/      ← symlink to most recent run

Cell markers (Python):
  # %%               code cell
  # %% Section       labeled code cell
  # %% [markdown]    markdown cell

Tools (all in code/scripts/):
  convert_to_notebooks.py    .py → .ipynb (no execution)
  clean_notebook.py          strip outputs from .ipynb
```


---

End of Skill Definition
