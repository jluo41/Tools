---
name: haipipe-ideation
description: >-
  One door over the Ideation capability groups: 1 Generate evidence-grounded
  candidates, 2 Test novelty, feasibility, journal fit, and Nature-level
  editorial shape, then 3 Select idea-and-target pairs through a human gate
  and hand them to Paper P0. Sync the evolving evidence landscape and
  candidate portfolio to the same evergreen Paper P0 page from Stage 1 onward,
  while keeping working projection separate from adopted Page Content and
  delivery.
  Use for research directions, idea generation, novelty checks, idea pressure
  tests, journal targeting, Nature-paper fit, and idea portfolios; use
  haipipe-discovery for external source execution.
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "0.5.2"
  last_updated: "2026-09-20"
  folder_owner: canonical
  primary_face: direction
  page_ruling: none
  # version history: ./CHANGELOG.md
---

# /haipipe-ideation · evidence-grounded directions

`haipipe-ideation` is the semantic layer between the two execution banks and
the Paper journey:

```text
Task Run/Results ──┐
                   ├─ 1 GENERATE ──▶ Direction + admitted Idea Cards
Discovery Results ┘                            │
                                               ▼
                   sync ─────▶ P0 working cockpit
                                               │
                                               ▼
                                      2 TEST each Idea
                                  novelty · feasibility · journal fit
                                               │
                   sync ─────▶ same P0 working cockpit
                                               │
                                               ▼
                                      3 SELECT portfolio
                                  human idea + target decision
                                               │
                                               ▼
                                      bounded handoff → Paper P0
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

`haipipe-paper` may route semantic idea work here. `haipipe-paper-ideation`
loads this owner when a Paper Idea portfolio needs semantic work or sync.
`haipipe-page` resolves that adapter for an Ideation Page and owns Page writing,
release and delivery. Load only the requested capability and reuse already
loaded owners; do not recursively re-enter the routers. An Ideation-only audit
stays within its declared read-only scope. Sync/release does not create or
replace the sole I3 human selection receipt.

## Numbered capability families

The directory numbers follow the same law as Discovery's
`1_search/2_review/3_synthesize`: they are capability groups, not BJTR levels,
Run ids, or extra folders in a project artifact.

```text
ideation/
├── haipipe-ideation/                         public door + shared contracts
├── 1_generate/
│   └── haipipe-ideation-generate/            evidence → diverse admitted cards
├── 2_test/
│   ├── haipipe-ideation-test/                stage router + test matrix
│   ├── haipipe-novelty-check/                claim × closest-work verification
│   ├── haipipe-idea-pressure-test/           falsifiability + feasibility
│   ├── haipipe-journal-fit/                  broad screen + deep venue fit
│   └── haipipe-nature-paper-review/          Nature-family editorial overlay
└── 3_select/
    └── haipipe-ideation-select/              portfolio + human gate + handoff
