---
name: excalidraw-job
description: >-
  A Job drawn as one Studio topic, a staircase: the Job on top (why it exists, when it is done), each Task a step lower
  and further right, every Run named on its own card with its state (the current one marked, none hidden), and each Task's results
  as charts, tables and the figures it already holds, in a block outside the frame, its panels side by side, the
  blocks inside the frame's top and bottom or past both by the same amount. Smaller
  frames that explain it (its words, how sure, what is open) step down and to the right; nothing is left-aligned or
  filled. Read from disk on every build. Use to draw a Job, to turn a Job's results topic (job_results.py) into the
  whole Job, or to see at a glance why a Job exists and what it found. Trigger: draw the job, job drawing, the whole
  job, job staircase, tasks and runs, job results as charts, what did the job find, /excalidraw-job.
allowed-tools: Bash, Read, Edit, Write, Grep, Glob
metadata:
  version: "0.9.5"
  last_updated: "2026-10-19"
  # version history: ./CHANGELOG.md
---

# /excalidraw-job · a Job as one drawing, a staircase

> **Every Task and every Run is explicit (JL 261019).** Each Task is its own step, and each Run is its own card with
> its folder name (`r02_q4km_throughput_fullctx_calib`) and its state (`complete`, `queued`, `no result yet`),
> whether or not it ran. Never draw "3 Runs: r01 · r02 · r03" as one grey card. Asked on Proj12 b13 s21: "you should
> show me the tasks and runs to be very explicit … this is what we required in the /excalidraw-job". Only a Task of
> more than 24 Runs folds, by what its Runs do (a series across folds, a family of one first word), and each folded
> card lists every Run by its full name, one a line, with its state.

> **Results are real code, in colour; In and Out name their paths (JL 261019).** "We will use the real python code
> generate result to report the results here … do not use this black and white anymore", and of 📥 In and 📤 Out:
> "the data here is not complete … could you also show the path for these data?". A results panel is a PNG that a
> Run's own Python code drew from that Run's real result files (a figure Run, `figures:`); the drawing shows it and
> never draws or retypes a number itself. Every bar takes a colour by what it is about (the dataviz palette in
> `job_drawing.py` `PALETTE`): one source, one hue in every chart, a chart of one source all in that hue; a total, a
> reference or an absence grey; blue only when a bar names no source; never all-dark bars. A Project's figure drawer
> (LLMRec's `work/_tools/figures/draw_figures.py`) keeps the same `PALETTE` and names its sources once, so a figure
> Run and a `charts:` panel agree. Each In and Out item is `{item, path}`, every input listed, its words whole (26
> words), its path drawn under it exactly as on disk, red when this machine has no such file.

> **Folder names, never new names; each Run says what it read and wrote (JL 261019).** "Why the name here used is not
> the same as the task folder name or the run folder name? we don't need to create the new named to add the cognitive
> burden to us", and of the Run cards: "we might want to show briefly about its input and output". The Job, each Task
> and each Run are drawn by their folder names, exactly (`🧱 j01_physician_pool_by_region_specialty`,
> `🧩 t01_ranks_from_review_platforms`, `r06_fold2to9_hgvitals`); only a family step the face names (`t17-t26`) keeps
> its face title, and a paper's or video's own filed title stands beside its Run as `📄 …`. Every Run card carries
> `📥 in:` and `📤 out:` (a Run on its own card; a folded card lists names only), one line each (`run_io`; `+3` means
> three more files not shown), read from the face's `runs: {in, out}`, else `run.yaml` `reads:` and
> `writes:`, else its config (`_meta.input`, `grid_path`, `sources:`, `output_root` …), else its receipt, the output
> falling back to what `result/` holds; a path keeps its last whole names (`…/1-CandidatePool/v2026-08/grid_folds.parquet`)
> and an empty side says `not recorded`. `job_check.py` fails a drawing that names any Task or Run otherwise.

Asked 261012: "show the sNN as the excalidraw as the job, to make the job's aim, plan and results". Asked 261013 on
Physician-SPACE's LLMRec Blocks, with a hand sketch (the Job, then T1, T2, T3 each a step lower and further right, a
"T1 Results" box beside each, outside the frame), and over one afternoon:

