---
name: haipipe-run
description: >-
  Define, allocate, resume, count, or audit HAIPIPE Runs using their owning
  domain contracts. Use when deciding Run versus Step, resolving
  Ticket/Result/receipt identity, choosing reuse versus new work, or composing
  Workflow Run Specs. Covers Execution, Discovery, Page, Insight, Design,
  Paper, and Labeling profiles. Trigger: Run contract, Run catalogue, Run
  ticket, runtime receipt, orphan Result, /haipipe-run.
metadata:
  version: "0.28.0"
  last_updated: "2026-09-22"
---

# /haipipe-run · one commission, one identity, preserved history

A Run is one durable, addressable commission for a bounded target and close
rule. Its authored Ticket and generated Result/receipt describe the same work.
It is Level 4 beneath its owning Folder/Task; Result is its generated projection,
not another hierarchy level. A Run may contain several Steps and execution
attempts. The owner defines any permitted Version history.

```text
Run identity = authored Ticket identity = generated Result identity
```

The identity is owner-qualified. Insight additionally qualifies each execution
by version beneath one immutable RI binding; see the identity reference.

A Workflow is a list of Runs. Its definition describes planned work as Run
Specs; its runtime lists the actual Run Instances. Dependencies and routes
connect those entries and permit branching, waiting, and parallel execution.
A list does not impose serial execution or allocate future identities.

## When and by whom

| Reader | Use this contract for |
|---|---|
| Workflow / Paper / Ideation planner | deciding which bounded work deserves a Spec and which native profile applies |
| Task / Discovery / Page / Insight / Design / Paper / Labeling owner | allocation, reuse, history, receipt, and closure invariants |
| Selected worker | the commissioned Ticket and its output/authority boundary |
| Run presenter / Task or Workflow table | locating, diagnosing, and counting the same native records |
| Direct user request | explaining or auditing Runs and the next required action |

Resolve the owner and selected Workflow/Spec before allocation. For an audit,
missing ownership is a finding, not a reason to hide the record. Load only the
relevant owner profile after this contract. Workers do not reload every family
for each call. Ordinary shell commands do not automatically become Runs.

| Request | Read next |
|---|---|
| Select or define a type/profile; see what kinds exist | [Run catalogue](ref/run-catalog.md) and the selected owner |
| Allocate, reuse, retry, reopen, or resolve storage | [Identity and history](ref/identity-and-history.md) |
| Scaffold/read receipts, report status, count, or audit | [Receipts and inventory](ref/receipts-and-inventory.md) |
| Compose multiple Runs or maintain a shared frontier | [Workflow](../../task/haipipe-workflow/SKILL.md) and its [runtime contract](../../task/haipipe-workflow/ref/workflow-runtime.md) |
| Present Runs in a Page | [Run presenter](../../page/haipipe-workbench-page/ref/run-space.md) |

## What earns a Run

Allocate only when all six hold:

1. A bounded goal or target is named.
2. A stable type/profile resolves and the owner can allocate an address.
3. A Ticket/Spec commissions an actor and action or interaction.
4. A close rule can settle success or truthful non-success.
5. The outcome has a durable Result/receipt.
6. Closure is independent of the caller's presentation surface.

Planning candidates and SURVEY reservations have no allocated Run inventory
row. Human decisions qualify only under these same tests. A click, signature,
comment, gate evaluation, script, tool/API call, or retry is internal when it
serves an existing Run's target and close rule. A separate commission may make
review its own Run; a label such as Gate 1 does not establish that commission.
Do not count both an umbrella episode and the independently closable work it
groups. A control-only Workflow invocation can truthfully have `runs: []`.

## Ownership and planned versus actual work

| Object / authority | Owns |
|---|---|
| Shared Run contract | qualification, identity/history facts, lifecycle and inventory invariants |
| Folder/domain profile | native naming/storage, operations, schemas, acceptance and promotion authority |
| Run Type | reusable defaults, allowed actor/action/Result, and default close rule |
| Run Spec | bounded goal, actor, action, inputs/dependencies, gates/routes, cardinality and internal Steps |
| Workflow definition | Spec list, dependency/Route graph, entry and overall completion rules |
| Run Instance | allocated address, frozen type/contract, state, attempts, Result and receipt |
| Worker | execution method and declared outputs within the commission |
| Run Spec × Workspace Cell | skill bindings, interaction, authority and projection for that surface |
| Presenter | read-only views of native records |

A Workspace never becomes the execution owner. Do not create a horizontal
`run-for-<folder-kind>` owner. Use the existing native owner and selected worker.
When a Workflow declares Workspaces, bind its Cells using
[workflow-table](../../0_utils/table-workflow/SKILL.md); a standalone Run does
not require inventing a Workbench roster or aggregate controller.

A Spec can materialize zero, one, or many instances. Symbolic cardinality is
planned demand; only allocated native records describe actual work. A Runtime
may index reused Results without allocating or executing them again. When a
shared frontier is useful, `workflow_runtime_id` identifies its aggregate
receipt; it is never a child Run address.

