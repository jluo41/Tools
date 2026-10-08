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
  build_*.py, canvas.write, render_png, seed snapshot, /haipipe-studio.
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "0.4.1"
  last_updated: "2026-10-08"
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
├── ref/topic-contract.md      the folder, face, numbering, builders, sessions, buttons
├── scripts/canvas.py          the merge-safe writer
├── scripts/render_png.py      the offline PNG preview
├── scripts/new_topic.py       topic · session
└── tests/test_haipipe_studio.py
```
