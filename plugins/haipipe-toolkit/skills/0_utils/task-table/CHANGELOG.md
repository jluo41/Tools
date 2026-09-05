# Changelog · task-table

## 0.3.0 · 2026-09-05

- Make the Task Folder the only main-table row grain: one task remains one row
  even when it owns multiple configurations and Runs.
- Add a generated Config Catalog with one row per config, declared purpose,
  mode, input, output, and purpose provenance; missing purpose is explicit.
- Keep Runs Overview as the one-Run appendix and link each Run to its matching
  config when the ticket/config stems pair.
- Update the renderer, schema, command surface, example contract, and UI prompt
  to expose Configs without conflating Task, Config, and Run grains.

## 0.2.0 · 2026-09-04

- Make Task Tables explicitly two-lens: plan fields remain distinguishable
  from observed task-tree and runtime display facts.
- Define the Tables-family boundary: `/workflow-table` owns Phase/Cycle design,
  `/task-table` owns task-folder projection, and a unified `/board-table` is a
  future sibling rather than an alias for Folder inventory.
- Record that the current Folder has separate Folder-tab, Outline, and Runs
  projections but no unified Board Table.

## 0.1.0 · 2026-09-04

- First release: the generated sibling of `/workflow-table`. One row per task
  folder, keyed on `bNNjNNtNN`, saying what the task develops, reads, writes,
  and whether it has run.
- Three plan words (`develops:`, `input:`, `output:`) are owned by the task
  page head; the table projects them and falls back to the ticketed script's
  docstring headline and the newest config's `out_*` keys, naming the source
  in every row.
- Shape (JL 260904): a block is a section, a job is one table with its
  rollup on the heading line, a task is one row (Addr · Task · Develops ·
  Input · Output · Code · Runs · State). Runs Overview (reusing
  `/workflow-table`'s `bNNjNNtNNrNN` row; receipts only by default) and Store
  Slots are appendices from the same scan.
- `--check` re-renders and fails on drift; `--expect-fail` proves the gate
  can fail (haipipe-task GATE-1). No PyYAML: every key read is a top-level
  scalar.
- First corpora: `examples/Project-PhyReview-Pipeline/tasks.new` (47 tasks,
  0 receipts) and `examples/Project-Personality-OpioidRx/task` (39 tasks, 11
  receipts, none carrying a `status` field, rendered as `? (no status)`).
