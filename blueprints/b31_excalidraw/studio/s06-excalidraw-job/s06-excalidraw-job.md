s06 · excalidraw-job: a Job as one drawing
==========================================

Made on 261012 (asked: "I want a new sNN for the excalidraw-job, which will show the sNN as the excalidraw as the job to
make the job's aim plan and results"), beside s02 to s05 (report, slide, read, section) and b31 s01 (excalidraw-studio).

**Stage:** agreed

**Topic:** what the skill `excalidraw-job` draws and how: a Job as one Studio topic of its Block, a staircase (since
0.6.0, 261013). The main frame: the Job on top (why it exists, when it is done), each Task a step lower and further
right, its Runs branching from its step (the current one marked 📌, reruns quiet). Each Task's results stand outside
the frame, small, level with its step: one sentence, then charts and tables read from its Runs' result files, then
the figures the Task already holds. A small frame of its words (terms, how sure, what closes each open point) steps
down and right. Every number is read from disk on every build; the face holds words and paths. This topic draws the
skill's parts, its workflow, its folder, and the first staircase it drew (Physician-SPACE LLMRec b04 s27), so a
session knows what a Job drawing holds before it makes one.

**Feeds:** none yet


Files
-----

```text
s06-excalidraw-job/
├── s06-excalidraw-job.md              this face; the drawing's words are its yaml blocks
├── build_s06_excalidraw_job.py        the builder; reads this face, the skill and the first Jobs drawn
├── s06-excalidraw-job.excalidraw      four frames as stairs: ① the skill, then ② ③ ④ each lower and further right
├── s06-excalidraw-job.png             its preview
├── .s06-excalidraw-job.seed.json      generated snapshot for preserving marks
└── examples/                          the first Job drawn, copied so the drawing stays true without Knowledge-Base
    ├── demo-staircase.png             a made-up Job drawn as a staircase at this build, drawn in frame ④
    ├── b01-s21-j01-math-classic-ml.png    the first Job drawn (Proj10, 261012), kept as history
    └── facts.json                     check.py's verdict on the demo, from the last build
```


What the drawing holds
----------------------

Four frames as stairs (b31 s01, 261013): ① the skill, the main frame, at the origin; ②, ③ and ④ each lower and
further right (`canvas.stairs`), a named arrow into each; no act names down a left edge.
Facts (version, functions, tests, the first Jobs' checks) are read from disk on every build; `{name}` in a yaml
string below is filled by the builder.

```yaml
stairs:
  order: [①, ②, ③, ④]
  arrows: [drawn by, kept in, made]
```

```text
① the skill, one mind map
   └─drawn by─▶ ② the workflow: a Job's files to a staircase and its results
                   └─kept in─▶ ③ its folder, as a tree
                                  └─made─▶ ④ a demo staircase, checked; the real ones named
```

① 🧠 the skill as a mind map: centre "a Job as a staircase, its results beside it"; the ask, the staircase, its
   results, its Runs, its words, its script, and what it never does.
② 🔁 the workflow: the Job's files into job_ladder.py, then what one build does.
③ 🧰 the skill folder and the folder a Job topic is written into, both as trees, and who owns each input.
④ 🖼️ a made-up Job drawn as a staircase, its preview and check.py's verdict; the real ones named (Tools is public).

Rebuild: `python build_s06_excalidraw_job.py`, then `check.py` on the drawing.


The skill as a mind map (①)
---------------------------

```yaml
mindmap:
  centre: "a Job as a staircase, its results beside it"
  branches:
  - title: 🙋 What was asked
    by: asked 261013
    summary: "Job, then Tasks as steps, results on the right"
  - title: 🪜 ① The staircase
    summary: "each Task a step lower and further right"
    by: standing
  - title: 📊 Its results
    summary: "charts and tables from disk; the Task's figures"
    by: standing
  - title: 📌 Its Runs
    summary: "the current one marked; reruns quiet"
    by: standing
  - title: 📖 ② Its words
    summary: "terms, how sure, what closes each open point"
    by: standing
  - title: 🐍 Its script
    summary: "job_ladder.py, {n_funcs} functions, v{version}"
    by: standing
  - title: 🚫 It never
    summary: "edits the Job, a Task page or a Run"
    by: standing
```


The workflow (②)
----------------

```yaml
flow_in:
  labels: [and, and, read by, writes]
  steps:
  - title: 🧱 the Job face
    lines: ["goal:, close:"]
  - title: 📝 the Task pages
    lines: ["question, finding"]
  - title: 🧾 the Runs
    lines: ["state, result files"]
  - title: 🐍 job_ladder.py
    key: true
    lines: ["a staircase"]
  - title: 🗺️ the topic
    lines: ["sNN-<jNN>-<job>/, assets/"]
flow_run:
  labels: [then, then, then]
  steps:
  - title: 📖 Read
    lines: ["Tasks, Runs, pages"]
  - title: 🪜 The stairs
    lines: ["Job, Tasks, Runs"]
  - title: 📊 Results
    lines: ["charts, tables"]
  - title: 💾 Write
    lines: ["marks kept"]
```


Where it lives and what it made (③ ④)
-------------------------------------

```yaml
owners:
- "the Job face: haipipe-job (goal:, close:, answers:, its Tasks in order); this skill only reads it"
- "the Task pages and their Runs: haipipe-discovery or haipipe-task"
- "the topic's folder, numbering and sessions: haipipe-studio; job_results.py draws a group of Jobs"
- "how each frame reads: excalidraw-studio's principles, draw.py, check.py"
- "the drawing and its face's job: yaml: this skill"
commands:
- "make <job>: the Block's topic sNN-<jNN>-<job>, drawn"
- "draw <topic>: redraw one; what its builder calls"
- "adopt <topic>: a one-Job results topic, now the whole Job"
- "preview <job> <out>: draw a Job anywhere, its Block untouched"
first:
  title: "🖼️ What it draws: a made-up Job as a staircase"
  sub: "excalidraw-job's own test fixture, drawn at every build; the real Jobs drawn stay in their SPACEs (Tools is public)"
  key: "Key point: each Job says why it exists and what it found, its results as charts beside its steps; before, a
    column of text boxes no one read."
  drawn:
  - "first real staircase: Physician-SPACE LLMRec b04 s27 (j08), 261013"
  - "the paper's s01-ideation redrawn by the same principles, 261013"
  open:
  - "⏳ later: the other 17 LLMRec Job faces name no charts yet; their results fall back to tables"
  - "⏳ later: results kept outside the repository cannot be charted from a clone"
  - "⏳ later: excalidraw-task to follow the same staircase (s07)"
```


Decided
-------

s06-D01 · Created (asked 261012: "I want a new sNN for the excalidraw-job, which will show the sNN as the excalidraw as
    the job to make the job's aim plan and results"): the topic on excalidraw-job, beside s02 to s05.
s06-D02 · excalidraw-job is its own skill, the sixth beside excalidraw-studio, -report, -slide, -read and -section
    (asked 261012, on s01's skill-folder frame: "I think here we might have the excalidraw-job?") (261012)
s06-D03 · A Job's drawing shows the whole Job in four frames: why, in → Tasks → out, what it concluded, its tables,
    formulas and pictures (asked 261012: "我想在这个桌上把这个 job 的所有内容都展示出来") (261012)
s06-D04 · First drawn on Proj10 b01 s21 to s23 by `adopt`: folders kept, aims and readings drafted from their Task
    pages; every frame passes check.py (261012)
s06-D05 · Few words (asked 261012: "add at least of words, (especially the small versions as possible) when drawing
    the workflow"; "make the draft to be less of wordy and concise"): excalidraw-studio's ⑦; the Job drawing is two
    frames, a Task's detail its own topic (excalidraw-task, built by the Proj10 session); this topic's ① and ② are
    redrawn short (261012)
s06-D06 · Open 4 settled: a workflow of four steps (three arrows) is a map; draw.py's kind() takes three (261012)
s06-D07 · Stage → agreed (JL 261012: "I think for others sNN, we can give them to level 3 as well"): the open points move to Later, drawn plain as
    "⏳ later:" (261012)
s06-D08 · A Job is a staircase (asked 261013, with a hand sketch: "先是 Job，下面跟着 Task 1、Task 2、Task 3 … 相当于一个
    阶梯状的图 … 右边就开始说明每一个具体的结果都是什么"; "current ones in the job sNN are very bad"): excalidraw-job 0.6.0,
    job_ladder.py, the default for every Job; `layout: classic | plain` keeps the old frames (261013)
s06-D09 · Results are charts and tables, not words (asked 261013: "你的 results 应该是图和表格呀 … 如果你有 Python 画的图，
    也一起扔过来"; "for the task, we might want to add the figures and table from it"): the face's `charts:` and
    `tables:` are read from the current Run's files; the Task's own figures follow (261013)
s06-D10 · 主次分明, frames as stairs (asked 261013: "一个很大的 frame，然后有一些小的 frame 是解释这些大的 frame 的 … 你不能
    每一个都是朝左对齐"): the staircase is the main frame; its words frame is small (`canvas.explains`) and steps down and
    right (`canvas.stairs`); this topic's own four frames are placed the same way (261013)


Open
----

(none open: agreed 261012, s06-D07)


Later
-----

1. b01's three Job topics keep their `-results` folder names so links still work; rename them `sNN-<jNN>-<job>`
   with `renamed-from:` in each face, when the old names stop being linked.
2. Many Job faces still say `goal: open` and `close: open`; the aims are drafted in the topics' faces. Move them
   into the Job faces (haipipe-job's), so ① reads them from the Job itself.
3. Work Jobs are now drawn with their numbers (Proj10 work/b01, b02, b11, 261012); a Job with pictures of its own
   (④) is not drawn yet.

(write here, or mark the drawing in red)
