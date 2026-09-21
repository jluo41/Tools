# Report a Stata Task

Use `/haipipe-task-for-stata report <tNN-task-path>` after execution.
Read shared `haipipe-task/fn/stage-report.md` and the Workflow Report schema.

For each actual rNN Ticket, inspect `$OUTPUT_ROOT/<task>/results/<run>/`:
- per-step `log/*.txt`, checking Stata `r(NNN)` errors and declared completion markers;
- required `summary.txt`, `.do` config snapshot, and manifest when the topology emits one;
- required heavy `.dta` assets in the declared Store, and light coefficient tables in Results;
- required `runtime.yaml` written by the Task controller, checking it against original engine evidence.

Write `workflow/report.yaml` with `runs` bound to Run Spec ids and full bNNjNNtNNrNN addresses.
`receipt` points to `runtime.yaml`, which cites exact logs/snapshots/summary paths.
Legacy runs lacking the receipt or sufficient original evidence remain incomplete; never fabricate timestamps or a pass.
Internal step status is an annotation: done requires output plus clean completion evidence; skipped requires a configured flag or verified reuse; failure or missing output cannot pass.
Compare source/synth/full flags and versions in config snapshots against declared inputs; expose drift.
Keep planned cardinality separate from actual count and never invent completed Runs for planned variants.
A per-script report is only a projection of the same actual Run ids.

Return `status`, `summary`, `artifacts`, `next`, `task_folder`, `report_path`, `actual_runs`, and `verdict`.
