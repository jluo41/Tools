---
name: hai-ideation
description: "Owns Idea Blocks: a direction Block, one Idea Job per candidate, evaluation Tasks and human-selected Paper handoff. Generates evidence-grounded candidates and tests novelty, feasibility and journal fit. Use for research directions and journal targeting. Trigger: ideation, research idea, novelty check, journal fit, /hai-ideation."
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill, Bash(*), mcp__codex__codex, WebSearch, WebFetch, Agent, mcp__codex__codex-reply, mcp__manual_review__review, mcp__manual_review__review_reply
metadata:
  version: "0.9.0"
  last_updated: "2026-11-24"
  folder_owner: canonical
  primary_face: direction
  page_ruling: none
  # version history: ./CHANGELOG.md
---

# /hai-ideation · evidence-grounded directions

`hai-ideation` is the semantic layer between the two execution banks and
the Paper journey:

```text
Task Run/Results ──┐
                   ├─ 1 GENERATE ──▶ Direction Block + admitted Idea Jobs
Discovery Results ┘                            │
                                               ▼
                   sync ─────▶ optional Paper projection
                                               │
                                               ▼
                                      2 TEST each Idea
                                  novelty · feasibility · journal fit
                                               │
                   sync ─────▶ optional Paper projection
                                               │
                                               ▼
                                      3 SELECT portfolio
                                  human idea + target decision
                                               │
                                               ▼
                                      bounded handoff → linked Paper Block
```

It owns the Generate/Test/Select capability routing, bundle, semantic synthesis, card
vocabulary, comparative venue-fit reading, Paper sync packet, sole human
selection record, and final Paper handoff. Its numbered children own the craft
inside each capability group. It does not own external source retrieval, internal
computation, a binding venue contract, Paper Page prose, a Story, or citation
authority.

## Start with the requested outcome

Brainstorm provisional ideas inline, test one Idea on the requested axes, or
maintain a durable portfolio for Paper. Missing evidence stays provisional or
HOLD and names the next owner action. Inline work does not create a portfolio
unless the user asks to keep it. The person decides each Idea and target; the
machine compares options and prepares the record.

For durable execution, read [references/workflow-runs.md](references/workflow-runs.md):
the Workflow is a list of owner-native Runs with explicit dependencies.
Generate/Test/Select are capability groups used as internal Steps, not Run ids.
A Run has its own commissioned target and closure; a Gate resolves a condition;
a projection displays another artifact's authority; a receipt preserves what
happened. A router invocation or a receipt alone is not a Run.

## Paper and Page entrypoints

All Paper projection routes below apply only when a Paper is already bound,
explicitly requested, or is an existing legacy Paper-local portfolio. A new
Idea Job's missing Page binding does not create a Paper or prevent selection.


`hai-paper` may route semantic idea work here. `hai-paper-ideation`
loads this owner when a Paper Idea portfolio needs semantic work or sync.
`hai-draft` resolves that adapter for an Ideation Page and owns Page writing,
release and delivery. Load only the requested capability and reuse already
loaded owners; do not recursively re-enter the routers. An Ideation-only audit
stays within its declared read-only scope. Sync/release does not create or
replace the sole I3 human selection receipt.

## Numbered capability families

The door is the one listed skill; every stage specialist we wrote and every vendored
original is a part of it, read from `_parts/<name>/PART.md` (JL 261026: other people's
skills are not called directly, they live in parts). The stage vocabulary stays 1 Generate,
2 Test, 3 Select; the numbered folders are gone. `task/` keeps its numbers as permanent
domain ids.

