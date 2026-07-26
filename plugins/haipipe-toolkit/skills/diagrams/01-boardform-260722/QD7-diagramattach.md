# Attaching a drawing from the page

state: 🟡 PARTIAL
owner: CC
method: one button in 🖼 Diagram that writes the same line an author would type

## Question
When an ASCII figure is not enough and the shape is worth drawing on together, how does the drawing get attached to a page without leaving the page to hand-edit the markdown?

The board already accepts an excalidraw: a share URL alone on a line inside `## Diagram` renders as an interactive excalidraw with a fallback link, and `QA4 §2` rules how that behaves and why the ASCII figure and the plain link both stay.
What was missing is the way in.
Attaching a drawing meant opening the page's `.md`, finding the Diagram section, and knowing that the URL has to sit on a line by itself, which is three pieces of knowledge that a reader looking at the rendered page does not have and should not need.
That gap matters more here than for prose, because a drawing is the thing people reach for in the middle of a discussion, and a mechanism that requires leaving the discussion to use a text editor gets used once and then abandoned.
Every other write on this board already comes back to the page: comments, discussion, sentence apparatus, checkbox state, structure.
Diagram was the one section that could only be read.

## Boundary
- ✅ Covered here
  **Getting an excalidraw onto a page from the page**: the control, where the URL lands in the source, what happens when the section is missing, and what the endpoint refuses.
- ↪ Covered elsewhere
  How the excalidraw renders, why the ASCII figure stays, and why the fallback link is not redundant: that is `QA4 §2`.
  The embed syntax itself, as a line of board grammar: `ref/board-form.md §5`.
  Whether the body prose is editable in the page, and what two people editing at once does: that is `QE4`.
  The chat drawer and the terminal: `QD2` and `QD3`.

## Diagram

```
  browser                       serve.py                        build.py
  ───────                       ────────                        ────────
  🖼 Diagram
   ┌ ascii figure ┐   POST      writes ONE line into ## Diagram
   │ 🖌 Add …     │ /_board/    ───────────────────────────────►  ## Diagram
   │  [paste URL] │  diagram    ① section exists  → append/replace  ```ascii```
   │  Save        │ ──────────► ② no section      → create it              (blank)
   └──────────────┘             ③ not excalidraw  → refuse, nothing written  URL
          ▲                                                          │
          └──────── live refresh swaps div.wrap ◄── rebuilt board.html ┘

  the md is still the only source; the page just types the line for you
```

http://127.0.0.1:5599/_excalidraw/?board=Tools/plugins/haipipe-toolkit/skills/diagrams/01-boardform-260722/fig/board.excalidraw&frame=QD7

## Content
### 1 · The write path
#### The button lives in the section it changes
(one control, inside 🖼 Diagram, on the page it belongs to)
The control renders at the bottom of an open Diagram section, reading `🖌 Add an excalidraw`, or `🖌 Replace the excalidraw` when the page already has one.
It is added by `board.js`, not by the generator, which is the same rule every write affordance on this board follows: strip the scripts and the figure, the excalidraw, and the fallback link are all still there to read.
The page it writes to comes from the enclosing slide's `data-file`, so the button cannot address a page other than the one it is sitting in.

#### What lands in the markdown is what an author would have typed
(no new syntax, no marker, nothing that only the button knows how to produce)
`serve.py` writes the URL on a line of its own inside `## Diagram` and nothing else.
The result is indistinguishable from a hand-edit, so the md stays the single source, `build.py` renders it by the rule that already existed, and a page that was written by hand and a page that was written by the button are the same file.
Nothing is stored in the browser: if `serve.py` is not running the control says so and tells the reader the line to paste.

### 2 · The rulings baked into the endpoint
#### One excalidraw per page, so a second paste replaces the first
(otherwise a section quietly accumulates iframes nobody meant to keep)
The renderer will embed every matching line, so stacking was the easy behaviour and the wrong one.
A page is one question and its Diagram is one figure; pasting a new URL is almost always a correction, not an addition.
The response says `replaced: true` when that happened, so the page can tell the difference.

#### A missing Diagram section is created in its fixed place
(before Content, because the on-stage order is not negotiable)
The page grammar puts Diagram after Opening and before Content, so the endpoint inserts the new section immediately before `## Content`, or before `## Items to Finish` when a page has no Content.
It does not append at the end, which would produce a section that renders in the wrong place and reads as though the layout rules did not apply to it.

