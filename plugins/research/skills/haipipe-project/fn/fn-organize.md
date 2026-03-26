fn-organize: File Inventory + Proposed Reorganization + Verification
======================================================================

Inspects a project folder, inventories all relevant files (inside the project
and related files outside), proposes structural reorganization to match the
standard layout, and — if the user approves and reorganization is applied —
immediately verifies that all imports and paths still work.

Writes to: examples/{PROJECT_ID}/docs/organize-report.md

Write access policy:
  ALLOWED    docs/organize-report.md   (create or overwrite)
  ALLOWED    tasks/INDEX.md            (update after reorganization, if paths changed)
  ALLOWED    examples/{PROJECT_ID}/    (move/rename files ONLY if user confirms in Phase 2)
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
  Use the FnClass and ModelClass names from task config/ YAMLs as the search keys.

**Step 1a — Inventory the project folder:**

  Walk examples/{PROJECT_ID}/ recursively.
  Skip _old/ entirely — do not scan or report its contents.
  Group files by top-level folder (cc-archive/, tasks/, docs/, paper/,
  and any extra dirs).
  For each file record: relative path, file type/extension, size if large (> 100KB).

  For tasks/: list each task subfolder and its contents, including:
    - {task}/{task}.py (main script)
    - {task}/{task}.ipynb (notebook, if present)
    - {task}/config/ (task-specific YAML configs)
    - {task}/runs/ (run scripts and variant notebooks)
    - {task}/results/ (output folders)

  Detect YAML config files at the project root and flag them for relocation
  into the appropriate task's config/ subfolder (see Phase 2).

**Step 1b — Inventory related files outside the project:**

  Collect the following (from prior scan or fresh scan per above):

    Pipeline Fn files (code/haifn/):
      For each FnClass used in task config/ YAMLs: the .py file containing that class.

    ML model files (code/hainn/):
      For each ModelInstanceClass / TunerClass in task config/ YAMLs:
        code/hainn/instance/...    (instance file)
        code/hainn/tuner/...       (tuner file)
        code/hainn/algo/...        (algorithm file, if found)

    Builder files (code-dev/1-PIPELINE/):
      Any build_*.py files in WorkSpace dirs whose name references the project
      datasets (inferred from task config/ YAML filenames).

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

    tasks/
      {task_name}/
        {task_name}.py  [py]
        {task_name}.ipynb  [ipynb]  (if present)
        config/
          {filename}  [{ext}]
          ...
        runs/
          {variant}.sh  [sh]
          {variant}.ipynb  [ipynb]  (if present)
          ...
        results/
          {foldername}/
            {filename}  [{ext}]
          ...
      ...

    docs/
      {filename}  [{ext}]
      ...

    paper/   [recognized — not reorganized]
      {filename}  [{ext}]
      ...

    _old/   [recognized — not scanned]

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

Goal: compare the current layout to the standard structure and propose
specific moves. Present the proposal to the user and wait for approval before
touching any files.

