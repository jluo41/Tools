---
name: hai-display
description: "The one door for display work: routes by kind to its part (table, figure, diagram, illustration, slide, tex), then every display passes the blind-review revise loop. Use to make or revise a table or figure. Trigger: 画图, regression table, generate figures, figure to svg, /hai-display."
metadata:
  version: "0.8.0"
  last_updated: "2026-11-01"
allowed-tools: Bash(*), Read, Write, Edit, Grep, Glob, Agent, mcp__codex__codex, mcp__codex__codex-reply, WebSearch, mcp__codex-image2__generate, mcp__codex-image2__generate_start, mcp__codex-image2__generate_status
---

# /hai-display · one door, five renderers, one unit contract

Every display is one UNIT: a folder holding the approved inputs, the recipe that draws, and the winning render, per `../ref/display-unit-output-contract.md`.
This door decides only WHICH renderer draws it.
The unit contract decides what the folder looks like, and it wins any disagreement with this file.

## 🧭 Route by kind

```
the ask                          kind             renderer (read this part)
──────────────────────────────────────────────────────────────────────────
numbers as a typeset table       📊 table         _parts/table/PART.md
numbers as a plot                📈 figure        _parts/figure/PART.md
a concept as an editable SVG     📐 diagram       _parts/diagram/PART.md
a concept as an AI illustration  🎨 illustration  _parts/illustration/PART.md
slides as pictures, one style    🖼 slide         _parts/slide/PART.md
a figure in the document's TeX   ✒️ tex           _parts/tex/PART.md
how the study works (method)     🕒 method        ../hai-display-method/SKILL.md
an existing figure → editable SVG 🔁 convert      _parts/figure-to-svg/PART.md
one icon or logo → SVG           🔁 convert      _parts/icon-to-svg/PART.md
an HTML slide → SVG/PDF/PPTX     🔁 convert      _parts/html-to-svg/PART.md
  (or an algorithm block,                           hand-authored: the writer
   or a display equation)                           is a person, not a script
```

🔁 convert starts from a file that already exists (replicate it); 📐 diagram draws a new concept.

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
   a review packet holding only each unit's `preview.pdf` page 1 (the display and its caption) and
   `assets/figure.png` when the unit has one (a table has none); the method pages stay out, so the
   reviewer judges the display as a reader sees it. This is the one reviewer rule for every kind:
   a Codex reviewer (`mcp__codex__codex`) is only an optional second opinion when that tool is
   available; it never replaces the fresh agent, and its words never decide the pass.
3. **Record** its text verbatim as `<unit>/review/rNN.md` and set the README `review:` line.
4. **Revise** from the review, re-render, recompile `preview.pdf`, and go to step 2 with a new
   reviewer.
5. **Pass rule**: overall >= 8/10 and question, readability, honesty and journal-ready each
   >= 7/10, for every display. Stop after round 4 and hand the person what is still open.

The maker never scores its own displays, and a pass is not acceptance: it only lets the person
decide. A paper also reviews its whole set once, across Sections (hai-paper-evidence, which
`/hai-paper-display` opens).

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

## 📄 preview.pdf: the display, what it says, then how it was made

JL 261101: "I want to make the preview the first page to be the display and content, could you make the second page
and beyond to be things like the methods, to explain how this display is generated". Every unit's `preview.pdf` has:

```text
page 1      the display as a reader sees it: float.tex (the figure or table, its caption, its label)
page 2 on   "What this display says", from method.md's ## Message: what we want to say with this display,
            1 to 3 sentences, the finding the reader should leave with (JL 261103: "the first section should
            be: what we want to say with this display"); a method.md with no Message says so, so the gap shows
            then "How this display was made", from the rest of method.md:
            ## Data · ## Sample · ## Method · ## Outcomes · ## Made by (the Runs, by path) · ## Numbers
            (read from Result files, or screen readings still to return)
```

```bash
python <this skill>/scripts/build_preview.py <unit folder>     # writes preview.tex, compiles preview.pdf
python <this skill>/scripts/build_preview.py <unit> --method-from <source version>/result/preview.pdf
                                                   # a paper's framed unit (Figure 1): its own float, then the
                                                   # source version's method pages, written once with that version
python <this skill>/scripts/build_preview.py <unit> --look paper                # the paper's default page
python <this skill>/scripts/build_preview.py <unit> --preamble-from <delivery/<job>/latex/master.tex>
                                                   # page 1 exactly as that built paper prints it
python <this skill>/scripts/build_preview.py --help                             # every flag
```

