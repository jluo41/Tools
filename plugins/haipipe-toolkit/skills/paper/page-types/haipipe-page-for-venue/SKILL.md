---
name: haipipe-page-for-venue
description: >-
  The Paper Page Type for one external submission target such as a journal,
  funder, or patent office. It separates binding desk rules from observed venue
  patterns, records provenance and timing, exposes disagreements and unknowns,
  and hands a verified venue contract to Narrative and Section Pages. Use when
  researching, creating, refreshing, comparing, or checking a venue Page.
metadata:
  outline:
    mode: fixed
    source: "this SKILL.md"
    shape: "Target Identity and Scope → Fit and Desk Reject → Venue Structure → Unit Guidance → Submission Rules → Cost Clock and Odds → Gaps and Handoff"
---

# /haipipe-page-for-venue · make one external desk inspectable

Load `haipipe-page` first and `haipipe-page-workflow` when running the Page.
Name the Page `QBv<n>-<slug>.md`; that filename is its sole type key under the
current base resolver.

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
   target · article/application category · audience · what this Page covers

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

Venue Pages are evidence-heavy Pages:

- `bibex/` stores desk sources, exemplar citations, source notes, and the local
  bibliography.
- `probe/` stores questions such as missing limits, review timing, or unclear
  category rules.
- The storage-less value surface joins each quantitative venue fact to its
  probe-card value id `PP<NN>.v<n>`.
- `display/` may contain a fit matrix, structure table, submission checklist,
  or comparison diagram. A single Venue Page may own many displays.
- `pagex/` links reusable playbooks or related Venue Pages by bounded scope.

Every number and binding rule must be clickable or traceable to its evidence
card/source. A bare uncited number is an open obligation.

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

`template.md` is the scaffold for a new Venue Page. This variant owns no
scripts; Board machinery builds and checks it.
