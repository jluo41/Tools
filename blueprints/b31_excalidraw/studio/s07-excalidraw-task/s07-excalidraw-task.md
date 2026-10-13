s07 · excalidraw-task: a Task as one drawing
============================================

Made on 261012 (asked: "I think we even need to have the excalidraw-task as well, to show the details of each tasks
as well"; then "have you aded s07 excalidraw-task and update it to hte s01 as well?"), beside s06 (excalidraw-job).
The skill was built the same day by the Proj10 session, which JL had asked for one topic per Task in b51.

**Stage:** agreed

**Topic:** what the skill `excalidraw-task` draws and how: a Task as one Studio topic of its Block, in few words. The
idea first (its question as the key point; what it is, how it works, why it matters; its videos in reading order; the
questions to be ready for), then one frame per video: its key point, its steps in order, how to say it in an
interview, and what to check against the video, in red. The page keeps the full text; the face holds the short words.
A Job's drawing (excalidraw-job) points to each Task's topic.

**Feeds:** none yet


Files
-----

```text
s07-excalidraw-task/
├── s07-excalidraw-task.md              this face; the drawing's words are its yaml blocks
├── build_s07_excalidraw_task.py        the builder; reads this face, the skill and the first Tasks drawn
├── s07-excalidraw-task.excalidraw      four frames in two acts, joined by named arrows
├── s07-excalidraw-task.png             its preview
└── examples/                           the first Task drawn, copied so the drawing stays true without Knowledge-Base
    ├── b01-s24-t01-entropy-cross-entropy-kl.png
    └── facts.json                      check.py's verdicts on the first Tasks, from the last build that could read them
```


What the drawing holds
----------------------

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
Act 1 · What it draws          ① the skill, one mind map ─drawn by─▶ ② the workflow, a page to its frames
         │ kept in
Act 2 · Where it lives         ③ its folder, as a tree ─made─▶ ④ the first Tasks drawn, checked
```


The skill as a mind map (①)
---------------------------

```yaml
mindmap:
  centre: "a Task as one drawing: its idea, then each video"
  branches:
  - title: 🙋 What was asked
    by: asked 261012
    summary: "each Task an sNN; each frame, what a video told"
  - title: ⓪ The idea
    summary: "question, what, how, why; videos in order"
    by: standing
  - title: 🎬 A frame per video
    summary: "its key point, its steps, its interview line"
    by: standing
  - title: 🔍 Check first
    summary: "what to check against the video, in red"
    by: standing
  - title: 📥 Its words
    summary: "the page first, then short words in the face"
    by: standing
  - title: 🐍 Its script
    summary: "task_drawing.py, {n_funcs} functions, v{version}"
    by: standing
  - title: 🚫 It never
    summary: "edits the Task page or a Run"
    by: standing
```


The workflow (②)
----------------

```yaml
flow_in:
  labels: [and, read by, writes]
  steps:
  - title: 📝 the Task page
    lines: ["idea, videos, checks"]
  - title: 🗒️ the face
    lines: ["the short words"]
  - title: 🐍 task_drawing.py
    key: true
    lines: ["idea + a frame per video"]
  - title: 🗺️ the topic
    lines: ["sNN-tNN-<task>/"]
flow_run:
  labels: [then, then, then]
  steps:
  - title: 🛠️ make
    lines: ["the page's words first"]
  - title: ✍️ write
    lines: ["idea, videos, in the face"]
  - title: 🔁 draw
    lines: ["the short words"]
  - title: 🔍 check.py
    lines: ["⑦ on every frame"]
```


Where it lives and what it made (③ ④)
-------------------------------------

```yaml
owners:
- "the Task page and its Runs: haipipe-discovery; this skill only reads them"
- "the page readers: excalidraw-job's job_drawing.py (section, concept, plain), shared, not copied"
- "the topic's folder, numbering and sessions: haipipe-studio"
- "how each frame reads: excalidraw-studio's principles (⑦), draw.py, check.py"
- "the drawing and its face's task: yaml: this skill"
limits:
- "idea: question ≤ 14 words; what, why ≤ 20; how 3 to 5 steps ≤ 8"
- "a video: name ≤ 6; says ≤ 20; 3 to 5 points ≤ 10; hook ≤ 16; checks ≤ 8"
commands:
- "make <task | job>: one topic per Task, drawn"
- "draw <topic>: redraw one; what its builder calls"
- "preview <task> <out>: draw a Task anywhere"
first:
  source: ../Knowledge-SPACE/examples-2-tech/Proj10-LLM-Baseline/discovery
  picture: b01_ml_foundations/studio/s24-t01-entropy-cross-entropy-kl
  blocks: [b01_ml_foundations, b51_llm_serve]
  open:
  - "⏳ later: Task topics past the runs band start at s31 (b51 took s01 to s10)"
  - "⏳ later: the face's short words are written per Task; each pass needs a check"
  - "⏳ later: only Discovery Tasks with video pages drawn so far; work Tasks next"
```


Decided
-------

s07-D01 · Created (asked 261012: "I think we even need to have the excalidraw-task as well, to show the details of each
    tasks as well"): the topic on excalidraw-task, beside s06 (excalidraw-job); the skill is the Proj10 session's.
s07-D02 · First drawn on b01's six Tasks (s24 to s29) and b51's ten (s01 to s10); every b01 frame passes check.py,
    with the short words written from each page (261012)
s07-D03 · Stage → agreed (JL 261012: "I think for others sNN, we can give them to level 3 as well"): the open points move to Later, drawn plain as
    "⏳ later:" (261012)
s07-D04 · A Task follows excalidraw-job's staircase (JL 261013: "you should also think about how to update the
    /excalidraw-task as well, we try to follow the same idea"): the Task's question on top, each Run or video a step
    lower and further right, the current Run marked; each step's results outside the frame, small (charts, curves,
    tables, its figures, a video's screenshots); a small frame for its words and formulas; transcripts only when
    asked. Proposed, not yet built (261013)
s07-D05 · Built (261013): excalidraw-task 0.5.0, `scripts/task_stairs.py`, the default for every Task;
    `layout: rows | plain` keeps the frames before it. Each step is level with its results block; first drawn as
    previews on LLMRec b04 j08 t02 (a work Task) and Proj10 b51 t01 (six videos); tests read the staircase (261013)


Open
----

1. Proj10's video Task topics (b01 s24 to s29, b51 s01 to s10) become staircases on their next rebuild: rebuild
   them in their SPACE and read them; add `current:` and `charts:` where a work Task has numbers.


Later
-----

1. A Job with more Tasks than the runs band holds: Proj10 numbers Task topics from s31 (b51 took s01 to s10);
   say it in haipipe-studio's numbering when it settles.
2. The short words are written by hand or by an agent: excalidraw-task could check its own word limits before a
   build, not only ⑦ after it.

(write here, or mark the drawing in red)
