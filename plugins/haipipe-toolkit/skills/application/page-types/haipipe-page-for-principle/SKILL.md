---
name: haipipe-page-for-principle
description: >-
  The Page Type contract for one PRINCIPLE page on a DesignBoard: a single executable design rule in the form because <W>, do <move>, within <rail>, citing exactly one Wisdom handoff from an InsightBoard. This is the ONLY DesignBoard layer that may read the InsightBoard; everything below it knows principles and nothing about evidence. Use when a settled handoff must become something a designer can act on, when a rule applies across several audiences, or when a design move has no stated warrant. Trigger: design principle, because do within, rail, warrant, page-type principle, /haipipe-page-for-principle.
metadata:
  version: "0.1.0"
  last_updated: "2026-08-20"
  summary: "One rule, one warrant. The only DesignBoard layer that touches the InsightBoard, which is what keeps evidence out of the design pages below it."
  group-token: "P"
  outline:
    mode: fixed
    source: "this SKILL.md"
    shape: "Rule → Warrant → Rail → Scope → Declined Alternatives"
  parent: haipipe-page-for-brief
---

# /haipipe-page-for-principle · one rule, and the evidence that warrants it

Load `haipipe-page`, then `haipipe-page-for-brief`, then this contract. Load `haipipe-plugin-pagex` to bind the Wisdom handoff.

Declare `page-type: principle`. This page lives in `<DesignBoard>/1-P-principle/P<NN>-<slug>/`.

## The one shape

Every principle page states one rule in exactly this form:

```text
because <W handoff>, do <move>, within <rail>
```

If the sentence needs an "and" between two moves, it is two principles. A rule that cannot name a `W` is not a principle, it is a preference, and it belongs in the Brief's promise or nowhere.

## The wall

```text
🔎 InsightBoard  ──── PageX ────▶  1-P-principle/   ← the ONLY crossing
                                        │
                                        ▼
                                   2-DS-design/     knows principles only
```

A Design page never binds a `W` page directly and never opens a `D`, `I` or `K` page at all. Routing every warrant through a principle is what stops design re-interpreting evidence, and it means a changed handoff reopens one principle rather than every design that leaned on it.

## Fixed Content outline

```text
### 1 · Rule                the because/do/within sentence, once
### 2 · Warrant             the W page and handoff row, bound by PageX
### 3 · Rail                what this rule forbids, inherited from the handoff
### 4 · Scope               which audiences, jobs and venues it applies to
### 5 · Declined Alternatives  moves this warrant does NOT license
```

- **Rule** is one sentence. Its `<move>` is actionable by a designer with no evidence access.
- **Warrant** binds one handoff at an exact version. A principle citing two handoffs is doing two jobs.
- **Rail** carries the handoff's forbidden clause forward verbatim. The rail is not the designer's caution, it is the evidence's limit.
- **Scope** may be `all arcs` or a named list. A principle scoped to one audience says so, so the others can decline it visibly.
- **Declined Alternatives** records the tempting move this warrant does not support, which is where most overreach would otherwise enter.

## Closing rule

A principle page closes when its rule names one warrant at a pinned version, its rail repeats that warrant's forbidden clause, and a designer can apply it without opening the InsightBoard.

## Staleness

A changed `W` handoff clears this page's `state:` and every design division that cited this principle. The propagation is one hop down, never a search: the Design Roster in `BR00-brief` lists which designs cite which principles.

## Closing checks

- The rule is one because/do/within sentence with no conjoined second move.
- Exactly one handoff is bound, at a pinned version.
- The rail repeats the handoff's forbidden clause rather than paraphrasing it.
- Scope names the arcs it applies to.
- No message copy appears: a principle says what to do, never what to say.
- A designer with no InsightBoard access can act on it.

This variant owns no scripts.
