---
name: haipipe-question
description: >-
  Owns what a board Question is and how it is recorded: a topic that many sections,
  sessions and Runs feed and that grows into its report; its size (a topic, not a
  decision); its folder `<board>/reports/qNN_<topic>/` beside `studio/`; its entry in
  the board's question register; and the open report frame it starts. The report itself
  (answer-status, Answer · Evidence · Limits · Next, figures, check) is haipipe-report's.
  Use to propose, create, size, rename
  or find a board Question, to turn a proposed Related question into a folder, or to
  read which questions a board has. Trigger: question, board question, block question,
  reports folder, qNN, add a question, propose a question, question granularity,
  /haipipe-question.
allowed-tools: Bash, Read, Write, Edit, Grep, Glob
metadata:
  version: "0.6.0"
  last_updated: "2026-10-07"
  # version history: ./CHANGELOG.md
---

# /haipipe-question · a board's questions and their reports

A board's `reports/` folder is its list of questions: each `qNN_<topic>/` holds one
Question and the report that answers it (JL 261003: "reports is a list of questions").
Every board kind uses the same shape: a Task Block (`tasks/bNN_<block>/`), a Paper board
(`papers/Paper-<Name>/`) and a skill Block (`Tools/blueprints/bNN_<block>/`).

```text
<board>/
├── board.md                    the question register (Questions, Related resources)
├── studio/                     drawings the whole Block shares (the question map)
└── reports/
    └── q01_<topic>/
        ├── q01_<topic>.md      the report Page: Opening, then Answer · Evidence · Limits · Next
        ├── page.toml           registers the Page with the Page reader
        └── studio/             this report's own drawings (the rule below)
```

