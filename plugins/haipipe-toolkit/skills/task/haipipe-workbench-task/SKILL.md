---
name: haipipe-workbench-task
description: >-
  Open and interpret a question-driven Task Block Workbench: Task cards with
  Logic, Work and Report, freeform Roadmap Studio drawings, Related Paper and
  Progress. Use for visual tracking across one tasks/bNN_* Block and opening
  its Question reports. Execution belongs to haipipe-task; report writing to
  haipipe-page.
metadata:
  version: "0.4.0"
  last_updated: "2026-10-02"
---

# Task Block Workbench

One `tasks/bNN_*/board.md` declaring `board-kind: task-block` opens one
Workbench. Guide explains the family. Task Space holds this Block's work.
Guide's four Views (Description, Method, RoadMap Draw, Related Paper) come from
the `task` entry of `workbench-shared/guide_families.py`, this skill's
`ref/workbench-table.md` and `ref/task-papers.md`, and the generated
`servers/workbench-task/studio/task-workbench-design.excalidraw` ("Workbench design").
Space navigation is followed immediately by its View navigation.

## Open

Use the existing shared host at the selected SPACE, Project, tasks or Block
root. Derive the board path relative to the root:

```text
/_board/task-board?path=<block>/board.md&view=task
/w/<block-folder>
```

The short route uses the Block's basename. When names collide between
Projects, use the canonical full root-relative `path=`. A Block served as root
uses `path=board.md`. The bare endpoint opens the only Block or lists Blocks.
All URLs are origin-relative; use the running host's configured origin.
Do not start another host when the needed one is already running.

The host is `<plugin>/servers/_host/serve.py`; the presenter is
`<plugin>/servers/workbench-task/`. The full host supplies embedded Excalidraw
and its native save API. `--only task,page` supplies Questions, reports and
execution drill-downs but disables drawing routes. The shared Guide remains
available. Preserve the existing host's authentication settings.

## Four working Views

| Space › View | Contents | Source |
|---|---|---|
| Scope › Block | The spine, close condition and Jobs | `board.md` |
| Scope › Questions | The Question register: id, topic, question, linked Tasks | `board.md` Questions |
| Scope › Resources | Workspace data: each `_WorkSpace` folder a Job declares (`raw_store` + `cohort`, or a `_WorkSpace/` path, in `src/config-defaults.yaml`) and the Block's ProjectResult folder, its files by kind (data named and sized only; documents, figures, drawings and scripts pop out); then the Related resources and the add form | Job defaults; `board.md` Related resources |
| Task › Questions | Stacked collapsible Question cards; **Logic left / Task Work middle / Report right** | `board.md` Questions; native Tasks; report Pages |
| Task › Studio | One freeform drawing per collapsible row, embedded Excalidraw and full-screen editing | Block `studio/*.excalidraw` |
| Check › Runs | Every Run and its receipt status | Native Ticket/Result reader |
| Check › Tasks | Each Task Folder's run counts and audit findings | Native Task reader |
| Check › Reports | Each report's answer status, evidence warnings and next action | Same snapshot as Task; no second progress file |

Each Space has the shared Runs panel on the right (`servers/workbench-page/runs_panel.py`):
its run types are this skill's `ref/workbench-table.md` rows for that Space, each with its
agent, skill and a prompt to copy; Task's "Run a Task" lists every native Run with its
status. The panel starts nothing. Earlier `view=` keys still open: `related-paper` is
Scope › Resources and `progress` is Check › Reports.

The Work column follows Insight's Task Work: one light tree per Question,
Block → Job → Task → Run, each level written once. Jobs appear in the order the
register first names them; a Task line folds its Runs and its Task Page, and
each opens in the shared pop-out with an own-tab link. A Task line says only how many
Runs it folds; execution status belongs to Progress. `role` shows as
the Task line's hover text, falling back to the Task's Opening.

Work order follows `board.md`. Optional `work[].stage` is kept for other
readers; the tree does not show it. Do not infer types or progress from names.
One Task may support several Questions; unassigned Tasks stay under **Not under a Question**.
Questions can be answered by reasoning or existing evidence without BJTR work.
A Block with no Question register retains its existing work in that fold.

The Report column follows Insight's Report cell: the report's title, which
opens the existing Page reader for `reports/qNN_<topic>/qNN_<topic>.md` in the
same pop-out, then the first paragraph of its Opening. No status, path,
Evidence, Limits or Next are shown there; Progress keeps them. An `.excalidraw` file the report links under
Evidence is listed below the Opening and opens read-only in the shared
Excalidraw viewer, in the same pop-out; the drawing stays where its Run wrote it. `page.toml` explicitly registers each report.
`answer-status` is the declared Question
answer; `state:` remains the Page's own state. A changed linked evidence file
is flagged for rereading without silently changing either field. This display
is not a Page CHECK, evidence certification, adoption or release.

For creating a Question, writing a Report or adding a resource, read
`../haipipe-task/ref/block-questions.md`. Task owns the Block register and work
references; Page owns the Report writing flow. Keep report Page Folders out of
native Task iteration and BJTR counters. The resource form adds only its
register entry; it does not download a paper or execute a Discovery workflow.

## Freeform drawing

Names and contents are freeform: ideation, possible workflows, paths or other
useful sketches. There is no required type, Topic hierarchy or metadata form.
**Add drawing** opens a new native Block scene. Expanding an existing row
loads its viewer; **Edit drawing** takes the native editor's pen. The existing
Excalidraw lock permits one editing surface at a time. Collapsing retains its
mounted canvas; finish editing before refreshing. Full-screen opens the same
file and obeys that lock. No drawings or reports are created just by opening
the Workbench page.

## Continue with a session

A session edits the Question register, Reports and native work through their
owning skills; a browser reload rereads them. Question/drawing folds persist in this
browser session. The page keeps the shared workbench shell (title, band, Space row with
Guide first, one box per Space with the Runs panel on the right) and its colors and tab
sizes; it adds no search or refresh controls of its own.

Keep execution, Question answers and Page acceptance distinct:

- Native Run status comes from the shared Ticket/Result reader, including
  redirected Job stores. A running receipt is not a heartbeat.
- Build counts describe existing files, not a passed review. Only allocated,
  non-superseded Task Tickets enter Task completion counts; Page Runs and
  orphan Results remain visible without inflating those counts.
- Signed readings and declared execution reports never imply Folder closure.
  Closure still belongs to `haipipe-task` and its current Page gates.

Server integration and source formats are documented in
`<plugin>/servers/workbench-task/README.md`.
