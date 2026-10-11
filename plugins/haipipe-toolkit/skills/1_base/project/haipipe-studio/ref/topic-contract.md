# The topic contract · studio/sNN-<topic>/ at any level

Read before adding, redrawing or saving a studio topic, or writing a builder. The Idea
Studio of every level (Block, Job, Task) is its `studio/` folder: one topic per folder,
each a drawing to think on together and a short face that says what it settles. How a
drawing should look (a dense scratch, a plain design prototype, a report picture) is
`excalidraw-report`'s; this contract is the folder, its face, its builder and its sessions.

## The folder

```text
<level>/studio/
├── sNN-<topic>/
│   ├── sNN-<topic>.md              the face: Topic · Feeds · Files · Decided · Open
│   ├── sNN-<topic>.excalidraw      its drawing (the first one the Idea Studio shows)
│   ├── sNN-<topic>.png             its preview (render_png.py)
│   ├── .sNN-<topic>.seed.json      the builder's last drawing: what canvas.write compares with
│   ├── build_sNN_<topic>.py        the builder, when a script draws it
│   └── history/                    older builders or drawings kept on a redesign
├── _build/                         the level's shared builder helpers and make.sh
└── <loose>.excalidraw              a loose drawing: its own topic
<level>/runs/run-draw-<sNN>/        the topic's soft Run: one pass per working session
```

1. **One topic, one folder**: a topic is a question being thought through, not a picture.
2. **At any level**: a Block's `studio/` holds what the whole Block shares; a Job's or a
   Task's holds its own. A report's own drawing goes in its report folder (`haipipe-report`).
3. **Its drawings**: the first `.excalidraw` is the one the Idea Studio opens across the row;
   more are links beside it. A topic with a builder opens view only; one drawn by hand edits
   in place.

## Numbering

```text
s01-s09   concepts          what the level is, its trees and words
s11-s19   levels            Block · Job · Task, one topic each
s21-s29   runs and skills   the Runs, the buttons and the skills that own them
s31-s39   Guide             the theme's Guide: Description · Method · RoadMap Draw · Related Paper
s51-s59   server            how the screens are served
s61-s69   slide drafts      a proposed deck: its logic flow and its slides, before the deck is built
```

1. **Next free in its band**: `new_topic.py --band <band>` takes the lowest free NN there.
2. **Never reused**: a number stays with its topic; a renumbering is written into the face
   of the Block (a "Renumbered" note), never done silently.
3. **Two digits**, then a dash and a short kebab topic: `s21-run-skill`.

## The face

```text
sNN · <title>
=============

**Topic:** <one paragraph: what this topic thinks through, and why now>

**Feeds:** `reports/` qNN_<topic> · qNN_<topic>

Files
-----
(a tree of the folder)

Decided
-------
sNN-D01 · <what was decided> (<who> <date>)

Open
----
1. <an open point>
```

The Idea Studio reads the face by these marks, so keep them:

1. **`**Topic:**`**: its paragraph is the row's one line.
2. **`**Feeds:**`**: every `qNN_<topic>` named there becomes a chip on the row, and the
   topic is listed in that Question's row under "from the Idea Studio" (`haipipe-report`).
3. **Decided**: each line starting `sNN-DNN` counts as one decision.
4. **Open**: each numbered line under the `Open` heading counts as one open point.
5. **ASCII headings** (`===`, `---`), as every doc here.

## The look

Trees, lines and boxes in black; red only for an uncertain or open question; green only for a change
we made, where we made it (JL 261007). No other colour and no fills: `canvas.INK`, `canvas.RED`,
`canvas.GREEN`. `canvas.write` enforces it on what the builder draws (`apply_palette`: any other
stroke becomes black, a fill transparent; images, transparent strokes and the person's own marks
are left alone; a slide draft s61-s69 is left as drawn, or pass `palette=`), and
`canvas.off_palette(els)` lists anything off it. A scratch's sticky
colours and a design scratch's coloured panels are not used in a studio topic; a report drawing's
plots and figures are `excalidraw-report`'s. One exception, inside a slide of a slide draft (below).

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
cut into frames "· 1", "· 2", and `canvas.write` warns about each.

