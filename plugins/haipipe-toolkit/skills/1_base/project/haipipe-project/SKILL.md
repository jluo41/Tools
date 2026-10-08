---
name: haipipe-project
description: >-
  Create, inspect, audit, or safely update project containers under examples/ or a sibling domain world such as examples-nlp/.
  Owns the Project boundary, README.md, project.yaml, project profile and Git
  mode, and the optional top-level worlds tasks/, discoveries/, cowork/,
  papers/, insights/, designs/, labelings/, and external/, plus platforms/ for code repos. Use for new projects, repository
  topology, project structure reviews, compliance previews, or root-level
  migrations. Child-world internals remain owned by their domain skills.
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "0.11.0"
  last_updated: "2026-10-06"
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
├── cowork/         optional/lazy · coordination text: tickets, people, emails,
│                   meetings, design notes; one CoWork Block per topic,
│                   bNN_<topic>/board.md + jNN_<job>/ Jobs (haipipe-cowork)
├── platforms/      optional/lazy · project-owned code repos as submodules
│                   (software and hybrid profiles only)
├── papers/         optional/lazy · academic consumers
├── insights/       optional/lazy · older register-kind Insight boards (new: a tasks/ Block)
├── designs/        optional/lazy · Design boards and folders
├── labelings/      optional/lazy · labeling Blocks; a Job is one dataset with one label
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

/haipipe-project audit [<project>|--all|<Block|Job|Task|Run>] [--deep]
    Read-only. A Project: root compliance (--deep adds counts per level). A Block,
    Job, Task or Run: its shape against the ladder, down to each Run. Read fn/audit.md.

/haipipe-project update [<project>|--all|<Block|Job|Task>] [--apply]
    A Project: add or reconcile the root contract; record unsafe moves as migration
    debt. Below it: a dry run of the move to one folder per Run and the missing
    run.yaml cards; --apply does it. Read fn/update.md.

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
insights/       → haipipe-insight    older register-kind <Dataset>-InsightBoard/ only (new work: an Insight Block in tasks/)
designs/        → haipipe-design     Design boards and Design Folders
labelings/      → subjective-label   bNN_<block>/ Blocks; a Job jNN_<dataset>_<label>/
cowork/         → this skill owns the boundary; haipipe-cowork owns each bNN_ Block
platforms/      → each repo owns its code; this skill owns only the link
external/       → this skill owns only the read-only root boundary
```

Insight and Design are peer worlds (JL 261001: "no more applications"). An
Insight topic is one task Block (JL 261005; the Prototype + Instance pair is retired):
`tasks/b5N_<topic>_dikw/` with `workbench: insight` in its board.md, one Job per DIKW
level, one Task per question holding its question, its one script, its runs and its
answering page. A new dataset is a new `datasets:` entry, never a copy of the code.

```text
tasks/
└── b5N_<topic>_dikw/               an Insight Block: board-kind: task-block · workbench: insight
    ├── board.md                    datasets: {<name>: <extract .parquet>, …}
    ├── meta/                       meta.md · partitions.md · thresholds.yaml · status.md (generated)
    ├── j01_data/ … j04_wisdom/     one Job per level; one Task per question:
    │                               question.md · scripts/ · runs/<dataset>_<partition>.sh · the page
    └── studio/                     question-map.excalidraw (generated) and hand sketches
insights/
└── <Dataset>-InsightBoard/         older register-kind board, until carried over
```

The internals (question file, run, report, status) belong to `haipipe-insight`
(`ref/block-contract.md`). An older register-kind board, `<Dataset>-InsightBoard/`,
keeps its layout in `insights/` and runs its code from `tasks/`. A
Design board reads a signed Insight handoff. `applications/`
is legacy: old boards move to `insights/_old/` and `designs/_old/`. Task-side
consumer-neutral Insight Pages still live on their Task Board. `results/` is
never a canonical Project-root directory.

`diagram/` is retired (JL 261003: "no more diagram"). Coordination text and
project-level Boards go to `cowork/`; code the Project owns goes to
`platforms/`, one submodule per repo. An existing `diagram/` is declared
migration debt, like `applications/`; no routine update moves its Boards.

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
provides deterministic root checks.

## The ladder below the root

Below the root this skill checks **shape only**, at every level: Block → Job → Task →
Run → pass. `ref/ladder.md` is the one table (each level's face, the folders it may hold,
its children, hard and soft Run names, family extras), read by `scripts/ladder.py`. The
child-world owner still owns **content** (a Page's sections, a ticket's body, a Run's
close rule); route those requests to it. What a Run is, hard or soft, with its passes and
`run.yaml`: haipipe-run.

## Return

```text
status:    ok | debt | blocked | failed
summary:   what was created, reconciled, or found
artifacts: paths changed or inspected
next:      safest concrete next action
```
