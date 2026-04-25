---
name: haipipe-project
description: "Run any project-level work in the haipipe workspace. Parses intent (build vs read vs modify) and dispatches to the right specialist (haipipe-project-new for scaffolding, -inspect for review/summary/inventory/overview, -organize for reorganizing files). Use for creating new projects under examples/, auditing structure, generating docs, reorganizing. Trigger: project scaffold, new experiment, project review, project summary, organize project, reorganize files, /haipipe-project."
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
/haipipe-project new <project_id>              -> scaffold a new project
/haipipe-project review <project_id>           -> structural audit
/haipipe-project summarize <project_id>        -> generate summary doc
/haipipe-project inventory [project_id]        -> file inventory
/haipipe-project overview [project_id]         -> overview of one or all projects
/haipipe-project organize <project_id>         -> reorganize files (modifies!)
/haipipe-project "<natural language>"          -> infer function, dispatch
```

---

Specialists
-----------

```
haipipe-project-new        BUILD: scaffold new project (creates files)
haipipe-project-inspect    READ:  review, summarize, inventory, overview (no writes)
haipipe-project-organize   MODIFY: reorganize files (mv/rename, dry-run supported)
```

---

Two Structural Rules (cross-cutting; ref'd by all specialists)
---------------------------------------------------------------

Rule 1 — Two-level task hierarchy:
  `tasks/` contains group folders: `{G}_{group_name}/` (e.g., `A_data/`, `B_training/`).
  Each group contains task folders: `{G}{N}_{name}/` (e.g., `B1_train_stats/`).
  Each task is self-contained: `*.py`, `config/`, `runs/`, `results/`, `README.md`.
  No flat task folders directly in `tasks/` — they must be inside a group.

Rule 2 — Code always has a paired example:
  Every new pipeline Fn stub or ML model stub in Track A auto-generates
  a paired example task in `tasks/`.

These rules live in `ref/project-structure.md` and `ref/code-structure.md`,
which all three specialists read.

---

Function Verb Map
------------------

```
new, scaffold, create project, init           -> haipipe-project-new
review, audit, check, validate, lint          -> haipipe-project-inspect (review)
summarize, summary, docs                      -> haipipe-project-inspect (summarize)
inventory, list files, files                  -> haipipe-project-inspect (inventory)
overview, show, status                        -> haipipe-project-inspect (overview)
organize, reorganize, fix structure, move     -> haipipe-project-organize
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
  - new                                  -> haipipe-project-new
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
