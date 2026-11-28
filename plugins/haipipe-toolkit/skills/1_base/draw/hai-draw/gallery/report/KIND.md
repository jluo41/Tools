---
name: report
part-of: hai-draw
description: "Draws in Excalidraw in two modes: a scratch (a sketchy whiteboard of a question's material, with a comment loop) and a report drawing (a report's answer and evidence in named frames). Use to think on a canvas or picture a report. Trigger: scratch, working drawing, /hai-draw report."
allowed-tools: Bash, Read, Edit, Write, Grep, Glob
metadata:
  version: "0.8.6"
  last_updated: "2026-10-26"
  # version history: ./CHANGELOG.md
---

# /hai-draw report · a dense scratch to think on together

The drawing is a whiteboard the person and the agent both work on, not a finished slide. It holds a lot
of real information and leaves the shape open, so the person can move things, circle them, cross them out
and draw their own idea next to them. A neat template of labelled boxes is the failure to avoid: it looks
tidy and says nothing.

```text
real material  ─▶  loose clusters on one canvas  ─▶  the person draws on it  ─▶  reseed keeps their marks
(disk, skills,      stickies · trees · excerpts ·      moves, marks, crosses,      only untouched s- elements
 receipts, runs)    marks · arrows · open questions    adds their own              are redrawn
```

A scratch is not judged by `check.py` (hai-draw SKILL.md § Shapes that keep their own rules): its frames,
sizes and layout below are its own. Its colours and fonts are the draw.py look (§ The draw.py look).


What makes a good scratch
-------------------------

1. **Dense with the real thing, at the right level.** First ask what the drawing is about.
   A **design scratch** (how skills, levels or contracts should work) is a prototype: its
   material is the concepts, each with its contract (folder pattern, what it must hold,
   who owns it), generic trees with placeholders (`〈project〉`, `bNN_〈topic〉`, `〈run〉`),
   concept matrices, flows, and what the skills say about themselves. It shows no
   workspace content: no real project names, paths or counts, only the high-level concepts.
   A **results report** draws the data itself: the tree read from the directory, the receipt
   lines, the counts, the names a finding is about. Either way a reader learns the situation
   without opening a file; a box holding only a label is wasted space.
2. **Loose, not templated.** No required headline, blocks, zones, key or frames. Group what
   belongs together into clusters; leave the gaps between clusters. Pick the arrangement the
   material suggests, and let it differ from the last drawing.
3. **Sketchy shapes, readable words.** `roughness: 1` on boxes, notes, marks and arrows;
   words in Nunito (`fontFamily` 6), never the hand-script Virgil (`1`), Excalifont (`5`) or
   Comic Shanns (`8`); Cascadia (`fontFamily` 3) only for real paths, code and tables. Sticky
   notes are unfilled black boxes; red marks what is open. Keep everything straight and
   aligned (`angle: 0`, no random offsets): tilt reads as crooked. Size each note and row to
   its content so clusters sit evenly.
4. **Point at what matters.** A red rectangle fitted around the one line that is wrong (never
   an ellipse: it cuts across the lines above and below), an arrow from a short hand note to
   it. A question gets a `?`, not a verdict the person has not given.
