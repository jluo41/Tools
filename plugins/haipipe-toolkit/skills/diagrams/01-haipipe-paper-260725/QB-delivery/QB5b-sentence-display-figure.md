# A sentence with a Display · figure
state: 🟡 PARTIAL
owner: JL
method: the same stable id as a table, plus the two things a figure has and a table does not

## Opening
When a sentence sends the reader to a figure, what is different from sending them to a table? Mechanically nothing, and in what a reader can verify, everything. A table shows its numbers, so a wrong one is checkable on sight; a plausible-looking plot built from the wrong column is invisible.

Mechanically, nothing: both are display units behind a stable id. The difference is what a reader can verify. A table shows its numbers, so a wrong one is checkable on sight. A figure shows a rendering, and a plausible-looking plot built from the wrong column is invisible. A figure also has candidates in a way a table rarely does, so the id has to keep pointing at the same unit while the picture behind it changes.


The approach is the same stable id as a table, plus an explicit candidate state, because a figure changes behind its id while a table usually does not. What we want is that a sentence citing an unpromoted candidate says so, rather than reading as settled while the picture underneath it is still being chosen.
Scope: This page covers The figure reference in prose, the `> Display:` lane for a figure, candidate promotion, and what the panel shows. Neighbouring pages cover The sentence itself is `QC5`; the rendering mechanism is `QA9` on the boardform board; a table is `QB5a`; who owns rendering is `QB5c`; how a figure is drawn is the Display family, not this board.

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

 LIVE ON MISQ RIGHT NOW (re-read 260727 evening, AFTER the id regroup)
   S-Display-4c   candidate C-enriched rendered, awaiting promotion
                  ── the unit this page calls display02 throughout; the
                     MISQ ids were regrouped twice on 260727, see Content
   S-Display-1b   PROMOTED, and it is the case this page wanted: candidate H
                  is live as a VECTOR assets/figure.pdf and the raster it
                  replaced is preserved as candidates/G-codex-4panel.png
   a sentence citing 4c today is citing something about to change; a
   sentence citing 1b is citing something that changed TWICE in one day.

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
   the prose      QB5b-sentence-display-figure.md  ## Content   (S6)
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

### S6 of the paragraph on `QC5`
`QC5` carries one paragraph with all four attachment types. This is its last sentence, the one that sends the reader to a figure, written here and resolved against `_fixture/displays/display02-discretion-gradient/`:

The association concentrates in the cohorts where the physician has prescribing latitude and flattens where opioids are protocolized (\ref{fig:discretion-gradient}).
> Display: display02 · target=S-Display-2 · kind=figure · state=candidate-C · promoted=no

Two chips, one unit, and both amber. Click either and the panel shows BOTH pictures, captioned LIVE and CANDIDATE, because `assets/figure.png` is what the manuscript compiles while `candidates/C-enriched.png` is what is waiting. These are the real files, and the amber says the prose may be describing a picture that will not ship.

The paragraph's other sentences are the sibling pages': S1 to S3 the citations are `QB3a`, S4 the numbers is `QB4a`, S5 the table is `QB5a`.

### Why this is not `QB5a` with a different file extension
Look at the two display chips in that one paragraph. `QB5a`'s table puts its ROWS in the panel, so a wrong number is checkable on sight. This one puts two PICTURES in the panel: you can see that both exist and which is live, and you still cannot tell from either image whether it was built from the right column. Same grammar, same resolver, same lane, and a reader's ability to check collapses. That asymmetry is the whole reason these are two faces rather than one.

### A reference that resolves to nothing
`\ref{fig:agreeableness_dist}` is cited in `sections/05-2_data_construction.tex:152` on this paper and matches no `\label`:

The trait distribution is shown in \ref{fig:agreeableness_dist}.

### Candidates are the difference
A figure unit typically holds several candidates and one promoted asset.
The sentence must keep referring to the unit while the candidate behind it changes, and the lane must say which candidate is live and whether it has been promoted.
This is live on the MISQ paper right now: `S-Display-2` sits at "candidate C rendered, awaiting promotion" and `S-Display-1B` at "v1 live, candidate E awaiting promotion". A sentence citing either one today is citing something that is about to change.

### The MISQ ids in this page were renamed twice on 260727
This page cites the MISQ paper as its live example, and that paper's display registry moved under it twice in one day. Pass 1 renumbered the units to reading order in the morning. Pass 2, in the evening, regrouped them into BLOCK plus MEMBER, where the number is the narrative block a unit serves and the letter is its position inside that block.