#### The refusals are the part worth trusting
(a write endpoint is judged by what it declines to write)
A URL that is not `excalidraw.com` or `app.excalidraw.com` is refused outright and nothing is written.
The scan for `## Diagram` skips fenced code blocks, because `QA4` carries example markdown inside fences and a naive search writes into the example: that exact trap was hit by the comment layer on 260723 and is now avoided by construction.
Creating a section that holds only an excalidraw succeeds but returns a warning, since `QA4 §2` rules that the ASCII figure is the half that survives being copied, and a silent success would let the page teach the opposite.

### 3 · What is deliberately not built
Removing an excalidraw from the page is not possible; that still means editing the md.
A page with no Diagram section shows no button at all, because the section is only generated when the markdown has one, so the very case that most needs the button is the one that lacks it.
Nothing records who attached a drawing, unlike comments and discussion, which carry initials.
Two people attaching at once is unhandled, the same gap `QE4` owns for body text.

## Items to Finish
- [x] 🖌 An excalidraw can be attached from the page
      The control exists in 🖼 Diagram, posts to `/_board/diagram`, and the excalidraw is on the page after the live refresh.
      Verified 260726 on a throwaway board: a URL added to a page that already had an ASCII figure landed on its own line below the fence, with a blank line before it, exactly as an author would have written it.
- [x] 🔁 A second paste replaces rather than stacks
      Verified on the same board: the second URL overwrote the first in place and the response carried `replaced: true`, leaving one excalidraw in the section.
- [x] 🛡 The endpoint refuses what it should
      A non-Excalidraw URL was rejected with nothing written, and the section scan skips fenced examples.
      The missing-section case created `## Diagram` immediately before `## Content` and returned the warning about the absent ASCII figure.
- [ ] 🗑 An excalidraw can be removed from the page
      Attaching is reversible only by hand today, which makes a wrong paste a reason to open the editor after all.
      This closes when the control can clear the URL as well as set it.
- [ ] 🕳 A page with no Diagram section can still get one
      The button is generated inside the Diagram section, so exactly the pages that have no figure have no way to add one.
      This closes when the entry point exists somewhere that is present on every page.
- [ ] ✍️ An attached drawing records who attached it
      Comments and discussion carry initials and this does not, so an excalidraw appears with no author.
      This closes when the write carries a signature or a ruling says a drawing does not need one.
- [ ] 🧪 A fresh agent finds and uses the control without being told
      The button is discoverable only if a reader opens the Diagram section, which is collapsed by default.
      This closes when a cold read confirms it, or reports that it does not.

## Where we are
Built and working, verified against a throwaway board covering four cases: a good URL, a replacement, a refused URL, and a page with no Diagram section.
Three items are ticked and four are open, and the open ones are all about the edges rather than the main path.
The code is uncommitted in the `Tools` submodule, alongside the `--host` flag from `QE6`.

- 260726 CC · 🖌 The Diagram section became writable from the page
  Diagram was the last body section that could only be read, while comments, discussion, sentence apparatus, checkboxes, and structure all wrote back.
  JL asked for the button after the `QA4 §2` rewrite documented the syntax: knowing the line to type is not the same as being able to add the drawing.
  The endpoint is 60 lines in `serve.py`, the control is 50 in `board.js`, and the generator was not touched, so a board built by an older copy of the skill still renders every excalidraw.

## Files
- `serve.py`
  `add_diagram` and the `/_board/diagram` route. All the refusals and the placement rules live here.
- `haipipe-board/assets/board.js`
  `wireXcal`, called from `rewire()` so the control survives a live refresh.
- `haipipe-board/assets/board.css`
  `.xadd` and its row. Dashed outline, so it reads as an affordance rather than as content.
- `src/body.py`
  The renderer that turns the written line into an excalidraw plus its fallback link. Not modified by this question.

## Glossary
affordance: a control the page offers, added by script, that writes into the markdown rather than into the browser.
`data-file`: the attribute each rendered page carries naming its own source `.md`, which is how a control knows what it may write to.

## Discussion
> JL: what I mean is here, I want to add the excalidraw myself.
>> CC0726: built as a button inside 🖼 Diagram. The line it writes is the same line a hand-edit would produce, so nothing about the format depends on the button existing.

## Log
260726 1210 · opened and built: `/_board/diagram` endpoint, `wireXcal` control, `.xadd` styles; four cases verified on a throwaway board; removal, signature, and the no-section case left open
