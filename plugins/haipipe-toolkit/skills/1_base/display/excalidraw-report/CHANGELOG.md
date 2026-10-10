# Changelog

## 0.8.2 · 2026-10-09 · Theme folders are singular

- Docs name the singular Theme folders (s01-D29, JL 261007): `work/`, `discovery/`, `paper/`, `insight/`,
  `design/`, `labeling/`, `ideation/`; the older plural names still read.

## 0.8.1 · 2026-10-07 · The report builder and the studio writers moved to their skills (b03 s21)

- `ref/build_report_drawing.py` moved to `haipipe-report`'s `scripts/` (the report's own skill);
  a shim stays here, so the old command still runs.
- The merge-safe writer `canvas.py` and the previewer `render_png.py` moved from b03's
  `studio/_build/` to `haipipe-studio`'s `scripts/`; SKILL.md and `ref/elements.md` name them there.
  This skill keeps the drawing kit: scratch and report modes, elements, plot kit, pictures.

## 0.8.0 · 2026-10-07 · A report drawing built from studio frames

- New `ref/build_report_drawing.py` (moved here from b03's design `_build/`, so every Block can use
  it): a report's `## Figures` list names studio frames; the script copies each frame, scaled to one
  width, under a heading frame, each with a caption and source line. It writes the drawing whole,
  with stable ids; it no longer needs a canvas writer, since nobody edits a generated report.
- SKILL.md, "A report drawing": the rule and the command. The workbench's Rebuild report drawing
  prompt names the script.

## 0.7.1 · 2026-10-07 · The snapshot sits beside its drawing

- canvas.write keeps its snapshot as `<folder>/.<name>.seed.json`, beside the drawing, not in one
  `_build/` by name: two Blocks each had an `s11-…` drawing, shared one snapshot, and 520 new
  elements of one counted as deleted. An old `_build/` snapshot is used once, only if most of its
  elements are on that drawing.

## 0.7.0 · 2026-10-07 · Designing a workbench: screens with what is on disk

- JL 261007: "I think the s02 excalidraw is brilliant". New section for workbench design
  drawings: one frame per Space and one full screen per level, an "on disk" tree under each
  screen saying what part of the screen each file feeds, a pop-out column, the served
  workbench as the starting point, one shared module for the screens, and a box-and-arrow
  logic tree with labelled arrows in clear channels.
- What JL turned down on the way, now named in the section: row sketches in place of screens,
  boxes inside boxes in one cell, details shown on closed rows.

## 0.6.0 · 2026-10-06 · Two modes in one skill: scratch and report drawing

- A pull met two lines of work made the same day: this machine's scratch line (0.2.0 to
  0.5.0: dense scratch, concepts only for design work, plain tables, shared canvas that keeps
  the person's marks, the comment loop) and upstream's report line (0.3.0 plots and 0.4.0
  "report evidence before layout": plot kit, embedded pictures, frame choice). Both are kept.
- SKILL.md keeps the scratch text and gains "A report drawing", a short summary pointing to
   (upstream's full 0.4.0 guidance), ,
   and . The description names both modes.

## Scratch line (this machine, 2026-10-05)

### 0.5.0 · 2026-10-05 · The comment loop

- JL 261005: "this workflow scratch is great ... It is really good to make people to add their
  own comments". New section: the person marks in red, the agent reads the marks (non-`s-`
  elements), replies in blue beside each from a `REPLIES` list, folds decisions into the
  builder without moving the person's marks, rebuilds, and asks for a tab reload.

### 0.4.3 · 2026-10-05 · Stale tabs and re-measured text

- Text width and height no longer count as an edit (a save re-measures text). A canvas
  holding seed elements from an older build is a stale copy saved by an open editor tab:
  missing seed elements are redrawn, not taken as deletions. Ask the person to reload the
  tab after a rebuild.

### 0.4.2 · 2026-10-05 · Boxes, labelled arrows, a tree per concept

- JL 261005 on a flow of rounded boxes with labelled arrows and red dashed open links:
  "things like this is great". Added it, and the tree-per-concept shape (box, definition,
  folder tree with a definition per entry, open questions in red), to the concept section.

### 0.4.2 · 2026-10-05 · The Questions zone is a frame

- JL 261005: "could you make the questions to be a frame. no wrapped with the box". The
  zone is an Excalidraw `frame` named Questions; its stickies carry its `frameId`, so it
  moves, exports and hides as one unit. No drawn rectangle around it.

### 0.4.1 · 2026-10-05 · Keep the person's marks for real

- An Excalidraw save re-stamps every element's `version`, so "version above 1 = the person
  touched it" kept the whole seed and froze the drawing. The writer now uses content-based
  `s-` ids and a seed snapshot (`_build/.<name>.seed.json`): the person's elements, edits
  and deletions are kept; untouched seed elements are redrawn. Worked writer: b03 `canvas.py`.