## A proposal topic: one section, drawn so it can be written

A topic that works on one section of a proposal or a paper draws five frames in two rows. The worked
example is b03_event_cgm's s03 for SHIFT Task 2.1 (JL 261010, on its drawing: "I think this one is very
very great!"). The first row is the thinking, each frame one screen; the second row is the long reads,
each one frame that grows down (`canvas.reads_down`).

```text
row 1   ① the idea workflow        ② why and the plan        ③ the proposal figure
          one screen, one flow        one screen                one screen, caption beside
row 2   ④ the draft today, marked up        ⑤ the section written out
          one frame, read down                one large frame, read down
```

1. **① The idea workflow**: one connected flow from the inputs through the steps and the model to its
   use, every loop drawn closed (in s03 the data loop, the model-improvement loop, and the red loop that
   stops when there is no gain). The checks that would show it works sit beside it; each open question
   is red, inside the box it is about. The words are cut short until it fits one screen.
2. **② Why and the plan**: the lab's own papers it builds on (each one's status and what it gives this
   section), a small sketch of what the model sees, and the plan in order.
3. **③ The figure**: the proposal's picture, its change notes and caption in a column beside it.
4. **④ The draft today, marked up**: the shared draft is only read, printed to PDF, and each related
   passage is cut from its own page in the draft's order. A numbered red box on the passage, an arrow to
   a note: its title, `Change:` the wording we propose, `Why:`, and in red `Ask the team:` with the name
   of who can answer. The frame closes with every open question again, by who can answer.
5. **⑤ The section written out**: every part of the template as a section map read left to right:
   paragraph (its job), point (role and gist), Text (our wording), Evidence. Rules below.

