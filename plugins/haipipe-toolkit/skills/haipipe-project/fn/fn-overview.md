fn-overview: Task-by-Task Project Overview
============================================

Reads every task's README.md and produces a structured overview
of what the project does, organized by group.

Read-only: does NOT modify any files.

---

Step 0: Identify Target Project
=================================

Follow the auto-detection rules in SKILL.md.
Confirm PROJECT_PATH and PROJECT_ID.

---

Step 1: Read Project-Level Context
=====================================

Read these files (if they exist):

  tasks/README.md          <- flow graph, status table
  docs/TODO.md             <- task progress, paper status
  docs/data-map.md         <- pipeline stages, data flow

Extract:
  - Project purpose (first paragraph or flow graph header)
  - Paper venue + status (from TODO.md or tasks/README.md)
  - Pipeline stages used (from data-map.md)

---

Step 2: Walk Groups and Tasks
===============================

For each group folder in tasks/:

  1. Read {G}_{group}/README.md -> extract Purpose line
  2. For each task folder inside the group:
     a. Read {task}/README.md -> extract What, Why sections (1-2 lines each)
     b. If README.md is missing: infer purpose from task name
     c. Note: status (done/wip/stub) from group README task table
     d. Note: paper artifact if mentioned (Table N, Figure N, Rebuttal PN)

---

Step 3: Produce Overview
==========================

Output format (print directly, do NOT write to file):

  **Project header:**
    Project name, purpose, paper venue/status, pipeline stages.

  **Per group:**
    Group name, purpose, task count.

    Table with columns:
      | Task | What | Paper/Rebuttal | Status |

    - "What" = one sentence from README What section
    - "Paper/Rebuttal" = Table/Figure/Rebuttal point reference (or "—")
    - "Status" = done/wip/stub

  **Summary stats:**
    Total tasks, done count, wip count, stub count.

---

Step 4: Optionally Highlight Gaps
===================================

After the overview, note:
  - Tasks with missing README.md (can't describe them)
  - Tasks marked wip or stub (incomplete work)
  - Groups with no flow documented in group README

Keep this section brief (bullet list only).

---

MUST NOT
---------

- Do NOT write any files -- overview is printed to the user only
- Do NOT modify README.md files
- Do NOT run pipeline commands

---

Next Steps
-----------

After overview:
  - To fill gaps (missing README, .py): run /haipipe-project review
  - To reorganize files: run /haipipe-project organize
  - To generate a project summary: run /haipipe-project summarize
