# Attaching a drawing from the page: one button that types the line for you

state: 🟡 PARTIAL · add, replace and remove all ship; the cold read is the one thing left
owner: CC
method: one button in 🖼 Diagram that writes the same line an author would type
session: 652d8901-e381-4f1d-9678-d286261ad6d4
## Opening
How does a reader attach a drawing to a page without opening the markdown by hand?
A drawing here is an Excalidraw canvas: a shared whiteboard a colleague can draw on while you talk.
Attaching it means one line inside the page's `## Diagram` section, plain text anyone could type.
A button writing anything cleverer than that line would make the file depend on the button.
So this page settles one control, the exact line it writes, and everything the write refuses.

**Where this page sits**: `QB4 §2` rules what a `## Diagram` section holds, which is the ascii figure that opens with the section and the canvas that takes one more click.
It says what a good canvas line looks like and never says how that line gets into the file.
This page is that other half: the control, where the line lands, and what the write declines.
`QB5c` owns editing body prose from the page, and `QE4` owns what happens when two people write at the same time.

**What a canvas is, and what it is not**: A canvas is an Excalidraw scene, and this board keeps one scene with one frame per page.
It is where colleagues move boxes around while they are talking.
It never replaces the ascii figure, because the figure is the half that survives being pasted into a chat, an email, or a commit message.

**Why it matters**: A drawing is worth adding during the discussion that needs it, not an hour later.
If adding one means leaving the page, opening an editor, finding `## Diagram`, and typing a URL in the right place, the drawing does not get added at all.
The button takes away every step except the paste.

## Diagram

**The round trip**: how a pasted URL becomes a line in the markdown and comes back as a canvas.

```
🖌 ATTACH A DRAWING · the round trip

  🌐 THE PAGE          🛠 live/xcal.py         📝 THE PAGE'S .md
  ──────────           ──────────────          ─────────────────
  🖼 Diagram    ━━━━▶  POST               ━━▶   ## Diagram
   ▧ ascii             /_board/diagram           ▧ the fenced figure
   ✏️ Excalidraw        ➕ add   🔁 replace        (one blank line)
    🖌 paste a URL      🗑 remove 🕳 create        🔗 the URL line
       ▲                                              │
       └── 🔄 live refresh ◀━━ 🏗 build.py rebuilds ◀──┘

⚖️ the .md stays the only source · the page just types the line for you
🚫 no marker · no metadata · nothing only the button knows how to write
```

/_excalidraw/?board=Tools/plugins/haipipe-toolkit/skills/diagrams/01-boardform-260722/board.excalidraw&frame=QB8

## Content
### 1 · The write path
**Four things one button does**: each action, and the single line of markdown it changes.

```
🖌 ONE CONTROL · four actions · one line of markdown each

  ➕ ADD      no URL in ## Diagram yet   ━━▶ a new line below the fence
  🔁 REPLACE  a URL is already there     ━━▶ that same line, overwritten
  🗑 REMOVE   the URL line + one blank   ━━▶ figure and heading untouched
  🕳 CREATE   the page has no ## Diagram ━━▶ a section before Content

  🖥 built by 50-xcal.js · never by build.py
  📄 strip every script: figure, canvas and fallback link still read
```
📌 One control in 🖼 Diagram adds, replaces, and removes a drawing, and it is there even on a page that has no Diagram section yet.

#### 1.1 · The button lives in the section it changes
(one control, inside 🖼 Diagram, on the page it belongs to)
The control renders inside the ✏️ Excalidraw half of an open Diagram section, reading `🖌 Excalidraw Canvas`.
It is added by `50-xcal.js`, not by the generator, which is the rule every write affordance on this board follows.
Strip the scripts and the figure, the canvas, and the fallback link are all still there to read.
The page it writes to comes from the enclosing slide's `data-file`, so the button cannot address a page other than the one it is sitting in.

#### 1.2 · What lands in the markdown is what an author would have typed
(no new syntax, no marker, nothing that only the button knows how to produce)
`add_diagram` writes the URL on a line of its own inside `## Diagram` and nothing else.
The result is the file a hand edit would have produced, so the markdown stays the single source and `build.py` renders it by the rule that already existed.
A page written by hand and a page written by the button are the same file.
Nothing is kept in the browser: when `serve.py` is not running, the control says so and tells the reader to edit the URL line themselves.

#### 1.3 · Removing a drawing takes out one line and leaves the rest
(deleting a drawing and deleting a section are different acts with different blast radii)
`🗑 Remove` appears whenever the page already has a canvas, and posts `{remove: true}` to the same endpoint.
It deletes the URL line and the one blank line above it, and touches nothing else: the ascii figure, the heading, and the section all stay.
Removing the section itself is still a hand edit, on purpose.