**Step 2a — Detect structural deviations:**

  Check the following against the standard layout:

  Folder-level issues:
    [ ] Missing mandatory folders (cc-archive/, tasks/, docs/)
        -> propose: create the missing folder
    [ ] Extra top-level folders not in the standard set
        (paper/ and _old/ are recognized — do NOT propose moving them)
        -> propose: migrate contents to the nearest matching standard folder,
           or flag for user decision if the content is ambiguous

  File placement issues:
    [ ] .py or .sh files at the project root (not inside tasks/)
        -> propose: move to tasks/{task}/ (infer task name from filename)
    [ ] YAML files at the project root or outside task folders
        -> propose: move to tasks/{task}/config/
        -> if a YAML is used by multiple tasks, propose placing it in one task's
           config/ and creating symlinks from each other task's config/
    [ ] Non-.md files in cc-archive/ (.py, .yaml, .ipynb, etc.)
        -> propose: move to the appropriate folder (tasks/, tasks/{task}/config/)
    [ ] Non-.md files at the root of docs/
        (code files, notebooks, CSVs are not planning docs)
        -> propose: move to the appropriate standard folder

  Notebook issues:
    [ ] .ipynb files at the project root
        -> propose: move to tasks/{task}/ as {task}.ipynb or tasks/{task}/runs/ as {variant}.ipynb
    [ ] .ipynb files found in non-task locations (cc-archive/, docs/, etc.)
        -> propose: move to the matching task folder
    [ ] .ipynb exists in a task folder without a matching .py source file
        -> flag: ".py source missing — consider recreating from .ipynb or adding .py"
    [ ] .py exists in a task folder without a matching .ipynb
        -> this is fine (Python-first workflow); no action needed

  tasks/ layout issues:
    [ ] Flat .py or .sh files directly in tasks/ (not in a task subfolder)
        -> propose: create a task folder tasks/{task_name}/ and move the file there;
           also create runs/ and results/ subdirectories within the task folder
    [ ] tasks/INDEX.md missing
        -> propose: create tasks/INDEX.md (global task index format per ref)

  Config symlink proposals:
    [ ] Same YAML filename referenced by multiple tasks
        -> propose: place the canonical copy in one task's config/, create symlinks
           from each other task's config/ pointing to the canonical copy
    [ ] Existing config/ at project root with YAMLs used by multiple tasks
        -> propose: move each YAML to its primary task's config/, symlink from
           secondary tasks

  Per-task folder issues (for each tasks/{task}/ found):
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
             results/{task_desc}/  ->  tasks/{task_name}/results/{variant}/
           Ask user to confirm the task mapping before moving.

  Run-result alignment issues (per task):
    [ ] A run script in {task}/runs/ has no matching folder in {task}/results/
        -> flag: "run without results — may be pending or failed"
    [ ] A result folder in {task}/results/ has no matching run script in {task}/runs/
        -> flag: "orphaned result folder — check if its run script was renamed or deleted"

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
  | 1 | train_model.py                          | tasks/train_model/train_model.py | .py at root -> tasks/ |
  | 2 | config.yaml                             | tasks/train_model/config/config.yaml | YAML at root -> task config/ |
  | 3 | notes.ipynb                             | tasks/analysis/analysis.ipynb | notebook at root -> task folder |
  | 4 | shared.yaml                             | tasks/train_model/config/shared.yaml + symlink from tasks/eval_model/config/shared.yaml | shared config -> canonical + symlink |
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
    - Create symlinks for shared configs (use relative symlinks where possible).
    - Do NOT move or modify files in code/, code-dev/ — those are read-only.
    - Do NOT move cc-archive/ session files (.md files named cc_* or di_*).
    - Do NOT move paper/ — it is recognized and left as-is.
    - Do NOT scan or touch _old/ — it is recognized and left as-is.

  After all moves, append the applied-changes log to docs/organize-report.md:

  ```
  Applied Changes
  ---------------
    [1] moved: train_model.py  ->  tasks/train_model/train_model.py
    [2] moved: config.yaml  ->  tasks/train_model/config/config.yaml
    [3] symlink: tasks/eval_model/config/shared.yaml  ->  ../train_model/config/shared.yaml
    ...
    Total: {N} file(s) moved/renamed, {M} symlink(s) created.
  ```

  Then proceed immediately to Phase 3.

---

Phase 3: Post-Reorganization Verification
==========================================

Goal: confirm that all scripts still have valid imports and path references
after any file moves, and that all symlinks are valid. Runs immediately after
Phase 2d (or on demand via `organize verify`).

**Step 3a — Import resolution check:**

  Scan all .py files in tasks/ for haipipe imports:
    grep -rn "from haifn\|from hainn\|import haifn\|import hainn" tasks/**/*.py

  Reuse FnClass / ModelClass locations from Phase 1 (no re-scan needed).

  For each imported class name:
    [ ] Class exists in code/haifn/ or code/hainn/
        Not found -> [ERROR] "Script {script} imports {ClassName} — class not found in codebase."
    [ ] Import path matches the actual file location
        Mismatch -> [ERROR] "Script {script}: import path {import_stmt} does not match {actual_path}."

