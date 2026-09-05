# Changelog · haipipe-plugin-runs

## 0.9.7 — 2026-09-04

- Resolve canonical Task Tickets from `<task>/runs/` against Job-owned
  `<job>/results/<task>/<run>/` without copying Results into the Task Folder.
- Derive a missing Task receipt id from the Block/Job/Task path plus local rNN,
  and show the full b/j/t/r identity instead of a Paper `P` route.

## 0.9.6 — 2026-09-04

- Distinguish the cross-Folder neutral classification schema from the current
  Board Page adapter, which truthfully presents Page-local pairs only; external
  Supporting Runs remain in Outline and open at their owning Folder.

## 0.9.5 — 2026-09-04

- Clarify that Runs is an optional presenter beneath the Task Face and treat
  PageX only as historical migration input.

## 0.9.4 — 2026-09-03

- Distinguish Outline's evidence-grouped source/Run inventory from this
  top-level presenter of physically allocated page-local Runs.

## 0.9.3 — 2026-09-03

- Clarify that Outline evidence-side Run details show Purpose/Plan,
  Availability, and Next action as separate facts while raw paths remain
  non-downloading text.

## 0.9.1 — 2026-09-03

- Keep Runs visible on source-backed Board Pages even when no local Run is
  allocated, using one truthful empty state without creating empty folders.

## 0.9.0 — 2026-09-03

- Point evidence lineage to the Outline plugin's Evidence Workspace and name
  its generated folder `outline/evidence/supporting-runs/`.
- Keep Runs limited to physical page-local `runs/` and `results/` pairs.

## 0.8.4 — 2026-09-03

- Use Run/Result as the only reader-facing object names and show their exact,
  wrapping repository-relative paths.
- Route Outline lineage to the unified Evidence Items panel; keep Runs limited
  to real page-local Run–Result pairs.

## 0.8.3 — 2026-09-02

- Clarify navigation ownership: Outline Run tokens open Evidence → Run links;
  only physical page-local Ticket–Result pairs belong in this Runs overview.

## 0.8.1 — 2026-09-02
- Evidence Item detail rows show PageX source count and accepted authorities
  beside Supporting Runs and the local Run. PageX remains a source binding,
  never an extra Run or Result row.

## 0.8.0 — 2026-09-01
- Add `Page · Evidence Item` to the Page group. Its compact row shows typed
  item target, support count, local Run, status, and ready Result; detailed
  Supporting Runs and frozen input remain behind the row.

## 0.7.0 — 2026-09-01
- Present each independently closable Labeling operation as one Run row and
  group by P0-P5 episode without adding Round/Test/Scan/Audit umbrella rows.
- Resolve Labeling Tickets and safe Result envelopes from root `runs/` and
  `results/`, while canonical protected artifacts stay in their domain paths.

## 0.6.0 — 2026-09-01
- Add Labeling as a fourth Run family with Calibration Round, Qualification
  Test, Production Scan, and Final Audit operations.
- Resolve Labeling through its authority-owned domain folders and keep the Runs
  view read-only, protected-data-safe, and control-free.

## 0.5.1 — 2026-09-01
- Load the neutral `haipipe-run` contract before presenting Run identities,
  paired Results, receipts, and normalized statuses.

## 0.5.0 — 2026-09-01
- Replace the independent Runs, Results, Notebook, and Scripts segments with
  two regions: one compact Run overview and one collapsible Scripts tree.
- Group complete Run identities as Execution, Discovery, or Page; Page shows
  Division Writing and Display. Keep Ticket and Result together in one row and
  expose commands, receipts, logs, outputs, and script links only on click.
- Fix the overview to five statuses (`Ready`, `Running`, `Done`, `Failed`,
  `Held`) derived from the owning Run contract. Make Scripts freestyle: no
  manifest, internal grammar, one-to-one binding, or unbound-file finding.

## 0.4.0 — 2026-09-01
- Rename the presenter from Execution to Runs. Execute remains a workflow
  action; the plugin presents a plural collection of durable Run identities.
- Add the two physical dialects behind one logical pair: Folder-local
  `runs/<run>.sh <-> results/<run>/` and Job-backed Task
  `<task>/runs/<run>.sh <-> <job>/results/<task>/<run>/`.
- Treat config, scripts, and runtime notebooks as conditional projections;
  never copy job-owned Results into a Task Page to fake Folder-local storage.

## 0.3.0 — 2026-09-01
- Rename the presenter from Code to Execution. Its stable unit is the exact
  `runs/<RUNNAME>.sh <-> results/<RUNNAME>/` pair; `scripts/` and config are
  optional supporting material.
- Make no-code execution explicit: a Run may dispatch a skill, CLI, API, or
  external worker. Discovery Paper Runs are the first concrete case.
- Preserve the lifecycle boundary: Execution presents attempts and receipts;
  the owning workflow phase still decides run permission and Folder closure.

## 0.2.0 — 2026-08-31
- Under the former Code name, execution was treated as universal Task-Face
  behavior and the presenter was limited to Folders with code. Version 0.3.0
  supersedes that name and narrows the distinction correctly: the Task Face is
  universal, while materialized Run/Result execution remains optional.
- The presenter gained no lifecycle authority and exposed no run button.

## 0.1.0 — 2026-08-31
- Born contract-only as the presenter owed to scripts/ · runs/ · results/;
  segments fixed as Runs, Results, and Scripts.
