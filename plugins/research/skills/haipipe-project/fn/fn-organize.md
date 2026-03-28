fn-organize: File Inventory + Reorganization + Verification
=============================================================

Inventories project files, proposes reorganization to standard layout,
applies changes if approved, and verifies paths after moves.

Writes to: docs/organize-report.md, tasks/INDEX.md (after reorg)
File moves: examples/{PROJECT_ID}/ only (with user approval)
Read-only: code/, code-dev/

---

Step 0: Identify Target Project
=================================

Auto-detect from git status or ask. Set PROJECT_PATH and PROJECT_ID.

---

Phase 1: File Inventory
========================

Goal: produce a complete picture of all project-related files.

**Step 1a -- Project folder inventory:**
  Walk examples/{PROJECT_ID}/ recursively (skip _old/).
  Group by top-level folder. For tasks/: list each task subfolder contents
  ({task}.py, config/, runs/, results/).
  Flag files at project root that belong inside task folders.

**Step 1b -- Related external files:**
  For each FnClass/ModelClass in task config/ YAMLs, find the source file in
  code/haifn/, code/hainn/, or code-dev/. If docs/data-map.md exists, reuse
  its class resolution instead of re-scanning.

**Step 1c -- Write Section 1 to docs/organize-report.md:**
  List all project files grouped by folder, plus related external files.

---

Phase 2: Proposed Reorganization
==================================

Compare current layout to standard and propose specific moves.

**Detect and propose fixes for:**

  Folder-level:
    - Missing mandatory folders (tasks/) -> create
    - Extra top-level folders -> migrate contents to standard location

  File placement:
    - .py/.sh at project root -> move to tasks/{task}/
    - YAML outside task config/ -> move to tasks/{task}/config/
    - Non-.md in cc-archive/ -> move to appropriate folder

  tasks/ layout:
    - Flat scripts in tasks/ -> create task subfolder, move inside
    - Missing tasks/INDEX.md -> create
    - Per-task: missing {task}.py, INDEX.md, bash scripts outside runs/,
      results outside results/

  Config sharing:
    - Same YAML used by multiple tasks -> canonical copy + symlinks

  Legacy layout:
    - Top-level config/ -> distribute to task folders
    - Top-level results/ -> migrate to tasks/{task}/results/

  Run-result alignment:
    - Run without results -> flag as pending
    - Result without run -> flag as orphaned

**Build proposal table:**

  | # | Current Path | Proposed Path | Reason |
  |---|-------------|---------------|--------|

  If nothing needs to change: "All files in correct locations."

**Ask user:** "Apply this reorganization? (yes/no)"

  NO: save proposal to organize-report.md, remind to run `organize verify` later. Stop.
  YES: execute moves, create symlinks, log to organize-report.md, proceed to Phase 3.

  Move rules:
    - Create missing folders first, then move/rename files.
    - Use relative symlinks for shared configs.
    - Do NOT move code/, code-dev/, cc-archive/ session files, paper/, or _old/.

---

Phase 3: Post-Reorganization Verification
==========================================

Runs after Phase 2 applies changes, or standalone via `organize verify`.

Perform these checks on all task .py and .sh files:

  **Import resolution:**
    All haifn/hainn imports in task scripts resolve to existing classes in code/.

  **Config reference check:**
    All FnClass/ModelClass names in config/ YAMLs exist in code/.

  **Relative path check:**
    All paths referenced in scripts (config/, results/, docs/) exist.
    Common post-reorg issue: scripts referencing old flat paths instead of
    the new task-folder paths (e.g., tasks/{task}.py -> tasks/{task}/{task}.py).

  **Symlink validity:**
    All symlinks in the project resolve to existing targets.

Append results to docs/organize-report.md Section 3.
Print summary: ERROR count, WARN count, PASS count.

For `organize verify` standalone: if docs/organize-report.md exists, read it
for context. Otherwise run Phase 1 scan first.

---

Phase 4: Project Diagram (optional)
=====================================

Generate a draw.io diagram of the project structure.
Requires drawio MCP server. If unavailable, skip with a note:
  "Skipping diagram -- drawio MCP not installed.
   Run: claude mcp add drawio -- npx @next-ai-drawio/mcp-server@latest"

  mxGraphModel XML conventions:
    - Root node: PROJECT_ID, rounded rect, fill=#dae8fc (light blue), fontStyle=1
    - Mandatory folders (tasks/, docs/): fill=#d5e8d4 (green)
    - Task subfolders: fill=#fff2cc (yellow), sub-label with run/config counts
    - sbatch/: fill=#ffe6cc (orange)
    - paper/: fill=#e1d5e7 (light purple)
    - _old/ and non-standard dirs: fill=#f5f5f5 (grey), dashed edge
    - All edges: edgeStyle=orthogonalEdgeStyle
    - Cell IDs: short unique (p1, cc1, t1, t_task1, ...)
    - Target size: ~1200x900 px

  MCP call sequence:
    1. start_session
    2. create_new_diagram with the mxGraphModel XML
    3. export_diagram  path=docs/project-diagram.drawio  format=drawio
    4. export_diagram  path=docs/project-diagram.png     format=png

---

MUST NOT
---------

- Do NOT move files in code/, code-dev/ -- read only
- Do NOT move cc-archive/ session files or paper/ or _old/
- Do NOT apply moves without explicit user YES
- Do NOT modify YAML config content (moves OK, edits not)
- Do NOT create new .py scripts -- organize only moves existing files
