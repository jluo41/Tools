fn-organize: File Inventory + Proposed Reorganization + Verification
======================================================================

Inspects a project folder, inventories all relevant files (inside the project
and related files outside), proposes structural reorganization to match the
standard layout, and — if the user approves and reorganization is applied —
immediately verifies that all imports and paths still work.

Writes to: examples/{PROJECT_ID}/docs/organize-report.md

Write access policy:
  ALLOWED    docs/organize-report.md   (create or overwrite)
  ALLOWED    scripts/INDEX.md          (update after reorganization, if paths changed)
  ALLOWED    examples/{PROJECT_ID}/    (move/rename files ONLY if user confirms in Phase 2)
  BLOCKED    config/                   (read only — never modify YAMLs)
  BLOCKED    code/                     (read only — never modify library or generated code)
  BLOCKED    code-dev/                 (read only — never modify builders)

---

Step 0: Identify the Target Project
=====================================

Use the same auto-detection logic as fn-review.md Step 0:
  1. Check git status for recently modified files under examples/
  2. Find most recently modified project if ambiguous
  3. List all Proj* directories and ask user to pick if still unclear

Confirm path before proceeding. Set:

  PROJECT_PATH = examples/{PROJECT_ID}/
  PROJECT_ID   = basename of that path

---

Phase 1: File Inventory
========================

Goal: produce Section 1 of docs/organize-report.md — a complete picture of
all files that belong to or are used by this project.

**Reuse prior scan results when available:**

  Check whether docs/data-map.md exists on disk:
    YES -> read docs/data-map.md to extract FnClass and ModelClass names
           already resolved. Do NOT re-scan code/ from scratch.
    NO  -> scan the same range fn-review would scan:
    code/haifn/fn_source/, code/haifn/fn_record/, code/haifn/fn_case/,
    code/haifn/fn_aidata/, code/haifn/fn_model/
    code/hainn/algo/, code/hainn/tuner/, code/hainn/instance/
    code-dev/1-PIPELINE/ (all WorkSpace dirs)
  Use the FnClass and ModelClass names from config/ YAMLs as the search keys.

**Step 1a — Inventory the project folder:**

  Walk examples/{PROJECT_ID}/ recursively.
  Group files by top-level folder (cc-archive/, config/, scripts/,
  results/, docs/, nb/, and any extra dirs).
  For each file record: relative path, file type/extension, size if large (> 100KB).

**Step 1b — Inventory related files outside the project:**

  Collect the following (from prior scan or fresh scan per above):

    Pipeline Fn files (code/haifn/):
      For each FnClass used in config/ YAMLs: the .py file containing that class.

    ML model files (code/hainn/):
      For each ModelInstanceClass / TunerClass in config/ YAMLs:
        code/hainn/instance/...    (instance file)
        code/hainn/tuner/...       (tuner file)
        code/hainn/algo/...        (algorithm file, if found)

    Builder files (code-dev/1-PIPELINE/):
      Any build_*.py files in WorkSpace dirs whose name references the project
      datasets (inferred from config/ YAML filenames).

    If no related files are found for a category, note: "(none found)".

**Step 1c — Write Section 1 to docs/organize-report.md:**

  Format:

  ```
  Organize Report: {PROJECT_ID}
  ==============================
  Generated: {YYMMDD}

  Section 1 — File Inventory
  ===========================

  Project Folder: examples/{PROJECT_ID}/
  ----------------------------------------

    cc-archive/
      {filename}  [{ext}]
      ...

    config/
      {filename}  [{ext}]
      ...

    scripts/
      {filename}  [{ext}]
      ...

    results/
      {foldername}/
        {filename}  [{ext}]
      ...

    docs/
      {filename}  [{ext}]
      ...

    nb/   [optional]
      {filename}  [{ext}]
      ...

    {extra_dir}/   [non-standard]
      {filename}  [{ext}]
      ...

  Related Files Outside Project
  ------------------------------

    Pipeline Fn files (code/haifn/):
      {relative path from repo root}  [FnClass: {FnClassName}, Stage: {N}]
      ...

    ML model files (code/hainn/):
      {relative path}  [class: {ClassName}]
      ...

    Builder files (code-dev/):
      {relative path}  [dataset: {dataset}, Stage: {N}]
      ...
  ```

  Report to user: "Section 1 written. Moving to Phase 2 — Proposed Reorganization."

---

Phase 2: Proposed Reorganization
==================================

