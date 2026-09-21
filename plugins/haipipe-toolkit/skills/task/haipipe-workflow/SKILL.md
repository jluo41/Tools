---
name: haipipe-workflow
description: >-
  IPO workflow designer, builder, executor, and reporter. Defines a Workflow as
  a list of Runs: planned Run Specs with dependencies and routes, and actual
  auditable Run Instances. Use for workflow planning, Run Type/Spec design, gates, routes,
  build scripts, execution, reports, or Workflow × Workspace bindings.
  Trigger: workflow, run graph, run spec, run type, gate, route, IPO, plan
  workflow, build workflow, execute workflow, report, /haipipe-workflow.
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill, Workflow
metadata:
  version: "0.3.1"
  last_updated: "2026-09-15"
  # version history: ./CHANGELOG.md
---

# /haipipe-workflow · compose Runs, do not invent Phases

A Workflow is a list of independently closable Runs. Its definition lists
Run Specs; its runtime lists allocated Instances. The graph expresses their
dependencies and routes, including branches and parallel work:

```text
Workflow Definition = Run Specs + graph compiled from their Routes
Workflow Execution  = Run Instances

I → Process[Run₁, Run₂, … Runₙ] → O
```

`Plan`, `Build`, `Execute`, and `Report` are commands for working with this
definition. They are not domain Phases and do not receive runtime authority.

Load `haipipe-run` whenever the Workflow has executable work. Load
`workflow-table` when the user needs the Run Spec × Workspace projection.
Resolve type/profile keys through the shared
[Run catalogue](../../run/haipipe-run/ref/run-catalog.md).
Load [`ref/workflow-runtime.md`](ref/workflow-runtime.md) when multiple Runs,
branching, resume, human HOLD, or aggregate audit state justify a Workflow
Runtime. One straightforward Run may rely on its own receipt.

## Core objects

| Object | Owns | Does not own |
|---|---|---|
| Plugin | member Workspace roster and stable ids | Run execution or Workflow order |
| Workflow | graph compiled from Spec-owned Routes, entry specs, terminal rules, Workflow I/O | concrete runtime truth or a second Route authority |
| Run Type | reusable defaults, allowed action/result, default close rule | one target or instance id |
| Run Spec | target/goal, actor, action/interaction, gates, routes, cardinality | current execution state or surface behavior |
| Cell | one Run Spec × member Workspace binding: skills, interaction, authority, projection | a second Gate/Route or copied Run |
| Run Instance | id, state, attempts, frozen inputs, Result, terminal outcome, receipt | Workflow graph definition |
| Workflow Runtime | optional frontier and aggregate index of Run-owned decisions | another Run identity |
| Step | one internal action or interaction inside a Run | independent Workflow row or Run id |
| Workspace | presentation and interaction surface | execution authority |

The word `phase` may still appear in the low-level JavaScript Workflow API as
progress-group metadata. It is a display label only. Never derive ownership,
gate, route, identity, or cardinality from it.

## Run Spec contract

Every Run Spec answers:

```yaml
id: <stable-spec-id>
run_type: <catalogue key>
purpose: <why this independently closable Run exists>
target: <bounded target grammar>
actor: {mode: human | automatic | agent | hybrid, owner: <literal owner>}
action: <action or interaction>
input: []                       # optional; may be empty
depends_on: []                  # optional
entry_gate:                     # optional; omitted means open
  mode: automatic | human | agent | hybrid
  assertion: <testable entry condition>
exit_gate:                      # closure semantics are required
  mode: automatic | human | agent | hybrid
  assertion: <testable close condition>
routes:
  <outcome>: <spec-id> | SELF | NEW_VERSION | NEW_RUN | CLOSE | HOLD
result:
  payload: <schema/pointer or none>
  receipt: <required durable receipt schema/path>
cardinality: <1 | 0..N | symbolic formula>
cells:
  - workspace_id: <member Workspace id>
    mode: <own | action | review | decision | read-only | empty>
    owner_skill: <literal owner Skill or none>
    worker_skill_chain: [<ordered literal Skills>]
    interaction: <allowed interaction or none>
    authority_change: <create | revise | bind | promote | release | none>
    source_projection: <source/read-write rule or none>
```

Required semantic fields are stable Spec and instance identity, Run Type,
bounded target/goal, actor, action/interaction, lifecycle state, close rule,
terminal outcome, and durable receipt. Inputs, dependencies, entry gate, and
Result payload are conditional. When a Plugin Workspace roster is declared,
Cell bindings are required, with one Cell per member Workspace. A standalone
Run/Workflow without such surfaces may omit the roster and Cells; never invent
a Plugin merely to execute one bounded commission. A terminal Run may omit an explicit route only when `CLOSE`
is its declared default.

## Human decisions and interactions

