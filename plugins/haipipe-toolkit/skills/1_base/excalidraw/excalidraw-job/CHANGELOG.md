excalidraw-job · Changelog
==========================

## [0.9.4] · 2026-10-19 · a big Task folds by what its Runs do; three staircases or more; legacy bands

- Asked 261019 on Physician-SPACE LLMRec b01 ("I don't think these sNN jNN well structured", then "I think we have the
  /excalidraw-job"). j02 t02's 57 Runs had shown its newest 20 (folds 06-09) and folded folds 00-05 into one list with
  no state marks, so `job_check.py` failed and the order read as random.
- `fold_groups`: past MOST, a series of 3 or more Runs that differ only in a two-digit counter is one card
  (`🔁 fold01-09 brave v1 · 9 Runs`), a family of 5 or more sharing a first word without digits another
  (`page-evidence-item`), each card at most `FOLD_LINES` (12) Runs; every other Run keeps its own card. Each folded Run
  is one line, named in full, with its mark. b01 j02 t02: 12 Run cards and 5 series cards, every fold visible.
- `split_steps`: `parts:` takes three or more, each later part cut at its own `from:` Task (b01 j02: websites, search
  engines, our own ranks; b01 j03: the builder, the released site, the RateMDs photo lane), so each staircase stays
  under check.py's 600 words while every Run is named.
- `propose_tree.py`: a Task whose older Runs already fill a band (r01-r57) numbers a new Run after its last one (r58),
  its type kept in `run_type`; before, it stopped with "band of main is full".
- A folded card is as wide as its longest line (at most RUN_W), so a list card leaves no empty box beside it.
- A proposed Run's card says `◌ proposed <date> · waits for a yes` in ink, and `🧩 needs first:` from its
  run.yaml, so it reads apart from a Run that only has not run yet (b01 s21 reader review, 261019).
- Tests: `test_a_big_task_folds_by_series_each_run_marked`, three parts in `test_the_face_names_steps_and_two_staircases`,
  `test_a_task_numbered_before_the_bands_takes_the_next_number`. 29 pass.


## [0.9.3] · 2026-10-19 · a family in its place: each Task drawn once

- Asked 261019 on PD2D b00's j51, whose four families were drawn twice (a summary step in ① with its chart, then
  their own staircases ③-⑥): "你为什么不把之前最大那个地方给删掉，然后把这个东西移到上面去？这样的话就不会重复了" (delete the
  big part before and move these up, so nothing repeats). A step with `frame: in place` is no step in ①: the Job's
  frames follow its order (the steps before it, the family's own staircase, the steps after it; `story_segments`),
  each Task once. Its `notes:` sit under its frame's key point, two columns, smaller. j51: 7 frames, 12,916 px tall.
- `frame: true` keeps the 0.7.3 shape (a summary step in ①, its staircase after).

## [0.9.2] · 2026-10-19 · notes beside a results block

- Asked 261019 on PD2D b00's j51, over the prediabetes-entry table and the diabetes-signal chart: "在这两个图的右边再加一些
  注释吧，说明一下这里面都是什么意思" (add notes to the right of these two figures saying what they mean). The face's
  `notes: {<task or family step key>: [line | {term, means}]}` draws a column under "📖 how to read it" to the right of
  that step's charts and tables, inside its results box, smaller and marked `canvas.aside`.

## [0.9.2] · 2026-10-19 · a Run's plan on its card, one wide card a row

- Asked 261019 on Knowledge-Base Proj10 b11 s23: "这里能说一说每一个 run 的 aim 是什么？为什么要这样做？… 数据集有多大
  … 你想在哪里 run？", and "像这种 run 比较复杂、比较具体的，我们就一个 run 占一行。可以把它变得宽一些".
- `job_ladder.run_plan`: a Run's `run.yaml` may hold `aim`, `why`, `settings` (a mapping), `host`, `time`, `after`;
  its card draws them (🎯 aim, ❔ why, ⚙ settings, ▶ host · ⏱ time · after), and such a Run is never quieted.
- A Task whose Runs carry a plan draws one card a row, 1,700 px wide (`RUN_WIDE`); a face's `job.run_cols: 1` asks
  for it too. `propose_tree.py` passes a plan's `aim`, `why`, `settings`, `host`, `time` into each `run.yaml`.

## [0.9.1] · 2026-10-19 · job_check reads CSV and Markdown results; a family's Run folds carry their state

- `job_check.py` looked for a percentage only in .json and .yaml results. It now reads .csv tables (a cohort funnel)
  and the numbers in a result's .md files (a Discovery paper's facts.md and abstract.md). Over REACH-SPACE's 76 Job
  topics this took the passes from 59 to 66; the 10 left quote a number from another Job (`cites:` it) or compute
  a ratio no file states.
