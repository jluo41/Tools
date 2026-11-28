---
name: hai-report
description: "Owns a Block's Questions and their reports at any level: where a Question lives, shaping and reviewing asks, linking work to it (answers:), and the report Page. Use to propose, review or answer a question. Trigger: report, answer a question, qNN, /hai-report, /hai-question."
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "0.3.2"
  last_updated: "2026-10-26"
  # version history: ./CHANGELOG.md
---

# /hai-report · a Question, the work on it, and what it says

**No new `reports/` anywhere since 261110 (JL: "we will no longer use the reports/, please use
the job or studio"; CoWork first, 261109).** A Question's answer lives in the Studio topic that
answers it, as a `Q01 · Answer` part of its face (`hai-studio` `ref/topic-contract.md`); the
face's `report:` points at that topic. Work done in answer (a review round, a feedback pass) is a
Job, `jNN_review_<kind>_v<MMDD>/` with `for: <the Job it serves>` (`hai-job`). No level keeps
a `reports/` folder. The `reports/qNN_<topic>/` Page below describes older folders, still read
until they move.

A Report keeps its Page source at its owning level. Its delivered formats go to
its containing Block's `delivery/<report-source-path>/<lane>/`; for a Block
Report this is `delivery/reports/qNN_<topic>/<lane>/`. Report ownership and
answer status do not change when storage moves. Use the shared Delivery path
helper (owner: `hai-delivery`); no Job, Task or Report owns another physical `delivery/` directory.


A level's Audience Report is one row per Question: the Question on the left, the Work that
answers it in the middle, the Report on the right (JL 261007: "to define the question -
work - report workflow in the Audience report"). This skill owns that row from the
Question's status rightwards, and the asking before it (§ Questions below; folded in from
`hai-question` on 2026-10-16).

```text
Question                 Work                              Report
register row · status    Jobs, Tasks whose face says       the answering topic's face: Q01 · Answer
studio topics feeding    answers: <id> (or <id>.E<n>)      (an older Block: reports/qNN_<topic>/ Page)
  │                        │                                 │
hai-report § Questions   theme work skills                 hai-report
```

Read `ref/report-contract.md` before writing, linking or checking a report: the row, the
link rule, the walk, the Page, report kinds, figures, the check and the buttons.



Questions: what one is, and how it is recorded
----------------------------------------------

(Folded in from the retired `hai-question`, 2026-10-16: "no need for the question anymore".)

A board's `## Questions` register is its list of questions. In an older Block each `reports/qNN_<topic>/` holds one
Question and the report that answers it (JL 261003: "reports is a list of questions").
Every board kind uses the same shape: a Task Block (`work/bNN_<block>/`), a Paper board
(`paper/Paper-<Name>/`) and a skill Block (`Tools/examples/bNN_<block>/`).

```text
<board>/
├── board.md                    the question register (Questions, Related resources)
├── s01-<name>/                 a Block Studio topic: its face Feeds: the Question and holds its `Q01 · Answer`
└── reports/                    an older Block only
    └── q01_<topic>/
        ├── q01_<topic>.md      the report Page: Opening, then Answer · Evidence · Limits · Next
        └── page.toml           registers the Page with the Page reader
```

1. **One drawing**: a report has exactly one `.excalidraw`, linked once from its `### Evidence`; more views are frames inside it (`hai-draw report` rules 6, 9, 11). `--drawing <name>` makes it as a Block sNN that feeds the report.
2. **A topic, not a decision**: a Question is a topic many sections, sessions and Runs feed, that grows into its report (JL 261003). A narrow decision is something its report records.
3. **The report test**: could it fill a report's Answer, Evidence, Limits and Next?
4. **The reuse test**: would the next few sections or Runs on this work feed it too?
5. **Too narrow or too broad**: one yes/no answers it, lift it; it is the board's whole spine, name the part. Read the register (and an older Block's `reports/`) before proposing one.

```text
✅ topic                                   ❌ decision
"How are records cut into cases?"          "Why do empty days make empty cases?"
"Which model should ship?"                 "Is fold 3's AUC above 0.80?"
```