```

Load only the current stage. `haipipe-ideation-test` loads its specialist for
the requested axis; a generic test loads novelty, pressure, and journal fit,
while Nature review is loaded only when the user names Nature or a
Nature-family target remains live. Each specialist is directly invocable for
a one-off task without forcing the durable owner-bound Workflow.

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

1. `haipipe-task` for internal Task Runs, Results, and reports.
2. `haipipe-discovery`, `haipipe-discovery-search`,
   `haipipe-discovery-review`, and `haipipe-discovery-synthesize` for external
   search, per-Subject review, cross-Result synthesis, canonical Subject
   resolution, and Discovery Result/Bib reuse.
3. `haipipe-run` whenever a proposed action might be an addressable Run.
4. `haipipe-paper-venue` when a shortlisted target needs a new or refreshed
   versioned Venue contract. It describes one desk; it never chooses the idea's
   target.
5. `haipipe-paper-ideation` after Generate or Test when syncing the evolving
   portfolio into the Paper-specific P0 cockpit, and after Select when
   projecting the final verdict/target/`went to` edges. That adapter must use
   the current `haipipe-page` update boundary: a working projection may be
   refreshed without publishing adopted Page Content or delivery. Load the
   base Page workflow only when actually updating that Page, not for an
   Ideation-only audit.

Then load the current numbered capability owner:

1. `haipipe-ideation-generate` for evidence-bounded candidate generation and
   admission.
2. `haipipe-ideation-test` for the test matrix, plus only the requested
   novelty, pressure, journal, or Nature specialist.
3. `haipipe-ideation-select` for comparison, the human decision receipt, and
   Paper handoff.

Discovery is the external-evidence executor: its live work is search, per-source
review, and cross-Result evidence synthesis. A checked Discovery
`3_synthesize` Page is the input to this layer. Discovery has no Idea route or
compatibility redirect; new semantic direction and Idea Cards start here.

## Grain and durable home

One durable ideation unit holds one research direction and a dynamic candidate
set. There is no fixed idea count: every new admitted candidate receives the
next stable, zero-padded `iNN` card (`i01`, `i02`, ...), and one unit may hold
one, six, or many cards. Historical unpadded ids such as `i1` remain valid
identities; record their canonical alias instead of renaming an existing file
or rewriting history. Card order is
only the current comparison or attention order; it is not a claim that the
first card is objectively best and it never selects a card automatically.
Admission is explicit: assigning `iNN` makes the candidate durable. A phrase
rejected before admission may be recorded as a rejected framing with its
source and reason, but it is not retroactively promoted into an Idea Card.
When a project needs a persistent record, use an explicit BJTR container:

```text
<project>/ideations/
└── b01_<direction>_<qualifier>/
    └── j01_<inquiry>_<qualifier>/
        └── t01_<direction>_<qualifier>/
            ├── ideation.yaml
            ├── t01_<direction>_<qualifier>.md   human Direction face
            ├── bundle/evidence-bundle.yaml
            ├── cards/direction.yaml
            ├── cards/i01_<idea>.yaml
            ├── cards/test-matrix.yaml
            ├── cards/venue-fit/i01_venue-fit.yaml
            ├── workflow/                         generation, novelty, pressure,
            │                                     Nature, selection, and search receipts
            ├── projection/paper-ideation-sync.yaml  I1/I2 working-state adapter
            └── handoff/paper-ideation.yaml       only after human selection
