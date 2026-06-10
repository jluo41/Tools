fn-organize: File Inventory + Reorganization + Verification
=============================================================

Inventories project files, proposes reorganization to standard layout, applies moves with user approval, and verifies paths after.

Writes: docs/organize-report.md
Moves files only inside examples/{PROJECT_ID}/. code/ and code-dev/ are read-only.


Step 0 — Identify project
==========================
Auto-detect or ask. Confirm PROJECT_PATH and PROJECT_ID.


Phase 1 — File inventory
=========================
1a. Walk examples/{PROJECT_ID}/ recursively (skip _old/). Group by top
    folder. For tasks/, list each group folder + its task contents
    (*.py, configs/, runs/, results/, notebooks/). Flag flat tasks
    (not inside a group) and root-level files that belong inside tasks.
1b. For each FnClass/ModelClass in task configs/ YAMLs, locate the
    source file in code/. Reuse docs/data-map.md if present.
1c. Write Section 1 of organize-report.md.


Phase 2 — Proposed reorganization
==================================
Detect and propose fixes for:
- Missing mandatory folders (tasks/, diagram/) — create.
- .py / .sh at project root — move into a task folder.
- YAML outside task configs/ — move to {task}/configs/.
- Flat task folders in tasks/ — create group, move tasks inside.
- configs/ as symlink — flag, propose own copy (each task owns its YAMLs).
- Top-level configs/, results/ — distribute into the right tasks.
- runs/<run>.sh ↔ results/<run>/ orphans — flag.
- runs/*.sh missing logging header — flag.

Build proposal table: | # | Current Path | Proposed Path | Reason |.
"All files in correct locations." if nothing to change.

Ask: "Apply this reorganization? (yes/no)"
- NO: save proposal, remind to run `organize verify` later, stop.
- YES: execute moves, log to report, proceed to Phase 3.

Move rules: create missing folders first; never move code/, code-dev/,
cc-archive/ session files, paper/, _old/.


Phase 3 — Verification
=======================
Run after Phase 2 applies, or standalone via `organize verify`.

Checks on all task .py and .sh files:
- Import resolution: haifn/hainn imports resolve to existing classes
- Config refs: FnClass/ModelClass names exist in code/
- Relative paths: configs/, results/, docs/ paths in scripts exist
  (common post-reorg issue: scripts still reference old flat paths)
- No symlinks in configs/ — each task owns its own YAMLs

Append to Section 3 of report. Print ERROR/WARN/PASS counts.

For standalone `organize verify`: read existing report if present,
otherwise run Phase 1 first.


Phase 4 — Targeted --fix Modes
================================
Each --fix mode runs INSTEAD of the full Phase 1-3 flow. Each prints a
plan first and requires explicit user YES.

--fix flat-tasks
  For each task directly under tasks/ (no group prefix): ask which
  group letter to use (or infer from name); create tasks/{G}{NN}_{group}/;
  git mv the task into it, renumbering prefix to {NN}_.

--fix renumber
  Within each group, reassign NN to fill gaps and reflect intended order.
  Plan: list of {NN_old}_name → {NN_new}_name renames.

--fix paired
  (a) Auto-example: every Track A stub has a paired Track B example
      task. Scaffold missing ones via /haipipe-project task task-folder.
  (b) Logging-header: every runs/*.sh begins with the standard header
      (Template A) or papermill header (Template B). Prepend if missing.

--fix migrate-to-diagram   (one-time README → diagram/)
  Idempotent. Always run with --dry-run first; commit before applying.

  M1. Project root: parse tasks/README.md (flow / tree / status table).
      Create {PROJECT}/diagram/. Delegate to /diagram-ascii to seed
      01-story (research narrative), 02-boundary (in/out/definitions),
      03-exploration (status rows → Active/Backlog/Tried bullets).
      Bundle via /diagram-ascii-canvas. git rm the README.

  M2. Group folders: git rm each {group}/README.md. Substantive prose
      gets folded into project's 03-exploration or task's 01-overview;
      ASK user where it goes if non-trivial.

  M3. Task folders: parse {task}/README.md sections (What/Why/Inputs/
      Outputs/Runs). Create {task}/diagram/. /diagram-ascii seeds
      01-overview (verbatim copy), 02-design (Architecture section if
      Stage 5; else TODO + .py summary), 03-runs (Runs table; map
      old todo → planned), 04-progress (seed with "{YYMMDD} — migrated
      from README.md"). Bundle. git rm the README.

  M4. paper/ folders: create diagram/ if absent. /diagram-ascii seeds
      01-overview (sections + claims; ASK user), 02-figure-plan
      (figure list + status), 03-rebuttal (only during rebuttal).
      Bundle to paper.excalidraw.

  M5. Report: READMEs removed, diagrams created, canvases bundled.

--fix drop-legacy
  Remove legacy top-level: docs/, cc-archive/, _old/.
  Empty: git rm -r. Non-empty: ask user (preserve / leave / drop).
  cc-archive/ session files are usually safe to drop (conversation
  logs, not source) — confirm.


MUST NOT
=========
- Move files in code/ or code-dev/.
- Move paper/ contents (paper/ may be a submodule).
- Apply moves without explicit user YES.
- Modify YAML config content (moves OK, edits not).
- Create new .py scripts (organize only moves existing files).
- Re-run --fix migrate-to-diagram on a migrated project without
  --dry-run first.


Next steps
===========
- Validate code sync + verify migration: /haipipe-project review
- Task-by-task summary: /haipipe-project overview
- After --fix migrate-to-diagram: open .excalidraw files, spot-check canvases
