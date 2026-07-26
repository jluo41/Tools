# A sentence with a Display · figure
state: ✅ SETTLED
owner: JL
method: the same stable id as a table, plus the two things a figure has and a table does not

## Question
When a sentence sends the reader to a figure, what is different from sending them to a table? Mechanically nothing, and in what a reader can verify, everything. A table shows its numbers, so a wrong one is checkable on sight; a plausible-looking plot built from the wrong column is invisible.

Mechanically, nothing: both are display units behind a stable id. The difference is what a reader can verify. A table shows its numbers, so a wrong one is checkable on sight. A figure shows a rendering, and a plausible-looking plot built from the wrong column is invisible. A figure also has candidates in a way a table rarely does, so the id has to keep pointing at the same unit while the picture behind it changes.


The approach is the same stable id as a table, plus an explicit candidate state, because a figure changes behind its id while a table usually does not. What we want is that a sentence citing an unpromoted candidate says so, rather than reading as settled while the picture underneath it is still being chosen.
## Boundary
- ✅ Covered here
  The figure reference in prose, the `> Display:` lane for a figure, candidate promotion, and what the panel shows.
- ↪ Covered elsewhere
  The sentence itself is `QC0`; the rendering mechanism is `QA9` on the boardform board; a table is `QC3`; who owns rendering is `QD1`; how a figure is drawn is the Display family, not this board.

## Diagram
```
 MECHANICALLY IDENTICAL TO A TABLE. VERIFIABLY, THE OPPOSITE.

   a TABLE            shows its numbers
                      a wrong one is checkable ON SIGHT
   a FIGURE           shows a rendering
                      a plausible plot built from the WRONG COLUMN
                      is invisible                             ⚠️

 CANDIDATES ARE THE OTHER DIFFERENCE

   the sentence   …the gradient is monotone (Figure~\ref{display02})
                          │  the id must not move
                          ▼
   ┌ display02 ─ the UNIT ────────────────────────────────────┐
   │  candidates/  a  b  c ◄live   d                          │
   │  promoted:    no                                    ⚠️    │
   │  the picture behind the id CHANGES; the id does not      │
   └──────────────────────────────────────────────────────────┘
     > Display: display02 · target=S-Display-2 · kind=figure
              · state=candidate-c · promoted=no

 LIVE ON MISQ RIGHT NOW
   S-Display-2   candidate C rendered, awaiting promotion
   S-Display-6   v1 live, candidate E awaiting promotion
   a sentence citing either one today is citing something
   that is about to change.

 CHIP STATES
   ✅ promoted    the live asset IS what the argument was written against
   🟡 candidate   rendered, not promoted: the prose may be describing a
                  picture that will not ship        ◄ no table equivalent
   ⏳ requested   a row exists; nothing rendered
   ⏸️ folded      merged into another unit (S-Display-3 into Figure 2)
   ⚠️ orphan      the sentence names an id no unit owns

 THE CARD'S ONE OBLIGATION
   a thumbnail is a PREVIEW, never the evidence. The card must name
   WHICH CANDIDATE it is showing, or it reassures the reader about
   the wrong picture.

 WHERE THIS PAGE'S EVIDENCE LIVES IN THE BOARD FOLDER
   the prose      QC4-sentence-display-figure.md  ## Content   (S6)
   the unit       _fixture/displays/display02-discretion-gradient/
     float.tex                    \label{fig:discretion-gradient}
     assets/figure.png            LIVE, what the manuscript compiles
     candidates/C-enriched.png    WAITING, and why the chip is amber
   both pictures are in the panel; neither tells you it used the right column
```

## Content
### What sits where
```
 in the sentence   a stable display id, projected as \ref{} in LaTeX
 under it          > Display: display02 · target=S-Display-2 · kind=figure
                            · state=candidate-c · promoted=no
```

### S6 of the paragraph on `QC0`
`QC0` carries one paragraph with all four attachment types. This is its last sentence, the one that sends the reader to a figure, written here and resolved against `_fixture/displays/display02-discretion-gradient/`:

The association concentrates in the cohorts where the physician has prescribing latitude and flattens where opioids are protocolized (\ref{fig:discretion-gradient}).
> Display: display02 · target=S-Display-2 · kind=figure · state=candidate-C · promoted=no

Two chips, one unit, and both amber. Click either and the panel shows BOTH pictures, captioned LIVE and CANDIDATE, because `assets/figure.png` is what the manuscript compiles while `candidates/C-enriched.png` is what is waiting. These are the real files, and the amber says the prose may be describing a picture that will not ship.

The paragraph's other sentences are the sibling pages': S1 to S3 the citations are `QC1`, S4 the numbers is `QC2`, S5 the table is `QC3`.