### 0.4.0 · 2026-10-05 · A plain table for designing a concept

- JL 261005 on a colour-coded grid filled with project counts: "too colorful, make it just
  simple"; "what I care about is the design of the skills, not to report the current
  content ... I don't want to see any content related to the drfirst content, but the high
  level concepts"; "just use the lines to create the tables, make it easier for me to put
  the content".
- New section: a drawing that designs a concept is a lines-only table with placeholders,
  black and gray, one definition row, an empty row and a notes column; no project data.

### 0.3.5 · 2026-10-05 · A design scratch shows concepts, not workspace content

- JL 261005 on the b03 canvas: "what I am about is the design of the skills, not to report
  the current content ... it is the prototypes, I don't want to see any content related to
  the drfirst content, but the high level concepts". Rule 1 now separates a design scratch
  (concepts, contracts, placeholders, skill quotes; no real names, paths or counts) from a
  results report (data read from disk). Rule 7 follows.

### 0.3.4 · 2026-10-05 · A Questions zone

- JL 261005: "make the questions zone that put all the questions there, and also the ideas
  there and I can put my thoughts here". One boxed zone, a row per register question:
  question sticky, blue idea stickies, pink choice stickies, an empty "your thoughts" box.

### 0.3.3 · 2026-10-05 · Mark with a rectangle, not a ring

- JL 261005 on the receipt ring: "don't use this. Make the rectangle". The red mark is a
  rectangle fitted to the one line (`mark()`), never an ellipse that crosses its neighbours.

### 0.3.2 · 2026-10-05 · Straight, not tilted

- JL 261005 on the b03 canvas: "it is not even vertical". Notes and boxes keep `angle: 0`
  and no random offsets; each note and row is sized to its content.

### 0.3.1 · 2026-10-05 · Readable words

- Words use Nunito (`fontFamily` 6), not the hand-script Virgil (`1`); JL 261005 asked for a
  more readable font than the hand script. Shapes keep `roughness: 1`; paths stay monospace.

### 0.3.0 · 2026-10-05 · A dense scratch, not a template (JL 261005)

- After 0.2.0 still read as a template, JL 261005: "what I want is the real scratch, it is too
  structured ... Too structure, make the human's creativities to be limited"; then "I want
  the intensive information level".
- The default drawing is now a hand-drawn scratch: loose clusters on one canvas, no required
  headline, blocks, zones, key or frames; sticky notes, rough boxes, rings and arrows; dense
  with real material read from disk (trees, receipts, counts, matrices, skill quotes, the real
  names behind each finding); open questions as pink stickies; empty room to draw.
- The canvas is shared: the script's elements carry `s-` ids; a rebuild redraws only untouched
  ones (version 1) and keeps everything the person added or moved. Sticky text is bound.
- The 0.2.0 element catalogue moved under "Tidy views" in `ref/elements.md`, used only when a
  polished report frame is asked for. New scratch helpers: `sticky`, `mono`, `ring`, `arrow`,
  merge-safe `write`; the previewer maps the hand font and monospace.
- Worked example: `Tools/designs/b03_project/studio/_build/build_project_scratch.py`.

### 0.2.0 · 2026-10-05 · Content first: the drawing carries the evidence (JL 261005)

- Rewritten after JL 261005: "excalidraw-report <--- this skill need to be updated, I feel it
  is not well written, I feel it's just like too structured. It's not like put all the basic
  element data figures displays in it. It just like give me the beautiful but meaningless
  outlines."
- Content first: step 1 inventories what the report has (numbers, tables, figures, trees,
  code, comparisons, steps, status); step 2 picks a display element per piece; the layout
  follows. New density rule with a test: could someone answer the report's question and
  quote its key numbers from the drawing alone? A label-only box is a smell.
- Display element catalogue: headline, table, bar chart, dot-interval chart, embedded PNG
  figure, folder tree, code/config excerpt, comparison, flow spine, status rows, call-out.
  Python helpers for each in new `ref/elements.md` (shapes from b11's and b00's builders,
  tested end to end with placeholder data and the Pillow previewer).
- The headline / big blocks / orange call-out / zones template is now one layout (the status
  view), not the default. Fixed sizes ("46px", "3 or 4 blocks") became guidance, except the
  readability floor (detail not below about 14px).
- Kept: salient at a glance, one reading direction, one file per report with a frame per
  view to the right, generated by studio/_build/ and checked by the PNG, real names and
  numbers with clickable sources (now aggregates only, no row-level records), linked from
  `### Evidence`. Worked examples now point to b11 and b00 builders.