Goal: compare the current layout to the standard 5-part structure and propose
specific moves. Present the proposal to the user and wait for approval before
touching any files.

**Step 2a — Detect structural deviations:**

  Check the following against the standard in ref/project-structure.md:

  Folder-level issues:
    [ ] Missing mandatory folders (cc-archive/, config/, scripts/, results/, docs/)
        -> propose: create the missing folder
    [ ] Extra top-level folders not in the standard five
        -> propose: migrate contents to the nearest matching standard folder,
           or flag for user decision if the content is ambiguous

  File placement issues:
    [ ] .py or .sh files at the project root (not inside scripts/)
        -> propose: move to scripts/
    [ ] YAML files outside config/
        -> propose: move to config/
    [ ] Non-.md files in cc-archive/ (.py, .yaml, .ipynb, etc.)
        -> propose: move to the appropriate folder (scripts/, config/)
    [ ] Non-.md files at the root of docs/
        (code files, notebooks, CSVs are not planning docs)
        -> propose: move to the appropriate standard folder

  nb/ issues:
    [ ] .ipynb files found outside nb/ (in scripts/, cc-archive/, project root, etc.)
        -> propose: move to nb/
    [ ] nb/ exists but nb/INDEX.md is missing
        -> propose: create nb/INDEX.md (see ref/project-structure.md for format)
    [ ] nb/ does not exist but .ipynb files were found anywhere in the project
        -> propose: create nb/ and move all .ipynb files there

  scripts/ layout issues:
    [ ] Flat .py or .sh files directly in scripts/ (not in a task subfolder or sbatch/)
        -> propose: create a task folder scripts/{task_name}/ and move the file there;
           also create runs/ and results/ subdirectories within the task folder
    [ ] .ipynb files in scripts/
        -> propose: move to nb/
    [ ] scripts/INDEX.md missing
        -> propose: create scripts/INDEX.md (global task index format per ref)

  Per-task folder issues (for each scripts/{task}/ found):
    [ ] Task folder is missing INDEX.md
        -> propose: create {task}/INDEX.md (run inventory format per ref)
    [ ] Task folder has no {task}.py file
        -> propose: create {task}/{task}.py stub (or flag if .py was given a different name)
    [ ] Task folder has bash scripts at the task root (not inside runs/)
        -> propose: move them into {task}/runs/
    [ ] Task folder has result folders at the task root (not inside results/)
        -> propose: move them into {task}/results/

  Top-level results/ issues (legacy layout):
    [ ] Project has a top-level results/ folder with result subfolders
        -> propose: migrate each result subfolder into the matching task folder:
             results/{task_desc}/  ->  scripts/{task_name}/results/{variant}/
           Ask user to confirm the task mapping before moving.

  Run-result alignment issues (per task):
    [ ] A run script in {task}/runs/ has no matching folder in {task}/results/
        -> flag: "run without results — may be pending or failed"
    [ ] A result folder in {task}/results/ has no matching run script in {task}/runs/
        -> flag: "orphaned result folder — check if its run script was renamed or deleted"

