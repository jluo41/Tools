# haipipe-run · CHANGELOG

## 0.24.0 · 2026-09-13

Define the Page projection as Run P, Run E, and Supporting Runs inside Plugin
Outline. Native external Runs keep their identity and are inspected by
reference rather than copied into the Page.

## 0.23.0 · 2026-09-13

Make `riNN` the native Insight Run binding: it points to one normal R ticket,
freezes a new dataset, and owns an independent Result history. A changed
dataset allocates a sibling RI instead of overwriting R or masquerading as a
rerun/version of the old dataset.

## 0.22.0 · 2026-09-13

Define the Task–Page cross-face handoff: Page proposes without reserving a
Task identity, Task returns a native Result, and Page binds it by full identity,
path, and fingerprint without collapsing either closure boundary.

## 0.21.0 · 2026-09-13

Require new runtime receipts to use offset-bearing RFC 3339 date-times; retain
date-only values as readable legacy history without pretending they establish
within-day order or duration.

## 0.20.0 · 2026-09-13

Add the native `rlNN` Labeling Run family while preserving one generic Level-4
Ticket/runtime/Result contract.
