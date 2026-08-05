---
name: haipipe-board-page-for-display
description: >-
  The VARIANT contract for a DISPLAY unit Page: one page per display unit a paper or application ships, such as a figure, table, or diagram, mirroring the unit's folder (float, assets, caption, provenance) and carrying the human acceptance that no file in that folder can hold. It loads haipipe-board-page for the base frame and adds only what a display page needs: Content that mirrors the unit rather than arguing a question, the acceptance ladder from requested through rendered to accepted-into-prose, the rule that every shown number carries provenance from a Value binding or a named run, and the placement record binding the unit to the sentence that cites it. Use when writing or fixing a display page, when a rendered unit was never accepted by a person, when a figure shows a number nothing traces, or when a unit ships but no sentence points at it. Trigger: display page, display unit, S-Display, figure page, table page, float, preview, caption, acceptance, placement, /haipipe-board-page-for-display.
metadata:
  version: "0.1.0"
  last_updated: "2026-08-05"
  summary: "First cut, on JL's ruling that display stands alone: mirror-shaped like a Skill page, but its unit is produced BY this project and closes on human acceptance, not on shipping."
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

# /haipipe-board-page-for-display · a unit you can look at, and the acceptance it waits for

**LOAD `haipipe-board-page` FIRST.** It owns the base frame. This file adds only what a display page needs and no other kind does.

**The kind this variant covers**: one page per display UNIT.

```
kind      subject                              closes when
──────────────────────────────────────────────────────────────────────
Display   ONE unit's folder: float · assets ·  a person ACCEPTS the rendered
unit      caption · source recipe               unit into the work
```

**Where it stands beside the mirror type**: a Skill page and a display page are both mirror-shaped, and they differ in the two facts that matter. A Skill page mirrors a unit maintained ELSEWHERE and closes when that unit ships; a display page mirrors a unit THIS project produces and closes only when a person accepts it. Shipping is an event; acceptance is a judgment. That difference is why display stands alone rather than riding `-for-skill` (JL 260805), and why its `state:` line is a gate position no machine may flip.

## 🪜 The acceptance ladder

A display page's state answers one question: how far up this ladder is the unit?

```
① REQUESTED    the need exists · what the unit must show, and for which claim
② SOURCED      the producing run or recipe is named · nothing rendered yet
③ RENDERED     preview exists · a person can LOOK at it
④ ACCEPTED     a person said yes to THIS render · dated, on this page
⑤ PLACED       a sentence cites it · the placement record names the sentence
```

A unit may fall back down: a re-render after acceptance returns to ③, because acceptance was of a specific render, not of the unit's name. The page's Log carries each rung with its date.

## 🔢 Every shown number carries provenance

A display is where an untraceable number hides best, because a figure asserts without a sentence. The rule is the Value route's rule, applied at the unit:

```
each number the unit shows  →  a Value binding on a Value topic page, BY PATH,
                               or the producing run named on this page
🚫 a rendered number nothing traces is a defect of THIS page, even when
   the figure "looks right"
```

## 🔗 The placement record

A unit that renders beautifully and is cited by no sentence is unfinished work wearing finished clothes. The page carries one placement record per consumer: which section, which sentence, and whether the citation landed. An accepted-but-unplaced unit is a visible open row, never a silent success.

## 📂 Files

```
haipipe-board-page-for-display/
├── SKILL.md            this variant contract
└── CHANGELOG.md        version history
```

Owns no scripts. The base is `haipipe-board-page`; the number rule leans on `haipipe-board-page-for-value`; the paper family's display machinery (renderers, request rows, the displays/ folder shape) stays in the paper and display families, which this contract names but never contains.
