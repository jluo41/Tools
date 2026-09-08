---
name: haipipe-ideation
description: >-
  Semantic ideation layer that turns internal Task evidence and external
  Discovery Results into grounded Direction and Idea Cards, pressure-tests
  claims and journal fit, records a human idea-and-target selection, and
  prepares a bounded handoff to haipipe-page-ideation. Use for
  evidence-grounded research directions, novelty review, and idea-to-venue
  portfolios; use haipipe-discovery for external search/read/synthesis,
  haipipe-paper-venue for one target's verified contract, and
  haipipe-page-ideation for the paper's P0 page.
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "0.2.1"
  last_updated: "2026-09-07"
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
                   ├─ evidence bundle → Direction Card → Idea Cards
Discovery Results ┘                         │
                                            ├─ novelty + feasibility
                                            ├─ Idea × Venue Fit Cards
                                            ├─ human idea + target selection
                                            └─ bounded handoff → Paper P0
```

It owns the bundle, semantic synthesis, card vocabulary, comparative venue-fit
reading, selection record, and Paper handoff. It does not own external source
retrieval, internal computation, a binding venue contract, paper prose, a
Story, or citation authority.

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
5. `haipipe-page-ideation` only at handoff, when selected cards are ready to
   enter the Paper-specific P0 page. Load the base Page workflow only when
   actually running a Page phase, not for an Ideation-only audit.

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
            ├── cards/venue-fit/i01_venue-fit.yaml
            ├── workflow/                         receipts and search requests
            └── handoff/paper-ideation.yaml       only after human selection
```

`bNN`, `jNN`, and `tNN` retain their normal meanings and naming grammar. The
ideation folder is not a fourth execution bank: do not create a local `rNN`
Run, `runs/`, or `results/` lane for bundling, synthesis, or selection. A
pressure test that is independently closable is commissioned in its owning
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
for the phase table and Run boundary. Read [references/receipts.md](references/receipts.md)
when writing search/return, selection, or Paper handoff receipts. Read
[references/venue-fit.md](references/venue-fit.md) whenever generating,
reviewing, or selecting journal/venue candidates.

## Verbs and routing

```text
/haipipe-ideation <direction>              inspect, bundle, synthesize
/haipipe-ideation bundle <unit>            freeze internal + external inputs
/haipipe-ideation search <unit>            reuse or request Discovery evidence
/haipipe-ideation synthesize <unit>        write Direction + Idea Cards
/haipipe-ideation pressure-test <unit>     fill evidence gaps through owners
/haipipe-ideation venue-fit <unit>         broad-screen all ideas; deep-fit finalists
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

Work in this order, repeating the search or pressure-test route when evidence
changes:

1. Freeze the direction question, scope, time boundary, and decision rule.
2. Build the evidence bundle from owner artifacts. Keep observations,
   interpretations, proposals, and unresolved gaps distinct.
3. Cluster convergent signals and preserve contradictions; do not average away
   disagreement or turn a search hit into a finding.
4. Generate candidate Idea Cards from the bundle. Every material claim names
   its supporting paths and whether the support is internal, external, or an
   inference.
5. Pressure-test each candidate claim-by-claim: prior work through Discovery,
   feasibility and data availability through Task, and limits through the
   source owners. A candidate is not evidence.
6. Broad-screen every admitted Idea Card for field, audience, contribution
   type, method/evidence shape, plausible article type, and obvious desk
   mismatch. Keep the screen even when the idea is eliminated.
7. Deep-fit the candidates that remain live against current versioned Venue
   contracts. Compare scope, contribution significance, novelty delta,
   method/design, evidence floor, article type, generality/impact, and
   compliance/openness. Record desk risks, missing evidence, and a reroute.
   Static rankings, remembered rules, and external skill packs may seed the
   screen but cannot establish a binding desk fact.
8. Compare and, when useful, order candidates by explicit novelty delta,
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

Ideation stops at a human decision and, for every selected card, a complete
handoff packet. It does not create a Paper repository, `Story00-ideation`,
Story, Venue Page, binding desk rule, or manuscript content. It may recommend
targets and records the person's intended target/category only after a current
Venue contract supports the deep fit. `handoff/paper-ideation.yaml` contains
paths, IDs, statuses, claim-level support, novelty readings,
pilot/feasibility receipt or waiver, Venue Fit Card and contract paths, the
human idea-and-target decision, and hard limits. It does not duplicate
evidence or venue rules.

`haipipe-page-ideation` consumes that packet, writes the Paper-specific P0
page, and binds the origin in each selected Story direction. Multiple selected
cards route to distinct Stories (`Story-A`, `Story-B`, ...); they do not become
several competing ideas inside one Story. No handoff is emitted without a
person's selection record and one selected target/category per selected card;
an unselected or target-unresolved portfolio remains in ideation. A later
target change requires a new human receipt and refreshed Story/Venue binding.
Ideation owns the person's intended target at G0; the Story confirms that
choice as its current operational target and owns every later rebind. A legacy
Story path such as `Story01-seed` may satisfy G0 when the receipt records its
canonical `Story-A` role and both artifacts link to each other; migration does
not mint a duplicate Story or treat historical `pagex/` navigation as a
selection receipt.

## One-off mode

For an inline brainstorm or evidence map, return Direction/Idea Card-shaped
content without writing files. If the user asks to keep it, route through a
durable BJTR unit and the same owner-bound evidence rules.
