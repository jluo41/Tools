# Workflow concepts

## IPO and the Run graph

Every Workflow has one external shape:

```text
Input → Process[directed Run Specs] → Output
```

The Process is not a Phase list. It is a graph whose nodes are independently
closable Run Specs and whose edges are named Routes.

```text
Workflow Definition
├── input
├── run_specs
│   ├── Run Spec A ──route──▶ Run Spec B
│   └── Run Spec B ──route──▶ CLOSE | HOLD | A
└── output

Workflow Execution
└── Run Instances, each joined to one Run Spec and one receipt
```

## Ownership

| Layer | Stable responsibility |
|---|---|
| Run Type | reusable defaults and close semantics |
| Run Spec | one planned graph node: target, actor, action, gates, routes, bindings |
| Run Instance | one actual attempt: id, state, frozen input, Result, receipt |
| Step | internal work within a Run |
| Version | immutable reopen episode for the same target |
| Workspace | where a person or worker sees/acts on the Run |

`Plan`, `Build`, `Execute`, and `Report` are operations on these objects, not
domain lifecycle authorities.

## Gate and Route

Gate and Route belong to the Run:

- entry Gate is conditional; omission means `open`;
- exit Gate or inherited close rule is required;
- decision mode is `human`, `automatic`, `agent`, or `hybrid`;
- a terminal Run may default to `CLOSE`;
- every other outcome names `SELF`, `NEW_VERSION`, `NEW_RUN`, another Run Spec,
  or `HOLD`.

A human decision is a Run only when it has its own bounded question,
commission, durable Result/receipt, and close boundary. Otherwise it is an
internal Gate or Step.

## Definition versus runtime

The plan may say `cardinality: N`; it does not prove N Runs exist. An actual Run
exists only when an instance id/Ticket and receipt are allocated. A Result file,
retry, script, model call, progress group, or Runtime Workspace card never adds
another Run identity.

## Steps and sub-workflows

Steps are internal and may call agents, skills, tools, or sub-workflows. A
callee owns its internal Run graph. The caller sees only its external Input,
Output, terminal outcome, and receipt summary.

## Low-level API note

The JavaScript Workflow engine currently exposes `meta.phases`, `opts.phase`,
and `phase(title)` for progress grouping. Those fields are presentation
metadata. A generated script may populate them from Run Spec labels, but they
must never own a gate, route, target, identity, receipt, or cardinality.
