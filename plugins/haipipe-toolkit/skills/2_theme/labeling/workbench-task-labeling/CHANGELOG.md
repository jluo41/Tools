# Changelog

## 0.5.0 · 2026-11-06 · Each step one closed bar; the items Task's cards as side tabs (b15 review, round 4)

- Every meaning, expression and items step is one closed section holding its flow, your sign and its prompt (a prompt
  card and notes box sat open under every closed Process bar). Under the bar, while the step waits, the first open
  question of its forms ("🙋 Items recipe choices: Q1 · The text judged"), never an instruction line.
- Items: Data's Results bar says its point ("600 rows · 30 chats · 20 raters", `task_labeling.data_point`), its tiles
  first, then its cards as side tabs, each with its state word; Items and Embedding the same. Each step's Process
  links its own Runs (r01_describe opens its card and receipt). Sign asks for no name; Embedding's button says
  "later"; "1 column"; a recipe's speakers read "speaker: Person"; its prompt is grey like its siblings'.
- Meaning: Prepare's bar says "Prepare Loop 3's report"; an answered loop shows the date its answers came back (the
  answer file's `received:` line, not the file's time on disk).
- Expression: Release's button says "released · 3 wait" while release choices wait; a done Rewrite offers the next
  round; the runs table says "24 items"; a final label's card opens its question.
- The walkthrough (Tools/blueprints/Project-Ladder/labeling/b02_labeling_walkthrough): the meaning and expression
  faces carry their titles, the meaning Aim says "the guideline and its labels", the forms were rebuilt by
  `collect.py build`, and the two drawn topics have previews (`render_png.py`).


## 0.4.0 · 2026-11-06 · Every labeling Task on the shared shape; each view's own forms last (b15 review, round 2)

- The items Task leaves the single-section layout: Data · Items · Embedding are its views on the focus page every
  level shares (path, Aim, both rails: Report · Work · Studio · Interactions · Delivery · Skills · Files), each ⚙️
  Process then 📊 Results, closed bars with their state words (`task_labeling.items_view`, `items_words`,
  `items_default`). Its Data step finds the Job's files from a host rooted inside the SPACE (`items_task.at`), so the
  Data cards' file and Draw again work there.
- 🙋 Interaction is the last section of every meaning, expression and items view, with that view's own forms
  (`labeling_steps.view_forms`, `task_labeling.item_forms`); Process no longer embeds a form, and the Preferences
  prompt reads the answers from the form in 🙋 Interaction. A step that waits on a form says so under its closed bar.
- The form route serves every labeling Task kind's forms (it gave a 404 for an items or expression Task's Answer).
- The meaning Task's second step is named Prepare; each loop box opens that loop's answered form; Update says what an
  answer changed in plain words (`rule now: …`) and shows the reference labels lNN.
- The expression Task's round boxes read their own state (e02 `released`) and open their round report; the errors
  bar counts the kinds that hold an error (`4 errors, all executor limit`); the approved-meaning line shows on Rewrite.
- No prompt shows the grey session line (Copy still carries it); no page shows who signed, only that and when.
- Tests: `test_labeling_steps.py`, `test_bar_words.py`, `test_labeling_focus.py`.

## 0.3.0 · 2026-11-06 · A state word on every bar, and what waits under it (JL 261106)

- Every numbered bar of a 🧭 meaning or 🛠 expression step carries its state word, read from the Task's files
  (`labeling_steps.bar_word`, `_map_word`, `_draws`; the shared `ui_parts._section`); a step that waits on you shows
  the one thing that waits under its closed bar. `🏷 Final labels` keeps its title; signed or not is its word.
- The items Task's steps say `✍ waits for your sign` and `→ signed, ready to run`; while the recipe or the build waits,
  the line under the step names it, and a waiting form that `feeds:` the step comes first, with its Answer button.
- A building Task's bars (`decision_report_view.section`) carry a word and the waiting line, shown while closed.
- An expression Task skips a 🙋 form (`rNN_collect_…`) when it reads its steps' Runs, so a form named `…_release_…` is
  never taken for the Release step.
- Tests: `tests/test_bar_words.py`.

## 0.2.0 · 2026-11-01

- The 🧭 meaning and 🛠 expression steps page (labeling_steps.py; b15 s58, stage 2; JL 261101: "Please make them work"): Frame · Report · Preferences · Update and Rewrite · Run · Evaluate · Release, read from the Task's files; the form route and the Approve sign; the placeholder Job (tests/labeling_example.py).

## [0.1.1] — 2026-10-26

Commands to the hidden `haipipe-labeling-*` skills now go through the door: `/haipipe-labeling <kind>`. (hide 261026)

## 0.1.0 · 2026-10-16 · New: the labeling Task's screen (JL 261016: "go ahead with workbench-task-labeling", b32 s41-D15)

- The manual of `servers/workbench-labeling/workbench-task-labeling/`: the Task's layout by type
  (`task_labeling.py`, moved out of `labeling_theme.py`), the engine's Labeling workbench (`labeling.py`) and its tab
  (`60-workbench-labeling.js`). Its sections came from `workbench-labeling` 0.32.0, unchanged in substance;
  `ref/view-structure.md` moved with them.
