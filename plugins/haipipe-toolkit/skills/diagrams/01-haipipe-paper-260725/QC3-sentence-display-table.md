# A sentence with a Display · table
state: ✅ SETTLED
owner: JL
method: the sentence points at a stable display id; the numbers stay in the task layer that computed them

## Question
When a sentence sends the reader to a table, what does it point at, and what has to be true for that pointer to hold? A table is two things with two owners: the task layer computes the numbers, the paper frames them, and the sentence points at neither half directly.

A table is two things with two owners. The numbers are computed by the task layer and land as `source_data.csv` with provenance. The framing, which rows and columns the argument needs, the venue formatting, and the caption, belongs to the paper. A sentence points at the unit, not at either half, which is what lets the numbers be re-run without touching a word of prose.


The approach is to point at a stable display id and keep the two halves with their owners: the task layer computes the numbers, the paper frames them. What we want is to be able to re-run the analysis and rebuild the table without touching a word of prose, and to have any hand-typed number stand out as the defect it is.
## Boundary
- ✅ Covered here
  The table reference in prose, the `> Display:` lane for a table, chip states, and what the panel shows.
- ↪ Covered elsewhere
  The sentence itself is `QC0`; the rendering mechanism is `QA9` on the boardform board; a figure is `QC4` and differs more than it looks; who owns rendering is `QD1`; the render contract is `QD2`; hand-typing numbers into a `.tex` is a defect ruled at the display stage.

## Diagram
```
 A TABLE IS TWO THINGS WITH TWO OWNERS, AND THE SENTENCE
 POINTS AT NEITHER HALF

   the sentence           …the effect concentrates in low-back pain
                          (Table~\ref{display08})
                                   │  a STABLE ID, never a filename
                                   ▼
   ┌ display08 ─ the UNIT ─────────────────────────────────────┐
   │                                                           │
   │  TASK layer owns          PAPER owns                      │
   │  source_data.csv          which rows and columns the      │
   │  + provenance             argument needs                  │
   │  the numbers              venue formatting                │
   │                           the caption                     │
   │                           \label / \ref wiring            │
   └───────────────────────────────────────────────────────────┘
   under the sentence
     > Display: display08 · target=S-Display-8 · kind=table
              · state=rendered

 WHY THE ID AND NOT THE FILE
   the id survives a re-render, a candidate promotion, a citation
   style and an output format. So the numbers can be RE-RUN without
   touching a word of prose. A Section never names
   table3-main-results.tex.

 CHIP STATES
   ✅ rendered    the unit exists and its source data is current
   ⏳ requested   a row exists for it; nothing built
   ⚠️ stale       built, but the source data has been RE-RUN since
   ⚠️ orphan      the sentence names an id no unit owns

 THE DEFECT THIS EXISTS TO PREVENT
   hand-typing a number into the unit's .tex.  It looks identical
   and it has cut the link back to the run that produced it.

 WHY A TABLE IS NOT A FIGURE (and QC4 is a separate face)
   the panel shows the ROWS, not a thumbnail of them: a table's evidence
   IS its numbers, so the reader can check the claim on sight.

 WHERE THIS PAGE'S EVIDENCE LIVES IN THE BOARD FOLDER
   the prose      QC3-sentence-display-table.md  ## Content   (S5)
   the unit       _fixture/displays/display05-descriptives/
     float.tex              \label{tab:descriptives}   ← what \ref{} greps
     assets/table-body.tex  the ROWS the panel prints
     source/REBUILD.md      no source_data.csv here, so no staleness to show
```

## Content
### What sits where
```
 in the sentence   a stable display id, projected as \ref{} in LaTeX
 under it          > Display: display08 · target=S-Display-8 · kind=table
                            · state=rendered
```
The id survives a new rendering, a candidate promotion, a citation style, and an output format. A Section refers to `display08`, never to `table3-main-results.tex` or a candidate filename.

### S5 of the paragraph on `QC0`
`QC0` carries one paragraph with all four attachment types. This is its fifth sentence, the one that sends the reader to a table, written here and resolved against `_fixture/displays/display05-descriptives/`:

Operationalization details and descriptive statistics for all variables are presented in \ref{tab:descriptives}.
> Display: display05 · target=S-Display-5 · kind=table · state=rendered