### Why this is not `QC3` with a different file extension
Look at the two display chips in that one paragraph. `QC3`'s table puts its ROWS in the panel, so a wrong number is checkable on sight. This one puts two PICTURES in the panel: you can see that both exist and which is live, and you still cannot tell from either image whether it was built from the right column. Same grammar, same resolver, same lane, and a reader's ability to check collapses. That asymmetry is the whole reason these are two faces rather than one.

### A reference that resolves to nothing
`\ref{fig:agreeableness_dist}` is cited in `0-sections/05-2_data_construction.tex:152` on this paper and matches no `\label`:

The trait distribution is shown in \ref{fig:agreeableness_dist}.

### Candidates are the difference
A figure unit typically holds several candidates and one promoted asset.
The sentence must keep referring to the unit while the candidate behind it changes, and the lane must say which candidate is live and whether it has been promoted.
This is live on the MISQ paper right now: `S-Display-2` sits at "candidate C rendered, awaiting promotion" and `S-Display-6` at "v1 live, candidate E awaiting promotion". A sentence citing either one today is citing something that is about to change.

### Chip states as built, and the five this page first proposed
```
 what this page      what a chip        why
 first proposed      actually renders
 ─────────────────   ────────────────   ──────────────────────────────────
 ✅ promoted          ✅ ok              the live asset IS what the argument
                                        was written against
 🟡 candidate         ✦ ready           a candidate is rendered and not
                                        promoted: the prose may be describing
                                        a picture that will not ship
 ⏳ requested         ⏳ owed            the unit folder exists, assets/ is empty
 ⏸️ folded            —                  no detector; nothing computes it yet
 ⚠️ orphan            ❓ unowned         the id, or the \ref{} label, resolves
                                        to nothing
```
Same five rows as `QC3` except `candidate`, which the table page has no equivalent for and which is the state most likely to produce a sentence that quietly stops being true. Two rows are worth reading twice: `promoted` and `candidate` collapsed into states `QC2` had already built, for the reason below, and `folded` is still only a word on this page.

### The panel as built
The chip carries the unit id, its kind, its `\label`, the state sentence, the README's Reader Takeaway, and a link row that names **every asset and every candidate separately**, so the panel cannot be read as showing one picture when another is live.

The picture is SHOWN, not linked (JL 260726). A figure's evidence is the image, so linking to it and calling that a preview was never the right shape.

```
 ┌ disp fig · broken     display02 ──────────────────────────┐
 │ STALE — source_data.csv was re-run AFTER figure.pdf …     │
 │ It ALSO has 2 candidate(s) waiting                        │
 │                                                           │
 │  LIVE · figure.png            ← what the manuscript shows │
 │  ┌───────────────────────┐                                │
 │  │      [the picture]    │                                │
 │  └───────────────────────┘                                │
 │  CANDIDATE · C-enriched.png   ← what is waiting           │
 │  ┌───────────────────────┐                                │
 │  │      [the picture]    │                                │
 │  └───────────────────────┘                                │
 └───────────────────────────────────────────────────────────┘
```

Both are shown, each captioned LIVE or CANDIDATE, which is this page's own rule made structural: the card cannot show one picture while another is what compiles, because it shows BOTH and names them. That turns `display02` from a sentence about staleness into a side-by-side you can just look at.

A `.pdf` asset cannot be an `<img>`, so a unit holding only a PDF still shows nothing and its links row says where the file is. Images are referenced and `loading="lazy"`, never embedded as data URIs, so the page carries no image weight until a panel opens.

### `candidate` and `ready` turned out to be one state
`QC4` proposed 🟡 `candidate` and `QC2` had already built ✦ `ready`. Building this made it obvious they are the same fact in two vocabularies: something landed, and the manuscript has not caught up. A landed probe answer under a `{VAL:?}` and a rendered candidate under a stale `assets/` are the same colour of problem, so they are the same colour of chip.

## Items to Finish
- [x] 🆔 Point at a stable display id
      The id survives candidate promotion; the sentence never names a candidate file.
- [x] 🎨 Build the figure chip
      Shipped 260726. `candidates/` drives the ready state, and a stale unit discloses its candidates in the same panel rather than reporting only the friendlier half.
- [ ] 🔍 Detect a folded unit
      `folded` has no detector: no README on the MISQ paper records a fold, so there is nothing to read. Either the fold gets recorded or the state is dropped.
- [ ] 📐 Rule what a candidate-state citation means
      Whether a sentence may cite an unpromoted candidate at all, and whether doing so blocks the section's gate.
- [x] 🖼 Show the picture in the card
      Every image asset and every image candidate renders inline, captioned LIVE or CANDIDATE. JL 260726.
