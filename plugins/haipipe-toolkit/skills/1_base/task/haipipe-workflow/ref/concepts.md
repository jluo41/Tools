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

The Workflow is projected through a Workbench-owned Workspace roster:

```text
Run Spec × member Workspace = Cell
Cell = Skill + interaction + authority/projection binding
```

Skill and actual Run Instance are not additional axes.

## Ownership

| Layer | Stable responsibility |
|---|---|
| Workbench | member Workspace roster and stable ids |
| Run Type | reusable defaults and close semantics |
| Run Spec | one planned graph node: target, actor, action, gates, routes, cardinality |
| Cell | one Run Spec × Workspace binding for Skill, interaction, authority, and projection |
| Run Instance | one actual attempt: id, state, frozen input, Result, receipt |
| Workflow Runtime | optional frontier/index for aggregate coordination; never another Run |
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

Create a Workflow Runtime only when multiple Runs, branching, resume, human
HOLD, or cross-Run audit needs aggregate state. One simple Run may use only its
own receipt.

## Steps and sub-workflows

Steps are internal and may call agents, skills, tools, or sub-workflows. A
callee owns its internal Run graph. The caller sees only its external Input,
Output, terminal outcome, and receipt summary.

## Low-level API note

The JavaScript Workflow engine currently exposes `meta.phases`, `opts.phase`,
and `phase(title)` for progress grouping. Those fields are presentation
metadata. A generated script may populate them from Run Spec labels, but they
must never own a gate, route, target, identity, receipt, or cardinality.
