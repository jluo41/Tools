---
name: excalidraw-report
description: >-
  Draw in Excalidraw, in one of two modes. A scratch: a sketchy whiteboard packed with the
  real material of a question (or, for design work, its concepts with placeholders), laid
  out as loose clusters, sticky notes, arrows and red marks, with the questions in a frame,
  seeded by a script in studio/_build/ that never overwrites what the person drew, and a
  comment loop on the canvas. A report drawing: a report's answer and its evidence (values,
  plots from a native plot kit, tables, embedded source figures, the logic), one drawing per
  report with named frames, linked from its Evidence. Use for a scratch, a working drawing,
  "draw it so we can think", "too structured", a report's picture, plots, /excalidraw-report.
allowed-tools: Bash, Read, Edit, Write, Grep, Glob
metadata:
  version: "0.8.2"
  last_updated: "2026-10-09"
  # version history: ./CHANGELOG.md
---

# /excalidraw-report · a dense scratch to think on together

The drawing is a whiteboard the person and the agent both work on, not a finished slide.
It holds a lot of real information and leaves the shape open, so the person can move
things, circle them, cross them out and draw their own idea next to them (JL 261005: "too
structure, make the human's creativities to be limited"; "I want the intensive information
level"). The earlier failure was the opposite: a neat template of labelled boxes, "beautiful
but meaningless outlines".

```text
real material  ─▶  loose clusters on one canvas  ─▶  the person draws on it  ─▶  reseed keeps their marks
(disk, skills,      stickies · trees · excerpts ·      moves, marks, crosses,      only untouched s- elements
 receipts, runs)    marks · arrows · open questions    adds their own              are redrawn
```


What makes a good scratch
-------------------------

1. **Dense with the real thing, at the right level.** First ask what the drawing is about.
   A **design scratch** (how skills, levels or contracts should work) is a prototype: its
   material is the concepts, each with its contract (folder pattern, what it must hold,
   who owns it), generic trees with placeholders (`<project>`, `bNN_<topic>`, `<run>`),
   concept matrices, flows, and what the skills say about themselves. It shows no
   workspace content: no real project names, paths or counts (JL 261005: "it is the
   prototypes, I don't want to see any content related to the drfirst content, but the
   high level concepts"). A **results report** draws the data itself: the tree read from
   the directory, the receipt lines, the counts, the names a finding is about. Either way
   a reader learns the situation without opening a file; a box holding only a label is
   wasted space.
2. **Loose, not templated.** No required headline, blocks, zones, key or frames. Group what
   belongs together into clusters; leave the gaps between clusters. Pick the arrangement the
   material suggests, and let it differ from the last drawing.
3. **Sketchy shapes, readable words.** `roughness: 1` on boxes, notes, marks and arrows;
   words in Nunito (`fontFamily` 6), a clean rounded sans, never the hand-script Virgil
   (`1`) or Excalifont (`5`), which are hard to read (JL 261005); monospace (`fontFamily`
   3) only for real paths, code and tables. Sticky notes in a few soft fills (yellow the
   ask, green fits, orange bends, gray empty, pink open). Keep everything straight and
   aligned (`angle: 0`, no random offsets): tilt reads as crooked (JL 261005: "it is not
   even vertical"). Size each note and row to its content so clusters sit evenly.
4. **Point at what matters.** A red rectangle fitted around the one line that is wrong (never
   an ellipse: it cuts across the lines above and below; JL 261005), an arrow from a
   short hand note to it. A question gets a `?`, not a verdict the person has not given.
5. **A Questions zone.** One Excalidraw frame named "Questions" (a `frame` element whose
   children carry its `frameId`, never a drawn box around them; JL 261005: "make the
   questions to be a frame, no wrapped with the box") holds every question, one row each: the question
   sticky (read from the Block's `board.md` register), then our ideas as blue stickies and
   each choice the person must make as a pink sticky (JL 261005: "make the questions zone
   that put all the questions there, and also the ideas there and I can put my thoughts
   here").
   Undecided points go into the row of the question they belong to, not a loose pile.
6. **Draw anywhere, no fenced room.** Never draw a "room to sketch" or "your thoughts" box:
   the whole canvas is the person's (JL 261005: "I don't want this, I want to scratch
   anywhere"). Leave open space between clusters and beside each question row instead.
   Do not fill every corner.
7. **Facts read, not typed.** In a results report, counts, paths and excerpts come from
   disk when the script runs, aggregates and schema only, no row-level records or
   identifiers (PHI rules). In a design scratch, the questions come from the Block's
   `board.md` and the concepts from the skills, with placeholders, never from a scan of a
   workspace.
8. **Readable when zoomed in, findable when zoomed out.** Words about 18 to 30px,
   monospace 14 to 16px, one big title. Nothing overlapping; check the PNG.


Designing a concept: a plain table
----------------------------------

When the drawing is for designing a concept (a skill, a contract, a hierarchy) rather than
showing where a project stands, it is a prototype: no project content, no counts, no real
names, and no colour (JL 261005: "too colorful, make it just simple"; "what I care about is
the design of the skills, not to report the current content"). Draw a table with lines
only: rows and columns named by the concepts, a first row that defines each column, one
empty row and a notes column for what comes next. Each cell gets a short gray placeholder
(`bNN_<topic>`, `?` where nothing is settled) and is otherwise empty, so the person writes
and sketches in it. Black and gray only, `roughness: 0` lines, Nunito text.

Two shapes the person liked for concepts (JL 261005, "things like this is great"):

- **A flow of boxes**: each concept a rounded sketch box (`roughness: 1`) holding its folder
  or name in monospace; arrows between boxes carry a short label (`bind Result id + hash`,
  `signed handoff`); an open link is a red dashed arrow whose label starts with `?`.
- **A tree per concept**: the box on top, a gray one-line definition under it, then its
  folder tree with a gray definition beside every entry, then its open questions in red.
  Route arrows box edge to box edge, or around the trees, never through text.

Worked examples: `Tools/blueprints/b01_haipipe-toolkit/j03_project_workbench/studio/_build/build_ladder_grid.py` (table) and
`build_ladder_trees.py` (a tree per level, boxes and labelled arrows).


Designing a workbench: screens with what is on disk
---------------------------------------------------

When the design is a workbench (its Spaces, what each shows, what backs it), draw the screens
themselves, not rows that describe them (JL 261007: "I think the s02 excalidraw is brilliant").

```text
frame per Space:  [ Block tab ]   [ Job tab ]   [ Task tab ]   | pop-out, from any tab's ↗
                   screen          screen        screen         |  [ window ]
                   on disk         on disk       on disk        |  [ window ]
```

1. **One frame per Space, one full screen per level.** Each screen has the level tabs, the
   Spaces row with the open one outlined, the third row as buttons (the selected one outlined),
   the content, and the Runs panel on the right. A level that has no children shows its Work
   Details dashed.
2. **"On disk" under every screen.** Draw the folders and files that back the screen as a
   tree, each line with a gray note on what part of the screen it feeds (`<topic>.md` -> the
   row's details). The screen and its files are read together.
3. **A pop-out column.** The last column holds the windows a `↗` opens, from any tab, each
   with a title bar and a close button.
4. **Start from the served workbench.** Read the server code that renders the Space today and
   draw that, then change only what was asked; do not invent extra boxes (a cell that holds
   boxes inside boxes was "too complicated"). A closed row shows its name only; its details
   come with opening it.
5. **One module for the screens.** Every drawing that shows the same screens imports one
   module, so a change lands in all of them.
6. **Pair it with a logic tree.** Boxes and plain lines for what holds what; labelled arrows
   for how the parts relate, routed in clear channels (never through a box or a caption);
   red dashed for what is open.

Worked example: `Tools/blueprints/b01_haipipe-toolkit/j03_project_workbench/studio/s04-studio-and-report/` (`studio_report_ui.py`,
the screens, their on-disk trees and the pop-outs; `build_s04_studio_and_report.py`, frame 5,
the logic tree).


The canvas is shared
--------------------

The script seeds the drawing; the person owns what they draw. Never judge a person's edit
by Excalidraw's `version`: a save re-stamps every element. Instead the writer:

1. gives each seed element a content-based id (`s-` + a hash of what it draws), so the same
   thing keeps the same id across builds, whatever order the code draws in;
2. keeps a snapshot of what it drew last beside the drawing (`<folder>/.<name>.seed.json`), so two
   drawings with the same name in two Blocks never share one;
3. on a rebuild keeps every element without an `s-` id (the person's own), every `s-`
   element whose content differs from the snapshot (the person edited it), leaves out
   every `s-` element the snapshot has but the canvas lost (the person deleted it), and
   redraws the rest.

Compare content, not layout: a save also re-measures text with its real font, so a text's
width and height never count as an edit. An open ✏️ Edit tab pushes its copy back to the file
every few seconds, so a tab still on an older version can save over a rebuild: when the
canvas holds seed elements from an older build, treat it as stale and redraw what is missing
instead of honouring it as deleted, and ask the person to reload the tab after a rebuild.

The first build with no snapshot takes the canvas's seed elements as the snapshot. Sticky
text is bound to its note (`containerId`), frames to their children (`frameId`); remap both
with the ids. Place new content where the person's marks will still line up (a new column
or frame beside, not a shifted layout under their comments). The `.png` is a preview.
The writer: `haipipe-studio`'s `scripts/canvas.py` (moved from b03 `studio/_build/`, 261007).


The comment loop
----------------

The drawing is a conversation (JL 261005: "It is really good to make people to add their
own comments"). The person writes on the canvas in red: a note, a ring, an arrow, a rough
mock-up. The agent answers on the same canvas, so the thread stays beside the thing it is
about.

```text
seed drawing ─▶ person marks in red ─▶ agent reads the marks ─▶ reply in blue + fold into builder ─▶ rebuild
     ▲                                                                                                  │
     └──────────────────────── the person reloads the tab and marks again ◀────────────────────────────┘
```

1. **Read the marks.** The person's elements are the ones without an `s-` id. Read every
   text; resolve what each points at (an arrow's end, the seed elements inside a ring).
2. **Answer in blue, beside the mark.** A reply is a seed element the builder draws from a
   `REPLIES` list (position, text), placed next to the comment, never over it. It says what
   was done, what exists already (with the real file), and the next open `?`.
3. **Fold the decision into the builder.** A mark that settles something ("these two are
   freestyle") changes the seed text; an idea (a new screen, a new level) becomes new seed
   content placed where the person's marks do not move: a new column to the left or right,
   or a new frame, never a shifted layout.
4. **Never touch the person's marks.** Do not move, restyle, delete or "resolve" them; they
   stay as the record of the conversation.
5. **Rebuild, then ask for a reload.** The open Edit tab still holds the old copy; the
   writer redraws what a stale save drops, but a reload avoids the round trip.

Worked example: `build_ladder_trees.py` (`REPLIES`, the Space level added to the left).


Build and look
--------------

```bash
B=<Block>/studio/_build
python $B/build_<name>.py              # writes ../<name>.excalidraw, keeping the person's marks
bash $B/make.sh                        # every drawing + its .png preview (render_png.py)
```

Keep the disk reading in its own module (`disk_facts.py` or similar) so several drawings
share it. Open the PNG, crop each cluster, fix overlaps and cut-off text, rerun. The
previewer draws Nunito as a plain sans and monospace in Menlo; Excalidraw shows its own
fonts. Use ASCII (`->`, `!=`, `x`) in text: symbols such as ✓ → ≠ × may not render.

Helpers (sticky with bound text, mark, mono block, merge-safe write, and the tidy elements)
are in `ref/elements.md`. Worked example: `Tools/blueprints/b01_haipipe-toolkit/j03_project_workbench/studio/_build/`
(`build_project_scratch.py`, `disk_facts.py`, `make.sh`); the merge-safe writer and the previewer
are `haipipe-studio`'s `scripts/canvas.py` and `scripts/render_png.py`, a studio topic's contract is
`haipipe-studio`'s.


A report drawing
----------------

When the drawing is a Question's report picture, to show others what was found, switch to the
report mode: read the full report and its cited Results first, then give the first frame the
answer and the strongest evidence, and further named frames the comparisons, figures, examples
and logic. Real values with clickable sources; plots from `ref/plot_kit.py` (native shapes:
`hbar`, `compare`, `share_bar`, `columns`, `spans`, `gauge`, `trend`); source figures embedded
as image elements (`picture()`, `ref/add_pictures.py`); preview the first frame only with
`ref/render_excalidraw.py --frame first`. One Question, one drawing, linked once from its
`### Evidence`. A scratch on the same canvas stays; the report frames sit beside it.
Full guidance, rules 0 to 12, frame choice and worked examples: `ref/report-drawing.md`.

**Built from studio frames.** When the report's pictures already exist as frames of the Block's
studio drawings, the report drawing is generated, never drawn by hand: the report's `.md` lists
its figures under `## Figures` (a yaml block: `from` a studio drawing, the `frame` name, a
`caption`), and `haipipe-report`'s `scripts/build_report_drawing.py <reports/qNN_topic/>` copies each frame (with the
person's marks, without their red notes), scales it to one width, straightens it, and stacks the
figures under a heading frame with a source line each. The frame's name is the contract: rename a
studio frame and the build names the frames it can find. Rebuild after the studio changes; the
workbench's Audience Report shows the result (Rebuild report drawing). Designed in
`Tools/blueprints/b01_haipipe-toolkit/j03_project_workbench/studio/s04-studio-and-report/`.


Boundary
--------

`excalidraw-section` draws a paper's structure from its Draft plans; this skill draws the
working material of one question or report. A manuscript figure is a display unit
(`haipipe-display`). The report's words belong to `haipipe-page` / `haipipe-question`; the
workbench that shows the picture is `workbench-cowork` or `workbench-work`.