**Step 3b — Config reference check:**

  For each YAML in tasks/*/config/:
    [ ] FnClass names still exist in code/haifn/ (same check as fn-review Step 7a)
        Broken -> [ERROR] "tasks/{task}/config/{yaml}: FnClass {name} not found after reorganization."

**Step 3c — Relative path check:**

  Scan all .py files for project-relative path references:
    grep -rn "config/\|results/\|docs/\|cc-archive/" tasks/**/*.py

  Also scan all .sh files in task runs/ for Python script path references
  (these commonly reference $PROJ/tasks/{task}/{task}.py):
    grep -rn "tasks/" tasks/**/runs/*.sh

  For each referenced path:
    [ ] The referenced file/folder exists at that path relative to where the
        script is expected to be run from (project root or $PROJ).
        Not found -> [WARN] "{script} references '{path}' which does not exist."

  Common issues after task-folder reorganization:
    - Run scripts that previously called $PROJ/tasks/train_num.py
      must now call $PROJ/tasks/train_num/train_num.py
    - Any hardcoded results/ at project root should now point to
      tasks/{task}/results/ instead.

**Step 3d — Symlink validity check:**

  Find all symlinks within the project folder:
    find examples/{PROJECT_ID}/ -type l

  For each symlink:
    [ ] Target exists and is readable
        Broken -> [ERROR] "Symlink {link_path} -> {target} is broken (target does not exist)."
    [ ] Target is within the project folder (no dangling external references)
        External -> [WARN] "Symlink {link_path} points outside the project: {target}."

**Step 3e — Write verification results to docs/organize-report.md:**

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
    tasks/{task}/config/{yaml}: {FnClass} -> {PASS / ERROR: reason}
    ...

  Relative Path Check
  -------------------
    {script}: '{path}' -> {PASS / WARN: reason}
    ...

  Symlink Validity Check
  ----------------------
    {link_path} -> {target}: {PASS / ERROR: reason / WARN: reason}
    ...

  Summary
  -------
    ERROR: {count}  (must fix before running tasks)
    WARN:  {count}  (review — may be intentional)
    PASS:  {count}
  ```

  If all checks pass:
    Print: "Verification passed. All imports, paths, and symlinks are intact."

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

  [CH-2] tasks/INDEX.md in sync?
  "Quick check: (1) tasks/INDEX.md lists every task subfolder; (2) each
   {task}/INDEX.md has a row for every .sh in {task}/runs/ and the matching
   result folder in {task}/results/. Update any entries affected by moves."

---

Phase 4: Project Diagram
=========================

Goal: generate a draw.io diagram of the final project structure and save it
to docs/project-diagram.png and docs/project-diagram.drawio.

Requires the drawio MCP server to be installed:
  claude mcp add drawio -- npx @next-ai-drawio/mcp-server@latest

If the drawio MCP tools are NOT available, skip Phase 4 and print:
  "Skipping diagram — drawio MCP not installed.
   Run: claude mcp add drawio -- npx @next-ai-drawio/mcp-server@latest"

**Step 4a — Build the mxGraphModel XML:**

  Construct an mxGraphModel XML diagram that shows the project's folder
  structure. Use the file inventory from Phase 1 Section 1 as the source.

  Layout rules:
    - Root node: project folder name (PROJECT_ID), large rounded rectangle,
      fill=#dae8fc (light blue), at center-top.
    - Three mandatory folder nodes beneath root: cc-archive/, tasks/, docs/
      — rounded rectangles, fill=#d5e8d4 (light green).
    - tasks/ expands to show each task subfolder as a child node,
      fill=#fff2cc (yellow). Each task node shows: "{task_name}" with a
      sub-label listing run script count, config count, and result status.
      If the task has a .ipynb, note it in the sub-label.
    - docs/ shows its files as small notes: TODO.md, data-map.md,
      dependency-report.md, organize-report.md, project-diagram.png.
    - cc-archive/ shows file count: "N session files".
    - paper/ shown as a recognized folder node, fill=#e1d5e7 (light purple),
      connected to root with solid edge.
    - _old/ shown as a recognized folder node, fill=#f5f5f5 (grey),
      connected to root with dashed edge, label includes "(not scanned)".
    - Extra non-standard folders (materials/, etc.) shown as grey
      nodes, fill=#f5f5f5, connected to root with dashed edge.
    - sbatch/ shown as a child of tasks/ with fill=#ffe6cc (orange).
    - All edges: style=edgeStyle=orthogonalEdgeStyle.
    - Diagram size: fit to content, roughly 1200x900 px.

  Cell ID convention: use short unique IDs (p1, cc1, t1, t_task1, …).

  Example skeleton (adapt to actual project):

  ```xml
  <mxGraphModel>
    <root>
      <mxCell id="0"/><mxCell id="1" parent="0"/>
      <!-- root project node -->
      <mxCell id="p1" value="ProjC-Model-1-ScalingLaw" style="rounded=1;fillColor=#dae8fc;strokeColor=#6c8ebf;fontStyle=1;fontSize=13;" vertex="1" parent="1">
        <mxGeometry x="400" y="20" width="280" height="50" as="geometry"/>
      </mxCell>
      <!-- folder nodes -->
      <mxCell id="cc1" value="cc-archive/&#xa;8 session files" style="rounded=1;fillColor=#d5e8d4;strokeColor=#82b366;" vertex="1" parent="1">
        <mxGeometry x="60" y="140" width="160" height="50" as="geometry"/>
      </mxCell>
      <!-- edge: root -> cc-archive -->
      <mxCell id="e_cc" style="edgeStyle=orthogonalEdgeStyle;" edge="1" source="p1" target="cc1" parent="1">
        <mxGeometry relative="1" as="geometry"/>
      </mxCell>
      <!-- tasks/ with task subfolders -->
      <mxCell id="t1" value="tasks/" style="rounded=1;fillColor=#d5e8d4;strokeColor=#82b366;" vertex="1" parent="1">
        <mxGeometry x="300" y="140" width="160" height="50" as="geometry"/>
      </mxCell>
      <mxCell id="t_train" value="train_model/&#xa;config: 3 YAMLs&#xa;runs: 2 scripts&#xa;notebook: yes" style="rounded=1;fillColor=#fff2cc;strokeColor=#d6b656;" vertex="1" parent="1">
        <mxGeometry x="250" y="260" width="180" height="70" as="geometry"/>
      </mxCell>
      <!-- ... remaining nodes ... -->
    </root>
  </mxGraphModel>
  ```

**Step 4b — Call MCP tools:**

  1. Call start_session  (opens browser with live preview)
  2. Call create_new_diagram with the XML from Step 4a
  3. Call export_diagram:
       path:   {PROJECT_PATH}/docs/project-diagram.drawio
       format: drawio
  4. Call export_diagram:
       path:   {PROJECT_PATH}/docs/project-diagram.png
       format: png

  After export, print:
    "Diagram saved:
       docs/project-diagram.drawio
       docs/project-diagram.png"

  Append to docs/organize-report.md:
    "Phase 4 — Diagram
     Generated: {YYMMDD}
     docs/project-diagram.drawio
     docs/project-diagram.png"

---

`organize verify` — Standalone Verification
=============================================

If the user runs `/haipipe-project organize verify [path]` without having
run Phase 1 or 2 first:

  1. Identify the project (same auto-detect logic).
  2. Check if docs/organize-report.md exists:
       Yes  -> read the existing report for context (FnClass names from Section 1).
       No   -> run Phase 1 scan first to build the file inventory, then proceed.
  3. Run Phase 3 steps 3a–3e exactly.
  4. Append results to docs/organize-report.md (or create if missing).

This lets the user trigger verification after a manual reorganization without
re-running the full organize flow.

---

MUST NOT
---------

- Do NOT move or rename files in code/, code-dev/ — read only.
- Do NOT move cc-archive/ session history files (cc_*.md, di_*.md).
- Do NOT move paper/ — it is recognized and left as-is.
- Do NOT scan or modify _old/ — it is recognized and left as-is.
- Do NOT apply any moves without explicit user YES in Step 2c.
- Do NOT run any pipeline commands (haistep-*, train, evaluate).
- Do NOT modify YAML configs during reorganization (moves are allowed, edits are not).
- Do NOT create new scripts or stub files — organize only moves existing files.
- Do NOT create .py or .ipynb notebook files — organize produces recommendations only.
- DO create tasks/INDEX.md if tasks/ exists but INDEX.md is missing (INDEX.md is structural).
- DO flag .ipynb files in task folders that lack a matching .py source (Python-first workflow).
- DO create symlinks for shared configs (symlinks are structural, not content).
