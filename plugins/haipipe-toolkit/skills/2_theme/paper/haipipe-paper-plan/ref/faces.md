# The two plan faces, as templates

Copy, then replace every `<…>`. Placeholders only; the worked example is named in `../SKILL.md`.


## s03-paper-dataflow

`studio/s03-paper-dataflow/s03-paper-dataflow.md`:

````markdown
s03 · Paper dataflow: how the data becomes each answer
======================================================

**Tags:** `Plan`

**Stage:** explore

**Topic:** how the paper's data becomes the answer to each of its <n> research questions: <the inputs, in one
sentence>; <what the pipeline matches and tables>; then each question waits on the Runs its story names (s02 §7).
Drawn by excalidraw-workflow from `s03-paper-dataflow-drawing.yaml` and the story; the displays come from
`s04-paper-workflow`.

**Feeds:** `s04-paper-workflow` (the Run behind each display) and the tickets of the Runs still to make.

**Pipeline:** `work/<bNN_block>/` (and any other Block) <what each Job does, in order>; `runs/<run-pipeline-…>/` reruns
it, or "no pipeline Run yet". <who> presses Run.


Files
-----

```text
s03-paper-dataflow/
├── s03-paper-dataflow.md              this face
├── s03-paper-dataflow-drawing.yaml    the building map's words: the foundation cards and their numbers' files
├── s03-paper-dataflow.excalidraw      the building map
├── s03-paper-dataflow.png             its preview
└── build_s03_paper_dataflow.py        forwards to excalidraw-workflow's workflow_drawing.py
```


Decided
-------

(none yet: s03-D01 · <a decision made while planning the flow, not one the story records> (<who> <date>); an
agent's decision reads "(proposed by <agent> <date>)" until a person agrees it)


Open
----

1. <the first open point>
````

`s03-paper-dataflow-drawing.yaml`: the foundation only; every question row is read from the story.

```yaml
title: "<the paper>'s data flow: from <the data> to <n> answers"
sub: "solid = a Run's result is on disk · dashed = not run yet · every number read from its Result on each build"
columns:
  D: ["THE DATA", "what every question reads"]
  S: ["THE MATCHING", "<how the inputs are linked>"]
  T: ["THE TABLES", "<the tables every question stands on>"]
  A: ["ANALYSIS", "the Runs each question waits on (s02 §7)"]
  C: ["HYPOTHESIS → CLAIM", "the guess, and what the paper would say"]
  F: ["IN THE PAPER", "the displays, from s04-paper-workflow"]
foundation:
  D:
  - key: <input>
    title: "<an input>"
    lines: ["<what it holds>", "<bNN.jNN> · <where>"]
    count: {json: "<path from the SPACE root to a Result's metrics.json>", say: "{<key>:,} <unit>"}   # nested keys joined by _
  S:
  - {key: <link>, title: "<a matching step>", lines: ["<bNN.jNN.tNN>"]}
  T:
  - {key: <table>, title: "<a table>", lines: ["<bNN.jNN.tNN>"], down: true}
links:
- {from: <input>, to: <link>}
feeds: {1: <table>, 2: <table>}            # the table each question's row stands on
numbers:                                    # an analysis card's answer, read from its Result (optional)
  T5: {json: "<a Result's metrics.json>", say: "<words with {<key>:.2f}>"}
figures_state: "made by a figure Run inside its Job"
overview:
- [D, "THE DATA", "<inputs>", "<Blocks>"]
- [S, "THE MATCHING", "<what>", "<Job>"]
- [T, "THE TABLES", "<what>", "<Job>"]
- [A, "ANALYSIS", "{analysis}", "<Job>"]
- [C, "HYPOTHESIS → CLAIM", "{questions} questions · {subq} hypotheses", "{claims}"]
- [F, "IN THE PAPER", "the displays, from s04", "figure Runs in each Job"]
notes: []
```


## s04-paper-workflow

`studio/s04-paper-workflow/s04-paper-workflow.md`:

````markdown
s04 · Paper workflow: <a <words>-word <kind> in <n> sections, <n> displays, sent by <date>>
==========================================================================================

**Tags:** `Plan`

**Stage:** explore

**Topic:** how the paper's answers become the paper: the Sections in reader order, the question each answers, its
words and displays; each display and the Run that makes it; the steps to the send. The questions and evidence rows
are read from the story, never copied here. When the first version is made, its `## Narrative` is seeded from the
Sections table.

**Feeds:** the first version's `## Narrative` (`j01_v<MMDD>_<desk>`), and `s03-paper-dataflow`'s "in the paper" column.

**Budget:** <desk, article type>: <words> words of text, <abstract>, up to <n> tables or figures (desk record <QBv…>,
or "own estimate: no desk record").

**Send:** <YYYY-MM-DD> (proposed <date> | agreed by <person> <date>).


Files
-----

```text
s04-paper-workflow/
├── s04-paper-workflow.md            this face: the Sections, the displays, the timeline
├── s04-paper-workflow.excalidraw    the paper as it reads, its displays, the steps to the send
├── s04-paper-workflow.png           its preview
└── build_s04_paper_workflow.py      forwards to excalidraw-workflow's paperflow_drawing.py
```


### 1 · Sections

| S | section | answers | job | displays | evidence | words |
|---|---|---|---|---|---|---|
| S0 | Abstract | RQ1, RQ2 | <one plain sentence: what it must establish> | — | <E rows> | <n> (outside the count) |
| S1 | Introduction | — | <…> | — | <D rows> | <n> |
| S3 | Results: <the question, short> | RQ1 | <…> | Figure 1 | E<n> to E<m> | <n> |


### 2 · Displays

| Display | title | kind | answers | made by | state |
|---|---|---|---|---|---|
| Figure 1 | <what it shows> | figure | RQ1 | <bNN.jNN.tNN.rNN, or a new figure Run after T<n>> | not started |

A Run that makes two displays is named on both rows. `answers` lists the questions in the story's order; when the
venue leads with another, the `job` sentence says which leads.


### 3 · Timeline

| W | step | when | who | state |
|---|---|---|---|---|
| W1 | G0: mark the story | <MM-DD> | <person> marks | not started |
| W<n> | Send to <desk> | <MM-DD> | <person> sends | not started |

A person's step names who and the verb (marks, presses, reads, signs, sends, agrees, approves, decides, starts).


Decided
-------

(none yet)


Open
----

1. <the first open point>
````
