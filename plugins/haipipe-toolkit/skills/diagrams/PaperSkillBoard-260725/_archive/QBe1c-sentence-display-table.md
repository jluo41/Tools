# A sentence with a Display · table
state: 🟡 PARTIAL
owner: JL
method: the sentence points at a stable display id; the numbers stay in the task layer that computed them

## Opening
When a sentence sends the reader to a table, what does it point at, and what has to be true for that pointer to hold?
A table is two things with two owners: the task layer computes the numbers, the paper frames them, and the sentence points at neither half directly.

A table is two things with two owners. The numbers are computed by the task layer and land as `source_data.csv` with provenance. The framing, which rows and columns the argument needs, the venue formatting, and the caption, belongs to the paper. A sentence points at the unit, not at either half, which is what lets the numbers be re-run without touching a word of prose.


The approach is to point at a stable display id and keep the two halves with their owners: the task layer computes the numbers, the paper frames them. What we want is to be able to re-run the analysis and rebuild the table without touching a word of prose, and to have any hand-typed number stand out as the defect it is.
Scope: This page covers The table reference in prose, the `> Display:` lane for a table, chip states, and what the panel shows. Neighbouring pages cover The sentence itself is `QC5`; the rendering mechanism is `QA9` on the boardform board; a figure is `QBe1d` and differs more than it looks; who owns rendering is `QBe2a`; the render contract is `QBe2b`; hand-typing numbers into a `.tex` is a defect ruled at the display stage.

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

 WHY A TABLE IS NOT A FIGURE (and QBe1d is a separate face)
   the panel shows the ROWS, not a thumbnail of them: a table's evidence
   IS its numbers, so the reader can check the claim on sight.

 WHERE THIS PAGE'S EVIDENCE LIVES IN THE BOARD FOLDER
   the prose      QBe1c-sentence-display-table.md  ## Content   (S5)
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

### S5 of the paragraph on `QC5`
`QC5` carries one paragraph with all four attachment types. This is its fifth sentence, the one that sends the reader to a table, written here and resolved against `_fixture/displays/display05-descriptives/`:

Operationalization details and descriptive statistics for all variables are presented in \ref{tab:descriptives}.
> Display: display05 · target=S-Display-5 · kind=table · state=rendered

Two chips, one unit. The sentence writes `\ref{tab:descriptives}`; the lane writes `display05`. Both resolve to `display05-descriptives`, as would its folder name: three ways to name one unit, one resolver. Click either and the panel shows the table's ROWS, so a number in a sentence can be checked against the row it came from without leaving the page.

The paragraph's other sentences are the sibling pages': S1 to S3 the citations are `QBe1a`, S4 the numbers is `QBe1b`, S6 the figure is `QBe1d`.

### A reference that resolves to nothing, and reads the same
`\ref{tab:cohort-descriptives}` is cited in `sections/05_data_variables.tex:112` on this paper and matches no `\label` anywhere, so it compiles to `??`:

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