Two chips, one unit. The sentence writes `\ref{tab:descriptives}`; the lane writes `display05`. Both resolve to `display05-descriptives`, as would its folder name: three ways to name one unit, one resolver. Click either and the panel shows the table's ROWS, so a number in a sentence can be checked against the row it came from without leaving the page.

The paragraph's other sentences are the sibling pages': S1 to S3 the citations are `QC1`, S4 the numbers is `QC2`, S6 the figure is `QC4`.

### A reference that resolves to nothing, and reads the same
`\ref{tab:cohort-descriptives}` is cited in `0-sections/05_data_variables.tex:112` on this paper and matches no `\label` anywhere, so it compiles to `??`:

Cohort composition is reported in \ref{tab:cohort-descriptives}.

One hyphenated word longer than the one that works, and nothing in the prose says so.

### The two halves and their owners
```
 bank deliverable    source_data.csv + provenance     the TASK layer computes it
 consumer deliverable which rows and columns the       the PAPER frames it,
                     argument needs, venue format,     and owns the caption
                     \label / \ref wiring
```
A reference naming only one half is incomplete. Hand-typing a number into the unit's `.tex` is a defect, because it breaks the link back to the run.

### Chip states as built
```
 ✅ ok         the unit is built and its source data is not newer than it
 ✦ ready      a candidate is waiting while assets/ still holds the old one
 ⏳ owed       the unit folder exists and assets/ is EMPTY
 ⚠️ broken     STALE: source_data.csv is NEWER than the built asset, so the
               manuscript is showing numbers the data no longer says
 ❓ unowned    the id, or the \ref{} label, resolves to nothing
```
Staleness is computed rather than declared: the mtime of `source/source_data.*` against the newest file in `assets/`. Nobody has to remember to mark it, which is the only way a stale state ever gets reported.

### Three ways a face names a display, and all three resolve
```
 display04                  the SHORT id. What the S-Display faces actually
                            write: "kind: table · registry id display04"
 display04-main-regression  the LONG id, folder-shaped. What a Section writes.
 \ref{tab:results}          the LaTeX form, resolved through the unit's own
 `tab:results`              float.tex \label{}. Backticked or bare.
```
The kind comes from `\begin{table}` in that same `float.tex`, which is why the chip can put a table icon on one and a figure icon on the other without being told.

### The panel as built
Click a display chip and the panel gives the unit id, its kind, its `\label`, the state sentence, the README's Reader Takeaway, and a link row: `float.tex`, `README`, `source_data.csv`, every asset, and every waiting candidate, plus the Placement line.

The table body IS shown, not linked (JL 260726): `assets/table-body.tex` renders in the panel, first 40 lines with a count of what was cut. That is what this page meant by "a preview of the table itself, not a thumbnail of one": a reader checking whether a sentence's claim matches the rows can do it without leaving the page.

It shows the LaTeX source rather than typeset rows. For a `booktabs` body that is readable enough to check a coefficient against a sentence, which is the job; typesetting it in the browser would mean the board rendering LaTeX, and that is a different project.

## Items to Finish
- [x] 🆔 Point at a stable display id
      Not a filename, not a candidate, not a float number.
- [x] 🎨 Build the table chip
      Shipped 260726. Three reference forms resolve to one unit: `display04`, `display04-main-regression`, and `\ref{tab:results}` via the unit's own `float.tex`.
- [x] 🔭 Audit the .tex the board does not render
      `build.py` prints dead `\ref{}` and uncited units, the same way it prints broken citation keys.
- [x] 📐 Define what the card shows
      The table body, first 40 lines, with the remainder counted. Ruled by building it: "the rows this sentence cites" needs the sentence to declare which rows, and no sentence does.
- [ ] 🎨 Typeset the rows rather than showing the source
      The panel shows `table-body.tex` as LaTeX. Readable for checking a number; not what a reader of the paper sees.
- [x] 🔍 Detect orphan and stale
      Orphan is an id or label resolving to nothing. Stale is COMPUTED from mtimes, `source/source_data.*` against the newest file in `assets/`, so nobody has to remember to mark it.
- [ ] 🧪 One live example on the MISQ paper
      `S-Display-8` is venue-mandatory and already rendered, so it is the cheapest real test.

## Where we are
Built and live on the MISQ board 260726. Seven table chips, all `ok`, all resolving to a real unit with a real `float.tex`. The figure side is where the trouble is: `QC4` counts 4 `ok`, 2 `ready` and 3 `broken` on the same board, from the same resolver.

