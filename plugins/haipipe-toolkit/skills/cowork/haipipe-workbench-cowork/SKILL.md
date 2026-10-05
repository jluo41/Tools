---
name: haipipe-workbench-cowork
description: >-
  Open and interpret a CoWork Block Workbench, in the Insight Workbench's style:
  Scope (Block, People, Resources, RoadMap Draw), Work (Jobs, Questions as
  Logic │ Work │ Report rows, Emails, Meetings), Check (Waiting on, Drafts,
  Reports) and Delivery (Reports, Done jobs), each with the shared Runs panel,
  and the shared Guide. Also the Project view: every cowork Block of a Project in
  one table. Use to see who we wait on, which drafts are not sent, a Job's
  state, or a Block's Questions. The Block contract belongs to haipipe-cowork;
  report writing to haipipe-page.
metadata:
  version: "0.2.1"
  last_updated: "2026-10-04"
---

# CoWork Block Workbench

One `cowork/bNN_*/board.md` declaring `board-kind: cowork-block` opens one Workbench
(`haipipe-cowork` owns the Block). It is drawn as the Task Workbench is
(`servers/workbench-task/`, after the Insight Workbench): the title alone in the
header, the Block band, the Spaces Guide · Scope · Work · Check · Delivery, every
View opened by a heading and one lead line, and each Space's content in one box
beside its Runs panel. Guide comes from the `cowork` entry of
`workbench-shared/guide_families.py`.

## Open

Use the existing shared host; do not start another when one is running.

```text
/_board/cowork-board?path=<Block>/board.md          one Block
/w/<block-folder>                                   the same, short
/_board/cowork-board?path=<Project>/cowork          every Block of a Project
/_board/cowork-board                                every cowork Block under the root
```

The host is `<plugin>/servers/_host/serve.py`; the presenter is
`<plugin>/servers/workbench-cowork/` (`coworkboard.py` reads, `cowork_views.py`
draws). It reads the Block's files on every open and stores nothing.

## Spaces and Views

| Space › View | Contents | Source |
|---|---|---|
| Scope › Block | state, spine, close condition, status, waits-for, the Jobs with their states, board.md | `board.md` header; job pages |
| Scope › People | who to ask for help, as written | `j00_people/j00_people.md` |
| Scope › Resources | Related resources, each Job's `design/` and `materials/` files, then the OneDrive folders by name | `board.md`; Jobs; `onedrive:` |
| Scope › RoadMap Draw | the Block's drawings, each a folding row; a generated one is view only | `studio/*.excalidraw` |
| Work › Jobs | one row per open Job: state, waiting on, since, waited, next, ticket; then each Job's page, Timeline, Checklist and files | `jNN_<job>/` pages |
| Work › Questions | one row per Question: Logic │ Work (the Block files it cites) │ Report (the Opening's first paragraph, then a picture of each `.excalidraw` its Evidence links, from the `.png` beside it, opening in the pop-out) | `board.md` Questions; `reports/` |
| Work › Emails | each thread or draft across Jobs, newest first, with its Job; drafts marked | `jNN_<job>/emails/*.md` |
| Work › Meetings | each meeting note across Jobs, newest first, with its Job | `jNN_<job>/meetings/*.md` |
| Check › Waiting on | open Jobs whose move is not ours, longest wait first | job page headers |
| Check › Drafts | email drafts and open checklist steps (`- [ ]`), with their Job | `jNN_<job>/emails/`; `CHECKLIST.md` |
| Check › Reports | each report's answer status, findings and next action | report Pages |
| Delivery › Reports | answered reports, word for word | report Pages |
| Delivery › Done jobs | Jobs whose state is ✅ DONE | job page headers |

Each Space has the shared Runs panel on the right (`servers/workbench-page/runs_panel.py`),
folded at first; its run types are the rows of `ref/workbench-table.md` for that Space,
each with its agent, skill and a prompt to copy. Nothing starts a run, and nothing sends
a message: the person signs every send.

A draft is an `emails/*.md` whose name contains `draft` or whose header has
`status: draft`. Waiting days count from the job page's `since` to today.

## Boundary

The Workbench reads; `haipipe-cowork` and its agents write the Block, `haipipe-question`
the Questions, `haipipe-page` the reports. The Project view only lists Blocks and their
open Jobs; it has no registers of its own.
