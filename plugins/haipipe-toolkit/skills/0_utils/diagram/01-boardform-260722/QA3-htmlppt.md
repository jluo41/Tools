# One file, two modes
state: 🟡 PARTIAL
owner: CC
method: one file, two modes: scroll to read / one question per screen. JL has ruled: merge

## Question
`board.html` is normally one long document — one person scrolls and reads, which works well; but projecting in a meeting wants "one screen per question". Should these be two files, or one file with two modes?

- Why it is hard
  Two files (`board.html` + `deck.html`) means two things to keep in sync, and they will drift. One file has to satisfy two opposite layouts at once — "scroll to read" and "one screen per page".
- What breaks if we leave it
  Mid-meeting you want to expand one question's details and have to switch files — awkward, and it is easy to project the stale copy.
- What it affects downstream
  Whether the remaining projection features (arrow-key paging, presenter mode) get built and where — they all need JS, and the board has the invariant "must never depend on JS to be readable".

## Boundary
- ✅ Covered here
  **Projection**: one file or two, how focus mode doubles as a slide, whether paging and presenter mode get built.
- ↪ Covered elsewhere
  How the single-question page is **laid out** (section order, names, what folds) — that is `QA4`. Nor how the board is **shared with others** — that is `QE1`.

## Diagram
```
             Q*.md ──build.py──► board.html   ← the only file
                                    │
                ┌───────────────────┴───────────────────┐
           default: scroll & read              click a row: one question per screen
           all questions on one page           only that question on screen
           read alone / send to an RA          project in a meeting
                └────── same file, same content ──────┘

✗ no second deck.html            still missing: ← → paging · presenter mode (both need JS)
```

## Items to Finish
- [x] One question per screen, paged (board.html's focus mode already does it)
- [x] Only one file, no second `deck.html`
- [ ] Arrow-key ← → paging
- [ ] Presenter mode (presenter sees the discussion, audience does not)
- [ ] Content still comes only from `Q-xxx.md`, no second copy of the text maintained

## Where we are
The repo now holds only `board.html`; no `deck.html` is in use anywhere.
The one leftover, `subjective-label/diagram/01-sublabel-license-260722/deck.html`, is an old broken build that constructs its DOM with JS at load time and has nothing to do with `/html-ppt` — QB3 cleans it up.

What is still missing are the `/html-ppt` capabilities that are purely JS: arrow-key ← → paging, presenter mode (S), overview grid (O).
All of these require JS. **The "zero-script" premise was already voided over in QA6** — the comment layer introduced a script block.
The replacement rule: scripts may only **enhance**; after stripping every `<script>`, the body must still be complete. This is now an assertion inside `build.py`, checked on every build (measured: ~15k characters of body survive stripping).
So arrow-key paging is now buildable, under the same rule: without JS you click to page, with JS the arrow keys also work.
`/html-ppt`'s `base.css` sets `.slide` to `opacity:0` by default and relies on `runtime.js` to reveal it — that approach must NOT be copied; if a script comes in, it is one hand-written, purely enhancing script.

## Files
- `build.py`
  The focus-mode CSS block (`body:has(.q:target)`) IS the whole "one screen per question" implementation; paging / presenter mode would also land here.
- `ref/board-form.md`
  §8 page: one file, two modes — written there.

## Glossary
progressive enhancement: the page is fully functional without JS and merely nicer with it. The exact opposite of "blank page without JS".

## Discussion
> JL: do we still have both deck.html and board.html? I want to merge them into one.
>> CC0722: merged. Only `board.html` remains — one file, two modes. What is left are just the arrow-key-style capabilities that need JS.

## Log
260724 1242 · Translated to English (JL 260724: everything on the board in English)
260723 · Rewritten to the new structure: Question expanded into "one paragraph + bullets", added `## Boundary` (drawing the line against QA4 / QE1) and `## Files`; the retired `## Why here` merged into Question
260723 0930 · The premise "board.html stays zero-script" voided — QA6's comment layer brought in JS.
              The preserved property is now "body survives stripping every script", asserted inside build.py
260723 0919 · Renumbered Q3 → QA3; state OPEN → PARTIAL
260722 2340 · JL ruled: merge, no second file. Question rewritten
260722 2330 · The draft claimed "VS Code preview inevitably blocks JS". JL challenged it ("that can't be right"); verified wrong —
              the real cause was port 3000 not being forwarded (two Failed-to-connect-tunnel lines in remoteagent.log)
260722 2255 · Opened: should there be a separate deck.html for projection?
