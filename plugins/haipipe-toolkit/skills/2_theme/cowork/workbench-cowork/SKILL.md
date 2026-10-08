---
name: workbench-cowork
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
  version: "0.4.1"
  last_updated: "2026-10-07"
---

# CoWork Block Workbench

One `cowork/bNN_*/board.md` declaring `board-kind: cowork-block` opens one Workbench
(`haipipe-cowork` owns the Block). It is drawn as the Task Workbench is
(`servers/workbench-work/`, after the Insight Workbench): the title alone in the
header, the Block band, the Spaces Guide · Scope · Work · Check · Delivery, every
View opened by a heading and one lead line, and each Space's content in one box
beside its Runs panel. Guide is the theme's own, in its server folder:
`servers/workbench-cowork/guide/` (`guide.yaml`: Description and RoadMap Draw; `method.md`, its
cards in `methods/cowork/` and `methods.excalidraw`: Method) and `related/papers.md` (Related
Paper). The Workbench Table stays here, in `ref/workbench-table.md`.

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
| Work › Questions | one row per Question: Logic │ Work (the Block files it cites) │ Report (the Opening's first paragraph, then the report's one drawing as the `.png` beside it, opening in the pop-out; a second drawing or a linked picture is a finding in Check, JL 261005) | `board.md` Questions; `reports/` |
| Work › Emails | each thread or draft across Jobs, newest first, with its Job; drafts marked | `jNN_<job>/emails/*.md` |
| Work › Meetings | each meeting note across Jobs, newest first, with its Job | `jNN_<job>/meetings/*.md` |
| Check › Waiting on | open Jobs whose move is not ours, longest wait first | job page headers |
| Check › Drafts | email drafts and open checklist steps (`- [ ]`), with their Job | `jNN_<job>/emails/`; `CHECKLIST.md` |
| Check › Reports | each report's answer status, findings and next action | report Pages |
| Delivery › Reports | answered reports, word for word | report Pages |
| Delivery › Done jobs | Jobs whose state is ✅ DONE | job page headers |

Each Space has the shared Runs panel on the right (`servers/workbench/runs_panel.py`),
folded at first; its run types are the rows of `ref/workbench-table.md` for that Space,
each with its agent, skill and a prompt to copy. Nothing starts a run, and nothing sends
a message: the person signs every send.

A draft is an `emails/*.md` whose name contains `draft` or whose header has
`status: draft`. Waiting days count from the job page's `since` to today.

## On the base frame (proposed, b13 Q01)

The same Block also opens in the base frame every theme shares (`servers/workbench/frame.py`):
`/_board/workbench?path=<Block or Job folder>`. The levels are Guide · Block · Job ▾ · Task ▾, and
each level has the six Spaces Description | Idea Studio · Audience Report | Work Details | Runs ·
Delivery. `servers/workbench-cowork/cowork_theme.py` fills them; anything it leaves out is the
base's default.

| Level › Space | Third row | Contents |
|---|---|---|
| Block › Description | Scope · People · Resources · Related | the face's fields; `j00_people`; Related resources, Job files, OneDrive; `related/related.md` |
| Block › Audience Report | none | Question │ Work │ Report from the Questions register |
| Block › Work Details | All · open · waiting · done | one row per Job: state, waiting on (days), next; a row opens the Job |
| Block › Delivery | delivery/ · Reports · Done jobs | `delivery/`; answered reports; Jobs marked ✅ DONE |
| Job › Description | Job · Files | the job page header; `materials/` and `design/` |
| Job › Audience Report | none | the Block's Questions whose `work:` cites this Job |
| Job › Work Details | Timeline · Checklist · Emails · Meetings | Timeline: every dated line, email and meeting, newest first, drafts marked |

An email, a meeting or a checklist step is a row of its Job, not a Task. The Task tab stays greyed
until a Job has a `tNN_<doc>/` (a document written with others in rounds), which opens as the
base's Page Task. Idea Studio and Runs are the base's (`studio/` topics; `runs/` by run type).
Today's Check Space has no place here; where waiting-on and drafts show is b13 Q02.

## Boundary

The Workbench reads; `haipipe-cowork` and its agents write the Block, `haipipe-question`
the Questions, `haipipe-page` the reports. The Project view only lists Blocks and their
open Jobs; it has no registers of its own.
