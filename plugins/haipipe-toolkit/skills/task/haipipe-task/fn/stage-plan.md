# fn/stage-plan — audit, repair, and define Runs

Use for `/haipipe-task plan <tNN-task-folder>`.
Read `ref/hierarchy.md`, then `../haipipe-workflow/ref/plan-schema.md` (resolved from the Task skill directory) and `ref/workflow-template.yaml`.
A Workflow is a list of Runs; `workflow/plan.yaml` is the only authoritative definition roster.

## Procedure

1. Run the audit in `fn/audit.md`; collect type, Run stems, sibling Tasks, shared configs, and findings.
2. Preserve existing work and improve an existing plan in place. Resolve native
   profiles through `../../run/haipipe-run/ref/run-catalog.md` from the Task skill
   directory; `task.execute` binds this owner's Ticket/Result contract.
3. Repair missing per-run configs under `scripts/config/`, retaining shared parameters and adding accurate `_meta` purpose, inputs, and outputs.
4. Create missing Tickets only for explicitly commissioned work on the selected
   engine/platform; Python uses the shared shell template and Stata uses its
   PowerShell dialect. Create the paired planned receipt at allocation.
   Uncommissioned future work stays a Spec without a Run id or Ticket.
5. Flag notebook naming mismatches without renaming existing notebooks.
6. Read the full workers and the numbered domain specialist's `ref/workflow-plan-sample*.yaml`.
7. Define each independently executable config/Ticket variant as a Run Spec with a stable id, catalogue run_type, target, actor, gates, routes, Result receipt, cardinality, and Cells from the owning Plugin's Workspace roster.
8. Keep data stages, notebook cells, tool calls, and pre/post execution checks as internal `steps` or gates in that Run Spec.
9. Resolve output paths through `RESULT_STORE`, then Job `src/config-defaults.yaml` store, then the Job root.
10. Check input/output paths against the actual project, preserve heavy store outputs, and return exact changed paths for independent review.

A separately commissioned review may be another Run Spec when it has its own owner, close condition, and receipt; the label Gate 1 or Gate 2 alone does not justify a Run.
If no Workspace surface is declared, omit the Plugin roster and Cells as the
shared Schema permits. An explicitly declared but unresolved roster or missing
catalogue profile blocks definition freeze; do not invent either.

## Script detail

Use optional `run_specs[].steps` for ordered internal procedures with `label`, `section`, `required`, `prompt`, `files_in`, and `files_out`.
These annotations do not change cardinality, route, or Run identity.
If an existing `workflow/plan-script-<worker>.yaml` remains useful, migrate it to a read-only projection containing `plan: workflow/plan.yaml`, `run_spec_ids`, and internal `steps` only.
It must never contain a second `run_specs` or `phases` roster.
Prefer keeping details in the authoritative plan when a separate projection adds nothing.
Config is input, not another plan layer.

Return `status`, `summary`, `artifacts`, `next`, `task_folder`, `plan_path`, and `run_specs` (the definition count, never executed count).
Planning does not execute a Ticket or claim a completed Run.