1. **A staircase**: "先是 Job，下面跟着 Task 1、Task 2、Task 3，再往下就是各种各样的 Run，相当于一个阶梯状的图".
2. **Results on the right**: "右边就开始说明每一个具体的结果都是什么 … 既清楚这东西为什么存在，也能直接看懂它告诉了我什么".
3. **Room**: "这个 frame 可以很大，但核心是留出足够的空白，不要太挤、太 compact"; Tasks may share a column.
4. **Charts, not words**: "你的 results 应该是图和表格呀 … 如果你有 Python 画的图，也一起扔过来"; and "for the task,
   we might want to add the figures and table from it".
5. **主次分明**: one large main frame, small frames that explain it ("大小有致"); "棋盘上不能落满所有的子"; "你不能每
   一个都是朝左对齐".
6. **Results use the room** (261014): "这个 result 右边有这么多的空位你都不用，非要挤着那么一块"; "以 job frame 的上
   下为界限 … 最上面和最下面的 frame 可以超过 job frame 的最上和最下，但超出部分一定要对称、均匀".

```text
① 🪜 the staircase (main, large)                    outside: within ①'s top and bottom, or past both equally;
                                                     past twice ①'s height: side-by-side columns
   🎯 the reading (the key point)
   🧱 b03 j03 · why · done when · answers ──▶ 📥 in · 📤 out
    └─▶ 🧩 t01 · asks · did ─ r01 · r02 (grey) · r04 📌 current ───────────▶ 📊 t01: one sentence · charts
          └─▶ 🧩 t02 · asks · did ─ its Runs ──────────────────────────────▶ 📊 t02: tables · its figures
                └─▶ 🧩 t03 … ──────────────────────────────────────────────▶ 📊 t03 (dashed while nothing is found)
   ❓ what is open → in ②
     └──▶ ② 📖 words to know · how sure · what is open and what closes it (small, canvas.explains)
            └──▶ ③ in detail: design grids, models, chart, settings, the Job's own pictures (when the face asks)
```


The frames
----------

