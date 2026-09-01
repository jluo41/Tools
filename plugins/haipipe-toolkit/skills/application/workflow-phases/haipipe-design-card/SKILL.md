---
name: haipipe-design-card
description: >-
  DesignBoard workflow phase D1 and Folder contract for a proposed design Card:
  stance, thesis, wager, grant, posture, expected effect, and the human
  release-or-kill decision before realization. Trigger: design card, design
  direction, wager, grant, D1, /haipipe-design-card.
metadata:
  version: "1.0.4"
  last_updated: "2026-08-31"
  workflow: haipipe-design-workflow
  phase: D1
  folder_kind: design-card
  primary_face: task
  page_ruling: domain-gate
---

# /haipipe-design-card · state the bet before making the artifact

Load `haipipe-folder`, `haipipe-design`, `haipipe-design-workflow`, and
`haipipe-plugin-design`.

## Position

D1 follows GD0 for each Design roster row. One card begins one design thread.
GD1 is the person's release/kill gate; proposed cards never fan out.

## Folder Kind

A Design Card is the smallest reviewable wager: `stance`, `thesis`, `grant`,
posture, its posture-specific success/failure test, and state. Ordinary bets
carry expected effect plus falsification. A brainstorm carries the sentinel
`expected effect: pool, predicts nothing`, `pool-target`, and the pool's six
completion checks; it never predicts an effect merely to satisfy a generic
field.

This is the first identity of one stable `design/DU<NN>-<slug>/` Folder. While
the card is proposed or awaiting GD1, that Folder's current identity is
`folder-kind: design-card`; later phases grow and reclassify it in place rather
than minting parallel Card, Unit, and Verdict directories.

## Input

The GD0-closed Brief, one audience/job/venue row, board `reads:`, signed Wisdom
handoffs or other allowed inspiration, venue rails, and prior terminal threads.

## Page Face

`card.md` must let a person answer what is being tried, for whom, under which
read grant, and what would make the posture fail. For a bet this is expected
effect plus falsification; for brainstorm it is the target, no-reuse rule,
provenance labels, distinctness, and venue rails. The grant is a path subset of
board `reads:`. Stance and grant are distinct.

## Task Face

Choose one posture (`vary`, `challenge`, `brainstorm`, or `propose`); write the
card without realizing the unit; check grant ⊆ reads; detect duplicate bets;
present named cards; then record only a person's `released` or `killed` act.

## Plugins

- `design` required; the thread starts at `design/DU<NN>-<slug>/card.md`;
- `pagex` is read through the parent Design Folder's grant;
- `render` and `code` forbidden before release.

## Gate and Closure

GD1 passes only when the card is the Folder's sole design material, carries its
posture-specific wager fields, grant resolves, and a person releases that
named card. Brainstorm must use `pool, predicts nothing`, never a forecast;
ordinary bets still require effect and falsification. `workflow/` control metadata is legal and is not realization.
`killed` is an equal-rank terminal. `proposed` is open and may carry forward.

## Handoff

Hand D2 exactly the released card, its grant, audience/job/venue, posture,
posture-specific obligations, and venue rails. On GD1 release, preserve
the Folder address, append `D1 → D2` to `workflow/phase.yaml`, and make
`folder-kind: design-unit` current before realization starts.

## Files

- Card: `<DesignFolder>/design/DU<NN>-<slug>/card.md`
- Phase identity/history: `<thread>/workflow/phase.yaml` (control metadata,
  never realization material)
- Receipt: `<DesignFolder>/outline/<DesignFolder-stem>-log.md`
