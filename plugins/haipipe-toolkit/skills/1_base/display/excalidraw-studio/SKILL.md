---
name: excalidraw-studio
description: >-
  How a Studio topic's drawing looks and reads: nine principles (one frame as large as a screen; a workflow
  map or a mind map inside; the frames as one story, in acts, joined by named arrows; a folder tree only for
  real folders; big words and one slight colour for the key point; each frame's density measured; few words
  in a workflow, fewest small ones; room between boxes; vivid, never a wall of text), the look
  (black, red open, green a change, Nunito, names no one), the shapes that keep their own rules (screens,
  s00, reports, slides), and one set of drawing helpers every builder imports (scripts/draw.py). Use before
  drawing or redrawing any sNN topic, to check a drawing against the principles, or to pick a pattern (mind
  map, flow, acts, folder tree, a checked picture). Loaded by /haipipe-studio before it draws or redraws a
  topic; its new builders start on draw.py. The topic folder, face, numbering, sessions and the writer that
  keeps a person's marks stay haipipe-studio's. Trigger: studio drawing, draw a topic, redraw, too many
  frames, low density, mind map, workflow map, acts, named arrows, key point, folder tree, /excalidraw-studio.
allowed-tools: Bash, Read, Edit, Write, Grep, Glob
metadata:
  version: "0.3.7"
  last_updated: "2026-10-12"
  # version history: ./CHANGELOG.md
---

# /excalidraw-studio · how a Studio drawing reads

