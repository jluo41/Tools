---
name: workflow
part-of: hai-draw
description: "Draws a study's workflow as one building map, left to right, from the data and tests to where each answer lands in the paper, with a review overlay for reviewer comments; also the s04 paper flow. Trigger: draw the paper workflow, building map, review overlay, s04 drawing, /hai-draw workflow."
allowed-tools: Bash, Read, Edit, Write, Grep, Glob
metadata:
  version: "0.3.0"
  last_updated: "2026-10-26"
  # version history: ./CHANGELOG.md
---

# /hai-draw workflow · a paper's building map, with what the reviewers hit

One script draws every paper's building map, with the review overlay; hai-paper-story calls it for a paper's
workflow topic. The map keeps its own shape (hai-draw SKILL.md § Shapes that keep their own rules).

```text
THE DATA ─▶ THE SOURCES ─▶ THE TESTS ─▶ ANALYSIS ─▶ SUB-QUESTION → CLAIM ─▶ IN THE PAPER     light version
│ the foundation: every question stands on it │ │ one row per sub-question                  │
Stage 1 ──▶ the method ──▶ held-out test ──┐    Question 1 · T4 ─┐  Q1a guess → C1 ─┐  Figure 2
Stage 2   input ladder    the gate (T8)   └──▶ T5 ─────────────┘  Q1b guess → C2 ─┘
T1        registers (T2) ─▶ the new round ───▶ Question 2 · T10 … Q2a → C3 …          Figure 3
❗ red border + line: what the reviewers asked us to change    🛠 green: the work that fixes it
```


What it reads
-------------

| part of the map | read from, on every build |
|---|---|
| the question line | the telling's face `**The paper's question**:`, else its `**Topic:**` (board.md `story-current:`; an older Board's A1-Story Page's `## Opening`) |
| each question row: name, question, its Tasks, sub-questions, claims, contribution, work | the Board Questions in board.md `## Questions`, each report's `#### 3.N · Question N · RQN` block (else the face) |
| an analysis card: name, question, its folder, ran or not | the face's §7 T table and §6 D table; the Project's `work/` (or `tasks/`): a Task ran when a Run's `result/` (or an older `results/`) holds a real file; a drawn telling's short table (`\| T \| work \| where \| state \| starts \|`) says it in `state` (a new Run in a Task that ran before is not done) |
| a sub-question card's evidence state | the face's §5 E table; a claim resting on several hypotheses (`from 1a, 1b`) is drawn on the first and named beside the others |
| an analysis card's answer | the yaml's `numbers:` (keyed by T row: `{json, say}`, read like `count:`) |
| the foundation columns (data, sources, tests), their links, the displays | the topic's `<topic>-drawing.yaml` |
| a count on a foundation card | its `count:`, a JSON file on disk read now (never typed): a list counted (`list:`), or an object's values filling `say` (`{rows:,}`, nested keys joined by `_`) |
| the "in the paper" card of each question | the yaml's `figures:`, else the displays the Board's `s04-paper-workflow` face names for that question |
| the overlay | the newest version's comments reports (or `review:`), their `## Review Items` table's `hits` and `fixed by` |


The review overlay
------------------

A comments report's Review Items table (hai-paper-comments) may carry two more cells:

```text
| item | cites | lands on | hits | fixed by | work | reply | state | … |
| Review-more-shots | E1.2 · R3.1 | s02-… §7 T9 · t03_research-design · C3 | stage2 | goal · T9 · D1 | … |
```

1. **hits**: the part of the submitted study the point attacks: a foundation card's `key` (`stage2`, `agent`), a
   Task or Discovery id (`T1`), or `—`. The card gets a red border and one line, `❗ reviewers: <items>`.
2. **fixed by**: the work that answers it: a card `key`, a T or D id, a claim id (`C2`), a Question's landing
   (`Q1`, its paper card), or a Section stem (`t03_research-design`). Each card gets a green border and
   `🛠 fixes: <items>`.
3. **Writing fixes**: an item answered only by Section stems is listed under the map in green, with its Sections.
4. **Nothing fixes it**: an item with no `fixed by` is listed under the map in red, `❓ nothing fixes yet`.
5. **Labels**: an item's label is its name, `Review-more-shots` → "more shots".
6. **The legend**: a line under the question says what red and green mean and which report they came from.

The overlay decides nothing: the dispositions stay the person's, in the comments report.


The words
---------

`<topic>/<topic>-drawing.yaml`, beside the face:

