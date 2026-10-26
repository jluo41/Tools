s00 · Background and index
==========================

**Stage:** closed

**Topic:** what this Block stands on, for a reader new to it, and an index of its studio topics (sNN), Jobs (jNN)
and Questions (qNN) with how far each has come. The background is the yaml below, written by a person; the index
is read from disk on every build (JL 2026-10-12: "for every block, we also want to have the s00-overview").

**Feeds:** none; it indexes the whole Block.


Files
-----

```text
s00-overview/
├── s00-overview.md          this face; its yaml is the Background frame
├── s00-overview.excalidraw  the drawing: Background, then Index; a person's marks are kept
└── s00-overview.png         its preview
```

Rebuild: `python <haipipe-studio>/scripts/block_index.py <this Block> --draw`, haipipe-studio being
`Tools/plugins/haipipe-toolkit/skills/1_base/project/haipipe-studio/`.


Background
----------

One frame per entry, two at most, each a folder tree: a string is a leaf, `{label: [children]}` a branch; an emoji
leads each node (🧭 📖 🎯 🧱 …), and a leaf that starts with "❓" is still open and draws red. Without an `intro`, the
first frame opens with the Block's spine.

```yaml
background:
- title: 🧭 What b31 stands on
  cols: 2
  tree:
  - 🎯 Done when:
    - each Excalidraw skill has a topic here that names what it draws, how, and what it made, checked on a real drawing
  - 📖 What it is about:
    - "seven skills draw what every Block's Studio shows: excalidraw-studio (how a topic's drawing reads), excalidraw-report, excalidraw-slide, excalidraw-read, excalidraw-draft, excalidraw-job, excalidraw-task"
    - "s01 holds the principles every topic drawing follows; s02 to s07 one topic per skill; s21 one mode measured"
  - 🧱 What it owns:
    - the principles, and how each skill draws
    - "not here: a topic's folder, face and sessions (haipipe-studio)"
```


Studio plan and proposals
-------------------------

The topics and Jobs this Block needs, made or proposed (asked 261012: "s00 should also work in a way for the
proposing the sNN and jNN as well"). A proposed one is red and dashed until a person ticks it; nothing proposed
is made before. `block_index.py` draws all three (`job_proposals` since haipipe-studio 0.13.8).

```yaml
studio_plan:
  title: 🧠 b31 · how the Excalidraw skills draw
  intro: the principles first, then one topic per kind of drawing, then the modes measured and the builders moved
  steps:
  - title: 📐 The principles
    ids: [s01]
    why: how every Studio drawing reads, agreed before any skill draws
    next: each kind follows them
  - title: 🖼️ Each kind of drawing
    ids: [s02, s03, s04, s05, s06, s07]
    why: "one topic per excalidraw skill: what it draws, how, and what it made"
    next: measured on real drawings
  - title: ⏱️ Measured and moved
    ids: [s21, s22, s23]
    why: a mode's steps and cost measured; the builders moved onto draw.py; the density floors set
```

```yaml
studio_proposals:
- id: s01
  title: Drawing principles, excalidraw-studio's topic
  group: Principles
  priority: 1
  status: created
  question: How should every Studio topic's drawing read?
  output: the drawing principles and the look, carried into excalidraw-studio
- id: s02
  title: excalidraw-report
  group: Kinds
  priority: 2
  status: created
  question: How does excalidraw-report draw a scratch and a report's drawing, and what has it made?
  output: its modes, steps and scripts, checked on real drawings
- id: s03
  title: excalidraw-slide
  group: Kinds
  priority: 2
  status: created
  question: How does excalidraw-slide draw a deck before it is built, and what has it made?
  output: slides.py to drawing to deck, checked on real drafts
- id: s04
  title: excalidraw-read
  group: Kinds
  priority: 2
  status: created
  question: How does excalidraw-read put a paper onto a canvas (a file we revise is excalidraw-draft, s21)?
  output: its read and revise modes, checked on real canvases
- id: s05
  title: excalidraw-draft
  group: Kinds
  priority: 2
  status: created
  question: How does excalidraw-draft draw a paper's Sections as a map?
  output: from Draft plans and Evidence Items to the map, checked on a real one
- id: s06
  title: excalidraw-job
  group: Kinds
  priority: 2
  status: created
  question: How does excalidraw-job draw a whole Job, from its aim to what it found?
  output: two frames in few words, read from a Job's files, checked on a real Job
- id: s07
  title: excalidraw-task
  group: Kinds
  priority: 2
  status: created
  question: How does excalidraw-task draw a Task, its idea and then each video?
  output: an idea frame and a frame per video, in few words, checked on real Tasks
- id: s21
  title: Revise mode, measured
  group: Measured
  priority: 3
  status: created
  question: What does excalidraw-draft cost, step by step, on a real file?
  output: its steps, scripts and seconds
- id: s22
  title: Every builder on draw.py
  group: Measured
  priority: 4
  status: proposed
  jobs: [j01]
  question: Which Studio builders still keep their own drawing helpers, and what moves each onto excalidraw-studio's draw.py?
  output: a list of builders and their move, each rebuilt clean on draw.py
  why: "only 6 of 94 Studio builders under blueprints/ import excalidraw-studio's scripts/draw.py (all in b31); 88 draw with their own helpers, so the principles reach one Block"
- id: s23
  title: Density floors, measured
  group: Measured
  priority: 5
  status: proposed
  question: What density does a good text frame have, measured across every Block's drawings?
  output: the text floor canvas.py checks, measured
  why: "the text floor was set by hand on 261012, not measured: SPARSE_MIN = 120 in haipipe-studio's canvas.py; a map frame is measured by ⑦ since s01 Open 6 was settled (s01-D19)"
```

```yaml
job_proposals:
- id: j01
  slug: builder-migration
  title: Move every Studio builder onto draw.py
  status: proposed
  topics: [s22, s01]
  finish: each Block's builders import excalidraw-studio's draw.py and rebuild clean
  why: "88 of 94 Studio builders do not import draw.py yet; s22 lists them, this Job moves them, one Block at a time"
```


Decided
-------

s00-D01 · Stage → closed (JL 261012: "we can close s01 now and s00"). b31's background, Studio plan and proposals
    are settled: seven skills, a topic each (s01 to s07), and s21; s22, s23 and the Job j01 stay proposed, red and
    dashed, until a person ticks them. block_index.py still redraws the index from disk when a topic or Job changes.


Open
----

1. Settled 261012: the background was rewritten for the Excalidraw skills; excalidraw-job (s06) joined as the sixth,
   excalidraw-task (s07) as the seventh.
2. Settled 261012: `block_index.py` draws `job_proposals` (haipipe-studio 0.13.8): a red dashed row per Job not made yet.
3. Settled 261012: the proposed Job j02 (canvas-key-colour, "Let canvas.py keep the one key-point colour") was done
   without a Job: haipipe-studio 0.13.14 keeps `canvas.KEY` in the palette (b31 s01-D18). It is off `job_proposals`.

(none open: closed 261012, s00-D01)

