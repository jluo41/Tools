---
name: haipipe-display-tex
description: "Author a TeX-NATIVE display unit by hand: a TikZ figure, an algorithm2e block, or a display equation, written as one .tex in the unit's recipe/ and \\input by float.tex, so the display shares the document's own fonts, math, and macros. The writer is a PERSON, not a script. Use when user says tikz, TikZ 图, 用 LaTeX 画图, TeX-native figure, algorithm block, 算法框, display equation, 公式 float, a figure that must match the paper's fonts or carry real math. Not for data plots (haipipe-display-figure), editable SVG schematics (haipipe-display-diagram), or AI concept art (haipipe-display-illustration)."
argument-hint: "[what to draw, and the unit directory]"
metadata:
  version: "0.1.0"
  last_updated: "2026-08-16"
  summary: "The ✒️ tex kind gets its craft written down (JL 260816), from the two TikZ units QPf5 authored by hand: the two-compile law, the preamble declaration, and the sizing rule."
---

# /haipipe-display-tex · the display the document itself draws

The other renderers run a script and hand you a picture.
This kind has no script: a PERSON writes TeX, and the document's own engine draws it.
That is the whole reason to choose it, and the whole reason it needs rules.

Everything about the unit folder is `../ref/display-unit-output-contract.md`; this file owns only the TeX-native delta.

## ✒️ One kind, three shapes

```
shape                    float.tex wraps it as        typical packages
─────────────────────────────────────────────────────────────────────────
a TikZ figure            figure + \caption + \label   tikz + libraries
an algorithm block       algorithm + \caption         algorithm2e / algorithmic
a display equation       equation + \label, no caption amsmath
```

They are ONE kind because they share a writer (a person), a recipe (a hand-authored `.tex`), and a binding (`float.tex` `\input`s it).
Naming them separately would be three names for one mechanism (ruled JL 260816).

## 📐 The two compiles, and why both exist

This is the rule that makes a TeX-native unit usable by anyone but its author.

```
recipe/<name>.tex        the drawing · no \documentclass, no preamble
   │
   ├─ recipe/asset.tex ──▶ assets/figure.pdf     ⚙️ standalone class
   │     the FIGURE ALONE, cropped                  what CONSUMERS embed
   │
   └─ float.tex ─▶ preview.tex ─▶ preview.pdf    ⚙️ article class
         + caption + label                          what a PERSON accepts
```

`float.tex` `\input`s your recipe, so a document that includes it must carry your packages.
Most consumers cannot: the board's own LaTeX export builds a plain `\includegraphics` block, because its wrapper master knows nothing about tikz.
**So a TeX-native unit is not finished until `assets/figure.pdf` exists.**
The unit ships both: the native source for a document that shares your preamble, and a compiled PDF for every document that does not.

`recipe/asset.tex` is that second compile's wrapper, and it is part of the recipe, not an afterthought:

```latex
\documentclass[tikz,border=4mm]{standalone}
\usetikzlibrary{positioning, arrows.meta}
\begin{document}
\input{<name>.tex}
\end{document}
```

`preview.tex` is the first compile's wrapper, and its package list IS the unit's dependency declaration: a reader who wants to `\input` your `float.tex` copies those lines into their preamble.
Both compile from INSIDE the unit folder, so their `\input` paths stay relative and short:

```bash
cd <unit-dir> && pdflatex -interaction=nonstopmode preview.tex
cd <unit-dir>/recipe && pdflatex -interaction=nonstopmode asset.tex   # → assets/figure.pdf
```

## 📏 The rules, each earned on a real unit

- **A clipped preview is a FAILED build, not a cosmetic flaw.** `preview.tex`'s `geometry` must be wider than the drawing; QPf5's Display2 needed `paperwidth` 200 → 235mm, and until it did, the reader accepted a figure whose right-hand box was cut off. Always LOOK at the compiled PDF before calling ④ BUILD done.
- **Declare styles once, at the top of the recipe.** Named `\tikzset` styles (`box`, `flow`, `lbl`) keep a change to a look one edit instead of forty; hard-coded per-node options are how a figure stops being maintainable.
- **Move an arrow, not a box, when a label collides.** Small anchor offsets (`±5mm`) fix crowding without disturbing the layout a reader has already understood.
- **No title, no caption inside the drawing.** The caption lives in `float.tex`'s `\caption{}`, the same law the figure renderer keeps; a baked-in title prints twice in the document.
- **Grayscale first.** Encode the contrast with shape, weight, or position; color is a second channel, never the only one (a contract invariant).
- **A rebuild is deterministic.** Recompiling the same recipe gives the same PDF, so hand-editing an output is pointless by construction. Say that in the recipe's first comment line.
- **State no number you were not given.** A concept figure carries no data; a real count in a label comes from the unit's `intake/`, never from the author's memory.

## 🧭 When this kind, and when not

```
pick ✒️ tex          the figure needs the document's fonts, math, or macros;
                     or it IS math (an equation, an algorithm)
pick 📐 diagram      a boxes-and-arrows schematic that should stay EDITABLE
                     as SVG, generated deterministically from a JSON spec
pick 🎨 illustration a richer concept image than a vector spec can express
pick 📈 figure       any picture of DATA
```

The trade is honest: TeX-native buys typographic unity and the full TeX language, and costs you the script, the editability, and a preamble every consumer must either share or bypass through `assets/figure.pdf`.

## 📂 Files

- `../ref/display-unit-output-contract.md`
  The unit folder every kind writes into; it wins any disagreement with this file.
- `../haipipe-display/SKILL.md`
  The door that routes here.
- `../../diagrams/BoardSkillBoard-260722/QPf-page-folder/QPf5-display/display/`
  Two worked units, `Display1-pipeline-tikz` and `Display2-small-paper-tikz`: the specimens these rules came from.
