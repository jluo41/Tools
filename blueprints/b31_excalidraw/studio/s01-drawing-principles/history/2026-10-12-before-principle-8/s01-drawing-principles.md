s01 · Drawing principles: how a Studio drawing reads
====================================================

New on 261012 (JL: "I think we need the sNN for the excalidraw principle"), after a day of redraws that
went the wrong way: a shape meant for one drawing (s00's index) was copied to every topic, and JL said "I
think you ruin the whole things. I just mean for the s00 to have the tree, why you make all the others to
be the tree as well". This topic keeps the principles in one place, with JL's words and dates, so a
session reads them here before it draws.

**Stage:** closed

**Topic:** how a Studio topic's drawing should read: how big a frame is, what goes inside it, how the
frames are arranged, and which shapes belong to which kind of drawing. The skills hold the rules they
enforce (haipipe-studio "The look", `canvas.py`; excalidraw-report); this topic is where the principles
are agreed first, then carried into those skills.

**Feeds:** none yet


The Excalidraw principles
-------------------------

The skill `excalidraw-studio` holds them; frame ① of the drawing shows them, title and summary in big words, and an
open point in red. The words are each branch's `title` and `summary` in the `mindmap:` block below; its `leaves`
are the detail, kept here and not drawn (⑦).

```text
① 🖼️ One frame, as large as possible            fill one screen with facts; never a slide
② 🗺️ Inside it, a workflow map or a mind map    a workflow or a mind map inside; never a list
③ 📖 The frames form the narrative              one story: laid out by its shape, acts, named arrows
④ 🚫 A folder tree only for folders             a folder tree only for real folders
⑤ 🔍 Big words and one slight colour            big words for the logic; one soft colour for the key point
⑥ 📊 A text frame's density, measured          enough words in a text frame; merge a thin one
⑦ 🪶 Few words in a workflow, fewest small ones  a map reads from boxes and arrows: few words, few small
🎨 The look                                      black lines, red open, green a change; names no one
📚 Shapes that keep their own rules              screens, s00, reports and slides keep their own rules
```


Files
-----

```text
s01-drawing-principles/
├── s01-drawing-principles.md              this face; the drawing's words are its yaml blocks
├── build_s01_drawing_principles.py        the builder; reads this face, canvas.py and the examples
├── s01-drawing-principles.excalidraw      five frames in two acts, joined by named arrows (below)
├── s01-drawing-principles.png             its preview
├── .s01-drawing-principles.seed.json      generated snapshot for preserving marks
├── examples/                              four b10 previews as they were on 261012, kept so the
│                                          verdicts in ③ stay true when those topics are redrawn
└── history/                               the drawing before ⑦ (builder, face, preview; 261012)
```


What the drawing holds
----------------------

Five frames in two acts, each act a row named at the left, as b10 s52 does (JL 261012: "I love the act things
here as well, we can do it as well"); a named arrow for each step. Each frame is as large as one screen, its key
point marked with one slight colour (⑤); in its top right corner, a text frame's density (⑥) or a map's words (⑦).

```yaml
acts:
- name: Act 1 · What a drawing must do, and where that lives
  frames: [①, ④, ⑤]
  arrow: [lives in, draws s00]
- name: Act 2 · How a drawing is checked, and four that were
  frames: [②, ③]
  arrow: applied to
between: {from: ①, to: ②, label: checked by}
```

```text
Act 1 · What a drawing must do      ① the Excalidraw principles ─lives in─▶ ④ the skill folders ─draws─▶ ⑤ s00
         │ checked by
Act 2 · How a drawing is checked    ② the checks, seven stages ─applied to─▶ ③ four drawings, one to copy
```

① 📐 the Excalidraw principles: the first frame; "The Excalidraw principles" in the centre (the key point), the
   seven asked for in bold and the two standing rules around it, five on the left and four on the right, each its
   title (46 px) and its one-line summary (32 px), an open point in red (28 px); no small detail (⑦).
② 🔁 the checks: seven stages, each check a short line with the principle it guards and who checks it (canvas.py
   or check.py, read live, or a person); the loop back to the builder. What each check caught stays in the face.
③ 🧪 four drawings from 261012: b10 s05's tree pass and b10 s05 restored (both drawn as s07, since merged into s05), b10 s52 (the one to copy, highlighted),
   each checked against the principles; then b10 s51 before and after.
④ 🧰 the skill folders: excalidraw-studio (the key point) and haipipe-studio, the four excalidraw skills, folder
   trees read from disk.
⑤ 🗂️ s00, a Block's background and index: the one drawing with its own shape; what it reads, what it draws, and
   what it proposes, new topics (sNN) and new Jobs (jNN), until a person ticks them; b31's own proposals read live.

Rebuild: `python build_s01_drawing_principles.py`, then `render_png.py` for the preview.


The principles (the mind map, ①)
--------------------------------

JL's words (261012): "the principle is that one frame should be as large as possible, wihtin the frame,
we want the workflow map or the mindmap, the frames should be well arrange to form the narrative. These
are the principles. No more folder tree for the non folder items."

```yaml
mindmap:
  centre: a Studio drawing reads as one story
  branches:
  - title: 🖼️ ① One frame, as large as possible
    summary: "fill one screen with facts; never a slide"
    by: asked 261012
    leaves:
    - fills one screen, about 2560 x 1440, at most 2800 x 1600
    - dense with facts; words 20 px or more
    - never many small frames that each say one thing (a slide)
    - "✅ one screen, or one tall frame read down (Open 1 settled)"
  - title: 🗺️ ② Inside it, a workflow map or a mind map
    summary: "a workflow or a mind map inside; never a list"
    by: asked 261012
    leaves:
    - "workflow: steps joined by arrows; a loop drawn closed; checks beside the step"
    - "mind map: one centre, branches by meaning"
    - not a list, not a table of names
    - draw the logic, flows, checks, loops and gates
  - title: 📖 ③ The frames form the narrative
    summary: "one story: laid out by its shape, acts, named arrows"
    by: asked 261012
    leaves:
    - the main picture first and largest (261011)
    - "laid out by the story's shape: a row, a grid or a branch; never one row by habit, never one long column (261012)"
    - "acts: a row of frames per act, the act named at the left (s52)"
    - "a named arrow between frames: checked by, applied to, lives in (261010)"
    - one long piece read down is one tall frame (261010)
  - title: 🚫 ④ A folder tree only for folders
    summary: "a folder tree only for real folders"
    by: asked 261012
    leaves:
    - "yes: servers/, a skill folder, a Block's files"
    - "no: ideas, rules, steps, Questions, groups"
    - the tree, boxes and emoji shape is s00's alone (261012)
    - "✅ check.py flags folder-tree lines for a person (Open 3 settled)"
  - title: 🔍 ⑤ Big words and one slight colour for the key point
    summary: "big words for the logic; one soft colour for the key point"
    by: asked 261012
    leaves:
    - "zoomed out, the logic still shows: titles and arrows large"
    - "a frame's title 60 px, a node's 38 px, a detail 22 to 26 px"
    - "one slight colour marks the key point; red stays open, green a change"
    - "✅ canvas.py keeps it since haipipe-studio 0.13.14 (Open 5 settled)"
  - title: 📊 ⑥ A text frame's density, measured
    summary: "enough words in a text frame; merge a thin one"
    by: asked 261012
    leaves:
    - "words per million px, counted on every build, frame by frame"
    - "a text frame: at least 120 (canvas.SPARSE_MIN); a slide-like one holds 40 to 110"
    - "a map frame is not measured here: ⑦ measures it (the map floor of 70 retired, 261012)"
    - "a thin frame is merged into its neighbour, never padded"
    - "✅ a floor per kind of frame, and an upper bound: settled by ⑦ (Open 6)"
  - title: 🪶 ⑦ Few words in a workflow, fewest small ones
    summary: "a map reads from boxes and arrows: few words, few small"
    by: asked 261012
    leaves:
    - "a step is a short name, 28 px or more; an arrow one to three words"
    - "at most 200 words in a map frame, at most a quarter under 28 px"
    - "the detail goes to its own frame or topic, or stays in the face"
    - "check.py's ⑦ row; draw.py's badge: 🪶 words, % small"
  - title: 🎨 The look
    summary: "black lines, red open, green a change; names no one"
    by: standing
    leaves:
    - black lines and words; red open; green a change (261007)
    - "the one slight colour of ⑤ marks a key point, nothing else"
    - a short green note where it changed (261007)
    - Nunito; Cascadia for paths; no handwriting (261009)
    - "names no one: 'asked 261012', 'a person agrees' (261012)"
    - never a person's own photo
  - title: 📚 Shapes that keep their own rules
    summary: "screens, s00, reports and slides keep their own rules"
    by: standing
    leaves:
    - "a screen inside a drawing: the workbench's own colours (canvas.ui_frame)"
    - "a mark on a screen: a red box and a red → note, never a colour the screen lacks (261012)"
    - "s00, a Block's index: its tree, boxes, emoji (261012)"
    - "a report's drawing: excalidraw-report; a slide draft, s61 to s69: excalidraw-slide"
```


Checking a drawing (the workflow, ②)
------------------------------------

Each check names the principle it guards and who checks it: a `canvas.py` function (the drawing reads
whether it exists, live), a person, or nobody yet (red); the drawing groups them by `stage`, in order.

```yaml
checks:
- step: a builder draws from disk
  stage: build
  guards: ""
  by: build_<topic>.py
  caught: 'reads the face and the disk; nothing it can read is typed'
- step: frames too large?
  stage: size
  guards: ①
  by: canvas.oversized
  caught: 's51 at 10:03: nine small frames'
- step: words too small?
  stage: size
  guards: ①
  by: canvas.small_text
  caught: 'under 20 px, a frame reads only at 100% zoom'
- step: a text frame too thin?
  stage: size
  guards: ⑥
  by: canvas.sparse
  caught: 'b04 s00 frames of 38 to 113 words per million px read like slides'
- step: a map, or a list?
  stage: inside
  guards: ②
  by: person
  caught: 's05''s Across frame (then s07): tables of names'
- step: a tree of things not folders?
  stage: inside
  guards: ④
  by: check.py
  caught: 's05''s tree pass (then s07): groups and rules drawn as folders'
- step: a map with too many words?
  stage: inside
  guards: ⑦
  by: check.py
  caught: '175 of 181 map frames in Tools, median 386 words, 98% small (261012)'
- step: one story, main picture first?
  stage: story
  guards: ③
  by: canvas.one_column
  caught: 's05''s map pass (then s07) opened like s00''s index'
- step: readable zoomed out?
  stage: look
  guards: ⑤
  by: person
  caught: 'a 22 px title vanishes at 25% zoom; 38 px stays'
- step: black, red, green; Nunito
  stage: look
  guards: look
  by: canvas.off_palette
  caught: 'violet dashed buttons that the screen never had (s05, then s07)'
- step: written, marks kept
  stage: write
  guards: ""
  by: canvas.write
  caught: 'every rebuild today: 0 marks lost'
- step: a person agrees, or marks red
  stage: agree
  guards: all
  by: person
  caught: '"you ruin the whole things": five topics restored'
loop: a failed check goes back to the builder, never to the drawing by hand
```


The skill folders that hold them (④)
------------------------------------

Real folders, so they are drawn as folder trees (principle ④); each tree is read from disk on every build.
`holds` says which principles or checks live in that skill.

```yaml
skills:
- name: haipipe-studio
  path: 1_base/project/haipipe-studio
  why: a Studio topic's folder, face, builder and the look of its drawing
  holds:
  - "SKILL.md, The look: the palette, the font, frames in rows, a frame fits the screen"
  - "scripts/canvas.py: write keeps a person's marks; oversized, small_text, sparse, one_column, off_palette"
  - "scripts/render_png.py: the preview; scripts/new_topic.py: a topic and its sessions"
  - "scripts/topic_map.py and block_index.py: s00's tree and boxes, for s00 only"
  link: enforces ① ③ ⑤ ⑥
- name: excalidraw-studio
  path: 1_base/excalidraw/excalidraw-studio
  key: true
  why: how a Studio topic's drawing reads, one place to read before drawing
  holds:
  - "the principles agreed here (b31 s01), as its SKILL.md"
  - "the patterns: a mind map, a workflow of stages, a screen, checked examples, a folder tree for folders"
  - "scripts/draw.py: one set of drawing helpers every builder imports (s01 to s07, excalidraw-job and excalidraw-task use it)"
  - "haipipe-studio keeps the topic itself: its folder, face, numbering, sessions and canvas.write"
  link: holds the look
- name: excalidraw-report
  path: 1_base/excalidraw/excalidraw-report
  why: how a drawing looks in two modes, a scratch and a report's drawing
  holds:
  - "a scratch: loose clusters, sticky notes, red marks"
  - "a report's drawing: its answer and its evidence"
  link: a report's drawing
- name: excalidraw-slide
  path: 1_base/excalidraw/excalidraw-slide
  why: a slide draft, s61 to s69, one frame per slide
  holds:
  - "its own colours and one frame per slide, by design"
  link: a slide draft
- name: excalidraw-read
  path: 1_base/excalidraw/excalidraw-read
  why: one paper read onto a canvas, its passages and links
  holds:
  - "the revise mode: a co-author's file, one shot per section (b31 s21)"
  link: a paper reading
- name: excalidraw-draft
  path: 1_base/excalidraw/excalidraw-draft
  why: a paper's Sections as a map, read left to right
  holds:
  - "generated from the Draft plans and Evidence Items"
  link: a paper map
- name: excalidraw-job
  path: 1_base/excalidraw/excalidraw-job
  why: a Job as one drawing, why, what it did, what it found
  holds:
  - "two frames in few words, read from the Job on disk"
  link: a Job
  since: "✎ 261012 added, asked on this frame (b31 s06)"
- name: excalidraw-task
  path: 1_base/excalidraw/excalidraw-task
  why: a Task as one drawing, its idea, then each video
  holds:
  - "a frame per video: what it told, what to check"
  link: a Task
  since: "✎ 261012 added (b31 s07)"
```


s00, a Block's index, and what it proposes (⑤)
-----------------------------------------------

Asked 261012: "I think we should have a new frame for the s00-background-and-index for it as well. s00 should also
work in a way for the proposing the sNN and jNN as well." s00 is drawn by haipipe-studio's `block_index.py` from
the Block on disk and from its face's yaml (`background`, `index`, `studio_plan`, `studio_proposals`, and, asked
for here, `job_proposals`); this frame shows that path and b31's own proposals, read from its s00 face.

```yaml
s00:
  steps:
  - title: 📂 the Block on disk
    lines: ["its face, board.md", "studio/, jNN_<job>/, runs/"]
  - title: ✍️ the s00 face
    lines: ["background, index, plan", "proposed topics and Jobs"]
  - title: ⚙️ block_index.py draws
    lines: ["plan, background, index", "💡 proposals, red and dashed"]
  - title: 🙋 a person ticks
    lines: ["red and dashed until ticked"]
  - title: 🧱 made
    key: true
    lines: ["new_topic.py, or jNN_<job>/", "the next build shows it"]
  labels: [read with, draws, shown to, then]
  own_shape:
  - "a tree, boxes, emoji"
  - "it reads down"
  - "proposals in the last frame"
```


Four drawings from 261012 (③)
-----------------------------

Kept in `examples/` as they were that day; the verdicts are this topic's reading, one line per principle. The ⑥
lines of s51 and s52, and a green line on what changed since, are read from check.py on their drawings on every
build.

JL 261012, on b10 s52-host-and-share: "I think this is very a good example, (except for the coloring)". Read here
as: copy its acts (rows of frames named at the left), one idea a frame sized to what it holds, a mind map or a
numbered workflow inside, boxes with an emoji title, a why line and short leaves, named arrows between boxes and
between frames, open points red in place. Its colouring is the one thing not to copy: all black, so no frame
marks its key point (principle ⑤); if JL meant something else by "the coloring", correct this line. Measured: its
six frames hold 74 to 102 words per million px, under the 120 floor, and still read well, because the arrows and
boxes carry the meaning: so ⑥'s floor depends on the kind of frame (Open 6).

JL 261012, on s51's four frames: "I feel the frame here is of low information density and too many frame? Or it
should be good enough, as each frame to be one specific topic." Measured: 69, 87, 69 and 75 words per million px,
all under the floor of 120 (922 words in all). Four topics, one a frame, is right (③); the frames are too thin
(⑥): 922 words fill about two screens. Two ways out: merge ① and ② (one host, one request: the same path, 525
words, 142 per million px) and ③ with ④ (397 words, 107, plus the route table it dropped); or keep four and put
back the facts the 10:03 version held (each Workbench's routes, the Handler's mixins, the Guide by level).

Since, the same day: ⑥'s floor became the floor of a frame's kind (a map frame 70, Open 6), so both pass it; and both
were redrawn by their own session with a key point in each frame (s52-D16, s51 "Redrawn 261012"). The verdicts above
stay that day's reading; the green line under each says what check.py finds today (s01-D16).

```yaml
examples:
- name: b10 s05 (was s07), the tree pass
  when: 261012, withdrawn the same day
  image: examples/b10-s05-tree-pass-261012.png
  verdict:
  - "✅ ① three large frames"
  - "❌ ② two of them folder trees of ideas"
  - "❌ ③ opened like s00's index"
  - "❌ ④ groups, rules, decisions drawn as folders"
- name: b10 s05 (was s07), restored
  when: 261012, after the restore
  image: examples/b10-s05-restored-261012.png
  verdict:
  - "✅ ① the screens frame fills a screen"
  - "🔶 ② the frames below hold tables"
  - "✅ ③ the screens first, the rules below"
  - "✅ ④ its one tree is In Tools, real folders"
- name: b10 s52-host-and-share, the one to copy
  when: 261012, its look as it was that day
  image: examples/b10-s52-host-and-share-261012.png
  drawing: ../../../b10_project_workbench/studio/s52-host-and-share/s52-host-and-share.excalidraw
  key: true
  verdict:
  - "✅ ① six frames, one idea each, each sized to what it holds"
  - "✅ ② a mind map or a numbered workflow; boxes joined by named arrows"
  - "✅ ③ three acts, named at the left; named arrows between frames"
  - "✅ ④ no folder tree; short lines under each box"
  - "🔶 ⑤ all black: no frame marks its key point"
  since: "✎ redrawn 261012 by its session: a key point in each frame, titles 60 px (s52-D16)"
before_after:
  name: b10 s51, before and after (261012)
  before:
  - Start
  - Status and next
  - The folders
  - One request
  - The frame
  - Routes
  - Where links land
  - The Guide
  - Questions
  before_note: "seen at 10:03: nine small frames in two columns, no arrow between them"
  after: ../../../b10_project_workbench/studio/s51-server-runtime/s51-server-runtime.excalidraw
  after_note: "read live from s51's drawing: its frames, in order, joined by arrows"
  image: examples/b10-s51-server-runtime-261012.png
  verdict:
  - "🔶 ① four frames a screen wide, but only two screens of words"
  - "✅ ② each a map of boxes and arrows"
  - "✅ ③ joined by arrows, left to right"
  - "✅ ④ no folder tree at all"
  since: "✎ redrawn 261012 by its session: a key point in each frame, thin frames given facts"
```


Decided
-------

s01-D01 · Decided (JL 261012): the four principles above. A frame is as large as it can be and dense; inside
    it, a workflow map or a mind map; the frames arranged into one narrative; a folder tree only for real
    folders and files.
s01-D02 · Decided (JL 261012: "I just mean for the s00 to have the tree, why you make all the others to be the
    tree as well"): the tree, boxes and emoji shape is s00's alone; the five b10 topics redrawn in it today
    (s03, s05, s06, s21, and s07, since merged into s05) were restored the same day.
s01-D03 · Decided (JL 261012, on b10 s05, then s07: "if we want to show the indicator, we can use the red box to circle
    them and give --> text to explain them, I don't want it to be mislead the UI design"): a screen inside a
    drawing shows only the screen's own colours; what is proposed, guessed or missing is a red box with a
    red → note.
s01-D04 · Proposed (261012): s01's own drawing is four screen-sized frames read left to right, a mind map, a
    workflow map, the checked examples and the skill folders, so it shows the principles as well as stating them.
s01-D05 · Decided (JL 261012: "another principle to to use the good font size and slight color to highlight the
    key point, what even I zoom out, I can see the logics"): principle ⑤, big words for the structure (titles,
    arrows) and one slight colour for each frame's key point; red stays open, green a change.
s01-D06 · Decided (JL 261012: "gurantee which frame's information density"): principle ⑥, each frame's density
    is measured on every build, words per million px, and shown beside the frame; a thin frame is merged.
s01-D07 · Decided (JL 261012: "add a frame to b31-s01 about what are the skill folder for it"): frame ④, the
    skill folders that hold the principles, read from disk.
s01-D08 · Decided and built (JL 261012: "should we also have a excalidraw-studio?", then "Please go ahead and do it"):
    yes; built as `skills/1_base/excalidraw/excalidraw-studio/` 0.1.0 (SKILL.md, scripts/draw.py, a test), and
    haipipe-studio's "The look" now points to it (haipipe-studio 0.13.7). A skill `excalidraw-studio`
    beside excalidraw-report, -slide, -read and -section, owning how a Studio topic's drawing looks: these
    principles as its SKILL.md, the patterns (mind map, workflow of stages, screen, checked examples, folder
    tree for folders, the density badge, the key-point colour, the layout by the story), and one set of drawing
    helpers every builder imports. haipipe-studio keeps the topic: folder, face, numbering, sessions and the
    writer that keeps a person's marks (`canvas.write`). Why: today the look is split across haipipe-studio's
    "The look", excalidraw-report's scratch mode and `canvas.py`, every builder keeps its own helpers, and a
    rule written for s00 reached every topic (261012) because it lived in the skill that owns topics.
s01-D09 · Decided (JL 261012: "we should not put all the frames just always from left to right? it needs a better
    arrangement"): frames are laid out by the story's shape, a row, a grid or a branch, with a named arrow
    for each step between them; principle ③ says so. s01's own: two by two, ① → ② → ③, ① → ④.
s01-D11 · Decided (JL 261012: "I think this is very a good example, (except for the coloring)"): b10
    s52-host-and-share is the drawing to copy (acts, one idea a frame, maps with named arrows); its colouring is
    not. Principle ③ gains acts; ⑥ measures a map frame apart from a text frame.
s01-D12 · Decided (JL 261012: "where is the mind map frame for us to list all the principles summarized in the
    text?"): each branch of the mind map (①) carries a one-line `summary`, drawn large under its title, so the
    eight summaries around the centre read as the principles in text, even zoomed out; the details stay small.
s01-D13 · Decided (JL 261012: "I love the act things here as well, we can do it as well"): s01's frames are
    grouped into acts, a row each, the act named at the left (the `acts:` block); principle ③ says so.
s01-D14 · Decided (JL 261012: "I think we should have a new frame for the s00-background-and-index for it as well.
    s00 should also work in a way for the proposing the sNN and jNN as well"): frame ⑤ shows s00, the one drawing
    with its own shape: what `block_index.py` reads, what it draws, and what it proposes, topics (sNN, through
    `studio_proposals`, drawn today) and Jobs (jNN, through `job_proposals`, drawn since haipipe-studio 0.13.8), red and
    dashed until a person ticks them. b31's own s00 face proposes both.
s01-D15 · Decided (JL 261012: "for the s01, I asked so many times, where is the frame for showing the excalidarw
    principles????"): frame ① is "The Excalidraw principles", first and top left: each principle's title and summary
    in big words around one centre, details small; the same list heads this face. Before, it was titled "The
    principles: a Studio drawing reads as one story", its principles boxed among small details, unreadable zoomed out.
s01-D16 · Decided (asked 261012: "could you message the sessions b10-s05 s00 s51-s52-server-share to make them to
    follow the drawing principles"): after the three sessions redrew, frame ③'s s51 and s52 lines read check.py on
    every build: ⑥ against the floor of each frame's kind (s51's line said "under the text floor of 120", wrong for
    map frames), and a green line on what changed since. The pictures and the other verdicts stay that day's.
s01-D17 · Decided (asked 261012, on frame ④: "I think here we might have the excalidraw-job?"): excalidraw-job is
    the sixth skill, a Job as one drawing (b31 s06); frame ④ shows five drawing kinds, three a row, with a green line
    on the new one. The "keeps the topic" label now fits between the two boxes (it ran into the yellow one).
s01-D18 · Decided (found 261012 by the session that redrew b10 s52: a builder writing with `canvas.write`'s default
    palette lost every key point): haipipe-studio 0.13.14 adds `canvas.KEY` (#fff3bf) to the studio look;
    `apply_palette` keeps it and `off_palette` does not report it. Open 5 is settled, and b31 s00's proposed Job
    j02 (canvas-key-colour) was done without a Job. `Drawing.write` still writes with the palette off, so what a
    builder draws stays as drawn.
s01-D19 · Decided (asked 261012: "add at least of words, (especially the small versions as possible) when drawing the
    workflow", and "make the draft to be less of wordy and concise"; principle ⑦, excalidraw-studio 0.3.0): ① gains
    ⑦, five principles on the left and four on the right; each principle shows its title, its summary and an open
    point, none under 28 px, and its leaves stay in this face. ② keeps one short line per check (the principle it
    guards, who checks it) and drops the limits list, the density chart and the caught lines (they stay here); a
    check for ⑦ is added, and ④ is now flagged by check.py. ⑤ keeps the flow in short lines, b31's made topics in one
    line and each proposal in a red dashed box. ③'s s51 and s52 lines read ⑦ for a map. The drawing before is in
    history/ (261012). Open 6 settled.
s01-D20 · Decided (asked 261012: "have you aded s07 excalidraw-task and update it to hte s01 as well?"): frame ④ shows
    six drawing kinds, three a row: excalidraw-task (b31 s07) joins, with a green line; excalidraw-job's box says two
    frames, not four (261012)
s01-D21 · Stage → closed (JL 261012: "we can close s01 now and s00"). The seven principles are agreed and live in excalidraw-studio
    (0.3.2); this drawing follows them (0 ❌). Opens 1 to 4 settled, so the drawing shows no red open point. A new
    principle reopens this topic.
s01-D10 · Decided (JL 261012: "no need to put JL, it can be anyone"): a drawing names no one. A principle says
    when it was asked ("asked 261012"), a check says "a person"; who asked stays in the face's Decided lines,
    the record, never on the drawing.


Open
----

1. Settled 261012 (s01-D21): "as large as possible" is up to the screen limit (2800 x 1600); a long piece read down
   is one tall frame (`canvas.reads_down`); more than that is a second frame in the story.
2. Settled 261012 (s01-D21): the rules live in excalidraw-studio (its seven principles, `draw.py`, `check.py`), which
   haipipe-studio loads before it draws; `canvas.py` keeps the checks it runs when a builder writes.
3. Settled 261012 (s01-D21): no check in `canvas.write`; `check.py`'s ④ row counts folder-tree lines and asks a
   person whether they are real folders.
4. Settled 261012 (s01-D21): b31's board no longer excludes the look of a drawing; it names the seven skills.
5. Settled 261012 (s01-D18): `canvas.KEY` (#fff3bf) is part of the studio look since haipipe-studio 0.13.14;
   `canvas.write`'s palette keeps it.
6. Settled 261012 (s01-D19): ⑥ measures a text frame (at least 120 words per million px); a map frame is measured by
   ⑦ instead, at most 200 words and a quarter of them small, and the map floor of 70 is retired.
7. Settled 261012: excalidraw-studio was created (s01-D08).

(none open: closed 261012, s01-D21)
