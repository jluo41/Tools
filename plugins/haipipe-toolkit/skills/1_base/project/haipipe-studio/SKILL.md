---
name: haipipe-studio
description: >-
  Owns Block Studio topics shared across Block, Job and Task views: their faces,
  numbering, drawings, builders that preserve human marks, and session passes.
  Use to add or redraw a Studio topic, build or update a Block's s00 background
  index from its Studios and Jobs, explain their progress and expected outputs
  as a connected tree, preview a drawing, or save a Studio session. Also covers
  proposal topics and s61-s69 slide drafts under their specific contracts.
  How a topic's drawing looks and reads is excalidraw-studio's: load
  /excalidraw-studio before drawing or redrawing a topic (its principles,
  draw.py, check.py). Scripts: canvas.py, render_png.py, new_topic.py and
  block_index.py.
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "0.13.19"
  last_updated: "2026-10-13"
  # version history: ./CHANGELOG.md
---

# /haipipe-studio · the topics a Block owns

The Block owns its Studio topics in `studio/`, one topic per `sNN-<topic>/`.
Block, Job and Task views share that Studio. Each topic has a drawing to think on
together and a short face that says what it settles and which Questions it feeds. This skill owns the folder, the face, the numbering, the builders that
keep a person's marks, and the sessions. How a topic's drawing looks and reads is `excalidraw-studio`'s: load
`/excalidraw-studio` before drawing or redrawing a topic (its principles, `scripts/draw.py` to draw with,
`scripts/check.py` to check); a report's drawing is `excalidraw-report`'s.

```text
<block>/studio/sNN-<topic>/
├── sNN-<topic>.md            Topic · Feeds · Files · Decided · Open
├── sNN-<topic>.excalidraw    the drawing (a builder's, with the person's marks kept)
├── sNN-<topic>.png           its preview
└── build_sNN_<topic>.py      the builder, when a script draws it
<block>/runs/run-draw-<sNN>/  one pass per working session
```

Read `ref/topic-contract.md` before adding a topic or writing a builder.


Topic count per Block
---------------------

Recommend at most **10 sNN topics per Block**. This counts topic folders, not the
largest sNN number: s51 can be one of a Block's ten topics. Keep each topic about
one connected subject. Before adding an eleventh, reuse a related topic or split
an independent area into a peer Block. s00, the background and index, is not counted. This is guidance, not a hard limit;
existing topics keep their ids and files. `new_topic.py` gives a non-blocking
reminder above ten, and a Job/Task input creates the topic in its owning Block.


Infer topics from the work
--------------------------

A Block that has Jobs and Tasks but no topics (an old Block, a new one brought up to date) gets its topics
from what its work already does, never from a generic list (JL 261012: "learn how to infer the relevant
studios from the existing block job and task"; b10 s10). `scripts/block_inventory.py <block>` reads every
Job and Task face and prints what repeats; read `ref/infer-topics.md` for the rules.

1. **A recurring Task kind** is a method topic: how that kind of Task is done (b00: 281 profile Tasks).
2. **A field that splits the Tasks** is one topic when the method differs by it (b00: 7 raw families).
3. **What stands out** goes to a topic's Open list and to the Report, naming the Jobs.
4. **No work, no topic**: each topic's **Topic:** line names the Tasks it explains.


Groups
------

A topic's groups are its `**Tags:**` line. The workbench's Studio row edits them: `+ Group`
names one, dragging a card onto a group adds the tag, × on a card's group (shown under the
mouse) takes it out, × beside a group deletes the tag from every topic. `studio/_groups.txt`
keeps the Block's groups in button order, empty ones included; dragging a group sideways
rewrites it. Both are plain text: edit them by hand when that is quicker. Current is the
person's own and stays in the browser (b10 s02-D16, D17). Related, folded under the topics, has
the same bar: there an item's groups are its subfolder (`meetings/` → meetings) and the names in
its row's `group` cell of `related/related.md`, and `related/_groups.txt` keeps their order (JL
261011); `haipipe-related` owns that folder.

