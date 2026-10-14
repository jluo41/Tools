---
name: excalidraw-workflow
description: >-
  A study's workflow drawn as one building map, read left to right: the finished data, its sources or inputs, the
  tests, the analysis each sub-question needs, the sub-question with its guess and claim, and where the answer lands
  in the paper; a light version on top, one row per sub-question below. With a version's comments report it carries
  the review overlay: a red border and ❗ line on what the reviewers asked to change, a green border and 🛠 line on the
  work that fixes it, read from each Review Item's hits and fixed by cells. Words in the topic's
  <topic>-drawing.yaml; the topic's builder forwards to scripts/workflow_drawing.py; everything else (the telling,
  the Board Questions' reports, the Task folders, the Review Items) is read on every build. haipipe-paper-story calls
  it for a paper's workflow topic whenever it is installed. Use to draw or redraw a paper's workflow, to see what
  the reviewers hit and what answers each point, or to give a new paper the same building map. Trigger: draw the
  paper workflow, building map, workflow drawing, paper structure map, what did the reviewers hit, review overlay,
  /excalidraw-workflow.
allowed-tools: Bash, Read, Edit, Write, Grep, Glob
metadata:
  version: "0.1.0"
  last_updated: "2026-10-14"
  # version history: ./CHANGELOG.md
---

# /excalidraw-workflow · a paper's building map, with what the reviewers hit

Asked 261014 on DrFirst-SPACE's Paper-TestToLearn-MS2026, after Management Science's decision: "for the s04, could you
highlight that which part the reviewers wanted us to change, and how will our new field experiment and analsysis will
fix it?"; "we should keep the current structure, it will serverd as the building map"; "How do you think we can add it
to the themes/paper skills set"; "or call it /excalidraw-workflow, saying how do we want to make the paper workflow".

The map was a script each paper copied (haipipe-paper-story: "copy an existing builder and change only its SPEC");
five copies had drifted apart and all still read the retired `A1-Story/` Page. This skill is that script once, with
the review overlay added, so every paper draws its building map the same way.

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
| the question line | the telling's face `**Topic:**` (board.md `story-current:`; an older Board's A1-Story Page's `## Opening`) |
| each question row: name, question, its Tasks, sub-questions, claims, contribution, work | the Board Questions in board.md `## Questions`, each report's `#### 3.N · Question N · RQN` block (else the face) |
| an analysis card: name, question, its folder, ran or not | the face's §7 T table and §6 D table; the Project's `work/` (or `tasks/`): a Task ran when a Run's `result/` (or an older `results/`) holds a real file |
| a sub-question card's evidence state | the face's §5 E table |
| the foundation columns (data, sources, tests), their links, the displays | the topic's `<topic>-drawing.yaml` |
| a count on a foundation card | its `count:`, a JSON file on disk counted now (never typed) |
| the overlay | the newest version's comments reports (or `review:`), their `## Review Items` table's `hits` and `fixed by` |


The review overlay
------------------

A comments report's Review Items table (haipipe-paper-comments) may carry two more cells:

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
W=Tools/plugins/haipipe-toolkit/skills/1_base/display/excalidraw-workflow/scripts/workflow_drawing.py
python $W make <topic folder> [--force]     # the forwarding builder, and a words yaml from a template if none
#   write <topic>-drawing.yaml; fill hits and fixed by in the version's Review Items
python <topic folder>/build_sNN_<topic>.py   # redraw; a person's marks are kept (canvas.write)
python Tools/plugins/haipipe-toolkit/skills/1_base/project/haipipe-studio/scripts/render_png.py <x>.excalidraw <x>.png
```

`make --force` replaces a topic's own builder: keep the old one in the topic's `history/` first. Then read the
picture as a reader, with these questions, answered from the picture alone:

1. What goes in, what is built from it, and what tests it?
2. For each question: which analyses answer it, what is guessed, and what would the paper claim?
3. Which parts did the reviewers attack, and which work answers each point?
4. What is answered only in the writing, and what has no answer yet?


Worked example
--------------

DrFirst-SPACE `examples-4-learning/Project-ExpLearn-SMSDesign/paper/Paper-TestToLearn-MS2026/studio/s04-paper-workflow/`:
the Management Science redesign, 2 questions and 4 sub-questions, the input ladder's Stage 2.5 designs counted from the
Design Board, and the 20 Review Items of `j02_v1007_mansci/reports/q01_editor-decision-0916/` (19 on cards; scope is
fixed in the writing).

Older copies of the same map, not yet moved to this skill (each still reads `A1-Story/`): DrFirst-SPACE
Paper-MessageTradeOffEgm, Paper-RxSavingsNudge and Paper-LLMSocialOutcome-PNAS2026; WellDoc-SPACE
Paper-TimeEventDM-ISR2026.


Boundary
--------

This skill draws the map; it decides nothing. What a telling says is `haipipe-paper-story`'s; a comments batch, its
Review Items and their dispositions are `haipipe-paper-comments`'; a paper's Sections, paragraphs and evidence cards
are `excalidraw-section`; an ideation is `excalidraw-ideation`; a Job is `excalidraw-job`; how any topic's drawing
looks is `excalidraw-studio`'s; the topic folder, face and sessions are `haipipe-studio`'s. The map keeps its own
column layout (agreed as the building map, 261014), so it is drawn with its own canvas helpers and written through
haipipe-studio's `canvas.write`, not laid out by `draw.py`'s frames.