```
 what this page says      pass 1 (morning)       live id (evening)      unit
 ──────────────────────   ────────────────────   ────────────────────   ──────────────────────
 S-Display-2              S-Display-8            S-Display-4c           discretion gradient
 S-Display-3              S-Display-9            S-Display-2c           llm measurement, folded
 S-Display-4              S-Display-6            S-Display-4a           main regression
 S-Display-5              S-Display-4            S-Display-3b           cohort descriptives
 S-Display-7              S-Display-7            S-Display-4b           context regression
 S-Display-8              S-Display-5            S-Display-3c           variable operationalization
 S-Display-9              S-Display-2            S-Display-2a           agreeableness distribution
 S-Display-10             S-Display-3            S-Display-2b           validation summary
 S-Display-11             S-Display-10           S-Display-3a           inclusion funnel, no folder
 S-Display-1A / 1B        unchanged              S-Display-1a / 1b      the pinned pair, block 01
```

Two things about this table are the point rather than the bookkeeping. The `_fixture/` ids on this page are NOT in it and were deliberately left alone: the fixture is this board's own frozen evidence, so its `display02-discretion-gradient` stays what it is no matter what the paper does. And the historical rows in Items and Log keep the ids they were written with, because a record rewritten to today's names stops being a record. Only LIVE ROUTES were repointed, which is the `## Files` block below.

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
Same five rows as `QB5a` except `candidate`, which the table page has no equivalent for and which is the state most likely to produce a sentence that quietly stops being true. Two rows are worth reading twice: `promoted` and `candidate` collapsed into states `QB4a` had already built, for the reason below, and `folded` is still only a word on this page.

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
`QB5b` proposed 🟡 `candidate` and `QB4a` had already built ✦ `ready`. Building this made it obvious they are the same fact in two vocabularies: something landed, and the manuscript has not caught up. A landed probe answer under a `{VAL:?}` and a rendered candidate under a stale `assets/` are the same colour of problem, so they are the same colour of chip.

## Items to Finish
- [ ] 🪞 The panel reads README.md, and the S-Display page is the one that is true
      HALF-CLOSED 260727 on JL's ask ("I want it can be clicked to the URL to the Stage-Display accordingly"). A display panel now carries a one-click anchor to the S-Display face that owns the unit, AND quotes that page's own `state:` line beside it. So the README's takeaway is still shown, but it can no longer be the only thing a reader has: the authority is one click away and its state is on the chip's own panel. Measured on the MISQ board: 69 links across 10 units, every one resolving to a real face.
      What that surfaced immediately is the thing the READMEs were hiding. Not one of the ten units is settled: `S-Display-1A` REVISE-blocked, `S-Display-3` FOLDED, `S-Display-4` planned and blocked on D01, `S-Display-5` blocked on D07 plus a server re-export, `S-Display-1B` candidate E awaiting promotion, `S-Display-7` SE column incomplete, and 8, 9, 10 all awaiting gate. Zero green.
      Still open: whether the panel should stop reading `Reader Takeaway` from the README at all.
      EIGHT UNITS CHECKED 260727, EIGHT DISAGREE. Not a stale file, a stale FILE TYPE. `display08`'s README says `Status: planned · Called by: (not yet inserted)` while its S-Display page says `🟡 rendered, awaiting gate` and disk holds a complete five-block `assets/table-body.tex`. `display05` is a THREE-way split: the S-Display page says `candidates/A-table1.tex 🔴 blocked, legacy single-cohort body still in unit`, and disk holds only a `.gitkeep` in `candidates/` with the five-cohort body already shipped in `assets/`. `display01b`'s README predates the D02 fold ruling and does not know candidate E exists. `display01a` and `display02` failed the same way earlier the same day. `display03` is the worst: its README says `rendered (reused legacy asset)` while its S-Display page says `⏸️ FOLDED into Figure 2, never \input standalone`, so the README does not merely lag, it asserts the opposite.
      One number now exists in three versions across those files. The cross-model MAE range reads `0.085-0.127` in `display10`'s README, `0.085-0.131` on its S-Display page, and `0.085` to `0.131` in the shipped `table-body.tex`. No sentence quotes a range yet, so no prose is wrong today; the point is that a panel sourced from the README would print the one figure that matches nothing on disk.
      Measured on `display01a-hero-concept` 260727: its README says state "rendered" while `0-lifecycle/3-display/S-Display-1a-hero-concept.md` says `🔴 rendered but REVISE-blocked`, and they disagree on FIVE things including which file is the live render. Disk agrees with the S page; the README is stale.
      The resolver takes `Reader Takeaway` and `Placement` from `README.md`, so a chip's panel can present a stale takeaway with full confidence. Either the S-Display page becomes the authority the panel reads, or the two have to be kept in step by something other than goodwill. `display02` failed the same way on `S-Main-7` the same day, where the README said "rendered" and the accepted candidate had never been promoted.
