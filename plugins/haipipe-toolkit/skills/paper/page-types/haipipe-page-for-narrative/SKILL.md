---
name: haipipe-page-for-narrative
description: >-
  The Paper Page Type for one venue-aligned Narrative. It converts a stable Seed
  and one Venue Page into claims, argument order, reader journey, evidence and
  display allocation, and a detailed one-row-per-section outline. Use when
  designing or retargeting a paper story, deciding claim roles, repairing the
  section map, or giving Section Pages executable handoffs.
metadata:
  version: "0.3.0"
  outline:
    mode: grammar
    source: "this SKILL.md"
    shape: "first word from {Venue, Claim, Argument, Reader, Section, Evidence, Handoff}; Handoff is one page-level division, always last"
---

# /haipipe-page-for-narrative · claims in reader order

Load `haipipe-page`, then this Page Type, then `haipipe-page-workflow` for RUN.
Declare `page-type: narrative` and record the Venue Page it reads.

## 📐 Grain and boundary

There is one Narrative per target venue. A second target creates a second
Narrative reading the same Seed.

Narrative owns:

- the venue-aligned audience, editor question, promise, pitch, and framing;
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
1  Venue Position and Promise
   target · audience · editor question · contribution promise · hard constraints

2  Claim System
   claim id · exact proposition · role · importance · current evidence state · limit

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
claim has a stable id and a precise sentence:

```text
claim-id | proposition | role | evidence ids | status | boundary | lands in
```

Useful roles include setup, gap, mechanism, peak result, consequence, boundary,
and contribution. A claim may be provisional, but it may not be invisible.

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
