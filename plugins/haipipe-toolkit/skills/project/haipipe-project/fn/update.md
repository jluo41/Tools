# `update` · reconcile an existing Project root safely

Update root contracts without silently migrating child-owned or generated
material.

```text
/haipipe-project update <project>
/haipipe-project update --all
```

## Safe mutations

- Add a missing `project.yaml` from observable facts and the Project README.
- Add a missing `README.md` with a short mission and real current entry points.
- Correct manifest id or Git mode when disk evidence is decisive.
- Add explicit migration debt for legacy root paths.
- Remove stale root-layout prose from README when it points to retired worlds.

Do not overwrite a person's narrative beyond the stale structural statement
being reconciled.

## Never routine-update

- Move or rename a Git submodule.
- Move generated Results or notebooks.
- Convert old pipelines into BJTR.
- Move an active Board or rewrite child-world internals.
- Rename `paper/`, `insights/`, or another legacy root without its owner's
  migration plan and explicit approval.

For those cases, record `migration.status: needed`, list the exact paths, and
explain the proposed owner/destination. Acknowledged debt is safer than a false
`ok`.

Run `scripts/audit_projects.py` before and after. Return changed paths,
remaining debt, and the narrowest owner-specific migration to do next.