Timeline, folded under Related, shows what moved when on one axis down the page, the oldest day at the
top, at three levels (Days · Topics · Everything), and follows the same bar (JL 261011; b10 s08). It reads only what a topic keeps: a decision's date in its brackets (`sNN-DNN · …
(JL 261011)`), a session's pass `pNN-<MMDD>`, a drawing's green `✎ <YYMMDD>` notes. A decision with no
date is left off it (b10 s08-D10), so date every decision.

Folder, folded under Timeline, shows the Block's own folder as one tree (JL 261012; b10 s09): a folder says how many
things it holds and what it is for (a shared name's fixed line, a Run's card, else its face's title), a file opens in
the pop-out. Nothing is written for it; a topic's folder is listed like any other.

Numbering
---------

```text
s00     background and index: one per Block, drawn by block_index.py (next section), never by hand
s01-s09 concepts · s11-s19 levels · s21-s29 runs and skills · s31-s39 Guide · s51-s59 server
s61-s69 slide drafts: a proposed deck, its logic flow and its slides, before the deck is built
```

The next free number in the band; a number is never reused, unless a person asks for it back (b10 s09, 261012):
then the new topic's decisions start after the old ids still kept where the old topic merged, and the old
`runs/run-draw-<sNN>/` moves into that topic's `history/`, so the Timeline does not read it as the new one's.
s00 is only ever `s00-background-and-index`: an older s00 topic moves to the next free s0x (b11 and b12's `s00-*-structure` became s04 on 261012).


Background and index (s00)
--------------------------

Read [ref/background-index.md](ref/background-index.md) when making or updating this entry point.
It connects the Block's purpose to all its Studios and Jobs, then to what the work should produce;
the generated inventory and the proposed finish stay distinct.

Every Block has `studio/s00-background-and-index/` (JL 261012: "for every block, we also want to have the
s00-background-and-index to show the background information, and what are the sNN and jNN and what are the
progress of them"). It is the first topic a newcomer opens.

```text
① Studio plan   the face's `studio_plan` yaml, when a Block's session writes one: the topics it needs as one
                story, steps joined by named arrows (b32 EB1A's first frame)
② Background    the face's `background:` yaml, typed by a person: boxes with arrows, or a tree
③ Index         read from disk on every build, a mind map read left to right, one row per item:
                🎯 Block ─thinks in─▶ 🧠 Studio ─▶ [ a topic: what it is for ] ──────▶ 📝 the Questions it feeds
                         └works in──▶ 🧱 Jobs   ─▶ [ a Job: state · steps · next ] ─▶ 🏁 what it must deliver
④ Proposed      the face's `studio_proposals` and `job_proposals`, when any is not made yet; one row each:
                ❓ the gap it closes ─▶ 🧠 the topic ─▶ 🧱 the Job ─▶ 🏁 what it delivers (red dashed until made)
```

The index (JL 261012, on b10's: "This one can be larger, of height. Currently it is too compact. each studio
should be a row."; then "this one is much better"):

1. **One row per item**: each topic and Job in its own box, in one column; never two or three columns.
2. **Taller, not tighter**: the frame grows down as its rows need; only its width stays one screen.
3. **The root**: the Block's box; under it its state, why it exists, when it is done, where it stands now.
4. **Arrows out**: from a topic's Feeds and a Job's `close:` line; dashed when the Job is on hold.
5. **No counts, no links**: tallies go stale; red names only real gaps (a Question nobody feeds).
6. **Proposed, not made**: not in the index; one red line per branch names them, and ④ draws them (JL 261012:
   "we also need to propose the new studio and new jobs in a new frame"). See `ref/background-index.md`.

How s00 looks, and only s00 (JL 261012: "I just mean for the s00 to have the tree, why you make all the others to
be the tree as well"; other topics keep their own drawings):

1. **Four frames at most**: the Studio plan (if written), the background, the index, what we propose next.
2. **Trees, boxes, arrows**: a background is a folder tree, or boxes with trees joined by named arrows.
3. **Emoji lead nodes**: ✅ done · 🔶 partly · ⬜ open · ❓ open (red) · 🧠 📝 🧱 📤 things.
4. **Sizes set apart**: title 60 · Block 44 · branch 38 · item 30 · heading 26 · output 22 · detail 20.
5. **Every language**: Chinese and other scripts are kept and wrap a character at a time; only emoji are
   stripped from the faces' own words.


The writer also creates `build_s00_background_and_index.py` in the topic. It forwards to the current
shared generator through the SPACE's `Tools` symlink, using a relative path; it contains no copied drawing
logic. Workbench therefore recognizes the drawing as generated and opens it view only. Existing local
builders are preserved. Rerun this builder after shared Tools changes to refresh the scene and preview.

`python $S/block_index.py <block> --draw` draws it; `--all <root>` draws every Block under a root. A face's
optional `index:` yaml says what no face does: `first` (where to start), `boundary`, `open`, and per Job
`label`, `finish` (what it must deliver) and `action`; per topic a `note` (b32 EB1A's index_plan, the model JL
picked on 261012: "for the index, I love this type of things ... This is more like the mindmap, right?").


A Job's current results (s21-s29)
---------------------------------

Each Job gets a topic that shows what its Runs have produced so far (JL 261012: "for each jNN, make the sNN to
show what are the current results"). It is the Block's, `studio/sNN-<jNN>-<job>-results/`, in the runs band;
a Job keeps no studio/ of its own. `scripts/job_results.py` makes it and its builder redraws it:

```bash
python $S/job_results.py <block>                                 # one topic per Job not drawn yet
python $S/job_results.py <block> --jobs j11_x,j12_y --slug <s> --title '<t>'   # a group of Jobs, a frame each
```

1. **From disk, every build**: each Task, each Run (`runs/<run>/result/`, or the older `results/<run>/`), its
   state, its headline values (a before and after pair as one: `acc 26.1% → 41.0%`), a source Run's title.
2. **Words in the face**: the `results:` yaml holds per Job its `reading` (the frame's key point), per Run the
   values to `show` (`at: <file>:<key>`), and the `open` points; the face's "Runs on disk" list is generated.
3. **More Jobs than the band**: group the Jobs that share their Tasks into one topic, one frame per Job and a
   first frame with a row per Job (Proj10 b03: 31 Jobs in five topics).
4. **The whole Job**: to show why the Job exists, what goes in and out, what it concluded and its tables and
   pictures (asked 261012), draw it with `excalidraw-job` (`job_drawing.py make <job>`), or `adopt` a one-Job
   results topic: its builder then calls excalidraw-job, and its `results:` words move into a `job:` yaml.


Add, redraw, save
-----------------

```bash
S=Tools/plugins/haipipe-toolkit/skills/1_base/project/haipipe-studio/scripts
X=Tools/plugins/haipipe-toolkit/skills/1_base/display/excalidraw-studio/scripts
python $S/new_topic.py topic <level> --slug <topic> --title '<title>' --band run [--feeds q01_x] [--builder]
python <block>/studio/sNN-<topic>/build_sNN_<topic>.py          # redraw: the person's marks are kept
python $S/render_png.py <drawing>.excalidraw <drawing>.png        # the preview
python $X/check.py <drawing>.excalidraw                            # against excalidraw-studio's principles
python $S/new_topic.py session <block> sNN --title '<session>' [--ask …] [--summary …] [--changed …]
```

0. **Draw with excalidraw-studio**: before drawing or redrawing a topic, load `/excalidraw-studio` (the Skill
   tool) and follow its "Redraw a topic with the principles"; a new builder (`--builder`) already starts on its
   `draw.py`, and `check.py` says what still breaks. This skill keeps the folder, the face and the sessions.
1. **Face marks**: `**Stage:**` (explore · shaping · agreed · closed), `**Topic:**`, `**Feeds:** qNN_<topic>`,
   `sNN-DNN` decisions, a numbered Open list. A person moves the stage; see `ref/topic-contract.md` § The face.
2. **Builder**: draws through `canvas.write`; never hand-edit its output, change the builder.
3. **Marks kept**: what a person adds, edits or deletes survives a rebuild (the seed snapshot).
4. **Session**: a pass of `run-draw-<sNN>`, written by `haipipe-run`'s `soft_run.py`.
5. **Changes**: red for open; every change to a drawing gets a short green note where it changed.
6. **Read it as a reader, then a reviewer** (JL 261012: "after you create such a draw, you should ask it yourself,
   If I am a reader, will this answer my questions for this job etc. Maybe you need to call a reviewer for it as
   well"): `check.py` passing is not done. Answer the reader's questions for the topic's kind (Job, Task, video or
   Run frame, s00) from the rendered frames alone; then call `haipipe-studio-reviewer-agent` in a fresh context, fix
   its gaps in the face or the builder, and repeat until it returns `answers`. The questions and the loop:
   `ref/reader-review.md`.


The look
--------

**How a topic's drawing reads now lives in `excalidraw-studio`** (`skills/1_base/display/excalidraw-studio/`,
agreed on b31 s01-drawing-principles, 261012): its principles (one frame as large as a screen; a workflow
map or a mind map inside; the frames as one story, in acts, joined by named arrows; a folder tree only for real
folders; big words and one slight colour for the key point; each frame's density measured; few words in a
workflow, fewest small ones) and its drawing
helpers, `scripts/draw.py`. Read it before drawing a topic. This section keeps what `canvas.py` enforces when a
builder writes; where the two differ (a mind map instead of a tree), follow `excalidraw-studio`. The slight
key-point colour is part of the look since 0.13.14: `canvas.KEY`, kept by the palette (b31 s01-D18). The tree,
boxes and emoji shape below is s00's alone.

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
5. **A screen in colour**: a frame that draws the workbench's screen wears the workbench's own light colours
   (JL 261012: "make the UI to be more colorful, like the same to what we see"). Mark it
   `canvas.ui_frame(frame)`; `canvas.write` then colours it by `colour_ui` from `canvas.UI`, the colours of
   `servers/workbench/frame.py`: gray panes, white buttons, the open tab blue, a proposed one violet dashed,
   stage pills in their own colours, links blue, a status word (answered, partial, open) its colour, a
   count bar blue. Red questions and green notes in it keep their colour; the rest of the drawing stays black.

One readable font (JL 261009: "I think the font should be more readable"): every word in Nunito,
Excalidraw's "Normal" font (`fontFamily` 6, `canvas.FONT`); paths and code may use Cascadia (3,
`canvas.CODE_FONT`). No hand-drawn Virgil (1) or Excalifont (5), no Comic Shanns (8). `canvas.write`
sets it on what a builder writes (`apply_font`), a change note included; the person's own marks and a
slide draft keep their fonts.

Frames in rows, never one long column (JL 261009: "don't put all the things in one column"): a builder
places its frames with `canvas.grid(els, [[...], [...]])`, read left to right and then down, two to four a
row; each frame moves with what is drawn in it. `canvas.write` warns when 4 or more frames stand in one
column.
Frames as stairs, not left-aligned rows (JL 261013: "你不能每一个都是朝左对齐。你朝左对齐好像就是每一个一列都是非常
重要的"): a drawing with one main frame places it first, at the origin, and each frame after it lower and further
right, `canvas.stairs(els, [main, (id, dx), …])`; a small frame that explains the main one is marked
`canvas.explains(frame)`, so check.py does not hold it to a screen's size ("主次分明 … 大小有致").
One idea, one dense frame (JL 261010: "既然是 idea，你搞那么多 frame 干嘛呀？... 一个 frame 的信息量是非常大的"):
a topic's idea is drawn as one connected flow, dense with facts, its most important part the largest;
a separate frame is for separate material (a source marked up, a reference picture), never for one more
step of the same idea. Large means much information, not a large canvas (next rule).

`canvas.tree(x, y, nodes, width, frame, cols=N)` draws one tree; a leaf starting "❓" or "? " draws red,
"✎ " green. Use ❓ only for what is open.
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
   counted), and `canvas.numbered_frames(els)` one piece cut into "· 1", "· 2"; `canvas.write` warns about
   each. For a Block's s00 only, it also warns past three frames and on a frame that reads like a slide.
7. **Side notes smaller**: notes beside the main content (the page pictures they explain) are written
   smaller than it, and `canvas.aside(e)` keeps them out of `small_text` (JL 261011: "The content or the
   font size, can be much smaller, than the main content").


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
3. **Never stacked in a corner**: no list of changes above the title or in a corner (JL 261010: "why the
   changes here is always in the left up corner ... add it to the places where we change it"). All the
   changes in one place is the face's Decided list. A whole new topic, frame or a rename gets no canvas
   note; it goes in the face. An old builder's top list moves next to what it describes (b10 s01
   `changes_at`: under the screen that shows it, else beside or above it, never on top of other words).
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

In the shared Studio reached from Block, Job or Task. Save new shared-topic
sessions against the Block; a Job/Task input also finds the Block when the topic
has no retained local copy. An explicitly selected legacy local topic keeps its
local Run and passes until that topic is moved.


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
| `excalidraw-studio` | how a topic's drawing looks and reads: its principles, `draw.py`, `check.py`; loaded before drawing |
| `excalidraw-job` | a Job as one topic: why, in and out, what it concluded, its tables; reads `job_results.py`'s readers |
| `excalidraw-report` | a report's drawing and a scratch: their modes, elements, plot kit, pictures |
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
├── ref/infer-topics.md        topics inferred from a Block's Jobs and Tasks (b10 s10)
├── scripts/canvas.py          the merge-safe writer
├── scripts/render_png.py      the offline PNG preview
├── scripts/new_topic.py       topic · session
├── scripts/block_inventory.py what a Block's Jobs and Tasks already do: kinds, splits, sub-questions
├── scripts/block_index.py     a Block's s00: its background, then its index as a map with each topic's and Job's progress
├── scripts/topic_map.py       a topic's frames from its face: trees, or boxes with their trees joined by named arrows
├── scripts/job_results.py     a Job's current results as a topic, read from its Runs on every build
└── tests/test_haipipe_studio.py
```
