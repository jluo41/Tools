# haipipe-run · CHANGELOG

## 0.26.1 · 2026-09-15

Replace Phase-owned Run profiles with Workflow Run Spec graphs. Gate and Route
now belong to each Run; distinguish Run Type, Run Spec, and Run Instance; make
human decision Runs conditional on bounded commission, durable receipt, and
independent closure; retain RP feedback as Steps and reopenings as Versions.
Entry gates default open, exit close semantics are mandatory, terminal routes
default to `CLOSE`, and gate/route modes are `human | automatic | agent |
hybrid`; phase/controller labels are adapter metadata, not ontology. Add the
Workflow Runtime boundary: one aggregate `workflow_runtime_id` records frontier
and indexes Run-owned control decisions while child Runs retain owner-native
identities, Tickets, Results, and receipts.
Clarify that Workflow Runtime is optional aggregate infrastructure and that
Skill/interaction/projection behavior belongs to Run Spec × Workspace Cells,
not directly to the Run Spec or Workspace.

## 0.26.0 · 2026-09-14

Clarify that `rp-struct-01` is one multi-person Structure Run containing the
SHAPE and SURVEY cycles, with later structure ids reserved for independent
post-closure goals.

## 0.25.0 · 2026-09-14

Align the Page-facing Run contract with typed `rp-struct-NN`, `rp-sec-NN`,
`rp-para-NN_Pxx[-Pyy]`, and `re-value/display/cite` identities. Clarify that
`DISPLAY` covers tables and figures and that `V_`, `D_`, and `C_` placeholders
are labels bound to a Result/Card, not child Runs.

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
