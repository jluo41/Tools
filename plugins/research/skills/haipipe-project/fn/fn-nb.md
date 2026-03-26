fn-nb: Create Notebook Inside a Task Folder
=============================================

Creates a notebook for a specific task within a project. Notebooks live
**inside task folders**, not in a separate nb/ directory. The .py script
is ALWAYS the source of truth; .ipynb is derived from it via jupytext.

Two notebook types:

  **Demo notebook** -- {task}.ipynb at the task root.
    Derived from {task}.py. Same logic, just interactive.
    One per task. Demonstrates the task end-to-end.

  **Parameterized run notebook** -- runs/{variant}.ipynb inside the task folder.
    Has specific config/params baked in for a particular experiment variant.
    Multiple allowed per task. Each lives under {task}/runs/.

Conversion command (always):
  jupytext --to notebook {task}.py -o {task}.ipynb

Writes to:
  ALLOWED    {task}/{task}.ipynb              (demo notebook, converted from .py)
  ALLOWED    {task}/runs/{variant}.py         (parameterized run script)
  ALLOWED    {task}/runs/{variant}.ipynb      (converted from run .py)
  ALLOWED    {task}/INDEX.md                  (update if run notebook created)
  BLOCKED    config/                          (read only)
  BLOCKED    code/                            (read only)

---

Step 1: Identify the Target Task
==================================

Auto-detect or accept user specification:

  1. If the user names a task explicitly, use it.
  2. Otherwise, check git status for recently modified files under examples/.
     Look for task folders (directories containing a .py script of the same name).
  3. If ambiguous, list candidate task folders and ask the user to pick.

Set:
  PROJECT_PATH = examples/{PROJECT_ID}/
  TASK_PATH    = path to the task folder (e.g., examples/{PROJECT_ID}/{task}/)
  TASK_NAME    = basename of the task folder

Confirm the task folder contains {TASK_NAME}.py (the source script).
If it does not exist, stop and report:
  "No {TASK_NAME}.py found in {TASK_PATH}. The .py script must exist first."

---

Step 2: Determine Notebook Type
=================================

Ask the user which type of notebook to create:

  "What kind of notebook for task '{TASK_NAME}'?
   (a) **Demo notebook** -- {TASK_NAME}.ipynb at task root (from {TASK_NAME}.py)
   (b) **Parameterized run** -- runs/{variant}.ipynb with specific config baked in"

If the user says "demo" or (a):
  Set: NB_TYPE = demo
  Set: SOURCE_PY   = {TASK_PATH}/{TASK_NAME}.py
  Set: TARGET_IPYNB = {TASK_PATH}/{TASK_NAME}.ipynb

If the user says "run" or (b):
  Ask for a variant name and the specific params/config to bake in.
  Set: NB_TYPE = run
  Set: VARIANT = user-provided name (e.g., "baseline_lr1e3", "ablation_no_fair")
  Set: SOURCE_PY   = {TASK_PATH}/runs/{VARIANT}.py
  Set: TARGET_IPYNB = {TASK_PATH}/runs/{VARIANT}.ipynb

If a demo .ipynb already exists at the target path:
  Warn: "{TARGET_IPYNB} already exists. Overwrite? (yes/no)"
  Proceed only if the user confirms.

---

Step 3: Create the Notebook (Demo)
=====================================

For NB_TYPE = demo:

The source script {TASK_NAME}.py already exists -- it IS the source of truth.
Convert it directly to .ipynb:

  ```bash
  source .venv/bin/activate
  jupytext --to notebook {SOURCE_PY} -o {TARGET_IPYNB}
  ```

If jupytext is not installed, fall back to the NotebookEdit tool:
  Read each `# %%` cell from the .py and write corresponding notebook cells.

After conversion, verify:

  ```bash
  python -c "import json; nb=json.load(open('{TARGET_IPYNB}')); print(f'Cells: {len(nb[\"cells\"])}')"
  ```

The .py remains the source of truth. If edits are needed later, edit the
.py and re-convert. Do NOT edit the .ipynb directly.

---

Step 4: Create the Notebook (Parameterized Run)
=================================================

For NB_TYPE = run:

4a. Ensure the runs/ directory exists:
  Create {TASK_PATH}/runs/ if it does not exist.