A human decision may be its own Run. It qualifies only when the question is
bounded, explicitly commissioned, independently closable, and returns a
durable decision Result/receipt. A click, comment, signature, or feedback turn
without those properties is a Gate or Step inside another Run.

For a fixed-scope interactive Page/RP Run:

```text
feedback       → next Step in the same Run
reopen target  → NEW_VERSION in the same Run
accept         → exit Gate → CLOSE or next Run Spec
change goal    → NEW_RUN
```

Do not allocate a Run per chat turn, sentence, retry call, shell command, or
model call when they share one target and close rule.

## PLAN · author the graph

`/haipipe-workflow plan` creates or revises `plan.yaml`.

1. Name Workflow purpose, Input, and Output.
2. Resolve the Plugin-owned Workspace roster when the Workflow declares those
   surfaces; otherwise retain a standalone definition without invented Cells.
3. List independently closable Run Specs; reject pseudo-Runs that are only
   Steps, files, tools, or projections.
4. Resolve each Run Type, target, actor, action/interaction, exit gate, routes,
   and cardinality.
5. For a declared roster, materialize one Cell per Run Spec × member Workspace; bind Skills and
   interaction/projection behavior in those Cells.
6. Draw every forward, backward, SELF, HOLD, and terminal route.
7. State entry Run Specs and Workflow terminal rules.
8. Freeze only after every destination, close rule, and applicable Cell resolves.

Use [`ref/plan-schema.md`](ref/plan-schema.md) for the complete shape.

## BUILD · compile the graph

`/haipipe-workflow build` translates the frozen plan into an executable
`.workflow.js` or a manual checklist.

- Preserve Run Spec ids in labels and receipts.
- Validate routes before execution.
- Generate structured output schemas for Result/receipt fields.
- Map the engine's optional `meta.phases` and `opts.phase` only to progress
  groups; they do not recreate Phase authority.
- Keep the generated script replaceable from the frozen plan.

Use [`ref/template.workflow.js`](ref/template.workflow.js) and
[`ref/workflow-api.md`](ref/workflow-api.md).

## EXECUTE · materialize Run Instances

`/haipipe-workflow execute` starts from an entry Run Spec and follows Results:

```text
Run Spec → allocate Instance → freeze inputs → perform action/interaction
         → evaluate exit Gate → write Result/receipt → follow Route
```

The definition contains planned cardinality. Runtime truth comes only from
allocated instance ids and valid receipts. Record deviations; do not mutate the
frozen graph during execution. A materially changed target or close rule
requires a new Run Instance or a newly frozen Workflow definition according to
the owning dialect.

Create a Workflow Runtime only when aggregate coordination is useful. It may
index Run-owned Gate/Route records and preserve the frontier, but it is not a
Run and cannot replace any Run receipt.

## REPORT · echo definition with runtime truth

`/haipipe-workflow report` joins each instance to its Run Spec:

| Run Instance | Run Spec | Run Type | Target | Actor | Status | Gate outcome | Route taken | Result | Receipt |
|---|---|---|---|---|---|---|---|---|---|

Report planned and actual cardinality separately. Put active and
recovery-needed Runs first. Do not count Run Type rows, Steps, Results,
Workspace projections, or proposed instances as completed Runs.

## Sub-workflow boundary

A Run Spec may invoke another skill or Workflow. Only the callee's Input,
Output, terminal outcome, and receipt summary cross the boundary. The caller
does not absorb the callee's internal Runs or renumber them.

```text
CALLER Run Spec ──sub_I──▶ CALLEE Workflow
CALLER receipt ◀─sub_O + terminal summary── CALLEE
```

## Validation

Before freezing or reporting, require:

- every Run Spec id and Run Type is unique/resolved;
- every Run has a bounded target, actor, action/interaction, close rule, and
  durable receipt;
- every nonterminal route resolves to a Run Spec or explicit control outcome;
- human decision Runs pass the independent-close test;
- feedback Steps and Versions are not counted as Runs;
- planned cardinality is separate from actual allocated instances;
- with a declared Plugin roster, every Run Spec has one Cell per member Workspace;
- Cell Skill/interaction/projection bindings do not redefine Run Gate/Route;
- Workspace bindings are presentation/interaction only;
- low-level progress groups are not treated as semantic Phases;
- the report mirrors the graph and names actual route outcomes.

On a missing target, actor, close rule, route, owner, or receipt, return `HOLD`
with the exact unresolved field.

## Output

```text
status:    ok | hold | failed
operation: plan | build | execute | report | inspect | template
workflow:  <name>
definition: <plan path or inline>
instances: <actual Run ids or []>
route:     <next Run Spec | CLOSE | HOLD>
runtime:   <workflow_runtime_id | none>
summary:   <one sentence>
```
