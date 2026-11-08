haipipe-studio · Changelog
==========================


## [0.29.0] — 2026-11-05

`five_parts.build` takes `writer=`. None keeps the plain overwrite (`quick_draw.write`), so every existing five-part
builder is unchanged; `five_parts.marks_writer` writes through `canvas.write`, which keeps a person's marks and edits
on the canvas and writes the seed snapshot beside it, with the builder's own colours. The paper and work theme UI cells
(b16 j01 `paper_ui_cells.py`, b17 j03 `work_ui_cells.py`) now pass it: before, a rebuild overwrote the canvas with no
snapshot. The first build under it starts from an empty file (the old one moved aside), or every old element is kept
as a mark.


## [0.28.1] — 2026-10-31

`studio_move.py` rewrites a link only when its path, read from the file's folder or one above it, leads to a topic
that moves; a held topic, another Block's `studio/` and a template's `studio/sNN-<topic>` stay as written. It no
longer walks result/, results/, passes/, _runs/, delivery/, _old/, _legacy/ or notebooks/ (ladder.py's NO_RELINK).
Found by Ladder-b17's review (the old `LEFT` rule turned `../b02_b/studio/s03-gamma` into a path that does not
exist and rewrote a Result, a closed pass and an archive). New `tests/test_studio_move.py`; it fails on the old script.
No studio/ folder is left in the live SPACEs (JL 261031, b35 r02); the script stays for an old branch or copy.

## [0.28.0] — 2026-10-31

A topic has no page of its own (JL 261031: "first we will remove the single page for the studio"; "when we click
this, we will be point to" the card in `section=studio`; b35-s02-D05). The workbench's `focus_page.py` drops
`topic_page` and its sections (Slide, Mind map, Open, Decided, Rounds, Result, Files); `topic_home` gives an sNN's
card in its level's Studio under its group, and the left rail, the card's anchor (`id`) and a `:target` outline in
`focus.css` land the reader on it; `frame_view.py` sends an old sNN link on (302). A card's name and line open the
face, its picture the slide, in the pop-out. `static_page` keeps the workbench frame for a builder's delivery pages,
its path ending at the card. New section "Where a topic opens".

## [0.27.0] — 2026-10-31

Every sNN beside its Jobs (JL 261031: "please update all the /studio folders to put them under the block folder"):
new `scripts/studio_move.py <path> [--apply]` moves each `<level>/studio/<sNN>-<topic>/` to `<level>/sNN-<topic>/`
(an `sNN_<topic>` takes the hyphen). It rewrites `sNN-<topic>` in every text file of the paths given, makes a
moved file's relative climb past studio/ one level shorter (checked: each lands on the same folder), and makes a
moved builder's `Path(__file__)` climb (`HERE.parents[5]`, `.parent.parent`) one level shorter. Generated files are
never rewritten; their generators rerun. A studio/ left holding only `_groups.txt` goes, its order kept in
`<level>/_studio_groups.txt`; one that still holds loose items (a mind map, a question map, draw/) stays.
`job_results.py` makes a results topic beside the Jobs and counts both places. `studio_update.py audit` now names
the move (kind `move`) instead of waiting for it. The slides step of 0.26 (`.ideas.md`, `.slides.json`,
`topic_slides.py`, a scratch card per slide until a picture is asked for) is recorded here too.


## [0.26.0] — 2026-10-30

`/haipipe-studio update` (JL 261030: "should we have something like /haipipe-studio update"; "please go ahead to
update the whole studios here, and also for their draw"): new `scripts/studio_update.py`. `audit <path>` lists, per
sNN, what today's rules say it misses; `update <path>` prints the plan; `--apply` does the mechanical steps (a Stage
line, `delivery/` with `deck/` and a `render.yaml`, its mind map, its drawing in five parts with the old drawing kept
whole as the Design part, copied to `result/first-drawing.excalidraw`, and a builder that drew it moved to
`result/first-drawing-builder/`). The For line and the Delivery type are an agent's proposal (`brief`, `name`,
`name-batch`), with an Open point asking a person to agree them. The move out of `studio/` is listed but never made
until every Theme's screen reads an sNN beside its Jobs. `five_parts.card()` renders the card from only the elements
in a fixed 1350 x 820 region of the canvas, so a wide Design neither shifts nor shrinks it. Found in the run across
six SPACEs: `uv run` now passes `--no-project` (a SPACE's own `pyproject.toml` broke the render); a drawing counts as
five-part only once this script marks it, set last, so a draw cut short is drawn again; and only a script that draws
the sNN's own drawing is parked (a deck's, a table's or another drawing's builder stays).


## [0.25.0] — 2026-10-30

Each sNN names its main delivery type (JL 261030: "for each delivery, we should also say what is the type, give the
main delivery type"; "we should also add this to the skill, that what type of delivery we want to render"): a
`**Delivery type:**` line under `**For:**`, one word of skill · ui · code · draft · display · data, never deck (every
sNN has one). The one-delivery section, rendered from b35-s01, says what each type's `delivery/` holds and how
`render.yaml` hands it over. `new_topic.py` writes the line; the workbench shows the type as a pill beside the stage on
the sNN's card and its page (`frame.DELIVERY_TYPES`); `gallery_scan.py` reads it (`type_of`, a new "Each delivery type"
table) and no longer calls a delivery "deck" when it holds anything besides `deck/`. b35's s01 to s05 name theirs.


## [0.24.0] — 2026-10-30

