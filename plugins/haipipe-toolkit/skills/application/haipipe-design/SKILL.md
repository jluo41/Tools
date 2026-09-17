---
name: haipipe-design
description: >-
  Canonical owner of one stable Design Folder, its Design Item register, and
  the Design Plugin's five Spaces: Goal, Design, Insight, Run, and Delivery. Keeps Page and
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

# /haipipe-design · one Plugin, five Spaces, two Run graphs

## Version governance

Only explicit user approval may authorize `1.0.0`; until then the family stays at `0.4.0`.

This Design family is exactly `v0.4.0`. Do not change that version or publish a
`v1.x` release without explicit user permission. Architecture changes and
field-test repairs do not authorize a version upgrade.

## Design Items

A **Design Item** is one design target with its own acceptance rules: one
message, one UI card, one candidate pool. It is what a person asks for,
judges, and adopts; a Design Folder holds one or many. Items are registered,
goal and rules only, in `outline/<stem>-design-items.md`:

```text
## ITEM01 · Send the tested winner, verbatim
type: sms
audience: full SMSR2 population, unconditioned
job: prescription review
goal: Field the salience template exactly as round 1 sent it
stance: follow                     # follow · challenge · explore · generate
basis: evidence-informed           # brief-only · evidence-informed
mode: compose
expected: salience stays the best arm on click and authentication when re-fielded
falsified: a concurrently fielded round-2 arm beats it on click outside overlapping intervals
evidence:
- handoff · ../../../A00_InsightBoard/1-F-full/FW01-send-salience/FW01-send-salience.md
acceptance:
- ≤ 160 characters including the opt-out suffix
- ends with 'Reply STOP to opt-out' verbatim
```

`goal`, `stance`, `basis`, `expected`, and `falsified` are the register's
copy of the v2 `design_intent`; a Commission freezes them into its config and
compiles the `acceptance` lines into criteria. `evidence` lines carry the
Ticket input roles. The register carries no state. Every Design Run Ticket names the item it
serves (`item: ITEM01`); the item's state is derived by walking those Runs in
order (`not commissioned → commissioned → generated → verified → adopted`,
with `generate failed`, `verify failed`, `declined`, and `hold` as truthful
stops). A Commission may release one item or a set; a Generate produces
candidates for exactly one item; an Adopt decides exactly one item. An item
is never a Page division, a Run, or a Result: the Page explains it, the Runs
produce and judge it, the Result is its candidate.

## Plugin and Spaces

`Space` is the only reader-facing word for a plugin surface (JL 260916). One
Design Plugin presents the Folder through five Spaces, in time order:

| Space | Shows |
|---|---|
| Goal Space | the ask, from the Brief line that names the folder: venue, who, their job, how many designs (wanted · registered · adopted), which Insight board |
| Design Space | one card per Design Item: goal, why in plain words, insight pointer, expected/falsified, rules, state, who is waited on, buttons |
| Insight Space | per item, the supporting insights: page, signed by whom, what it says, pinned or not; "needs an insight" when none is named; the board's signed pages no item uses |
| Run Space | each item's Commission → Generate → Verify → Adopt timeline: who, when, outcome, next |
| Delivery Space | the adopted draft per item: exact text, hash, verifier, the person's words |

`Run Space` and `Delivery Space` are fixed platform names; `Goal`, `Design`,
and `Insight Space` are Design's own. Every word on the surface is a plain
word (the Brief and its lines, signed insight, draft, run record, records
check); contract words stay in the files. Steps are always named by their Run words. A Space is a
presentation/interaction surface, never another Run or execution owner; the
presenter is `haipipe-plugin-design`.

## One Folder, two independent Workflows

The rule is one Folder, two workflows: the Page workflow explains and delivers the Folder, the Design workflow commissions, generates, verifies, and adopts drafts; neither mints the other's Runs (the Page workflow's `rp00_mermaid-structure` Run and the Design workflow's `rdNN_*` Runs never share an id).

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
| stable Folder, Design Item register, the list of Spaces, authority boundaries, closure | `haipipe-design` |
| graph compiled from each Design Run Spec's Routes | `haipipe-design-workflow` |
| generic identity, Ticket/Result pairing, receipt invariants | `haipipe-run` |
| generation/verification unit work | `haipipe-design-unit` |
| Page RP/evidence/delivery/check graph | `haipipe-page-workflow` |
| Space table and projections | `workflow-table` |

Candidate wording, arrangement, visual form, or behavior changes route to a
new `Design.generate` revise Run with frozen base and feedback. Wording that
only explains an unchanged candidate stays in a Page Writing Step. A changed
decision target gets a new decision Run; a new comment inside the same fixed
decision stays a Step.

## Folder shape

Use `2-Design/Design-<NN>-<audience>-<job>-<venue>/`:

```text
Design-<NN>-<audience>-<job>-<venue>/
├── <stem>.md
├── outline/
│   ├── <stem>-design-items.md      # Design Item register · goal and rules only
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

The Commission Run freezes the Design Item it serves (`item: ITEM<NN>`), target,
unit shape/count, allowed sources, criteria, output scope, iteration budget,
config, and one `design_intent`:

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

A Result never becomes the adoption authority by itself: a named person adopts exact version hashes in a decision Run, and only that decision closes the item.

Design closes when every commissioned Run is truthfully terminal, required
independent verification is complete, the adoption decision Run is terminal,
and current previews match the exact decided hashes. Page closes separately
after release and fresh CHECK. Preserve rejected, failed, declined, and
superseded Runs.

Stop after adoption/decline. Implementation, sending, allocation, testing, and
measurement belong to downstream owners.

## Clean-break contract

Unsupported Design bytes are not readable history: legacy shapes are refused, never reinterpreted.

This skill has one current grammar only: Design v0.4.0, v2 Ticket/Result
contracts, and `rdNN_commission|generate|verify|adopt_*` ids. It does not read,
migrate, route, validate, or continue v1 Tickets/Results, D0-D5/GD0-GD6,
`rNN_design_*`, `design/DU*/`, PageX, or previous phase-shaped Design folders.
A decisive unsupported marker ends inspection. There is no compatibility or
migration path.
