---
name: workbench-cowork
description: >-
  Open and interpret a CoWork Block on the shared workbench frame (the work
  shape every Block, Job and Task page takes). Use to see who we wait on, which
  drafts are not sent, a Job's state, or a Block's Questions. The older
  cowork-board page (Scope, Work, Check, Delivery) is retired and described
  only for reading old links. The Block contract belongs to haipipe-cowork.
metadata:
  version: "0.5.2"
  last_updated: "2026-10-11"
---

# CoWork Block Workbench

One `cowork/bNN_*/board.md` declaring `board-kind: cowork-block` opens one Workbench
(`haipipe-cowork` owns the Block). It opens on the shared frame every theme uses
(`servers/workbench/page/`): cowork is one of the work-shaped themes
(`focus_base.py` `WORK_SHAPE`), so its Block and Job pages read as a work page does
(`../../work/workbench-work/SKILL.md`, Current focus pages). The cowork-board page this
skill once described (Spaces Guide · Scope · Work · Check · Delivery, presenter
`servers/workbench-cowork/`) is retired: its code sits in `servers/_old/workbench-cowork/`
and its route is no longer registered. `ref/workbench-table.md` lists that page's run types.

## Open

Use the existing shared host; do not start another when one is running.

```text
/wb <Block | Job>                                   the focus page, on the running host
/w/<block-folder>                                   the same Block, short
/_board/workbench?path=<Block or Job folder>        the shared frame, full path
```

The host is `<plugin>/servers/_host/serve.py`; the page is the shared frame's
(`<plugin>/servers/workbench/page/`). It reads the Block's files on every open and stores nothing.

## Retired page: Spaces and Views

What the retired cowork-board page showed (`servers/_old/workbench-cowork/`), kept to read an old
link or an older Block, never as the page to build toward. Drawings now live in `sNN-<topic>/`
beside the Jobs and answers in those topics (`haipipe-cowork`), not in `studio/` or `reports/`.

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

Each Space has the shared Runs panel on the right (`servers/workbench/page/runs_panel.py`),
folded at first; its run types are the rows of `ref/workbench-table.md` for that Space,
each with its agent, skill and a prompt to copy. Nothing starts a run, and nothing sends
a message: the person signs every send.

A draft is an `emails/*.md` whose name contains `draft` or whose header has
`status: draft`. Waiting days count from the job page's `since` to today.

## On the shared frame

A Block opens in the frame every theme shares (`servers/workbench/page/frame.py`):
`/_board/workbench?path=<Block or Job folder>`. The levels are Guide · Block · Job ▾ · Task ▾, and
each level has the six Spaces Description | Idea Studio · Audience Report | Work Details | Runs ·
Delivery. The table below is the cowork fill `cowork_theme.py` gave them; that module is in
`servers/_old/workbench-cowork/`, so until it returns a cowork page shows the base's default.

| Level › Space | Third row | Contents |
|---|---|---|
| Block › Studio › Related (folds under the topics) | one part, folded until a Related link opens it | `related/related.md`, grouped by `related/` subfolder (`materials/`, `meetings/` …), each row opening on its file; a Word file is read in place (the frame's own view) |
| Block › Description | Scope · People · Resources | the face's fields; `j00_people`; Related resources, Job files, OneDrive |
| Block › Audience Report | none | Question │ Work │ Report from the Questions register |
| Block › Work Details | All · open · waiting · done | one row per Job: state, waiting on (days), next; a row opens the Job |
| Block › Delivery | delivery/ · Reports · Done jobs | `delivery/`; answered reports; Jobs marked ✅ DONE |
| Job › Description | Job · Files | the job page header; `materials/` and `design/` |
| Job › Audience Report | none | the Block's Questions whose `work:` cites this Job |
| Job › Work Details | Timeline · Checklist · Emails · Meetings | Timeline: every dated line, email and meeting, newest first, drafts marked |

An email, a meeting or a checklist step is a row of its Job, not a Task. The Task tab stays greyed
until a Job has a `tNN_<doc>/` (a document written with others in rounds), which opens as the
base's Page Task. Idea Studio and Runs are the base's (`sNN-<topic>/` topics; `runs/` by run type).
Today's Check Space has no place here; where waiting-on and drafts show is b13 Q02.

## Boundary

The Workbench reads; `haipipe-cowork` and its agents write the Block, `haipipe-report`
the Questions; an answer is written in its Studio topic (`haipipe-studio`). The Project view only lists Blocks and their
open Jobs; it has no registers of its own.
