s06 · excalidraw-job: a Job as one drawing
==========================================

Made on 261012 (asked: "I want a new sNN for the excalidraw-job, which will show the sNN as the excalidraw as the job to
make the job's aim plan and results"), beside s02 to s05 (report, slide, read, section) and b31 s01 (excalidraw-studio).

**Stage:** agreed

**Topic:** what the skill `excalidraw-job` draws and how: a Job as one Studio topic of its Block, in two frames and few
words (excalidraw-studio ⑦). ① why the Job exists (its aim, each Task's question, when it is done), ② what goes in,
its Tasks in order with each one's state and finding, and what comes out, the Job's reading as the key point. A Task's
detail is its own topic (excalidraw-task). Every word is read from the Job on disk on every build; the topic's face
adds only the aim and the reading. This topic draws the skill's parts, its workflow, its
folder, and the first Jobs it drew (Knowledge-Base's Proj10 b01 s21 to s23), so a session knows what a Job drawing
holds before it makes one.

**Feeds:** none yet


Files
-----

```text
s06-excalidraw-job/
├── s06-excalidraw-job.md              this face; the drawing's words are its yaml blocks
├── build_s06_excalidraw_job.py        the builder; reads this face, the skill and the first Jobs drawn
├── s06-excalidraw-job.excalidraw      four frames in two acts, joined by named arrows
├── s06-excalidraw-job.png             its preview
├── .s06-excalidraw-job.seed.json      generated snapshot for preserving marks
└── examples/                          the first Job drawn, copied so the drawing stays true without Knowledge-Base
    ├── b01-s21-j01-math-classic-ml.png    its preview, drawn in frame ④
    └── facts.json                     check.py's verdicts on b01 s21 to s23, from the last build that could read them
```


What the drawing holds
----------------------

Four frames in two acts, a row each, the act named at the left, a named arrow for each step (b31 s01 principle ③).
Facts (version, functions, tests, the first Jobs' checks) are read from disk on every build; `{name}` in a yaml
string below is filled by the builder.

```yaml
acts:
- name: Act 1 · What it draws
  frames: [①, ②]
  arrow: drawn by
- name: Act 2 · Where it lives and what it made
  frames: [③, ④]
  arrow: made
between: {from: ①, to: ③, label: kept in}
```

```text
Act 1 · What it draws          ① the skill, one mind map ─drawn by─▶ ② the workflow, a Job to two frames
         │ kept in
Act 2 · Where it lives         ③ its folder, as a tree ─made─▶ ④ the first Jobs drawn, checked
```

① 🧠 the skill as a mind map: centre "a Job as one drawing, in few words"; the ask, its two frames, a Task's
   detail, its words, its script, and what it never does.
② 🔁 the workflow: the Job's files into the script, then what one build does, frame by frame.
③ 🧰 the skill folder and the folder a Job topic is written into, both as trees, and who owns each input.
④ 🖼️ the first Job drawn (b01 s21), its preview, and check.py's verdicts on b01 s21 to s23; red where one fails.

Rebuild: `python build_s06_excalidraw_job.py`, then `check.py` on the drawing.


The skill as a mind map (①)
---------------------------

```yaml
mindmap:
  centre: "a Job as one drawing, in few words"
  branches:
  - title: 🙋 What was asked
    by: asked 261012
    summary: "aim, plan, results; all on one canvas; few words"
  - title: 🎯 ① Why
    summary: "the aim, each Task's question, when done"
    by: standing
  - title: 🔁 ② In → Tasks → out
    summary: "each Task: its state, its finding, → its topic"
    by: standing
  - title: 🧩 A Task's detail
    summary: "its own topic: excalidraw-task"
    by: standing
  - title: 📥 Its words
    summary: "from disk; the face: aim and reading"
    by: standing
  - title: 🐍 Its script
    summary: "job_drawing.py, {n_funcs} functions, v{version}"
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
    lines: ["their state"]
  - title: 🐍 job_drawing.py
    key: true
    lines: ["two frames"]
  - title: 🗺️ the topic
    lines: ["sNN-<jNN>-<job>/"]
flow_run:
  labels: [then, then, then]
  steps:
  - title: 📖 Read
    lines: ["Tasks, Runs, pages"]
  - title: 🎯 ① Why
    lines: ["a mind map"]
  - title: 🔁 ② In → out
    lines: ["a workflow"]
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
  source: ../Knowledge-Base/examples-C2-tech/Proj10-LLM-Baseline/discovery/b01_ml_foundations/studio
  picture: s21-j01-math-classic-ml-results
  topics: [s21-j01-math-classic-ml-results, s22-j02-rl-basics-results, s23-j03-pre-llm-nlp-results]
  open:
  - "⏳ later: the -results folder names; rename with renamed-from: kept"
  - "⏳ later: many Job faces leave goal: and close: open; the aims sit in the topics' faces"
  - "⏳ later: a Job with pictures of its own (④) is not drawn yet"
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