**Step 2e — Notebook Coverage Check:**

  Goal: check whether nb/ contains demo notebooks that cover the pipeline stages
  used by this project. This is an advisory check — it produces recommendations,
  not file moves.

  Determine which stages are active:
    Prefer docs/data-map.md if it exists — it already has the declared stages
    and FnClass names resolved; no re-scan needed.
    Fallback: read config/ YAML filenames if docs/data-map.md is absent.
    Active stage pairs: for each adjacent active pair (e.g., S1+S2 -> S1→S2 segment),
    a demo notebook is recommended.

  Read nb/INDEX.md if it exists:
    For each active stage-pair segment (S1→S2, S2→S3, S3→S4, S4→S5, S5→S6):
      [ ] nb/INDEX.md has a row covering this segment with status != deprecated
          -> COVERED
      [ ] nb/INDEX.md has a row for this segment with status=planned
          -> PLANNED (note: not yet created)
      [ ] No row covers this segment
          -> GAP: recommend adding a planned row and notebook

  If nb/ does not exist at all:
    Flag all active stage-pair segments as GAP.
    Recommend: create nb/ + nb/INDEX.md with planned rows for each segment.

  Collect all PLANNED rows and GAP items as advisory recommendations.
  These do NOT appear in the file-move proposal table (Step 2b).
  They are written to organize-report.md as a separate section.

  Append to docs/organize-report.md:

  ```
  Section 2b — Notebook Coverage
  ================================

  Active stages (from config/): {list of active stage numbers}
  Active segments requiring demo coverage: {e.g., S1→S2, S2→S3, S3→S4}

  | Segment | Status | Notebook | Notes |
  |---------|--------|----------|-------|
  | S1→S2   | COVERED  | 001_260315_demo_s1_to_s2.ipynb | |
  | S2→S3   | PLANNED  | (planned) | nb/INDEX.md row exists; notebook not yet created |
  | S3→S4   | GAP      | (none)    | No entry in nb/INDEX.md |

  Recommendations:
    {For each PLANNED row:}
      - Create the planned notebook for {segment}: {suggested filename}
    {For each GAP:}
      - Add a planned row to nb/INDEX.md for {segment}, then create the notebook
    {If nb/ missing entirely:}
      - Create nb/ and nb/INDEX.md; add planned rows for all active segments
  ```

  If all segments are COVERED: print "Notebook coverage: all active segments covered."

  If any GAP or PLANNED segments were found, after writing Section 2b, ask:

    ```
    Found {N} segment(s) needing notebooks ({list of SEGMENT_KEYs}).
    Create notebooks now?
      yes      -> run /haipipe-project nb for each segment in sequence
      pick     -> list segments and let user choose which to create now
      no       -> skip; run /haipipe-project nb [path] later per segment
    ```

    If yes or pick:
      For each selected segment: execute fn-nb.md Steps 3–7 in full.
      Project is already identified (Step 0); pass SEGMENT_KEY directly to
      fn-nb Step 1 (skip the "ask which segment" prompt).
      On completing each notebook, continue to the next selected segment.

    If no:
      Print: "Run /haipipe-project nb {PROJECT_PATH} to create notebooks
              for: {list of SEGMENT_KEYs}"

**Step 2b — Build proposal table:**

  Compile all proposed changes into a table. If nothing needs to change, say so.

  Format:

  ```
  Section 2 — Proposed Reorganization
  =====================================

  {If no changes needed:}
  All files are already in the correct locations. No moves required.

  {If changes needed:}
  The following moves are proposed to bring the project to standard layout.
  No files have been changed yet.

  | # | Current Path (relative to project root) | Proposed Path | Reason |
  |---|----------------------------------------|---------------|--------|
  | 1 | train_model.py                          | scripts/001_{YYMMDD}_train_model.py | .py at root -> scripts/ |
  | 2 | notes.ipynb                             | cc-archive/notes.ipynb | notebook outside scripts/ |
  | 3 | workspace/outputs/                      | (flag) contents -> _WorkSpace/ or results/ | non-standard folder |
  ...

  Pending confirmation — no files have been moved yet.
  ```

**Step 2c — Ask the user:**

  Print exactly:

  ```
  Proposed {N} change(s) above.
  Apply this reorganization now? (yes / no)
  If no: I will remind you to run verification once you reorganize manually.
  ```

  Wait for user response before proceeding.

  If user says NO (or defers):
    Append to docs/organize-report.md:

      ```
      Status: Reorganization deferred.
      Reminder: once you move/rename files manually, run:
        /haipipe-project organize verify {PROJECT_PATH}
      to check that imports and paths still work.
      ```

    Print to user:
      "Reorganization skipped. Reminder saved to docs/organize-report.md.
       Run /haipipe-project organize verify {PROJECT_PATH} after manual moves."

    Then print this checkpoint (verbatim):

      [CH-6] reorganization pending verification?
      "Reminder: if you moved or renamed files manually, run
       /haipipe-project organize verify to confirm imports and paths still work."

    Stop here.

  If user says YES:
    Proceed to Step 2d.

**Step 2d — Apply the reorganization:**

  Execute each proposed move from the table in order:
    - Create any missing folders first.
    - Move/rename files.
    - Do NOT move or modify files in code/, code-dev/, config/ — those are read-only.
    - Do NOT move cc-archive/ session files (.md files named cc_* or di_*).

  After all moves, append the applied-changes log to docs/organize-report.md:

  ```
  Applied Changes
  ---------------
    [1] moved: train_model.py  ->  scripts/001_{YYMMDD}_train_model.py
    [2] moved: notes.ipynb  ->  cc-archive/notes.ipynb
    ...
    Total: {N} file(s) moved/renamed.
  ```

  Then proceed immediately to Phase 3.

---

Phase 3: Post-Reorganization Verification
==========================================

