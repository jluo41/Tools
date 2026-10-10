---
name: haipipe-project
description: >-
  Create, inspect, audit, or safely update project containers under examples/ or a sibling domain world such as examples-nlp/.
  Owns the Project boundary, README.md, project.yaml, project profile and Git
  mode, and the optional top-level worlds work/, discovery/, cowork/,
  paper/, insight/, design/, labeling/, ideation/, and external/, plus platforms/ for code repos. Use for new projects, repository
  topology, project structure reviews, compliance previews, and root-level migrations:
  `audit` flags what an existing Project or SPACE is missing against the current contract
  (old plural Theme folders, flat Runs, missing faces) and the step that fixes it, `update`
  plans the fix as a dry run, `update --apply` applies it. Child-world internals remain
  owned by their domain skills.
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "0.14.0"
  last_updated: "2026-10-09"
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
├── work/          optional/lazy · computational evidence bank
├── discovery/    optional/lazy · external-evidence bank
├── cowork/         optional/lazy · coordination text: tickets, people, emails,
│                   meetings, design notes; one CoWork Block per topic,
│                   bNN_<topic>/board.md + jNN_<job>/ Jobs (haipipe-cowork)
├── platforms/      optional/lazy · project-owned code repos as submodules
│                   (software and hybrid profiles only)
├── paper/         optional/lazy · academic consumers
├── insight/       optional/lazy · older register-kind Insight boards (new: a work/ Block)
├── design/        optional/lazy · Design boards and folders
├── labeling/      optional/lazy · labeling Blocks; a Job is one dataset with one label
├── ideation/      optional/lazy · Ideation directions (bNN/jNN/tNN, no Runs)
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
    Read-only. A Project: every finding and the update step that fixes it (root, singular
    Theme folders, Job-centred layout, one folder per Run, faces), what a person decides,
    and the Tools gate. A Block, Job, Task or Run: its shape against the ladder, down to
    each Run. Read fn/audit.md.

/haipipe-project update [<project>|--all|<Block|Job|Task>] [--apply]
    A dry run unless --apply. A Project: every step audit found work for, in order (root,
    themes, convert, runs, faces); --apply runs them, re-audits after each, verifies tickets
    and links, and never commits. Below it: the move to one folder per Run and the missing
    run.yaml cards. Read fn/update.md.

/haipipe-project feedback "<text>"
/haipipe-project digest [session] [--dry-run]
    Existing feedback capture and confirmed transcript harvest.

/haipipe-project
    List active Projects, profile, Git mode, state, and migration status.
```

## Boundary and ownership

```text
work/          → haipipe-task       BJTR execution; Task = Page; Run = identity
discovery/    → haipipe-discovery  Discovery BJTR and Paper/Source Runs
paper/         → haipipe-paper      academic consumer
insight/       → haipipe-insight    older register-kind <Dataset>-InsightBoard/ only (new work: an Insight Block in work/)
design/        → haipipe-design     Design boards and Design Folders
labeling/      → subjective-label   bNN_<block>/ Blocks; a Job jNN_<dataset>_<label>/
ideation/      → haipipe-ideation   one direction per Task; its Runs live in work/ or discovery/
cowork/         → this skill owns the boundary; haipipe-cowork owns each bNN_ Block
platforms/      → each repo owns its code; this skill owns only the link
external/       → this skill owns only the read-only root boundary
```

Insight and Design are peer worlds (JL 261001: "no more applications"). An
Insight topic is one task Block (JL 261005; the Prototype + Instance pair is retired):
`work/b5N_<topic>_dikw/` with `workbench: insight` in its board.md, one Job per DIKW
level, one Task per question holding its question, its one script, its runs and its
answering page. A new dataset is a new `datasets:` entry, never a copy of the code.

**Current Insight layout (haipipe-insight, 261009):** a topic's Prototype is a task-world Block
`work/Prototype-bNN-<Topic>/` (`board-kind: prototype`, a Job per release, `proposals/`) and each
dataset is a Board `insight/Insight-<name>/`. haipipe-insight's SKILL.md is the authority; the
`b5N_<topic>_dikw` Block below is its older layout (`ref/prototype_from_block.py` carries it).

```text
work/
└── b5N_<topic>_dikw/               an Insight Block: board-kind: task-block · workbench: insight
    ├── board.md                    datasets: {<name>: <extract .parquet>, …}
    ├── meta/                       meta.md · partitions.md · thresholds.yaml · status.md (generated)
    ├── j01_data/ … j04_wisdom/     one Job per level; one Task per question:
    │                               question.md · scripts/ · runs/<dataset>_<partition>.sh · the page
    └── studio/                     question-map.excalidraw (generated) and hand sketches
insight/
└── <Dataset>-InsightBoard/         older register-kind board, until carried over
```

The internals (question file, run, report, status) belong to `haipipe-insight`
(`ref/block-contract.md`). An older register-kind board, `<Dataset>-InsightBoard/`,
keeps its layout in `insight/` and runs its code from `work/`. A
Design board reads a signed Insight handoff. `applications/`
is legacy: old boards move to `insight/_old/` and `design/_old/`. Task-side
consumer-neutral Insight Pages still live on their Task Board. `results/` is
never a canonical Project-root directory.

`diagram/` is retired (JL 261003: "no more diagram"). Coordination text and
project-level Boards go to `cowork/`; code the Project owns goes to
`platforms/`, one submodule per repo. An existing `diagram/` is declared
migration debt, like `applications/`; no routine update moves its Boards.

## Safe update law

- Add a missing `project.yaml` or `README.md` when the user asks to update.
- Reconcile facts that are observable on disk; do not invent ownership or state.
- Treat `applications/`, root `results/`, old pipeline roots, and misplaced
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
