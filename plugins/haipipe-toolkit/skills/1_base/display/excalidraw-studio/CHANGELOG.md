excalidraw-studio · Changelog
=============================

## [0.3.7] · 2026-10-12 · Tables as a grid; arrows between frames only where one leads on

- Asked 261012 on Proj10 work/b01, showing b03's model × engine table: "I want the tables like this", and "no need to
  have the --> all the time".
- `Drawing.grid_table(x, y, columns, rows, widths)`: column names small and grey, one grey rule above each row, no
  boxes; a value cell `{big, tag, color}` draws its number large and its mark and Run small under it; a `dim` row is
  grey. `GREY` is exported.
- ③: named acts are enough; an arrow between frames only where one frame leads on. `check.py`'s ③ passes a drawing
  with acts named and no arrows; an arrow through a third frame still fails.

## [0.3.6] · 2026-10-12 · ⑨ Vivid, never a wall of text

- Asked 261012, on a Job's ③ "explained from zero" frame (Words to know, What goes in, What comes out: boxes of text,
  1,000 to 1,700 words): "things like this should be forbiden, so rigid, not vivid, no one have the incentive to zoom
  in and read".
- Principle ⑨: every frame leads with something to look at (a chart, a real row, a screenshot, a formula, a
  scoreboard); a frame of only text boxes is forbidden; its words stay in the face.
- `check.py`: a row ⑨ fails a frame with no picture and more than `WALL_WORDS` (600) words; s00 and slide drafts keep
  their own shapes. b03's results frames (75 to 280 words, a scoreboard or an answer table) pass.
  A frame that draws a real folder tree (④, ten or more tree lines) is its own picture and passes ⑨.
- excalidraw-job: ③ `detail_frame` is drawn only when a face sets `job: detail: true`; a new ③ `chart_frame` draws a
  face's `job: chart:` (before → after bars, every number read from a Run's receipt).

## [0.3.5] · 2026-10-12 · ⑧ Room between boxes, the numbers big

- Asked 261012, on b01 s32's Run frame (a grid of boxes stretched edge to edge) against a hand-moved version with its
  boxes stepped apart: "You can leave some rooms, not all the things nested together … I think this should be added
  as one principle as well. I think for a task, we want to salient show the numbers and the values."
- Principle ⑧: boxes only as wide as their words, apart, a flow stepping right and down; a Task's measured values as a
  scoreboard, each number large.