Goal: confirm that all scripts still have valid imports and path references
after any file moves. Runs immediately after Phase 2d (or on demand via
`organize verify`).

**Step 3a — Import resolution check:**

  Scan all .py files in scripts/ for haipipe imports:
    grep -n "from haifn\|from hainn\|import haifn\|import hainn" scripts/*.py

  Reuse FnClass / ModelClass locations from Phase 1 (no re-scan needed).

  For each imported class name:
    [ ] Class exists in code/haifn/ or code/hainn/
        Not found -> [ERROR] "Script {script} imports {ClassName} — class not found in codebase."
    [ ] Import path matches the actual file location
        Mismatch -> [ERROR] "Script {script}: import path {import_stmt} does not match {actual_path}."

**Step 3b — Config reference check:**

  For each YAML in config/:
    [ ] FnClass names still exist in code/haifn/ (same check as fn-review Step 7a)
        Broken -> [ERROR] "config/{yaml}: FnClass {name} not found after reorganization."

**Step 3c — Relative path check:**

  Scan all .py files for project-relative path references:
    grep -rn "config/\|results/\|docs/\|cc-archive/" scripts/**/*.py

  Also scan all .sh files in task runs/ for Python script path references
  (these commonly reference $PROJ/scripts/{task}/{task}.py):
    grep -rn "scripts/" scripts/**/runs/*.sh

  For each referenced path:
    [ ] The referenced file/folder exists at that path relative to where the
        script is expected to be run from (project root or $PROJ).
        Not found -> [WARN] "{script} references '{path}' which does not exist."

  Common issues after task-folder reorganization:
    - Run scripts that previously called $PROJ/scripts/train_num.py
      must now call $PROJ/scripts/train_num/train_num.py
    - Any hardcoded results/ at project root should now point to
      scripts/{task}/results/ instead.

**Step 3d — Write verification results to docs/organize-report.md:**

  ```
  Section 3 — Verification
  =========================
  Verified: {YYMMDD}

  Import Resolution
  -----------------
    {script}: {ClassName} -> {PASS / ERROR: reason}
    ...

  Config Reference Check
  ----------------------
    {yaml}: {FnClass} -> {PASS / ERROR: reason}
    ...

  Relative Path Check
  -------------------
    {script}: '{path}' -> {PASS / WARN: reason}
    ...

  Summary
  -------
    ERROR: {count}  (must fix before running scripts)
    WARN:  {count}  (review — may be intentional)
    PASS:  {count}
  ```

  If all checks pass:
    Print: "Verification passed. All imports and paths are intact."

  If any ERROR:
    Print: "Verification found {N} issue(s). See docs/organize-report.md Section 3."
    List each ERROR item inline so the user can act immediately.

---

Checkpoints
-----------

Print these after Phase 3 completes (verbatim — no extra analysis needed):

  [CH-3] file paths valid?
  "Quick check: any scripts that reference config/, results/, or docs/ paths —
   confirm those paths still exist relative to the project root."

  [CH-2] scripts/INDEX.md in sync?
  "Quick check: (1) scripts/INDEX.md lists every task subfolder; (2) each
   {task}/INDEX.md has a row for every .sh in {task}/runs/ and the matching
   result folder in {task}/results/. Update any entries affected by moves."

---

`organize verify` — Standalone Verification
=============================================

If the user runs `/haipipe-project organize verify [path]` without having
run Phase 1 or 2 first:

  1. Identify the project (same auto-detect logic).
  2. Check if docs/organize-report.md exists:
       Yes  -> read the existing report for context (FnClass names from Section 1).
       No   -> run Phase 1 scan first to build the file inventory, then proceed.
  3. Run Phase 3 steps 3a–3d exactly.
  4. Append results to docs/organize-report.md (or create if missing).

This lets the user trigger verification after a manual reorganization without
re-running the full organize flow.

---

MUST NOT
---------

- Do NOT move or rename files in code/, code-dev/, or config/ — read only.
- Do NOT move cc-archive/ session history files (cc_*.md, di_*.md).
- Do NOT apply any moves without explicit user YES in Step 2c.
- Do NOT run any pipeline commands (haistep-*, train, evaluate).
- Do NOT modify YAML configs during reorganization.
- Do NOT create new scripts or stub files — organize only moves existing files.
- Do NOT create .ipynb notebook files — Step 2e produces recommendations only; the user creates the notebooks.
- DO create nb/INDEX.md if nb/ exists but INDEX.md is missing (INDEX.md is structural, not a notebook).
