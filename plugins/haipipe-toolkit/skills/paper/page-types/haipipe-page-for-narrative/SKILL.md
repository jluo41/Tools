---
name: haipipe-page-for-narrative
description: >-
  The Paper Page Type for one venue-aligned Narrative: how one paper is told to
  one desk. It converts the Seed's Establishment Board and one shared Venue Page
  into the paper's venue decision, claims with E-row parents, argument order,
  reader journey, evidence and display allocation, and a detailed
  one-row-per-section outline. One page per target venue, living beside the Seed
  in the story group. Use when designing or retargeting a paper story, deciding
  claim roles, repairing the section map, or giving Section Pages executable
  handoffs. Trigger: narrative page, paper story, claim system, claim roles,
  argument arc, reader journey, section map, venue decision, retarget,
  page-type narrative, /haipipe-page-for-narrative.
metadata:
  version: "0.4.0"
  last_updated: "2026-08-21"
  summary: "0.4.0 wires the joins its two 0.3.0 neighbors created (JL 260821): every claim cites its Seed E-row parent, division 1 is the paper's venue DECISION binding the shared QBv bank page, and Narratives live beside the Seed in one 0-SD-seed/ group as SD<NN> pages. Restored 260821 after a parallel-session collision reverted the file."
  group-token: "SD"
  outline:
    mode: grammar
    source: "this SKILL.md"
    shape: "first word from {Venue, Claim, Argument, Reader, Section, Evidence, Handoff}; Handoff is one page-level division, always last"
---

# /haipipe-page-for-narrative · claims in reader order

Load `haipipe-page`, then this Page Type, then `haipipe-page-workflow` for RUN.
Declare `page-type: narrative` and record the shared Venue Page it binds.

In a runtime paper board a Narrative lives BESIDE the Seed, in the one story
group, as an `SD<NN>` page (JL 260821):

```text
0-SD-seed/
├── SD00-seed/                    what the paper IS · venue-free · exactly one
├── SD01-narrative-<venue>/       how it is told to desk 1
└── SD02-narrative-<venue>/       how it is told to desk 2
```

The group law: the story group decides the telling; no manuscript prose lives
here. SD00 stays venue-free; every SD<NN> above it names its venue.

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
pagex/     Probe's accepted-Page lane: Seed, Venue, analysis, or literature Pages
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
