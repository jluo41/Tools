# CHANGELOG · haipipe-task-for-page

## 0.3.4 · 2026-09-04

Require page-service Tickets to preserve every upstream Result path/hash in
`RUN_INPUTS` across planned, running, and terminal receipts.

## 0.3.3 · 2026-09-04

Specify the complete page-service Ticket delta, including `TASK_NAME`, and
require the generic scaffolder's full `status: planned` receipt before launch.
Repair the specimen proposal's canonical Result path.

## 0.3.2 · 2026-09-04

Pin the page-serving Ticket contract: family `Execution`, operation
`collect-page-values`, target batch, and `values.yaml` as the declared Result
gate, so the generic scaffolder cannot retain unrelated defaults.

## 0.3.1 · 2026-09-04

Align the page-serving specialist with the canonical nested Task dialect:
task-owned code lives in `scripts/`, per-Run configuration in
`scripts/config/`, Tickets in `runs/`, and generated Results under resolved
`$OUTPUT_ROOT/results/<task>/<run>/`. Replace the specimen's retired Probe
binding with current Supporting Run → Local Input → local Evidence Item Run.

## 0.2.2 · 2026-08-31

Make the serving job genuinely generic: any Folder Page Face uses
`tasks/b<NN>_page_service/j<NN>_values_<page-stem>/`; Paper's older service
block name remains a readable project profile, not the universal contract.

## 0.2.1 · 2026-08-31

The serving-page diagram now places the address in canonical
`evidence/probe/`; the collection job remains a whole-Folder PageX relation.

## 0.2.0 · 2026-08-31

The serving Page now links its collection job as one whole Folder through
PageX. PageX reads Page Face, plan, report and QA live; the separate `task/`
lane and `haipipe-plugin-task` dependency are gone.

## 0.1.0 · 2026-08-31

First release (JL: "it try to do the task for the probing, and generated the
evidences"). One collection job per Board Page answers the page's task-route
probe cards with code: reads upstream task folders, writes values.yaml +
QA digests, proposes the owning-block task for any value with no source
(workflow/proposals.md, measurement never direction). Replaces per-question
generic dispatch for a page's TASK-route values; the Discovery route, the
probe card address (PP<NN>.v<n>) and the one-door dispatch rule
(haipipe-probe-q-executor-agent) are unchanged. Registered in haipipe-task
0.10.0 (type table + keyword map), haipipe-page 0.44.0, haipipe-plugin-chat
0.3.0, haipipe-page-probe 0.12.0, haipipe-page-evidence 0.13.0.

Field-tested same day (cold subagent, scratchpad job for SM05-results: 0 landed ·
3 owed · GATE-3 proven to fail first). Frictions folded back: QA files keep
fn/qa.md's frozen state set (`concern` was wrong here — it is the card's word),
the §🧱 tree carries the task page `tNN_<task>.md`, the specimen pins upstream at
the JOB level, uses the real project path and page stem, and states the
slug-to-numbered-QA-file join.