#### 1.4 · A page with no Diagram section still has a way in
(the pages that most needed the button were the ones that had none)
`wireXcal` walks PAGES rather than Diagram sections, so a page without one gets a `🖼 Add a Diagram` control where the section would render, between Opening and Content.
That is the same place the endpoint has always inserted a new `## Diagram`, so the button and the writer agree about the layout instead of each holding its own opinion.
The endpoint never needed changing: it had created the missing section since the day it shipped, and only the way in was absent.

### 2 · The rulings baked into the endpoint
**What the write will not do**: the three refusals, the one thing it skips, and the two warnings.

```
🛡 A WRITE ENDPOINT IS JUDGED BY WHAT IT DECLINES

  🚫 REFUSE  not an Excalidraw link        ━━▶ nothing is written
  🚫 REFUSE  remove, no URL to remove      ━━▶ nothing is written
  🚫 REFUSE  remove, no ## Diagram at all  ━━▶ nothing is written
  🙈 SKIP    a URL inside a code fence     ━━▶ examples stay examples
  ⚠️ WARN    canvas, and no ascii figure   ━━▶ written, and flagged
  ⚠️ WARN    new section, canvas only      ━━▶ written, and flagged

  📍 one canvas per page · a second paste replaces, never stacks
```
📌 The endpoint holds four rulings: one canvas per page, a fixed place for a new section, a short list of writes it refuses, and two writes it allows while saying they are poor.

#### 2.1 · One canvas per page, so a second paste replaces the first
(otherwise a section quietly collects canvases nobody meant to keep)
The renderer embeds every canvas URL it finds, so stacking was the easy behaviour and the wrong one.
A page is one question and its Diagram is one figure, so pasting a new URL is almost always a correction rather than an addition.
The response says `replaced: true` when that happened, so the page can tell the difference.

#### 2.2 · A missing Diagram section is created in its fixed place
(before Content, because the on-stage order is not negotiable)
The page grammar puts Diagram after Opening and before Content, so the endpoint inserts the new section immediately before `## Content`, or before `## Aims` when a page has no Content.
It does not append at the end, which would produce a section that renders in the wrong place and reads as though the layout rules did not apply to it.

#### 2.3 · What the endpoint refuses outright
(three writes it declines, each leaving the file exactly as it was)
A URL that is neither an `excalidraw.com` link nor this board's own Excalidraw host is refused, and nothing is written.
A removal is refused when the Diagram holds no canvas, and again when the page has no `## Diagram` at all.
The board's own host is not guessable, so `board.md` declares it once on its `excalidraw:` line and the endpoint accepts anything under it.
Without that line the control could not take the very URL this board tells every page to use.

#### 2.4 · What it skips, and what it warns about
(a warning is how the endpoint says yes and still tells the truth)
The scan for `## Diagram` skips fenced code blocks, because pages carry example markdown inside fences and a plain search writes into the example.
The comment layer hit that exact trap on 260723, and it is now avoided by construction.
Two writes succeed and return a warning for the same reason: a canvas added to a section with no ascii figure, and a new section created holding only a canvas.
`QB4 §2` rules that the ascii figure is the half that survives being copied, so a silent success would let the page teach the opposite.

### 3 · What this page does not do
**Where the rest lives**: every gap names the page or the ruling that owns it.

```
🕳 NOT HERE · and never left without an owner

  ✍️ who attached it        ━━▶ ⚖️ ruled NO, 260726 · see ## Law
  👥 two people at once     ━━▶ 📄 QE4, the same gap for body text
  🖼 what a canvas may be   ━━▶ 📄 QB4 §2.7 · one scene, one frame
  📜 the embed line itself  ━━▶ 📄 ref/board-form.md §5
  🔍 can a reader find it?  ━━▶ 📍 P1, waiting on a cold read
```
📌 Four things a reader might expect here are owned elsewhere, and the fifth is still open on this page.

Nothing records who attached a drawing, and that is a ruling rather than a gap: `## Law` carries it with the reason.
Two people attaching at once is unhandled, which is the same gap `QE4` owns for body text.
What a canvas URL may be, and the rule that a canvas never replaces the ascii figure, belong to `QB4 §2.7`.
The embed line as a piece of board grammar is `ref/board-form.md §5`.
Whether a reader who was never told about the button can find it is still open here, because the control sits two clicks deep.

## Aims
### A1 · 🖌 The write path
- A1.1 · A drawing can be attached, replaced, and removed from the page, with no editor.
  **Done when:** add, replace, and remove run in that order on a real page and leave the file byte-identical to where it started.