| frame | answers | read from |
|---|---|---|
| ① 🪜 The staircase | why the Job exists, its Tasks in order as steps, each Task's Runs, which Run to read | the Job face's `goal:`, `close:`, `answers:` (or `job.aim`); each Task page's `## Opening` (or `tasks.<t>.asked`, `.did`); each Run's receipt (its state mark), the face's `runs:` (its sentence, 📌 `current`), else `summary.headline` in its result, else what its `result/` holds |
| 📊 results, outside ① | what each Task found: one sentence, then charts, tables, its own figures | the finding (`tasks.<t>.found`, `conclusions`, else the page's `**Why it matters**`, `**Answer**` …); `charts:` and `tables:` read from the current Run's result files; else its `show` picks as a table; the pictures the Task holds (`figures:`, else its Runs' results, then its draft) |
| ② 📖 its words | the terms its labels use, how sure the reading is, what is open and what closes each | the face's `terms`, `sure`, `open: [{item, closer}]` |
| ③ on, in detail | only what the face asks for, or the Job's own pictures (not a Task's) | `design`, `models`, `chart`, `settings`, `detail: true`; `.png` and `.jpg` in the Job's folders outside its Tasks |

1. **The stairs**: each Task one step lower and 380 px further right; past four Tasks, several share a column.
   A Task's Runs stand in a grid, up to three a row (`run_cols`), so a Job grows wide, not tall.
   A big Job keeps its stairs (asked 261014): a family of Tasks is one step, listing its Tasks inside it, its
   Runs folded by what they do, its results a row or a bar per Task (`members: true`); past six steps, or where
   the face's `parts:` says (two parts or more, each from its own Task), the staircase continues in the next frame,
   joined by a "continues" arrow. A part per kind of work keeps each under check.py's 600 words.
   A step is as tall as its own boxes; its results stand outside, placed by rule 10.
2. **Room on purpose**: 170 px between steps; the frame may be large (`canvas.large`), never filled.
3. **Quiet reruns**: once a Task marks a 📌 current Run, the others are grey, but each still shows its name and
   its state; only the current one speaks. The current card is named in full too, never just `r03`.
4. **Every Run a card**: a Run that has not run, or has nothing to report, still takes its own card, named, its
   state on the second line (`⬜ no result yet`). Only past 24 Runs in one Task does the rest fold, by what they do
   (`fold_groups`): a series of 3 or more that differ only in a two-digit counter (`fold01-09 brave v1`) is one card,
   a family of 5 or more sharing a first word without digits (`page-evidence-item`) another, at most 12 Runs a card;
   every other Run keeps its own card. Each folded Run is its own line, named in full, with its mark (JL 261019; LLMRec
   b01 j02 t02 had shown its newest 20 Runs and folded folds 00-05 out of sight, unmarked). A 📌 current Run and a
   ◌ proposed one never fold; the face's `folds:` folds Runs it names into one titled card at any size. A card with
   a plan (aim, why, settings) takes a row of its own, 1,700 px wide; the others keep the grid.
5. **Results are pictures, from real code, in colour**: the figures a figure Run's Python code drew from its real
   result files first (`figures:`), else a chart per `charts:` entry (three at most), a table per `tables:` entry (two
   at most). Every bar is coloured by what it is about (`jd.bar_colors`): its own `color:`, the chart's `colors:` by
   label, the chart's `color:`, then the face's `colors:` by name, else blue; grey for a total or an absence. Each block is titled with its step's own name: `📊 t02 · <name>: results`.
   In a block they stand side by side, up to three a row, each under the shortest column so far; a long table
   (8 rows or more, a paper table) takes the columns nothing else fills, in parts of at least 4 rows.
6. **No left-aligned frames**: ② and ③ step down and right (`canvas.stairs`); ② is small (`canvas.explains`).
7. **Red is real**: ❓ names something missing on disk (no reading, no close, no finding), never a guess.
8. **The old frames**: `layout: classic` keeps ① why and ② in → Tasks → out; `layout: plain`, the model tables.
9. **From zero as the main**: `layout: explained`, as JL's sketch: one frame ① titled "explained from zero", as
   wide as its widest step and no wider, the Job at its top left, each Task a step lower and further right, and from each one line out of the frame
   to its result, a small table (its `settings` rows, low end → high end), level with it; the skeleton
   (title, Job, Task names, result headers) in type that reads at 10% zoom; ② words, ③ `formula`, the
   design grids small, stepping down.
10. **Results fill the room, evenly**: the blocks, in step order, are as wide as it takes (1 to 3 panels a row,
    `place_results`) for them together to stand about as tall as ①. Shorter than ①, each sits as near its step as
    it can, inside ①'s top and bottom; taller, they are one run centred on ①, rising above it exactly as far as
    they hang below (`results_layout`). Every other block steps 240 px right (错位). A step's line runs straight to
    its block where they are level; else it bends in its own lane between ① and the blocks and meets the block at
    its title, so no two lines cross
    (`results_lanes`). `canvas.stairs` and `canvas.grid` count results that rise above a frame.


The face's words
----------------

```yaml
job:
  name: j03_google_vs_direct_recommendation   # the Job folder, in the topic's Block
  aim: "…"                       # the Job's meaning in one sentence; empty: its face's goal: line
  reading: "…"                   # what it found: the staircase's key point, the main result first (30 words)
  inputs:                        # what goes in, with counts, EVERY input (up to 6 drawn); 📥 beside the Job
  - {item: "The j01 pool: 1,029,246 physicians", path: _WorkSpace/…/1-CandidatePool/v2026-08/npi_pool.parquet}
  - {item: "…", path: [<file>, <folder>/]}   # a string still works; path: one or a list, each drawn under the item
                                 #   in grey, broken only after a slash; red ❓ when not found under the Job or any
                                 #   folder above it (_WorkSpace/ under the SPACE root, work/ under the Project)
  outputs: [ … ]                 # what comes out, the same shape (up to 6 drawn); 📤 beside the Job
  colors: {HealthGrades: blue, Vitals: orange}   # one source, one hue: a bar whose label holds the name takes it
  tasks:                         # per Task folder
    t01_<task>: {asked: …, did: …, found: …}   # found: one sentence first; the results block shows that sentence
  steps:                         # a family of Tasks as one step; unasked, past 8 Tasks, 3 or more of one kind
  - {title: "the 10 diabetes signals", tasks: t17-t26}    # a range or [t14, t15]; `key:` names it in charts:
    #   frame: "in place" draws the family as its own staircase in its place in the story, never also as a
    #   step in ①, so each Task is drawn once (the face's notes for its key sit under its key point);
    #   frame: true draws the family again as its own staircase, its Tasks as steps; reading: that frame's key
    #   point; run: + show_each: [{label, at: "file.json:key"}] gives every member Task the same picks
  parts: [{title: "…"}, {title: "…", from: t27, key: "…"}]   # two staircases or more (unasked past 6 steps, two,
                                 #   at the middle step); key: each later one's key point, else its title
  runs:                          # per Run, `tNN_task/rNN_run`: what it is and what makes it differ (18 words)
    t01_<task>/r04_<run>: {says: "p12: the same audit on parser p1.2", current: true}   # current: 📌, the one to read
    t01_<task>/r06_<run>: {in: "fold02-09 query rows", out: [PlatformRank/v2026-08/fold02/]}   # in, out: words for
                                                                 #   📥 and 📤 when no file on disk says them
  folds:                         # per Task: Runs the face folds into one titled card, whatever the Task's size
    t04_<task>: [{title: "binds t05's r01-r09 receipts, no rebuild", runs: "r0[1-9]_*"}]   # runs: a glob or a list
  show: {}                       # per Run, values picked from its result (as job_results.py's show); a table when
                                 #   the Task names no chart or table
  charts:                        # per Task: bars drawn with matplotlib from the current Run's result (or `run:`),
                                 #   each bar coloured (color:, colors: {label: grey}); a figure Run comes first
    t02_<task>:
    - {title: "Jaccard with Google, by model (95% interval)", file: metrics.json, each: metrics.by_model,
       value: jaccard_low.point, low: jaccard_low.ci_lower, high: jaccard_low.ci_upper, fmt: pct}
    - {title: "What Google's rows became", bars: [{label: matched, at: metrics.g.rows_npi_auto}], fmt: int}
    - {title: "Slope by context (95% CI)", file: tables/h2-slopes.csv, sort: false, bars: [{label: low back pain,
       at: "model_id=m5&context=lbp.estimate", low: "model_id=m5&context=lbp.ci_lo", high: "…ci_hi"}]}
       # each: one bar per entry of a mapping (labels: renames; model names are shortened); bars: named values, a
       # CSV's row by col=v&col2=v, each with its own low/high; fmt: pct | int; digits: n; sort: false keeps the
       # file's order; low/high draw 95% whiskers
    t17-t26:                     # a family step (its key): one bar per member Task, each from its own Run
    - {title: "Rows per table", members: true, run: r02_profile, file: profile.json, label: table, value: rows,
       fmt: int}                # tables: the same, `columns: [{label, at, fmt}]`, one row per member Task
  notes:                         # per Task or family step key: short lines (or {term, means}) drawn to the
    t17-t26: ["each bar: one table", {term: present, means: "diabetes seen …"}]   #   right of its results,
                                 #   smaller, under "📖 how to read it": what each name, number and verdict means
  tables:                        # per Task: rows from a CSV under the current Run's result
    t02_<task>:
    - {title: "Rank agreement by model", file: rank_agreement.csv, columns: [model_dir, kendall_tau_b_mean, n],
       sort: -kendall_tau_b_mean, rows: 6}   # where: "col=v&col2=v" keeps only those rows (one model of many)
    - {title: "Table 1 (s27 · t04 r01_…), one key", run: r01_…, file: key_npi_lists.csv, where: "query_key=…",
       widths: [1.8, 2.6, 2.6, 1.4], columns: [engine, {at: npi_list_search, label: searched NPIs, items: 2}]}
                                 #   a column {at, label, items, sep}: a joined list shows its first items, "+k more";
                                 #   {at, label, words: n}: a long text cell shows its first n words (a meaning)
                                 #   every CSV table names its source under it: runs/<run>/result/<file>
                                 #   path: <file under the Block> in place of file: (a Task whose Runs keep none)
    t01_<papers>:                # a Task of one subject per Run (a paper): a row per Run, cells from each Run
    - {title: "Its papers", runs: true, rows: 12, columns: [{label: paper, at: "runtime.yaml:subject.title"},
       {label: says, at: says}]}   # at: says is the face's sentence on that Run; past rows, counted
                                 #   only: "r0[4-9]_*" keeps the Runs those globs name; a Run with nothing in
                                 #   the columns takes no row
  figures:                       # per Task: globs under the Task for the pictures to show (default: two found)
    t01_<task>: ["runs/r05_*_figures_*/result/*.png"]   # prefer this: a figure Run draws the charts into its own
                                 #   result/ (JL 261013: "make them run in the run's results"); `charts:` is a
                                 #   quick look drawn into the topic's assets/, for a Task with no figure Run yet
  terms: [{term: …, means: …}]   # every label the drawing shows, spelled out (means: 25 words); in ②
  sure: "…"                      # how sure the reading is, and why (50 words); in ②
  open: [{item: …, closer: …}]   # each open point and exactly what would close it; in ②
  later: [{item: …, closer: …}]  # Stage agreed moves open points here: drawn plain in ②, never red (no ❓ left)
  conclusions: {}                # per Task: its finding, when the page's own is not the right one
  layout: ""                     # empty: the staircase; classic: ① why, ② in → Tasks → out; plain: the model tables;
                                 #   explained: one ①, its Tasks as steps, each result a small table outside
                                 #   it (a settings row whose first cell is t01 is t01's: its low end → high end)
  design: {frames: [ … ]}        # each Task's Runs as grids, one mark per Run (0.4.0); in ③
  detail: false                  # true: ③ "explained from zero" (intro, terms, formula, a box per Task); in ③
```

The face holds words and paths; every number is read from a Run's result on every build, and every chart is redrawn
into the topic's `assets/` (generated: never edited, never tracked). Results that live outside the repository (a
`heavy.yaml` pointer, a store under `_WorkSpace/`) cannot be charted from a clone: say them in `runs:` and name their
source file. After a build, read the picture as a reader and call the reviewer: haipipe-studio `ref/reader-review.md`.

