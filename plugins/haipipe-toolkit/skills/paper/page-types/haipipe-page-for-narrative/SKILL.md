---
name: haipipe-page-for-narrative
description: >-
  The Paper Page Type for one venue-aligned Narrative: how one paper is told to
  one desk. It converts the Seed's §8 handoff (carrying its Establishment
  Board ids) and one shared Venue Page
  into the paper's venue decision, claims with E-row parents, argument order,
  reader journey, evidence and display allocation, and a detailed
  one-row-per-section outline. One page per target venue, in the paper's own
  narrative group (A2-NA) beside the venue-free story group. Use when
  designing or retargeting a paper story, deciding
  claim roles, repairing the section map, or giving Section Pages executable
  handoffs. Trigger: narrative page, paper story, claim system, claim roles,
  argument arc, reader journey, section map, venue decision, retarget,
  page-type narrative, /haipipe-page-for-narrative.
metadata:
  version: "0.5.1"
  last_updated: "2026-08-27"
  summary: "0.5.1 (JL 260827): gate-receipt duty sunk from the workflow's receipts law into this contract — G5's and G6's receipt Log rows live on this page; a Section page never holds a gate receipt. 0.5.0 (JL 260824): narratives move OUT of the story group into their own A2-NA-narrative group — NA<NN>-narrative-<desk>, one page per desk in arrival order, token NA — because journey 0.5.0 makes the story group the venue-free P0-P3 head (ideation, seed, roadmap, collection) and Narrative the P4 phase; SD-numbered narratives are grandfathered. 0.4.4 (JL 260824): ideation 0.5.0 vocabulary in the story-group figure (SD00 line reads 'the ideas'). 0.4.3 (JL 260824): ideation-first story order — narratives start at SD02, after SD00-ideation and SD01-seed. 0.4.2 (JL 260824): the map row names the telling's DESK ROOM files (<N>-<desk><year>/sections/...), because each telling owns a self-contained room with its own displays/ copies and reference.bib per the door's room law; board address is 0-paperboard/. 0.4.1 renames the runtime home to the A1-SD-story group under the 260823 scaffold grammar (0-SD-seed/ boards grandfathered), keeping the seed contract 0.4.0 and this file in agreement. 0.4.0 wires the joins (JL 260821): every claim cites its Seed E-row parent, division 1 is the paper's venue DECISION binding the shared QBv bank page."
  group-token: "NA"
  outline:
    mode: grammar
    source: "this SKILL.md"
    shape: "first word from {Venue, Claim, Argument, Reader, Section, Evidence, Handoff}; Handoff is one page-level division, always last"
---

# /haipipe-page-for-narrative · claims in reader order

Load `haipipe-page`, then this Page Type, then `haipipe-page-workflow` for RUN.
Declare `page-type: narrative` and record the shared Venue Page it binds.

In a runtime paper board Narratives are the P4 group of their own — one page
per desk, in arrival order, reading the story group's Seed from next door
(journey 0.5.0, JL 260824; SD-numbered narratives inside the story group are
grandfathered):

```text
0-paperboard/
├── A1-SD-story/                  P0-P3 · ideation · seed · roadmap · collection
│                                 the venue-free head this group never joins
└── A2-NA-narrative/
    ├── NA01-narrative-<desk>/    how the paper is told to desk 1
    └── NA02-narrative-<desk>/    how it is told to desk 2
```

The group law: the narrative group decides the telling, one desk one page; no
manuscript prose lives here, and every NA<NN> names its desk in its slug. The
story group stays wholly venue-free — a venue word inside A1 is a leak.

## 📐 Grain and boundary

There is one Narrative per target venue. A second target creates a second
Narrative reading the same Seed.

