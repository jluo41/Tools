---
name: haipipe-plugin-direction
description: >-
  The direction/ plugin of a Design page: one strategy CARD per file, each declaring a bet BEFORE any artifact exists — stance toward named evidence, thesis (the design move), and expected effect with its falsification line. Cards are probe-shaped: proposed by the machine, RELEASED only by a person, then realized as one design/ unit by one arm-agent, or killed and kept as a tombstone. A card without an expected effect may not be released, which is the executable form of "never design for design's sake". Trigger: direction card, strategy card, design direction, stance, release a card, kill a direction, treatment candidate, /haipipe-plugin-direction.
metadata:
  version: "0.2.0"
  last_updated: "2026-08-24"
  summary: "0.2.0 (JL 260824): the three laws gained teeth — nine checker rules over direction/, each proven to fail on a one-way-broken board first, plus `mode: record` for pre-contract slates. 0.1.0: the strategy-card plugin, probe-shaped, with two lives."
---

# /haipipe-plugin-direction · declare the bet before the artifact

**LOAD `haipipe-plugin` FIRST.** It owns what any plugin is: storage, surface, writer, boundary.
This file owns only direction's delta: the card grammar, the release gate, and the grant chain.

## 🎯 Why this exists

A designed message is a bet, and a bet placed after seeing the outcome is not a bet. The card exists so the stance, the move and the wager are written down and RELEASED by a person before any copy exists. Its two precedents are both in the family: probe cards (proposed, human-released, dispatched) give it its lifecycle; the retired stage ladder's failure (arms invented ad hoc, nobody could later say why 13) gives it its reason.

A direction has two lives. The PROPOSAL lives here, because the artifact folder does not exist yet, a killed card needs a tombstone, and the release gate must be visible on disk. The REALIZATION lives in the `design/` unit that cites the card back; after landing, the card keeps only its terms and a pointer, and changing the terms means returning HERE for re-release, never editing them inside the unit.

## 🗂 Storage · one card, one file

```text
<page>/direction/
└── DR<NN>-<slug>.md      one strategy card
```

Card grammar, every field required unless marked:

```text
# DR<NN> · <name>
state: proposed | released | landed | killed
stance: follow <board·page id> | follow-all | ignore | bet-against <board·page id>
depth: copy | copy+why | copy+why+expectation
thesis: <the design move, one or two sentences>
expected effect: <what it should achieve AND the falsification line>   (ignore cards: baseline, calibrates)
grant: <the exact evidence this card may hand its unit>                (ignore cards: none)
released: ⬜ | <person> <YYMMDD>
landed: — | <DU id>                                                    (killed cards: the reason, kept forever)
```

## ⚖️ Three laws

1. **Release is a person's act.** The machine proposes; only a person flips `released:`. A card at `proposed` blocks its own fan-out and nothing else, so proposing is always safe. This is the standing stop-after-draft ruling wearing its design clothes.
2. **No expected effect, no release.** A card that cannot say what it is for and what would falsify it is not a bet; `ignore` cards state `baseline, calibrates` explicitly rather than leaving the field empty.
3. **The grant narrows, never widens.** `grant` must sit inside the owning board's `reads:`; the unit's `evidence.md` must sit inside the grant. A `bet-against` card's grant includes the claim it bets against, because refuting something you may not read is not a bet either.

## 🔎 What the checker enforces (260824)

The three laws above stopped being prose on 260824. `check.py · check_design_family` reads every `direction/DR*.md` and reports:

```text
card-field-missing / -empty   any of the eight fields absent or blank
card-state-word               a `state:` off the four-word ladder
card-released-no-wager        released or landed with no expected effect   ← law 2
card-released-unsigned        `state: released` with `released: ⬜`        ← law 1
card-proposed-signed          a signature on a card still `proposed`
card-grant-path               a grant entry resolving to nothing
card-grant-outside-reads      a grant reaching outside the board's `reads:` ← law 3
card-landed-ghost / -empty    `landed:` naming no unit, or missing on a landed card
```

Each was proven to FAIL on a board broken exactly that one way before it was trusted; the proofs are `tests/test_design_family.py`. A board may declare `mode: record` on board.md when it holds a PRE-CONTRACT artifact, which relaxes the vocabulary rules (a historical `released:`, no stance, no grant) and nothing structural.

## ⚙️ Writer

The page's producer (or the design door's `direction` verb) writes cards at `proposed`. A person edits `released:` and `state:`. The arm-agent that realizes a card writes ONLY the `landed:` pointer, nothing else on the card.

## 📡 Surface

The owning page's division table cites cards by id, and the page's state line counts them (`three cards proposed · none released`). A killed card stays in the folder as its own tombstone; deleting one deletes the record that the bet was considered.
