---
name: haipipe-design
description: >-
  Canonical owner of one stable Design Folder, its Design Item register, and
  the Design Workbench's five Spaces: Goal, Design, Insight, Run, and Delivery. Keeps Page and
  Design Run lists distinct. Use for commissioning, generating, independently
  verifying and handing off exact Design candidates. Ends when Verify passes,
  never implementation, distribution, experimentation, or measurement.
metadata:
  version: "0.4.0"
  last_updated: "2026-09-20"
  folder_owner: canonical
  folder_kind: design
  primary_face: page
  page_ruling: domain-gate
  outline:
    mode: grammar
    source: "Brief + Design Run Results"
    shape: "commission decision → generation → verification → delivery handoff"
---

# /haipipe-design · one Workbench, five Spaces, two Run lists

## Version governance

Only explicit user approval may authorize `1.0.0`; until then the family stays at `0.4.0`.

This Design family is exactly `v0.4.0`. Do not change that version or publish a
`v1.x` release without explicit user permission. Architecture changes and
field-test repairs do not authorize a version upgrade. The two Design workbenches
(`haipipe-workbench-design`, `haipipe-workbench-design/ref/design-board.md`) version separately.

## Design Items

A **Design Item** is one design target with its own acceptance rules: one
message, one UI card, one candidate pool. It is what a person asks for,
judges, and hands off; a Design Folder holds one or many. Items are registered,
goal and rules only, in `outline/<stem>-design-items.md`:

```text
## ITEM01 · Send the salience wording unchanged
type: sms
audience: all patients
job: prescription review
goal: Send the salience wording unchanged, so the reader sees whose office wrote and what to review
stance: follow                     # follow · challenge · explore · generate
basis: evidence-informed           # brief-only · evidence-informed
mode: compose                      # compose · revise · brainstorm · theory-driven · challenge
expected: a first-time reader can say who sent it and what to do after one read
falsified: a cold reader cannot name the next step from the text alone
evidence:
- handoff · ../../../A00_SMSR2Full-InsightBoard/1-F-full/FW01-send-salience/FW01-send-salience.md
acceptance:
- ≤ 160 characters including the opt-out suffix
- ends with 'Reply STOP to opt-out' verbatim
```

`evidence` paths are relative to the Design Folder (the folder holding
`<stem>.md`), not to the register file under `outline/`. A line is
`role · path` (or `role  path`); the roles are `evidence`, `handoff`,
`inspiration`, `reference`, and `avoid` (`base` and `feedback` are written by
revise runs). On screen a `handoff` reads "signed insight".

`expected` and `falsified` judge design quality. They may name what a later
experiment will check, but Design Runs judge design quality only, so
they carry no experiment words (arm, allocation, power, winner, field).

`goal`, `stance`, `basis`, `expected`, and `falsified` are the register's
copy of the v2 `design_intent`. Adding an item checks the bindings the records
check enforces: a `challenge` stance goes with `challenge` mode and only with
it; `challenge` or `theory-driven` mode needs both `expected` and
`falsified`; `brainstorm` goes with stance `explore` or `generate` and carries
neither. A Commission pins its config (the goal sentence, stance, basis, mode,
expected, falsified, the compiled criteria, and the raw rule text) and the
item's evidence files with sha256; it does not pin the Brief version or venue
packs. Generate and Verify inherit the released design fields and evidence list,
deriving only `review_mode` and the operation's permitted `mode` as specified in
`haipipe-design-unit/references/unit-contract.md`, so an
edit to the register after release reaches only a new Commission (and so a
new item). The register carries no state. Every Design Run record names the
item it serves (`item: ITEM01`); the item's state is derived by walking those
Runs in order:

```text
not commissioned → commission open → commissioned | commission held
  → generate queued → generating → generated | generate failed
  → verify queued → verifying → ready | verify failed | verify invalid
queued run out of date: a queued run whose pinned file changed since it was queued
blocked: a Run needs the named input/record repair; this is not a Commission hold
records invalid: a previously ready candidate no longer matches its checked records; inspect before handoff
```

The full fold, with who each state waits on, is in
`haipipe-workbench-design/ref/space-mapping.md`. A Commission releases exactly
one Design Item (Release all writes one Commission per item); a second
Release of the same item is refused, and a held Commission can be released
later through a new Commission Run, preserving the held decision. A Generate produces a draft for exactly one item; a passed Verify makes
exactly one item ready. A brief-only item (`basis: brief-only`) is legal and may be
delivered; it rests on the Brief alone. An item is never a Page division, a
Run, or a Result: the Page explains it, the Runs produce and judge it, the
Result is its draft.

## Workbench and Spaces

`Space` is the only reader-facing word for a workbench surface (JL 260916). One
Design Workbench presents the Folder through five Spaces, in time order:

