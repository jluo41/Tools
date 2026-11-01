---
name: haipipe-studio
description: >-
  Owns Studio topics at every level (Project, Block, Job, Task; a page shows its own and its children's; one sNN numbering per Block): their faces,
  numbering, drawings, builders that preserve human marks, and session passes.
  Use to add or redraw a Studio topic, preview a drawing, or save a Studio session. Also covers
  proposal topics and s61-s69 slide drafts under their specific contracts.
  How a topic's drawing looks and reads is excalidraw-studio's: load
  /excalidraw studio before drawing or redrawing a topic (its principles,
  draw.py, check.py). Scripts: canvas.py, render_png.py, new_topic.py and topic_slides.py. Also the Page's Studio screen: one tab with the live drawing above
  the chat, and its lane contracts (ref/screen.md, chat.md, draw.md). Trigger: studio
  workbench, studio tab, page chat, keep this session, autodraw, chat and draw
  together, /workbench-studio (the retired name of this screen).
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "0.28.1"
  last_updated: "2026-10-31"
  # version history: ./CHANGELOG.md
---

# /haipipe-studio · the topics a Block owns

<!-- render b35-s01 first-principle: generated from Tools blueprints/Project-PageParts/work/b35_studio/s01-studio-skill/delivery/skill/first-principle.md; edit it there, then render_delivery.py -->
**Studio: from idea to delivery** (JL 261030). One topic, one idea, one delivery: a topic starts as one open idea
and ends in what it hands over, a deck, always, and the thing the deck is about (skills or code, a figure, a draft).
Its face names that delivery first, in its `**For:**` line.

## First principle: a Studio is never a report

JL 261029: "studio 一定要切记 不要把 studio 写成一个中规中矩的 report 啊 ... Studio 的这个 First principle 就是这个".
A Studio is where an idea is still open. Report says what was found and how far the work is; the Studio shows what
we are still thinking.

1. **Ideas, not status**: show the open question, its options side by side, which way we lean, and what is unknown.
2. **Divergent**: two to four options, a "what if", a sketch; never one tidy list of what was done.
3. **Pictures first**: a drawing, a mind map, an illustrated slide (style `sketch-notes`, JL 261029); few words on each.
4. **No bookkeeping on screen**: decided, started, counts and dates belong in a round's record and in Report.
5. **When it settles, it leaves**: an agreed idea goes to its delivery, through Work; the Studio keeps the next open one.
6. **It must pull you in** (JL 261029: "打开之后必须能够足够吸引人去 explore ... 如果做不到的话 这个 studio 做得就
   不好"): a drawing, a mind map or a slide, opened, catches the eye in seconds and makes a reader want to explore.
   One clear focal point, a picture before words, a question the reader wants answered. A wall of text, a table
   of rows or a grid of equal boxes fails, however correct. The attract test (`ref/reader-review.md`) comes first.

```text
Studio: "What is a Block?"  A topic │ B stage │ C promise to a reader (leaning) │ still open: …
Report: "Q01 answered: a Block is one delivery for one reader."
```
<!-- /render b35-s01 first-principle -->

<!-- render b35-s01 where-it-sits: generated from Tools blueprints/Project-PageParts/work/b35_studio/s01-studio-skill/delivery/skill/where-it-sits.md; edit it there, then render_delivery.py -->
There is no `studio/` folder: each topic is an `sNN-<topic>/` folder that sits directly beside the Jobs or Tasks of
the level it serves, a Block's beside its `jNN_` folders, a Job's beside its `tNN_` folders, a Task's beside `runs/`
(b35 s01-D12, JL 261030: "we just have sNN, along side with jNN, to make it visible directly"). Which level: the one
that uses its delivery. The count is capped per level (JL 261030: "we might have many sNN, but we need to control the
numbers"): at most **9 at a Block, 5 at a Job, 3 at a Task**; more means the level is really two. A page shows its own
topics and its children's. An older Block's `sNN-<topic>/` still reads, until it is moved. A topic's address is `bNN.jNN-sNN` (dots for the ladder, a hyphen before the topic:
`b17.j01-s07`, s01-D02), always followed by its names, `b17-s04:theme_work @ workbench_page_structure`,
`b17.j01.t03-s09:theme_work.tables.cut @ which_cut_first` (s01-D03, `frame.topic_label`): never an address alone. `new_topic.py topic <Block, Job or Task>` puts the topic in that folder and refuses one past its level's limit (`--over-limit` to add it anyway). Each topic has a drawing to think on
together and a short face that says what it settles and which Questions it feeds. This skill owns the folder, the face, the numbering, the builders that
keep a person's marks, and the sessions. How a topic's drawing looks and reads is `excalidraw-studio`'s: load
`/excalidraw studio` before drawing or redrawing a topic (its principles, `scripts/draw.py` to draw with,
`scripts/check.py` to check); a report's drawing is `excalidraw-report`'s.

```text
<Block, Job or Task>/sNN-<topic>/
├── sNN-<topic>.md            Topic · Feeds · Files · Decided · Open
├── sNN-<topic>.excalidraw    the drawing (a builder's, with the person's marks kept)
├── sNN-<topic>.png           its preview
├── build_sNN_<topic>.py      the builder, when a script draws it
├── sNN-<topic>.mindmap.md    its structured side, the mind map: Markdown, drawn as the §1 map (haipipe-mindmap)
├── sNN-<topic>.ideas.md      its open ideas: a question, its options, the leaning, what is unknown
├── slides/idea-NN-<slug>.png  one picture per idea (haipipe-display _parts/slide, its deck's style; source)
├── sNN-<topic>.slides.json   the record: "style" (default sketch-notes), then per idea: content, image, notes
├── sNN-<topic>.slides.html   the deck to look at, one picture a slide (generated, git-ignored)
├── sNN-<topic>.slides.pptx   the same as PowerPoint, notes as speaker notes (generated, git-ignored)
├── passes/pNN-<MMDD>/        one round each: a working session or a meeting (pass.md)
├── result/                   its own working output: mock pages, trial pictures, extra drawings and builders (b17
                              s01-D06); messy is fine. A Task Run's output stays in that Run's result/, shown here
└── delivery/                 the agreed version: deck/ (its slides, they stay here) and the thing it hands over;
                              render.yaml says where each piece goes, render_delivery.py writes it there
```

An sNN hands over through its own `delivery/` (JL 261030: "studio/sNN/delivery, this is the delivery, and then we do
the render, to render the delivery out, to that area, like the haipipe-studio"). Two steps: the agreed, clean version
goes into `delivery/` (never `result/`, which is messy by design), then a render writes it out to where it is used. A
text piece (a skill's section, a Section's draft) lands between `<!-- render <address> <block> -->` markers in its
target, a region nobody edits by hand; a code piece is built by the Task that `render.yaml` names; the deck stays in
`delivery/deck/`. `python $S/render_delivery.py <sNN>` checks every piece, `--apply` writes the ones that differ.
<!-- /render b35-s01 where-it-sits -->

Read `ref/topic-contract.md` before adding a topic or writing a builder.


Two sides of a topic: its drawing and its mind map
--------------------------------------------------

Every sNN has two sides, linked by number (JL 261026): the free drawing, `sNN-<topic>.excalidraw`, and its mind map,
`sNN-<topic>.mindmap.md`. The mind map is not a canvas: it is drawn the way a draft Task's §1 Structure map is
(HTML, the root at the left, each node's children to its right), and a person edits it where they read it. The
workbench card switches the two (Free · Structured).

```text
s01-work-ladder/
  s01-work-ladder.md           the face ─── from-topic ──▶ s01-work-ladder.mindmap.md   the mind map's source
  s01-work-ladder.excalidraw   Free                        drawn as §1's map ◀── Structured: click, type, ＋, drag
```

1. **Made together**: `new_topic.py topic` writes the face, then starts the mind map: its root, its Files and a note
   that it is not written yet.
2. **Kept in step**: haipipe-mindmap's `scripts/mindmap.py refresh <sNN-topic>.mindmap.md` rereads the face; words a person changed
   and nodes a person added stay.
3. **Edited in place**: a change on the card is one POST to `/_board/mindmap`, written into the `.mindmap.md`.
4. **The rest**: the grammar, a Block's or a world's work map (`from-work`), the commands:
   [`../haipipe-mindmap/SKILL.md`](../haipipe-mindmap/SKILL.md), the skill that also draws a draft's §1 map.


<!-- render b35-s01 how-many: generated from Tools blueprints/Project-PageParts/work/b35_studio/s01-studio-skill/delivery/skill/how-many.md; edit it there, then render_delivery.py -->
How many sNN per level
----------------------

At most **9 sNN at a Block, 5 at a Job, 3 at a Task** (`new_topic.py` `LIMITS`). This counts topic folders at that
level, not the largest number: s51 can be one of a Block's nine. Keep each topic about one delivery. Before adding one
past the limit, reuse a related topic, put it on the Job or Task that uses its delivery, or split the level; existing
topics keep their ids and files. A topic is numbered free across the whole Block (Block, Jobs and Tasks share one sNN
numbering).
<!-- /render b35-s01 how-many -->


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


Where a topic opens
-------------------

A topic has no page of its own (JL 261031: "first we will remove the single page for the studio"; b35-s02-D05). Every
link to it, the left rail's sNN and an old `?path=…/sNN-<topic>&layout=focus` link, opens its card in its level's
Studio section, under its group, outlined (`focus_page.py` `topic_home`; the server sends an old link on with a 302).
The card's name and line open the face, its picture the slide, and Slide, Draw, Mind map, Work and Delivery pop out
over the page. A builder's page in `delivery/` (`focus_page.static_page`) wears the workbench frame, its path ending
at that card.


Groups
------

A topic's groups are its `**Tags:**` line. The workbench's Studio row edits them: `+ Group`
names one, dragging a card onto a group adds the tag, × on a card's group (shown under the
mouse) takes it out, × beside a group deletes the tag from every topic. `_studio_groups.txt` (an older Block's `studio/_groups.txt`)
keeps the Block's groups in button order, empty ones included; dragging a group sideways
rewrites it. Both are plain text: edit them by hand when that is quicker. Current is the
person's own and stays in the browser (b10 s02-D16, D17). Related, folded under the topics, has
the same bar: there an item's groups are its subfolder (`meetings/` → meetings) and the names in
its row's `group` cell of `related/related.md`, and `related/_groups.txt` keeps their order (JL
261011); `haipipe-related` owns that folder.

Runs, folded under Delivery, lists every hard Run (`runs/rNN_*`) of every Task under the Block, Job → Task, each
with its mark, status and finish day, and a tally per Job and Task (JL 261019; b10 s06-D07). It reads the Runs'
receipts; nothing is written for it.

Timeline, folded under Runs, shows what moved when on one axis down the page, the oldest day at the
top, at three levels (Days · Topics · Everything), and follows the same bar (JL 261011; b10 s08). It reads only what a topic keeps: a decision's date in its brackets (`sNN-DNN · …
(JL 261011)`), a session's pass `pNN-<MMDD>`, a drawing's green `✎ <YYMMDD>` notes. A decision with no
date is left off it (b10 s08-D10), so date every decision.

Folder, folded under Timeline, shows the Block's own folder as one tree (JL 261012; b10 s09): a folder says how many
things it holds and what it is for (a shared name's fixed line, a Run's card, else its face's title), a file opens in
the pop-out. Nothing is written for it; a topic's folder is listed like any other.

Numbering
---------

```text
s01-s09 concepts · s11-s19 levels · s21-s29 runs and skills · s31-s39 Guide · s51-s59 server
s41-s49 Task procedures: one per Task type of a theme, sNN-task-<type>-procedure (b15, JL 261014)
s61-s69 slide drafts: a proposed deck, its logic flow and its slides, before the deck is built
s10-s19 a paper Board's related work: s10 the map, s11-s19 one type each (haipipe-paper-related); a paper
        Board draws no level topics, so the band is free there (JL 261019)
```

The next free number in the band; a number is never reused, unless a person asks for it back (b10 s09, 261012):
then the new topic's decisions start after the old ids still kept where the old topic merged, and the old
`runs/run-draw-<sNN>/` moves into that topic's `history/`, so the Timeline does not read it as the new one's.
No s00 (retired 261029)
-----------------------

A Block has no `s00-overview/` any more (JL 261029: "以后像这种东西可能就不大有用了 我就直接把它删掉吧 ...
我们这个 mini map 这不算 overview 吗？"). The workbench's Report › MindMap draws the Block from disk on every open:
what it must find out with each answer, its Jobs and Tasks, its topics. So a background and index drawing only went
stale beside it. An old `s00-overview/` is deleted, with its `runs/run-draw-s00/`; git keeps both. Numbers start at
s01, and a number s00 gave up is still never reused.


<!-- render b35-s01 one-delivery: generated from Tools blueprints/Project-PageParts/work/b35_studio/s01-studio-skill/delivery/skill/one-delivery.md; edit it there, then render_delivery.py -->
One topic, one idea, one delivery (261030)
------------------------------------------

A Studio runs from idea to delivery (JL 261030: "studio: from idea to delivery"; "one studio, one idea and one
delivery"). Each topic, s01 as much as s07, holds one idea and ends in its own delivery, named first on its face
(`**For:**`, "so one studio should link to a delivery, this is the outcome oriented"). A Block's delivery is its
topics' deliveries together, listed in its `board.md` `## Deliveries`.

The thing is **one clean thing of one type**: a skill, a draft, a display, workbench code, a data table, a server
package (JL 261030: "so each studio with a clear delivery, right? either skills or draft, or display"). A mixed
delivery is several sNN, one per type; no clean delivery, no sNN ("is the delivery is not clean or is not one type, we
will not treat it as a studio"). b35 went from seven sNN to three this way (b35 board.md `## Deliveries`).

Its face says which type in one word, the `**Delivery type:**` line under `**For:**` (JL 261030: "for each delivery,
we should also say what is the type, give the main delivery type"; "we should also add this to the skill, that what
type of delivery we want to render"). The deck is never the type, since every sNN has one. The type says what
`delivery/` holds besides `deck/`, and how `render.yaml` hands it over; the workbench shows it on the sNN's card,
beside its stage:

```text
type     delivery/ holds             render.yaml hands it over as
skill    skill/ text pieces          from: to: block:  render_delivery.py writes them into SKILL.md or ref/
ui       ui/ screen drafts           code: by:         a Task builds the screen in the workbench
code     the package's agreed spec   code: by:         a Task builds it (a script, a server package, an algorithm)
draft    web/ latex/ word/           from: rendered_by: the Theme's skill builds the Word, PDF or LaTeX
display  figure/ table/ slide/       from: rendered_by: haipipe-display renders the figure or table
data     the table's contract        code: by:         a Run writes the table to its store
```

A delivery is a deck, always, and the thing the deck is about (JL 261030: "delivery could be: slide (a must) and the
associated skills, code, or figures, draft, etc."). The thing gives the topic its kind and its first question (b35-s01, a scan of every `studio/` topic and `delivery/`
folder in the eight SPACEs, 261030):

```text
every topic      deck (slides)          a must: what a reader takes away, in pictures
story            story, Section plan    the claim, for which reader (a paper's Block)
question         report page            what answers it
table contract   data table             what one row means
display          figure                 what the figure shows
paper version    full paper, Word, PDF  what this send holds (a paper's version Job, assembled)
section          written Section        what this Section must say (a paper's draft Task)
label contract   schema, label contract what one label means (a labeling Job, b15 s13)
items, building, scanning, score       a labeling Task's own: item set · signed Label Handoff · final labels · score
run plan         server package, code   which Runs, in what order
design           skill, tool change     what the tool should do
algorithm        algorithm code, tuner  its forward, loss and metric (hainn L1-L2)
ask              letter, meeting note   what we need from whom
```
<!-- /render b35-s01 one-delivery -->


<!-- render b35-s01 themes: generated from Tools blueprints/Project-PageParts/work/b35_studio/s01-studio-skill/delivery/skill/themes.md; edit it there, then render_delivery.py -->
One Studio, every Theme
-----------------------

The Studio is the same in every Theme (JL 261030: "how could the haipipe-studio skill will be adopted to different
theme?"): an sNN beside the Jobs or Tasks it serves, its face (`**For:**`, Covers, Excluded), its drawing in five
parts, its `delivery/`, and a render out. A Theme plugs in by three things only: the kinds of delivery its sNN make,
where the render writes, and which skill renders. The Theme's own skill renders; haipipe-studio never builds a paper,
a label set or a release itself.

```text
Theme      an sNN delivers (Block · Job · Task)                      render writes into               rendered by
work       skill design · table contract · display, a figure         a skill, the workbench, a store render_delivery.py, a Task
paper      story · paper version · section                           the Section page, manuscript    haipipe-paper-assemble
display    a figure or table, its slide rules                        the page's displays             haipipe-display
labeling   label contract · items, ground truth, building, scanning,  the labeling Job                haipipe-labeling
           score
design     design goals · design Job · reason ideas, one design,      designs.json, the release       haipipe-design-delivery
           review whole
insight    question map · analysis plan, a release on a freeze ·      the Design handoff              haipipe-insight
           Data, Information, Knowledge, Wisdom
discovery  a question's evidence · a paper's card                     the evidence Bib                haipipe-discovery
cowork     ask, a letter or meeting note                             sent to a person                a person, haipipe-cowork
```

In `delivery/render.yaml` a piece is one of three: a text piece (`from:`, `to:`, `block:`), written between render
markers by `render_delivery.py`; a code piece (`code:`, `by:` a Task); or a Theme piece (`from:`, `rendered_by:` the
Theme's skill), which `render_delivery.py` only reports, since the Theme's skill builds it (the paper's manuscript, a
designs.json release).
<!-- /render b35-s01 themes -->


A Job's current results (s21-s29)
---------------------------------

Each Job gets a topic that shows what its Runs have produced so far (JL 261012: "for each jNN, make the sNN to
show what are the current results"). It lives in the Job's own `studio/` (JL 261028; excalidraw-job `make` writes it there), in the runs band, and the
Block's page shows it with the Job marked; older ones in the Block's `studio/` still work. `scripts/job_results.py` makes it and its builder redraws it:

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
X=Tools/plugins/haipipe-toolkit/skills/1_base/excalidraw/excalidraw-studio/scripts
python $S/new_topic.py topic <level> --slug <topic> --title '<title>' --band run [--feeds q01_x] [--builder]
python <block>/sNN-<topic>/build_sNN_<topic>.py          # redraw: the person's marks are kept
python $S/render_png.py <drawing>.excalidraw <drawing>.png        # the preview
python $X/check.py <drawing>.excalidraw                            # against excalidraw-studio's principles
python $S/new_topic.py session <block> sNN --title '<session>' [--ask …] [--summary …] [--changed …]
```

0. **Draw with excalidraw-studio**: before drawing or redrawing a topic, load `/excalidraw studio` (the Skill
   tool) and follow its "Redraw a topic with the principles"; a new builder (`--builder`) already starts on its
   `draw.py`, and `check.py` says what still breaks. This skill keeps the folder, the face and the sessions.
1. **Face marks**: `**Stage:**` (explore · shaping · agreed · closed), `**Topic:**`, `**Feeds:** qNN_<topic>`,
   `sNN-DNN` decisions, a numbered Open list. A person moves the stage; see `ref/topic-contract.md` § The face.
2. **Builder**: draws through `canvas.write`; never hand-edit its output, change the builder.
3. **Marks kept**: what a person adds, edits or deletes survives a rebuild (the seed snapshot).
4. **Round**: each working session or meeting is one `passes/pNN-<MMDD>/pass.md` inside the topic: Notes, Decided,
   Started (what it sent to Work), Read (from `related/`), Changed. `new_topic.py session` writes it.
5. **Changes**: red for open; every change to a drawing gets a short green note where it changed.
5b. **A data topic** (`**Delivery type:** data`): its own five_parts builder, whose first Design sketch is the data
   built step by step, a small table per step with its real columns and made-up rows (JL 261031: "what is the
   physical data"); excalidraw-studio § A data topic, `five_parts.data_table` and `data_step`. Start by copying an
   example builder (b63.j01-s01 or s02), not `new_topic.py --builder`, which still starts an old draw.py builder.
6. **Read it as a reader, then a reviewer** (JL 261012: "after you create such a draw, you should ask it yourself,
   If I am a reader, will this answer my questions for this job etc. Maybe you need to call a reviewer for it as
   well"): `check.py` passing is not done. Answer the reader's questions for the topic's kind (Job, Task, video or
   Run frame) from the rendered frames alone; then call `haipipe-studio-reviewer-agent` in a fresh context, fix
   its gaps in the face or the builder, and repeat until it returns `answers`. The questions and the loop:
   `ref/reader-review.md`.


The look
--------

**How a topic's drawing reads now lives in `excalidraw-studio`** (`skills/1_base/excalidraw/excalidraw-studio/`,
agreed on b31 s01-drawing-principles, 261012): its principles (one frame as large as a screen; a workflow
map or a mind map inside; the frames as one story, in acts, joined by named arrows; a folder tree only for real
folders; big words and one slight colour for the key point; each frame's density measured; few words in a
workflow, fewest small ones) and its drawing
helpers, `scripts/draw.py`. Read it before drawing a topic. This section keeps what `canvas.py` enforces when a
builder writes; where the two differ (a mind map instead of a tree), follow `excalidraw-studio`. The slight
key-point colour is part of the look since 0.13.14: `canvas.KEY`, kept by the palette (b31 s01-D18).

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
   each.
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

A topic that works on one section of a proposal or a paper copies b21_event_cgm's s03 (SHIFT Task 2.1;
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

A topic is the discussion itself, so it has no soft Run of its own any more (JL 261029: a Studio is the
discussion; its rounds live with it). Its rounds are `passes/` inside it; an old `runs/run-draw-<sNN>/` stays readable
until it is moved in.

| What it does | where | how |
|---|---|---|
| add a topic | `<level>/sNN-<topic>/` | `new_topic.py topic` |
| render its delivery | where each piece is used (`delivery/render.yaml`) | `render_delivery.py <sNN> [--apply]` |
| count the galleries | every sNN and every `delivery/` in the SPACEs, by level, Theme and kind (names only) | `gallery_scan.py` |
| update the existing sNN | each sNN against today's rules (audit), the plan (update), the mechanical steps and the five-part drawing, the old drawing kept whole (update --apply); an agent's For and Delivery type (brief, name, name-batch); an sNN still in studio/ listed for the move | `studio_update.py audit\|update [--apply]\|brief\|name\|name-batch` |
| move sNN out of studio/ | each `sNN-<topic>/` to beside its Jobs; a link rewritten only when its path leads to a moving topic, never in result/, passes/ or _old/; relative climbs and builder `parents[N]` rewritten; a studio/ left with only `_groups.txt` goes (`_studio_groups.txt`) | `studio_move.py <path> [--apply]` |
| redraw a topic | the topic's drawing | rerun its builder, then the preview |
| save this session or meeting | a round, `passes/pNN-<MMDD>/` | `new_topic.py session [--kind meeting]` |
| rebuild its slides | `sNN-<topic>.slides.html` and `.slides.pptx` | `topic_slides.py <topic>` (a round rebuilds them) |

In the Studio of the topic's own level (Block, Job or Task; JL 261028); a Job or Task input finds the topic in its own
folder first, else wherever it lives in the Block.

The life of a topic: `**Stage:**` explore → shaping → agreed → closed, moved by a person; each round may move it. The
workbench's Studio row shows the four words with the current one marked, the number of rounds, and the last round's
Decided and Started.


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
| `haipipe-studio` | the topic folder, its face, numbering, builders and their writer, previews, sessions; the Page's Studio screen (`ref/screen.md`) |
| `excalidraw-studio` | how a topic's drawing looks and reads: its principles, `draw.py`, `check.py`; loaded before drawing |
| `excalidraw-job` | a Job as one topic: why, in and out, what it concluded, its tables; reads `job_results.py`'s readers |
| `excalidraw-report` | a report's drawing and a scratch: their modes, elements, plot kit, pictures |
| `haipipe-report` | a report's own drawing, built from studio frames its `## Figures` lists |


The Studio screen
-----------------

The Page's Studio tab is this skill's too (folded in from the retired `workbench-studio`, 2026-10-16, s21-D05):
one tab with the live Excalidraw editor above the chat, so the scene the chat redraws changes in front of the
person talking. `ref/screen.md` is the screen manual (load `workbench` first); `ref/chat.md` and `ref/draw.md` are
its two lane contracts, `ref/workbench-table.md` its table. The code is `servers/workbench/`. The old name
`/workbench-studio` still triggers this skill.


Files
-----

```text
haipipe-studio/
├── SKILL.md
├── CHANGELOG.md
├── agents/openai.yaml
├── ref/topic-contract.md      the folder, face, numbering, builders, sessions, buttons, a proposal topic
├── ref/infer-topics.md        topics inferred from a Block's Jobs and Tasks (b10 s10)
├── ref/screen.md              the Page's Studio screen: drawing above, chat below
├── ref/chat.md · ref/draw.md  the screen's two lane contracts
├── ref/gallery.md            the studio gallery: every kind of sNN, the newest real one each (b35-s05)
├── ref/workbench-table.md     the Studio screen's table
├── ref/history/               the retired workbench-studio changelog
├── scripts/canvas.py          the merge-safe writer
├── scripts/render_png.py      the offline PNG preview
├── scripts/new_topic.py       topic (its face, then its mind map) · session
├── scripts/block_inventory.py what a Block's Jobs and Tasks already do: kinds, splits, sub-questions
├── scripts/topic_map.py       a topic's frames from its face: trees, or boxes with their trees joined by named arrows
├── scripts/job_results.py     a Job's current results as a topic, read from its Runs on every build
└── tests/test_haipipe_studio.py
```