A topic holds **asks**: an ask is one thing one piece of work answers (an Insight question
file, a Task's Run request, a paper's sub-question). The report test sizes a topic; an ask
is shaped by `ref/asking.md` and judged by `ref/review.md` (Q1 "one thing" tests an ask).

Propose, then create. A question is first **proposed**: a chat reply names it as
`(proposed) <Board> "<short question>"` and offers its register id, the board's next free `QNN`,
with the Studio topic that will answer it. It is **created** only when the person agrees. To create one:

1. **Pick the id**: the next free `QNN` in the register, or `Q-<word>-<number>` when the register is cut by a word (`Q-food-1`); ids never move or get reused.
2. **Name its slug**: the id in lower case, then two or three snake_case words: `q07_<topic>` (an older Block's report folder took this name).
3. **Register it**: add the entry to `board.md`'s `## Questions` register; its `group:` line (comma-separated) puts its card on the Report's group bar.
4. **Name where the answer goes**: the register's `report:` points at the face of the Studio topic that answers it, which gets a `Q01 · Answer` part (an older Block: a same-stem report `.md` with `answers:` and `answer-status: open`, and `page.toml`).
5. **Hand it on**: from here the report is the walk below.

On a Task Block the helper does steps 1 to 4 (it refuses a duplicate id, an existing folder and a work path that is not a Task):

```bash
B=Tools/plugins/haipipe-toolkit/skills/1_base/project/hai-report/ref/block_questions.py
python $B add-question <block> --id Q02 --slug <topic> --title '<short question>' \
  --question '<the question>' [--group '<Group>'] [--hypothesis …] [--acceptance …] [--work jNN_<job>/tNN_<task>]
python $B set-group <block> --id Q-food-1 --group 'Food, All events'     # only the group: line changes
python $B add-report <block> --id Q-food-1 --slug input_forms \
  [--title '<title>'] [--evidence '<label>|<path in the Block>'] [--drawing api_food]
```

`--evidence 'label|path'` (repeatable) lists a file inside the Block under `### Evidence`;
`--drawing <name>` (once) makes the report's one drawing as a Block Studio topic, `sNN-<name>/` beside the
Jobs, whose face **Feeds:** the report (hai-studio `new_topic.py`; no `studio/` folder, JL 261031 b35 r02).
It is a pointer for the writer, not an answer: `answer-status` stays `open`, no
`results-read:` is written. A Paper board has no register block: its questions are the
Story's `RQ<n>`, and a report names them in `answers:`; make its folder and frame by hand.
The register's full contract is `ref/block-questions.md`.

Find a board's questions:

```bash
ls <board>/reports/                                   # an older Block only: one folder per question
sed -n '/^## Questions/,/^## /p' <board>/board.md     # the register
grep -h '^answer-status:' <board>/reports/*/q*.md     # where each one stands
```

Ask or review (`/hai-report ask <folder>`, `/hai-report review <folder>`): load
`ref/asking.md` to shape one ask before any work (eight method cards in `ref/asking-methods/`,
it returns the ask, the method and what it refused), or `ref/review.md` to judge it by
seven tests Q1-Q7 (keep, split, merge or move; it proposes, a person signs). Matching a
chat's questions to recorded ones is `ask-questions` (`0_utils`); Insight's own question
files stay with `hai-insight`.


The walk
--------

```text
open  ─▶  partial  ─▶  answered
```

1. **open**: asked, no answer yet; the report frame § Questions makes.
2. **partial**: some Work answers part of it; the report says which part.
3. **answered**: the Opening states the answer; Evidence links the exact Results or Pages.
4. **Who moves it**: the report's writer, never the frame and never a Run finishing alone.
5. **Checked**: not a fourth state; the Page's CHECK verdict is shown beside answered (decided 261007).

`results-read:` records when the evidence was read; evidence newer than it is flagged.


The link rule
-------------

Work names the Question it answers, on its own face, so the link lives with the work:

```text
jNN_<job>/jNN_<job>.md          answers: Q01
jNN_<job>/tNN_<task>/tNN_<task>.md   answers: Q01.E2, Q04
```

`<id>.E<n>` is one need (Evidence Item) of a Question and counts for it. The register's
`work:` list still links work whose face cannot say it. An id the level's register does not
have is an error.


The report Page
---------------

In an older Block, an ordinary `hai-draft` Page in `reports/qNN_<topic>/`, with three header lines
(`answers:`, `answer-status:`, `results-read:`), an Opening that states the answer, and the
Content divisions **Answer · Evidence · Limits · Next**. Write it through the Page flow
(load `hai-draft`); never type final prose into generated Content. A comments batch is a
report of type comments: `reports/qNN_<kind>-<MMDD>/`, `page-type: comments`, a register row
in `group: comments`.


Figures and the check
---------------------

```bash
S=Tools/plugins/haipipe-toolkit/skills/1_base/project/hai-report/scripts
python $S/build_report_drawing.py <level>/reports/qNN_<topic>/     # an older Block: the drawing, from ## Figures
python $S/check_report.py <level folder>                           # the rows, and what is wrong
```

1. **One drawing**: built from the studio frames the report's `## Figures` lists; never by hand.
2. **Preview**: `hai-studio`'s `scripts/render_png.py <drawing> <png>`.
3. **Check**: mechanical (states, links, Evidence, freshness); exit 1 on an error.
4. **Judgement**: the Page's CHECK, in a fresh context (`hai-draft-check-agent`).


Infer the reports from the work
-------------------------------

A Block with Jobs and Tasks but no Questions gets them from what its work answers, at each level (JL 261012:
"I don't ask the questions that is meaningless ... ask the questions that are closely related to the jobs and
tasks"; b10 s10). Read it with `hai-studio`'s `scripts/block_inventory.py <block>`; the rules and a worked
example are `ref/infer-reports.md`.

1. **Task**: its own sub-questions; its report is its face, nothing new registered.
2. **Job**: what its one Task of a kind answers for it, when the Jobs differ (b00: ready for Source?).
3. **Block**: where the Jobs' answers differ, and what that means next (b00: 3 drops blocked; 60 tables with
   no event time).
4. **Kept only if** named Tasks answer it and they do not all answer it the same way; the theme's kinds only
   group it. § Questions then makes the row.


The buttons it owns
-------------------

| Button | Run | does |
|---|---|---|
| Write the report | `run-report-<qNN>` | the Page flow; moves the walk |
| Rebuild report drawing | `run-figures-<qNN>` | `build_report_drawing.py`, then the preview |
| Check a report | `run-check-<qNN>` | `check_report.py`, then the Page's CHECK |

Soft Runs in the level's `runs/`, one per target, a pass per round (`hai-run`).
Ask a Question (`run-ask-<qNN>`) is § Questions below.


Boundary
--------

| Owner | Owns |
|---|---|
| `hai-report` | the asking (§ Questions): a Question's size, id, register row, folder, the open frame; the row's Work link and Report cell, the walk, the report Page's header and divisions, figures, check |
| `hai-draft` | writing the report's prose, its Draft, evidence binding, CHECK and release |
| `hai-draw report` | the drawing kit: scratch and report modes, plot kit, pictures |
| `hai-studio` | the studio topics a Question's row lists as feeding it |
| theme workbenches | the screens: `servers/workbench/page/block_index_page/frame.py` `question_rows`, and each theme's own row |


Files
-----

```text
hai-report/
├── SKILL.md
├── CHANGELOG.md
├── agents/openai.yaml
├── ref/report-contract.md        the full contract
├── ref/block-questions.md        the question register's contract (moved from hai-question)
├── ref/block_questions.py        add-question, add-report, set-group helper
├── ref/asking.md                 shape an ask before any work; ref/asking-methods/ holds its 8 cards
├── ref/review.md                 the seven tests Q1-Q7 and the verdict
├── ref/infer-reports.md          Questions and reports inferred from a Block's Jobs and Tasks (b10 s10)
├── scripts/build_report_drawing.py   the report drawing from ## Figures (moved from hai-draw report)
├── scripts/check_report.py       the row reader and mechanical check
└── tests/test_haipipe_report.py
```
