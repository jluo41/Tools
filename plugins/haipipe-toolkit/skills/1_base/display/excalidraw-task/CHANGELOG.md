excalidraw-task · Changelog
===========================

## [0.6.0] · 2026-10-14 · A board or cover, read for the reader

- JL 261014, on 海安雨's video covers in his GitHub index (each one the finished whiteboard, no text): "you can try
  to add your comments and understanding for the readers".
- `task_drawing.py`: `board_frame` draws "rNN · The board, read" (or "The cover, read" for `kind: cover`, a paper
  video's first slide) from the topic's `reads/<rid>-*/board.yaml`, in the transcript frame's layout: the picture
  on the left, each part outlined and numbered, one note per part on the right (Board shows · Our reading · → this
  Task). Outlines only (a fill hid the picture in the png); yellow on a cover's dark slide. The picture is copied
  to `assets/<rid>-board.jpg`, since `embed` keys a picture by its file name.
- `draw_task` (rows) and `task_stairs.draw_task` (with `detail: true`) put it before the transcript frame; a topic
  with no board.yaml draws as before.
- After a cold reviewer: a box's number moves to its top-right corner when its top-left sits in an earlier box;
  the line under the title says what a note holds and what → names; covers embedded at JPEG q60.
- First drawn: Proj10 b13 s31 (r06 board, r07 and r08 covers).

## [0.5.0] · 2026-10-13 · The staircase: a Task's sources as steps, their results beside them

- JL 261013: "you should also think about how to update the /excalidraw-task as well, we try to follow the same idea",
  after excalidraw-job 0.6.0's staircase ("主次分明", "阶梯状的结构", "你的 results 应该是图和表格呀").
- `scripts/task_stairs.py`, the default (`draw_task` sends every Task there unless `layout: rows | plain`): ① the
  Task's question on top, each Run or video a step lower and right in reading order (its name, key point, what it
  ran, its role in the reading order on its stair); `current: true` marks the Run to read, the others go quiet.