- [x] 🟢 The panel told the truth and the CHIP PAINTED IT GREEN. Ruled and built 260727
      Measured 260727, and it is this page's own law broken one level up. `worst state wins` was written about the files inside a unit. The S-Display page is now a second source of state on the same unit, the resolver already computes it, and the chip's colour does not consume it.
      22 chips render `ok` while linking to a page that says the unit is not agreed:
      - `S-Display-3` · `⏸️ FOLDED into Figure 2 (JL 2026-07-10)` · 10 chips, all `ok`
        The worst of the three. JL retired this unit, and ten sentences cite it in green.
      - `S-Display-1A` · `🔴 rendered but REVISE-blocked` · 8 chips, all `ok`
      - `S-Display-4` · `🔴 planned · blocked on D01` · 4 chips, all `ok`
      The contradiction is inside this page. The item above states "Zero green" about the ten units; the resolver it describes paints 54 of 71 chips green on the same board. Both sentences are true because they measure different things: the chip state comes from disk, where `float.tex` exists and the mtimes are fine, and the S page's state comes from whether the unit is AGREED. A unit can be perfectly built and still be one JL has folded away.
      RULED 260727: `worst state wins` spans both sources. The argument that decided it is JL's own workflow, "jump to that display and think about how to update it", which only starts if something prompts the click, and a green chip does not.
      Only 🔴 and ⏸️ downgrade, and that line is the substance of the ruling rather than a detail. 🟡 is the normal condition of a live paper and does not make a citation wrong; it covers six of the ten units here, so downgrading it would amber almost every chip on the board and the distinction would stop informing. Green now means agreed AND built. Anything else means do not lean on this unit yet.
      No new state word was needed, which is the check that the ruling fits the existing vocabulary rather than bending it. ⏸️ takes `parked`, already in use for a probe deferred on purpose, and grey is the right colour for a unit set aside. 🔴 takes `owed`, already in use for a unit with nothing built, because in both cases work is outstanding and the tooltip says which kind.
      Measured before and after on the MISQ board: `ok` 54 → 32, and the 22 that moved are exactly the 22 predicted, 10 to `parked` and 12 to `owed`. The disk state is never discarded, only outranked: a downgraded chip's tooltip leads with what disk found, then names the S page and quotes its state line verbatim, because a downgrade whose reason is invisible would be the same defect in a new place.
- [x] 🆔 Point at a stable display id
      The id survives candidate promotion; the sentence never names a candidate file.
- [x] 🎨 Build the figure chip
      Shipped 260726. `candidates/` drives the ready state, and a stale unit discloses its candidates in the same panel rather than reporting only the friendlier half.
- [x] 🔍 Detect a folded unit
      Closed 260727 by the ruling above, and it was reading the wrong file. This item said `folded` has no detector because no README records a fold. True, and beside the point: `S-Display-3` has recorded `⏸️ FOLDED into Figure 2 (JL 2026-07-10)` the whole time. A fold is an authoring decision, so the page the author writes is where it was always going to be, and the README was never going to carry it. Its ten chips now read `parked`.
- [ ] 📐 Rule what a candidate-state citation means
      Whether a sentence may cite an unpromoted candidate at all, and whether doing so blocks the section's gate.
- [x] 🖼 Show the picture in the card
      Every image asset and every image candidate renders inline, captioned LIVE or CANDIDATE. JL 260726.