```text
ideation/
├── hai-ideation/                     public door + shared contracts
│   └── _parts/
│       ├── generate/                     1 · evidence → diverse admitted cards
│       ├── test/                         2 · stage router + test matrix
│       ├── novelty-check/                2 · claim × closest-work verification
│       ├── pressure-test/                2 · falsifiability + feasibility
│       ├── journal-fit/                  2 · broad screen + deep venue fit
│       ├── nature-paper-review/          2 · Nature-family editorial overlay
│       ├── select/                       3 · portfolio + human gate + handoff
│       ├── framing-research-questions/   original, science-superpowers · fuzzy interest → falsifiable question
│       ├── kill-argument/                original, ARIS · two-thread adversarial attack and defense
│       ├── paper-reviewer/               original, nature-paper-skills · reviewer-side critical evaluation
│       ├── idea-creator/                 original, ARIS · generate and rank ideas from a direction
│       └── aris-novelty-check/           original, ARIS · literature novelty sweep (ours is novelty-check)
```

Read only the current stage's part (`_parts/<stage>/PART.md`). `hai-ideation test` loads its specialist for
the requested axis; a generic test loads novelty, pressure, and journal fit,
while Nature review is loaded only when the user names Nature or a
Nature-family target remains live. Each specialist is directly invocable for
a one-off task without forcing the durable owner-bound Workflow.

Ours run by default. A vendored original runs only when the user names it or a
stage skill selects it as an independent second pass: `hai-ideation generate`
may call `framing-research-questions` to sharpen a fuzzy interest into a
falsifiable question (that question is the Idea Card's `question`, the Idea's
name on the Paper Ideation Page and its Workbench card; `title` is only a
handle) and `idea-creator` as an alternate generation lens;
`hai-ideation novelty-check` compares against `aris-novelty-check`;
`hai-ideation pressure-test` against `kill-argument`;
`hai-ideation nature-paper-review` against `paper-reviewer`. An original's output is a
proposal packet: the stage skill normalizes it, records it in the receipt, and
keeps every authority listed in
[references/external-skill-map.md](references/external-skill-map.md). The
originals never write cards, select an Idea, or open a Run.

## Boundary and loading order

Choose the operating mode before loading owners:

- **build/refresh** loads every owner needed to create or change evidence,
  cards, fit, receipts, or handoff;
- **read-only audit** loads this skill and its directly named card/receipt
  references, then inspects only the supplied Ideation artifact and owner
  artifacts it directly cites. A missing receipt or contract is reported as
  `HOLD`; it does not authorize an archive-wide search, browsing, or Page
  lifecycle crawl.

Load the relevant owner before acting on that owner's artifact:

1. `hai-task` for internal Task Runs, Results, and reports.
2. `hai-discovery`, `hai-discovery-search`,
   `hai-discovery-review`, and `hai-discovery-synthesize` for external
   search, per-Subject review, cross-Result synthesis, canonical Subject
   resolution, and Discovery Result/Bib reuse.
3. `hai-run` whenever a proposed action might be an addressable Run.
4. `hai-paper-venue` when a shortlisted target needs a new or refreshed
   versioned Venue contract. It describes one desk; it never chooses the idea's
   target.
5. `hai-paper-ideation` after Generate or Test when syncing the evolving
   portfolio into the Paper-specific P0 cockpit, and after Select when
   projecting the final verdict/target/`went to` edges. That adapter must use
   the current `hai-draft` update boundary: a working projection may be
   refreshed without publishing adopted Page Content or delivery. Load the
   base Page workflow only when actually updating that Page, not for an
   Ideation-only audit.

Then load the current numbered capability owner:

1. `hai-ideation generate` for evidence-bounded candidate generation and
   admission.
2. `hai-ideation test` for the test matrix, plus only the requested
   novelty, pressure, journal, or Nature specialist.
3. `hai-ideation select` for comparison, the human decision receipt, and
   Paper handoff.

Discovery is the external-evidence executor: its live work is search, per-source
review, and cross-Result evidence synthesis. A checked Discovery
`hai-discovery-synthesize` Page is the input to this layer. Discovery has no Idea route or
compatibility redirect; new semantic direction and Idea Cards start here.

## Grain and durable home

Read [CONSTITUTION.md](CONSTITUTION.md) and
[references/idea-block.md](references/idea-block.md) before saving new work.
One Block holds a bounded research direction. Each admitted candidate is one
Job with one stable `iNN` Card. Its Tasks answer development/evaluation
questions; they apply skills as methods, with several skills possible in one
Task. The Job remains the idea's home when a linked Paper is created.