A topic adopted from `job_results.py` keeps its `results:` yaml's reading and open points: `adopt` carries them into
`job:`. Write the aim and the reading from the Job's own pages; say in the face's Decided line that they were drafted.


A family of Jobs, a table per Job
---------------------------------

Asked 261013 on Proj01 b00_rawdata (14 raw drops, 310 Tasks, one table each): "describe for each task, what we have
done, what are the content, I might want more figures and tables, to understand what I have". A family topic
(`group`, its Jobs in the face's `results: jobs:`) whose `group:` yaml gives a Job a `table` draws one act per Job:
① its steps, its reading and a row per Task, ② a chart, ③ its pictures; before them, for several Jobs, a box per Job
and the Jobs as a table. `each:` holds the words every Job shares; a Job's own entry adds to them.

```yaml
group:
  jobs_table: {title, sub, key, columns, caption}   # one row per Job; cells as below, read under each Job folder
  each:                                             # every Job's, unless its own entry says otherwise
    flow: [{title, lines, key}]                     # its steps; a line's {<file>:<key>|<fmt>|<when empty>} and
    arrows: [read by, …]                            #   {count:<glob>} are read under the Job on every build
    table:
      rows: "t*_profile_*"                          # which Task folders are rows (skip: [globs] leaves some out)
      file: runs/r07_full_scan/result/description.json   # where a bare `at` reads, in each Task
      sort: "-Rows"                                 # by a column, largest first
      columns:
      - {label: Table, at: table, else: title}      # a value; the Task's title when it has none
      - {label: Done, runs: true}                   # its Runs and their marks: ✅ r02 r07
      - {label: Rows, at: row.rows, bar: true}      # drawn as bars beside the table, row by row, log scale
      - {label: First → last month, at: [time.first_month, time.last_month], none: "no time column"}
      - {label: Source must check, at: flags, pick: flag, only: {severity: [check]}}   # fmt: count | gb | words
    figures: {pictures: [{file: "<glob under the Job>", caption}]}   # pictures its Runs already drew
    scan: {file: "<path in a Task>", caption}        # the picture shown for each Task its entry names in `scans`
  j51_<job>:
    gist: "…"        # its box in the family's first frame
    reading: "…"     # ①'s key point; slots allowed
    shows: "…"       # ③'s key point: what its pictures show
    scans: [t25_<task>, t40_<task>]
    chart: {title, key, bars: [{label, at: "<path under the Block>:<key>"}]}   # ② as chart_frame's bars
    open: ["…", {item, closer}]
```

The words are the face's; every number is a slot or a cell, read on every build. A table frame holds the bars as a
picture beside it, so ⑨ reads it as a scoreboard, not a wall of text. First drawn: Proj01 b00_rawdata s21 (seven
WellDoc drops), s22 (AI-READI), s23 (six external cohorts).


Commands
--------

```bash
J=Tools/plugins/haipipe-toolkit/skills/1_base/excalidraw/excalidraw-job/scripts/job_drawing.py
python $J make <job folder> [--nn NN] [--dry-run]   # the Block's topic studio/sNN-<jNN>-<job>/ (s21-s29), drawn
python $J draw <topic folder>                       # redraw one (what the topic's builder calls)
python $J adopt <topic folder> [--aim '…']          # a one-Job results topic, now drawn as the whole Job
python $J preview <job folder> <out.excalidraw> [--face <face.md>]   # draw a Job anywhere; its Block is not
                                                    #   touched; --face draws it with that face's job: yaml
python Tools/plugins/haipipe-toolkit/skills/1_base/excalidraw/excalidraw-studio/scripts/check.py <topic>.excalidraw
```

1. **One topic per Job**: `make` refuses a Job that already has one (a results topic or a whole-Job topic), and
   haipipe-studio's `job_results.py` reads a face's `job: name`, so neither makes a second.
2. **Adopt**: rewrites the builder and the face's Topic, Words and Files; keeps the folder's name and its Decided and
   Open lists, so links to the topic still work.
3. **Write the words**: per Task `found`; per Run `says` and one 📌 `current`; then `charts:` for what a reader must
   see at a glance, `tables:` for exact rows, `figures:` when the Task's own pictures are not the first two found.
4. **Check**: `check.py` after every build (no ❌); open the preview and read the whole picture, not a crop.
5. **Save the session**: haipipe-studio's `new_topic.py session <block> sNN`, a pass of `run-draw-<sNN>`.


Propose the tree, then evaluate the drawing
-------------------------------------------

Asked 261019: "现在我感觉我说一句你才改一句 … 一定要把这些 run 也 propose 好，然后每一个 run 都要排序排好", "for the
/excalidraw-job, for the run, could you also show what are the related files", and "how do you evaluate the sNN jNN
with /excalidraw-job, do we have the evaluation?". Before a Job is drawn, propose what it is missing; after, check it.

```bash
S=Tools/plugins/haipipe-toolkit/skills/1_base/excalidraw/excalidraw-job/scripts
python $S/propose_tree.py <job folder> --plan <plan.yaml> [--apply]   # proposed Tasks and Runs, numbered by type
python $S/job_check.py <topic folder>                                 # is the drawing true to its disk?
```

1. **Group** (`ref/propose-tree.md`): Job = one setup (model, data, engine); Task = one algorithm on it; Run = one
   setting. A knob the worker already takes is a Run (a sweep), never a Task.
2. **Order by type**: r0x smoke, r1x main, r2x sweep, r3x repeat, r4x score, r5x ablation; `after:` names the Run
   it waits for. Older Runs keep their names; a Task whose older Runs already fill a band numbers its new one after
   its last Run (r58 after r01-r57), its type kept in `run.yaml` `run_type`.
3. **Every card's state**: ✅ completed · ❌ failed, with its cause · 🔶 running · ⬜ ready (dashed) · ◌ proposed
   (dashed, with what it is for). A proposed Task's step is dashed; its results block says it is a plan, in grey.
4. **Every card's files**: `📥 in:` and `📤 out:` (what it read, what it wrote, one line each), then its ticket (🧾) and
   its config (⚙), each by its file name.
5. **Evaluate in three layers**: `check.py` for how it reads; `job_check.py` for what it claims (every Task and Run
   named, every card marked, every failure explained, every percentage in the words found in a result file, or in a
   Job the face lists under `cites:`); then a fresh reviewer reads it as a newcomer (haipipe-studio
   `ref/reader-review.md`). A drawing is done when all three pass.


Boundary
--------

| Owner | Owns |
|---|---|
| `excalidraw-job` | the Job's drawing: the staircase, its results blocks and charts, the face's `job:` yaml, `make`, `draw`, `adopt`, `preview` |
| `excalidraw-task` | a Task's own topic: its videos or Runs, its answers, tables, formulas; pointed to as `→ details: sNN` |
| `haipipe-studio` | the topic folder, numbering, sessions, `canvas.write`, `canvas.stairs` (frames as stairs), `canvas.explains` (a small explaining frame); `job_results.py`, whose `dig` reads a name with a dot whole |
| `excalidraw-studio` | the principles every frame follows, `draw.py`, `check.py` (an explaining frame is not held to a screen) |
| `dataviz` | how a chart reads: its colours (the reference palette in `PALETTE`), no legend on labelled bars, quiet axes, whiskers for intervals |
| `haipipe-job` | the Job face itself (`goal:`, `close:`, `answers:`, its Tasks in order); this skill only reads it |
| `haipipe-discovery`, `haipipe-task` | the Task pages and Runs it reads; it never writes them |

Its readers (`labelled`, `section`, `concept`, `tables`, `formulas`, `aims`, `task_info`, `table`) are for
excalidraw-task to import too, so a Task's page reads the same in both drawings.


Files
-----

```text
excalidraw-job/
├── SKILL.md                    this file
├── CHANGELOG.md                its versions
├── agents/openai.yaml          Codex's card
├── scripts/job_drawing.py      the readers, make, draw, adopt, preview; the classic, plain and explained frames; draw_job
│                               sends every Job to the staircase unless the face says layout: classic, plain or explained;
│                               PALETTE and bar_colors, every chart's colours
├── scripts/job_ladder.py       the staircase, its In and Out with paths (io_card), its results blocks (charts, tables,
│                               figures), its words frame; each Run
│                               card's state (✅ ❌ 🔶 ⬜ ◌, dashed until it ran), its cause or purpose, its files
├── scripts/propose_tree.py     proposed Tasks and Runs from a plan, each Run numbered by its type's band
├── scripts/job_check.py        a drawing against its disk: names, marks, causes, every percentage claimed
├── ref/propose-tree.md         how to group Job, Task and Run; Run types, order and states
├── tests/test_job_drawing.py   a Job made on a small Block, drawn, checked; one topic per Job; a Task's pointer
└── tests/test_job_ladder.py    steps move right, quiet reruns, charts and tables from results, frames as stairs
```

The first Jobs drawn: Knowledge-Base's Proj10-LLM-Baseline `discovery/b01_ml_foundations` s21 to s23 (adopted
261012); the staircase's first, Physician-SPACE LLMRec `work/b04_analysis_physician_visibility` s27 (b03 j03, 261013). Its own
Studio topic is Tools' `blueprints/b31_excalidraw/studio/s06-excalidraw-job/`.
