---
name: haipipe-report
description: >-
  Owns the Question │ Work │ Report workflow of the Audience Report at any level (Block,
  Job, Task): what each cell of the row reads, how work links to a Question (`answers: <id>`
  or a need `<id>.E<n>` on a Job or Task face), the walk open → partial → answered, the
  report Page (Opening · Answer · Evidence · Limits · Next) and its header lines, its
  `## Figures` and generated drawing, report kinds (a comments batch), and the report check.
  Use to write, rebuild, check or read a Question's report, to link work to a Question, or
  to say where a Question stands. Trigger: report, write the report, answer a question,
  answer-status, answers:, Question Work Report, Audience Report, report drawing, ## Figures,
  rebuild report drawing, check a report, comments batch, /haipipe-report.
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
metadata:
  version: "0.1.1"
  last_updated: "2026-10-07"
  # version history: ./CHANGELOG.md
---

# /haipipe-report · a Question, the work on it, and what it says

A level's Audience Report is one row per Question: the Question on the left, the Work that
answers it in the middle, the Report on the right (JL 261007: "to define the question -
work - report workflow in the Audience report"). This skill owns that row from the
Question's status rightwards; asking the Question is `haipipe-question`.

```text
Question                 Work                              Report
register row · status    Jobs, Tasks whose face says       reports/qNN_<topic>/qNN_<topic>.md
studio topics feeding    answers: <id> (or <id>.E<n>)      Opening · drawing · answer-status
  │                        │                                 │
haipipe-question         theme work skills                 haipipe-report
```

Read `ref/report-contract.md` before writing, linking or checking a report: the row, the
link rule, the walk, the Page, report kinds, figures, the check and the buttons.


The walk
--------

```text
open  ─▶  partial  ─▶  answered
```

1. **open**: asked, no answer yet; the report frame `haipipe-question` makes.
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

An ordinary `haipipe-page` Page in `reports/qNN_<topic>/`, with three header lines
(`answers:`, `answer-status:`, `results-read:`), an Opening that states the answer, and the
Content divisions **Answer · Evidence · Limits · Next**. Write it through the Page flow
(load `haipipe-page`); never type final prose into generated Content. A comments batch is a
report of type comments: `reports/qNN_<kind>-<MMDD>/`, `page-type: comments`, a register row
in `group: comments`.


Figures and the check
---------------------

```bash
S=Tools/plugins/haipipe-toolkit/skills/1_base/project/haipipe-report/scripts
python $S/build_report_drawing.py <level>/reports/qNN_<topic>/     # the drawing, from ## Figures
python $S/check_report.py <level folder>                           # the rows, and what is wrong
```

1. **One drawing**: built from the studio frames the report's `## Figures` lists; never by hand.
2. **Preview**: `haipipe-studio`'s `scripts/render_png.py <drawing> <png>`.
3. **Check**: mechanical (states, links, Evidence, freshness); exit 1 on an error.
4. **Judgement**: the Page's CHECK, in a fresh context (`haipipe-page-check-agent`).


The buttons it owns
-------------------

| Button | Run | does |
|---|---|---|
| Write the report | `run-report-<qNN>` | the Page flow; moves the walk |
| Rebuild report drawing | `run-figures-<qNN>` | `build_report_drawing.py`, then the preview |
| Check a report | `run-check-<qNN>` | `check_report.py`, then the Page's CHECK |

Soft Runs in the level's `runs/`, one per target, a pass per round (`haipipe-run`).
Ask a Question (`run-ask-<qNN>`) is `haipipe-question`'s.


Boundary
--------

| Owner | Owns |
|---|---|
| `haipipe-question` | the asking: a Question's size, id, register row, folder, the open frame |
| `haipipe-report` | the row's Work link and Report cell, the walk, the report Page's header and divisions, figures, check |
| `haipipe-page` | writing the report's prose, its Draft, evidence binding, CHECK and release |
| `excalidraw-report` | the drawing kit: scratch and report modes, plot kit, pictures |
| `haipipe-studio` | the studio topics a Question's row lists as feeding it |
| theme workbenches | the screens: `servers/workbench/frame.py` `question_rows`, and each theme's own row |


Files
-----

```text
haipipe-report/
├── SKILL.md
├── CHANGELOG.md
├── agents/openai.yaml
├── ref/report-contract.md        the full contract
├── scripts/build_report_drawing.py   the report drawing from ## Figures (moved from excalidraw-report)
├── scripts/check_report.py       the row reader and mechanical check
└── tests/test_haipipe_report.py
```
