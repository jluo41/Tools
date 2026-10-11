---
name: haipipe-studio
description: >-
  Owns the Idea Studio at any level (Block, Job, Task): a studio topic `studio/sNN-<topic>/`
  with its face (Topic · Feeds · Files · Decided · Open), its drawings, and its builder
  `build_*.py` that redraws from disk while keeping every mark a person drew (canvas.write,
  a seed snapshot beside the drawing); the numbering (s0x concepts · s1x levels · s2x runs and
  skills · s3x Guide · s5x server · s6x slide drafts, a proposed deck drawn from one slides.py);
  sessions as passes of the topic's soft Run
  `run-draw-<sNN>`; and the scripts canvas.py, render_png.py and new_topic.py. Use to add,
  redraw or number a studio topic, write a builder, preview a drawing, or save a session.
  Trigger: studio, studio topic, Idea Studio, add a topic, redraw, save this session, sNN,
  build_*.py, canvas.write, render_png, seed snapshot, proposal topic, draft marked up,
  section written out, /haipipe-studio.
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "0.8.0"
  last_updated: "2026-10-10"
  # version history: ./CHANGELOG.md
---

# /haipipe-studio · the topics a level thinks on

Every level has an Idea Studio: its `studio/` folder, one topic per `sNN-<topic>/`, each a
drawing to think on together and a short face that says what it settles and which
Questions it feeds. This skill owns the folder, the face, the numbering, the builders that
keep a person's marks, and the sessions. How a drawing should look is `excalidraw-report`'s.

```text
<level>/studio/sNN-<topic>/
├── sNN-<topic>.md            Topic · Feeds · Files · Decided · Open
├── sNN-<topic>.excalidraw    the drawing (a builder's, with the person's marks kept)
├── sNN-<topic>.png           its preview
└── build_sNN_<topic>.py      the builder, when a script draws it
<level>/runs/run-draw-<sNN>/  one pass per working session
```

Read `ref/topic-contract.md` before adding a topic or writing a builder.


Numbering
---------

```text
s01-s09 concepts · s11-s19 levels · s21-s29 runs and skills · s31-s39 Guide · s51-s59 server
s61-s69 slide drafts: a proposed deck, its logic flow and its slides, before the deck is built
```

The next free number in the band; a number is never reused.


Add, redraw, save
-----------------

```bash
S=Tools/plugins/haipipe-toolkit/skills/1_base/project/haipipe-studio/scripts
python $S/new_topic.py topic <level> --slug <topic> --title '<title>' --band run [--feeds q01_x] [--builder]
python <level>/studio/sNN-<topic>/build_sNN_<topic>.py          # redraw: the person's marks are kept
python $S/render_png.py <drawing>.excalidraw <drawing>.png        # the preview
python $S/new_topic.py session <level> sNN --title '<session>' [--ask …] [--summary …] [--changed …]
```

1. **Face marks**: `**Topic:**`, `**Feeds:** qNN_<topic>`, `sNN-DNN` decisions, a numbered Open list.
2. **Builder**: draws through `canvas.write`; never hand-edit its output, change the builder.
3. **Marks kept**: what a person adds, edits or deletes survives a rebuild (the seed snapshot).
4. **Session**: a pass of `run-draw-<sNN>`, written by `haipipe-run`'s `soft_run.py`.
5. **Changes**: red for open; every change to a drawing gets a short green note where it changed.


The look
--------