5. **A Questions zone.** One Excalidraw frame named "Questions" (a `frame` element whose
   children carry its `frameId`, never a drawn box around them) holds every question, one row
   each: the question sticky (read from the Block's `board.md` register), then our ideas as
   stickies, then each choice the person must make, in red. Undecided points go into the row
   of the question they belong to, not a loose pile.
6. **Draw anywhere, no fenced room.** Never draw a "room to sketch" or "your thoughts" box:
   the whole canvas is the person's. Leave open space between clusters and beside each
   question row instead. Do not fill every corner.
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
names, black only. Draw a table with lines only: rows and columns named by the concepts, a
first row that defines each column, one empty row and a notes column for what comes next.
Each cell gets a short placeholder (`bNN_〈topic〉`, `?` where nothing is settled) and is
otherwise empty, so the person writes and sketches in it. `roughness: 0` lines, Nunito text.

Two more shapes for concepts:

- **A flow of boxes**: each concept a rounded sketch box (`roughness: 1`) holding its folder
  or name in Cascadia; arrows between boxes carry a short label (`bind Result id + hash`,
  `signed handoff`); an open link is a red dashed arrow whose label starts with `?`.
- **A tree per concept**: the box on top, a one-line definition under it, then its folder
  tree with a definition beside every entry, then its open questions in red. Route arrows
  box edge to box edge, or around the trees, never through text.


Designing a workbench: screens with what is on disk
---------------------------------------------------

When the design is a workbench (its Spaces, what each shows, what backs it), draw the screens
themselves, not rows that describe them.

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
   tree, each line with a note on what part of the screen it feeds (`〈topic〉.md` -> the
   row's details). The screen and its files are read together.
3. **A pop-out column.** The last column holds the windows a `↗` opens, from any tab, each
   with a title bar and a close button.
4. **Start from the served workbench.** Read the server code that renders the Space today and
   draw that, then change only what was asked; do not invent extra boxes (a cell that holds
   boxes inside boxes is too complicated). A closed row shows its name only; its details
   come with opening it.
5. **One module for the screens.** Every drawing that shows the same screens imports one
   module, so a change lands in all of them.
6. **Pair it with a logic tree.** Boxes and plain lines for what holds what; labelled arrows
   for how the parts relate, routed in clear channels (never through a box or a caption);
   red dashed for what is open.


The canvas is shared
--------------------

The script seeds the drawing; the person owns what they draw. The writer is `hai-studio`'s
`scripts/canvas.py` (`canvas.write`, marks kept). What a scratch builder must give it:

1. **Content ids**: each seed element's id is `s-` + a hash of what it draws, so the same
   thing keeps its id across builds; the snapshot sits beside the drawing
   (`〈folder〉/.〈name〉.seed.json`). Never judge a person's edit by Excalidraw's `version`.
2. **Bound ids**: sticky text is bound to its note (`containerId`), frames to their children
   (`frameId`); remap both with the ids.
3. **New content beside**: a new column or frame beside, never a shifted layout under the
   person's comments.
4. **A stale tab**: an open ✏️ Edit tab saves its copy back every few seconds and can save over
   a rebuild; the writer redraws what a stale save drops, and the person reloads the tab
   after a rebuild. The `.png` is a preview.


The comment loop
----------------

The drawing is a conversation. The person writes on the canvas in red: a note, a ring, an
arrow, a rough mock-up. The agent answers on the same canvas, so the thread stays beside the
thing it is about.

```text
seed drawing ─▶ person marks in red ─▶ agent reads the marks ─▶ reply beside + fold into builder ─▶ rebuild
     ▲                                                                                                   │
     └──────────────────────── the person reloads the tab and marks again ◀─────────────────────────────┘
```

1. **Read the marks.** The person's elements are the ones without an `s-` id. Read every
   text; resolve what each points at (an arrow's end, the seed elements inside a ring).
2. **Answer beside the mark.** A reply is a seed element the builder draws from a `REPLIES`
   list (position, text), in black next to the comment, never over it; what it changed is a
   green change note. It says what was done, what exists already (with the real file), and
   the next open `?`.
3. **Fold the decision into the builder.** A mark that settles something changes the seed
   text; an idea (a new screen, a new level) becomes new seed content placed where the
   person's marks do not move: a new column to the left or right, or a new frame.
4. **Never touch the person's marks.** Do not move, restyle, delete or "resolve" them; they
   stay as the record of the conversation.
5. **Rebuild, then ask for a reload.**


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
are in `ref/elements.md`; the previewer is `hai-studio`'s `scripts/render_png.py`, and a
studio topic's contract is `hai-studio`'s.


A report drawing
----------------

When the drawing is a Question's report picture, to show others what was found, switch to the
report mode: read the full report and its cited Results first, then give the first frame the
answer and the strongest evidence, and further named frames the comparisons, figures, examples
and logic. Real values with clickable sources; plots from `ref/plot_kit.py` (native shapes:
`hbar`, `compare`, `share_bar`, `columns`, `spans`, `gauge`, `trend`) and source figures embedded
as image elements (`picture()`, `ref/add_pictures.py`) keep their own colours; boxes and words
keep the draw.py look. Preview the first frame only with `ref/render_excalidraw.py --frame first`.
One Question, one drawing, linked once from its `### Evidence`. A scratch on the same canvas
stays; the report frames sit beside it. `check.py` judges it. Full guidance, rules 0 to 12,
frame choice and worked examples: `ref/report-drawing.md`. A newer Block keeps a Question's
answer in the Studio topic that answers it (`hai-report`), not in a report drawing.


Boundary
--------

`hai-draw draft` draws a paper's structure from its Draft plans; this kind draws the
working material of one question or report. A manuscript figure is a display unit
(`hai-display`). The report's words belong to `hai-draft` / `hai-report`; the
workbench that shows the picture is `workbench-cowork` or `workbench-work`.
