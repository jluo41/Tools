---
name: hai-draw
description: "Draws on an Excalidraw canvas: which of the three drawing engines a drawing uses (the five-part drawing, the quick sketch, draw.py), the look and the nine principles each follows, and a gallery of drawing kinds: job, task, story, ideation, workflow, slide, draft, report or scratch, read. Use for any drawing. Trigger: draw, drawing, excalidraw, studio drawing, redraw a topic, /hai-draw."
argument-hint: "[kind] [args...]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Agent, Skill
metadata:
  version: "0.3.0"
  last_updated: "2026-11-27"
  # version history: ./CHANGELOG.md (skill-scoped, never loaded at invocation)
---

# /hai-draw · which engine, which look, which kind

Rules come in three layers, and the higher one wins:

```text
1  hai-studio/CONSTITUTION.md     every Studio drawing (A02 five parts, A04 pictures, A07 〈 〉 names)
2  this file                      which engine draws it, and that engine's look
3  gallery/<kind>/KIND.md         one kind's own shape and commands; it never restates 1 or 2
```

Read `../../project/hai-studio/CONSTITUTION.md` before the first edit of any Studio drawing, even to add one node.
The topic itself (folder, face, numbering, sessions, `canvas.write`, `render_png.py`) is `hai-studio`'s; this
skill draws.


Vivid first: icons in every drawing
-----------------------------------

This holds for every engine and every kind, before any other rule here.

1. **Draw the real things as icons**: a server, a database, a cloud, a phone, a person, a document, a hospital,
   each lit by its state (ok green, wait orange, bad red, off grey). `hai-studio/scripts/icons.py`; in a draw.py
   drawing, `d.icon("server", "b_app", x, y, "bad")`; any item of a downloaded library, `icon_library.py`.
2. **Every frame leads with something to look at**: icons, a big number (`icons.big_number`), a chart a Run drew,
   a screenshot. Words name the pictures; they never stand in for them.
3. **A box of words is not a picture**: a frame of only boxes, arrows and text is not done, however short.
4. **Checked**: `check.py` ⑨ fails a frame with no picture and fewer than three icon shapes; `five_parts.build`
   warns a Design under 20 picture shapes (CONSTITUTION A04).
   `check.py` also measures the whole drawing, frames or none, as its `V` lines: at most half of its things are
   boxes that only hold words (a row of text boxes beside one screenshot fails), no block of text is longer than
   30 words, and it says whether a number is drawn big (44 px or more). A `V ❌` is not done.
5. **Look before saying done**: render it (`render_png.py`) and ask whether a newcomer sees the things first.


Pick the engine
---------------

Every drawing is made by exactly one of three engines, and each engine has its own look. A rule below names the
engine it holds for; nothing here holds for all three unless it says so.

| engine | made by | when | its look |
|---|---|---|---|
| **five-part drawing** | `new_topic.py topic … --builder` → `five_parts.py` | the default for a topic a builder draws | § The five-part drawing |
| **quick sketch** | `new_topic.py topic …` (no `--builder`) → `quick_draw.py` | a new topic's light sketch, to mark up by hand | § The quick sketch |
| **draw.py** | `--builder draw`, or a gallery kind's script | a special shape: a screen, a report, a slide draft, every gallery kind | § The principles, § The draw.py look |

An existing drawing keeps its engine until someone redraws it. `check.py` tells them apart: a drawing with the
five part names is judged as a five-part drawing (⑤P), any other as a draw.py drawing (①-⑨).


The gallery
-----------

A gallery kind is a draw.py drawing of one recurring shape. Pick the kind, read its `KIND.md`, and run its
script from its own folder, `gallery/<kind>/scripts/` or `ref/`; never copy a kind's script here.

