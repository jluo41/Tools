## 0.4.1 · 2026-10-07 · The Guide moves into the server folder (JL, via b02)

- `ref/cowork-method.md`, `ref/methods/cowork/`, `ref/cowork-methods.excalidraw` and
  `ref/cowork-papers.md` move to `servers/workbench-cowork/guide/` (`method.md`, `methods/cowork/`,
  `methods.excalidraw`) and `related/papers.md`; the Guide entry is `guide/guide.yaml`, and the
  `cowork` entry and `COWORK_DESIGN` leave `servers/workbench/guide_families.py`. `ref/` keeps only
  the Workbench Table; its `Tools ›` folder is now the server folder.

## 0.4.0 · 2026-10-07 · The cowork theme on the base frame (b13 Q01, proposed)

- New `servers/workbench-cowork/cowork_theme.py`: the Block and Job levels in the six Spaces of
  `/_board/workbench`; emails, meetings and checklist steps are rows of a Job's Work Details, not
  Tasks; the Task tab greyed until a Job has a `tNN_<doc>/`. Today's four-Space page is unchanged.

## 0.3.0 · 2026-10-07 · Renamed from haipipe-workbench-cowork (JL 261007)

- The skill is `workbench-cowork` (was `haipipe-workbench-cowork`), its folder `cowork/workbench-cowork/`, its trigger `/workbench-cowork`; every live reference in Tools follows. Older entries below keep the old name.

# Changelog

## 0.2.2 · 2026-10-05 · One drawing per Question

- Report column: one picture, the report's one drawing (JL 261005: "for each question we should
  just have one excalidraw"). A second drawing or a linked picture shows under Check › Reports
  as a finding; a picture belongs inside the drawing (`excalidraw-report` rule 11). Withdraws
  the same morning's picture thumbs (JL 261005, "I want to put things into the workbench"),
  which the new rule replaces.

## 0.2.1 · 2026-10-04

- Report column: a drawing the report's Evidence links (`studio/*.excalidraw`) shows as
  a picture from the `.png` beside it, at most 260px tall; a click opens the drawing in
  the shared pop-out (as in the Task Workbench), with "Open in its own tab" in its bar.
  Work paths wrap instead of running into the Report column. First used for
  Project-Samsung b13 Q03 (JL: "it is too crowded for the Q3").

## 0.2.0 · 2026-10-04

- Work › Jobs replaces Work › Tickets: one row per open Job from its page header
  (state, waiting on, since, waited, next, ticket), then each Job's page, Timeline,
  Checklist and files. Emails and Meetings list every Job's notes with a Job column;
  Check › Waiting on and Drafts read the Jobs; Delivery › Done jobs replaces Closed
  tickets; the Project view counts open Jobs.
- Scope › People reads `j00_people/j00_people.md`; a 📇 REFERENCE or ✅ DONE Job is not
  counted as open.
- Run table: "Open a job", "Update a job", "Add a person"; the method page, its cards,
  the methods drawing and the design drawing follow the Job model.
- Tests: `servers/workbench-cowork/tests/test_coworkboard.py` (6) build a Block from the
  templates and check Jobs from page headers, every View, the file reader and its
  refusals, the Project view, HTTP GET, `/w/` and the resource POST, and the audit rule.

## 0.1.0 · 2026-10-04

- New workbench `servers/workbench-cowork/` (`coworkboard.py` reads, `cowork_views.py`
  draws) at `/_board/cowork-board`, short `/w/<block>`: Spaces Guide · Scope (Block,
  People, Resources, RoadMap Draw) · Work (Tickets, Questions, Emails, Meetings) · Check
  (Waiting on, Drafts, Reports) · Delivery (Reports, Closed tickets), each with the shared
  Runs panel from `ref/workbench-table.md`. A Project view lists every Block with its open
  tickets and who we wait on.
- Reuses the Task Workbench's stylesheet and script (its `home` Space and POST `route`
  became config values) and its Question/report reader (`live.task_questions`).
- Block text files open in the pop-out through `&show=<file>`; OneDrive folders are listed
  by name only, since they sit outside the served root.
- Guide: `cowork` entry in `workbench-shared/guide_families.py`, `ref/cowork-method.md`
  (six steps), `ref/methods/cowork/` cards, `ref/cowork-methods.excalidraw`,
  `ref/cowork-papers.md` (7 papers, checked online), and the generated
  `servers/workbench-cowork/studio/cowork-workbench-design.excalidraw`.
