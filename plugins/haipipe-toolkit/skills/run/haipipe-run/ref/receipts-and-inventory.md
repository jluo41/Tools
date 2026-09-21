# Run receipts and inventory

Read when scaffolding, settling, presenting or auditing Runs. Resolve the
selected [profile](run-catalog.md) and [identity](identity-and-history.md).

## Required facts and write ownership

Each allocated Run has an authored Ticket, a deterministic Result address and
a machine-readable lifecycle receipt, conventionally `runtime.yaml`. The
Result payload can be a decision or truthful non-success, not necessarily a
substantial artifact. Allocate the planned receipt before expensive work.

| Fact | Authoritative source |
|---|---|
| Owner, native identity, type/operation and target | profile + frozen Ticket; identity on receipt must agree |
| Actor, action, inputs/dependencies and close rule | commissioned Spec/Ticket and inherited profile |
| State, events/times, actual outcome and failure | native lifecycle receipt |
| Attempts / feedback / Versions | native append-only history or referenced journals |
| Output, provenance and checks | Result envelope/artifacts and required validation receipts |
| Gate decision, route taken | native Run records; Runtime may index them |
| Evidence admission, release and promotion | separately authorized owner records |

These are semantic requirements, not a universal replacement YAML schema.
Existing profiles can store facts in different fields or linked records.
Do not fabricate duplicate actor/type/route fields just to resemble an example.
Conversely, a required fact that cannot be resolved is an explicit contract gap.

The owner defines who writes which records. For Task, the scaffolder creates
planned state and the Ticket owns execution updates. Design workers write
Results while their caller owns runtime. Interactive Pages preserve the human
actor and journal. A read-only presenter cannot repair any of these on read.
Use the native atomic-write method and preserve prior history before updates.

## States, outcomes, and times

`status`, `terminal_outcome`, gate verdict, and promotion describe different
facts. A completed decision may choose hold; a completed evaluation may return
a negative verdict if its gate permits that. A failed process alone never
implies a valid Result, and process success alone never establishes acceptance.
Use the native profile to decide completion and permissible retries.

| Native meaning | Display meaning |
|---|---|
| Planned, allocated, not started | Ready |
| Executing | Running |
| Waiting for scoped human feedback/decision | Waiting |
| Complete with required owner evidence | Done |
| Failed | Failed |
| Blocked, unresolved, missing/invalid required records | Held / Needs attention |
| Superseded | Historical; distinguish from current work |

This is a projection, not another persisted state ledger. Preserve native
state detail. Missing receipts do not imply Ready; claimed complete records
with missing artifacts are findings. Structural display checks do not replace
semantic review or independent verification.

New non-null timestamps use RFC 3339 with an explicit UTC offset. Record
allocation using the owner's created/queued field where supported; leave
`started_at` null until work starts and `finished_at` null while unfinished.
Waiting does not establish a finish time. A pre-start failure can truthfully
have null start plus recorded terminal time/reason. Actual instantaneous work
may start and finish within one second; scaffolding alone cannot prove it did.
Legacy date-only timestamps remain readable with limited temporal precision.

### Coherent example: Task receipt lifecycle

Use the [Task schema](../../../task/haipipe-task/ref/runtime-yaml-schema.md)
for its complete schema and provenance fields. These are lifecycle excerpts
from the same native receipt, not standalone valid receipts or new schemas:

```yaml
# Allocated; the frozen Ticket/profile supplies worker and close semantics.
run: r01_execution_fit-model
family: Execution
operation: fit-model
target: model-a / frozen-data-v1 / config-v1
ticket: t01_model/runs/r01_execution_fit-model.sh
result: t01_model/results/r01_execution_fit-model/
status: planned
started_at: null
finished_at: null
failure: null
```

```yaml
# After launch; identity, inputs and other fields remain in this receipt.
status: running
started_at: "2026-09-20T12:00:00-04:00"
finished_at: null
failure: null
```

```yaml
# After the declared artifact/metric gate passes.
status: complete
started_at: "2026-09-20T12:00:00-04:00"
finished_at: "2026-09-20T12:08:00-04:00"
failure: null
```

An unsuccessful attempt instead records the owner's failed/blocked status
and reason. Its evidence stays recoverable before any retry. Interactive
writing uses [RP journals](../../../page/page-workflows/haipipe-page-workflow/ref/interactive-writing-run.md),
not this Task example or delegated paragraph fields.

## Inventory procedure

1. State owner scope, historical/current scope and counting grain. A request
   for kinds uses the catalogue; actual execution needs native records.
2. Resolve each owner/profile and its physical Ticket/Result/receipt stores.
   Enumerate their union so orphan Tickets, Results and runtimes remain visible.
3. Join by full logical identity; validate stems, resolved paths and stored
   identity. Multiple aliases/views of one execution produce one row. Two
   owners may legitimately have the same local `r01` or `rd01`.
4. Separate valid allocated records from plans and incomplete allocations.
   Report duplicates, missing pairs/receipts, unknown ownership and unresolved
   storage without inferring completed work or fabricating history.
5. Check required facts, frozen inputs, actor/worker, state/timestamps and
   history continuity through the selected native schema.
6. Resolve the owner's acceptance evidence before endorsing `complete`.
   Report discrepancies between a stored claim and available evidence.
7. Inspect reuse, evidence admission and promotion separately. An accepted
   Result does not become invalid merely because a consumer has not selected it.
8. Present active/recovery-needed work first, with exact next action/owner.

Use columns appropriate to the question, for example:

```text
Owner · Run · Type/profile · Target · Native state · Outcome ·
Ticket · Result · Receipt · Participation · Findings
```

A Workflow report joins each managed instance to its Spec. Existing accepted
Results can appear as reused dependencies with exact version/hash; report new
allocation count separately. Cardinality belongs to the definition. Controller
receipts, Cells, Steps, calls, retries, Versions, Result files, Cards, Labels,
and supporting aliases do not create additional logical Run rows.

Insight has a logical RI binding and version-qualified executions. Count
bindings in Run inventory; list exact executions separately when requested.
Do not collapse two different bindings because they share a base recipe, or
claim two new RI allocations because one binding has two publications.

## Audit boundaries

An orphan record stays visible even if a profile cannot be loaded. State
which invariants could not be checked. Do not turn a partial inventory into a
claim of complete coverage. Never execute workers merely to answer a read-only
inventory request. Repair goes through the owner with its existing authority.
Keep safe pointers and summaries in shared views; never copy protected raw
artifacts or credentials into a receipt or presentation layer.
