# The Display as a folder
state: 🟡 PARTIAL
owner: JL
method: fix the folder's contents from the units that exist, and move the folder inside 0-lifecycle

## Question
What is a display folder made of, and where does it sit in a paper? Every unit on this paper already has the same five parts, so the anatomy is settled by practice rather than by anything written down, and the one thing that was written down, its LOCATION, is now ruled the other way.

**The folder lives in `0-lifecycle/`, one per paper (JL 2026-07-27).** It sits at the paper root today, beside `sections/`, because `QA6` ⑦ ruled the deliverable UNNUMBERED and the machinery numbered. A display unit fails that test on inspection: of its five parts, four are working state that no reader ever sees.

## Boundary
- ✅ Covered here
  What the folder contains, what each part is for, which parts are machinery, and where the folder belongs in a paper.
- ↪ Covered elsewhere
  WHY a unit has both a page and a folder is `QA3@display`, ruled and not re-argued: "A page decides; a folder renders. Neither replaces the other." What the Intake inside `source/` must carry is `QB2@display`; how `candidates/` is promoted into `assets/` is `QB4@display`; who ASKED for the render that fills them is `QD2`; the caption and label inside `float.tex` are `QD3`; where the float lands is `QD4`.

## Content
### What one unit actually contains
Measured across all ten units on this paper, 2026-07-27. Every one has the same four subfolders, so this is the shape, not a proposal.

```
 displays/display01b-research-design/
 │
 ├── float.tex        THE DELIVERABLE. \caption, \label, \includegraphics.
 │                    The only file a compiled manuscript ever reaches.
 ├── assets/          the LIVE asset the float points at        figure.png
 ├── candidates/      rendered, NOT chosen                      E-combined-design.png
 ├── versions/        superseded assets, kept                   5 files here
 ├── source/          how to rebuild it: prompts, preflight,    4 files here
 │                    the JSON the renderer consumed
 ├── preview.tex      float.tex compiled STANDALONE, so the card
 └── preview.pdf      can show the float as the manuscript will set it
```

### The delete test, applied honestly
`QA6` ⑦ ruled that a numbered folder is working machinery and an unnumbered one is the deliverable, and put `displays/` unnumbered next to `sections/`. Run that test part by part and the unit splits four to one:

- `float.tex` · deliverable. It is what `\input` reaches.
- `assets/` · deliverable, but only the one file the float names.
- `candidates/`, `versions/`, `source/`, `preview.*` · machinery, every one. Delete them and the manuscript still compiles identically.

A folder that is four-fifths machinery does not belong beside `sections/`, and that is what the 2026-07-27 ruling fixes: the display folder moves inside `0-lifecycle/`, where the rest of the paper's working state already lives, next to the `S-Display-*` pages that decide it.

### The two halves are already in one place, in spirit
`0-lifecycle/3-display/` holds the twelve decision pages and `_DISPLAY_REQUEST.md`. `displays/` holds the ten unit folders. `QA3@display` says these are two things and must stay two, and it does not say they live in two different trees. Bringing the folder in makes the page and the folder siblings, which is what a reader looking for one display expects.

### What this does NOT change
The unit id, the label, and every `\ref{}` in the manuscript. A sentence points at the UNIT, never at a file, which `QC3`'s law already fixes: "The id survives a re-render, a promotion, a citation style and an output format." A path move is exactly the kind of change that law exists to absorb.

## Items to Finish
- [x] 📐 Fix the anatomy from the units that exist
      Five parts, ten units, no exceptions: `float.tex` plus `assets/ candidates/ versions/ source/` plus `preview.tex`/`preview.pdf`. Measured 2026-07-27 rather than designed.
- [x] ⚖️ Rule where the folder lives
      Inside `0-lifecycle/`, one per paper (JL 2026-07-27). The delete test is what settles it: four of the five parts are working state.
- [ ] 🚚 Move it, and repoint everything that names the old path
      `dialect_paper.py` resolves `displays/` then falls back to `0-displays/`, so the resolver needs the new path or every marker on the board goes `unowned`. Also: every `> Display:` lane on the S-Main pages, the `Registry id` lines, `_preview/gallery-preview.tex`, and `0-lifecycle/3-display/4-display.tex`.
- [ ] 🧹 Rule the four legacy folders that are not units
      `displays/` also holds `Figure/ Table/ AppendixFigure/ AppendixTable/`, which predate the unit layout. §4 still `\input`s one of them, which is why `tab:agreeableness-distribution` resolves to the wrong label.
- [ ] 📎 Say what `QA6` ⑦ now reads
      That face put `displays/` in the unnumbered half. It has to be amended or this page contradicts it, and a board that contradicts itself is worse than either answer.

## Where we are
The anatomy is fixed and the location is ruled; neither has been applied. The folder is still at the paper root, and `QA6` ⑦ still says it belongs there.

Rewritten 2026-07-27 on JL's ruling. The first draft of this face asked whether a display was owed at all, which JL judged not good enough: that is a question the DRAFT phase already answers every time it files a display request, whereas the folder and its contents were written down nowhere.

## Files
- `displays/`
  Ten unit folders plus four legacy `Figure/ Table/ AppendixFigure/ AppendixTable/` folders.
- `0-lifecycle/3-display/`
  The twelve `S-Display-*` decision pages and `_DISPLAY_REQUEST.md`; the destination.
- `dialect_paper.py`
  Resolves `displays/` first and `0-displays/` as fallback. It decides whether every display marker on the board resolves after the move.
