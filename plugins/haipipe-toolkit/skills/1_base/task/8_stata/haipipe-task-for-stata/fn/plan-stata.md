# Plan a Stata Task

Use `/haipipe-task-for-stata plan <tNN-task-path>`; Job scope enumerates direct Task children through `haipipe-task`.
Read `ref/stata-dialect.md`, shared `haipipe-task/fn/stage-plan.md`, and `haipipe-workflow/ref/plan-schema.md`.

1. Detect cms/case/data/reg from workers and explicit input, never from a prefix letter.
2. Scan `scripts/config/rNN_*.do` and `runs/rNN_*.ps1`; resolve shared cohort/source globals.
3. Expand independently commissioned variants: cms year; case cohort/source/year; data cross-year spec; reg window/family/source.
4. Use `ref/workflow-plan-sample-<stage>.yaml` to write the sole `workflow/plan.yaml` Run Spec roster.
5. Keep dispatcher branches, parallel extraction, estimation workers, describe, and summary as internal `steps` of the variant Run.
6. A separately requested describe-only Ticket is another Run when it has its own goal and receipt; a describe Step alone is not.
7. Bind code/server preflight review to entry gates and required light/heavy Results to exit gates.
8. Retain per-script details only as read-only projections under the shared schema.

Stata logs, config snapshots, and summary files remain primary engine evidence.
The Task controller writes `runtime.yaml` under the same Run identity and binds exact logs, snapshots and required Results per `ref/stata-dialect.md`.
Keep receipt bookkeeping outside thin worker/Ticket bodies; do not fabricate Python notebooks or execution status.
Unresolved output roots, server prerequisites, catalogue keys, or Workbench Cells block execution.

Return `status`, `summary`, `artifacts`, `next`, `task_folder`, `plan_path`, `run_specs`, and `stage`.
