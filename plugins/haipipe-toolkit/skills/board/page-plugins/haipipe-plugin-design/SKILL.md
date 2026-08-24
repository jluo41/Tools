---
name: haipipe-plugin-design
description: >-
  The design/ plugin of a Design page: one artifact UNIT per folder, display-shaped — README.md whose kind: routes to a venue pack the way a display unit's kind: routes to a renderer, spec.md compiled from the Brief and the venue rails, evidence.md binding only what the owning direction card granted, and content/ holding the artifact itself (copy.txt, email.html, card.pen, whatever the kind needs). One released card begets one unit through one arm-agent; units are folder-isolated so agents cannot collide. Trigger: design unit, artifact unit, DU folder, unit spec, message artifact, design plugin, /haipipe-plugin-design.
metadata:
  version: "0.2.0"
  last_updated: "2026-08-24"
  summary: "0.2.0 (JL 260824): eight checker rules over design/, including unit-dead-reference, written after a unit cited its own card one level short and left the wager unreachable. 0.1.0: the artifact plugin, display-shaped plus a spec."
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

One further `state:` exists and only on a board that declares `mode: record` on board.md: `historical-record`, for a unit transcribed from an artifact made before this contract. Nothing judged it and no acceptance list existed to judge it against, so neither `judged` nor `accepted@v<N>` would be true. See `haipipe-plugin-direction` for the card side of record mode.

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

## 🔎 What the checker enforces (260824)

`check.py · check_design_family` reads every `design/DU*/` and reports:

```text
unit-no-readme · unit-file-missing · unit-no-content   the folder contract
unit-depth-word / -no-why / -extra-why                 depth matches the files present
unit-state-word                                        draft · judged · accepted@v<N>
unit-no-direction · unit-direction-ghost               the unit names a card that exists
unit-dead-reference                                    ANY relative reference that
                                                       resolves to nothing            ← law 1
unit-evidence-outside-grant                            evidence beyond the card's grant ← law 2
```

`unit-dead-reference` exists because of a real failure: on 260824 a unit cited its owning card one directory level short, which left the wager unreachable from the artifact and so broke law 1 while every self-check reported clean. Each rule was proven to fail on a one-way-broken board before being trusted; see `tests/test_design_family.py`.

## ⚙️ Writer

One arm-agent per released card writes the whole folder and may touch nothing outside it: not the page prose, not a sibling unit, not the card beyond its `landed:` pointer. A person writes only the division's `accepted:` row. Re-opening a landed unit (venue change, evidence moved) clears the owning division's `accepted:` row and only that row.

## 📡 Surface

The owning division cites the unit by id and carries its stance and acceptance; `render/` projects `content/` into what the recipient sees, stamped with design, warrant and render versions as `haipipe-plugin-render` already rules.