This is the one preview recipe for every kind: a part never runs `pdflatex` on `preview.tex` by hand. The script
compiles inside the unit, so `float.tex` references its asset unit-relative (`\input{assets/table-body.tex}`,
`\includegraphics{assets/figure.pdf}`). Its plain head already loads booktabs, siunitx, threeparttable and graphicx; a
unit that needs more keeps them in its own `preview.tex` head, which the script keeps. A candidate preview runs the same
script on `candidates/<id>/`: a copy of `float.tex` with the candidate asset beside it, the active unit untouched.

**Who writes `float.tex`**: the renderer writes the file (the `table`/`figure` environment and the line that
`\input`s or `\includegraphics` its asset); the caller owns its words (caption, `\label`, placement) and the renderer
copies them in unchanged. With no caption given the renderer leaves `float.tex` pending and builds no preview.

**Page 1 looks like the paper's page** (JL 261101: "the full pdf preview, just like the one we will see in the paper
pdf"). `--preamble-from` takes a built paper's `master.tex` head (its class, fonts, caption style, `preamble.tex`,
header and page number) and drops only its title lines and `endfloat`, so the display stays on page 1. `--look paper`
is the paper's default head (12pt, letter, 1in, Times, 1.5 spacing, the page number below) for a paper not built yet.
A paper's display goes through hai-paper-evidence's `scripts/preview_display.py`, which picks the head for you.

Who writes what: the display's maker (the Run's own script, or the agent that draws it) writes `method.md` once per
version, beside that version's `float.tex`; its first `# title` line is a file title and does not print. The caption
that prints is `float.tex`'s; a caption on a Task face is a note for the list and must say the same.
The builder keeps the unit's own preamble (an existing `preview.tex`'s lines before `\begin{document}`), so it works
for every kind. A unit with no `method.md` gets a page 2 that says so: the gap shows. `preview.tex` is the builder's
output; never edit it by hand, write `method.md` or `float.tex` and rerun it. Each version of a display (each Run of
its Task) gets its own `preview.pdf`; the workbench's Evidence view shows the newest one, both pages.

## 🚪 Where the unit lands

**In a draft Task: `<task>/display/Display<n>-<slug>/`**, beside `draft/` and `evidence/` (JL 261016). A display is
built on evidence: its README names `built_on:` cards of `<task>/evidence/cards.yaml` (CITE 4, VALUE 1), and the numbers
it shows come from those cards' Runs, read with hai-evidence's `scripts/cards.py`, so a figure and the sentence
citing it cannot disagree.

**In a paper, the display's one home is its display Task** (JL 261113; the display Job moved onto the paper Board as
`j01_evidence_display` on 261031). The picture or table body is drawn by a Run of that Task (one Task per display,
each Run a version) into that Run's `result/`; the Task holds the question, caption, legend, number, size and
`review/rNN.md`, and a Section only cites it (an older Board: a Section-side `Display<n>-<slug>/` whose
`intake/manifest.yaml` points at the Run's `result/`, still read). A picture fix from the
revise loop goes to the display Task's Run script, as a new Run. The rules are hai-paper-evidence's rule 3.

For an older Page, the caller supplies the unit directory. For a Page DISPLAY Result, that is
`<page>/results/<re-run>/payload/<unit>/`; an older Board's Paper Section Page uses the same Page-owned Result
address. A View uses the View-owned path in the shared output contract. A non-Page Paper workflow
supplies its unit path through its Paper adapter. Renderers never choose a paper root or create a
second unit copy. Page citations and the human `accepted:` decision belong to
`1_base/draft/workbench-task-draft/ref/evidence/displays.md`.

**A bare input (a CSV or JSON, no Task, Page or paper): the unit lands next to it**, at
`<input folder>/display/Display<n>-<slug>/` (`n` the next free number, the slug what the display shows), the same
`display/Display<n>-<slug>/` shape a draft Task uses. Do not stop to ask for a unit path. The person who asked is the
caller: copy the file into `intake/inputs/`, seed `intake/manifest.yaml` from `../ref/intake-manifest.template.yaml`
(`origin.type: external`, `holder` the input folder, `artifact` and `provenance` the input file itself), write the
README `question:` from the ask, and write `float.tex` with a caption drafted from the ask by the caption rule, marked
in the README as `caption: drafted, for the person to approve`. Then make, preview and review as above.

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