| Space | Shows |
|---|---|
| Goal Space | the ask, from the Brief line that names the folder: venue, who, their job, how many designs (wanted · registered · ready), which Insight board |
| Design Space | one foldable row per Design Item; opened, the design beside Why this design, From insight to design, The bet, Rules, Runs, and the buttons |
| Insight Space | per item, the supporting insights: page, signed by whom, what it says, pinned or not; "needs an insight" when none is named; the board's signed pages no item uses |
| Run Space | each item's Commission → Generate → Verify timeline: who, when, outcome, next |
| Delivery Space | a read-only handoff of each item whose Verify passed |

`Run Space` and `Delivery Space` are fixed platform names; `Goal`, `Design`,
and `Insight Space` are Design's own. Every word on the surface is a plain
word (the Brief and its lines, signed insight, draft, run record, records
check); contract words stay in the files and never appear beside their plain
word. No roster, handoff, Ticket, candidate, DU, or Brief line id (`R1`)
reaches the screen, and an insight page shows as its label and title
(`full-W01 · Send salience`), never its file id `FW01`. The Runs list uses real Run names;
Steps are actions inside one Run. A Space is a
presentation/interaction surface, never another Run or execution owner; the
presenter is `haipipe-workbench-design`.

## One Folder, two independent Workflows

The rule is one Folder, two workflows: the Page workflow explains and delivers the Folder, the Design workflow commissions, generates, and verifies drafts; neither mints the other's Runs (the Page workflow's `rp-struct-01` Run and the Design workflow's `rdNN_*` Runs never share an id).

```text
PAGE RUN GRAPH                          DESIGN RUN GRAPH
rp-struct-01                            rdNN_commission_*
rp-sec-NN / rp-para-NN_*                       │ release
Page evidence/delivery/check                    ▼
                                       N × rdNN_generate_*
                                                │ draft
                                                ▼
                                       J × rdNN_verify_*
                                                │ pass
                                                ▼
                                       Verify pass → Delivery ready
```

Page Runs explain the work. Design Runs decide scope, generate or judge the
candidate, and hand off exact versions. They share the Folder but never share Run
ids, Results, gates, counters, or receipts.

## Design Workflow

A Workflow is a list of Runs. The Design Workflow contains Commission,
Generate and Verify Runs, each with its own identity, target, actor, gate and
Result or receipt. Run Specs describe the allowed types below; Routes describe
dependencies and which Run may be created next. A route graph is a view of
those relationships, not another execution unit.

| Run Type | Actor | Target | Action | Exit Gate | Normal Route |
|---|---|---|---|---|---|
| `Design.commission` | human | one Design Item's config version | release or hold | exact version decision is durably recorded | `generate`, or `HOLD` (a person may release later) |
| `Design.generate` | agent | one released item | generate/revise | the records check passes (Result integrity and self-check) | `verify`; a draft that fails the check goes back to `generate` |
| `Design.verify` | fresh agent | named immutable generation Results | independent verify | complete coverage settles pass/fail | `delivery` (pass), `generate` (fail); a review that fails the check goes back to `verify` |

Delivery is a read-only projection of the exact Verify-passed draft and its
verification pointer, outside the Run list.

```text
Actual current Design Runs per Design Item = C Commission + N Generate + J Verify
```

Count allocated records, including held, failed, blocked and superseded Runs;
attempts inside one Run do not add identities. C=1 on a path with one release
and no earlier held decisions. Each Item permits at most one release.

The agent side never routes to HOLD: HOLD is a person's decision at
Commission. A draft that passed its independent review is ready for Delivery;
failed candidates can be revised through a new Generate Run.

Commission is the human decision Run because it has a bounded question,
explicit Ticket, named actor, independently closable decision Result, and
durable receipt. Delivery is not a Run. A click, comment, or feedback message
inside Commission is a Step/Gate event, not another Run.

## Ownership

| Concern | Owner |
|---|---|
| stable Folder, Design Item register, the list of Spaces, authority boundaries, closure | `haipipe-design` |
| Run list, Run Specs and graph compiled from their Routes | `haipipe-design-workflow` |
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

Use `2-Design/Design-<NN>-<audience>-<job>-<venue>/`, where each part is the first three content words of that Brief cell, filler words (with, within, a, the, of, for, or, under, …) dropped, so the name says the goal: `Design-01-all-patients-prescription-review-sms`. A renamed folder keeps its `Design-NN` number, and an old link finds it by that number. The Page title is one plain phrase from the same Brief line, `<job> <venue> for <who>` (`Prescription review SMS for all patients`):

