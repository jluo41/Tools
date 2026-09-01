# Changelog · haipipe-plugin-runs

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