```text
<project>/paper/Idea-<Slug>/          beside Paper- and Grant-; no ideation/ world (JL 261124)
├── board.md + ideation.yaml         direction and pointer-only Job index
└── jNN_<idea>/                      one Idea, existing unit schemas
    ├── ideation.yaml                layout: idea-job; address: Idea-<Slug>.jNN
    ├── cards/ + bundle/             one Card, context and evidence pointers
    ├── workflow/ + projection/      assessments, decisions and sync revision
    ├── handoff/                     human-selected Paper destination
    └── tNN_<question>/              bounded evaluation or development
        └── runs/run-assess-<target>/ shared soft Run, if commissioned
```

Local assessment Runs write reviews and decision records. Scientific
computation remains in Work; external evidence acquisition remains in
Discovery. Reuse their full owner-qualified Results. No skill invocation,
card edit, matrix refresh or sync operation automatically creates a Run.

An existing multi-card Task unit remains readable at its current path. It
keeps its original evidence and projection gates. Do not relabel it as a
single-idea Job or move it implicitly. A requested conversion needs an
identity/path map and preserved immutable history; see the Block contract.

Read [references/evidence-bundle.md](references/evidence-bundle.md) for evidence
pointers, [references/idea-card.md](references/idea-card.md) for scientific
fields, [references/workflow-table.md](references/workflow-table.md) and
[references/workflow-runs.md](references/workflow-runs.md) for owner routes,
[references/receipts.md](references/receipts.md) for assessments/decisions,
[references/venue-fit.md](references/venue-fit.md) for target comparisons, and
[references/manifest-and-sync.md](references/manifest-and-sync.md) for Job
manifests and optional Paper projections. The
[example](references/end-to-end-example.md) separates new and legacy layouts.

## Type contract

For `task-type: ideation`, read [references/assessment-task.md](references/assessment-task.md)
for plan/build/run/audit. This is authored scientific reasoning about owner
evidence, using shared soft Runs; it has no generated scientific Result.

```yaml
task-type: ideation
skill: hai-ideation
does: Develop or assess one bounded question about its parent Idea Job.
worker: Agent applies the requested Ideation parts; no generated campaign is required.
config: Frozen inputs, semantic revision and criterion in the soft Run Ticket.
ticket: runs/run-assess-<target>/run-assess-<target>.md; hai-run soft writer.
result: Authored assessments/*.yaml with full assessment bindings and Card pointers.
heavy: none
roles: [check, describe]
companions: [hai-task, hai-run, hai-discovery]
plan_sample: none
```

## Verbs and routing

```text
/hai-ideation <direction>              inspect, bundle, synthesize
/hai-ideation generate <unit>          run 1_generate
/hai-ideation test <unit>              run the complete 2_test matrix
/hai-ideation novelty-check <idea>     run the claim-level novelty specialist
/hai-ideation pressure-test <idea>     run falsifiability + feasibility checks
/hai-ideation journal-fit <idea>       broad-screen; deep-fit finalists
/hai-ideation nature-paper-review <idea>  apply the Nature editorial overlay
/hai-ideation sync <unit>              refresh the P0 working projection
/hai-ideation select <unit>            record the person's idea + target decision
/hai-ideation handoff <unit>           emit the Paper P0 packet
```

For a missing external source, first scan the local Discovery bank. If no
completed Result satisfies the frozen question, request a Discovery
`source-map` or `source-reading` Task and route acquisition to
`hai-discovery-search`. Discovery's `discovery.yaml` remains
consumer-unaware: the ideation request is recorded in this unit's workflow
receipt, not inserted as a parent or consumer field in the Discovery bank.

For a missing internal fact, reuse an existing Task Result or commission a Task
Run only when the analysis has its own target, Ticket, Result, and acceptance gate.
Do not manufacture a local Result to make a card look supported.