```text
the ask                                           kind        read
────────────────────────────────────────────────────────────────────────────────────────
a Job as a staircase of Tasks and Runs            job         gallery/job/KIND.md
a Task as a staircase of its Runs                 task        gallery/task/KIND.md
a paper's story: its research questions           story       gallery/story/KIND.md
an ideation: every idea under the question        ideation    gallery/ideation/KIND.md
a study's workflow as a building map              workflow    gallery/workflow/KIND.md
a slide deck proposed on one canvas (s61-s69)     slide       gallery/slide/KIND.md
a draft: a paper's Sections or one Section        draft       gallery/draft/KIND.md
a report's drawing, or a scratch whiteboard       report      gallery/report/KIND.md
one paper's PDF read onto a canvas                read        gallery/read/KIND.md
```

1. **Kind unclear**: name the two likeliest kinds and ask which.
2. **A kind draws its whole drawing**: its script writes every frame of its topic; the five-part drawing is
   not involved.
3. **A kind keeps its own shape** where `KIND.md` says so (§ Shapes that keep their own rules); everywhere else
   it follows the principles.


The five-part drawing
---------------------

The default for a topic a builder draws. Every such drawing is Idea · Now · Design · Process · Delivery, laid
out by `hai-studio/scripts/five_parts.py` (CONSTITUTION A02).

1. **Design is pictures** (CONSTITUTION A04): it leads with icons of the real things (`hai-studio/scripts/icons.py`),
   each lit by its live state, and a big number. A table holds only data rows; a sticky holds two short lines of
   at most 14 characters. `five_parts.build` warns under 20 picture shapes.
2. **Design's three sketches**: A the pieces step by step, B how it grew, C the open choices.
3. **Process** lists the topic's Job, each Task and each Run with its state, agent and skill from its run.yaml.
4. **Its colours are its own**: icons, coloured data rows, red questions, orange leanings. The principles ①-⑨
   and the draw.py look do not judge it.

How to build one:

- **Start from `new_topic.py --builder`**: it writes `build_sNN_<topic>.py` (its header, `SPEC`, `design()`) and
  `sketch_<topic>.py` beside it, three functions `(x, y) -> (els, y_bottom)`: `sketch_a`, `sketch_b`, `sketch_c`.
  Both import five_parts by a path relative to the topic. Fill every placeholder; `check.py` counts the ones left.
- **Marks kept**: the builder passes `writer=five_parts.marks_writer` (`canvas.write` with `palette=False`): a
  person's marks survive a rebuild and the colours stay. An older builder without it rewrites the drawing.
- **Unique ids**: every table and step needs its own eid; `data_step` adds `<eid>_t`, `data_table` adds `<eid>_h`,
  `_hd`, `_bd`, `_cJ`, `_vJ`, `_rI_J`. A clash stops `build` with an assertion naming the id.
- **The old drawing**: when the topic's owner says the kept first drawing goes, delete `result/first-drawing*` and
  `result/first-drawing-builder/`; they are git-ignored, so read them first and keep any fact the new sketch needs.

**A data topic** (`**Delivery type:** data`) draws in sketch A how the data is built, never a list of file or
level names:

1. **A data row per step**: the step's real column names over two or three rows with example ids (B1, D1, S1),
   never a row copied from the data (`five_parts.data_table`); beside it the icon of what holds it.
2. **An arrow per step, saying what it does**: "no billing for 4-52 weeks = an absence" (`five_parts.data_step`).
3. **One example followed through**: the same ids from the raw rows to the estimate.
4. **Streams that join**: two sources that build the unit side by side, joined where the unit is made.
5. **Every cut of the unit** side by side (pair x window, pair x year); a planned one in grey.
6. **End at what the next one reads**: the estimate that leaves the store, or the file the next step reads.


The quick sketch
----------------

A new topic without `--builder` gets `quick_draw.py`'s sketch: its life line with the stage marked, and the idea
drawn by hand as one pattern (cycle, timeline, tree, fan-in) with the kit's box, oval, diamond, arrow, line, dot
and text. It follows `references/workflow-diagrams/excalidraw-diagram-skill`: colour as meaning (`quick_draw.SEM`),
Excalidraw's code font, free text unless a shape carries meaning. It is never a list of the face's lines. An
existing sketch is never overwritten; to draw the topic properly, give it a builder. A sketch still leads
with icons of the real things (§ Vivid first), dragged in from `hai-studio/ref/icons/own-icons.excalidrawlib`.


The principles
--------------

