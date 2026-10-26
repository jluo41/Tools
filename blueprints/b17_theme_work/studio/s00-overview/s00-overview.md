s00 · Overview
==============

**Stage:** shaping

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
- title: 🧭 What b17 is about
  cols: 2
  tree:
  - 🎯 What it settles:
    - How the work Theme fits the shared ladder, level by level, and what a work Block, Job, Task and Run each hold
      and show on screen.
  - ✅ Done when:
    - Each of its four Questions has a report with an answer status, and each answer names the skill, workbench or
      builder change that settled it.
  - 📖 The work Theme in one breath:
    - A Task plans, builds, runs and reports its work.
    - Each Run is one ticket with its result and its receipt.
    - Jobs group Tasks; a Question's report reads their Runs.
  - 🧭 Where it stands today:
    - 'Folders: one folder per Run is now the ladder''s rule, as s01 proposed.'
    - 'Screens: work Blocks now open on Goal · Plan · Execution · Results (261021), not the six Spaces s01 proposed.'
    - 'Skills: workbench-work and haipipe-work live in 2_theme/work; the task-for-* kinds stay in base for now.'
  - 🚪 Start here:
    - s01 · the ladder, Block down to Run (the Q01 grid).
    - Then Q01's report, reports/q01_work_ladder/.
  - ➡️ Next:
    - 'Settle Q01: say what was adopted and what replaced the rest.'
    - Answer Q02 and Q03 from what is built now.
    - 'Q04: decide the pipelines'' home and the task agents.'
```

The reading order of the topics, drawn as the Studio plan:

```yaml
studio_plan:
  title: 🚪 Where to start · the topics in reading order
  intro: Start at s01, the ladder; each step leads to the next.
  steps:
  - title: 1 · The question
    ids: [s01]
    why: what each level holds and shows (Q01)
    next: which skills build it?
  - title: 2 · The skills
    ids: [s02]
    why: what moves to the work theme, what stays in base (Q04)
    next: how does each element look?
  - title: 3 · The looks
    ids: [s32]
    why: one look per element, picked from b03 (Q01, Q03)
    next: and what is built today?
  - title: 4 · Today's workbench
    ids: [s03]
    why: the "before" the ladder replaces
```


Open
----

1. Q01 is still marked open although half of it was adopted and half replaced since 261007: settle it (see Next).
2. Q02, Q03 and Q04 have reports with no answer yet.

(write here, or mark the drawing in red)
