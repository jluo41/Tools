---
name: haipipe-paper-narrative
description: >-
  Paper journey phase P3 (Narrative) and the Page Type contract for one
  venue-aligned narrative: how one paper is told to one desk. Turns the Seed's
  handoff plus a Venue Page into claims, argument order, a first-view
  Section-control table, display allocation, and a one-row-per-section outline. Use when designing or
  retargeting a paper story, deciding what the paper says and refuses to say,
  or repairing its section map. Trigger: narrative page, paper story, claim
  roles, section map, page-type narrative.
metadata:
  version: "0.8.1"
  last_updated: "2026-09-02"
  group-token: "NA"
  outline:
    mode: grammar
    source: "this SKILL.md"
    shape: "first word from {Venue, Claim, Argument, Reader, Section, Evidence, Handoff}; Handoff is one page-level division, always last"
---

# /haipipe-paper-narrative · claims in reader order

Load `haipipe-page`, then this Page Type, then `haipipe-page-workflow` for RUN.
Declare `page-type: narrative` and record the shared Venue Page it binds.

## 🧭 Journey phase

This skill is journey phase P3 Narrative (tell) of the paper journey and owns
the `page-type: narrative` contract below. Enter through gate G4, reading the
Seed's handoff (never the Roadmap directly). Exit through gate G5: one bank
page bound, every claim parented to an E-row, every section-map row budgeted.
`haipipe-paper-workflow` holds the full gate assertions; this block only places
the phase. The page itself always runs through `/haipipe-page` and
`haipipe-page-workflow` (OUTLINE → … → CHECK), never a private lifecycle. In a
runtime paper board Narratives close the story group: one page per desk, in
arrival order after the venue-free head, reading the Seed from the same group
(tokens re-ruled JL 260831; a separate `A2-NA-narrative` group with NA-numbered
narratives is grandfathered): ```text 0-paperboard/ └── A1-Story/ ├──
Story00-ideation · Story01-seed · Story02-roadmap   the venue-free head ├──
Story03-narrative-<desk>/ how the paper is told to desk 1 └──
Story04-narrative-<desk>/ how it is told to desk 2 ``` The group law: the
narrative pages decide the telling, one desk one page; no manuscript prose
lives here, and every `Story<NN>-narrative` names its desk in its slug. The
head pages (Story00 to Story02) stay wholly venue-free; a venue word enters
the group only through a narrative page, anywhere else it is a leak.

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
- one generated Section-control table as the first, open view of `## Outline`;
- one optional story-flow diagram inside the folded Argument Arc Content
  division or in `studio/draw/`, never ahead of the table;
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

## 🗺️ The first-view Section-control table

The Narrative's first job is to make the whole paper inspectable at one glance.
The page keeps the base Page structure unchanged: `Opening → Outline → Content
→ Aims`. `Outline` opens by default. For `page-type: narrative`, its first view
is a generated Section-control table; the generic plan-and-evidence table stays
available underneath in a closed drawer. Never hand-copy either table into a
Page-authored `## Outline` or legacy `## Diagram` block.

The Section-control table is projected from the detailed rows in the
Per-section Outline Content division. Those rows are the authority; changing a
row changes the projection on rebuild. The view is the executive compression
of the Claim System, Argument Arc, Reader Journey, Per-section Outline, and
Handoffs. Every live manuscript and appendix Section appears exactly once, in
reader order.

```text
| Section | reader job | outline shape | must say / establish | must not say | evidence gate or cut rule | reader exit |
```

Each row must let a person answer, without opening the Section:

- why this Section exists in the story;
- the ordered moves or paragraph shape it executes;
- which proposition or boundary it must establish;
- which attractive but unlicensed claim it must refuse;
- what evidence must be accepted, and what is cut when it is absent;
- what the next Section may assume when the reader exits.

Keep cells compact and proposition-level. Use claim and Evidence Item ids where
they reduce ambiguity. A conditional row names its cut rule explicitly; it
never makes optional evidence look required for the sufficient paper. Retired
Sections do not receive live rows. The generated table, detailed Section rows,
and handoff packets must agree; any disagreement reopens Narrative.

The reader-order story flow remains useful but secondary. Put a compact ASCII
flow inside the Argument Arc Content division, where Content is shut by default,
or create a real scene under `studio/draw/`. It must not precede or duplicate
the default Section-control table.

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

The detailed row expands its corresponding generated Section-control row.
It must include machine-projectable `QUESTION`, `MOVES`, `ESTABLISH`, `REFUSE`,
`GATE`, and `EXIT` fields. It may add files, budgets, ids, and open obligations,
but it may not change the projected row's reader job, say/refuse boundary,
evidence gate, or exit state silently.

## 📊 Runs Results boundary

Narrative decides what a result does in the story; it is not a regression-output
store. The Section-control table may show:

- the claim's disposition: accepted, conditional, or cut;
- direction and a clinically meaningful scale category only when needed to
  decide prominence or order;
- the Evidence Item id and the gate or cut rule.

It does not show full model tables, logs, exploratory output, or a pile of
estimates. Exact estimates, confidence intervals, P values, sample sizes,
cluster counts, and run-specific model/specification labels remain in accepted
probe `## Values` records and the Results Section. The table may name an
estimator family such as OLS/LPM when that identity defines the paper boundary
or distinguishes the licensed analysis from refused alternatives such as IV or
DID. Evidence/display chips may open their owning accepted artifact on demand;
that linked material is not copied Narrative content and does not relax the
table's compression rule. A pending Run is named as a gate, never narrated as a
provisional finding. A Run cannot license a new claim: the Seed E-row licenses
it, Narrative allocates it, and the Section reports it. Optional evidence that
does not land is cut without making the sufficient paper look incomplete.

## 🃏 Evidence and displays

Narrative uses the same Page-local lanes as every Page:

```text
pagex/     Probe's accepted-Page lane: the Seed (§8 handoff only — never the
           Roadmap), the bank Venue Page, analysis or
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
- `Outline` opens with one generated Section-control table; the generic plan
  table is secondary and folded, and no Page-authored Outline/Diagram survives.
- Every Section-control row states the Section's job, shape, say/refuse
  boundary, evidence gate or cut rule, and reader exit.
- Claims, detailed Section rows, generated table, and handoffs tell the same
  paper in the same order.
- Runs Results are compressed to claim disposition, a necessary direction or
  scale category, and the evidence gate; exact result packets stay downstream.
- Every important claim has an id, exact proposition, role, landing Section, and
  evidence status.
- Every reader-ordered Section has one complete outline row.
- Every evidence/display allocation resolves or is visibly open.
- Every Section handoff is bounded and versioned.
- No final section prose or copied raw evidence has become a second authority.
- CHECK judges the built Narrative and only CHECK closes it.

This variant owns no scripts.
