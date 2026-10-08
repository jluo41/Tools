# `audit` · read-only Project-root compliance

Audit one Project or every active Project under `examples/`.

```text
/haipipe-project audit <project>
/haipipe-project audit --all
```

Read `../ref/project-structure.md`, then run:

```text
python3 <haipipe-project>/scripts/audit_projects.py <project>
python3 <haipipe-project>/scripts/audit_projects.py --all --root <workspace>/examples
```

The audit checks only root facts: README, manifest schema, id, profile, Git
mode, state, mission, allowed worlds, profile-owned code roots, and declared
migration debt. Inside `cowork/` it also checks each CoWork Block `bNN_<topic>/`:
a `board.md` declaring `board-kind: cowork-block`; only `studio/`, `reports/`,
`_old/` and `jNN_<job>/` Jobs at its top (no `README.md` or `PEOPLE.md`); a
`j00_people/`; and each Job's `jNN_<job>.md` page declaring `job-kind: cowork-job`, with
only `design/`, `materials/`, `emails/`, `meetings/`, `_old/` inside. An old numbered
topic folder is a finding. It does not inspect
BJTR, Discovery, Paper, Application, Board, Page, or Run internals: the ladder audit
below does that.

Report `ok`, `debt`, or `failed` per Project. A declared legacy path is
`debt`, not `ok`; an undeclared noncanonical root is a finding. Exclude
`_backup`.

This verb never writes manifests or moves paths. Route requested changes to
`update`.


## Any level · the ladder audit

Point it at a Block, a Job, a Task or a Run (or a Project or world to walk all of them).
The level comes from the folder name: `bNN_` Block, `jNN_` Job, `tNN_` Task, a folder in
`runs/` a Run. The rules are one table, `../ref/ladder.md`; the script only reads it.

```text
/haipipe-project audit <Block|Job|Task|Run>
python3 <haipipe-project>/scripts/ladder.py audit <path> [--only] [--quiet] [--summary]
python3 <haipipe-project>/scripts/audit_projects.py <project> --deep     root report + counts per level
```

`--only` checks that level alone, `--quiet` hides folders that are ok all the way down,
`--summary` prints counts per level. It walks `tasks/`, `discoveries/` and `labelings/`;
`cowork/` keeps the check above; `papers/`, `designs/` and `insights/` keep their family layouts.

It checks the **shape** at every level: the face, which folders sit where, the child
prefixes, hard and soft Runs in the right places, `run.yaml` against its folder, the old
`runs/<run>.sh` + `results/<run>/` layout, dated soft names, heavy files in a Result
(AGENTS rule 10) and absolute paths in tickets, cards and receipts (rule 7). The owning
skill still judges the **content**. Each finding is `failed` or `debt`
(`../ref/ladder.md` § What the audit reports); a folder takes its worst finding.

```text
tasks/b00_<topic>/                       ok
  j51_<job>/                             debt
      · no face j51_<job>.md
    t07_<task>/                          debt
        · 8 Run(s) in the old layout (runs/<run>.* + results/<run>/)
```

Read-only. Fixes go through `update`.
