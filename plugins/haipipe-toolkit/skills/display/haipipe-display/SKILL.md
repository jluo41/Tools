---
name: haipipe-display
description: "THE one door for display work: say what you want shown and this routes it to the right renderer by KIND, then the renderer writes a display unit per ref/display-unit-output-contract.md. Four renderers: 📊 haipipe-display-table · 📈 haipipe-display-figure · 📐 haipipe-display-diagram · 🎨 haipipe-display-illustration; the ✒️ TeX-native tikz method is authored by hand into the unit's recipe/. Use when user says 做表, 生成表格, regression table, 画图, 作图, generate figures, paper plots, 架构图, concept figure, make a display, render a unit, display unit, which renderer, /haipipe-display."
argument-hint: "[what to display, or a unit/intake path]"
metadata:
  version: "0.2.0"
  last_updated: "2026-08-16"
  summary: "Pure router (JL 260816): table and figure stay full skills; poster and slides retired; the door only decides which renderer draws."
---

# /haipipe-display · one door, four renderers, one unit contract

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
a concept in the paper's own TeX ✒️ tikz          no skill: author
                                                  recipe/<name>.tikz.tex by hand,
                                                  float.tex \inputs it
```

Data kinds (📊 📈) read ONLY the approved extract in the unit's `intake/`, never the raw data; what a caller owes that folder is `../ref/display-intake-contract.md`.
Concept kinds (📐 ✒️ 🎨) carry no numbers at all; their input is the spec or prompt they draw.
Pick ✒️ tikz when the figure should share the paper's own fonts and math; pick 📐 diagram when it should stay editable as SVG.

## 🚪 Where the unit lands

A PAPER's unit lands at `displays/displayNN-<slug>/` under the paper root.
A BOARD PAGE's unit lands at `<page>/display/<stem>-DisplayN-<slug>/`, and the page-side rules (address, citation chips, the human `accepted:` tick) belong to `haipipe-plugin-display`, not to this door.

## 📂 Files

- `../ref/display-unit-output-contract.md`
  The unit contract every renderer writes into; if this door and it disagree, it wins.
- `../ref/display-intake-contract.md`
  What a caller owes `intake/` before any data kind draws.
- `../README.md`
  The family map: renderers, the constitution, and the tooling beside them.