One Question, one drawing (JL 261005: "for each question we should just have one
excalidraw"). A report has exactly one `.excalidraw`, linked once from its `### Evidence`:
more views are frames inside it, and a screenshot or figure the report cites is an image
inside it too ("some png can be put into the excalidraw as well"), never a second link
(`excalidraw-report` rules 6, 9 and 11). It lives in the report's folder (JL 261004), as
`reports/qNN_<topic>/studio/<name>.excalidraw` or, drawn by a Block builder, as
`reports/qNN_<topic>/qNN_<topic>.excalidraw` beside the Page; its build script, when a script
draws it, sits in that `studio/_build/` or the Block's. The Block's `studio/` keeps only the
drawings the whole Block shares: the question map, the road map, and any drawing several
Questions or Jobs use. `--drawing <name>` (once) makes the blank drawing in the report's
`studio/` and lists it under `### Evidence`. The workbenches show the first drawing a report
links (else its own, unlinked); a second drawing or a linked picture is a finding in Check.


A question is a topic
---------------------

A board Question is a topic that many sections, sessions and Runs feed, and that grows
into its report over time (JL 261003: "it is a topic question … eventually it can
develop the report"). A narrow decision is one of the things its report records, not a
question of its own.

```text
✅ topic                                   ❌ decision
"How are questions recorded and answered?" "Should a reply link its board question?"
"How are records cut into cases?"          "Why do empty days make empty cases?"
"Which model should ship?"                 "Is fold 3's AUC above 0.80?"
```

1. **The report test**: could it fill a report's Answer, Evidence, Limits and Next?
2. **The reuse test**: would the next few sections or Runs on this work feed it too?
3. **Too narrow**: one section or one yes/no answers it; lift it a level.
4. **Too broad**: it is the board's whole spine; name the part this work is on.
5. **Reuse first**: read `<board>/reports/` and the register before proposing one.


A topic holds asks
------------------

A question has two sizes (JL 261003). A **topic** is a board Question: it grows into
its report and is recorded here. An **ask** is one thing one piece of work answers: an
Insight question file, a Task's Run request, a paper's sub-question. A topic holds
several asks, and its report gathers their answers.

```text
topic   "What drives no-shows?"                     reports/q01_no_shows/  (this skill)
  ├─ ask   no-show rate by weekday                  its page or Run
  ├─ ask   do reminders cut no-shows?               its page or Run
  └─ ask   which clinics get reminders?             its page, signed
```

The report test above sizes a topic. An ask is shaped by `haipipe-question-asking` and
judged by `haipipe-question-review` (Q1 "one thing" is a test of an ask, not of a topic).


Propose, then create
--------------------

A question is first **proposed**: a chat reply names it as
`(proposed) <Board> "<short question>"` (`response-format`'s Related question line) and
offers its folder, `<board>/reports/qNN_<topic>/`, with the board's next free NN and a
short snake_case topic. It is **created** only when the person agrees; a proposal writes
nothing.

To create one:

1. **Pick the id**: the next free `QNN` in the register, or `Q-<word>-<number>` when the
   register is cut by a word such as an event type (`Q-food-1`, `Q-exercise-2`; JL 261004);
   ids never move or get reused.
2. **Name the folder**: the id in lower case, then the topic in two or three snake_case
   words: `q07_<topic>` or `q-food-1_<topic>`.
3. **Register it**: add the entry to `board.md`'s `## Questions` register.
4. **Frame the report**: the same-stem `.md` with `answers:` and `answer-status: open`, and `page.toml`.
5. **Hand it on**: from here the report is `haipipe-report`'s (the walk, the Page, its figures).

On a Task Block the helper does steps 1 to 4 in one command (it refuses a duplicate id,
an existing folder and a work path that is not a Task):

```bash
python Tools/plugins/haipipe-toolkit/skills/1_base/question/haipipe-question/ref/block_questions.py \
  add-question <block> --id Q02 --slug <topic> --title '<short question>' \
  --question '<the question>' [--hypothesis …] [--acceptance …] [--work jNN_<job>/tNN_<task>]

# a report for a Question already in the register (steps 2 and 4, and its report: line)
python …/block_questions.py add-report <block> --id Q-food-1 --slug input_forms \
  [--title '<title>'] [--evidence '<label>|<path in the Block>'] [--drawing api_food]
```

`--evidence 'label|path'` (either command, repeatable) lists a file inside the Block under
the frame's `### Evidence`: a Task Result, a source Page, or a drawing, which the workbench
then shows in the Report column. `--drawing <name>` (once per Question) makes the report's one
drawing in `reports/<id>_topic/studio/` and lists it the same way. It is a pointer for the writer, not an
answer; `answer-status` stays `open` and no `results-read:` is written until someone reads it.

A Paper board has no register block yet: its questions are the Story's research
questions (`RQ<n>`), and a report names them in `answers:`
(`haipipe-paper/ref/paper-ladder.md`). Create its folder and Page frame by hand,
with the same header lines.

The register's full contract is `ref/block-questions.md`. The report's (header lines,
Content divisions, freshness against `results-read:`, the walk, figures, the check, the
word "report" routed between Task and Page) is `haipipe-report`'s `ref/report-contract.md`.


Find a board's questions
------------------------

```bash
ls <board>/reports/                                   # one folder per question
sed -n '/^## Questions/,/^## /p' <board>/board.md     # the register: id, title, question, work
grep -h '^answer-status:' <board>/reports/*/q*.md     # where each one stands
```


Boundary
--------

This skill owns the asking: what a Question is, its size, its id, folder and register
entry, and the open report frame. The report (its header lines, Content divisions, the walk
open → partial → answered, its figures and check, how work links by `answers:`) belongs to
`haipipe-report` (b03 s21, 261007). Writing the report's text belongs to `haipipe-page`
(the report is an ordinary Page). The Task work a question cites
belongs to `haipipe-task`. The screens that show questions belong to
`workbench-work` and `workbench-paper`. Matching a chat's questions to
recorded ones belongs to `ask-questions`; how a reply shows its Related question belongs
to `response-format`. Shaping an ask is `haipipe-question-asking`; judging it is
`haipipe-question-review`. Insight's question files (its asks at Data, Information,
Knowledge and Wisdom) are Insight's own and stay with `haipipe-insight`.