- `draw.py`: `Drawing.room(frame)` marks a frame laid out with room; `Drawing.area_of` gives ⑥ the boxes' area for it
  (the frame's otherwise), so the room is not read as thinness; the badge's own box is an aside. `check.py` uses
  `area_of`. Frames without the mark measure as before.
- excalidraw-task (0.3.x): `rows_of` draws stairs by default (asked 261012, on a ③ frame: "I don't want this circle back
  line any more, give me the stair version"): each row steps right and hangs off the row above's first box by a
  short straight drop; `fit()` trims or grows a room frame to its boxes; Run frames show their values as a
  scoreboard (`big_values`). A face keeps the old rows with `task: layout: rows`.

## [0.3.4] · 2026-10-12 · A detail frame's floor follows its type size

- Measured by the Proj10 session on b51 s01 (261012): video frames filled with words, at ⑦'s 28 to 30 px, read 81 to
  86 words per million px, under ⑥'s 120, which was set for body words of 20 to 24 px. A word at 30 px takes
  (30/24)² of the room, so a frame just as full reads about 77.
- `Drawing.detail_floor`: a detail frame's floor is 120 × (24 / body px)², the body being the size most of its words
  are set in (88 at 28 px, 77 at 30 px). The badge and `check.py` use it; a plain text frame keeps 120.

## [0.3.3] · 2026-10-12 · A detail frame is measured by ⑥

- Asked 261012, on b01's Task topics: "I still cannot get the full picture of the rNN of a video". A video's full frame
  (shots, terms, the formula explained, steps with why, the Run) is the frame ⑦ sends the detail to; with screenshots
  it was a picture (not measured), but a video with no usable screen (b01 s29 r04, 358 words) failed ⑦ as a map.
- `draw.py`: `Drawing.detail(frame)` marks such a frame, `Drawing.is_detail`; its badge measures words per million px
  against the text floor. `check.py`: a detail frame's ⑥ is the text floor and its ⑦ says "📖 a detail frame".
  A builder marks only the frames meant for close reading; a workflow or a mind map stays under ⑦.

## [0.3.2] · 2026-10-12 · s00 keeps its own words

- ⑦ (0.3.0) failed every frame of every s00 (b10's: 332 to 713 words; b31's: 218 to 466): s00's index names each
  topic and Job with a short line, so 200 words cannot hold without dropping topics (asked by the s00 session; JL
  closed s00 today, s00-D01). Like a slide draft's sizes, s00's words are its own shape: `check.py` names a Block's s00
  (haipipe-studio `canvas.is_s00`) under ⑦, "🗂️ s00's own", and does not judge it; every other check still applies.
  The Shapes table says so. `tests/test_draw.py` checks it.

## [0.3.1] · 2026-10-12 · check.py counts a node that starts like the badge

- `check.py` left out every text starting with 📊, 🪶, "✅ a" or "❌ a", meant for the badge; a node titled that way
  went uncounted (b31 s01's ① counted 192 words, its badge 209: the titles of ⑥ "📊 …" and ⑦ "🪶 …"). It now
  leaves out the badge only: a text marked `canvas.aside`, or one of the badge's own lines (`BADGE`, for drawings
  built before 0.3.0). The badge and check.py now give one count. `tests/test_draw.py` checks it.

## [0.3.0] · 2026-10-12 · Principle ⑦: few words in a workflow

- Asked 261012: "add at least of words, (especially the small versions as possible) when drawing the workflow", and
  "make the draft to be less of wordy and concise". A map frame (a workflow, a mind map) reads from its boxes and
  arrows: at most 200 words, at most a quarter of them a detail (under 28 px); the detail goes to its own frame or
  topic.
- ⑥'s map floor (70 words per million px) is retired: it pushed words into maps, the opposite of ⑦. ⑥ measures text
  frames; `MAP_FLOOR` stays importable for old builders.
- `draw.py`: `SMALL`, `MAP_WORDS`, `SMALL_SHARE`, `Drawing.words_small`; a map's badge shows its words and its small
  share (🪶), and the badge's own words are `canvas.aside`, not counted. `check.py`: a ⑦ row per frame.

## [0.2.5] · 2026-10-12 · A mind map's centre box grows with its words

- `draw.py`'s `mind_map` drew its centre (the key point) in a fixed 210 px box, so a centre of four lines or more ran
  out of it (found drawing excalidraw-job's ① "Why", whose centre is a Job's aim). The box now grows past three lines
  of 44 px words; every centre that fit before keeps its 210 px (b31 s02 to s05, b10 s10), so those drawings do not
  change.
- The Shapes table names excalidraw-job (b31 s06): a Job as one drawing, four frames in two acts.

## [0.2.4] · 2026-10-12 · Three checks fixed by the sessions that redrew with them

- Found by the b10 sessions that redrew s00, s51 and s52 (asked 261012: "could you message the sessions b10-s05 s00
  s51-s52-server-share to make them to follow the drawing principles"):
  - ① read `customData.reads_down`, a key nothing writes; it now asks haipipe-studio's `canvas.is_read_down` (what
    `canvas.reads_down` marks), so a frame read down passes on its width (b10 s00's plan and index).
  - ⑤ counted a green change note's small words, which ⑥ already leaves out; now neither counts them (b10 s52 ①
    went from 12% to 19% only by its required change note).
  - ③ fails a story arrow that runs through a third frame (b10 s52: an act's turn drawn halfway down crossed a
    taller frame); `crossings()` names the frame. No Studio drawing on disk has one now.
- `draw.py`'s `write` says why the palette stays off; haipipe-studio 0.13.14's palette now keeps the key colour.
- `tests/test_draw.py`: a frame read down, a green note, an arrow through a frame.

## [0.2.3] · 2026-10-12 · A slide draft keeps its own sizes

- With excalidraw-slide 0.2.0: `check.py` names a slide draft (s61-s69, haipipe-studio's
  `canvas.is_slide_draft`) and does not judge its frame sizes, its left-to-right frames, word sizes or density (① ③ ⑤ ⑥); its
  folder trees and map/text kind are still read. The Shapes table says what a slide draft is.

## [0.2.2] · 2026-10-12 · A mind map counts as a map

- `Drawing.kind` counts lines as well as arrows between boxes, so a mind map (`mind_map`, whose links are lines)
  is measured against the map floor (70), not the text floor (120). Found redrawing b31 s03, whose mind map frame
  read as text at 96.

## [0.2.1] · 2026-10-12 · Linked with haipipe-studio

- Asked 261012: "will the /haipipe-studio call the skill of /excalidraw-studio? Could you link them". haipipe-studio
  (0.13.11) now loads this skill before drawing or redrawing a topic and names it in its Boundary; its
  `new_topic.py --builder` writes a builder on `draw.py`. This skill's description, opening and Boundary say so.

## [0.2.0] · 2026-10-12 · Check a drawing, redraw a topic

- Asked 261012: "if I want to update the current draw with these principles, how should I do?" `scripts/check.py
  <drawing>` checks each frame against the principles it can read (① size and slide-like frames, ② map or text,
  ③ acts and arrows between frames, ④ folder-tree lines, ⑤ small words, a large title and a key point, ⑥ density
  against the floor of its kind) and says 👤 where a person decides. SKILL.md gains "Redraw a topic with the
  principles": check, story, words, builder, look, save, one topic at a time.

## [0.1.0] · 2026-10-12 · A skill for how a Studio drawing reads

- New (b31 s01-D08, asked 261012: "should we also have a excalidraw-studio?" then "please go ahead and do it"):
  the six principles agreed on b31 s01-drawing-principles (one frame as large as possible; a workflow map or
  a mind map inside; the frames as one story, in acts, joined by named arrows; a folder tree only for folders;
  big words and one slight colour for the key point; each frame's density measured), the look (names no one),
  the shapes that keep their own rules, and the boundary with haipipe-studio.
- `scripts/draw.py`: one `Drawing` with the helpers taken out of b31 s01's builder: frames, text, wrapped
  paragraphs, boxes, the key-point box, lines, pictures, the density badge (a text frame at least 120 words per
  million px, a map frame at least 70, a picture not measured), `mind_map`, `flow`, `folder_tree`, `acts` (rows
  named at the left, named arrows) and `write` (haipipe-studio's canvas.write, a person's marks kept).
- `tests/test_draw.py`.