## Aims
- [ ] 🪞 The panel reads README.md, and the S-Display page is the one that is true
      HALF-CLOSED 260727 on JL's ask ("I want it can be clicked to the URL to the Stage-Display accordingly"). A display panel now carries a one-click anchor to the S-Display face that owns the unit, AND quotes that page's own `state:` line beside it. So the README's takeaway is still shown, but it can no longer be the only thing a reader has: the authority is one click away and its state is on the chip's own panel. Measured on the MISQ board: 69 links across 10 units, every one resolving to a real face.
      What that surfaced immediately is the thing the READMEs were hiding. Not one of the ten units is settled: `S-Display-1A` REVISE-blocked, `S-Display-3` FOLDED, `S-Display-4` planned and blocked on D01, `S-Display-5` blocked on D07 plus a server re-export, `S-Display-1B` candidate E awaiting promotion, `S-Display-7` SE column incomplete, and 8, 9, 10 all awaiting gate. Zero green.
      Still open: whether the panel should stop reading `Reader Takeaway` from the README at all.
      EIGHT UNITS CHECKED 260727, EIGHT DISAGREE. Not a stale file, a stale FILE TYPE. `display08`'s README says `Status: planned · Called by: (not yet inserted)` while its S-Display page says `🟡 rendered, awaiting gate` and disk holds a complete five-block `assets/table-body.tex`. `display05` is a THREE-way split: the S-Display page says `candidates/A-table1.tex 🔴 blocked, legacy single-cohort body still in unit`, and disk holds only a `.gitkeep` in `candidates/` with the five-cohort body already shipped in `assets/`. `display01b`'s README predates the D02 fold ruling and does not know candidate E exists. `display01a` and `display02` failed the same way earlier the same day. `display03` is the worst: its README says `rendered (reused legacy asset)` while its S-Display page says `⏸️ FOLDED into Figure 2, never \input standalone`, so the README does not merely lag, it asserts the opposite.
      One number now exists in three versions across those files. The cross-model MAE range reads `0.085-0.127` in `display10`'s README, `0.085-0.131` on its S-Display page, and `0.085` to `0.131` in the shipped `table-body.tex`. No sentence quotes a range yet, so no prose is wrong today; the point is that a panel sourced from the README would print the one figure that matches nothing on disk.
      Measured on `display01a-hero-concept` 260727: its README says state "rendered" while `0-lifecycle/3-display/S-Display-1a-hero-concept.md` says `🔴 rendered but REVISE-blocked`, and they disagree on FIVE things including which file is the live render. Disk agrees with the S page; the README is stale.
      The resolver takes `Reader Takeaway` and `Placement` from `README.md`, so a chip's panel can present a stale takeaway with full confidence. Either the S-Display page becomes the authority the panel reads, or the two have to be kept in step by something other than goodwill. `display02` failed the same way on `S-Main-7` the same day, where the README said "rendered" and the accepted candidate had never been promoted.
- [x] 🟢 A table chip went green off disk, not off whether the unit is AGREED. Ruled and built 260727
      The table half of `QBe1d`'s item of the same name, which carries the argument and the ruling; this is the count on this side. Measured 260727: `S-Display-4` says `🔴 planned · blocked on D01` and its 4 chips all rendered `ok`, because `float.tex` exists and the mtimes are fine. Disk-built and author-agreed are two different facts and only one of them reached the colour.
      Those 4 now read `owed`. `S-Display-4` is the unit the MAIN REGRESSION table hangs on, so this was the sharpest case on the table side: the paper's central result was pointing at a display whose own page says it is still planned and blocked on D01.
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
- [x] 🧪 One live example on the MISQ paper
      CLOSED 260727 on the unit that was `S-Display-8` and is now `S-Display-3c`. It is the cheapest real test and it turned out to be the only WIRED one: the master reaches `sections/05_data_variables.tex`, which both `\input`s that unit's `float.tex` and references `\ref{tab:variable-operationalization}`, so Table 3 prints and resolves in the compiled PDF. Every other unit in the set is declared and unreferenced, and the compile log shows exactly two `??`, `tab:descriptives` and `tab:gradient_results`. `tab:descriptives` is the near miss this face should care about: the sentence and the label both exist and nothing inputs the float, so one `\input` line separates a working citation from a `??`.

## States
Built and live on the MISQ board. Recounted 260727 after the S-Display jump links landed: 38 table chips, 36 `ok` and 2 `unowned`, against 33 figure chips at 18 `ok`, 7 `ready` and 8 `broken` from the same resolver. The earlier reading of "seven table chips, all ok" was taken 260726, before the `> Display:` lanes on `S-Main-4` and `S-Main-5` were written, and is superseded.

Both `unowned` table chips are a `\ref{}` matching no unit, so neither carries an S-Display jump link, which is correct: there is no owning face to jump to. Every one of the other 69 display chips does carry one.

Since the 260727 ruling on `QBe1d`, `ok` counts the ruling as well as the files. On this side that moved the 4 `S-Display-4` chips to `owed`, which matters more than the count suggests: that unit carries the main regression table, so the paper's central result had been pointing at a display whose own page says planned and blocked on D01.

The figure side is still where the rest of the trouble is: 8 `broken` and 7 `ready` there against 0 and 0 here, from the same resolver.

The finding is not on the board, it is in the audit, and it is the same shape as `QBe1a`'s:

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

That second row is the sixth-link diagnostic of the provenance chain (`QD1@display`) firing at scale: nine displays exist, are built, and nothing in the manuscript points at them. Whether the sections are behind or the displays are speculative is a judgment; the board's job was only to make it visible.

