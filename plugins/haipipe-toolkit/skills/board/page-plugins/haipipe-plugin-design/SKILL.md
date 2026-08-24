---
name: haipipe-plugin-design
description: >-
  The design/ plugin of a Design page: one artifact UNIT per folder, display-shaped — README.md whose kind: routes to a venue pack the way a display unit's kind: routes to a renderer, spec.md compiled from the Brief and the venue rails, evidence.md binding only what the owning direction card granted, and content/ holding the artifact itself (copy.txt, email.html, card.pen, whatever the kind needs). One released card begets one unit through one arm-agent; units are folder-isolated so agents cannot collide. Trigger: design unit, artifact unit, DU folder, unit spec, message artifact, design plugin, /haipipe-plugin-design.
metadata:
  version: "0.1.0"
  last_updated: "2026-08-24"
  summary: "New 260824 (JL): the design family's artifact plugin, display-shaped plus a spec. A unit proves nothing and bets everything; its wager terms live on its direction card, never duplicated here."
---

# /haipipe-plugin-design · one bet, realized as one folder

**LOAD `haipipe-plugin` FIRST.** It owns what any plugin is: storage, surface, writer, boundary.
This file owns only design's delta: the unit anatomy, the spec as compiled config, and the kind routing.

## 🎯 Why this exists

A display unit shows something already known; a design unit realizes a bet not yet judged by the world. Both need a folder, because an artifact is never one file for long: an SMS grows an email twin, an HTML preview, a .pen card, three variants. The folder is also the arm-agent's write boundary, which is what makes fan-out safe: one released card, one agent, one folder, no collisions — the display family proved this shape.

## 🗂 Storage · one unit, one folder

```text
<page>/design/
└── DU<NN>-<slug>/
    ├── README.md        identity · kind: routes to a venue pack · direction: cites the card back
    ├── spec.md          the COMPILED config the agent obeys and the judge checks against
    ├── evidence.md      the granted evidence rows, bound by path (pagex mechanics)
    └── content/         the artifact itself · format follows kind
```

README fields: `unit:` id, `kind:` (sms | email | push | reminder | ui-card | dashboard | checklist | report — the venue packs ARE the route table; a new object is a new pack, this plugin does not change), `serves:` the owning division, `direction:` the card id, `depth:` copied from the card, `state: draft | judged | accepted@v<N>`.

## 📋 spec.md · compiled, never invented

Three blocks, each naming its source, because a spec value with no source is a new requirement nobody approved:

```text
requirements   ← the Brief (outcome, guardrail, kill, promise)
rails          ← the venue pack (length caps, forbidden moves, tone, timing)
acceptance     ← the judge's list: rails pass · stance fidelity (the content visibly
                 does what the card's thesis says) · files complete
```

## ⚖️ Three laws

1. **The wager lives on the card.** Expected effect and falsification line are the direction card's fields; this folder cites the card and never restates them, so the bet's terms cannot drift in two places.
2. **Evidence within grant.** `evidence.md` binds only rows inside the owning card's `grant`, which sits inside the board's `reads:`. The chain narrows at every step and the judge checks the set-difference.
3. **A unit without a passing spec cannot be accepted.** `state:` moves draft → judged (the acceptance list passed) → accepted@v<N> (a person's row on the owning division names this unit and a render version). No person, no accepted.

## ⚙️ Writer

One arm-agent per released card writes the whole folder and may touch nothing outside it: not the page prose, not a sibling unit, not the card beyond its `landed:` pointer. A person writes only the division's `accepted:` row. Re-opening a landed unit (venue change, evidence moved) clears the owning division's `accepted:` row and only that row.

## 📡 Surface

The owning division cites the unit by id and carries its stance and acceptance; `render/` projects `content/` into what the recipient sees, stamped with design, warrant and render versions as `haipipe-plugin-render` already rules.
