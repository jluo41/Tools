# Workflow Runtime Contract

This reference applies the root-level
[`WORKFLOW-DESIGN-PRINCIPLE.md`](../../../../../../../WORKFLOW-DESIGN-PRINCIPLE.md)
to executable HAI workflows.

## Canonical model

```text
Workflow Definition
  = Run Specs + RunTypes + gate policies + route policies + completion policy

Workflow Runtime
  = one execution identity
  + concrete Run instances
  + index of Run-owned gate evaluations
  + index of Run-owned route decisions
  + execution frontier
  + runtime receipt

Run
  = RunType + Ticket + Input/Target + Execution + Result + Receipt
```

`Workflow Runtime` is an aggregate controller/ledger. It is not an additional
Level-4 Run and must never be counted as one of its child Runs.

`Gate` and `Route` are not top-level entities in this contract:

- each Run Type/Spec declares its Gate predicates and allowed Route outcomes;
- the Workflow Definition validates the graph compiled from those Routes;
- each Run receipt records the actual gate evaluation and route decision;
- the Runtime indexes and projects those Run-owned records;
- a gate evaluation becomes a separate Run only when it has its own bounded
  target, Ticket → Result closure, and reusable receipt.

## Runtime envelope

The owning workflow chooses the physical path. A new runtime envelope should
carry at least this shape:

```yaml
schema: haipipe.workflow-runtime/v1
workflow_id: <reusable-definition-id>
workflow_version: <frozen-definition-version>
workflow_runtime_id: <one-execution-id>
status: planned | running | held | complete | failed

definition:
  run_types: [<run-type-id>, ...]
  transitions:
    - from: <run-type-id>
      when: <declared-condition>
      to: <run-type-id | HOLD | CLOSE>
  completion:
    required_terminal_runs: <declared rule>
    final_acceptance: <declared rule>

runs:
  - run_id: <owner-native-run-id>
    run_type: <run-type-id>
    status: planned | running | held | complete | failed
    ticket: <resolved Ticket path>
    result: <resolved Result path>
    receipt: <resolved Run runtime receipt path>

control:
  gates:
    - key: <stable-control-key>
      run_id: <owner-native-run-id>
      status: pending | passed | held | failed
      mode: automatic | human | agent | hybrid
      authority: <person or declared predicate>
      evidence: [<path@hash>, ...]
      run_receipt: <resolved Run receipt path>
  routes:
    - from_run_id: <owner-native-run-id>
      decision: <next-run-type | HOLD | CLOSE>
      mode: automatic | human | agent | hybrid
      reason: <why this route was selected>
      evidence: [<path@hash>, ...]
      run_receipt: <resolved Run receipt path>

frontier:
  - run_type: <next-runnable-run-type>
    target: <bounded target>
    state: runnable | held | waiting

output:
  path: <final output path>
  acceptance: pending | passed | failed
```

The envelope is a contract, not a demand that every dialect use these exact
field names. Existing dialect fields may remain as adapter aliases when
the new `workflow_runtime_id`, `run_type`, `control`, and `frontier` meanings
are unambiguous.

## Execution law

1. Freeze the Workflow Definition before creating a Runtime.
2. Create one new `workflow_runtime_id` for one execution attempt of that
   definition.
3. Materialize only the initial Runs justified by the input and RunType rules.
4. Execute each Run through its authored Ticket and pair its Result/receipt.
5. Record the gate evaluation on the Run receipt after its Result exists; index
   that record in the Runtime.
6. Select only a route declared by the Definition; record the reason and mode
   on the Run receipt and project it into the Runtime frontier.
7. Materialize the next Run(s), or record `HOLD`/`CLOSE`.
8. Close the Runtime only when all required Runs are terminal, no required
   control decision is unresolved, the frontier is empty, and final acceptance
   passes.

All control uses the same record shape. `human` names a person,
`automatic` evaluates only a declared predicate, `agent` names a delegated
judge/worker, and `hybrid` records both machine/agent work and human authority.
Page controller `copilot | auto` remains a session waiting policy, not a Gate
or Route decision mode.

## Identity and counting

```text
workflow_id          reusable definition
workflow_runtime_id  one execution of that definition
run_type_id          reusable behavior contract
run_id               one concrete bounded execution
```

Do not use `workflow_runtime_id` as an `rNN`, `riNN`, `rp-*`, or other
owner-native Run ID. Do not count a Runtime, control record, step, tool call,
retry, or human action as a second Run when the owning Run already contains
that work. A changed target, dataset, question, or acceptance contract still
requires a new owner-native Run under `haipipe-run`.

## Low-level adapter mapping

Existing workflow tooling may continue to expose:

```text
plan.yaml       frozen Workflow Definition
.workflow.js    executable adapter
phase(...)      engine progress-group call, not a Run identity
report.yaml     structured projection of the Runtime and child Runs
runtime.yaml    per-Run receipt; an aggregate Runtime may reference it
```

When a low-level adapter still serializes a `phase` field, treat it only as a
progress/dispatch label. Never allocate a duplicate Run from it. Design's
clean-break contract rejects previous phase-shaped Design grammar entirely.