The section written out (JL 261010: "the bullet points should be close to each other, and in the right
side, the evidence can be free style and be multiple columns, and use the lines to connect to the text"):

1. **Tight text**: text rows sit 8 px apart; the evidence never pushes them apart.
2. **Free evidence**: cards in two columns on the right, each beside the first text it supports; a line
   joins text and card and goes around other cards, never through one.
3. **No long lines**: a later text more than about one screen (1,400 px) from its card gets a one-line
   card naming the item ("full card above") instead of a long line.
4. **The card**: `E<nn> · VALUE|CITE|DISPLAY · label`, what it needs, where it comes from. Black when
   traced to a published paper or a repo file; dashed red while it waits, with its ask and who answers.
5. **The figure is evidence**: a DISPLAY item whose full card holds the picture and its caption, at the
   figure's own row. The frame closes with every waiting ask, by who can answer.

Where the words live: every word is in the face, in yaml blocks the builder reads (s03: `idea`,
`workflow_figure`, `draft_changes`, `task21_section`, `task21_evidence`); the builder only lays them out,
so a wording change is a face edit and a rebuild. A draft change finds its passage by `anchors` (a start
and an end phrase, each found exactly once in the draft): when the draft is edited the boxes move on the
next rebuild, and a phrase found twice or not at all stops the build. The written-out section prints its
word count against the template's page budget. Our wording reaches the shared file by a person, never by
an agent.

What went wrong on the way, so it is not done again (all JL 261010, on s03):

```text
❗ one 9,200 x 5,650 px idea frame        "This is too huge"            ✅ fits one screen
❗ the whole drawing scaled to 20%         words 6 px, 3 px at 50%       ✅ words stay 20 px
❗ the written-out cut into 9 frames,       "should be one large frame"   ✅ one frame, read down
   the draft into 4
❗ evidence stacked under each point       text rows spread apart        ✅ evidence laid out on its own
```

The builders to copy from (WellDoc-SPACE, `examples-0-cowork/Project-SHIFT-Study/cowork/b03_event_cgm/studio/`):
`s03-related-work-structure/idea_frame.py` draws ① and ②; `draft_pages.py` ④; `task21_section.py` ⑤, with
its line routing (`evidence_route`); `build_s03_related_work_structure.py` reads the face and the draft,
draws ③ and sets the rows; `_build/draw_kit.py` and `_build/word_pdf.py` are the level's helpers.

## A slide draft (s61-s69)

A topic that proposes a deck before it is built: `studio/s6N-<deck>/` with its face, one `slides.py`
(the ONE source), its builder, its drawing, `build_deck.py` and the deck in its own `delivery/`. The
studio writer leaves its colours as drawn (`canvas.is_slide_draft`). Its drawing contract (frames left
to right, the half-size slide skeleton, the accent inside a slide, the fields of `slides.py`, the deck
writer) is `excalidraw-slide`'s `ref/slide-draft.md` (moved there 261007, words kept).

## Drawing with a builder

A builder draws the topic from what is on disk, so a rebuild follows the code and the files
while keeping everything a person drew.

```python
sys.path.insert(0, str((HERE / "<relative path to haipipe-studio/scripts>").resolve()))
import canvas
canvas.write(out, els, "build_sNN_<topic>.py", redraw_frames=())
```

1. **canvas.write** gives each element a stable id from its content and merges with the canvas
   on disk against the last build's snapshot (`.sNN-<topic>.seed.json`, beside the drawing):
   anything the person added stays; a seed element the person edited stays; one they deleted
   stays deleted; every other seed element is redrawn. Frames are layout: the builder owns them.
2. **Check before regenerating**: a person's edits are detected by the snapshot, never by
   Excalidraw's `version` field (a save re-stamps them all).
3. **Never hand-edit the output**: change the builder or what it reads, then rerun it.
4. **Preview**: `render_png.py <drawing> <png> [scale]` draws a PNG with Pillow; Excalidraw
   shows the real drawing.
5. **A Block's make.sh**: `studio/_build/make.sh` reruns every builder of the level and every
   preview, so one command rebuilds the whole studio.
6. **Marks**: an open point drawn in red. Every change to a drawing, asked for or found on a
   redraw, gets a short green note right where it changed (`✎ <YYMMDD> <what changed>`, made by
   `canvas.change_note`) and the same line in the title frame (JL 261007: "leave the short green
   comments to where we changed"). Old notes stay; a note goes only with the thing it marks. A slide
   draft keeps a note about one slide only under that slide (`excalidraw-slide`, JL 261008).

`new_topic.py topic … --builder` writes a builder of this shape and runs it once.

## Sessions

A working session on a topic (a chat that redrew it, a person's round of marks answered) is
one pass of the topic's soft Run, `runs/run-draw-<sNN>/` (`haipipe-run`): the Run is made on
the first session, and each session adds `passes/pNN-<MMDD>/pass.md` (its title, its ask, a
summary, what it changed). The Idea Studio counts them on the row and lists them in the Runs
panel under `run-draw-<sNN>`. Older `chat/` summaries in a topic folder stay readable.

## The buttons

One button, `run-draw-<sNN>` (the frame names a button by its Run); its cards are the topics' Runs.

| What it does | Run | how |
|---|---|---|
| add a topic | `run-draw-<sNN>`, new | `new_topic.py topic <level> --slug … --title … --band …` |
| redraw a topic | a pass of `run-draw-<sNN>` | rerun its `build_*.py` (or draw by hand), then the preview |
| save this session | a pass of `run-draw-<sNN>` | `new_topic.py session <level> sNN --title …` |

## The scripts

```text
scripts/canvas.py        the merge-safe writer (moved here from a design Block's studio/_build/)
scripts/render_png.py    the offline PNG preview (moved the same way)
scripts/new_topic.py     topic · session
```

Every builder imports these from here (the copies in a design Block's `studio/_build/` are
retired). A Block that still keeps older snapshots by stem in a folder of its own
(`.<stem>.seed.json`, from before snapshots sat beside their drawings) can append that folder
to `canvas.LEGACY_DIRS`; better, move each snapshot beside its drawing.
