# The look

Part of hai-studio's topic contract (`ref/topic-contract.md`). This file is what `canvas.py` enforces when a
builder writes. How a drawing should read is `hai-draw`'s (load `/hai-draw` before drawing); where
the two differ, follow `hai-draw`.

## Two looks

1. **The five-part drawing, the default**: `five_parts.py` draws in colour: icons, coloured data tables, red question
   stickies, orange leanings. It writes through `five_parts.marks_writer` (`canvas.write` with `palette=False`), so
   its colours stay and a person's marks are kept.
2. **The black look**: for a `draw.py` drawing, a special shape (a screen, a report, a slide draft) and an older
   topic. The rest of this file is the black look.

## Black, red, green

```text
black  #1e1e1e   every line, box, tree, arrow and word              canvas.INK
red    #e03131   an uncertain or open question (? …)                 canvas.RED
green  #2f9e44   a change we made, where we made it (✎ <date> …)    canvas.GREEN
```

1. **Shapes**: trees, lines, boxes and text; boxes unfilled.
2. **No other colours**: no blue, teal or gray accents, no sticky fills, no coloured panels. The slight key-point
   colour `canvas.KEY` is kept. Inside a slide of a slide draft, colours stay as drawn.
3. **Enforced**: `canvas.write` turns any other stroke black and drops fills in what a builder draws; images and the
   person's own marks are untouched. `canvas.off_palette(els)` lists what is off it.
4. **Not here**: a report drawing's plots and embedded figures follow `hai-draw report`.
5. **A screen in colour**: a frame that draws the workbench's screen wears the workbench's own light colours. Mark it
   `canvas.ui_frame(frame)`; `canvas.write` colours it from `canvas.UI`. Red questions and green notes in it keep
   their colour.

## One readable font

Every word in Nunito (`fontFamily` 6, `canvas.FONT`); paths and code may use Cascadia (3, `canvas.CODE_FONT`). No
hand-drawn font. `canvas.write` sets it on what a builder writes; the person's own marks and a slide draft keep
theirs.

## Frames

1. **In rows, never one long column**: `canvas.grid(els, [[...], [...]])`, read left to right and then down, two to
   four a row; each frame moves with what is drawn in it. `canvas.write` warns when 4 or more frames stand in one
   column.
2. **Stairs when one frame is the main one**: the main frame first, at the origin, each later frame lower and further
   right: `canvas.stairs(els, [main, (id, dx), …])`. A small frame that explains the main one is marked
   `canvas.explains(frame)`, so `check.py` does not hold it to a screen's size.
3. **One idea, one dense frame**: an idea is one connected flow, dense with facts, its most important part the
   largest. A separate frame is for separate material (a source marked up, a reference picture), never for one more
   step of the same idea.
4. **A tree**: `canvas.tree(x, y, nodes, width, frame, cols=N)`. A leaf starting "❓" or "? " draws red, "✎ " green.
   Use ❓ only for what is open.

## Each frame fits the screen

1. **At 50% zoom** the whole frame is on screen and its words still read.
2. **At 100% zoom** most of the frame is on screen, not one box of it.
3. **In numbers**: about 2560 x 1440 px; at most 2800 x 1600 (`canvas.FRAME_MAX`). Body words 20 px or more
   (`canvas.TEXT_MIN`); box titles about 23, the frame's title about 34.
4. **Room comes from words**: boxes sized to their words, short gaps, fewer words. Never a bigger canvas and never
   smaller type.
5. **One long piece, one frame**: a piece read top to bottom (a section written out, a draft's pages marked up) is
   one frame that grows down, its width within the screen; never cut into frames "· 1", "· 2". Mark it
   `canvas.reads_down(frame)`.
6. **Side notes smaller**: notes beside the main content are written smaller than it; `canvas.aside(e)` keeps them
   out of the small-text check.
7. **Checked on write**: `canvas.oversized(els)` (frames over the size), `canvas.small_text(els)` (frames whose words
   are mostly under 20 px), `canvas.numbered_frames(els)` (one piece cut into numbered frames). `canvas.write` warns
   about each.

## Change notes

Every change to a drawing, asked for or found on a redraw, gets a short green note right where it changed.

```text
✎ 261007 Delivery decided: stays in each level skill      (green, beside the changed box)
```

1. **Where**: beside the thing that changed, inside its frame. Never a list of changes above the title or in a
   corner; all the changes in one place is the face's Decided list.
2. **Short**: `✎ <YYMMDD> <what changed>`, one line, a few words; who asked goes in the face.
3. **Not for a whole new topic, frame or rename**: that goes in the face.
4. **How**: `canvas.change_note(x, y, what, date, frame)` returns the green text element.
5. **Kept**: old notes stay; a note is removed only when its thing is removed.
