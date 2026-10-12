haipipe-report · Changelog
==========================

## [0.2.0] · 2026-10-12 · Questions inferred from the work, at each level

- `ref/infer-reports.md`: a Task asks its own sub-questions (its report is its face); a Job, what its one Task
  of a kind answers when the Jobs differ; a Block, where the Jobs' answers differ and what that means next. A
  Question is kept only if named Tasks answer it and not all the same way (JL 261012: "I don't ask the
  questions that is meaningless"; b10 s10). Reads `haipipe-studio`'s `scripts/block_inventory.py`; worked on
  b00_rawdata (4 Block Questions, one per Job).

## [0.1.1] · 2026-10-07

- A comments batch's `<kind>` is its theme's (a paper's: review · editor · coauthor · meeting ·
  advisor, from haipipe-paper-comments); feedback · meeting · sent only where a theme has none.
- "checked" settled (b03 s21-D04): not a fourth answer state; the report Page's CHECK verdict
  shows beside answered.
- `excalidraw-report/ref/build_report_drawing.py` retired (b03 s21 phase 5).

## [0.1.0] · 2026-10-07 · New: the Question │ Work │ Report workflow (b03 s21)

- New skill (JL 261007: "I think we want to have a haipipe-report as well to define the
  question - work - report workflow in the Audience report"). It owns the row each level's
  Audience Report draws, from the Question's status rightwards; `haipipe-question` keeps the
  asking.
- `ref/report-contract.md`: the row and what each cell reads; the link rule (`answers: <id>`
  or a need `<id>.E<n>` on a Job or Task face); the walk open → partial → answered ("checked"
  left open); the report Page, moved from `haipipe-question/ref/block-questions.md` with its
  words kept; report kinds (a comments batch, b16); figures; the check; the buttons.
- `scripts/build_report_drawing.py` moved in from `excalidraw-report/ref/`, which keeps a
  shim. Its output's `source` field now names this skill.
- `scripts/check_report.py`: new, the row reader and mechanical check.
- `servers/workbench/frame.py` `_answering` reads `<id>.E<n>` as its Question.
