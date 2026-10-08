# Bounded standing authorization

Use only when a person authorizes batching of mechanical register operations.
Record an existing explicit instruction as its source; do not make the person
repeat authorization already given for the same scope. The record cannot
expand that instruction or stand in for a handoff signature/new-computation
release.

Store the grant at
`<board>/_runs/insight/<workflow_runtime_id>/authorizations/<id>.yaml`.
The person supplies the decision; an agent may transcribe it with its exact
source and actor identity. A machine-generated name or approval token is never
evidence of the person's decision.

```yaml
schema: haipipe.insight-authorization/v1
authorization_id: <unique-id>
board: <exact-board-path>
workflow_runtime_id: <exact-runtime-id>
authorized_by: <person>
authorized_at: <RFC3339-with-offset>
source: <durable-user-instruction-or-signed-record-address>
scope:
  targets: [{question: QK3, partition: B}]
  run_ids: []  # exact native ids if scoped to Runs; empty grants no Run execution
permitted_actions:
  - canonical-mark-spelling
  - derived-header-reconciliation
  - licensed-partial-final-settlement
forbidden_actions:
  - new-computation-release
  - handoff-signature
expires:
  runtime_terminal: true
  at: <optional-earlier-RFC3339-limit>
status: active
```

List only actions actually granted. The examples are the maximum allowed
mechanical classes, not defaults. A grant must name bounded target cells or
native Run ids and an expiry; an unbounded board-wide phrase alone is not this
contract. The grant expires at runtime closure/failure, its explicit earlier
limit, or the person's revocation. A held runtime remains resumable within the
original scope and any time limit.

Before each use, resolve source, person, board, runtime, target, action, expiry
and revocation. The action's normal owner and gate predicates still apply.
Append a control receipt in the owning Folder log naming authorization path,
action, exact target, licensing rule, evidence and result. Quote the licensing
sentence for partial-final settlement and write its reciprocal answering-Page
receipt. The runtime indexes those control receipts; it creates no decision Run.

If the grant does not cover an action, apply the ordinary owner rule and report
the missing decision where one is required. A grant never writes `signed:` on
a W handoff and never releases a new Supporting computation.