- [ ] 📐 Preview a PDF-only unit
      A `.pdf` asset cannot be an `<img>`. Either the renderer also emits a raster, or the panel renders the PDF, or this stays a stated gap.
      EXERCISED FOR REAL 260727, and the gap is now smaller and better understood. `display01b` promoted a VECTOR pdf over a raster png, so it is a PDF-only unit on purpose rather than by accident, and `assets/figure.png` was deleted after verifying the raster survives byte-identical at `candidates/G-codex-4panel.png`. The panel still shows the unit, because it leads with `preview.pdf` as an `<object>`, and on tonight's board 142 of 218 display cards carry one. What shows NOTHING is the asset row itself, which is the residual hole: a `.pdf` asset gets a link where a `.png` asset gets a picture, so a PDF-only unit's card has one picture where a raster unit's has two.
      Worth noting for whoever closes it: promoting the vector made the unit's text MEASURABLE, which a raster never was. Its labels are 10.8 pt on a 959.76 pt page, so at `width=\textwidth` they print at 5.3 pt against a 7 pt floor. That is a fact about the figure a card could in principle compute and no reader can see in a thumbnail.
- [x] 🧪 One live example on a promoted unit and one on a candidate
      CLOSED 260727 by `display01b`, which was both at once inside a single day and is now the promoted half. Candidate G, a raster, was promoted at 17:07 and held the asset for about an hour; candidate H, a vector with a live `.pptx` source, superseded it at 18:24. Both are in `candidates/` as lettered files, so the card can name the promoted asset and the candidate it replaced, separately, which is this page's one obligation.
      The candidate half is `S-Display-4c`, still holding `candidates/C-enriched.pdf` unpromoted against a live asset older than its own `source_data.csv`. So the pair this item asked for now exists on one board: a unit whose picture just changed twice, and a unit whose picture has not changed since it should have.

## Where we are
Built and live on the MISQ board 260726, and it caught both figures this page predicted it would.

```
 display01b   candidate E-combined-design.png waiting; assets/ still holds
             figure.png, so the compiled paper shows the OLD one
 display02   STALE and ALSO holding 2 candidates: source_data.csv was
             re-run AFTER figure.pdf was built, so the manuscript is
             showing numbers the data no longer says
 display01a, display03   settled
```

`display02` is the case this page was written for. `S-Display-2` describes it as "candidate C rendered, v1 still live", which is true and is not the worst of it: the underlying data has ALSO moved since the live asset was built. The prose says one thing, the asset shows another, and the data says a third. The chip reports the stale state and discloses the candidates in the same panel, because reporting only the candidate would have been the more reassuring half.

The panel now shows the pictures side by side, captioned, so `display02`'s three-way disagreement is visible rather than described.

As of 260727 the chip's colour also answers whether the unit is AGREED, not only whether its files are in order. The display chips on the MISQ board now read 32 `ok`, 12 `owed`, 10 `parked`, 8 `broken`, 7 `ready` and 2 `unowned`, where before the ruling 54 were `ok`. Nothing about the assets changed; 22 chips stopped claiming a unit was fine when its own page said otherwise.

`folded` never needed a detector after all, which closes that gap from the other end. It was filed as unreadable because no README on this paper records a fold, and that was the wrong file to read: `S-Display-3` has said `⏸️ FOLDED into Figure 2 (JL 2026-07-10)` all along. Its ten chips are the ten now reading `parked`.

The other one closed 260726. A unit whose only asset is a `.pdf` used to preview nothing; the panel now leads with `preview.pdf`, the compiled float, so every unit shows something regardless of what its `assets/` holds. The `.pdf` ASSET still cannot be an `<img>`, which is a different and much smaller hole: the float above it already shows the same graphic in place.

- 260726 CC · 🔗 Closing this unblocks `QA9`'s chip renderer
  `QA9` on the boardform board owns the MECHANISM: the fold, the badge, the drawer, the tint, the click-to-add.
  Its one unbuilt item, inline-marker chips, is blocked on four rulings, and this face is the figure one: what the chip means, what states it has, and what resolves it, which here is a display id whose figure is not checkable on sight.
  The mechanism cannot be built against a guess, so that item stays open until all four of `QB3a` to `QB5b` say what to render.

## Law
- A panel names every asset and every candidate separately. A card that shows one picture while another is live is worse than no card.
- Worst state wins, and the panel discloses the rest. A stale unit that also holds candidates is reported STALE and still lists them; reporting only the candidate would be the more reassuring half of the truth.
- `candidate` and `ready` are one state. Something landed and the manuscript has not caught up, whether the thing that landed is a probe answer or a rendered figure.
- Worst state wins across BOTH sources of truth about a unit, not only across the files inside it (JL 260727). Disk answers whether the assets are built, are stale, have a candidate waiting. The unit's own S-Display page answers whether the paper may lean on it at all, which disk cannot know. A unit can be perfectly built and still be one the author has folded away.
- Only 🔴 and ⏸️ on that page downgrade a chip: 🔴 to `owed`, ⏸️ to `parked`. 🟡 does not, because work in progress is the normal condition of a live paper and ambering it would amber nearly everything. So GREEN MEANS AGREED AND BUILT, and every other colour means do not lean on this unit yet.
- A downgraded chip states its own reason. The tooltip leads with what disk found, then names the S page and quotes its `state:` line verbatim. A downgrade a reader cannot account for is the same false signal pointing the other way.

