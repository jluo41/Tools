---
name: haipipe-cowork
description: >-
  Own the CoWork Block: one coordination topic of a Project, `cowork/bNN_<topic>/`
  with its `board.md` (board-kind: cowork-block), its Jobs (`jNN_<job>/`, one line of
  work each, the state in the job page's header), its people Job `j00_people/`, its
  Questions and `reports/qNN_<topic>/`, and its `studio/`. Use to create, migrate,
  update or audit a cowork Block or Job, to record who has the next move, to place an
  email, meeting, design note or drawing, or to decide which Block or Job a piece of
  coordination belongs to. Trigger: cowork, cowork block, job, ticket, who are we
  waiting on, open a job, update a job, checklist, who to ask, /haipipe-cowork.
metadata:
  version: "0.2.1"
  last_updated: "2026-10-09"
---

# CoWork Block

`cowork/` is the Project world for coordination: requests to other offices, the
people we work with, emails, meetings, design notes and drawings. Since 2026-10-04
(JL) every coordination topic is a **Block**, the same unit a Task Block is, and the
work inside a Block is split into **Jobs** ("otherwise the work is hard to do").
`workbench-cowork` opens a Block.

```text
Project/
└── cowork/
    ├── README.md                   the map: every Block, the goal, cross-Block steps
    ├── PEOPLE.md                   the study team across Blocks, and an index
    ├── emails/ meetings/ studio/   material that serves every Block
    ├── _old/                       replaced material; do not use
    └── bNN_<topic>/                Block = CoWork Board
        ├── board.md                fixed: header, the text, the Questions register
        ├── studio/                 fixed: drawings the whole Block shares; scripts in studio/_build/
        ├── reports/qNN_<topic>/    fixed: a Question's report Page (haipipe-question); its own
        │                           drawings in reports/qNN_<topic>/studio/
        ├── _old/                   fixed: replaced material; do not use
        ├── j00_people/             who to ask for help (state 📇 REFERENCE)
        │   └── j00_people.md
        └── jNN_<job>/              one line of work, usually one request to one office
            ├── jNN_<job>.md        the job page; its header holds the Job's state
            ├── Timeline.md         the dates, one line each
            ├── CHECKLIST.md        the steps, numbered; each draft message inside its step
            └── design/ materials/ emails/ meetings/   only when the Job has them
```

No other names at a Block's top level: not `README.md` (the Block's README is its
`board.md`), `PEOPLE.md` (now `j00_people/`), `ticket/`, `design/`, `materials/`,
`emails/` or `meetings/` (they live inside a Job). There is no `tNN` level: a Job's
items are single files and nothing in cowork runs code. Work that runs code (a lab
test, a data pull) is a Task Block in the Project's `work/`; a cowork Question cites it.

## Block numbers

Ranges, the same idea as Task Blocks; each range starts at x1.

| Range | Holds | Example (Project-Samsung) |
|---|---|---|
| `b0x` | gates: approvals everything else waits for | `b01_irb` |
| `b1x` | systems we build or connect | `b11_azure_account`, `b12_epic_streaming`, `b13_smartwatch_connector` |
| `b2x` | partners and vendors | `b21_welldoc_app` |
| `b3x` | study operations: recruitment, enrollment, SOPs, site visits | `b31_patient_recruitment` |

The name after the number is lowercase words joined by `_`. A Block number never
changes once other files cite it.

## Jobs

A Job is one line of work: one request to one office (`j02_hopkins_rit4630`), one
change to file (`j02_cir_watch_app`), one stage of a process (`j03_baseline_visit`).
Number Jobs from `j01` in the order the work runs; `j00_people` is always first. A
Job's files stay with it, so one folder answers "who are we waiting on, and what did
they say".

The job page `jNN_<job>/jNN_<job>.md` (`ref/job-page-template.md`) starts with the
header the workbench reads; it is the only place the Job's state is written:

```text
# <Job title>
job-kind: cowork-job
state: 🟡 ACTIVE          🔴 OPEN · 🟡 ACTIVE · ⏸️ ON HOLD · ✅ DONE · 📇 REFERENCE
waiting-on: us            us, the person whose move it is, or nobody
since: 2026-10-02         when the current wait began
next: send the v3 diagram and the IRB wording
ticket: RIT-4630          the office's number, when it has one
url: https://jira.jh.edu/browse/RIT-4630
```

Then the text: what we asked for, why, where it stands. `Timeline.md` gets a dated
line each time something happens; `CHECKLIST.md` holds the steps (`- [ ]` open,
`- [x]` done), each message drafted inside its step. A step number never changes once
cited. Steps that span Jobs go in the Job they move most, or in `board.md`.

## board.md

`ref/block-board-template.md` is the frame:

```text
# <Title>
board-kind: cowork-block
state: 🟡 ACTIVE            🔴 OPEN · 🟡 ACTIVE · ⏸️ ON HOLD · ✅ CLOSED
owner: <initials>
spine: <one sentence: what this Block is and where it stops>
close: <what must be true for this Block to close>
status: <YYYY-MM-DD> <one line: where it stands now>
waits-for: <Block names it waits on, comma separated; optional>
onedrive: <SPACE-relative OneDrive folders of this Block, comma separated; optional>
```

Then the text (what the Block is, its Jobs and where things are), then the optional
`## Questions` register (`haipipe-question`, `ref/block-questions.md`; in a cowork Block
a Question's `work:` names files inside the Block) and `## Related resources`.

## Rules

1. **Drafts are not sent by agents.** A message is drafted in its checklist step or the
   Job's `emails/`; the person reviews and sends it. Mark a draft with `status: draft`
   on its own line, or `draft` in the file name, until it is sent.
2. **One home per file.** A ticket page, email or meeting belongs to the Job whose work
   it moves; material for every Block goes to the cowork root folders.
3. **Waiting is a field.** When the next move changes hands, update `waiting-on` and
   `since` in the job page header and add the date to the Job's `Timeline.md`.
4. **No participant data, no keys.** Git keeps history. Office files, recordings and
   anything over 5 MB stay local through `cowork/.gitignore`.
5. **Drawings are generated.** A drawing is rebuilt by its script in `studio/_build/`,
   never edited by hand.
6. **Paths are Block-relative** inside a Block (`j02_hopkins_rit4630/emails/...`) and
   Project-relative elsewhere; never `/Users/...`.

## Open the workbench

`workbench-cowork` presents one Block at `/_board/cowork-board?path=<Block>/board.md`
(short: `/w/<block-folder>`), and every Block of a Project at
`/_board/cowork-board?path=<Project>/cowork`.

## Create or migrate a Block

1. Pick the range and the next free number; make `bNN_<topic>/` with `board.md` from
   `ref/block-board-template.md` and `j00_people/j00_people.md`.
2. Make one Job per line of work from `ref/job-page-template.md`; move each file to the
   Job it serves; split a shared `Timeline.md` or checklist by Job, keeping step numbers.
3. Sweep every file that names a moved path (the Project, drawing build scripts, memory
   notes), rebuild the drawings, then run the Project audit:
   `python <haipipe-project>/scripts/audit_projects.py <Project>`.

Boundary: `haipipe-project` owns the `cowork/` world inside a Project and its audit;
`haipipe-question` owns Questions and report Pages; this skill owns the Block, its Jobs
and their folders.
