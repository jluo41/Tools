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
migration debt. It does not inspect BJTR, Discovery, Paper, Application, Board,
Page, or Run internals.

Report `ok`, `debt`, or `failed` per Project. A declared legacy path is
`debt`, not `ok`; an undeclared noncanonical root is a finding. Exclude
`_backup`.

This verb never writes manifests or moves paths. Route requested changes to
`update`.