## Log
- 260727 · A READER OF THIS PAGE TOLD JL THE CARD WAS TEXT ONLY, WHICH IS THE FAILURE THIS PAGE EXISTS TO PREVENT, POINTING THE OTHER WAY. Asked whether a display could be embedded in the evidence card, CC measured `board.html` with a regex that stopped at the first `</div>`, found no `<img>` inside a card it had truncated, reported "the evidence card is text only", and proposed building a feature that shipped on 260726. Re-measured properly: 218 display cards, 142 carrying the compiled `preview.pdf` as an `<object>` under "AS THE FLOAT WILL PRINT, caption included", 32 carrying LIVE or CANDIDATE images inline, 142 carrying the `S-Display` anchor with the page's own `state:` quoted, and 103 `<img>` on the board of which only 9 are markdown embeds. The lesson is not about a regex. A card whose contents are only visible on hover cannot be verified by grepping the HTML, so this page's own claims should be checked with a parse that respects nesting, or in the browser, and never with a truncating pattern.
- 260727 · The MISQ registry was regrouped into block plus member, and the split between COMPUTED and DECLARED state decided what survived it. Everything the resolver computes came through the rename untouched: 218 cards, every kind read from `float.tex`, every `S-Display` anchor, every preview path. Everything a human had typed broke: 17 hand-written labels on the Main pages still read `Display 06 · main regression` while pointing at `display04a-main-regression/preview.png`, four `⚠️ State ·` notes pasted onto `S-Display-0` restated states the cards already carry, a rename mapping TABLE was rewritten on both sides so it claimed the morning pass had produced the evening's names, nine generated contract blocks written under older ids were silently mis-mapped, and the two page anchors that had to swap did not. That is `QB5a`'s "staleness is COMPUTED, never declared" holding under a second kind of stress: not a re-render, a RENAME. Live routes were repointed on this page and the historical rows keep their old ids, with a translation table in `## Content` so both can be read.
- 260727 · Ruled and built on JL's "please continue": `worst state wins` now spans disk AND the unit's S-Display page. Only 🔴 and ⏸️ downgrade, to `owed` and `parked`; 🟡 does not, because it covers six of ten units here and ambering it would drown the signal it is meant to carry. `Paper._gate()` applies it in both `display()` and `ref()`, and `_sdisplay()` is cached because every chip now asks twice. On the MISQ board `ok` went 54 to 32 and the 22 that moved are exactly the 22 predicted. Two things fell out of building it. No new state word was needed, `parked` and `owed` already meant this. And the `folded` detector item closed from the other end: it had been filed as undetectable because no README records a fold, when the S page had said `⏸️ FOLDED` all along, which is where an authoring decision was always going to live.
- 260727 · JL asked whether a display panel could also point at that display's Stage page on the paper board, "so we can jump to that display, and think about how to update it". It already does, from earlier the same day: 69 of 71 display chips carry a `🗂 S-Display-N · <state>` anchor, and the 2 without one are `unowned` refs that own no unit, which is correct. Verified by counting the rendered anchors rather than reading the code. What the count exposed is the item added above: the panel now names the S page's state and the chip's COLOUR still ignores it, so 22 chips sit green while linking to a page that says the unit is folded or blocked. `S-Display-3` is the case that makes it plain, folded by JL on 2026-07-10 and cited by ten green chips. Also fixed a `SyntaxWarning` that shipped with the feature: `_sdisplay()`'s docstring contains `\input` and was not raw, so every build printed a warning before its first line of output.
- 260726 · JL: "remove the icons, just keep different colors", then "only the box fill color to be of opacity, how about you make the font color to be 100% solid". Both done in `board.css`. Every chip carried a kind emoji in `::before` and a state glyph in `::after`, so `QC5`'s eleven-chip paragraph carried twenty-two decorations before a word of prose; both are gone and colour alone says the state. The first attempt at the fade used `opacity` on the whole chip, which dimmed the TEXT as well, and that was the wrong axis: the text is the content and the box is the decoration, so only the box gives ground. Now the fill sits at 6%, the border at 14% and the text at 100%, and hover deepens the fill without ever touching the text. `broken` and `unowned` keep a heavier box on purpose, because a defect that sinks into the prose is a defect nobody acts on. The glyph was the third copy of the state anyway: the `title=` names it in words and the panel repeats it in its header.
- 260726 · JL: "for the display, could we also make the float.tex's pdf to be embedded in the popped out window as well?" Yes, and the file to embed turned out to be `preview.pdf` rather than `assets/figure.pdf`: it is `float.tex` COMPILED STANDALONE, so it carries the caption, the notes and the numbering set by the paper's own class, which `assets/` never does. It leads the panel on the same terms as a citation's `.bbl`: show the thing as the manuscript will set it. All 10 MISQ units already had one. A preview older than the asset it previews is labelled rather than hidden.
- 260726 · JL: "add the google scholar search link"; and "for the values, displays, figures, I cannot click them". The citation panel's link row gained a `🔎 Scholar` search, last and with its own glyph because everything above it is an identifier and a query is not; on this paper 195 of 216 entries had no clickable pointer before it. The dead chips were a CSS class collision: `.fig`, meant for markdown images, also matched every figure panel (`chipcard disp fig <state>`) and its `display:block` un-hid the closed popover, so five invisible full-width panels lay over the page eating clicks. Scoped to `img.fig`, with `.chipcard:not(:popover-open){display:none}` as a guard. My first diagnosis blamed `<summary>` and added a script handler; the A/B showed the handler changed nothing and it was reverted, so the chip is script-free again. Verified in headless Chrome 150: 11/11 on `QC5` and 25/25 on the MISQ board's first slide, reachable, opening, and landing on screen.
- 260726 · JL: "read QA6 ⑦ The paper folder, we have done many changes here, right?" Correct, and the board was teaching the superseded layout. QA6 ruled 260726 that the deliverable is UNNUMBERED (`displays/`, `sections/`) and the resolver still had `0-displays` hardcoded in six places. Proved it by renaming the fixture and rebuilding: four id chips went `unowned` and both `\ref{}` chips went GREEN through the "a \label that is not a display unit" branch, which is the silent false-green `QB5a` and `QB5b` exist to prevent. `Paper` now resolves `displays/` first and falls back to `0-displays/`; the fixture moved to the ruled name. Still open on QA6's side: `.board-refs.bbl` is machinery sitting in the unnumbered half.
- 260726 · JL, on the embed: "I don't want you to refer something, please just make it real in the content, not refer a markdown". Reverted. The example prose is written directly in each page's `## Content`: `QC5` carries the whole paragraph, `QB3a`-`QB5b` carry only their own sentences from it, labelled by position. The rule that came out of it is the one on `QC5`: PROSE lives on the page, EVIDENCE lives in `_fixture/` (`.bib`, `.bst`, `0-displays/`, `1-probes/`), and `_fixture/` never holds a paragraph. Same visit fixed the panel: without `position-area` support the base `.chipcard` had no `max-height`, so a two-image figure panel grew past the viewport and spilled over the page.
- 260726 · Built. Building it collapsed this page's proposed `candidate` state into `QB4a`'s existing `ready`: they are the same fact in two vocabularies. `display02` came back STALE rather than merely candidate-waiting, which is a worse fact than `S-Display-2` records, and it was found by comparing mtimes rather than by reading anything a person wrote.

## Files
**The skills this ruling binds.**

- `haipipe-paper-draft-display`
  Same as `QB5a`, plus the candidate state: a unit with an unpromoted candidate must not read as settled.
- `haipipe-paper-revise-place`
  Places the reference. It cannot see which candidate is live, which is why the lane has to say.
- `4-display/`
  Owns promotion. This face rules only what the sentence may claim while promotion is pending.

**Where the evidence lives** (live routes, repointed 260727 after the regroup)
- `0-lifecycle/3-display/S-Display-4c-discretion-gradient.md`
  Candidate C-enriched rendered, awaiting promotion. Was `4-display/S-Display-2-…`.
- `0-lifecycle/3-display/S-Display-1b-research-design.md`
  Candidate H promoted as a vector; G preserved as the candidate it replaced. Was `4-display/S-Display-1B-…`.
- `0-lifecycle/3-display/S-Display-2c-llm-measurement.md`
  The folded unit this page's `parked` ruling was measured on. Was `S-Display-3`.