## Semantic protocol

Work through the numbered families, repeating an owner route when evidence
changes:

1. **1 Generate:** freeze the direction, scope, time boundary, and decision
   rule; build the evidence bundle; cluster signals without erasing
   contradictions; generate diverse candidates; deduplicate; and admit only
   cards with a falsifiable proposition, method, minimum experiment, expected
   outcome, failure reading, and explicit Core Claims. New claims enter Test
   as `unverified`, never as novel by construction.
   Refresh `projection/paper-ideation-sync.yaml` and, when a Paper P0 path is
   in scope, ask `hai-paper-ideation` to project the Direction, Discovery
   Landscape, Opportunity Map, and candidate set into that same evergreen Page.
   Treat this as a semantic-source update followed by a Page working-projection
   update; do not claim that adopted Page Content or delivery is current unless
   the Page release barrier has opened and `hai-draft-writing` has completed
   its Page-level pass.
2. **2 Test:** run every admitted card through claim-level closest-work
   verification, falsifiability and feasibility review, and broad journal
   screening. Deep-fit live finalists against current versioned Venue
   contracts. Apply the Nature overlay only to a named Nature-family
   candidate. Preserve the adversarial rejection, defense, unresolved gaps,
   and reroute; do not collapse novelty and identification credibility.
   Refresh the sync packet whenever evidence adds, changes, merges, eliminates,
   or reorders an Idea. When a Paper is bound, route the changed packet
   through its P0 working projection boundary; a changed `sync_revision` alone is not a Page release.
3. **3 Select:** compare and, when useful, order candidates by explicit novelty delta,
   testability, evidence coverage, cost, and risk. The machine may recommend;
   only a person may select, defer, abandon, choose the intended target and
   article category, or authorize the Paper handoff. `PROCEED` and
   `PROCEED WITH CAUTION` both map to selection; the latter must name accepted
   risks. A person may select none, one, or several ideas. Each selected Job
   has its own target decision and normally routes to its own Paper Block;
   order alone is never a selection receipt. Explicit split/merge decisions
   preserve all source Jobs and their lineage.

The bundle is a manifest of pointers, not a copy of Result Cards, facts,
reports, or BibTeX. A Discovery citation is load-bearing only when
the direct Result Card, matching one-entry Result Bib, and runtime verification
receipt are reachable. A derived Discovery aggregate Bib is a navigation aid,
never a substitute for that lineage. Internal evidence must likewise retain
its owner path, status, and locator.

## Venue and Paper boundary

Ideation exposes two pointer-only adapters with different authority:

```text
projection/paper-ideation-sync.yaml   I1/I2 working state · no selection
handoff/paper-ideation.yaml           I3 human-selected idea-target pairs
```

The sync packet begins after Generate and is refreshed through Test. It carries
the Direction Card, accepted Discovery synthesis pointers, a Discovery
Landscape summary, an Opportunity Map, every admitted/deferred/eliminated Idea
Card, the current Test Matrix, and open gaps. `hai-paper-ideation` uses it
to maintain the bound Paper's evergreen Ideation view. A new Idea Job
may remain unbound throughout Generate/Test/Select; its missing Paper view is
not a scientific blocker. Existing Paper-local Task portfolios retain their
legacy projection gates. The Page
may summarize and display those pointers; it does not become a second Idea
portfolio, evidence store, or selection authority.

### Page projection boundary

`sync_revision` is the current semantic revision of the Ideation unit. It is
not a promise that the P0 Page's adopted Markdown or delivery has already been
rewritten. The sync packet also carries a `projection.change_class`, which
selects the narrowest Page route; the revision number alone identifies the
semantic source (no content hash). A P0 update has three
independently reportable surfaces:

```text
semantic source       Ideation cards + sync packet                 current revision
working projection    Page Outline/preview/Bullet Workspace        may be current first
adopted release       Page Content + declared delivery             waits for Page release
```

