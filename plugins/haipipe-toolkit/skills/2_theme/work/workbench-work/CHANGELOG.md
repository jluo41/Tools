## 0.7.1 · 2026-10-07 · The board page answers at `/_board/work-board` (JL 261007)

- Every theme's board page is now `/_board/<theme>-board`, named as its theme is: this one moved from `/_board/task-board` to `/_board/work-board`. The old name still answers (serve.py renames it before any route reads it), so older links keep working; every link the server writes uses the new name.

## 0.7.0 · 2026-10-07 · Renamed to workbench-work: the task theme is the work theme (JL 261007)

- The skill is `workbench-work` (was `workbench-task`), its folder `1_base/task/workbench-work/`, its trigger `/workbench-work`; it pairs with `servers/workbench-work/` (was `servers/workbench-task/`). The level keeps its name: a `tNN_<task>/` folder is a Task in every theme. Every live reference in Tools follows; older entries below keep the old names.

## 0.6.0 · 2026-10-07 · Renamed from haipipe-workbench-task (JL 261007)

- The skill is `workbench-task` (was `haipipe-workbench-task`), its folder `task/workbench-task/`, its trigger `/workbench-task`; every live reference in Tools follows. Older entries below keep the old name.

# Changelog

## 0.5.5 · 2026-10-05 · One drawing per Question

- Report column shows a report's one drawing; a second drawing or a linked picture is a finding
  in Check (`task_questions.report_snapshot`, shared with CoWork; JL 261005).

## 0.5.4 · 2026-10-05 · Databricks receipts read truthfully