```yaml
title: "The redesigned paper: from one finished experiment to the next"
sub: "…"                                  # grey, under the title
review: j02_v1007_mansci                  # optional: the version whose comments report draws the overlay
columns: {D: [TITLE, sub], S: […], T: […], A: […], C: […], F: […]}
foundation:                               # three columns of cards, top to bottom
  D:
  - {key: stage1, title: "…", lines: ["…"], gray: "…"}
  - {key: stage2, title: "…", gap: 20, down: true}             # down: an arrow from the card above
  - {key: T1, task: T1, line: "…", where: "…", state: ""}      # task: a §7 row, its folder and state read
  S:
  - {key: method, title: "How insights are made", tasks_of: 1} # a question's Tasks, from its report
  - key: ladder                                                # group: small cards in one dashed box
    group:
    - {key: goal, title: "Goal only", lines: ["…"], dashed: true,
       count: {json: "<path from the SPACE root>", list: designs, where: {job: j01},
               say: "{n} designs released {released}", none: "held"}}
  T:
  - {key: T9, task: T9, tasks_of: 2, down: true, dashed_arrow: true}
links:                                    # arrows between foundation cards
- {from: stage1, to: method, label: "Stage 1 only"}
- {from: stage2, to: heldout, dashed: true, route: under, label: "…"}    # under: below the columns first
feeds: {1: heldout, 2: T9}                # the test each question row stands on
figures: {1: "Figure 2 · Table 3 (proposed)"}
figures_state: "drawn by T15"
overview:                                 # the light version; {analysis} {questions} {subq} {claims} are filled
- [D, "THE FINISHED EXPERIMENT", "…", "…"]
notes: ["…"]
```


Steps
-----

```bash
W=Tools/plugins/haipipe-toolkit/skills/1_base/draw/hai-draw/gallery/workflow/scripts/workflow_drawing.py
python $W make <topic folder> [--force]     # the forwarding builder, and a words yaml from a template if none
#   write <topic>-drawing.yaml; fill hits and fixed by in the version's Review Items
python <topic folder>/build_sNN_<topic>.py   # redraw and its .png
```

`make --force` replaces a topic's own builder: keep the old one in the topic's `history/` first. Then the reader
review (hai-studio `ref/reader-review.md`) asks these four questions, from the picture alone:

1. What goes in, what is built from it, and what tests it?
2. For each question: which analyses answer it, what is guessed, and what would the paper claim?
3. Which parts did the reviewers attack, and which work answers each point?
4. What is answered only in the writing, and what has no answer yet?


Worked example
--------------

`〈Client-SPACE〉` `examples-4-learning/Project-ExpLearn-SMSDesign/paper/Paper-TestToLearn-MS2026/s04-paper-workflow/`:
the Management Science redesign, 2 questions and 4 sub-questions, the input ladder's Stage 2.5 designs counted from the
Design Board, and the 20 Review Items of `j02_v1007_mansci/reports/q01_editor-decision-0916/` (19 on cards; scope is
fixed in the writing).


The paper flow (s04-paper-workflow)
-----------------------------------

`scripts/paperflow_drawing.py` draws the other half of a paper's plan (hai-paper-plan), the way hai-draw story
draws s02 (principles ①, ③).

```text
① 📝 the paper as it reads (main): the budget and the send date as its key, then each Section a step lower and
   further right: its research questions (names read from the telling), its words, its displays; red and dashed
   when every evidence row it names is absent; "❗ RQn has no section" when a question lands nowhere
      ② what each Section must do            ③ the displays as stairs: what each shows, the Run that makes it
   ④ from here to the send (below): each step with its date and who; a person's step marked 🙋
```

It reads the face's `**Budget:**` and `**Send:**` lines and its three tables (`| S | section | answers | job |
displays | evidence | words |`, `| Display | title | kind | answers | made by | state |`, `| W | step | when | who |
state |`), and from the telling (board.md `story-current:`) each question's name and the E table's support states.
`paperflow_drawing.py make <topic>` writes the forwarding builder; templates are hai-paper-plan's `ref/faces.md`.

`scripts/displayplan_drawing.py` draws the third plan topic, `s06-paper-displays` (hai-paper-plan): ① the
displays in the paper's order as steps (`Figure 1 (Display A)`, its type and name, what it shows, the question, the
Section, main or supplement, the Run), ② the venue's display rules from `venues/<venue>/call.md`, ③ hai-paper-plan's `display_plan.check` line by
line. A display no Run makes yet, or one that breaks a rule, is red and dashed. `displayplan_drawing.py make <topic>`
writes the forwarding builder; when s06 exists, `paperflow_drawing.py` takes s04's displays from it.


Boundary
--------

This kind draws the map; it decides nothing. What a telling says is `hai-paper-story`'s; a comments batch, its
Review Items and their dispositions are `hai-paper-comments`'; a paper's Sections, paragraphs and evidence cards
are `hai-draw draft`; an ideation is `hai-draw ideation`; a Job is `hai-draw job`; how any drawing
looks is hai-draw SKILL.md's; the topic folder, face and sessions are `hai-studio`'s. The map keeps its own
column layout, so it is drawn with its own canvas helpers and written through hai-studio's `canvas.write`, not
laid out by `draw.py`'s frames.
