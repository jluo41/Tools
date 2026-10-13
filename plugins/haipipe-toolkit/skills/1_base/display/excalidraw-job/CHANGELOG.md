excalidraw-job · Changelog
==========================

## [0.6.0] · 2026-10-13 · The staircase: Tasks as steps, results as charts and tables, frames as stairs

- Asked 261013 on Physician-SPACE's LLMRec Blocks, with a hand sketch: "先是 Job，下面跟着 Task 1、Task 2、Task 3 …
  相当于一个阶梯状的图 … 右边就开始说明每一个具体的结果都是什么", "current ones in the job sNN are very bad", "这个 frame
  可以很大，但核心是留出足够的空白", "你的 results 应该是图和表格呀", "for the task, we might want to add the figures and
  table from it", "主次分明 … 大小有致", "棋盘上不能落满所有的子", "你不能每一个都是朝左对齐".
- `scripts/job_ladder.py`, the default drawing (`draw_job` sends every Job here unless `layout: classic | plain`):
  ① the staircase: the Job on top (why, done when, answers; in and out beside it), each Task a step 380 px lower and
  right (`columns`: four columns at most, several Tasks may share one), its card (asks, did, → details: sNN), its Runs
  branching right. A face's `runs: {<t>/<r>: {says, current: true}}` marks 📌 the Run to read; the others go grey,
  names only. Runs with nothing to report fold into one row; a rerun that says the same says `↺ as r01`.
