---
name: haipipe-workbench-task
description: >-
  Open and interpret a question-driven Task Block Workbench, in the Insight
  Workbench's style: Scope (Block, Questions, Resources, RoadMap Draw with the
  generated question map), Task (one table per register group, a row per
  Question: Logic, Task Work, Report), Check and Delivery, each with the shared
  Runs panel, and the shared Guide with its Method page. Use for visual
  tracking across one tasks/bNN_* Block and opening its Question reports.
  Execution belongs to haipipe-task; report writing to haipipe-page.
metadata:
  version: "0.5.4"
  last_updated: "2026-10-05"
---

# Task Block Workbench

One `tasks/bNN_*/board.md` declaring `board-kind: task-block` opens one
Workbench, drawn in the Insight Workbench's style (`servers/workbench-insight/`):
the title alone in the header, the Block band, the Spaces Guide · Scope · Task ·
Check · Delivery, every View opened by a heading and one lead line, and each
Space's content in one box beside its Runs panel. Guide explains the family;
its four Views (Description, Method, RoadMap Draw, Related Paper) come from the
`task` entry of `workbench-shared/guide_families.py`. Method is the shared method
page: `ref/task-methods.excalidraw` first, then `ref/task-method.md` as fold
cards with its Run and Report method cards (`ref/methods/`); Related Paper is
`ref/task-papers.md`; RoadMap Draw opens the generated
`servers/workbench-task/studio/task-workbench-design.excalidraw`.

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

## Spaces and Views

| Space › View | Contents | Source |
|---|---|---|
| Scope › Block | The spine, close condition, Jobs and board.md, as label and value rows | `board.md` |
| Scope › Questions | The Question register: id, group, topic, question, linked Tasks | `board.md` Questions |
| Scope › Resources | Workspace data: each `_WorkSpace` folder a Job declares (`raw_store` + `cohort`, or a `_WorkSpace/` path, in `src/config-defaults.yaml`) and the Block's ProjectResult folder, its files by kind (data named and sized only; documents, figures, drawings and scripts pop out); then the Related resources and the add form | Job defaults; `board.md` Related resources |
| Scope › RoadMap Draw | The question map first (generated, view only), then freeform drawings, each a folding row | Block `studio/*.excalidraw` |
| Task › each group | One table per register `group:` (one, Questions, when there is none): a row per Question, **Logic │ Task Work │ Report** | `board.md` Questions; native Tasks; report Pages |
| Check › Runs | Every Run and its receipt status | Native Ticket/Result reader |
| Check › Tasks | Each Task Folder's run counts and audit findings | Native Task reader |
| Check › Reports | Each report's answer status, evidence warnings and next action | Same snapshot; no second progress file |
| Delivery › Reports | Each report whose `answer-status` is `answered`: its Opening and Answer word for word, its evidence and drawings | report Pages |

Each Space has the shared Runs panel on the right (`servers/workbench-page/runs_panel.py`),
folded at first as Insight's: its run types are this skill's `ref/workbench-table.md` rows
for that Space, each with its agent, skill and a prompt to copy; Task's "Run a Task" lists
every native Run with its status. Clicking a Question row (outside its links) selects it:
the Task panel narrows to that Question's Runs and names it in each prompt. The panel
starts nothing. Earlier `view=` keys still open: `task` is the first group, `studio` is
Scope › RoadMap Draw, `related-paper` is Scope › Resources, `progress` is Check › Reports.

A row follows Insight's partition table. Logic shows "Question N", the title, the
question and its aim (when the register gives one), with "What we expect" (hypothesis) and "What would answer it" (acceptance) under
a folded **More**. Task Work is one light tree, Block → Job → Task → Run, each level written
once, a Task folding its Runs and its Task Page, each opening in the shared pop-out with an
own-tab link; the fold's line counts Tasks and Runs, never their status. Report shows the
report's title (the pop-out to the Page reader), the first paragraph of its Opening, any
`.excalidraw` it links under Evidence (shown as its `.png` preview when one sits beside it,
as CoWork's, and opened read-only in the Excalidraw viewer; a picture is drawn by the
`excalidraw-report` skill), and a tag
"report qNN". A named id (`Q-food-1`) shows as itself, and a Question with no `title`
shows its question once. No status, path, Limits or Next appear in the table; Check keeps them.

Work order follows `board.md`. Optional `work[].stage` is kept for other readers; the
table does not show it, and `role` is the Task line's hover text, falling back to the
Task's Opening. Do not infer types or progress from names. One Task may support several
Questions; Tasks under no Question close the last group's table under **Not under a
Question**. Questions can be answered by reasoning or existing evidence without BJTR work.
`page.toml` explicitly registers each report. `answer-status` is the declared Question
answer; `state:` remains the Page's own state. A changed linked evidence file is flagged
for rereading without silently changing either field. This display is not a Page CHECK,
evidence certification, adoption or release.

For creating a Question, writing a Report or adding a resource, read
`../../question/haipipe-question/ref/block-questions.md` (the register, its optional
`group:`, report folders). A Question is shaped by `haipipe-question-asking` and judged by
`haipipe-question-review`; Page owns the Report writing flow. Keep report Page Folders out
of native Task iteration and BJTR counters. The resource form adds only its register
entry; it does not download a paper or execute a Discovery workflow.

## RoadMap Draw

The first row is the question map, `studio/question-map.excalidraw`, written only by
`servers/workbench-task/studio/question_map.py <block>` from the register: one frame per
group, a row per Question (Question → its Tasks with their Jobs → its report). It shows
view only and says when `board.md` is newer than it (rerun the script). The rows after it
are freeform: ideation, possible workflows, paths or other useful sketches, with no
required type or metadata. **Add drawing** opens a new native Block scene. Expanding a row
loads its viewer; **Edit drawing** takes the native editor's pen. The existing Excalidraw
lock permits one editing surface at a time. Full-screen opens the same file and obeys that
lock. No drawings or reports are created just by opening the Workbench page.

## Continue with a session

A session edits the Question register, Reports and native work through their
owning skills; a browser reload rereads them. Question/drawing folds persist in this
browser session. The page keeps Insight's shell (title, band, Space row with Guide first,
one box per Space with the Runs panel on the right), its colors, tab sizes and class
names; it adds no search or refresh controls of its own.

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