When a Generate, Test, or Select result changes, update the semantic source and
route the packet to `hai-paper-ideation`. `state` changes refresh the
generated working projection; `portfolio` changes refresh it by stable
`idea_id` and inspect whether the Page shell is affected; `structure` changes
stop at the Page OUTLINE/SHAPE workflow until any required human decision is
made. Ideation does not send prose changes through this adapter. A narrow Page
update may refresh the working projection and leave adopted Content and
`delivery/` stale by design. Only after all required Page Runs and evidence
Results are ready may `hai-draft-writing` perform the Page-level CONTENT pass
and refresh delivery.

The sync operation itself is not a Page Run, does not mint `rpNN`, and does not
create a local Ideation Run. Every returned P0 status must report the working,
release, and delivery surface states separately, including the consumed
revision and receipt where present. I3 selection remains the sole human
authority even when the working projection is current.

I3's versioned selection receipt (current view: `workflow/selection.yaml`)
is the single human authority for selecting
an Idea, target/category, accepted risks, and Story route. The Paper P0 Page
only projects that receipt into verdict, target, and `went to` fields. Page
approval or CHECK cannot create or override an Ideation selection.

Ideation does not itself create the Paper repository, P0 Page, Story, Venue
Page, binding desk rule, or manuscript content. After selection,
`handoff/paper-ideation.yaml` contains paths, IDs, statuses, claim-level
support, novelty readings, pilot/feasibility receipt or waiver, Venue Fit Card
and contract paths, the sole human selection receipt, latest sync packet, and
hard limits. It duplicates neither evidence nor venue rules.

New selected Idea Jobs normally route to separate Paper Blocks and their Stories.
An existing Paper-local portfolio retains its distinct Story routes
(`Story-A`, `Story-B`, ...); it is not migrated by selection. A later target change
requires a new human receipt and refreshed Story/Venue binding. Ideation owns
the person's intended target at G0; the Story confirms that choice as its
current operational target and owns every later rebind. A legacy Story path
such as `Story01-seed` may satisfy G0 when the receipt records its canonical
`Story-A` role and both artifacts link to each other; migration does not mint a
duplicate Story or treat historical `pagex/` navigation as a selection receipt.

## One-off mode

For an inline brainstorm or evidence map, return Direction/Idea Card-shaped
content without writing files. If the user asks to keep it, route through a
durable BJTR unit and the same owner-bound evidence rules.
In child protocols, durable ids, receipt writes and sync updates apply only
when saving a unit; one-off requests apply the scientific reasoning inline.

For one-off novelty, Journal fit, or Nature review, reuse supplied verified
Discovery Results/current Venue contracts first. In build/refresh, missing
sources route to Discovery's one-off search/read workers; binding desk facts
still require the Venue owner's verified contract before a durable selection.
Return direct links, access dates, reading depth and limitations inline.
Discovery's one-off worker mode needs no folder; do not create a durable
source bank or Ideation unit solely to answer an inline question. If the user
asks to retain evidence, follow that owner's durable Result/Bib/runtime rules.
Respect no-search and read-only audit scope: unavailable or unverified sources
remain provisional/HOLD, with the missing check named. Memory is never a
verified novelty finding or current submission rule.

## Mechanical gate check

For new Blocks, first run `scripts/check_idea_block.py <block>`; use its
`--gate <gate> --job <jNN_slug>` form for a particular Idea Job. Before
claiming a durable stage ready, run the semantic gate (Job root for the new
layout, Task root for a legacy portfolio):

```bash
python scripts/check_ideation.py <ideation-unit> --gate generate
python scripts/check_ideation.py <ideation-unit> --gate sync
python scripts/check_ideation.py <ideation-unit> --gate test
python scripts/check_ideation.py <ideation-unit> --gate select
python scripts/check_ideation.py <ideation-unit> --gate handoff
```

The checker tests artifact shape and cross-file assertions; it cannot judge
scientific novelty, editorial merit, or a person's decision. A green
mechanical gate never upgrades an unverified source or substitutes for the
specialist's evidence-bound reading.