- A1.2 · Every page has a way in, whether or not it already carries a `## Diagram` section.
  **Done when:** a page with no Diagram section shows the control in the place the section would render.

### A2 · 🛡 The rulings baked into the endpoint
- A2.1 · The endpoint refuses every write it cannot make safely, and says why.
  **Done when:** a non-Excalidraw URL, a removal with nothing to remove, and a removal on a page with no section each fail with nothing written.
- A2.2 · A written line never lands inside a fenced example.
  **Done when:** the section scan skips code fences, checked against a page whose Content shows markdown inside a fence.

### A3 · 🕳 What this page does not do
- A3.1 · Everything this page declines to build names the page or the ruling that owns it.
  **Done when:** each declined item on the page points at an owning page id or at a dated ruling in `## Law`.

### P · 🏁 Page-level
- P1 · A reader who was never told about the button finds it and uses it.
  **Done when:** a cold read reports that a fresh agent found the control, or reports that it did not.
- P2 · This page's own 🖼 Diagram carries a canvas that opens.
  **Done when:** `board.excalidraw` holds a frame named `QB8` and the ✏️ Excalidraw row shows it.

## States
### A1 · 🖌 The write path
- ✅ A1.1 · Verified 260726 on a fixture: add, then replace, then remove returned the file BYTE-IDENTICAL to the original, and a second remove refused with "this Diagram has no excalidraw to remove".
- ✅ A1.2 · `wireXcal` walks pages rather than Diagram sections, so a page without one gets a `🖼 Add a Diagram` control between Opening and Content, which is where the endpoint has always inserted the section.

### A2 · 🛡 The rulings baked into the endpoint
- ✅ A2.1 · All three refusals hold in `add_diagram`, and each returns its own message rather than a shared failure.
- ✅ A2.2 · The `## Diagram` scan toggles on every code-fence line and skips what is inside, so a markdown example in Content is never written into.

### A3 · 🕳 What this page does not do
- ✅ A3.1 · Four declined items, four owners: the ruling in `## Law`, `QE4`, `QB4 §2.7`, and `ref/board-form.md §5`.

### P · 🏁 Page-level
- ⬜ P1 · Not started. The control sits inside the ✏️ Excalidraw row, which is two clicks below the page, so being findable is the open question and no fresh agent has been asked yet.
- 🧠 P2 · Waiting on a drawing. The URL line was repointed from `frame=QD5` to `frame=QB8` on 260802, since QD5 is a different page today; `board.excalidraw` carries no `QB8` frame yet, so the row stays empty until someone draws one.

The write path ships in both directions, and its code is committed in the `Tools` submodule.
What is left needs a fresh reader and a drawing, not more code.

## Files
### ⚙️ Engines · what RUNS this subject
- `live/xcal.py`
  `add_diagram`, where every refusal and every placement rule lives, plus `serve_frame`, which cuts this page's frame out of the board's one scene.
- `cli/serve.py`
  Where `/_board/diagram` is routed to `add_diagram`. No rule about the write lives here.
- `assets/js/10-drawer/10-comment/50-xcal.js`
  `wireXcal`, the control itself. `rewire()` in `50-structure.js` calls it, so the button survives a live refresh.
- `assets/css/10-focus.css`
  `.xadd` and `.xadd-row`. The dashed outline, so the control reads as an affordance rather than as content.
- `assets/css/60-chips.css`
  The buttons inside that row, including `✨ Create one for me` and `🗑 Remove`.
- `src/body.py`
  The renderer that turns the written line into an embedded canvas plus its fallback link. Open it to see what the line becomes; this page changes nothing in it.

### 📋 Contracts · what CARRIES a rule to other pages
- `ref/board-form.md`
  §5, the body-syntax table: an Excalidraw link alone on a line is a canvas. That row is the format this endpoint writes to.

### 📤 Output files · what a BUILD writes
- `board/QB/QB8-diagramattach.html`
  ⚠️ Generated by `cli/build.py`. Never hand-edit.

## Law
- 260726 CC · 📝 **What lands in the markdown is what an author would have typed**
  The endpoint writes a bare URL on a line of its own inside `## Diagram`, and never anything else.
  No marker, no metadata, and no field that only the button knows how to produce. This is what keeps the markdown the single source: a page written by hand and a page written by the button are the same file, `build.py` renders both by the rule that already existed, and a board built by an older copy of the skill still shows every canvas. Every other ruling on this page follows from it.
- 260726 CC · ✍️ **A drawing carries no signature**
  An attached drawing does not record who attached it, unlike a comment or a discussion line, which carry initials.
  A signature is a thing no author types beside a URL, so adding one would invent syntax that only the button knows how to produce, which is exactly the property the ruling above protects. Attribution is not lost: the boards are in git, so `git log -S<url>` names who added a drawing and when, with no new format to maintain.

