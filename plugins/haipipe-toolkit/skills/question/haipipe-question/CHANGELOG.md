haipipe-question — Changelog
============================

## [0.5.1] — 2026-10-05

- One Question, one drawing (JL 261005: "for each question we should just have one
  excalidraw"; "some png can be put into the excalidraw as well"): a report links exactly one
  `.excalidraw`; more views and any picture go inside it (`excalidraw-report` 0.2.0, rules 6,
  9, 11). `ref/block_questions.py --drawing` refuses a second name.
  `servers/workbench-task/task_questions.py` keeps the first drawing and records a second
  drawing or a linked picture as a finding, for the Task and CoWork workbenches; the CoWork
  picture-thumb change of the same morning is withdrawn.
- The metadata version catches up with the 0.5.0 entry below.

## [0.4.1] — 2026-10-04

- Short questions (JL 261004: "the sentence length is too long here, hard to read at a
  glance"): `question` is one question of about 12 words, no brackets and no "done when";
  its parts and what counts as done move to `acceptance`, in short sentences
  (`ref/block-questions.md`). First applied to Project-Samsung's b13 register.

## [0.5.0] — 2026-10-04

- A report's drawings live in its own folder (JL 261004, "make this the rule"):
  `reports/qNN_<topic>/studio/<name>.excalidraw`, a script that draws one in
  `reports/qNN_<topic>/studio/_build/`. The Block's `studio/` keeps only drawings the whole
  Block shares (the question map, drawings several Questions or Jobs use).
- `ref/block_questions.py --drawing <name>` (add-question and add-report) makes the blank
  drawing there and lists it under `### Evidence`; given `--evidence` is now checked before
  anything is written. `servers/workbench-task/task_questions.py` shows a report's own
  drawings even before the report links them (Task, CoWork and Discovery workbenches).
  Test: `servers/workbench-cowork/tests/test_coworkboard.py::test_a_reports_drawing_lives_in_its_report_folder`.

## [0.4.0] — 2026-10-04

- CoWork Blocks (`board-kind: cowork-block`, haipipe-cowork) hold Questions too:
  `ref/block_questions.py` accepts them, and there `--work` names a file inside the
  Block (a ticket page, a design note). First used for Project-Samsung's
  `b01_irb` (Q01, Q02) and `b11_azure_account` (Q01 to Q03).

## [0.3.0] — 2026-10-04

- Named ids (JL 261004): a Question id may be `Q-<word>-<number>` (`Q-food-1`,
  `Q-exercise-2`) beside `Q01`; its report folder is the id in lower case
  (`q-food-1_<topic>`). `task_questions.py` (`QUESTION_ID`, `PAGE_STEM`) and the
  `block_questions.py` helper accept both; first used by b51_externalstore's register.
- `block_questions.py add-report`: frames the report of a Question already in the register
  (add-question refuses an existing id) and writes its `report:` line. `--evidence
  'label|path'` on either command lists a Block file under the frame's `### Evidence`,
  so a `studio/` drawing shows in the Task Workbench's Report column; it writes no answer
  and no `results-read:`. Test: `test_add_report_frames_a_registered_question_with_its_drawing`.
- `aim:` (JL 261004, "each question serve an aim"): an optional register line saying what
  answering the question achieves; the Task Workbench shows it under the question. A good
  entry is a slug (`title`), the full question, then the aim.

## [0.2.0] — 2026-10-03

- A topic holds asks (JL 261003): a board Question is a topic recorded here; an ask is one
  thing one piece of work answers (an Insight question file, a Run request); a topic's
  report gathers its asks' answers. Two sister skills join: `haipipe-question-asking`
  (shape an ask, eight method cards) and `haipipe-question-review` (Q1-Q7).

## [0.1.0] — 2026-10-03

- New skill, first of the `skills/question/` skillset (JL 261003: "I think question is
  very important … should I put all the question related skills into here").
- Owns what a board Question is: a topic many sections, sessions and Runs feed, that
  grows into its report (JL 261003: "it is a topic question … eventually it can develop
  the report"); five size tests and a topic/decision table, moved from response-format.
- Owns proposing and creating a question: `(proposed)` in a reply, its folder offered,
  created only on agreement (JL 261003: "propose to generate the questions folder under
  the report as well").
- `ref/block-questions.md` and `ref/block_questions.py` moved here from `haipipe-task`;
  `servers/workbench-task/taskboard.py` and every pointer in `task/` follow.
