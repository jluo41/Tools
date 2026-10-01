---
name: haipipe-project
description: >-
  Create, inspect, audit, or safely update project containers under examples/ or a sibling domain world such as examples-nlp/.
  Owns the Project boundary, README.md, project.yaml, project profile and Git
  mode, and the optional top-level worlds tasks/, discoveries/, diagram/,
  papers/, insights/, designs/, and external/. Use for new projects, repository
  topology, project structure reviews, compliance previews, or root-level
  migrations. Child-world internals remain owned by their domain skills.
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "0.5.0"
  last_updated: "2026-10-01"
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

# /haipipe-project · own the Project boundary

One Project is one durable research or software boundary. This skill owns only
the root contract; it never restates or rewrites the internal grammar of a
Task, Discovery, Paper, Application, Page, or Run.

## Canonical root

```text
examples/ProjNN-<domain>-<purpose>/
├── README.md       required human entry
├── project.yaml    required machine contract
├── tasks/          optional/lazy · computational evidence bank
├── discoveries/    optional/lazy · external-evidence bank
├── diagram/        optional/lazy · story, Boards, and meetings
├── papers/         optional/lazy · academic consumers
├── insights/       optional/lazy · one InsightBoard per dataset
├── designs/        optional/lazy · Design boards and folders
└── external/       optional/lazy · pinned, read-only upstream material
```

Do not create empty world directories merely to satisfy a skeleton. Git cannot
preserve them without placeholder noise; the owning skill creates a world when
the first real artifact is requested.

Two independent declarations replace name-based inference:

```yaml
profile: research | software | hybrid
git_mode: workspace | submodule
```

`profile` says what may live at the root. `git_mode` says how the Project is
stored. A `Proj...` name does not imply either value.

Read `ref/project-structure.md` before creating, auditing, or updating a Project.

## Commands

```text
/haipipe-project new <id> [--profile <profile>] [--git-mode workspace]
    Create README.md + project.yaml. Create no empty worlds. Read fn/project.md.

/haipipe-project repo <id> --org <owner> [--profile <profile>]
    Create or adopt a repo-backed Project and record git_mode: submodule.
    Read fn/repo-project.md. `repo` is explicit authorization for that topology;
    the Project name is not a router.

/haipipe-project audit [<project>|--all]
    Read-only Project-root compliance report. Read fn/audit.md.

/haipipe-project update [<project>|--all]
    Add or reconcile the root contract without moving legacy code, Results, or
    submodules. Record unsafe moves as migration debt. Read fn/update.md.

/haipipe-project feedback "<text>"
/haipipe-project digest [session] [--dry-run]
    Existing feedback capture and confirmed transcript harvest.

/haipipe-project
    List active Projects, profile, Git mode, state, and migration status.
```

## Boundary and ownership

```text
tasks/          → haipipe-task       BJTR execution; Task = Page; Run = identity
discoveries/    → haipipe-discovery  Discovery BJTR and Paper/Source Runs
papers/         → haipipe-paper      academic consumer
insights/       → haipipe-insight    <Dataset>-InsightBoard/, one per extract
designs/        → haipipe-design     Design boards and Design Folders
diagram/        → haipipe-board / haipipe-page plus Project story surfaces
external/       → this skill owns only the read-only root boundary
```

Insight and Design are peer worlds (JL 261001: "no more applications"). An
InsightBoard reads one dataset and keeps its questions, reports and light run
results inside its `insights/<Dataset>-InsightBoard/` folder; the code it runs
stays in `tasks/`. A Design board reads a signed Insight handoff. `applications/`
is legacy: old boards move to `insights/_old/` and `designs/_old/`. Task-side
consumer-neutral Insight Pages still live on their Task Board. `results/` is
never a canonical Project-root directory.

## Safe update law

- Add a missing `project.yaml` or `README.md` when the user asks to update.
- Reconcile facts that are observable on disk; do not invent ownership or state.
- Treat `paper/`, `applications/`, root `results/`, old pipeline roots, and misplaced
  submodules as migration debt until their owner and destination are resolved.
- Never move a submodule, generated Result bank, or large code tree as part of a
  routine update. Report the exact source, proposed destination, and required
  pointer/config edits first.
- A manifest that acknowledges legacy paths is honest but not fully compliant.
- Exclude `examples/_backup/` from active-project audit and update.

`fn/update.md` owns the exact mutation boundary. `scripts/audit_projects.py`
provides deterministic root checks. Route any deeper request to the child-world
owner instead of extending this skill downward.

## Return

```text
status:    ok | debt | blocked | failed
summary:   what was created, reconciled, or found
artifacts: paths changed or inspected
next:      safest concrete next action
```