- `servers/workbench-page/runs.py`: a `.cmd` ticket is a ticket; a receipt `status: ok` (the
  Databricks runner's word) is complete; a receipt listing a non-empty `outputs:` is its
  Result when the output stays on the server by rule; a receipt whose `host` is a selftest
  reads as planned, not complete. `servers/workbench-task/taskboard.py` names `ok` in the
  receipt message. Tests: `servers/workbench-task/tests/test_run_receipts.py` (5). On
  REACH-SPACE, Check now shows b01_reach_jhu 125 complete (was 0), PD2D b00 61 complete,
  ADHD b00's 28 selftest seeds as planned.

## 0.5.3 · 2026-10-04

- Report cell: a drawing the report links under Evidence shows as its `.png` preview when
  one sits beside the `.excalidraw` (JL 261004: "they make the draw to be the preview"), as
  the CoWork workbench does; clicking it opens the drawing in the pop-out. Without a `.png`
  it stays a text link. `task_questions.py` (`png`), `task_views.py` (`.rp-thumb`),
  `90-task-workbench.css`. Test: `test_add_report_frames_a_registered_question_with_its_drawing`.
  First used by b51_externalstore, whose `studio/_build/make.sh` writes the previews.

## 0.5.2 · 2026-10-04

- `assets/js/90-task-workbench.js` reads `home` (the working Space a bare address opens,
  default `task`) and `route` (where its forms POST, default `/_board/task-board`) from
  the page config, so the CoWork Workbench reuses the script unchanged. Task pages are
  unaffected.

## 0.5.1 · 2026-10-04

- Named Question ids (JL 261004): `Q-food-1` and `Q-exercise-2` open beside `Q01` (rule
  in `servers/workbench-task/task_questions.py`, owned by `haipipe-question`); the Logic
  cell shows a named id as itself, and a Question with no `title` prints its question
  once instead of twice. Guide's Task › Report folder row matches `reports/q*_*/*.md`.
  Test: `test_named_question_ids_and_a_question_without_a_title`.
- The pop-out opens a drawing (`/_excalidraw/…`, e.g. a report's linked `.excalidraw`) with
  no referrer, as the RoadMap Draw frames and the Design and Insight pop-outs do; it showed
  Excalidraw's "I'm not a pretzel!" refusal (`assets/js/90-task-workbench.js`).
- A register `aim:` shows under the question in the Logic cell ("Aim …", `.q-aim`).

## 0.5.0 · 2026-10-03

- The page follows the Insight Workbench (the Haipipe-Insight-v5 work): the title alone in
  the header, the Spaces Guide · Scope · Task · Check · Delivery, every View opened by a
  heading and one lead line, Insight's colors, sizes and class names (`.hl` table, `.kind`,
  `.q-more`, `.bj` tree, `details.draw`, the pop box), and the Runs panel folded at first.
- Task › each group: the register's optional `group:` makes one Task View per group, each
  a table with a row per Question (Logic │ Task Work │ Report), replacing the stacked
  cards; a heading and no lead, as Insight's partition Views. Clicking a row narrows the
  Task Runs panel to that Question's Runs and names it in the prompts.
- Scope › RoadMap Draw replaces Task › Studio. Its first row is the question map, written
  only by `servers/workbench-task/studio/question_map.py` and shown view only, with a
  stale note when board.md is newer.
- Delivery › Reports: the answered reports, word for word, with their evidence.
- Guide › Method is the shared method page: `ref/task-method.md` (the eight steps, Run
  and Report methods, the tests T0 to T8, why it works, Reference), seven method cards in
  `ref/methods/`, and `ref/task-methods.excalidraw`, first drawn by
  `workbench-shared/studio/method-canvas.py`. `ref/task-papers.md` is grouped by card.
- Workbench Table: Ask a Question uses `haipipe-question-asking`, Review the questions
  `haipipe-question-review`; Draw and "Draw the question map" sit in Scope › RoadMap Draw;
  Task rows are "each group"; Delivery › Reports runs "Build the report".

## 0.4.0 · 2026-10-03

- Three working Spaces in the shared shell: Scope (Block · Questions · Resources), Task
  (Questions · Studio) and Check (Runs · Tasks · Reports), each Space's Views and content in
  one box, with the shared Runs panel on the right built from `ref/workbench-table.md`.
- The Workbench Table gains the full Task lifecycle (plan, review, build, code review, run,
  report) and report planning, after an independent review; planned skills marked `(new)`.
- `task` leaves the conformance test's RUNS_GAPS.
- The page uses the shared shell exactly as Insight, Design and Shared draw it: 📋 title with
  all boards · board index, the Block band, the Space row, `wtab` View tabs inside one box,
  Insight's colors and tab sizes; the bespoke heading, search and refresh controls are gone.
- Scope › Resources lists the _WorkSpace folders each Job declares and the Block's
  ProjectResult folder, read-only: data files named and sized, the rest in the pop-out.

## 0.3.0 · 2026-10-03

- Guide meets the shared workbench rules: a Description and a five-step Method in the
  `task` registry entry; the Workbench Table `ref/workbench-table.md` (Scope · Task ·
  Check); the Related Paper table `ref/task-papers.md` (14 papers, checked online); and a
  generated "Workbench design" drawing, `servers/workbench-task/studio/task-workbench-design.py`,
  replacing the earlier four-View design. `task` leaves the conformance test's GAPS.

## 0.2.2 · 2026-10-03

- Work follows Insight's Task Work: one light Block → Job → Task → Run tree per
  Question, each level once, Runs folded, no status.
- Report shows only the title and the Opening's first paragraph; the title opens
  the report in the same pop-out as a Run. Status stays in Progress.

## 0.2.1 · 2026-10-02

- Share Paper's Work row markup and CSS: type pill, short name, explanation,
  shared-Question tags and counts; reveal the indented native tree on expansion.
- Open a selected Run's exact Result in a pop-out. Preserve native store
  resolution, and keep Task navigation and audit details inside their fold.

## 0.2.0 · 2026-10-02

- Task Space now has Task, Roadmap Studio, Related Paper and Progress; each
  Question has side-by-side Logic / Work / Report columns.
- Reports are ordinary Block-owned Pages under `reports/`. The register and
  reports supply one snapshot for Question cards and Progress.
- Add freeform drawing rows, resource authoring, session context and source
  warnings while preserving native Task and Page ownership.

## 0.1.0 · 2026-10-02

- Introduce the read-only Task Block Workbench contract: Progress, Runs and
  Scope, using existing Job/Task folders and Ticket/Result records.
