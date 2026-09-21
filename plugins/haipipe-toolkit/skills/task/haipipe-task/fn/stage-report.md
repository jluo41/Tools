# fn/stage-report — report actual Runs from receipts

Use for `/haipipe-task report <tNN-task-folder>`.
Read `workflow/plan.yaml` and the Report schema in `haipipe-workflow/ref/plan-schema.md`.
Write `workflow/report.yaml` inside the Task Folder.

1. Resolve `$OUTPUT_ROOT` using the shared output-root contract.
2. Read each relevant `runtime.yaml`, config snapshot, CODE_REVIEW.md, RUN_AUDIT.md, manifests, logs, and required Result files.
3. Emit `runs` entries only for actual owner-native Run Instances, each bound to `run_spec_id`, full Run identity (for Task, bNNjNNtNNrNN), actor, target, truthful status, gate outcome, route, Result, and receipt.
4. Record missing, failed, stale, pending external, or skipped execution honestly; a planned spec without an allocated Run has no fabricated Run entry.
5. Keep planned cardinality distinct from actual count; retries stay under their
   Run and unallocated definitions are not actual Runs. Separate reused Results
   from new allocations. Enumerate Tickets and receipts together; show missing
   pairs as recovery findings rather than hiding them or calling them Ready.
6. Close only when required Result gates and terminal route support closure; process exit alone is insufficient.
7. Report exact evidence paths and discrepancies to the independent reviewer.

Internal step observations may live under `runs[].steps` as receipt-backed annotations; they are not workflow rows.
A retained `report-script-<worker>.yaml` is a read-only projection naming `report: workflow/report.yaml`, `run_ids`, and step observations; it never creates another Run roster.
Plan/Build/Execute/Report controller status may be summarized separately without counting it as Runs.

Return `status`, `summary`, `artifacts`, `next`, `task_folder`, `report_path`, and `actual_runs`.
If execution was manual or is still pending, say so and identify the missing receipt instead of marking it complete.