The table preview shipped 260726: seven panels render their `table-body.tex` inline, so a number in a sentence can be checked against the row it came from without leaving the page.

It showed LaTeX source rather than typeset rows, and that gap closed the same day. The panel now leads with the unit's `preview.pdf`, which is `float.tex` compiled standalone, so a table chip opens on the actual typeset rows plus the caption and the notes. A table unit carries no image at all, so before this there was no way to SEE one.

- 260726 CC · 🔗 Closing this unblocks `QA9`'s chip renderer
  `QA9` on the boardform board owns the MECHANISM: the fold, the badge, the drawer, the tint, the click-to-add.
  Its one unbuilt item, inline-marker chips, is blocked on four rulings, and this face is the table one: what the chip means, what states it has, and what resolves it, which here is a display id whose table is checkable on sight.
  The mechanism cannot be built against a guess, so that item stays open until all four of `QBe1a` to `QBe1d` say what to render.

## Law
- A sentence points at the display UNIT, never at a file, a candidate, or a float number. The id survives a re-render, a promotion, a citation style and an output format.
- Staleness is COMPUTED, never declared. A state a human has to remember to set is a state that will be wrong.
- The same law holds under a RENAME, which is the harder case (260727). A re-render only stales a state; renaming the units stales the WORDS a page used to name them. Measured on the MISQ regroup that evening: every computed thing survived, 218 evidence cards with their kinds, anchors and previews intact, and every declared thing broke, including 17 hand-written display labels, four pasted state notes, a mapping table rewritten on both sides so it misreported its own history, and nine generated contract blocks mis-mapped because they had been written under older ids. So a page states a display's identity ONCE, in the marker the resolver reads, and never a second time in prose beside it.
- A LIVE ROUTE is repointed and a HISTORICAL ROW is not. A record rewritten to today's ids stops being a record, and a rename mapping table is the one shape a global id rewrite must never touch. Where both live on one page, the page carries a translation table rather than a rewrite.
- A display's KIND comes from its own `float.tex`. The board does not guess table from figure, and the chip says which before it says anything else.