- Results, outside ①, level with each step, small: one sentence of the finding, then `charts:` (bars drawn with
  matplotlib from the current Run's result: `each` with `value`/`low`/`high`, or `bars`; 95% whiskers, a zero line,
  model names shortened), `tables:` (rows from a CSV under the Run's result), else the `show` picks as a table, then
  the figures the Task already holds (`figures:`, else its Runs' results, then its draft). Dashed while nothing is
  found. Charts are generated into the topic's `assets/` on every build.
- ② 📖 its words (`terms`, `sure`, `open` with each `closer`), small (`canvas.explains`); ③ the face's design grids,
  models, chart, settings, `detail: true` and the Job's own pictures (a Task's stay in its results). ② and ③ step
  down and right of ① (`canvas.stairs`); no act names down a left edge.
- Shared, for this: haipipe-studio `canvas.stairs` and `canvas.explains`, and `job_results.dig` reads a name with a
  dot whole (`codex-gpt-5.6-luna`, in JSON and in a CSV row's `col=value`); excalidraw-studio `check.py` holds an
  explaining frame to neither a screen's size nor a dense frame's words.
- Tests: `tests/test_job_ladder.py` (steps right, quiet reruns, charts and a table from results, a Task's figures and
  tables, frames as stairs); `test_job_drawing.py` reads the staircase.
- First drawn: LLMRec `work/b04_analyses_of_llm_ranks/studio/s27` (j08: six charts from three Runs' metrics.json).

## [0.5.0] · 2026-10-13 · A family of Jobs, a table per Job

- Asked 261013 on Proj01 b00_rawdata: "describe for each task, what we have done, what are the content, I might want
  more figures and tables, to understand what I have".
- `group`, when a Job's words hold a `table`: one act per Job (`table_acts`): ① its steps (`flow`, each line's slots
  read under the Job), its reading, one row per Task with each cell read from that Task's own file (`table_rows`,
  `cell`), the `bar` columns drawn as bars lined up with the rows (`bars_png_rows`); ② its `chart` (chart_frame);
  ③ its pictures and its named Tasks' own pictures (`figures_frame`, key point `shows`). Several Jobs first get a box
  each (`gist`) and the Jobs as a table (`jobs_frame`). `each:` holds the words every Job shares.
- `fill`: `{<file>:<key>|<fmt>|<when empty>}` and `{count:<glob>}` in any line, read on every build.
- A cell's `most: N` keeps a list's first N and says how many more (a table's measured columns: `only: {role:
  [value]}`), after the first reviews asked what each table's columns hold.
- excalidraw-studio's `draw.py`: `grid_table(pad=)` and `rows_at` (each row's top and height), `picture(fid=)` (two
  pictures with one file name no longer share one image).
- First drawn: Proj01 b00_rawdata s21 (seven WellDoc drops), s22 (AI-READI v3), s23 (six external cohorts).

## [0.4.0] · 2026-10-13 · The design: each Task's Runs, one mark per Run

- Asked 261013 on Proj11 b01 s21: "How could I see in a glance about the design for each task and their runs? … and
  for these runs, what are their status?"
- `design_frame`: `job: design: {runs_word, frames: [{title, sub, key, caption, grids: [{task, title, rows, cols,
  row_name, col_name, ticket, evals, failed}]}]}`. Each grid is one sweep: a row per row value, a column per setting,
  one mark per Run read from disk on every build: ✅ every eval found, 🔶 some, ⬜ a ticket and no eval, ❌ a listed
  failure (red), · not in the design. Patterns take `{row}`, `{col}` and a column's own fields; `<path>:<key>` asks
  for a value inside a file. Grids flow left to right and wrap; the key point is each Task's tally.
- The design frames are their own act (Act 2, what each Task ran), before what the Runs found (Act 3); frame marks
  follow reading order. ② shows a Task's tally from the design when the Task holds no Run of its own, and its 📍 line
  the whole design's tally.
- ③ "explained from zero" takes the next free mark, so no two frames share one.
- First drawn: Proj11-CGM-FM work/b01 s21 (j01 pretrain: 477 Runs in 10 grids).

## [0.3.0] · 2026-10-12 · Results as b03 reports them: charts and grid tables

- Asked 261012 on Proj10 work/b01: a ③ of text boxes "should be forbiden, so rigid, not vivid"; "should we have a table
  for that?"; "setup the list of models and we can select and explore"; "I want the tables like this".
- ③ "explained from zero" only when the face sets `job: detail: true`.
- `chart_frame`: `job: chart: {title, sub, key, caption, legend, bars: [{label, at, contrast}]}`, before → after bars
  read from disk.
- `settings_frame`: `job: settings: {title, sub, key, caption, columns, rows: [{state, cells}]}`, drawn as draw.py's
  grid_table (b03's grid); a planned row grey.
- `matrix_frame`: `job: models: {file, measures: [{label, task, at, fmt}]}`, one row per model in the list file
  (☑ selected first, ☐ a candidate grey), one column per measure, each cell read from the Run whose run.yaml (or
  result JSON) names that model; ⬜ to run for a selected model not yet measured. `run_model()` finds a Run's model.
- `job: layout: plain`: the models grid, then the chart, then the settings; acts named, no arrows between frames.

## [0.2.0] · 2026-10-12 · ③ The Job explained from zero

- Asked 261012, on work/b01 s21: "for things like this, this is very thin, I think for the /haipipe-studio, after you
  create such a draw, you should ask it yourself, If I am a reader, will this answer my questions for this job".
- A third frame, ③ "explained from zero", drawn when the face's `job:` yaml has intro, terms, inputs, outputs, formula,
  tasks {asked, did, found}, sure or open {item, closer}; built with excalidraw-task's boxes, answer first, marked a
  detail frame. ② shows the face's inputs and outputs instead of "n Runs" and "n pages", and "no result yet" is drawn
  only when no Run finished.
- First drawn: Proj10 work/b01 s21 (GSM8K data preparation), then reviewed by haipipe-studio-reviewer-agent.

## [0.1.0] · 2026-10-12 · A Job as one drawing

- New skill, asked 261012: "show the sNN as the excalidraw as the job, to make the job's aim, plan and results", then,
  on b01_ml_foundations' s21 to s23, "我想在这个桌上把这个 job 的所有内容都展示出来" (what goes in and comes out, what it
  concluded, its tables and figures).
- `scripts/job_drawing.py`: four frames in two acts (① why, ② in → Tasks → out, ③ what it concluded, ④ tables,
  formulas and pictures), read from the Job face, the Block's board, each Task page and each Run on every build;
  `make`, `draw`, `adopt` (a one-Job results topic from haipipe-studio's `job_results.py`), `preview`.
- First drawn: Proj10-LLM-Baseline `discovery/b01_ml_foundations` s21, s22, s23, adopted; every frame passes
  excalidraw-studio's `check.py`.
- `tests/test_job_drawing.py`: a small Block with one Job, two Tasks and a Run, made, drawn and checked.
- One topic per Job, both ways: `make` refuses a Job that already has a topic (results or whole Job), and
  haipipe-studio's `job_results.py covered()` reads a face's `job: name` (fixed by the Proj10 session, which found
  that an adopted Block would otherwise get duplicate results topics). A test holds both.
- Same day, few words (asked 261012: "add at least of words … when drawing the workflow"; "make the draft to be less
  of wordy and concise"; excalidraw-studio 0.3.0's ⑦): two frames instead of four. ① keeps each Task's question only;
  ② is the workflow with each Task's state and one-sentence finding, the reading as its key point, and `→ details:
  sNN` to a Task's own topic (a face's `task:` yaml, excalidraw-task's). The old ③ (conclusions) and ④ (tables and
  formulas) moved to the Task topics; a pictures frame appears only when the Job has pictures. Both frames pass ⑦.
