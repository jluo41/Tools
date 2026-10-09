# `update` · reconcile an existing Project root safely

Update root contracts without silently migrating child-owned or generated
material.

```text
/haipipe-project update <project>|--all             dry run of every step (below), and what a person decides
/haipipe-project update <project>|--all --apply     run the steps in order; verify; never commit
```

Always `audit` first (fn/audit.md): it names the step that fixes each finding. The steps are in
§ A Project · the steps; the root-only mutations are the first of them.

## Safe mutations

- Add a missing `project.yaml` from observable facts and the Project README.
- Add a missing `README.md` with a short mission and real current entry points.
- Correct manifest id or Git mode when disk evidence is decisive.
- Add explicit migration debt for legacy root paths.
- Remove stale root-layout prose from README when it points to retired worlds.

Do not overwrite a person's narrative beyond the stale structural statement
being reconciled.

## Never routine-update

Outside the stepped Project update below (which does each of these only for the layouts it names,
after `audit`, as a dry run first):

- Move or rename a Git submodule.
- Move generated Results or notebooks.
- Convert old pipelines into BJTR.
- Move an active Board or rewrite child-world internals.
- Rename a legacy root without its owner's migration plan and explicit approval. A plural Theme
  folder is renamed only by `scripts/rename_themes.py` (see Theme names below).

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
3. **The ticket.** A moved hard `.sh` ticket gets one comment line and one more `dirname` on its
   own path, so it resolves its Task, Job and Block as it did from `runs/`; its `results/$RUN…`
   becomes `runs/$RUN…/result`. A ticket that builds `TICKET` from `dirname "$0"` keeps that line
   as is. A Job-level Result `<job>/results/<task>/<run>/` is found and moved too.
4. **Relink.** References to each moved Result and ticket are rewritten in hand-written text under
   every `examples*/` world (Markdown, yaml, py, sh, json, tex): `<task>/results/<run>` and
   `results/<task>/<run>` → `<task>/runs/<run>/result`; inside the Task, `results/<run>` →
   `runs/<run>/result`; `runs/<run>.sh` → `runs/<run>/<run>.sh`. Never inside a Result, `passes/`,
   `notebooks/`, `delivery/`, `_legacy/`, `_old/`, or a file marked generated.
5. **Tidy.** A retired `diagram/` (or `diagram-<topic>/`) goes to `studio/` (links to what it held
   follow it), a Job's `notebooks/<task>/` into that Task's `notebooks/`, a Job's `workflow/` to the
   Job's `_old/workflow/`.
6. **Skips.** A name that is neither hard nor soft (`re-…`, `rdNN_…`, `riNN_…`) is listed,
   not moved: its owner maps it (haipipe-run `ref/run-catalog.md`). A destination that
   exists is never overwritten.

A move never edits a file inside a Result (AGENTS rule 0): folders move whole, and a
receipt keeps the old path it recorded as history, with `run.yaml` `moved_from:` pointing
back. Move one Block at a time, only after the owning skill's ticket template writes the
new layout (a ticket that still writes `results/<run>/` would recreate it). Run the ladder
audit before and after.


## Theme names · rename_themes.py

```text
python3 <haipipe-project>/scripts/rename_themes.py <project> [--list] [--apply]
```

Moves `tasks/` → `work/`, `discoveries/` → `discovery/`, `papers/` → `paper/`, `insights/` → `insight/`,
`designs/` → `design/`, `labelings/` → `labeling/`, `ideations/` → `ideation/` (s01-D29). The folder is
renamed on disk like the ladder's moves; a submodule inside moves by `git mv`. Each moved ticket's
check that its world is named `tasks` also accepts `work` (its store address does not change), and
hand-written references follow: `<Project>/<old>/` anywhere, a bare `<old>/` path inside the Project;
never inside a Result, a receipt, a frozen Design `inputs/`, an archive or a generated file. A pair
whose new folder exists is refused. Run the root and ladder audits after.


## A Project · the steps

`update` at Project level dry-runs every step `audit` found work for; `--apply` runs them in this
order, re-runs the ladder audit after each and stops if its failures rose, then verifies.

```text
python3 <haipipe-project>/scripts/project.py update <project>|--all [--root <SPACE>]
python3 <haipipe-project>/scripts/project.py update <project> --apply [--steps root,themes,…] [--state <dir>]
```

```text
tools    gate   the Tools this SPACE runs must read the new layout (the Ticket template writes
                runs/<run>/result/ and accepts work/), and the audit's worlds must match the decided
                Theme names (haipipe-page src/themes.py); otherwise --apply refuses and changes nothing
root     auto   README.md and project.yaml from disk; mission "open" when no README says it
themes   auto   tasks/ → work/, discoveries/ → discovery/, papers/ → paper/ … (scripts/rename_themes.py)
convert  auto   a Job-centred v0.8.1 Job (scripts/<tNN>/, runs/<tNN>/) into Task folders; a v0.8.1
                ticket header inside a Task rewritten to find its Task from its own path
runs     auto   per Block: one folder per Run, run.yaml cards, moved tickets patched, references
                relinked, retired folders tidied (scripts/ladder.py update, § Any level)
faces    auto   a missing Task, Job or Block face from disk (haipipe-job new_job.py face; a Discovery
                Block through board_sync.py; a task Block's spine from its studio overview "Purpose")
verify          root audit, ladder audit, ticket probe (scripts/probe_tickets.py), link check against
                the snapshot --apply took before its first step (scripts/link_check.py)
```

### The Tools gate

A SPACE runs its own copy of Tools. Before any Project moves, that copy must read the new layout;
otherwise new tickets would recreate the old one and readers would lose their Results. `audit` reports
the gate as `TOOLS` lines; `update --apply` refuses while any is open.

### What a person decides

`audit` marks these `person` and the dry run lists them under `decide`; `--apply` never touches them:

1. **An old root folder** that is not a world (`literature/`, `probes/`, `narratives/`, an empty or
   untracked leftover): its destination, usually the owning world's `_old/` or `work/_legacy/`.
2. **A folder in a world that is not a Block** (pre-ladder names such as `A1_<topic>/`): carry it
   onto the ladder or archive it in `_legacy/`.
3. **A failed ladder finding**: a heavy file in a Result (a private repo may keep a discovery
   `paper.pdf`: `visibility: private`), an absolute path in a ticket or a new receipt, a Run name that
   is neither hard nor soft.
4. **Tools drift**: when the decided names and the contract disagree, Tools is fixed first.

### Rules the steps keep

1. **Never run a Run.** Tickets are verified with the path probe: it runs a ticket only up to its
   result-folder line, with every writing command dropped, under the ticket's own name; an owner's own
   gate (a BLOCKED message) counts as gated, not failed.
2. **Never edit what a Run or generator wrote.** Results, receipts, `passes/`, notebooks, delivery, a
   Design's frozen `inputs/`, archives and files marked generated are moved whole or left alone. A moved
   Run's old receipt keeps its recorded paths (run.yaml `moved_from:`).
3. **Links only follow what moved.** A reference is rewritten only where it names the moved folder; a
   bare word never. The link check compares before and after in one form, so a link that was already
   broken is reported as such, not blamed on the move.
4. **Moves stay reviewable.** Folders are renamed on disk; a submodule moves by `git mv` so
   `.gitmodules` follows; a stale `.gitmodules` entry is left. Commit each repository with `git add -A`
   so git records renames, a Project before the SPACE that points at it.
5. **Trust the decisions, not the prose.** The decided Theme names come from `themes.py`, not from any
   skill's text; a mismatch is a Tools finding.
