# The look

Part of haipipe-studio's topic contract (`ref/topic-contract.md`).


The five-part drawing (the default, `five_parts.py`, JL 261112) draws in colour, its icons, coloured tables and
stickies its own (`five_parts.marks_writer`, `palette=False`). The black look below is for a draw.py drawing, a
special shape and a topic drawn before 261112 (SKILL.md § The look).
Trees, lines and boxes in black; red only for an uncertain or open question; green only for a change
we made, where we made it (JL 261007). No other colour and no fills: `canvas.INK`, `canvas.RED`,
`canvas.GREEN`. `canvas.write` enforces it on what the builder draws (`apply_palette`: any other
stroke becomes black, a fill transparent; images, transparent strokes and the person's own marks
are left alone; a slide draft s61-s69 is left as drawn, or pass `palette=`), and
`canvas.off_palette(els)` lists anything off it. A scratch's sticky
colours and a design scratch's coloured panels are not used in a studio topic; a report drawing's
plots and figures are `excalidraw-report`'s. One exception, inside a slide of a slide draft (`ref/slide-draft-topic.md`).

One font, for reading (JL 261009): every word in Nunito (`fontFamily` 6, `canvas.FONT`), paths and code
in Cascadia (3, `canvas.CODE_FONT`); `canvas.write` sets it on what a builder writes (`apply_font`), and a
change note is written in it. Hand-drawn Virgil (1) and Excalifont (5) and Comic Shanns (8) are not used.

Frames in rows, never one long column (JL 261009: "don't put all the things in one column"). A builder
draws each frame where it likes, then calls `canvas.grid(els, rows, gap=150)` once before `write`: `rows`
lists every frame id once, row by row, read left to right and then down, two to four frames a row, and
each frame moves with everything drawn in it. `canvas.one_column(els)` is true when 4 or more frames share
one column, and `canvas.write` prints a warning then. Keep a frame's number out of its name when the number
can change (a frame's id comes from its name).

One idea, one large frame (JL 261010, on a topic split into 12 frames: "你这么多 frame，其实只相当于我的一个
frame。你要把它的体量做大"). The idea is one big connected flow in one frame, with many facts in it and its most
important part drawn largest; more frames are for separate material beside it (a source document marked up,
reference figures). Many small frames that each hold a few points are the wrong shape. Large means much
information, not a large canvas: each frame fits the screen (JL 261010, on a 9,200 px idea frame: "This is too huge, what I want is: when I zoom in 50% I can read the whole workflow, when I read 100%, I can see most part of the frame").
At 50% zoom the whole frame is on screen and its words read; at 100% most of it is. So a frame is about
2560 x 1440 px (the workbench's 1280 x 720 pane at 50%), at most 2800 x 1600 (`canvas.FRAME_MAX`), body words
20 px or more (`canvas.TEXT_MIN`); room comes from boxes sized to their words and fewer words, never a bigger
canvas or smaller type (scaling a drawing down shrinks its words below reading). One piece read top to bottom
(a section written out, a draft's pages marked up) stays one frame that grows down, its width within the
screen, and is never cut into frames "· 1", "· 2" (JL 261010: "the draft take should be one single frame, and
the Written out should be one large frame"); the builder marks it `canvas.reads_down(frame)`, and its height
is not checked. `canvas.oversized(els)` lists the frames over the size,
`canvas.small_text(els)` the frames whose words are mostly under 20 px, `canvas.numbered_frames(els)` one piece
cut into frames "· 1", "· 2", and `canvas.write` warns about each. Notes beside the main content (the page
pictures they explain) are smaller than it, marked `canvas.aside(e)`, and not counted (JL 261011).