Gate/Route modes are `human | automatic | agent | hybrid`. Entry may default
open; exit semantics are mandatory and may be inherited from the type. A
terminal route may default to `CLOSE`; nonterminal routes are explicit.
Inputs, dependencies and a domain payload can be empty; target, actor, action,
close rule and durable outcome cannot. Resolve required facts through the
profile/Ticket/receipt rather than copying every field into every dialect.
A controller `Run()` label is adapter metadata, not an authority or Run node.

## Choose the next action

| Situation | Action |
|---|---|
| Exact accepted Result satisfies the request | reuse its full identity, version, path and hash |
| Matching open commission exists | resume through its owner |
| Same frozen contract failed | preserve failure and append an owner-permitted attempt |
| Open RP receives feedback within its goal | append a Step |
| Same RP target is reopened | use its declared Version rule; preserve closed history |
| Independent later Section writing session is commissioned | Page may allocate the next `rp-sec-NN` even for the same Section |
| Frozen data, goal, target, or acceptance changes materially | new Run; record supersedes only for an actual replacement |
| Input/authority/profile is missing | report the gap; do not invent a Ticket, identity, approval, or completed Result |

Interactive history is a scoped exception: do not apply evolving RP feedback
to frozen Execution or Discovery inputs. Version journals are append-only
while open and immutable after closure. New participants, sentences, labels,
Steps, or Versions do not allocate child Runs.

## Lifecycle

1. **Plan:** resolve owner, profile, bounded commission, dependencies and close
   rule. Check for reusable Results or a compatible open Run.
2. **Allocate/scaffold:** the owner chooses a collision-free native identity,
   authors its Ticket and creates a planned receipt at the resolved Result
   address before expensive work. Freeze required inputs before dispatch.
3. **Execute:** invoke the selected worker through the Ticket and native runner.
   Preserve attempts and feedback history using the selected profile.
4. **Validate/settle:** apply the owner's Result gate; record actual outcome,
   errors and route. Process exit alone cannot establish completion.
5. **Bind/promote:** the authorized consumer references the exact Result and
   separately records any evidence admission, Page release, or promotion.

Timestamps describe actual events. Unstarted/unfinished/unknown values remain
null; non-null new timestamps use RFC 3339 with an explicit UTC offset.
Scaffolding is not proof of completion. Waiting for a human is a normal state.
A complete bounded decision can record `hold` while its Workflow remains held.

## Example: one commission, several activities

A Workflow commissions one model fit and a separate independent evaluation.
Its definition has two Specs with an evaluation dependency. The Task owner
allocates the fit; its internal calls and an unchanged-input retry remain one
Run with two attempts. Only when commissioned and ready does evaluation get
its own Ticket and receipt. Two Pages can reuse that fit Result without new
fit Runs. The eventual inventory has two native Runs, not a row for every
call, retry, Result file, consumer, or controller invocation.

## Result, evidence, and closure

A Result may be a checked artifact, judgment, decision, or truthful failure.
The Result gate belongs to its profile. Evidence admission and downstream
promotion are separate facts; an unused valid Result stays valid. Feedback
and accepted writing history are authoritative records, not regenerable caches.
When upstream data changes, preserve the historical Result and mark affected
downstream bindings stale until new work or valid reuse resolves them.

For a Task-to-Page handoff: Page proposes work, Task allocates/executes its
native Run, Task returns the Result/receipt, and Page binds the full identity
and fingerprint. Neither face can close the other's obligations; use the
[Task/Page closure contract](../../task/haipipe-task/ref/task-page.md).
RE labels and Cards are projections of one focal Result. Supporting Runs keep
their native identities. Accepted RP prose does not prove RE evidence ready
or close whole-Page CHECK. Page RD builds can be Runs; Design Delivery is a
read-only projection of exact Generate/Verify Results.

## Inventory and boundaries

State the inventory scope and grain. Enumerate the union of native Tickets
and receipts/Results; diagnose missing pairs and duplicate addresses. Count
one row per owner-qualified logical Run and keep recovery-needed records
visible. Separate valid allocated, reused, planned, and incomplete records;
never silently treat missing receipts as valid allocations. Historical
execution versions may be expanded with an explicit execution count.

Use the [receipt/inventory procedure](ref/receipts-and-inventory.md) before
claiming completion or totals. Presenters cannot repair records on read,
allocate Runs, or turn their display states into domain acceptance. Keep
artifacts in their governed stores with safe pointers; no credentials, private
tokens, PHI, or raw sensitive rows in shared receipts.

## Files

The three `ref/` files own shared catalogue, identity/history, and receipt/audit
detail. Domain references linked by the catalogue own their concrete profiles.
`agents/openai.yaml` supplies invocation metadata; `CHANGELOG.md` records
changes. Do not duplicate domain schemas or fabricate a missing implementation.
