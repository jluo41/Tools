fn-organize: File Inventory + Reorganization + Verification
=============================================================

Inventories project files, proposes reorganization to standard layout,
applies changes if approved, and verifies paths after moves.

Writes to: docs/organize-report.md, tasks/README.md, group README.md (after reorg)
File moves: examples/{PROJECT_ID}/ only (with user approval)
Read-only: code/, code-dev/

---

Step 0: Identify Target Project
=================================

Follow the auto-detection rules in SKILL.md.
Confirm PROJECT_PATH and PROJECT_ID.

---

Phase 1: File Inventory
========================

Goal: produce a complete picture of all project-related files.

**Step 1a -- Project folder inventory:**
  Walk examples/{PROJECT_ID}/ recursively (skip _old/).
  Group by top-level folder. For tasks/: list each group folder and its task
  subfolder contents (*.py, config/, runs/, results/).
  Flag task folders not inside a group folder.
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
    - .py/.sh at project root -> move to tasks/{G}_{group}/{task}/
    - YAML outside task config/ -> move to tasks/{G}_{group}/{task}/config/
    - Non-.md in cc-archive/ -> move to appropriate folder

  tasks/ layout:
    - Flat task folders in tasks/ -> create group folder, move tasks inside
    - Missing group README.md -> create
    - Per-task: missing *.py, README.md, bash scripts outside runs/,
      results outside results/

  Config ownership:
    - Each task must have its own config/ with real YAML files
    - If config/ is a symlink -> flag, propose copying to make it independent

  Legacy layout:
    - Top-level config/ -> distribute to task or group folders
    - Top-level results/ -> migrate to tasks/{G}_{group}/{task}/results/

  Run-result alignment:
    - If runs/ exists: run without results -> flag as pending
    - If runs/ exists: result without run -> flag as orphaned
    - If no runs/: results/ with flat files or default/ -> OK

**Build proposal table:**

  | # | Current Path | Proposed Path | Reason |
  |---|-------------|---------------|--------|

  If nothing needs to change: "All files in correct locations."

**Ask user:** "Apply this reorganization? (yes/no)"

  NO: save proposal to organize-report.md, remind to run `organize verify` later. Stop.
  YES: execute moves, log to organize-report.md, proceed to Phase 3.

  Move rules:
    - Create missing folders first, then move/rename files.
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
    the new group/task paths (e.g., tasks/{task}/ -> tasks/{G}_{group}/{task}/).

  **No symlinks:**
    Flag any config/ symlinks -- each task should own its own config files.

Append results to docs/organize-report.md Section 3.
Print summary: ERROR count, WARN count, PASS count.

For `organize verify` standalone: if docs/organize-report.md exists, read it
for context. Otherwise run Phase 1 scan first.

---

Phase 4: Targeted --fix Modes
==============================

Each --fix mode runs INSTEAD of the full Phase 1-3 flow when invoked
explicitly. The full flow handles general layout drift; these modes
handle specific structural transitions.

ALL modes still print a change plan first and require explicit user YES.

---

--fix flat-tasks
----------------
  For each task folder directly under tasks/ (no group letter prefix):
    1. Ask the user which group letter G to use, or infer from task name.
    2. Create tasks/{G}_{group_name}/ if absent.
    3. git mv the flat task into it, renaming the prefix to {G}{N}_.
  Plan: list of {old_path} -> {new_path} pairs.

---

--fix renumber
--------------
  Within each group, reassign N digits to fill gaps and reflect intended
  order. Ask the user for desired order if ambiguous.
  Plan: list of {G}{N_old}_name -> {G}{N_new}_name renames.

---