Two galleries (JL 261030: "we might also have a sNN for the gallery of the deliveries, and gallery of the studios, as
the new sNN"): b35-s04 the delivery gallery and b35-s05 the studio gallery. New `scripts/gallery_scan.py` finds every
sNN and every `delivery/` in the SPACEs on the machine, by folder and file names only (never a file's content, never
`_WorkSpace/`; a SPACE inside a SPACE is a copy and is skipped), and sorts them by level, Theme and kind; both
drawings read it on every rebuild. `--write <sNN> studio|delivery` writes each gallery's
`delivery/skill/gallery.md`, the newest real one of each kind; s05's renders into the new `ref/gallery.md`. Only a
Tools sNN shows its face's words there, since Tools is public; another SPACE's shows its path.

## [0.23.0] — 2026-10-30

One Studio, every Theme (JL 261030: "how could the haipipe-studio skill will be adopted to different theme?"): the
Studio's shape is the same everywhere; a Theme plugs in by its kinds of delivery, where the render writes, and which
skill renders. The table renders from b35-s01's `delivery/skill/themes.md`. `render_delivery.py` knows a third piece,
`rendered_by: <Theme skill>`, which it reports and leaves to that skill.

## [0.22.0] — 2026-10-30

An sNN hands over through its own `delivery/` (JL 261030: "studio/sNN/delivery, this is the delivery, and then we do
the render, to render the delivery out, to that area, like the haipipe-studio"): the agreed version (its deck, which
stays, and the thing), and `delivery/render.yaml` naming where each piece goes. New `scripts/render_delivery.py`
checks or writes each text piece between `<!-- render <address> <block> -->` markers; a code piece names the Task that
builds it. `new_topic.py` makes `delivery/deck/` for every new sNN. This skill's own opening, "where it sits", the count
per level and "one topic, one idea, one delivery" are now rendered from b35-s01's `delivery/skill/`.

## [0.21.0] — 2026-10-30

No `studio/` folder (JL 261030: "we don't have the studio/sNN, we just have sNN, along side with jNN, to make it
visible directly"): an `sNN-<topic>/` sits beside the Jobs or Tasks of the level that uses its delivery, one numbering
per Block, at most 9 at a Block, 5 at a Job, 3 at a Task ("we might have many sNN, but we need to control the
numbers"). `new_topic.py` writes there, drops the `**At:**` line, and refuses one past the limit (`--over-limit`);
`frame.py` finds sNN beside Jobs (`topic_owner`, `_studio_groups.txt`), an older `studio/` still reads. b35 moved first.

## [0.20.0] — 2026-10-30

Studio: from idea to delivery; one topic, one idea, one delivery (JL 261030: "one studio, one idea and one
delivery"). A delivery is a deck, always, and the thing the deck is about: skills or code, a figure, a draft, a data
table, a server package ("slide (a must) and the associated skills, code, or figures, draft"); the thing gives the
topic its type (SKILL.md lists them). A new face names its delivery first, a `**For:**` line (`new_topic.py`). A
Block's `board.md` lists its topics' deliveries under `## Deliveries`. b35 got `s01-studio-skill/`, first by
JL's word, and its six topics moved down one number (s01-s06 became s02-s07); the `b35 sNN-Dnn` citations in skills
and code moved with them. Drawings use Excalidraw's code font, Comic Shanns (`fontFamily: 8`, `quick_draw.FONT`; JL 261030:
"could you use this font type?").


## [0.19.0] — 2026-10-29

Every topic gets a quick drawing by default, `sNN-<topic>.excalidraw` beside its face (`scripts/quick_draw.py`, called by
`new_topic.py topic`), opened from the topic's label in its Block's map (JL 261029: "where is the pop out excalidraw for
it?"; "could you add them as the default?"; "this should be in the label"). It is a drawing, never the face's lines as
text (JL, of a first version that listed them: "this is fucking report, not the draw"): the method of
coleam00/excalidraw-diagram-skill (`references/workflow-diagrams/`), its idea as one pattern (cycle, timeline, tree,
fan-in), free text unless a shape carries meaning, colour as meaning, rendered and looked at before it is shown. A new
topic starts with its life line, its stage marked; `quick_draw.py`'s kit (box, oval, diamond, arrow, line, dot, ask)
draws the idea. b35's six topics each have theirs. A topic made with `--builder` keeps its builder's drawing.

## [0.18.1] — 2026-10-29

A topic has its own `result/` for working output, messy is fine (b35 s01-D10); a Task Run's output stays in the Run and the topic shows it.

## [0.18.0] — 2026-10-29

One `studio/` per Block (b35 s01-D05): a topic's face names its rung, `**At:**`; `new_topic.py topic <Job|Task>` writes the topic into the Block's `studio/` with that line (the 261028 "a Task keeps its own Studio" is replaced). Address `bNN.jNN-sNN` (s01-D02), always after the folder name (s01-D03); the workbench row shows it, and a Job or Task page lists the Block topics at it (`frame.topic_address`, `frame._hung_here`).

## [0.17.0] — 2026-10-29

Idea slides take a named style, `"style"` in `sNN-<topic>.slides.json`; a Studio's is `sketch-notes` (JL 261029: "sketch note looks great"). Each slide records its `content`; haipipe-display `_parts/slide/scripts/slide_prompt.py` builds the prompt from the style and the content. The b15 glossy look is now the style `glossy-cartoon`, no longer the Studio default.

## [0.16.0] · 2026-10-29 · no s00; rounds live in the topic

- First principle (JL 261029): a Studio is never a report; what it shows is open ideas, options, pictures. Rule 6:
  everything a topic shows (drawing, mind map, slide) must pull a reader in within seconds; `ref/reader-review.md`
  starts with the attract test.

- A topic is the discussion (JL 261029); each working session or meeting is one round, `passes/pNN-<MMDD>/pass.md`
  inside the topic (Notes, Decided, Started, Read, Changed), written by `new_topic.py session [--kind meeting]`.
  `runs/run-draw-<sNN>/` is gone: Tools' 38 such Runs moved their 217 passes into their topics.
- A topic's life is its Stage, explore → shaping → agreed → closed; the workbench row shows it with the rounds.
- Slides (JL 261029: "这 studio 可能先做一个 slide"; "真正的 PPT slide"): `scripts/topic_slides.py` writes
  `sNN-<topic>.slides.html` and `.slides.pptx`: one illustrated picture per open idea (`sNN-<topic>.ideas.md`,
  image generation in the b15 deck's style, kept in `slides/`, recorded in `sNN-<topic>.slides.json`); never a
  slide that lists what was done. The Studio row gets a Slides button.

- s00-overview is retired (JL 261029: "以后像这种东西可能就不大有用了 我就直接把它删掉吧 ... 我们这个 mini map
  这不算 overview 吗？"): the workbench's Report › MindMap draws the Block from disk. `scripts/block_index.py`,
  `ref/background-index.md` and their tests are deleted; Tools' 15 `s00-overview/` folders and 2 `run-draw-s00/`
  Runs are deleted (git keeps them).

## [0.15.0] · 2026-10-28 · A topic lives at its own level

- JL 261028: Studio lives at every level. `new_topic.py topic <Job or Task>` makes the topic in that level's
  `studio/` (it used to climb to the Block); the number is free across the whole Block (`block_topics`), so a number
  names one topic. `session` finds the topic where it lives and writes `runs/run-draw-<sNN>/` beside it.
- `job_results.covered()` counts a Job's own topic. Tests: a child keeps its own topic; one numbering per Block.
- LLMRec b03: s21-s26 moved into their Jobs (`jNN_*/studio/`) and redrawn there.

## [0.14.10] · 2026-10-26 · s00 is s00-overview

- `block_index.py` draws `s00-overview/` (its builder `build_s00_overview.py`); SKILL.md,
  `ref/background-index.md` and the tests say so. Was s00-background-and-index; haipipe-project's audit renames an
  older one.

## [0.14.9] · 2026-10-26 · the mind map takes the topic's name

- The topic folder holds `sNN-<topic>.mindmap.md` beside `sNN-<topic>.md` and its drawing (was `mNN-<topic>…`):
  SKILL.md, `ref/topic-contract.md`, `new_topic.py`, which now starts the map with its root, Files and "Not written
  yet" (haipipe-mindmap `skeleton`).

## [0.14.8] — 2026-10-26

Commands to the excalidraw kinds now go through the door: `/excalidraw <kind>` (the `excalidraw-*` skills are hidden from the listing). (hide 261026)

## [0.14.7] · 2026-10-26 · every topic has two sides: its drawing and its mind map

- The mind map is now this skill's part, `_parts/mindmap/` (was the skill haipipe-mindmap, JL 261026: "the mindmap will
  also be in the haipipe-studio, they are linked to each other"), drawn as the draft's §1 Structure map in HTML and
  edited in place, not on a canvas.
- `scripts/new_topic.py topic` writes the face, then the topic's mind map `mNN-<topic>.mindmap.md` from it, so a new
  topic has both sides. Test: `test_a_new_topic_has_both_sides_its_drawing_and_its_mind_map`.
- SKILL.md § Two sides of a topic, and `ref/topic-contract.md`: the mNN files are the `.mindmap.md` and its static
  `.mindmap.html`; the card's Structured side edits the map in place.

## [0.14.6] · 2026-10-25 · a topic's structured side; drawings read as UTF-8

- `ref/topic-contract.md` and SKILL.md: the topic folder holds its structured side, `mNN-<topic>.mindmap.md` with
  its `.excalidraw`, `.png` and (git-ignored) `.mindmap.html`, made and synced by haipipe-mindmap; never the topic's
  main drawing. The workbench card switches Free and Structured (servers/workbench/frame.py).
- `scripts/render_png.py`: reads a drawing as UTF-8 (Windows read it in its code page), and falls back to Windows'
  fonts (Arial Unicode or Microsoft YaHei, Segoe UI, Arial; Cascadia Mono or Consolas; Segoe UI Emoji) when the Mac
  and Linux font paths are missing. `canvas.py` (its read, its write, the measuring font) and `shrink_media.py`
  read and write UTF-8 too.

## [0.14.5] · 2026-10-21 · who does a Task is never a topic

- `scripts/block_inventory.py`: `owner:`, `session:`, `codex-session:` and a face's own `goal:`, `close:` and
  `emoji:` lines are never a split (WHO), so `/wb update` stops proposing `s01-owner` (a fresh agent's b04 trial).

## [0.14.4] · 2026-10-20 · Feeds finds a report by its Question id

- `scripts/job_results.py`: a new results topic's **Feeds:** line reads the Job's `answers:` as Question ids (`Q01`,
  `Q-food-1`; a need `Q01.E2` counts for `Q01`) and names each one's `reports/<id>_<topic>/` folder; before, it read
  only `qNN_` folder names, so a Job answering `Q-food-1` was written "none yet" (b51 261020). `--jobs` with one Job
  now gives the one-Job title (`j01 · ext food: current results`), not "ext food and more". Test:
  `test_feeds_find_the_report_of_each_answered_id`.

## [0.14.3] · 2026-10-19 · The reviewer knows a plan topic

- `ref/reader-review.md` names the questions for a paper's s03-paper-dataflow and s04-paper-workflow (haipipe-paper-
  plan's four), and that a gap only the drawer can close goes to the drawer's owner once instead of another round (a
  fresh-agent test looped twice on it).

## [0.14.2] · 2026-10-19 · A topic opens centred

- A Studio topic a person clicks open scrolls so its drawing sits in the middle of the window, and the drawing
  inside is fitted and centred once its frame has a real size (JL 261019: "How do you make it, when I click it, the
  draw will in the center of the page"). `servers/workbench/frame.py` (STUDIO_JS: a clicked row scrolls to the
  centre; rows the page opens itself do not jump) and `servers/workbench/assets/xcal-boot.js` (the fit waits, at
  most 2 s, for the frame's size, then is made again). Checked in headless Chrome at 1440 x 900: the s02 drawing
  sits at 120 to 780 px, the whole story fitted at 17%.

**[0.14.1] · 2026-10-19 · s10-s19 is a paper Board's related work (JL 261019)**

- Numbering: on a paper Board, s10 is the related-work map and s11-s19 one topic per type of closest work,
  owned by the new `haipipe-paper-related` (JL 261019: "for the related work we can do things like
  s10-related-work, and after that, we have s11 s12, etc"). A paper Board draws no level topics, so the band is free.
- `new_topic.py`: `--band related` takes the next free s10-s19.

**[0.14.0] · 2026-10-16 · The Studio screen folds in from workbench-studio (JL 261016, s21-D05)**

- `workbench-studio` is retired into this skill: its manual is `ref/screen.md`, its lane contracts `ref/chat.md` and
  `ref/draw.md`, its table `ref/workbench-table.md`, its changelog `ref/history/workbench-studio-CHANGELOG.md`.
  `SKILL.md` gains a short "The Studio screen" section and the screen's triggers (`/workbench-studio` stays one).
- Relative links in the moved files re-pointed to `../../../workbench/workbench/` and `../../../draft/`.

**[0.13.24] · 2026-10-15 · a Job's Runs list names each Run's own state**

- `job_results.tally` named every blocked, running or draft Run "partly", while excalidraw-job's drawing named it
  blocked (found by the b13 reader review, 261014: "8 partly" beside "8 blocked"). The list now says each 🔶 Run's own
  word: `8 Runs: 8 blocked`.

**[0.13.23] · 2026-10-14 · canvas.stairs and canvas.grid count results that rise above a frame**

- excalidraw-job 0.7.4 centres a staircase's results on it, so they may rise above its top as far as they hang below
  (JL 261014: "超出部分一定要对称、均匀"). `canvas.stairs` now puts the next frame's highest follower, not its own
  edge, below the last frame and its followers; `canvas.grid` gives a row the room its followers take above it.

**[0.13.22] · 2026-10-14 · s41-s49: Task procedures**

- A new band, s41-s49, for one topic per Task type of a theme, named `sNN-task-<type>-procedure`: its steps,
  Runs, disk, tabs and prompts (b15 s41-task-items-procedure, JL 261014: "it should be a new series").
  `new_topic.py --band procedure`. s51-s59 stays the server band.

**[0.13.21] · 2026-10-14 · canvas.stairs moves what follows a frame**

- `canvas.stairs` moved a frame and what is drawn in it, but not what is marked `customData.follows` its id (a
  staircase's results, drawn outside it), so a second staircase frame left its results behind; it now moves them, as
  `canvas.grid` did (excalidraw-job 0.7.2, two staircases for a big Job).
- The next frame now starts below the last one's followers too, not only below its own edge: a tall results block
  (two charts beside a 12-Task family step) had run into the second staircase's results.

**[0.13.20] · 2026-10-13 · Stata esttab tables read as rows; small numbers stay plain**

- `job_results.load` reads a Stata esttab CSV (every cell `="…"`) through `esttab_rows`: each cell whole (a comma
  inside `="1,208,934"` is not a column), the title and notes dropped, the first column `term`, a standard-error row
  `<term>_se`; so `tables:` and `show` can pick `term=trait_l2.(5)`. Found on Physician-SPACE OpioidRx's v0618 cohort
  tables, which excalidraw-job could not show (261013).
- `number`: 0.0000375, never 3.75e-05.
- Test: `test_an_esttab_csv_reads_as_rows_and_small_numbers_stay_plain`.

**[0.13.19] · 2026-10-13 · Frames as stairs, a small frame that explains, a name with a dot**

- `canvas.stairs(els, order, gap, step)`: the main frame at the origin, each next frame lower and further right
  (JL 261013: "你不能每一个都是朝左对齐"); every frame placed once; each moves with what is drawn in it. New test.
- `canvas.explains(frame)` / `is_explains`: a frame small on purpose, explaining the main one ("主次分明 … 大小有致");
  excalidraw-studio's check.py reads it.
- `job_results.dig`: a name with a dot in it (`codex-gpt-5.6-luna`) is matched whole, as a JSON key and in a CSV
  row's `col=value`; every other path reads as before.

**[0.13.18] · 2026-10-13 · job_results reads a Stata Task's older layout and a CSV table**

- Asked 261013 (Physician-SPACE OpioidRx: "report the results of each job as the new sNN"): the Stata Blocks keep
  `results/run_<cohort>_<window>_<model>_<trait>/` and `results/<trait>/rNN_<…>/`; `runs_of` now finds both, so a Job or
  Task drawing lists those Runs and their state instead of "no Run yet".
- `state_of`: a result folder whose files sit one level down (`tables/`, `describe/`) reads as a result on disk.
- `load` reads a `.csv` as its rows (numbers as numbers) and `dig` picks a row by `col=value&col2=value2`, so a face can
  show `tables/h2-slopes.csv:model_id=m5&context=lbp.estimate` read from disk on every build. New test.

**[0.13.17] · 2026-10-12 · Folder, the Studio's fourth folding part; an undated decision is left off the Timeline**

- JL 261012: "在 related 和 timeline 下面再搞一个 folder，这样我就可以看到这些 folder 里面（也就是这个 block 的 folder）
  都长什么内容". The Studio folds a fourth part under Timeline, Folder: the Block's own folder as one tree, a folder
  with its count and what it is for, a file opening in the pop-out (workbench 1.23.0; b10 s09-block-folder).
- The Timeline paragraph said a decision with no date "is listed at its end"; since b10 s08-D10 it is left off.
- A retired number asked back: b10's Folder topic was first made as s33, since s09 had merged into s01 that morning
  and its decisions keep their ids there (s01-D37); JL then asked for it as s09-block-folder. Its decisions start at
  s09-D10, after the old D01 to D09, and the old `runs/run-draw-s09/` moved to s01's `history/run-draw-s09/`, so the
  Timeline does not read the old session as the new topic's. The Numbering section says how.
- `new_topic.py`'s next free number reads only the folders on disk, so it would hand out a retired number (s07 in
  b10); pass `--nn` until it knows them.

**[0.13.16] · 2026-10-12 · A small s00 background merges into the index; every s00 redrawn**

JL 261012 ("yes, please do it") on redrawing every Block's s00 with 0.13.13's acts and key points. The first pass left
74 of 112 Blocks with one failing check: the default "🧭 What this Block stands on" tree drew a frame of about
1480 x 556, under a third of a screen, which excalidraw-studio reads as a slide. A tree background that small now
merges into the top of the index frame, under its title (`merge_into_index`, excalidraw-studio's "a thin frame is
merged, not padded"): its heading, tree and green notes stay; its key box goes, and so does an opening line that only
repeats the spine, since the Block's box already says it. Several merge in their own order. The acts are numbered by
position, so a drawing with no story row starts at Act 1, and the made act says "and what we propose next" only when
there is a proposals frame. All 112 s00 drawings in Tools, WellDoc, Knowledge-Base and jluo41-repo are redrawn.
`block_index.py --draw` now prints each drawing's path relative to its SPACE (the folder with env.sh, else its
repository), never /Users/... (AGENTS.md rule 12; found by b31-s01).

**[0.13.15] · 2026-10-12 · A Job's topic can show the whole Job**

Asked 261012 on Proj10 b01's s21 to s23, which showed only their Runs' states: "我想在这个桌上把这个 job 的所有内容都展示出来".
The new `excalidraw-job` skill draws a Job as four frames (why, in → Tasks → out, what it concluded, its tables,
formulas and pictures), reading Tasks, Runs and states through `job_results.py`'s readers; its `adopt` turns a one-Job
results topic into the whole Job. "A Job's current results" says when to use it; the Boundary table names it.

**[0.13.14] · 2026-10-12 · The palette keeps the key-point colour**

Found by b10 s52's redraw (261012): a builder writing with `canvas.write`'s default palette lost every key point,
since `apply_palette` turned each fill but white transparent; only `Drawing.write` (palette off) kept them.
`canvas.KEY` (#fff3bf, excalidraw-studio's principle 5) is now part of the studio look: `apply_palette` keeps it
and `off_palette` does not report it. The skeleton test checks both. No drawing changes until it is rebuilt, and
a rebuilt one changes only where a builder drew that colour.

**[0.13.13] · 2026-10-12 · s00 takes excalidraw-studio's principles where they fit its shape**

JL 261012, through b31-s01: bring the s00 index drawings closer to excalidraw-studio's principles, only where they
fit s00's own shape. Each frame's key point now sits on the one slight colour (#fff3bf, principle 5): the opening line
of the Studio plan, the background and the proposals, and the index's root box (the Block and why it exists). The
frames are two acts (principle 3), each a row named at the left: "Act 1 · The story, and what the Block stands on"
(plan ─stands on─▶ background) and "Act 2 · What is made, and what we propose next" (index ─still needs─▶
proposals), with "is made so far as" from the plan down to the index; laid out by excalidraw-studio's
`Drawing.acts`. The drawing is written with the palette off so the key colour stays. The frames keep s00's shape
(trees, boxes, emoji, plan, proposals); topic_map.py, which also draws sNN topics, is unchanged. b10's s00 is
redrawn; the other Blocks' wait for JL.

**[0.13.12] · 2026-10-12 · ④ reads as rows: gap, topic, Job, what it delivers**

JL 261012, on b10's s00 without a proposals frame: "for the s00, we will also have the proposed sNN and jNN, how do
you think we should add a new frame for it?" ④ is now one row per proposal, read left to right like the index:
❓ the gap it closes (the proposal's `why`) ─▶ 🧠 the topic ─▶ 🧱 the Job ─▶ 🏁 what it delivers. A proposed topic
and the first Job resting on it share a row; a Job left over sits beside the made topic it rests on, in black. Drawn
by `block_index.proposal_rows` and `proposals_frame` (no longer topic_map's box grid). b10 got its first proposals
(s14, j01 to j03), and b10 and b31 are redrawn.

**[0.13.11] · 2026-10-12 · Linked to excalidraw-studio**

Asked 261012: "will the /haipipe-studio call the skill of /excalidraw-studio? Could you link them". The description,
the opening and "Add, redraw, save" now send a topic's drawing to `/excalidraw-studio` (load it before drawing or
redrawing; its `check.py` after); the Boundary names it. `new_topic.py --builder` writes a builder on
excalidraw-studio's `draw.py` (a frame, its key point, a workflow map, the density badge, an act), so a new topic
starts on the principles; the skeleton test allows the one key-point colour.

**[0.13.10] · 2026-10-12 · s00's proposals get their own frame**

JL 261012: "we also need to propose the new studio and new jobs in a new frame". The proposed topics and Jobs
not made yet leave the index (0.13.8 drew them as rows there) for a last frame, "💡 what we propose next"
(`proposals_frame`): red dashed boxes with status, question or condition and finish, arrows from each topic to the
Jobs that rest on it, and a made topic they rest on beside them in black. The index keeps what is on disk and one
red line per branch naming the proposals; the Studio plan no longer lists proposed Jobs. A proposal may carry a
`why`, the gap it closes. `topic_map` boxes take `proposed: true` (red dashed edge and title). b31 redrawn.

**[0.13.9] · 2026-10-12 · Register generated S00 topics in Workbench**

The shared S00 generator now leaves a local `build_s00_overview.py` runner pointing through
the owning SPACE's `Tools` symlink. The current Workbench recognizes `build_*.py` as generated drawings;
without this runner S00 incorrectly offered the hand-drawn Edit control. The runner calls the current
shared generator on every rebuild, uses a relative path, and preserves an existing local builder.

**[0.13.8] · 2026-10-12 · s00 draws proposed topics and Jobs**

Asked 261012, through the b31 session: "s00 should also work in a way for the proposing the sNN and jNN as well."
`block_index.py` reads the face's `job_proposals` yaml beside `studio_proposals`. In the index, each topic or Job
proposed but not made is a red dashed row at the end of its branch (`⬜ jNN_<slug> · title [status]`, what it rests
on, a dashed arrow to its finish), until its folder exists; a Job number already taken is flagged. The Studio plan
lists each proposed Job under the topics it rests on. b31 is the first to use it (s22, s23, j01, j02).

**[0.13.7] · 2026-10-12 · The look moves to excalidraw-studio**

Asked 261012 ("should we also have a excalidraw-studio?", then "please go ahead and do it"): how a topic's drawing
reads is now its own skill, `excalidraw-studio` (b31 s01-D08): the six principles agreed on b31
s01-drawing-principles and the drawing helpers every builder imports (`scripts/draw.py`). "The look" here opens by
pointing to it and keeps what `canvas.py` enforces; the tree, boxes and emoji shape is s00's alone.

**[0.13.6] · 2026-10-12 · s00's index: one row per item**

JL 261012, on b10's index: "This one can be larger, of height. Currently it is too compact. each studio should be a
row."; then "this one is much better". `block_index.py` draws the index in one column, each topic and Job its own
row (box, then an arrow to what it leads to), the frame growing down as far as its rows need; the two- and
three-column layouts and the detail steps are gone. s00 may also open with a Studio plan frame, drawn from the
face's `studio_plan` yaml (story steps with named arrows; b32 EB1A's first frame, b10 the first to use it). SKILL.md's
s00 section says so, with the sizes and the language rule.

**[0.13.5] · 2026-10-12 · The tree is s00's alone**

JL 261012: "I think you ruin the whole things. I just mean for the s00 to have the tree, why you make all the
others to be the tree as well...." 0.12.0 to 0.13.4 made every topic three frames of trees in boxes; that rule was
meant for s00 only. Now: `canvas.frame_limit` and the slide warning (`sparse`) apply to a Block's s00 only
(`canvas.is_s00`); "The look" no longer asks other topics for three frames or trees; the s00 section keeps the
rule. b10 s02 and s51 are back to their drawings before today (5 and 9 frames); the RunSkill session restores s03,
s05, s06, s07 and s21. `topic_map.py` stays, as s00's drawing engine and an optional tool.

**[0.13.4] · 2026-10-12 · A topic leads with its own picture**

JL 261012, on s07 redrawn under 0.13.0: "why s07 following the index????? it is very weird." The 0.13.0 order
(① Background ② Map ③ one more) made every topic copy s00's shape. Now: ① the topic's own picture, first and
largest (its screen, its flow, the tree of its subject); ② a working map only if its parts need explaining; ③ a
background only if a newcomer needs it, short and last. `topic_map.draw_topic(..., lead=)` draws a builder's frame
(a screen) before the face's frames. b10 s02 and s51 reordered: s02 opens on the Studio screen, s51 on one request.

**[0.13.3] · 2026-10-12 · s00 also proposes the Studios still needed**

The Block's background index includes grounded Studio candidates with their
question, source Jobs/Tasks, expected output, suggested group and priority.
`ref/background-index.md` keeps proposals separate from actual folders, stages
and inventory counts; it recommends a first batch without creating the topics.

**[0.13.2] · 2026-10-12 · s00's index is a mind map**

JL 261012, on b32 EB1A's background index: "for the index, I love this type of things"; "This type of the tree";
"This is more like the mindmap, right?". `block_index.py` draws the index left to right: the Block (state, why it
exists, done when, now) ─thinks in─▶ Studio and ─works in─▶ Jobs, then each topic (under the Block's Studio groups,
what it is about, its first open point) and each Job (state · steps or Tasks done · waiting, next step), each with
an arrow to what it leads to: the Questions a topic feeds, what a Job must deliver (its `close:`, or the face's
optional `index:` plan), dashed when on hold; a Question nobody feeds and Jobs with no `close:` line are one red
note each. Each topic and Job is its own box: its name, what it is for (the face's **Topic:** line, or the Job's
state, steps and next step), and where it leads (JL 261012: "I want to focus on eahc item ... the studio item and
job item should have the box as well"; "we might also want to understand what is this studio item for"). No counts
anywhere, they go stale ("number like this is meaning less, this will change"; "what is the 7 open for???? that is
meaningless"), and no links ("no need to add the link"). Text is measured with a real font; one column of boxes when
it fits, else two or three, a group cut in two labelled "continued". `topic_map.draw_topic(..., fill=)` lets a
builder put live facts into the face's frames (the RunSkill session's ask). All 82 s00s redrawn.

**[0.13.1] · 2026-10-12 · Groups are proposed with the topics; a kind is not the Block's name**

`ref/infer-topics.md` § Groups: `/wb update` proposes each topic's group with it, named for a subject of the
Block's work, never the Block's name or a status (b10_aidatastore's first pass used `Aidatastore` for all three,
caught by the cold review), two to six per Block, in topic order in `studio/_groups.txt`, none on s00 (JL 261012:
"for the studio's group tags, during the updating, you will propose them yourself"). `scripts/block_inventory.py`
skips a Task name's first word when it only repeats the Block's subject: `t01_aidatastore_materialize` in
b10_aidatastore is a materialize Task.

**[0.13.0] · 2026-10-12 · Trees in boxes, joined by arrows; emoji on every node**

JL 261012: "it is not that vivid ... add the things like the emoji", then "the tree is the pure tree here, there
are no logic between them ... we need to display, show the index, and also need to explain, why we have them, so we
can have both tree and box, and -->". `scripts/topic_map.py` (new) draws a topic's frames from a `frames:` yaml in its
face: a folder tree, or boxes (each with an emoji title, a why line and its own tree) on a grid joined by named
arrows (a "?" label is red and dashed: a link not recorded yet); `draw_topic(folder, extra=...)` adds a builder's own
frame, such as a screen. `block_index.py` draws s00's index as that map (Block → Studio → Questions ← Jobs →
delivery, related → Studio), its arrows counted from the faces (a topic's **Feeds:**, a Job's or Task's `answers:`,
a Job's delivery/ files); it steps down from full detail to one line per topic or Job until the frame fits 2800 x
1600; every node leads with a state or thing emoji; a background entry may be `boxes:` + `arrows:`. A Task's state
word is read from its head only ("🟡 PARTIAL · r03 done" is partly). `render_png.py` draws emoji in colour (Apple
Color Emoji), keycaps and joined emoji whole. `canvas.tree_text` draws a leaf starting ❓ red.

Readable zoomed out (JL 261012: "If I just zoom in, how could I make it still readabale? SHould we give the box a
large font size things?"): frame titles 48 px, box titles 36, why lines and arrow labels 24, trees 20; boxes and
arrows 3 px. A box takes the most tree columns its column's width allows. A map frame (customData map) needs two
thirds of SPARSE_MIN words (`MAP_SHARE`): its boxes and arrows carry meaning.

The index groups its topics by the Block's own Studio groups, as the workbench's group bar does (JL 261012: "what
is the rational you grouping these stadio items?"): a topic under its first **Tags:** tag, the groups in
studio/_groups.txt order with the bar's emoji (frame.group_emoji), its other tags on its line; the numbering bands
cut into fours are gone.

`frame_limit` counts only a topic's own drawing, `sNN-<topic>.excalidraw`; a reference drawing beside it, whose
frames reports may cite, is not counted. `canvas.UI_KIND` (b10 s01-D16, from the RunSkill session): a box marked
customData ui_kind "fixed" or "suggested" in a ui_frame takes the workbench's group-button colours, gray and amber.
b10 s02 and s51 redrawn as three map frames; all 82 s00s redrawn; tests 22.

**[0.12.2] · 2026-10-12 · `--feeds` takes a report folder either way**

`new_topic.py topic --feeds reports/q01_x` wrote `**Feeds:** \`reports/\` reports/q01_x`, a link that does not
open (three b10_aidatastore topics, found by the cold review after `/wb update`). A leading `reports/` is now
dropped, so `reports/q01_x` and `q01_x` give the same line.

**[0.12.1] · 2026-10-12 · Background indexes connect work to its finish**

`ref/background-index.md` explains the reader's path from a Block's purpose to
every Studio and Job, then to its expected output. Folder branches show ownership;
arrows show grounded relationships, with proposed outputs separate from current
state. It keeps the disk-derived s00 inventory, older topic paths, source dates
and human marks, and checks completeness and connected endpoints. Equal-card
grids are not the default for this work map; slides, screens and report figures
retain their own contracts. The discovery description is shortened and validates
with Codex skill metadata rules.

**[0.12.0] · 2026-10-12 · Three frames, each a tree; s00 in every Block**

A topic's drawing is three frames at most, ① its Background, ② its Tree, ③ one more (a screen or the
reference), each a folder tree, never a row of slide-like frames (JL 261012: "每一个 frame 都太像一张 slide，而且每个
frame 里的内容又太少，它本身又不是一个 tree 结构 ... 我个人更 prefer 那种 tree 结构，就像 folder tree 那样"). `canvas.tree()`
draws one ("? " leaves red, "✎ " green); `canvas.write` warns over `MAX_FRAMES` (`frame_limit`: s32, s61-s69,
reports, Guides and `reads_down` pieces not counted) and on a frame under `SPARSE_MIN` words per million px
(`sparse`, which skips a frame with no words or over FRAME_MAX). Every Block gets `s00-overview/`
(JL 261012: "for every block, we also want to have the s00-overview"): `scripts/block_index.py <block>
--draw` (or `--all <root>`) draws the face's background trees, then the index read from disk (each topic's stage,
decisions, passes and first open point; each Job's Tasks and their states; Questions, related, delivery); a
Block without the face gets one seeded from its own. Drawn for all 84 Blocks of Tools and WellDoc; b11's and
b12's `s00-*-structure` became s04. First written by b31_prep_ai's session (canvas.tree, sparse, block_index.py).

**[0.11.1] · 2026-10-12 · A status field is not a topic**

`scripts/block_inventory.py` no longer offers `state:`, `status:`, `stage:` or a date as a split to build a
topic on: b01_sourcestore's `state:` (DONE 124 · PARTIAL 11) and b51_externalstore's (SETTLED 31 · OPEN 23)
came back as topics in the first `/wb update` dry runs. Where the work stands can still ground a Question.

**[0.11.0] · 2026-10-12 · A screen in its own colours**

A frame that draws the workbench's screen is marked `canvas.ui_frame(frame)`, and `canvas.write` colours what
is drawn in it with the workbench's own light colours (`canvas.UI`, `STAGE_UI`, `STATUS_UI`, read from
`servers/workbench/frame.py`): gray panes behind white buttons, the open tab blue, a proposed button violet
dashed, stage pills, links, status words and count bars in their screen colours (JL 261012: "make the UI to
be more colorful, like the same to what we see"). A pane moves behind what it holds. Red questions, green
notes, arrows and every frame not marked stay as before. First used in b10 s02, s03, s05 to s08.

**[0.10.0] · 2026-10-12 · Topics inferred from a Block's work**

`scripts/block_inventory.py <block>` reads every Job and Task face of a Block (writes nothing) and prints what
repeats: Task kinds across Jobs, the fields that split them, the sub-questions most Tasks of a kind answer and
how their answers spread, and what stands out; then candidate topics and Questions, each naming its Tasks.
`ref/infer-topics.md`: a recurring kind is a method topic, a split one topic, no work no topic (JL 261012:
"learn how to infer the relevant studios from the existing block job and task"; b10 s10). Worked on b00_rawdata.

**[0.9.2] · 2026-10-11 · A topic's Run starts with its close rule**

`new_topic.py session` writes the close rule into the ticket when a topic's first session makes
`run-draw-<sNN>`: a person moves the topic's Stage to agreed, or names what is still wrong in red on the
drawing (`DRAW_CLOSE`). It used to leave `close: <what settles it>`, so the Run had no end (b10 s06-D06).

**[0.9.1] · 2026-10-11 · The Timeline runs down one axis**

The Studio's Timeline is one axis down the page, oldest day at the top, at three levels (Days · Topics ·
Everything); its own topic is b10 s08-studio-timeline (JL 261011). A drawing's sample of a change note must
not start with ✎, or the Timeline reads it as one.

**[0.9.0] · 2026-10-11 · The Studio's Timeline reads each decision's date**

Timeline folds under Related in the Studio (JL 261011: "add another section of the Timeline"): what moved
when, newest day first, following the group bar. It reads a decision's date in its brackets, a session's
pass `pNN-<MMDD>` and a drawing's green `✎ <YYMMDD>` notes; Groups in SKILL.md says so, and that a
decision with no date is listed at the end.

**[0.8.4] · 2026-10-11 · Related's groups start from its subfolders**

In Related, under the topics, an item's subfolder is its first group (`meetings/` → meetings), the row's `group` cell adds more (b10 s04-D08); the folder belongs to the new `haipipe-related`.

**[0.8.3] · 2026-10-11 · Side notes smaller than the content**

A note beside the main content (excalidraw-draft: the change, why and who answers, beside the
page pictures) is written smaller than the pictures it explains (JL 261011: "The content or the font size,
can be much smaller, than the main content"). `canvas.aside(e)` marks such a note, and `small_text` leaves it
out, as it leaves out green change notes.

**[0.8.2] · 2026-10-10 · A topic's stage**

Each topic face carries a `**Stage:**` line: explore · shaping · agreed · closed (b10 s09-D03).
A person moves it with a decision row; the gate only counts. `new_topic.py` writes `explore`;
the shared Studio shows the stage as a badge on each card, "no stage" when the line is missing.

**[0.8.1] · 2026-10-10 · Block topics and recommended count**

Recommend at most 10 topics per Block, counting folders rather than sNN values.
The writer resolves Job/Task inputs to their Block and reminds above ten without
refusing creation. Existing topics and legacy session reads stay intact.

## [0.8.0] · 2026-10-10 · A proposal topic

- b21_event_cgm's s03 (SHIFT Task 2.1) is the worked example of a topic that works on one section of a
  proposal or a paper (JL 261010, on its drawing: "I think this one is very very great!"). Five frames in
  two rows: ① the idea workflow, ② why and the plan, ③ the proposal figure, each one screen; ④ the draft
  today marked up and ⑤ the section written out, each one frame read down. The rules of each frame, the
  section-written-out layout (tight text rows, evidence cards free in two columns joined by lines that go
  around cards, a one-line card instead of a line longer than a screen, the figure as a DISPLAY item), where
  the words live (the face's yaml; a draft passage found by its anchors), what went wrong on the way, and
  the builders to copy from: `ref/topic-contract.md` § A proposal topic; a short section in SKILL.md.
- `canvas.numbered_frames(els)` finds one piece cut into numbered frames ("X · 1", "X · 2"), and
  `canvas.write` warns about it (JL asked twice on 261010 for one frame instead of many: b32_aid_ai's s03 and b21_event_cgm's s03). Tested.

## [0.7.1] · 2026-10-10 · One long piece, one frame

- A piece read top to bottom (a section written out, a draft's pages marked up) stays ONE frame that grows
  down; only its width must fit the screen (JL 261010, after b21_event_cgm's s03 had cut Task 2.1 written out
  into 9 frames and the marked-up draft into 4: "the draft take should be one single frame, and the Written
  out should be one large frame"). `canvas.reads_down(frame)` marks such a frame (`customData.reads`), and
  `canvas.oversized` then checks its width only. 0.7.0's "longer material takes more frames in rows" is
  withdrawn. SKILL.md (The look), `ref/topic-contract.md`, tested in `tests/test_haipipe_studio.py`.

## [0.7.0] · 2026-10-10 · Each frame fits the screen

- A frame is sized to read on one screen: the whole frame at 50% zoom, most of it at 100% (JL 261010, on
  the 9,200 x 5,650 px idea frame of b21_event_cgm's s03: "This is too huge, what I want is: when I zoom in
  50% I can read the whole workflow, when I read 100%, I can see most part of the frame"). About
  2560 x 1440 px, the workbench's 1280 x 720 pane at 50% zoom, at most 2800 x 1600 (`canvas.FRAME_MAX`);
  body words 20 px or more (`canvas.TEXT_MIN`); room comes from fewer words and boxes sized to them, never
  from scaling the drawing down (that shrinks the words), and longer material takes more frames in rows.
  `canvas.oversized(els)` lists the frames over the size, `canvas.small_text(els)` the frames whose words
  are mostly under 20 px (green notes not counted), and `canvas.write` warns about each. "One idea, one large frame" now reads "one
  dense frame": large means much information, not a large canvas. SKILL.md (The look),
  `ref/topic-contract.md`, tested in `tests/test_haipipe_studio.py`.
- `render_png.py` stacks a text's lines at the canvas's own line height (1.25 x the font size), so a
  preview no longer draws lines over the next box's words.

## [0.6.1] · 2026-10-10 · One idea, one large frame

- A topic's idea is one big connected frame, dense with facts, its key part largest; extra frames only for
  separate material such as a marked-up source (JL 261010 to a Codex session that split s03 of
  b32_aid_ai into 12 frames: "你这么多 frame，其实只相当于我的一个 frame"). In SKILL.md (The look) and
  `ref/topic-contract.md`.

## [0.6.0] · 2026-10-09 · Frames in rows

- `canvas.grid(els, rows, gap)` places a drawing's frames in rows, read left to right and then down;
  each frame moves with what is drawn in it (JL 261009, on a studio topic of 8 frames stacked 11,600 px
  tall: "don't put all the things in one column, I told you"). `canvas.one_column(els)` finds the old
  layout and `canvas.write` warns about it. The rule is in SKILL.md (The look) and
  `ref/topic-contract.md`; tested in `tests/test_haipipe_studio.py`.

## [0.5.0] · 2026-10-09 · One readable font

- Every word a builder writes is Nunito, Excalidraw's "Normal" font (`canvas.FONT` = 6), and code
  stays Cascadia (`canvas.CODE_FONT` = 3) (JL 261009, on a drawing in Comic Shanns with notes in
  Virgil: "I think the font should be more readable, change it"). `canvas.write` applies it with
  the palette (`apply_font`); `change_note` and the `new_topic.py` builder template write it. A
  person's own marks and a slide draft keep their fonts. Every studio drawing takes the font on its
  next rebuild.

## [0.4.1] · 2026-10-08 · Change notes on a slide draft

- A slide draft's change note about one slide sits only under that slide, not repeated in the title
  frame (JL 261008: "why this is not under each slide?"); the rule is excalidraw-slide's.

## [0.4.0] · 2026-10-07 · Slide drafts drawn by excalidraw-slide

- How a slide draft is drawn moved to the new `excalidraw-slide` skill (JL 261007: "go"), words kept:
  SKILL.md § Slide drafts and `ref/topic-contract.md` § A slide draft are now pointers. This skill keeps
  the s61-s69 band, the folder, the face, the sessions and the palette exemption. `canvas.ACCENT ·
  ACCENT_FILL · MUTED` stay, the same values as `slide_kit`'s, for the builders that read them here.
- `canvas.assign_ids` gives ids by position: two elements a builder gave one id stay two (b11). `write`
  warns when a canvas has no snapshot and no seed ids, so another writer's drawing is not doubled.

## [0.3.1] · 2026-10-07 · A slide draft keeps its deck

- The deck lives with its draft (JL 261007: "we can have the delivery in the s61 as well"):
  `studio/s6N-<deck>/build_deck.py` writes `studio/s6N-<deck>/delivery/<deck>.pptx · .pdf`; the
  level's `delivery/` holds a pointer, never a copy.

## [0.3.0] · 2026-10-07 · Slide drafts

- New kind of topic, s61-s69 (JL 261007: "one type is about propose the slide draft"): a proposed
  deck drawn before it is built, from one `slides.py` the deck writer also reads. Frames left to
  right: logic flow · the slides (half size, one skeleton) · on disk and open. `new_topic.py --band
  slides`; SKILL.md § Slide drafts; `ref/topic-contract.md` § A slide draft.
- The one colour exception (JL 261007: "make the slide to be a bit colorful by highlight the
  important things"): inside a slide, one accent marks its key thing. `canvas.ACCENT · ACCENT_FILL ·
  MUTED`, and `canvas.off_palette(els, slides=True)` allows them.

## [0.2.0] · 2026-10-07 · Change notes; the old copies retired

- `canvas.write` enforces the look (JL 261007, "Recolour all"): `apply_palette` maps any other stroke
  to black and drops fills in the builder's elements; images, transparent strokes and the person's
  marks untouched; slide drafts (s61-s69) exempt (JL: "but for the slide draft, maybe not").
- The look (JL 261007: "just the color of black, with red for uncertainty questions, and green for
  our previous changes"): trees, lines and boxes in black; red for an uncertain question; green for
  a change. `canvas.INK · RED · GREEN` and `canvas.off_palette(els)`.
- Every change to a drawing gets a short green note where it changed, `✎ <YYMMDD> <what changed>`,
  and the same line in the title frame (JL 261007: "when I change the draw, you can leave the short
  green comments to where we changed"). `canvas.change_note(x, y, what, date, frame)` makes the
  note; the builder skeleton keeps a `CHANGES` list and draws it in the title frame.
- b03 s21 phase 5: every builder imports `canvas` from `scripts/` here; the copies in b03's
  `studio/_build/` are retired. `canvas.LEGACY_DIRS` stays for a Block that still keeps older
  snapshots in a folder of its own.

## [0.1.0] · 2026-10-07 · New: the Idea Studio at any level (b03 s21)

- New skill (JL 261007: "what skill we should have for the studio and for the report").
- `ref/topic-contract.md`: `sNN-<topic>/` at any level, its face (Topic · Feeds · Files ·
  Decided · Open, the marks the Idea Studio reads), the numbering (s0x concepts · s1x levels ·
  s2x runs and skills · s3x Guide · s5x server), builders that keep a person's marks, previews,
  sessions as passes of `run-draw-<sNN>`, the buttons.
- `scripts/canvas.py` and `scripts/render_png.py` moved in from b03's design `studio/_build/`,
  which keeps shims so every Block's builders still import them. `canvas.legacy_seed` now looks
  only in `canvas.LEGACY_DIRS`, which a shim fills with its own folder.
- `scripts/new_topic.py`: new, `topic` (the scaffold, `--builder` writes and runs a builder) and
  `session` (a pass of `run-draw-<sNN>`, through haipipe-run's `soft_run.py`).