## Report line (upstream, 2026-10-05)

0.4.0 · 2026-10-05 · Report evidence before layout
------------------------------------------------

- Read the full report and cited Results/figures before choosing the frames; map material
  findings to plots, exact tables, source images, examples or explanations.
- Replace the fixed three/four-block overview and one-line item limits with enough readable
  evidence. The first frame includes results; further frames hold needed detail.
- Explain the problem, why the method matters, how it works and what the evidence supports;
  labelled relationships can branch where the reasoning branches.
- Preserve units, conditions, differences, sample sizes and source links. Separate measured,
  derived, externally reported and missing results; do not rank incompatible benchmarks.
- Keep the existing one-drawing rule and source-builder workflow. Make image resolution,
  plot choice and frame count serve the evidence instead of limiting it. Reuse existing
  report or shared Block builders and identify the outputs their build commands regenerate.

### 0.3.0 · 2026-10-05 · Numbers are drawn: plots

- Rule 12 (JL 261005: "make sure this will include more plots as well"): sizes, shares, counts
  over time, date coverage and progress are plotted, with every value read from the cited Result
  and written on its mark. New § Plots: which number takes which plot, six plot rules.
- `ref/plot_kit.py`: the drawing engine as a `Doc` class plus seven plots of native Excalidraw
  shapes: `hbar`, `compare`, `share_bar`, `columns`, `spans`, `gauge`, `trend`. Each was rendered
  and looked at with REACH data; the look caught spans drawn past the axis (now clamped, with ◀
  and the true years) and a trend label on its own line (now beside the point).
- `ref/render_excalidraw.py` (the renderer every builder copies) gains `--frame first|<name>`:
  the `.png` beside a report drawing is the Report column's preview, so it is the first frame,
  whose headline is the answer; four frames side by side shrank to an unreadable strip.
- Worked example: REACH-SPACE b01_reach_jhu Q01, four frames ("Two schemas", "Where the rows
  are", "Inside deid.omop", "Q01 status"), built from the two table catalogs and the report's
  Evidence Item Results. The Task Workbench shows a report's own unlinked drawing with its
  `.png` preview too (`servers/workbench-task/task_questions.py`).

### 0.2.0 · 2026-10-05 · One Question, one drawing; pictures inside it

- Rule 6 (JL 261005: "for each question we should just have one excalidraw"): a report has
  exactly one `.excalidraw`; more views are frames in it. The Block road map stays in the
  Block's `studio/` and is no longer linked from a report.
- Rule 11 (JL 261005: "some png can be put into the excalidraw as well"): a screenshot or
  figure the report cites is an image inside the drawing, read from its source file on every
  build, long side at most 1600 px; a helper `picture()` in Draw.
- `ref/add_pictures.py`: appends a "Pictures" frame to a drawing another builder made; a Block's
  `make.sh` runs it on the built file before the render. Used for Project-Samsung b13
  (`connector-app-develop-host-setup`, the QR desk card) and b31 (Q02's five step frames, Q06's
  QR card); b11 Q06 and Q08 take version 3 as a frame (`BESIDE`) instead of a second link.
- Rule 9: a second drawing link or a picture link is a finding in Check, not a second thumb.
  Enforced in `servers/workbench-task/task_questions.py` (Task and CoWork workbenches);
  tests `test_coworkboard.py::test_one_question_shows_one_drawing_and_a_picture_goes_inside_it`
  and `::test_a_reports_drawing_lives_in_its_report_folder`, both failing before the change.
  First applied to Project-REACH-PD2D's cowork reports.

## Before the split

## 0.1.1 · 2026-10-04 · Salience first

- Rule 0, the three-second test (JL 261004: "with a glance of look, we get nothing, nothing is
  salient. people then lost the interest to zoom in"): a headline that is the answer, three or
  four big blocks, large step words, one orange call-out; detail small and gray. Checked by
  viewing the render at a quarter size. Applied to both frames of b13's
  connector-app-develop-host-setup.

## 0.1.0 · 2026-10-04 · Report pictures that read at a glance (JL 261004)

- New skill (JL 261004: "I don't like this from left and from right workflow, could you make it
  as concise and readable as possible?"; "make the report draw to be very easy to read and make
  the logic flows to be very very clear").
- Ten rules: one reading direction (a numbered spine, top to bottom; no wrapping rows), one line
  per item, zones in the order things happen, coloured dots with a key of only the colours used,
  who acts as a tag, one file per report with one named frame per view, real names and clickable
  sources, generated by studio/_build/, linked from the report's Evidence, checked by looking.
- First applied: b13_smartwatch_connector frame "Patient phone setup" (8 visit steps on one
  spine, replacing two 4-card rows that wrapped back to the left).