A Studio topic's drawing is where a person and an agent think about one topic together. It has to read as
one story, zoomed out, and hold enough to work on, zoomed in. The principles were agreed on a drawing of
their own, `Tools/blueprints/b31_excalidraw/studio/s01-drawing-principles/` (b31 s01), after a day when one
shape meant for a single drawing (s00's index) was copied to every topic and had to be undone; the model to
copy is b10 s52-host-and-share.

```text
① principles ──checked by──▶ ② the checks ──applied to──▶ a drawing that reads as one story
     │ lives in
     ▼
this skill: SKILL.md (the rules) · scripts/draw.py (the helpers) · haipipe-studio canvas.write (marks kept)
```

Read the principles, pick the patterns, draw with `scripts/draw.py`, write through haipipe-studio's
`canvas.write` (via `Drawing.write`), check the frame badges, rebuild until every check passes.

**With /haipipe-studio** (linked 261012): haipipe-studio makes the topic (`new_topic.py topic`), keeps its face and
saves its sessions; before it draws or redraws, it loads this skill. `new_topic.py --builder` writes a builder
already on `draw.py` (a frame, its key point, a workflow map, the density badge, an act); `check.py` comes after
every rebuild.

```text
/haipipe-studio  new_topic.py topic ─▶ /excalidraw-studio  principles · draw.py ─▶ builder ─▶ check.py
       ▲                                                                                        │
       └──────────────── new_topic.py session: a pass of run-draw-<sNN> ◀──────────────────────┘
```


The principles
--------------

```text
① 🖼️ one frame, as large as possible    fill one screen (about 2560 x 1440, at most 2800 x 1600) with facts;
                                       never many small frames that each say one thing (a slide)
② 🗺️ inside it, a workflow map or a     steps joined by arrows, a loop drawn closed, checks beside the step;
     mind map                          or one centre with branches by meaning; never a list or a table of names
③ 📖 the frames form the narrative      laid out by the story's shape (a row, a grid, a branch), never one row
                                       by habit or one long column; acts, a row of frames each, named at the
                                       left; an arrow between frames only where one leads on (not by habit),
                                       never through a third frame; the main picture first and largest; one long piece
                                       read down is one tall frame (canvas.reads_down: its width fits)
④ 🚫 a folder tree only for folders     servers/, a skill folder, a Block's files: yes; ideas, rules, steps,
                                       Questions, groups: no
⑤ 🔍 big words, one slight colour       titles and arrows large enough to read zoomed out (frame title 60 px,
                                       a node 38 px, a detail 20 to 26 px); one slight colour (#fff3bf) marks
                                       each frame's key point; red stays open, green a change
⑥ 📊 each frame's density, measured     words per million px, on every build, in the frame's corner: a text
                                       frame at least 120; a map frame is measured by ⑦; a picture or a screen
                                       is not measured; a thin frame is merged, not padded
⑦ 🪶 few words in a workflow, fewest    a map reads from its boxes and arrows, not its words: a step is a short
     small ones                        name (28 px or more), an arrow one to three words; at most 200 words in
                                       a map frame, at most a quarter of them a detail (under 28 px); the
                                       detail goes to its own frame or topic (a Task's: excalidraw-task); that
                                       frame is marked Drawing.detail and ⑥ measures it (a video's full frame),
                                       its floor scaled by its type: 120 × (24 / body px)², 77 at 30 px
⑧ 🌬️ room between boxes, the numbers  each box only as wide as its words need, never stretched to fill a row;
     big                               boxes stand apart with clear space, a flow stepping right and down like
                                       stairs; nothing nested edge to edge (asked 261012: "leave some rooms, not
                                       all the things nested together"); a row hangs off the row above by a short
                                       straight drop, never a line circling back across the frame ("I don't want
                                       this circle back line any more, give me the stair version"); a Task's
                                       measured values come first, as
                                       a scoreboard: each number large, its label small above it ("for a task,
                                       we want to salient show the numbers and the values"); the room is not
                                       thinness: a frame marked Drawing.room has ⑥ measured over its boxes
⑨ 🎨 vivid, never a wall of text       every frame leads with something to look at: a chart read from disk, a
                                       real data row, a screenshot, a formula worked through, a scoreboard;
                                       a frame of only text boxes is forbidden (asked 261012: "things like this
                                       should be forbiden, so rigid, not vivid, no one have the incentive to
                                       zoom in and read"); check.py ⑨ fails a frame with no picture and more
                                       than 600 words; the words stay in the face
```


The look
--------

1. **Colours**: black lines and words; red for an open point (❓) or a missing check; green for a change
   note where it changed (`canvas.change_note`); the one slight colour of ⑤ for a key point, nothing else.
2. **Font**: Nunito for words, Cascadia for paths and code; never a handwritten font.
3. **Names no one**: a principle says when it was asked ("asked 261012"), a check says "a person"; who asked
   lives in the face's Decided lines, never on the drawing; never a person's own photo.
4. **Marks**: a mark on a screen or a picture is a red box and a red → note, never a colour the screen lacks.


Shapes that keep their own rules
--------------------------------

| drawing | its shape | owner |
|---|---|---|
| a Studio topic, sNN | the principles | this skill |
| a screen inside a topic | the workbench's own colours, `canvas.ui_frame` | haipipe-studio `canvas.py` |
| s00, a Block's background and index | its tree, boxes, emoji; its Studio plan; proposed sNN and jNN; its words, since an index names every topic and Job (`check.py` names it for ⑦, does not judge) | haipipe-studio `block_index.py` |
| a report's drawing, a scratch | excalidraw-report | excalidraw-report |
| a slide draft, s61 to s69 | three frames left to right, slides at half size; its own sizes, words and colours (`check.py` names it, does not judge) | excalidraw-slide |
| a paper read onto a canvas | excalidraw-read | excalidraw-read |
| a file we change, section by section beside its updated sentences | two frames: the plan, then the side-by-side that reads down (3,320 px wide on purpose) | excalidraw-revise |
| a paper's Sections as a map | excalidraw-section | excalidraw-section |
| a Job as one drawing: why, in and out, what it concluded, its tables | four frames in two acts | excalidraw-job |


The helpers: scripts/draw.py
----------------------------

```python
sys.path.insert(0, str(<Tools>/plugins/haipipe-toolkit/skills/1_base/display/excalidraw-studio/scripts))
from draw import Drawing, KEY, RED
d = Drawing()
f = d.frame("① The principles: one mind map")      # one screen; a frame's name starts with its mark
d.heading("🧠 The principles", "one line on what the frame says")
d.mind_map("the centre", branches)                 # branches: {title, by, summary, leaves}
d.flow(steps, x, y, w, labels=[...])               # a workflow in one row, named arrows
d.grid_table(x, y, columns, rows, widths)          # b03's grid: grey rules, a value's number large, its Run small
d.text(x, y, "\n".join(Drawing.folder_tree(path, open_=("scripts",))), 20, code=True)   # real folders only
d.picture(png, x, y, w, hmax)                      # a checked picture; not measured for density
d.badge(f)                                         # ⑥: the frame's density in its corner
d.acts([{"name": "Act 1 · …", "frames": [f["id"], g["id"]], "arrow": "lives in"}], between=[(f["id"], h["id"], "checked by")])
d.write(out, "build_sNN_<topic>.py")               # canvas.write: a person's marks kept
```

1. **One Drawing per builder**: its `els` and `files`; a frame's elements belong to the frame drawn last.
2. **Words from the face**: a builder reads the words from its face's yaml blocks; facts it can read from disk
   it reads on every build, never typed.
3. **Check**: every frame carries its badge; open the preview (`render_png.py`) and look before saying done.


Redraw a topic with the principles
----------------------------------

Asked 261012: "if I want to update the current draw with these principles, how should I do?" Ask the agent
`/excalidraw-studio redraw <Block> <sNN>`; it does these steps, one topic at a time.

```text
1 🔍 check     python scripts/check.py <topic>.excalidraw       what breaks, frame by frame (✅ ❌ 👤)
2 🧭 story     the main picture; the acts; a named arrow for each step   from the face's Topic and Decided
3 ✍️ words     the face's yaml blocks: each frame's map, its key point     never typed in the builder
4 🧱 builder   rewrite it on scripts/draw.py: frame, mind_map or flow,      old builder, face and preview
               key, badge, acts, write                                    copied to history/ first
5 🖼️ look      render_png.py, read the preview; check.py again            until ✅, or a reason written
6 💾 save      a decision line in the face; a pass of run-draw-<sNN>       haipipe-studio new_topic.py session
```

1. **One topic at a time**: a style asked for one topic stays on that topic until it is agreed here
   (the 261012 lesson: s00's shape copied to every topic, then undone).
2. **Marks kept**: a person's marks on the old drawing survive (canvas.write); never redraw by hand.
3. **👤 lines**: check.py cannot tell a map drawn in words from a list, or a real folder from an idea drawn as
   one; a person (or the agent, saying why) decides.
4. **The person reviews**: open the topic in the Studio, mark in red what is wrong, ask again; the next build
   keeps the red marks.


Boundary
--------

| Owner | Owns |
|---|---|
| `excalidraw-studio` | how a Studio topic's drawing looks and reads: the principles, the look, the patterns, `draw.py` |
| `haipipe-studio` | the topic: folder, face, numbering, builders' place, sessions, `canvas.write` and its checks, `render_png.py`, s00 (`block_index.py`); it loads this skill before drawing, and `new_topic.py --builder` starts a builder on `draw.py` |
| `excalidraw-report` · `-slide` · `-read` · `-section` · `-job` | their own drawings (b31 s02 to s06) |


Files
-----

```text
excalidraw-studio/
├── SKILL.md            this file
├── CHANGELOG.md        its versions
├── agents/openai.yaml  Codex's card
├── scripts/draw.py     the helpers every Studio builder imports
├── scripts/check.py    a drawing checked against the principles, frame by frame
└── tests/test_draw.py  a drawing made with them, then checked: frames, acts, density, a folder tree
```
