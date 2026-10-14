excalidraw-job · Changelog
==========================

## [0.7.1] · 2026-10-14 · the staircase: wide cards, Task thumbnails, compact steps

- Wide cards (JL 261013 on Proj10 b01 s22: "make it wider, each one to be a few lines, and much wider"): a Task's
  box 820 → 1200, its card 660 → 1080, a Run's card 640 → 960, the Job's box 1100 → 1400, its in and out
  760 → 1000. Committed as 0ec97be0 without this note.
- Task thumbnails (JL 261013: "use one excalidraw to embed the other one"): Excalidraw cannot embed a drawing in
  another, so `topic_thumb` renders a Task topic's first frame into the Job topic's assets/ (redrawn when that
  drawing is newer) and its results block shows it, the picture and its caption linked to the Task's
  `.excalidraw`. Landed inside 0.7.0's commit without this note.
- Compact steps (JL 261014: "I don't want the margin between the two tasks be too large … this should be in
  different rows"): a step is as tall as its own boxes; its results block hangs outside on its own row and its
  line bends down to it, so a tall results block no longer pushes the next Task away. j02's ① 2820 → 2042 tall.

## [0.7.0] · 2026-10-13 · layout: explained, JL's sketch: a wide frame, Tasks as steps, results outside

- Asked 261013 on WellDoc Proj11 `work/b01_clm_foundation_model` s21 (j01 pretrain), over one evening: "make ⑦ 📚 j01
  · pretrain: explained from zero to be the main … others to support it"; "make it to be per tasks"; "each task to a
  row, did you really carefully read the content of the /excalidraw-job????"; "why you don't just make the main frame
  to be wider"; "read [the Paper-LLMRecPhy-work] session" (its rules: 主次分明, stairs, 留白, results small, never a
  full board); then a sketch (WellDoc-SPACE `image.png`): a wide, low frame, JOB at its top left, Task 1, 2, 3 each a
  step lower and further right, a long line from each out through the frame's edge to "result 1, 2, 3", level.
  Four tries before it missed that sketch: frames stacked beside ①, two Tasks a row, results as big tables and grids
  of ✅ inside a tall frame. Each one broke a rule this skill already wrote down.
- `draw_explained` (`job_drawing.py`): ① the reading; the Job (why, done when) with In and Out (job_ladder's cards);
  each Task a step 560 px further right, its stair hanging off the last one's, a small card under it (asks, did, its
  Runs or the design's tally, → its topic); the frame ends where its widest step ends (JL: "too much margin"; 3,600 px at least); outside it, level
  with each step, a small results card (`results_card`): one sentence and a table (a settings row's low end → high end;
  the face's `chart` for the Job), dashed when no number is on disk.
  Below, stepping down and right (`canvas.stairs`): ② job_ladder's `notes_frame`, ③ `formula_frame`, the design grids.
- Shared on the way: `lay_grids` (design_frame's grid loop), `grid_note` (a grid's note wraps to its width),
  `mark_grid`/`grid_size` take `small`; a Task box with no Run folder says where its runs are counted.
- Then JL: "how could you list the runs and the running status as well". Each step's Runs branch right below its
  line out, as small cards in a row (`run_cards`, `job_ladder.run_cols`): a card per Run folder (its mark, its
  name, its state); when the Task holds none yet, a card per design grid (a sweep): its Runs by state (evaluated,
  half evaluated, not evaluated, failed), why a mark is red, where its tickets are.
- Then: "for the tasks, I want the runs to be fully displayed here, so I can know for this task what are the runs
  we have". A sweep's card holds its whole grid as a picture (`grid_png`): a square per Run, its row and column
  naming it, green evaluated, orange half, grey a ticket not evaluated, red failed, a dot for no ticket; long
  column names tilt. The design frames below are gone: every Run now stands beside its step.
- Then: "could you make this 10% to be the same size of 40% or 50%?" and "I think we can have the things like table,
  not this figure". Two type sizes: the skeleton (the title 160 px, the reading's first sentence, the Job and each
  Task by its folder's words at `BIG` 120 px, each result's header at `MID` 80 px) reads at 10% zoom as 28 px reads
  at about 45%; the detail stays 24 to 34 px. Results are tables (`results_card`): a Task's settings rows as
  sweep, then each measure's low → high, the numbers large and their settings small under them; the Job's `chart`
  as a row per series, a column per bar. `pair_png` is gone.
- Then: "how to make the j02 and j03 as well … could you make it work the same way?". Drawn on Proj11 b01 s22
  (j02 finetune) and s23 (j03 evaluate). An `at` now reads (`read_data`) a JSON past job_results' 4 MB cap (j03 t01's
  7 MB token counts) and an executed notebook's printed results, each output line `<name>: {…}` a key (j02's scores
  live only in the legacy notebooks: `run_num_1m_next2h.ipynb:test-id.kl`), so no number is copied beside a face. A
  settings row may name its own measures (`heads:`); a Task page's "SCAFFOLD" line is no title (a face's
  `tasks.<t>.title` wins); `fmt_value` keeps a cell short (2.02B, 51.6M, 0.192).
- Test: `test_explained_layout_makes_the_words_from_zero_the_main_frame`. First drawn: Proj11 b01 s21.

## [0.6.2] · 2026-10-13 · Runs as a grid: a Job grows wide, not tall

- JL on Proj10 b01 s21 (j01, two Tasks of six and four Runs): "the width is kind of small, you can make it wider
  … I don't want to make it very tall and narrow". A Task's Runs now stand in a grid beside its step, `run_cols`
  a row (one alone, two up to four, three past that), each row as tall as its tallest card; the branch meets each
  row's first card, and the frame widens to the widest grid. j01's ① went from 2140 x 3863 to 3476 x 2572.

## [0.6.1] · 2026-10-13 · Stata tables: bars with their own intervals, a table's row filter

- Asked 261013 on Physician-SPACE's OpioidRx Blocks ("for each jobs, make the plan first", then redraw them as
  staircases): its Stata Runs write one CSV per kind (`tables/h2-slopes.csv`) holding several models, so a chart
  picks rows by `col=v&col2=v` and each bar may now carry its own `low:` and `high:` (`chart_rows`), and a table
  shows only the rows its `where: "col=v&col2=v"` picks (`task_tables`).
- From the five Block agents' reports the same day: ② drew only 12 `terms` and dropped the rest silently; it now
  draws 16 (`TERMS`) and counts the rest ("… 3 more terms in the face"). A chart of counts in the millions labels
  its bars and ticks `113.2M`, not 113,219,741 run off the edge.
- JL the same evening: "for the figures etc. you should make them run in the run's results". A Task's figures
  (`figures:`, a figure Run's PNGs) now come right after its finding, before its tables; SKILL.md says to prefer
  a figure Run over `charts:`. "Done when" shows 34 words, not 22 (four reviews found its end cut).
- Tests: `test_a_stata_csv_gives_bars_with_whiskers_and_a_filtered_table`,
  `test_terms_past_the_cap_are_counted_and_millions_stay_short`.
- First drawn: OpioidRx `work/b03_CD_visit_pain/studio/s22` (t06's pooled slopes, r02 and r01, with 95% intervals).

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
- From a fresh-agent trial on LLMRec b03 s21 (the same day): a 📌 current Run never folds into the "more Runs" row;
  a chart's axis has a few ticks with thousands separators (they ran together); a settings or model cell prints
  71,427, not 7.143e+04. New test.
- Each step is spaced to its measured results block, so it stays level with its results and the line runs straight
  across; the extra height is room (excalidraw-task 0.5.0 does the same).

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
