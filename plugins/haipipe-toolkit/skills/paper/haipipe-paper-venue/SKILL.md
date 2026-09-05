---
name: haipipe-paper-venue
description: >-
  Paper Page Type for one external submission target: a journal, funder, or
  patent office. Separates binding desk rules from observed venue patterns,
  records provenance, and hands a verified venue contract to Narrative and
  Section Pages. Use when researching, creating, refreshing, or comparing a
  venue Page.
metadata:
  version: "0.6.0"
  last_updated: "2026-09-04"
  page_ruling: none
  outline:
    mode: fixed
    source: "this SKILL.md"
    shape: "Target Identity and Scope → Fit and Desk Reject → Venue Structure → Unit Guidance → Submission Rules → Cost Clock and Odds → Gaps and Handoff"
---

# /haipipe-paper-venue · make one external desk inspectable

For a concrete Venue Page RUN, load `haipipe-page`,
`haipipe-page-workflow`, the current Page phase, `haipipe-paper-workflow`, this
Page Type, and its phase references in canonical order. Name the Page
`QBv<n>-<slug>.md`; that filename is its sole type key under the current base
resolver.

## 🏛 Grain and boundary

One Venue Page describes one submission target. It does not choose the paper's
target and does not write the paper's Narrative.

```text
Venue Page   what this external desk requires, rewards, rejects, and costs
Narrative    how this paper is told for that desk
Section      how one unit satisfies its Narrative row and desk constraints
```

A target may be a journal, funder, conference, regulator, or patent office. Use
the target's own document units when journal section kinds do not apply.

**The bank is a library, not a phase** (JL 260823). Venue Pages live in the
shared QBv bank and sit outside the paper journey: nothing about a paper
advances by writing one. The decision to target a desk lives on that paper's
Narrative §1, which binds the bank page and never restates it; a missing desk
gets its bank page minted as a sub-step of starting that Narrative.

## 📚 Two profiles (0.4.0)

A venue page declares which of two profiles it is, because their evidentiary
floors differ by an order of magnitude and a reader must not misread one as an
underweight instance of the other:

```text
PACK-BACKED    an exemplar pack sits behind it · budgets are measured ·
               PACK OBSERVATION rows are expected throughout
               (reference implementation: QBv1-misq)
CfP-ONLY       a call-for-papers or published rule sheet is the ONLY source ·
               every length is a DESK RULE · the page SAYS, where a pack
               observation would normally sit, that none exists
               (reference implementation: QBv17-wise)
```

A CfP-only page is legitimately short. What it may never do is fill the gap
with invented observations; its two honest moves are the DESK RULE and the
marked OWN ESTIMATE.

## ⚖️ Authority and provenance

Every venue statement is typed:

```text
DESK RULE          published by the target; binding at a named moment
PACK OBSERVATION   measured from exemplars; informative, not binding
PACK PRESCRIPTION  suggested by a playbook without enough observations
LOCAL DECISION     a paper-specific choice; never attributed to the desk
UNKNOWN            visible gap with an owner or refresh route
```

For desk facts record source, access date, access method, and enforcement time:
submission, revision, acceptance, or publication. When desk and pack disagree,
the desk wins for compliance and the disagreement remains visible.

## 📐 Required Content outline

```text
1  Target Identity and Scope
   target · article/application category · audience · what this Page covers ·
   the page's PROFILE, declared: pack-backed or CfP-only (0.4.0)

2  Fit and Desk Reject
   contributions rewarded · methods permitted · explicit or observed rejection tests

3  Venue Structure
   target reading/order units · total limits · required components · resolver gaps

4  Unit Guidance
   one comparable record per section/document unit: job, observed shape, budget,
   displays/citations expected, anti-patterns, source

5  Submission Rules
   format · anonymity · references · disclosures · portal · files · timing of enforcement

6  Cost, Clock, and Odds
   fees · review timing · reported acceptance information · uncertainty

7  Gaps and Handoff
   stale or missing facts · desk/pack conflicts · verified contract consumed by Narrative
```

The exact number of Unit Guidance divisions may vary with the target. Keep the
seven roles inspectable.

## 🃏 Evidence and displays

Venue Pages are evidence-heavy Pages, using the same three Outline-plugin
workspaces as every current Page:

```text
Context Workspace    desk identity, profile, requirements, related links
Bullet Workspace     venue propositions and typed Evidence Item ids
Evidence Workspace   Supporting Runs → Local Input → Local Run → typed Result
```

Desk sources and exemplars normally arrive through Discovery Supporting Run
Results. LAND freezes the chosen Results and any governed page-local captures
into one Local Input, then one local Run produces a `VALUE`, `CITE`, or
`DISPLAY` Result. Related Venue Pages and playbooks remain Context links until
a Supporting Run Result makes their content independently auditable. There is
no active PageX, probe, bibex, value, or display plugin; old lanes are
migration-only input.

Every number and binding rule must resolve to its Evidence Item plus full
Run/Result identity. A bare uncited number is an open obligation.

## 📤 Handoff

Narrative and Section Pages consume a versioned Venue contract rather than
copying the whole Page:

```text
target and category
binding rules + enforcement moments
observed patterns, explicitly nonbinding
reader order/document units
total and per-unit constraints
required displays/citations/disclosures
known conflicts, unknowns, and refresh date
```

## ✅ Closing checks

- One target and category are unambiguous.
- Every venue statement has an authority type and source.
- Every desk rule has an enforcement moment.
- Desk/pack disagreements and missing facts remain visible.
- Structure totals and per-unit guidance are reconciled or explicitly conflict.
- Narrative can consume a bounded, versioned venue contract.
- CHECK judges the rendered Page and its linked evidence before closure.

`page_ruling: none` is explicit: Venue CHECK may close the bank Page when its
semantic/mechanical contract and artifact-specific gates pass. A later
Narrative target decision remains owned by the paper journey and is not a
second Venue-page approval.

`template.md` is the scaffold for a new Venue Page. This variant owns no
scripts; Board machinery builds and checks it.
