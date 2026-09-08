---
name: haipipe-display
description: "THE one door for display work: say what you want shown and this routes it to the right renderer by KIND, then the renderer writes a display unit per ref/display-unit-output-contract.md. Five renderers: 📊 haipipe-display-table · 📈 haipipe-display-figure · 📐 haipipe-display-diagram · 🎨 haipipe-display-illustration · ✒️ haipipe-display-tex (hand-authored TikZ, algorithm blocks, display equations). Use when user says 做表, 生成表格, regression table, 画图, 作图, generate figures, paper plots, 架构图, concept figure, make a display, render a unit, display unit, which renderer, /haipipe-display."
metadata:
  version: "0.3.5"
  last_updated: "2026-09-08"
---

# /haipipe-display · one door, five renderers, one unit contract

Every display is one UNIT: a folder holding the approved inputs, the recipe that draws, and the winning render, per `../ref/display-unit-output-contract.md`.
This door decides only WHICH renderer draws it.
The unit contract decides what the folder looks like, and it wins any disagreement with this file.

## 🧭 Route by kind

```
the ask                          kind             renderer
──────────────────────────────────────────────────────────────────────────
numbers as a typeset table       📊 table         haipipe-display-table
numbers as a plot                📈 figure        haipipe-display-figure
a concept as an editable SVG     📐 diagram       haipipe-display-diagram
a concept as an AI illustration  🎨 illustration  haipipe-display-illustration
a figure in the document's TeX   ✒️ tex           haipipe-display-tex
  (or an algorithm block,                           hand-authored: the writer
   or a display equation)                           is a person, not a script
```

Data kinds (📊 📈) read ONLY the approved extract in the unit's `intake/`, never the raw data; what a caller owes that folder is `../ref/display-intake-contract.md`.
Concept kinds (📐 ✒️ 🎨) carry no numbers at all; their input is the spec or prompt they draw.
Pick ✒️ tex when the figure should share the document's own fonts and math, or when it IS math; pick 📐 diagram when it should stay editable as SVG.

## 🧭 Concept-first gate for visual displays

For a diagram, illustration, or PowerPoint-native figure whose composition or
icon language is not already frozen, choose the visual direction before doing
the editable reconstruction. Use this order:

```text
inspect current/previous visual
  → concept image or sketch
  → composition freeze
  → editable SVG/PPT reconstruction
  → exported candidate Result
  → caller promotion
```

- Inspect the current render and identify the invariants: must-keep icons,
  bottles, labels, arrows, panel count, relationships, and palette.
- Make a low-cost, human-visible composition reference first. It may be a
  user-supplied image, an existing candidate, an Image Gen concept, or a
  sketch. The reference answers layout and visual-language questions; it is
  not automatically the final asset.
- Record the approved composition in `recipe/` (for example
  `concept-reference.md` or the renderer's `prompt.md`) before native
  authoring. Include what must remain, what may be shortened, and what must
  not be introduced.
- Rebuild the approved composition as editable native objects or SVG and
  re-typeset every label. A generated bitmap may guide the reconstruction but
  must not replace an editable diagram or PowerPoint source.
- If the user asks to discuss the visual direction first, stop after the
  concept reference. Do not mutate `assets/`, `float.tex`, or the Board until
  the composition ruling is clear. Candidate promotion remains the caller's
  decision.

Text reduction is an information-density edit, not permission to remove the
existing visual encoding: preserve iconography, object semantics, and grouping
unless the user explicitly asks to delete or replace them. This gate does not
apply to ordinary data tables or plots, which follow the approved-intake and
FigureSpec routes.

## 🚪 Where the unit lands

A PAPER's unit lands at `displays/displayNN-<slug>/` under the paper root.
A BOARD PAGE's unit lands at
`<page>/outline/evidence/display/<stem>-DisplayN-<slug>/` (a PAPER Section page names
the unit `Display<n>-<slug>`, its own id `S-<desk>-Main-<N>-<Title>` carrying the index,
JL 260908; `S-Display-*` and `Sec<N>-Display<n>-*` are retired), and the page-side rules
(address, citation chips, the human `accepted:` tick) belong to
`board/page-plugins/haipipe-plugin-outline/ref/evidence/displays.md`, not to this door.

## 📂 Files

- `../ref/display-unit-output-contract.md`
  The unit contract every renderer writes into; if this door and it disagree, it wins.
- `../ref/display-intake-contract.md`
  What a caller owes `intake/` before any data kind draws.
- `../README.md`
  The family map: renderers, the constitution, and the tooling beside them.