The finding is not on the board, it is in the audit, and it is the same shape as `QC1`'s:

```
 4 dead \ref{}    cited in a section, resolving to NO \label anywhere,
                  so they compile to ??
                  tab:cohort-descriptives   05_data_variables.tex:112
                  tab:variables             05_data_variables.tex:130
                  tab:gradient_results      06_empirical_analysis.tex:53
                  fig:agreeableness_dist    05-2_data_construction.tex:152
 9 of 10 units    their \label is referenced by NO section
                  only display05's tab:descriptives is actually cited
```

That second row is `QD6`'s sixth-link diagnostic firing at scale: nine displays exist, are built, and nothing in the manuscript points at them. Whether the sections are behind or the displays are speculative is a judgment; the board's job was only to make it visible.

The table preview shipped 260726: seven panels render their `table-body.tex` inline, so a number in a sentence can be checked against the row it came from without leaving the page. What it shows is LaTeX source, not typeset rows, which is the remaining item.

- 260726 CC · 🔗 Closing this unblocks `QA9`'s chip renderer
  `QA9` on the boardform board owns the MECHANISM: the fold, the badge, the drawer, the tint, the click-to-add.
  Its one unbuilt item, inline-marker chips, is blocked on four rulings, and this face is the table one: what the chip means, what states it has, and what resolves it, which here is a display id whose table is checkable on sight.
  The mechanism cannot be built against a guess, so that item stays open until all four of `QC1` to `QC4` say what to render.

## Law
- A sentence points at the display UNIT, never at a file, a candidate, or a float number. The id survives a re-render, a promotion, a citation style and an output format.
- Staleness is COMPUTED, never declared. A state a human has to remember to set is a state that will be wrong.
- A display's KIND comes from its own `float.tex`. The board does not guess table from figure, and the chip says which before it says anything else.

## Log
- 260726 · JL: "add the google scholar search link"; and "for the values, displays, figures, I cannot click them". Two changes. The citation panel's link row gained a `🔎 Scholar` search, last and with its own glyph because everything above it is an identifier and a query is not; on this paper 195 of 216 entries had no clickable pointer before it. And the chips inside a sentence drawer were dead: `<summary>` consumes the click before the nested button's default action runs, which is why citations opened and values, tables and figures did not. The panel is now asserted explicitly one frame later; `preventDefault` stays out of `board.js`.
- 260726 · JL: "read QA6 ⑦ The paper folder, we have done many changes here, right?" Correct, and the board was teaching the superseded layout. QA6 ruled 260726 that the deliverable is UNNUMBERED (`displays/`, `sections/`) and the resolver still had `0-displays` hardcoded in six places. Proved it by renaming the fixture and rebuilding: four id chips went `unowned` and both `\ref{}` chips went GREEN through the "a \label that is not a display unit" branch, which is the silent false-green `QC3` and `QC4` exist to prevent. `Paper` now resolves `displays/` first and falls back to `0-displays/`; the fixture moved to the ruled name. Still open on QA6's side: `.board-refs.bbl` is machinery sitting in the unnumbered half.
- 260726 · JL, on the embed: "I don't want you to refer something, please just make it real in the content, not refer a markdown". Reverted. The example prose is written directly in each page's `## Content`: `QC0` carries the whole paragraph, `QC1`-`QC4` carry only their own sentences from it, labelled by position. The rule that came out of it is the one on `QC0`: PROSE lives on the page, EVIDENCE lives in `_fixture/` (`.bib`, `.bst`, `0-displays/`, `1-probes/`), and `_fixture/` never holds a paragraph. Same visit fixed the panel: without `position-area` support the base `.chipcard` had no `max-height`, so a two-image figure panel grew past the viewport and spilled over the page.
- 260726 · Built. Three reference forms turned out to be in live use for one unit (`display04`, `display04-main-regression`, `\ref{tab:results}`), so all three resolve rather than one being declared canonical. The audit found 4 dead `\ref{}` compiling to `??` and 9 of 10 units cited by nothing, neither of which any chip could show, because the board renders faces and the manuscript lives in `0-sections/`.

## Files
- `0-lifecycle/4-display/S-Display-8-variable-operationalization.md`
  A rendered, venue-mandatory table unit.
- `0-displays/`
  Where the units and their source data live.
