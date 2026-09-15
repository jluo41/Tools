---
name: haipipe-design
description: >-
  Canonical owner of one stable Design Folder and the Design Plugin's five
  Workspaces: Plan, Create, Review, Run/Runtime, and Delivery. Keeps Page and
  Design Run graphs distinct. Use for commissioning, generating, independently
  verifying, previewing, and adopting exact Design candidates. Ends at adopted
  candidates, never implementation, distribution, experimentation, or measurement.
metadata:
  version: "0.4.0"
  last_updated: "2026-09-15"
  folder_owner: canonical
  folder_kind: design
  primary_face: page
  page_ruling: domain-gate
  outline:
    mode: grammar
    source: "Brief + Design Run Results"
    shape: "commission decision → generation → verification → adoption decision"
---

# /haipipe-design · one Plugin, five Workspaces, two Run graphs

## Version governance

This Design family is exactly `v0.4.0`. Do not change that version or publish a
`v1.x` release without explicit user permission. Architecture changes and
field-test repairs do not authorize a version upgrade.

## Plugin and Workspaces

One Design Plugin solves the whole Design problem through five member
Workspaces:

| Workspace id | UI label | Purpose |
|---|---|---|
| `plan` | Plan | Brief, Commission, target, constraints, Run graph |
| `create` | Create | generation action and candidate comparison |
| `review` | Review | independent verification and findings |
| `runtime` | Run | read-only Run Instance, Gate, Route, Result, receipt view |
| `delivery` | Delivery | exact previews and adoption decision |

Use `runtime` as the stable id; the UI may label it `Run`. A Workspace is a
presentation/interaction surface, never another Run or execution owner.

## One Folder, two independent Workflows

```text
PAGE RUN GRAPH                          DESIGN RUN GRAPH
rp-struct-01                            rdNN_commission_*
rp-sec-NN / rp-para-NN_*                       │ release
Page evidence/delivery/check                    ▼
                                       N × rdNN_generate_*
                                                │ ready
                                                ▼
                                       J × rdNN_verify_*
                                                │ pass
                                                ▼
                                       rdNN_adopt_* → CLOSE
```

Page Runs explain the work. Design Runs decide scope, generate or judge the
candidate, and adopt exact versions. They share the Folder but never share Run
ids, Results, gates, counters, or receipts.

## Design Workflow

The canonical Workflow is a directed Run Spec graph:

| Run Type | Actor | Target | Action | Exit Gate | Normal Route |
|---|---|---|---|---|---|
| `Design.commission` | human | one Commission/config version | release or hold | exact version decision is durably recorded | `generate` or `HOLD` |
| `Design.generate` | agent | one released unit/set/sequence | generate/revise | Result integrity and self-check pass | `verify` or `HOLD` |
| `Design.verify` | fresh agent | named immutable generation Results | independent verify | complete coverage settles pass/fail | `adopt`, `generate`, or `HOLD` |
| `Design.adopt` | human | exact verified candidate hashes | adopt/decline/revise | exact decision and preview/handoff versions recorded | `CLOSE`, `generate`, or `HOLD` |

```text
Expected actual Design Runs = 1 + N_generate + J_verify + 1
```

Commission and Adopt are human decision Runs because each has a bounded
question, explicit Ticket, named actor, independently closable decision
Result, and durable receipt. A click, comment, or feedback message inside one
of them is a Step/Gate event, not another Run.

## Ownership

| Concern | Owner |
|---|---|
| stable Folder, Workspace roster, authority boundaries, closure | `haipipe-design` |
| graph compiled from each Design Run Spec's Routes | `haipipe-design-workflow` |
| generic identity, Ticket/Result pairing, receipt invariants | `haipipe-run` |
| generation/verification unit work | `haipipe-design-unit` |
| Page RP/evidence/delivery/check graph | `haipipe-page-workflow` |
| Workspace table and projections | `workflow-table` |

Candidate wording, arrangement, visual form, or behavior changes route to a
new `Design.generate` revise Run with frozen base and feedback. Wording that
only explains an unchanged candidate stays in a Page Writing Step. A changed
decision target gets a new decision Run; a new comment inside the same fixed
decision stays a Step.

## Folder shape

Use `2-DS-design/DS<NN>-<audience>-<job>-<venue>/`:

```text
DS<NN>-<audience>-<job>-<venue>/
├── <stem>.md
├── outline/
│   ├── <stem>-logic.mmd
│   ├── evidence/
│   └── decisions/
├── workflow/
├── scripts/config/
├── runs/
│   ├── rp-struct-NN.md
│   ├── rp-sec-NN.md
│   ├── rp-para-NN_Pxx[-Pyy].md
│   └── rdNN_commission|generate|verify|adopt_*.yaml
├── results/
│   └── rdNN_commission|generate|verify|adopt_*/
│       ├── result.yaml or decision.yaml
│       ├── checks.yaml                # when applicable
│       └── runtime.yaml
└── delivery/
    ├── render/
    └── web|latex|word/
```

Every Design Run keeps the same stem across Ticket and Result. Completed
Results/decisions are immutable. `delivery/render/` may exist before adoption
because a person must inspect exact candidates; it never becomes a second
Result or Run.

## Commission = bounded design bet

The Commission Run freezes target, unit shape/count, allowed sources, criteria,
output scope, iteration budget, config, and one `design_intent`:

```yaml
design_intent:
  move: <what this design is trying>
  basis: brief-only | evidence-informed
  stance: follow | challenge | explore | generate
  expected_effect: <typed forecast or null>
  failure_condition: <distinguishing condition or null>
```

The move is a bet, not a conclusion. Release grants permission to generate; it
does not prove the bet. The creative motion remains **diverge → bet → vary →
converge**. A candidate set is not an experiment and has no arm, allocation,
power, or measured winner.

## Evidence and Page interlock

Keep signed handoff, factual evidence, inspiration, and design intent distinct.
Pin the exact authority/source path and hash. A Page `rp-*` Run is never Design
evidence or Design authority.

The adoption Run records exact candidate hashes, independent verification
Results, preview manifest, and handoff versions. Its terminal adoption receipt
is the Folder's `domain-gate` consumed by Page CHECK. Page CHECK verifies the
projection; it does not ask the same candidate decision again.

Page and Design Runs may proceed when their own dependencies are ready. Page
release waits for every Page promise and bound Design Result it presents.

## Closure

Design closes when every commissioned Run is truthfully terminal, required
independent verification is complete, the adoption decision Run is terminal,
and current previews match the exact decided hashes. Page closes separately
after release and fresh CHECK. Preserve rejected, failed, declined, and
superseded Runs.

Stop after adoption/decline. Implementation, sending, allocation, testing, and
measurement belong to downstream owners.

## Clean break

This skill has one current grammar only: Design v0.4.0, v2 Ticket/Result
contracts, and `rdNN_commission|generate|verify|adopt_*` ids. It does not read,
migrate, route, validate, or continue v1 Tickets/Results, D0-D5/GD0-GD6,
`rNN_design_*`, `design/DU*/`, PageX, or previous phase-shaped Design folders.
A decisive unsupported marker ends inspection. There is no compatibility or
migration path.