## Log
- 260803 · Left `QB · Delivery` for the new `QBe · Delivery Element` group, and `QB12c` became `QBe1c`, then took its place in the unit-size order ruled the same day (JL 260803: sentence, display, section); the old id resolves as a declared alias in `board.md ## Links`.
- 260727 · Extended this face's own law after the MISQ id regroup, which stressed it in a way a re-render never does. What the resolver computes survived the rename and what a human had typed did not, in five separate shapes, and the two new law lines above are what that measurement licenses: state a display's identity once in the marker, and repoint live routes while leaving historical rows their old ids. The 🧪 item also closed, on the unit that was `S-Display-8` and is now `S-Display-3c`, which is the only unit in this paper whose float reaches the compiled PDF.
- 260727 · The ruling landed on `QBe1d` and this side consumed it without a change of its own, which is the same evidence `QBe1a` recorded when `QBe1b`'s bracket resolver shipped: these are faces of one mechanism, not parallel ones. Four table chips moved `ok` to `owed`, all on `S-Display-4`, the main regression table.
- 260727 · JL asked whether a display panel could also point at that display's Stage page on the paper board. It already does, from earlier the same day, and verifying the count rather than the code turned up two things for this side. The chip census here was stale: 38 table chips now, not the seven recorded 260726, because the `> Display:` lanes on `S-Main-4` and `S-Main-5` landed in between. And a table chip goes green off disk while the unit's own S page may say it is blocked, which is the same defect `QBe1d` now carries the ruling for.
- 260726 · JL: "remove the icons, just keep different colors", then "only the box fill color to be of opacity, how about you make the font color to be 100% solid". Both done in `board.css`. Every chip carried a kind emoji in `::before` and a state glyph in `::after`, so `QC5`'s eleven-chip paragraph carried twenty-two decorations before a word of prose; both are gone and colour alone says the state. The first attempt at the fade used `opacity` on the whole chip, which dimmed the TEXT as well, and that was the wrong axis: the text is the content and the box is the decoration, so only the box gives ground. Now the fill sits at 6%, the border at 14% and the text at 100%, and hover deepens the fill without ever touching the text. `broken` and `unowned` keep a heavier box on purpose, because a defect that sinks into the prose is a defect nobody acts on. The glyph was the third copy of the state anyway: the `title=` names it in words and the panel repeats it in its header.
- 260726 · JL: "for the display, could we also make the float.tex's pdf to be embedded in the popped out window as well?" Yes, and the file to embed turned out to be `preview.pdf` rather than `assets/figure.pdf`: it is `float.tex` COMPILED STANDALONE, so it carries the caption, the notes and the numbering set by the paper's own class, which `assets/` never does. It leads the panel on the same terms as a citation's `.bbl`: show the thing as the manuscript will set it. All 10 MISQ units already had one. A preview older than the asset it previews is labelled rather than hidden.
- 260726 · JL: "add the google scholar search link"; and "for the values, displays, figures, I cannot click them". The citation panel's link row gained a `🔎 Scholar` search, last and with its own glyph because everything above it is an identifier and a query is not; on this paper 195 of 216 entries had no clickable pointer before it. The dead chips were a CSS class collision: `.fig`, meant for markdown images, also matched every figure panel (`chipcard disp fig <state>`) and its `display:block` un-hid the closed popover, so five invisible full-width panels lay over the page eating clicks. Scoped to `img.fig`, with `.chipcard:not(:popover-open){display:none}` as a guard. My first diagnosis blamed `<summary>` and added a script handler; the A/B showed the handler changed nothing and it was reverted, so the chip is script-free again. Verified in headless Chrome 150: 11/11 on `QC5` and 25/25 on the MISQ board's first slide, reachable, opening, and landing on screen.
- 260726 · JL: "read QA6 ⑦ The paper folder, we have done many changes here, right?" Correct, and the board was teaching the superseded layout. QA6 ruled 260726 that the deliverable is UNNUMBERED (`displays/`, `sections/`) and the resolver still had `0-displays` hardcoded in six places. Proved it by renaming the fixture and rebuilding: four id chips went `unowned` and both `\ref{}` chips went GREEN through the "a \label that is not a display unit" branch, which is the silent false-green `QBe1c` and `QBe1d` exist to prevent. `Paper` now resolves `displays/` first and falls back to `displays/`; the fixture moved to the ruled name. Still open on QA6's side: `.board-refs.bbl` is machinery sitting in the unnumbered half.
- 260726 · JL, on the embed: "I don't want you to refer something, please just make it real in the content, not refer a markdown". Reverted. The example prose is written directly in each page's `## Content`: `QC5` carries the whole paragraph, `QBe1a`-`QBe1d` carry only their own sentences from it, labelled by position. The rule that came out of it is the one on `QC5`: PROSE lives on the page, EVIDENCE lives in `_fixture/` (`.bib`, `.bst`, `displays/`, `1-probes/`), and `_fixture/` never holds a paragraph. Same visit fixed the panel: without `position-area` support the base `.chipcard` had no `max-height`, so a two-image figure panel grew past the viewport and spilled over the page.
- 260726 · Built. Three reference forms turned out to be in live use for one unit (`display04`, `display04-main-regression`, `\ref{tab:results}`), so all three resolve rather than one being declared canonical. The audit found 4 dead `\ref{}` compiling to `??` and 9 of 10 units cited by nothing, neither of which any chip could show, because the board renders faces and the manuscript lives in `sections/`.

## Files
**The skills this ruling binds.**

- `haipipe-paper-draft-display`
  Maps a claim to an existing unit, or files a DR row. It may never link a unit that does not exist, which is what keeps a table chip honest.
- `haipipe-paper-revise-place`
  Turns a done DR row into `\input` + `\ref`. The `\input` PATH is the open question this face carries to `QBe3a`.
- `4-display/`
  Owns the unit. This face only rules how a SENTENCE names it.

**Where the evidence lives** (live routes, repointed 260727 after the MISQ regroup; see `QBe1d` for the translation table)
- `0-lifecycle/3-display/S-Display-3c-variable-operationalization.md`
  A rendered, venue-mandatory table unit, and now the ONLY unit in the set whose float reaches the compiled manuscript: `sections/05_data_variables.tex` inputs it and references its label. Was `4-display/S-Display-8-…`.
- `displays/`
  Where the units and their source data live.