- [ ] 📐 Preview a PDF-only unit
      A `.pdf` asset cannot be an `<img>`. Either the renderer also emits a raster, or the panel renders the PDF, or this stays a stated gap.
- [ ] 🧪 One live example on a promoted unit and one on a candidate
      `S-Display-6` is both at once, so it tests the interesting case on its own.

## Where we are
Built and live on the MISQ board 260726, and it caught both figures this page predicted it would.

```
 display06   candidate E-combined-design.png waiting; assets/ still holds
             figure.png, so the compiled paper shows the OLD one
 display02   STALE and ALSO holding 2 candidates: source_data.csv was
             re-run AFTER figure.pdf was built, so the manuscript is
             showing numbers the data no longer says
 display01, display03   settled
```

`display02` is the case this page was written for. `S-Display-2` describes it as "candidate C rendered, v1 still live", which is true and is not the worst of it: the underlying data has ALSO moved since the live asset was built. The prose says one thing, the asset shows another, and the data says a third. The chip reports the stale state and discloses the candidates in the same panel, because reporting only the candidate would have been the more reassuring half.

The panel now shows the pictures side by side, captioned, so `display02`'s three-way disagreement is visible rather than described. Two gaps remain and both are in Items: a unit whose only asset is a `.pdf` still previews nothing, and `folded` has no detector because no README records a fold.

- 260726 CC · 🔗 Closing this unblocks `QA9`'s chip renderer
  `QA9` on the boardform board owns the MECHANISM: the fold, the badge, the drawer, the tint, the click-to-add.
  Its one unbuilt item, inline-marker chips, is blocked on four rulings, and this face is the figure one: what the chip means, what states it has, and what resolves it, which here is a display id whose figure is not checkable on sight.
  The mechanism cannot be built against a guess, so that item stays open until all four of `QC1` to `QC4` say what to render.

## Law
- A panel names every asset and every candidate separately. A card that shows one picture while another is live is worse than no card.
- Worst state wins, and the panel discloses the rest. A stale unit that also holds candidates is reported STALE and still lists them; reporting only the candidate would be the more reassuring half of the truth.
- `candidate` and `ready` are one state. Something landed and the manuscript has not caught up, whether the thing that landed is a probe answer or a rendered figure.

## Log
- 260726 · JL: "add the google scholar search link"; and "for the values, displays, figures, I cannot click them". Two changes. The citation panel's link row gained a `🔎 Scholar` search, last and with its own glyph because everything above it is an identifier and a query is not; on this paper 195 of 216 entries had no clickable pointer before it. And the chips inside a sentence drawer were dead: `<summary>` consumes the click before the nested button's default action runs, which is why citations opened and values, tables and figures did not. The panel is now asserted explicitly one frame later; `preventDefault` stays out of `board.js`.
- 260726 · JL: "read QA6 ⑦ The paper folder, we have done many changes here, right?" Correct, and the board was teaching the superseded layout. QA6 ruled 260726 that the deliverable is UNNUMBERED (`displays/`, `sections/`) and the resolver still had `0-displays` hardcoded in six places. Proved it by renaming the fixture and rebuilding: four id chips went `unowned` and both `\ref{}` chips went GREEN through the "a \label that is not a display unit" branch, which is the silent false-green `QC3` and `QC4` exist to prevent. `Paper` now resolves `displays/` first and falls back to `0-displays/`; the fixture moved to the ruled name. Still open on QA6's side: `.board-refs.bbl` is machinery sitting in the unnumbered half.
- 260726 · JL, on the embed: "I don't want you to refer something, please just make it real in the content, not refer a markdown". Reverted. The example prose is written directly in each page's `## Content`: `QC0` carries the whole paragraph, `QC1`-`QC4` carry only their own sentences from it, labelled by position. The rule that came out of it is the one on `QC0`: PROSE lives on the page, EVIDENCE lives in `_fixture/` (`.bib`, `.bst`, `0-displays/`, `1-probes/`), and `_fixture/` never holds a paragraph. Same visit fixed the panel: without `position-area` support the base `.chipcard` had no `max-height`, so a two-image figure panel grew past the viewport and spilled over the page.
- 260726 · Built. Building it collapsed this page's proposed `candidate` state into `QC2`'s existing `ready`: they are the same fact in two vocabularies. `display02` came back STALE rather than merely candidate-waiting, which is a worse fact than `S-Display-2` records, and it was found by comparing mtimes rather than by reading anything a person wrote.

## Files
- `0-lifecycle/4-display/S-Display-2-discretion-gradient.md`
  Candidate C rendered, awaiting promotion.
- `0-lifecycle/4-display/S-Display-6-research-design.md`
  v1 live with candidate E pending: both states on one unit.