They hold for a draw.py drawing: a gallery kind and a special shape. `check.py` measures them frame by frame.

```text
① 🖼️ one frame, as large as possible    fill one screen (about 2560 x 1440, at most 2800 x 1600) with facts; one
                                       main frame, largest, and smaller frames that explain it
                                       (canvas.explains); never many equal frames, never a frame per point
② 🗺️ inside it, a map                   a workflow (steps joined by arrows, a loop drawn closed, checks beside the
                                       step) or a mind map (one centre, branches by meaning); never a list or a
                                       table of names
③ 📖 the frames form the narrative      laid out by the story's shape (a row, a grid, a branch); acts, a row of
                                       frames each, named at the left; an arrow between frames only where one
                                       leads on, never through a third frame; the frames after the main one step
                                       down and right of it (canvas.stairs), never left-aligned rows; one long
                                       piece read down is one tall frame (canvas.reads_down)
④ 🚫 a folder tree only for folders     servers/, a skill folder, a Block's files: yes; ideas, rules, steps: no
⑤ 🔍 big words, one slight colour       frame title 60 px, a node 38 px, a detail 20 to 26 px; check.py fails a
                                       frame whose largest text is under 40 px or whose words are mostly under
                                       20 px; one slight colour (#fff3bf) marks each frame's key point
⑥ 📊 each frame's density, measured     words per million px, in the frame's corner on every build: a text frame
                                       at least 120; a map frame is measured by ⑦; a picture or a screen is not
                                       measured; a thin frame is merged, not padded
⑦ 🪶 few words in a map                 a step is a short name (28 px or more), an arrow one to three words; at
                                       most 200 words in a map frame, at most a quarter of them under 28 px; the
                                       detail goes to its own frame (Drawing.detail, ⑥ scaled 120 × (24 / body
                                       px)²); a signboard drawn k times a frame's size (canvas.signboard) holds
                                       200 × k words
⑧ 🌬️ room between boxes, numbers big    each box as wide as its words; boxes apart with clear space; a row hangs
                                       off the row above by a short straight drop, never a line circling back;
                                       measured values first, as a scoreboard: the number large, its label small
                                       above it; a frame marked Drawing.room has ⑥ measured over its boxes
⑨ 🎨 vivid, icons first               every frame leads with something to look at (§ Vivid first): icons of
                                       the real things, a chart read from disk, a screenshot, a scoreboard;
                                       check.py fails a frame with no picture and fewer than three icon shapes,
                                       and one with no picture and more than 600 words (600 a panel in a frame
                                       of panels, canvas.columns); the words stay in the face
```


The draw.py look
----------------

1. **Colours**: black lines and words (`canvas.INK`); red for an open point or a missing check (`canvas.RED`);
   green for a change note where it changed (`canvas.change_note`); the key colour of ⑤ (`canvas.KEY`). Nothing
   else: `canvas.write` turns any other stroke black and drops fills.
2. **Pictures and icons keep their colours**: a chart a Run's own code drew, a screenshot, an icon lit by its
   state (`canvas.is_icon`). Colour on a drawing comes from a picture or an icon, never from a box.
3. **A screen keeps the workbench's colours**: a frame marked `canvas.ui_frame(frame)`.
4. **Font**: Nunito for words, Cascadia for paths and code.
5. **Names no one**: who asked lives in the face's Decided lines, never on the drawing; never a person's photo.
6. **Marks**: a mark on a screen or a picture is a red box and a red → note.
7. **Full names, never short ids**: `goal × method version × inputs version`, never `G × m × i`; `the second draft`,
   never `v2`. An id appears only as a folder or file's literal name, in Cascadia, beside its words.
8. **A name not yet fixed is written in 〈 〉** (CONSTITUTION A07): `〈the aim〉`, never a bare word or a letter.


Shapes that keep their own rules
--------------------------------

`check.py` names these and does not judge the rules it lists; every other rule still holds.

