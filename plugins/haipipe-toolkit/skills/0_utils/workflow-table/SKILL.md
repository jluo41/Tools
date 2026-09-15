---
name: workflow-table
description: >-
  Design, audit, and render a canonical Workflow × Workspace table. One Plugin
  or work object declares multiple member Workspaces; one Workflow declares a
  directed Run Spec graph; every Run Spec × Workspace intersection is a Cell
  that binds skills, interaction, authority, and projections. Use for Page,
  Task, Board, Discovery, Design, Labeling, or similar workflow contracts; not
  for ordinary data tables or a single-Run status report.
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "0.4.4"
  last_updated: "2026-09-15"
  # version history: ./CHANGELOG.md
---

# /workflow-table · Run Spec × Workspace

The two axes are exactly:

```text
rows     = Workflow Run Specs
columns  = member Workspaces declared by one Plugin/work object
cell     = one Run Spec × one member Workspace
```

Skill and Run are not extra axes. The Run Spec is the planned execution node;
skills and Workspace behavior bind through Cells. Actual Run Instances appear
only in the runtime projections.

## Core ownership

```text
Plugin/work object ──declares──> plural Workspace roster
Workflow          ──declares──> directed Run Spec graph
Run Spec × member Workspace ──is──> Cell
Run Spec          ──owns──> target · actor · action · gates · routes · cardinality
Cell              ──binds──> skill · interaction · authority · projection
Run Instance      ──materializes from──> one Run Spec
```

| Object | Grain | Planning truth | Runtime truth |
|---|---|---|---|
| Workflow Table row | one Run Spec | type, target, actor, gates, routes, cardinality | summarized instance state |
| Cell | one Run Spec × member Workspace | skill and surface binding | interaction/projection state |
| Runs Overview | one actual Run Instance | none | id, status, Result, receipt, route taken |
| Human Queue | one actual Run awaiting human actor/Gate | expected human role | question, state, decision receipt |
| Skill Coverage | one literal skill | used-by Cells | validation evidence |

## Workspace roster

One Plugin/work object declares multiple Workspaces:

```yaml
workspace_roster:
  id: design-workspaces
  declared_by: haipipe-design
  workspaces:
    - {id: plan, label: Plan}
    - {id: create, label: Create}
    - {id: review, label: Review}
    - {id: runtime, label: Run}
    - {id: delivery, label: Delivery}
```

Use `runtime` as the stable id for the Workspace that presents Runs. Its UI
label may be `Run`; the Workspace itself is not another Run.

## Run Spec rows

Each row is one independently closable Run Spec:

The table is a definition view, not an event log. A Step, Version, retry, or
actual Run Instance never receives another Workflow Table row. `NEW_VERSION`
updates the runtime projection of the same Run Instance. `NEW_RUN` allocates a
new Instance; it still uses the same parameterized Run Spec row unless the
Workflow definition truly declares different behavior or close semantics.

```text
Workflow Table:  Page.interactive-writing  cardinality 0..N   ← one Spec row
Runtime:         rp-para-01_P01/v001/s001-s003,
                 rp-para-01_P01/v002, rp-para-02_P02/v001      ← two Runs
```

| Field | Meaning |
|---|---|
| `id` | stable Workflow node id |
| `run_type` | Run Catalogue key |
| `purpose` | why this Run independently closes |
| `target` | bounded goal/target grammar |
| `actor` | `human`, `automatic`, `agent`, or `hybrid`, plus owner |
| `action` | bounded action or interaction |
| `input` / `depends_on` | conditional frozen inputs and upstream Specs |
| `entry_gate` | optional; omitted means open |
| `exit_gate` | required close semantics, directly or via Run Type default |
| `routes` | outcome → Run Spec, `SELF`, `NEW_VERSION`, `NEW_RUN`, `CLOSE`, or `HOLD` |
| `result` | optional payload plus required durable receipt |
| `cardinality` | planned demand, never actual inventory |

Gate and Route belong here, not independently in each Cell. A Cell may collect
or present a Gate because of its Workspace binding, but it cannot redefine it.

## Cells

The coordinate is exactly `<run-spec-id>@<workspace-id>`. Every Run Spec has
one explicit Cell for every member Workspace; unused intersections are
`mode: empty`.

| Cell mode | Meaning |
|---|---|
| `own` | presents/edits the authoritative Run Spec or its allowed object |
| `action` | lets the bound actor/skill perform the Run action |
| `review` | presents evidence and evaluates the Run's declared Gate |
| `decision` | collects a human decision required by this Run; does not create a second Run |
| `read-only` | projects the same Run Instance/Result without mutation or recounting |
| `empty` | explicit no binding |

