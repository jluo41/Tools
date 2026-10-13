---
name: excalidraw-job
description: >-
  A Job drawn as one Studio topic, a staircase: the Job on top (why it exists, when it is done), each Task a step lower
  and further right, its Runs branching from its step (the current one marked, reruns quiet), and each Task's results
  as charts, tables and the figures it already holds, in a small block outside the frame, level with its step. Smaller
  frames that explain it (its words, how sure, what is open) step down and to the right; nothing is left-aligned or
  filled. Read from disk on every build. Use to draw a Job, to turn a Job's results topic (job_results.py) into the
  whole Job, or to see at a glance why a Job exists and what it found. Trigger: draw the job, job drawing, the whole
  job, job staircase, tasks and runs, job results as charts, what did the job find, /excalidraw-job.
allowed-tools: Bash, Read, Edit, Write, Grep, Glob
metadata:
  version: "0.6.0"
  last_updated: "2026-10-13"
  # version history: ./CHANGELOG.md
---

# /excalidraw-job · a Job as one drawing, a staircase

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

```text
① 🪜 the staircase (main, large)                                         outside, small, level with each step
   🎯 the reading (the key point)
   🧱 j08 · why · done when · answers ──▶ 📥 in · 📤 out
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
2. **Room on purpose**: 170 px between steps; the frame may be large (`canvas.large`), never filled.
3. **Quiet reruns**: once a Task marks a 📌 current Run, the others are grey names; only the current one speaks.
4. **Quiet Runs fold**: a Run with nothing to report never takes a row; past six, the latest that report show.
5. **Results are pictures**: a chart per `charts:` entry, a table per `tables:` entry, then the Task's own figures.
6. **No left-aligned frames**: ② and ③ step down and right (`canvas.stairs`); ② is small (`canvas.explains`).
7. **Red is real**: ❓ names something missing on disk (no reading, no close, no finding), never a guess.
8. **The old frames**: `layout: classic` keeps ① why and ② in → Tasks → out; `layout: plain`, the model tables.


The face's words
----------------

```yaml
job:
  name: j08_google_vs_direct_recommendation   # the Job folder, in the topic's Block
  aim: "…"                       # the Job's meaning in one sentence; empty: its face's goal: line
  reading: "…"                   # what it found: the staircase's key point, the main result first (30 words)
  inputs: [ … ]                  # what goes in, with counts (1 to 3 drawn); 📥 beside the Job
  outputs: [ … ]                 # what comes out (1 to 3 drawn); 📤 beside the Job
  tasks:                         # per Task folder
    t01_<task>: {asked: …, did: …, found: …}   # found: one sentence first; the results block shows that sentence
  runs:                          # per Run, `tNN_task/rNN_run`: what it is and what makes it differ (18 words)
    t01_<task>/r04_<run>: {says: "p12: the same audit on parser p1.2", current: true}   # current: 📌, the one to read
  show: {}                       # per Run, values picked from its result (as job_results.py's show); a table when
                                 #   the Task names no chart or table
  charts:                        # per Task: bars drawn with matplotlib from the current Run's result (or `run:`)
    t02_<task>:
    - {title: "Jaccard with Google, by model (95% interval)", file: metrics.json, each: metrics.by_model,
       value: jaccard_low.point, low: jaccard_low.ci_lower, high: jaccard_low.ci_upper, fmt: pct}
    - {title: "What Google's rows became", bars: [{label: matched, at: metrics.g.rows_npi_auto}], fmt: int}
       # each: one bar per entry of a mapping (labels: renames; model names are shortened); bars: named values;
       # fmt: pct | int; digits: n; sort: false keeps the file's order; low/high draw 95% whiskers
  tables:                        # per Task: rows from a CSV under the current Run's result
    t02_<task>:
    - {title: "Rank agreement by model", file: rank_agreement.csv, columns: [model_dir, kendall_tau_b_mean, n],
       sort: -kendall_tau_b_mean, rows: 6}
  figures:                       # per Task: globs under the Task for the pictures to show (default: two found)
    t01_<task>: ["runs/r04_*/result/*.png"]
  terms: [{term: …, means: …}]   # every label the drawing shows, spelled out (means: 25 words); in ②
  sure: "…"                      # how sure the reading is, and why (50 words); in ②
  open: [{item: …, closer: …}]   # each open point and exactly what would close it; in ②
  conclusions: {}                # per Task: its finding, when the page's own is not the right one
  layout: ""                     # empty: the staircase; classic: ① why, ② in → Tasks → out; plain: the model tables
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
J=Tools/plugins/haipipe-toolkit/skills/1_base/display/excalidraw-job/scripts/job_drawing.py
python $J make <job folder> [--nn NN] [--dry-run]   # the Block's topic studio/sNN-<jNN>-<job>/ (s21-s29), drawn
python $J draw <topic folder>                       # redraw one (what the topic's builder calls)
python $J adopt <topic folder> [--aim '…']          # a one-Job results topic, now drawn as the whole Job
python $J preview <job folder> <out.excalidraw>     # draw a Job anywhere; its Block is not touched
python Tools/plugins/haipipe-toolkit/skills/1_base/display/excalidraw-studio/scripts/check.py <topic>.excalidraw
```

1. **One topic per Job**: `make` refuses a Job that already has one (a results topic or a whole-Job topic), and
   haipipe-studio's `job_results.py` reads a face's `job: name`, so neither makes a second.
2. **Adopt**: rewrites the builder and the face's Topic, Words and Files; keeps the folder's name and its Decided and
   Open lists, so links to the topic still work.
3. **Write the words**: per Task `found`; per Run `says` and one 📌 `current`; then `charts:` for what a reader must
   see at a glance, `tables:` for exact rows, `figures:` when the Task's own pictures are not the first two found.
4. **Check**: `check.py` after every build (no ❌); open the preview and read the whole picture, not a crop.
5. **Save the session**: haipipe-studio's `new_topic.py session <block> sNN`, a pass of `run-draw-<sNN>`.


Boundary
--------

| Owner | Owns |
|---|---|
| `excalidraw-job` | the Job's drawing: the staircase, its results blocks and charts, the face's `job:` yaml, `make`, `draw`, `adopt`, `preview` |
| `excalidraw-task` | a Task's own topic: its videos or Runs, its answers, tables, formulas; pointed to as `→ details: sNN` |
| `haipipe-studio` | the topic folder, numbering, sessions, `canvas.write`, `canvas.stairs` (frames as stairs), `canvas.explains` (a small explaining frame); `job_results.py`, whose `dig` reads a name with a dot whole |
| `excalidraw-studio` | the principles every frame follows, `draw.py`, `check.py` (an explaining frame is not held to a screen) |
| `dataviz` | how a chart reads: one series, no legend, quiet axes, whiskers for intervals |
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
├── scripts/job_drawing.py      the readers, make, draw, adopt, preview; the classic and plain frames; draw_job
│                               sends every Job to the staircase unless the face says layout: classic or plain
├── scripts/job_ladder.py       the staircase, its results blocks (charts, tables, figures), its words frame
├── tests/test_job_drawing.py   a Job made on a small Block, drawn, checked; one topic per Job; a Task's pointer
└── tests/test_job_ladder.py    steps move right, quiet reruns, charts and tables from results, frames as stairs
```

The first Jobs drawn: Knowledge-Base's Proj10-LLM-Baseline `discovery/b01_ml_foundations` s21 to s23 (adopted
261012); the staircase's first, Physician-SPACE LLMRec `work/b04_analyses_of_llm_ranks` s27 (j08, 261013). Its own
Studio topic is Tools' `blueprints/b31_excalidraw/studio/s06-excalidraw-job/`.