- A family step's folded Run boxes (`r02 · profile semantics × 10`) now lead with their state mark, as 0.9.0 asks of
  every Run card.

## [0.9.0] · 2026-10-19 · propose the tree, show each Run's state and files, check against disk

- Asked 261019: "一定要把这些 run 也 propose 好，然后每一个 run 都要排序排好"; "for the run, could you also show what
  are the related files"; "how do you evaluate the sNN jNN with /excalidraw-job, do we have the evaluation?".
- `ref/propose-tree.md`: Job = setup, Task = algorithm, Run = setting; Run types by band (r0x smoke, r1x main, r2x
  sweep, r3x repeat, r4x score, r5x ablation) so a Task's Runs sort into the order they run; five states.
- `scripts/propose_tree.py`: proposed Tasks (face `state: ◌ proposed`) and Runs (`run.yaml` `status: proposed`,
  `run_type`, `says`, `after`, a stub ticket that exits 3 with what it needs); dry run unless `--apply`.
- `job_ladder.py`: each Run card shows its state mark (✅ ❌ 🔶 ⬜ ◌), is dashed until it ran, says why it failed (its
  receipt's `failure:`) or what it is proposed for, and names its files (ticket, config, result/). A proposed Task's
  step is dashed, and its results block says it is a plan in grey, not a red gap.
- `scripts/job_check.py`: the drawing against its disk (every Task and Run named, every card marked, every failure
  explained, every percentage in the face's words found in a result file or a `cites:` Job).
- First used on Knowledge-Base Proj10 b11 j12 (eight verl algorithms) and j01 (baseline sweeps, pass@k).

## [0.8.2] · 2026-10-19 · the Runs' table and chart beside their results

- The face's `chart` and `settings` frames (what the Runs found; each Run and what is left) now stand to the right
  of the staircase's results block, top-aligned with ①, each with a named arrow; no longer stacked below it
  (JL 261019: "It should be in the right of the runs' results").

## [0.8.1] · 2026-10-19 · the header counts the to-finish table

- The staircase header adds the face's to-finish count when `job.settings.rows` exists: ✅ done, ❌ failed, ⬜ left, and whether the Job is closed (JL 261019, "how could we quickly know the status?").

## [0.8.0] · 2026-10-19 · every Task and Run explicit

- Asked 261019 on Proj12 b13 s21, three planned Runs drawn as one grey "3 Runs: r01 · r02 · r03 / no result yet":
  "you should show me the tasks and runs to be very explicit … this is what we required in the /excalidraw-job".
- `shown_runs`: every Run is its own card, whether or not it reports; only past `MOST` (now 24, was 8) does a Task
  fold, keeping the 📌 current, then the latest that report, then the latest planned; the folded card lists every
  folded Run by its full name (`run_label`), not `r01 · r02 … r09`.
- A Run with no result says its state (`⬜ no result yet`, `⬜ queued`), not "nothing in result/ yet".
- A quiet rerun (beside a 📌 current Run) keeps its state line; the current card is always named in full.

## [0.7.5] · 2026-10-14 · results too tall for one run stand in columns

- Asked 261014 on Proj10 b12 s21 (five transcript blocks, about 10,000 px in one run beside a 3,614 px frame; the
  rule "以 job frame 的上下为界限 … 超出部分一定要对称、均匀"): past `SPILL` (2) times ①'s height, the blocks stand
  in side-by-side columns, in step order, the fewest whose tallest fits (`results_columns`), each column centred on
  ① so what rises above it equals what hangs below (`results_in_columns`). Below that, 0.7.4's one run is unchanged.
- Links never cross: the first column's bend in `results_lanes`; a later column's link drops beside ①, runs under
  the columns before it and climbs the gap left of its own column.
- A block with transcript rows and no chart, figure or table puts its title and finding across the top and the Run
  rows under them, instead of an empty column beside them.
- Proj10 b12 s21: two columns, 1,170 px above and below ① (was one run of about 10,000 px).
- Tests: columns that fit, overflow equal above and below, no overlap, no crossing link.
- A Run card names its Run in full when the name fits the card's share of ①'s words (asked 261014: "why here the
  run's name is not full?"); its sentence takes what is left, none when under 4 words. A Job past about 12 Runs
  still cuts the name, so ① stays under 600 words.
- A Task shows up to 8 Runs before the rest fold into one row (was 6), and a screenshot's caption up to 20 words at
  20 px (was 12 words at 18 px), so the Runs of a Job of about 12 and their captions read whole.
- A card whose full name takes all its room shows the name alone, not a file count in place of its sentence
  (found on Proj10 b61, 261015).

## [0.7.4] · 2026-10-14 · results fill the room beside the frame, evenly

- Asked 261014 on LLMRec b04 s27 (a screenshot of its results, one narrow column hanging 4,800 px below a 3,218 px
  frame): "这个 result 右边有这么多的空位你都不用，非要挤着那么一块。而且我这个跟左边的 frame 也不好对齐"; then the rule:
  "以 job frame 的上下为界限 … 最上面和最下面的 frame 可以超过 job frame 的最上和最下，但超出部分一定要对称、均匀";
  and "你想想这个 results … 你到底想好去怎么 display 是非常重要的".
- A results block lays its panels (charts, figures, tables, the picked numbers) side by side, up to three a row,
  each under the shortest column so far (`results_block(cols=)`); never a column with nothing in it. A long table
  takes the columns nothing else fills, in parts of at least 4 rows, each part's header level with the first's.
- `place_results`: each block is measured at 1, 2 and 3 panels a row; the narrowest width at which the blocks
  together fit ①'s height is used, else the widest. Shorter than ①, each block sits as near its step as it can,
  inside ①'s top and bottom; taller, they are one run centred on ①, as far above it as below (`results_layout`).
  Every other block steps 240 px right (was 520, and only for transcript columns).
- A step's line runs straight to its block where they are level; else it bends in its own lane between ① and the
  blocks: lines that turn up take lanes left to right, lines that both turn down right to left, so none cross
  (`results_lanes`).
- haipipe-studio `canvas.stairs` and `canvas.grid` now count results that rise above a frame, so a second
  staircase's results never reach into the frame above it.
- Each chart is drawn once a build (`chart_png` keeps it), though a block is measured three times.
- A fresh-agent test of this version (261014, j08 drawn into a scratch folder): the layout held (137 px above ①,
  137 below, no overlaps, no crossings), and it found three gaps, now closed. Each block is titled with its step's
  own name, larger (`📊 t02 · <name>: results`); a bent line meets its block at that title, not its blank bottom;
  `preview --face <face.md>` draws a Job with a face's `job:` yaml (before, preview ignored every face).
- LLMRec's 25 Job topics redrawn: b04 s27's results 3,530 px tall beside a 3,218 px frame (155 px above and
  below), was 6,924 tall with 4,789 below it; Discovery b01 s22, 5,033 beside 3,209 (912 above and
  below), 9,750 before its paper tables stood in parts.
- Tests: results inside the frame or past it evenly, never overlapping; lanes that never cross; panels side by side.

## [0.7.3] · 2026-10-14 · a family step drawn again as its own staircase

- Asked 261014 on PD2D b00's j51, over its four family steps: "we can make them into different job frames as well
  … just like this" (the second staircase). A face step with `frame: true` keeps its compact step in the main
  staircase, now pointing "→ each Task: frame ③", and is drawn again after it as its own staircase: each member
  Task a step with its page, its Runs and its results. The question the members share is said once, in the frame's
  key point (`reading:`), not on every step. `run:` with `show_each: [{label, at}]` gives every member the same
  picks from its own Run (`expand_each`), so each table shows its rows, columns and patients.
- j51: 7 frames (two staircases, four family staircases, its words); frame ① stays under 600 words.

## [0.7.3] · 2026-10-14 · a table per Run, and Later drawn plain for an agreed topic

- Asked 261014 on Physician-SPACE LLMRec's 25 Job topics: "make the report of the task to be shown as the table,
  then make it to the level 3 of the agreed".
- A row per Run (`tables: <t>: [{runs: true, columns: [{label, at}]}]`, `run_rows`): a Task whose every Run is
  one subject (a Discovery paper) is a table, its cells read from each Run's own result (`<file>:<key>`) or the
  face's `says`; `rows` caps it (12), the rest counted. Its Run column is narrow.
- `later:` (`notes_frame`): stage agreed means no red ❓ and no open point (haipipe-studio topic contract), so an
  agreed topic's open points move to `later:`, drawn plain in ② as "⏳ Later, and what would start it".
- Then a fresh reader review of 6 LLMRec topics: "no Task page is named" in any of them. Each step now ends
  `📄 page: <tNN_task>/<tNN_task>.md`, linked to the page. A Run table takes `only:` (globs on the Run names) and
  skips a Run with nothing in its columns; the picked numbers' table is headed `measure (<its Run>)` · `value`.
- A table may read a file anywhere in the Block (`path:`), for a Task whose own Runs keep no result. A picked
  number keeps its unit: the row splits at the face's own label ("Claude transport response | 1,326 chars").
- Tests: a row per Run, capped and counted; Later plain, never red; the page line and its link; `only:`;
  `path:`; a unit beside its number.

## [0.7.2] · 2026-10-14 · a big Job keeps its stairs: a family of Tasks as one step, two staircases

- Asked 261014 on a 33-Task raw-data Job (one Task per table), drawn 14,780 px tall: "if possibel, let's still be
  the steps / stairs", then "if the job is too large, in the sNN jNN, you can have two frames to arange that".
- A family step (`step_groups`): the face's `steps: [{title, tasks: t17-t26}]`, else, past 8 Tasks, each run of 3 or
  more Tasks of one kind (the folder's first word: `profile`, `procdf`). It lists its Tasks two a row with their
  marks, folds their Runs by what they do (`r02 · profile semantics × 10`), and its results read one value per
  member Task from that Task's own Run: `charts:` and `tables:` entries with `members: true` (`family_step`,
  `member_rows`). The 33-Task Job: 6 steps, 2,346 px.
- Two staircases (`split_steps`): past 6 steps, at the middle step, or where the face's `parts:` says; the second
  is named by what it holds (never "· 1", "· 2"), has its own key point and results, and is joined by "continues".
  haipipe-studio's `canvas.stairs` now moves the results that follow a frame, as `canvas.grid` did.
- A page title's address (`B00/J51/T14 · …`) is dropped from the step, which already says its id (`bare`).
- Tests: a family is one step; named steps, a named split and the split past six.

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
- 261014: a Task with Run folders still shows its design grids beside them (`run_cards`): Xuzhe's j02 Runs r01, r02
  had hidden the 24 legacy runs t01's grid counts. Found by rebuilding s22 from a copy of GitHub's main.
- 261014: each result card ends with where its numbers were read (`file_lines`, `path_lines`; JL: "how do you
  get this? … could you show the files here as well? … give it a path"): a group per key, a path under the
  Project's work/ folder, files alike folded to one pattern (`eval_clm_*_*_nb/forecast.json`, 24 files), else
  the folder holding them, broken only after a "/". The j01 table so shows it is read from j03's files.
- 261014: one file read for many keys is one line, its keys listed (`file_lines`): Physician-SPACE OpioidRx
  b03 s21's table read 20 values of one CSV and printed its path 20 times.
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