A non-empty Cell states owner skill, worker skill chain, interaction, inputs
shown, outputs shown, authority change, and source/projection rule. It
references the row's Gate/Route; it never carries a conflicting copy.

## Worked Design table

Design uses one Plugin with five Workspaces and four Run Spec kinds:

| Run Spec row | Plan | Create | Review | Run (`runtime`) | Delivery |
|---|---|---|---|---|---|
| `commission` · `Design.commission` | own + human decision | empty | empty | read-only | preview receipt |
| `generate` · `Design.generate` | brief projection | agent action | empty | read-only | candidate preview |
| `verify` · `Design.verify` | criteria projection | empty | independent agent action | read-only | verdict preview |
| `adopt` · `Design.adopt` | scope projection | empty | verified-set projection | read-only | human decision |

```text
Design.commission ──release──▶ N × Design.generate
N generation Runs ──ready──▶ J × Design.verify
verification pass ──ready──▶ Design.adopt
adopt ──▶ CLOSE
decline/revise ──▶ generate | HOLD

Expected actual Runs = 1 + N + J + 1
```

Commission and Adopt are decision Runs because each has a bounded question,
explicit commission, human actor, durable decision Result/receipt, and its own
close rule. An individual click/comment remains a Step or Gate inside that Run.

## Synchronized projections

Default report order:

```text
Workflow Table → Runs Overview → Human Queue → Skill Coverage
```

### Workflow Table

Render one row per Run Spec and member Workspace Cells. The row owns planned
Gate/Route/cardinality; Cells own surface bindings.

### Runs Overview

Use one row per actual instance:

```text
Run · Run Spec · Run Type · Target · Actor · Status · Gate outcome ·
Route taken · Result · Receipt · Projected-in Cells
```

Runtime Workspace cards are read-only projections of these same ids. They do
not mint, rename, copy, or recount Runs.

### Human Queue

Use one row per actual Run currently waiting for its human actor or human Gate:

```text
Run · Run Spec · Human role · Question · State · Decision receipt
```

This is a derived queue, not a separate authority ledger. If the whole bounded
decision qualifies as a Run, it already appears in Runs Overview; if only one
Gate inside another Run needs input, the queue points to that same Run.

### Skill Coverage

Use one row per literal participating skill and list every `used_by_cells`
coordinate. See [`ref/skill-coverage.md`](ref/skill-coverage.md).

## Run Catalogue

The catalogue defines reusable Run Types, not Workflow rows or live instances.
A Run Spec references one key and may override only fields its type allows.
See [`ref/run-catalog.md`](ref/run-catalog.md).

## Design or audit procedure

1. Resolve the one Plugin/work object and plural Workspace roster.
2. Resolve the Workflow's directed Run Spec graph.
3. Check each Run Spec against `haipipe-run`: independent closure, target,
   actor, action, Gate, Route, receipt, and cardinality.
4. Materialize one Cell per Run Spec × member Workspace.
5. Bind skills and source/projection rules in Cells.
6. Render the four synchronized projections.
7. Compare planned cardinality with actual instance receipts without equating
   them.
8. Report unresolved owner, type, target, Gate, Route, receipt, or skill as
   `HOLD`; never fill it with a plausible guess.

## Validation gates

- exactly one Plugin/work object declares a plural Workspace roster;
- Workspace ids are unique and every Cell references one member;
- Workflow rows are Run Specs, never Phases, Steps, Versions, retries, actual
  Run Instances, files, calls, or views;
- every Run Spec has required identity, type, target, actor, action, close rule,
  terminal receipt, cardinality, and resolvable routes;
- Gate/Route are row-owned and Cells do not redefine them;
- every row has one Cell per member Workspace;
- read-only Runtime Cells preserve the source Run identity;
- human decision Runs satisfy independent closure; feedback turns do not;
- planned demand and actual Runs remain distinct;
- Skill Coverage resolves literal skills through Cell coordinates;
- all rendered projections agree with one declaration.

The complete normalized grammar is in
[`ref/workflow-table-schema.md`](ref/workflow-table-schema.md).

## Files

```text
workflow-table/
├── SKILL.md
├── CHANGELOG.md
├── agents/openai.yaml
└── ref/
    ├── workflow-table-schema.md
    ├── run-catalog.md
    └── skill-coverage.md
```
