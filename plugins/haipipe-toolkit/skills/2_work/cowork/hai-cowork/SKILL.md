---
name: hai-cowork
description: "Owns the CoWork Block (cowork/bNN_<topic>/): its board.md, its Jobs, its people Job j00_people/, its Questions and Studio topics. Use to create, update or audit a cowork Block or Job, or record who has the next move. Trigger: cowork, who are we waiting on, open a job, who to ask, /hai-cowork."
metadata:
  version: "0.2.3"
  last_updated: "2026-10-26"
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
        ├── board.md                fixed: header, the text, the Questions register (a Question's
        │                           report: points at the topic that answers it)
        ├── sNN-<topic>/            Studio topics beside the Jobs (hai-studio): each face has
        │                           view: under its title, and a "Q01 · Answer" part per Question
        │                           it answers; no reports/ folder (JL 261109)
        ├── related/ delivery/      what came in; what goes out
        ├── _old/                   fixed: replaced material; do not use
        ├── j00_people/             who to ask for help (state 📇 REFERENCE)
        │   └── j00_people.md
        └── jNN_<job>/              one line of work, usually one request to one office
            ├── jNN_<job>.md        the job page; its header holds the Job's state
            ├── Timeline.md         the dates, one line each
            ├── CHECKLIST.md        the steps, numbered; each draft message inside its step
            ├── design/ materials/ emails/ meetings/   only when the Job has them
            └── (delivery in Block)       delivery/jNN_<job>/<date>-<what>/
```

No other names at a Block's top level: not `README.md` (the Block's README is its
`board.md`), `PEOPLE.md` (now `j00_people/`), `ticket/`, `design/`, `materials/`,
`emails/` or `meetings/` (they live inside a Job). There is no `tNN` level: a Job's
items are single files and nothing in cowork runs code. Work that runs code (a lab
test, a data pull) is a Task Block in the Project's `work/`; a cowork Question cites it.


Delivery storage (JL 261010)
---------------------------

The rule is owned by `hai-delivery`: only the Block keeps a `delivery/`; a Job writes
`delivery/jNN_<job>/`, a Task `delivery/jNN_<job>/tNN_<task>/<lane>/`, a Report
`delivery/reports/qNN_<report>/<lane>/`, all through the `hai-draft/src/common.py` helpers.

In this skill, a Page's or Job's `delivery/<lane>/` means its source subtree
inside Block Delivery. Old local lanes are read-only migration inputs. Rebuild
from source before removing generated output; preserve a hand-owned fragment
when the source cannot reproduce it. A storage migration grants no acceptance,
release, send or submission approval.


## Block numbers

Ranges, the same idea as Task Blocks; each range starts at x1.

| Range | Holds | Example (Project-<Name>) |
|---|---|---|
| `b0x` | gates: approvals everything else waits for | `b01_irb` |
| `b1x` | systems we build or connect | `b11_cloud_account`, `b12_record_streaming`, `b13_device_connector` |
| `b2x` | partners and vendors | `b21_<partner>_app` |
| `b3x` | study operations: recruitment, enrollment, SOPs, site visits | `b31_patient_recruitment` |

The name after the number is lowercase words joined by `_`. A Block number never
changes once other files cite it.

## Jobs

A Job is one line of work: one request to one office (`j02_<office>_<ticket>`), one
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
ticket: <ID>              the office's number, when it has one
url: https://<tracker>/browse/<ID>
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
`## Questions` register (`hai-report`, `ref/block-questions.md`; in a cowork Block
a Question's `work:` names files inside the Block) and `## Related resources`.

## Rules

1. **Drafts are not sent by agents.** A message is drafted in its checklist step or the
   Job's `emails/`; one that goes out with attachments is a folder of its own,
   `<Block>/delivery/jNN_<job>/<date>-<what>/` (the draft and the files, together; JL 261009), which the
   Job's Delivery lists. `scripts/email_page.py <draft.md>` turns the draft into
   `<draft>.html`, a page with a Copy button for To, Cc, Subject and the body, so it pastes
   into Outlook with its paragraphs, numbers and bullets; the Block's `delivery/jNN_<job>/build.py`
   calls it after making the attachments. The person reviews and sends it. Mark a draft with `status: draft`
   on its own line, or `draft` in the file name, until it is sent.
2. **One home per file.** A ticket page, email or meeting belongs to the Job whose work
   it moves; material for every Block goes to the cowork root folders.
3. **Waiting is a field.** When the next move changes hands, update `waiting-on` and
   `since` in the job page header and add the date to the Job's `Timeline.md`.
4. **No participant data, no keys.** Git keeps history. Office files, recordings and
   anything over 5 MB stay local through `cowork/.gitignore`.
5. **Drawings are generated.** A studio topic follows `hai-studio`: `sNN-<topic>/` holds
   its face `.md`, its builder `build_sNN_<topic>.py` beside the drawing, and the preview.
   A drawing is never edited by hand.
7. **Answers live in topics, not reports/** (JL 261109: "we might not need the reports anymore").
   The focus page never shows a `reports/qNN_*/` page. A Question's answer, evidence and limits
   go in the face of the topic whose `**Feeds:**` names it; its board.md `report:` points at that
   face. An older Block's `reports/`: fold each page that holds an answer into its topic, drop the
   empty ones (the Question stays in board.md), then move `reports/` to `_old/reports/`.
   `hai-studio` `studio_update.py audit` lists faces with no `view:`, no `**Why:**`, or
   `**Feeds:**` still pointing at `reports/`.
6. **Paths are Block-relative** inside a Block (`j02_<office>_<ticket>/emails/...`) and
   Project-relative elsewhere; never `/Users/...`.

## Open the workbench

`/w/<block-folder>` (or `/wb <Block>`) opens a Block on the shared frame, `/_board/workbench?path=<Block>` (since
261007); a Job opens with `path=<Block>/<jNN_job>`. A cowork page takes the work shape
(`servers/workbench/page/block_index_page/focus_base.py` `WORK_SHAPE`). The older page `/_board/cowork-board` is retired: its
route is no longer registered and its code sits in `servers/_old/workbench-cowork/`.

## Create or migrate a Block

1. Pick the range and the next free number; make `bNN_<topic>/` with `board.md` from
   `ref/block-board-template.md` and `j00_people/j00_people.md`.
2. Make one Job per line of work from `ref/job-page-template.md`; move each file to the
   Job it serves; split a shared `Timeline.md` or checklist by Job, keeping step numbers.
3. Sweep every file that names a moved path (the Project, drawing build scripts, memory
   notes), rebuild the drawings, then run the Project audit:
   `python <hai-project>/scripts/audit_projects.py <Project>`.

Boundary: `hai-project` owns the `cowork/` world inside a Project and its audit;
`hai-report` owns Questions and report Pages; this skill owns the Block, its Jobs
and their folders.
