---
name: haipipe-design
description: >-
  Canonical owner of one stable Design Folder. Keeps its Page workflow and
  Design workflow distinct: Page Runs explain the work; released Design Runs
  generate and independently verify candidate units; a person adopts exact
  versions. Use for a Design Folder or DesignBoard. Ends at adopted candidates,
  never implementation, distribution, experimentation, or measurement.
metadata:
  version: "0.4.0"
  last_updated: "2026-09-13"
  folder_owner: canonical
  folder_kind: design
  primary_face: page
  page_ruling: domain-gate
  outline:
    mode: grammar
    source: "Brief + released commissions + version-bound Design Results"
    shape: "commissioned bets → candidate differences → verification → adoption → current projection"
---

# /haipipe-design · one Folder, two workflows

## Version governance

This Design family remains pre-1.0. Only explicit user approval may authorize
`1.0.0` or any higher major version. Architecture size, clean breaks, and
field-test repairs do not independently authorize a major-version jump.

A Design Folder is one durable work object with a Page Face and a Task Face.
It contains two orthogonal workflows. Never collapse their identities, gates,
or counters:

```text
📖 PAGE WORKFLOW                         🎨 DESIGN WORKFLOW
rp00 Mermaid Structure                  Commission: freeze a bounded bet
rp01+ paragraph interactions            ✋ person releases named commission
Page release → CONTENT                  rdNN_generate_* → DU Result
fresh CHECK → CLOSE                     rdNN_verify_*   → review Result
                                        delivery/render/*     → candidate preview
                                        ✋ person adopts exact version → STOP
```

A **Page Run** changes or accepts how the Folder explains the design. A
**Design Run** produces or judges the candidate itself. A DU is the immutable
Result of a generation Run, never a nested phase Folder. Verification produces
a separate Result and never edits the DU.

## Ownership and routing

| Concern | Owner |
|---|---|
| stable Folder, authority boundaries, adoption, closure | `haipipe-design` |
| Commission → Generate → Verify → Adopt | `haipipe-design-workflow` |
| Design Ticket/Result and unit work | `haipipe-design-unit` |
| `rp00`, paragraph Page Runs, Page release and CHECK | `haipipe-page-workflow` |
| Run identity, pairing, immutable history and runtime | `haipipe-run` |

Route by the object being changed. Candidate wording, arrangement, visual form,
or behavior goes to a new Design `revise` generation Run with frozen base and
feedback. Wording that merely describes an unchanged candidate goes to a Page
Writing Step. Choosing an existing candidate or recording a person's release
or adoption creates no Run.

## Folder shape

Use `2-DS-design/DS<NN>-<audience>-<job>-<venue>/`. Audience × behavior job ×
primary venue is stable scope. A new configuration inside that scope creates a
new Run, not a new Folder.

```text
DS<NN>-<audience>-<job>-<venue>/
├── <stem>.md                         📖 current Page projection
├── outline/
│   ├── <stem>-logic.mmd              rp00 whole-Page structure
│   ├── evidence/                     Page CITE/VALUE/DISPLAY workspace
│   └── decisions/                    immutable release/adoption receipts
├── workflow/                         machine lifecycle/Page receipts
├── scripts/config/                   frozen per-Design-Run configs
├── runs/
│   ├── rp00_mermaid-structure/       Page-owned interaction
│   ├── rpNN_pNN[-pNN]/               Page-owned interaction
│   └── rdNN_generate|verify_*.yaml   owner-native Design Tickets
├── results/rdNN_generate|verify_*/   DU/review Result + checks + runtime
└── delivery/
    ├── render/                       recipient-view candidate previews
    └── web|latex|word/               released Page projections
```

Materialize optional lanes only when used. `delivery/render/` may exist before
adoption because the person must see a candidate before choosing it. It is not
a Page build. Page release writes Page projections and never rewrites a DU or
candidate render.

## Commission = a bounded design bet

Before allocation, compile one already-written Commission and frozen config.
It names target, unit shape/count, allowed sources, criteria, output scope,
iteration budget, and `design_intent`:

```yaml
design_intent:
  move: <what this design is trying>
  basis: brief-only | evidence-informed
  stance: follow | challenge | explore | generate
  expected_effect: <typed forecast or null>
  failure_condition: <distinguishing condition or null>
```

The move is a bet, not a conclusion. A human release grants permission to run
the named Commission; it does not warrant its claim. Insight/handoff authority,
criteria, independent verification, and eventual adoption remain distinct.
Modes refine this honesty: compose/revise need no fake theory; brainstorm has
no forecast; theory-driven and challenge make their anticipated effect and
failure/distinguishing condition explicit.

The creative motion is **diverge → bet → vary → converge**. Insight narrows
what may responsibly be claimed; Design expands the candidate space inside
that boundary. A candidate set is not an experiment. It has no arm, allocation,
power, or measured winner; those belong downstream.

## Evidence and authority

Keep four things separate:

```text
signed W handoff   → domain authority for the Design Commission
evidence           → support for an asserted factual Page claim
inspiration        → material that may shape expression, never warrant it
design intent      → forecast/bet, never observed evidence
```

For empirical Design authority, pin the exact contextual, signed Application W
handoff by path/hash in the Commission and X1 crossing. A static handoff has no
invented Supporting Run id. Raw D/I/K prose or a Task RF does not become direct
Design authority.

The Page Face obeys the current Page evidence contract independently. A factual
Page claim binds a typed item under `outline/evidence/` through a real
Supporting Result, or through frozen local material and a Page-local typed
Result. The Design Ticket's `handoff` input is not itself a Page Evidence item,
and a Page `rpNN` Run is never Design evidence. A PageX path is not a valid
Design input or evidence address.

## Human authority and Page interlock

There are exactly two Design-domain human acts:

1. **Release** an exact existing Commission/config.
2. **Adopt** exact DU member hashes + independent verification + render/handoff
   versions.

The Folder declares `page_ruling: domain-gate`; therefore the adoption receipt
is also the owner ruling consumed by Page CHECK. CHECK verifies that the Page
and declared projections match the adopted versions. It must not ask the person
to select or accept the same candidate again. Page display-item acceptance,
when any Page evidence display exists, remains a separate Page evidence gate.

Page work and Design work may proceed whenever their own dependencies are
ready. `rp00` organizes the Page's argument; it does not ideate candidates or
release a Commission. An open paragraph Page Run does not block an unrelated
released Design Run. Page release waits for all Page Runs and required Task
Results, including Design Results the Page promises to present.

## Closure

The Design side is terminal when commissioned Runs are truthful terminal,
required independent reviews are complete, the person has adopted or declined
the named candidates, and current previews match those exact versions. The Page
side closes only after one release and fresh CHECK of the same versions. Report
the two states separately until both are closed.

Preserve every rejected, failed, and superseded attempt. Stop after adoption;
implementation, sending, allocation, and measurement belong to downstream Task
owners.

## Clean-break contract

This skill has one current grammar. It does not read, migrate, route, or validate
Design D0–D5/GD0–GD6 folders, `design/DU*/`, PageX bindings, v1 Tickets/Results,
or `rNN_design_*` identities. A Folder containing those shapes is not a current
Design Folder. Stop content inspection after a decisive unsupported marker.
Unsupported Design bytes are not readable history, migration inputs, fallback
evidence, or compatibility surfaces. Leaving unrelated files unchanged during
an audit is merely non-mutation; it grants no read, routing, or continuation
semantics.