- Each step's results outside the frame, small and level with it: `charts` (excalidraw-job's chart_png from the
  Run's result), its `show` numbers as a table, its `plot` curves, two `shots`, the pictures its result holds;
  without face words, the numbers its result names or its `summary.headline`; `check` (else the page's) in red; its
  link. Steps are spaced to their measured results, so each line runs straight across.
- ② words to know, formulas (mathtext), be ready to answer, open: small (`canvas.explains`); ③ the transcript and
  full frames only with `detail: true`. Frames placed by `canvas.stairs`.
- Tests read the staircase: reading order as steps moving right, the face's words, roles, checks, links; nothing
  under 28 px in ①.
- First drawn: LLMRec b04 j08 t02 (a work Task) and Proj10 b51 t01 (six videos), as previews.

## [0.4.3] · 2026-10-13 · Long transcripts, rolled out

- Rolled out to every video Task of Proj10's b11 (37) and b51 (10), at JL's ask (261012: "please go ahead to add it
  all of the discoveries we have found"): 205 videos, each with a reading of its Run's transcript PDF; 1,779 quotes,
  all matched in the PDF.
- A transcript of more than `LONG_PDF` = 4 pages shows only its pages with passages, each cut between whole lines
  from a few lines above its first passage to a few below its last (`<rid>-transcript-p<N>-band.jpg`), and the frame's
  subtitle says so ("42 pages, the 9 with passages shown"). b11 s39 r08, a 2h 26m video, has 42 pages: its topic went
  from 46 MB to 12 MB. `transcript_pages` returns the PDF's page count too.
- The Run transcript PDFs set Greek letters, ≈ and ≠ in the CJK font (Proj10's `export_run_transcript_pdfs.py`): before,
  Latin Modern had none, so "position × θ_i" printed as "position ×  _i" in every PDF and every transcript frame.
- A video Run whose page has no `Video →` line takes its link from its own receipt (`run_url`: result/runtime.yaml,
  then run.yaml), so its screenshots can be found: b11 s46 r02 drew none before.

## [0.4.2] · 2026-10-12 · Numbered passages, no arrows

- Asked 261012 on b11 s47's transcript frames: "this looks ugly, what are better ways? I think for the index, why not
  with 1, 2, 3, 4, with the circles". Each highlighted passage now carries its number in a circle of the highlight's
  own yellow, in the page's margin, and its note carries the same circle; the long slanted arrows from passage to note
  and the "E1" labels are gone. The explanation frame's argument boxes name their passages the same way ("claim · ②").
  JL, on seeing it: "this is exactly what I want".

## [0.4.1] · 2026-10-12 · layout: plain, and a Run's table

- Asked 261012 on Proj10 work/b01: "no need to have the --> all the time"; "I want the tables like this".
- A face's `task: layout: plain`: boxes with room between, no arrows or arrow words, no steps; no arrow or words
  between frames either (acts stay named). Stairs stay the default; video Tasks are unchanged.
- A Run's `table: {columns, rows: [{label, cells: [{at, fmt, unit} | words], dim}], caption}` replaces its 📊 scoreboard
  with draw.py's grid_table, in the open (a card with no colour has no box), "⚙️ What it ran" below it.
- `fit()` counts a table's rules when it trims a room frame.

## [0.4.0] · 2026-10-12 · A video's transcript, read like a paper

- Asked 261012 on Proj10's b11 s47: "the pdf of the transcript should be looks like what we did in the
  /excalidraw-read, to put them in the most left, and highlight them, and in the right, we give the comments". A video
  with a reading (the topic's `reads/<rid>-*/reading.yaml`, written with /excalidraw-read on the Run's
  `result/transcript-article.pdf`) gets a frame of its own before its explanation, `rNN · The transcript, read`: the
  PDF's pages whole on the left, each excerpt's quote highlighted yellow where it stands (read_paper's `find`), its id
  in the margin, and to the right one note per excerpt, level with it, with an arrow (Says · Comment · → this Task).
  The pages are rendered into `assets/<rid>-transcript-p<N>.jpg`, again when the PDF or the reading is newer.
- Each video is its own act, one row: its transcript frame, then its explanation frame ("read, then explained"); the
  arrow down to the next row says what the next video adds. The explanation frame keeps the transcript's argument
  as boxes and drops the cropped passage cards, which the transcript frame now shows on the page.
- Video frames use the stairs (boxes hang off the row above, never a line back across) and are wider and shorter
  (asked 261012: "for each frame it can be even wider and less high"): `VIDEO_W` 6400, six screenshots, six steps,
  four argument boxes to a row; the screenshot box asks for room for its shots at full size.
- Tried and removed the same day: each video as one row read to the right (about 54,000 px wide), which no one could
  read at any zoom.
- Run transcript PDFs (`result/transcript-article.pdf`, `transcript-original.pdf`) come from Proj10's
  `b00_source_intake/j01_video_channels/src/export_run_transcript_pdfs.py`; a Run with no reading still shows its
  article's pages as one row of pictures.

## [0.3.1] · 2026-10-12 · What a newcomer still missed

- Asked 261012 on Proj10's b11 s31: "I feel the core part of the content is not there". A reader review found the core
  formula with no end-to-end example, Q = XW never written, words used but never defined, and two screenshots whose
  captions did not match the picture. The face's words now carry those (the agents' brief has the lessons); the code:
- The idea frame's 💡 What it is adds the page's 🧠 Mental model, ✅ Learning outcome and 🧭 Core path under the intro;
  the video list ends with what ★ and 🎬 mean; screenshot captions are 28 px; a one-video act is "Video 7", not
  "Videos 7 to 7".
- `video_frames.pick` never keeps a cross-fade (a sample halfway between its neighbours, two slide titles overlapping):
  it keeps the sample before, the slide whole. In 3 b11 videos it replaced 3 blended frames; `--reframe` re-picks a cache.
- `field` stops a paragraph at a heading too (b11 s36's Mental model ran into its "#### Connectivity diagram"); a
  frame's screenshots wrap four to a row, so it can show 2 to 8 (b11 s34's reviewer asked for two more).
- The page's own text sketch right after its **Mental model** (`sketch_of`) is drawn in monospace under 🧠 Picture it
  (`code_item`); b11 s36's reviewer found "Picture it" pointing at a four-token sketch that was never drawn.
- From Proj10-LLM-Baseline's session:
  1. `idea.questions` accept `{q, a}`, drawn as the question with its answer under it;
  2. when the face's `open` list is empty, the page's `### N · Limits` division is drawn red on the idea frame;
  3. `FONT_GAPS` swaps glyphs Nunito lacks (ᵀ → ^T and similar);
  4. the Run box names its result folder;
  5. `parse` returns `task["work"]` when a page has no video divisions, so a work Task with no Run says Runs;
  6. a setext title ("Title" over "===") is read before a later `# ` heading, and a work page titled by its folder
     name is drawn in the folder's own words;
  7. `preview <task> <out> --words <yaml>` draws a Task from a words file, for an agent's reader self-check;
  8. teaching frames carry the detail mark;
  9. a failed Run's error is one line (`failure_line`, 160 characters), and work Run frames are sized to their words.

## [0.3.0] · 2026-10-12 · Work Tasks: one frame per Run

- Asked 261012, for every Block of a Project: "make the very detailed sNN-task and sNN-job". A work Task has no videos;
  its sources are Runs with results. `parse` now reads a work Task's Runs from disk (job_results' `runs_of`, shared
  tickets left out), and a Run frame opens with ⚙️ what it ran (the face's `config`) ─▶ 📊 what it measured (`show`,
  else the numbers its result names by a known key) and 📈 its curves (`plot`, drawn by matplotlib from a json list or
  a log), then the same words, formula, steps, 🎤 what it means, ❓ still to check and 🧾 the Run.
- A frame with words only is 2000 px wide with "Words to know" beside the steps (b01 s29 r04 went from 53 to 91 words
  per million px); downloads compare their bytes with Content-Length and write `video.part` first, since Bilibili may
  end a stream early with no error (14 videos had been cut).

## [0.2.0] · 2026-10-12 · Frames that teach from zero

- Asked 261012: "the frame can be even larger, and with more details as possible, suppose we know nothing about these
  type of knowledge … could we get the screenshot of the video … I want the formula etc things and understand them".
- `scripts/video_frames.py`: a video's screenshots (download once into `_WorkSpace/video_frames/<id>/`, distinct frames
  by second, a contact sheet); Bilibili through its player API at 480p with waits when it caps the rate.
- A video frame is 2800 px wide and grows down: 📸 what the screen shows (the face's `shots`, copied into `assets/`,
  empty margins cropped), 📖 words to know, 🧮 each formula drawn by mathtext with every symbol and a worked example,
  🪜 the steps with why, then 🎤 say it, ❓ check, and 🧾 the Run from its receipts (asked by excalidraw-job's session).
- The idea frame: the intro, words to know, the core formula explained, how it works, why it matters, the videos,
  the questions. The face's schema and limits are in SKILL.md, for the agents that write them.

## [0.1.0] · 2026-10-12 · A Task as one drawing

- New skill. Asked 261012 on Proj10's `discovery/b51_llm_serve`: "I cannot still read the content of it. … should we
  have each task to be a sNN and each from to describe what is the video told about"; and, in excalidraw-job's
  session, "we even need to have the excalidraw-task as well, to show the details of each tasks".
- `scripts/task_drawing.py`: the idea frame (the question; What it is ─▶ How it works ─▶ Why it matters; the videos in
  reading order ─▶ the questions to be ready for), then one frame per source (what it says; its points in order; how
  to say it; what to check, in red), with the arrow into each frame saying what that source does. `make` (a Task, or
  each Task of a Job), `draw`, `preview`.
- Few words in large type (excalidraw-studio ⑦): the face's `task:` yaml holds the short words (`idea`, `videos`,
  each with word limits); anything it leaves out is read from the page. The first build, all from the page, held
  300 to 550 words a frame; with the face's words, 140 to 200, none under 28 px.
- Reads the page with excalidraw-job's `section`, `concept`, `first_para` and `plain`. Its own `field` and `items`
  read a labelled paragraph to its end and a list after a blank line, which `labelled` does not.
- First drawn: Proj10 `discovery/b51_llm_serve` s01 to s10, one topic per Task.
