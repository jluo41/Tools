---
name: haipipe-display
description: "THE one door for display work: say what you want shown and this routes it to the right renderer by KIND, then the renderer writes a display unit per ref/display-unit-output-contract.md. Five renderers: 📊 haipipe-display-table · 📈 haipipe-display-figure · 📐 haipipe-display-diagram · 🎨 haipipe-display-illustration · ✒️ haipipe-display-tex (hand-authored TikZ, algorithm blocks, display equations). Every display a reader sees then MUST pass the revise loop (ref/display-revise-loop.md): one question per display, one colour scheme, a blind review by a fresh agent saved as review/rNN.md, revise, review again until overall >= 8/10 with no dimension under 7, at most 4 rounds. Use when user says 做表, 生成表格, regression table, 画图, 作图, generate figures, paper plots, 架构图, concept figure, make a display, render a unit, display unit, which renderer, display review, display loop, revise the figures, blind review of displays, journal-ready figures, /haipipe-display, /haipipe-paper-display."
metadata:
  version: "0.4.0"
  last_updated: "2026-10-22"
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
Concept kinds (📐 ✒️ 🎨) do not calculate values. They may show a count, percentage, or estimate
only when the caller declares a verified `role: values` source in `intake/manifest.yaml`.
Pick ✒️ tex when the figure should share the document's own fonts and math, or when it IS math; pick 📐 diagram when it should stay editable as SVG.

One renderer invocation that produces one bounded unit may be modeled as one Run in a parent
Workflow. Its numbered instructions, tool calls, compile, review, and retries are Steps inside that
Run. `origin.run` remains the upstream source-provenance field.

## 🔁 Revise loop (a must)

A rendered unit is not done. Every display a reader will see goes through the loop in
`../ref/display-revise-loop.md` before anyone may tick `accepted:` (JL 261022: "display should also
have a loop, like the draft is a loop").

```text
make ─▶ blind review r01 ─▶ pass? ─ yes ─▶ the person may tick accepted:
            ▲                 │ no (fewer than 4 rounds)
            └─ review rNN ◀── revise: the maker fixes and re-renders
after r04 with no pass ─▶ stop; hand the person the open problems
```

1. **Make** each unit with a README `question:` (the ONE question it answers), the one colour
   scheme of the paper or report, and a folder name that says what it is
   (`Display2-figure1-rq1-names-match-request`, never a method name). Keep the caption short:
   a 10-15 word title and a legend of at most 75 words that only defines what is drawn
   (symbols, bars, colours, scales, abbreviations); the finding goes in the text, not the caption.
2. **Blind review**: spawn a FRESH agent (Agent tool, a new general-purpose agent, never yourself,
   never the round before's reviewer) with the reviewer brief from the ref, pasted verbatim. Give it
   a review packet holding only each unit's `preview.pdf` and `assets/figure.png`.
3. **Record** its text verbatim as `<unit>/review/rNN.md` and set the README `review:` line.
4. **Revise** from the review, re-render, recompile `preview.pdf`, and go to step 2 with a new
   reviewer.
5. **Pass rule**: overall >= 8/10 and question, readability, honesty and journal-ready each
   >= 7/10, for every display. Stop after round 4 and hand the person what is still open.

The maker never scores its own displays, and a pass is not acceptance: it only lets the person
decide. A paper also reviews its whole set once, across Sections (haipipe-paper-evidence, which
`/haipipe-paper-display` opens).

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
- The caller owns the composition ruling. A specific user-directed layout is
  sufficient; if materially different compositions remain plausible, show the
  reference or candidates and wait for the caller to choose before rebuilding.
  Record the selected composition and its invariants in `recipe/`.
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

**In a draft Task: `<task>/display/Display<n>-<slug>/`**, beside `draft/` and `evidence/` (JL 261016). A display is
built on evidence: its README names `built_on:` cards of `<task>/evidence/cards.yaml` (CITE 4, VALUE 1), and the numbers
it shows come from those cards' Runs, read with haipipe-evidence's `scripts/cards.py`, so a figure and the sentence
citing it cannot disagree.

**In a paper, the unit frames a work Run's picture** (JL 261022). The picture or table body is drawn by a Run of
the paper's work Block (its `jNN_paper_displays` Job, one Task per display) into that Run's `result/`; the paper's
`Display<n>-<slug>/` names the question, caption, legend, number, size and `review/rNN.md`, its `intake/manifest.yaml`
points at the Run's `result/`, and its `recipe/` copies the picture in and draws nothing. A picture fix from the
revise loop goes to the work Run's script. The rules are haipipe-paper-evidence's rule 3.

For an older Page, the caller supplies the unit directory. For a Page DISPLAY Result, that is
`<page>/results/<re-run>/payload/<unit>/`; a Paper Section Page uses the same Page-owned Result
address. A View uses the View-owned path in the shared output contract. A non-Page Paper workflow
supplies its unit path through its Paper adapter. Renderers never choose a paper root or create a
second unit copy. Page citations and the human `accepted:` decision belong to
`1_base/workbench/workbench-task-draft/ref/evidence/displays.md`.

## 📂 Files

- `../ref/display-unit-output-contract.md`
  The unit contract every renderer writes into; if this door and it disagree, it wins.
- `../ref/display-intake-contract.md`
  What a caller owes `intake/` before any data kind draws.
- `../ref/display-revise-loop.md`
  The revise loop every shown display must pass: the reviewer brief, the record, the pass rule,
  the question, colour and naming rules.
- `../README.md`
  The family map: renderers, the constitution, and the tooling beside them.