4b. Create the parameterized .py script:
  Create {SOURCE_PY} as a cell-wise Python script using `# %%` markers.
  Base it on {TASK_NAME}.py but with specific params/config baked in.

  The script should:
  - Import the same modules as the parent task script
  - Override specific config values with the baked-in params
  - Be runnable standalone: `python {SOURCE_PY}`
  - Follow the notebook-cell-python skill conventions:
      `# %%` for code cells
      `# %% [markdown]` for markdown cells (content as `# ` prefixed lines)

  Typical cell structure:

  ---------------------------------------------------------------------
  Cell 1  [markdown]  -- Title + Variant Description
  ---------------------------------------------------------------------

    # %% [markdown]
    # # Run: {VARIANT} -- {TASK_NAME}
    # **Project:** {PROJECT_ID}
    # **Created:** {YYMMDD}
    #
    # **Variant description:** {user-provided description}
    # **Key params:** {param1}={val1}, {param2}={val2}, ...
    #
    # Based on: ../{TASK_NAME}.py

  ---------------------------------------------------------------------
  Cell 2  [code]  -- Config Overrides
  ---------------------------------------------------------------------

    # %% Config Overrides
    # These params differ from the default {TASK_NAME}.py
    {PARAM_1} = {VALUE_1}
    {PARAM_2} = {VALUE_2}
    # ... (all baked-in overrides listed explicitly)

  ---------------------------------------------------------------------
  Remaining cells  -- Adapted from {TASK_NAME}.py
  ---------------------------------------------------------------------

    Copy the relevant logic from {TASK_NAME}.py, substituting the
    overridden params where they appear. Keep the same cell structure
    but with the specific config values applied.

  Fill in all {placeholders} using the values collected from the user
  and from the parent task script.

4c. Convert the .py to .ipynb:

  ```bash
  source .venv/bin/activate
  jupytext --to notebook {SOURCE_PY} -o {TARGET_IPYNB}
  ```

  If jupytext is not installed, fall back to the NotebookEdit tool.

4d. Verify:

  ```bash
  python -c "import json; nb=json.load(open('{TARGET_IPYNB}')); print(f'Cells: {len(nb[\"cells\"])}')"
  ```

---

Step 5: Update Task INDEX.md (Run Notebooks Only)
===================================================

If NB_TYPE = run, update {TASK_PATH}/INDEX.md to record the new run notebook.

If {TASK_PATH}/INDEX.md does not exist, skip this step (do not create one
just for a run notebook -- INDEX.md is managed by other flows).

If it exists, append or update a line in the runs section:

  | runs/{VARIANT}.py | runs/{VARIANT}.ipynb | {description} | {YYMMDD} | wip |

If NB_TYPE = demo, no INDEX.md update is needed -- the demo notebook is
a direct derivative of the task script and needs no separate tracking.

---

Step 6: Report to User
========================

For NB_TYPE = demo, print:

  ```
  Demo Notebook Created
  ===================================
  Project:     {PROJECT_ID}
  Task:        {TASK_NAME}
  Source:      {SOURCE_PY}          (source of truth)
  Notebook:    {TARGET_IPYNB}       (converted from .py)

  Next steps:
    1. Open {TARGET_IPYNB} and run all cells top-to-bottom.
    2. If edits are needed, edit {SOURCE_PY} and re-convert:
       jupytext --to notebook {SOURCE_PY} -o {TARGET_IPYNB}
    3. Never edit the .ipynb directly.
  ```

For NB_TYPE = run, print:

  ```
  Parameterized Run Notebook Created
  ===================================
  Project:     {PROJECT_ID}
  Task:        {TASK_NAME}
  Variant:     {VARIANT}
  Source:      {SOURCE_PY}          (source of truth)
  Notebook:    {TARGET_IPYNB}       (converted from .py)
  Key params:  {param1}={val1}, {param2}={val2}, ...

  Task INDEX.md: {updated / not present, skipped}

  Next steps:
    1. Review {SOURCE_PY} to confirm baked-in params are correct.
    2. Open {TARGET_IPYNB} and run all cells top-to-bottom.
    3. If edits are needed, edit {SOURCE_PY} and re-convert:
       jupytext --to notebook {SOURCE_PY} -o {TARGET_IPYNB}
    4. Never edit the .ipynb directly.
  ```

---

CHECKPOINT HINTS
-----------------

After completing this flow, the agent should be able to answer:

  [x] Which task folder was targeted?
  [x] What type of notebook was created (demo or parameterized run)?
  [x] Where does the .py source live? Where does the .ipynb live?
  [x] For runs: what params were baked in? Is the variant recorded in INDEX.md?
  [x] Is the .ipynb valid JSON with the expected number of cells?

---

MUST NOT
---------

- Do NOT edit the .ipynb directly -- edit the .py and re-convert.
- Do NOT create notebooks in a separate nb/ folder -- they live in task folders.
- Do NOT move or modify files in config/ or code/.
- Do NOT run any pipeline commands (haistep-*, train, evaluate).
- Do NOT fill in implementation details in commented-out code cells --
  leave them as stubs for the user to complete.
