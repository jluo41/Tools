# Task to Intake
state: ✅ SETTLED
owner: JL
method: make a task export a compact, safe aggregate and provenance record before a display is allowed to snapshot it

## Opening
How does Task hand a result to Display without handing over its whole workspace?

The display-input task exports only `source_data.csv` and `provenance.json` for one run.
Paper Display then snapshots the approved aggregate into Intake.

## Diagram
```text
task holder
results/<run>/source_data.csv      canonical aggregate
results/<run>/provenance.json      hash · selection · safety
              │
              ▼
Display Intake snapshot             small approved render input
```

## Content
### Task's output is not the final figure
Task may make diagnostics for its own work.
Those diagnostics are not automatically a paper visual.
The Display unit regenerates the selected visual from its approved snapshot.

### Provenance is carried, not inferred
The manifest repeats holder, run, artifact, and hashes.
This keeps a display auditable even when the task environment is remote or later changes.

## Aims
- [x] 📤 Define the display-input task output contract
      One compact aggregate and provenance record are required.
- [x] 🔗 Define task-to-Intake materialization
      Paper Display copies the approved aggregate and records its origin.

## States
`haipipe-task-for-display` now produces display-ready inputs rather than a canonical paper asset.

## Files
- `task/7_display/haipipe-task-for-display/SKILL.md`
  Task-side output contract.
- `task/7_display/haipipe-task-for-display/ref/provenance-template.json`
  Provenance record shape.

## Law
Law: Task exports evidence; Display renders it; neither takes the other's role.

## Log
260727 · Reframed the display task around a verified aggregate instead of a final paper figure.
