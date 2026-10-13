s00 · Background and index
==========================

**Stage:** closed

**Tags:** `Structure`

**Topic:** what this Block stands on, for a reader new to it, and an index of its studio topics (sNN), Jobs (jNN)
and Questions (qNN) with how far each has come. The background is the yaml below, written by a person; the index
is read from disk on every build (JL 2026-10-12: "for every block, we also want to have the s00-background-and-index
to show the background information, and what are the sNN and jNN and what are the progress of them").

**Feeds:** none; it indexes the whole Block.


Files
-----

```text
s00-background-and-index/
├── s00-background-and-index.md          this face; its yaml is the Background frame
├── s00-background-and-index.excalidraw  the drawing: Background, then Index; a person's marks are kept
└── s00-background-and-index.png         its preview
```

Rebuild: `python <haipipe-studio>/scripts/block_index.py <this Block> --draw`, haipipe-studio being
`Tools/plugins/haipipe-toolkit/skills/1_base/project/haipipe-studio/`.


Background
----------

One frame per entry, two at most. An entry is a folder `tree:` (a string is a leaf, `{label: [children]}` a
branch), or `boxes:` with `arrows:` between them: each box sits `at: [column, row]`, says `why` it is there and
holds its own tree; each arrow names how one box leads to the next. An emoji leads each node (🧭 📖 🎯 🧱 …); a
leaf that starts with "❓" is still open and draws red. Without an `intro`, the first frame opens with the Block's
spine.

```yaml
background:
- title: 🧭 What this Block stands on
  boxes:
  - id: project
    at: [0, 0]
    title: 🏗 A Project, from its root down to one Run
    why: the one folder tree every Theme shares
    tree:
    - "📁 examples*/<Project>/ holds Themes: work, discovery, cowork, paper, insight, design, labeling"
    - 🧩 a Theme holds Blocks, bNN_<topic>/, each with its face board.md and its Questions
    - 🧱 a Block holds Jobs, jNN_<job>/; a Job holds Tasks, tNN_<task>/
    - 🏃 a Task holds Runs, runs/<run>/, each with its result beside it
    - ⚙️ a Run is hard (rNN_, it executes code) or soft (run-<type>-<target>, a step a person or an agent does)
  - id: workbench
    at: [1, 0]
    title: 🖥 The workbench
    why: one screen for any Block, Job or Task folder
    tree:
    - 🪟 one base frame, servers/workbench/frame.py, draws them all
    - "🔝 the top row: Studio | Block · Job · Task | Delivery, Guide beside it"
    - "🗂 the same Spaces at every level: Description · Studio · Report | Work · Runs · Delivery"
    - 🎨 each theme fills the frame from servers/workbench-<theme>/
    - "🔗 /wb <path> opens it: Tools on port 5623, WellDoc on 5602"
  - id: skills
    at: [2, 0]
    title: 🧰 The skill behind each button (s10)
    why: every button names the one skill that does its work
    tree:
    - 🧱 haipipe-block · the Block's face, its Questions, a new Block
    - 📋 haipipe-job and haipipe-task · the Job and the Task
    - 🧠 haipipe-studio · these topics, their drawings and sessions
    - 📝 haipipe-report · a Question's report Page
    - 🏃 haipipe-run · every Run's folder, card and passes
    - 📤 haipipe-delivery · what leaves the Block
  - id: history
    at: [3, 0]
    title: 🕰 Where it came from
    why: why some names and numbers look older than the Block
    tree:
    - 🚚 promoted from b01's j03 on 2026-10-10, keeping its topic and Question numbers
    - "🔀 b02_workbench merged in on 2026-10-07: the folder and the workbench are the same thing"
    - ✏️ haipipe-board became haipipe-block on 2026-10-12 (s21-D07)
    - 🚫 not here: each Theme's own insides; haipipe-task, -discovery, -paper and the others own them
    - "🗑 s11 to s13, the Block, Job and Task variants, deleted 2026-10-12 at JL's ask"
    - "🔀 merged on 2026-10-12 at JL's ask: s07 into s05, s21 into s10 (now s10-haipipe-project), s09 into s01"
    - "🕰 later: 13 topics against a guide of 10; s08 into s02 could merge"
  - id: chat
    at: [0, 1]
    title: 💬 A chat section
    why: a question comes up while we work on something
    tree:
    - each reply section ends with a Studio line that names its topic here
  - id: topic
    at: [1, 1]
    title: 🧠 A topic here, studio/sNN-<topic>/
    why: where the question is thought through and decided
    tree:
    - ✅ a decision is an sNN-DNN line in the topic's face
    - ❓ what is still open is its Open list, red on the drawing
  - id: change
    at: [2, 1]
    title: 🛠 A skill, checker or server change
    why: most answers here are code, not a Task Run, so b10 has no Jobs
    tree:
    - 📜 the skill's CHANGELOG says what changed and why
    - ✎ the topic's drawing gets a green note where it changed
  - id: report
    at: [3, 1]
    title: 📝 A report Page, reports/qNN_<topic>/
    why: the Question's answer, ⬜ open → 🔶 partial → ✅ answered
    tree:
    - it links the changed files and the topic's drawings
  arrows:
  - {from: project, to: workbench, label: is drawn by}
  - {from: skills, to: workbench, label: do each button's work}
  - {from: chat, to: topic, label: a Studio line names}
  - {from: topic, to: change, label: decides}
  - {from: change, to: report, label: answers a Question in}
  - {from: topic, to: workbench, label: shows in its Studio}
  - {from: change, to: skills, label: updates}
```


Studio plan
-----------

The topics this Block needs, as its story: each step names its topics and the arrow to the next. Drawn as the first
frame by haipipe-studio's `block_index.py`; a topic made or proposed shows its stage, question and output.

```yaml
studio_plan:
  title: 🧠 b10 · the Studio plan, as one story
  intro: "From the tree every Project shares, to the workbench that shows it, its details, every level, and the server that serves it."
  steps:
  - title: 🏗 The tree, and how a Block works
    why: what a Project, Block, Job, Task and Run are, how a Block's topics, Jobs and Tasks relate, and haipipe-project, which keeps the tree in shape and names the skill behind each button
    ids: [s01, s10, s14]
    next: is shown on
  - title: 🖥 The workbench's Spaces, one skill each
    why: Studio, Delivery, Related, Report (with its groups across the themes) and Run, each seen from its screen and from the skill behind it
    ids: [s02, s03, s04, s05, s06]
    next: worked out in
  - title: 🔍 The details of those Spaces
    why: "the Studio's Timeline and Folder: what moved when, and what the Block folder holds"
    ids: [s08, s09]
    next: drawn for every level
  - title: 🪜 The Guide, and the screens
    why: the Guide, and every element the screens draw
    ids: [s31, s32]
    next: served by
  - title: 🛰 The server
    why: how the workbench server starts, answers one request, and is shared with the team
    ids: [s51, s52]
```


Proposals
---------

New topics and Jobs this Block needs, each grounded in a gap on disk (its `why`). Proposed 2026-10-12; a person agrees
each before its folder is made. Drawn in s00's last frame, one row each: the gap, the topic, the Job, what it delivers.
b10 has no Jobs yet ("most answers here are code"); these three are code work big enough to track as Jobs.

```yaml
studio_proposals:
- id: s14
  slug: cross-theme-content
  title: Content across Themes
  group: Structure
  priority: 1
  status: conditional
  condition: once b10 is back near 10 topics (s08 into s02; s07, s09 and s21 were merged on 2026-10-12)
  why: Q04 (reports/q04_cross_theme_content) is open and no topic or Job feeds it
  question: What crosses between Themes and how is it bound, such as a paper taking from work and discovery, or a design from insight?
  jobs: []
  output: one binding rule per pair of Themes, written into Q04's report
```

```yaml
job_proposals:
- id: j01
  slug: runs_folder_move
  title: Move every Block's Runs into runs/<run>/
  status: proposed
  why: "s01 Open 0 names the move as the next step (\"then the move, one Block at a time\"), and no Job does it"
  topics: [s01, s06]
  finish: every Block keeps its Runs under runs/<run>/, moved one Block at a time and passed by haipipe-project's checker
- id: j02
  slug: theme_rename_rest
  title: Finish the Theme rename in WellDoc and Physician
  status: proposed
  why: s01's theme-rename-plan.md has phases 2 and 3 done for DrFirst only; phase 4 (WellDoc, Physician) and 5 remain
  topics: [s01]
  finish: phases 4 and 5 of theme-rename-plan.md done, every SPACE on work/ and singular Theme folders
- id: j03
  slug: update_keep
  title: Write the ticked lines in one command, wb.py update --keep
  status: conditional
  condition: once s10 Open 1 settles on one command rather than the agents' step
  why: s10 Open 1 asks whether /wb update should write the ticked lines itself; today an agent does it
  topics: [s10]
  finish: wb.py update <Block> --keep writes the ticked lines, with a test on b51
```


Decided
-------

s00-D01 · Stage → closed (JL 261012: "we can close s00 and s01"). s00's shape is settled: the background, the Studio plan, the
    index and the proposals, drawn in two acts with a key point each by block_index.py (haipipe-studio 0.13.16).
    The index is still redrawn from disk whenever a topic or Job changes; its Open point moved to Later.


Open
----

(none: closed 261012, s00-D01)


Later
-----

1. 13 topics against haipipe-studio's guide of 10 (s00 not counted; s09-block-folder added 2026-10-12): merge s08 into s02? (s11 to s13 were deleted
   on 2026-10-12; s07 was merged into s05, s21 into s10 and s09 into s01 the same day.)

(write here, or mark the drawing in red)
