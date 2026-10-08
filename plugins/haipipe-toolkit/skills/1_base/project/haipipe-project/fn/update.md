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


## Any level · one folder per Run

`update` also takes a Block, a Job, a Task or a Run. It is a dry run that prints every
move; nothing changes until `--apply`.

```text
/haipipe-project update <Block|Job|Task> [--apply]
python3 <haipipe-project>/scripts/ladder.py update <path> [--apply]
```

What it may do, in each `runs/` below the path:

1. **Old layout → one folder per Run.** A hard Run's `runs/<run>.sh` (and a same-stem
   `.yaml`) moves into `runs/<run>/`, and `results/<run>/` moves whole to
   `runs/<run>/result/`. A soft Run's dated tickets on one target
   (`run-<type>-<target>.md`) become one Run, `runs/run-<type>-<target>/`: each date
   is a pass (`passes/pNN-<MMDD>/`, holding that date's old result folder and its ticket
   as `ask.md`); the latest ticket becomes the Run's ticket. An emptied `results/` is removed.
2. **The card.** It writes `run.yaml` for every Run that has none, from its ticket and
   receipt, with `moved_from:` naming the old paths. Unknown fields stay null.
3. **Skips.** A name that is neither hard nor soft (`re-…`, `rdNN_…`, `riNN_…`) is listed,
   not moved: its owner maps it (haipipe-run `ref/run-catalog.md`). A destination that
   exists is never overwritten.

A move never edits a file inside a Result (AGENTS rule 0): folders move whole, and a
receipt keeps the old path it recorded as history, with `run.yaml` `moved_from:` pointing
back. Move one Block at a time, only after the owning skill's ticket template writes the
new layout (a ticket that still writes `results/<run>/` would recreate it). Run the ladder
audit before and after.