```

`bNN`, `jNN`, and `tNN` retain their normal meanings and naming grammar. The
ideation folder is not a fourth execution bank: do not create a local `rNN`
Run, `runs/`, or `results/` lane for bundling, synthesis, or selection.
An independently closable portfolio reconciliation or pressure test is
commissioned in its owning
Task or Discovery folder, where that owner creates the full BJTR Run and
same-stem Result. References always use the owner-native full address, never a
bare local `rNN`.

The shared cross-layer interpretation of bNN/jNN/tNN/rNN and the historical
Discovery numbering retrofit lives at
`../../discovery/haipipe-discovery/ref/bjtr-alignment.md`. Ideation may reuse
the bNN/jNN/tNN address grammar for its direction container, but only the
owning Task or Discovery folder can commission the corresponding Run.

Read [references/evidence-bundle.md](references/evidence-bundle.md) for the
bundle schema and provenance rules, [references/idea-card.md](references/idea-card.md)
for Direction/Idea Card fields, and [references/workflow-table.md](references/workflow-table.md)
for the capability table; [references/workflow-runs.md](references/workflow-runs.md)
defines the Workflow Run Specs and boundaries. Read [references/receipts.md](references/receipts.md)
when writing search/return, selection, or Paper handoff receipts. Read
[references/venue-fit.md](references/venue-fit.md) whenever generating,
reviewing, or selecting journal/venue candidates. Read
[references/manifest-and-sync.md](references/manifest-and-sync.md) for the
unit manifest, Generate receipt, and Paper P0 working-state adapter. Read
[references/external-skill-map.md](references/external-skill-map.md) when
auditing where the generation, novelty, EIC, or Nature procedures came from.
Read
[references/end-to-end-example.md](references/end-to-end-example.md) when a
complete specimen is more useful than another abstract rule.

## Verbs and routing

```text
/haipipe-ideation <direction>              inspect, bundle, synthesize
/haipipe-ideation generate <unit>          run 1_generate
/haipipe-ideation test <unit>              run the complete 2_test matrix
/haipipe-ideation novelty-check <idea>     run the claim-level novelty specialist
/haipipe-ideation pressure-test <idea>     run falsifiability + feasibility checks
/haipipe-ideation journal-fit <idea>       broad-screen; deep-fit finalists
/haipipe-ideation nature-review <idea>     apply the Nature editorial overlay
/haipipe-ideation sync <unit>              refresh the P0 working projection
/haipipe-ideation select <unit>            record the person's idea + target decision
/haipipe-ideation handoff <unit>           emit the Paper P0 packet
```

For a missing external source, first scan the local Discovery bank. If no
completed Result satisfies the frozen question, request a Discovery
`source-map` or `source-reading` Task and route acquisition to
`haipipe-discovery-search`. Discovery's `discovery.yaml` remains
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
   in scope, ask `haipipe-paper-ideation` to project the Direction, Discovery
   Landscape, Opportunity Map, and candidate set into that same evergreen Page.
   Treat this as a semantic-source update followed by a Page working-projection
   update; do not claim that adopted Page Content or delivery is current unless
   the Page release barrier has opened and `haipipe-page-content` has completed
   its Page-level pass.
2. **2 Test:** run every admitted card through claim-level closest-work
   verification, falsifiability and feasibility review, and broad journal
   screening. Deep-fit live finalists against current versioned Venue
   contracts. Apply the Nature overlay only to a named Nature-family
   candidate. Preserve the adversarial rejection, defense, unresolved gaps,
   and reroute; do not collapse novelty and identification credibility.
   Refresh the sync packet whenever evidence adds, changes, merges, eliminates,
   or reorders an Idea. Route the changed packet through the same P0 working
   projection boundary; a changed `sync_revision` alone is not a Page release.
3. **3 Select:** compare and, when useful, order candidates by explicit novelty delta,
   testability, evidence coverage, cost, and risk. The machine may recommend;
   only a person may select, defer, abandon, choose the intended target and
   article category, or authorize the Paper handoff. `PROCEED` and
   `PROCEED WITH CAUTION` both map to selection; the latter must name accepted
   risks. A person may select none, one, or several cards. Each selected card
   has its own target decision and becomes its own Paper Story; order alone is
   never a selection receipt.

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
Card, the current Test Matrix, and open gaps. `haipipe-paper-ideation` uses it
to maintain one evergreen `Story00-ideation` reader-facing cockpit. The Page
may summarize and display those pointers; it does not become a second Idea
portfolio, evidence store, or selection authority.

### Page projection boundary

`sync_revision` is the current semantic revision of the Ideation unit. It is
not a promise that the P0 Page's adopted Markdown or delivery has already been
rewritten. The sync packet also carries a `source_hash` and a
`projection.change_class`; the hash identifies the exact semantic source and
the change class selects the narrowest Page route. A P0 update has three
independently reportable surfaces:

```text
semantic source       Ideation cards + sync packet                 current revision
working projection    Page Outline/preview/Bullet Workspace        may be current first
adopted release       Page Content + declared delivery             waits for Page release
```

When a Generate, Test, or Select result changes, update the semantic source and
route the packet to `haipipe-paper-ideation`. `state` changes refresh the
generated working projection; `portfolio` changes refresh it by stable
`idea_id` and inspect whether the Page shell is affected; `structure` changes
stop at the Page OUTLINE/SHAPE workflow until any required human decision is
made. Ideation does not send prose changes through this adapter. A narrow Page
update may refresh the working projection and leave adopted Content and
`delivery/` stale by design. Only after all required Page Runs and evidence
Results are ready may `haipipe-page-content` perform the Page-level CONTENT pass
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

Multiple selected cards route to distinct Stories (`Story-A`, `Story-B`, ...);
they do not become competing Ideas inside one Story. A later target change
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

Run the checker before claiming a durable stage ready:

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