```text
Design-<NN>-<audience>-<job>-<venue>/
├── <stem>.md                           # always: the Page (new-folder writes it)
├── outline/
│   ├── <stem>-design-items.md          # always: Design Item register · goal and rules only
│   ├── feedback/<run>.md               # when used: the feedback a revise Generate was queued with
│   ├── <stem>-draft-request.md         # when used: an open request for the agent to draft items
│   ├── <stem>-logic.mmd                # when used: Page workflow
│   └── evidence/                       # when used: Page-owned typed evidence
├── workflow/                           # when used: Page workflow receipts
├── scripts/config/                     # once a Run exists: one config per Design Run
├── runs/
│   ├── rp-struct-NN.md                 # when used: Page Runs
│   ├── rp-sec-NN.md
│   ├── rp-para-NN_Pxx[-Pyy].md
│   └── rdNN_commission|generate|verify_*.yaml
├── results/
│   └── rdNN_commission|generate|verify_*/
│       ├── result.yaml or decision.yaml
│       ├── checks.yaml                # Generate and Verify
│       ├── content/                   # Generate: the draft bytes
│       ├── render/                    # optional Run-local pictures, measurements, manifest.json
│       └── runtime.yaml
└── delivery/
    ├── render/                         # legacy display evidence; new pictures stay in Results
    └── web|latex|word/                 # when used: Page delivery
```

`new-folder` writes only the Page and the register; everything else appears
when the step that writes it runs. Commission decisions live in
`results/rdNN_commission_*/decision.yaml`, never under `outline/`. Every
Design Run keeps the same stem across run record and Result. Completed Results
and decisions are immutable. Workers render inside their own Result. The presenter
reads those pictures without copying or modifying them; Delivery shows only the
ready candidate. Existing `delivery/render/manifest.json` remains a legacy display
source for exact candidate versions, never a second Result or Run.

## Commission = bounded design bet

The Commission Run names the Design Item it serves (`item: ITEM<NN>`) and
pins its config (the goal sentence, stance, basis, mode, expected, falsified,
the compiled criteria, the raw rule text, unit shape/count, and
`max_iterations: 2`, the worker's budget inside one Generate run) and the
item's evidence files, each with sha256. It does not pin the Brief version,
the board's `reads:`, or venue packs. The config carries one `design_intent`:

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
power, or measured winner. `expected_effect` and `failure_condition` state
design quality a reader can check now (a first-time reader can say who sent
it and what to do); they may name what a later experiment will check, but the
Design Runs judge design quality only.

## Evidence and Page interlock

Keep signed handoff, factual evidence, inspiration, and design intent distinct.
Pin the exact authority/source path and hash. A Page `rp-*` Run is never Design
evidence or Design authority.

The Verify Result records the exact draft hash and independent review; the
insight pins live on the Commission and on each Generate and Verify run record.
The Verify-passed candidate is the Folder's Design handoff consumed by Page
CHECK. Page CHECK verifies the projection; it does not ask the same candidate
decision again.

Page and Design Runs may proceed when their own dependencies are ready. Page
release waits for every Page promise and bound Design Result it presents.

## Closure

A Result becomes ready for Delivery only when an independent Verify passes and
the records check is clean; no second person decision closes the item.

Design closes when every commissioned Run is truthfully terminal and required
independent verification is complete. Page closes separately after release
and fresh CHECK. Preserve failed and superseded Runs; historical decisions
remain readable only as legacy evidence.

Stop after Verify pass and Delivery handoff. Implementation, sending, allocation, testing, and
measurement belong to downstream owners.

## Clean-break contract

Unsupported Design bytes are not readable history: legacy shapes are refused,
never reinterpreted. Historical `rdNN_adopt_*` records from the retired flow
may be read only as legacy Delivery evidence; new writers must not create them.

This skill has one current grammar only: Design v0.4.0, v2 Ticket/Result
contracts, the `2-Design/Design-NN-…` folder, and
`rdNN_commission|generate|verify_*` ids. It does not read, migrate,
route, validate, or continue v1 Tickets/Results, D0-D5/GD0-GD6,
`rNN_design_*`, `design/DU*/`, `2-DS-design/DS*`, PageX, or previous
phase-shaped Design folders; the workbench serves them with HTTP 410. A decisive
unsupported marker ends inspection. An old `DS` link is rewritten to the
`Design-NN` folder only when the file it names no longer exists, so a DS
folder still on disk answers 410 for itself. There is no compatibility or
migration path.

A closed record is not asked to migrate. Move the retired folder under the
board's `_archive/` and drop its row from `board.md` `## Pages`: the board
checker leaves every `_` folder unjudged (the reading `check_draw_folders`
already states, "a person's deliberate parking"), the bytes stay on disk for
the Log to cite, and the old link heals to the `Design-NN` folder that
replaced it. Parking is not migration and not reinterpretation: nothing in
the archived folder is read, and the live board no longer claims it.