**The venue DECISION lives here; the venue RECORD does not.** A paper never
creates a venue page: the shared QBv bank (one consumer-neutral page per desk,
refreshed on the desk's clock) is bound through `pagex/`, and this page's Venue
division owns only the decision and its local consequences.

Narrative owns:

- the venue decision, binding the shared QBv bank page by path;
- the venue-aligned audience, editor question, promise, desk-shaped opening,
  and framing (the venue-free one-minute pitch is the Seed's, division 2);
- claims and their rhetorical roles;
- the argument arc and reader journey;
- one detailed outline row per manuscript or appendix Section;
- cross-section allocation of evidence and displays;
- the bounded packet each Section Page executes.

Narrative does not write final section prose and does not replace the source
cards it cites.

## 🧬 Required Content roles

The instance outline is a grammar, so divisions may be combined or repeated
when the paper requires it. Every role below must remain inspectable.

```text
1  Venue Decision
   the chosen desk · the bound QBv bank page · audience · editor question ·
   contribution promise · the local consequences of choosing this desk

2  Claim System
   claim id · exact proposition · E-row parent · role · current evidence state · limit

3  Argument Arc
   dependency order: what must be understood before each claim can land

4  Reader Journey
   what the reader believes, asks, sees, and concludes at each turn

5  Per-section Outline
   one detailed row per reader-ordered manuscript or appendix Section

6  Evidence and Display Allocation
   which cards, citations, values, and displays land where; conflicts and reuse

7  Section Handoffs
   one bounded execution packet per Section Page
```

## 🧾 Claims are required

Without claims there is no narrative—only a topic list. Each consequential
claim has a stable id, a precise sentence, and an E-ROW PARENT on the Seed's
Establishment Board:

```text
claim-id | proposition | E-row parent | role | evidence ids | status | boundary | lands in
```

A claim with no E-row parent is a new claim and belongs on the Seed first, or
nowhere: crowning and ordering happen here, but LICENSING happens on the
E-board, which is what keeps two Narratives from silently telling two
different papers. Useful roles include setup, gap, mechanism, peak result,
consequence, boundary, and contribution. A claim may be provisional, but it
may not be invisible.

Narrative may itself make evidence-dependent judgments. For example, “C2 is the
peak claim” depends on the magnitude, credibility, and venue fit of its support.
Such judgments use the Narrative Page's own cards and bindings. The Page is not
evidence-free merely because its output is an outline.

## 📋 The governing per-section outline

Write one row per Section in reader order. Make the row detailed enough that a
fresh Section agent does not invent the paper's logic.

```text
section-id
section kind and working title
room files · the tex under this telling's desk room, <N>-<desk><year>/sections/
reader question
reader state on entry
reader state on exit
claim role and claim ids
must establish, as propositions
evidence card ids
citation ids
value ids
display ids or explicit none
paragraph/move outline
required transition in
required transition out
venue allocation and constraints
known limitation or risk
open obligations
```

A Section Page points to exactly one current row. Reordering or materially
changing a row reopens that Section. Existing prose is input to revision, not
authority over Narrative.

## 🃏 Evidence and displays

Narrative uses the same Page-local lanes as every Page:

```text
pagex/     Probe's accepted-Page lane: the Seed (§8 handoff only — never the
           Roadmap or Collection), the bank Venue Page, analysis or
           literature Pages
probe/     Probe's Task/Discovery QA lane: unresolved judgments and missing support
bibex/     citations supporting framing, method rationale, limitations, or claims
display/   zero or more maps, tables, or figures that make the argument inspectable
```

Values remain in each probe card's `## Values` block and are cited by
`PP<NN>.v<n>`; Narrative never creates a second value store.

One Narrative may own many displays: a claim map, section matrix, evidence
ledger, or alternative arc. Each display is independently accepted. Displays
may later be consumed by the paper, but their first job here is to let a person
inspect the Narrative itself.

## 📤 Section handoff packet

Each Section receives only:

```text
Narrative row id and version
claim ids and exact propositions
reader entry/exit states
allowed evidence/citation/value/display ids
paragraph/move outline
venue allocation and hard constraints
open obligations the Section must expose, not invent answers for
```

Gates G5 (Narrative → Section) and G6 (Section → assemble) both leave their
receipt Log row on this page, stating the gate, the assertion results, and
who ticked; a Section page never holds a gate receipt.

## ✅ Closing checks

- Venue and venue-aligned promise are explicit and consistent with Seed limits.
- Every important claim has an id, exact proposition, role, landing Section, and
  evidence status.
- Every reader-ordered Section has one complete outline row.
- Every evidence/display allocation resolves or is visibly open.
- Every Section handoff is bounded and versioned.
- No final section prose or copied raw evidence has become a second authority.
- CHECK judges the built Narrative and only CHECK closes it.

This variant owns no scripts.