--fix paired
------------
  Two sub-checks:
  (a) Auto-example pairing — every Track A stub has a paired Track B
      example task. If missing, scaffold the paired task via
      Skill("haipipe-project-new", "task ...") with diagram/ included.
  (b) Logging-header conformance — every runs/*.sh begins with the
      standard logging header (see project-structure.md). If missing,
      prepend the header (preserving the rest of the script).

---

--fix migrate-to-diagram        (ONE-TIME README → diagram/ migration)
------------------------

  Migrates a project from the legacy README.md doc surface to the new
  diagram/ surface. Idempotent: safe to re-run.

  Step M1 — Project root
    If examples/{PROJECT}/tasks/README.md exists:
      Parse its three sections (flow graph, directory tree, status table).
      Create examples/{PROJECT}/diagram/ if absent.
      Seed three .txt files via /diagram-ascii:
        Skill("diagram-ascii",
          "Convert the project README at {tasks/README.md path} into the
           project-level story diagram. Produce three .txt files in
           {PROJECT}/diagram/:
             01-story.txt        — re-frame the README intro as a research
                                   narrative (motivation + research question
                                   + expected impact). Drop status tables;
                                   they belong in {task}/diagram/03-runs.
             02-boundary.txt     — extract scope (in / out / definitions)
                                   from the README intro; ASK user if not
                                   clearly present.
             03-exploration.txt  — convert the status table rows into
                                   'Active' / 'Backlog' / 'Tried' bullets,
                                   high-level only (no per-run rows).
           Project-level diagram is HIGH-LEVEL ONLY. Do NOT copy task
           tables, run logs, or file-level detail into these files.")
      Bundle:
        Skill("diagram-ascii-canvas",
          "Bundle {PROJECT}/diagram/ into {PROJECT}/diagram/project.excalidraw")
      git rm tasks/README.md.

  Step M2 — Group folders
    For each tasks/{G}_{group}/README.md:
      git rm. Group folders no longer have READMEs. Any unique content
      (purpose blurb, flow within group) is folded into the project-level
      03-exploration.txt or the per-task 01-overview.txt — ASK user where
      the content should go before deletion if README has substantive prose.

  Step M3 — Task folders
    For each {task}/README.md:
      Parse the five sections (What / Why / Inputs / Outputs / Runs).
      Create {task}/diagram/ if absent.
      Seed via /diagram-ascii:
        Skill("diagram-ascii",
          "Convert the task README at {task}/README.md into a 4-file task
           diagram folder. Produce in {task}/diagram/:
             01-overview.txt   — copy What / Why / Inputs / Outputs verbatim
                                 into ─§ sections; one block each, 1-3 lines.
             02-design.txt     — extract the Architecture section if present
                                 (Stage 5 tasks). Otherwise seed with TODO
                                 + a 1-line summary of the .py logic.
             03-runs.txt       — copy the Runs table into a single section.
                                 If status values use the old vocabulary
                                 (todo|wip|done|deprecated), map todo→planned.
             04-progress.txt   — start a fresh dated log, seed with one entry:
                                 '{YYMMDD} — migrated from README.md'.")
      Bundle:
        Skill("diagram-ascii-canvas",
          "Bundle {task}/diagram/ into {task}/diagram/task.excalidraw")
      git rm {task}/README.md.

  Step M4 — paper/ folders (if any)
    For each paper/Paper-*/:
      Create diagram/ if absent. Seed via /diagram-ascii:
        Skill("diagram-ascii",
          "Write the paper-level diagram for {paper-folder-name}. Produce in
           {paper-folder}/diagram/:
             01-overview.txt    — sections + headline claims; ASK user.
             02-figure-plan.txt — figure list + status; seed empty if unknown.
             03-rebuttal.txt    — only if the project is in rebuttal phase.")
      Bundle to paper.excalidraw.

  Step M5 — Report migration summary:
    READMEs removed, diagram/ folders created, .excalidraw files bundled.

  ⚠️ This is a content-bearing migration. Always run --dry-run first.
  ⚠️ Commit before running so the README content stays in git history.

---

--fix drop-legacy
-----------------
  Remove top-level legacy folders that are no longer part of the standard
  layout: docs/, cc-archive/, _old/.

  For each:
    - If empty: git rm -r.
    - If non-empty: ASK user. Options:
        (a) Move worth-keeping files elsewhere (which?) and git rm the rest.
        (b) Leave alone (skip for now).
        (c) git rm -r without preserving (last-resort; user must confirm).
    - cc-archive/ session files: usually safe to drop — they're conversation
      logs, not source. Confirm before removing.

  Plan: list of paths to remove + disposition for non-empty folders.

---

MUST NOT
---------

- Do NOT move files in code/, code-dev/ -- read only.
- Do NOT move paper/ contents (paper/ may be a submodule).
- Do NOT apply moves without explicit user YES.
- Do NOT modify YAML config content (moves OK, edits not).
- Do NOT create new .py scripts -- organize only moves existing files.
- Do NOT re-run --fix migrate-to-diagram on an already-migrated project
  without --dry-run first; the tool is idempotent but the user should see
  the empty plan before re-confirming.

---

Next Steps
-----------

After organize:
  - To validate code sync and verify migration:  /haipipe-project review
  - To see a task-by-task summary:                /haipipe-project overview
  - If --fix migrate-to-diagram was applied:      open the bundled
                                                  .excalidraw files and
                                                  spot-check the canvases