## Glossary
- 🎛 **affordance**: a control the page offers, added by script, that writes into the markdown rather than into the browser.
- 🖼 **canvas**: the Excalidraw half of a `## Diagram` section, where colleagues draw together. This board keeps one scene with one frame per page.
- ▧ **ascii figure**: the fenced text drawing in `## Diagram`. It is the half that survives being pasted into a chat, an email, or a commit message, so a canvas never replaces it.
- 🏷 **`data-file`**: the attribute each rendered page carries naming its own source `.md`, which is how a control knows what it may write to.

## Discussion
> JL: what I mean is here, I want to add the excalidraw myself.
>> CC0726: built as a button inside 🖼 Diagram. The line it writes is the same line a hand-edit would produce, so nothing about the format depends on the button existing.

## Log
260802 · Brought to the page contract. `## Boundary` deleted on JL's 260731 ruling and its "covered elsewhere" list moved into `### 3`, where the prose that needs those pointers lives. The Opening's blank line was in the wrong place, so the four sentences explaining the question were hidden in More details while the page showed a bare question; rewritten to the on-stage paragraph plus labelled drawer parts. `## Items to Finish` and `## Where we are` became `## Aims` and `## States` with ids, and the three dated records under Where we are moved down here unchanged. Content is numbered all the way down and every division opens with a captioned figure. Four stale statements fixed: the control reads `🖌 Excalidraw Canvas`, not `🖌 Add an excalidraw`; the endpoint also accepts this board's own Excalidraw host, declared on `board.md`'s `excalidraw:` line; the no-Content anchor is `## Aims`, not `## Items to Finish`; and `### 3` still said removal and the no-section entry point were not built, five lines under the ticked items that built them. Files repointed to `live/xcal.py` and `assets/js/10-drawer/10-comment/50-xcal.js` after the live-layer and asset splits moved both, and the Diagram URL repointed from `frame=QD5` to `frame=QB8`, since QD5 is a different page since 260801
260801 · Relocated QD → QB (id QD5 → QB8), beside QB4b: this is the hand-attach write-half of the ## Diagram section that QB4b specs, not a chat concern (JL); the QD7 merge here was reverted and QD7 restored to QD
- 260726 CC · 🔁 The control became reversible, and reachable everywhere
  Removal closes the gap that sent a wrong paste back to the editor this button exists to avoid, and it is a line-level edit: the section and the ascii figure are never touched.
  The missing-section case turned out to need no endpoint work at all, only an entry point, because the writer had handled it since day one and the button was generated inside the very section it needed to create.
  The signature item closed as a ruling rather than a build: a drawing carries no initials because the md line must stay indistinguishable from a hand-edit, and git already answers who added it.
- 260726 CC · 🐛 `✨ Create one for me` had never worked
  It read `face.dataset.file`, and `face` is not defined anywhere in `board.js`; the ReferenceError was swallowed by the surrounding `try`, so the button reported "serve.py is not running" no matter what was running.
  The wrong error is what hid it: a control that lies about why it failed is worse than one that visibly breaks, because the reported cause sends the reader to check a server that was fine.
  Found by reading the function while moving the control, not by using it.
- 260726 CC · 🖌 The Diagram section became writable from the page
  Diagram was the last body section that could only be read, while comments, discussion, sentence apparatus, checkboxes, and structure all wrote back.
  JL asked for the button after the Diagram-source rewrite (now `QAa2 §0`) documented the syntax: knowing the line to type is not the same as being able to add the drawing.
  The endpoint is 60 lines in `serve.py`, the control is 50 in `board.js`, and the generator was not touched, so a board built by an older copy of the skill still renders every excalidraw.
260731 · Items, Where we are, and Files regrouped to the QB4d/QB4e/QB4f subsection conventions (matrix retrofit)
260726 2300 · 🗑 removal + 🕳 an entry point on every page (JL asked for QD5): `add_diagram` takes `{remove:true}` and deletes the URL line plus its blank line, refusing when there is nothing to remove or no section; `wireXcal` walks pages instead of sections and drops a `🖼 Add a Diagram` control between Opening and Content when there is no section; the signature item ruled NO because a signature is syntax no author types; fixed `face.dataset.file`, an undefined variable that made `✨ Create one for me` report the wrong error since it shipped; add/replace/remove round trip verified byte-identical
260726 1210 · opened and built: `/_board/diagram` endpoint, `wireXcal` control, `.xadd` styles; four cases verified on a throwaway board; removal, signature, and the no-section case left open
