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
