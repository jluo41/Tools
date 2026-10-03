---
name: haipipe-workbench-task
description: >-
  Open and interpret a question-driven Task Block Workbench: Task cards with
  Logic, Work and Report, freeform Roadmap Studio drawings, Related Paper and
  Progress. Use for visual tracking across one tasks/bNN_* Block and opening
  its Question reports. Execution belongs to haipipe-task; report writing to
  haipipe-page.
metadata:
  version: "0.2.1"
  last_updated: "2026-10-02"
---

# Task Block Workbench

One `tasks/bNN_*/board.md` declaring `board-kind: task-block` opens one
Workbench. Guide explains the family. Task Space holds this Block's work.
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

| View | Contents | Source |
|---|---|---|
| Task | Stacked collapsible Question cards; **Logic left / Work middle / Report right** | `board.md` Questions; native Tasks; report Pages |
| Roadmap Studio | One freeform drawing per independently collapsible row, embedded Excalidraw and full-screen editing | Block `studio/*.excalidraw` |
| Related Paper | Papers, repositories and references; contribution, notes and linked Questions | `board.md` Related resources |
| Progress | The same Reports' answers, evidence warnings, execution counts and next actions | Same snapshot as Task; no second progress file |

A Work entry follows Paper's shared presentation: a type pill and short name,
an explanation on the next line, shared-Question references and Task/Run counts.
Opening it reveals the indented Block → Job → Task → Run tree. Folder levels
are plain lines; Task disclosure opens its Runs, and a Run opens its exact
Result in a pop-out with an own-tab link. Task navigation and audit findings
stay inside **Task details**. The shared module is
`servers/workbench-shared/work_items.py`; each family keeps its source reader.

The short name is the Task Page's first `#` heading, falling back to its folder
name when no heading is present. Work order follows `board.md`.
Optional `work[].stage` supplies a display label;
otherwise use the native `task-type`, then Task. `role` supplies the explanation,
falling back to the Task's Opening. Do not infer types or progress from names.
One Task may support several Questions; unassigned Tasks stay under **Not under a Question**.
Questions can be answered by reasoning or existing evidence without BJTR work.
A Block with no Question register retains its existing work in that fold.

Report cards open the existing Page reader for
`reports/qNN_<topic>/qNN_<topic>.md`, with a Page Workbench link for writing
and evidence work. `page.toml` explicitly registers each report.
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

Use **Copy context to session** from a Question or Progress card to carry the
question, logic, native work paths, report path, current answer, limits and
next action. A session edits those source records through their owning skills;
Refresh rereads them. Question/drawing folds persist in this browser session.
Optional refresh pauses during drawing or resource editing and while a Run
result is open.

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