| drawing | its own shape | `check.py` | owner |
|---|---|---|---|
| a screen inside a topic | the workbench's own colours, `canvas.ui_frame` | judged, colours exempt | hai-studio `canvas.py` |
| a scratch whiteboard | real material packed on one board, no frames | not judged | report |
| a report's drawing | its answer and evidence, its plots in their own colours | judged | report |
| a slide draft, s61 to s69 | three frames left to right, slides at half size; sizes, words and colours inside a slide as drawn | ① ③ ⑤ ⑥ ⑦ named | slide |
| a paper read onto a canvas, and a topic drawn from its readings | each logic frame keeps a key point | ⑥ ⑦ named | read |
| a paper's building map, s03-paper-dataflow | column layout, no frames, blue claim cards, small card text read zoomed in | ③ named | workflow |
| a file we change beside its updated sentences | two frames: the plan, then the side by side read down (3,320 px wide) | judged | draft |


The helpers: scripts/draw.py
----------------------------

```python
sys.path.insert(0, str(<Tools>/plugins/haipipe-toolkit/skills/1_base/draw/hai-draw/scripts))
from draw import Drawing, KEY, RED
d = Drawing()
f = d.frame("① The principles: one mind map")      # one screen; a frame's name starts with its mark
d.heading("🧠 The principles", "one line on what the frame says")
d.mind_map("the centre", branches)                 # branches: {title, by, summary, leaves}
d.flow(steps, x, y, w, labels=[...])               # a workflow in one row, named arrows
d.grid_table(x, y, columns, rows, widths)          # grey rules, a value's number large, its Run small
d.text(x, y, "\n".join(Drawing.folder_tree(path, open_=("scripts",))), 20, code=True)   # real folders only
d.icon("cylinder", "b_db", x, y, "ok")            # an icon of a real thing, lit by its state (icons.py)
d.picture(png, x, y, w, hmax)                      # a checked picture; not measured for density
d.badge(f)                                         # ⑥: the frame's density in its corner
d.acts([{"name": "Act 1 · …", "frames": [f["id"], g["id"]], "arrow": "lives in"}], between=[(f["id"], h["id"], "checked by")])
d.write(out, "build_sNN_<topic>.py")               # canvas.write: a person's marks kept
```

1. **One Drawing per builder**: its `els` and `files`; a frame's elements belong to the frame drawn last.
2. **Words from the face**: a builder reads its words from the face; facts on disk it reads on every build.
3. **Check**: every frame carries its badge; render the preview (`render_png.py`) and look before saying done.


Redraw a topic
--------------

`/hai-draw redraw <Block> <sNN>`, one topic at a time, on the topic's own engine.

```text
1 🔍 check     python scripts/check.py <topic>.excalidraw        what breaks (✅ ❌ 👤)
2 🧭 story     the main picture, the acts, a named arrow per step   from the face's Topic and Decided
3 ✍️ words     the face holds the words                            never typed in the builder
4 🧱 builder   five-part: fill SPEC and the sketches; draw.py:      old builder, face and preview
               frame, map, key, badge, acts, write                  copied to history/ first
5 🖼️ look      render_png.py, read the preview; check.py again     until ✅, or a reason written
6 💾 save      a decision line in the face; a round in passes/      hai-studio new_topic.py session
```

1. **One topic at a time**: a style asked for one topic stays on it until it is agreed here.
2. **Marks kept**: a person's marks survive (`canvas.write`); never redraw by hand.
3. **👤 lines**: check.py cannot tell a map drawn in words from a list; a person, or the agent saying why, decides.
4. **The person reviews**: they mark in red on the canvas; the next build keeps the red marks.
5. **A reader's review**: after drawing, `hai-studio-reviewer-agent` reads it as a newcomer (hai-studio
   `ref/reader-review.md`).


Files
-----

```text
hai-draw/
├── SKILL.md            this file: the engines, the looks, the principles, the gallery
├── CHANGELOG.md        its versions
├── agents/openai.yaml  Codex's card
├── scripts/draw.py     the helpers every draw.py builder imports
├── scripts/check.py    a drawing checked against its engine's rules, frame by frame
├── tests/test_draw.py  a drawing made with them, then checked
└── gallery/<kind>/     one drawing kind each: KIND.md, its own scripts/, ref/, tests/
```