A studio drawing is a tree, lines and boxes, in black (JL 261007: "I just want the tree and lines with
box with no much colors, just the color of black, with red for uncertainty questions, and green for
our previous changes"):

```text
black  #1e1e1e   every line, box, tree, arrow and word              canvas.INK
red    #e03131   an uncertain or open question (? …)                 canvas.RED
green  #2f9e44   a change we made, where we made it (✎ <date> …)    canvas.GREEN
```

1. **Shapes**: trees, lines, boxes and text; boxes unfilled.
2. **No other colours**: no blue, teal or gray accents, no sticky fills, no coloured panels; the
   one exception is inside a slide of a slide draft (below).
3. **Enforced**: `canvas.write` turns any other stroke black and drops fills in what a builder draws
   (images and the person's own marks untouched; a slide draft s61-s69 is left as drawn).
   `canvas.off_palette(els)` lists them first, if a builder wants to see.
4. **Not here**: a report drawing's plots and embedded figures follow `excalidraw-report`'s report mode.

One readable font (JL 261009: "I think the font should be more readable"): every word in Nunito,
Excalidraw's "Normal" font (`fontFamily` 6, `canvas.FONT`); paths and code may use Cascadia (3,
`canvas.CODE_FONT`). No hand-drawn Virgil (1) or Excalifont (5), no Comic Shanns (8). `canvas.write`
sets it on what a builder writes (`apply_font`), a change note included; the person's own marks and a
slide draft keep their fonts.

Frames in rows, never one long column (JL 261009: "don't put all the things in one column"): a builder
places its frames with `canvas.grid(els, [[...], [...]])`, read left to right and then down, two to four a
row; each frame moves with what is drawn in it. `canvas.write` warns when 4 or more frames stand in one
column.
One idea, one dense frame (JL 261010: "既然是 idea，你搞那么多 frame 干嘛呀？... 一个 frame 的信息量是非常大的"):
a topic's idea is drawn as one connected flow, dense with facts, its most important part the largest;
a separate frame is for separate material (a source marked up, a reference picture), never for one more
step of the same idea. Large means much information, not a large canvas (next rule).
Each frame fits the screen (JL 261010, on a 9,200 px idea frame: "This is too huge, what I want is: when I zoom in 50% I can read the whole workflow, when I read 100%, I can see most part of the frame"):

1. **50% zoom**: the whole frame is on screen and its words still read.
2. **100% zoom**: most of the frame is on screen, not one box of it.
3. **In numbers**: about 2560 x 1440 px, the workbench's 1280 x 720 pane at 50% zoom; at most
   2800 x 1600 (`canvas.FRAME_MAX`). Body words 20 px or more (`canvas.TEXT_MIN`), so 10 px on screen at
   50%; box titles about 23, the frame's title about 34.
4. **Room from words**: boxes sized to their words, short gaps, fewer words; never a bigger canvas, and
   never smaller type (scaling a whole drawing down shrinks its words below reading).
5. **One long piece, one frame**: a piece read top to bottom (a section written out, a draft's pages
   marked up) is never cut into frames "· 1", "· 2"; it is one frame that grows down, its width still
   within the screen (JL 261010: "the draft take should be one single frame, and the Written out should
   be one large frame"). The builder marks it `canvas.reads_down(frame)`.
6. **Checked**: `canvas.oversized(els)` lists the frames over the size (a `reads_down` frame by its width
   only), `canvas.small_text(els)` the frames whose words are mostly under 20 px (green notes not
   counted), and `canvas.numbered_frames(els)` one piece cut into "· 1", "· 2"; `canvas.write` warns
   about each.


Change notes
------------

Every change to a drawing, asked for or found on a redraw, gets a short green note right where it
changed (JL 261007: "when I change the draw, you can leave the short green comments to where we
changed"):

```text
✎ 261007 Delivery decided: stays in each level skill      (green, beside the changed box)
```

1. **Where**: beside the thing that changed, inside its frame, never in a separate legend only.
2. **Short**: `✎ <YYMMDD> <what changed>`, one line, a few words; who asked goes in the face.
3. **Also listed**: the same line in the drawing's title frame, so all changes read in one place. A
   slide draft is the exception: a note about one slide sits only under that slide (`excalidraw-slide`).
4. **How**: `canvas.change_note(x, y, what, date, frame)` returns the green text element.
5. **Kept**: old notes stay; a note is removed only when its thing is removed.

The face's Decided list records the decision; the green note shows where the drawing changed.


A proposal topic
----------------

A topic that works on one section of a proposal or a paper copies b03_event_cgm's s03 (SHIFT Task 2.1;
JL 261010: "I think this one is very very great!"): five frames in two rows.

```text
row 1   ① idea workflow     ② why and the plan     ③ proposal figure       each one screen
row 2   ④ draft today, marked up      ⑤ section written out              each one frame, read down
```

1. **① Idea**: one connected flow, loops drawn closed, checks beside it, open questions red in place.
2. **④ Draft**: read only; passages cut from their pages, red box, arrow to Change, Why, Ask.
3. **⑤ Written out**: paragraph, point, Text, Evidence; tight rows; cards free, joined by lines.
4. **Words in the face**: yaml blocks the builder reads; a draft passage is found by its anchors.
5. **Who answers**: every red ask names a person; ④ and ⑤ close listing them.

The frames one by one, the rules of ⑤, what went wrong on the way and the builders to copy from:
`ref/topic-contract.md` § A proposal topic.


Slide drafts
------------

A topic numbered s61-s69 proposes a deck before it is built: one `slides.py` that its drawing and
its deck both read, the deck generated into the topic's own `delivery/`. This skill keeps its number
band, its folder and face, its sessions, and leaves its colours as drawn (`canvas.is_slide_draft`).
How it is drawn (the frames, the slide skeleton, the accent, `slides.py`'s fields, the deck writer)
is `excalidraw-slide`'s (moved there 261007).


The buttons it owns
-------------------

One button, named by its Run, `run-draw-<sNN>` (haipipe-run rule 6): a new topic is a new Run,
the rest are its passes.

| What it does | Run | how |
|---|---|---|
| add a topic | `run-draw-<sNN>`, new | `new_topic.py topic` |
| redraw a topic | a pass of `run-draw-<sNN>` | rerun its builder, then the preview |
| save this session | a pass of `run-draw-<sNN>` | `new_topic.py session` |

At every level, in the Idea Studio Space.


Moved here
----------

`canvas.py` and `render_png.py` were in a design Block's `studio/_build/` and every theme's
design Block imported them from there; they now live in `scripts/` (b03 s21, 261007). Every
builder imports them from here; the old copies are retired. A builder adds this skill's
`scripts/` to `sys.path` just before `import canvas`.


Boundary
--------

| Owner | Owns |
|---|---|
| `haipipe-studio` | the topic folder, its face, numbering, builders and their writer, previews, sessions |
| `excalidraw-report` | how a drawing looks: scratch and report modes, elements, plot kit, pictures |
| `haipipe-report` | a report's own drawing, built from studio frames its `## Figures` lists |
| `haipipe-run` | the soft Run `run-draw-<sNN>` and its card |
| `workbench-studio` | the Page's Studio tab (drawing and chat together) |


Files
-----

```text
haipipe-studio/
├── SKILL.md
├── CHANGELOG.md
├── agents/openai.yaml
├── ref/topic-contract.md      the folder, face, numbering, builders, sessions, buttons, a proposal topic
├── scripts/canvas.py          the merge-safe writer
├── scripts/render_png.py      the offline PNG preview
├── scripts/new_topic.py       topic · session
└── tests/test_haipipe_studio.py
```
