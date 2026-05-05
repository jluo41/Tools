---
name: haipipe-project
description: "Run any project-level work in the haipipe workspace. Parses intent (build vs read vs modify) and dispatches to the right specialist (haipipe-project-task for scaffolding projects/task-groups/task-folders, -inspect for review/summary/inventory/overview, -organize for reorganizing files). Use for creating new projects/task-groups/task-folders (model-run, evaluation, paper figure/table, data-pipeline) under examples/, auditing structure, generating docs, reorganizing. Trigger: project scaffold, new task, new figure task, new evaluation task, project review, project summary, organize project, reorganize files, /haipipe-project."
argument-hint: [function] [project_id] [args...]
allowed-tools: Bash, Read, Grep, Glob, Skill
---

Skill: haipipe-project (orchestrator)
======================================

User-facing entry for project-level work. Routes by **risk profile**
(build / read / modify) — the three specialists differ in `allowed-tools`
and blast radius.

```
/haipipe-project                               -> overview of all projects under examples/
/haipipe-project task                          -> scaffold (asks: project / task-group / task-folder)
/haipipe-project task project <project_id>     -> scaffold a new project
/haipipe-project task task-group               -> scaffold a new task-group
/haipipe-project task task-folder              -> scaffold a new task-folder (asks task-type)
/haipipe-project review <project_id>           -> structural audit
/haipipe-project summarize <project_id>        -> generate summary doc
/haipipe-project inventory [project_id]        -> file inventory
/haipipe-project overview [project_id]         -> overview of one or all projects
/haipipe-project organize <project_id>                      -> reorganize files (modifies!)
/haipipe-project scan-status <task_dir> [key] [out_txt]     -> scan B01 eval, update status.json + txt
/haipipe-project "<natural language>"                       -> infer function, dispatch
```

---

Specialists
-----------

```
haipipe-project-task       BUILD:  scaffold project / task-group / task-folder (creates files)
haipipe-project-inspect    READ:   review, summarize, inventory, overview (no writes)
haipipe-project-organize   MODIFY: reorganize files (mv/rename, dry-run supported)
```

---

Two Structural Rules (cross-cutting; ref'd by all specialists)
---------------------------------------------------------------

Rule 1 — Three-level hierarchy (project → task-group → task-folder):
  `examples/{PROJECT_ID}/tasks/` contains task-groups: `{G}{NN}_{group_name}/`
    (e.g., `A01_pretraining_clm/`, `B01_evaluation_clm/`, `C01_paper_figures/`).
  Each task-group contains task-folders: `{NN}_{task_name}/`
    (e.g., `01_train_clm_num_modelsize/` inside `A01_pretraining_clm/`).
  Each task-folder is self-contained: `*.py`, `configs/`, `runs/`, `results/`,
    `notebooks/` (NO README.md — doc surface is `diagram/`).
  No flat task folders directly in `tasks/` — they must be inside a task-group.
  Group letter convention: A=model-run, B=evaluation, C=display, D=demo.

Rule 2 — Code always has a paired example:
  Every new pipeline Fn stub or ML model stub in Track A auto-generates
  a paired example task in `tasks/`.

These rules live in `ref/project-structure.md` and `ref/code-structure.md`,
which all three specialists read.

---

Function Verb Map
------------------

```
task, new, scaffold, create, init             -> haipipe-project-task
  (sub-scopes: project / task-group / task-folder; ask if missing)
review, audit, check, validate, lint          -> haipipe-project-inspect (review)
summarize, summary, docs                      -> haipipe-project-inspect (summarize)
inventory, list files, files                  -> haipipe-project-inspect (inventory)
overview, show, status                        -> haipipe-project-inspect (overview)
organize, reorganize, fix structure, move     -> haipipe-project-organize
scan-status, scan eval, eval status          -> haipipe-project-inspect (scan-status)
```

---

Routing Logic
-------------

```
Step 1: Parse $ARGUMENTS.

Step 2: Resolve function via verb map.
  - If verb is unambiguous -> done.
  - If first positional looks like a project_id (matches an existing
    examples/{X}/) and no verb -> default to overview for that project.
  - If no args at all -> overview across ALL projects (umbrella inline).

Step 3: Decide specialist:
  - task / new / scaffold                -> haipipe-project-task
  - review/summarize/inventory/overview  -> haipipe-project-inspect
  - organize                             -> haipipe-project-organize

Step 4: Dispatch:
    Skill("haipipe-project-<specialist>", args="<verb> <remaining_args>")

Step 5: Capture the structured tail and present.
```

---

Cross-Project Overview (no-arg case)
-------------------------------------

When invoked with no arguments, list all projects under `examples/` with
a one-line status per project (task count, last-modified, violations
flagged). Inline (no specialist dispatch needed for this lightweight view).

---

Disambiguation Rules
---------------------

  - Verb missing, project_id present -> default to `overview` for that id.
  - Verb missing, no args            -> cross-project overview (inline).
  - `organize` without project_id    -> ASK which project. Don't guess.
  - Multi-project ops (e.g. "review all") -> dispatch sequentially per project.

---

Specialist Return Contract
---------------------------

```
status:    ok | blocked | failed
summary:   2-3 sentences on what was done
artifacts: [paths created / read / moved]
next:      suggested next command
```

---

Files Owned by This Umbrella
-----------------------------

```
ref/project-structure.md   Track B layout (tasks/, configs/, runs/, results/, paper)
ref/code-structure.md      Track A layout (code-dev/, hainn/, haifn/) + paired-example rule
```

These ref files are SHARED across specialists. Each specialist reads them
when its function depends on the rules. The inventory helper scripts
(`ref/inventory/*.py`) live with `haipipe-project-inspect` since only that
specialist uses them.
