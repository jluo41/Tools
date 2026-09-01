---
name: haipipe-design-unit
description: >-
  DesignBoard workflow phase D2 and Folder contract for realizing one released
  Card into a complete design Unit, including spec, evidence, content,
  ideation when required, and either a scorable prospect or pool provenance.
  Trigger: design unit,
  realize design, D2, /haipipe-design-unit.
metadata:
  version: "1.0.4"
  last_updated: "2026-09-01"
  workflow: haipipe-design-workflow
  phase: D2
  folder_kind: design-unit
  primary_face: task
  page_ruling: none
---

# /haipipe-design-unit · realize one released bet

Load `haipipe-folder`, the Design door/workflow, `haipipe-plugin-design`, and
the selected venue pack.

## Position

D2 begins only after GD1 and ends at the complete-unit assertion GD2. Released
cards may realize in parallel, one designer per thread.

## Folder Kind

A Design Unit is the complete realization beside one card. It is not yet a
verdict or accepted division. Its posture-required content, spec, evidence or
disclaimer, and forecast or pool provenance must be inspectable without
reconstructing the designer's chat.

D2 is the second current identity of the same stable DU Folder born in D1.
`folder-kind: design-unit` means realization is current; it does not move the
card or create a sibling Unit Folder.

## Input

The released card and grant; Brief roster row; venue pack; inherited rails;
allowed templates/fielded set; and the posture-specific obligations.

## Page Face

Every unit exposes `README`, `spec`, `evidence`, and `content/`. Ordinary and
generate bets expose `prospect.md`; generate also exposes `ideation.md`.
Brainstorm exposes `ideation.md` plus `inspiration.md` and expressly has no
`prospect.md`. A reader can see the exact artifact, its invariant/variable
split, evidence use or pool disclaimer, safety rails, and posture-owned outlook.

## Task Face

One designer realizes the card. Generate runs explicit diverge then converge;
brainstorm produces a genuinely new pool with no comparator or forecast;
other postures follow their card. Evidence stays within grant, every file is
complete, and the card state becomes `landed` only after materialization.

## Plugins

- `design` required and owns the thread files;
- `studio` optional as the human's authoring room;
- `runs` optional only for a declared Run/Result unit, never for
  arbitrary artifact generation; scripts remain optional;
- `render` is produced later for acceptance.

## Gate and Closure

GD2 passes when all posture-required files exist, evidence ⊆ grant, content is
complete, rails are explicit, and the card state is `landed`. A proposed card
with sibling files or a released card with a partial unit fails.

## Handoff

Hand D3 the immutable card/grant plus the complete landed unit. Do not hand the
designer's private reasoning as evidence. On GD2, append `D2 → D3` to
`workflow/phase.yaml` and make `folder-kind: design-verdict` current. A failed
verdict appends `D3 → D2` before re-realization; history is never rewritten.

## Files

- Unit: `<DesignFolder>/design/DU<NN>-<slug>/`
- Phase identity/history: `<unit>/workflow/phase.yaml`
- Required file grammar: `haipipe-plugin-design`
