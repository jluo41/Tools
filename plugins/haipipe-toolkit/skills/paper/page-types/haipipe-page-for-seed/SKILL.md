---
name: haipipe-page-for-seed
description: >-
  The Paper Page Type for one venue-free Seed per paper. It establishes the
  stable research identity, question, stakes, available source Pages, headline
  establishment, boundaries, and a bounded handoff to venue-specific
  Narratives. Use when starting a paper, repairing its identity, separating the
  paper from venue framing, or retargeting without rewriting what the study is.
metadata:
  outline:
    mode: fixed
    source: "this SKILL.md"
    shape: "Identity → Research Question → Stakes → Source Pages → Establishment and Boundaries → Narrative Handoff"
---

# /haipipe-page-for-seed · establish what the paper is

Load `haipipe-page` first and `haipipe-page-workflow` when running the Page.
Declare `page-type: seed`.

## 🌱 Grain and boundary

There is exactly one Seed per paper. It survives retargeting unchanged.

```text
Seed       what the work is; venue-free
Venue      what one external desk requires
Narrative  how this work is told to that desk
Section    how one Narrative row becomes manuscript content
```

Seed must not name a selected venue, editor, target audience, venue-specific
pitch, section order, or submission rule. If changing the target desk requires
changing Seed, the boundary has leaked.

## 📐 Fixed Content outline

Use these six divisions in order. A title may add a paper-specific phrase after
the fixed role.

```text
### 1 · Identity
working title · one-sentence identity · unit of analysis · scope

### 2 · Research Question
primary RQ · secondary RQs only when indispensable · answer form

### 3 · Stakes
real-world problem · intellectual problem · why this study is worth finishing

### 4 · Source Pages
existing Board Pages and task/discovery outputs the paper may read by scope

### 5 · Establishment and Boundaries
what is established · provisional · absent · hard limits and non-claims

### 6 · Narrative Handoff
the smallest typed packet from which any venue-specific Narrative can begin
```

The Narrative handoff contains:

```text
identity          one sentence
primary RQ        one answerable sentence
stakes            practical + intellectual
established       proposition ids and source Page/card ids
provisional       proposition ids and missing obligations
hard boundaries   what the paper will not claim
open tensions     what Narrative must order rather than silently settle
```

## 🃏 Evidence rule

Seed is not evidence-free. If it states a factual proposition—sample coverage,
the existence of a gap, or a headline association—it must bind that statement
to Page-local evidence.

- Probe routes existing accepted Board Pages through its `pagex/` lane.
- Probe routes unresolved Task/Discovery questions into QA cards in `probe/`.
- Citations live in `bibex/`.
- A display is allowed when it materially clarifies identity, scope, or
  establishment; it lives in `display/` and has its own acceptance state.

Do not copy raw evidence into the handoff. Hand off ids, status, interpretation,
and boundaries.

## ✅ Closing checks

- One identity and one primary RQ are visible.
- Every establishment is marked established, provisional, or absent.
- Every consequential factual statement resolves to a Page/card/source id.
- The handoff can seed more than one venue-specific Narrative.
- No venue, editor promise, venue-specific audience, or manuscript prose leaked
  into the Page.
- The current outline is approved and CHECK closes the built Seed version.

This variant owns no scripts. The generic Page template and workflow own the
frame, plugins, receipts, and lifecycle.
